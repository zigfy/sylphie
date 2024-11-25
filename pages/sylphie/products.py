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

def products_info():
    st.write("Informações sobre cadastro de itens.")
    products_file = fr"planilhas/cxx.xlsx"
    new_file = r"planilhas/produtos_competitividade.xlsx"
    products_df = pd.read_excel(products_file)
    products_df['COD_MATERIAL'] = products_df['COD_MATERIAL'].fillna(0).astype(int).astype(str).apply(lambda x: x.zfill(18))
    skus = products_df['COD_MATERIAL']
    skus_info = []
    st.dataframe(products_df)

    data_df = pd.DataFrame(data=query("""
SELECT COD_PRODUTO, DESC_PRODUTO, COD_EAN11, DATA_ULTATUALIZACAO, DESC_STATUS, COD_FORNECEDOR_REGULAR
FROM BI_DW.PRODUTOS
"""), columns='COD_PRODUTO, DESC_PRODUTO, COD_EAN11, DATA_ULTATUALIZACAO, DESC_STATUS, COD_FORNECEDOR_REGULAR')
    
    st.dataframe(data_df)

    #matched_values = sqldf(f"SELECT * FROM products_df LEFT JOIN data_df ON products_df.COD_MATERIAL = data_df.COD_PRODUTO", )
    #st.dataframe(matched_values)