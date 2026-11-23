import streamlit as st
import pandas as pd

from database.queries import listar_resultados_por_escola


st.set_page_config(
    page_title="Resultados da Escola",
    page_icon="📊",
    layout="wide"
)


# Verificar login
if not st.session_state.get("logado", False):
    st.warning("Você precisa estar logado para acessar esta página.")
    st.stop()


escola_id = st.session_state.get("escola_id")

if escola_id is None:
    st.error("Escola não identificada.")
    st.stop()


st.title(" Resultados da Escola")

st.write(
    "Visualize os resultados das avaliações realizadas pelos alunos da escola."
)

st.divider()


# Buscar resultados
resultados = listar_resultados_por_escola(escola_id)


if not resultados:
    st.info("Ainda não existem resultados registrados para esta escola.")
    st.stop()


# Transformar em DataFrame
colunas = [
    "id",
    "aluno",
    "turma",
    "materia",
    "avaliacao",
    "acertos",
    "total_questoes",
    "nota",
    "data_correcao"
]

df = pd.DataFrame(resultados, columns=colunas)


# Filtros
st.subheader(" Filtrar resultados")

col1, col2, col3 = st.columns(3)


with col1:
    turmas = ["Todas"] + sorted(df["turma"].dropna().unique().tolist())

    turma_selecionada = st.selectbox(
        "Turma",
        turmas,
        key="filtro_turma_escola"
    )


with col2:
    materias = ["Todas"] + sorted(df["materia"].dropna().unique().tolist())

    materia_selecionada = st.selectbox(
        "Matéria",
        materias,
        key="filtro_materia_escola"
    )


with col3:
    avaliacoes = ["Todas"] + sorted(
        df["avaliacao"].dropna().unique().tolist()
    )

    avaliacao_selecionada = st.selectbox(
        "Avaliação",
        avaliacoes,
        key="filtro_avaliacao_escola"
    )


# Aplicar filtros
df_filtrado = df.copy()


if turma_selecionada != "Todas":
    df_filtrado = df_filtrado[
        df_filtrado["turma"] == turma_selecionada
    ]


if materia_selecionada != "Todas":
    df_filtrado = df_filtrado[
        df_filtrado["materia"] == materia_selecionada
    ]


if avaliacao_selecionada != "Todas":
    df_filtrado = df_filtrado[
        df_filtrado["avaliacao"] == avaliacao_selecionada
    ]


st.divider()


# Resumo
st.subheader(" Resumo dos resultados")

quantidade_resultados = len(df_filtrado)

media_notas = (
    df_filtrado["nota"].mean()
    if quantidade_resultados > 0
    else 0
)

maior_nota = (
    df_filtrado["nota"].max()
    if quantidade_resultados > 0
    else 0
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Correções encontradas",
        quantidade_resultados
    )

with col2:
    st.metric(
        "Média das notas",
        f"{media_notas:.2f}"
    )

with col3:
    st.metric(
        "Maior nota",
        f"{maior_nota:.2f}"
    )


st.divider()


# Tabela
st.subheader(" Resultados dos alunos")

if df_filtrado.empty:
    st.info("Nenhum resultado encontrado com os filtros selecionados.")
else:
    df_exibicao = df_filtrado[
        [
            "aluno",
            "turma",
            "materia",
            "avaliacao",
            "acertos",
            "total_questoes",
            "nota",
            "data_correcao"
        ]
    ].copy()

    df_exibicao.columns = [
        "Aluno",
        "Turma",
        "Matéria",
        "Avaliação",
        "Acertos",
        "Total de Questões",
        "Nota",
        "Data da Correção"
    ]

    st.dataframe(
        df_exibicao,
        use_container_width=True,
        hide_index=True
    )


st.divider()


if st.button(" Voltar ao painel da escola"):
    st.switch_page("pages/painel_escola.py")