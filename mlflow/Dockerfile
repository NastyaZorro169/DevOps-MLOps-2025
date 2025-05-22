FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt mlflow

COPY . .

EXPOSE 5000

CMD ["python", "webapp.py", "--port=5000"]