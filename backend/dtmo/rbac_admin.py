from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, DateTime, ForeignKey, String, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, Session, mapped_column

from dtmo.api.routes import get_session
from dtmo.audit import AuditDecision
from dtmo.audit.store import append_persistent_audit_event
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal, ROLE_PERMISSIONS, Role
from dtmo.persistence.models import Base, utc_now

router = APIRouter(prefix="/api/v1/admin/rbac", tags=["admin-rbac"])

MANAGED_HUMAN = "human"
MANAGED_SERVICE_ACCOUNT = "service_account"
MANAGED_PRINCIPAL_TYPES = frozenset({MANAGED_HUMAN, MANAGED_SERVICE_ACCOUNT})


class RbacValidationError(ValueError):
    """Raised when requested managed identity state violates the RBAC contract."""


class RbacConflictError(ValueError):
    """Raised when a valid request would violate an administrative safety invariant."""


class ManagedPrincipal(Base):
    __tablename__ = "managed_principals"

    subject: Mapped[str] = mapped_column(String(255), primary_key=True)
    display_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    principal_type: Mapped[str] = mapped_column(String(32), index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_by: Mapped[str] = mapped_column(String(255))
    updated_by: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class ManagedRoleAssignment(Base):
    __tablename__ = "managed_role_assignments"

    subject: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("managed_principals.subject", ondelete="CASCADE"),
        primary_key=True,
    )
    role: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    assigned_by: Mapped[str] = mapped_column(String(255))
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


@dataclass(frozen=True, slots=True)
class ManagedPrincipalState:
    subject: str
    display_name: str | None
    principal_type: str
    active: bool
    roles: tuple[Role, ...]
    created_by: str
    updated_by: str
    created_at: datetime
    updated_at: datetime


