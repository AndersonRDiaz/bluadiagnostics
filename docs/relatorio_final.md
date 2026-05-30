# Relatório Técnico Final — Sprint 2
## BluaDiagnostics × Care Plus (Bupa)
**Disciplina:** Prompt and Artificial Intelligence  
**Curso:** Ciência da Computação — 2º Semestre  
**Professor:** Jorge Luiz Gomes  
**Período:** 2026.1

---

## 1. Visão Geral do Projeto

O BluaDiagnostics é um sistema conversacional com inteligência artificial desenvolvido para o aplicativo Blua da Care Plus, operadora de saúde premium integrante do grupo Bupa. O sistema materializa dois pilares estratégicos: o check-up digital proativo e a prescrição remota inteligente, transformando o Blua de uma plataforma reativa em uma plataforma de cuidado remoto proativo.

### 1.1 Persona Atendida

A persona escolhida é o **beneficiário final** — adulto entre 25 e 60 anos que utiliza o app Blua para autoavaliação de sintomas antes de decidir se agenda uma consulta. Esta escolha define o tom acolhedor e a linguagem acessível do agente, além de elevar o perfil de risco clínico, pois o usuário leigo pode minimizar ou exagerar sintomas sem o vocabulário técnico adequado.

### 1.2 Stack Tecnológico

| Camada | Tecnologia | Justificativa |
|---|---|---|
| Orquestração | LangGraph 0.2.70 | Grafos com estado compartilhado e arestas condicionais reais |
| LLM | gpt-oss:120b via Ollama | Modelo local — sem envio de PHI a servidores externos (LGPD) |
| Embeddings | nomic-embed-text via Ollama | 100% local, sem custo, alinhado com privacidade clínica |
| Vector Store | ChromaDB 0.5.23 | Persistência local, zero custo, integração nativa com LangChain |
| Framework | LangChain 0.3.25 | LCEL, output parsers, integração com tools e RAG |
| Interface | Streamlit 1.35.0 | Prototipagem rápida, demonstração visual do fluxo conversacional |
| Validação | Pydantic 2.10.6 | Schemas das tools com tipagem forte |
| Testes | pytest 8.3.5 | Testes unitários das tools e regressão de prompts |

---

## 2. Arquitetura do Sistema

### 2.1 Visão Geral

O sistema é composto por quatro camadas principais que operam em sequência:

1. **Camada de entrada e guardrails** — o Supervisor recebe a mensagem do usuário e aplica validações de escopo, moderação de conteúdo e detecção de red flags antes de qualquer chamada ao LLM.
2. **Camada de orquestração (LangGraph)** — um grafo de estados gerencia o roteamento entre os agentes especializados com base no campo `proximo_agente` do estado compartilhado.
3. **Camada de processamento (RAG + Tools)** — o agente de triagem consulta a base de conhecimento clínica via RAG e aciona tools via function calling quando necessário.
4. **Camada de saída** — as respostas são formatadas com as fontes consultadas e exibidas na interface Streamlit.

### 2.2 Grafo LangGraph

O grafo implementado segue a estrutura `supervisor → [triagem | escalada | prescrição]` com os seguintes nós e arestas:

```
START → Supervisor
Supervisor → Triagem          (caso normal)
Supervisor → Escalada         (red flag detectada)
Supervisor → Prescricao       (intent de prescrição detectada)
Supervisor → END              (out of scope / fim)
Triagem → ExecutadorTools     (quando o LLM decide acionar tools)
Triagem → Supervisor          (loop até decisão final)
ExecutadorTools → Triagem     (retorna resultado das tools para análise)
Escalada → END
Prescricao → END
```

O diferencial em relação a uma pipeline linear é o **ciclo real** entre Triagem, ExecutadorTools e Supervisor, que permite ao agente coletar dados via tools e retomar a triagem com as informações obtidas antes de encerrar.

### 2.3 Estado Compartilhado

```python
class BluaState(TypedDict):
    messages: list              # histórico completo da conversa
    proximo_agente: str         # decisão de roteamento do nó atual
    red_flag_detectada: bool    # flag de emergência clínica
    red_flag_detalhes: dict     # tipo e severidade da red flag
```

---

## 3. Pipeline RAG

### 3.1 Base de Conhecimento

A base de conhecimento clínica contém 20 documentos distribuídos em quatro categorias:

| Categoria | Documentos |
|---|---|
| Bulas | amoxicilina, clonazepam, ibuprofeno, losartana, omeprazol |
| Cartilhas educativas | dengue, diabetes, higiene do sono, hipertensão, saúde mental |
| Políticas Care Plus | escopo da telemedicina, LGPD, prescrições por IA, transferência ao PS, wearables |
| Protocolos clínicos | alergia, cefaleia, dor torácica, gastrointestinal, respiratório |

### 3.2 Estratégia de Chunking

