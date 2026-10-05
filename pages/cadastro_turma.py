import streamlit as st
from database.queries import cadastrar_turma


st.set_page_config(
    page_title="Cadastro de Turma",
    page_icon="🏫",
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

st.title("🏫 Cadastro de Turma")

st.write("Cadastre uma turma da sua escola.")


# =========================
# DADOS DA TURMA
# =========================

nome = st.text_input("Nome da turma *")


st.divider()


# =========================
# BOTÃO CADASTRAR
# =========================

if st.button("CADASTRAR TURMA", use_container_width=True):

    if not nome:
        st.warning("Informe o nome da turma.")

    else:
        try:

            escola_id = st.session_state["escola_id"]

            cadastrar_turma(
                escola_id,
                nome
            )

            st.success("Turma cadastrada com sucesso!")

        except Exception as erro:
            st.error("Não foi possível cadastrar a turma.")
            st.error(str(erro))