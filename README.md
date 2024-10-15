# TraduzAI

## A Personalized Solution for Effective and Fluent Translation in Different Contexts

### Resumo

Este projeto visa desenvolver um sistema de tradução automática que, além de traduzir de uma língua para outra, seja
capaz de interpretar e traduzir jargões técnicos de áreas como medicina, psicologia, direito, matemática, química, física,
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

### Índice

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

### 0-Requisitos

- **Python 3.12** ou superior
- Conta na **AWS** com acesso ao **Amazon Translate**

---

### 1-Instalação

#### 1.1 Clonar o Repositório

```bash
git clone https://github.com/TraduzAI/aws-translator-with-python
cd aws-translator-with-python
```

#### 1.2 Criar e Configurar o Arquivo `.env`

```dotenv
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
OPENAI_API_KEY=
```

##### 1.2 Preencha os campos com suas credenciais da AWS e OpenAI:

- **AWS_ACCESS_KEY_ID**: ID da chave de acesso da AWS
- **AWS_SECRET_ACCESS_KEY**: Chave de acesso secreta da AWS
- **AWS_REGION**: Região da AWS onde o serviço Amazon Translate está disponível (por exemplo, us-east-1)
- **OPENAI_API_KEY**: Chave de acesso da API da OpenAI

##### 1.3 Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 2. Código-Fonte

O código principal agora está dividido em diferentes módulos para separar as responsabilidades e facilitar a manutenção. A estrutura dos diretórios é a seguinte:

```
aws-translator-with-python/
│
├── main.py
├── services/
│   ├── __init__.py
│   ├── aws_translate_service.py
│   └── openai_service.py
```

- **`main.py`**: Contém a interface gráfica utilizando Tkinter e faz uso dos serviços de tradução e simplificação.
- **`services/aws_translate_service.py`**: Contém a lógica para tradução utilizando o AWS Translate.
- **`services/openai_service.py`**: Contém a lógica para simplificação de texto utilizando a API da OpenAI.

### 3. Como Executar

Após ter clonado o repositório e configurado o arquivo `.env`, você pode executar o aplicativo com o seguinte comando:

```bash
python main.py
```

Nota: Certifique-se de que o arquivo `main.py` está no diretório atual e de que as credenciais da AWS e OpenAI foram corretamente configuradas no arquivo `.env`.

### 4. Como Usar

#### 4.1 Interface do Usuário:

A interface do usuário foi desenvolvida com a biblioteca Tkinter em Python, permitindo uma interação intuitiva e
amigável com o sistema de tradução.

#### 4.2 Elementos da Interface:

- **Caixa de Texto (Entrada)**: Permite inserir o texto que você deseja traduzir.
- **Menu Suspenso (Seleção de Idioma)**: Permite escolher o idioma de destino para a tradução.
- **Botão "Traduzir"**: inicia o processo de tradução do texto inserido.
- **Caixa de Texto (Saída)**: Exibe o texto traduzido após a conclusão do processo.
- **Mensagens de Erro**: Exibidas em caso de falha na tradução ou erro de conexão com a AWS.

#### 4.3 Processo de Tradução:

- **Detecção Automática de Idioma**: O sistema detecta automaticamente o idioma do texto de origem.
- **Tradução de Texto**: O texto é traduzido para o idioma selecionado no menu suspenso.
- **Simplificação de Jargões Técnicos**: O texto traduzido é simplificado usando a API da OpenAI para torná-lo mais acessível ao público geral.
- **Exibição do Resultado**: O texto traduzido e simplificado é exibido na caixa de texto inferior.