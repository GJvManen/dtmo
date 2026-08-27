from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import Page, Route, async_playwright

VIEWPORT = {"width": 1440, "height": 1000}
GOVERNANCE_ROUTE = "/workbench/governance"


def session_fixture() -> dict[str, object]:
    return {
        "subject": "docs-auditor@example.test",
        "roles": ["auditor"],
        "permissions": ["read:governance"],
    }


def health_fixture() -> dict[str, object]:
    return {
        "status": "ok",
        "version": "documentation-fixture",
        "environment": "development",
        "publication_gate": "closed",
        "authentication": "documentation-fixture",
    }


def governance_fixture() -> dict[str, object]:
    return {
        "status": "ok",
        "frameworks": [
            {
                "id": "normenkader-ibp",
                "name": "Normenkader IBP",
                "kind": "education-sector security framework",
                "coverage": "partial",
                "coverage_label": "Explicit partial mapping",
                "mapping_ids": ["DTMO-TVM-01"],
                "note": "Only repository-recorded relationships are shown.",
                "provenance": ["backend/dtmo/governance_crosswalk.py"],
            },
            {
                "id": "mitre-attack",
                "name": "MITRE ATT&CK",
                "kind": "threat knowledge base",
                "coverage": "partial",
                "coverage_label": "Explicit partial mapping",
                "mapping_ids": ["DTMO-TVM-01"],
                "note": "Technique context is not compliance evidence.",
                "provenance": ["backend/dtmo/governance_crosswalk.py"],
            },
            {
                "id": "nist-csf",
                "name": "NIST CSF",
                "kind": "cybersecurity framework",
                "coverage": "partial",
                "coverage_label": "Explicit partial mapping",
                "mapping_ids": ["DTMO-TVM-01"],
                "note": "Unrecorded objects remain unmapped.",
                "provenance": ["backend/dtmo/governance_crosswalk.py"],
            },
            {
                "id": "cvss",
                "name": "CVSS",
                "kind": "vulnerability severity context",
                "coverage": "unmapped",
                "coverage_label": "Context only",
                "mapping_ids": [],
                "note": "CVSS severity does not establish control effectiveness or local exposure.",
                "provenance": ["docs/governance/FRAMEWORK_GOVERNANCE.md"],
            },
        ],
        "mappings": [
            {
                "id": "DTMO-TVM-01",
                "title": "Threat and vulnerability management evidence",
                "statement": "Repository evidence supports explicit partial governance traceability.",
                "source": "DTMO governance registry",
                "section": "Threat and vulnerability management",
            }
        ],
        "control_crosswalk": {
            "status": "ok",
            "verified_on": "2026-08-27",
            "mapping_count": 3,
            "mapping_count_by_framework": {"normenkader-ibp": 1, "mitre-attack": 1, "nist-csf": 1},
            "claim_boundary": "Mappings are repository-backed traceability only and do not prove compliance or control effectiveness.",
            "controls": [
                {
                    "dtmo_control_id": "DTMO-TVM-01",
                    "title": "Threat and vulnerability management",
                    "implementation_refs": [
                        "backend/dtmo/governance_crosswalk.py",
                        "backend/tests/test_governance_knowledge.py",
                    ],
                    "mappings": [
                        {
                            "framework_id": "normenkader-ibp",
                            "object_type": "control",
                            "object_id": "SM.07",
                            "object_title": "Threat & Vulnerability Management",
                            "relationship": "supports",
                            "rationale": "Explicit repository mapping only.",
                            "source_url": "documentation-fixture",
                        },
                        {
                            "framework_id": "mitre-attack",
                            "object_type": "technique-context",
                            "object_id": "TA0007",
                            "object_title": "Discovery",
                            "relationship": "contextualizes",
                            "rationale": "Threat context only; no control equivalence is inferred.",
                            "source_url": "documentation-fixture",
                        },
                        {
                            "framework_id": "nist-csf",
                            "object_type": "function",
                            "object_id": "ID.RA",
                            "object_title": "Risk Assessment",
                            "relationship": "supports",
                            "rationale": "Explicit repository mapping only.",
                            "source_url": "documentation-fixture",
                        },
                    ],
                }
            ],
        },
        "authority_boundaries": [
            "Governance visibility does not grant review or sharing authority.",
            "Framework mappings do not grant administration or production authority.",
            "Repository evidence is not certification or independent assurance.",
        ],
        "claim_boundary": "Repository-backed governance evidence is documentation and engineering traceability only; it does not establish compliance, certification, production readiness or independent assurance.",
    }


async def _json(route: Route, payload: object) -> None:
    await route.fulfill(status=200, content_type="application/json", body=json.dumps(payload))


async def install_routes(page: Page) -> None:
    await page.route("**/health", lambda route: _json(route, health_fixture()))
    await page.route("**/api/v1/ui/session", lambda route: _json(route, session_fixture()))
    await page.route("**/api/v1/governance/knowledge", lambda route: _json(route, governance_fixture()))


async def run(base_url: str, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(viewport=VIEWPORT)
        page = await context.new_page()
        await install_routes(page)
        await page.goto(base_url.rstrip("/") + GOVERNANCE_ROUTE, wait_until="networkidle")

        await page.get_by_role("heading", name="Governance & Evidence", exact=True).wait_for(state="visible")
        await page.get_by_role("heading", name="Explicit coverage state", exact=True).wait_for(state="visible")
        await page.get_by_text("Normenkader IBP", exact=True).wait_for(state="visible")
        await page.get_by_text("MITRE ATT&CK", exact=True).wait_for(state="visible")
        await page.get_by_text("NIST CSF", exact=True).wait_for(state="visible")
        await page.get_by_text("CVSS", exact=True).wait_for(state="visible")
        await page.get_by_text("DTMO-TVM-01 · Threat and vulnerability management", exact=True).wait_for(state="visible")
        await page.get_by_text("normenkader-ibp · SM.07", exact=False).wait_for(state="visible")
        await page.get_by_role("heading", name="Evidence without synthetic assurance", exact=True).wait_for(state="visible")

        candidate_filename = "governance-evidence-workbench.png"
        await page.screenshot(path=str(output / candidate_filename), full_page=True)

        metadata = {
            "generated_at": datetime.now(UTC).isoformat(),
            "base_url": base_url,
            "canonical_route": GOVERNANCE_ROUTE,
            "browser": "chromium/playwright",
            "viewport": VIEWPORT,
            "capture_mode": "actual-runtime-ui-with-synthetic-fixture-data",
            "evidence_classification": "documentation-illustration-only",
            "journey": "framework inventory -> explicit typed crosswalk -> repository implementation references -> claim boundary",
            "fixture_backed": True,
            "credential_value_exposed": False,
            "compliance_proven": False,
            "certification_proven": False,
            "control_effectiveness_proven": False,
            "owner_acceptance_proven": False,
            "production_equivalent_proven": False,
            "independent_assurance_proven": False,
            "review_authority_proven": False,
            "share_authority_proven": False,
            "administration_authority_proven": False,
            "production_authority_proven": False,
            "files": [candidate_filename],
        }
        (output / "canonical-governance-capture-metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        await context.close()
        await browser.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture canonical DTMO UI-08 Governance & Evidence documentation screenshot.")
    parser.add_argument("--base-url", required=True, help="Running DTMO canonical base URL")
    parser.add_argument("--output", required=True, help="Output directory for unreviewed artifacts")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asyncio.run(run(args.base_url, Path(args.output)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
