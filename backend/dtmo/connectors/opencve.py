from __future__ import annotations

from typing import Any

import httpx

from dtmo.connectors.base import Connector, ConnectorRecord
from dtmo.vulnerability_intelligence import normalize_opencve_record


class OpenCVEConnector(Connector):
    id = "opencve"
    reliability = "trusted"

    async def fetch(self, client: httpx.AsyncClient) -> Any:
        token = self.settings.opencve_api_token.get_secret_value().strip()
        if not token:
            raise ValueError("OpenCVE API token is not configured")

        base = self.settings.opencve_api_base.rstrip("/")
        next_url: str | None = f"{base}/cves?page_size={self.settings.opencve_page_size}"
        pages: list[dict[str, Any]] = []
        for _ in range(self.settings.opencve_max_pages):
            if next_url is None:
                break
            response = await client.get(
                next_url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
            )
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
                raise ValueError("OpenCVE API v2 response has no results list")
            pages.append(payload)
            raw_next = payload.get("next")
            next_url = raw_next if isinstance(raw_next, str) and raw_next.strip() else None
        return {"pages": pages}

    def parse(self, payload: Any) -> list[ConnectorRecord]:
        if not isinstance(payload, dict) or not isinstance(payload.get("pages"), list):
            raise ValueError("OpenCVE connector payload has no pages list")

        records: list[ConnectorRecord] = []
        for page in payload["pages"]:
            if not isinstance(page, dict) or not isinstance(page.get("results"), list):
                raise ValueError("OpenCVE connector page has no results list")
            for item in page["results"]:
                if not isinstance(item, dict):
                    raise ValueError("OpenCVE result is not an object")
                normalized = normalize_opencve_record(item)
                raw = dict(item)
                raw["_dtmo_vulnerability"] = normalized.to_dict()
                records.append(
                    ConnectorRecord(
                        external_id=normalized.cve_id,
                        object_type="vulnerability",
                        title=normalized.title or normalized.cve_id,
                        url=f"https://app.opencve.io/cve/{normalized.cve_id}",
                        summary=normalized.description,
                        published_at=normalized.created_at,
                        source_reliability=self.reliability,
                        confidence=92,
                        raw=raw,
                    )
                )
        return records
