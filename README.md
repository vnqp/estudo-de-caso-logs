 Analisador de Logs de Chatbot — SAFE: Sentiment Analysis for Feedback Evaluation

Este projeto é uma ferramenta gráfica interativa para análise de sentimentos em interações de chatbot e avaliações de produtos, com ênfase na identificação de respostas impróprias ou desalinhadas ao contexto. A interface foi desenvolvida com Tkinter, e o processamento de linguagem natural é realizado com NLTK, VADER e recursos de tradução automática.
 Funcionalidades Principais

    Limpeza e pré-processamento de texto, com remoção de palavras irrelevantes e normalização.

    Análise de sentimento com VADER, classificando textos como positivos, neutros ou negativos.

    Detecção de incongruência entre nota e sentimento, útil em avaliações com notas destoantes do texto.

    Cálculo da confiabilidade da análise de sentimento, com base na intensidade e consistência do score.

    Identificação de temas relevantes mencionados pelos usuários (palavras-chave críticas).

    Classificação automática de respostas como apropriadas ou impróprias, com base no contexto e sentimento.

    Visualização gráfica da distribuição dos sentimentos, temas e confiabilidade.

    Interface gráfica funcional com Tkinter, permitindo interação completa com o processo em poucos cliques.

 Público-Alvo

    Gerentes de Produto: Avaliação de pontos fortes e fracos com base em feedbacks reais.

    Equipes de Marketing: Identificação de aspectos positivos para divulgação estratégica.

    Suporte ao Cliente: Detecção de recorrência de problemas e gargalos na experiência do usuário.

    Desenvolvedores: Priorização de correções com base em impacto emocional percebido.

 Como Usar

    Carregue seu arquivo de logs ou reviews.

    Acompanhe o pré-processamento e a tradução automática das entradas.

    Visualize a análise de sentimentos, os temas extraídos e possíveis anomalias.

    Utilize os gráficos para extrair insights imediatos sobre a percepção dos usuários.

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
