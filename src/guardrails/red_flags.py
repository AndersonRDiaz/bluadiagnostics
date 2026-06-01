from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# 1. Estrutura de uma categoria de red flag
# ---------------------------------------------------------------------------

@dataclass
class CategoriaRedFlag:
    """Representa uma categoria clínica de emergência com seus termos e orientação."""

    nome: str
    severidade: str  # "emergencia" | "urgencia"
    termos: list[str]
    orientacao: str
    protocolo_escalada: str

# ---------------------------------------------------------------------------
# 2. Base de conhecimento de red flags por categoria clínica
# ---------------------------------------------------------------------------

CATEGORIAS_RED_FLAG: list[CategoriaRedFlag] = [

    CategoriaRedFlag(
        nome="cardiovascular",
        severidade="emergencia",
        termos=[
            # Termos médicos e variações
            "dor no peito", "dor torácica", "dor toracica", "infarto", "parada cardíaca", "parada cardiaca",
            "dor forte no peito", "aperto no peito", "peso no peito", "pressão no peito", "pressao no peito","dor muito forte no peito",
            # Irradiação
            "irradia para o braço", "irradia para o braco", "dor no braço esquerdo", "dor no braco esquerdo",
            "dor no ombro esquerdo", "dor no maxilar", "dor no pescoço e peito", "dor na mandíbula","irradia pro braço",
            # Coloquialismos e gírias
            "peito rasgando", "coração apertado", "coracao apertado", "pontada no coração", "pontada no coracao",
            "coração acelerado com dor", "tendo um infarto", "tendo um treco", "peito doendo muito",
            # Sinais acompanhantes
            "sudorese fria", "suor frio", "palpitação forte", "palpitacao forte", "formigamento no braço", "formigamento no braco",
        ],
        orientacao="Sintoma compatível com síndrome coronariana aguda (infarto). Não aguarde — ligue imediatamente para o SAMU (192).",
        protocolo_escalada="SAMU_192_IMEDIATO",
    ),

    CategoriaRedFlag(
        nome="neurologica",
        severidade="emergencia",
        termos=[
            # Sinais clássicos de AVC (FAST)
            "boca torta", "rosto caído", "rosto caido", "rosto torto",
            "fraqueza no rosto", "fraqueza no braço", "fraqueza no braco", "fraqueza na perna",
            "não consigo falar", "nao consigo falar", "fala enrolada", "fala arrastada", "fala mole",
            "não entendo o que falam", "nao entendo o que falam", "confusão mental", "confusao mental",
            # Termos médicos e variações
            "avc", "derrame cerebral", "derrame", "convulsão", "convulsao", "ataque epilético",
            "pior dor de cabeça da vida", "pior dor de cabeca da vida", "dor de cabeça súbita", "dor de cabeca subita",
            "visão dupla", "visao dupla", "perda súbita de visão", "perda subita de visao", "cegueira repentina",
            # Desmaios e perda de sentido
            "desmaio", "perda de consciência", "perda de consciencia", "apagou", "desmaiou", "não acorda", "nao acorda",
            "paralisia", "paralisado", "paralisada", "metade do corpo adormecido", "não sinto meu corpo",
            "dormência súbita", "dormencia subita", "repuxando", "tremendo muito",
        ],
        orientacao="Sintoma compatível com AVC ou emergência neurológica. Ligue imediatamente para o SAMU (192). Não ofereça água ou comida ao paciente.",
        protocolo_escalada="SAMU_192_IMEDIATO",
    ),

    CategoriaRedFlag(
        nome="respiratoria",
        severidade="emergencia",
        termos=[
            # Termos técnicos
            "falta de ar", "falta de ar intensa", "respiração difícil", "respiracao dificil", "asma grave",
            "saturação baixa", "saturacao baixa", "oxigênio baixo", "oxigenio baixo",
            # Coloquialismos
            "não consigo respirar", "nao consigo respirar", "sem ar", "ar não vem", "ar nao vem",
            "sufocamento", "sufocando", "engasgou e não respira", "engasgou e nao respira", "afogando",
            "chiado no peito intenso", "puxando o ar", "respiração ofegante", "cansado pra respirar",
            # Sinais visuais
            "lábios roxos", "labios roxos", "rosto roxo", "boca roxa", "labio muito roxo", "labio roxo",
            "fazendo muito esforco", "muito esforco para respirar",
        ],
        orientacao="Dificuldade respiratória grave detectada. Ligue imediatamente para o SAMU (192). Mantenha o paciente sentado e calmo.",
        protocolo_escalada="SAMU_192_IMEDIATO",
    ),

    CategoriaRedFlag(
        nome="alergica_anafilaxia",
        severidade="emergencia",
        termos=[
            # Termos técnicos
            "anafilaxia", "choque anafilático", "choque anafilatico", "alergia grave", "reação alérgica grave", "reacao alergica grave",
            # Sintomas físicos descritivos
            "urticária com falta de ar", "urticaria com falta de ar", "empolado com falta de ar", "alergia no corpo todo",
            "inchaço na garganta", "inchaco na garganta", "garganta fechando", "fechou a garganta",
            "língua inchada", "lingua inchada", "não consigo engolir", "nao consigo engolir",
            "lábio inchado com dificuldade", "labio inchado com dificuldade", "rosto desfigurado",
        ],
        orientacao="Suspeita de anafilaxia (reação alérgica grave). Ligue imediatamente para o SAMU (192). Se houver epinefrina (EpiPen) disponível, use conforme orientação médica prévia.",
        protocolo_escalada="SAMU_192_IMEDIATO",
    ),

    CategoriaRedFlag(
        nome="sangramento_grave",
        severidade="emergencia",
        termos=[
            # Termos descritivos e coloquiais
            "sangue esguichando", "não para de sangrar", "nao para de sangrar", "sangrando muito", "jorrando sangue",
            "corte profundo", "hemorragia", "sangramento intenso", "poça de sangue", "poca de sangue",
            "sangue pela boca em quantidade", "vomitando sangue", "tossindo sangue",
            "fezes com muito sangue", "evacuando sangue",
            "sangramento pós-operatório", "sangramento pos-operatorio", "corte aberto", "rasgou a pele",
        ],
        orientacao="Sangramento grave identificado. Aplique pressão direta no local com um pano limpo. Ligue para o SAMU (192) imediatamente.",
        protocolo_escalada="SAMU_192_IMEDIATO",
    ),

    CategoriaRedFlag(
        nome="psiquiatrica_urgente",
        severidade="urgencia",
        termos=[
            # Expressões de ideação
            "quero me matar", "vou me matar", "não quero mais viver", "nao quero mais viver", "dar um fim em tudo", "acabar com tudo",
            "pensamento de suicídio", "pensamento de suicidio", "ideação suicida", "ideacao suicida",
            # Expressões de auto-mutilação
            "me machucar", "me machuquei de propósito", "me machuquei de proposito", "cortar os pulsos", "cortei os pulsos",
            "tomar todos os remédios", "tomar todos os remedios", "overdose",
        ],
        orientacao="Crise de saúde mental identificada. Ligue imediatamente para o CVV (188, disponível 24h) ou busque um pronto-socorro psiquiátrico/UPA. Você não está sozinho.",
        protocolo_escalada="CVV_188_UPA",
    ),

    CategoriaRedFlag(
        nome="trauma_acidente",
        severidade="emergencia",
        termos=[
            "acidente de carro", "acidente de moto", "bateu a cabeça forte", "bateu a cabeca forte",
            "queda de altura", "caiu da escada", "caiu do telhado", "fratura exposta", "osso pra fora",
            "atropelamento", "atropelado", "acidente grave", "ferimento por arma", "tiro", "facada",
        ],
        orientacao="Trauma grave ou acidente identificado. Não mova a vítima a menos que haja risco iminente no local (ex: fogo). Ligue imediatamente para o SAMU (192) ou Bombeiros (193).",
        protocolo_escalada="SAMU_192_IMEDIATO",
    ),

    CategoriaRedFlag(
        nome="obstetrica",
        severidade="emergencia",
        termos=[
            "grávida sangrando", "gravida sangrando", "bolsa estourou", "bolsa rompeu",
            "sangramento na gravidez", "dor muito forte na barriga gravida", "bebê não mexe", "bebe nao mexe",
            "contrações fortes", "contracoes fortes", "trabalho de parto", "eclâmpsia", "eclampsia",
        ],
        orientacao="Emergência obstétrica identificada. Dirija-se imediatamente à maternidade ou pronto-socorro obstétrico mais próximo, ou ligue para o SAMU (192).",
        protocolo_escalada="SAMU_192_IMEDIATO",
    ),
]

