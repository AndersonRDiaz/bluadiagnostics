from typing import Annotated, TypedDict, List, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class BluaState(TypedDict):
    """
    Representa o estado compartilhado (memória) do agente BluaDiagnostics.
    Este objeto viaja por todos os nós (agentes) do LangGraph.
    """
    
    # O histórico de mensagens. 
    # O 'add_messages' é crucial: ele garante que as novas mensagens sejam anexadas, 
    # e não que sobrescrevam as mensagens anteriores.
    messages: Annotated[list[BaseMessage], add_messages]
    
    # ==========================================
    # CONTEXTO CLÍNICO E DE NEGÓCIO
    # ==========================================
    paciente_id: Optional[str]
    sintomas_coletados: List[str]
    
    # O Guardrail principal do sistema
    red_flag_detectada: bool
    
    # NOVO: Guarda os detalhes ricos da emergência (categoria, protocolo, orientação)
    red_flag_detalhes: Optional[dict]
    
    # ==========================================
    # CONTROLE DE ROTEAMENTO (LANGGRAPH)
    # ==========================================
    # Indica qual será o próximo agente a atuar na conversa
    proximo_agente: str