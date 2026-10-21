import csv
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("slurm_metrics_demo", ROOT / "scripts" / "slurm_metrics_demo.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_summary_fixture():
    result = module.summarize(ROOT / "monitoring" / "synthetic_slurm_jobs.csv")
    assert result["total_jobs"] == 6
    assert result["job_states"]["COMPLETED"] == 2
    assert result["job_states"]["PENDING"] == 1
    assert result["terminal_jobs"] == 4
    assert result["completion_rate_terminal_pct"] == 50.0
    assert result["failure_rate_terminal_pct"] == 25.0
    assert result["average_queue_wait_minutes_started"] == 13.75

def test_rejects_duplicate_jobs(tmp_path):
    rows = list(csv.DictReader((ROOT / "monitoring" / "synthetic_slurm_jobs.csv").open()))
    rows.append(rows[0])
    file = tmp_path / "jobs.csv"
    with file.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="duplicate"):
        module.summarize(file)

def test_rejects_missing_columns(tmp_path):
    file = tmp_path / "bad.csv"
    file.write_text("job_id,state\\n1,COMPLETED\\n")
    with pytest.raises(ValueError, match="columns"):
        module.summarize(file)
