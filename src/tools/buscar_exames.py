from langchain_core.tools import tool
import json
from pydantic import BaseModel

class BuscarExamesSchema(BaseModel):
    paciente_id: str
    tipo_exame: str = "todos"

EXAMES_PACIENTES = {
    "987654321": [
        {"data": "03/2026", "tipo": "Hemograma", "resultado": "Normal", "medico": "Dr. João"},
        {"data": "03/2026", "tipo": "Glicemia em jejum", "resultado": "92 mg/dL (Normal)", "medico": "Dr. João"},
        {"data": "03/2026", "tipo": "Pressão arterial", "resultado": "138/88 mmHg (Limítrofe)", "medico": "Dr. João"}
    ],
    "111222333": [
        {"data": "01/2026", "tipo": "HbA1c", "resultado": "7.8% (Elevado)", "medico": "Dra. Silva"},
        {"data": "01/2026", "tipo": "Glicemia em jejum", "resultado": "145 mg/dL (Elevado)", "medico": "Dra. Silva"},
        {"data": "01/2026", "tipo": "Creatinina", "resultado": "1.1 mg/dL (Normal)", "medico": "Dra. Silva"}
    ],
    "444555666": [
        {"data": "12/2025", "tipo": "Hemograma", "resultado": "Normal", "medico": "Dr. Pedro"},
        {"data": "12/2025", "tipo": "TSH", "resultado": "2.1 mUI/L (Normal)", "medico": "Dr. Pedro"}
    ],
    "777888999": [
        {"data": "02/2026", "tipo": "Espirometria", "resultado": "VEF1 78% (Leve obstrução)", "medico": "Dra. Costa"},
        {"data": "02/2026", "tipo": "Peak Flow", "resultado": "420 L/min (Abaixo do esperado)", "medico": "Dra. Costa"}
    ],
    "321654987": [
        {"data": "04/2026", "tipo": "TSH", "resultado": "6.2 mUI/L (Elevado)", "medico": "Dr. Ramos"},
        {"data": "04/2026", "tipo": "T4 Livre", "resultado": "0.8 ng/dL (Baixo)", "medico": "Dr. Ramos"}
    ]
}

@tool(args_schema=BuscarExamesSchema)
def buscar_exames_paciente(paciente_id: str, tipo_exame: str = "todos") -> str:
    """
    Busca os exames laboratoriais e clínicos recentes do paciente na base Care Plus.
    Use quando o paciente mencionar resultados de exames ou quiser saber seus últimos resultados.
    """
    paciente_id_limpo = str(paciente_id).strip().replace(".", "").replace("-", "").replace(" ", "")
    print(f"⚙️ [TOOL] Buscando exames do paciente ID: {paciente_id_limpo}...")

    exames = EXAMES_PACIENTES.get(paciente_id_limpo)

    if not exames:
        return json.dumps({"erro": "Nenhum exame encontrado para este paciente."}, ensure_ascii=False)

    if tipo_exame != "todos":
        exames = [e for e in exames if tipo_exame.lower() in e["tipo"].lower()]

    return json.dumps({"exames": exames}, ensure_ascii=False)