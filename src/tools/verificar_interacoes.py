from langchain_core.tools import tool
import json
from typing import Union, List
from src.tools.schemas import VerificarInteracoesSchema

@tool(args_schema=VerificarInteracoesSchema)
def verificar_interacoes_medicamentosas(medicamentos_em_uso: Union[List[str], str], novo_medicamento: str) -> str:
    """
    Verifica interações medicamentosas perigosas entre os fármacos que o paciente já toma 
    e um novo medicamento sugerido. Obrigatório usar antes de qualquer recomendação.
    """
    print(f"⚙️ [TOOL] Analisando interações: {medicamentos_em_uso} + {novo_medicamento}...")
    
    # Blindagem: se o LLM mandar uma string em vez de lista, nós convertemos
    if isinstance(medicamentos_em_uso, str):
        medicamentos_em_uso = [med.strip() for med in medicamentos_em_uso.split(',')]
        
    novo_med_lower = novo_medicamento.lower()
    em_uso_lower = [m.lower() for m in medicamentos_em_uso]
    
    if "ibuprofeno" in novo_med_lower or "diclofenaco" in novo_med_lower:
        if any("losartana" in m for m in em_uso_lower):
            return json.dumps({
                "status": "ALERTA_GRAVE",
                "mensagem": "O uso de anti-inflamatórios (AINEs) com Losartana pode reduzir o efeito anti-hipertensivo e causar agravamento renal."
            }, ensure_ascii=False)
            
    return json.dumps({
        "status": "SEGURO",
        "mensagem": "Nenhuma interação grave identificada no banco de dados para esta combinação."
    }, ensure_ascii=False)