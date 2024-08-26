import streamlit as st

def login_screen():
    st.image("images\\logo.png", width=250)
    st.title("Faça logon no SAP:")

    username = st.text_input("Usuário SAP", type="password")
    password = st.text_input("Senha SAP", type="password")
    
    login_button = st.button("Login")
    
    if login_button:
        if authenticate(username, password):
            st.success("Login bem-sucedido!")
            st.session_state['logged_in'] = True
        else:
            st.error("Usuário ou senha inválidos.")
            
def authenticate(username, password):
    # we need to create an authentication flow, probably calling ABAP function or testing against windows AD vault
    # while we are developing, the default root account is below
    if username == "admin" and password == "admin":
        return True
    else:
        return False