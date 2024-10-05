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
    today = dt.date.today()
    today = today.strftime("%d/%m/%Y")
    print('conferencia de difusao de preços => pleno e vtex')
    csvf = st.file_uploader("insira o .csv do Pleno", type='csv')
    base_depor = st.file_uploader("planilha base", type='xlsx')
    if base_depor: depor_df = pd.read_excel(base_depor, sheet_name=None)
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

        st.write(tday_prices)
        st.write("tday_prices column types: ", tday_prices.dtypes)
        st.divider()
        st.write("outubro24: ", out24)
        st.write("original df column dtypes: ", out24.dtypes)
        st.download_button(label=f'Difusão {today}',
                           data=buffer,
                           file_name=f'Difusão {today}.xlsx',
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return 'difundido'