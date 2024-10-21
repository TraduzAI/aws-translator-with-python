# main.py

"""
Aplicação de Tradução e Simplificação de Texto com Métricas de Legibilidade
===========================================================================
Este módulo fornece uma aplicação gráfica para simplificar e traduzir textos,
calculando métricas de legibilidade tanto para o texto original quanto para o
texto simplificado. A interface permite a configuração de diversos parâmetros
como idioma de destino, área técnica, estilo de escrita, modelo OpenAI, entre
outros.

Classes:
    TranslationApp: Classe responsável pela interface gráfica e pela lógica
                    de tradução e simplificação de textos.

Dependências:
    - tkinter: biblioteca para criação de interfaces gráficas.
    - services.api.aws_translate_service.AwsTranslateService: serviço para tradução usando AWS.
    - services.api.openai_service.OpenAIService: serviço para simplificação de texto usando OpenAI.
    - services.document_service.DocumentService: serviço para importação e exportação de documentos.
    - services.language.readability_service.ReadabilityService: serviço para cálculo de métricas de legibilidade.
    - services.language.bleu_score_service.BleuScoreService: serviço para cálculo de BLEU Score.

Exemplo de Uso:
    >>> if __name__ == "__main__":
    >>>     root = tk.Tk()
    >>>     app = TranslationApp(root)
    >>>     root.mainloop()
"""

import os
import tkinter as tk
from tkinter import END, Tk, messagebox, filedialog
from services.api.aws_translate_service import AwsTranslateService
from services.api.openai_service import OpenAIService
from services.document_service import DocumentService
from services.language.readability_service import ReadabilityService
from services.language.bleu_score_service import BleuScoreService

# Constantes
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

