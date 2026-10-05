from queries import cadastrar_escola

try:
    id_escola = cadastrar_escola(
        "99999999",
        "Escola Teste",
        "",
        "Rua Teste",
        "Ararendá",
        "CE",
        "(88) 99999-9999",
        "teste@escola.com"
    )

    print("Escola cadastrada com sucesso!")
    print("ID da escola:", id_escola)

except Exception as erro:
    print("Erro ao cadastrar escola:")
    print(erro)