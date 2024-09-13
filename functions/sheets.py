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
