import streamlit as st
import pandas as pd
import openpyxl
import datetime as dt
import csv
from openpyxl.utils.dataframe import dataframe_to_rows
from functions.sheets import *
from sap_scripts.generate_script import *
from functions.vkp2_run import *

def difusao():
    print('conferencia de difusao de preços => pleno e vtex')
    # 1. pleno
    base_depor = st.file_uploader("planilha base", type='xlsx')
    csvf = st.text_input("insira o caminho do .csv do Pleno")
    if base_depor: xls_difusao = openpyxl.load_workbook(filename=base_depor, read_only=False)
    if csvf: tday_prices = pleno_csv(csvf)
    st.write(tday_prices)

    if st.button('Conferir'):
        if not base_depor: st.info("Você precisa enviar a planilha base para conferência do DE / POR.", icon=':material/warning:')    
    
    return 'difundido'