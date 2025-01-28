# menggunakan image Python yang ringan sebagai base image
FROM python:3.8-slim

# install dependencies yang diperlukan
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-server-dev-all

# set working directory di dalam container
WORKDIR /app

# salin requirements.txt ke dalam container
COPY requirements.txt .

# salin model ke dalam container
COPY ./model /app/model

# install dependensi yang ada di requirements.txt
RUN pip install -r requirements.txt

# salin seluruh kode aplikasi ke dalam container
COPY . .

# Tentukan perintah untuk menjalankan aplikasi FastAPI dengan Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]