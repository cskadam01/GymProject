FROM python:3.11-slim

# Függőségek
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kód
COPY backend /app/backend
# Ha az app futás közben a gyökérből olvas fájlokat (pl. mydatabase.db, sa.b64.txt), másold őket is:
# COPY mydatabase.db /app/mydatabase.db
# COPY sa.b64.txt /app/sa.b64.txt

# A 'from src....' importokhoz a 'src' szülőjét tesszük az importútvonalra
ENV PYTHONPATH=/app/backend

# Uvicorn: egyértelműen megadjuk, hol az app.py; Railway PORT-ot használunk
CMD ["sh","-c","uvicorn app:app --app-dir /app/backend/src --host 0.0.0.0 --port ${PORT:-8000}"]




