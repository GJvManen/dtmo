from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import httpx

from dtmo.config import Settings


TERMINAL_STATES = {"success", "failure", "deleted"}
ALLOWED_TLP = {0, 1, 2, 3}


@dataclass(slots=True)
class CortexAnalysisResult:
    canonical_id: str
    observable_type: str
    observable_value: str
    analyzer_id: str
    job_id: str
    status: str
    report: dict[str, Any]
    raw: dict[str, Any]


class CortexPolicyError(ValueError):
    pass


class CortexAdapter:
    """Bounded analyzer-only Cortex connector.

    Responders and all external side-effect actions are deliberately excluded.
    Cortex output is enrichment evidence only: it never authorizes DTMO sharing or
    proves local compromise by itself.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @staticmethod
    def _csv(value: str) -> set[str]:
        return {part.strip().lower() for part in value.split(",") if part.strip()}

    def _headers(self) -> dict[str, str]:
        token = self.settings.cortex_api_token.get_secret_value().strip()
        if not token:
            raise CortexPolicyError("Cortex API token is required")
        return {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    def _validate_request(
        self,
        *,
        observable_type: str,
        observable_value: str,
        analyzer_id: str,
        tlp: int,
    ) -> None:
        kind = observable_type.strip().lower()
        if kind not in self._csv(self.settings.cortex_allowed_observable_types):
            raise CortexPolicyError(f"observable type is not approved: {kind}")
        if not observable_value.strip() or len(observable_value) > 8192:
            raise CortexPolicyError("observable value is empty or oversized")
        if kind in {"mail", "email", "user-agent"}:
            raise CortexPolicyError("personal-data observable analysis is not approved")
        approved = self._csv(self.settings.cortex_allowed_analyzers)
        requested = analyzer_id.strip().lower()
        if not requested or requested not in approved:
            raise CortexPolicyError("analyzer request is outside the explicit allowlist")
        if tlp not in ALLOWED_TLP:
            raise CortexPolicyError("TLP must be an explicit Cortex value 0..3")

    @staticmethod
    def _job_id(payload: Any) -> str:
        if not isinstance(payload, dict):
            raise CortexPolicyError("Cortex job response must be an object")
        value = payload.get("id")
        if not isinstance(value, (str, int)) or not str(value).strip():
            raise CortexPolicyError("Cortex job response has no stable job id")
        return str(value).strip()

    def _normalize_report(
        self,
        *,
        canonical_id: str,
        observable_type: str,
        observable_value: str,
        analyzer_id: str,
        expected_job_id: str,
        payload: Any,
    ) -> CortexAnalysisResult:
        if not isinstance(payload, dict):
            raise CortexPolicyError("Cortex report response must be an object")
        encoded = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        if len(encoded) > self.settings.cortex_max_result_bytes:
            raise CortexPolicyError("Cortex result exceeds configured size limit")
        actual_job_id = self._job_id(payload)
        if actual_job_id != expected_job_id:
            raise CortexPolicyError("Cortex job identity mismatch")
        returned_analyzer = str(payload.get("analyzerId", payload.get("analyzerDefinitionId", ""))).strip()
        if returned_analyzer and returned_analyzer.lower() != analyzer_id.strip().lower():
            raise CortexPolicyError("Cortex analyzer identity mismatch")
        status = str(payload.get("status", "")).strip().lower()
        report_raw = payload.get("report", {})
        if report_raw is None:
            report_raw = {}
        if not isinstance(report_raw, dict):
            raise CortexPolicyError("Cortex analyzer report must be an object")
        report = dict(report_raw)
        report["external_share_authorized"] = False
        report["local_compromise_proven"] = False
        raw = dict(payload)
        raw["_dtmo_cortex"] = {
            "canonical_id": canonical_id,
            "job_id": expected_job_id,
            "analyzer_id": analyzer_id,
            "analyzer_only": True,
            "responders_allowed": False,
            "external_share_authorized": False,
            "local_compromise_proven": False,
        }
        return CortexAnalysisResult(
            canonical_id=canonical_id,
            observable_type=observable_type,
            observable_value=observable_value,
            analyzer_id=analyzer_id,
            job_id=expected_job_id,
            status=status,
            report=report,
            raw=raw,
        )

    async def analyze(
        self,
        client: httpx.AsyncClient,
        *,
        canonical_id: str,
        observable_type: str,
        observable_value: str,
        analyzer_id: str,
        tlp: int,
    ) -> CortexAnalysisResult:
        self._validate_request(
            observable_type=observable_type,
            observable_value=observable_value,
            analyzer_id=analyzer_id,
            tlp=tlp,
        )
        base = self.settings.cortex_api_base.rstrip("/")
        if not base:
            raise CortexPolicyError("Cortex API base is required")
        headers = self._headers()
        response = await client.post(
            f"{base}/api/analyzer/{analyzer_id}/run",
            headers={**headers, "Content-Type": "application/json"},
            json={
                "data": observable_value,
                "dataType": observable_type.strip().lower(),
                "tlp": tlp,
                "message": f"DTMO canonical item {canonical_id}",
                "parameters": {},
            },
        )
        response.raise_for_status()
        job_id = self._job_id(response.json())
        report = await client.get(
            f"{base}/api/job/{job_id}/waitreport",
            headers=headers,
            params={"atMost": f"{self.settings.cortex_wait_seconds}second"},
        )
        report.raise_for_status()
        return self._normalize_report(
            canonical_id=canonical_id,
            observable_type=observable_type,
            observable_value=observable_value,
            analyzer_id=analyzer_id,
            expected_job_id=job_id,
            payload=report.json(),
        )
