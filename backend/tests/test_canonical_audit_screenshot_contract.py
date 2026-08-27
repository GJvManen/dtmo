from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "tools/capture_canonical_audit_screenshot.py"
WORKFLOW = ROOT / ".github/workflows/canonical-audit-screenshot.yml"
RUN_RECORD = ROOT / "docs/development/runs/RUN-20260827-377.md"


def test_audit_capture_uses_canonical_route_and_read_only_journey():
    text = CAPTURE.read_text(encoding="utf-8")
    assert 'AUDIT_ROUTE = "/workbench/administration"' in text
    assert 'name="Security & audit"' in text
    assert 'data-admin-security="audit-evidence"' in text
    assert '"read_only": True' in text
    assert '"fixture_backed": True' in text
    assert '"audit_read_only": True' in text
    assert '"audit_fixture_rendered": True' in text
    assert '"request_id_correlation_rendered": True' in text
    assert '"mutation_executed": False' in text
    assert '"token_revocation_executed": False' in text
    assert '"production_activity_proven": False' in text
    assert '"review_authority_proven": False' in text
    assert '"share_authority_proven": False' in text
    assert '"publication_authority_proven": False' in text
    assert 'page.goto(base_url.rstrip("/") + AUDIT_ROUTE' in text
    assert '"/ui/auditor"' not in text
    assert "share.review" in text
    assert "misp.export.prepare" in text
    assert "rbac.role.update" in text
    assert "req-docs-review-001" in text


def test_ui10_gate_is_exact_head_and_fail_closed():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "github.event.pull_request.head.sha || github.sha" in workflow
    assert "Verify exact-head checkout" in workflow
    assert "capture_canonical_audit_screenshot.py" in workflow
    assert "audit-correlation-workbench.png" in workflow
    assert 'metadata.get("canonical_route") != "/workbench/administration"' in workflow
    assert 'metadata.get("audit_read_only") is not True' in workflow
    assert 'metadata.get("audit_fixture_rendered") is not True' in workflow
    assert 'metadata.get("request_id_correlation_rendered") is not True' in workflow
    assert 'metadata.get("mutation_executed") is not False' in workflow
    assert 'metadata.get("token_revocation_executed") is not False' in workflow
    assert '"production_activity_proven", "owner_acceptance_proven", "production_equivalent_proven", "independent_assurance_proven"' in workflow
    assert '"review_authority_proven", "share_authority_proven", "publication_authority_proven"' in workflow


def test_ui10_run_record_keeps_candidate_unpromoted_until_review():
    text = RUN_RECORD.read_text(encoding="utf-8")
    assert "audit-correlation-workbench.png" in text
    assert "/workbench/administration" in text
    assert "must not replace `audit-correlation.png`" in text
    assert "documentation illustration only" in text
    assert "read-only append-only audit evidence" in text
    assert "does not prove production activity" in text
    assert "does not grant review, sharing or publication authority" in text
