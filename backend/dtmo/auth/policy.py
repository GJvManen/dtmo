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


class Permission(StrEnum):
    READ_INTELLIGENCE = "read:intelligence"
    REVIEW_INTELLIGENCE = "review:intelligence"
    SHARE_APPROVE = "approve:share"
    MANAGE_CONNECTORS = "manage:connectors"
    MANAGE_USERS = "manage:users"
    READ_AUDIT = "read:audit"
    EXPORT_REPORTS = "export:reports"


ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.EXECUTIVE: frozenset({Permission.READ_INTELLIGENCE, Permission.EXPORT_REPORTS}),
    Role.CISO: frozenset({Permission.READ_INTELLIGENCE, Permission.REVIEW_INTELLIGENCE, Permission.EXPORT_REPORTS}),
    Role.SOC: frozenset({Permission.READ_INTELLIGENCE, Permission.REVIEW_INTELLIGENCE}),
    Role.CERT: frozenset({Permission.READ_INTELLIGENCE, Permission.REVIEW_INTELLIGENCE, Permission.EXPORT_REPORTS}),
    Role.PRIVACY: frozenset({Permission.READ_INTELLIGENCE, Permission.REVIEW_INTELLIGENCE, Permission.EXPORT_REPORTS}),
    Role.AUDITOR: frozenset({Permission.READ_INTELLIGENCE, Permission.READ_AUDIT}),
    Role.ADMIN: frozenset(Permission),
}


@dataclass(frozen=True)
class Principal:
    subject: str
    roles: frozenset[Role]

    def can(self, permission: Permission) -> bool:
        return any(permission in ROLE_PERMISSIONS[role] for role in self.roles)


def require(principal: Principal, permission: Permission) -> None:
    if not principal.can(permission):
        raise PermissionError(f"{principal.subject} lacks {permission}")
