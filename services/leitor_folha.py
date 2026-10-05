import cv2
import numpy as np

from services.gerar_folha_pdf import definir_layout

ESCALA = 2

def encontrar_marcadores_cantos(imagem_gray):
    # Aplicar Threshold Adaptativo para lidar com sombras e iluminação do ecrã
    thresh = cv2.adaptiveThreshold(
        imagem_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 11, 2
    )

    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    marcadores = []
    for c in cnts:
        area = cv2.contourArea(c)
        # Filtra por tamanho mínimo do quadrado (ajusta se necessário)
        if area > 1000: 
            x, y, w, h = cv2.boundingRect(c)
            ar = w / float(h)
            
            # Verifica se é aproximadamente um quadrado (aspect ratio entre 0.8 e 1.2)
            if 0.8 <= ar <= 1.2:
                # Calcula o centro do quadrado
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    marcadores.append((cX, cY))

    # Se detetou exatamente os 4 cantos
    if len(marcadores) == 4:
        return np.array(marcadores, dtype="float32")
    else:
        raise ValueError(f"Foram encontrados {len(marcadores)} marcadores em vez de 4.")

def ordenar_pontos(pts):
    # Inicializa a matriz de 4 pontos ordenados
    rect = np.zeros((4, 2), dtype="float32")
    
    # O canto superior esquerdo tem a menor soma (x + y)
    # O canto inferior direito tem a maior soma (x + y)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # O canto superior direito tem a menor diferença (y - x)
    # O canto inferior esquerdo tem a maior diferença (y - x)
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def detectar_marcadores(imagem):

    cinza = cv2.cvtColor(
        imagem,
        cv2.COLOR_BGR2GRAY
    )

    # Binarização
    _, binaria = cv2.threshold(
        cinza,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    altura, largura = imagem.shape[:2]

    regioes = {
        "superior_esquerdo": (
            0,
            0,
            int(largura * 0.25),
            int(altura * 0.25)
        ),

        "superior_direito": (
            int(largura * 0.75),
            0,
            largura,
            int(altura * 0.25)
        ),

        "inferior_esquerdo": (
            0,
            int(altura * 0.75),
            int(largura * 0.25),
            altura
        ),

        "inferior_direito": (
            int(largura * 0.75),
            int(altura * 0.75),
            largura,
            altura
        )
    }

    candidatos_por_canto = {}

    # ----------------------------------------
    # 1. ENCONTRAR CANDIDATOS
    # ----------------------------------------

    for nome, (x1, y1, x2, y2) in regioes.items():

        regiao = binaria[
            y1:y2,
            x1:x2
        ]

        contornos, _ = cv2.findContours(
            regiao,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        candidatos = []

        for contorno in contornos:

            area = cv2.contourArea(
                contorno
            )

            if area < 50:
                continue

            x, y, w, h = cv2.boundingRect(
                contorno
            )

            if h == 0:
                continue

            proporcao = w / float(h)

            # Precisa ser aproximadamente quadrado
            if not (
                0.75 <= proporcao <= 1.25
            ):
                continue

            centro_x = (
                x1 + x + w / 2
            )

            centro_y = (
                y1 + y + h / 2
            )

            candidatos.append({
                "x": centro_x,
                "y": centro_y,
                "w": w,
                "h": h,
                "area": area
            })

        candidatos_por_canto[nome] = candidatos

    # ----------------------------------------
    # 2. DESCOBRIR O TAMANHO DO MARCADOR
    # ----------------------------------------

    # O marcador superior esquerdo é usado
    # como referência porque não há QR Code nele.

    candidatos_esquerdo = (
        candidatos_por_canto[
            "superior_esquerdo"
        ]
    )

    if not candidatos_esquerdo:

        return None

    # O marcador normalmente é um dos
    # menores quadrados relevantes.
    #
    # Como aumentamos o marcador para 18,
    # esperamos aproximadamente 18-30 pixels.

    candidatos_validos = [
        c
        for c in candidatos_esquerdo
        if 12 <= c["w"] <= 40
        and 12 <= c["h"] <= 40
    ]

    if not candidatos_validos:

        return None

    marcador_referencia = max(
        candidatos_validos,
        key=lambda c: c["area"]
    )

    tamanho_referencia = (
        marcador_referencia["w"]
        + marcador_referencia["h"]
    ) / 2

    # ----------------------------------------
    # 3. ESCOLHER UM MARCADOR EM CADA CANTO
    # ----------------------------------------

    pontos = []

    for nome in regioes:

        candidatos = (
            candidatos_por_canto[nome]
        )

        candidatos_validos = []

        for candidato in candidatos:

            tamanho = (
                candidato["w"]
                + candidato["h"]
            ) / 2

            # O marcador precisa ter tamanho
            # parecido com o marcador de referência.
            diferenca = abs(
                tamanho - tamanho_referencia
            )

            if diferenca <= (
                tamanho_referencia * 0.45
            ):

                candidatos_validos.append(
                    candidato
                )

        if not candidatos_validos:

            return None

        # Escolhe o candidato cujo tamanho
        # é mais parecido com o marcador original.

        candidato = min(
            candidatos_validos,
            key=lambda c: abs(
                (
                    c["w"]
                    + c["h"]
                ) / 2
                - tamanho_referencia
            )
        )

        pontos.append([
            candidato["x"],
            candidato["y"]
        ])

    # ----------------------------------------
    # 4. ORDENAR OS PONTOS
    # ----------------------------------------

    pontos = np.array(
        pontos,
        dtype=np.float32
    )

    return ordenar_pontos(pontos)

def corrigir_perspectiva(imagem, pontos):
    escala = ESCALA
    destino = np.array(
        [
            [36 * escala, 36 * escala],
            [559 * escala, 36 * escala],
            [559 * escala, 803 * escala],
            [36 * escala, 803 * escala]
        ],
        dtype=np.float32
    )

    matriz = cv2.getPerspectiveTransform(pontos, destino)
    return cv2.warpPerspective(imagem, matriz, (595 * escala, 842 * escala))


def calcular_posicoes_questoes(quantidade_questoes):
    respostas = {}
    alternativas = ["A", "B", "C", "D", "E"]

    quantidade_colunas = definir_layout(quantidade_questoes)
    questoes_por_coluna = (
        quantidade_questoes + quantidade_colunas - 1
    ) // quantidade_colunas
    largura_pdf = 595
    altura_pdf = 842
    x_margem = 50
    largura_util = largura_pdf - 100
    x_circulo = 25
    y_primeira_questao = 597
    passo_y = 22
    passo_x = 25

    for numero in range(1, quantidade_questoes + 1):
        indice = numero - 1
        coluna = indice // questoes_por_coluna
        linha = indice % questoes_por_coluna
        x_base = (
            x_margem
            + coluna * (largura_util / quantidade_colunas)
            + x_circulo
        ) / largura_pdf
        y_atual = (
            altura_pdf - (y_primeira_questao - linha * passo_y)
        ) / altura_pdf
        for idx_alt, alternativa in enumerate(alternativas):
            x_atual = x_base + (idx_alt * passo_x / largura_pdf)
            respostas[(numero, alternativa)] = (x_atual, y_atual)

    return respostas

    questoes_por_coluna = 10

    # Configuração calibrada para o alinhamento correto dos círculos
    config_colunas = [
        {"x_a_pct": 0.126, "y_ini_pct": 0.290, "passo_x_pct": 0.042, "passo_y_pct": 0.0260},
        {"x_a_pct": 0.402, "y_ini_pct": 0.288, "passo_x_pct": 0.042, "passo_y_pct": 0.0262},
        {"x_a_pct": 0.676, "y_ini_pct": 0.288, "passo_x_pct": 0.042, "passo_y_pct": 0.0263}
    ]

    for numero in range(1, quantidade_questoes + 1):
        indice = numero - 1
        coluna = min(2, indice // questoes_por_coluna)
        linha = indice % questoes_por_coluna

        cfg = config_colunas[coluna]

        x_base = cfg["x_a_pct"]
        y_atual = cfg["y_ini_pct"] + (linha * cfg["passo_y_pct"])

        for idx_alt, alternativa in enumerate(alternativas):
            x_atual = x_base + (idx_alt * cfg["passo_x_pct"])
            respostas[(numero, alternativa)] = (x_atual, y_atual)

    return respostas


def detectar_respostas(folha, quantidade_questoes):
    cinza = cv2.cvtColor(folha, cv2.COLOR_BGR2GRAY)
    altura, largura = cinza.shape[:2]

    # Limiar para capturar marcações escuras
    _, binaria = cv2.threshold(cinza, 120, 255, cv2.THRESH_BINARY_INV)

    posicoes_pct = calcular_posicoes_questoes(quantidade_questoes)

    respostas = {}
    alternativas = ["A", "B", "C", "D", "E"]
    debug_img = folha.copy()

    for numero in range(1, quantidade_questoes + 1):
        candidatos = []

        for alternativa in alternativas:
            x_pct, y_pct = posicoes_pct[(numero, alternativa)]

            cx = int(x_pct * largura)
            cy = int(y_pct * altura)

            raio = int(largura * 0.009)

            x1 = max(0, cx - raio)
            x2 = min(largura, cx + raio + 1)
            y1 = max(0, cy - raio)
            y2 = min(altura, cy + raio + 1)

            area_binaria = binaria[y1:y2, x1:x2]

            if area_binaria.size == 0:
                continue

            pixels_escuros = np.sum(area_binaria == 255)
            percentual = pixels_escuros / area_binaria.size

            candidatos.append((alternativa, percentual, (cx, cy)))

            cv2.circle(debug_img, (cx, cy), raio, (255, 0, 0), 1)

        if not candidatos:
            respostas[numero] = None
            continue

        candidatos.sort(key=lambda item: item[1], reverse=True)
        melhor_alt, maior_pct, pos_centro = candidatos[0]
        segundo_pct = candidatos[1][1] if len(candidatos) > 1 else 0

        # Média da linha para garantir isolamento de preenchimento real
        media_pct = sum(c[1] for c in candidatos) / len(candidatos)

        # Só aceita se houver preenchimento real (>= 18%) e se destacar das outras alternativas
        if maior_pct >= 0.18 and (maior_pct - media_pct) >= 0.10:
            respostas[numero] = melhor_alt
            cv2.circle(debug_img, pos_centro, 4, (0, 0, 255), -1)
        else:
            respostas[numero] = None

    cv2.imwrite("debug_alinhameto.jpg", debug_img)
    return respostas


def ler_codigo_qr(imagem):
    detector = cv2.QRCodeDetector()
    codigo, _, _ = detector.detectAndDecode(imagem)
    if codigo:
        return codigo.strip()
    ampliada = cv2.resize(imagem, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    codigo, _, _ = detector.detectAndDecode(ampliada)
    return codigo.strip() if codigo else None


def ler_folha(caminho_imagem, quantidade_questoes, codigo_qr_esperado=None):
    imagem = cv2.imread(caminho_imagem)
    if imagem is None:
        raise ValueError("Não foi possível abrir a imagem.")

    if codigo_qr_esperado is not None:
        codigo_qr_lido = ler_codigo_qr(imagem)
        if not codigo_qr_lido:
            raise ValueError(
                "Nao foi possivel ler o QR Code da folha. "
                "Fotografe a folha inteira, com o QR Code nitido e visivel."
            )
        if codigo_qr_lido != str(codigo_qr_esperado).strip():
            raise ValueError(
                "Esta folha pertence a outra avaliacao e nao pode ser corrigida "
                "com o gabarito selecionado."
            )

    pontos = detectar_marcadores(imagem)
    if pontos is None:
        raise ValueError("Não foi possível detectar os 4 marcadores da folha.")

    folha = corrigir_perspectiva(imagem, pontos)
    return detectar_respostas(
        folha,
        quantidade_questoes
    )