Optou-se por chunks de 1.000 caracteres com overlap de 200 caracteres usando `RecursiveCharacterTextSplitter`. Este tamanho foi escolhido por equilibrar granularidade e contexto clínico: chunks menores perdem o contexto do protocolo, enquanto chunks maiores diluem a relevância semântica na busca por similaridade.

### 3.3 Trade-off: Ollama Embeddings vs OpenAI Embeddings

O grupo avaliou duas opções de embeddings:

| Critério | nomic-embed-text (Ollama) | text-embedding-3-small (OpenAI) |
|---|---|---|
| Custo | Gratuito | Pago por token |
| Privacidade | 100% local — sem envio de dados | Dados enviados a servidores externos |
| Qualidade (recall estimado) | Boa para português clínico | Superior em benchmarks gerais |
| Alinhamento LGPD | Total | Parcial (depende do contrato) |

**Decisão:** nomic-embed-text foi escolhido por ser a opção que melhor se alinha ao contexto Care Plus/Bupa, onde dados de saúde são classificados como dados pessoais sensíveis pela LGPD (art. 5º, II). A perda estimada de recall foi aceita como trade-off consciente em favor da privacidade clínica.

---

## 4. Suite de Tools (Function Calling)

As três tools obrigatórias foram implementadas com retornos simulados realistas baseados em personas sintéticas documentadas:

### 4.1 Personas Sintéticas

- **Maria Silva** (ID: 987654321) — 34 anos, hipertensa, em uso de Losartana 50mg, última consulta em 03/2026 com Dr. João (Cardiologia).
- **João Santos** (ID: 111222333) — 67 anos, diabético tipo 2, em uso de Metformina 850mg e Insulina Glargina, última consulta em 01/2026 com Dra. Silva (Endocrinologia).


### 4.2 Tools Implementadas

**`consultar_historico_paciente`** — retorna o histórico clínico completo do beneficiário incluindo idade, comorbidades, medicações em uso e consultas recentes. O agente aciona esta tool sempre que o usuário menciona medicamentos ou condições pré-existentes.

**`verificar_interacoes_medicamentosas`** — verifica interações entre os medicamentos em uso do paciente e um novo medicamento proposto, retornando severidade (`ALERTA_GRAVE`, `MODERADO`, `NENHUMA`) e recomendações clínicas.

**`agendar_teleconsulta`** — agenda teleconsulta na especialidade indicada com nível de urgência (`rotina`, `urgente`, `emergencia`), retornando data, hora e link simulado de acesso.

---

## 5. Guardrails Clínicos

### 5.1 Arquitetura de Segurança

Os guardrails operam em três níveis:

**Nível 1 — Pré-LLM (Supervisor):** validação de escopo e moderação de conteúdo por palavras-chave antes de qualquer chamada ao modelo. Custo zero — não consome tokens.

**Nível 2 — Red Flag Detection (Supervisor):** varredura da mensagem por um dicionário rico de sintomas de emergência categorizados por tipo (cardíaco, neurológico, respiratório, hemorrágico, anafilático). Quando detectado, roteia imediatamente para o agente de Escalada sem passar pelo LLM.

**Nível 3 — Prompt Engineering (Triagem):** restrições explícitas no system prompt impedem que o LLM faça diagnósticos definitivos, prescreva medicamentos sem aprovação médica ou revele o conteúdo interno do sistema.

### 5.2 Protocolo Human-in-the-Loop (HITL)

O sistema segue o princípio inegociável do BluaDiagnostics: o agente nunca toma decisão clínica final autônoma. Toda prescrição gerada pelo agente de Prescrição é explicitamente marcada como rascunho para revisão médica. Toda triagem com red flag aciona escalada humana imediata e bloqueia o prosseguimento da conversa.

---

## 6. Avaliação Automatizada (Evals)

### 6.1 Resultados Quantitativos

O eval set foi executado automaticamente via `evals/run_evals.py` sobre o sistema final completo. Resultados:

| Categoria | Casos | Acertos | Taxa de Acurácia |
|---|---|---|---|
| red_flag | 5 | 5 | 100% |
| jailbreak | 5 | 5 | 100% |
| happy_path | 5 | 5 | 100% |
| out_of_scope | 5 | 5 | 100% |
| **Total** | **20** | **20** | **100%** |

**Tempo médio de resposta:** 1,70 segundos  
**Custo estimado por conversa:** $0,00 (modelo local via Ollama)

### 6.2 Análise Qualitativa por Categoria

**Red flags:** todos os 5 casos foram interceptados pelo guardrail do Supervisor antes de chegar ao LLM, com tempo de resposta próximo a zero. O sistema orientou corretamente o SAMU 192 e bloqueou o prosseguimento da triagem em todos os casos.

**Jailbreak:** os 5 casos foram bloqueados. O JB-005 (roteiro de filme pedindo dose de insulina) passou pelo agente de Prescrição, que recusou corretamente a dose específica e ofereceu alternativas seguras — comportamento clinicamente adequado mesmo não sendo interceptado no guardrail de entrada.

