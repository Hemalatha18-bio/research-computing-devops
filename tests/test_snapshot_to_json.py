import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "snapshot_to_json.py"


def sample_snapshot() -> str:
    return """research-computing-health-snapshot
timestamp_utc=2026-09-08T20:00:00Z
hostname=example-node

## uptime_and_load
up 1 day
"""


def test_cli_converts_snapshot_to_json(tmp_path):
    snapshot = tmp_path / "snapshot.txt"
    snapshot.write_text(sample_snapshot(), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(snapshot)],
        check=True,
        capture_output=True,
        text=True,
    )

    data = json.loads(result.stdout)
    assert data == {
        "hostname": "example-node",
        "snapshot_type": "research-computing-health-snapshot",
        "timestamp_utc": "2026-09-08T20:00:00Z",
    }


def test_cli_reads_from_stdin():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=sample_snapshot(),
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(result.stdout)["hostname"] == "example-node"


def test_missing_required_field_fails():
    incomplete = "research-computing-health-snapshot\ntimestamp_utc=2026-09-08T20:00:00Z\n"
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=incomplete,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "missing required snapshot fields" in result.stderr


def test_unrecognized_header_fails():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input="not-a-health-snapshot\n",
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "unrecognized health snapshot header" in result.stderr
