# Synthetic SLURM Job Monitoring — Portfolio Demonstration

> **Entirely synthetic.** All job IDs, timestamps, partitions and metrics in this example are invented for documentation/testing. This is **not** a capture of a real cluster or a deployed Datadog integration.

## Try it

```bash
python scripts/slurm_metrics_demo.py monitoring/synthetic_slurm_jobs.csv
pytest -q tests/test_slurm_metrics_demo.py
```

The standalone Python script parses fixture records, validates timestamp order and job states, and prints machine-readable JSON. It does not query `sacct`, connect to Slurm, send data to Datadog, or require credentials.

## Sample dashboard layout

| Widget | Visualization | Metric / interpretation |
| --- | --- | --- |
| 1. Job state overview | Query-value tiles | Total and counts by PENDING, RUNNING, COMPLETED, FAILED, CANCELLED, TIMEOUT |
| 2. Submission vs completion | Timeseries (requires timestamped event rollup) | New jobs by submission timestamp vs completed jobs by finish timestamp |
| 3. Completion rate | Query value | Completed / terminal jobs (not all submitted jobs) |
| 4. Failure rate | Query value | (FAILED + TIMEOUT) / terminal jobs |
| 5. Queue wait | Summary / timeseries | Mean submitted-to-started minutes among started jobs |
| 6. Partition mix | Stacked bar | Jobs grouped by partition and job state |

## Example output

The six-row fixture contains 2 completed, 1 failed, 1 pending, 1 running and 1 cancelled job. Consequently, the **terminal-only completion rate is 50% (2/4)** and the **terminal-only failure rate is 25% (1/4)**. These synthetic percentages are **not** operational performance claims.

## Production adaptation boundaries

A real deployment would require permission to read scheduler accounting, a documented snapshot versus event model, scrubbed identifiers, monitored freshness/collection failures, scheduler-specific normalization and verified metric mappings.

The script calculates metrics from **one CSV snapshot**; it does **not** implement a live monitoring pipeline. Avoid summing repeated snapshots as if they were distinct job events. No production Datadog queries, infrastructure identifiers, service endpoints, hostnames or alert thresholds are published.

## Design considerations

- **Denominators matter:** current PENDING and RUNNING jobs are excluded from terminal-job completion/failure rates.
- **Queue wait isn't runtime:** use submitted-to-started for wait, started-to-finished for duration.
- **High usage is not itself failure:** correlate with scheduler status, workload demand and service impact.
- **Missing telemetry must be visible:** distinguish zero jobs from stale or missing collection.
- **Alert responsibly:** threshold selection needs baselines and an approved runbook; this example prescribes none.

Related: [overall dashboard design](dashboard_design.md), [high-CPU runbook](../runbooks/high_cpu.md), [failed-service runbook](../runbooks/failed_service.md).
