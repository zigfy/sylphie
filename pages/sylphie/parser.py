import json
import pandas as pd
import streamlit as st
from pages.sylphie.vkp2 import *
from pages.sylphie.pricing import *
from functions.database import *

def parser_sql() -> str:
    st.write('parser CSV para consultas sql e super tático')
    zerofill = st.checkbox(label='zero-fill', help='completar com zeros?')
    itens = st.text_input('insira os SKUs para parsear...')
    if itens:
        parsed_itens = parser_csv(itens, zerofill)
        st.write(f"Seu texto é: {parsed_itens}")
        return parsed_itens
    

def parser_json() -> None:
    st.write('esse utilitário permite transformar uma consulta SQL em um JSON.')
    sql = st.text_input('QUERY SQL ->')
    sql_lojas = """
    SELECT
    SAP as COD_SAP, LOJA, SHOPPING_RUA as IS_SHOPPING, SITUACAO, ENDERECO, BAIRRO, CEP, CIDADE, UF,
    CNPJ, TELEFONE_1, TELEFONE_2, TELEFONE_3, TELEFONE_4, LATITUDE, LONGITUDE,
    EMAIL_LOJA, EMAIL_REGIONAL, EMAIL_SUP
    FROM BI_DW.LOJAS
"""
    
    if sql:
        results = pd.DataFrame(data= query(sql_lojas), columns=["COD_SAP", "LOJA", "IS_SHOPPING", 'SITUACAO',
    'ENDERECO', 'BAIRRO', 'CEP', 'CIDADE', 'UF',
    'CNPJ', 'TELEFONE_1', 'TELEFONE_2', 'TELEFONE_3', 'TELEFONE_4', 'LATITUDE', 'LONGITUDE',
    'EMAIL_LOJA', 'EMAIL_REGIONAL', 'EMAIL_SUP'])
        
        results['IS_SHOPPING'] = results['IS_SHOPPING'].apply(lambda x: x.strip().upper() == "SHOPPING" if pd.notnull(x) or pd.notna(x) else False)
        results[['ENDERECO', 'NUMERO']] = results['ENDERECO'].str.split(',', n=1, expand=True)
        results['NUMERO'] = results['NUMERO'].str.strip()
        
        if not results.empty:
            lojas_dict = {
                "lojas": {
                    str(row['COD_SAP']): {
                        "COD_SAP": row['COD_SAP'],
                        "CNPJ": row.get('CNPJ', ""),
                        "ENDERECO": row.get('ENDERECO', ""),
                        "NUMERO": row.get("NUMERO", ""),
                        "CEP": row.get('CEP', ""),
                        "IS_SHOPPING": row.get('IS_SHOPPING', ""),
                        "CIDADE": row.get('CIDADE', ""),
                        "UF": row.get('UF', ""),
                        "BAIRRO": row.get('BAIRRO', ""),
                    }
                    for _, row in results.iterrows()
                }
            }
            lojas_json = json.dumps(lojas_dict, indent=2, ensure_ascii=False)
            st.json(lojas_json)
        else:
            st.write("Nenhum resultado encontrado para a consulta.")
    else:
        st.write("Digite uma consulta SQL.")
