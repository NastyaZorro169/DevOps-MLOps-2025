FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

WORKDIR /app

# Копируем только requirements.txt сначала
COPY requirements.txt .

# Устанавливаем зависимости и mlflow в одном шаге, чтобы не плодить слои
RUN pip install --no-cache-dir -r requirements.txt mlflow

# Копируем остальной код приложения
COPY . .

EXPOSE 5000

CMD ["python", "webapp.py", "--port=5000"]