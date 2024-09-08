import streamlit as st
import pandas as pd
import openpyxl
import datetime
import sys
import os

from functions.sheets import *
from sap_scripts.generate_script import vkp2_script
from sap_scripts.run_script import run_sap_script
from pages.sylphie.sap_login import login_screen

def alter_pricing():
    st.write("Conferência de preços para alteração...")
    mecs = st.selectbox("Mecânica de Preço:", ['De/Por', 'De/MSRP', 'Cancelar/Prorrogar']) 
    if mecs == "De/Por":
        file = st.file_uploader("Insira a planilha de alteração", type='xlsx')
        if file is not None:
            sheet = pd.read_excel(file, skiprows=1, engine='openpyxl')
            sheet_pyxl = openpyxl.load_workbook(file)
            pyxl_names = sheet_pyxl.sheetnames
            # st.write(pyxl_names)
            requested = sheet_pyxl['Solicitados'] #worksheet pricing changer
            st.write(requested)
            file_details = {"Filename": file.name, "FileType":file.type, "Size": file.size}
            st.write(file_details)
            # st.dataframe(sheet) # just for logging
            st.write(requested['B1'].value)

            # catch all 'sku sap' column
            skus = []
            st.write("max_rows -> ",requested.max_row)
            st.write(getColumn_values(requested, column=f"B"))
            # vkp2_script(file_path, username, password, transaction, skus, store, start_date, end_date, export_path, filename)
            # do vkp2 thing
            # return the prices on an array or list or something like it