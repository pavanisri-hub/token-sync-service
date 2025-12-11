FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --prefix=/install -r requirements.txt


FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app


RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

COPY --from=builder /install /usr/local

COPY . /app

COPY cron/2fa-cron /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron

RUN mkdir -p /data /cron && chmod -R 755 /data /cron

EXPOSE 8080
r
CMD service cron start && uvicorn main:app --host 0.0.0.0 --port 8080
