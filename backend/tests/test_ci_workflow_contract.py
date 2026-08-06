from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
OBSERVER_WORKFLOW = ROOT / ".github" / "workflows" / "ci-observer.yml"
REQUIRED_TRIGGERS = {"workflow_dispatch", "push", "pull_request"}
REQUIRED_JOBS = {
    "workflow-contracts",
    "test",
    "migrations",
    "container",
    "dependency-review",
}
REQUIRED_OBSERVER_INPUTS = {
    "observed_run_id",
    "observed_conclusion",
    "observed_head_sha",
    "observed_url",
}


def _load_workflow(path: Path = WORKFLOW) -> dict[str, Any]:
    loaded = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    assert isinstance(loaded, dict), f"{path.name} must be a YAML mapping"
    return loaded


def _steps(job: dict[str, Any]) -> list[dict[str, Any]]:
    steps = job.get("steps")
    assert isinstance(steps, list), "Every release-critical job must define steps"
    return [step for step in steps if isinstance(step, dict)]


def _combined_run(job: dict[str, Any]) -> str:
    return "\n".join(str(step.get("run", "")) for step in _steps(job))


def test_ci_workflow_preserves_release_critical_structure() -> None:
    workflow = _load_workflow()

    triggers = workflow.get("on")
    assert isinstance(triggers, dict), "CI workflow must define mapping-style triggers"
    assert REQUIRED_TRIGGERS <= set(triggers), "Required CI triggers were removed"

    permissions = workflow.get("permissions")
    assert isinstance(permissions, dict)
    assert permissions.get("contents") == "read"

    jobs = workflow.get("jobs")
    assert isinstance(jobs, dict), "CI workflow must define jobs"
    assert REQUIRED_JOBS <= set(jobs), "Required release-blocking jobs were removed"


def test_workflow_contract_job_is_independently_observable() -> None:
    jobs = _load_workflow()["jobs"]
    contract_job = jobs["workflow-contracts"]
    assert isinstance(contract_job, dict)

    run_commands = _combined_run(contract_job)
    assert "pytest backend/tests/test_ci_workflow_contract.py" in run_commands
    assert "--junitxml=artifacts/workflow-contracts.xml" in run_commands
    assert "artifacts/workflow-contract-evidence.json" in run_commands
    for field in {
        "schema_version",
        "workflow",
        "run_id",
        "run_attempt",
        "head_sha",
        "repository",
        "event_name",
        "conclusion",
        "run_url",
    }:
        assert f'"{field}"' in run_commands
    assert "GITHUB_RUN_ID" in run_commands
    assert "GITHUB_RUN_ATTEMPT" in run_commands
    assert "GITHUB_SHA" in run_commands
    assert "GITHUB_REPOSITORY" in run_commands

    upload_steps = [
        step
        for step in _steps(contract_job)
        if str(step.get("uses", "")) == "actions/upload-artifact@v4"
    ]
    assert upload_steps, "Workflow contract evidence must be uploaded"
    upload_with = upload_steps[0].get("with")
    assert isinstance(upload_with, dict)
    assert upload_with.get("name") == "workflow-contract-evidence"
    upload_path = str(upload_with.get("path", ""))
    assert "artifacts/workflow-contracts.xml" in upload_path
    assert "artifacts/workflow-contract-evidence.json" in upload_path
    assert upload_steps[0].get("if") == "always()"


