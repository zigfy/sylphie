import streamlit as st
import pandas as pd
import openpyxl
import sys
import os

from pages.sylphie.vkp2 import *
from pages.sylphie.vtex import *
from pages.sylphie.tests import *
from pages.sylphie.parser import *
from pages.sylphie.pricing import *
from pages.sylphie.difusao import *
from pages.sylphie.products import *
from pages.sylphie.sap_login import *
from pages.sylphie.dataframes import *
from sap_scripts.generate_script import *
from sap_scripts.run_script import run_sap_script

def main():
    st.set_page_config(page_title="Sylphie", page_icon="images\\logo.png", layout="wide")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login_screen()
    else:
        app()

def app():
    st.image("images\\logo.png", width=250)
    st.write("Bem-vindo! Selecione a transação desejada.")

            # Caixinha de pesquisa para as transações
    transaction = st.selectbox("Transação", ["Difusão", "Preços", "VTEX", "Produtos - Cadastro", "VKP2", "SQL - Parser", "JSON - Parser", "DataFrames", "tests", "SE16N", "VKP6", "ZSD063"])

    if transaction == "VKP2":
        # Mostra a tela para a transação VKP2
        vkp2_home(transaction)

    if transaction == "DataFrames":
        open_dataframe()

    if transaction == "SQL - Parser":
        parser_sql()

    if transaction == "Preços":
        alter_pricing()

    if transaction == "Difusão":
        difusao()

    if transaction == "VTEX":
        vtex_diffusion()

    if transaction == "tests":
        tests()

    if transaction == "Produtos - Cadastro":
        products_info()

    if transaction == "JSON - Parser":
        parser_json()
main()