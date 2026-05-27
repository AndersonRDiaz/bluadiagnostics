def moderar_conteudo(texto: str) -> bool:
    """Verifica se a linguagem é abusiva ou ofensiva."""
    palavras_ofensivas = ["idiota", "imbecil", "burro", "inutil", "merda", "maldito"]
    
    texto_lower = texto.lower()
    if any(ofensa in texto_lower for ofensa in palavras_ofensivas):
        return False
    return True