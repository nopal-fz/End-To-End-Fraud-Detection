import pandas as pd
from sqlalchemy import create_engine
import string
import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# buat koneksi ke PostgreSQL
db_url = 'postgresql://postgres:postgresql123@localhost:5432/fraud_warehouse'
engine = create_engine(db_url)

# ambil data dari PostgreSQL
query = "SELECT * FROM transactions_mart"
df = pd.read_sql(query, engine)

print(df.head())

# fungsi cleaning
def cleaning(text):
    # stopword
    stop_factory = StopWordRemoverFactory().get_stop_words()
    # stemmer
    stem_factory = StemmerFactory()
    stemmer = stem_factory.create_stemmer()
    
    text = text.lower() # ubah teks menjadi lower case
    text = text.strip(' ') # menghapus spasi di awal dan di akhir
    text = re.sub(r'\d+', '', text) # menghapus angka
    text = text.translate(str.maketrans('','', string.punctuation)) # menghapus punctuation
    text = re.sub(r'\b[a-zA-Z]\b', '', text) # menghapus kata yang hanya terdiri dari satu huruf
    text = re.sub(r'\s+', ' ', text) # menghapus spasi berlebih
    text = word_tokenize(text) # tokenisasi
    text = [word for word in text if word not in stop_factory] # menghapus stopword
    text = [stemmer.stem(word) for word in text] # stemming
    text = ' '.join(text)
    return text

# fungsi TF-IDF
def tfidf(df):
    tfidf = TfidfVectorizer(max_features=1000)
    X = tfidf.fit_transform(df['Teks_bersih']).toarray()
    y = df['label']
    
    return X, y, tfidf