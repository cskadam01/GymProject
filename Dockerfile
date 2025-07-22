# 1. Használjunk egy minimal Python image-et
FROM python:3.11-slim

# 2. Munkakönyvtár beállítása
WORKDIR /app

# 3. Követelmények bemásolása és telepítése
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Az összes backend fájl bemásolása
COPY backend/ ./backend/

# 5. A FastAPI app futtatása
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]


