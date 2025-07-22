FROM python:3.11-slim

# 1. requirements.txt bemásolása
COPY requirements.txt /backend/

# 2. Telepítés
RUN pip install --no-cache-dir -r /backend/requirements.txt

# 3. backend mappa bemásolása
COPY backend /backend

# 4. Most állítjuk be a WORKDIR-t, miután már létezik
WORKDIR /backend/src

# 5. Futás
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]




