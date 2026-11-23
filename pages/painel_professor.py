import streamlit as st
from database.queries import listar_turmas_materias_por_professor


st.set_page_config(
    page_title="Painel do Professor",
    page_icon="👨‍🏫",
    layout="centered"
)


if not st.session_state.get("professor_logado", False):
    st.warning(
        "Você precisa fazer login para acessar esta página."
    )
    st.stop()


st.title(" Painel do Professor")

st.write(
    "Bem-vindo,",
    st.session_state.get("nome_professor", "")
)


st.divider()


st.subheader("Menu")


col1, col2 = st.columns(2)


with col1:

    if st.button(
        " Meus Gabaritos",
        use_container_width=True
    ):
        st.switch_page("pages/cadastro_gabarito.py")


    if st.button(
        " Meus Resultados",
        use_container_width=True
    ):
        st.info("Área de resultados será criada aqui.")


with col2:

    if st.button(
        " Minhas Turmas",
        use_container_width=True
    ):
        professor_id = st.session_state["professor_id"]

        resultados = listar_turmas_materias_por_professor(
            professor_id
        )

        if not resultados:
            st.info(
                "Você ainda não possui turmas e matérias vinculadas."
            )

        else:
            st.subheader(" Minhas Turmas")

            for resultado in resultados:

                turma_id = resultado[0]
                turma_nome = resultado[1]
                materia_id = resultado[2]
                materia_nome = resultado[3]

                st.write(
                    f" **{turma_nome}** — 📚 {materia_nome}"
                )


st.divider()


if st.button(
    " Sair",
    use_container_width=True
):

    st.session_state.pop("professor_logado", None)
    st.session_state.pop("professor_id", None)
    st.session_state.pop("professor_escola_id", None)
    st.session_state.pop("nome_professor", None)

    st.switch_page("app.py")