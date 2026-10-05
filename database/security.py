import bcrypt


def gerar_hash_senha(senha):
    senha_bytes = senha.encode("utf-8")

    hash_senha = bcrypt.hashpw(
        senha_bytes,
        bcrypt.gensalt()
    )

    return hash_senha.decode("utf-8")

def verificar_senha(senha, senha_hash):
    senha_bytes = senha.encode("utf-8")
    hash_bytes = senha_hash.encode("utf-8")

    return bcrypt.checkpw(
        senha_bytes,
        hash_bytes
    )