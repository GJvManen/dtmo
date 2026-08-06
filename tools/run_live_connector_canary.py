from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from dtmo.connectors.canary import CanaryPolicy, parse_cisa_kev, run_live_canary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the governed DTMO live connector canary")
    parser.add_argument(
        "--source-url",
        default="https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
    )
    parser.add_argument("--output", default="artifacts/live-connector-canary-evidence.json")
    parser.add_argument("--timeout-seconds", type=float, default=15.0)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--minimum-interval-seconds", type=float, default=2.0)
    parser.add_argument("--maximum-records", type=int, default=2000)
    return parser.parse_args()


async def main_async() -> int:
    args = parse_args()
    policy = CanaryPolicy(
        connector_id="cisa-kev-canary",
        source_url=args.source_url,
        licence="US Government public domain",
        terms_url="https://www.cisa.gov/about/website-policies",
        source_reliability="authoritative",
        timeout_seconds=args.timeout_seconds,
        max_attempts=args.max_attempts,
        minimum_interval_seconds=args.minimum_interval_seconds,
        maximum_records=args.maximum_records,
    )
    evidence = await run_live_canary(policy, parse_cisa_kev)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output.read_text(encoding="utf-8"))
    return 0 if evidence.status == "completed" and evidence.records and not evidence.publish_approved else 1


def main() -> None:
    raise SystemExit(asyncio.run(main_async()))


if __name__ == "__main__":
    main()
