from langchain_core.tools import tool
import json
import random
from src.tools.schemas import AgendarTeleconsultaSchema

@tool(args_schema=AgendarTeleconsultaSchema)
def agendar_teleconsulta(paciente_id: str, especialidade: str, urgencia: str) -> str:
    """
    Agenda uma teleconsulta médica na especialidade indicada para o beneficiário.
    Use esta ferramenta APENAS QUANDO o paciente solicitar ativamente o agendamento de uma consulta 
    ou quando o protocolo de triagem exigir a escalação para um médico humano.
    """
    print(f"⚙️ [TOOL] Agendando {especialidade} ({urgencia}) para o ID: {paciente_id}...")
    
    # Simulando um agendamento bem-sucedido
    return json.dumps({
        "status": "SUCESSO",
        "mensagem": f"Teleconsulta agendada com a especialidade {especialidade} para o seu benefício.",
        "id_beneficiario": paciente_id,
        "tipo_consulta": urgencia
    }, ensure_ascii=False)

