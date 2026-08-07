from __future__ import annotations

import argparse
import json
from pathlib import Path

from dtmo.connectors.contracts import approved_cisa_kev_contract, validate_connector_contracts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate governed DTMO connector contracts")
    parser.add_argument("--output", default="artifacts/connector-contract-evidence.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = validate_connector_contracts([approved_cisa_kev_contract()])
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output.read_text(encoding="utf-8"))
    raise SystemExit(0 if report.decision == "pass" and report.as_dict()["publish_approved"] is False else 1)


if __name__ == "__main__":
    main()
