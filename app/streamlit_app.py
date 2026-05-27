import sys
import os

# Garante que a raiz do projeto está no path
caminho_atual = os.path.dirname(os.path.abspath(__file__))
raiz = os.path.abspath(os.path.join(caminho_atual, ".."))
if raiz not in sys.path:
    sys.path.insert(0, raiz)

import streamlit as st
import uuid
from langchain_core.messages import HumanMessage
from src.graph.builder import compilar_grafo


# Configuração visual da página
st.set_page_config(page_title="Care Plus - Triagem", page_icon="🩺", layout="centered")
st.title("🩺 Care Plus - Atendimento Virtual")
st.markdown("Bem-vindo ao sistema de triagem inteligente. Como posso ajudar você hoje?")

# Carrega o LangGraph de forma otimizada
@st.cache_resource
def carregar_sistema():
    return compilar_grafo()

app = carregar_sistema()

# Gerenciamento avançado de sessão e memória
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4()) # ID único para não misturar conversas
if "messages" not in st.session_state:
    st.session_state.messages = []
if "emergencia" not in st.session_state:
    st.session_state.emergencia = False

# Sidebar: Ferramenta de apoio para a gravação do vídeo
with st.sidebar:
    st.header("🔧 Controle da Sessão")
    if st.button("🔄 Reiniciar Atendimento"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.emergencia = False
        st.rerun()

# Exibe o histórico de mensagens
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Regra de Negócio: Bloqueia o app se o protocolo de emergência foi ativado
if st.session_state.emergencia:
    st.error("⚠️ Atendimento virtual bloqueado por protocolo de segurança. Por favor, procure atendimento presencial imediatamente.")
else:
    # Caixa de texto normal
    if prompt := st.chat_input("Digite seus sintomas ou dúvidas médicas..."):
        
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Analisando protocolos e histórico..."):
                
                estado_inicial = {"messages": [HumanMessage(content=prompt)]}
                config = {"configurable": {"thread_id": st.session_state.session_id}}
                
                resultado = app.invoke(estado_inicial, config)
                resposta_final = resultado['messages'][-1].content
                
                st.markdown(resposta_final)
                st.session_state.messages.append({"role": "assistant", "content": resposta_final})
                
                # Detecção visual da Escalada: Se o SAMU foi chamado, ativa a trava
                if "192" in resposta_final or "SAMU" in resposta_final.upper():
                    st.session_state.emergencia = True
                    st.rerun() # Recarrega a tela para sumir com a caixa de texto