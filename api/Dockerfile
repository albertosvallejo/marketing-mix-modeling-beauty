# ── Dockerfile — HairBright MMM API ──────────────────────────────────────────
# Imagen ligera: solo FastAPI + numpy + scipy + arviz (sin pymc ni pandas)
# Python 3.11-slim  ·  Multi-stage build para minimizar tamaño final
#
# Build:   docker build -t hairbright-mmm-api .
# Run:     docker run -p 8000:8000 hairbright-mmm-api
# Compose: docker compose up
# ─────────────────────────────────────────────────────────────────────────────

# ── Stage 1: builder ──────────────────────────────────────────────────────────
# Instala dependencias y compila extensiones C en una imagen temporal.
# Solo el resultado (site-packages) se copia al stage final.
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Dependencias del sistema para compilar numpy/scipy/arviz
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ── Stage 2: runtime ─────────────────────────────────────────────────────────
# Imagen final sin compiladores — solo lo necesario para ejecutar la API.
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    # Evita que numpy intente detectar threads en entornos con poca CPU
    OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1

# Dependencias de sistema para runtime (libopenblas sin headers de compilación)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libopenblas0 \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar site-packages compilados desde el stage builder
COPY --from=builder /usr/local/lib/python3.11/site-packages \
                    /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

WORKDIR /app

# Copiar código fuente de la API
COPY main.py .
COPY schemas.py .
COPY model_backend.py .

# Copiar el bundle del modelo (los .npy y metadata.json)
# El bundle NO va al repo (está en .gitignore), se copia en build time
# desde el directorio local.  En producción (Cloud Run / K8s) puede
# montarse como volumen o descargarse desde GCS en el ENTRYPOINT.
COPY mmm_bundle_20260420/ ./mmm_bundle_20260420/

# Usuario no-root por seguridad
RUN useradd --no-create-home --shell /bin/false appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE ${PORT}

# Healthcheck — Docker reiniciará el contenedor si la API no responde
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Arrancar uvicorn leyendo $PORT para compatibilidad con Cloud Run / Railway
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1"]
