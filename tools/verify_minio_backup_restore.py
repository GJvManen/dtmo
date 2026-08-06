from __future__ import annotations

import argparse
import hashlib
import io
import json
import tarfile
import time
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from minio import Minio


@dataclass(frozen=True)
class ObjectEvidence:
    object_name: str
    size: int
    sha256: str
    provenance_reference: str
    content_type: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "object_name": self.object_name,
            "size": self.size,
            "sha256": self.sha256,
            "provenance_reference": self.provenance_reference,
            "content_type": self.content_type,
        }


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _metadata_value(metadata: dict[str, str], name: str) -> str:
    wanted = name.lower()
    for key, value in metadata.items():
        normalized = key.lower().removeprefix("x-amz-meta-")
        if normalized == wanted:
            return value
    raise ValueError(f"missing object metadata: {name}")


def _ensure_bucket(client: Minio, bucket: str) -> None:
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)


def _empty_bucket(client: Minio, bucket: str) -> None:
    _ensure_bucket(client, bucket)
    objects = list(client.list_objects(bucket, recursive=True))
    if objects:
        for obj in objects:
            client.remove_object(bucket, obj.object_name)
    if list(client.list_objects(bucket, recursive=True)):
        raise RuntimeError(f"target bucket {bucket!r} is not empty")


def _read_object(client: Minio, bucket: str, object_name: str) -> bytes:
    response = client.get_object(bucket, object_name)
    try:
        return response.read()
    finally:
        response.close()
        response.release_conn()


def _snapshot(client: Minio, bucket: str) -> list[ObjectEvidence]:
    evidence: list[ObjectEvidence] = []
    for item in sorted(client.list_objects(bucket, recursive=True), key=lambda obj: obj.object_name):
        data = _read_object(client, bucket, item.object_name)
        stat = client.stat_object(bucket, item.object_name)
        evidence.append(
            ObjectEvidence(
                object_name=item.object_name,
                size=len(data),
                sha256=_sha256(data),
                provenance_reference=_metadata_value(stat.metadata, "provenance-reference"),
                content_type=stat.content_type or "application/octet-stream",
            )
        )
    return evidence


def _seed_source(client: Minio, bucket: str) -> list[ObjectEvidence]:
    _empty_bucket(client, bucket)
    fixtures = (
        (
            "raw/education-advisory.json",
            b'{"source":"vendor-advisory","severity":"high","status":"candidate"}\n',
            "provenance://source/vendor-advisory/2026-08-06/001",
            "application/json",
        ),
        (
            "raw/historical-incident.txt",
            b"Historical education incident evidence with preserved source context.\n",
            "provenance://historical/education-incident/001",
            "text/plain",
        ),
    )
    for object_name, data, provenance, content_type in fixtures:
        client.put_object(
            bucket,
            object_name,
            io.BytesIO(data),
            len(data),
            content_type=content_type,
            metadata={
                "provenance-reference": provenance,
                "content-sha256": _sha256(data),
            },
        )
    return _snapshot(client, bucket)


def _write_backup(
    client: Minio,
    bucket: str,
    objects: list[ObjectEvidence],
    backup_path: Path,
) -> str:
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "source_bucket": bucket,
        "objects": [item.as_dict() for item in objects],
    }
    with tarfile.open(backup_path, "w:gz") as archive:
        manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
        manifest_info = tarfile.TarInfo("manifest.json")
        manifest_info.size = len(manifest_bytes)
        archive.addfile(manifest_info, io.BytesIO(manifest_bytes))
        for item in objects:
            data = _read_object(client, bucket, item.object_name)
            member = PurePosixPath("objects") / item.object_name
            info = tarfile.TarInfo(str(member))
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    if not backup_path.is_file() or backup_path.stat().st_size == 0:
        raise RuntimeError("MinIO backup archive was not created")
    return _sha256(backup_path.read_bytes())


def _restore_backup(client: Minio, target_bucket: str, backup_path: Path) -> list[ObjectEvidence]:
    _empty_bucket(client, target_bucket)
    with tarfile.open(backup_path, "r:gz") as archive:
        manifest_member = archive.getmember("manifest.json")
        manifest_file = archive.extractfile(manifest_member)
        if manifest_file is None:
            raise RuntimeError("backup manifest cannot be read")
        manifest = json.load(manifest_file)
        for item in manifest["objects"]:
            object_name = str(item["object_name"])
            member_name = str(PurePosixPath("objects") / object_name)
            member_file = archive.extractfile(member_name)
            if member_file is None:
                raise RuntimeError(f"backup object cannot be read: {object_name}")
            data = member_file.read()
            expected_digest = str(item["sha256"])
            if _sha256(data) != expected_digest:
                raise RuntimeError(f"backup object digest mismatch: {object_name}")
            client.put_object(
                target_bucket,
                object_name,
                io.BytesIO(data),
                len(data),
                content_type=str(item["content_type"]),
                metadata={
                    "provenance-reference": str(item["provenance_reference"]),
                    "content-sha256": expected_digest,
                },
            )
    return _snapshot(client, target_bucket)


def verify_minio_backup_restore(
    *,
    source: Minio,
    target: Minio,
    source_bucket: str,
    target_bucket: str,
    backup_path: Path,
) -> dict[str, Any]:
    source_objects = _seed_source(source, source_bucket)
    started = time.monotonic()
    backup_sha256 = _write_backup(source, source_bucket, source_objects, backup_path)
    restored_objects = _restore_backup(target, target_bucket, backup_path)
    restore_seconds = round(time.monotonic() - started, 6)

    source_manifest = [item.as_dict() for item in source_objects]
    restored_manifest = [item.as_dict() for item in restored_objects]
    if source_manifest != restored_manifest:
        raise RuntimeError("restored MinIO object manifest does not match source")
    if not all(item.provenance_reference.startswith("provenance://") for item in restored_objects):
        raise RuntimeError("restored objects lost valid provenance references")

    return {
        "schema_version": 1,
        "decision": "pass",
        "source_bucket": source_bucket,
        "target_bucket": target_bucket,
        "clean_target_verified": True,
        "object_count": len(source_objects),
        "backup_sha256": backup_sha256,
        "backup_size_bytes": backup_path.stat().st_size,
        "restore_seconds": restore_seconds,
        "rpo_basis": "quiesced-source-fixture-zero-seconds",
        "object_manifest": source_manifest,
        "provenance_references_verified": True,
        "source_target_manifest_equal": True,
    }


def _client(endpoint: str, access_key: str, secret_key: str, secure: bool) -> Minio:
    return Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify clean MinIO backup and restore integrity")
    parser.add_argument("--source-endpoint", required=True)
    parser.add_argument("--target-endpoint", required=True)
    parser.add_argument("--access-key", required=True)
    parser.add_argument("--secret-key", required=True)
    parser.add_argument("--source-bucket", default="dtmo-source")
    parser.add_argument("--target-bucket", default="dtmo-restore")
    parser.add_argument("--backup", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--secure", action="store_true")
    args = parser.parse_args()

    evidence = verify_minio_backup_restore(
        source=_client(args.source_endpoint, args.access_key, args.secret_key, args.secure),
        target=_client(args.target_endpoint, args.access_key, args.secret_key, args.secure),
        source_bucket=args.source_bucket,
        target_bucket=args.target_bucket,
        backup_path=args.backup,
    )
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
