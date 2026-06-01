from typing import Annotated, TypedDict, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class BluaState(TypedDict):
    """
    Representa o estado compartilhado (memória) do agente BluaDiagnostics.
    """
    messages: Annotated[list[BaseMessage], add_messages]
    
    # CONTEXTO CLÍNICO E DE NEGÓCIO
    paciente_id: Optional[str]
    sintomas_coletados: List[str]
    
    # --- NOVO: REQUISITO DO RAG ---
    contexto_rag: List[str] 
    
    # GUARDRAILS
    red_flag_detectada: bool
    red_flag_detalhes: Optional[dict]
    
    # CONTROLE DE ROTEAMENTO (LANGGRAPH)
    proximo_agente: str
    
    # --- NOVO: CONTROLE DE TOOLS ---
    agente_ativo: str # Guarda qual agente (Triagem ou Prescricao) chamou a tool