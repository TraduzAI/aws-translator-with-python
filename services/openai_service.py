import os
import time
import random
from dotenv import load_dotenv
from openai import OpenAI


class OpenAIService:
    def __init__(self):
        self.openai_client = None
        self.OPENAI_API_KEY = None

        # Carrega as credenciais OpenAI
        self.load_credentials()

        # Inicializa o cliente OpenAI
        self.init_openai_client()

    def load_credentials(self) -> None:
        """Carrega as credenciais OpenAI do arquivo .env."""
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

        # Verifica se a chave da API está presente
        if not self.OPENAI_API_KEY:
            raise ValueError("Chave da API OpenAI faltando. Por favor, verifique o arquivo .env.")

    def init_openai_client(self):
        """Inicializa o cliente OpenAI."""
        try:
            self.openai_client = OpenAI(api_key=self.OPENAI_API_KEY)
        except Exception as e:
            raise ConnectionError(f"Falha ao inicializar o cliente OpenAI: {str(e)}")

    def simplify_text(self, text: str, area_tecnica: str, estilo: str) -> str:
        """Simplifica o texto usando a API da OpenAI."""
        messages = [
            {"role": "system", "content": f"Você é um especialista em {area_tecnica}."},
            {
                "role": "user",
                "content": f"Reescreva o seguinte texto em um estilo {estilo}, tornando-o acessível para pessoas leigas:\n\nTexto: {text}"
            }
        ]

        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Erro ao simplificar o texto após várias tentativas: {str(e)}")
                else:
                    wait_time = 2 ** attempt + random.uniform(0, 1)
                    time.sleep(wait_time)
