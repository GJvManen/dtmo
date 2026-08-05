from __future__ import annotations

from typing import Any

import httpx

from dtmo.connectors.base import Connector, ConnectorRecord


class CisaKevConnector(Connector):
    id = "cisa-kev"
    reliability = "authoritative"
    url = (
        "https://raw.githubusercontent.com/cisagov/kev-data/"
        "develop/known_exploited_vulnerabilities.json"
    )

    async def fetch(self, client: httpx.AsyncClient) -> Any:
        response = await client.get(self.url)
        response.raise_for_status()
        return response.json()

    def parse(self, payload: Any) -> list[ConnectorRecord]:
        vulnerabilities = payload.get("vulnerabilities")
        if not isinstance(vulnerabilities, list):
            raise ValueError("CISA KEV payload has no vulnerabilities list")
        records: list[ConnectorRecord] = []
        for item in vulnerabilities:
            cve = item["cveID"]
            records.append(
                ConnectorRecord(
                    external_id=cve,
                    object_type="vulnerability",
                    title=item.get("vulnerabilityName", cve),
                    url="https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
                    summary=item.get("shortDescription", ""),
                    published_at=item.get("dateAdded"),
                    source_reliability=self.reliability,
                    confidence=98,
                    raw=item,
                )
            )
        return records
