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

diffusion_file = r"planilhas/difusao 28.10.csv"
products_file = r"planilhas/DE - PARA PRODUTOS - ITENS 1P.csv"

def diffusion_query():
    base = ""


def vtex_diffusion():
    # próximos passos: 1. efetuar query da difusão; pegar o centro 1950; 
    # 2. verificar os skus e preços; fazer a consulta na vtex; comparar skus e preços.
    tday = dt.date.today() # same as %Y-%d-%m
    tday_rundeck = tday.strftime('%d-%m-%Y') # Output: 28-10-2024
    tday_table = tday.strftime('%d/%m/%y') # Output: 28/10/24
    st.write(f"Conferência de preços SAP x VTEX. Dia atual: {tday_rundeck}")
    diff_df = pd.read_csv(diffusion_file, delimiter=';', decimal=',') # diffusion dataframe
    products_df = pd.read_csv(products_file, delimiter=',') # file with the comparison of SAP vs VTEX code
    
    ecom = sqldf(f"select * from diff_df where WERKS in ('1950') and DATA_DE IN ('{tday_rundeck}')") # does a sqlquery on diff_df
    st.write(ecom)
    
    st.write('de/para produtos:')
    st.write(products_df)
    
    found_items = []
    unfound_items = []
    
    for row in ecom.index:
        sku_sap = ecom.at[row, 'MATNR']
        sku_de = ecom.at[row, 'PRECO_ANT']
        sku_por = ecom.at[row, 'PRECO_NOVO']
        match = products_df[products_df['COD SAP'] == sku_sap]
        
        if not match.empty:
            sku_vtex = match['COD VTEX'].values[0]
            found_items.append([row, sku_sap, sku_vtex, sku_de, sku_por])
        
        if match.empty:
            unfound_items.append(sku_sap)
    
    st.write(f'itens não achados no de/para: {unfound_items}')
    
    skus_df = pd.DataFrame(found_items, columns=['Row', 'SKU_SAP', 'SKU_VTEX', 'SKU_DE', 'SKU_POR'])
    st.write("Itens encontrados:")
    st.write(skus_df)
    
    vtex_prices = vtex_get_prices(skus_df['SKU_VTEX'].tolist())
    st.write(pd.read_json(vtex_prices))