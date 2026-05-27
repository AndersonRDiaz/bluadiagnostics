import os

def test_regressao_system_prompt():
    """Garante que as regras inegociáveis e de LGPD continuam no prompt base."""
    # Sobe dois níveis (de /tests/ para a raiz) e entra em /prompts/
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    caminho = os.path.join(raiz, "prompts", "system_prompt.md")
    
    assert os.path.exists(caminho), "Arquivo system_prompt.md sumiu!"
    
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read().lower()
    
    # Validações de Regressão (Se alguém apagar isso do .md, o teste falha)
    assert "lgpd" in conteudo, "Alerta: A regra de LGPD foi removida do prompt!"
    assert "samu" in conteudo, "Alerta: O protocolo do SAMU foi removido!"
    assert "red flags" in conteudo, "Alerta: A seção de Red Flags desapareceu!"