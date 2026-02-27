# syntax=docker/dockerfile:1.2
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_ARTIFACT_PATH=data/model.skops

WORKDIR /app

COPY pyproject.toml README.md /app/
COPY challenge /app/challenge
COPY data/model.skops /app/data/model.skops

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir .

RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]
