from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import qrcode


def definir_layout(quantidade_questoes):
    if quantidade_questoes <= 10:
        return 1
    if quantidade_questoes <= 20:
        return 2
    return 3

def gerar_folha_pdf(
    nome_avaliacao,
    turma_materia,
    quantidade_questoes,
    codigo_qr,
    caminho_pdf
):
    pdf = canvas.Canvas(
        caminho_pdf,
        pagesize=A4
    )

    largura, altura = A4

    pdf.setFont("Helvetica-Bold", 16)

    pdf.drawCentredString(
        largura / 2,
        altura - 50,
        "FOLHA DE RESPOSTAS"
    )

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        50,
        altura - 80,
        f"Avaliação: {nome_avaliacao}"
    )

    pdf.drawString(
        50,
        altura - 100,
        f"Turma e matéria: {turma_materia}"
    )

    pdf.drawString(
        50,
        altura - 120,
        f"Quantidade de questões: {quantidade_questoes}"
    )
    qr = qrcode.make(codigo_qr)

    qr_path = "qr_temp.png"
    qr.save(qr_path)

    pdf.drawImage(
        qr_path,
        largura - 170,
        altura - 190,
        width=120,
        height=120
    )


    y = altura - 220

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        50,
        y,
        "QUESTÕES"
    )

    tamanho_marcador = 18

    pdf.rect(
        30,
        altura - 45,
        tamanho_marcador,
        tamanho_marcador,
        fill=1
    )

    pdf.rect(
        largura - 42,
        altura - 45,
        tamanho_marcador,
        tamanho_marcador,
        fill=1
    )

    pdf.rect(
        30,
        30,
        tamanho_marcador,
        tamanho_marcador,
        fill=1
    )

    pdf.rect(
        largura - 42,
        30,
        tamanho_marcador,
        tamanho_marcador,
        fill=1
    )

    y -= 25

    pdf.setFont("Helvetica", 10)

    # Define a quantidade de colunas
    quantidade_colunas = definir_layout(quantidade_questoes)

    # Calcula quantas questões ficarão em cada coluna
    questoes_por_coluna = (
        quantidade_questoes + quantidade_colunas - 1
    ) // quantidade_colunas

    # Largura disponível para cada coluna
    largura_coluna = (
        (largura - 100) / quantidade_colunas
    )

    # Desenha as questões
    for numero in range(1, quantidade_questoes + 1):

        indice = numero - 1

        coluna = indice // questoes_por_coluna
        linha = indice % questoes_por_coluna

        x = (
            50
            + coluna * largura_coluna
        )

        y_questao = (
            y - linha * 22
        )

        pdf.drawString(
            x,
            y_questao,
            f"{numero}"
        )

        alternativas = ["A", "B", "C", "D", "E"]

        x_inicial = x + 25

        for indice_alternativa, alternativa in enumerate(alternativas):

            x_alternativa = (
                x_inicial
                + indice_alternativa * 25
            )

            pdf.circle(
                x_alternativa,
                y_questao,
                6
            )

            pdf.drawString(
                x_alternativa + 8,
                y_questao - 3,
                alternativa
            )
    pdf.save()

