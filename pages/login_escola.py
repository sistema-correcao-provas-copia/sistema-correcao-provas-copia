import streamlit as st
from database.queries import buscar_responsavel_por_email
from database.security import verificar_senha

st.set_page_config(
    page_title="Login - Área da Escola",
    page_icon="🏫"
)

st.title("🏫 Área da Escola")
st.write("Entre com os dados da sua escola.")

email = st.text_input("E-mail")
senha = st.text_input("Senha", type="password")

if st.button("ENTRAR", use_container_width=True):
    if not email or not senha:
        st.warning("Preencha o e-mail e a senha.")
    else:
        responsavel = buscar_responsavel_por_email(email)

        if responsavel is None:
            st.error("E-mail ou senha incorretos.")
        else:
            senha_correta = verificar_senha(
                senha,
                responsavel[4]
            )

            if senha_correta:
                st.session_state["logado"] = True
                st.session_state["responsavel_id"] = responsavel[0]
                st.session_state["escola_id"] = responsavel[1]
                st.session_state["nome_responsavel"] = responsavel[2]

                st.switch_page("pages/painel_escola.py")
            else:
                st.error("E-mail ou senha incorretos.")

st.divider()

if st.button("Esqueci minha senha", use_container_width=True):
    st.switch_page("pages/esqueci_senha.py")

if st.button("CADASTRAR", use_container_width=True):
    st.switch_page("pages/cadastro_escola.py")