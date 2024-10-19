import os
import tkinter as tk
from tkinter import END, Tk, messagebox, filedialog
from services.aws_translate_service import AwsTranslateService
from services.openai_service import OpenAIService
from services.document_service import DocumentService

# Constantes separadas para melhorar a organização
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
    'Geral',
    'Medicina',
    'Psicologia',
    'Direito',
    'Matemática',
    'Química',
    'Física',
    'Programação',
    'Filosofia',
    'Engenharia Civil',
    'Engenharia Mecânica',
    'Engenharia Elétrica',
    'Engenharia Química',
    'Engenharia de Produção',
    'Engenharia de Computação',
    'Engenharia Ambiental',
    'Biologia',
    'Bioquímica',
    'Genética',
    'Medicina Veterinária',
    'Nutrição',
    'Biomedicina',
    'Sociologia',
    'Antropologia',
    'Ciência Política',
    'Educação',
    'Psicopedagogia',
    'Direito Penal',
    'Direito Civil',
    'Direito Tributário',
    'Direito Trabalhista',
    'Direito Ambiental',
    'Direito Internacional',
    'Direito de Família',
    'Direito Empresarial',
    'Direito Constitucional',
    'Economia',
    'Administração de Empresas',
    'Administração Pública',
    'Contabilidade',
    'Finanças',
    'Marketing',
    'Ciência da Computação',
    'Sistemas de Informação',
    'Engenharia de Software',
    'Segurança da Informação',
    'Análise de Dados',
    'Inteligência Artificial',
    'Matemática Aplicada',
    'Estatística',
    'Física Aplicada',
    'Química Aplicada',
    'Geografia',
    'Literatura',
    'Artes Visuais',
    'Música',
    'Teatro',
    'Cinema',
    'Fisioterapia',
    'Terapia Ocupacional',
    'Enfermagem',
    'Saúde Pública',
    'Psicologia Clínica',
    'Medicina Esportiva',
    'Logística',
    'Comércio Exterior',
    'Relações Internacionais',
    'Gestão de Recursos Humanos',
    'Engenharia Biomédica',
    'Ciência de Dados'
]

ESTILOS = [
    'Formal',
    'Informal',
    'Técnico',
    'Conversacional',
    'Persuasivo',
    'Narrativo',
    'Acadêmico',
    'Conciso',
    'Humorístico',
    'Descritivo',
    'Diretivo',
    'Objetivo',
    'Inspirador',
    'Jargão Especializado'
]

MODELOS_DISPONIVEIS = [
    'gpt-3.5-turbo-0125',
    'gpt-4-turbo',
    'gpt-4o-mini',
    'gpt-4o'
]


