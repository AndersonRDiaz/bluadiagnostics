from langchain_core.tools import tool
import json
from src.tools.schemas import ConsultarHistoricoSchema

BANCO_DE_DADOS_PACIENTES = {
    "987654321": {
        "nome": "Maria",
        "idade": 34,
        "comorbidades": ["Hipertensão"],
        "medicacoes_em_uso": ["Losartana 50mg"],
        "ultimas_consultas": ["03/2026 com Dr. João (Cardiologia)"]
    },
    "111222333": {
        "nome": "João",
        "idade": 67,
        "comorbidades": ["Diabetes Tipo 2"],
        "medicacoes_em_uso": ["Metformina 850mg", "Insulina Glargina"],
        "ultimas_consultas": ["01/2026 com Dra. Silva (Endocrinologia)"]
    }
}

@tool(args_schema=ConsultarHistoricoSchema)
def consultar_historico_paciente(paciente_id: str, janela_meses: int = 12) -> str:
    """
    Busca o histórico clínico completo do paciente na base da Care Plus.
    Use esta ferramenta SEMPRE que precisar saber a idade, comorbidades ou 
    medicações que o paciente já toma antes de fazer qualquer prescrição ou triagem.
    """
    print(f"⚙️ [TOOL] Buscando histórico do paciente ID: {paciente_id} (Janela: {janela_meses} meses)...")
    
    paciente = BANCO_DE_DADOS_PACIENTES.get(paciente_id)
    
    if paciente:
        return json.dumps(paciente, ensure_ascii=False)
    else:
        return json.dumps({"erro": "Paciente não encontrado na base de dados da Care Plus."}, ensure_ascii=False)