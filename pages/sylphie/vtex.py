import io
import csv
import numpy as np
import openpyxl
import xlsxwriter
import pandas as pd
import datetime as dt
import streamlit as st
from pandasql import sqldf
from io import StringIO
from functions.sheets import *
from functions.database import *
from functions.requests import *
from functions.vkp2_run import *
from sap_scripts.generate_script import *
from openpyxl.utils.dataframe import dataframe_to_rows


def vtex_diffusion():
    tday = dt.date.today() # same as %Y-%d-%m
    tday_rundeck = tday.strftime('%d-%m-%Y') # Output: 28-10-2024 | use it when you extract from google storage
    tday_table = tday.strftime('%d/%m/%y') # Output: 28/10/24 | use it when you extract from Oracle

    st.write(f"Conferência de preços SAP x VTEX. Dia atual: {tday_rundeck}")
    start_button = st.button("Iniciar conferência...")
    if start_button:
    # NEW CONF. METHOD ->
        # produtos = st.file_uploader(label=f"Faça o upload do arquivo de produtos atualizado.") # pode ser fixo também
        volume_difusao = fr"G:\Meu Drive\Development\sylphie\planilhas\vtex\Pricing_volume_difusao.xlsx"

        if os.path.exists(volume_difusao):
            last_modified_date = dt.date.fromtimestamp(os.path.getmtime(volume_difusao))
            print("Última data de modificação do arquivo de difusão: ", last_modified_date)
            if last_modified_date != tday:
                os.remove(volume_difusao)
                download_file(uri=f"https://storage.cloud.google.com/ri-happy-extracoes/Pricing/volume_difusao.xlsx",
                          dir=fr"G:\Meu Drive\Development\sylphie\planilhas\vtex")
            else:
                st.write(f"""O arquivo de difusão está com a data de hoje ({last_modified_date}). 
                         O download será ignorado. Continuando a conferência...""")
        else:
            download_file(uri=f"https://storage.cloud.google.com/ri-happy-extracoes/Pricing/volume_difusao.xlsx",
                          dir=fr"G:\Meu Drive\Development\sylphie\planilhas\vtex")

        products_file = fr"planilhas/produtos vtex 06.11.csv"
        # diff_df = pd.read_csv(diffusion_file, delimiter=';', decimal=',') # diffusion dataframe
        products_df = pd.read_csv(products_file, delimiter=';', decimal=',') # file with the comparison of SAP vs VTEX code
        products_df['COD SAP'] = products_df['COD SAP'].fillna(0, inplace=False).astype(int).astype(str)
        products_df['COD VTEX'] = products_df['COD VTEX'].fillna(0, inplace=False).astype(int).astype(str)
        # old ecom_df creation method -> ecom = sqldf(f"select * from diff_df where CENTRO in ('1950') and DATA_DE IN ('{tday_table}')") # does a sqlquery on diff_df
        # ecom = diffusion_query(date=tday_table, CENTRO='1950')
        ecom = pd.read_excel(volume_difusao)
        ecom = pd.DataFrame(ecom, columns=['MATERIAL', 'CENTRO', 'DATA_DE', 'DATA_ATE',
                                        'VALIDADE', 'PRECO_ANT', 'PRECO_NOVO', 'TIPO'])
        ecom['PRECO_ANT'] = ecom['PRECO_ANT'].str.replace(",", ".")
        ecom['PRECO_NOVO'] = ecom['PRECO_NOVO'].str.replace(",", ".")
        
        ecom = ecom.astype({
            'MATERIAL': str,
            'CENTRO': str,
            'DATA_DE': 'datetime64[s]',
            'DATA_ATE': 'datetime64[s]',
            'PRECO_ANT': float,
            'PRECO_NOVO': float})
        
        ecom['DATA_DE'] = pd.to_datetime(ecom['DATA_DE'], format='%d-%m-%Y', exact=True)
        ecom['DATA_ATE'] = pd.to_datetime(ecom['DATA_ATE'], format='%d-%m-%Y', exact=True)
        tday_rundeck = [tday_rundeck]
        tday_rundeck = pd.to_datetime(tday_rundeck, format='%d-%m-%Y', exact=True)
        ecom = ecom[(ecom['CENTRO'].isin(['1950'])) & (ecom[ecom['DATA_DE'].isin(tday_rundeck)])]
        ecom['DATA_DE'] = ecom['DATA_DE'].dt.strftime('%d-%m-%Y')
        ecom['DATA_ATE'] = ecom['DATA_ATE'].dt.strftime('%d-%m-%Y')
        
        found_items = []
        unfound_items = []
        invalid_rows = []

        for row in ecom.index:
            sku_sap = ecom.at[row, 'MATERIAL']
            sku_de = ecom.at[row, 'PRECO_ANT']
            sku_por = ecom.at[row, 'PRECO_NOVO']
            price_type = ecom.at[row, 'TIPO']
            match = products_df[products_df['COD SAP'] == sku_sap]

            if not match.empty:
                sku_vtex = match['COD VTEX'].values[0]
                sku_vtex = sku_vtex.lower()
                print("first if condition on line 84", sku_sap, sku_vtex, sku_de, sku_por, price_type)

                if "none" in sku_vtex:
                    print(sku_vtex, "is none on row ", row)
                    invalid_rows.append(sku_sap, sku_vtex, row)
                    sku_vtex = sku_vtex.replace("none", "")
                    print(f"after none treatment, sku_vtex on row {row} is {sku_vtex}.")
                found_items.append([sku_sap, sku_vtex, sku_de, sku_por, price_type])

            if match.empty:
                unfound_items.append(sku_sap)
        
        unfound_items = pd.DataFrame(unfound_items)
        
        found_items_df = pd.DataFrame(found_items, columns=['COD_SAP', 'COD_VTEX', 'PRECO_ANT', 'PRECO_NOVO', 'TIPO'])
        found_items_df = found_items_df.dropna(subset=['COD_VTEX'])
        found_items_df = found_items_df.astype({"COD_SAP": str, "COD_VTEX": str})
        cod_vtex_list = found_items_df['COD_VTEX'].tolist()
        cleaned_cod_vtex_list = [item for item in cod_vtex_list if item and "None" not in item]

        st.write("Itens encontrados na difusão para o centro 1950:")
        st.dataframe(ecom)
        
        prices_json_path = vtex_get_prices(cleaned_cod_vtex_list)
        base_prices, policy_price = json_to_table(prices_json_path)
        vtex_current_prices = pd.DataFrame(base_prices)
        
        right_prices = []
        wrong_prices = []
        for row in found_items_df.index:
            for line in vtex_current_prices.index:
                if vtex_current_prices.at[line, 'COD_VTEX'] == found_items_df.at[row, 'COD_VTEX']:
                    if found_items_df.at[row, 'PRECO_NOVO'] == vtex_current_prices.at[line, 'PRECO_POR']:
                        right_prices.append([found_items_df.at[row, 'COD_SAP'], found_items_df.at[row, 'COD_VTEX'], found_items_df.at[row, 'PRECO_ANT'],
                                            found_items_df.at[row, 'PRECO_NOVO'], vtex_current_prices.at[line, 'PRECO_DE'],
                                            vtex_current_prices.at[line, 'PRECO_POR']])
                    else:
                        prices = []
                        wrong_prices.append([found_items_df.at[row, 'COD_SAP'], found_items_df.at[row, 'COD_VTEX'], found_items_df.at[row, 'PRECO_ANT'],
                                            found_items_df.at[row, 'PRECO_NOVO'], vtex_current_prices.at[line, 'PRECO_DE'],
                                            vtex_current_prices.at[line, 'PRECO_POR']])
                        
        if wrong_prices:
            wrong_prices = pd.DataFrame(wrong_prices, columns=['COD_SAP', 'COD_VTEX', 'PRECO_ANT SAP', 'PRECO_NOVO SAP',
                                                                'PRECO_DE VTEX', 'PRECO_POR VTEX'])
            print(wrong_prices)
            st.warning('PREÇOS INCORRETOS ENCONTRADOS! VERIFICAR ABAIXO.', icon='🚨')
            st.dataframe(wrong_prices)
            path = os.path.join(os.path.dirname(__file__), '../..', 'planilhas/diffusion/errors', f'erros vtex {tday_rundeck}.xlsx')
            wrong_prices.to_excel(path)

        
        st.success("Itens com preço correto SAP X VTEX: ", icon=":material/verified:")
        right_prices_df = pd.DataFrame(right_prices, columns=['COD_SAP', 'COD_VTEX', 'PRECO_ANT SAP', 'PRECO_NOVO SAP', 'PRECO_DE VTEX', 'PRECO_POR VTEX'])
        st.dataframe(right_prices_df)

        # st.write(f'Preços Vigentes na VTEX no dia {tday_rundeck}')
        # st.dataframe(vtex_current_prices)
        # st.dataframe(policy_price)

        st.warning(f'itens não encontrados no de/para:', icon=":material/help:")
        st.dataframe(unfound_items)