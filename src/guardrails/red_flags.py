def detectar_red_flags(texto: str) -> bool:
    """Retorna True se o texto contiver sintomas de emergência médica."""
    termos_emergencia = [
        "dor no peito", "falta de ar", "desmaio", "pior dor da vida", 
        "sangramento", "paralisia", "confusão mental", "infarto", "avc"
    ]
    
    texto_lower = texto.lower()
    return any(termo in texto_lower for termo in termos_emergencia)