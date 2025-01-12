FROM python:3.9-slim

WORKDIR /app

# Installa curl per healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

HEALTHCHECK CMD curl --fail http://localhost:5001/health || exit 1

CMD ["python", "server.py"]