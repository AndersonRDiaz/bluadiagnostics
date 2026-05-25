import json
from src.graph.builder import compilar_grafo

def rodar_avaliacoes():
    app = compilar_grafo()
    with open("evals/sprint1_eval_set.json", "r", encoding="utf-8") as f:
        testes = json.load(f)
    
    resultados = []
    for teste in testes:
        config = {"configurable": {"thread_id": "test_1"}}
        res = app.invoke({"messages": [{"role": "user", "content": teste["input"]}]}, config)
        resultados.append({"input": teste["input"], "output": res["messages"][-1].content})
    
    with open("evals/sprint2_results.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4)
    print("✅ Avaliações concluídas. Resultados salvos em evals/sprint2_results.json")

if __name__ == "__main__":
    rodar_avaliacoes()