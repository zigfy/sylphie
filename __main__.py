import streamlit as st
import pandas as pd
import openpyxl
import datetime
import sys
import os

from pages.sylphie.vkp2 import *
from pages.sylphie.pricing import *
from pages.sap.sap_login import login_screen
from sap_scripts.generate_script import vkp2_script
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
    st.write("Bem-vindo! Selecione a transação desejada.")

            # Caixinha de pesquisa para as transações
    transaction = st.selectbox("Transação", ["VKP2", "DataFrames", "Preços", "Parser", "SE16N", "VKP6", "ZSD063"])

    if transaction == "VKP2":
        # Mostra a tela para a transação VKP2
        vkp2_home(transaction)

    if transaction == "DataFrames":
        st.write("Reading dataframes according to the path below:")
        path = st.text_input("Insira o caminho do arquivo...")
        if st.button('abrir arquivo'):
            df = pd.read_html(path, header=0)[0]
            st.dataframe(df)

    if transaction == "Parser":
        st.write('parser CSV para consultas sql e super tático')
        itens = st.text_input('insira os SKUs para parsear...')
        def parser_csv(input):
            # Separar os valores por linha, remover espaços em branco e aspas simples
            lines = [line.strip() for line in input.split()]
            # Adicionar aspas simples em cada valor e juntar com vírgulas
            parsed = ', '.join(f"'{line}'" for line in lines)
            return parsed
        if itens:
            parsed_itens = parser_csv(itens)
            st.write(f"Seu texto é: {parsed_itens}")

    if transaction == "Preços":
        st.write("Conferência de preços para alteração...")
        alter_pricing()

main()