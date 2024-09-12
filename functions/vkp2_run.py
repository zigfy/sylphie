import streamlit as st
import pandas as pd
import openpyxl
import datetime
import sys
import os

from sap_scripts.generate_script import *
from sap_scripts.run_script import run_sap_script

def vkp2_runner(username, password, transaction, skus, store, start_date, end_date, export_path, filename):
    # Gera o arquivo VBS e executa o script
    file_path = os.path.join(export_path + filename + ".vbs")
    vbs_file = cret_vkp2_script(file_path, username, password, transaction, skus, store, start_date, end_date, export_path, filename)
    run_sap_script(vbs_file)
    print('run sap foi executado...')

    # Mostra opção para abrir o arquivo exportado
    file_to_open = os.path.join(export_path + filename)
    if os.path.exists(file_to_open):
        st.write(f"O arquivo {file_to_open} foi encontrado.")
        st.write("Dados exportados:")
        df = pd.read_excel(file_to_open, header=0)[0]
        st.dataframe(df)
        if st.button("Abrir arquivo exportado"):
            try:
                df = pd.read_html(file_to_open)
                st.write("Dados exportados:")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Erro ao abrir o arquivo: {e}")
            else:
                st.warning(f"O arquivo {file_to_open} não foi encontrado.")