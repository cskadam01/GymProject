FROM python:3.11-slim

# Függőségek
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kód bemásolása (gyökér -> /app)
# Ha csak a src kellene, akkor elég: COPY src /app/src
COPY . .

# Ha a src importál bármit a backend-ből vagy máshonnan, így biztos a PYTHONPATH
ENV PYTHONPATH=/app
WORKDIR /app/src

# Railway-n a PORT változót érdemes használni; fallback 8000 lokális futtatáshoz
CMD ["sh","-c","uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]





