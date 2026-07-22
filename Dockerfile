# Etapa de build
FROM python:3.11-slim AS build

WORKDIR /app

RUN pip install --upgrade pip setuptools wheel

COPY ./api/config/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --from=build /usr/local /usr/local

WORKDIR /app
USER appuser

COPY ./api .
