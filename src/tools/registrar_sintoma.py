from langchain_core.tools import tool
import json
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class RegistrarSintomaSchema(BaseModel):
    paciente_id: str
    sintoma: str
    intensidade: int
    duracao: Optional[str] = "não informada"

@tool(args_schema=RegistrarSintomaSchema)
def registrar_sintoma_vital(paciente_id: str, sintoma: str, 
                             intensidade: int, duracao: str = "não informada") -> str:
    """
    Registra um sintoma relatado pelo paciente durante a triagem digital.
    Use quando o paciente descrever um sintoma com intensidade mensurável (0-10).
    Isso estrutura os dados para o médico revisar posteriormente.
    """
    try:
        paciente_id_limpo = str(paciente_id).strip().replace(".", "").replace("-", "").replace(" ", "")
        print(f"⚙️ [TOOL] Registrando sintoma para paciente ID: {paciente_id_limpo}...")

        registro = {
            "paciente_id": paciente_id_limpo,
            "sintoma": sintoma,
            "intensidade": intensidade,
            "duracao": duracao,
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "status": "registrado — aguardando revisão médica"
        }

        return json.dumps(registro, ensure_ascii=False)
        
    except Exception as e:
        print(f"❌ [TOOL ERROR] Falha ao registrar sintoma: {str(e)}")
        return json.dumps({
            "erro": f"Erro interno ao salvar sintoma: {str(e)}. Apenas acolha o paciente e continue a avaliação."
        }, ensure_ascii=False)