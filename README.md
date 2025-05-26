# 🔍 SAFE: Sentiment Analysis for Feedback Evaluation

**SAFE** é uma ferramenta interativa para análise de sentimentos em interações de chatbots e avaliações de produtos, com foco na detecção de respostas impróprias ou desalinhadas com o contexto. Utiliza técnicas de Processamento de Linguagem Natural (PLN), análise de confiabilidade e visualização gráfica para auxiliar na interpretação de feedbacks.

## 🧠 Funcionalidades Principais

- **Limpeza e pré-processamento** textual, incluindo remoção de stopwords e normalização.
- **Análise de sentimentos com VADER**, categorizando como positivo, neutro ou negativo.
- **Detecção de incongruência** entre nota e sentimento (ex: nota alta com sentimento negativo).
- **Cálculo de confiabilidade** da análise com base em intensidade e consistência do score.
- **Identificação de temas relevantes** por extração de palavras-chave críticas.
- **Classificação de respostas** como apropriadas ou impróprias, com base no conteúdo e contexto.
- **Visualizações gráficas** da distribuição de sentimentos, temas e confiabilidade.
- **Interface gráfica com Tkinter**, intuitiva e funcional, permitindo operação com poucos cliques.

## 🎯 Público-Alvo

- **Gerentes de Produto** — Avaliam pontos fortes e fracos com base em feedbacks reais.
- **Equipes de Marketing** — Identificam temas positivos para uso estratégico em campanhas.
- **Suporte ao Cliente** — Detectam problemas recorrentes e gargalos na experiência do usuário.
- **Desenvolvedores** — Priorizam correções com base no impacto emocional do feedback.

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Tkinter** — Interface gráfica
- **NLTK + VADER** — Processamento de linguagem e análise de sentimento
- **Google Translator API** — Tradução automática
- **Matplotlib / Seaborn** — Visualizações gráficas

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
   cd .\src\
   python -m streamlit run .\main.py
   ```

> **Importante:** 
> -As bibliotecas `nltk` e `tkinter` podem precisar de instalação adicional dependendo do seu sistema operacional.
> - É necessário dar cd na pasta .\src\ do projeto antes de executar o streamlit para evitar conflitos.

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
