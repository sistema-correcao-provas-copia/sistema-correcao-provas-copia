import streamlit as st
from PIL import Image
from io import BytesIO

from database.queries import (
    listar_gabaritos_por_professor,
    listar_alunos_por_turma,
    listar_questoes_por_gabarito,
    cadastrar_folha_resposta,
    cadastrar_resultado,
    cadastrar_respostas_aluno
)

from services.corrigir_respostas import corrigir_respostas
from services.leitor_folha import ler_folha

st.set_page_config(
    page_title="Corrigir Prova",
    page_icon="📝",
    layout="centered"
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

st.title("📝 Corrigir Prova")

st.write(
    "Selecione uma avaliação e depois escolha o aluno que será corrigido."
)


# ============================================================
# IDENTIFICAÇÃO DO PROFESSOR
# ============================================================

professor_id = st.session_state["professor_id"]


# ============================================================
# BUSCAR AVALIAÇÕES DO PROFESSOR
# ============================================================

gabaritos = listar_gabaritos_por_professor(
    professor_id
)


if not gabaritos:
    st.info(
        "Você ainda não possui avaliações cadastradas."
    )
    st.stop()


# ============================================================
# SELECIONAR AVALIAÇÃO
# ============================================================

st.subheader("📚 Selecione a avaliação")


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
        "turma_id": turma_id,
        "turma": turma,
        "materia": materia,
        "quantidade": quantidade,
        "codigo_qr": codigo_qr
    }


avaliacao_escolhida = st.selectbox(
    "Avaliação",
    list(opcoes.keys())
)


dados_avaliacao = opcoes[
    avaliacao_escolhida
]


# ============================================================
# GUARDAR DADOS DA AVALIAÇÃO
# ============================================================

st.session_state["gabarito_id"] = dados_avaliacao["id"]
st.session_state["nome_avaliacao"] = dados_avaliacao["nome"]
st.session_state["turma_id"] = dados_avaliacao["turma_id"]
st.session_state["quantidade_questoes"] = dados_avaliacao["quantidade"]

questoes_gabarito = listar_questoes_por_gabarito(
    dados_avaliacao["id"]
)

st.session_state["questoes_gabarito"] = questoes_gabarito

with st.expander("🔍 Visualizar gabarito carregado"):

    if questoes_gabarito:

        for questao in questoes_gabarito:

            numero = questao[0]
            alternativa = questao[1]

            st.write(
                f"Questão {numero}: alternativa correta {alternativa}"
            )

    else:

        st.warning(
            "Este gabarito ainda não possui questões cadastradas."
        )
st.divider()


# ============================================================
# INFORMAÇÕES DA AVALIAÇÃO
# ============================================================

st.subheader("📋 Informações da avaliação")

st.write(
    f"**Avaliação:** {dados_avaliacao['nome']}"
)

st.write(
    f"**Turma:** {dados_avaliacao['turma']}"
)

st.write(
    f"**Matéria:** {dados_avaliacao['materia']}"
)

st.write(
    f"**Quantidade de questões:** {dados_avaliacao['quantidade']}"
)


st.divider()


# ============================================================
# LISTAR ALUNOS DA TURMA
# ============================================================

st.subheader("👨‍🎓 Alunos da turma")


turma_id = dados_avaliacao["turma_id"]


alunos = listar_alunos_por_turma(
    turma_id
)


if not alunos:

    st.info(
        "Não existem alunos cadastrados nesta turma."
    )

else:

    for aluno in alunos:

        aluno_id = aluno[0]
        nome_aluno = aluno[1]
        matricula = aluno[2]

        if st.button(
            f"👤 {nome_aluno} — Matrícula: {matricula or 'Não informada'}",
            use_container_width=True,
            key=f"aluno_{aluno_id}"
        ):

            st.session_state["aluno_id"] = aluno_id
            st.session_state["nome_aluno"] = nome_aluno

            st.success(
                f"Aluno selecionado: {nome_aluno}"
            )


# ============================================================
# FOTOGRAFAR FOLHA
# ============================================================

