from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


def _request(url: str, *, method: str = "GET") -> tuple[int, dict[str, str], bytes]:
    request = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(request, timeout=5) as response:  # noqa: S310 - bounded loopback CI probe
        return response.status, {k.lower(): v for k, v in response.headers.items()}, response.read()


def _json(url: str, *, method: str = "GET") -> tuple[int, dict[str, str], Any]:
    status, headers, body = _request(url, method=method)
    return status, headers, json.loads(body.decode("utf-8"))


def _wait_for_health(base_url: str, timeout_seconds: int = 60) -> None:
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            status, _, payload = _json(f"{base_url}/health")
            if status == 200 and payload.get("status") == "healthy":
                return
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            last_error = exc
        time.sleep(1)
    raise RuntimeError(f"runtime health probe did not become ready: {last_error}")


def _write_junit(path: Path, results: list[tuple[str, str | None]]) -> None:
    failures = sum(message is not None for _, message in results)
    suite = ET.Element("testsuite", name="phase8-staging-emulator-runtime", tests=str(len(results)), failures=str(failures), errors="0", skipped="0")
    for name, message in results:
        case = ET.SubElement(suite, "testcase", classname="staging_emulator_runtime", name=name)
        if message is not None:
            failure = ET.SubElement(case, "failure", message=message)
            failure.text = message
    tree = ET.ElementTree(ET.Element("testsuites"))
    tree.getroot().append(suite)
    ET.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:18000")
    parser.add_argument("--output-dir", default="artifacts")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[tuple[str, str | None]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        results.append((name, None if condition else detail))

    try:
        _wait_for_health(args.base_url)
        status, headers, health = _json(f"{args.base_url}/health")
        check("health_status", status == 200 and health.get("status") == "healthy", f"unexpected health response: {status} {health}")
        check("production_mode", health.get("environment") == "production", f"environment={health.get('environment')!r}")
        check("human_publication_gate", health.get("publication_gate") == "human-approval-required", f"publication_gate={health.get('publication_gate')!r}")
        check("authentication_contract", health.get("authentication") == "api-key-and-rbac", f"authentication={health.get('authentication')!r}")
        check("security_header_nosniff", headers.get("x-content-type-options") == "nosniff", "missing X-Content-Type-Options")
        check("security_header_frame_deny", headers.get("x-frame-options") == "DENY", "missing X-Frame-Options DENY")
        check("security_header_referrer", headers.get("referrer-policy") == "no-referrer", "missing Referrer-Policy")
        check("correlation_header", bool(headers.get("x-correlation-id")), "missing correlation header")

        ready_status, _, ready = _json(f"{args.base_url}/ready")
        check("ready_status", ready_status == 200 and ready.get("status") == "ready", f"unexpected ready response: {ready_status} {ready}")

        connectors_status, _, connectors = _json(f"{args.base_url}/connectors")
        connector_disabled = connectors_status == 200 and isinstance(connectors, list) and bool(connectors) and connectors[0].get("enabled") is False
        check("live_connectors_default_off", connector_disabled, f"unexpected connector inventory: {connectors}")

        run_status, _, run_result = _json(f"{args.base_url}/connectors/cisa-kev/run", method="POST")
        check("connector_run_fail_closed", run_status == 200 and run_result.get("status") == "disabled", f"unexpected connector run response: {run_status} {run_result}")

        metrics_status, _, metrics_body = _request(f"{args.base_url}/metrics")
        metrics_text = metrics_body.decode("utf-8")
        check("metrics_available", metrics_status == 200 and "dtmo_http_requests_total" in metrics_text, "expected HTTP request metrics not found")
    except Exception as exc:  # noqa: BLE001 - evidence writer must report probe failure
        results.append(("runtime_probe", str(exc)))

    _write_junit(output_dir / "phase8-staging-emulator-runtime.xml", results)
    failures = [name for name, message in results if message is not None]
    report = {
        "decision": "pass" if not failures else "fail",
        "objective": "Phase 8 staging emulator production-mode container runtime smoke",
        "checks": {name: message is None for name, message in results},
        "failed_checks": failures,
        "claim_boundary": {
            "full_dependency_topology_executed": False,
            "real_staging_environment_proven": False,
            "deployment_parity_proven": False,
            "ten_external_evidence_classes_satisfied": False,
            "phase_8_complete": False,
            "production_acceptance_complete": False,
        },
    }
    (output_dir / "phase8-staging-emulator-runtime.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
