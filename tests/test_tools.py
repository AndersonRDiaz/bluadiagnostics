from src.tools.consultar_historico import consultar_historico_paciente

def test_consultar_historico():
    resultado = consultar_historico_paciente.invoke({"paciente_id": "987654321"})
    assert "Maria" in resultado
    print("✅ Teste de Ferramenta: Passou!")

if __name__ == "__main__":
    test_consultar_historico()