import streamlit as st
from pages.sylphie.vkp2 import *
from pages.sylphie.pricing import *

def parser() -> str:
    st.write('parser CSV para consultas sql e super tático')
    zerofill = st.checkbox(label='zero-fill', help='completar com zeros?')
    itens = st.text_input('insira os SKUs para parsear...')
    if itens:
        parsed_itens = parser_csv(itens, zerofill)
        st.write(f"Seu texto é: {parsed_itens}")
        return parsed_itens