# Importação das bibliotecas necessárias
import pandas as pd  # Para manipulação de dados em DataFrames
import numpy as np  # Para cálculos numéricos eficientes
import re  # Para manipulação e processamento de strings usando expressões regulares
import nltk  # Biblioteca para processamento de linguagem natural
import seaborn as sns  # Biblioteca para visualização de dados estatísticos
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos
import tkinter as tk  # Módulo para criação de interfaces gráficas
from tkinter import ttk, messagebox  # Widgets e mensagens de alerta do Tkinter
from deep_translator import GoogleTranslator  # Módulo para tradução automática
from nltk.corpus import stopwords  # Lista de stopwords (palavras irrelevantes)
from sklearn.feature_extraction.text import TfidfVectorizer  # Vetorização de texto
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # Analisador de sentimentos baseado em léxicos

# Etapa 1: Captura dos logs do chatbot

# Baixa os recursos necessários do NLTK (stopwords, tokenizador e léxico de sentimentos)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')

# Criando um dicionário com dados simulados dos logs do chatbot
data = {
    "timestamp": [  # Lista de timestamps para cada interação
        "2025-03-18 10:00", "2025-03-18 10:05", "2025-03-18 10:10",
        "2025-03-18 10:15", "2025-03-18 10:20", "2025-03-18 10:25"
    ],
    "user": ["Usuário1", "Usuário2", "Usuário3", "Usuário4", "Usuário5", "Usuário6"],  # Usuários que interagiram
    "chatbot_response": [  # Respostas do chatbot, algumas contendo linguagem imprópria
        "Não posso ajudar gente da sua laia.",
        "Desculpe, mas não tenho essa informação.",
        "Isso é inaceitável! Não vou te ajudar.",
        "Por favor, envie sua mensagem novamente.",
        "Você é burro ou o quê?",
        "Are you dumb?"
    ]
}

# Convertendo o dicionário para um DataFrame do pandas
df = pd.DataFrame(data)

# Etapa 2: Tradução das respostas do chatbot
# Função para traduzir textos para inglês usando GoogleTranslator
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)  # Traduz automaticamente
    except Exception as e:
        return text  # Retorna o texto original se a tradução falhar

# Etapa 3: Limpeza e normalização do texto
# Função para pré-processamento de texto (limpeza e remoção de stopwords)
def preprocess_text(text):
    text = text.lower()  # Converte o texto para letras minúsculas
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove caracteres especiais e números, mantendo apenas letras e espaços
    words = text.split()  # Divide o texto em uma lista de palavras
    words = [word for word in words if word not in stopwords.words('english')]  # Remove palavras irrelevantes (stopwords)
    return ' '.join(words)  # Junta as palavras limpas de volta em uma string


# Etapa 4: Análise de sentimento
# Criação do analisador de sentimento usando Vader
analyzer = SentimentIntensityAnalyzer()

# Função para classificar a resposta do chatbot com base no score de sentimento
def classify_sentiment(score):
    if score < -0.3:
        return "Imprópria"  # Sentimento negativo, possivelmente ofensivo
    elif score > 0.3:
        return "Positiva"  # Sentimento positivo
    else:
        return "Neutra"  # Sentimento neutro ou ambíguo

# Etapa 5: Processamento completo
# Função para traduzir as respostas do chatbot e salvar no DataFrame
def translate_responses():
    df["translated_response"] = df["chatbot_response"].apply(translate_to_english)  # Aplica a função de tradução
    messagebox.showinfo("Sucesso", "Tradução concluída!")  # Exibe uma mensagem de sucesso

# Função para análise de sentimento das respostas do chatbot
def analyze_sentiment():
    if "translated_response" not in df:  # Se as respostas ainda não foram traduzidas, traduz primeiro
        translate_responses()
    
    df["clean_response"] = df["translated_response"].apply(preprocess_text)  # Aplica pré-processamento
    df["sentiment_score"] = df["clean_response"].apply(lambda x: analyzer.polarity_scores(x)["compound"])  # Calcula o score de sentimento
    df["classification"] = df["sentiment_score"].apply(classify_sentiment)  # Classifica as respostas
    messagebox.showinfo("Sucesso", "Análise de sentimento concluída!")  # Exibe mensagem de sucesso

# Etapa 6: Visualização dos logs
# Função para exibir os logs do chatbot em uma nova janela
def show_logs():
    log_window = tk.Toplevel(root)  # Cria uma nova janela dentro da interface
    log_window.title("Logs do Chatbot")  # Define o título da janela
    text = tk.Text(log_window, wrap=tk.WORD)  # Cria um widget de texto
    text.insert(tk.END, df.to_string())  # Insere os logs do DataFrame no widget de texto
    text.pack(expand=True, fill='both')  # Expande o widget na janela

# Etapa 7: Exibição de classificação visual
# Função para exibir gráfico da classificação das respostas
def show_classification_chart():
    if "classification" not in df:  # Verifica se a análise de sentimento já foi realizada
        messagebox.showerror("Erro", "Realize primeiro a análise de sentimento.")  # Exibe erro se ainda não foi feita
        return
    
    plt.figure(figsize=(8, 5))  # Define o tamanho do gráfico
    sns.countplot(x=df["classification"], palette="coolwarm")  # Cria um gráfico de barras para a classificação
    plt.title("Classificação das Respostas do Chatbot")  # Define o título do gráfico
    plt.xlabel("Classification")  # Define o rótulo do eixo X
    plt.ylabel("Frequência")  # Define o rótulo do eixo Y
    plt.show()  # Exibe o gráfico

# Etapa 8: Interface gráfica para interação com o sistema
# Criando a interface gráfica
root = tk.Tk()  # Inicializa a janela principal do Tkinter
root.title("Análise de Logs do Chatbot")  # Define o título da janela
root.geometry("400x300")  # Define o tamanho da janela

# Estilizando os botões da interface
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10, background="darkred")

# Criando um frame para organizar os elementos da interface
frame = ttk.Frame(root, padding=10)
frame.pack(expand=True, fill='both')

# Adicionando um rótulo de instrução
label = ttk.Label(frame, text="Selecione uma opção:", font=("Arial", 20))
label.pack()

# Botões da interface para interagir com as funções
btn_logs = ttk.Button(frame, text="Exibir Logs", command=show_logs, width=20)
btn_logs.pack(pady=5)

btn_translate = ttk.Button(frame, text="Traduzir Respostas", command=translate_responses, width=20)
btn_translate.pack(pady=5)

btn_analyze = ttk.Button(frame, text="Analisar Sentimento", command=analyze_sentiment, width=20)
btn_analyze.pack(pady=5)

btn_chart = ttk.Button(frame, text="Visualizar Classificação", command=show_classification_chart, width=20)
btn_chart.pack(pady=5)

btn_exit = ttk.Button(frame, text="Sair", command=root.quit, width=20)
btn_exit.pack(pady=5)

# Inicia o loop da interface gráfica
root.mainloop()