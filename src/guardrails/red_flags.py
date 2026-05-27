def detectar_red_flags(texto: str) -> bool:
    """Retorna True se o texto contiver sintomas de emergência médica."""
    termos_emergencia = [
        # Mapeamento Genérico
        "desmaio", "pior dor da vida", "confusão mental", "infarto", "avc", "paralisia",
        
        # Cardiovascular / Neurológico
        "dor no peito",
        "paralisado",
        "dificuldade de falar",
        
        # Respiratório / Alérgico
        "falta de ar",
        
        # Sangramento - agora mais específico
        "sangue esguichando",   # Era só "sangue" antes — muito genérico
        "corte profundo",
        "não para de sangrar",
        "nao para de sangrar",
        
        # Cianose
        "roxo",
        
        # Esforço respiratório
        "esforco",
        "esforço"
    ]
    
    texto_lower = texto.lower()
    return any(termo in texto_lower for termo in termos_emergencia)