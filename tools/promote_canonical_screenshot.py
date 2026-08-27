from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import struct
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
CANONICAL_SOURCE = "command-center-workbench.png"
CANONICAL_TARGET = "overview-dashboard.png"
CANONICAL_ROUTE = "/workbench/command-center"


def _png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:8] != PNG_SIGNATURE or header[12:16] != b"IHDR":
        raise ValueError("source image is not a valid PNG with an IHDR header")
    return struct.unpack(">II", header[16:24])


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def promote(
    artifact_root: Path,
    repository_root: Path,
    *,
    expected_image_sha256: str,
    source_run_id: str,
    source_head_sha: str,
    source_artifact_digest: str,
    reviewer: str,
) -> dict[str, object]:
    generated = artifact_root / "generated"
    metadata_path = generated / "canonical-capture-metadata.json"
    source = generated / CANONICAL_SOURCE
    if not metadata_path.is_file() or not source.is_file():
        raise ValueError("canonical capture metadata or source PNG is missing")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    required = {
        "canonical_route": CANONICAL_ROUTE,
        "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
        "evidence_classification": "documentation-illustration-only",
        "live_connectivity_proven": False,
        "owner_acceptance_proven": False,
        "production_equivalent_proven": False,
    }
    for key, expected in required.items():
        if metadata.get(key) != expected:
            raise ValueError(f"canonical capture metadata mismatch for {key}")

    actual_sha256 = _sha256(source)
    if actual_sha256 != expected_image_sha256.lower():
        raise ValueError("source image SHA-256 does not match reviewed image")

    width, height = _png_dimensions(source)
    if width < 1200 or height < 900:
        raise ValueError("canonical screenshot is unexpectedly small")

    target = repository_root / "docs" / "visual" / "screenshots" / CANONICAL_TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)

    record = {
        "id": "UI-01",
        "product_surface": "Canonical Command Center",
        "target_image": CANONICAL_TARGET,
        "source_image": CANONICAL_SOURCE,
        "source_run_id": str(source_run_id),
        "source_head_sha": source_head_sha,
        "source_artifact_digest": source_artifact_digest,
        "image_sha256": actual_sha256,
        "dimensions": {"width": width, "height": height},
        "canonical_route": CANONICAL_ROUTE,
        "capture_mode": metadata["capture_mode"],
        "evidence_classification": metadata["evidence_classification"],
        "reviewer": reviewer,
        "claim_boundaries": {
            "live_connectivity_proven": False,
            "owner_acceptance_proven": False,
            "production_equivalent_proven": False,
        },
    }
    review_dir = repository_root / "docs" / "visual" / "screenshots" / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    (review_dir / "UI-01-current.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )
    return record


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Promote one reviewed canonical screenshot fail-closed.")
    parser.add_argument("--artifact-root", required=True)
    parser.add_argument("--repository-root", default=".")
    parser.add_argument("--expected-image-sha256", required=True)
    parser.add_argument("--source-run-id", required=True)
    parser.add_argument("--source-head-sha", required=True)
    parser.add_argument("--source-artifact-digest", required=True)
    parser.add_argument("--reviewer", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    record = promote(
        Path(args.artifact_root),
        Path(args.repository_root),
        expected_image_sha256=args.expected_image_sha256,
        source_run_id=args.source_run_id,
        source_head_sha=args.source_head_sha,
        source_artifact_digest=args.source_artifact_digest,
        reviewer=args.reviewer,
    )
    print(json.dumps(record, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