# ---------------------------------------------------------------------------
# 3. Funções públicas
# ---------------------------------------------------------------------------

def detectar_red_flags(texto: str) -> bool:
    """
    Retorna True se o texto contiver sintomas de emergência médica.

    Mantém a assinatura original — use esta função onde o código já
    espera apenas um booleano (ex.: roteamento no grafo LangGraph).
    """
    resultado = detectar_red_flags_detalhado(texto)
    return resultado["red_flag_detectada"]


def detectar_red_flags_detalhado(texto: str) -> dict:
    """
    Retorna um dicionário completo com contexto clínico da detecção.

    Use esta função nos evals automatizados, no agente de escalada e
    no relatório técnico para mostrar qual categoria foi ativada.

    Retorno:
    {
        "red_flag_detectada": bool,
        "categorias_ativadas": list[str],   # ex.: ["cardiovascular"]
        "severidade_maxima": str | None,    # "emergencia" | "urgencia" | None
        "termos_encontrados": list[str],    # quais termos bateram
        "orientacao": str | None,           # texto para exibir ao usuário
        "protocolo_escalada": str | None,   # código interno do protocolo
    }
    """
    texto_lower = texto.lower()

    categorias_ativadas: list[str] = []
    termos_encontrados: list[str] = []
    orientacoes: list[str] = []
    protocolos: list[str] = []
    severidades_ativadas: list[str] = []

    for categoria in CATEGORIAS_RED_FLAG:
        termos_da_categoria = [t for t in categoria.termos if t in texto_lower]
        if termos_da_categoria:
            categorias_ativadas.append(categoria.nome)
            termos_encontrados.extend(termos_da_categoria)
            orientacoes.append(categoria.orientacao)
            protocolos.append(categoria.protocolo_escalada)
            severidades_ativadas.append(categoria.severidade)

    # Prioriza "emergencia" sobre "urgencia" se houver múltiplas categorias
    if "emergencia" in severidades_ativadas:
        severidade_maxima = "emergencia"
    elif "urgencia" in severidades_ativadas:
        severidade_maxima = "urgencia"
    else:
        severidade_maxima = None

    return {
        "red_flag_detectada": len(categorias_ativadas) > 0,
        "categorias_ativadas": categorias_ativadas,
        "severidade_maxima": severidade_maxima,
        "termos_encontrados": list(set(termos_encontrados)),  # remove duplicatas
        "orientacao": orientacoes[0] if orientacoes else None,
        "protocolo_escalada": protocolos[0] if protocolos else None,
    }