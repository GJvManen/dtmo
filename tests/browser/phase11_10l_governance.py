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
                {"id": "normenkader-ibp", "name": "Normenkader IBP", "kind": "education-security-framework", "coverage": "unmapped", "coverage_label": "Nog niet gemapt", "mapping_ids": [], "note": "No repository-backed control-level crosswalk.", "provenance": ["docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md"]},
                {"id": "mitre-attack", "name": "MITRE ATT&CK", "kind": "threat-behavior-taxonomy", "coverage": "unmapped", "coverage_label": "Nog niet gemapt", "mapping_ids": [], "note": "No repository-backed technique-level mapping.", "provenance": ["docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md"]},
                {"id": "cvss", "name": "CVSS", "kind": "vulnerability-scoring-context", "coverage": "context_only", "coverage_label": "Context, geen first-class score", "mapping_ids": [], "note": "Context only.", "provenance": ["backend/dtmo/api/schemas.py"]},
                {"id": "dtmo-governance", "name": "DTMO security & release governance", "kind": "internal-governance", "coverage": "mapped_internal", "coverage_label": "Repository-backed", "mapping_ids": ["identity-access"], "note": "Internal governance is repository-backed.", "provenance": ["docs/security/SECURITY_OVERVIEW.md"]},
            ],
            "mappings": [{"id": "identity-access", "title": "Identity & access control", "statement": "RBAC and least privilege remain mandatory.", "source": "docs/security/SECURITY_OVERVIEW.md", "section": "Identity and access control"}],
            "authority_boundaries": ["Human review and external share approval remain separate authorities."],
            "claim_boundary": "External framework crosswalks are never inferred.",
        }))

        page.goto(BASE_URL, wait_until="networkidle")
        page.get_by_role("link", name="Governance & Evidence", exact=True).click()
        page.get_by_role("heading", name="Governance & Evidence").wait_for()
        assert page.get_by_text("Mapping visibility ≠ compliance approval").is_visible()
        assert page.get_by_text("Normenkader IBP").is_visible()
        assert page.get_by_text("MITRE ATT&CK").is_visible()
        assert page.get_by_text("CVSS").is_visible()
        assert page.get_by_text("DTMO security & release governance").is_visible()
        assert page.get_by_text("Evidence without synthetic assurance").is_visible()
        body = page.locator("body").inner_text().lower()
        assert "no inferred crosswalks" in body
        assert "publication" in body
        assert "production authority" in body
        browser.close()


if __name__ == "__main__":
    main()
