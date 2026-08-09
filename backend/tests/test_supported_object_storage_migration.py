from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "docker-compose.yml"
ENV_EXAMPLE = ROOT / ".env.example"


def test_legacy_minio_runtime_is_removed_from_compose() -> None:
    compose = COMPOSE.read_text(encoding="utf-8")

    assert "minio/minio:" not in compose
    assert "quay.io/minio/aistor/minio" in compose


def test_aistor_image_reference_fails_closed_without_digest_pinned_input() -> None:
    compose = COMPOSE.read_text(encoding="utf-8")

    assert "image: ${AISTOR_IMAGE:?" in compose
    assert "@sha256:<vendor-verified-digest>" in compose
    assert "latest" not in compose.lower()


def test_aistor_license_and_admin_credentials_are_external_inputs() -> None:
    compose = COMPOSE.read_text(encoding="utf-8")
    env_example = ENV_EXAMPLE.read_text(encoding="utf-8")

    assert "--license /run/secrets/aistor_license" in compose
    assert "aistor_license:" in compose
    assert "file: ${AISTOR_LICENSE_FILE:?" in compose
    assert "MINIO_ROOT_USER: ${MINIO_ROOT_USER:?" in compose
    assert "MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:?" in compose
    assert "MINIO_ROOT_USER=dtmo" not in env_example
    assert "MINIO_ROOT_PASSWORD=change-me-now" not in env_example


def test_s3_service_contract_and_persistent_volume_are_preserved() -> None:
    compose = COMPOSE.read_text(encoding="utf-8")
    env_example = ENV_EXAMPLE.read_text(encoding="utf-8")

    assert "  minio:\n" in compose
    assert "- minio_data:/data" in compose
    assert "DTMO_MINIO_ENDPOINT=minio:9000" in env_example
    assert "DTMO_PUBLISH_REQUIRES_HUMAN_APPROVAL=true" in env_example
