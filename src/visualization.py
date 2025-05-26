import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sentiment_analyzer import is_correct_prediction_limited

def clean_data_for_pie_chart(df, sentiment_class, theme_column, exclude_theme=None):
    cleaned_df = df.dropna(subset=[theme_column])
    sentiment_df = cleaned_df[cleaned_df["sentiment_class"] == sentiment_class]
    exploded_themes = sentiment_df[theme_column].explode()
    if exclude_theme:
        exploded_themes = exploded_themes[exploded_themes != exclude_theme]
    theme_counts = exploded_themes.value_counts()
    theme_counts = theme_counts[theme_counts > 0]
    return theme_counts

def display_visualizations(df, precision):  
    display_introduction()

    
    # Mostrar exemplos
    display_review_samples(df)

  

    # Mostrar distribuição de sentimentos
    display_sentiment_distribution(df)
    display_percentages(df)
    
    # Mostrar cruzamento de sentimento vs nota
    display_sentiment_vs_rating(df)

    
    # Mostrar distribuição de confiança
    display_confidence_distribution(df)

    display_confidence_by_rating(df)

    display_sentiment_bubble_chart(df)
    
    # Mostrar temas
    display_theme_distributions(df)
    
   
    # Mostrar reviews negativas
    display_negative_reviews(df)
    
    # Mostrar sugestões


    display_precision_info(precision)

    display_model_performance_analysis(df)

def display_introduction():
    """Mostra a introdução do programa e explica seu propósito."""
    st.title("📊 Análise de Sentimento em Reviews de Produtos")
    
    st.markdown("""
    ## 👋 Bem-vindo ao SAFE - Sentiment Analysis for Feedback Evaluation
    
    Este programa analisa e visualiza os sentimentos expressos em reviews de produtos com auxílio da IA, 
    permitindo que você entenda rapidamente como os clientes se sentem, 
    sem precisar ler milhares de avaliações individuais para que você possa gerar suas próprias conclusões sobre seu negócio.
    
    ### 🎯 O que este programa faz:
    
    1. **Analisa o sentimento** das reviews (positivo, neutro ou negativo)
    2. **Identifica temas importantes** mencionados pelos clientes
    3. **Compara as notas (1-5)** com o sentimento detectado nas reviews
    4. **Avalia a confiabilidade** da análise de sentimento
    5. **Sugere melhorias** com base na análise
    
    ### 📈 Quem pode usar este programa:
    
    - **Gerentes de Produto**: Para entender os pontos fortes e fracos de seus produtos
    - **Equipes de Marketing**: Para destacar os aspectos positivos em campanhas
    - **Suporte ao Cliente**: Para identificar problemas recorrentes
    - **Desenvolvedores**: Para priorizar melhorias de produto
    
    ### 🚀 Como usar:
    
    Basta carregar seus dados de reviews e navegar pelas diferentes visualizações para 
    obter insights imediatos sobre a opinião dos clientes. Cada seção inclui uma 
    explicação simples sobre como interpretar os resultados.
    
   ### 🚀 Exemplos:
    """)
    
    # Exemplos de reviews com diferentes características
    examples = [
        {
            "title": "Adorei este produto!",
            "text": "Comprei este produto há uma semana e estou impressionado com a qualidade. A bateria dura muito mais do que esperava e o design é fantástico. Recomendo fortemente para quem está procurando um produto de alta qualidade.",
            "rating": 5,
            "sentiment": "Positivo",
            "sentiment_score": 0.87,
            "confidence_percent": 95,
            "observacoes": ["✅ Nenhuma anomalia detectada"]
        },
        {
            "title": "Decepcionante",
            "text": "Produto chegou com defeito e o suporte ao cliente foi péssimo. Demorei semanas para conseguir uma resposta e ainda tive que pagar pelo envio da devolução. Não recomendo esta empresa.",
            "rating": 1,
            "sentiment": "Negativo",
            "sentiment_score": -0.92,
            "confidence_percent": 97,
            "observacoes": ["✅ Nenhuma anomalia detectada"]
        },
        {
            "title": "Não gostei, mas tem potencial",
            "text": "O produto tem boas ideias, mas a execução é falha. Interface confusa e muitos bugs. Espero que as próximas atualizações melhorem, pois o conceito é interessante.",
            "rating": 2,
            "sentiment": "Positivo",
            "sentiment_score": 0.25,
            "confidence_percent": 38,
            "observacoes": ["⚠️ Confiança baixa na classificação - Verifique se o texto condiz com a nota", 
                        "❗ Sentimento inesperado para essa nota"],
            "explanation": """
            <b>Por que este exemplo é importante?</b>
            
            Esta review ilustra um caso de <b>possível conflito entre nota e sentimento</b>. Com nota 2 (baixa), 
            seria esperado um sentimento negativo, mas o sistema detectou um sentimento positivo, embora com baixa confiança (38%).
            
            <b>O que está acontecendo aqui?</b>
            
            1. A review contém uma <b>mistura de elementos negativos</b> ("execução falha", "interface confusa", "muitos bugs") 
            que justificam a nota baixa.
            
            2. Mas também inclui <b>expressões positivas</b> ("boas ideias", "conceito interessante", "espero melhorias") 
            que podem ter levado o algoritmo a identificar um tom geral mais positivo.
            
            3. A <b>baixa confiança</b> (38%) indica que o próprio sistema reconhece a ambiguidade nesta análise.
            
            <b>Como interpretar casos semelhantes:</b>
            
            Quando você vir alertas como estes, vale a pena examinar manualmente as reviews para entender sutilezas 
            que o algoritmo pode ter perdido. Estes casos muitas vezes revelam <b>oportunidades de melhoria específicas</b> 
            ou mostram clientes que estão insatisfeitos mas veem potencial no produto.
            """
        }
    ]
    
    st.subheader("📚 Exemplos de Reviews e Como São Analisadas")
    
    for example in examples:
        st.markdown(f"**Nota {example['rating']} com Sentimento {example['sentiment']}**")
        st.markdown(f"📌 *{example['title']}*")
        st.markdown(f"📝 {example['text']}")
        st.markdown(f"🎯 Score de Sentimento: `{example['sentiment_score']}` ({example['confidence_percent']}% certeza)")
        for obs in example["observacoes"]:
            st.markdown(f"- {obs}")
        
        # Adiciona a explicação quando disponível
        if "explanation" in example:
            with st.expander("🧠 Entenda esta análise"):
                st.markdown(example["explanation"], unsafe_allow_html=True)


