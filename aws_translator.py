import tkinter as tk
from tkinter import END, Tk
from dotenv import load_dotenv
import boto3
import os


class AwsTranslateService:
    def __init__(self, root: Tk) -> None:

        self.texto_entrada = None
        self.destino_var = None
        self.texto_saida = None
        self.languages = None

        self.SECRET_KEY = None
        self.ACCESS_KEY = None
        self.REGION = None

        self.root = root
        self.root.geometry("400x500")
        self.root.title("AWS Tradutor")

        # Carrega as credenciais AWS
        self.load_aws_credentials()

        # Configura a interface gráfica
        self.create_widgets()

        # Inicializa o cliente AWS Translate
        self.translate_client = boto3.client(
            service_name='translate',
            region_name=self.REGION,
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET_KEY
        )

    def load_aws_credentials(self) -> None:
        """Carrega as credenciais AWS do arquivo .env."""
        load_dotenv()
        self.ACCESS_KEY: str = os.getenv('AWS_ACCESS_KEY_ID', '')
        self.SECRET_KEY: str = os.getenv('AWS_SECRET_ACCESS_KEY', '')
        self.REGION: str = os.getenv('AWS_REGION', '')

    def create_widgets(self) -> None:
        """Cria os widgets da interface gráfica."""
        # Opções de idiomas
        self.languages: dict[str, str] = {
            'Africâner': 'af',
            'Árabe': 'ar',
            'Bengali': 'bn',
            'Chinês (Simplificado)': 'zh',
            'Chinês (Tradicional)': 'zh-TW',
            'Dinamarquês': 'da',
            'Holandês': 'nl',
            'Inglês': 'en',
            'Francês': 'fr',
            'Alemão': 'de',
            'Grego': 'el',
            'Hebraico': 'he',
            'Hindi': 'hi',
            'Indonésio': 'id',
            'Italiano': 'it',
            'Japonês': 'ja',
            'Coreano': 'ko',
            'Norueguês': 'no',
            'Polonês': 'pl',
            'Português': 'pt',
            'Russo': 'ru',
            'Espanhol': 'es',
            'Sueco': 'sv',
            'Turco': 'tr',
            'Ucraniano': 'uk',
            'Vietnamita': 'vi'
        }

        idiomas_disponiveis = list(self.languages.keys())

        # Seleção do idioma de destino
        label_destino = tk.Label(self.root, text="Selecione o idioma de destino:")
        label_destino.pack(pady=(10, 0))
        self.destino_var = tk.StringVar(self.root)
        self.destino_var.set('Português')  # Valor padrão
        menu_destino = tk.OptionMenu(self.root, self.destino_var, *idiomas_disponiveis)
        menu_destino.pack()

        # Label de entrada
        label_entrada = tk.Label(self.root, text="Digite o texto para traduzir:")
        label_entrada.pack(pady=(10, 0))

        # Caixa de texto de entrada
        self.texto_entrada = tk.Text(self.root, height=10)
        self.texto_entrada.pack()

        # Botão de tradução
        botao_traduzir = tk.Button(
            self.root, text="Traduzir", command=self.traduzir_texto
        )
        botao_traduzir.pack(pady=(10, 0))

        # Label de saída
        label_saida = tk.Label(self.root, text="Texto traduzido:")
        label_saida.pack(pady=(10, 0))

        # Caixa de texto de saída
        self.texto_saida = tk.Text(self.root, height=10)
        self.texto_saida.pack()

    def traduzir_texto(self) -> None:
        """Realiza a tradução do texto inserido."""
        texto: str = self.texto_entrada.get("1.0", END).strip()
        if not texto:
            self.mostrar_mensagem_erro("Por favor, insira um texto para traduzir.")
            return

        codigo_idioma_destino: str = self.languages[self.destino_var.get()]

        try:
            response = self.translate_client.translate_text(
                Text=texto,
                SourceLanguageCode='auto',
                TargetLanguageCode=codigo_idioma_destino
            )
            texto_traduzido: str = response['TranslatedText']
            self.mostrar_resultado(texto_traduzido)
        except Exception as e:
            self.mostrar_mensagem_erro(f"Erro na tradução: {str(e)}")

    def mostrar_resultado(self, texto: str) -> None:
        """Exibe o resultado da tradução."""
        self.texto_saida.delete("1.0", END)
        self.texto_saida.insert(END, texto)

    def mostrar_mensagem_erro(self, mensagem: str) -> None:
        """Exibe uma mensagem na caixa de saída."""
        self.texto_saida.delete("1.0", END)
        self.texto_saida.insert(END, mensagem)


if __name__ == "__main__":
    root = tk.Tk()
    app = AwsTranslateService(root)
    root.mainloop()
