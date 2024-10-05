import streamlit as st
import pandas as pd
from datetime import datetime
import openpyxl
import os
import csv

def getColumn_values(requested_worksheet, column) -> list:
    last_row = requested_worksheet.max_row
    data = []
    y = 0
    for i in reversed(range(1, last_row)):
        matrix = requested_worksheet[f'{column}{i}'].value
        if matrix != None: # and matrix != 'SKU SAP':
            y += 1
            # we could increase performance using btree or b+tree
            data.append(matrix)
    st.info(body=f'{y} of {last_row} data found: {matrix}')
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
            dfs = pd.read_html(htm_file, header=0, decimal=',')
            htm_dfs.extend(dfs)
        except Exception as e:
            print(f"Erro ao processar o arquivo {htm_file}: {e}")
    
    if htm_dfs:
        df_final = pd.concat(htm_dfs, ignore_index=True)
        df_final.to_excel(f"{full_path}.xlsx", index=False)
        print(f"Dados combinados salvos em {full_path}")
        return df_final
    else:
        print("Nenhum dado foi encontrado nos arquivos HTML.")
        return None


def depor_compare(requested, vkp2):
    print('on development')


def clean_currency(value):
    if pd.isna(value) or value == '' or value is None:
        return ''  # return empty string for missing values
    if isinstance(value, str):
        # remove thousands separator (.)
        value = value.replace('.', '')
        # replace decimal comma (,) with a period (.)
        # value = value.replace(',', '.')
    return value


def insert_comma(value):
    #if pd.isna(value) or value == '' or value is None:
    #    return ''  # treatment for empty, None, or NaN values
    value = str(value)  # remove pontos decimais, convertendo para inteiro antes
    return value[:-2] + ',' + value[-2:]  # coloca a vírgula antes dos dois últimos dígitos


def parser_csv(input: str, zerofill: bool) -> str:
    lines = [line.strip() for line in input.split()]
    
    if not zerofill:
        parsed = ', '.join(f"'{line}'" for line in lines)
    else:
        parsed = ', '.join(f"'{line.zfill(18)}'" for line in lines)
    
    return parsed