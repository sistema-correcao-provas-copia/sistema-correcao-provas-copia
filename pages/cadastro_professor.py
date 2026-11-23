import streamlit as st
from database.queries import cadastrar_professor


st.set_page_config(
    page_title="Cadastro de Professor",
    page_icon="👨‍🏫",
    layout="centered"
)


# =========================
# VERIFICAR LOGIN
# =========================

if not st.session_state.get("logado", False):
    st.warning("Você precisa fazer login para acessar esta página.")
    st.stop()


# =========================
# TÍTULO
# =========================

st.title(" Cadastro de Professor")

st.write(
    "Cadastre um professor da sua escola."
)


# =========================
# DADOS DO PROFESSOR
# =========================

nome = st.text_input("Nome completo *")

cpf = st.text_input("CPF *")

email = st.text_input("E-mail *")

telefone = st.text_input("Telefone")

senha = st.text_input(
    "Senha *",
    type="password"
)

confirmar_senha = st.text_input(
    "Confirmar senha *",
    type="password"
)


st.divider()


# =========================
# BOTÃO CADASTRAR
# =========================

if st.button("CADASTRAR PROFESSOR", use_container_width=True):

    if (
    not nome
    or not cpf
    or not email
    or not senha
    or not confirmar_senha
    ):
        st.warning("Preencha todos os campos obrigatórios (*).")

    elif senha != confirmar_senha:
        st.error("As senhas não são iguais.")

    else:
        try:

            escola_id = st.session_state["escola_id"]

            cadastrar_professor(
                escola_id,
                nome,
                cpf,
                email,
                telefone,
                senha
            )

            st.success("Professor cadastrado com sucesso!")

        except Exception as erro:
            st.error("Não foi possível cadastrar o professor.")
            st.error(str(erro))