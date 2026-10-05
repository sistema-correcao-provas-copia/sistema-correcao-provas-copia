\# Sistema de Correção de Provas



\## Como rodar o projeto com Docker



\### Pré-requisitos

\- \[Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução.



\### Subindo a aplicação



1\. \*\*Gerar dependências atualizadas (se necessário):\*\*

&#x20;  ```bash

&#x20;  pip freeze > requirements.txt

## API inicial (dados de demonstração)

A API ASGI está em `api.py` e usa dados estáticos, sem acessar o banco. Para iniciá-la na raiz do projeto, execute:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

O contrato OpenAPI está em `openapi.json`. As cinco rotas são:

- `GET /api/escolas/{resource_id}/turmas`
- `GET /api/escolas/{resource_id}/materias`
- `GET /api/professores/{resource_id}/vinculos`
- `GET /api/professores/{resource_id}/gabaritos`
- `GET /api/professores/{resource_id}/resultados`

IDs de demonstração disponíveis: `1` e `2`. Respostas de sucesso usam `{ "data": [...] }`. Erros usam `{ "error": { "code": 400, "message": "...", "details": {} } }`; identificadores inválidos retornam 400, IDs não cadastrados retornam 404 e erros inesperados retornam 500.

