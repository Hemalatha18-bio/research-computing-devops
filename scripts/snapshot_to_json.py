#!/usr/bin/env python3
"""Convert the generic health snapshot header to machine-readable JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_FIELDS = {"timestamp_utc", "hostname"}


def parse_snapshot(text: str) -> dict[str, str]:
    """Parse key/value metadata before the first section heading."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "research-computing-health-snapshot":
        raise ValueError("unrecognized health snapshot header")

    data: dict[str, str] = {"snapshot_type": "research-computing-health-snapshot"}

    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if not stripped or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key:
            data[key] = value

    missing = REQUIRED_FIELDS.difference(data)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"missing required snapshot fields: {missing_list}")

    return data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a research-computing health snapshot header to JSON."
    )
    parser.add_argument(
        "snapshot",
        nargs="?",
        type=Path,
        help="Snapshot file to parse. Reads stdin when omitted.",
    )
    args = parser.parse_args()

    text = args.snapshot.read_text(encoding="utf-8") if args.snapshot else sys.stdin.read()

    try:
        data = parse_snapshot(text)
    except ValueError as exc:
        parser.error(str(exc))

    json.dump(data, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
