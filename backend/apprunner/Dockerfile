FROM python:3.12-slim

WORKDIR /app

RUN python -m pip install --upgrade pip setuptools wheel

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
EXPOSE 80
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","80"]
