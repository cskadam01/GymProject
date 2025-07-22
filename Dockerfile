# 1. Használjunk egy minimal Python image-et
FROM python:3.11-slim
FROM python:3.11-slim

# 1. Állítsuk be a munkakönyvtárat a konténeren belülre
WORKDIR /backend

# 2. requirements.txt a gyökérből van, úgy másoljuk:
COPY requirements.txt .

# 3. Telepítjük a függőségeket
RUN pip install --no-cache-dir -r requirements.txt

# 4. A teljes backend mappát bemásoljuk
COPY backend/ .

# 5. Elindítjuk az appot
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]



