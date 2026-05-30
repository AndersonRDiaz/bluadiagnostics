import re
import unicodedata

def remover_acentos(texto: str) -> str:
    """Remove acentos para padronizar a busca."""
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto

def validar_escopo(texto: str) -> bool:
    """Verifica se a interação do paciente permanece dentro do escopo médico."""
    assuntos_proibidos = [
        "politica", "futebol", "religiao", "receita de bolo", "investimento",
        "cartao de credito", "banco", "financeiro", 
        "cachorro", "gato", "veterinario", "pet",                        
        "imposto de renda", "receita federal", "tributario", "contador", 
        "aluguel", "imobiliaria", "contrato", "advogado"                 
    ]
    
    texto_limpo = remover_acentos(texto.lower())
    
    # O \b garante que só encontre a palavra isolada, e não dentro de outra palavra
    for assunto in assuntos_proibidos:
        padrao = rf"\b{assunto}\b"
        if re.search(padrao, texto_limpo):
            return False
            
    return True