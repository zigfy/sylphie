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

            # catch all needed columns
            st.write("max_rows -> ", requested.max_row)
            skus = getColumn_values(requested, column=f"B")
            start_date = getColumn_values(requested, column="F")
            end_date = getColumn_values(requested, column="G")
            price_policy = getColumn_values(requested, column="H")
            de_prices = getColumn_values(requested, column="I")
            por_prices = getColumn_values(requested, column="J")
            arred_prices = getColumn_values(requested, column="K")
            discount_column = ((por_prices[2] / de_prices[2]) - 1) # it needs a loop to calculate formula
            st.write(discount_column)
            st.write(requested['B1'].value, skus)
            st.write(requested['F1'].value, start_date)
            st.write(requested['G1'].value, end_date)
            st.write(requested['H1'].value, price_policy)
            st.write(requested['I1'].value, de_prices)
            st.write(requested['J1'].value, por_prices)
            st.write(requested['K1'].value, arred_prices)
            # vkp2_script(file_path, username, password, transaction, skus, store, start_date, end_date, export_path, filename)
            # do vkp2 thing
            # return the prices on an array or list or something like it