if "aluno_id" in st.session_state:

    st.divider()

    st.subheader("👤 Aluno selecionado")

    st.write(
        f"**Nome:** {st.session_state['nome_aluno']}"
    )

    st.subheader("📷 Fotografar folha de respostas")

    foto = st.camera_input(
        "Tire uma foto da folha de respostas",
        resolution="1080p"
    )


    if foto is not None:

        imagem = Image.open(
            BytesIO(foto.getvalue())
        )

        st.success(
            "📸 Foto capturada com sucesso!"
        )

        st.write(
            f"📐 Resolução da foto: "
            f"{imagem.width} × {imagem.height} pixels"
        )

        st.image(
            foto,
            caption="Folha fotografada"
        )

        # Guardar a foto na sessão
        st.session_state["foto_folha"] = foto.getvalue()

        st.success(
            "Foto armazenada temporariamente para a correção."
        )

        st.divider()

        st.subheader("🤖 Leitura automática")

        st.write(
            "O sistema irá identificar automaticamente "
            "as alternativas marcadas na folha."
        )

        if st.button(
            "🔍 Ler folha e corrigir",
            type="primary",
            use_container_width=True
        ):

            quantidade_questoes = int(
                st.session_state["quantidade_questoes"]
            )

            try:

                # ------------------------------------------------
                # SALVAR A FOTO TEMPORARIAMENTE
                # ------------------------------------------------

                caminho_temporario = "folha_temp.jpg"

                with open(
                    caminho_temporario,
                    "wb"
                ) as arquivo:

                    arquivo.write(
                        st.session_state["foto_folha"]
                    )


                # ------------------------------------------------
                # LER A FOLHA
                # ------------------------------------------------

                respostas_aluno = ler_folha(
                    caminho_temporario,
                    quantidade_questoes,
                    dados_avaliacao["codigo_qr"]
                )


                # ------------------------------------------------
                # MOSTRAR RESPOSTAS DETECTADAS
                # ------------------------------------------------

                st.success(
                    "✅ Folha lida com sucesso!"
                )

                st.subheader(
                    "🔎 Respostas detectadas"
                )

                for numero in range(
                    1,
                    quantidade_questoes + 1
                ):

                    resposta = respostas_aluno.get(
                        numero
                    )

                    if resposta is None:

                        st.write(
                            f"Questão {numero}: "
                            "Não respondida"
                        )

                    else:

                        st.write(
                            f"Questão {numero}: "
                            f"**{resposta}**"
                        )


                # ------------------------------------------------
                # MONTAR O GABARITO
                # ------------------------------------------------

                gabarito = {}

                for questao in (
                    st.session_state["questoes_gabarito"]
                ):

                    numero = questao[0]
                    alternativa_correta = questao[1]

                    gabarito[numero] = (
                        alternativa_correta
                    )


                # ------------------------------------------------
                # CORRIGIR
                # ------------------------------------------------

                acertos, total, nota = (
                    corrigir_respostas(
                        gabarito,
                        respostas_aluno
                    )
                )


                # ------------------------------------------------
                # SALVAR FOLHA
                # ------------------------------------------------

                folha_resposta_id = (
                    cadastrar_folha_resposta(
                        st.session_state["gabarito_id"],
                        st.session_state["aluno_id"]
                    )
                )


                # ------------------------------------------------
                # SALVAR RESULTADO
                # ------------------------------------------------

                cadastrar_resultado(
                    folha_resposta_id,
                    acertos,
                    total,
                    nota
                )


                # ------------------------------------------------
                # SALVAR RESPOSTAS
                # ------------------------------------------------

                cadastrar_respostas_aluno(
                    folha_resposta_id,
                    respostas_aluno
                )


                # ------------------------------------------------
                # GUARDAR RESULTADO NA SESSÃO
                # ------------------------------------------------

                st.session_state[
                    "folha_resposta_id"
                ] = folha_resposta_id

                st.session_state[
                    "acertos"
                ] = acertos

                st.session_state[
                    "total_questoes"
                ] = total

                st.session_state[
                    "nota"
                ] = nota


                st.success(
                    "🎉 Prova corrigida e resultado "
                    "salvo com sucesso!"
                )


            except Exception as erro:

                st.error(
                    f"❌ Erro ao ler a folha: {erro}"
                )

                
if "nota" in st.session_state:

    st.divider()

    st.subheader("📊 Resultado da correção")

    acertos = st.session_state["acertos"]
    total = st.session_state["total_questoes"]
    nota = st.session_state["nota"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Acertos",
            acertos
        )

    with col2:
        st.metric(
            "Questões",
            total
        )

    with col3:
        st.metric(
            "Nota",
            f"{nota:.2f}"
        )
