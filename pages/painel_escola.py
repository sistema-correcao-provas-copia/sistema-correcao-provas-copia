import streamlit as st


st.set_page_config(
    page_title="Painel da Escola",
    page_icon="🏫",
    layout="centered"
)


# Verificar se o usuário está logado
if not st.session_state.get("logado", False):
    st.warning("Você precisa fazer login para acessar esta página.")
    st.stop()


st.title(" Painel da Escola")

st.write(
    "Bem-vindo,",
    st.session_state.get("nome_responsavel", "")
)

st.divider()

st.subheader("Menu")

col1, col2 = st.columns(2)

with col1:

    if st.button(" Professores", use_container_width=True):
        st.switch_page("pages/cadastro_professor.py")

    if st.button(" Alunos", use_container_width=True):
        st.switch_page("pages/cadastro_aluno.py")

    if st.button(" Vincular Professor", use_container_width=True):
        st.switch_page("pages/cadastro_vinculo.py")

with col2:

    if st.button(" Turmas", use_container_width=True):
        st.switch_page("pages/cadastro_turma.py")

    if st.button(" Resultados", use_container_width=True):
        st.info("Resultados serão exibidos aqui.")

    if st.button(" Matérias", use_container_width=True):
        st.switch_page("pages/cadastro_materia.py")
        
    if st.button(" Visualizar resultados", use_container_width=True):
        st.switch_page("pages/resultados_escola.py")

st.divider()

if st.button(" Sair", use_container_width=True):
    st.session_state.clear()
    st.switch_page("app.py")