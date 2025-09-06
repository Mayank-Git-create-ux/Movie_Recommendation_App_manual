# preprocess.py
import pandas as pd
import re
import nltk
import joblib
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("preprocess.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("🚀 Starting preprocessing...")

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Text cleaning
stop_words = set(stopwords.words('english'))

# Load dataset - try main dataset first, fallback to sample
try:
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try to load main movies.csv first
    csv_path = os.path.join(current_dir, "movies.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        logging.info("✅ Main dataset loaded successfully. Total rows: %d", len(df))
    else:
        # Fallback to sample dataset for deployment
        sample_csv_path = os.path.join(current_dir, "sample_movies.csv")
        df = pd.read_csv(sample_csv_path)
        logging.info("✅ Sample dataset loaded successfully. Total rows: %d", len(df))
        
except Exception as e:
    logging.error("❌ Failed to load dataset: %s", str(e))
    raise e

def preprocess_text(text):
    text = re.sub(r"[^a-zA-Z\s]", "", str(text))
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)


# filter the required columns for recommendation
required_columns = ["genres", "keywords", "overview", "title"]

df = df[required_columns]

df = df.dropna().reset_index(drop=True)

df['combined'] = df['genres'] + ' ' + df['keywords'] + ' ' + df['overview']

logging.info("🧹 Cleaning text...")
df['cleaned_text'] = df['combined'].apply(preprocess_text)
logging.info("✅ Text cleaned.")


# Vectorization
logging.info("🔠 Vectorizing using TF-IDF...")
tfidf = TfidfVectorizer(max_features=5000)
tfidf_matrix = tfidf.fit_transform(df['cleaned_text'])
logging.info("✅ TF-IDF matrix shape: %s", tfidf_matrix.shape)

# Cosine similarity
logging.info("📐 Calculating cosine similarity...")
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
logging.info("✅ Cosine similarity matrix generated.")

# Save everything
current_dir = os.path.dirname(os.path.abspath(__file__))
joblib.dump(df, os.path.join(current_dir, 'df_cleaned.pkl'))
joblib.dump(tfidf_matrix, os.path.join(current_dir, 'tfidf_matrix.pkl'))
joblib.dump(cosine_sim, os.path.join(current_dir, 'cosine_sim.pkl'))
logging.info("💾 Data saved to disk.")

logging.info("✅ Preprocessing complete.")
