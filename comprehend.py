import tkinter as tk
from tkinter import END

from dotenv import load_dotenv
import boto3
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Obtém as credenciais e região do arquivo .env
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION = os.getenv('AWS_REGION')

root = tk.Tk()
root.geometry("400x500")
root.title("AWS Tradutor")

# Opções de idiomas
languages = {
    'Inglês': 'en',
    'Espanhol': 'es',
    'Francês': 'fr',
    'Alemão': 'de',
    'Português': 'pt',
    'Italiano': 'it',
    'Chinês (Simplificado)': 'zh',
    'Japonês': 'ja',
    'Coreano': 'ko',
    'Russo': 'ru'
}

nomes_idiomas = list(languages.keys())

# Seleção do idioma de origem
label_origem = tk.Label(root, text="Selecione o idioma de origem:")
label_origem.pack()
origem_var = tk.StringVar(root)
origem_var.set('Inglês')  # valor padrão
menu_origem = tk.OptionMenu(root, origem_var, *nomes_idiomas)
menu_origem.pack()

# Seleção do idioma de destino
label_destino = tk.Label(root, text="Selecione o idioma de destino:")
label_destino.pack()
destino_var = tk.StringVar(root)
destino_var.set('Português')  # valor padrão
menu_destino = tk.OptionMenu(root, destino_var, *nomes_idiomas)
menu_destino.pack()

# Label de entrada
label_entrada = tk.Label(root, text="Digite o texto para traduzir:")
label_entrada.pack()

# Caixa de texto de entrada
texto_entrada = tk.Text(root, height=10)
texto_entrada.pack()

# Label de saída
label_saida = tk.Label(root, text="Texto traduzido:")
label_saida.pack()

# Caixa de texto de saída
texto_saida = tk.Text(root, height=10)
texto_saida.pack()


def traduzir_texto():
    # Inicializa o cliente do AWS Translate com as credenciais do arquivo .env
    client = boto3.client(
        service_name='translate',
        region_name=REGION,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )

    # Obtém o texto da caixa de entrada
    texto = texto_entrada.get("1.0", "end-1c")  # Remove o último caractere de nova linha
    print("Texto de entrada:", texto)

    # Obtém os códigos dos idiomas selecionados
    codigo_idioma_origem = languages[origem_var.get()]
    codigo_idioma_destino = languages[destino_var.get()]

    # Tradução do texto
    response = client.translate_text(
        Text=texto,
        SourceLanguageCode=codigo_idioma_origem,
        TargetLanguageCode=codigo_idioma_destino
    )
    texto_traduzido = response['TranslatedText']
    print("Texto traduzido:", texto_traduzido)

    # Exibe o texto traduzido na caixa de saída
    texto_saida.delete("1.0", END)  # Limpa o conteúdo anterior
    texto_saida.insert(END, texto_traduzido)


# Botão de tradução
botao_traduzir = tk.Button(root, height=1, width=10, text="Traduzir", command=traduzir_texto)
botao_traduzir.pack()

root.mainloop()
