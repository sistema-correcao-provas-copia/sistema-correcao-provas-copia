import streamlit as st
import uuid
import qrcode
from io import BytesIO



from database.queries import (
    listar_vinculos_por_professor,
    cadastrar_gabarito,
    cadastrar_questao_gabarito
)


st.set_page_config(
    page_title="Cadastro de Gabarito",
    page_icon="📝",
    layout="centered"
)


# Verifica se o professor está logado
if not st.session_state.get("professor_logado", False):
    st.warning(
        "Você precisa fazer login como professor para acessar esta página."
    )
    st.stop()


st.title(" Criar Gabarito")

st.write(
    "Cadastre o gabarito de uma avaliação."
)


# Dados do professor logado
professor_id = st.session_state["professor_id"]


# Busca somente os vínculos desse professor
vinculos = listar_vinculos_por_professor(
    professor_id
)


if not vinculos:

    st.warning(
        "Você ainda não possui turmas e matérias vinculadas."
    )

    st.stop()


st.subheader("Dados da avaliação")


nome = st.text_input(
    "Nome da avaliação *",
    placeholder="Ex.: Avaliação de Matemática - 1º Bimestre"
)


# Cria as opções de turma + matéria
opcoes_vinculos = {}

for vinculo in vinculos:

    vinculo_id = vinculo[0]
    turma_id = vinculo[1]
    turma_nome = vinculo[2]
    materia_id = vinculo[3]
    materia_nome = vinculo[4]

    descricao = f"{turma_nome} — {materia_nome}"

    opcoes_vinculos[descricao] = {
        "vinculo_id": vinculo_id,
        "turma_id": turma_id,
        "materia_id": materia_id
    }


vinculo_escolhido = st.selectbox(
    "Turma e matéria *",
    opcoes_vinculos.keys()
)


dados_vinculo = opcoes_vinculos[
    vinculo_escolhido
]


quantidade_questoes = st.number_input(
    "Quantidade de questões *",
    min_value=1,
    max_value=100,
    value=10,
    step=1
)


st.divider()

st.subheader(" Gabarito das questões")

for numero in range(1, quantidade_questoes + 1):

    st.write(f"### Questão {numero}")

    col1, col2, col3 = st.columns(3)

    with col1:
        alternativa = st.selectbox(
            "Alternativa correta",
            ["A", "B", "C", "D", "E"],
            key=f"alternativa_{numero}"
        )

    with col2:
        peso = st.number_input(
            "Peso",
            min_value=0.01,
            value=1.0,
            step=0.5,
            key=f"peso_{numero}"
        )

    with col3:
        competencia = st.text_input(
            "Competência",
            placeholder="Ex.: C01",
            key=f"competencia_{numero}"
        )


if st.button(
    "CONTINUAR",
    use_container_width=True
):

    if not nome:

        st.warning(
            "Informe o nome da avaliação."
        )

    else:

        try:

            escola_id = st.session_state["professor_escola_id"]

            turma_id = dados_vinculo["turma_id"]

            materia_id = dados_vinculo["materia_id"]

            codigo_qr = str(uuid.uuid4())
            # Cria o gabarito
            id_gabarito = cadastrar_gabarito(
                escola_id,
                professor_id,
                turma_id,
                materia_id,
                nome,
                quantidade_questoes,
                codigo_qr
            )

            # Salva cada questão
            for numero in range(1, quantidade_questoes + 1):

                alternativa = st.session_state[
                    f"alternativa_{numero}"
                ]

                peso = st.session_state[
                    f"peso_{numero}"
                ]

                competencia = st.session_state[
                    f"competencia_{numero}"
                ]

                if not competencia:

                    st.warning(
                        f"Informe a competência da questão {numero}."
                    )

                    st.stop()

                cadastrar_questao_gabarito(
                    id_gabarito,
                    numero,
                    alternativa,
                    peso,
                    competencia
                )

            st.success(
                "Gabarito e questões cadastrados com sucesso!"
            )

            st.write(
                "ID do gabarito:",
                id_gabarito
            )
            qr = qrcode.make(codigo_qr)

            buffer = BytesIO()

            qr.save(buffer, format="PNG")

            st.subheader(" QR Code da avaliação")

            st.image(
                buffer.getvalue(),
                caption="QR Code do gabarito"
            )
            
        except Exception as erro:

            st.error(
                "Não foi possível criar o gabarito."
            )

            st.error(str(erro))