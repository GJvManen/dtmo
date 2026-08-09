from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from prometheus_client import generate_latest

from dtmo.alerts import StorageIntegrityAlertManager
from dtmo.lake.service import IntelligenceLake
from dtmo.logging import configure_logging


class MemoryObjectStore:
    def __init__(self) -> None:
        self.objects: dict[tuple[str, str], bytes] = {}

    async def put_bytes(self, bucket: str, key: str, data: bytes, content_type: str) -> None:
        del content_type
        self.objects[(bucket, key)] = data

    async def get_bytes(self, bucket: str, key: str) -> bytes:
        return self.objects[(bucket, key)]


def _json_events(caplog: pytest.LogCaptureFixture) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for record in caplog.records:
        try:
            payload = json.loads(record.getMessage())
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            events.append(payload)
    return events


@pytest.mark.asyncio
async def test_lake_integrity_failure_raises_critical_correlated_alert_without_sensitive_evidence(
    caplog: pytest.LogCaptureFixture,
) -> None:
    configure_logging("INFO")
    caplog.set_level("INFO", logger="storage.alerts")
    store = MemoryObjectStore()
    lake = IntelligenceLake(store)
    manager = StorageIntegrityAlertManager()
    original = b"student-sensitive-evidence: must-not-leak"
    receipt = await lake.land("controlled-source", "record-001", original, "application/octet-stream")

    store.objects[(receipt.bucket, receipt.key)] = b"tampered-evidence"
    integrity_ok = await lake.verify(receipt)
    assert integrity_ok is False

    signal = manager.observe(
        "raw-evidence-store",
        integrity_ok=integrity_ok,
        correlation="rc10-4-integrity-failure-001",
    )

    assert signal.state == "active"
    assert signal.transitioned is True
    assert signal.integrity_ok is False
    assert signal.correlation_id == "rc10-4-integrity-failure-001"
    assert signal.publish_approved is False
    assert "restore" in signal.action

    metrics = generate_latest().decode("utf-8")
    assert 'dtmo_storage_integrity_checks_total{result="fail",storage="raw-evidence-store"} 1.0' in metrics
    assert 'dtmo_storage_integrity_alert_active{storage="raw-evidence-store"} 1.0' in metrics
    assert (
        'dtmo_storage_integrity_alert_transitions_total{storage="raw-evidence-store",transition="raised"} 1.0'
        in metrics
    )

    raised = [
        event for event in _json_events(caplog) if event.get("event") == "storage_integrity_alert_raised"
    ]
    assert raised
    event_text = json.dumps(raised[-1], sort_keys=True)
    assert raised[-1]["storage_name"] == "raw-evidence-store"
    assert raised[-1]["correlation_id"] == "rc10-4-integrity-failure-001"
    assert raised[-1]["severity"] == "critical"
    assert raised[-1]["publish_approved"] is False
    assert receipt.key not in event_text
    assert receipt.sha256 not in event_text
    assert original.decode("utf-8") not in event_text
    assert "tampered-evidence" not in event_text


@pytest.mark.asyncio
async def test_successful_reverification_clears_storage_integrity_alert(
    caplog: pytest.LogCaptureFixture,
) -> None:
    configure_logging("INFO")
    caplog.set_level("INFO", logger="storage.alerts")
    store = MemoryObjectStore()
    lake = IntelligenceLake(store)
    manager = StorageIntegrityAlertManager()
    original = b"known-good-immutable-evidence"
    receipt = await lake.land("controlled-source", "record-002", original, "application/octet-stream")

    store.objects[(receipt.bucket, receipt.key)] = b"corrupted"
    assert await lake.verify(receipt) is False
    raised = manager.observe(
        "raw-evidence-recovery",
        integrity_ok=False,
        correlation="rc10-4-failure-002",
    )

    store.objects[(receipt.bucket, receipt.key)] = original
    integrity_ok = await lake.verify(receipt)
    assert integrity_ok is True
    cleared = manager.observe(
        "raw-evidence-recovery",
        integrity_ok=integrity_ok,
        correlation="rc10-4-recovery-002",
    )

    assert raised.state == "active" and raised.transitioned is True
    assert cleared.state == "clear" and cleared.transitioned is True
    assert cleared.correlation_id == "rc10-4-recovery-002"
    assert cleared.publish_approved is False

    metrics = generate_latest().decode("utf-8")
    assert 'dtmo_storage_integrity_alert_active{storage="raw-evidence-recovery"} 0.0' in metrics
    assert (
        'dtmo_storage_integrity_alert_transitions_total{storage="raw-evidence-recovery",transition="raised"} 1.0'
        in metrics
    )
    assert (
        'dtmo_storage_integrity_alert_transitions_total{storage="raw-evidence-recovery",transition="cleared"} 1.0'
        in metrics
    )

    cleared_events = [
        event for event in _json_events(caplog) if event.get("event") == "storage_integrity_alert_cleared"
    ]
    assert cleared_events
    assert cleared_events[-1]["correlation_id"] == "rc10-4-recovery-002"
    assert cleared_events[-1]["publish_approved"] is False


def test_repeated_integrity_failure_does_not_repeat_raise_transition() -> None:
    manager = StorageIntegrityAlertManager()
    storage_name = "raw-evidence-no-storm"

    first = manager.observe(storage_name, integrity_ok=False, correlation="rc10-4-first-003")
    second = manager.observe(storage_name, integrity_ok=False, correlation="rc10-4-second-003")

    assert first.state == second.state == "active"
    assert first.transitioned is True
    assert second.transitioned is False


def test_storage_integrity_rejects_unbounded_storage_identifier() -> None:
    manager = StorageIntegrityAlertManager()
    with pytest.raises(ValueError, match="bounded operational storage identifier"):
        manager.observe("storage name with spaces", integrity_ok=False)


def test_storage_integrity_prometheus_rule_is_critical_actionable_and_recoverable() -> None:
    contract = yaml.safe_load(Path("ops/prometheus/dtmo-alerts.yml").read_text(encoding="utf-8"))
    storage_group = next(group for group in contract["groups"] if group["name"] == "dtmo.storage.alerts")
    rule = storage_group["rules"][0]

    assert rule["alert"] == "DTMOStorageIntegrityFailure"
    assert rule["expr"] == "dtmo_storage_integrity_alert_active == 1"
    assert rule["labels"]["severity"] == "critical"
    assert "verify checksum and size receipts" in rule["annotations"]["action"]
    assert "known-good immutable evidence" in rule["annotations"]["action"]
    assert "subsequent successful integrity verification" in rule["annotations"]["clear_condition"]
