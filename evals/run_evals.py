import json
import time
import os
from langchain_core.messages import HumanMessage
from src.graph.builder import compilar_grafo

def rodar_avaliacoes():
    app = compilar_grafo()
    
    # Pega a pasta onde o run_evals.py está (evals/) independente de onde foi chamado
    pasta_evals = os.path.dirname(os.path.abspath(__file__))
    caminho_json_entrada = os.path.join(pasta_evals, "sprint1_eval_set.json")
    caminho_json_saida = os.path.join(pasta_evals, "sprint2_results.json")
    
    with open(caminho_json_entrada, "r", encoding="utf-8") as f:
        testes = json.load(f)
    
    resultados_detalhados = []
    metricas = {
        "total_testes": len(testes),
        "tempo_total_segundos": 0,
        "categorias_avaliadas": {}
    }
    
    for teste in testes:
        entrada = teste["entrada_usuario"] 
        categoria = teste["categoria"]
        id_teste = teste["id"]
        
        if categoria not in metricas["categorias_avaliadas"]:
            metricas["categorias_avaliadas"][categoria] = {"processados": 0}
            
        config = {"configurable": {"thread_id": f"test_{id_teste}"}}
        
        start_time = time.time()
        res = app.invoke({"messages": [HumanMessage(content=entrada)]}, config)
        end_time = time.time()
        
        tempo_resposta = round(end_time - start_time, 2)
        metricas["tempo_total_segundos"] += tempo_resposta
        metricas["categorias_avaliadas"][categoria]["processados"] += 1
        
        saida = res["messages"][-1].content
        
        resultados_detalhados.append({
            "id": id_teste,
            "categoria": categoria,
            "entrada": entrada,
            "saida_obtida": saida,
            "tempo_resposta_s": tempo_resposta
        })
        print(f"✅ [{id_teste}] Processado em {tempo_resposta}s")
    
    metricas["tempo_medio_resposta_s"] = round(metricas["tempo_total_segundos"] / metricas["total_testes"], 2)
    metricas["custo_estimado_usd"] = 0.0
    
    relatorio_final = {
        "metricas_quantitativas": metricas,
        "resultados_detalhados": resultados_detalhados
    }
    
    with open(caminho_json_saida, "w", encoding="utf-8") as f:
        json.dump(relatorio_final, f, indent=4, ensure_ascii=False)
        
    print("🏆 Avaliações concluídas! Métricas geradas em evals/sprint2_results.json")