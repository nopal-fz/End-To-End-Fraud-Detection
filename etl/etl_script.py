from google.cloud import bigquery
from sqlalchemy import create_engine
import pandas as pd

# set up BigQuery client
client = bigquery.Client.from_service_account_json('C:\\Users\\NAUFAL FAIZ\\Documents\\Fraud ETL\\data\\fraud-detection-project-449112-d58ffa4a2213.json')

# query untuk menarik data
query = """
SELECT 
  Teks, 
  label 
FROM `fraud-detection-project-449112.fraud_data.transactions `;
"""
df = client.query(query).to_dataframe()

# menampilkan beberapa baris pertama
print(df.head())

# set up kredensial PostgreSQL Anda
db_url = 'postgresql://postgres:postgresql123@localhost:5432/fraud_warehouse'

# buat koneksi ke PostgreSQL
engine = create_engine(db_url)

# save dataframe ke PostgreSQL
df.to_sql('transactions_mart', engine, if_exists='replace', index=False)

print("Data berhasil disimpan ke PostgreSQL")