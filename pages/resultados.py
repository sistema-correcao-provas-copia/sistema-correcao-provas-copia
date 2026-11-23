import streamlit as st
import pandas as pd

from database.queries import listar_resultados_por_professor


st.set_page_config(
    page_title="Resultados",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# VERIFICAÇÃO DE LOGIN
# ============================================================

if not st.session_state.get("professor_logado", False):
    st.warning(
        "Você precisa fazer login como professor para acessar esta página."
    )
    st.stop()


# ============================================================
# TÍTULO
# ============================================================

st.title(" Resultados das Correções")

st.write(
    "Consulte e filtre as notas dos alunos das avaliações vinculadas ao seu usuário."
)


professor_id = st.session_state["professor_id"]


# ============================================================
# BUSCAR RESULTADOS
# ============================================================

resultados = listar_resultados_por_professor(
    professor_id
)


if not resultados:

    st.info(
        "Nenhuma correção foi encontrada."
    )

    st.stop()


# ============================================================
# TRANSFORMAR RESULTADOS EM DATAFRAME
# ============================================================

dados = []


for resultado in resultados:

    dados.append({
        "Aluno": resultado[1],
        "Turma": resultado[2],
        "Matéria": resultado[3],
        "Avaliação": resultado[4],
        "Acertos": resultado[5],
        "Questões": resultado[6],
        "Nota": float(resultado[7]),
        "Data": resultado[8]
    })


df = pd.DataFrame(dados)


# ============================================================
# FILTROS
# ============================================================

st.subheader(" Filtros")


col1, col2, col3 = st.columns(3)


with col1:

    turmas = ["Todas"] + sorted(
        df["Turma"].dropna().unique().tolist()
    )

    turma_selecionada = st.selectbox(
        "Turma",
        turmas
    )


with col2:

    materias = ["Todas"] + sorted(
        df["Matéria"].dropna().unique().tolist()
    )

    materia_selecionada = st.selectbox(
        "Matéria",
        materias
    )


with col3:

    avaliacoes = ["Todas"] + sorted(
        df["Avaliação"].dropna().unique().tolist()
    )

    avaliacao_selecionada = st.selectbox(
        "Avaliação",
        avaliacoes
    )


# ============================================================
# APLICAR FILTROS
# ============================================================

df_filtrado = df.copy()


if turma_selecionada != "Todas":

    df_filtrado = df_filtrado[
        df_filtrado["Turma"] == turma_selecionada
    ]


if materia_selecionada != "Todas":

    df_filtrado = df_filtrado[
        df_filtrado["Matéria"] == materia_selecionada
    ]


if avaliacao_selecionada != "Todas":

    df_filtrado = df_filtrado[
        df_filtrado["Avaliação"] == avaliacao_selecionada
    ]


# ============================================================
# RESUMO
# ============================================================

st.divider()

st.subheader(" Resumo")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Correções encontradas",
        len(df_filtrado)
    )


with col2:

    if len(df_filtrado) > 0:
        media = df_filtrado["Nota"].mean()
    else:
        media = 0

    st.metric(
        "Média das notas",
        f"{media:.2f}"
    )


with col3:

    if len(df_filtrado) > 0:
        maior_nota = df_filtrado["Nota"].max()
    else:
        maior_nota = 0

    st.metric(
        "Maior nota",
        f"{maior_nota:.2f}"
    )


# ============================================================
# TABELA
# ============================================================

st.divider()

st.subheader(" Lista de resultados")


if df_filtrado.empty:

    st.warning(
        "Nenhum resultado corresponde aos filtros selecionados."
    )

else:

    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True
    )