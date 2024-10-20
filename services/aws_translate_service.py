# services/aws_translate_service.py

"""
AWS Translate Service Module
============================

Este módulo fornece serviços para traduzir textos utilizando a API AWS Translate.
Ele gerencia a autenticação com a AWS, inicializa o cliente de tradução e executa
a tradução de textos para o idioma de destino especificado.

Classes:
    AwsTranslateService: Classe responsável pela tradução de textos usando AWS Translate.

Dependências:
    - boto3: Biblioteca da AWS para interagir com os serviços da AWS.
    - dotenv: Biblioteca para carregar variáveis de ambiente a partir de um arquivo .env.
    - os: Biblioteca padrão para interagir com o sistema operacional.

Exemplo de Uso:
    >>> from services.aws_translate_service import AwsTranslateService
    >>> translator = AwsTranslateService()
    >>> texto = "Hello, how are you?"
    >>> texto_traduzido = translator.translate_text(texto, 'pt')
    >>> print(texto_traduzido)
    "Olá, como você está?"
"""

import boto3
import os
from dotenv import load_dotenv


class AwsTranslateService:
    """
    Serviço para traduzir textos utilizando a API AWS Translate.

    Esta classe gerencia a autenticação com a AWS, inicializa o cliente de tradução
    e fornece métodos para traduzir textos para diferentes idiomas de destino.

    Métodos:
        translate_text(text: str, target_language_code: str) ⇾ str:
            Traduz o texto fornecido para o idioma de destino especificado.
    """

    def __init__(self):
        """
        Inicializa a instância do AwsTranslateService.

        Este metodo realiza os seguintes passos:
            1. Carrega as credenciais da AWS a partir do arquivo .env.
            2. Inicializa o cliente AWS Translate usando as credenciais carregadas.

        Exceções:
            - ValueError: Se alguma das credenciais da AWS estiver faltando no arquivo .env.
            - ConnectionError: Se houver falha ao inicializar o cliente AWS Translate.
        """
        self.translate_client = None
        self.ACCESS_KEY = None
        self.SECRET_KEY = None
        self.REGION = None

        # Carrega as credenciais AWS
        self.load_credentials()

        # Inicializa o cliente AWS Translate
        self.init_translate_client()

    def load_credentials(self) -> None:
        """
        Carrega as credenciais AWS do arquivo .env.

        Este metodo realiza os seguintes passos:
            1. Carrega as variáveis de ambiente a partir do arquivo .env.
            2. Obtém as credenciais AWS (ACCESS_KEY_ID, SECRET_ACCESS_KEY, REGION) das variáveis de ambiente.
            3. Verifica se todas as credenciais estão presentes; caso contrário, lança uma exceção.

        Exceções:
            - ValueError: Se alguma das credenciais da AWS estiver faltando no arquivo .env.

        Teoria:
            - As credenciais AWS são necessárias para autenticar e autorizar solicitações à API AWS Translate.
            - É uma prática recomendada armazenar credenciais sensíveis em arquivos de ambiente (.env) para evitar exposição acidental.
        """
        load_dotenv()
        self.ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', '')
        self.SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
        self.REGION = os.getenv('AWS_REGION', '')

        # Verifica se todas as credenciais estão presentes
        if not all([self.ACCESS_KEY, self.SECRET_KEY, self.REGION]):
            raise ValueError("Credenciais AWS faltando. Por favor, verifique o arquivo .env.")

    def init_translate_client(self):
        """
        Inicializa o cliente AWS Translate.

        Este metodo utiliza as credenciais carregadas para criar um cliente AWS Translate
        que será utilizado para realizar as traduções de textos.

        Exceções:
            - ConnectionError: Se houver falha ao inicializar o cliente AWS Translate devido a credenciais inválidas
              ou problemas de rede.

        Teoria:
            - O cliente AWS Translate gerencia as solicitações de tradução, incluindo a autenticação e comunicação
              com o serviço AWS Translate.
        """
        try:
            self.translate_client = boto3.client(
                service_name='translate',
                region_name=self.REGION,
                aws_access_key_id=self.ACCESS_KEY,
                aws_secret_access_key=self.SECRET_KEY
            )
        except Exception as e:
            raise ConnectionError(f"Falha ao inicializar o cliente AWS Translate: {str(e)}")

    def translate_text(self, text: str, target_language_code: str) -> str:
        """
        Traduz o texto fornecido para o idioma de destino especificado.

        Este metodo realiza os seguintes passos:
            1. Utiliza o cliente AWS Translate para traduzir o texto.
            2. Retorna o texto traduzido.

        Parâmetros:
            text (str): O texto a ser traduzido.
            target_language_code (str): Código do idioma de destino (e.g., 'pt' para Português, 'es' para espanhol).

        Retorna:
            str: O texto traduzido para o idioma de destino.

        Exceções:
            - Exception: Se ocorrer um erro durante a tradução, como um código de idioma inválido ou problemas de rede.

        Teoria:
            - AWS Translate é um serviço de tradução automática baseado em aprendizado de máquina que suporta múltiplos idiomas.
            - O parâmetro 'SourceLanguageCode' está definido como 'auto' para permitir que o serviço detecte automaticamente o idioma de origem.
            - 'TargetLanguageCode' especifica o idioma para o qual o texto será traduzido.
        """
        try:
            response = self.translate_client.translate_text(
                Text=text,
                SourceLanguageCode='auto',  # Detecta automaticamente o idioma do texto de origem
                TargetLanguageCode=target_language_code
            )
            return response['TranslatedText']
        except Exception as e:
            raise Exception(f"Erro na tradução: {str(e)}")