def test_ci_observer_preserves_independent_execution_evidence() -> None:
    observer = _load_workflow(OBSERVER_WORKFLOW)
    assert observer.get("name") == "RC4 CI Observer"

    triggers = observer.get("on")
    assert isinstance(triggers, dict)
    workflow_dispatch = triggers.get("workflow_dispatch")
    assert isinstance(workflow_dispatch, dict)
    inputs = workflow_dispatch.get("inputs")
    assert isinstance(inputs, dict)
    assert REQUIRED_OBSERVER_INPUTS <= set(inputs)
    for input_name in REQUIRED_OBSERVER_INPUTS:
        input_contract = inputs[input_name]
        assert isinstance(input_contract, dict)
        assert input_contract.get("required") == "true"

    workflow_run = triggers.get("workflow_run")
    assert isinstance(workflow_run, dict)
    assert workflow_run.get("workflows") == ["RC4 Quality Gate"]
    assert workflow_run.get("types") == ["completed"]

    permissions = observer.get("permissions")
    assert isinstance(permissions, dict)
    assert permissions.get("actions") == "read"
    assert permissions.get("contents") == "read"

    jobs = observer.get("jobs")
    assert isinstance(jobs, dict)
    observe = jobs.get("observe")
    assert isinstance(observe, dict)
    commands = _combined_run(observe)
    assert "set -euo pipefail" in commands
    assert "artifacts/ci-observation.json" in commands
    assert "schema_version" in commands
    assert "observed_workflow" in commands
    assert "GITHUB_STEP_SUMMARY" in commands
    assert "actions/runs/[0-9]+" in commands
    assert "[0-9a-fA-F]{40}" in commands

    upload = next(
        step for step in _steps(observe) if step.get("uses") == "actions/upload-artifact@v4"
    )
    upload_with = upload.get("with")
    assert isinstance(upload_with, dict)
    assert upload_with.get("name") == "ci-observation-evidence"
    assert upload_with.get("path") == "artifacts/ci-observation.json"
    assert upload_with.get("if-no-files-found") == "error"
    assert upload.get("if") == "always()"


def test_release_jobs_preserve_blocking_commands_and_services() -> None:
    jobs = _load_workflow()["jobs"]

    test_job = jobs["test"]
    test_commands = _combined_run(test_job)
    assert "ruff check backend database" in test_commands
    assert "mypy backend/dtmo" in test_commands
    assert "pytest" in test_commands
    assert "--cov=dtmo" in test_commands
    assert "--cov-report=xml:artifacts/coverage.xml" in test_commands
    assert "--cov-fail-under=80" in test_commands
    assert "--junitxml=artifacts/tests.xml" in test_commands
    test_upload = next(
        step for step in _steps(test_job) if step.get("uses") == "actions/upload-artifact@v4"
    )
    test_upload_with = test_upload.get("with")
    assert isinstance(test_upload_with, dict)
    assert test_upload_with.get("name") == "test-evidence"
    test_upload_path = str(test_upload_with.get("path", ""))
    assert "artifacts/tests.xml" in test_upload_path
    assert "artifacts/coverage.xml" in test_upload_path
    assert test_upload.get("if") == "always()"

    migrations = jobs["migrations"]
    assert isinstance(migrations.get("services"), dict)
    assert "postgres" in migrations["services"]
    migration_commands = _combined_run(migrations)
    assert "alembic upgrade head" in migration_commands
    assert "alembic downgrade base" in migration_commands

    container_commands = _combined_run(jobs["container"])
    assert "docker build -t dtmo:rc4 ." in container_commands
    assert "set -euo pipefail" in container_commands
    assert "docker logs dtmo" in container_commands
    assert "docker rm -f dtmo" in container_commands
    assert "curl -fsS http://127.0.0.1:8000/health" in container_commands
    assert "curl -fsS http://127.0.0.1:8000/openapi.json" in container_commands
    assert "human-approval-required" in container_commands

    dependency_review = jobs["dependency-review"]
    assert "if" not in dependency_review
    audit_commands = _combined_run(dependency_review)
    assert "pip-audit --format=json" in audit_commands
    assert "artifacts/pip-audit.json" in audit_commands
    upload = next(
        step
        for step in _steps(dependency_review)
        if step.get("uses") == "actions/upload-artifact@v4"
    )
    upload_with = upload.get("with")
    assert isinstance(upload_with, dict)
    assert upload_with.get("name") == "dependency-audit-evidence"
    assert upload_with.get("path") == "artifacts/pip-audit.json"
    assert upload_with.get("if-no-files-found") == "error"
    assert upload.get("if") == "always()"
