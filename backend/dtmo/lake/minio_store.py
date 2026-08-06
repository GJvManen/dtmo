from __future__ import annotations

import asyncio
from io import BytesIO

from minio import Minio
from minio.error import S3Error

from dtmo.config import Settings, get_settings


class MinioObjectStore:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._client: Minio | None = None

    @property
    def client(self) -> Minio:
        """Create the MinIO client only when object storage is actually used.

        Application import, health checks and unit-test collection must not require
        object-storage credentials or a reachable MinIO service. Production
        configuration validation remains enforced by ``Settings``.
        """
        if self._client is None:
            self._client = Minio(
                self.settings.minio_endpoint,
                access_key=self.settings.minio_access_key,
                secret_key=self.settings.minio_secret_key.get_secret_value(),
                secure=self.settings.minio_secure,
            )
        return self._client

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
        except (S3Error, OSError, ValueError):
            return False
