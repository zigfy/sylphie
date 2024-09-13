import streamlit as st
import pandas as pd
from datetime import datetime
import openpyxl
import os

def getColumn_values(requested, column) -> list:
    last_row = requested.max_row
    data = []
    y = 0
    for i in reversed(range(1, last_row)):
        matrix = requested[f'{column}{i}'].value
        if matrix != None: # and matrix != 'SKU SAP':
            y += 1
            # we could increase performance using btree or b+tree
            data.append(matrix)
    st.write(y, "of", last_row, " data found:", matrix)
    # st.write(data)
    return data

def format_date(date_input):
    if isinstance(date_input, datetime):
        return date_input.strftime('%d.%m.%Y')
    
    possible_formats = ['%d.%m.%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']
    
    for fmt in possible_formats:
        try:
            return datetime.strptime(date_input, fmt).strftime('%d.%m.%Y')
        except ValueError:
            continue
    raise ValueError(f"Data no formato inválido: {date_input}")

def htm_toexcel(htm_files: list, full_path: str):
    htm_dfs = [] 
    for htm_file in htm_files:
        try:
            dfs = pd.read_html(htm_file, header=0)
            htm_dfs.extend(dfs)
        except Exception as e:
            print(f"Erro ao processar o arquivo {htm_file}: {e}")
    
    if htm_dfs:
    # Concatena todos os DataFrames
        df_final = pd.concat(htm_dfs, ignore_index=True)

        # Salva o DataFrame final em uma planilha Excel
        df_final.to_excel(f"{full_path}.xlsx", index=False)

        print(f"Dados combinados salvos em {full_path}")
        return df_final
    else:
        print("Nenhum dado foi encontrado nos arquivos HTML.")
        return None