SPECIALITIES = [
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

STYLES = [
    'Formal',
    'Informal',
    'Técnico',
    'Conversacional',
    'Persuasivo'
]

AVAILABLE_MODELS = [
    'gpt-3.5-turbo-0125',
    'gpt-4-turbo',
    'gpt-4o-mini',
    'gpt-4o'
]

COMPLEXITY_LEVELS = ['Básico', 'Intermediário', 'Avançado']


class TranslationApp:
    """
    Aplicação para Simplificação e Tradução de Textos com Métricas de Legibilidade.

    Esta classe implementa uma interface gráfica que permite ao usuário inserir um texto,
    selecionar parâmetros como idioma de destino, área técnica, estilo de escrita, e
    outros. A aplicação utiliza serviços para simplificar o texto, traduzi-lo, e calcular
    métricas de legibilidade tanto para o texto original quanto para o texto simplificado.

    Métodos:
        __init__(root: Tk) → None:
            Inicializa a aplicação com a janela raiz fornecida.

        setup_root_window() → None:
            Configurações iniciais da janela principal.

        initialize_services() → None:
            Inicializa os serviços necessários para a aplicação.

        initialize_variables() → None:
            Inicializa as variáveis utilizadas na interface.

        create_widgets() → None:
            Cria e organiza os widgets da interface gráfica.

        create_title() → None:
            Cria o título da aplicação.

        create_option_menu(parent, label_text, variable, options) → None:
            Cria um menu de opções dentro do frame fornecido.

        create_option_menus(parent) → None:
            Cria todos os menus de opções principais.

        create_complexity_option_menu(parent) → None:
            Cria o menu de seleção de nível de complexidade.

        create_focus_aspects_checkboxes(parent) → None:
            Cria as caixas de seleção para focar em aspectos específicos.

        create_api_parameter_entries(parent) → None:
            Cria os campos para ajuste dos parâmetros da API OpenAI.

        create_summarize_checkbox(parent) → None:
            Cria a caixa de seleção para resumir o texto.

        create_translate_button(parent) → None:
            Cria o botão para realizar a tradução e simplificação.

        create_text_input(parent) → None:
            Cria a área de entrada de texto.

        create_import_export_buttons(parent) → None:
            Cria os botões para importação e exportação de documentos.

        create_text_output(parent) → None:
            Cria a área de saída de texto.

        create_readability_metrics_display(parent) → None:
            Cria a exibição das métricas de legibilidade.

        create_button(parent, text, command, bg_color, **pack_options) → None:
            Função auxiliar para criar botões.

        translate_text() → None:
            Realiza a simplificação e tradução do texto inserido.

        metric_key_from_name(name) → str:
            Mapeia o nome da métrica para a chave no dicionário.

        update_readability_metrics(metrics_original, metrics_simplified, bleu_score=None) → None:
            Atualiza a exibição das métricas de legibilidade.

        show_results(texto: str) → None:
            Exibe o resultado da tradução e simplificação.

        import_document() → None:
            Importa texto de um documento.

        export_document() → None:
            Exporta o texto de saída para um documento.
    """

    def __init__(self, root: Tk) -> None:
        """
        Inicializa a aplicação com a janela raiz fornecida.

        Args:
            root (Tk): A janela raiz da aplicação Tkinter.
        """
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
        self.complexity_var = None
        self.focus_clarity_var = None
        self.focus_conciseness_var = None
        self.focus_formality_var = None
        self.temperature_var = None
        self.max_tokens_var = None
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
        """
        Configurações iniciais da janela principal.

        Define o tamanho, título e subtítulo da janela.
        """
        self.root.geometry("1200x900")  # Ajustado para acomodar novas opções
        self.root.title("TraduzAI")
        self.root.subtitle = "Uma Solução Personalizada para Tradução Eficaz e Fluente em Diferentes Contextos"

    def initialize_services(self):
        """
        Inicializa os serviços necessários para a aplicação.

        Instancia os serviços de tradução, simplificação, manipulação de documentos,
        cálculo de legibilidade e BLEU Score.

        Exceções:
            - Exibe uma mensagem de erro e encerra a aplicação se ocorrer um erro
              na inicialização dos serviços.
        """
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
        """
        Inicializa as variáveis utilizadas na interface.

        Define valores padrões para menus de opções, caixas de seleção e
        parâmetros da API.
        """
        self.estilo_var = tk.StringVar(self.root, value='Informal')
        self.area_var = tk.StringVar(self.root, value='Ciência da Computação')
        self.destino_var = tk.StringVar(self.root, value='Português')
        self.summarize_var = tk.BooleanVar()
        self.modelo_var = tk.StringVar(self.root, value='gpt-3.5-turbo-0125')
        self.complexity_var = tk.StringVar(self.root, value='Intermediário')
        self.focus_clarity_var = tk.BooleanVar()
        self.focus_conciseness_var = tk.BooleanVar()
        self.focus_formality_var = tk.BooleanVar()
        self.temperature_var = tk.DoubleVar(self.root, value=0.8)
        self.max_tokens_var = tk.IntVar(self.root, value=1500)  # Ajustado para evitar exceder limites

    def create_widgets(self) -> None:
        """
        Cria e organiza os widgets da interface gráfica.

        Divide a janela principal em três frames: esquerdo para opções de entrada,
        central para entrada e saída de texto, e direito para exibição das métricas.
        """
        self.create_title()

        # Frame principal para organizar elementos
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Configurar grid para 'main_frame'
        main_frame.columnconfigure(0, weight=1, uniform='column')
        main_frame.columnconfigure(1, weight=2, uniform='column')
        main_frame.columnconfigure(2, weight=1, uniform='column')
        main_frame.rowconfigure(0, weight=1)

        # Frame esquerdo para entradas (primeiro terço)
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        # Frame central para entrada/saída de texto e botões de importação/exportação (segundo terço)
        middle_frame = tk.Frame(main_frame)
        middle_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        # Frame direito para métricas (terceiro terço)
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

        # Criar widgets no left_frame
        self.create_option_menus(left_frame)
        self.create_complexity_option_menu(left_frame)
        self.create_focus_aspects_checkboxes(left_frame)
        self.create_api_parameter_entries(left_frame)
        self.create_summarize_checkbox(left_frame)
        self.create_translate_button(left_frame)

        # Criar widgets no middle_frame
        self.create_text_input(middle_frame)
        self.create_import_export_buttons(middle_frame)
        self.create_text_output(middle_frame)

        # Criar widgets no right_frame
        self.create_readability_metrics_display(right_frame)

    def create_title(self):
        """
        Cria o título da aplicação.

        Adiciona um rótulo na parte superior da janela com o nome da aplicação e um subtítulo.
        """
        title_label = tk.Label(
            self.root,
            text="TraduzAI\n"
                 "Uma Solução Personalizada para Tradução Eficaz e Fluente em Diferentes Contextos",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=10)

    @staticmethod
    def create_option_menu(parent, label_text, variable, options):
        """
        Função auxiliar para criar um menu de opções dentro do frame fornecido.

        Args:
            parent (tk.Widget): Widget pai onde o menu será adicionado.
            label_text (str): Texto do rótulo do menu.
            variable (tk.Variable): Variável associada ao menu de opções.
            options (list): Lista de opções disponíveis no menu.
        """
        label = tk.Label(parent, text=label_text, font=("Helvetica", 12))
        label.pack(pady=(10, 0))
        menu = tk.OptionMenu(parent, variable, *options)
        menu.config(width=25)
        menu.pack(pady=(0, 10))

    def create_option_menus(self, parent):
        """
        Cria todos os menus de opções principais dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde os menus serão adicionados.
        """
        self.create_option_menu(parent, "Idioma de destino:", self.destino_var, LANGUAGES.keys())
        self.create_option_menu(parent, "Área técnica:", self.area_var, SPECIALITIES)
        self.create_option_menu(parent, "Estilo de escrita:", self.estilo_var, STYLES)
        self.create_option_menu(parent, "Modelo OpenAI:", self.modelo_var, AVAILABLE_MODELS)

    def create_complexity_option_menu(self, parent):
        """
        Cria o menu de seleção de nível de complexidade.

        Args:
            parent (tk.Widget): Frame onde o menu será adicionado.
        """
        self.create_option_menu(parent, "Nível de Complexidade:", self.complexity_var, COMPLEXITY_LEVELS)

    def create_focus_aspects_checkboxes(self, parent):
        """
        Cria as caixas de seleção para focar em aspectos específicos dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde as caixas de seleção serão adicionadas.
        """
        label = tk.Label(parent, text="Focar em:", font=("Helvetica", 12))
        label.pack(pady=(10, 0))
        checkbox_clarity = tk.Checkbutton(parent, text="Clareza", variable=self.focus_clarity_var,
                                          font=("Helvetica", 12))
        checkbox_clarity.pack(pady=(0, 5))
        checkbox_conciseness = tk.Checkbutton(parent, text="Concisão", variable=self.focus_conciseness_var,
                                              font=("Helvetica", 12))
        checkbox_conciseness.pack(pady=(0, 5))
        checkbox_formality = tk.Checkbutton(parent, text="Formalidade", variable=self.focus_formality_var,
                                            font=("Helvetica", 12))
        checkbox_formality.pack(pady=(0, 5))

    def create_api_parameter_entries(self, parent):
        """
        Cria os campos para ajuste dos parâmetros da API OpenAI dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde os campos serão adicionados.
        """
        label = tk.Label(parent, text="Parâmetros da API OpenAI:", font=("Helvetica", 12, "bold"))
        label.pack(pady=(10, 0))

        # Frame principal para os parâmetros
        params_frame = tk.Frame(parent)
        params_frame.pack(pady=(5, 5))

        # Temperature
        temperature_label = tk.Label(params_frame, text="Temperature:", font=("Helvetica", 12))
        temperature_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        temperature_entry = tk.Entry(params_frame, textvariable=self.temperature_var, width=5)
        temperature_entry.grid(row=0, column=1, padx=5, pady=5)

        # Max Tokens
        max_tokens_label = tk.Label(params_frame, text="Max Tokens:", font=("Helvetica", 12))
        max_tokens_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        max_tokens_entry = tk.Entry(params_frame, textvariable=self.max_tokens_var, width=5)
        max_tokens_entry.grid(row=1, column=1, padx=5, pady=5)

        # Centralizar o frame dos parâmetros
        params_frame.pack(anchor='center')

    def create_summarize_checkbox(self, parent):
        """
        Cria a caixa de seleção para resumir o texto dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde a caixa de seleção será adicionada.
        """
        checkbox_summarize = tk.Checkbutton(
            parent,
            text="Resumir",
            variable=self.summarize_var,
            font=("Helvetica", 12)
        )
        checkbox_summarize.pack(pady=(10, 10))

    def create_translate_button(self, parent):
        """
        Cria o botão para realizar a tradução e simplificação dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde o botão será adicionado.
        """
        self.create_button(
            parent=parent,
            text="Simplificar Linguagem e Traduzir",
            command=self.translate_text,
            bg_color="#4CAF50",
            padx=20,
            pady=10
        )

    def create_text_input(self, parent):
        """
        Cria a área de entrada de texto dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde a área de entrada será adicionada.
        """
        label_entrada = tk.Label(
            parent,
            text="Texto para Simplificar e Traduzir:",
            font=("Helvetica", 12, "bold")
        )
        label_entrada.pack(pady=(10, 0))
        self.texto_entrada = tk.Text(parent, height=25, width=70, wrap='word')
        self.texto_entrada.pack(pady=(5, 10))

    def create_import_export_buttons(self, parent):
        """
        Cria os botões para importação e exportação de documentos dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde os botões serão adicionados.
        """
        button_frame = tk.Frame(parent)
        button_frame.pack(pady=(5, 10))
        self.create_button(button_frame, "Importar Documento", self.import_document, "#2196F3", side=tk.LEFT, padx=5)
        self.create_button(button_frame, "Exportar Documento", self.export_document, "#FF9800", side=tk.LEFT, padx=5)

    def create_text_output(self, parent):
        """
        Cria a área de saída de texto dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde a área de saída será adicionada.
        """
        label_saida = tk.Label(
            parent,
            text="Texto Simplificado e Traduzido:",
            font=("Helvetica", 12, "bold")
        )
        label_saida.pack(pady=(10, 0))
        self.texto_saida = tk.Text(parent, height=25, width=70, wrap='word', state='disabled')
        self.texto_saida.pack(pady=(5, 10))

    def create_readability_metrics_display(self, parent):
        """
        Cria a exibição das métricas de legibilidade dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde as métricas serão exibidas.
        """
        # Frame para as métricas do texto original
        original_frame = tk.LabelFrame(parent, text="Métricas do Texto Original", font=("Helvetica", 12, "bold"))
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
            label_name.grid(row=i, column=0, sticky='w', padx=(0, 5), pady=2)
            label_value = tk.Label(original_metrics_frame, text="", anchor='e', font=("Helvetica", 11))
            label_value.grid(row=i, column=1, sticky='e', pady=2)
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
        original_desc_label = tk.Label(original_frame, text=original_description, justify='left', wraplength=400,
                                       font=("Courier", 10))
        original_desc_label.pack(padx=10, pady=(10, 0))

        # Frame para as métricas do texto simplificado
        simplified_frame = tk.LabelFrame(parent, text="Métricas do Texto Simplificado", font=("Helvetica", 12, "bold"))
        simplified_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Frame interno para organizar as métricas em tabela
        simplified_metrics_frame = tk.Frame(simplified_frame)
        simplified_metrics_frame.pack(padx=10, pady=10)

        # Labels para as métricas do texto simplificado
        self.simplified_metric_labels = {}

        for i, name in enumerate(metric_names):
            label_name = tk.Label(simplified_metrics_frame, text=name + ":", anchor='w', font=("Helvetica", 11, "bold"))
            label_name.grid(row=i, column=0, sticky='w', padx=(0, 5), pady=2)
            label_value = tk.Label(simplified_metrics_frame, text="", anchor='e', font=("Helvetica", 11))
            label_value.grid(row=i, column=1, sticky='e', pady=2)
            self.simplified_metric_labels[name] = label_value

        # Adiciona o label para o BLEU Score
        row_index = len(metric_names)
        bleu_label_name = tk.Label(simplified_metrics_frame, text='BLEU Score:', anchor='w',
                                   font=("Helvetica", 11, "bold"))
        bleu_label_name.grid(row=row_index, column=0, sticky='w', padx=(0, 5), pady=2)
        self.bleu_score_label = tk.Label(simplified_metrics_frame, text="", anchor='e', font=("Helvetica", 11))
        self.bleu_score_label.grid(row=row_index, column=1, sticky='e', pady=2)

    @staticmethod
    def create_button(parent, text, command, bg_color, **pack_options):
        """
        Função auxiliar para criar botões.

        Args:
            parent (tk.Widget): Widget pai onde o botão será adicionado.
            text (str): Texto exibido no botão.
            command (callable): Função chamada quando o botão é clicado.
            bg_color (str): Cor de fundo do botão.
            **pack_options: Opções adicionais para o método pack() ou grid().
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

    def translate_text(self) -> None:
        """
        Realiza a simplificação e tradução do texto inserido.

        Este método executa os seguintes passos:
            1. Obtém o texto de entrada da interface.
            2. Coleta os parâmetros selecionados pelo usuário.
            3. Utiliza o serviço OpenAI para simplificar o texto.
            4. Calcula as métricas de legibilidade para o texto original e simplificado.
            5. Traduz o texto simplificado para o idioma de destino.
            6. Calcula o BLEU Score entre o texto simplificado e traduzido.
            7. Atualiza a interface com as métricas calculadas e o texto traduzido.

        Exceções:
            - Exibe uma mensagem de erro se ocorrer qualquer problema durante o processo.
        """
        texto = self.texto_entrada.get("1.0", END).strip()
        if not texto:
            messagebox.showwarning("Entrada Vazia", "Por favor, insira um texto para simplificar e traduzir.")
            return

        codigo_idioma_destino = LANGUAGES.get(self.destino_var.get(), 'pt')
        area_tecnica = self.area_var.get()
        estilo = self.estilo_var.get()
        summarize = self.summarize_var.get()
        modelo_selecionado = self.modelo_var.get()
        complexity_level = self.complexity_var.get()

        focus_aspects = []
        if self.focus_clarity_var.get():
            focus_aspects.append('clareza')
        if self.focus_conciseness_var.get():
            focus_aspects.append('concisão')
        if self.focus_formality_var.get():
            focus_aspects.append('formalidade')

        temperature = self.temperature_var.get()
        max_tokens = self.max_tokens_var.get()

        try:
            # Simplifica o texto usando a API OpenAI com os novos parâmetros
            texto_simplificado = self.openai_service.simplify_text(
                text=texto,
                area_tecnica=area_tecnica,
                estilo=estilo,
                summarize=summarize,
                model=modelo_selecionado,
                complexity_level=complexity_level,
                focus_aspects=focus_aspects,
                temperature=temperature,
                max_tokens=max_tokens
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

            self.show_results(texto_traduzido)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    @staticmethod
    def metric_key_from_name(name):
        """
        Mapeia o nome da métrica para a chave no dicionário.

        Args:
            name (str): Nome da métrica exibida na interface.

        Returns:
            str: Chave correspondente no dicionário de métricas.
        """
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
        """
        Atualiza a exibição das métricas de legibilidade na interface.

        Args:
            metrics_original (dict): Métricas de legibilidade do texto original.
            metrics_simplified (dict): Métricas de legibilidade do texto simplificado.
            bleu_score (float, opcional): BLEU Score calculado. Defaults to None.
        """
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

    def show_results(self, texto: str) -> None:
        """
        Exibe o resultado da tradução e simplificação na área de saída de texto.

        Args:
            texto (str): Texto traduzido e simplificado a ser exibido.
        """
        self.texto_saida.config(state='normal')
        self.texto_saida.delete("1.0", END)
        self.texto_saida.insert(END, texto)
        self.texto_saida.config(state='disabled')

    def import_document(self):
        """
        Importa texto de um documento selecionado pelo usuário.

        Permite ao usuário selecionar um arquivo de texto, PDF, Word ou eBook e
        importa o conteúdo para a área de entrada de texto.

        Exceções:
            - Exibe uma mensagem de erro se ocorrer algum problema durante a importação.
        """
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
        """
        Exporta o texto de saída para um documento escolhido pelo usuário.

        Permite ao usuário salvar o texto traduzido e simplificado em formatos
        como TXT, PDF ou DOCX.

        Exceções:
            - Exibe uma mensagem de erro se não houver texto para exportar ou
              se ocorrer algum problema durante a exportação.
        """
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
