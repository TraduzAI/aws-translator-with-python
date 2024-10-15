import tkinter as tk
from tkinter import END, Tk, messagebox
from services.aws_translate_service import AwsTranslateService
from services.openai_service import OpenAIService


class TranslationApp:
    def __init__(self, root: Tk) -> None:
        self.texto_entrada = None
        self.estilo_var = None
        self.area_var = None
        self.destino_var = None
        self.languages = None
        self.texto_saida = None
        self.summarize_var = tk.BooleanVar()  # Variável para o checkbox de resumir
        self.root = root
        self.root.geometry("600x750")
        self.root.title("AWS Tradutor com Simplificação de Jargões Técnicos")

        # Inicializa os serviços
        try:
            self.aws_translate_service = AwsTranslateService()
            self.openai_service = OpenAIService()
        except Exception as e:
            messagebox.showerror("Erro ao Inicializar", str(e))
            self.root.destroy()
            return

        # Configura a interface gráfica
        self.create_widgets()

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
        areas_tecnicas = ['Geral', 'Medicina', 'Psicologia',
                          'Direito', 'Matemática', 'Química',
                          'Física', 'Programação', 'Filosofia']
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

        # Checkbox para resumir
        checkbox_summarize = tk.Checkbutton(
            self.root,
            text="Resumir o texto",
            variable=self.summarize_var,
            font=("Helvetica", 12)
        )
        checkbox_summarize.pack(pady=(5, 10))

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
        """Realiza a simplificação (e opção de resumir) e traduz o texto inserido."""
        texto = self.texto_entrada.get("1.0", END).strip()
        if not texto:
            messagebox.showwarning("Entrada Vazia", "Por favor, insira um texto para simplificar e traduzir.")
            return

        codigo_idioma_destino = self.languages.get(self.destino_var.get(), 'pt')
        area_tecnica = self.area_var.get()
        estilo = self.estilo_var.get()
        summarize = self.summarize_var.get()

        try:
            # Simplificação com OpenAI
            texto_simplificado = self.openai_service.simplify_text(texto, area_tecnica, estilo, summarize)

            # Tradução com AWS Translate
            texto_traduzido = self.aws_translate_service.translate_text(texto_simplificado, codigo_idioma_destino)

            # Exibe o resultado na caixa de saída
            self.mostrar_resultado(texto_traduzido)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def mostrar_resultado(self, texto: str) -> None:
        """Exibe o resultado da tradução e simplificação."""
        self.texto_saida.config(state='normal')
        self.texto_saida.delete("1.0", END)
        self.texto_saida.insert(END, texto)
        self.texto_saida.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
