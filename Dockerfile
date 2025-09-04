FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend /app/backend
ENV PYTHONPATH=/app/backend
WORKDIR /app/backend/src
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]




