from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from dtmo.auth.policy import Principal, Role
from dtmo.auth.token_state import TokenReplayError, TokenRevokedError, TokenStateStore
from dtmo.auth.tokens import AuthenticatedPrincipal, PrincipalType


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}

    def exists(self, key: str) -> int:
        return int(key in self.values)

    def get(self, key: str) -> str | None:
        return self.values.get(key)

    def set(self, key: str, value: str, *, ex: int, nx: bool = False) -> bool:
        del ex
        if nx and key in self.values:
            return False
        self.values[key] = value
        return True


def _principal(*, jti: str = "token-1", one_time: bool = False) -> AuthenticatedPrincipal:
    now = datetime(2026, 8, 6, 12, 0, tzinfo=UTC)
    return AuthenticatedPrincipal(
        principal=Principal("analyst@example.test", frozenset({Role.ANALYST})),
        principal_type=PrincipalType.HUMAN,
        jti=jti,
        issuer="https://issuer.example.test",
        authenticated_at=now,
        expires_at=now + timedelta(minutes=10),
        one_time=one_time,
    )


def test_active_reusable_token_keeps_stable_jti_binding() -> None:
    store = TokenStateStore(FakeRedis())  # type: ignore[arg-type]
    principal = _principal()
    store.assert_active(principal, now=principal.authenticated_at)
    store.assert_active(principal, now=principal.authenticated_at + timedelta(seconds=1))


def test_revoked_token_is_rejected_until_expiry() -> None:
    store = TokenStateStore(FakeRedis())  # type: ignore[arg-type]
    principal = _principal()
    store.revoke(principal.jti, expires_at=principal.expires_at, now=principal.authenticated_at)
    with pytest.raises(TokenRevokedError, match="revoked"):
        store.assert_active(principal, now=principal.authenticated_at)


def test_one_time_token_replay_is_rejected() -> None:
    store = TokenStateStore(FakeRedis())  # type: ignore[arg-type]
    principal = _principal(one_time=True)
    store.assert_active(principal, now=principal.authenticated_at)
    with pytest.raises(TokenReplayError, match="already been used"):
        store.assert_active(principal, now=principal.authenticated_at + timedelta(seconds=1))


def test_jti_cannot_be_rebound_to_another_principal() -> None:
    store = TokenStateStore(FakeRedis())  # type: ignore[arg-type]
    original = _principal()
    store.assert_active(original, now=original.authenticated_at)
    changed = AuthenticatedPrincipal(
        principal=Principal("attacker@example.test", frozenset({Role.ANALYST})),
        principal_type=PrincipalType.HUMAN,
        jti=original.jti,
        issuer=original.issuer,
        authenticated_at=original.authenticated_at,
        expires_at=original.expires_at,
    )
    with pytest.raises(TokenReplayError, match="bound to another principal"):
        store.assert_active(changed, now=changed.authenticated_at)


def test_revoke_requires_non_empty_identifier() -> None:
    store = TokenStateStore(FakeRedis())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="required"):
        store.revoke(
            " ",
            expires_at=datetime(2026, 8, 6, 12, 10, tzinfo=UTC),
            now=datetime(2026, 8, 6, 12, 0, tzinfo=UTC),
        )
