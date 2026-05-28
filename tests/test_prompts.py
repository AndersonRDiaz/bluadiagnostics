import pytest
from src.agents.triagem import carregar_prompt_triagem

def test_carregamento_prompt_triagem():
    """Testa se o prompt é carregado e concatenado corretamente sem retornar vazio."""
    prompt_completo = carregar_prompt_triagem()
    
    assert prompt_completo is not None
    assert len(prompt_completo) > 100  # Garante que o texto tem um tamanho substancial

def test_prompt_contem_guardrails_obrigatorios():
    """Testa se as restrições inegociáveis e LGPD estão presentes no texto final."""
    prompt_completo = carregar_prompt_triagem()
    
    # Verifica a existência das proteções vitais que você configurou
    assert "NUNCA realize diagnostico definitivo" in prompt_completo
    assert "ESCALADA HUMANA" in prompt_completo
    assert "LGPD" in prompt_completo