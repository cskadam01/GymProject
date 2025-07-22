# 1. Python image
FROM python:3.11-slim

# 2. Ez mostantól fontos! Az appod itt van:
WORKDIR /backend/src

# 3. requirements.txt a gyökérből jön
COPY requirements.txt /backend/

# 4. Telepítés (itt is a helyes útvonalat adjuk meg)
RUN pip install --no-cache-dir -r /backend/requirements.txt

# 5. backend mappa bemásolása
COPY backend /backend

# 6. Most már a /backend/src-ben vagyunk, úgyhogy innen indulhat:
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]



