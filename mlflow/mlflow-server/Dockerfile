FROM python:3.8-slim

RUN pip install mlflow

ENV ARTIFACT_ROOT=/mlruns
ENV BACKEND_STORE_URI=sqlite:///mlflow.db
ENV HOST=0.0.0.0
ENV PORT=5500

EXPOSE 5500

CMD mlflow server \
    --backend-store-uri $BACKEND_STORE_URI \
    --default-artifact-root $ARTIFACT_ROOT \
    --host $HOST \
    --port $PORT