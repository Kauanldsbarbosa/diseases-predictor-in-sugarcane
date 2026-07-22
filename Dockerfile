# Etapa de build
FROM python:3.12-alpine3.19 AS build

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    libpq-dev \
    build-base

WORKDIR /app

RUN pip install --upgrade pip setuptools wheel

COPY ./api/config/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-alpine3.19

RUN apk add --no-cache postgresql-libs  # <-- essa é a lib necessária!

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=build /usr/local /usr/local

WORKDIR /app
USER appuser

COPY ./api .

