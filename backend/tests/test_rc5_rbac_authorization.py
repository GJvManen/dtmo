from __future__ import annotations

import pytest

from dtmo.auth.policy import (
    Permission,
    Principal,
    Role,
    require,
    require_separate_share_approval,
)


def principal(subject: str, *roles: Role) -> Principal:
    return Principal(subject=subject, roles=frozenset(roles))


def test_analyst_can_ingest_but_cannot_review_or_share_approve() -> None:
    analyst = principal("analyst@example.org", Role.ANALYST)

    require(analyst, Permission.INGEST_INTELLIGENCE)
    with pytest.raises(PermissionError):
        require(analyst, Permission.REVIEW_INTELLIGENCE)
    with pytest.raises(PermissionError):
        require(analyst, Permission.SHARE_APPROVE)


def test_reviewer_cannot_ingest_or_share_approve() -> None:
    reviewer = principal("reviewer@example.org", Role.REVIEWER)

    require(reviewer, Permission.REVIEW_INTELLIGENCE)
    with pytest.raises(PermissionError):
        require(reviewer, Permission.INGEST_INTELLIGENCE)
    with pytest.raises(PermissionError):
        require(reviewer, Permission.SHARE_APPROVE)


def test_publisher_can_share_approve_but_cannot_review() -> None:
    publisher = principal("publisher@example.org", Role.PUBLISHER)

    require(publisher, Permission.SHARE_APPROVE)
    with pytest.raises(PermissionError):
        require(publisher, Permission.REVIEW_INTELLIGENCE)


def test_service_account_is_limited_to_non_human_duties() -> None:
    service = principal("connector:vendor-feed", Role.SERVICE_ACCOUNT)

    assert service.is_service_account
    require(service, Permission.INGEST_INTELLIGENCE)
    require(service, Permission.MANAGE_CONNECTORS)
    with pytest.raises(PermissionError):
        require(service, Permission.REVIEW_INTELLIGENCE)
    with pytest.raises(PermissionError):
        require(service, Permission.SHARE_APPROVE)


def test_service_account_cannot_combine_human_or_admin_roles() -> None:
    with pytest.raises(ValueError, match="service accounts cannot combine"):
        principal("connector:vendor-feed", Role.SERVICE_ACCOUNT, Role.ADMIN)


def test_share_approval_requires_a_different_human_principal() -> None:
    publisher = principal("publisher@example.org", Role.PUBLISHER)

    require_separate_share_approval(publisher, reviewed_by="reviewer@example.org")
    with pytest.raises(PermissionError, match="different principal"):
        require_separate_share_approval(publisher, reviewed_by="publisher@example.org")


def test_principal_requires_subject_and_role() -> None:
    with pytest.raises(ValueError, match="subject"):
        Principal(subject=" ", roles=frozenset({Role.ANALYST}))
    with pytest.raises(ValueError, match="at least one role"):
        Principal(subject="analyst@example.org", roles=frozenset())
