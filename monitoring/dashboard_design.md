# Monitoring Design: Research Computing Overview Dashboard

## Goal

Design a high-level dashboard that helps an operations or research-computing team answer three questions quickly:

1. Is the platform available?
2. Is resource behavior expected for current workloads?
3. Where should an engineer investigate next?

This is a vendor-neutral design. It can be implemented in Datadog or another approved observability platform without exposing production configuration here.

## Dashboard Sections

### 1. Availability

Suggested signals:

- reachable/healthy node count;
- failed health checks;
- critical service availability;
- recent alert count; and
- nodes entering/leaving service.

### 2. CPU and Load

Suggested signals:

- CPU utilization by node;
- load average normalized by CPU count;
- sustained saturation duration;
- top outlier nodes; and
- correlation with active scheduler workloads.

**Interpretation note:** high CPU can be desirable in HPC. Alerts should consider workload context rather than treating utilization alone as a failure.

### 3. Memory

Suggested signals:

- used/available memory;
- swap activity;
- out-of-memory events;
- nodes with sustained memory pressure; and
- workload memory utilization relative to requests where scheduler data are available.

### 4. Filesystem / Storage

Suggested signals:

- filesystem capacity percentage;
- inode utilization;
- I/O latency or throughput when available;
- mount availability; and
- rapid capacity growth.

### 5. Scheduler / Workload Signals

If exposed through approved telemetry:

- running and queued jobs;
- failed jobs;
- queue wait trends;
- node allocation state;
- resource-request versus resource-use summaries; and
- unusually long or repeatedly failing workloads.

### 6. GPU / AI Workloads

For GPU-enabled environments, useful signals can include:

- GPU utilization;
- memory utilization;
- temperature/health indicators;
- allocated versus idle GPUs; and
- workload failures associated with GPU resources.

## Alert Design Principles

### Prefer symptoms with context

A useful alert should indicate an actionable condition, not simply a high metric value.

For example, instead of:

> CPU > 90%

consider a condition conceptually closer to:

> Sustained CPU saturation + no expected scheduled workload + service latency/error impact

Exact thresholds must be determined from the real environment and historical baselines; this repository intentionally does not invent production values.

### Link alerts to runbooks

Each operational alert should point to a version-controlled or approved internal runbook covering:

- evidence collection;
- expected-versus-abnormal behavior;
- escalation conditions; and
- safe recovery procedures.

Example mappings in this repository:

| Signal | Runbook |
|---|---|
| Sustained high CPU / load | `runbooks/high_cpu.md` |
| Service unavailable or repeatedly failing | `runbooks/failed_service.md` |

## Dashboard Audience

A good research-computing dashboard should support multiple levels of detail:

- **Tier 1 / user support:** easy-to-read health summaries and clear escalation signals.
- **Engineers:** deeper node, service, scheduler, and resource context.
- **Team leads:** trends, recurring failure patterns, and capacity signals.

## Public Portfolio Boundary

This document intentionally excludes:

- real cluster names;
- real Datadog queries or monitor IDs;
- internal service names;
- alert thresholds copied from production;
- private dashboards;
- network/topology details; and
- employer-specific escalation contacts.
