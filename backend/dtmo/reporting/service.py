from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class ReportPackage:
    title: str
    generated_at: str
    audience: str
    executive_summary: str
    findings: list[dict[str, Any]]
    recommendations: list[str]
    evidence: list[dict[str, Any]]
    human_review_required: bool = True


class ReportingService:
    def build(
        self,
        *,
        title: str,
        audience: str,
        findings: list[dict[str, Any]],
        recommendations: list[str],
        evidence: list[dict[str, Any]],
    ) -> ReportPackage:
        if not evidence:
            raise ValueError("reports require evidence")
        return ReportPackage(
            title=title,
            generated_at=datetime.now(timezone.utc).isoformat(),
            audience=audience,
            executive_summary=f"{len(findings)} bevindingen vereisen beoordeling voor {audience}.",
            findings=findings,
            recommendations=recommendations,
            evidence=evidence,
        )

    def to_json(self, report: ReportPackage) -> bytes:
        return json.dumps(report.__dict__, ensure_ascii=False, indent=2).encode()

    def to_csv(self, report: ReportPackage) -> bytes:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["title", "severity", "confidence", "source_url"])
        writer.writeheader()
        for finding in report.findings:
            writer.writerow(
                {
                    "title": finding.get("title", ""),
                    "severity": finding.get("severity", ""),
                    "confidence": finding.get("confidence", ""),
                    "source_url": finding.get("source_url", ""),
                }
            )
        return output.getvalue().encode("utf-8-sig")
