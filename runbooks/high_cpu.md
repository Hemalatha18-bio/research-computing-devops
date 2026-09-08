# Runbook: High CPU / Sustained Load

## Purpose

Provide a repeatable investigation path when monitoring reports high CPU utilization or sustained system load on a research-computing node.

> High CPU is not automatically a failure in HPC. Fully utilized CPUs may indicate a healthy scientific workload. The goal is to determine whether the activity is expected, inefficient, runaway, or affecting other services.

## Trigger

Use this runbook when one or more of the following occurs:

- CPU utilization remains near saturation longer than the expected workload window.
- Load average rises significantly above the node's available CPU capacity.
- A user-facing service becomes slow while CPU utilization is elevated.
- Monitoring detects a process consuming unexpected CPU resources.

## 1. Establish Scope

Record:

- affected node or service;
- alert start time;
- current CPU and load metrics;
- whether the node is assigned to an active workload;
- whether other nodes show the same pattern; and
- reported user impact, if any.

Do not terminate processes simply because CPU utilization is high.

## 2. Collect Evidence

Useful read-only commands include:

```bash
uptime
nproc
ps -eo pid,user,comm,%cpu,%mem --sort=-%cpu | head
free -h
df -hP
```

If the environment has a scheduler, correlate the node with scheduler/job information using the site's approved tooling and procedures.

## 3. Investigation Questions

### Is the utilization expected?

Check whether the top CPU consumers correspond to scheduled scientific or AI workloads. Sustained high CPU can be normal when a job requested and is actively using those resources.

### Is there resource contention?

Look for:

- more active work than the node was intended to run;
- memory pressure or swapping;
- storage or network symptoms that make processes spin or retry;
- multiple processes unexpectedly competing for the same resource; or
- a service process consuming resources outside its normal pattern.

### Is the process making progress?

When approved observability or application logs are available, compare CPU activity with job progress, throughput, logs, or task completion. High CPU with no observable progress may justify deeper investigation.

## 4. Decision Points

- **Expected scheduled workload, no impact:** document and continue monitoring.
- **Expected workload with system impact:** escalate according to local capacity/performance procedures.
- **Unexpected process or possible runaway behavior:** collect evidence and escalate to the service/node owner before taking disruptive action.
- **System instability or broad service impact:** follow the organization's incident/escalation procedure.

## 5. Escalation Notes

Include:

- timestamp and affected node/service;
- CPU/load metrics;
- top process information;
- related job/workload context;
- memory/filesystem observations;
- known user impact; and
- actions already taken.

## 6. Resolution / Follow-up

After resolution:

- document the cause;
- record whether the alert threshold was useful;
- link the incident/ticket if applicable;
- note any monitoring or runbook improvement; and
- avoid placing production-specific identifiers or sensitive data in public documentation.
