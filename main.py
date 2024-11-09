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
    'Afrikaans': 'af',
    'العربية': 'ar',
    'বাংলা': 'bn',
    '中文 (简体)': 'zh',
    '中文 (繁體)': 'zh-TW',
    'Dansk': 'da',
    'Nederlands': 'nl',
    'English': 'en',
    'Français': 'fr',
    'Deutsch': 'de',
    'Ελληνικά': 'el',
    'עברית': 'he',
    'हिन्दी': 'hi',
    'Bahasa Indonesia': 'id',
    'Italiano': 'it',
    '日本語': 'ja',
    '한국어': 'ko',
    'Norsk': 'no',
    'Polski': 'pl',
    'Português': 'pt',
    'Русский': 'ru',
    'Español': 'es',
    'Svenska': 'sv',
    'Türkçe': 'tr',
    'Українська': 'uk',
    'Tiếng Việt': 'vi'
}

SPECIALITIES = {
    'Saúde, Medicina e Psicologia': 'Saúde, Medicina e Psicologia',
    'Matemática': 'Matemática',
    'Física': 'Física',
    'Estatística': 'Estatística',
    'Ciência da Computação': 'Ciência da Computação',
    'Ciência de Dados e Aprendizado de Máquina': 'Ciência de Dados e Aprendizado de Máquina',
    'Ciências Biológicas': 'Ciências Biológicas',
    'Ciências Sociais': 'Ciências Sociais',
    'Direito': 'Direito',
    'Engenharia': 'Engenharia',
    'Administração e Economia': 'Administração e Economia',
    'Artes e Humanidades': 'Artes e Humanidades',
    'Comércio e Logística': 'Comércio e Logística'
}

STYLES = {
    'Formal': 'Formal',
    'Informal': 'Informal',
    'Técnico': 'Técnico',
    'Conversacional': 'Conversacional',
    'Persuasivo': 'Persuasivo'
}

COMPLEXITY_LEVELS = {
    'Básico': 'Básico',
    'Intermediário': 'Intermediário',
    'Avançado': 'Avançado'
}

