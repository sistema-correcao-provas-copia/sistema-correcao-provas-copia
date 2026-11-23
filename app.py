import streamlit as st

st.set_page_config(
    page_title="Sistema de Correção de Provas",
    page_icon="📝",
    layout="centered"
)
st.markdown("""
<style>
.barra-superior {
    background-color: #ffffff;
    padding: 15px;
    border-bottom: 1px solid #ddd;
    display: flex;
    justify-content: space-between;
}
</style>

""", unsafe_allow_html=True)

# Título
st.image("logo_oficial.PNG")
st.title("Sistema de Correção de Provas")

st.write(
    "Uma plataforma para facilitar a criação, "
    "correção e acompanhamento de avaliações."
)

st.divider()

# Informativos
st.subheader(" Informativos")

st.info(" Crie provas e cadastre seus respectivos gabaritos.")

st.info(" Utilize QR Codes para identificar as folhas de respostas.")

st.info(" Faça a correção das provas de forma rápida e organizada.")

st.info(" Acompanhe os resultados e o desempenho dos alunos.")

st.divider()

# Áreas de acesso
st.subheader("Acessar sistema")

col1, col2 = st.columns(2)

with col1:
    escola = st.button(
        " Área da Escola",
        use_container_width=True
    )

with col2:
    professor = st.button(
        " Área do Professor",
        use_container_width=True
    )

if escola:
    st.switch_page("pages/login_escola.py")

if professor:
    st.switch_page("pages/login_professor.py")