FROM python:3.11-slim

# 1) Függőségek
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Kód: csak a backend mappa kell, benne a src
COPY backend /app/backend

# 3) A PYTHONPATH legyen a 'src' SZÜLŐJE, hogy a 'from src....' import működjön
ENV PYTHONPATH=/app/backend

# 4) Nem bízzuk a WORKDIR-re az importot, megadjuk az app-könyvtárat
CMD ["sh","-c","uvicorn app:app --app-dir /app/backend/src --host 0.0.0.0 --port ${PORT:-8000}"]





