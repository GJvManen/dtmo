from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime

from redis import Redis
from redis.exceptions import RedisError

from .tokens import AuthenticatedPrincipal


class TokenStateError(RuntimeError):
    """Raised when token state cannot be established safely."""


class TokenRevokedError(TokenStateError):
    """Raised when a token identifier has been revoked."""


class TokenReplayError(TokenStateError):
    """Raised when a one-time bearer token is used more than once."""


@dataclass(frozen=True, slots=True)
class TokenStateStore:
    client: Redis
    namespace: str = "dtmo:token-state"

    @classmethod
    def from_url(cls, redis_url: str) -> TokenStateStore:
        return cls(Redis.from_url(redis_url, decode_responses=True))

    def _key(self, category: str, jti: str) -> str:
        digest = hashlib.sha256(jti.encode("utf-8")).hexdigest()
        return f"{self.namespace}:{category}:{digest}"

    @staticmethod
    def _ttl_seconds(expires_at: datetime, now: datetime) -> int:
        expiry = expires_at.astimezone(UTC)
        current = now.astimezone(UTC)
        return max(1, int((expiry - current).total_seconds()))

    def is_revoked(self, jti: str) -> bool:
        token_id = jti.strip()
        if not token_id:
            raise ValueError("token identifier is required")
        try:
            return bool(self.client.exists(self._key("revoked", token_id)))
        except RedisError as exc:
            raise TokenStateError("token state backend unavailable") from exc

    def assert_active(
        self,
        authenticated: AuthenticatedPrincipal,
        *,
        now: datetime | None = None,
    ) -> None:
        current = now or datetime.now(UTC)
        ttl = self._ttl_seconds(authenticated.expires_at, current)
        replay_key = self._key("used", authenticated.jti)
        binding_key = self._key("binding", authenticated.jti)
        binding = "|".join(
            (
                authenticated.issuer,
                authenticated.principal.subject,
                authenticated.principal_type.value,
                ",".join(sorted(role.value for role in authenticated.principal.roles)),
            )
        )
        try:
            if self.is_revoked(authenticated.jti):
                raise TokenRevokedError("bearer token has been revoked")
            existing_binding = self.client.get(binding_key)
            if existing_binding is None:
                self.client.set(binding_key, binding, ex=ttl, nx=True)
                existing_binding = self.client.get(binding_key)
            if existing_binding != binding:
                raise TokenReplayError("token identifier is already bound to another principal")
            if authenticated.one_time and not self.client.set(replay_key, "used", ex=ttl, nx=True):
                raise TokenReplayError("one-time bearer token has already been used")
        except TokenStateError:
            raise
        except RedisError as exc:
            raise TokenStateError("token state backend unavailable") from exc

    def revoke(self, jti: str, *, expires_at: datetime, now: datetime | None = None) -> None:
        token_id = jti.strip()
        if not token_id:
            raise ValueError("token identifier is required")
        current = now or datetime.now(UTC)
        ttl = self._ttl_seconds(expires_at, current)
        try:
            self.client.set(self._key("revoked", token_id), "revoked", ex=ttl)
        except RedisError as exc:
            raise TokenStateError("token state backend unavailable") from exc
