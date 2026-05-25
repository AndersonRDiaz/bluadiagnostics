from langchain_core.tools import tool
import json
import random

@tool
def agendar_teleconsulta(paciente_id: str, especialidade: str, urgencia: str) -> str:
    """Agenda teleconsulta na especialidade indicada para o beneficiario."""
    print(f"⚙️ [TOOL] Agendando {especialidade} ({urgencia}) para o ID {paciente_id}...")
    
    # Validando se o ID existe (opcional, para dar mais realismo)
    if paciente_id not in ["987654321", "111222333"]:
        return json.dumps({"erro": "ID Inválido. Não foi possível agendar."})
        
    # Gera um número de protocolo falso
    protocolo = f"CP-{random.randint(10000, 99999)}"
    
    return json.dumps({
        "status": "SUCESSO",
        "protocolo": protocolo,
        "mensagem": f"Consulta de {especialidade} agendada com sucesso.",
        "data_hora_sugerida": "Amanhã às 14:30"
    }, ensure_ascii=False)