class TranslationApp:
    def __init__(self, root: Tk) -> None:
        self.modelo_var = None
        self.summarize_var = None
        self.destino_var = None
        self.area_var = None
        self.estilo_var = None
        self.texto_saida = None
        self.texto_entrada = None
        self.document_service = None
        self.openai_service = None
        self.aws_translate_service = None
        self.root = root
        self.setup_root_window()
        self.initialize_services()
        self.initialize_variables()
        self.create_widgets()

    def setup_root_window(self):
        """Configurações iniciais da janela principal."""
        self.root.geometry("600x800")
        self.root.title("Tradutor e Simplificador de Textos Técnicos")

    def initialize_services(self):
        """Inicializa os serviços necessários."""
        try:
            self.aws_translate_service = AwsTranslateService()
            self.openai_service = OpenAIService()
            self.document_service = DocumentService()
        except Exception as e:
            messagebox.showerror("Erro ao Inicializar", str(e))
            self.root.destroy()
            raise

    def initialize_variables(self):
        """Inicializa as variáveis usadas na interface."""
        self.texto_entrada = None
        self.texto_saida = None
        self.estilo_var = tk.StringVar(self.root, value='Informal')
        self.area_var = tk.StringVar(self.root, value='Geral')
        self.destino_var = tk.StringVar(self.root, value='Português')
        self.summarize_var = tk.BooleanVar()
        self.modelo_var = tk.StringVar(self.root, value='gpt-3.5-turbo-0125')

    def create_widgets(self) -> None:
        """Cria os widgets da interface gráfica."""
        self.create_title()
        self.create_option_menus()
        self.create_text_input()
        self.create_import_export_buttons()
        self.create_summarize_checkbox()
        self.create_translate_button()
        self.create_text_output()

    def create_title(self):
        """Cria o título da aplicação."""
        title_label = tk.Label(
            self.root,
            text="Sistema de Tradução e Simplificação de Textos Técnicos",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=10)

    def create_option_menus(self):
        """Cria os menus de opções."""
        self.create_option_menu("Selecione o idioma de destino:", self.destino_var, LANGUAGES.keys())
        self.create_option_menu("Selecione a área técnica:", self.area_var, AREAS_TECNICAS)
        self.create_option_menu("Selecione o estilo de escrita:", self.estilo_var, ESTILOS)
        self.create_option_menu("Selecione o modelo OpenAI para simplificação:", self.modelo_var, MODELOS_DISPONIVEIS)

    def create_option_menu(self, label_text, variable, options):
        """Função auxiliar para criar um menu de opções."""
        label = tk.Label(self.root, text=label_text, font=("Helvetica", 12))
        label.pack(pady=(10, 0))
        menu = tk.OptionMenu(self.root, variable, *options)
        menu.config(width=20)
        menu.pack(pady=(0, 10))

    def create_text_input(self):
        """Cria a caixa de texto para entrada."""
        label_entrada = tk.Label(
            self.root,
            text="Digite o texto para simplificar e traduzir:",
            font=("Helvetica", 12)
        )
        label_entrada.pack(pady=(10, 0))
        self.texto_entrada = tk.Text(self.root, height=10, width=70, wrap='word')
        self.texto_entrada.pack(pady=(5, 10))

    def create_import_export_buttons(self):
        """Cria os botões de importar e exportar."""
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=(5, 10))
        self.create_button(button_frame, "Importar Documento", self.import_document, "#2196F3", side=tk.LEFT, padx=5)
        self.create_button(button_frame, "Exportar Documento", self.export_document, "#FF9800", side=tk.LEFT, padx=5)

    def create_summarize_checkbox(self):
        """Cria o checkbox para resumir o texto."""
        checkbox_summarize = tk.Checkbutton(
            self.root,
            text="Resumir o texto",
            variable=self.summarize_var,
            font=("Helvetica", 12)
        )
        checkbox_summarize.pack(pady=(5, 10))

    def create_translate_button(self):
        """Cria o botão de tradução."""
        self.create_button(
            parent=self.root,
            text="Simplificar e Traduzir",
            command=self.traduzir_texto,
            bg_color="#4CAF50",
            pady=10
        )

    def create_text_output(self):
        """Cria a caixa de texto para saída."""
        label_saida = tk.Label(
            self.root,
            text="Texto simplificado e traduzido:",
            font=("Helvetica", 12)
        )
        label_saida.pack(pady=(10, 0))
        self.texto_saida = tk.Text(self.root, height=15, width=70, wrap='word', state='disabled')
        self.texto_saida.pack(pady=(5, 10))

    @staticmethod
    def create_button(parent, text, command, bg_color, **pack_options):
        """Função auxiliar para criar botões.

        Args:
            parent (tk. Widget): Widget pai onde o botão será adicionado.
            text (str): Texto exibido no botão.
            command (callable): Função chamada ao clicar no botão.
            bg_color (str): Cor de fundo do botão.
            **pack_options: Opções adicionais para o metodo pack().
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
            texto_simplificado = self.openai_service.simplify_text(
                texto, area_tecnica, estilo, summarize, modelo_selecionado
            )
            texto_traduzido = self.aws_translate_service.translate_text(
                texto_simplificado, codigo_idioma_destino
            )
            self.mostrar_resultado(texto_traduzido)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def mostrar_resultado(self, texto: str) -> None:
        """Exibe o resultado da tradução e simplificação."""
        self.texto_saida.config(state='normal')
        self.texto_saida.delete("1.0", END)
        self.texto_saida.insert(END, texto)
        self.texto_saida.config(state='disabled')

    def import_document(self):
        """Importa texto de um documento."""
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
        """Exporta o texto de saída para um documento."""
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
