import importlib.metadata

pacotes = [
    'python-dotenv',
    'boto3',
    'awscli',
    'openai',
    'python-docx',
    'reportlab',
    'PyPDF2',
    'ebooklib',
    'textstat',
    'langdetect'
]

for nome_pacote in pacotes:
    try:
        versao = importlib.metadata.version(nome_pacote)
        print(f"{nome_pacote}: {versao}")
    except importlib.metadata.PackageNotFoundError:
        print(f"{nome_pacote}: Não está instalado")
