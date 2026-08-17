from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import httpx


TLP_LEVELS = {"white": 0, "clear": 0, "green": 1, "amber": 2, "red": 3}


class CortexPolicyError(ValueError):
    pass


@dataclass(slots=True, frozen=True)
class CortexConnectorConfig:
    api_base: str
    api_token: str
    allowed_analyzers: frozenset[str]
    allowed_observable_types: frozenset[str] = frozenset({"cve", "ip", "domain", "url", "hash"})
    max_result_bytes: int = 1_000_000


@dataclass(slots=True)
class CortexAnalyzerResult:
    canonical_id: str
    analyzer_id: str
    job_id: str
    status: str
    report: dict[str, Any]


class CortexAnalyzerConnector:
    """Bounded Cortex analyzer connector.

    This connector deliberately excludes Cortex responders and any automatic response
    authority. It submits one explicitly allowlisted analyzer job and imports only the
    resulting report as enrichment evidence.
    """

    def __init__(self, config: CortexConnectorConfig) -> None:
        self.config = config

    def _headers(self) -> dict[str, str]:
        token = self.config.api_token.strip()
        if not token:
            raise CortexPolicyError("Cortex API token is required")
        return {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    def _validate(self, *, observable_type: str, observable_value: str, analyzer_id: str, tlp: str) -> int:
        kind = observable_type.strip().lower()
        if kind not in self.config.allowed_observable_types:
            raise CortexPolicyError(f"observable type is not approved: {kind}")
        if not observable_value.strip() or len(observable_value) > 8192:
            raise CortexPolicyError("observable value is empty or oversized")
        analyzer = analyzer_id.strip()
        if not analyzer or analyzer.lower() not in {item.lower() for item in self.config.allowed_analyzers}:
            raise CortexPolicyError("analyzer request is outside the explicit allowlist")
        if kind in {"email", "mail"}:
            raise CortexPolicyError("personal-data observable analysis is not approved")
        tlp_key = tlp.strip().lower().removeprefix("tlp:")
        if tlp_key not in TLP_LEVELS:
            raise CortexPolicyError("unknown TLP value")
        return TLP_LEVELS[tlp_key]

    @staticmethod
    def _identity(payload: Any) -> str:
        if not isinstance(payload, dict):
            raise CortexPolicyError("Cortex response must be an object")
        value = payload.get("id", payload.get("jobId"))
        if not isinstance(value, (str, int)) or not str(value).strip():
            raise CortexPolicyError("Cortex response has no stable job id")
        return str(value).strip()

    async def analyze(
        self,
        client: httpx.AsyncClient,
        *,
        canonical_id: str,
        observable_type: str,
        observable_value: str,
        analyzer_id: str,
        tlp: str,
        wait: str = "30s",
    ) -> CortexAnalyzerResult:
        tlp_level = self._validate(
            observable_type=observable_type,
            observable_value=observable_value,
            analyzer_id=analyzer_id,
            tlp=tlp,
        )
        base = self.config.api_base.rstrip("/")
        if not base:
            raise CortexPolicyError("Cortex API base is required")

        response = await client.post(
            f"{base}/api/analyzer/{analyzer_id}/run",
            headers=self._headers(),
            json={"dataType": observable_type.strip().lower(), "data": observable_value, "tlp": tlp_level},
        )
        response.raise_for_status()
        job_id = self._identity(response.json())

        report_response = await client.get(
            f"{base}/api/job/{job_id}/report",
            headers=self._headers(),
            params={"atMost": wait},
        )
        report_response.raise_for_status()
        payload = report_response.json()
        if not isinstance(payload, dict):
            raise CortexPolicyError("Cortex report response must be an object")
        encoded = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        if len(encoded) > self.config.max_result_bytes:
            raise CortexPolicyError("Cortex report exceeds configured size limit")
        returned_job_id = self._identity(payload)
        if returned_job_id != job_id:
            raise CortexPolicyError("Cortex job identity mismatch")

        report = dict(payload)
        report["_dtmo_cortex"] = {
            "canonical_id": canonical_id,
            "analyzer_id": analyzer_id,
            "job_id": job_id,
            "read_only_result_import": True,
            "responder_execution_authorized": False,
            "external_share_authorized": False,
            "local_compromise_proven": False,
        }
        return CortexAnalyzerResult(
            canonical_id=canonical_id,
            analyzer_id=analyzer_id,
            job_id=job_id,
            status=str(payload.get("status", "")).strip().lower(),
            report=report,
        )
