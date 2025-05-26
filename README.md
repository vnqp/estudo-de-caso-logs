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

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute o programa:

   ```bash
   python -m streamlit src/main.py
   ```

> **Importante:** As bibliotecas `nltk` e `tkinter` podem precisar de instalação adicional dependendo do seu sistema operacional.

## Organização do Projeto

```
analisador-chatbot/
│
├── src              # Pasta principal do projeto com o código e data file de reviews.
│
│
│
│
│
├── requirements.txt     # Lista de dependências
├── README.md            # Este arquivo
└── .gitignore           # Arquivos a serem ignorados pelo Git
```
