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
    products_df = pd.read_excel(products_file)
    st.dataframe(products_df)
    skus = products_df['COD_MATERIAL']
    skus_info = []

    for row in products_df.index:
        sku = products_df.at[row, 'COD_MATERIAL']
        skus_info.append(products_query(sku))

    st.dataframe(skus_info)