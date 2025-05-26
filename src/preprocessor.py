import re
import nltk
from nltk.corpus import stopwords

# Download dos recursos necessários do NLTK
def download_nltk_resources():
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('vader_lexicon')

# Pré-processamento do texto
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [word for word in words if word not in stopwords.words('english')]
    return ' '.join(words)