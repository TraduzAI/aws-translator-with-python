# main.py

import os
import tkinter as tk
from tkinter import END, Tk, messagebox, filedialog
from services.api.aws_translate_service import AwsTranslateService
from services.api.openai_service import OpenAIService
from services.document_service import DocumentService
from services.language.readability_service import ReadabilityService
from services.language.bleu_score_service import BleuScoreService


# Constants
LANGUAGES = {
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

AREAS_TECNICAS = [
    'Saúde, Medicina e Psicologia',
    'Matemática',
    'Física',
    'Estatística',
    'Ciência da Computação',
    'Ciência de Dados e Aprendizado de Máquina',
    'Ciências Biológicas',
    'Ciências Sociais',
    'Direito',
    'Engenharia',
    'Administração e Economia',
    'Artes e Humanidades',
    'Comércio e Logística'
]

ESTILOS = [
    'Formal',
    'Informal',
    'Técnico',
    'Conversacional',
    'Persuasivo'
]

MODELOS_DISPONIVEIS = [
    'gpt-3.5-turbo-0125',
    'gpt-4-turbo',
    'gpt-4o-mini',
    'gpt-4o'
]


class TranslationApp:
    def __init__(self, root: Tk) -> None:
        self.bleu_score_label = None
        self.original_metric_labels = None
        self.simplified_metric_labels = None
        self.simplified_metrics_text = None
        self.original_metrics_text = None
        self.texto_saida = None
        self.texto_entrada = None
        self.modelo_var = None
        self.summarize_var = None
        self.destino_var = None
        self.area_var = None
        self.estilo_var = None
        self.readability_service = None
        self.document_service = None
        self.openai_service = None
        self.aws_translate_service = None
        self.bleu_score_service = None  # Adicionado
        self.root = root
        self.setup_root_window()
        self.initialize_services()
        self.initialize_variables()
        self.create_widgets()

    def setup_root_window(self):
        """Initial configurations of the main window."""
        self.root.geometry("1200x700")  # Adjusted window size
        self.root.title("TraduzAI")
        self.root.subtitle = "Uma Solução Personalizada para Tradução Eficaz e Fluente em Diferentes Contextos"

    def initialize_services(self):
        """Initializes the necessary services."""
        try:
            self.aws_translate_service = AwsTranslateService()
            self.openai_service = OpenAIService()
            self.document_service = DocumentService()
            self.readability_service = ReadabilityService()  # Initialize ReadabilityService
            self.bleu_score_service = BleuScoreService()  # Initialize BleuScoreService
        except Exception as e:
            messagebox.showerror("Erro ao Inicializar", str(e))
            self.root.destroy()
            raise

    def initialize_variables(self):
        """Initializes variables used in the interface."""
        self.estilo_var = tk.StringVar(self.root, value='Informal')
        self.area_var = tk.StringVar(self.root, value='Geral')
        self.destino_var = tk.StringVar(self.root, value='Português')
        self.summarize_var = tk.BooleanVar()
        self.modelo_var = tk.StringVar(self.root, value='gpt-3.5-turbo-0125')

    def create_widgets(self) -> None:
        """Creates the widgets of the graphical interface."""
        self.create_title()

        # Main frame to organize elements
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Configure grid for 'main_frame'
        main_frame.columnconfigure(0, weight=1, uniform='column')
        main_frame.columnconfigure(1, weight=1, uniform='column')
        main_frame.columnconfigure(2, weight=1, uniform='column')
        main_frame.rowconfigure(0, weight=1)

        # Left frame for inputs (first third)
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # Middle frame for text input/output and import/export buttons (second third)
        middle_frame = tk.Frame(main_frame)
        middle_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        # Right frame for metrics (third third)
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

        # Create widgets in left_frame
        self.create_option_menus(left_frame)
        self.create_summarize_checkbox(left_frame)
        self.create_translate_button(left_frame)

        # Create widgets in middle_frame
        self.create_text_input(middle_frame)
        self.create_import_export_buttons(middle_frame)
        self.create_text_output(middle_frame)

        # Create widgets in right_frame
        self.create_readability_metrics_display(right_frame)

    def create_title(self):
        """Creates the application title."""
        title_label = tk.Label(
            self.root,
            text="TraduzAI\n"
                 "Uma Solução Personalizada para Tradução Eficaz e Fluente em Diferentes Contextos",
            font=("Helvetica", 15, "bold")
        )
        title_label.pack(pady=10)

    def create_option_menus(self, parent):
        """Creates the option menus inside the provided frame."""
        self.create_option_menu(parent, "Idioma de destino:", self.destino_var, LANGUAGES.keys())
        self.create_option_menu(parent, "Área técnica:", self.area_var, AREAS_TECNICAS)
        self.create_option_menu(parent, "Estilo de escrita:", self.estilo_var, ESTILOS)
        self.create_option_menu(parent, "Modelo OpenAI:", self.modelo_var,
                                MODELOS_DISPONIVEIS)

    @staticmethod
    def create_option_menu(parent, label_text, variable, options):
        """Helper function to create an option menu inside the provided frame."""
        label = tk.Label(parent, text=label_text, font=("Helvetica", 12))
        label.pack(pady=(10, 0))
        menu = tk.OptionMenu(parent, variable, *options)
        menu.config(width=25)
        menu.pack(pady=(0, 10))

    def create_summarize_checkbox(self, parent):
        """Creates the checkbox to summarize the text inside the provided frame."""
        checkbox_summarize = tk.Checkbutton(
            parent,
            text="Resumir",
            variable=self.summarize_var,
            font=("Helvetica", 12)
        )
        checkbox_summarize.pack(pady=(5, 10))

    def create_translate_button(self, parent):
        """Creates the translation button inside the provided frame."""
        self.create_button(
            parent=parent,
            text="Simplificar Linguagem e Traduzir",
            command=self.traduzir_texto,
            bg_color="#4CAF50",
            padx=20,
            pady=10
        )

    def create_text_input(self, parent):
        """Creates the text input box."""
        label_entrada = tk.Label(
            parent,
            text="Texto para Simplificar e Traduzir:",
            font=("Helvetica", 12)
        )
        label_entrada.pack(pady=(10, 0))
        self.texto_entrada = tk.Text(parent, height=20, width=60, wrap='word')
        self.texto_entrada.pack(pady=(5, 10))

    def create_import_export_buttons(self, parent):
        """Creates the import and export buttons."""
        button_frame = tk.Frame(parent)
        button_frame.pack(pady=(5, 10))
        self.create_button(button_frame, "Importar Documento", self.import_document, "#2196F3", side=tk.LEFT, padx=5)
        self.create_button(button_frame, "Exportar Documento", self.export_document, "#FF9800", side=tk.LEFT, padx=5)

    def create_text_output(self, parent):
        """Creates the text output box."""
        label_saida = tk.Label(
            parent,
            text="Texto Simplificado e Traduzido:",
            font=("Helvetica", 12)
        )
        label_saida.pack(pady=(10, 0))
        self.texto_saida = tk.Text(parent, height=20, width=60, wrap='word', state='disabled')
        self.texto_saida.pack(pady=(5, 10))

    def create_readability_metrics_display(self, parent):
        """Cria frames para exibir as métricas de legibilidade."""
        # Frame para as métricas do texto original
        original_frame = tk.LabelFrame(parent, text="Métricas do Texto Original", font=("Helvetica", 11, "bold"))
        original_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Frame interno para organizar as métricas em tabela
        original_metrics_frame = tk.Frame(original_frame)
        original_metrics_frame.pack(padx=10, pady=10)

        # Labels para as métricas do texto original
        self.original_metric_labels = {}
        metric_names = [
            'Índice de Flesch Reading Ease',
            'Grau de Flesch-Kincaid',
            'Índice SMOG',
            'Índice de Coleman-Liau',
            'Índice ARI',
            'Pontuação de Dale-Chall'
        ]

        for i, name in enumerate(metric_names):
            label_name = tk.Label(original_metrics_frame, text=name + ":", anchor='w', font=("Helvetica", 11, "bold"))
            label_name.grid(row=i, column=0, sticky='w', padx=(0, 5))
            label_value = tk.Label(original_metrics_frame, text="", anchor='e', font=("Helvetica", 11))
            label_value.grid(row=i, column=1, sticky='e')
            self.original_metric_labels[name] = label_value

        # Adicionar descrições abaixo das métricas do texto original
        original_description = (
            "1 - Índice de Flesch Reading Ease:\n\tMede a facilidade de leitura;\n\tValores mais altos indicam texto mais fácil.\n"
            "2 - Grau de Flesch-Kincaid:\n\tIndica o nível escolar necessário;\n\tValores mais baixos indicam texto mais acessível.\n"
            "3 - Índice SMOG:\n\tEstima os anos de educação necessários;\n\tValores mais baixos são melhores.\n"
            "4 - Índice de Coleman-Liau:\n\tBaseado em caracteres por palavra e palavras por frase;\n\tValores mais baixos indicam maior facilidade.\n"
            "5 - Índice ARI:\n\tUsa caracteres por palavra e palavras por frase;\n\tValores mais baixos indicam texto mais simples.\n"
            "6 - Pontuação de Dale-Chall:\n\tCompara com uma lista de palavras familiares;\n\tValores mais baixos indicam texto mais fácil."
        )
        original_desc_label = tk.Label(original_frame, text=original_description, justify='left', wraplength=600,
                                       font=("Courier", 10))
        original_desc_label.pack(padx=10, pady=(10, 0))

        # Frame para as métricas do texto simplificado
        simplified_frame = tk.LabelFrame(parent, text="Métricas do Texto Simplificado", font=("Helvetica", 11, "bold"))
        simplified_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Frame interno para organizar as métricas em tabela
        simplified_metrics_frame = tk.Frame(simplified_frame)
        simplified_metrics_frame.pack(padx=10, pady=10)

        # Labels para as métricas do texto simplificado
        self.simplified_metric_labels = {}

        for i, name in enumerate(metric_names):
            label_name = tk.Label(simplified_metrics_frame, text=name + ":", anchor='w', font=("Helvetica", 11, "bold"))
            label_name.grid(row=i, column=0, sticky='w', padx=(0, 5))
            label_value = tk.Label(simplified_metrics_frame, text="", anchor='e', font=("Helvetica", 11))
            label_value.grid(row=i, column=1, sticky='e')
            self.simplified_metric_labels[name] = label_value

        # Adiciona o label para o BLEU Score
        row_index = len(metric_names)
        bleu_label_name = tk.Label(simplified_metrics_frame, text='BLEU Score:', anchor='w',
                                   font=("Helvetica", 11, "bold"))
        bleu_label_name.grid(row=row_index, column=0, sticky='w', padx=(0, 5))
        self.bleu_score_label = tk.Label(simplified_metrics_frame, text="", anchor='e', font=("Helvetica", 11))
        self.bleu_score_label.grid(row=row_index, column=1, sticky='e')

    @staticmethod
    def create_button(parent, text, command, bg_color, **pack_options):
        """Helper function to create buttons.

        Args:
            parent (tk.Widget): Parent widget where the button will be added.
            text (str): Text displayed on the button.
            command (callable): Function called when the button is clicked.
            bg_color (str): Background colour of the button.
            **pack_options: Additional options for the pack() or grid() method.
        """
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg="white",
            font=("Helvetica", 12, "bold")
        )
        button.pack(**pack_options)

    def traduzir_texto(self) -> None:
        """Realiza a simplificação e tradução do texto inserido."""
        texto = self.texto_entrada.get("1.0", END).strip()
        if not texto:
            messagebox.showwarning("Entrada Vazia", "Por favor, insira um texto para simplificar e traduzir.")
            return

        codigo_idioma_destino = LANGUAGES.get(self.destino_var.get(), 'pt')
        area_tecnica = self.area_var.get()
        estilo = self.estilo_var.get()
        summarize = self.summarize_var.get()
        modelo_selecionado = self.modelo_var.get()

        try:
            # Simplifica o texto usando a API OpenAI
            texto_simplificado = self.openai_service.simplify_text(
                texto, area_tecnica, estilo, summarize, modelo_selecionado
            )

            # Calcula as métricas de legibilidade para o texto original
            metrics_original = self.readability_service.calculate_readability(texto)

            # Calcula as métricas de legibilidade para o texto simplificado
            metrics_simplified = self.readability_service.calculate_readability(texto_simplificado)

            # Traduz o texto simplificado
            texto_traduzido, source_language_code = self.aws_translate_service.translate_text(
                texto_simplificado, codigo_idioma_destino
            )

            # Calcula o BLEU Score
            bleu_score = self.bleu_score_service.compute_bleu_score(
                texto_simplificado, texto_traduzido, source_language_code
            )

            # Atualiza as métricas, incluindo o BLEU Score
            self.update_readability_metrics(metrics_original, metrics_simplified, bleu_score)

            self.mostrar_resultado(texto_traduzido)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    @staticmethod
    def metric_key_from_name(name):
        """Mapeia o nome da métrica para a chave no dicionário."""
        mapping = {
            'Índice de Flesch Reading Ease': 'flesch_reading_ease',
            'Grau de Flesch-Kincaid': 'flesch_kincaid_grade',
            'Índice SMOG': 'smog_index',
            'Índice de Coleman-Liau': 'coleman_liau_index',
            'Índice ARI': 'automated_readability_index',
            'Pontuação de Dale-Chall': 'dale_chall_readability_score'
        }
        return mapping.get(name)

    def update_readability_metrics(self, metrics_original, metrics_simplified, bleu_score=None):
        """Atualiza a exibição das métricas de legibilidade."""
        # Atualiza as métricas do texto original
        for name, label in self.original_metric_labels.items():
            key = self.metric_key_from_name(name)
            value = metrics_original.get(key, 'N/A')
            label.config(text=f"{value:.2f}" if isinstance(value, float) else value)

        # Atualiza as métricas do texto simplificado
        for name, label in self.simplified_metric_labels.items():
            key = self.metric_key_from_name(name)
            value = metrics_simplified.get(key, 'N/A')
            label.config(text=f"{value:.2f}" if isinstance(value, float) else value)

        # Atualiza o BLEU Score
        if bleu_score is not None:
            self.bleu_score_label.config(text=f"{bleu_score:.2f}")
        else:
            self.bleu_score_label.config(text="")

    def mostrar_resultado(self, texto: str) -> None:
        """Displays the result of the translation and simplification."""
        self.texto_saida.config(state='normal')
        self.texto_saida.delete("1.0", END)
        self.texto_saida.insert(END, texto)
        self.texto_saida.config(state='disabled')

    def import_document(self):
        """Imports text from a document."""
        file_path = filedialog.askopenfilename(
            title="Selecionar Documento",
            filetypes=[
                ("Todos os arquivos", "*.*"),
                ("Documento de Texto", "*.txt"),
                ("Documento PDF", "*.pdf"),
                ("Documento Word", "*.docx"),
                ("eBooks", "*.epub")
            ]
        )
        if file_path:
            try:
                text = self.document_service.import_document(file_path)
                self.texto_entrada.delete("1.0", END)
                self.texto_entrada.insert(END, text)
            except Exception as e:
                messagebox.showerror("Erro ao Importar Documento", str(e))

    def export_document(self):
        """Exports the output text to a document."""
        output_text = self.texto_saida.get("1.0", END).strip()
        if not output_text:
            messagebox.showwarning("Nenhum texto para exportar", "Não há texto traduzido e simplificado para exportar.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Salvar Documento",
            defaultextension=".txt",
            filetypes=[
                ("Documento de Texto", "*.txt"),
                ("Documento PDF", "*.pdf"),
                ("Documento Word", "*.docx")
            ]
        )
        if file_path:
            try:
                ext = os.path.splitext(file_path)[1].lower()
                format_map = {'.txt': 'txt', '.pdf': 'pdf', '.docx': 'docx'}
                format = format_map.get(ext)
                if not format:
                    messagebox.showerror("Formato não suportado", f"Formato de arquivo não suportado: {ext}")
                    return
                text = self.texto_saida.get("1.0", END)
                self.document_service.export_document(text, file_path, format)
                messagebox.showinfo("Exportação bem-sucedida", f"Documento exportado com sucesso: {file_path}")
            except Exception as e:
                messagebox.showerror("Erro ao Exportar Documento", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
