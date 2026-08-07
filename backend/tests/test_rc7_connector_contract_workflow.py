from pathlib import Path

import yaml


WORKFLOW = Path(".github/workflows/connector-contracts.yml")


def _workflow() -> dict[str, object]:
    loaded = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    if True in loaded and "on" not in loaded:
        loaded["on"] = loaded.pop(True)
    return loaded


def test_connector_contract_gate_is_observable_retained_and_fail_closed() -> None:
    workflow = _workflow()
    triggers = workflow["on"]
    assert isinstance(triggers, dict)
    assert "pull_request" in triggers
    assert "workflow_dispatch" in triggers

    permissions = workflow["permissions"]
    assert permissions == {"contents": "read"}

    jobs = workflow["jobs"]
    assert isinstance(jobs, dict)
    contract_job = jobs["connector-contracts"]
    gate_job = jobs["connector-contract-gate"]
    assert isinstance(contract_job, dict) and isinstance(gate_job, dict)

    commands = "\n".join(
        str(step.get("run", "")) for step in contract_job["steps"] if isinstance(step, dict)
    )
    assert "test_rc7_connector_contracts.py" in commands
    assert "tools/validate_connector_contracts.py" in commands
    assert "evidence['decision'] == 'pass'" in commands
    assert "evidence['publish_approved'] is False" in commands

    upload = next(
        step
        for step in contract_job["steps"]
        if isinstance(step, dict) and "upload-artifact" in str(step.get("uses", ""))
    )
    assert upload["with"]["name"] == "connector-contract-evidence"
    assert upload["with"]["if-no-files-found"] == "error"
    assert upload["with"]["retention-days"] == 30

    assert gate_job["if"] == "always()"
    assert gate_job["needs"] == ["connector-contracts"]
