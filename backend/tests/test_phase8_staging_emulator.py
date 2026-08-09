from pathlib import Path

COMPOSE = Path("infrastructure/staging-emulator/docker-compose.yml")
NGINX = Path("infrastructure/staging-emulator/nginx.conf")
QA = Path("docs/qa/PHASE8_STAGING_EMULATOR_GATE.md")


def test_emulator_preserves_production_security_invariants() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    for marker in [
        "DTMO_ENVIRONMENT: production",
        'DTMO_MINIO_SECURE: "true"',
        'DTMO_PUBLISH_REQUIRES_HUMAN_APPROVAL: "true"',
        'DTMO_FEATURE_LIVE_CONNECTORS: "false"',
        "DTMO_JWT_JWKS_JSON",
        "DTMO_PRIVACY_PSEUDONYMIZATION_SECRET",
        "internal: true",
        "127.0.0.1:${STAGING_EMULATOR_HTTPS_PORT:-8443}:8443",
        "no-new-privileges:true",
    ]:
        assert marker in text
    assert "plugins.security.disabled" not in text


def test_emulator_requires_immutable_images_and_external_secrets() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    for variable in [
        "DTMO_IMAGE", "POSTGRES_IMAGE", "REDIS_IMAGE", "OPENSEARCH_IMAGE",
        "AISTOR_IMAGE", "PROMETHEUS_IMAGE", "GRAFANA_IMAGE", "NGINX_IMAGE",
    ]:
        assert f"${{{variable}:?" in text
    assert "change-me" not in text
    assert "AISTOR_APP_ACCESS_KEY" in text
    assert "AISTOR_APP_SECRET_KEY" in text


def test_tls_gateway_is_bounded() -> None:
    text = NGINX.read_text(encoding="utf-8")
    assert "listen 8443 ssl" in text
    assert "TLSv1.2 TLSv1.3" in text
    assert "Strict-Transport-Security" in text
    assert "proxy_pass http://api:8000" in text


def test_qa_preserves_emulation_claim_boundary() -> None:
    text = QA.read_text(encoding="utf-8")
    assert "CI_VALIDATION_PENDING" in text
    assert "does not prove a real staging environment" in text
    assert "does not satisfy the ten deployment-parity evidence classes" in text
    assert "human share approval" in text
