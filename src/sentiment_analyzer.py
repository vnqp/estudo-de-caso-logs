import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from preprocessor import preprocess_text

def classify_sentiment(score):
    if score < 0.52:
        return "Negativo"
    elif score > 0.67:
        return "Positivo"
    else:
        return "Neutro"

def calculate_precision(df):
    def is_correct_prediction(row):
        predicted = row["sentiment_class"]
        real = row["class_index"]
        
        if real == 1:
            return predicted == "Negativo"
        elif real == 2:
            return predicted in ["Negativo", "Neutro"]
        elif real == 3:
            return predicted in ["Negativo", "Neutro", "Positivo"]
        elif real == 4:
            return predicted in ["Positivo", "Neutro"]
        elif real == 5:
            return predicted == "Positivo"
        return False
    
    return df.apply(is_correct_prediction, axis=1).mean()

def is_correct_prediction_limited(rating, sentiment):
    if rating == 1 and sentiment == "Negativo":
        return True
    if rating == 5 and sentiment == "Positivo":
        return True
    if rating == 4 and sentiment in {"Positivo", "Neutro"}:
        return True
    if rating == 2 and sentiment in {"Negativo", "Neutro"}:
        return True
    return False


def analyze_sentiment(df):
    analyzer = SentimentIntensityAnalyzer()
    df["clean_text"] = df["review_text"].apply(preprocess_text)
    df["sentiment_score"] = df["clean_text"].apply(lambda x: analyzer.polarity_scores(x)["compound"])
    df["sentiment_class"] = df["sentiment_score"].apply(classify_sentiment)
    df["confidence_percent"] = (df["sentiment_score"].abs() * 100).round(2)
    
    precision = calculate_precision(df)
    return df, precision
