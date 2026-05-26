from langchain_core.tools import tool
import json
import random

@tool
def agendar_teleconsulta(paciente_id: str, especialidade: str, urgencia: str) -> str:
    """
    Agenda uma teleconsulta médica na especialidade indicada para o beneficiário.
    Use esta ferramenta APENAS QUANDO o paciente solicitar ativamente o agendamento de uma consulta 
    ou quando o protocolo de triagem exigir a escalação para um médico humano.
    """

