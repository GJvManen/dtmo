from __future__ import annotations

import json
import os

from playwright.sync_api import sync_playwright


BASE_URL = os.environ.get("DTMO_BROWSER_BASE_URL", "http://127.0.0.1:4173/workbench/")


def fulfill(route, payload, status: int = 200) -> None:
    route.fulfill(status=status, content_type="application/json", body=json.dumps(payload))


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()

        page.route("**/health", lambda route: fulfill(route, {
            "status": "healthy",
            "version": "phase11.10l-browser-fixture",
            "environment": "repository-browser-fixture",
            "publication_gate": "human-review-required",
            "authentication": "fixture",
        }))
        page.route("**/api/v1/ui/session", lambda route: fulfill(route, {
            "subject": "phase11-10l-auditor",
            "roles": ["auditor"],
            "permissions": ["read:intelligence"],
        }))
        page.route("**/api/v1/governance/knowledge", lambda route: fulfill(route, {
            "status": "repository_backed",
            "frameworks": [
                {"id": "normenkader-ibp", "name": "Normenkader IBP", "kind": "education-security-framework", "coverage": "mapped_partial", "coverage_label": "Expliciete partiële crosswalk", "mapping_ids": ["ID.02", "SM.07"], "note": "Explicit typed repository-backed relationships; no blanket compliance.", "provenance": ["backend/dtmo/governance_crosswalk.py"]},
                {"id": "mitre-attack", "name": "MITRE ATT&CK", "kind": "threat-behavior-taxonomy", "coverage": "mapped_partial", "coverage_label": "Expliciete contextrelaties", "mapping_ids": ["T1078", "T1087"], "note": "Explicit detection/threat-classification context only.", "provenance": ["backend/dtmo/governance_crosswalk.py"]},
                {"id": "nist-csf", "name": "NIST Cybersecurity Framework", "kind": "cybersecurity-framework", "coverage": "mapped_partial", "coverage_label": "Expliciete partiële crosswalk", "mapping_ids": ["PR.AA", "ID.RA"], "note": "Explicit partial outcome relationships.", "provenance": ["backend/dtmo/governance_crosswalk.py"]},
                {"id": "cvss", "name": "CVSS", "kind": "vulnerability-scoring-context", "coverage": "context_only", "coverage_label": "Context-only", "mapping_ids": ["CVSS:4.0"], "note": "Scoring context only.", "provenance": ["backend/dtmo/governance_crosswalk.py"]},
                {"id": "dtmo-governance", "name": "DTMO security & release governance", "kind": "internal-governance", "coverage": "mapped_internal", "coverage_label": "Repository-backed", "mapping_ids": ["identity-access"], "note": "Internal governance is repository-backed.", "provenance": ["docs/security/SECURITY_OVERVIEW.md"]},
            ],
            "mappings": [{"id": "identity-access", "title": "Identity & access control", "statement": "RBAC and least privilege remain mandatory.", "source": "docs/security/SECURITY_OVERVIEW.md", "section": "Identity and access control"}],
            "control_crosswalk": {
                "status": "explicit_partial",
                "verified_on": "2026-08-27",
                "controls": [
                    {
                        "dtmo_control_id": "DTMO-TVM-01",
                        "title": "Threat and vulnerability management",
                        "implementation_refs": ["backend/dtmo/connectors/"],
                        "mappings": [
                            {"framework_id": "normenkader-ibp", "object_type": "control", "object_id": "SM.07", "object_title": "Threat and vulnerability management", "relationship": "implements-partially", "rationale": "Explicit repository-backed relationship.", "source_url": "https://www.normenkaderibp.nl/"},
                            {"framework_id": "mitre-attack", "object_type": "technique", "object_id": "T1087", "object_title": "Account Discovery", "relationship": "detection-context", "rationale": "Threat-behavior context only.", "source_url": "https://attack.mitre.org/techniques/T1087/"},
                            {"framework_id": "cvss", "object_type": "scoring-standard", "object_id": "CVSS:4.0", "object_title": "Common Vulnerability Scoring System 4.0", "relationship": "context-only", "rationale": "Scoring context only; no compliance equivalence.", "source_url": "https://www.first.org/cvss/v4.0/"},
                        ],
                    }
                ],
                "mapping_count": 3,
                "mapping_count_by_framework": {"normenkader-ibp": 1, "mitre-attack": 1, "cvss": 1},
                "claim_boundary": "Only explicit repository-backed relationships are shown; mapping visibility does not establish compliance or authority.",
            },
            "authority_boundaries": ["Human review and external share approval remain separate authorities."],
            "claim_boundary": "External framework relationships are shown only when explicitly recorded; typed partial mappings do not constitute certification or full compliance.",
        }))

        page.goto(BASE_URL, wait_until="networkidle")
        page.get_by_role("link", name="Governance & Evidence", exact=True).click()
        page.get_by_role("heading", name="Governance & Evidence").wait_for()
        assert page.get_by_text("Mapping visibility ≠ compliance approval", exact=True).is_visible()
        assert page.get_by_text("Normenkader IBP", exact=True).is_visible()
        assert page.get_by_text("MITRE ATT&CK", exact=True).is_visible()
        assert page.get_by_text("NIST Cybersecurity Framework", exact=True).is_visible()
        assert page.get_by_text("CVSS", exact=True).is_visible()
        assert page.get_by_text("DTMO security & release governance", exact=True).is_visible()
        assert page.get_by_text("Evidence without synthetic assurance", exact=True).is_visible()
        body = page.locator("body").inner_text().lower()
        assert "no inferred crosswalks" in body
        assert "id.02" in body
        assert "t1078" in body
        assert "publication" in body
        assert "production authority" in body
        browser.close()


if __name__ == "__main__":
    main()
