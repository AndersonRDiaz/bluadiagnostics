import os
from dotenv import load_dotenv
from src.graph.state import BluaState
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_community.chat_models import ChatOllama

load_dotenv()

def obter_llm_remoto():
    """Inicializa o modelo gpt-oss:120b apontando para a API externa."""
    return ChatOllama(
        base_url="https://ollama.com",
        model="gpt-oss:120b",
        headers={'Authorization': f"Bearer {os.getenv('OLLAMA_API_KEY')}"},
        temperature=0.1 # Temperatura mínima para garantir a estruturação rígida do relatório
    )

def invocar_prescricao(state: BluaState):
    print("💊 [PRESCRIÇÃO] Compilando histórico e gerando relatório via gpt-oss:120b...")
    
    llm = obter_llm_remoto()
    
    # Formatando o histórico completo de mensagens do estado para enviar ao modelo
    historico_conversas = ""
    for msg in state["messages"]:
        origem = "Paciente" if msg.type == "human" else "Assistente"
        historico_conversas += f"{origem}: {msg.content}\n"
        
    prompt_relatorio = [
        SystemMessage(content=(
            "Você é um assistente médico de retaguarda. Sua tarefa é ler o histórico de uma triagem "
            "e gerar um resumo clínico estruturado contendo: Sintomas Principais, Histórico Informado, "
            "e a Orientação Sugerida. Este documento será revisado por um médico humano."
        )),
        HumanMessage(content=f"Histórico do atendimento:\n{historico_conversas}\n\nGere o resumo estruturado:")
    ]
    
    # Chamada real ao modelo de 120B para sumarização
    relatorio_estruturado = llm.invoke(prompt_relatorio)
    
    mensagem_saida = (
        f"✅ Triagem finalizada com sucesso.\n\n"
        f"📋 **Resumo enviado para análise médica:**\n{relatorio_estruturado.content}\n\n"
        f"Um médico da Care Plus revisará os dados acima e entrará em contato em breve via aplicativo."
    )
    
    return {
        "messages": [AIMessage(content=mensagem_saida)],
        "proximo_agente": "Fim"
    }