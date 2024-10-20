# services/openai_service.py

"""
OpenAI Service Module
=====================

Este módulo fornece serviços para simplificar e, opcionalmente, resumir textos utilizando a API da OpenAI.
Ele gerencia a autenticação com a OpenAI, inicializa o cliente de tradução e executa a simplificação de textos
com base nos parâmetros fornecidos.

Classes:
    OpenAIService: Classe responsável pela interação com a API da OpenAI para simplificação de textos.

Dependências:
    - boto3: Biblioteca da AWS para interagir com os serviços da AWS.
    - dotenv: Biblioteca para carregar variáveis de ambiente a partir de um arquivo .env.
    - openai: Biblioteca oficial da OpenAI para interagir com a API OpenAI.
    - os: Biblioteca padrão para interagir com o sistema operacional.
    - time: Biblioteca padrão para manipulação de tempo.
    - random: Biblioteca padrão para geração de números aleatórios.
    - typing: Biblioteca padrão para anotações de tipos.

Exemplo de Uso:
    >>> from services.openai_service import OpenAIService
    >>> openai_service = OpenAIService()
    >>> texto_original = "This is a complex technical document."
    >>> texto_simplificado = openai_service.simplify_text(
    ...     text=texto_original,
    ...     area_tecnica="Computer Science",
    ...     estilo="informal",
    ...     summarize=True,
    ...     model="gpt-4"
    ... )
    >>> print(texto_simplificado)
    "This is a simplified version of the original technical document, making it easier to understand for non-experts."
"""

import os
import time
import random
from dotenv import load_dotenv
import openai


class OpenAIService:
    """
    Serviço para simplificar (e opcionalmente resumir) textos utilizando a API da OpenAI.

    Esta classe gerencia a autenticação com a OpenAI, inicializa o cliente de tradução
    e fornece métodos para simplificar textos de acordo com parâmetros específicos.

    Métodos:
        simplify_text(text: str, area_tecnica: str, estilo: str, summarize: bool, model: str) ⇾ str:
            Simplifica (e opcionalmente resume) o texto fornecido utilizando o modelo especificado da OpenAI.
    """

    def __init__(self):
        """
        Inicializa a instância do OpenAIService.

        Este metodo realiza os seguintes passos:
            1. Carrega as credenciais da OpenAI a partir do arquivo .env.
            2. Inicializa o cliente OpenAI com as credenciais carregadas.

        Exceções:
            - ValueError: Se a chave da API OpenAI estiver faltando no arquivo .env.
            - ConnectionError: Se houver falha ao inicializar o cliente OpenAI.
        """
        self.OPENAI_API_KEY = None
        self.client = None  # Instância do cliente OpenAI

        # Carrega as credenciais OpenAI
        self.load_credentials()

        # Inicializa o cliente OpenAI
        self.init_openai_client()

    def load_credentials(self) -> None:
        """
        Carrega as credenciais OpenAI do arquivo .env.

        Este metodo realiza os seguintes passos:
            1. Carrega as variáveis de ambiente a partir do arquivo .env.
            2. Obtém a chave da API OpenAI (`OPENAI_API_KEY`) das variáveis de ambiente.
            3. Verifica se a chave da API está presente; caso contrário, lança uma exceção.

        Exceções:
            - ValueError: Se a chave da API OpenAI estiver faltando no arquivo .env.

        Teoria:
            - As credenciais da OpenAI são necessárias para autenticar e autorizar solicitações à API OpenAI.
            - É uma prática recomendada armazenar credenciais sensíveis em arquivos de ambiente (.env) para evitar exposição acidental.
        """
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

        if not self.OPENAI_API_KEY:
            raise ValueError("Chave da API OpenAI faltando. Por favor, verifique o arquivo .env.")

    def init_openai_client(self):
        """
        Inicializa o cliente OpenAI.

        Este metodo utiliza a chave da API carregada para configurar a biblioteca OpenAI,
        que será utilizada para realizar chamadas à API de simplificação de textos.

        Exceções:
            - ConnectionError: Se houver falha ao inicializar o cliente OpenAI devido a credenciais inválidas
              ou problemas de conexão.

        Teoria:
            - A biblioteca OpenAI utiliza a chave da API para autenticar solicitações e garantir que o usuário
              tenha permissão para acessar os serviços da OpenAI.
        """
        try:
            openai.api_key = self.OPENAI_API_KEY
            self.client = openai
        except Exception as e:
            raise ConnectionError(f"Falha ao inicializar o cliente OpenAI: {str(e)}")

    def simplify_text(
            self,
            text: str,
            area_tecnica: str,
            estilo: str,
            summarize: bool,
            model: str
    ) -> str:
        """
        Simplifica (e opcionalmente resume) o texto fornecido usando a API da OpenAI.

        Este metodo realiza os seguintes passos:
            1. Define o prompt com base nos parâmetros fornecidos.
            2. Faz uma chamada à API OpenAI ChatCompletion para obter o texto simplificado.
            3. Implementa uma lógica de retry para lidar com possíveis falhas temporárias na API.

        Parâmetros:
            text (str): O texto a ser simplificado.
            area_tecnica (str): A área técnica do texto (e.g., "Computer Science", "Medicine").
            estilo (str): O estilo de escrita desejado (e.g., "informal", "formal", "casual").
            summarize (bool): Indica se o texto deve ser resumido além de ser simplificado.
            model (str): O modelo da OpenAI a ser utilizado (e.g., "gpt-4", "gpt-3.5-turbo").

        Retorna:
            str: O texto simplificado (e opcionalmente resumido) retornado pela API da OpenAI.

        Exceções:
            - Exception: Se ocorrer um erro durante a comunicação com a API OpenAI após várias tentativas.

        Teoria:
            - A OpenAI utiliza modelos de linguagem avançados para gerar texto de forma contextualizada e adaptada às instruções fornecidas.
            - A simplificação de texto envolve reescrever o conteúdo de maneira mais acessível, mantendo a essência das informações.
            - A funcionalidade de sumarização reduz o texto mantendo os pontos-chave, facilitando a compreensão rápida do conteúdo.
        """
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
                response = self.client.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    max_tokens=4096,
                    temperature=0.8,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                return response.choices[0].message['content'].strip()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Erro ao simplificar o texto após várias tentativas: {str(e)}")
                else:
                    wait_time = 2 ** attempt + random.uniform(0, 1)
                    time.sleep(wait_time)
