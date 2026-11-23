import streamlit as st
from database.queries import (
    cadastrar_aluno,
    cadastrar_alunos_excel,
    listar_turmas_por_escola,
    listar_matriculas_por_escola
)
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Cadastro de Aluno",
    page_icon="👨‍🎓",
    layout="centered"
)


# =========================
# VERIFICAR LOGIN
# =========================

if not st.session_state.get("logado", False):
    st.warning("Você precisa fazer login para acessar esta página.")
    st.stop()


# =========================
# TÍTULO
# =========================

st.title(" Cadastro de Aluno")

st.write("Cadastre um aluno da sua escola.")



# =========================
# ESCOLHA DO CADASTRO
# =========================

st.subheader("Como deseja cadastrar os alunos?")

opcao = st.radio(
    "Escolha uma opção:",
    [
        " Cadastrar aluno individualmente",
        "➕ Importar alunos por Excel"
    ],
    key="opcao_cadastro_aluno"
)


# =========================
# CADASTRO INDIVIDUAL
# =========================

if opcao == "➕ Cadastrar aluno individualmente":

    st.subheader("Dados do aluno")

    nome = st.text_input("Nome completo *")

    matricula = st.text_input("Matrícula")

    st.subheader("Turma")

    escola_id = st.session_state["escola_id"]

    turmas = listar_turmas_por_escola(escola_id)

    if turmas:

        opcoes_turmas = {
            nome: id_turma
            for id_turma, nome in turmas
        }

        turma_escolhida = st.selectbox(
            "Selecione a turma *",
            opcoes_turmas.keys()
        )

        turma_id = opcoes_turmas[turma_escolhida]

    else:

        st.warning("Nenhuma turma cadastrada.")
        turma_id = None

    st.divider()

    if st.button(
        "CADASTRAR ALUNO",
        use_container_width=True
    ):

        if not nome:

            st.warning("Informe o nome do aluno.")

        elif turma_id is None:

            st.warning("Selecione uma turma.")

        else:

            try:

                cadastrar_aluno(
                    escola_id,
                    turma_id,
                    nome,
                    matricula
                )

                st.success(
                    "Aluno cadastrado com sucesso!"
                )

            except Exception as erro:

                if "aluno_escola_matricula_unique" in str(erro):

                    st.warning(
                        " Já existe um aluno com essa matrícula nesta escola."
                    )

                else:

                    st.error(
                        "Não foi possível cadastrar o aluno."
                    )


# =========================
# IMPORTAÇÃO POR EXCEL
# =========================

