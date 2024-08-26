import streamlit as st

def login_screen():
    st.title("Login - Sylphie")
    st.image("images\\logo.png", width=150)

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
    # Aqui você pode adicionar a lógica de autenticação, por exemplo, validando com o SAP ou verificando contra um banco de dados
    # Para fins de teste, vamos apenas simular:
    if username == "admin" and password == "admin":
        return True
    else:
        return False