AVAILABLE_MODELS = [
    'gpt-3.5-turbo-0125',
    'gpt-4-turbo',
    'gpt-4o-mini',
    'gpt-4o'
]


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

        on_language_change(*args) → None:
            Callback function when the target language changes.

        update_interface_language() → None:
            Updates all interface labels to the selected language.
    """

    def __init__(self, root: Tk) -> None:
        """
        Inicializa a aplicação com a janela raiz fornecida.

        Args:
            root (Tk): A janela raiz da aplicação Tkinter.
        """
        # Atribuir a janela raiz
        self.root = root

        # Inicializar variáveis de interface
        self.title_label = self.subtitle_label = None
        self.texto_entrada = self.texto_saida = None
        self.area_option_menu = self.estilo_option_menu = self.complexity_option_menu = None
        self.bleu_score_label = None
        self.simplified_metric_labels = self.original_metric_labels = None

        # Inicializar variáveis e serviços
        self.aws_translate_service = self.openai_service = None
        self.document_service = self.readability_service = self.bleu_score_service = None

        # Inicializar variáveis de controle e configuração
        self.modelo_option_menu = None
        self.metrics_original = self.metrics_simplified = None
        self.destino_var = tk.StringVar(value='Português')
        self.area_var = tk.StringVar(value='Ciência da Computação')
        self.estilo_var = tk.StringVar(value='Informal')
        self.complexity_var = tk.StringVar(value='Intermediário')
        self.summarize_var = tk.BooleanVar()
        self.modelo_var = tk.StringVar(value='gpt-3.5-turbo-0125')
        self.max_tokens_var = tk.IntVar(value=1500)
        self.temperature_var = tk.DoubleVar(value=0.8)
        self.focus_clarity_var = self.focus_conciseness_var = self.focus_formality_var = tk.BooleanVar()

        # Inicializar caches e mapeamento de idiomas
        self.label_texts = {}
        self.translated_texts = {}
        self.language_codes = {name: code for name, code in LANGUAGES.items()}
        self.current_language_code = 'pt'  # Valor padrão

        # Dados originais e suas traduções
        self.original_specialities = SPECIALITIES
        self.original_styles = STYLES
        self.original_complexity_levels = COMPLEXITY_LEVELS
        self.translated_specialities = {}
        self.translated_styles = {}
        self.translated_complexity_levels = {}

        # Configuração da interface e inicialização dos serviços
        self.setup_root_window()
        self.initialize_services()
        self.initialize_variables()

        # Atualizar o idioma selecionado
        self.current_language_code = self.language_codes.get(self.destino_var.get(), 'pt')

        # Criar widgets da interface
        self.create_widgets()

    def setup_root_window(self):
        """
        Configurações iniciais da janela principal.

        Define o tamanho, título e subtítulo da janela.
        """
        self.root.geometry("1200x900")
        self.root.title("TraduzAI")

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
            self.readability_service = ReadabilityService()
            self.bleu_score_service = BleuScoreService()
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
        self.max_tokens_var = tk.IntVar(self.root, value=1500)
        self.metrics_original = None
        self.metrics_simplified = None

        # Set up a trace to detect changes in the target language
        self.destino_var.trace('w', self.on_language_change)

    def on_language_change(self, *args):
        """
        Callback function when the target language changes.

        Updates the interface language to match the selected target language.
        """
        selected_language = self.destino_var.get()
        new_language_code = self.language_codes.get(selected_language, 'pt')
        if new_language_code != self.current_language_code:
            self.current_language_code = new_language_code
            self.update_interface_language()

    def update_interface_language(self):
        try:
            # Obter todos os textos de rótulos para traduzir
            texts_to_translate = list(self.label_texts.keys())
            # Verificar se as traduções já estão em cache
            translations = {}
            for text in texts_to_translate:
                translations[text] = self.cached_translate_text(
                    text, self.current_language_code)
            # Atualizar rótulos com o texto traduzido
            for text, widget in self.label_texts.items():
                widget.config(text=translations[text])
            # Atualizar os OptionMenus
            self.translate_option_menus()
        except Exception as e:
            messagebox.showerror("Erro ao Traduzir Interface", str(e))

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

    def translate_option_menus(self):
        """
        Traduz as opções dos menus de seleção e atualiza os OptionMenus correspondentes.
        """
        # Tradução das especialidades
        self.translated_specialities = self.translate_options(self.original_specialities)

        # Atualização do OptionMenu de especialidades
        self.update_option_menu(
            self.area_option_menu,
            self.area_var,
            self.translated_specialities
        )

        # Tradução dos estilos
        self.translated_styles = self.translate_options(self.original_styles)

        # Atualização do OptionMenu de estilos
        self.update_option_menu(
            self.estilo_option_menu,
            self.estilo_var,
            self.translated_styles
        )

        # Tradução dos níveis de complexidade
        self.translated_complexity_levels = self.translate_options(self.original_complexity_levels)

        # Atualização do OptionMenu de níveis de complexidade
        self.update_option_menu(
            self.complexity_option_menu,
            self.complexity_var,
            self.translated_complexity_levels
        )

    def translate_options(self, options_dict):
        """
        Traduz as opções fornecidas e retorna um dicionário de traduções.

        Args:
            options_dict (dict): Dicionário de opções originais.

        Returns:
            dict: Dicionário com as opções originais e suas traduções.
        """
        translated_options = {}
        for original_text in options_dict.keys():
            translated_text = self.cached_translate_text(
                original_text, self.current_language_code)
            translated_options[original_text] = translated_text
        return translated_options

    def cached_translate_text(self, text, target_language_code):
        """
        Traduz o texto fornecido para o idioma de destino, utilizando cache.

        Args:
            text (str): Texto a ser traduzido.
            target_language_code (str): Código do idioma de destino.

        Returns:
            str: Texto traduzido.
        """
        if target_language_code not in self.translated_texts:
            self.translated_texts[target_language_code] = {}

        language_cache = self.translated_texts[target_language_code]

        if text in language_cache:
            return language_cache[text]
        else:
            translated_text, _ = self.aws_translate_service.translate_text(
                text, target_language_code)
            language_cache[text] = translated_text
            return translated_text

    @staticmethod
    def update_option_menu(option_menu, variable, translated_options):
        """
        Atualiza um OptionMenu com as opções traduzidas.

        Args:
            option_menu (tk.OptionMenu): O widget OptionMenu a ser atualizado.
            variable (tk.StringVar): A variável associada ao OptionMenu.
            translated_options (dict): Dicionário com as opções originais e traduzidas.
        """
        menu = option_menu['menu']
        menu.delete(0, 'end')

        # Mapeamento inverso das traduções para as opções originais
        inverse_translations = {v: k for k, v in translated_options.items()}

        # Obter o valor atual selecionado e mapeá-lo para a tradução
        current_value = variable.get()
        original_value = inverse_translations.get(current_value, current_value)

        # Atualizar as opções no menu
        for original_option, translated_option in translated_options.items():
            menu.add_command(
                label=translated_option,
                command=lambda value=translated_option: variable.set(value)
            )

        # Atualizar a variável com o valor traduzido
        variable.set(translated_options.get(original_value, list(translated_options.values())[0]))

    def create_title(self):
        """
        Cria o título da aplicação.

        Adiciona um rótulo na parte superior da janela com o nome da aplicação e um subtítulo.
        """
        # Criar e adicionar o título
        title_text = "TraduzAI"
        self.title_label = tk.Label(
            self.root,
            text=title_text,
            font=("Helvetica", 16, "bold")
        )
        self.title_label.pack(pady=(10, 0))  # Padding superior para espaçamento
        self.label_texts[title_text] = self.title_label  # Armazenar para tradução

        # Criar e adicionar o subtítulo abaixo do título
        subtitle_text = "Uma Solução Personalizada para Tradução Eficaz e Fluente em Diferentes Contextos"
        self.subtitle_label = tk.Label(
            self.root,
            text=subtitle_text,
            font=("Helvetica", 13, "bold")
        )
        self.subtitle_label.pack(pady=(0, 10))  # Padding inferior para espaçamento
        self.label_texts[subtitle_text] = self.subtitle_label  # Armazenar para tradução

    def create_option_menu(self, parent, label_text, variable, options):
        """
        Função auxiliar para criar um menu de opções dentro do frame fornecido.

        Args:
            parent (tk.Widget): Widget pai onde o menu será adicionado.
            label_text (str): Texto do rótulo do menu.
            variable (tk.Variable): Variável associada ao menu de opções.
            options (list): Lista de opções disponíveis no menu.

        Returns:
            tk.OptionMenu: O OptionMenu criado.
        """
        label = tk.Label(parent, text=label_text, font=("Helvetica", 12))
        label.pack(pady=(10, 0))
        self.label_texts[label_text] = label  # Armazenar para tradução

        menu = tk.OptionMenu(parent, variable, *options)
        menu.config(width=25)
        menu.pack(pady=(0, 10))

        return menu

    def create_option_menus(self, parent):
        """
        Cria todos os menus de opções principais dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde os menus serão adicionados.
        """
        # Primeiro, criar o OptionMenu 'Idioma de destino'
        self.create_option_menu(
            parent,
            "Idioma de destino:",
            self.destino_var,
            LANGUAGES.keys()
        )

        # Em seguida, criar os demais OptionMenus
        self.area_option_menu = self.create_option_menu(
            parent,
            "Área técnica:",
            self.area_var,
            self.original_specialities.keys()
        )
        self.estilo_option_menu = self.create_option_menu(
            parent,
            "Estilo de escrita:",
            self.estilo_var,
            self.original_styles.keys()
        )
        self.modelo_option_menu = self.create_option_menu(
            parent,
            "Modelo OpenAI:",
            self.modelo_var,
            AVAILABLE_MODELS
        )

    def create_complexity_option_menu(self, parent):
        """
        Cria o menu de seleção de nível de complexidade.

        Args:
            parent (tk.Widget): Frame onde o menu será adicionado.
        """
        self.complexity_option_menu = self.create_option_menu(
            parent,
            "Nível de Complexidade:",
            self.complexity_var,
            self.original_complexity_levels.keys()
        )

    @staticmethod
    def get_original_option(selected_value, translated_options):
        """
        Retorna a opção original a partir do valor selecionado traduzido.

        Args:
            selected_value (str): O valor selecionado (traduzido).
            translated_options (dict): Dicionário com as opções originais e traduzidas.

        Returns:
            str: A opção original correspondente.
        """
        inverse_translations = {v: k for k, v in translated_options.items()}
        return inverse_translations.get(selected_value, selected_value)

    def create_focus_aspects_checkboxes(self, parent):
        """
        Cria as caixas de seleção para focar em aspectos específicos dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde as caixas de seleção serão adicionadas.
        """
        label_text = "Focar em:"
        label = tk.Label(parent, text=label_text, font=("Helvetica", 12))
        label.pack(pady=(10, 0))
        self.label_texts[label_text] = label  # Armazenar para tradução

        checkbox_clarity = tk.Checkbutton(parent, text="Clareza", variable=self.focus_clarity_var,
                                          font=("Helvetica", 12))
        checkbox_clarity.pack(pady=(0, 5))
        self.label_texts["Clareza"] = checkbox_clarity  # Armazenar para tradução

        checkbox_conciseness = tk.Checkbutton(parent, text="Concisão", variable=self.focus_conciseness_var,
                                              font=("Helvetica", 12))
        checkbox_conciseness.pack(pady=(0, 5))
        self.label_texts["Concisão"] = checkbox_conciseness  # Armazenar para tradução

        checkbox_formality = tk.Checkbutton(parent, text="Formalidade", variable=self.focus_formality_var,
                                            font=("Helvetica", 12))
        checkbox_formality.pack(pady=(0, 5))
        self.label_texts["Formalidade"] = checkbox_formality  # Armazenar para tradução

    def create_api_parameter_entries(self, parent):
        """
        Cria os campos para ajuste dos parâmetros da API OpenAI dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde os campos serão adicionados.
        """
        label_text = "Parâmetros da API OpenAI:"
        label = tk.Label(parent, text=label_text, font=("Helvetica", 12, "bold"))
        label.pack(pady=(10, 0))
        self.label_texts[label_text] = label  # Armazenar para tradução

        # Frame principal para os parâmetros
        params_frame = tk.Frame(parent)
        params_frame.pack(pady=(5, 5))

        # Temperature
        temp_label_text = "Temperature:"
        temperature_label = tk.Label(params_frame, text=temp_label_text, font=("Helvetica", 12))
        temperature_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.label_texts[temp_label_text] = temperature_label  # Armazenar para tradução

        temperature_entry = tk.Entry(params_frame, textvariable=self.temperature_var, width=5)
        temperature_entry.grid(row=0, column=1, padx=5, pady=5)

        # Max Tokens
        max_tokens_label_text = "Max Tokens:"
        max_tokens_label = tk.Label(params_frame, text=max_tokens_label_text, font=("Helvetica", 12))
        max_tokens_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.label_texts[max_tokens_label_text] = max_tokens_label  # Armazenar para tradução

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
        text = "Resumir"
        checkbox_summarize = tk.Checkbutton(
            parent,
            text=text,
            variable=self.summarize_var,
            font=("Helvetica", 12)
        )
        checkbox_summarize.pack(pady=(10, 10))
        self.label_texts[text] = checkbox_summarize  # Armazenar para tradução

    def create_translate_button(self, parent):
        """
        Cria o botão para realizar a tradução e simplificação dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde o botão será adicionado.
        """
        text = "Simplificar Linguagem e Traduzir"
        button = self.create_button(
            parent=parent,
            text=text,
            command=self.translate_text,
            bg_color="#4CAF50",
            padx=20,
            pady=10
        )
        self.label_texts[text] = button  # Armazenar para tradução

    @staticmethod
    def create_button(parent, text, command, bg_color, **pack_options):
        """
        Função auxiliar para criar botões.

        Args:
            parent (tk.Widget): Widget pai onde o botão será adicionado.
            text (str): Texto exibido no botão.
            command (callable): Função chamada quando o botão é clicado.
            bg_color (str): Cor de fundo do botão.
            **pack_options: opções adicionais para o metodo pack().

        Returns:
            tk.Button: O botão criado.
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
        return button

    def create_text_input(self, parent):
        """
        Cria a área de entrada de texto dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde a área de entrada será adicionada.
        """
        label_text = "Texto para Simplificar e Traduzir:"
        label_entrada = tk.Label(
            parent,
            text=label_text,
            font=("Helvetica", 12, "bold")
        )
        label_entrada.pack(pady=(10, 0))
        self.label_texts[label_text] = label_entrada  # Armazenar para tradução

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

        # Criar e armazenar o botão "Importar Documento"
        button_import = self.create_button(button_frame, "Importar Documento", self.import_document, "#2196F3",
                                           side=tk.LEFT, padx=5)
        self.label_texts["Importar Documento"] = button_import  # Armazenar para tradução

        # Criar e armazenar o botão "Exportar Documento"
        button_export = self.create_button(button_frame, "Exportar Documento", self.export_document, "#FF9800",
                                           side=tk.LEFT, padx=5)
        self.label_texts["Exportar Documento"] = button_export  # Armazenar para tradução

    def create_text_output(self, parent):
        """
        Cria a área de saída de texto dentro do frame fornecido.

        Args:
            parent (tk.Widget): Frame onde a área de saída será adicionada.
        """
        label_text = "Texto Simplificado e Traduzido:"
        label_saida = tk.Label(
            parent,
            text=label_text,
            font=("Helvetica", 12, "bold")
        )
        label_saida.pack(pady=(10, 0))
        self.label_texts[label_text] = label_saida  # Armazenar para tradução

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
        self.label_texts["Métricas do Texto Original"] = original_frame  # Armazenar para tradução

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
            self.label_texts[name + ":"] = label_name  # Armazenar para tradução
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
        original_desc_label = tk.Label(
            original_frame,
            text=original_description,
            justify='left',
            wraplength=400,
            font=("Courier", 10)
        )
        original_desc_label.pack(padx=10, pady=(10, 0))
        self.label_texts[original_description] = original_desc_label  # Armazenar para tradução

        # Frame para as métricas do texto simplificado
        simplified_frame = tk.LabelFrame(parent, text="Métricas do Texto Simplificado", font=("Helvetica", 12, "bold"))
        simplified_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.label_texts["Métricas do Texto Simplificado"] = simplified_frame  # Armazenar para tradução

        # Frame interno para organizar as métricas em tabela

        simplified_metrics_frame = tk.Frame(simplified_frame)
        simplified_metrics_frame.pack(padx=10, pady=10)

        # Labels para as métricas do texto simplificado
        self.simplified_metric_labels = {}

        for i, name in enumerate(metric_names):
            label_name = tk.Label(simplified_metrics_frame, text=name + ":", anchor='w', font=("Helvetica", 11, "bold"))
            label_name.grid(row=i, column=0, sticky='w', padx=(0, 5), pady=2)
            self.label_texts[name + ":"] = label_name  # Armazenar para tradução
            label_value = tk.Label(simplified_metrics_frame, text="", anchor='e', font=("Helvetica", 11))
            label_value.grid(row=i, column=1, sticky='e', pady=2)
            self.simplified_metric_labels[name] = label_value

        # Adiciona o label para o BLEU Score
        row_index = len(metric_names)
        bleu_label_name = tk.Label(simplified_metrics_frame, text='BLEU Score:', anchor='w',
                                   font=("Helvetica", 11, "bold"))
        bleu_label_name.grid(row=row_index, column=0, sticky='w', padx=(0, 5), pady=2)
        self.label_texts['BLEU Score:'] = bleu_label_name  # Armazenar para tradução
        self.bleu_score_label = tk.Label(simplified_metrics_frame, text="", anchor='e', font=("Helvetica", 11))
        self.bleu_score_label.grid(row=row_index, column=1, sticky='e', pady=2)

    def translate_text(self) -> None:
        """
        Realiza a simplificação e tradução do texto inserido.

        Este metodo executa os seguintes passos:
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
        area_tecnica = self.get_original_option(self.area_var.get(), self.translated_specialities)
        estilo = self.get_original_option(self.estilo_var.get(), self.translated_styles)
        summarize = self.summarize_var.get()
        modelo_selecionado = self.modelo_var.get()
        complexity_level = self.get_original_option(self.complexity_var.get(), self.translated_complexity_levels)

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

            # Armazena as métricas para exportação
            self.metrics_original = metrics_original
            self.metrics_simplified = metrics_simplified

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
        como TXT, PDF ou DOCX, incluindo as métricas de legibilidade e o BLEU Score.

        Exceções:
            - Exibe uma mensagem de erro se não houver texto para exportar ou
              se ocorrer algum problema durante a exportação.
        """
        output_text = self.texto_saida.get("1.0", END).strip()
        if not output_text:
            messagebox.showwarning("Nenhum texto para exportar", "Não há texto traduzido e simplificado para exportar.")
            return

        if self.metrics_original is None or self.metrics_simplified is None:
            messagebox.showwarning("Métricas Indisponíveis", "As métricas não estão disponíveis para exportação.")
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

                # Obter o BLEU Score a partir do label
                bleu_score_text = self.bleu_score_label.cget("text")
                bleu_score = float(bleu_score_text) if bleu_score_text else None

                # Passar o BLEU Score para o método de exportação
                self.document_service.export_document(
                    text,
                    file_path,
                    format,
                    self.metrics_original,
                    self.metrics_simplified,
                    bleu_score  # Passando o BLEU Score
                )
                messagebox.showinfo("Exportação bem-sucedida", f"Documento exportado com sucesso: {file_path}")
            except Exception as e:
                messagebox.showerror("Erro ao Exportar Documento", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
