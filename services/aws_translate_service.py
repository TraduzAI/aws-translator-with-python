import boto3
import os
from dotenv import load_dotenv


class AwsTranslateService:
    def __init__(self):
        self.translate_client = None
        self.ACCESS_KEY = None
        self.SECRET_KEY = None
        self.REGION = None

        # Carrega as credenciais AWS
        self.load_credentials()

        # Inicializa o cliente AWS Translate
        self.init_translate_client()

    def load_credentials(self) -> None:
        """Carrega as credenciais AWS do arquivo .env."""
        load_dotenv()
        self.ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', '')
        self.SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
        self.REGION = os.getenv('AWS_REGION', '')

        # Verifica se todas as credenciais estão presentes
        if not all([self.ACCESS_KEY, self.SECRET_KEY, self.REGION]):
            raise ValueError("Credenciais AWS faltando. Por favor, verifique o arquivo .env.")

    def init_translate_client(self):
        """Inicializa o cliente AWS Translate."""
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
        """Traduz o texto usando o AWS Translate."""
        try:
            response = self.translate_client.translate_text(
                Text=text,
                SourceLanguageCode='auto',
                TargetLanguageCode=target_language_code
            )
            return response['TranslatedText']
        except Exception as e:
            raise Exception(f"Erro na tradução: {str(e)}")
