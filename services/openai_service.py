import os
import time
import random
from dotenv import load_dotenv
from openai import OpenAI


class OpenAIService:
    def __init__(self):
        self.OPENAI_API_KEY = None
        self.client = None  # Instância do cliente OpenAI

        # Carrega as credenciais OpenAI
        self.load_credentials()

        # Inicializa o cliente OpenAI
        self.init_openai_client()

    def load_credentials(self) -> None:
        """Carrega as credenciais OpenAI do arquivo .env."""
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

        if not self.OPENAI_API_KEY:
            raise ValueError("Chave da API OpenAI faltando. Por favor, verifique o arquivo .env.")

    def init_openai_client(self):
        """Inicializa o cliente OpenAI."""
        try:
            self.client = OpenAI(api_key=self.OPENAI_API_KEY)
        except Exception as e:
            raise ConnectionError(f"Falha ao inicializar o cliente OpenAI: {str(e)}")

    def simplify_text(self, text: str, area_tecnica: str, estilo: str, summarize: bool, model: str) -> str:
        """Simplifica (e opcionalmente resume) o texto usando a API da OpenAI com o modelo selecionado."""
        if summarize:
            # Prompt para simplificar e resumir
            messages = [
                {
                    "role": "system",
                    "content": (
                        f"Você é um especialista em {area_tecnica}. Seu objetivo é tornar conceitos dessa área "
                        f"mais acessíveis a pessoas leigas, resumindo o conteúdo sem perder informações essenciais."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Por favor, resuma e reescreva o seguinte texto de forma simples e clara, "
                        f"utilizando um estilo {estilo}. Garanta que o resumo seja fácil de entender, "
                        f"removendo termos técnicos complexos e usando linguagem cotidiana:\n\nTexto: {text}"
                    )
                }
            ]
        else:
            # Prompt para apenas simplificar sem resumir
            messages = [
                {
                    "role": "system",
                    "content": (
                        f"Você é um especialista em {area_tecnica}. Seu objetivo é tornar conceitos dessa área "
                        f"mais acessíveis a pessoas leigas."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Por favor, reescreva o seguinte texto de forma simples e clara, "
                        f"mas mantendo todas as informações originais. "
                        f"O objetivo não é resumir, mas tornar o texto acessível para pessoas que não são especialistas em {area_tecnica}, "
                        f"utilizando um estilo {estilo}. Garanta que o conteúdo seja fácil de entender, "
                        f"removendo termos técnicos complexos e usando linguagem cotidiana:\n\nTexto: {text}"
                    )
                }
            ]

        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=1000,
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
