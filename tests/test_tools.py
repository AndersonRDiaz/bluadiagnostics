from src.tools.consultar_historico import consultar_historico_paciente

def test_consultar_historico_paciente_existente():
    """Garante que a ferramenta retorna os dados corretos de um paciente cadastrado."""
    resultado = consultar_historico_paciente.invoke({"paciente_id": "987654321"})
    assert "Maria" in resultado
    assert "Hipertensão" in resultado

def test_consultar_historico_paciente_inexistente():
    """Garante que a ferramenta lida bem com IDs inválidos sem quebrar o sistema."""
    resultado = consultar_historico_paciente.invoke({"paciente_id": "000000000"})
    assert "erro" in resultado.lower() or "não encontrado" in resultado.lower()