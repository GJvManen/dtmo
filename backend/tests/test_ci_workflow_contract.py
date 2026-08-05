from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


WORKFLOW = Path(__file__).parents[2] / ".github" / "workflows" / "ci.yml"
REQUIRED_TRIGGERS = {"workflow_dispatch", "push", "pull_request"}
REQUIRED_JOBS = {
    "workflow-contracts",
    "test",
    "migrations",
    "container",
    "dependency-review",
}


def _load_workflow() -> dict[str, Any]:
    loaded = yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    assert isinstance(loaded, dict), "CI workflow must be a YAML mapping"
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

    uses = [str(step.get("uses", "")) for step in _steps(contract_job)]
    assert "actions/upload-artifact@v4" in uses

    upload_steps = [
        step
        for step in _steps(contract_job)
        if str(step.get("uses", "")) == "actions/upload-artifact@v4"
    ]
    assert upload_steps, "Workflow contract evidence must be uploaded"
    upload_with = upload_steps[0].get("with")
    assert isinstance(upload_with, dict)
    assert upload_with.get("name") == "workflow-contract-evidence"
    assert upload_with.get("path") == "artifacts/workflow-contracts.xml"
    assert upload_steps[0].get("if") == "always()"


def test_release_jobs_preserve_blocking_commands_and_services() -> None:
    jobs = _load_workflow()["jobs"]

    test_commands = _combined_run(jobs["test"])
    assert "ruff check backend database" in test_commands
    assert "mypy backend/dtmo" in test_commands
    assert "pytest --cov=dtmo" in test_commands
    assert "--cov-fail-under=80" in test_commands

    migrations = jobs["migrations"]
    assert isinstance(migrations.get("services"), dict)
    assert "postgres" in migrations["services"]
    migration_commands = _combined_run(migrations)
    assert "alembic upgrade head" in migration_commands
    assert "alembic downgrade base" in migration_commands

    container_commands = _combined_run(jobs["container"])
    assert "docker build -t dtmo:rc4 ." in container_commands
    assert "curl -fsS http://127.0.0.1:8000/health" in container_commands

    dependency_review = jobs["dependency-review"]
    assert dependency_review.get("if") == "github.event_name == 'pull_request'"
    review_steps = _steps(dependency_review)
    review = next(
        step for step in review_steps if step.get("uses") == "actions/dependency-review-action@v4"
    )
    review_with = review.get("with")
    assert isinstance(review_with, dict)
    assert review_with.get("fail-on-severity") == "high"
