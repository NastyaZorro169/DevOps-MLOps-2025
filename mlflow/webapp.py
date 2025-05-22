"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser,
with MLflow integration for model management and logging.
"""
import argparse
import io
import datetime
import requests
import time

from PIL import Image
import mlflow
import mlflow.pytorch
import torch
from flask import Flask, render_template, request, redirect
from dictionary import class_names

app = Flask(__name__)

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return redirect(request.url)

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        with mlflow.start_run():
            start_time = time.time()

            # Предсказание с использованием загруженной модели MLflow
            results = model([img]) # если модель pyfunc, иначе model([img])

            inference_time = time.time() - start_time

            # Логируем параметры и метрики
            mlflow.log_param("image_size", img.size)
            mlflow.log_metric("inference_time", inference_time)

            # Обновление меток на русский язык
            for i in range(len(results.xyxy[0])):
                class_index = int(results.xyxy[0][i][5])
                results.names[class_index] = class_names.get(results.names[class_index], results.names[class_index])

            results.render()  # обновляет results.ims с нарисованными рамками и метками

            now_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
            img_savename = f"static/{now_time}.png"
            Image.fromarray(results.ims[0]).save(img_savename)

            # Логируем артефакт — изображение с результатом
            mlflow.log_artifact(img_savename)

        return redirect(img_savename)

    return render_template("index.html")


def wait_for_mlflow(uri, timeout=60):
    start = time.time()
    while True:
        try:
            r = requests.get(uri)
            if r.status_code == 200:
                print("MLflow server is up")
                break
        except Exception:
            pass
        if time.time() - start > timeout:
            raise TimeoutError("MLflow server did not start in time")
        print("Waiting for MLflow server...")
        time.sleep(2)

def save_yolov5_model_and_get_uri():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.eval()

    with mlflow.start_run() as run:
        mlflow.pytorch.log_model(model, artifact_path="yolov5_model")
        run_id = run.info.run_id
        model_uri = f"runs:/{run_id}/yolov5_model"
        print(f"Model saved at URI: {model_uri}")
        return model_uri


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models with MLflow integration")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    parser.add_argument("--mlflow-uri", default="http://mlflow-server:5500", type=str, help="MLflow tracking server URI")
    args = parser.parse_args()

    mlflow.set_tracking_uri(args.mlflow_uri)
    wait_for_mlflow(args.mlflow_uri)

    model_uri = save_yolov5_model_and_get_uri()

    model = mlflow.pytorch.load_model(model_uri)
    model.eval()

    app.run(host="0.0.0.0", port=args.port)

