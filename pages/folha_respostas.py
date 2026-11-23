import streamlit as st 
import qrcode 
from io import BytesIO 

from services.gerar_folha_pdf import gerar_folha_pdf
from database.queries import listar_gabaritos_por_professor

st.set_page_config(
    page_title="Folha de Respostas",
    page_icon="📝",
    layout="centered"
)


if not st.session_state.get("professor_logado", False):
    st.warning(
        "Você precisa fazer login como professor para acessar esta página."
    )
    st.stop()


st.title(" Folha de Respostas")

st.write(
    "Aqui será gerada a folha de respostas da avaliação."
)
professor_id = st.session_state["professor_id"]

gabaritos = listar_gabaritos_por_professor(
    professor_id
)

if not gabaritos:

    st.info(
        "Você ainda não possui gabaritos cadastrados."
    )

    st.stop()


st.subheader("Selecione a avaliação")

opcoes = {}

for gabarito in gabaritos:
    id_gabarito = gabarito[0]
    nome = gabarito[1]
    turma_id = gabarito[2]
    turma = gabarito[3]
    materia = gabarito[4]
    quantidade = gabarito[5]
    codigo_qr = gabarito[6]

    descricao = (
        f"{nome} — {turma} — {materia}"
    )

    opcoes[descricao] = {
        "id": id_gabarito,
        "nome": nome,
        "quantidade": quantidade,
        "codigo_qr": codigo_qr
    }


gabarito_escolhido = st.selectbox(
    "Avaliação",
    opcoes.keys()
)


dados_gabarito = opcoes[
    gabarito_escolhido
]


st.divider()

st.write(
    " **Avaliação:**",
    gabarito_escolhido
)

st.write(
    " **Quantidade de questões:**",
    dados_gabarito["quantidade"]
)

st.divider()
codigo_qr = dados_gabarito["codigo_qr"]

qr = qrcode.make(codigo_qr)

buffer = BytesIO()
qr.save(buffer, format="PNG")

st.subheader(" QR Code da avaliação")

st.image(
    buffer.getvalue(),
    caption="QR Code do gabarito" 
)

st.divider()

if st.button(
    " GERAR FOLHA DE RESPOSTAS",
    use_container_width=True
):
    st.divider()

    caminho_pdf = "folha_respostas.pdf"

    gerar_folha_pdf(
        dados_gabarito["nome"],
        gabarito_escolhido,
        dados_gabarito["quantidade"],
        dados_gabarito["codigo_qr"],
        caminho_pdf
    )

    st.success("Folha de respostas gerada com sucesso!")

    with open(caminho_pdf, "rb") as arquivo:
        pdf_bytes = arquivo.read()

    st.download_button(
        label=" BAIXAR PDF",
        data=pdf_bytes,
        file_name="folha_respostas.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.write(
        f"**Avaliação:** {nome}"
    ) 

    st.write(
        f"**Turma e matéria:** {gabarito_escolhido}"
    )

    st.write(
        f"**Quantidade de questões:** {dados_gabarito['quantidade']}"
        )

    st.subheader(" QR Code")

    st.image(
        buffer.getvalue(),
        caption="Identificação da avaliação"
    )
    st.divider()

    st.subheader(" Questões")

    for numero in range(1, dados_gabarito["quantidade"] + 1):
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.write(f"**{numero}**")

        with col2:
            st.write("⬜ A")

        with col3: 
            st.write("⬜ B")

        with col4:
            st.write("⬜ C")

        with col5:
            st.write("⬜ D")
            
        with col6:
            st.write("⬜ E")