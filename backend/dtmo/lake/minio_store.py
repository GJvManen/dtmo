from __future__ import annotations

import asyncio
from io import BytesIO

from minio import Minio
from minio.error import S3Error

from dtmo.config import Settings, get_settings


class MinioObjectStore:
    def __init__(self, settings: Settings | None = None) -> None:
        cfg = settings or get_settings()
        self.client = Minio(
            cfg.minio_endpoint,
            access_key=cfg.minio_access_key,
            secret_key=cfg.minio_secret_key.get_secret_value(),
            secure=cfg.minio_secure,
        )

    async def ensure_bucket(self, bucket: str) -> None:
        def create() -> None:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)

        await asyncio.to_thread(create)

    async def put_bytes(
        self,
        bucket: str,
        key: str,
        data: bytes,
        content_type: str,
    ) -> None:
        await self.ensure_bucket(bucket)

        def upload() -> None:
            self.client.put_object(
                bucket,
                key,
                BytesIO(data),
                length=len(data),
                content_type=content_type,
            )

        await asyncio.to_thread(upload)

    async def get_bytes(self, bucket: str, key: str) -> bytes:
        def download() -> bytes:
            response = self.client.get_object(bucket, key)
            try:
                return response.read()
            finally:
                response.close()
                response.release_conn()

        return await asyncio.to_thread(download)

    async def ping(self) -> bool:
        try:
            await asyncio.to_thread(lambda: list(self.client.list_buckets()))
            return True
        except (S3Error, OSError):
            return False
