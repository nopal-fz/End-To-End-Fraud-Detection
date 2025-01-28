from preprocessing.preprocessing import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sqlalchemy import create_engine
import pandas as pd
import pickle

# buat koneksi ke PostgreSQL
db_url = 'postgresql://postgres:postgresql123@localhost:5432/fraud_warehouse'
engine = create_engine(db_url)

# ambil data dari PostgreSQL
query = "SELECT * FROM transactions_mart"
df = pd.read_sql(query, engine)

# cleaning dataframe
df['Teks_bersih'] = df['Teks'].apply(cleaning)
# ekstraksi fitur
X, y, tfidf = tfidf(df)

# save dataset hasil cleaning ke PostgreSQL dan csv
df.to_sql('transactions_mart_clean', engine, if_exists='replace', index=False)
print("Data berhasil disimpan ke PostgreSQL")

df.to_csv('transactions_mart_clean.csv', index=False)
print("Data berhasil disimpan ke CSV")

# train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# inisialisasi model
model = RandomForestClassifier()
# training model
model.fit(X_train, y_train)

# evaluasi model
y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))

# save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Model berhasil disimpan")

# save tfidf vectorizer
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf, f)
print("TF-IDF Vectorizer berhasil disimpan")