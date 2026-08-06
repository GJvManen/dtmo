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
    "postgres-restore",
    "container",
    "dependency-review",
    "release-gate",
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


def _artifact_upload_steps(job: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        step
        for step in _steps(job)
        if str(step.get("uses", "")).startswith("actions/upload-artifact@")
    ]


def test_ci_workflow_preserves_release_critical_structure() -> None:
    workflow = _load_workflow()
    triggers = workflow.get("on")
    assert isinstance(triggers, dict)
    assert REQUIRED_TRIGGERS <= set(triggers)
    permissions = workflow.get("permissions")
    assert isinstance(permissions, dict)
    assert permissions.get("contents") == "read"
    jobs = workflow.get("jobs")
    assert isinstance(jobs, dict)
    assert REQUIRED_JOBS <= set(jobs)


def test_workflow_contract_job_is_independently_observable() -> None:
    jobs = _load_workflow()["jobs"]
    contract_job = jobs["workflow-contracts"]
    assert isinstance(contract_job, dict)
    commands = _combined_run(contract_job)
    assert "python -m pytest backend/tests/test_ci_workflow_contract.py" in commands
    assert "--junitxml=artifacts/workflow-contracts.xml" in commands
    assert "artifacts/workflow-contract-evidence.json" in commands
    upload_steps = _artifact_upload_steps(contract_job)
    assert upload_steps
    upload_with = upload_steps[0].get("with")
    assert isinstance(upload_with, dict)
    assert upload_with.get("name") == "workflow-contract-evidence"
    assert "artifacts" in str(upload_with.get("path", ""))
    assert upload_steps[0].get("if") == "always()"


def test_dependency_audit_is_portable_fail_closed_and_observable() -> None:
    jobs = _load_workflow()["jobs"]
    dependency_job = jobs["dependency-review"]
    assert isinstance(dependency_job, dict)
    assert dependency_job.get("if") is None
    steps = _steps(dependency_job)
    assert not any("dependency-review-action" in str(step.get("uses", "")) for step in steps)
    commands = _combined_run(dependency_job)
    assert "python -m pip_audit" in commands
    assert "--format json" in commands
    assert "--output artifacts/pip-audit.json" in commands
    assert "AUDIT_EXIT_CODE=0" in commands
    assert "AUDIT_EXIT_CODE=$?" in commands
    assert "python -m json.tool artifacts/pip-audit.json" in commands
    assert "python -m pip_audit || true" in commands
    assert 'exit "$AUDIT_EXIT_CODE"' in commands
    assert "test -s artifacts/pip-audit.json" in commands
    upload = _artifact_upload_steps(dependency_job)[0]
    upload_with = upload.get("with")
    assert isinstance(upload_with, dict)
    assert upload_with.get("name") == "dependency-audit-evidence"
    assert upload_with.get("path") == "artifacts/pip-audit.json"
    assert upload_with.get("if-no-files-found") == "error"
    assert upload.get("if") == "always()"


def test_postgres_restore_is_clean_release_blocking_and_observable() -> None:
    jobs = _load_workflow()["jobs"]
    restore_job = jobs["postgres-restore"]
    assert isinstance(restore_job, dict)
    services = restore_job.get("services")
    assert isinstance(services, dict)
    assert "postgres" in services
    commands = _combined_run(restore_job)
    assert "python -m alembic upgrade head" in commands
    assert "dropdb --if-exists" in commands
    assert "createdb" in commands
    assert "tools/verify_postgres_backup_restore.py" in commands
    assert "--source-url" in commands
    assert "--target-url" in commands
    assert "artifacts/dtmo-postgres.dump" in commands
    assert "artifacts/postgres-restore-evidence.json" in commands
    upload = _artifact_upload_steps(restore_job)[0]
    upload_with = upload.get("with")
    assert isinstance(upload_with, dict)
    assert upload_with.get("name") == "postgres-restore-evidence"
    upload_path = str(upload_with.get("path", ""))
    assert "artifacts/postgres-restore-evidence.json" in upload_path
    assert "artifacts/dtmo-postgres.dump" in upload_path
    assert upload_with.get("if-no-files-found") == "error"
    assert upload.get("if") == "always()"


def test_aggregate_release_gate_blocks_missing_or_failed_evidence() -> None:
    jobs = _load_workflow()["jobs"]
    release_gate = jobs["release-gate"]
    assert isinstance(release_gate, dict)
    assert release_gate.get("if") == "always()"
    needs = release_gate.get("needs")
    assert isinstance(needs, list)
    assert {
        "workflow-contracts",
        "test",
        "migrations",
        "postgres-restore",
        "container",
        "dependency-review",
    } <= set(needs)
    commands = _combined_run(release_gate)
    assert '"postgres-restore": os.environ["POSTGRES_RESTORE"]' in commands
    assert 'results[name] != "success"' in commands
    assert "required = set(results)" in commands
    assert '"decision": "pass" if not failures else "blocked"' in commands
    assert "artifacts/release-gate-evidence.json" in commands
    assert "GITHUB_STEP_SUMMARY" in commands
    upload = _artifact_upload_steps(release_gate)[0]
    upload_with = upload.get("with")
    assert isinstance(upload_with, dict)
    assert upload_with.get("name") == "release-gate-evidence"
    assert upload_with.get("path") == "artifacts/release-gate-evidence.json"
    assert upload_with.get("if-no-files-found") == "error"
    assert upload.get("if") == "always()"


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
    workflow_run = triggers.get("workflow_run")
    assert isinstance(workflow_run, dict)
    assert workflow_run.get("workflows") == ["RC4 Quality Gate"]
    assert workflow_run.get("types") == ["completed"]
    jobs = observer.get("jobs")
    assert isinstance(jobs, dict)
    observe = jobs.get("observe")
    assert isinstance(observe, dict)
    commands = _combined_run(observe)
    assert "artifacts/ci-observation.json" in commands
    assert "GITHUB_STEP_SUMMARY" in commands
    upload = _artifact_upload_steps(observe)[0]
    upload_with = upload.get("with")
    assert isinstance(upload_with, dict)
    assert upload_with.get("name") == "ci-observation-evidence"
    assert upload.get("if") == "always()"


def test_release_jobs_preserve_blocking_commands_and_services() -> None:
    jobs = _load_workflow()["jobs"]
    test_commands = _combined_run(jobs["test"])
    assert "python -m ruff check backend database" in test_commands
    assert "python -m mypy backend/dtmo" in test_commands
    assert "python -m pytest --cov=dtmo" in test_commands
    assert "--cov-fail-under=80" in test_commands
    migrations = jobs["migrations"]
    assert isinstance(migrations.get("services"), dict)
    assert "postgres" in migrations["services"]
    migration_commands = _combined_run(migrations)
    assert "python -m alembic upgrade head" in migration_commands
    assert "python -m alembic downgrade base" in migration_commands
    container_commands = _combined_run(jobs["container"])
    assert "docker build --progress=plain -t dtmo:rc4 ." in container_commands
    assert "curl -fsS http://127.0.0.1:8000/health" in container_commands
