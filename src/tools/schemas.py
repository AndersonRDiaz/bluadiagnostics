from pydantic import BaseModel, Field

class ConsultarHistoricoSchema(BaseModel):
    """Schema de validação para a busca de histórico clínico."""
    paciente_id: str = Field(
        ..., 
        description="ID numérico do beneficiário na Care Plus (ex: '987654321')."
    )
    janela_meses: int = Field(
        12, 
        description="Tempo retroativo em meses para buscar o histórico. O padrão é 12."
    )

class VerificarInteracoesSchema(BaseModel):
    """Schema de validação para checagem de risco medicamentoso."""
    medicamentos_em_uso: list[str] = Field(
        ..., 
        description="Lista de strings com os nomes dos medicamentos que o paciente já utiliza."
    )
    novo_medicamento: str = Field(
        ..., 
        description="O nome do novo fármaco que se deseja verificar a interação."
    )

class AgendarTeleconsultaSchema(BaseModel):
    """Schema de validação para o agendamento no sistema."""
    paciente_id: str = Field(
        ..., 
        description="ID do beneficiário na Care Plus."
    )
    especialidade: str = Field(
        ..., 
        description="Especialidade médica desejada (ex: 'Cardiologia', 'Clínica Geral')."
    )
    urgencia: str = Field(
        ..., 
        description="Nível de urgência da consulta. Valores permitidos: 'rotina' ou 'urgencia'."
    )