import importlib.metadata

pacotes = [
    'annotated-types',
    'anyio',
    'awscli',
    'boto3',
    'botocore',
    'certifi',
    'charset-normalizer',
    'colorama',
    'distro',
    'docutils',
    'ebooklib',
    'h11',
    'httpcore',
    'httpx',
    'idna',
    'jiter',
    'jmespath',
    'langdetect',
    'lxml',
    'numpy',
    'openai',
    'packaging',
    'pillow',
    'pipdeptree',
    'portalocker',
    'pyasn1',
    'pydantic',
    'pydantic_core',
    'PyPDF2',
    'pyphen',
    'python-dateutil',
    'python-docx',
    'python-dotenv',
    'pywin32',
    'PyYAML',
    'regex',
    'reportlab',
    'requests',
    'rsa',
    's3transfer',
    'sacrebleu',
    'setuptools',
    'six',
    'sniffio',
    'tabulate',
    'textstat',
    'tqdm',
    'typing_extensions',
    'urllib3'
]

for nome_pacote in pacotes:
    try:
        versao = importlib.metadata.version(nome_pacote)
        print(f"{nome_pacote}: {versao}")
    except importlib.metadata.PackageNotFoundError:
        print(f"{nome_pacote}: Não está instalado")
