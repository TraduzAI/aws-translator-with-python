# TraduzAI

## Uma Solução Personalizada para Tradução Eficaz e Fluente em Diferentes Contextos

### Resumo

Este projeto visa desenvolver um sistema de tradução automática que, além de traduzir de uma língua para outra, seja
capaz de interpretar e traduzir jargões técnicos de áreas como medicina, psicologia, direito, matemática, química,
física, programação, filosofia, entre outras ciências exatas e naturais, para uma linguagem cotidiana e acessível para
pessoas que não são especialistas na área.

O sistema utiliza o **Amazon Translate** como base, incorporando modelos avançados de **Deep Learning**, como Redes
Neurais Recorrentes (RNNs) com atenção e a arquitetura **Transformer**, treinados em conjuntos de dados específicos de
domínio e estilo para aprimorar a qualidade das traduções.

A solução inclui uma interface gráfica intuitiva desenvolvida em Python com **Tkinter**, onde os usuários podem inserir
textos ou importar arquivos e selecionar o idioma de destino. O sistema detecta automaticamente o idioma de origem e
fornece uma tradução que não apenas mantém a precisão técnica, mas também converte termos complexos em uma linguagem
clara e acessível ao público geral.

Para facilitar a integração com outras plataformas, o projeto disponibiliza funcionalidades para exportar os resultados
em diferentes formatos, como **TXT**, **PDF** e **DOCX**, permitindo que empresas automatizem o atendimento a clientes
em diversos idiomas e incorporem a funcionalidade de tradução em suas aplicações.

Além disso, o sistema realiza análises de legibilidade utilizando seis métricas distintas: **Índice de Flesch Reading
Ease**, **Grau de Flesch-Kincaid**, **Índice SMOG**, **Índice de Coleman-Liau**, **Índice Automático de Legibilidade (ARI)** 
e **Pontuação de Dale-Chall**. Essas métricas auxiliam na avaliação da facilidade de leitura e compreensão dos
textos traduzidos e simplificados, garantindo que a linguagem seja adequada ao público-alvo.

O projeto também inclui técnicas de monitoramento da qualidade das traduções e ajuste fino dos modelos de **Deep
Learning**, utilizando métricas como o **BLEU score** e o feedback dos usuários. O processo contínuo de aprendizado visa
melhorar a precisão e fluidez das traduções, especialmente em domínios especializados com termos técnicos e jargões
complexos.

A infraestrutura do sistema é baseada na **AWS**, utilizando serviços como **Amazon S3** para armazenamento de dados e *
*Amazon CloudWatch** para monitoramento e registro de eventos, garantindo escalabilidade, segurança e alta
disponibilidade.

### Palavras-chave

Tradução Automática, Jargões Técnicos, Deep Learning, Redes Neurais Recorrentes, Transformer, Amazon Translate,
Personalização, Feedback do Usuário, Atendimento ao Cliente, Exportação de Arquivos, Monitoramento de Qualidade,
Legibilidade, Métricas de Legibilidade.

---

## Índice

1. [Requisitos](#1-requisitos)
2. [Instalação](#2-instalação)
3. [Código-Fonte](#3-código-fonte)
4. [Como Executar](#4-como-executar)
5. [Como Usar](#5-como-usar)
6. [Contribuição](#6-contribuição)
7. [Licença](#7-licença)

---

### 1. Requisitos

- Python 3.12 ou superior
- Conta na AWS com acesso ao Amazon Translate
- Chave de API da OpenAI
- **Bibliotecas Python necessárias**:

```plaintext
python-dotenv~=1.0.1
boto3~=1.35.37
awscli~=1.35.2
openai==1.51.2
python-docx~=0.8.11
reportlab~=3.6.13
PyPDF2~=3.0.1
ebooklib~=0.18
textstat==0.7.4
langdetect==1.0.9
```

---

## 2. Instalação

### 2.1 Clonar o Repositório

```bash
git clone https://github.com/TraduzAI/aws-translator-with-python
cd aws-translator-with-python
```

### 2.2 Criar e Configurar o Arquivo .env

Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

```dotenv
AWS_ACCESS_KEY_ID=suachaveAWS
AWS_SECRET_ACCESS_KEY=suasecretAWS
AWS_REGION=us-east-1
OPENAI_API_KEY=suaChaveOpenAI
```

### 2.3 Instalar as Dependências

```bash
pip install -r requirements.txt
```

---

## 3. Código-Fonte

A estrutura dos diretórios é a seguinte:

```plaintext
aws-translator-with-python/
├── main.py
├── requirements.txt
└── services/
    ├── __init__.py
    ├── aws_translate_service.py
    ├── openai_service.py
    ├── document_service.py
    └── readability_service.py
```

## 4. Como Executar

Após clonar o repositório e configurar o arquivo `.env`, execute o aplicativo com:

```bash
python main.py
```

---

## 5. Como Usar

### 5.1 Interface do Usuário

Desenvolvida com Tkinter para interação intuitiva.

### 5.2 Elementos da Interface

- **Seleção de Idioma**: Escolha do idioma de destino.
- **Seleção da Área Técnica**: Definição da área do texto.
- **Modelo OpenAI**: Escolha do modelo para simplificação.
- **Checkbox "Resumir"**: Resumo opcional.
- **Botões de Exportação**: Exportar como TXT, PDF ou DOCX.




### 5.3 Métricas de Legibilidade

#### Métricas do Texto Original e Texto Simplificado

- **Índice de Flesch Reading Ease**: Mede a facilidade de leitura; valores mais altos indicam texto mais fácil.
- **Grau de Flesch-Kincaid**: Indica o nível escolar necessário; valores mais baixos indicam texto mais acessível.
- **Índice SMOG**: Estima os anos de educação necessários; valores mais baixos são melhores.
- **Índice de Coleman-Liau**: Baseado em caracteres por palavra e palavras por frase; valores mais baixos indicam maior
  facilidade.
- **Índice Automático de Legibilidade (ARI)**: Usa caracteres por palavra e palavras por frase; valores mais baixos
  indicam texto mais simples.
- **Pontuação de Dale-Chall**: Compara com uma lista de palavras familiares; valores mais baixos indicam texto mais
  fácil.

---

## 6. Contribuição

1. Fork o repositório.
2. Crie uma branch: `git checkout -b feature/nova-feature`.
3. Commit: `git commit -m "Adiciona nova feature"`.
4. Push: `git push origin feature/nova-feature`.
5. Abra um Pull Request.

---

## 7. Licença

Este projeto está sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.

---
