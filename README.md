# AWS Tradutor com Interface Gráfica em Python

## Resumo

Este projeto visa desenvolver um sistema de tradução automática que, além de traduzir de uma língua para outra, seja
capaz de interpretar e traduzir jargões técnicos de áreas como medicina, direito, matemática, química, física,
programação, filosofia, entre outras ciências exatas e naturais, para uma linguagem cotidiana e acessível para pessoas
que não são especialistas na área.

O sistema utiliza o **Amazon Translate** como base, incorporando modelos avançados de **Deep Learning**, como Redes
Neurais Recorrentes (RNNs) com atenção e a arquitetura **Transformer**, treinados em conjuntos de dados específicos de
domínio e estilo para aprimorar a qualidade das traduções.

A solução inclui uma interface gráfica intuitiva desenvolvida em Python com **Tkinter**, onde os usuários podem inserir
textos e selecionar o idioma de destino. O sistema detecta automaticamente o idioma de origem e fornece uma tradução que
não apenas mantém a precisão técnica, mas também converte termos complexos em uma linguagem clara e acessível ao público
geral.

Para facilitar a integração com outras plataformas, o projeto disponibiliza uma API RESTful, construída com **AWS Lambda
** e **API Gateway**, permitindo que empresas automatizem o atendimento a clientes em diversos idiomas e incorporem a
funcionalidade de tradução em suas aplicações.

O projeto também inclui técnicas de monitoramento da qualidade das traduções e ajuste fino dos modelos de Deep Learning,
utilizando métricas como o **BLEU score** e o feedback dos usuários. O processo contínuo de aprendizado visa melhorar a
precisão e fluidez das traduções, especialmente em domínios especializados com termos técnicos e jargões complexos.

A infraestrutura do sistema é baseada na AWS, utilizando serviços como **Amazon S3** para armazenamento de dados e *
*Amazon CloudWatch** para monitoramento e registro de eventos, garantindo escalabilidade, segurança e alta
disponibilidade.

**Palavras-chave**: Tradução Automática, Jargões Técnicos, Deep Learning, Redes Neurais Recorrentes, Transformer, Amazon
Translate, Personalização, Feedback do Usuário, Atendimento ao Cliente, Monitoramento de Qualidade.

---

## Índice

- [Requisitos](#0-requisitos)
- [Instalação](#1-instalação)
    - [1.1 Clonar o Repositório](#11-clonar-o-repositório)
    - [1.2 Criar e Configurar o Arquivo `.env`](#12-criar-e-configurar-o-arquivo-env)
    - [1.3 Instalar as Dependências](#13-instalar-as-dependências)
- [Código-Fonte](#2-código-fonte)
- [Como Executar](#3-como-executar)
- [Como Usar](#4-como-usar)
    - [4.1 Interface do Usuário](#41-interface-do-usuário)
    - [4.2 Elementos da Interface](#42-elementos-da-interface)
    - [4.3 Processo de Tradução](#43-processo-de-tradução)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## 0-Requisitos

- **Python 3.8** ou superior
- Conta na **AWS** com acesso ao **Amazon Translate**

---

## 1-Instalação

### 1.1 Clonar o Repositório

```bash
git clone https://github.com/TraduzAI/aws-translator-with-python
cd aws-translator-with-python
```

### 1.2 Criar e Configurar o Arquivo `.env`

```dotenv
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
```

#### 1.2 Preencha os campos com suas credenciais da AWS:

- **AWS_ACCESS_KEY_ID**: ID da chave de acesso da AWS
- **AWS_SECRET_ACCESS_KEY**: Chave de acesso secreta da AWS
- **AWS_REGION**: Região da AWS onde o serviço Amazon Translate está disponível (por exemplo, us-east-1)

#### 1.3 Instalar as Dependências

```bash
pip install -r requirements.txt
```

## 2. Código-Fonte

O código principal está contido no arquivo app.py e é estruturado da seguinte forma:

```python 
import tkinter as tk
from tkinter import END, Tk
from dotenv import load_dotenv
import boto3
import os


class AWSTranslatorApp:
    def __init__(self, root: Tk) -> None:
        # Inicialização da interface e carregamento das credenciais
        pass

    def load_aws_credentials(self) -> None:
        # Carrega as credenciais AWS do arquivo .env
        pass

    def create_widgets(self) -> None:
        # Cria os componentes da interface gráfica
        pass

    def traduzir_texto(self) -> None:
        # Realiza a tradução usando o Amazon Translate
        pass

    def mostrar_resultado(self, texto: str) -> None:
        # Exibe o texto traduzido na interface
        pass

    def mostrar_mensagem(self, mensagem: str) -> None:
        # Exibe mensagens de erro ou aviso na interface
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = AWSTranslatorApp(root)
    root.mainloop()
```

## 3. Como Executar

Após ter clonado o repositório e configurado o arquivo `.env`, você pode executar o aplicativo com o seguinte comando:

```bash
python app.py
```

Nota: Certifique-se de que o arquivo app.py está no diretório atual e de que as credenciais da AWS foram corretamente
configuradas no arquivo .env.

## 4. Como Usar

### 4.1 Interface do Usuário:

A interface do usuário foi desenvolvida com a biblioteca Tkinter em Python, permitindo uma interação intuitiva e
amigável com o sistema de tradução.

### 4.2 Elementos da Interface:

- **Caixa de Texto (Entrada)**: Permite inserir o texto que você deseja traduzir.
- **Menu Suspenso (Seleção de Idioma)**: Permite escolher o idioma de destino para a tradução.
- **Botão "Traduzir"**: inicia o processo de tradução do texto inserido.
- **Caixa de Texto (Saída)**: Exibe o texto traduzido após a conclusão do processo.
- **Mensagens de Erro**: Exibidas em caso de falha na tradução ou erro de conexão com a AWS.

### 4.3 Processo de Tradução:

- **Detecção Automática de Idioma**: O sistema detecta automaticamente o idioma do texto de origem.
- **Tradução de Texto**: O texto é traduzido para o idioma selecionado no menu suspenso.
- **Exibição do Resultado**: O texto traduzido é exibido na caixa de texto inferior.

