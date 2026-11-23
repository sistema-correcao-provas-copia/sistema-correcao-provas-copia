import streamlit as st
from database.queries import cadastrar_escola, cadastrar_responsavel

st.set_page_config(
    page_title="Cadastro da Escola",
    page_icon="🏫",
    layout="centered"
)

st.title(" Cadastro da Escola")
st.write("Preencha os dados da escola e do responsável.")

# =========================
# DADOS DA ESCOLA
# =========================

st.header(" Dados da Escola")

nome_escola = st.text_input("Nome da escola *")

codigo_inep = st.text_input("Código INEP *")

cnpj = st.text_input("CNPJ")

endereco = st.text_input("Endereço")

col1, col2 = st.columns(2)

with col1:
    cidade = st.text_input("Cidade")

with col2:
    estado = st.selectbox(
        "Estado",
        [
            "CE", "AC", "AL", "AP", "AM", "BA", "DF",
            "ES", "GO", "MA", "MT", "MS", "MG", "PA",
            "PB", "PR", "PE", "PI", "RJ", "RN", "RS",
            "RO", "RR", "SC", "SP", "SE", "TO"
        ]
    )

col3, col4 = st.columns(2)

with col3:
    telefone_escola = st.text_input("Telefone")

with col4:
    email_escola = st.text_input("E-mail institucional *")


st.divider()

# =========================
# RESPONSÁVEL
# =========================

st.header("👤 Responsável pela Escola")

nome_responsavel = st.text_input("Nome completo *")

cpf = st.text_input("CPF *")

col5, col6 = st.columns(2)

with col5:
    email_responsavel = st.text_input("E-mail do responsável *")

with col6:
    telefone_responsavel = st.text_input("Telefone do responsável")

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
if st.button("CADASTRAR ESCOLA", use_container_width=True):

    if (
        not nome_escola
        or not codigo_inep
        or not email_escola
        or not nome_responsavel
        or not cpf
        or not email_responsavel
        or not senha
        or not confirmar_senha
    ):
        st.warning("Preencha todos os campos obrigatórios (*).")

    elif senha != confirmar_senha:
        st.error("As senhas não são iguais.")

    else:
        try:
            id_escola = cadastrar_escola(
                codigo_inep,
                nome_escola,
                cnpj,
                endereco,
                cidade,
                estado,
                telefone_escola,
                email_escola
            )
            cadastrar_responsavel(
                id_escola,
                nome_responsavel,
                cpf,
                email_responsavel,
                telefone_responsavel,
                senha
            )


            st.success("Escola cadastrada com sucesso!")
            st.write("ID da escola:", id_escola)

        except Exception as erro:
            st.error("Não foi possível cadastrar a escola.")
            st.error(str(erro))