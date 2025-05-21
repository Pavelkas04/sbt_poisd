FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y curl tar && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/journal

COPY main.py .

EXPOSE 8000

CMD ["python", "main.py"]
