from database.connection import conectar
from database.security import gerar_hash_senha


def cadastrar_escola(
    codigo_inep,
    nome,
    cnpj,
    endereco,
    cidade,
    estado,
    telefone,
    email
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO escola (
            codigo_inep,
            nome,
            cnpj,
            endereco,
            cidade,
            estado,
            telefone,
            email
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """

    valores = (
        codigo_inep,
        nome,
        cnpj,
        endereco,
        cidade,
        estado,
        telefone,
        email
    )

    cursor.execute(sql, valores)

    id_escola = cursor.fetchone()[0]

    conexao.commit()

    cursor.close()
    conexao.close()

    return id_escola


def cadastrar_responsavel(
    escola_id,
    nome,
    cpf,
    email,
    telefone,
    senha
):
    conexao = conectar()
    cursor = conexao.cursor()

    senha_hash = gerar_hash_senha(senha)

    sql = """
        INSERT INTO responsavel (
            escola_id,
            nome,
            cpf,
            email,
            telefone,
            senha_hash
        )
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    valores = (
        escola_id,
        nome,
        cpf,
        email,
        telefone,
        senha_hash
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

def buscar_responsavel_por_email(email):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT id, escola_id, nome, email, senha_hash
        FROM responsavel
        WHERE email = %s;
    """

    cursor.execute(sql, (email,))

    responsavel = cursor.fetchone()

    cursor.close()
    conexao.close()

    return responsavel

def cadastrar_professor(
    escola_id,
    nome,
    cpf,
    email,
    telefone,
    senha
):
    conexao = conectar()
    cursor = conexao.cursor()

    senha_hash = gerar_hash_senha(senha)

    sql = """
        INSERT INTO professor (
            escola_id,
            nome,
            cpf,
            email,
            telefone,
            senha_hash
        )
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    valores = (
        escola_id,
        nome,
        cpf,
        email,
        telefone,
        senha_hash
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()


def cadastrar_turma(
    escola_id,
    nome
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO turma (
            escola_id,
            nome
        )
        VALUES (%s, %s);
    """

    valores = (
        escola_id,
        nome
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

def cadastrar_aluno(
    escola_id,
    turma_id,
    nome,
    matricula
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO aluno (
            escola_id,
            turma_id,
            nome,
            matricula
        )
        VALUES (%s, %s, %s, %s);
    """

    valores = (
        escola_id,
        turma_id,
        nome,
        matricula
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

def listar_turmas_por_escola(escola_id):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT id, nome
        FROM turma
        WHERE escola_id = %s
        ORDER BY nome;
    """

    cursor.execute(sql, (escola_id,))

    turmas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return turmas

def cadastrar_alunos_excel(alunos):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO aluno (
            escola_id,
            turma_id,
            nome,
            matricula
        )
        VALUES (%s, %s, %s, %s);
    """

    for aluno in alunos:

        valores = (
            aluno["escola_id"],
            aluno["turma_id"],
            aluno["nome"],
            aluno["matricula"]
        )

        cursor.execute(
            sql,
            valores
        )

    conexao.commit()

    cursor.close()
    conexao.close()

def listar_matriculas_por_escola(escola_id):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT matricula
        FROM aluno
        WHERE escola_id = %s
        AND matricula IS NOT NULL;
    """

    cursor.execute(sql, (escola_id,))

    matriculas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return matriculas

def cadastrar_gabarito(
    escola_id,
    professor_id,
    turma_id,
    materia_id,
    nome,
    quantidade_questoes,
    codigo_qr
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO gabarito (
            escola_id,
            professor_id,
            turma_id,
            materia_id,
            nome,
            quantidade_questoes,
            codigo_qr
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """

    valores = (
        escola_id,
        professor_id,
        turma_id,
        materia_id,
        nome,
        quantidade_questoes,
        codigo_qr
    )

    cursor.execute(sql, valores)

    id_gabarito = cursor.fetchone()[0]

    conexao.commit()

    cursor.close()
    conexao.close()

    return id_gabarito

def cadastrar_questao_gabarito(
    gabarito_id,
    numero_questao,
    alternativa_correta,
    peso,
    competencia
):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO gabarito_questao (
            gabarito_id,
            numero_questao,
            alternativa_correta,
            peso,
            competencia
        )
        VALUES (%s, %s, %s, %s, %s);
    """

    valores = (
        gabarito_id,
        numero_questao,
        alternativa_correta,
        peso,
        competencia
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

def cadastrar_materia(escola_id, nome):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO materia (
            escola_id,
            nome
        )
        VALUES (%s, %s);
    """

    valores = (
        escola_id,
        nome
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

def listar_materias_por_escola(escola_id):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT id, nome
        FROM materia
        WHERE escola_id = %s
        ORDER BY nome;
    """

    cursor.execute(sql, (escola_id,))

    materias = cursor.fetchall()

    cursor.close()
    conexao.close()

    return materias

def cadastrar_vinculo_professor(
    professor_id,
    turma_id,
    materia_id
):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO professor_turma_materia (
            professor_id,
            turma_id,
            materia_id
        )
        VALUES (%s, %s, %s);
    """

    valores = (
        professor_id,
        turma_id,
        materia_id
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

def listar_professores_por_escola(escola_id):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT id, nome
        FROM professor
        WHERE escola_id = %s
        ORDER BY nome;
    """

    cursor.execute(sql, (escola_id,))

    professores = cursor.fetchall()

    cursor.close()
    conexao.close()

    return professores

def buscar_professor_por_email(email):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT id, escola_id, nome, email, senha_hash
        FROM professor
        WHERE email = %s;
    """

    cursor.execute(sql, (email,))

    professor = cursor.fetchone()

    cursor.close()
    conexao.close()

    return professor

def listar_turmas_materias_por_professor(professor_id):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT
            turma.id,
            turma.nome,
            materia.id,
            materia.nome
        FROM professor_turma_materia
        INNER JOIN turma
            ON professor_turma_materia.turma_id = turma.id
        INNER JOIN materia
            ON professor_turma_materia.materia_id = materia.id
        WHERE professor_turma_materia.professor_id = %s
        ORDER BY turma.nome, materia.nome;
    """

    cursor.execute(sql, (professor_id,))

    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados

def listar_vinculos_por_professor(professor_id):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT
            professor_turma_materia.id,
            turma.id,
            turma.nome,
            materia.id,
            materia.nome
        FROM professor_turma_materia
        INNER JOIN turma
            ON professor_turma_materia.turma_id = turma.id
        INNER JOIN materia
            ON professor_turma_materia.materia_id = materia.id
        WHERE professor_turma_materia.professor_id = %s
        ORDER BY turma.nome, materia.nome;
    """

    cursor.execute(sql, (professor_id,))

    vinculos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return vinculos

def listar_gabaritos_por_professor(professor_id):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT
            gabarito.id,
            gabarito.nome,
            turma.id,
            turma.nome,
            materia.nome,
            gabarito.quantidade_questoes,
            gabarito.codigo_qr
        FROM gabarito
        INNER JOIN turma
            ON gabarito.turma_id = turma.id
        INNER JOIN materia
            ON gabarito.materia_id = materia.id
        WHERE gabarito.professor_id = %s
        ORDER BY gabarito.data_criacao DESC;
    """

    cursor.execute(sql, (professor_id,))

    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados


def listar_alunos_por_turma(turma_id):

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT
            id,
            nome,
            matricula
        FROM aluno
        WHERE turma_id = %s
        ORDER BY nome;
    """

    cursor.execute(sql, (turma_id,))

    alunos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return alunos

def listar_questoes_por_gabarito(gabarito_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            numero_questao,
            alternativa_correta,
            peso,
            competencia
        FROM gabarito_questao
        WHERE gabarito_id = %s
        ORDER BY numero_questao;
    """, (gabarito_id,))

    questoes = cursor.fetchall()

    cursor.close()
    conn.close()

    return questoes

def cadastrar_folha_resposta(gabarito_id, aluno_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO folha_resposta (
            gabarito_id,
            aluno_id
        )
        VALUES (%s, %s)
        ON CONFLICT (gabarito_id, aluno_id)
        DO UPDATE SET data_correcao = CURRENT_TIMESTAMP
        RETURNING id;
    """, (gabarito_id, aluno_id))

    folha_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return folha_id

def cadastrar_resultado(
    folha_resposta_id,
    quantidade_acertos,
    quantidade_questoes,
    nota
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resultado (
            folha_resposta_id,
            quantidade_acertos,
            quantidade_questoes,
            nota
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (folha_resposta_id)
        DO UPDATE SET
            quantidade_acertos = EXCLUDED.quantidade_acertos,
            quantidade_questoes = EXCLUDED.quantidade_questoes,
            nota = EXCLUDED.nota,
            data_resultado = CURRENT_TIMESTAMP;
    """, (
        folha_resposta_id,
        quantidade_acertos,
        quantidade_questoes,
        nota
    ))

    conn.commit()

    cursor.close()
    conn.close()

def cadastrar_respostas_aluno(
    folha_resposta_id,
    respostas_aluno
):

    conn = conectar()
    cursor = conn.cursor()

    for numero_questao, alternativa in respostas_aluno.items():

        cursor.execute("""
            INSERT INTO resposta_aluno (
                folha_resposta_id,
                numero_questao,
                alternativa_marcada
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (folha_resposta_id, numero_questao)
            DO UPDATE SET
                alternativa_marcada = EXCLUDED.alternativa_marcada;
        """, (
            folha_resposta_id,
            numero_questao,
            alternativa
        ))

    conn.commit()

    cursor.close()
    conn.close()

def listar_resultados_por_professor(professor_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            resultado.id,
            aluno.nome,
            turma.nome,
            materia.nome,
            gabarito.nome,
            resultado.quantidade_acertos,
            resultado.quantidade_questoes,
            resultado.nota,
            resultado.data_resultado
        FROM resultado
        INNER JOIN folha_resposta
            ON resultado.folha_resposta_id = folha_resposta.id
        INNER JOIN aluno
            ON folha_resposta.aluno_id = aluno.id
        INNER JOIN gabarito
            ON folha_resposta.gabarito_id = gabarito.id
        INNER JOIN turma
            ON gabarito.turma_id = turma.id
        INNER JOIN materia
            ON gabarito.materia_id = materia.id
        WHERE gabarito.professor_id = %s
        ORDER BY resultado.data_resultado DESC;
    """, (professor_id,))

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultados

def listar_resultados_por_escola(escola_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            a.nome AS aluno,
            t.nome AS turma,
            m.nome AS materia,
            g.nome,
            r.quantidade_acertos,
            r.quantidade_questoes,
            r.nota,
            f.data_correcao
        FROM resultado r
        JOIN folha_resposta f
            ON r.folha_resposta_id = f.id
        JOIN aluno a
            ON f.aluno_id = a.id
        JOIN turma t
            ON a.turma_id = t.id
        JOIN gabarito g
            ON f.gabarito_id = g.id
        JOIN materia m
            ON g.materia_id = m.id
        WHERE t.escola_id = %s
        ORDER BY f.data_correcao DESC
    """, (escola_id,))

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultados