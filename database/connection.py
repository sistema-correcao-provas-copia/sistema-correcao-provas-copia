import psycopg2


def conectar():
    conexao = psycopg2.connect(
        host="localhost",
        database="sistema_correcao_provas",
        user="postgres",
        password="admin",
        port="5432",
        client_encoding="LATIN1"
    )

    return conexao