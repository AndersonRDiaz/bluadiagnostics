import os

def test_carregar_prompts():
    caminho = "prompts/system_prompt.md"
    assert os.path.exists(caminho), "System prompt não encontrado!"
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    assert len(conteudo) > 0
    print("Teste de Prompts: Passou!")

if __name__ == "__main__":
    test_carregar_prompts()