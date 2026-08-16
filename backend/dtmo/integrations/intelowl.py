from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any

import httpx

from dtmo.config import Settings


TERMINAL_STATES = {"finished", "completed", "failed", "killed", "timeout"}
EXTERNAL_RESTRICTED_HANDLING = {"red", "tlp:red", "review-required"}


@dataclass(slots=True)
class IntelOwlEnrichmentResult:
    canonical_id: str
    observable_type: str
    observable_value: str
    job_id: str
    status: str
    reports: list[dict[str, Any]]
    partial: bool
    raw: dict[str, Any]


class IntelOwlPolicyError(ValueError):
    pass


class IntelOwlAdapter:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _headers(self) -> dict[str, str]:
        token = self.settings.intelowl_api_token.get_secret_value().strip()
        if not token:
            raise IntelOwlPolicyError("IntelOwl API token is required")
        return {"Authorization": f"Token {token}", "Accept": "application/json"}

    @staticmethod
    def _csv(value: str) -> set[str]:
        return {part.strip().lower() for part in value.split(",") if part.strip()}

    def _validate_request(
        self,
        *,
        observable_type: str,
        observable_value: str,
        handling: str,
        analyzers: list[str],
        external_analyzers: set[str] | None = None,
    ) -> None:
        kind = observable_type.strip().lower()
        if kind not in self._csv(self.settings.intelowl_allowed_observable_types):
            raise IntelOwlPolicyError(f"observable type is not approved: {kind}")
        if not observable_value.strip() or len(observable_value) > 8192:
            raise IntelOwlPolicyError("observable value is empty or oversized")
        approved = self._csv(self.settings.intelowl_allowed_analyzers)
        requested = {name.strip().lower() for name in analyzers if name.strip()}
        if not requested or not requested.issubset(approved):
            raise IntelOwlPolicyError("analyzer request is outside the explicit allowlist")
        if kind in {"email", "mail"}:
            raise IntelOwlPolicyError("personal-data observable enrichment is not approved")
        external = {name.lower() for name in (external_analyzers or set())}
        if handling.strip().lower() in EXTERNAL_RESTRICTED_HANDLING and requested.intersection(external):
            raise IntelOwlPolicyError("handling policy forbids external analyzer disclosure")

    @staticmethod
    def _job_id(payload: Any) -> str:
        if not isinstance(payload, dict):
            raise IntelOwlPolicyError("IntelOwl submission response must be an object")
        value = payload.get("job_id", payload.get("id"))
        if not isinstance(value, (str, int)) or not str(value).strip():
            raise IntelOwlPolicyError("IntelOwl submission response has no job id")
        return str(value).strip()

    def _normalize_job(
        self,
        *,
        canonical_id: str,
        observable_type: str,
        observable_value: str,
        expected_job_id: str,
        payload: Any,
        analyzers: list[str],
    ) -> IntelOwlEnrichmentResult:
        if not isinstance(payload, dict):
            raise IntelOwlPolicyError("IntelOwl job response must be an object")
        encoded = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        if len(encoded) > self.settings.intelowl_max_result_bytes:
            raise IntelOwlPolicyError("IntelOwl result exceeds configured size limit")
        actual_job_id = self._job_id(payload)
        if actual_job_id != expected_job_id:
            raise IntelOwlPolicyError("IntelOwl job identity mismatch")
        status = str(payload.get("status", "")).strip().lower()
        reports_raw = payload.get("reports", payload.get("analyzer_reports", []))
        if not isinstance(reports_raw, list):
            raise IntelOwlPolicyError("IntelOwl analyzer reports must be a list")
        approved = self._csv(self.settings.intelowl_allowed_analyzers)
        reports: list[dict[str, Any]] = []
        failures = 0
        for report in reports_raw:
            if not isinstance(report, dict):
                raise IntelOwlPolicyError("IntelOwl analyzer report must be an object")
            analyzer = str(report.get("analyzer_name", report.get("name", ""))).strip()
            if not analyzer or analyzer.lower() not in approved:
                raise IntelOwlPolicyError("IntelOwl returned an unknown analyzer")
            item = dict(report)
            item["analyzer_name"] = analyzer
            item["external_share_authorized"] = False
            item["local_compromise_proven"] = False
            if str(report.get("status", "")).lower() in {"failed", "error", "killed"}:
                failures += 1
            reports.append(item)
        requested = {name.strip().lower() for name in analyzers if name.strip()}
        returned = {str(item["analyzer_name"]).lower() for item in reports}
        partial = failures > 0 or (status in {"finished", "completed"} and returned != requested)
        raw = dict(payload)
        raw["_dtmo_intelowl"] = {
            "canonical_id": canonical_id,
            "job_id": expected_job_id,
            "read_only_result_import": True,
            "external_share_authorized": False,
            "local_compromise_proven": False,
        }
        return IntelOwlEnrichmentResult(
            canonical_id=canonical_id,
            observable_type=observable_type,
            observable_value=observable_value,
            job_id=expected_job_id,
            status=status,
            reports=reports,
            partial=partial,
            raw=raw,
        )

    async def enrich(
        self,
        client: httpx.AsyncClient,
        *,
        canonical_id: str,
        observable_type: str,
        observable_value: str,
        handling: str,
        analyzers: list[str],
        external_analyzers: set[str] | None = None,
    ) -> IntelOwlEnrichmentResult:
        self._validate_request(
            observable_type=observable_type,
            observable_value=observable_value,
            handling=handling,
            analyzers=analyzers,
            external_analyzers=external_analyzers,
        )
        base = self.settings.intelowl_api_base.rstrip("/")
        if not base:
            raise IntelOwlPolicyError("IntelOwl API base is required")
        headers = self._headers()
        response = await client.post(
            f"{base}/api/analyze_observable",
            headers=headers,
            json={
                "observable_name": observable_value,
                "observable_classification": observable_type,
                "analyzers_requested": analyzers,
                "connectors_requested": [],
            },
        )
        response.raise_for_status()
        job_id = self._job_id(response.json())
        last_payload: Any = None
        for attempt in range(self.settings.intelowl_max_poll_attempts):
            result = await client.get(f"{base}/api/jobs/{job_id}", headers=headers)
            result.raise_for_status()
            last_payload = result.json()
            status = str(last_payload.get("status", "")).strip().lower() if isinstance(last_payload, dict) else ""
            if status in TERMINAL_STATES:
                return self._normalize_job(
                    canonical_id=canonical_id,
                    observable_type=observable_type,
                    observable_value=observable_value,
                    expected_job_id=job_id,
                    payload=last_payload,
                    analyzers=analyzers,
                )
            if attempt + 1 < self.settings.intelowl_max_poll_attempts:
                await asyncio.sleep(self.settings.intelowl_poll_interval_seconds)
        raise IntelOwlPolicyError("IntelOwl job polling exceeded configured bound")
