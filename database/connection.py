import os

import psycopg2


def _configurar_env():
    """Carrega segredos do Streamlit Cloud ou variáveis do ambiente local."""
    try:
        import streamlit as st

        for chave in ("DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_PORT"):
            if chave not in os.environ and chave in st.secrets:
                os.environ[chave] = str(st.secrets[chave])
    except Exception:
        # Fora do Streamlit, a configuração vem do ambiente do processo.
        pass


def conectar():
    _configurar_env()
    conexao = psycopg2.connect(
        host=os.getenv("DB_HOST", os.getenv("POSTGRES_HOST", "localhost")),
        database=os.getenv("DB_NAME", os.getenv("POSTGRES_DB", "sistema_correcao_provas")),
        user=os.getenv("DB_USER", os.getenv("POSTGRES_USER", "postgres")),
        password=os.getenv("DB_PASSWORD", os.getenv("POSTGRES_PASSWORD", "")),
        port=os.getenv("DB_PORT", os.getenv("POSTGRES_PORT", "5432")),
        client_encoding="LATIN1"
    )

    return conexao
