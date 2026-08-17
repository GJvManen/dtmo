from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Role(StrEnum):
    EXECUTIVE = "executive"
    CISO = "ciso"
    SOC = "soc"
    CERT = "cert"
    PRIVACY = "privacy"
    AUDITOR = "auditor"
    ADMIN = "admin"
    ANALYST = "analyst"
    SENIOR_ANALYST = "senior_analyst"
    REVIEWER = "reviewer"
    PUBLISHER = "publisher"
    SERVICE_ACCOUNT = "service_account"


class Permission(StrEnum):
    READ_INTELLIGENCE = "read:intelligence"
    INGEST_INTELLIGENCE = "ingest:intelligence"
    REVIEW_INTELLIGENCE = "review:intelligence"
    CASE_HANDOFF = "handoff:case"
    SHARE_APPROVE = "approve:share"
    MANAGE_CONNECTORS = "manage:connectors"
    MANAGE_USERS = "manage:users"
    REVOKE_TOKENS = "revoke:tokens"
    READ_AUDIT = "read:audit"
    EXPORT_REPORTS = "export:reports"


ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.EXECUTIVE: frozenset({Permission.READ_INTELLIGENCE, Permission.EXPORT_REPORTS}),
    Role.CISO: frozenset(
        {
            Permission.READ_INTELLIGENCE,
            Permission.REVIEW_INTELLIGENCE,
            Permission.CASE_HANDOFF,
            Permission.REVOKE_TOKENS,
            Permission.EXPORT_REPORTS,
        }
    ),
    Role.SOC: frozenset(
        {
            Permission.READ_INTELLIGENCE,
            Permission.INGEST_INTELLIGENCE,
            Permission.REVIEW_INTELLIGENCE,
        }
    ),
    Role.CERT: frozenset(
        {
            Permission.READ_INTELLIGENCE,
            Permission.INGEST_INTELLIGENCE,
            Permission.REVIEW_INTELLIGENCE,
            Permission.CASE_HANDOFF,
            Permission.EXPORT_REPORTS,
        }
    ),
    Role.PRIVACY: frozenset(
        {
            Permission.READ_INTELLIGENCE,
            Permission.REVIEW_INTELLIGENCE,
            Permission.EXPORT_REPORTS,
        }
    ),
    Role.AUDITOR: frozenset({Permission.READ_INTELLIGENCE, Permission.READ_AUDIT}),
    Role.ADMIN: frozenset(Permission),
    Role.ANALYST: frozenset(
        {
            Permission.READ_INTELLIGENCE,
            Permission.INGEST_INTELLIGENCE,
        }
    ),
    Role.SENIOR_ANALYST: frozenset(
        {
            Permission.READ_INTELLIGENCE,
            Permission.INGEST_INTELLIGENCE,
            Permission.REVIEW_INTELLIGENCE,
            Permission.CASE_HANDOFF,
        }
    ),
    Role.REVIEWER: frozenset(
        {
            Permission.READ_INTELLIGENCE,
            Permission.REVIEW_INTELLIGENCE,
        }
    ),
    Role.PUBLISHER: frozenset(
        {
            Permission.READ_INTELLIGENCE,
            Permission.SHARE_APPROVE,
            Permission.EXPORT_REPORTS,
        }
    ),
    Role.SERVICE_ACCOUNT: frozenset(
        {
            Permission.READ_INTELLIGENCE,
            Permission.INGEST_INTELLIGENCE,
            Permission.MANAGE_CONNECTORS,
        }
    ),
}


@dataclass(frozen=True)
class Principal:
    subject: str
    roles: frozenset[Role]

    def __post_init__(self) -> None:
        if not self.subject.strip():
            raise ValueError("principal subject is required")
        if not self.roles:
            raise ValueError("principal requires at least one role")
        if Role.SERVICE_ACCOUNT in self.roles and len(self.roles) != 1:
            raise ValueError("service accounts cannot combine human or administrator roles")

    @property
    def is_service_account(self) -> bool:
        return self.roles == frozenset({Role.SERVICE_ACCOUNT})

    def can(self, permission: Permission) -> bool:
        return any(permission in ROLE_PERMISSIONS[role] for role in self.roles)


def require(principal: Principal, permission: Permission) -> None:
    if not principal.can(permission):
        raise PermissionError(f"{principal.subject} lacks {permission}")


def require_separate_share_approval(principal: Principal, *, reviewed_by: str) -> None:
    """Require an authorized human approver distinct from the intelligence reviewer."""

    require(principal, Permission.SHARE_APPROVE)
    if principal.is_service_account:
        raise PermissionError("service accounts cannot approve external sharing")
    if principal.subject == reviewed_by:
        raise PermissionError("share approval must be performed by a different principal")
