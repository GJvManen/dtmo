FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 dtmo
WORKDIR /app

COPY pyproject.toml README.md alembic.ini ./
COPY backend ./backend
COPY database ./database
COPY tools/provision_grafana_reader.py ./tools/provision_grafana_reader.py
RUN python -m pip install --upgrade \
        pip \
        'setuptools>=78.1.1' \
        'msgpack>=1.2.1' \
    && python -m pip install . \
    && python -m pip install --upgrade --force-reinstall \
        'setuptools>=78.1.1' \
        'msgpack>=1.2.1' \
    && python - <<'PY'
from importlib.metadata import distributions, version
from pathlib import Path

for name, minimum in (("msgpack", "1.2.1"), ("setuptools", "78.1.1")):
    active = version(name)
    stale = []
    for dist in distributions():
        if (dist.metadata.get("Name") or "").lower() == name:
            stale.append((dist.version, str(Path(dist._path))))
    print(f"{name}={active}; metadata={stale}")
    assert len(stale) == 1, f"duplicate/stale {name} metadata: {stale}"
PY

USER dtmo
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"

CMD ["uvicorn", "dtmo.main:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8000"]
