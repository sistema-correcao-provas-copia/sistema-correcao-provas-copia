import streamlit as st

from database.queries import cadastrar_materia


st.set_page_config(
    page_title="Cadastro de Matéria",
    page_icon="📚",
    layout="centered"
)


if not st.session_state.get("logado", False):
    st.warning("Você precisa fazer login para acessar esta página.")
    st.stop()


st.title("📚 Cadastro de Matéria")

st.write("Cadastre uma matéria da sua escola.")


nome = st.text_input("Nome da matéria *")


st.divider()


if st.button(
    "CADASTRAR MATÉRIA",
    use_container_width=True
):

    if not nome:
        st.warning("Informe o nome da matéria.")

    else:

        try:

            escola_id = st.session_state["escola_id"]

            cadastrar_materia(
                escola_id,
                nome
            )

            st.success("Matéria cadastrada com sucesso!")

        except Exception as erro:

            st.error(
                "Não foi possível cadastrar a matéria."
            )

            st.error(str(erro))