def display_precision_info(precision):
    st.markdown("---")
    
    # Determinar a classificação da precisão e selecionar o emoji apropriado
    if precision >= 0.8:
        precision_level = "Excelente"
        emoji = "🎯"
        color = "green"
    elif precision >= 0.7:
        precision_level = "Boa"
        emoji = "👍"
        color = "darkgreen"
    elif precision >= 0.6:
        precision_level = "Aceitável"
        emoji = "⚠️"
        color = "orange"
    else:
        precision_level = "Precisa melhorar"
        emoji = "❗"
        color = "red"
    
    # Mostrar a precisão com formatação destacada
    st.markdown(f"""
    <h2 style='text-align: center;'>{emoji} Precisão Crua do Modelo</h2>
    <h1 style='text-align: center; color: {color};'>{precision*100:.1f}%</h1>
    <p style='text-align: center;'>Classificação: <strong>{precision_level}</strong></p>
    """, unsafe_allow_html=True)
    
    # Criar uma barra de progresso visual para a precisão
    st.progress(precision)
    
    # Explicação em um expander
    with st.expander("📌 O que significa esta precisão?"):
        st.markdown("""
        ### O que é a precisão crua do modelo?
        
        É uma medida de **quanto nosso modelo acerta** ao analisar o sentimento das reviews.
        
        ### Como calculamos a precisão:
        
        Comparamos as notas que os clientes deram (1-5 estrelas) com o sentimento que o modelo detectou:
        
        - **Nota 5** ⭐⭐⭐⭐⭐ → Deveria ser sentimento **Positivo**
        - **Nota 4** ⭐⭐⭐⭐ → Deveria ser **Positivo** ou **Neutro**
        - **Nota 3** ⭐⭐⭐ → Pode ser qualquer sentimento
        - **Nota 2** ⭐⭐ → Deveria ser **Negativo** ou **Neutro**
        - **Nota 1** ⭐ → Deveria ser sentimento **Negativo**
        
        ### Como interpretar este número:
        
        | Precisão | O que significa | Recomendação |
        |----------|-----------------|--------------|
        | 80-100% | Excelente | Pode confiar nos resultados para decisões importantes |
        | 70-80% | Boa | Confiável para a maioria das análises |
        | 60-70% | Aceitável | Use para tendências gerais, mas confira manualmente casos críticos |
        | Abaixo de 60% | Precisa melhorar | Use com cautela, verifique manualmente as conclusões |
        
        ### Por que a precisão pode não ser perfeita?
        
        - Algumas reviews contêm **sarcasmo ou ironia** que é difícil para o modelo detectar
        - Clientes podem dar **notas que não correspondem** ao texto da review
        - Reviews com **opiniões mistas** (parte positivas, parte negativas) são difíceis de classificar
        """)
    
    # Mostrar uma dica visual com base na precisão
    if precision < 0.7:
        st.warning("""
        ⚠️ **Dica**: Como a precisão está abaixo de 70%, recomendamos usar estes resultados como indicativos, 
        mas verificar manualmente as principais conclusões antes de tomar decisões importantes.
        """)
    
    st.markdown("---")

