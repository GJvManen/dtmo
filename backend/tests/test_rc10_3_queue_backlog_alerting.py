from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest
import yaml
from prometheus_client import generate_latest

from dtmo.alerts import QueueBacklogAlertManager
from dtmo.logging import configure_logging
from dtmo.performance.queue_burst import QueueBurstBudget, run_queue_burst_harness


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


def test_queue_backlog_raises_at_governed_threshold_with_correlation(
    caplog: pytest.LogCaptureFixture,
) -> None:
    configure_logging("INFO")
    caplog.set_level("INFO", logger="queue.alerts")
    manager = QueueBacklogAlertManager(raise_ratio=0.80, clear_ratio=0.50)
    queue_name = "rc10-3-ingestion-raise"

    signal = manager.observe(
        queue_name,
        depth=32,
        capacity=40,
        correlation="rc10-3-raise-001",
    )

    assert signal.state == "active"
    assert signal.transitioned is True
    assert signal.utilization_ratio == pytest.approx(0.80)
    assert signal.correlation_id == "rc10-3-raise-001"
    assert signal.publish_approved is False
    assert "downstream" in signal.action

    metrics = generate_latest().decode("utf-8")
    assert f'dtmo_queue_backlog_depth{{queue="{queue_name}"}} 32.0' in metrics
    assert f'dtmo_queue_backlog_capacity{{queue="{queue_name}"}} 40.0' in metrics
    assert f'dtmo_queue_backlog_utilization_ratio{{queue="{queue_name}"}} 0.8' in metrics
    assert f'dtmo_queue_backlog_alert_active{{queue="{queue_name}"}} 1.0' in metrics
    assert (
        f'dtmo_queue_backlog_alert_transitions_total{{queue="{queue_name}",transition="raised"}} 1.0'
        in metrics
    )

    raised = [event for event in _json_events(caplog) if event.get("event") == "queue_backlog_alert_raised"]
    assert raised
    assert raised[-1]["queue_name"] == queue_name
    assert raised[-1]["correlation_id"] == "rc10-3-raise-001"
    assert raised[-1]["raise_threshold"] == 0.8
    assert raised[-1]["clear_threshold"] == 0.5
    assert raised[-1]["publish_approved"] is False


def test_queue_backlog_hysteresis_prevents_flapping_and_clears_on_recovery(
    caplog: pytest.LogCaptureFixture,
) -> None:
    configure_logging("INFO")
    caplog.set_level("INFO", logger="queue.alerts")
    manager = QueueBacklogAlertManager(raise_ratio=0.80, clear_ratio=0.50)
    queue_name = "rc10-3-ingestion-recovery"

    raised = manager.observe(queue_name, depth=8, capacity=10, correlation="rc10-3-breach-002")
    still_active = manager.observe(queue_name, depth=6, capacity=10, correlation="rc10-3-hold-002")
    cleared = manager.observe(queue_name, depth=5, capacity=10, correlation="rc10-3-clear-002")

    assert raised.state == "active" and raised.transitioned is True
    assert still_active.state == "active" and still_active.transitioned is False
    assert cleared.state == "clear" and cleared.transitioned is True
    assert cleared.correlation_id == "rc10-3-clear-002"
    assert cleared.publish_approved is False

    metrics = generate_latest().decode("utf-8")
    assert f'dtmo_queue_backlog_alert_active{{queue="{queue_name}"}} 0.0' in metrics
    assert (
        f'dtmo_queue_backlog_alert_transitions_total{{queue="{queue_name}",transition="raised"}} 1.0'
        in metrics
    )
    assert (
        f'dtmo_queue_backlog_alert_transitions_total{{queue="{queue_name}",transition="cleared"}} 1.0'
        in metrics
    )

    events = _json_events(caplog)
    active_events = [event for event in events if event.get("event") == "queue_backlog_alert_active"]
    clear_events = [event for event in events if event.get("event") == "queue_backlog_alert_cleared"]
    assert len(active_events) == 1
    assert clear_events
    assert clear_events[-1]["correlation_id"] == "rc10-3-clear-002"


def test_accepted_rc8_queue_pressure_result_drives_breach_and_clear_contract() -> None:
    budget = QueueBurstBudget(250, 4, 10, 0, 0)
    result = asyncio.run(
        run_queue_burst_harness(
            budget=budget,
            duration_seconds=0.2,
            consumer_records_per_second=20,
            queue_capacity=4,
        )
    )
    assert result.decision == "pass"
    assert result.backpressure_events > 0
    assert result.max_queue_depth == result.queue_capacity

    manager = QueueBacklogAlertManager(raise_ratio=0.80, clear_ratio=0.50)
    breached = manager.observe(
        "rc10-3-rc8-pressure",
        depth=result.max_queue_depth,
        capacity=result.queue_capacity,
        correlation="rc10-3-rc8-breach",
    )
    recovered = manager.observe(
        "rc10-3-rc8-pressure",
        depth=0,
        capacity=result.queue_capacity,
        correlation="rc10-3-rc8-recovery",
    )

    assert breached.state == "active"
    assert breached.transitioned is True
    assert recovered.state == "clear"
    assert recovered.transitioned is True
    assert result.data_loss_records == 0
    assert result.duplicate_candidate_records == 0
    assert result.publication_state_preserved is True


def test_queue_backlog_rejects_invalid_thresholds_and_measurements() -> None:
    with pytest.raises(ValueError, match="0 <= clear < raise <= 1"):
        QueueBacklogAlertManager(raise_ratio=0.5, clear_ratio=0.5)

    manager = QueueBacklogAlertManager()
    with pytest.raises(ValueError, match="bounded operational queue identifier"):
        manager.observe("queue name with spaces", depth=1, capacity=10)
    with pytest.raises(ValueError, match="capacity must be positive"):
        manager.observe("valid-queue", depth=0, capacity=0)
    with pytest.raises(ValueError, match="between zero and capacity"):
        manager.observe("valid-queue", depth=11, capacity=10)


def test_queue_backlog_prometheus_rule_encodes_action_and_recovery_policy() -> None:
    contract = yaml.safe_load(Path("ops/prometheus/dtmo-alerts.yml").read_text(encoding="utf-8"))
    queue_group = next(group for group in contract["groups"] if group["name"] == "dtmo.queue.alerts")
    rule = queue_group["rules"][0]

    assert rule["alert"] == "DTMOQueueBacklog"
    assert rule["expr"] == "dtmo_queue_backlog_alert_active == 1"
    assert rule["labels"]["severity"] == "warning"
    assert ">=80%" in rule["annotations"]["threshold_policy"]
    assert "<=50%" in rule["annotations"]["threshold_policy"]
    assert "Inspect consumers" in rule["annotations"]["action"]
    assert "50% capacity or lower" in rule["annotations"]["clear_condition"]
