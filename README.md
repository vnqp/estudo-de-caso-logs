# Analisador de Logs de Chatbot

Este projeto consiste em uma ferramenta gráfica para análise de logs de um chatbot, com foco em detectar respostas impróprias com base na análise de sentimentos. A interface é desenvolvida com Tkinter e o processamento de linguagem natural é realizado com NLTK e VADER.

## Funcionalidades Principais

- **Tradução automática das respostas** para o inglês utilizando o Google Translator.
- **Limpeza e pré-processamento de texto** com remoção de palavras irrelevantes.
- **Análise de sentimento** das respostas utilizando o analisador VADER.
- **Classificação automática das respostas** como Positivas, Neutras ou Impróprias.
- **Visualização gráfica** da distribuição das classificações.
- **Interface gráfica simples e funcional** para interação com todas as etapas do processo.

## Instalação e Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/vnqp/estudo-de-caso-logs.git
   cd estudo-de-caso-logs
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute o programa:

   ```bash
   python code.py
   ```

> **Importante:** As bibliotecas `nltk` e `tkinter` podem precisar de instalação adicional dependendo do seu sistema operacional.

## Organização do Projeto

```
analisador-chatbot/
│
├── code.py              # Código principal com interface gráfica
├── requirements.txt     # Lista de dependências
├── README.md            # Este arquivo
└── .gitignore           # Arquivos a serem ignorados pelo Git
```
