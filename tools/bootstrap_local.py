#!/usr/bin/env python3
"""Prepare and validate the DTMO local reference environment.

This helper keeps real secrets outside source control, replaces placeholder values
in .env with generated local-only credentials, and fails early with actionable
messages for external prerequisites such as the AIStor image and license.
"""

from __future__ import annotations

import os
import secrets
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_EXAMPLE = ROOT / ".env.example"
ENV_FILE = ROOT / ".env"

PLACEHOLDER_PREFIX = "<external-"
GENERATED_KEYS = {
    "OPENSEARCH_INITIAL_ADMIN_PASSWORD": lambda: secrets.token_urlsafe(32),
    "GRAFANA_ADMIN_USER": lambda: "dtmo-local-admin",
    "GRAFANA_ADMIN_PASSWORD": lambda: secrets.token_urlsafe(32),
    "GRAFANA_DB_PASSWORD": lambda: secrets.token_urlsafe(32),
    "MINIO_ROOT_USER": lambda: "dtmo-local-aistor-admin",
    "MINIO_ROOT_PASSWORD": lambda: secrets.token_urlsafe(32),
}


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value
    return values


def write_env(values: dict[str, str]) -> None:
    lines = ENV_EXAMPLE.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    for raw in lines:
        if raw.strip() and not raw.lstrip().startswith("#") and "=" in raw:
            key = raw.split("=", 1)[0]
            if key in values:
                out.append(f"{key}={values[key]}")
                continue
        out.append(raw)
    ENV_FILE.write_text("\n".join(out) + "\n", encoding="utf-8")
    try:
        ENV_FILE.chmod(0o600)
    except OSError:
        pass


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def main() -> int:
    if not ENV_EXAMPLE.exists():
        return fail(".env.example is missing")

    docker = shutil.which("docker")
    if not docker:
        return fail("Docker CLI not found. Install/start Docker Desktop, then retry.")

    # `docker` is resolved exclusively via shutil.which("docker") above and no
    # command arguments in this helper are sourced from user input. Keep shell=False
    # (the subprocess default) so neither the executable nor arguments pass through
    # a shell. The narrow S603 suppression documents that trusted executable boundary.
    probe = subprocess.run(  # noqa: S603
        [docker, "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if probe.returncode != 0:
        return fail("Docker daemon is not running. Start Docker Desktop, wait until it is ready, then retry.")

    values = parse_env(ENV_FILE) if ENV_FILE.exists() else parse_env(ENV_EXAMPLE)

    changed = False
    for key, generator in GENERATED_KEYS.items():
        current = values.get(key, "")
        if not current or current.startswith(PLACEHOLDER_PREFIX):
            values[key] = generator()
            changed = True

    # Keep PostgreSQL development credentials internally consistent.
    postgres_password = values.get("POSTGRES_PASSWORD", "change-me") or "change-me"
    values["POSTGRES_PASSWORD"] = postgres_password
    values["DTMO_DATABASE_URL"] = (
        f"postgresql+psycopg://dtmo:{postgres_password}@postgres:5432/dtmo"
    )

    image = values.get("AISTOR_IMAGE", "")
    if not image or "<timestamp>" in image or "<vendor-verified-digest>" in image:
        print(
            "ACTION REQUIRED: set AISTOR_IMAGE in .env to a real vendor-supported AIStor image "
            "reference, preferably pinned by sha256 digest. The example value is documentation only.",
            file=sys.stderr,
        )
        print(
            "Example shape: quay.io/minio/aistor/minio:RELEASE.<real-release>@sha256:<real-digest>",
            file=sys.stderr,
        )
        if changed or not ENV_FILE.exists():
            write_env(values)
        return 2

    license_path = values.get("AISTOR_LICENSE_FILE", "")
    if not license_path or license_path.startswith("/secure/path/"):
        if (ROOT / "AISTOR_LICENSE_FILE").is_file():
            values["AISTOR_LICENSE_FILE"] = str((ROOT / "AISTOR_LICENSE_FILE").resolve())
            changed = True
        else:
            if changed or not ENV_FILE.exists():
                write_env(values)
            return fail(
                "Set AISTOR_LICENSE_FILE in .env to your local AIStor license file. "
                "If you placed it at ./AISTOR_LICENSE_FILE, rerun this helper."
            )

    resolved_license = Path(os.path.expanduser(values["AISTOR_LICENSE_FILE"]))
    if not resolved_license.is_file():
        if changed or not ENV_FILE.exists():
            write_env(values)
        return fail(f"AIStor license file not found: {resolved_license}")

    if changed or not ENV_FILE.exists():
        write_env(values)
        print("Prepared local .env with generated development-only credentials (mode 0600 where supported).")

    env = os.environ.copy()
    env.update(values)
    # Same trusted executable boundary as the daemon probe; arguments are fixed and
    # shell=False remains in force.
    config = subprocess.run(  # noqa: S603
        [docker, "compose", "config", "--quiet"], cwd=ROOT, env=env
    )
    if config.returncode != 0:
        return fail("docker compose config validation failed; resolve the message above before startup.")

    print("Local preflight PASS.")
    print("Next: docker compose up --build")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
