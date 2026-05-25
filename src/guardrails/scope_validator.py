def validar_escopo(texto: str) -> bool:
    """Verifica se a interação do paciente permanece dentro do escopo médico."""
    assuntos_proibidos = ["politica", "futebol", "religião", "receita de bolo", "investimento"]
    
    texto_lower = texto.lower()
    # Se o paciente tentar falar de algo fora do escopo, o guardrail detecta
    if any(assunto in texto_lower for assunto in assuntos_proibidos):
        return False
    return True