class ManagedPrincipalStore:
    def __init__(self, session: Session) -> None:
        self.session = session

    def _roles(self, subject: str) -> tuple[Role, ...]:
        values = self.session.scalars(
            select(ManagedRoleAssignment.role)
            .where(ManagedRoleAssignment.subject == subject)
            .order_by(ManagedRoleAssignment.role.asc())
        ).all()
        return tuple(Role(value) for value in values)

    def _state(self, row: ManagedPrincipal) -> ManagedPrincipalState:
        return ManagedPrincipalState(
            subject=row.subject,
            display_name=row.display_name,
            principal_type=row.principal_type,
            active=row.active,
            roles=self._roles(row.subject),
            created_by=row.created_by,
            updated_by=row.updated_by,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    def list(self) -> list[ManagedPrincipalState]:
        rows = self.session.scalars(
            select(ManagedPrincipal).order_by(ManagedPrincipal.subject.asc())
        ).all()
        return [self._state(row) for row in rows]

    def get(self, subject: str) -> ManagedPrincipalState | None:
        normalized = validate_subject(subject)
        row = self.session.get(ManagedPrincipal, normalized)
        return None if row is None else self._state(row)

    def active_admin_count(self) -> int:
        count = self.session.scalar(
            select(func.count())
            .select_from(ManagedPrincipal)
            .join(
                ManagedRoleAssignment,
                ManagedRoleAssignment.subject == ManagedPrincipal.subject,
            )
            .where(
                ManagedPrincipal.active.is_(True),
                ManagedPrincipal.principal_type == MANAGED_HUMAN,
                ManagedRoleAssignment.role == Role.ADMIN.value,
            )
        )
        return int(count or 0)

    def create(
        self,
        *,
        subject: str,
        display_name: str | None,
        principal_type: str,
        roles: Sequence[Role],
        active: bool,
        actor: str,
    ) -> ManagedPrincipalState:
        normalized_subject = validate_subject(subject)
        normalized_type = validate_principal_type(principal_type)
        normalized_roles = validate_roles(normalized_type, roles)
        if self.session.get(ManagedPrincipal, normalized_subject) is not None:
            raise RbacConflictError("managed principal already exists")
        row = ManagedPrincipal(
            subject=normalized_subject,
            display_name=normalize_display_name(display_name),
            principal_type=normalized_type,
            active=active,
            created_by=actor,
            updated_by=actor,
        )
        self.session.add(row)
        self.session.flush()
        for role in normalized_roles:
            self.session.add(
                ManagedRoleAssignment(
                    subject=normalized_subject,
                    role=role.value,
                    assigned_by=actor,
                )
            )
        self.session.flush()
        return self._state(row)

    def update(
        self,
        subject: str,
        *,
        display_name: str | None,
        active: bool | None,
        roles: Sequence[Role] | None,
        actor: str,
    ) -> ManagedPrincipalState:
        normalized_subject = validate_subject(subject)
        row = self.session.get(ManagedPrincipal, normalized_subject)
        if row is None:
            raise RbacConflictError("managed principal not found")
        current = self._state(row)
        next_active = current.active if active is None else active
        next_roles = (
            current.roles
            if roles is None
            else validate_roles(row.principal_type, roles)
        )
        if (
            current.active
            and Role.ADMIN in current.roles
            and (not next_active or Role.ADMIN not in next_roles)
            and self.active_admin_count() <= 1
        ):
            raise RbacConflictError("cannot remove or deactivate the last managed admin")
        if display_name is not None:
            row.display_name = normalize_display_name(display_name)
        if active is not None:
            row.active = active
        if roles is not None:
            self.session.execute(
                delete(ManagedRoleAssignment).where(
                    ManagedRoleAssignment.subject == normalized_subject
                )
            )
            self.session.flush()
            for role in next_roles:
                self.session.add(
                    ManagedRoleAssignment(
                        subject=normalized_subject,
                        role=role.value,
                        assigned_by=actor,
                    )
                )
        row.updated_by = actor
        row.updated_at = utc_now()
        self.session.flush()
        return self._state(row)


def validate_subject(value: str) -> str:
    subject = value.strip()
    if not subject:
        raise RbacValidationError("principal subject is required")
    if len(subject) > 255:
        raise RbacValidationError("principal subject is too long")
    if "/" in subject or any(ord(character) < 32 for character in subject):
        raise RbacValidationError("principal subject contains unsupported characters")
    return subject


def normalize_display_name(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if len(normalized) > 255:
        raise RbacValidationError("display name is too long")
    return normalized or None


def validate_principal_type(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in MANAGED_PRINCIPAL_TYPES:
        raise RbacValidationError("principal_type must be human or service_account")
    return normalized


def validate_roles(principal_type: str, roles: Sequence[Role]) -> tuple[Role, ...]:
    normalized = tuple(sorted(frozenset(roles), key=lambda role: role.value))
    if not normalized:
        raise RbacValidationError("at least one role assignment is required")
    if principal_type == MANAGED_SERVICE_ACCOUNT:
        if normalized != (Role.SERVICE_ACCOUNT,):
            raise RbacValidationError("service accounts must use only the service_account role")
    elif Role.SERVICE_ACCOUNT in normalized:
        raise RbacValidationError("human principals cannot use the service_account role")
    return normalized


class RoleCatalogResponse(BaseModel):
    role: Role
    permissions: list[Permission]
    eligible_principal_types: list[str]
    immutable: bool = True


class ManagedPrincipalCreateRequest(BaseModel):
    subject: str = Field(min_length=1, max_length=255)
    display_name: str | None = Field(default=None, max_length=255)
    principal_type: Literal["human", "service_account"] = "human"
    roles: list[Role] = Field(min_length=1)
    active: bool = True


class ManagedPrincipalUpdateRequest(BaseModel):
    display_name: str | None = Field(default=None, max_length=255)
    roles: list[Role] | None = Field(default=None, min_length=1)
    active: bool | None = None


class ManagedPrincipalResponse(BaseModel):
    subject: str
    display_name: str | None
    principal_type: str
    active: bool
    roles: list[Role]
    created_by: str
    updated_by: str
    created_at: datetime
    updated_at: datetime
    requires_token_reissue: bool = True
    authorization_note: str = (
        "Production bearer tokens are externally issued; assignment changes require "
        "identity-provider reconciliation or token reissue and never rewrite active tokens."
    )


def _human_admin(principal: Principal) -> None:
    if principal.is_service_account or Role.ADMIN not in principal.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="RBAC administration requires a human admin role",
        )


def _guard_target(principal: Principal, subject: str) -> str:
    normalized = validate_subject(subject)
    if normalized == principal.subject:
        raise RbacConflictError("administrators cannot change their own managed assignment")
    return normalized


def _response(state: ManagedPrincipalState) -> ManagedPrincipalResponse:
    return ManagedPrincipalResponse(
        subject=state.subject,
        display_name=state.display_name,
        principal_type=state.principal_type,
        active=state.active,
        roles=list(state.roles),
        created_by=state.created_by,
        updated_by=state.updated_by,
        created_at=state.created_at,
        updated_at=state.updated_at,
    )


def _audit(
    session: Session,
    *,
    principal: Principal,
    action: str,
    state: ManagedPrincipalState,
    request_id: str,
) -> None:
    role_list = ",".join(role.value for role in state.roles)
    append_persistent_audit_event(
        session,
        principal=principal.subject,
        principal_type="human",
        action=action,
        resource=f"principal:{state.subject}",
        decision=AuditDecision.ALLOW,
        request_id=request_id,
        provenance_reference=(
            f"principal_type:{state.principal_type};active:{str(state.active).lower()};roles:{role_list}"
        ),
    )


def _map_error(exc: ValueError) -> HTTPException:
    if isinstance(exc, RbacConflictError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/roles", response_model=list[RoleCatalogResponse])
async def role_catalog(
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_USERS))],
) -> list[RoleCatalogResponse]:
    _human_admin(principal)
    result: list[RoleCatalogResponse] = []
    for role in Role:
        types = (
            [MANAGED_SERVICE_ACCOUNT]
            if role is Role.SERVICE_ACCOUNT
            else [MANAGED_HUMAN]
        )
        result.append(
            RoleCatalogResponse(
                role=role,
                permissions=sorted(ROLE_PERMISSIONS[role], key=lambda item: item.value),
                eligible_principal_types=types,
            )
        )
    return result