def display_sentiment_distribution(df):
    st.subheader("🌟 Distribuição por Nota (class_index)")
    class_counts = df["class_index"].value_counts().sort_index()
    st.bar_chart(class_counts)

    st.markdown("---")
    st.subheader("📊 Distribuição de Sentimentos")
    st.bar_chart(df["sentiment_class"].value_counts())

    class_counts = df["class_index"].value_counts().sort_index()
    st.subheader("🥧 Distribuição Percentual das Notas")
    class_percent = class_counts / class_counts.sum() * 100
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(class_percent, labels=class_percent.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax_pie.set_title("Distribuição das Notas (em %)")
    ax_pie.axis('equal')
    st.pyplot(fig_pie)

    # Exibir explicação sobre as distribuições usando expander
    with st.expander("📌 Entenda estes gráficos"):
        st.markdown("""
        ### O que estes gráficos mostram?
        
        **Gráfico 1 - Distribuição de Sentimentos:**
        - Mostra quantas reviews são positivas, neutras ou negativas
        - Ajuda a entender o humor geral dos clientes sobre seu produto
        
        **Gráfico 2 - Distribuição por Nota:**
        - Exibe quantas reviews deram cada nota (de 1 a 5 estrelas)
        - Quanto mais reviews com notas altas (4-5), melhor a recepção do produto
        
        **Gráfico 3 - Distribuição Percentual:**
        - Apresenta as mesmas informações do gráfico anterior, mas em porcentagem
        - Facilita ver rapidamente qual proporção das reviews é positiva ou negativa
        
        ### Como usar esta informação:
        
        - Muitas notas baixas (1-2): Seu produto pode precisar de melhorias urgentes
        - Maioria de notas médias (3): Os clientes estão satisfeitos, mas não impressionados
        - Predominância de notas altas (4-5): Seu produto está agradando - destaque estes pontos!
        
        Se o sentimento não corresponder às notas (ex: muitas notas 5 mas sentimento neutro), 
        vale investigar o texto das reviews para entender melhor.
        """)
    st.markdown("---")

def display_sentiment_vs_rating(df):
    st.subheader("🔄 Cruzamento: Sentimento vs Nota")
    cross_tab = pd.crosstab(df["class_index"], df["sentiment_class"])
    st.dataframe(cross_tab)

    st.subheader("📈 Heatmap: Sentimento vs Nota")
    fig, ax = plt.subplots()
    sns.heatmap(cross_tab, annot=True, fmt="d", cmap="YlOrBr", ax=ax)
    ax.set_title("Distribuição entre Notas e Sentimentos")
    st.pyplot(fig)

    # Explicação dentro de um expander com texto simplificado
    with st.expander("📌 Como interpretar estes dados"):
        st.markdown("""
        ### O que estes gráficos mostram?
        
        Estes gráficos mostram **como as notas e os sentimentos se relacionam** nas reviews.
        
        **Tabela de Cruzamento:** 
        - Cada linha representa uma nota (1 a 5 estrelas)
        - Cada coluna mostra um sentimento (Positivo, Neutro, Negativo)
        - Os números mostram quantas reviews existem em cada combinação
        
        **Heatmap (mapa de calor):**
        - Mesma informação da tabela, mas em formato visual
        - Cores mais escuras = mais reviews naquela combinação
        - Números em cada quadrado = quantidade exata de reviews
        
        ### O que seria o esperado?
        
        **Normalmente esperamos ver:**
        - Notas 4-5 ⭐ com sentimento Positivo
        - Notas 3 ⭐ com sentimento Neutro
        - Notas 1-2 ⭐ com sentimento Negativo
        
        ### O que investigar:
        
        **Procure por padrões inesperados:**
        - Notas altas (4-5) com sentimentos negativos → cliente pode ter dado nota errada ou o texto contradiz a nota
        - Notas baixas (1-2) com sentimentos positivos → possível ironia ou sarcasmo não detectado
        - Muitas reviews neutras → podem indicar clientes indecisos ou reviews pouco informativas
        
        Use estas informações para identificar reviews que merecem atenção especial, como clientes que parecem insatisfeitos mesmo dando notas altas.
        """)
    st.markdown("---")


def display_confidence_distribution(df):
    st.subheader("📏 Distribuição de Reviews por Faixa de Confiança na Analise Sentimental")

    # Definir faixas de confiança
    bins = [0, 20, 40, 60, 80, 100]
    labels = ["0-20%", "21-40%", "41-60%", "61-80%", "81-100%"]
    df["confidence_range"] = pd.cut(df["confidence_percent"], bins=bins, labels=labels, include_lowest=True)
    
    # Contagem por faixa
    confidence_counts = df["confidence_range"].value_counts().sort_index()

    # Plot
    fig_conf, ax_conf = plt.subplots()
    sns.barplot(x=confidence_counts.index, y=confidence_counts.values, palette="Blues_d", ax=ax_conf)
    ax_conf.set_title("Quantidade de Reviews por Faixa de Confiança (%)")
    ax_conf.set_xlabel("Faixa de Confiança")
    ax_conf.set_ylabel("Número de Reviews")
    st.pyplot(fig_conf)

    # Histograma da confiança
    st.subheader("📊 Histograma da Confiança da Análise de Sentimento")
    fig_hist, ax_hist = plt.subplots()
    sns.histplot(df["confidence_percent"], bins=20, kde=True, color="skyblue", ax=ax_hist)
    ax_hist.set_title("Distribuição de Confiança (Score de Sentimento)")
    ax_hist.set_xlabel("Confiança (%)")
    ax_hist.set_ylabel("Número de Reviews")
    st.pyplot(fig_hist)

    # Boxplot de confiança por classe
    st.subheader("📦 Boxplot: Confiança por Classe de Sentimento")
    fig_box, ax_box = plt.subplots()
    sns.boxplot(x="sentiment_class", y="confidence_percent", data=df, palette="Set2", ax=ax_box)
    ax_box.set_title("Variação da Confiança por Sentimento")
    ax_box.set_xlabel("Classe de Sentimento")
    ax_box.set_ylabel("Confiança (%)")
    st.pyplot(fig_box)
   

def display_confidence_by_rating(df):
    st.subheader("🎯 Confiabilidade da Análise por Nota")
    
    # Criando o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Boxplot da confiança por nota
    sns.boxplot(x='class_index', y='confidence_percent', data=df, ax=ax)
    
    # Adicionando pontos individuais
    sns.stripplot(x='class_index', y='confidence_percent', data=df, 
                 size=4, color='.3', alpha=0.3, ax=ax)
    
    ax.set_title("Confiabilidade da Análise por Nota")
    ax.set_xlabel("Nota (1-5)")
    ax.set_ylabel("Confiança na Análise (%)")
    
    # Adicionar linha média
    overall_mean = df['confidence_percent'].mean()
    ax.axhline(y=overall_mean, color='r', linestyle='--', label=f'Média Geral: {overall_mean:.1f}%')
    ax.legend()
    
    st.pyplot(fig)
    
    # Estatísticas resumidas
    st.markdown("### 📊 Estatísticas de Confiabilidade por Nota")
    confidence_stats = df.groupby('class_index')['confidence_percent'].agg(['mean', 'median', 'std', 'min', 'max'])
    confidence_stats.columns = ['Média', 'Mediana', 'Desvio Padrão', 'Mínimo', 'Máximo']
    confidence_stats = confidence_stats.round(2)
    st.dataframe(confidence_stats)

    # Explicação em um expander
    with st.expander("📌 Entenda a confiabilidade da análise"):
        st.markdown("""
        ### O que é a confiabilidade?
        
        É o quanto a IA está **segura** sobre a classificação do sentimento de uma review.
        
        - **Confiança alta (próxima de 100%)** = A IA está bem certa do sentimento
        - **Confiança baixa (próxima de 0%)** = A IA está em dúvida sobre o sentimento
        
        ### Como ler este gráfico?
        
        **Boxplot (caixas coloridas):**
        - A linha no meio da caixa = valor típico (mediana) de confiança
        - Caixa inteira = onde está a maioria das reviews
        - Pontos cinza = reviews individuais
        - Linha vermelha tracejada = média geral de confiança
        
        ### O que procurar neste gráfico?
        
        **Padrões importantes:**
        
        1. **Caixas altas (acima de 70%)** = Bom! As reviews têm sentimento claro
        
        2. **Caixas baixas (abaixo de 50%)** = Reviews com linguagem ambígua ou confusa
        
        3. **Muitos pontos espalhados** = Reviews muito variadas em clareza
        
        4. **Diferenças entre notas:**
           - Confiança maior nas notas 1 e 5? Normal! Opiniões extremas são mais claras
           - Confiança menor na nota 3? Normal! Opiniões neutras costumam ser mais ambíguas
        
        ### Dica prática:
        
        Se a confiança for baixa em muitas reviews de uma nota específica, vale a pena ler essas reviews 
        manualmente. Pode haver nuances que a IA não conseguiu captar completamente.
        """)
    st.markdown("---")

def display_sentiment_bubble_chart(df):
    st.subheader("🔮 Mapa de Sentimento (Confiança × Nota × Volume)")
    
    # Agrupar dados
    grouped = df.groupby(['class_index', 'sentiment_class']).agg(
        count=('sentiment_class', 'count'),
        avg_confidence=('confidence_percent', 'mean')
    ).reset_index()
    
    # Criar gráfico de bolhas
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Definir cores por sentimento
    colors = {'Positivo': 'green', 'Neutro': 'blue', 'Negativo': 'red'}
    
    # Plotar bolhas
    for sentiment in grouped['sentiment_class'].unique():
        subset = grouped[grouped['sentiment_class'] == sentiment]
        scatter = ax.scatter(
            subset['class_index'], 
            subset['avg_confidence'],
            s=subset['count']*20,  # Tamanho proporcional à contagem
            alpha=0.6,
            color=colors[sentiment],
            label=sentiment
        )
    
    # Adicionar textos
    for _, row in grouped.iterrows():
        ax.annotate(
            f"{row['count']}",
            (row['class_index'], row['avg_confidence']),
            ha='center', va='center',
            fontsize=9
        )
    
    ax.set_title("Mapa de Sentimento: Nota vs Confiança vs Volume")
    ax.set_xlabel("Nota")
    ax.set_ylabel("Confiança Média (%)")
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.legend(title="Sentimento")
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    
    # Explicação em um expander com linguagem simplificada
    with st.expander("📌 Como entender este gráfico de bolhas"):
        st.markdown("""
        ### O que este gráfico mostra?
        
        Este é um gráfico "3 em 1" que mostra três informações importantes de uma só vez:
        
        1. **Posição horizontal (Nota)**: A nota que o cliente deu, de 1 a 5 estrelas
        
        2. **Posição vertical (Confiança)**: O quanto a IA está segura sobre o sentimento detectado
        
        3. **Tamanho da bolha (Volume)**: Quantas reviews existem com essa combinação
        
        **As cores representam o sentimento:**
        - 🟢 **Verde** = Sentimento Positivo
        - 🔵 **Azul** = Sentimento Neutro
        - 🔴 **Vermelho** = Sentimento Negativo
        
        ### O que indica um bom resultado?
        
        Um padrão "saudável" normalmente mostra:
        
        - 🔴 **Bolhas vermelhas** (negativas) maiores nas **notas baixas** (1-2)
        - 🔵 **Bolhas azuis** (neutras) maiores na **nota média** (3)
        - 🟢 **Bolhas verdes** (positivas) maiores nas **notas altas** (4-5)
        - Bolhas posicionadas **mais alto** no gráfico (indicando maior confiança)
        
        ### O que procurar de estranho?
        
        Fique atento a estas situações incomuns:
        
        - 🟢 **Bolhas verdes** nas **notas 1-2**: Clientes podem estar sendo sarcásticos ou o modelo pode estar confuso
        
        - 🔴 **Bolhas vermelhas** nas **notas 4-5**: Pode indicar clientes que deram nota boa mas fizeram críticas no texto
        
        - **Bolhas muito baixas** no gráfico: Reviews com linguagem ambígua ou confusa
        
        - **Muitas bolhas azuis** (neutras): Pode indicar reviews com pouco conteúdo emocional ou opiniões mistas
        
        ### Dica de uso:
        
        Quando encontrar combinações inesperadas (como sentimento positivo em nota baixa), vale a pena examinar 
        manualmente algumas dessas reviews para entender melhor o que está acontecendo.
        """)
    st.markdown("---")

def display_theme_distributions(df):
    st.subheader("🍕 Gráfico de Pizza - Temas em Reviews Negativas")
    negative_theme_counts = clean_data_for_pie_chart(df, "Negativo", "themes")
    if not negative_theme_counts.empty:
        # Gráfico
        fig, ax = plt.subplots()
        ax.pie(
            negative_theme_counts,
            labels=negative_theme_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=sns.color_palette("RdBu", len(negative_theme_counts))
        )
        ax.set_title("Distribuição dos Temas em Reviews Negativas")
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.info("Nenhum tema negativo encontrado.")

    st.subheader("🍰 Gráfico de Pizza - Temas em Reviews Positivas")
    positive_theme_counts = clean_data_for_pie_chart(df, "Positivo", "positive_themes")
    if not positive_theme_counts.empty:
        # Gráfico
        fig2, ax2 = plt.subplots()
        ax2.pie(
            positive_theme_counts,
            labels=positive_theme_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=sns.color_palette("YlGn", len(positive_theme_counts))
        )
        ax2.set_title("Distribuição dos Temas em Reviews Positivas")
        ax2.axis('equal')
        st.pyplot(fig2)
    else:
        st.info("Nenhum tema positivo encontrado.")

    # Explicação em um expander

    with st.expander("📌 Entenda os gráficos de temas"):

        st.markdown("""

        ### O que são estes gráficos de temas?

        

        Estes gráficos mostram os **assuntos mais comentados** pelos clientes, separados entre:

        

        - **Reviews negativas**: O que os clientes não gostaram

        - **Reviews positivas**: O que os clientes elogiaram

        

        ### Como isso ajuda seu negócio:

        

        - **Gráficos de pizza**: Mostram a proporção de cada tema (quanto maior a fatia, mais comentado)

        - **Tabelas**: Apresentam os números exatos de ocorrências de cada tema

        

        ### Como usar esta informação:

        

        ✅ **Nos temas negativos**: Concentre esforços para resolver os problemas mais mencionados

        

        ✅ **Nos temas positivos**: Destaque estes pontos fortes em seu marketing

        

        Por exemplo, se "entrega" for um tema negativo comum, melhore sua logística. 

        Se "qualidade" aparecer muito nos positivos, enfatize isso nas campanhas.

        """)

    

    col1, col2 = st.columns(2)

    

    with col1:

        st.subheader("🔴 Temas em Reviews Negativas")
        # Tabela

        st.markdown("##### Detalhamento dos temas negativos:")

        st.dataframe(

            negative_theme_counts.reset_index().rename(

                columns={"index": "Problema", 0: "Ocorrências"}

            )

        )

            

            # Adicionar significado para os temas negativos

        with st.expander("🔍 O que significam estes temas negativos?"):

            st.markdown("""

            - **Qualidade**: Produtos quebrados, mal feitos ou defeituosos

            - **Entrega**: Atrasos, produtos danificados durante transporte, entregas erradas

            - **Atendimento**: Problemas com suporte, dificuldade em resolver questões

            - **Preço**: Reclamações sobre custo-benefício ou preço alto demais

            - **Expectativa**: Produto diferente do anunciado ou esperado

            - **Usabilidade**: Dificuldade para usar, problemas de instalação

            - **Funcionamento**: Produtos que não funcionam como deveriam

            - **Durabilidade**: Produtos que quebraram ou estragaram rapidamente

            """)




    with col2:

        st.subheader("🟢 Temas em Reviews Positivas")

        st.markdown("##### Detalhamento dos temas positivos:")

        st.dataframe(

            positive_theme_counts.reset_index().rename(

                columns={"index": "Ponto forte", 0: "Ocorrências"}

            )

        )

            

        # Adicionar significado para os temas positivos

        with st.expander("🔍 O que significam estes temas positivos?"):

            st.markdown("""

            - **Qualidade**: Produtos bem feitos, bons materiais, boa construção

            - **Entrega**: Rapidez, cuidado no transporte, entrega antes do prazo

            - **Atendimento**: Suporte atencioso, respostas rápidas, resolução eficaz

            - **Preço**: Bom custo-benefício, promoções vantajosas

            - **Expectativa**: Produto superou o esperado, cliente positivamente surpreso

            - **Facilidade**: Produto fácil de usar, intuitivo, boa experiência

            - **Funcionamento**: Produto funciona perfeitamente como anunciado

            - **Durabilidade**: Produto resistente, mantém qualidade ao longo do tempo

            - **Desempenho**: Eficiência, bons resultados, alta performance

            """)

    

    # Dicas de ação baseadas nos temas

    st.subheader("💡 Insights e Recomendações")

    with st.expander("Ver sugestões de ação baseadas nos temas"):

        st.markdown("""

        ### Como agir com base nestes temas:

        

        #### Temas Negativos Frequentes:

        

        1. **Se "Qualidade" for um problema comum:**

           - Revisar processos de fabricação/fornecimento

           - Implementar testes de qualidade mais rigorosos

           - Considerar mudança de fornecedores

        

        2. **Se "Entrega" for muito mencionado:**

           - Avaliar parceiros logísticos

           - Melhorar embalagens para evitar danos

           - Revisar processos de envio e rastreamento

        

        3. **Se "Preço" aparecer frequentemente:**

           - Reavaliar estratégia de preços

           - Destacar melhor o valor agregado do produto

           - Considerar opções com melhor custo-benefício

        

        #### Temas Positivos a Destacar:

        

        1. **Se "Qualidade" for elogiada:**

           - Destacar isso em campanhas de marketing

           - Manter os padrões atuais de produção

           - Considerar linha premium ressaltando este aspecto

        

        2. **Se "Atendimento" for bem avaliado:**

           - Reconhecer e premiar a equipe de suporte

           - Compartilhar as boas práticas internamente

           - Destacar o suporte como diferencial competitivo

        

        3. **Se "Facilidade" for mencionada positivamente:**

           - Enfatizar a usabilidade em materiais promocionais

           - Manter a simplicidade em atualizações futuras do produto

           - Considerar tutoriais para outras funcionalidades menos utilizadas

        """)

    

    st.markdown("---")

def display_review_samples(df):
    st.subheader("📚 Samples por Combinação (Nota × Sentimento)")
    
    # Adiciona explicação em um expander
    with st.expander("📌 Entenda esta seção"):
        st.markdown("""
        ### O que são estas amostras?
        
        Aqui você encontra **exemplos reais de reviews** para cada combinação de nota e sentimento.
        
        - Cada expander mostra uma review diferente
        - As reviews são escolhidas aleatoriamente do seu conjunto de dados
        - Os alertas (⚠️❗) indicam possíveis inconsistências na análise
        
        ### Como usar estas amostras:
        
        - Revise exemplos com alertas para entender melhor as opiniões dos clientes
        - Use para verificar se a análise de sentimento está funcionando corretamente
        - Identifique padrões de linguagem nos comentários positivos e negativos
        """)

    sample_dict = {}

    # Heurística 1: Faixa flexível para correspondência nota × sentimento
    def is_sentiment_reasonable(rating, sentiment):
        if rating == 5:
            return sentiment in ["Positivo", "Neutro"]
        elif rating == 4:
            return sentiment in ["Positivo", "Neutro"]
        elif rating == 3:
            return True  # zona cinzenta
        elif rating == 2:
            return sentiment in ["Negativo", "Neutro"]
        elif rating == 1:
            return sentiment in ["Negativo", "Neutro"]
        return False

    # Heurística 2: Confiança baixa
    def is_low_confidence(confidence_percent):
        return confidence_percent < 30

    # Heurística 3: Discrepância entre nota e score de sentimento
    def has_discrepancy(rating, sentiment_score):
        if rating == 5 and sentiment_score < 0:
            return True
        elif rating == 1 and sentiment_score > 0:
            return True
        return False

    for rating in sorted(df["class_index"].unique()):
        for sentiment in ["Positivo", "Neutro", "Negativo"]:
            subset = df[(df["class_index"] == rating) & (df["sentiment_class"] == sentiment)]
            if not subset.empty:
                example = subset.sample(1).iloc[0]

                sentiment_score = example["sentiment_score"]
                confidence = example["confidence_percent"]

                observacoes = []

                if is_low_confidence(confidence):
                    observacoes.append("⚠️ Confiança baixa na classificação - Verifique se o texto condiz com a nota")
                if not is_sentiment_reasonable(rating, sentiment):
                    observacoes.append("❗ Sentimento inesperado para essa nota")
                if has_discrepancy(rating, sentiment_score):
                    observacoes.append("❗ Score de sentimento diverge da nota")

                if not observacoes:
                    observacoes.append("✅ Nenhuma anomalia detectada")

                sample_dict[(rating, sentiment)] = {
                    "title": example["review_title"],
                    "text": example["review_text"][:300] + ("..." if len(example["review_text"]) > 300 else ""),
                    "sentiment_score": sentiment_score,
                    "confidence_percent": confidence,
                    "observacoes": observacoes
                }

    # Cria containers para organizar os expanders em colunas
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    col_idx = 0

    # Ordenar as chaves para uma apresentação mais organizada
    sorted_keys = sorted(sample_dict.keys())

    for key in sorted_keys:
        value = sample_dict[key]

        # Determina os ícones baseados nas observações
        icons = set()
        for obs in value["observacoes"]:
            if "✅" in obs:
                icons.add("✅")
            if "⚠️" in obs:
                icons.add("⚠️")
            if "❗" in obs:
                icons.add("❗")
        icon = "".join(sorted(icons, key=lambda x: ["❗", "⚠️", "✅"].index(x)))

        # Escolhe a coluna atual
        col = columns[col_idx]

        # Cria o expander para esta amostra
        with col.expander(f"{icon} Nota {key[0]} - {key[1]}"):
            st.markdown(f"**{value['title']}**")
            st.markdown(f"{value['text']}")
            st.markdown(f"🎯 Score: `{value['sentiment_score']}` ({value['confidence_percent']}% certeza)")

            for obs in value["observacoes"]:
                if "✅" in obs:
                    st.success(obs)
                elif "⚠️" in obs:
                    st.warning(obs)
                elif "❗" in obs:
                    st.error(obs)

        col_idx = (col_idx + 1) % len(columns)

    st.markdown("---")



def display_negative_reviews(df):
    st.subheader("🚨 Reviews Negativas Detectadas")
    negative_df = df[df["sentiment_class"] == "Negativo"]
    if negative_df.empty:
        st.info("Nenhuma review negativa encontrada.")
    else:
        st.write(f"Total: {len(negative_df)} de {len(df)} reviews ({(len(negative_df)/len(df))*100:.2f}%)")
        st.dataframe(negative_df[["review_title", "review_text", "class_index"]], use_container_width=True)

    st.markdown("---")

    # Calculando a porcentagem de reviews positivas e negativas
    positive_percentage = (df["sentiment_class"] == "Positivo").mean() * 100
    negative_percentage = (df["sentiment_class"] == "Negativo").mean() * 100

def display_percentages(df):
    # Calcular porcentagens
    sentiment_counts = df['sentiment_class'].value_counts()
    total_reviews = len(df)
    
    # Garantir que existem as categorias (se não existirem, definir como 0)
    positive_count = sentiment_counts.get('Positivo', 0)
    negative_count = sentiment_counts.get('Negativo', 0)
    neutral_count = sentiment_counts.get('Neutro', 0)
    
    # Calcular porcentagens
    positive_percentage = (positive_count / total_reviews) * 100
    negative_percentage = (negative_count / total_reviews) * 100
    neutral_percentage = (neutral_count / total_reviews) * 100
    
    # Criar medidor visual com cores
    st.subheader("📊 Visão Geral do Sentimento")
    
    # Usar colunas para organizar o layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"### 😃 Positivas")
        st.markdown(f"<h1 style='text-align: center; color: green;'>{positive_percentage:.1f}%</h1>", unsafe_allow_html=True)
        st.markdown(f"({positive_count} reviews)")
    
    with col2:
        st.markdown(f"### 😐 Neutras")
        st.markdown(f"<h1 style='text-align: center; color: gray;'>{neutral_percentage:.1f}%</h1>", unsafe_allow_html=True)
        st.markdown(f"({neutral_count} reviews)")
    
    with col3:
        st.markdown(f"### 😟 Negativas")
        st.markdown(f"<h1 style='text-align: center; color: red;'>{negative_percentage:.1f}%</h1>", unsafe_allow_html=True)
        st.markdown(f"({negative_count} reviews)")
    
    # Criar um medidor visual simples
    progress_data = [
        {"label": "Positivas", "value": positive_percentage, "color": "green"},
        {"label": "Neutras", "value": neutral_percentage, "color": "gray"},
        {"label": "Negativas", "value": negative_percentage, "color": "red"}
    ]
    
    # Criar uma barra horizontal para visualizar a distribuição
    st.markdown("#### Distribuição de Sentimentos:")
    
    # Montar o HTML para a barra de progresso
    progress_html = '<div style="display: flex; width: 100%; height: 30px; border-radius: 5px; overflow: hidden;">'
    for item in progress_data:
        if item["value"] > 0:  # Só mostrar se tiver valor
            progress_html += f'<div style="width: {item["value"]}%; background-color: {item["color"]};" title="{item["label"]}: {item["value"]:.1f}%"></div>'
    progress_html += '</div>'
    
    st.markdown(progress_html, unsafe_allow_html=True)
    
    # Adicionar explicação em um expander
    with st.expander("📌 Como interpretar estes números"):
        st.markdown("""
        ### O que significam estas porcentagens?
        
        Estes números mostram como os clientes se sentem em relação ao seu produto ou serviço:
        
        - **Porcentagem Positiva**: Clientes satisfeitos que expressaram opiniões favoráveis
        - **Porcentagem Neutra**: Clientes com opiniões mistas ou que não expressaram emoções fortes
        - **Porcentagem Negativa**: Clientes insatisfeitos que expressaram críticas ou problemas
        
        ### Como avaliar estes resultados?
        
        **Cenário ideal:**
        - 70%+ positivas
        - Menos de 15% negativas
        
        **Situação aceitável:**
        - 50-70% positivas
        - 15-30% negativas
        
        **Requer atenção:**
        - Menos de 50% positivas
        - Mais de 30% negativas
        
        ### Dica de uso:
        
        Se a porcentagem de reviews negativas for alta, explore os temas negativos mais frequentes 
        para identificar os principais problemas a serem resolvidos prioritariamente.
        """)
    
    st.markdown("---")

def display_model_performance_analysis(df):
    st.subheader("🔍 Análise de Precisão Avançada do Modelo")
    
    # Explicação simplificada em um expander
    with st.expander("📌 Entenda esta seção"):
        st.markdown("""
        ### O que esta análise avançada mostra?
        
        Esta seção avalia o quanto o modelo de IA está **acertando na detecção de sentimentos**, comparando com uma previsão do que seria esperado com base nas notas dos clientes.
        
        **Como interpretamos as notas para esta comparação:**
        - Notas 5 ⭐⭐⭐⭐⭐ = Esperamos sentimento Positivo
        - Notas 1 ⭐ = Esperamos sentimento Negativo
        - Notas 2-4 ⭐⭐-⭐⭐⭐⭐ = Podem variar (consideramos principalmente 1 e 5 para esta análise)
        
        ### Como ler a Matriz de Confusão:
        
        A matriz mostra como o modelo **classificou** vs. como **deveria ter classificado**:
        
        - **Diagonal principal** (canto superior esquerdo ao inferior direito): Representa os **acertos** do modelo
        - **Fora da diagonal**: Representa os **erros** de classificação
        - Número em cada célula = quantidade de reviews naquela combinação
        
        ### O que significam as métricas abaixo:
        
        **Precision (Precisão)**: Quando o modelo diz que é positivo/negativo, qual % está correto?
        
        **Recall (Revocação)**: Do total de sentimentos realmente positivos/negativos, qual % o modelo conseguiu identificar?
        
        **F1 Score**: Uma média balanceada entre Precision e Recall (quanto maior, melhor)
        
        **Valores bons**: Acima de 70% indicam um modelo confiável para análises de negócio
        """)
    
    from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    
    # Criar categorização baseada na nota (class_index)
    df['expected_sentiment'] = df['class_index'].apply(lambda x: 
                                                      'Positivo' if x == 5 else 
                                                      'Negativo' if x == 1 else 
                                                      'Neutro')  # Tratando 2 e 4 como Neutro
    
    # Filtrar somente os casos com notas válidas
    clear_df = df[df['class_index'].isin([1, 2, 4, 5])]

    # Matriz de Confusão com cores mais intuitivas
    cm = confusion_matrix(
        clear_df['expected_sentiment'], 
        clear_df['sentiment_class'],
        labels=['Positivo', 'Neutro', 'Negativo']
    )
    
    # Criar visualização mais clara da matriz
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Calcular porcentagens por linha
    row_sums = cm.sum(axis=1)
    cm_percent = np.zeros_like(cm, dtype=float)
    for i in range(len(row_sums)):
        if row_sums[i] > 0:
            cm_percent[i] = cm[i] / row_sums[i] * 100
    
    # Plotar heatmap com valores absolutos
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Positivo', 'Neutro', 'Negativo'],
                yticklabels=['Positivo', 'Neutro', 'Negativo'],
                linewidths=1, linecolor='white', ax=ax)
    
    # Adicionar porcentagens
    for i in range(len(cm)):
        for j in range(len(cm)):
            if cm[i, j] > 0:
                ax.text(j + 0.5, i + 0.7, f"({cm_percent[i, j]:.1f}%)", 
                        ha="center", va="center", color="black", fontsize=9)
    
    ax.set_title('Matriz de Confusão: Esperado vs. Detectado', fontsize=14)
    ax.set_xlabel('Sentimento Detectado pelo Modelo', fontsize=12)
    ax.set_ylabel('Sentimento Esperado pela Nota', fontsize=12)
    st.pyplot(fig)
    
    # Preparar dados binários para análise separada
    binary_df = clear_df[clear_df['expected_sentiment'].isin(['Positivo', 'Negativo'])].copy()

    # Métricas com Positivo como classe positiva
    y_true_pos = binary_df['expected_sentiment'].map({'Positivo': 1, 'Negativo': 0})
    y_pred_pos = binary_df['sentiment_class'].map({'Positivo': 1, 'Negativo': 0, 'Neutro': 0}).astype(int)

    precision_pos = precision_score(y_true_pos, y_pred_pos)
    recall_pos = recall_score(y_true_pos, y_pred_pos)
    f1_pos = f1_score(y_true_pos, y_pred_pos)

    # Métricas com Negativo como classe positiva
    y_true_neg = binary_df['expected_sentiment'].map({'Negativo': 1, 'Positivo': 0})
    y_pred_neg = binary_df['sentiment_class'].map({'Negativo': 1, 'Positivo': 0, 'Neutro': 0}).astype(int)

    precision_neg = precision_score(y_true_neg, y_pred_neg)
    recall_neg = recall_score(y_true_neg, y_pred_neg)
    f1_neg = f1_score(y_true_neg, y_pred_neg)

    # Criar cards mais visuais para as métricas
    st.markdown("### Desempenho do Modelo")
    
    # Função para determinar cor com base no valor da métrica
    def get_color(value):
        if value >= 0.8:
            return "green"
        elif value >= 0.6:
            return "orange"
        else:
            return "red"

    # Criar duas colunas para as métricas
    col1, col2 = st.columns(2)
    
    # Coluna 1: Métricas para Positivo
    with col1:
        st.markdown("#### 😃 Detecção de Sentimentos Positivos")
        
        # Criar métricas visuais
        metrics_html = f"""
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px;">
            <h5 style="margin:0; color: {get_color(precision_pos)};">Precision: {precision_pos:.1%}</h5>
            <p style="margin:0; font-size: 0.8em;">Quando diz que é positivo, acerta {precision_pos:.1%} das vezes</p>
        </div>
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px;">
            <h5 style="margin:0; color: {get_color(recall_pos)};">Recall: {recall_pos:.1%}</h5>
            <p style="margin:0; font-size: 0.8em;">Detecta {recall_pos:.1%} dos sentimentos realmente positivos</p>
        </div>
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
            <h5 style="margin:0; color: {get_color(f1_pos)};">F1 Score: {f1_pos:.1%}</h5>
            <p style="margin:0; font-size: 0.8em;">Equilíbrio entre precisão e abrangência</p>
        </div>
        """
        st.markdown(metrics_html, unsafe_allow_html=True)
    
    # Coluna 2: Métricas para Negativo
    with col2:
        st.markdown("#### 😟 Detecção de Sentimentos Negativos")
        
        # Criar métricas visuais
        metrics_html = f"""
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px;">
            <h5 style="margin:0; color: {get_color(precision_neg)};">Precision: {precision_neg:.1%}</h5>
            <p style="margin:0; font-size: 0.8em;">Quando diz que é negativo, acerta {precision_neg:.1%} das vezes</p>
        </div>
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px;">
            <h5 style="margin:0; color: {get_color(recall_neg)};">Recall: {recall_neg:.1%}</h5>
            <p style="margin:0; font-size: 0.8em;">Detecta {recall_neg:.1%} dos sentimentos realmente negativos</p>
        </div>
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
            <h5 style="margin:0; color: {get_color(f1_neg)};">F1 Score: {f1_neg:.1%}</h5>
            <p style="margin:0; font-size: 0.8em;">Equilíbrio entre precisão e abrangência</p>
        </div>
        """
        st.markdown(metrics_html, unsafe_allow_html=True)

    # Avaliação geral do modelo
    avg_f1 = (f1_pos + f1_neg) / 2
    
    # Determinar a classificação do modelo
    if avg_f1 >= 0.8:
        model_rating = "Excelente"
        color = "green"
        emoji = "🌟"
    elif avg_f1 >= 0.7:
        model_rating = "Bom"
        color = "darkgreen"
        emoji = "✅"
    elif avg_f1 >= 0.6:
        model_rating = "Aceitável"
        color = "orange"
        emoji = "⚠️"
    else:
        model_rating = "Precisa melhorar"
        color = "red"
        emoji = "❗"
    
    # Mostrar avaliação geral
    st.markdown(f"""
    <div style="padding: 15px; background-color: #f8f9fa; border-radius: 5px; margin-top: 20px;">
        <h3 style="margin-top: 0; text-align: center; color: {color};">{emoji} Avaliação Geral do Modelo: {model_rating}</h3>
        <p style="text-align: center;">F1 Score médio: {avg_f1:.1%}</p>
    </div>
    """, unsafe_allow_html=True)

    # Adicionar dicas de uso dos resultados
    with st.expander("💡 Como usar estas informações"):
        st.markdown("""
        ### Como interpretar e usar estas métricas:
        
        #### Se o modelo tem bom desempenho (F1 > 70%):
        - Você pode confiar nas análises de sentimento para tomada de decisões
        - Use os insights dos temas para priorizar melhorias no produto
        
        #### Se o modelo tem desempenho médio (F1 entre 60-70%):
        - Use a análise como guia geral, mas verifique manualmente reviews críticas
        - Concentre-se nas tendências gerais em vez de casos específicos
        
        #### Se o modelo tem baixo desempenho (F1 < 60%):
        - Considere usar outro modelo de análise de sentimento
        - Verifique se as reviews têm características que dificultam a análise (sarcasmo, linguagem técnica)
        
        #### Desequilíbrio entre detecção positiva e negativa:
        - Se o modelo é melhor em detectar positivos: Pode estar perdendo problemas importantes
        - Se o modelo é melhor em detectar negativos: Pode estar subestimando a satisfação dos clientes
        """)
    
    st.markdown("---")
