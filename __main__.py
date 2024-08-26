import streamlit as st
import pandas as pd
import sys
import os

from sap_scripts.generate_script import create_vbs_script
from sap_scripts.run_script import run_sap_script

def main():
    st.set_page_config(page_title="Sylphie", page_icon="images\\solzinho-removebg-preview.png")
    st.title("Sylphie: automatização SAP")
    st.write("Preencha os detalhes abaixo para executar as transações no SAP.")
    st.logo('images\\logo.png')

    # Inputs do usuário
    username = st.text_input("Usuário SAP", type="password")
    password = st.text_input("Senha SAP", type="password")
    transaction = st.selectbox("Transação", ["VKP2", "SE16N", "VKPB", "VKP6", "ZSD063"])
    skus = st.text_area("SKUs (separados por vírgula)").split(",")
    store = st.text_input("Código da Loja")
    start_date = st.date_input("Data de Início")
    end_date = st.date_input("Data de Fim")
    export_path = st.text_input("Caminho de Exportação", value="C:\\Users\\zigfy\\Documents\\SAP\\SAP GUI\\")
    export_file = st.text_input("Nome do Arquivo Exportado", value="exported_data.xls")

    if st.button("Executar"):
        # Gera o arquivo VBS
        file_path = os.path.join(export_path, export_file + ".vbs")
        create_vbs_script(file_path, username, password, transaction, skus, store, start_date.strftime("%d.%m.%Y"), end_date.strftime("%d.%m.%Y"), export_path, export_file)
        run_sap_script(file_path)
        st.success("Script executado com sucesso!")

        # Verifica se o arquivo foi criado e permite ao usuário abrir o arquivo exportado
        file_to_open = os.path.join(export_path, export_file)
        if os.path.exists(file_to_open):
            st.write(f"O arquivo {file_to_open} foi encontrado.")
            if st.button("Abrir arquivo exportado"):
                try:
                    df = pd.read_excel(file_to_open)
                    st.write("Dados exportados:")
                    st.dataframe(df)
                    
                except Exception as e:
                    st.error(f"Erro ao abrir o arquivo: {e}")
        else:
            st.warning(f"O arquivo {file_to_open} não foi encontrado.")

if __name__ == "__main__":
    main()