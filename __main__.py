import streamlit as st
import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__), './sylphie/sap_scripts')))

from sap_scripts.generate_script import create_vbs_script
from sap_scripts.execute_script import run_sap_script

def main():
    st.title("Sylphie: Fase 1")
    st.write("Preencha os detalhes abaixo para executar as transações no SAP.")

    # Inputs do usuário
    username = st.text_input("Usuário SAP")
    password = st.text_input("Senha SAP", type="password")
    transaction = st.selectbox("Transação", ["VKP2", "SE16N", "VKPB", "VKP6", "ZSD063"])
    skus = st.text_area("SKUs (separados por vírgula)").split(",")
    store = st.text_input("Código da Loja")
    start_date = st.date_input("Data de Início")
    end_date = st.date_input("Data de Fim")
    export_path = st.text_input("Caminho de Exportação", value="C:\\Users\\zigfy\\Documents\\SAP\\SAP GUI")
    export_file = st.text_input("Nome do Arquivo Exportado", value="exported_data.xls")

    if st.button("Executar"):
        file_path = export_path + export_file + ".vbs"
        create_vbs_script(file_path, username, password, transaction, skus, store, start_date.strftime("%d.%m.%Y"), end_date.strftime("%d.%m.%Y"), export_path, export_file)
        run_sap_script(file_path)
        st.success("Script executado com sucesso!")

if __name__ == "__main__":
    main()