from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# load model
with open('C:\\Users\\NAUFAL FAIZ\\Documents\\Fraud ETL\\model\\model.pkl', 'rb') as f:
    model = pickle.load(f)
    
# load tfidf vectorizer
with open('C:\\Users\\NAUFAL FAIZ\\Documents\\Fraud ETL\\model\\tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)

# inisialisasi fastapi
app = FastAPI()

# pydantic untuk input data
class TransactionRequest(BaseModel):
    text: str

# endpoint untuk prediksi fraud
@app.post('/predict')
def predict(transaction: TransactionRequest):
    X_new = tfidf.transform([transaction.text])
    
    prediction = model.predict(X_new)
    
    result = "Fraud" if prediction[0] == 1 else "Not Fraud"
    return {"Text": transaction.text, "Prediction": result}

# menjalankan aplikasi fastapi
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)