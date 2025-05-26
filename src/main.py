import streamlit as st
import pandas as pd
from data_loader import load_dataset
from sentiment_analyzer import analyze_sentiment
from keyword_detector import detect_themes
from visualization import display_visualizations

# Configurações da página
st.set_page_config(page_title="SAFE - Análise de Sentimento", layout="centered")
st.title("SAFE - Sentiment Analysis for Feedback Evaluation")
st.title("Demonstração de Produto: Reviews da Amazon")

# Sessão
if "df_reviews" not in st.session_state:
    st.session_state.df_reviews = pd.DataFrame()
if "offset" not in st.session_state:
    st.session_state.offset = 0

# Interface de carregamento
if st.session_state.df_reviews.empty:
    df = load_dataset()
    if not df.empty:
        st.session_state.df_reviews = df

df = st.session_state.df_reviews

if not df.empty:
    total_reviews = len(df)
    st.subheader(f"📦 Dataset Carregado - Total de Reviews: {total_reviews}")
    st.write(df.head())

    if st.button("🔍 Executar Análise de Sentimento"):
        # Análise de sentimento otimizada
        df, precision = analyze_sentiment(df)
        df = detect_themes(df)
        display_visualizations(df, precision)

    if st.radio("Você está usando a API para carregar dados?", ("Sim", "Não"), index=1) == "Sim":
        if st.button("➕ Carregar mais reviews da API"):
            from data_loader import fetch_from_api
            new_data = fetch_from_api(offset=st.session_state.offset + 300)
            if not new_data.empty:
                st.session_state.offset += 300
                st.session_state.df_reviews = pd.concat([st.session_state.df_reviews, new_data], ignore_index=True)
                st.success("Mais reviews carregadas com sucesso.")
            else:
                st.warning("Nenhuma review adicional encontrada.")

