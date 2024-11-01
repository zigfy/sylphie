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

diffusion_file = r"planilhas/difusao 29.10.dsv"
products_file = r"planilhas/DE - PARA PRODUTOS - ITENS 1P.csv"

def diffusion_query():
    base = ""


def vtex_diffusion():
    # próximos passos: 1. efetuar query da difusão; pegar o centro 1950; 
    # 2. verificar os skus e preços; fazer a consulta na vtex; comparar skus e preços.
    tday = dt.date.today() # same as %Y-%d-%m
    tday_rundeck = tday.strftime('%d-%m-%Y') # Output: 28-10-2024 | use it when you extract from google storage
    tday_table = tday.strftime('%d/%m/%y') # Output: 28/10/24 | use it when you extract from Oracle
    st.write(f"Conferência de preços SAP x VTEX. Dia atual: {tday_rundeck}")
    diff_df = pd.read_csv(diffusion_file, delimiter=';', decimal=',') # diffusion dataframe
    products_df = pd.read_csv(products_file, delimiter=',') # file with the comparison of SAP vs VTEX code
    products_df = products_df.astype({'COD SAP': str, 'COD VTEX': str})
    
    ecom = sqldf(f"select * from diff_df where WERKS in ('1950') and DATA_DE IN ('{tday_table}')") # does a sqlquery on diff_df
    ecom = ecom.astype({'MATNR': str, 'WERKS': str})
    # st.write(ecom) # base diffusion dataframe
    
    # st.write('de/para produtos:')
    # st.write(products_df)
    
    found_items = []
    unfound_items = []
    
    for row in ecom.index:
        sku_sap = ecom.at[row, 'MATNR']
        sku_de = ecom.at[row, 'PRECO_ANT']
        sku_por = ecom.at[row, 'PRECO_NOVO']
        price_type = ecom.at[row, 'TIPO']
        match = products_df[products_df['COD SAP'] == sku_sap]
        
        if not match.empty:
            sku_vtex = match['COD VTEX'].values[0]
            found_items.append([sku_sap, sku_vtex, sku_de, sku_por, price_type])
        
        if match.empty:
            unfound_items.append(sku_sap)
    
    unfound_items = pd.DataFrame(unfound_items)
    
    found_items_df = pd.DataFrame(found_items, columns=['COD_SAP', 'COD_VTEX', 'PRECO_ANT', 'PRECO_NOVO', 'TIPO'])
    found_items_df = found_items_df.astype({"COD_SAP": str, "COD_VTEX": str})
    st.write("Itens encontrados na difusão para o centro 1950:")
    st.dataframe(ecom)
    
    prices_json_path = vtex_get_prices(found_items_df['COD_VTEX'].tolist())
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
        path = os.path.join(os.path.dirname(__file__), '../..', 'planilhas/diffusion', f'erros vtex {tday_rundeck}.xlsx')
        wrong_prices.to_excel(path)

    
    st.success("Itens com preço correto SAP X VTEX: ", icon=":material/verified:")
    right_prices_df = pd.DataFrame(right_prices, columns=['COD_SAP', 'COD_VTEX', 'PRECO_ANT SAP', 'PRECO_NOVO SAP', 'PRECO_DE VTEX', 'PRECO_POR VTEX'])
    st.dataframe(right_prices_df)

    # st.write(f'Preços Vigentes na VTEX no dia {tday_rundeck}')
    # st.dataframe(vtex_current_prices)
    # st.dataframe(policy_price)

    st.warning(f'itens não encontrados no de/para:', icon=":material/help:")
    st.dataframe(unfound_items)