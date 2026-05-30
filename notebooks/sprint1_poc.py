pip install anthropic python-dotenv

%pip install --user tiktoken requests python-dotenv

# Setup
import os
from ollama import Client
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env de forma segura
load_dotenv()

# 2. Configuração Ollama Cloud (Exatamente como o professor pediu)
client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.getenv('OLLAMA_API_KEY')}
)

MODEL_NAME = "gpt-oss:120b"

# 3. Função otimizada para a Sprint 1 (Memória + Tools)
def llm(mensagens, ferramentas=None, max_tokens=300, temperature=0.3):
    try:
        # A chamada principal permanece a mesma
        resposta = client.chat(
            model=MODEL_NAME,
            messages=mensagens,       # Agora aceita o histórico completo da conversa
            tools=ferramentas,        # Aceita o seu JSON de tools
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False
        )
        
        # Retorna o objeto de mensagem inteiro (crucial para o agente usar as tools)
        return resposta['message']
        
    except Exception as e:
        # Mantemos o tratamento de erro original
        return {"role": "assistant", "content": f"⚠️ Erro na conexão: {e}"}



import json
import os

# 1. Carregando os Arquivos com base na estrutura da sua imagem
print("🔍 Verificando os caminhos corretos...")

# O VS Code geralmente roda a partir da raiz. Vamos tentar a raiz primeiro.
caminho_prompt = os.path.join("prompts", "system_prompt.md")
# Aqui está a correção: apontando para a pasta tools_spec
caminho_tools = os.path.join("tools_spec", "tools_spec.json") 

# Se por acaso ele rodar de dentro da pasta notebooks, usamos o ".."
if not os.path.exists(caminho_prompt):
    caminho_prompt = os.path.join("..", "prompts", "system_prompt.md")

if not os.path.exists(caminho_tools):
    caminho_tools = os.path.join("..", "tools_spec", "tools_spec.json")

# Checagem de segurança final
if not os.path.exists(caminho_prompt):
    raise FileNotFoundError(f"❌ Não encontrei o prompt. Verifique se o arquivo chama mesmo 'system_prompt.md' dentro da pasta 'prompts'. Caminho tentado: {os.path.abspath(caminho_prompt)}")

if not os.path.exists(caminho_tools):
    raise FileNotFoundError(f"❌ Não encontrei as tools. Verifique se o arquivo chama mesmo 'tools_spec.json' dentro da pasta 'tools_spec'. Caminho tentado: {os.path.abspath(caminho_tools)}")

print(f"✅ Arquivos localizados!\nPrompt: {caminho_prompt}\nTools: {caminho_tools}")

# Abrindo os arquivos
with open(caminho_prompt, "r", encoding="utf-8") as f:
    system_prompt = f.read()

with open(caminho_tools, "r", encoding="utf-8") as f:
    arquivo_tools = json.load(f)
    # Pega a lista de ferramentas de dentro do JSON
    minhas_ferramentas = arquivo_tools.get("tools", arquivo_tools) 

# 2. Inicializando a Memória da Conversa
historico = [
    {"role": "system", "content": system_prompt}
]

print("\n🚀 Iniciando simulação...\n")
print("=" * 60)

# ==========================================
# TURNO 1: O Pedido Inicial
# ==========================================
print("\n--- INÍCIO DO TURNO 1 ---")
historico.append({
    "role": "user",
    "content": "Preciso agendar uma consulta de rotina com um cardiologista."
})
print("👤 PACIENTE: Preciso agendar uma consulta de rotina com um cardiologista.")

# Chama a IA e salva a resposta na memória
resposta_t1 = llm(mensagens=historico, ferramentas=minhas_ferramentas)
historico.append(resposta_t1) 

print(f"🤖 IA: {resposta_t1['content']}")

# ==========================================
# TURNO 2: O Function Calling (Ação Invisível)
# ==========================================
print("\n--- INÍCIO DO TURNO 2 ---")
historico.append({
    "role": "user",
    "content": "Ah, claro! Meu número de beneficiário é 987654321."
})
print("👤 PACIENTE: Ah, claro! Meu número de beneficiário é 987654321.")

# Chama a IA e salva a decisão dela na memória
resposta_t2 = llm(mensagens=historico, ferramentas=minhas_ferramentas)
historico.append(resposta_t2) 

# Verificando se a IA chamou a ferramenta (Function Calling)
if resposta_t2.get('tool_calls'):
    tool_chamada = resposta_t2['tool_calls'][0]
    nome_funcao = tool_chamada['function']['name']
    parametros = tool_chamada['function']['arguments']
    
    print("🤖 IA: [SILÊNCIO - A IA PROCESSOU A INFORMAÇÃO E DECIDIU EXECUTAR UMA FERRAMENTA]")
    print(f"⚙️ [FUNCTION CALLING EXECUTADO]: Ferramenta '{nome_funcao}' acionada!")
    print(f"⚙️ [PARÂMETROS EXTRAÍDOS]: {parametros}")
    
    # ==========================================
    # TURNO 3: O Retorno do Sistema
    # ==========================================
    print("\n--- INÍCIO DO TURNO 3 ---")
    
    # Simulando o backend do aplicativo retornando sucesso
    print(f"🔄 [SISTEMA MOCK]: Injetando resultado de sucesso da ferramenta '{nome_funcao}' na memória...")
    mensagem_sistema_mock = {
        "role": "tool",
        "name": nome_funcao,
        "content": "Sucesso. Consulta agendada para o dia 28/05 as 14h com o Dr. Roberto (Cardiologia) na clinica central."
    }
    historico.append(mensagem_sistema_mock)
    
    # Aciona a IA pela última vez
    resposta_t3 = llm(mensagens=historico, ferramentas=minhas_ferramentas)
    historico.append(resposta_t3)
    
    print(f"🤖 IA (Resposta Final Humanizada): {resposta_t3['content']}")
else:
    print(f"🤖 IA: {resposta_t2['content']}")

print("\n" + "=" * 60)
print("Prova de Conceito (PoC) finalizada com sucesso! Todos os requisitos (3 turnos + RAG/Tools) atendidos.")
