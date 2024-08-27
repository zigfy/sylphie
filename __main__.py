import streamlit as st
import pandas as pd
import sys
import os

from sap_scripts.generate_script import vkp2_script
from sap_scripts.run_script import run_sap_script
from pages.sap.sap_login import login_screen

def main():
    st.set_page_config(page_title="Sylphie", page_icon="images\\logo.png")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login_screen()
    else:
        app()

def app():
    st.title("Sylphie: automatização SAP")
    st.write("Bem-vindo! Selecione a transação desejada.")

            # Caixinha de pesquisa para as transações
    transaction = st.selectbox("Transação", ["VKP2", "DataFrames", "SE16N", "VKPB", "VKP6", "ZSD063"])

    if transaction == "VKP2":
                # Mostra a tela para a transação VKP2
        st.write("Preencha os detalhes para VKP2")

        username = st.text_input("Usuário SAP", type="password")
        password = st.text_input("Senha SAP", type="password")
        skus = st.text_area("SKUs (separados por vírgula)").split(",")
        store = st.text_input("Código da Loja")
        start_date = st.date_input("Data de Início")
        end_date = st.date_input("Data de Fim")
        export_path = st.text_input("Caminho de Exportação", value="C:\\Users\\{seu_usuário}\\Documents\\SAP\\SAP GUI\\")
        export_file = st.text_input("Nome do Arquivo Exportado", value="exported_data.xls")

        if st.button("Executar VKP2"):
            # Gera o arquivo VBS e executa o script
            file_path = os.path.join(export_path, export_file + ".vbs")
            vbs_file = vkp2_script(file_path, username, password, transaction, skus, store, start_date.strftime("%d.%m.%Y"), end_date.strftime("%d.%m.%Y"), export_path, export_file)
            run_sap_script(vbs_file)
            st.success("Script VKP2 executado com sucesso!")

            # Mostra opção para abrir o arquivo exportado
            file_to_open = os.path.join(export_path + export_file)
            if os.path.exists(file_to_open):
                st.write(f"O arquivo {file_to_open} foi encontrado.")
                if st.button("Abrir arquivo exportado"):
                    st.write("Dados exportados:")
                    df = pd.read_csv(file_to_open)
                    st.dataframe(df)
                    # except Exception as e:
                    #     st.error(f"Erro ao abrir o arquivo: {e}")
                    # else:
                    #     st.warning(f"O arquivo {file_to_open} não foi encontrado.")
        
        # tabel = pd.read_excel()

    #######################
    # Inputs do usuário

    # transaction = st.selectbox("Transação", ["VKP2", "SE16N", "VKPB", "VKP6", "ZSD063"])
    # skus = st.text_area("SKUs (separados por vírgula)").split(",")
    # store = st.text_input("Código da Loja")
    # start_date = st.date_input("Data de Início")
    # end_date = st.date_input("Data de Fim")
    # export_path = st.text_input("Caminho de Exportação", value="C:\\Users\\zigfy\\Documents\\SAP\\SAP GUI\\")
    # export_file = st.text_input("Nome do Arquivo Exportado", value="exported_data.xls")

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

main()