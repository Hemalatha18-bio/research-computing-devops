from pathlib import Path
import subprocess


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "system_health.sh"


def run_health_script():
    return subprocess.run(
        ["bash", str(SCRIPT)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def test_script_runs_successfully():
    output = run_health_script()
    assert "research-computing-health-snapshot" in output


def test_output_contains_core_sections():
    output = run_health_script()
    for expected in (
        "timestamp_utc=",
        "hostname=",
        "## uptime_and_load",
        "## cpu",
        "## memory",
        "## filesystems",
        "## top_cpu_processes",
    ):
        assert expected in output


def test_timestamp_looks_like_utc_iso8601():
    output = run_health_script()
    timestamp_line = next(
        line for line in output.splitlines() if line.startswith("timestamp_utc=")
    )
    value = timestamp_line.split("=", 1)[1]
    assert value.endswith("Z")
    assert "T" in value
