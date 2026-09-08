# Runbook: Failed or Unhealthy Service

## Purpose

Provide a safe, repeatable investigation path when a monitored service is reported as failed, unavailable, or unhealthy.

## Trigger

Use this runbook when:

- a monitoring check reports a failed service;
- a health endpoint stops responding;
- users report that a service is unavailable; or
- logs/metrics show repeated service restarts or failures.

## 1. Confirm the Symptom

Record:

- service name;
- affected host or environment;
- alert time;
- current user impact; and
- whether the issue is isolated or widespread.

Avoid immediately restarting a service before collecting enough evidence to understand the failure.

## 2. Collect Read-Only Evidence

On a systemd-based Linux host, approved examples may include:

```bash
systemctl status <service-name> --no-pager
journalctl -u <service-name> --since "15 minutes ago" --no-pager
uptime
free -h
df -hP
```

Use only commands and log access allowed by the local environment.

## 3. Common Investigation Areas

Check for:

- configuration or syntax errors;
- missing dependencies;
- exhausted disk space;
- memory pressure;
- permission problems;
- unavailable upstream dependencies;
- recent deployments or configuration changes; and
- repeated crash/restart loops.

## 4. Decision Points

- **Known transient issue with an approved restart procedure:** follow the approved internal recovery process.
- **Configuration-related failure:** compare against version-controlled or approved configuration before changing anything.
- **Dependency failure:** escalate to the owner of the affected dependency.
- **Unknown or recurring failure:** preserve logs/evidence and escalate rather than repeatedly restarting.

## 5. Escalation Package

Include:

- service and host scope;
- time of failure;
- current status;
- relevant error excerpts or error codes;
- recent known changes;
- CPU, memory, and disk observations;
- user impact; and
- actions already taken.

Do not include credentials, tokens, private hostnames, or other sensitive operational data in public issue trackers or documentation.

## 6. Post-Incident Follow-up

After the service is stable:

- document the root cause if known;
- update monitoring if the signal was weak or noisy;
- update this runbook if a new diagnostic step proved useful;
- add regression checks where practical; and
- link internal incident/ticket records only in approved internal systems.
