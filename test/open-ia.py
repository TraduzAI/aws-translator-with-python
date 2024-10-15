import openai
import os
from dotenv import load_dotenv
from openai.error import AuthenticationError, OpenAIError

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da API a partir das variáveis de ambiente
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    print("Chave API não encontrada. Verifique o arquivo .env.")
    exit(1)

try:
    # Exemplo de solicitação simples
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": "Escreva um haicai sobre programação."}
        ]
    )
    print("Chave API válida. Resposta do modelo:")
    print(response.choices[0].message['content'])

except AuthenticationError:
    print("Falha na autenticação. Verifique se a sua chave API está correta.")
except OpenAIError as e:
    print(f"Ocorreu um erro ao se comunicar com a API da OpenAI: {e}")
