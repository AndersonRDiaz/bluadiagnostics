import pytest
from src.tools.consultar_historico import consultar_historico_paciente
from src.tools.verificar_interacoes import verificar_interacoes_medicamentosas
from src.tools.agendar_teleconsulta import agendar_teleconsulta

def test_consultar_historico_paciente_sucesso():
    """Testa se a tool retorna dados da Maria, 34 anos, hipertensa."""
    resultado = consultar_historico_paciente.invoke({"paciente_id": "987654321"})
    
    assert isinstance(resultado, str)
    assert "erro" not in resultado.lower()
    assert "maria" in resultado.lower()
    assert "losartana" in resultado.lower()

def test_verificar_interacoes_medicamentosas_com_risco():
    """Testa se a tool identifica interação grave Losartana + Ibuprofeno."""
    resultado = verificar_interacoes_medicamentosas.invoke({
        "medicamentos_em_uso": ["Losartana"],
        "novo_medicamento": "Ibuprofeno"
    })
    
    assert isinstance(resultado, str)
    assert "alerta" in resultado.lower()

def test_agendar_teleconsulta_falta_dados():
    """Testa como a tool se comporta ao não receber todos os parâmetros."""
    with pytest.raises(Exception):
        agendar_teleconsulta.invoke({
            "paciente_id": "987654321",
            "especialidade": None,
            "urgencia": "rotina"
        })