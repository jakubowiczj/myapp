FROM python:3.12-slim

WORKDIR /app

# Zależności - w tym katalogu JEST requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kod aplikacji - w tym katalogu JEST folder app/
COPY . /app

# EB domyślnie kieruje ruch na 8080 → dopasowujemy
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
