from __future__ import annotations

from pathlib import Path


WORKFLOW = Path(__file__).parents[2] / ".github" / "workflows" / "ci.yml"


def test_ci_workflow_preserves_release_blocking_jobs_and_commands() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    required_fragments = (
        "workflow_dispatch:",
        "push:",
        "pull_request:",
        "test:",
        "migrations:",
        "container:",
        "dependency-review:",
        "ruff check backend database",
        "mypy backend/dtmo",
        "pytest --cov=dtmo",
        "--cov-fail-under=80",
        "alembic downgrade base",
        "alembic upgrade head",
        "docker build -t dtmo:rc4 .",
        "curl -fsS http://127.0.0.1:8000/health",
        "dependency-review-action@v4",
        "fail-on-severity: high",
    )

    missing = [fragment for fragment in required_fragments if fragment not in text]
    assert not missing, f"CI release-gate contract lost required fragments: {missing}"
