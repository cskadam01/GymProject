FROM python:3.11-slim

# 1. requirements.txt bemásolása
COPY requirements.txt /app/requirements.txt

# 2. Függőségek telepítése
RUN pip install --no-cache-dir -r /app/requirements.txt

# 3. backend mappa bemásolása
COPY backend /app/backend

# 4. WORKDIR: a `src` mappába lépünk
WORKDIR /app/backend/src

# 5. PYTHONPATH beállítása, hogy `src` működjön
ENV PYTHONPATH=/app/backend

# 6. FastAPI indítása
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]






