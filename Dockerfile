# -------- Stage 1: build deps --------
FROM python:3.12-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
    
ARG REQUIREMENTS
COPY requirements/ ./requirements

RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r ${REQUIREMENTS}


# -------- Stage 2: final image --------
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements ./requirements

RUN pip install --no-cache-dir /wheels/*

COPY . .

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "smart_home.asgi:application"]