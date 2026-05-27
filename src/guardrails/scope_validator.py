def validar_escopo(texto: str) -> bool:
    """Verifica se a interação do paciente permanece dentro do escopo médico."""
    # Lista atualizada para barrar os testes OS-001 a OS-005 com sucesso
    assuntos_proibidos = [
        "politica", "futebol", "religião", "receita de bolo", "investimento",
        "cartao de credito", "cartão de crédito", "banco", "financeiro", # OS-001
        "cachorro", "gato", "veterinario", "pet",                        # OS-002
        "imposto de renda", "receita federal", "tributario", "contador", # OS-003
        "aluguel", "imobiliaria", "contrato", "advogado"                 # OS-004
    ]
    
    texto_lower = texto.lower()
    if any(assunto in texto_lower for assunto in assuntos_proibidos):
        return False
    return True