else:

    st.subheader("Importar alunos por Excel")

    st.write(
        "Baixe o modelo, preencha os alunos e depois envie o arquivo."
    )

    # Criar modelo do Excel

    dados_modelo = {
        "Nome do aluno": [],
        "Matrícula": [],
        "Turma": []
    }

    df_modelo = pd.DataFrame(dados_modelo)

    memoria = BytesIO()

    df_modelo.to_excel(
        memoria,
        index=False,
        engine="openpyxl"
    )

    memoria.seek(0)

    # Botão para baixar o modelo

    st.download_button(
        label=" Baixar modelo Excel",
        data=memoria,
        file_name="modelo_alunos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    st.divider()

    # Enviar Excel preenchido
    arquivo_enviado = st.file_uploader(
        " Envie o arquivo Excel preenchido",
        type=["xlsx"]
    )

    if arquivo_enviado is not None:

        df_alunos = pd.read_excel(
            arquivo_enviado
        )

        colunas_obrigatorias = [
            "Nome do aluno",
            "Matrícula",
            "Turma"
        ]

        # =========================
        # VERIFICAR COLUNAS
        # =========================

        if not all(
            coluna in df_alunos.columns
            for coluna in colunas_obrigatorias
        ):

            st.error(
                "O Excel não está no formato correto."
            )

            st.write(
                "As colunas devem ser: "
                "Nome do aluno, Matrícula e Turma."
            )

        else:

            st.success(
                "Excel está no formato correto!"
            )

            # =========================
            # VERIFICAR CAMPOS VAZIOS
            # =========================

            nomes_vazios = (
                df_alunos["Nome do aluno"]
                .isna()
                .sum()
            )

            turmas_vazias = (
                df_alunos["Turma"]
                .isna()
                .sum()
            )


            if nomes_vazios > 0:

                st.error(
                    f"Existem {nomes_vazios} aluno(s) sem nome."
                )

            elif turmas_vazias > 0:

                st.error(
                    f"Existem {turmas_vazias} aluno(s) sem turma."
                )

            else:

                # =========================
                # VERIFICAR MATRÍCULAS REPETIDAS
                # =========================

                matriculas_repetidas = (
                    df_alunos["Matrícula"]
                    .dropna()
                    .duplicated()
                )

                if matriculas_repetidas.any():

                    st.error(
                        "Existem matrículas repetidas no Excel."
                    )

                    matriculas = (
                        df_alunos.loc[
                            matriculas_repetidas,
                            "Matrícula"
                        ]
                        .tolist()
                    )

                    st.write("Matrículas repetidas:")

                    for matricula in matriculas:

                        st.write(
                            f" {matricula}"
                        )


                # =========================
                # VERIFICAR MATRÍCULAS JÁ CADASTRADAS
                # =========================

                escola_id = st.session_state["escola_id"]

                matriculas_banco = listar_matriculas_por_escola(
                    escola_id
                )

                matriculas_banco = [
                    matricula[0]
                    for matricula in matriculas_banco
                ]

                matriculas_excel = (
                    df_alunos["Matrícula"]
                    .dropna()
                    .astype(str)
                    .tolist()
                )

                matriculas_existentes = [
                    matricula
                    for matricula in matriculas_excel
                    if matricula in matriculas_banco
                ]

                if matriculas_existentes:

                    st.error(
                        "Existem alunos no Excel que já estão cadastrados."
                    )

                    st.write("Matrículas já cadastradas:")

                    for matricula in matriculas_existentes:

                        st.write(
                            f" {matricula}"
                        )


                else:


                        
                    # =========================
                    # BUSCAR TURMAS
                    # =========================

                    escola_id = st.session_state["escola_id"]

                    turmas = listar_turmas_por_escola(
                        escola_id
                    )
                    opcoes_turmas = {
                    nome_turma: id_turma
                    for id_turma, nome_turma in turmas
                    }


                    turmas_cadastradas = [
                        nome_turma
                        for id_turma, nome_turma in turmas
                    ]

                    # =========================
                    # VERIFICAR TURMAS
                    # =========================

                    turmas_invalidas = []

                    for turma in df_alunos["Turma"]:

                        if turma not in turmas_cadastradas:
                            turmas_invalidas.append(turma)

                    if turmas_invalidas:

                        st.error(
                            "Existem turmas no Excel "
                            "que não estão cadastradas."
                        )

                        st.write(
                            "Turmas não encontradas:"
                        )

                        for turma in turmas_invalidas:

                            st.write(
                                f" {turma}"
                            )

                    else:

                        st.success(
                            "Todas as turmas estão cadastradas!"
                        )

                        st.subheader(
                            "Alunos encontrados"
                        )

                        st.dataframe(
                            df_alunos,
                            use_container_width=True
                        )

                        if st.button(
                            " CADASTRAR ALUNOS",
                            use_container_width=True
                        ):
                            alunos_para_cadastrar = []

                            for _, linha in df_alunos.iterrows():

                                turma_id = opcoes_turmas[linha["Turma"]]

                                aluno = {
                                    "escola_id": escola_id,
                                    "turma_id": turma_id,
                                    "nome": linha["Nome do aluno"],
                                    "matricula": linha["Matrícula"]
                                }

                                alunos_para_cadastrar.append(aluno)


                            cadastrar_alunos_excel(alunos_para_cadastrar)

                            st.success(
                                f"{len(alunos_para_cadastrar)} aluno(s) cadastrado(s) com sucesso!"
                            )

