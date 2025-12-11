# =====================================
# Stage 1: Builder
# =====================================
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --default-timeout=180 --prefix=/install -r requirements.txt


# =====================================
# Stage 2: Runtime
# =====================================
FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app

# -------------------------------
# FIX: Add working Debian sources
# -------------------------------
RUN echo "deb http://deb.debian.org/debian trixie main" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian-security trixie-security main" >> /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian trixie-updates main" >> /etc/apt/sources.list

# -------------------------------
# Install cron + timezone + ps command
# -------------------------------
RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
    procps \
    && rm -rf /var/lib/apt/lists/*

# timezone
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Copy installed Python deps
COPY --from=builder /install /usr/local

# Copy entire app
COPY . /app

# Install cron job
COPY cron/2fa-cron /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron

# Create runtime directories
RUN mkdir -p /data /cron && chmod -R 755 /data /cron

EXPOSE 8080

# -------------------------------
# IMPORTANT: Run cron in foreground
# -------------------------------
CMD ["sh", "-c", "cron && uvicorn main:app --host 0.0.0.0 --port 8080"]
