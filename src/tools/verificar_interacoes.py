from langchain_core.tools import tool
import json

@tool
def verificar_interacoes_medicamentosas(medicamentos_em_uso: list[str], novo_medicamento: str) -> str:
    """Verifica interacoes entre uma lista de farmacos e um novo medicamento."""
    print(f"⚙️ [TOOL] Analisando interações: {medicamentos_em_uso} + {novo_medicamento}...")
    
    novo_med_lower = novo_medicamento.lower()
    em_uso_lower = [m.lower() for m in medicamentos_em_uso]
    
    # Regra de negócio 1: Losartana + AINEs (Ibuprofeno/Diclofenaco)
    if "ibuprofeno" in novo_med_lower or "diclofenaco" in novo_med_lower:
        if any("losartana" in m for m in em_uso_lower):
            return json.dumps({
                "status": "ALERTA_GRAVE",
                "mensagem": "O uso de anti-inflamatórios (AINEs) com Losartana pode reduzir o efeito anti-hipertensivo e causar agravamento renal."
            }, ensure_ascii=False)
            
    # Regra genérica (Sem interações conhecidas no Mock)
    return json.dumps({
        "status": "SEGURO",
        "mensagem": "Nenhuma interação grave identificada no banco de dados para esta combinação."
    }, ensure_ascii=False)
