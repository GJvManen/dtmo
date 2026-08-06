from pathlib import Path

import pytest
import yaml

from tools.check_ci_execution_readiness import PreflightError, assess


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    workflows = tmp_path / ".github/workflows"
    workflows.mkdir(parents=True)
    tools = tmp_path / "tools"
    tools.mkdir()
    (workflows / "ci.yml").write_text(
        yaml.safe_dump(
            {
                "name": "RC4 Quality Gate",
                "on": {"push": {}, "pull_request": {}, "workflow_dispatch": {}},
                "jobs": {"workflow-contracts": {"runs-on": "ubuntu-latest"}},
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    (workflows / "ci-observer.yml").write_text(
        yaml.safe_dump(
            {
                "name": "RC4 CI Observer",
                "on": {"workflow_run": {"workflows": ["RC4 Quality Gate"]}},
                "jobs": {"observe": {"runs-on": "ubuntu-latest"}},
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    (tools / "verify_ci_evidence.py").write_text("# verifier\n", encoding="utf-8")
    return tmp_path


def test_assess_reports_repository_ready_but_not_gate_eligible(repository: Path) -> None:
    report = assess(repository)
    assert report["ready"] is True
    assert report["release_gate_eligible"] is False
    assert len(report["required_external_evidence"]) == 5
    assert "not proof" in report["statement"]


def test_assess_rejects_missing_manual_trigger(repository: Path) -> None:
    workflow_path = repository / ".github/workflows/ci.yml"
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    triggers = workflow.get("on", workflow.get(True))
    triggers.pop("workflow_dispatch")
    workflow_path.write_text(yaml.safe_dump(workflow, sort_keys=False), encoding="utf-8")

    with pytest.raises(PreflightError, match="workflow_dispatch"):
        assess(repository)


def test_assess_rejects_observer_bound_to_wrong_workflow(repository: Path) -> None:
    observer_path = repository / ".github/workflows/ci-observer.yml"
    observer = yaml.safe_load(observer_path.read_text(encoding="utf-8"))
    triggers = observer.get("on", observer.get(True))
    triggers["workflow_run"]["workflows"] = ["Different Workflow"]
    observer_path.write_text(yaml.safe_dump(observer, sort_keys=False), encoding="utf-8")

    with pytest.raises(PreflightError, match="not bound"):
        assess(repository)


def test_assess_rejects_missing_evidence_verifier(repository: Path) -> None:
    (repository / "tools/verify_ci_evidence.py").unlink()

    with pytest.raises(PreflightError, match="verifier is missing"):
        assess(repository)
