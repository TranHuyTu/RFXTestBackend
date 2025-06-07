# Dockerfile for FastAPI app
FROM python:3.12.10-slim-bookworm AS base
WORKDIR /usr/src/app

FROM --platform=arm64 base AS tranhuytu37/rfx_docker-app
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# Install Python dependencies

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


