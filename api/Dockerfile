# Dockerfile for FastAPI
FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl build-essential

RUN curl -O https://ollama.com/download/ollama-linux && \
    chmod +x ollama-linux && \
    mv ollama-linux /usr/local/bin/ollama && \
    ollama pull gemma2:2b

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "router:app", "--host=127.0.0.1", "--port=80"]
