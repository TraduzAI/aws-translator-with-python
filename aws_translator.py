import tkinter as tk
from tkinter import END, Tk, messagebox
from dotenv import load_dotenv
import boto3
import os
from openai import OpenAI
import random
import time


class AwsTranslateService:
    def __init__(self, root: Tk) -> None:
        self.translate_client = None
        self.openai_client = None
        self.texto_entrada = None
        self.destino_var = None
        self.texto_saida = None
        self.languages = None
        self.area_var = None
        self.estilo_var = None

        self.SECRET_KEY = None
        self.ACCESS_KEY = None
        self.REGION = None
        self.OPENAI_API_KEY = None

        self.root = root
        self.root.geometry("600x700")
        self.root.title("AWS Tradutor com Simplificação de Jargões Técnicos")

        # Carrega as credenciais AWS e OpenAI
        self.load_credentials()

        # Configura a interface gráfica
        self.create_widgets()

        # Inicializa o cliente AWS Translate
        self.init_translate_client()

    def load_credentials(self) -> None:
        """Carrega as credenciais AWS e OpenAI do arquivo .env."""
        load_dotenv()
        self.ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID', '')
        self.SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
        self.REGION = os.getenv('AWS_REGION', '')
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

        # Instancia o cliente OpenAI
        self.openai_client = OpenAI(api_key=self.OPENAI_API_KEY)

        # Verifica se todas as credenciais estão presentes
        if not all([self.ACCESS_KEY, self.SECRET_KEY, self.REGION, self.OPENAI_API_KEY]):
            messagebox.showerror(
                "Credenciais Faltando",
                "Por favor, verifique o arquivo .env e certifique-se de que todas as credenciais estão preenchidas."
            )
            self.root.destroy()

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
            messagebox.showerror(
                "Erro AWS",
                f"Falha ao inicializar o cliente AWS Translate: {str(e)}"
            )
            self.root.destroy()

    def create_widgets(self) -> None:
        """Cria os widgets da interface gráfica."""
        # Título
        title_label = tk.Label(
            self.root,
            text="Sistema de Tradução e Simplificação de Textos Técnicos",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=10)

        # Opções de idiomas
        self.languages = {
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
        label_destino = tk.Label(
            self.root,
            text="Selecione o idioma de destino:",
            font=("Helvetica", 12)
        )
        label_destino.pack(pady=(10, 0))
        self.destino_var = tk.StringVar(self.root)
        self.destino_var.set('Português')  # Valor padrão
        menu_destino = tk.OptionMenu(self.root, self.destino_var, *idiomas_disponiveis)
        menu_destino.config(width=20)
        menu_destino.pack(pady=(0, 10))

        # Seleção da área técnica
        label_area = tk.Label(
            self.root,
            text="Selecione a área técnica:",
            font=("Helvetica", 12)
        )
        label_area.pack(pady=(10, 0))
        self.area_var = tk.StringVar(self.root)
        self.area_var.set('Geral')  # Valor padrão
        areas_tecnicas = ['Geral', 'Medicina', 'Direito', 'Matemática', 'Química', 'Física', 'Programação', 'Filosofia']
        menu_area = tk.OptionMenu(self.root, self.area_var, *areas_tecnicas)
        menu_area.config(width=20)
        menu_area.pack(pady=(0, 10))

        # Seleção do estilo
        label_estilo = tk.Label(
            self.root,
            text="Selecione o estilo de escrita:",
            font=("Helvetica", 12)
        )
        label_estilo.pack(pady=(10, 0))
        self.estilo_var = tk.StringVar(self.root)
        self.estilo_var.set('Informal')  # Valor padrão
        estilos = ['Formal', 'Informal']
        menu_estilo = tk.OptionMenu(self.root, self.estilo_var, *estilos)
        menu_estilo.config(width=20)
        menu_estilo.pack(pady=(0, 10))

        # Label de entrada
        label_entrada = tk.Label(
            self.root,
            text="Digite o texto para traduzir e simplificar:",
            font=("Helvetica", 12)
        )
        label_entrada.pack(pady=(10, 0))

        # Caixa de texto de entrada
        self.texto_entrada = tk.Text(self.root, height=10, width=70, wrap='word')
        self.texto_entrada.pack(pady=(5, 10))

        # Botão de tradução
        botao_traduzir = tk.Button(
            self.root,
            text="Traduzir e Simplificar",
            command=self.traduzir_texto,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 12, "bold")
        )
        botao_traduzir.pack(pady=(10, 10))

        # Label de saída
        label_saida = tk.Label(
            self.root,
            text="Texto traduzido e simplificado:",
            font=("Helvetica", 12)
        )
        label_saida.pack(pady=(10, 0))

        # Caixa de texto de saída
        self.texto_saida = tk.Text(self.root, height=15, width=70, wrap='word', state='disabled')
        self.texto_saida.pack(pady=(5, 10))

    def traduzir_texto(self) -> None:
        """Realiza a tradução do texto inserido e simplifica o jargão."""
        texto = self.texto_entrada.get("1.0", END).strip()
        if not texto:
            messagebox.showwarning("Entrada Vazia", "Por favor, insira um texto para traduzir.")
            return

        codigo_idioma_destino = self.languages.get(self.destino_var.get(), 'pt')
        area_tecnica = self.area_var.get()
        estilo = self.estilo_var.get()

        try:
            # Tradução com AWS Translate
            response = self.translate_client.translate_text(
                Text=texto,
                SourceLanguageCode='auto',
                TargetLanguageCode=codigo_idioma_destino
            )
            texto_traduzido = response['TranslatedText']

            # Simplificação com OpenAI
            texto_simplificado = self.simplificar_texto(texto_traduzido, area_tecnica, estilo)

            # Exibe o resultado na caixa de saída
            self.mostrar_resultado(texto_simplificado)
        except Exception as e:
            messagebox.showerror("Erro na Tradução", f"Erro ao traduzir o texto: {str(e)}")

    def simplificar_texto(self, texto: str, area_tecnica: str, estilo: str) -> str:
        """Simplifica o texto usando a API da OpenAI."""
        messages = [
            {"role": "system", "content": f"Você é um especialista em {area_tecnica}."},
            {
                "role": "user",
                "content": f"Reescreva o seguinte texto em um estilo {estilo}, tornando-o acessível para pessoas leigas:\n\nTexto: {texto}"
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
                    messagebox.showerror(
                        "Erro na Simplificação",
                        f"Erro ao simplificar o texto após várias tentativas: {str(e)}"
                    )
                    return texto
                else:
                    wait_time = 2 ** attempt + random.uniform(0, 1)
                    time.sleep(wait_time)

    def mostrar_resultado(self, texto: str) -> None:
        """Exibe o resultado da tradução e simplificação."""
        self.texto_saida.config(state='normal')
        self.texto_saida.delete("1.0", END)
        self.texto_saida.insert(END, texto)
        self.texto_saida.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = AwsTranslateService(root)
    root.mainloop()
