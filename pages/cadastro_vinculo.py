import streamlit as st

from database.queries import (
    cadastrar_vinculo_professor,
    listar_professores_por_escola,
    listar_turmas_por_escola,
    listar_materias_por_escola
)


st.set_page_config(
    page_title="Vincular Professor",
    page_icon="🔗",
    layout="centered"
)


if not st.session_state.get("logado", False):
    st.warning("Você precisa fazer login para acessar esta página.")
    st.stop()


st.title(" Vincular Professor")

st.write(
    "Defina qual professor leciona determinada matéria em uma turma."
)


escola_id = st.session_state["escola_id"]


# Professores
professores = listar_professores_por_escola(escola_id)

if professores:

    opcoes_professores = {
        nome: id_professor
        for id_professor, nome in professores
    }

    professor_escolhido = st.selectbox(
        " Professor *",
        opcoes_professores.keys()
    )

    professor_id = opcoes_professores[professor_escolhido]

else:

    st.warning("Nenhum professor cadastrado.")
    professor_id = None


# Turmas
turmas = listar_turmas_por_escola(escola_id)

if turmas:

    opcoes_turmas = {
        nome: id_turma
        for id_turma, nome in turmas
    }

    turma_escolhida = st.selectbox(
        " Turma *",
        opcoes_turmas.keys()
    )

    turma_id = opcoes_turmas[turma_escolhida]

else:

    st.warning("Nenhuma turma cadastrada.")
    turma_id = None


# Matérias
materias = listar_materias_por_escola(escola_id)

if materias:

    opcoes_materias = {
        nome: id_materia
        for id_materia, nome in materias
    }

    materia_escolhida = st.selectbox(
        " Matéria *",
        opcoes_materias.keys()
    )

    materia_id = opcoes_materias[materia_escolhida]

else:

    st.warning("Nenhuma matéria cadastrada.")
    materia_id = None


st.divider()


if st.button(
    "CADASTRAR VÍNCULO",
    use_container_width=True
):

    if (
        professor_id is None
        or turma_id is None
        or materia_id is None
    ):

        st.warning(
            "É necessário ter professor, turma e matéria cadastrados."
        )

    else:

        try:

            cadastrar_vinculo_professor(
                professor_id,
                turma_id,
                materia_id
            )

            st.success(
                "Professor vinculado à turma e à matéria com sucesso!"
            )

        except Exception as erro:

            if "uq_professor_turma_materia" in str(erro):

                st.warning(
                    "Esse professor já está vinculado "
                    "a essa matéria nessa turma."
                )

            else:

                st.error(
                    "Não foi possível cadastrar o vínculo."
                )

                st.error(str(erro))