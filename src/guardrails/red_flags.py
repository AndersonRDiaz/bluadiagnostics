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
            # Dor torácica
            "dor no peito", "dor torácica", "dor toracica",
            "dor forte no peito","aperto no peito", "peso no peito",
            # Irradiação clássica de IAM
            "irradia para o braço", "irradia para o braco",
            "dor no braço esquerdo", "dor no braco esquerdo",
            "dor no ombro esquerdo", "dor no maxilar",
            # Sinais acompanhantes
            "sudorese fria", "suor frio", "palpitação forte", "palpitacao forte",
            "coração acelerado com dor", "infarto", "parada cardíaca", "parada cardiaca",
        ],
        orientacao="Sintoma compatível com síndrome coronariana aguda (infarto). Não aguarde — ligue imediatamente para o SAMU (192).",
        protocolo_escalada="SAMU_192_IMEDIATO",
    ),

    CategoriaRedFlag(
        nome="neurologica",
        severidade="emergencia",
        termos=[
            # Sinais clássicos de AVC (FAST)
            "boca torta", "rosto caído", "rosto caido",
            "fraqueza no rosto", "fraqueza no braço", "fraqueza no braco",
            "não consigo falar", "nao consigo falar",
            "fala enrolada", "não entendo o que falam", "nao entendo o que falam",
            # Outros neurológicos graves
            "avc", "derrame cerebral",
            "pior dor de cabeça da vida", "pior dor de cabeca da vida",
            "dor de cabeça súbita", "dor de cabeca subita",
            "visão dupla", "visao dupla", "perda súbita de visão", "perda subita de visao",
            "convulsão", "convulsao", "confusão mental", "confusao mental",
            "desmaio", "perda de consciência", "perda de consciencia",
            "paralisia", "paralisado", "paralisada",
            "dormência súbita", "dormencia subita",
        ],
        orientacao="Sintoma compatível com AVC ou emergência neurológica. Ligue imediatamente para o SAMU (192). Não ofereça água ou comida ao paciente.",
        protocolo_escalada="SAMU_192_IMEDIATO",
    ),

    CategoriaRedFlag(
        nome="respiratoria",
        severidade="emergencia",
        termos=[
            "falta de ar", "falta de ar intensa", "não consigo respirar", "nao consigo respirar",
            "respiração difícil", "respiracao dificil",
            "lábios roxos", "labios roxos", "rosto roxo",
            "saturação baixa", "saturacao baixa", "oxigênio baixo", "oxigenio baixo",
            "chiado no peito intenso", "asma grave",
            "sufocamento", "sufocando",
            "engasgou e não respira", "engasgou e nao respira",
            "labio muito roxo", "labio roxo", 
            "fazendo muito esforco", "muito esforco", "esforco",
        ],
        orientacao="Dificuldade respiratória grave detectada. Ligue imediatamente para o SAMU (192). Mantenha o paciente sentado e calmo.",
        protocolo_escalada="SAMU_192_IMEDIATO",
    ),

    CategoriaRedFlag(
        nome="alergica_anafilaxia",
        severidade="emergencia",
        termos=[
            "anafilaxia", "choque anafilático", "choque anafilatico",
            "urticária com falta de ar", "urticaria com falta de ar",
            "alergia grave", "reação alérgica grave", "reacao alergica grave",
            "inchaço na garganta", "inchaco na garganta",
            "língua inchada", "lingua inchada",
            "lábio inchado com dificuldade", "labio inchado com dificuldade",
        ],
        orientacao="Suspeita de anafilaxia (reação alérgica grave). Ligue imediatamente para o SAMU (192). Se houver epinefrina (EpiPen) disponível, use conforme orientação médica prévia.",
        protocolo_escalada="SAMU_192_IMEDIATO",
    ),

    CategoriaRedFlag(
        nome="sangramento_grave",
        severidade="emergencia",
        termos=[
            "sangue esguichando", "não para de sangrar", "nao para de sangrar",
            "corte profundo", "hemorragia", "sangramento intenso",
            "sangue pela boca em quantidade", "vomitando sangue",
            "fezes com muito sangue", "sangramento pós-operatório", "sangramento pos-operatorio",
        ],
        orientacao="Sangramento grave identificado. Aplique pressão direta no local. Ligue para o SAMU (192) imediatamente.",
        protocolo_escalada="SAMU_192_IMEDIATO",
    ),

    CategoriaRedFlag(
        nome="psiquiatrica_urgente",
        severidade="urgencia",
        termos=[
            "quero me matar", "vou me matar", "não quero mais viver", "nao quero mais viver",
            "pensamento de suicídio", "pensamento de suicidio",
            "me machucar", "me machuquei de propósito", "me machuquei de proposito",
            "ideação suicida", "ideacao suicida",
        ],
        orientacao="Crise de saúde mental identificada. Encaminhar para CVV (188, disponível 24h) e orientar busca imediata a pronto-socorro psiquiátrico ou UPA.",
        protocolo_escalada="CVV_188_UPA",
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