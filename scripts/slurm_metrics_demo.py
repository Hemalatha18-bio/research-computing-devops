#!/usr/bin/env python3
"""Aggregate synthetic SLURM-like job records; no cluster access or credentials."""
import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

STATES = {"PENDING", "RUNNING", "COMPLETED", "FAILED", "CANCELLED", "TIMEOUT"}
FINAL = {"COMPLETED", "FAILED", "CANCELLED", "TIMEOUT"}

def timestamp(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None

def summarize(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        expected = {"job_id", "submitted_at", "started_at", "finished_at", "state", "partition"}
        if not reader.fieldnames or not expected.issubset(reader.fieldnames):
            raise ValueError("Missing required CSV columns")
        rows = list(reader)
    counts = Counter()
    waits = []
    seen = set()
    for row in rows:
        job = row["job_id"].strip()
        state = row["state"].strip().upper()
        if not job or job in seen or state not in STATES or not row["partition"].strip():
            raise ValueError("Invalid/duplicate job ID, state or partition")
        seen.add(job)
        submitted = timestamp(row["submitted_at"])
        started = timestamp(row["started_at"])
        finished = timestamp(row["finished_at"])
        if submitted is None or (started and started < submitted) or (finished and (not started or finished < started)):
            raise ValueError("Invalid timestamp order")
        if state == "PENDING" and (started or finished):
            raise ValueError("Pending jobs cannot have start/end times")
        if state == "RUNNING" and (not started or finished):
            raise ValueError("Running jobs need a start and no finish")
        if state in {"COMPLETED", "FAILED", "TIMEOUT"} and (not started or not finished):
            raise ValueError("Completed/failed/timed-out jobs need start and finish times")
        if state == "CANCELLED" and started and not finished:
            raise ValueError("Started cancelled jobs require a finish time")
        if started:
            waits.append((started - submitted).total_seconds() / 60)
        counts[state] += 1
    terminal = sum(counts[x] for x in FINAL)
    return {
        "source": "synthetic_demo_only",
        "total_jobs": len(rows),
        "job_states": {s: counts[s] for s in sorted(STATES)},
        "terminal_jobs": terminal,
        "completion_rate_terminal_pct": round(100 * counts["COMPLETED"] / terminal, 2) if terminal else None,
        "failure_rate_terminal_pct": round(100 * (counts["FAILED"] + counts["TIMEOUT"]) / terminal, 2) if terminal else None,
        "average_queue_wait_minutes_started": round(sum(waits) / len(waits), 2) if waits else None,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", help="Synthetic job records CSV")
    args = parser.parse_args()
    print(json.dumps(summarize(args.csv_path), indent=2))

if __name__ == "__main__":
    main()
