import os
from dotenv import load_dotenv
import anthropic

# Carrega as variáveis do arquivo .env
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Cria o cliente da Anthropic
client = anthropic.Anthropic(api_key=api_key)

# System prompt — define o comportamento do assistente
SYSTEM_PROMPT = """
Você é um assistente especialista em tecnologia e programação.
Responda sempre em português brasileiro.
Seja direto e objetivo nas respostas.
Quando der exemplos de código, use blocos de código.
"""

# Histórico da conversa — começa vazio
historico = []

print("Chatbot iniciado. Digite 'sair' para encerrar.\n")

# Loop principal
while True:
    user_input = input("Você: ")

    if user_input.lower() == "sair":
        print("Encerrando chatbot. Até mais!")
        break

    historico.append({"role": "user", "content": user_input})

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=historico
        )
        resposta = response.content[0].text

    except anthropic.APIConnectionError:
        print("\n[Erro] Falha de conexão. Verifique sua internet e tente novamente.\n")
        historico.pop()  # remove a mensagem do usuário que não foi respondida
        continue

    except anthropic.AuthenticationError:
        print("\n[Erro] API Key inválida. Verifique o arquivo .env.\n")
        historico.pop()
        continue

    except anthropic.RateLimitError:
        print("\n[Erro] Limite de uso da API excedido. Tente novamente mais tarde.\n")
        historico.pop()
        continue

    except anthropic.APIStatusError as e:
        print(f"\n[Erro] A API retornou um erro: {e.status_code}\n")
        historico.pop()
        continue

    historico.append({"role": "assistant", "content": resposta})
    print(f"\nAssistente: {resposta}\n")