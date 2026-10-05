"""API inicial do sistema, servindo dados de demonstração sem acessar o banco."""

from __future__ import annotations

import logging
from typing import Any

from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

logger = logging.getLogger(__name__)

# IDs 1 e 2 são os únicos recursos disponíveis enquanto a API usa mocks.
MOCKS: dict[str, dict[int, list[dict[str, Any]]]] = {
    "turmas": {
        1: [{"id": 101, "nome": "3º Ano A"}, {"id": 102, "nome": "3º Ano B"}],
        2: [{"id": 201, "nome": "2º Ano A"}],
    },
    "materias": {
        1: [{"id": 11, "nome": "Matemática"}, {"id": 12, "nome": "Português"}],
        2: [{"id": 21, "nome": "Ciências"}],
    },
    "vinculos": {
        1: [
            {"id": 1, "turma": {"id": 101, "nome": "3º Ano A"}, "materia": {"id": 11, "nome": "Matemática"}},
            {"id": 2, "turma": {"id": 102, "nome": "3º Ano B"}, "materia": {"id": 12, "nome": "Português"}},
        ],
        2: [{"id": 3, "turma": {"id": 201, "nome": "2º Ano A"}, "materia": {"id": 21, "nome": "Ciências"}}],
    },
    "gabaritos": {
        1: [{"id": 301, "nome": "Avaliação bimestral", "turma_id": 101, "turma": "3º Ano A", "materia": "Matemática", "quantidade_questoes": 10, "codigo_qr": "GAB-301"}],
        2: [{"id": 302, "nome": "Revisão", "turma_id": 201, "turma": "2º Ano A", "materia": "Ciências", "quantidade_questoes": 5, "codigo_qr": "GAB-302"}],
    },
    "resultados": {
        1: [{"id": 401, "aluno": "Ana Silva", "turma": "3º Ano A", "materia": "Matemática", "avaliacao": "Avaliação bimestral", "quantidade_acertos": 8, "quantidade_questoes": 10, "nota": 8.0, "data_resultado": "2026-09-15"}],
        2: [{"id": 402, "aluno": "Bruno Souza", "turma": "2º Ano A", "materia": "Ciências", "avaliacao": "Revisão", "quantidade_acertos": 4, "quantidade_questoes": 5, "nota": 8.0, "data_resultado": "2026-09-16"}],
    },
}


def error(status: int, message: str, details: Any = None) -> JSONResponse:
    body: dict[str, Any] = {"error": {"code": status, "message": message}}
    if details is not None:
        body["error"]["details"] = details
    return JSONResponse(body, status_code=status)


async def list_mock(request: Request, collection_name: str) -> JSONResponse:
    raw_id = request.path_params["resource_id"]
    if not raw_id.isdecimal() or int(raw_id) < 1:
        return error(400, "O identificador deve ser um número inteiro positivo.", {"field": "resource_id"})
    resource_id = int(raw_id)
    collection = MOCKS[collection_name]
    if resource_id not in collection:
        return error(404, "Recurso não encontrado.", {"resource_id": resource_id})
    return JSONResponse({"data": collection[resource_id]})


async def http_error(_: Request, exc: HTTPException) -> JSONResponse:
    message = "Rota não encontrada." if exc.status_code == 404 else "Método HTTP não permitido."
    return error(exc.status_code, message, {"reason": str(exc.detail)})


async def internal_error(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Erro inesperado ao processar requisição da API", exc_info=exc)
    return error(500, "Erro interno ao processar a solicitação.")


def endpoint(collection: str):
    async def handler(request: Request) -> JSONResponse:
        return await list_mock(request, collection)
    return handler


routes = [
    Route("/api/escolas/{resource_id}/turmas", endpoint("turmas"), methods=["GET"]),
    Route("/api/escolas/{resource_id}/materias", endpoint("materias"), methods=["GET"]),
    Route("/api/professores/{resource_id}/vinculos", endpoint("vinculos"), methods=["GET"]),
    Route("/api/professores/{resource_id}/gabaritos", endpoint("gabaritos"), methods=["GET"]),
    Route("/api/professores/{resource_id}/resultados", endpoint("resultados"), methods=["GET"]),
]

app = Starlette(routes=routes, exception_handlers={404: http_error, 405: http_error, 500: internal_error})