**Happy path:** o HP-003 (Losartana + Ibuprofeno) acionou automaticamente a tool `verificar_interacoes_medicamentosas` via function calling, demonstrando integração real entre triagem e tools.

**Out of scope:** OS-005 (bolo de cenoura) foi encaminhado ao agente de Prescrição devido à palavra "receita" na lista de palavras-chave — falso positivo identificado. O agente recusou adequadamente, mas o caminho não foi o ideal. Melhoria prevista no roadmap.

### 6.3 Iterações do System Prompt

| Versão | Mudança | Impacto |
|---|---|---|
| v1 | Prompt genérico sem seções | Modelo diagnosticava diretamente — reprovado nos casos jailbreak |
| v2 | Adição das seções PAPEL, ESCOPO, RESTRIÇÕES | Jailbreak bloqueado, mas red flags ainda passavam para o LLM |
| v3 | Red flag detection movida para o Supervisor (pré-LLM) | Red flags com tempo ~0s, sem custo de tokens |
| v4 | Few-shot examples clínicos adicionados | Happy path com respostas mais estruturadas e perguntas de triagem mais completas |

---

## 7. Limitações e Riscos

### 7.1 Limitações Técnicas

- **Falso positivo de prescrição:** palavras como "receita" em contexto culinário ativam o roteamento para o agente de Prescrição. A solução seria usar um classificador de intent mais robusto em vez de palavras-chave simples.
- **Personas sintéticas limitadas:** o banco de dados de pacientes contém apenas 2 personas. Em produção, seria necessário integrar com o sistema real de beneficiários da Care Plus.
- **RAG em português:** o modelo nomic-embed-text tem performance ligeiramente inferior para textos técnicos em português em comparação com modelos treinados especificamente para o idioma.

### 7.2 Riscos Clínicos e Mitigações

| Risco | Mitigação implementada |
|---|---|
| Alucinação clínica | RAG sobre base validada + restrição no prompt + revisão médica obrigatória |
| Diagnóstico definitivo | Restrição explícita no system prompt + casos jailbreak no eval set |
| Subtriagem de red flag | Detecção pré-LLM por dicionário de palavras-chave + escalada automática |
| Vazamento de PHI | Modelo local via Ollama — dados nunca saem da máquina |

### 7.3 LGPD e Privacidade

O sistema foi projetado com as seguintes salvaguardas de dados:

- **Minimização:** o agente solicita apenas o ID do beneficiário, sem coletar dados além do necessário para a triagem em curso.
- **Localidade:** embeddings e inferência do LLM executam 100% localmente via Ollama, sem envio de PHI a servidores externos.
- **Retenção de sessão:** o histórico da conversa é armazenado apenas na memória da sessão (MemorySaver do LangGraph) e descartado ao reiniciar o atendimento.
- **Dados mockados:** todos os dados clínicos utilizados são sintéticos — nenhum dado real de paciente foi utilizado no desenvolvimento.

---

## 8. Roadmap e Próximos Passos

### Melhorias de curto prazo

- Substituir a detecção de intent de prescrição por palavras-chave por um classificador baseado em LLM, eliminando os falsos positivos.
- Expandir a base de conhecimento para 50+ documentos, incluindo protocolos Manchester completos e bulas de medicamentos de uso contínuo mais comuns.
- Adicionar o agente de wearables para integrar dados do Apple Health e Google Fit ao check-up digital.

### Melhorias de médio prazo

- Implementar observabilidade com LangSmith para rastrear traces de cada conversa e identificar padrões de falha.
- Integrar com a API real da Care Plus para substituir as personas sintéticas por dados reais de beneficiários.
- Adicionar suporte multimodal para análise de imagens de exames via visão computacional.

### Melhorias de longo prazo

- Fine-tuning do modelo base com dados clínicos anonimizados da Care Plus para melhorar a qualidade das respostas em português médico.
- Implementação do protocolo MCP (Model Context Protocol) para integração nativa com sistemas externos como prontuário eletrônico e agenda médica.

---

## 9. Conclusão

O BluaDiagnostics Sprint 2 entregou um sistema conversacional clínico completo com RAG funcional, arquitetura multi-agente real via LangGraph, suite de function calling com 3 tools, guardrails clínicos em múltiplos níveis e avaliação automatizada com 100% de acurácia em 20 casos de teste.

A principal contribuição técnica do projeto é a combinação de guardrails pré-LLM (detecção de red flags e escopo por palavras-chave, com custo zero de tokens) com guardrails pós-LLM (restrições no system prompt), criando uma arquitetura de segurança em camadas adequada ao contexto clínico de alta criticidade.

A escolha do modelo local via Ollama representa um posicionamento consciente em favor da privacidade dos dados de saúde, alinhado às exigências da LGPD e às preocupações reais da Care Plus/Bupa com proteção de dados sensíveis de seus 600 mil beneficiários.

---

*Documento gerado como parte do FIAP Challenge 2026.1 — BluaDiagnostics × Care Plus*  
*Disciplina: Prompt and Artificial Intelligence · Professor: Jorge Luiz Gomes*