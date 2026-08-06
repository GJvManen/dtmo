from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import pytest


MODULE_PATH = Path(__file__).parents[2] / "tools" / "verify_ci_evidence.py"
SPEC = importlib.util.spec_from_file_location("verify_ci_evidence", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
EvidenceError = MODULE.EvidenceError
verify = MODULE.verify


def _primary(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "schema_version": 1,
        "workflow": "RC4 Quality Gate",
        "run_id": "12345",
        "head_sha": "a" * 40,
        "repository": "GJvManen/dtmo",
        "conclusion": "success",
        "run_url": "https://github.com/GJvManen/dtmo/actions/runs/12345",
    }
    data.update(overrides)
    return data


def _observer(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "observed_workflow": "RC4 Quality Gate",
        "observed_run_id": "12345",
        "observed_head_sha": "a" * 40,
        "observed_conclusion": "success",
        "observed_url": "https://github.com/GJvManen/dtmo/actions/runs/12345",
    }
    data.update(overrides)
    return data


def test_verify_accepts_matching_successful_evidence() -> None:
    result = verify(_primary(), _observer())
    assert result["verified"] is True
    assert result["run_id"] == "12345"
    assert result["head_sha"] == "a" * 40


@pytest.mark.parametrize(
    ("primary_overrides", "observer_overrides", "message"),
    [
        ({"conclusion": "failure"}, {}, "did not conclude successfully"),
        ({"head_sha": "short"}, {}, "full lowercase commit SHA"),
        ({"run_url": "https://example.invalid/run/12345"}, {}, "run_url"),
        ({}, {"observed_run_id": "999"}, "run_id"),
        ({}, {"observed_head_sha": "b" * 40}, "head_sha"),
        ({}, {"observed_conclusion": "failure"}, "conclusion"),
    ],
)
def test_verify_rejects_invalid_or_mismatched_evidence(
    primary_overrides: dict[str, Any],
    observer_overrides: dict[str, Any],
    message: str,
) -> None:
    with pytest.raises(EvidenceError, match=message):
        verify(_primary(**primary_overrides), _observer(**observer_overrides))
