from pathlib import Path

import yaml


WORKFLOW = Path(".github/workflows/connector-state.yml")


def _workflow() -> dict[str, object]:
    loaded = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    if True in loaded and "on" not in loaded:
        loaded["on"] = loaded.pop(True)
    return loaded


def test_connector_state_gate_is_observable_and_fail_closed() -> None:
    jobs = _workflow()["jobs"]
    assert isinstance(jobs, dict)
    state_job = jobs["connector-state"]
    gate_job = jobs["connector-state-gate"]
    assert isinstance(state_job, dict) and isinstance(gate_job, dict)
    commands = "\n".join(
        str(step.get("run", "")) for step in state_job["steps"] if isinstance(step, dict)
    )
    assert "python -m alembic upgrade head" in commands
    assert "test_rc7_connector_state.py" in commands
    assert '"publish_approved": recovered.publish_approved' in commands
    assert 'evidence["decision"] != "pass"' in commands
    upload = next(
        step for step in state_job["steps"]
        if isinstance(step, dict) and "upload-artifact" in str(step.get("uses", ""))
    )
    assert upload["with"]["name"] == "connector-state-evidence"
    assert upload["with"]["if-no-files-found"] == "error"
    assert gate_job["if"] == "always()"
    assert gate_job["needs"] == ["connector-state"]
