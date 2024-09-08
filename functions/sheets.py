import streamlit as st
import pandas as pd
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