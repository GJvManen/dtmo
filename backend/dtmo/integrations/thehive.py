from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx


class TheHivePolicyError(ValueError):
    """Raised when a case handoff cannot be represented safely."""


class TheHiveAmbiguousDelivery(RuntimeError):
    """Raised when case creation may have reached TheHive but no identity was confirmed."""


TLP_MAP = {
    "clear": 0,
    "white": 0,
    "green": 1,
    "amber": 2,
    "red": 3,
    "amber+strict": 4,
}
PAP_MAP = {"clear": 0, "green": 1, "amber": 2, "red": 3}
SEVERITY_MAP = {"informational": 1, "low": 1, "medium": 2, "high": 3, "critical": 4}


@dataclass(frozen=True)
class TheHiveCaseResult:
    case_id: str
    case_number: int | None
    organization: str
    raw_result: dict[str, Any]


def _bounded_text(value: str, *, field: str, maximum: int) -> str:
    normalized = " ".join(value.split())
    if not normalized:
        raise TheHivePolicyError(f"{field} is required")
    if len(normalized) > maximum:
        raise TheHivePolicyError(f"{field} exceeds {maximum} characters")
    return normalized


def build_case_payload(
    *,
    canonical_id: str,
    title: str,
    summary: str,
    severity: str,
    tlp: str,
    pap: str,
    tags: list[str],
) -> dict[str, Any]:
    """Build the minimized, deterministic TheHive case payload."""

    tlp_value = TLP_MAP.get(tlp.strip().lower())
    pap_value = PAP_MAP.get(pap.strip().lower())
    severity_value = SEVERITY_MAP.get(severity.strip().lower())
    if tlp_value is None:
        raise TheHivePolicyError("unknown TLP mapping")
    if pap_value is None:
        raise TheHivePolicyError("unknown PAP mapping")
    if severity_value is None:
        raise TheHivePolicyError("unknown severity mapping")

    safe_tags = sorted({tag.strip() for tag in tags if tag.strip() and len(tag.strip()) <= 128})[:32]
    reference = _bounded_text(canonical_id, field="canonical_id", maximum=64)
    description = _bounded_text(summary, field="summary", maximum=4000)
    return {
        "title": _bounded_text(title, field="title", maximum=512),
        "description": f"{description}\n\nDTMO canonical reference: {reference}",
        "severity": severity_value,
        "tlp": tlp_value,
        "pap": pap_value,
        "tags": safe_tags,
    }


class TheHiveCaseAdapter:
    """Minimal API-v1 adapter for human-authorized case creation only."""

    def __init__(self, *, api_base: str, api_token: str, organization: str) -> None:
        base = api_base.rstrip("/")
        if not base:
            raise TheHivePolicyError("TheHive API base is required")
        if not api_token.strip():
            raise TheHivePolicyError("TheHive API token is required")
        if not organization.strip():
            raise TheHivePolicyError("TheHive organization is required")
        self.api_base = base
        self.api_token = api_token.strip()
        self.organization = organization.strip()

    async def create_case(self, client: httpx.AsyncClient, payload: dict[str, Any]) -> TheHiveCaseResult:
        try:
            response = await client.post(
                f"{self.api_base}/api/v1/case",
                headers={"Authorization": f"Bearer {self.api_token}", "X-Organisation": self.organization},
                json=payload,
            )
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            raise TheHiveAmbiguousDelivery("TheHive case delivery is ambiguous; reconciliation required") from exc

        if response.status_code in {401, 403, 409, 423}:
            raise TheHivePolicyError("TheHive rejected case creation under the configured authority/licensing boundary")
        if response.status_code < 200 or response.status_code >= 300:
            raise httpx.HTTPStatusError("TheHive case creation failed", request=response.request, response=response)

        try:
            data = response.json()
        except ValueError as exc:
            raise TheHiveAmbiguousDelivery("TheHive returned a malformed success response; reconciliation required") from exc
        if not isinstance(data, dict):
            raise TheHiveAmbiguousDelivery("TheHive returned a malformed success response; reconciliation required")
        case_id = data.get("_id") or data.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise TheHiveAmbiguousDelivery("TheHive success response lacks stable case identity; reconciliation required")
        number = data.get("number")
        return TheHiveCaseResult(
            case_id=case_id.strip(),
            case_number=number if isinstance(number, int) else None,
            organization=self.organization,
            raw_result=data,
        )
