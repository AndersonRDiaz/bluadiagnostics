import pytest
from src.tools.consultar_historico import consultar_historico_paciente
from src.tools.verificar_interacoes import verificar_interacoes_medicamentosas
from src.tools.agendar_teleconsulta import agendar_teleconsulta

def test_consultar_historico_paciente_sucesso():
    """Testa se a tool retorna os dados de um paciente mockado corretamente."""
    resultado = consultar_historico_paciente(paciente_id="12345")
    
    # Verifica se o retorno é uma string (conforme o esperado pelo LangGraph/LLM)
    assert isinstance(resultado, str)
    # Verifica se a string contém palavras-chave que deveriam estar no histórico
    assert "idade" in resultado.lower() or "comorbidades" in resultado.lower()

def test_verificar_interacoes_medicamentosas_com_risco():
    """Testa se a tool identifica uma interação grave simulada."""
    resultado = verificar_interacoes_medicamentosas(
        medicamentos_em_uso=["Losartana"],
        novo_medicamento="Ibuprofeno"
    )
    
    assert isinstance(resultado, str)
    assert "interação" in resultado.lower() or "risco" in resultado.lower()

def test_agendar_teleconsulta_falta_dados():
    """Testa como a tool se comporta ao não receber todos os parâmetros."""
    # Aqui depende de como você implementou a tool. Se ela levanta um erro ou retorna string:
    with pytest.raises(Exception):
         agendar_teleconsulta(paciente_id="12345", especialidade=None, urgencia="rotina")