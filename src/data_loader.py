import streamlit as st
import pandas as pd
import requests
import os

@st.cache_data
def fetch_from_api(offset=0, limit=300):
    url = f"https://datasets-server.huggingface.co/rows?dataset=yassiracharki/Amazon_Reviews_for_Sentiment_Analysis_fine_grained_5_classes&config=default&split=train&offset={offset}&limit={limit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        records = []
        for item in data["rows"]:
            row = item["row"]
            records.append({
                "review_title": row["review_title"],
                "review_text": row["review_text"],
                "class_index": row["class_index"]
            })
        return pd.DataFrame(records)
    except Exception as e:
        st.error(f"Erro ao buscar dataset via API: {e}")
        return pd.DataFrame()

@st.cache_data
def load_local_csv(filepath="./data/amazon_reviews.csv"):
    if os.path.exists(filepath):
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            st.error(f"Erro ao carregar CSV local: {e}")
    else:
        st.warning("Arquivo CSV local não encontrado.")
    return pd.DataFrame()

def load_dataset():
    data_source = st.radio("Escolha a fonte dos dados:", ("Selecione...", "API HuggingFace", "CSV local"))

    if data_source == "API HuggingFace":
        offset = st.number_input("Offset", min_value=0, value=0, step=50)
        limit = st.number_input("Limite", min_value=10, max_value=1000, value=300, step=50)
        return fetch_from_api(offset=offset, limit=limit)
    
    elif data_source == "CSV local":
        filepath = st.text_input("Caminho para o CSV local:", "./data/amazon_reviews.csv")
        return load_local_csv(filepath)
    
    return pd.DataFrame()  # Nenhuma opção selecionada ainda
