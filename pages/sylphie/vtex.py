import streamlit as st
import pandas as pd
import openpyxl
import datetime as dt
import xlsxwriter
import io
import csv
from openpyxl.utils.dataframe import dataframe_to_rows
from functions.sheets import *
from functions.vkp2_run import *
from functions.database import *
from sap_scripts.generate_script import *

def diffusion_query():
    base = ""

def vtex_diffusion():
    # próximos passos: 1. efetuar query da difusão; pegar o centro 1950; 
    # 2. verificar os skus e preços; fazer a consulta na vtex; comparar skus e preços.
    tday = dt.date.today()
    st.write(f"Conferência de preços SAP x VTEX. Dia atual: {tday}")
