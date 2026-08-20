FROM node:22.22.3-bookworm-slim@sha256:e21fc383b50d5347dc7a9f1cae45b8f4e2f0d39f7ade28e4eef7d2934522b752 AS frontend-build

WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/index.html frontend/tsconfig.json frontend/vite.config.ts ./
COPY frontend/src ./src
RUN npm run build

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DTMO_FRONTEND_DIST=/app/frontend/dist

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 dtmo
WORKDIR /app

COPY pyproject.toml README.md alembic.ini ./
COPY backend ./backend
COPY database ./database
COPY tools/provision_grafana_reader.py ./tools/provision_grafana_reader.py
COPY --from=frontend-build /frontend/dist ./frontend/dist
RUN python -m pip install --upgrade pip 'setuptools>=78.1.1' \
    && python -m pip install . \
    && rm -rf \
        /usr/local/lib/python3.12/site-packages/pip \
        /usr/local/lib/python3.12/site-packages/pip-*.dist-info \
        /usr/local/lib/python3.12/site-packages/setuptools \
        /usr/local/lib/python3.12/site-packages/setuptools-*.dist-info \
        /usr/local/lib/python3.12/site-packages/msgpack \
        /usr/local/lib/python3.12/site-packages/msgpack-*.dist-info \
        /usr/local/bin/pip \
        /usr/local/bin/pip3 \
        /usr/local/bin/pip3.12 \
    && python - <<'PY'
from importlib.metadata import PackageNotFoundError, version

for name in ("pip", "setuptools", "msgpack"):
    try:
        detected = version(name)
    except PackageNotFoundError:
        print(f"{name}=absent-from-runtime")
    else:
        raise AssertionError(f"build-only package remains in runtime: {name}={detected}")
PY

USER dtmo
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"

CMD ["uvicorn", "dtmo.main:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8000"]
