def corrigir_respostas(gabarito, respostas_aluno):

    acertos = 0

    total_questoes = len(gabarito)

    for numero_questao, alternativa_correta in gabarito.items():

        alternativa_marcada = respostas_aluno.get(numero_questao)

        if alternativa_marcada == alternativa_correta:
            acertos += 1

    if total_questoes > 0:
        nota = (acertos / total_questoes) * 10
    else:
        nota = 0

    return acertos, total_questoes, nota

if __name__ == "__main__":

    gabarito_teste = {
        1: "A",
        2: "C",
        3: "B",
        4: "D"
    }

    respostas_teste = {
        1: "A",
        2: "B",
        3: "B",
        4: "D"
    }

    acertos, total, nota = corrigir_respostas(
        gabarito_teste,
        respostas_teste
    )

    print("Acertos:", acertos)
    print("Total de questões:", total)
    print("Nota:", nota)