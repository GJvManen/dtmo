from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Protocol


class ObjectStore(Protocol):
    async def put_bytes(self, bucket: str, key: str, data: bytes, content_type: str) -> None: ...
    async def get_bytes(self, bucket: str, key: str) -> bytes: ...


@dataclass(frozen=True)
class RawObjectReceipt:
    bucket: str
    key: str
    sha256: str
    size: int
    source_id: str
    retrieved_at: str


class IntelligenceLake:
    def __init__(self, store: ObjectStore, bucket: str = "dtmo-raw") -> None:
        self.store = store
        self.bucket = bucket

    async def land(self, source_id: str, external_id: str, payload: bytes, content_type: str) -> RawObjectReceipt:
        digest = sha256(payload).hexdigest()
        date = datetime.now(timezone.utc).strftime("%Y/%m/%d")
        safe_external = external_id.replace("/", "_")[:180]
        key = f"{source_id}/{date}/{safe_external}-{digest[:12]}.raw"
        await self.store.put_bytes(self.bucket, key, payload, content_type)
        receipt = RawObjectReceipt(
            bucket=self.bucket,
            key=key,
            sha256=digest,
            size=len(payload),
            source_id=source_id,
            retrieved_at=datetime.now(timezone.utc).isoformat(),
        )
        await self.store.put_bytes(
            self.bucket,
            f"{key}.receipt.json",
            json.dumps(asdict(receipt), sort_keys=True).encode(),
            "application/json",
        )
        return receipt

    async def verify(self, receipt: RawObjectReceipt) -> bool:
        payload = await self.store.get_bytes(receipt.bucket, receipt.key)
        return len(payload) == receipt.size and sha256(payload).hexdigest() == receipt.sha256