@router.get("/principals", response_model=list[ManagedPrincipalResponse])
async def list_managed_principals(
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_USERS))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[ManagedPrincipalResponse]:
    _human_admin(principal)
    states = await session.run_sync(lambda sync: ManagedPrincipalStore(sync).list())
    return [_response(state) for state in states]


@router.post(
    "/principals",
    response_model=ManagedPrincipalResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_managed_principal(
    request: ManagedPrincipalCreateRequest,
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_USERS))],
    session: Annotated[AsyncSession, Depends(get_session)],
    request_id: Annotated[str, Header(alias="X-Request-ID", min_length=1, max_length=255)],
) -> ManagedPrincipalResponse:
    _human_admin(principal)
    try:
        subject = _guard_target(principal, request.subject)

        def mutation(sync: Session) -> ManagedPrincipalState:
            state = ManagedPrincipalStore(sync).create(
                subject=subject,
                display_name=request.display_name,
                principal_type=request.principal_type,
                roles=request.roles,
                active=request.active,
                actor=principal.subject,
            )
            _audit(
                sync,
                principal=principal,
                action="rbac.principal.create",
                state=state,
                request_id=request_id,
            )
            return state

        state = await session.run_sync(mutation)
    except ValueError as exc:
        raise _map_error(exc) from exc
    return _response(state)


@router.patch("/principals/{subject}", response_model=ManagedPrincipalResponse)
async def update_managed_principal(
    subject: str,
    request: ManagedPrincipalUpdateRequest,
    principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_USERS))],
    session: Annotated[AsyncSession, Depends(get_session)],
    request_id: Annotated[str, Header(alias="X-Request-ID", min_length=1, max_length=255)],
) -> ManagedPrincipalResponse:
    _human_admin(principal)
    try:
        normalized_subject = _guard_target(principal, subject)

        def mutation(sync: Session) -> ManagedPrincipalState:
            state = ManagedPrincipalStore(sync).update(
                normalized_subject,
                display_name=request.display_name,
                active=request.active,
                roles=request.roles,
                actor=principal.subject,
            )
            _audit(
                sync,
                principal=principal,
                action="rbac.principal.update",
                state=state,
                request_id=request_id,
            )
            return state

        state = await session.run_sync(mutation)
    except ValueError as exc:
        raise _map_error(exc) from exc
    return _response(state)
