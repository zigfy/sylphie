import streamlit as st
import pandas as pd
import openpyxl
import datetime as dt
import xlsxwriter
import io
import csv
from openpyxl.utils.dataframe import dataframe_to_rows
from functions.sheets import *
from sap_scripts.generate_script import *
from functions.vkp2_run import *


def difusao():
    tday = dt.date.today()
    today = tday.strftime("%d/%m/%Y")
    date = dt.datetime(2024, 10, 4, 00, 00, 00)
    print('conferencia de difusao de preços => pleno e vtex')
    csvf = st.file_uploader("insira o .csv do Pleno", type='csv')
    base_depor = st.file_uploader("planilha base", type='xlsx')
    if base_depor: depor_df = pd.read_excel(base_depor, sheet_name=None, skiprows=1)
    if csvf: tday_prices = pd.read_csv(csvf, delimiter=',', decimal='.')
    buffer = io.BytesIO()

    if st.button('Conferir'):
        out24 = pd.read_excel(base_depor, sheet_name='Outubro24', engine='openpyxl', skiprows=2)
        print('starting merge...')
        if not base_depor: st.info("Você precisa enviar a planilha base para conferência do DE / POR.", icon=':material/warning:')
        
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            for item, df in depor_df.items():
                df.to_excel(float_format="%.2f",sheet_name=item, excel_writer=writer, engine='xlsxwriter')
            tday_prices.to_excel(float_format="%.2f", sheet_name='Pleno', excel_writer=writer, engine='xlsxwriter')
        
        new_df = openpyxl.load_workbook(buffer)
        out24 = new_df['Outubro24']
        pleno = new_df['Pleno']

        date_requested = getColumn_values(out24, column='C'),
        sku = getColumn_values(out24, 'D'),
        description = getColumn_values(out24, 'E'),
        seller = getColumn_values(out24, 'F'),
        de_price = getColumn_values(out24, 'K'),
        por_price = getColumn_values(out24, 'L'),
        start_date = getColumn_values(out24, 'N'),
        end_date = getColumn_values(out24, 'O'),
        action_num = getColumn_values(out24, 'R')

        used_colunms = {date_requested, sku, description, seller,
                        de_price, por_price, start_date, end_date, action_num}
        
        pl_sku = getColumn_values(pleno, 'B'),
        pl_description = getColumn_values(pleno, 'C'),
        pl_de_price = getColumn_values(pleno, 'G'),
        pl_por_price = getColumn_values(pleno, 'H'),
        pl_estoque = getColumn_values(pleno, 'L')

        pleno_columns = [pl_sku, pl_description,
                            pl_de_price, pl_por_price, pl_estoque]

        used_rows = []
        for row, (start, end) in enumerate(zip(start_date[1:], end_date[1:])):
            if pd.to_datetime(start).date() <= date <= pd.to_datetime(end).date():
                used_rows.append(row)
            print(row)
        print(used_rows)
        # for value in used_colunms[start_date]:
        #    if value <= today:


        # st.write(tday_prices)
        # st.write("tday_prices column types: ", tday_prices.dtypes)
        # st.divider()
        # st.write("outubro24: ", out24)
        # st.write("original df column dtypes: ", out24.dtypes)
        # st.download_button(label=f'Difusão {today}',
        #                    data=buffer,
        #                    file_name=f'Difusão {today}.xlsx',
        #                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return 'difundido'