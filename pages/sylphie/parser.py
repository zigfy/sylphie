import streamlit as st
from pages.sylphie.vkp2 import *
from pages.sylphie.pricing import *

def parser():
    st.write('parser CSV para consultas sql e super tático')
    itens = st.text_input('insira os SKUs para parsear...')
    def parser_csv(input):
        # Separar os valores por linha, remover espaços em branco e aspas simples
        lines = [line.strip() for line in input.split()]
        # Adicionar aspas simples em cada valor e juntar com vírgulas
        parsed = ', '.join(f"'{line}'" for line in lines)
        return parsed
    if itens:
        parsed_itens = parser_csv(itens)
        st.write(f"Seu texto é: {parsed_itens}")
        return parsed_itens