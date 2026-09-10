# 1. Hafif ve güncel Python imajı
FROM python:3.11-slim

# 2. Python çıktılarının anında loglanması için
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 3. Çalışma dizini
WORKDIR /app

# 4. Önce kütüphaneleri yükleyelim (Docker Cache avantajı)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Tüm proje klasörlerini (database, handlers, services, main.py vb.) kopyalayalım
COPY . .

# 6. Botu çalıştıran komut
CMD ["python", "main.py"]