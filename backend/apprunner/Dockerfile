FROM python:3.12-slim

WORKDIR /app

# Zależności
COPY backend/apprunner/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kod aplikacji
COPY backend/apprunner /app

# EB kieruje ruch na 8080 → dopasowujemy
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
