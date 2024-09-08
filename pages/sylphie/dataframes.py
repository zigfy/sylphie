import streamlit as st
import pandas as pd

def open_dataframe():
    st.write("Reading dataframes according to the path below:")
    path = st.text_input("Insira o caminho do arquivo...")
    if st.button('abrir arquivo'):
        df = pd.read_html(path, header=0)[0]
        st.dataframe(df)