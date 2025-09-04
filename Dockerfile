FROM python:3.11-slim

# 1) requirements.txt telepítése (ez legyen az EGYETLEN függőségfájl)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# 2) kód
COPY backend /app/backend

# 3) ugyanaz a WORKDIR, mint régen
WORKDIR /app/backend/src

# 4) hogy a "from src...." importok menjenek
ENV PYTHONPATH=/app/backend

# 5) Uvicorn indítás (Railway PORT támogatással + ideiglenes debug log)
CMD ["sh","-c","uvicorn app:app --log-level debug --host 0.0.0.0 --port ${PORT:-8000}"]





