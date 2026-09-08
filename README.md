# Research Computing DevOps Lab

A public-portfolio style lab for demonstrating **HPC / research-computing automation, monitoring, troubleshooting, documentation, testing, and CI** with safe, generic examples.

> This repository is independent portfolio work. It does **not** contain Washington University internal code, hostnames, inventories, dashboards, credentials, alert rules, cluster architecture, or proprietary configuration.

## Why This Project

Scientific computing environments need more than fast hardware. They also need repeatable configuration, observable systems, clear runbooks, reliable automation, and documentation that helps teams troubleshoot problems consistently.

This repository demonstrates those practices with sanitized examples that can be reviewed and executed without access to a production HPC cluster.

## What It Demonstrates

- **Infrastructure as Code:** Ansible playbooks for generic compute-node configuration
- **Linux automation:** Bash-based system health collection
- **Machine-readable operations data:** Python conversion of health-snapshot metadata to JSON
- **Monitoring & observability:** dashboard and alert design concepts for HPC systems
- **Operational documentation:** runbooks for high CPU and failed-service scenarios
- **Testing:** automated validation of scripts and expected outputs
- **Continuous integration:** GitHub Actions checks for Python tests, shell syntax, and Ansible syntax
- **Security-conscious portfolio practice:** no real infrastructure identifiers or internal configuration

## Repository Structure

```text
research-computing-devops/
├── .github/workflows/ci.yml
├── ansible/
│   ├── inventory.example.ini
│   └── playbooks/
│       └── configure_compute_node.yml
├── monitoring/
│   └── dashboard_design.md
├── runbooks/
│   ├── failed_service.md
│   └── high_cpu.md
├── scripts/
│   ├── snapshot_to_json.py
│   └── system_health.sh
├── tests/
│   ├── test_snapshot_to_json.py
│   └── test_system_health.py
├── .gitignore
├── LICENSE
├── requirements-dev.txt
└── README.md
```

## 1. Ansible Automation

`ansible/playbooks/configure_compute_node.yml` is a deliberately generic example showing how a shell-based setup process can be represented as an idempotent Ansible playbook.

It demonstrates:

- package management through Ansible modules;
- creation of a managed configuration directory;
- deployment of a simple managed file;
- tags for selective execution; and
- handlers and idempotent task design.

Use only against systems you are authorized to manage. The example inventory uses reserved `.invalid` hostnames so it cannot accidentally target a real environment.

Syntax-check the playbook:

```bash
ansible-playbook \
  -i ansible/inventory.example.ini \
  ansible/playbooks/configure_compute_node.yml \
  --syntax-check
```

For a real lab environment, inventory entries, privilege escalation, package names, and policies would be adapted to the target platform after review.

## 2. System Health Collection

`scripts/system_health.sh` collects a compact local snapshot of:

- hostname;
- timestamp;
- uptime/load information;
- CPU count;
- memory usage;
- filesystem usage; and
- top CPU-consuming processes.

Run it locally:

```bash
bash scripts/system_health.sh
```

The output is intended as a troubleshooting aid, not a replacement for a monitoring platform.

For automation workflows, `scripts/snapshot_to_json.py` converts the snapshot header metadata to JSON. It accepts a snapshot file or stdin and validates required fields before emitting structured output.

```bash
bash scripts/system_health.sh > health_snapshot.txt
python scripts/snapshot_to_json.py health_snapshot.txt
```

Or stream directly:

```bash
bash scripts/system_health.sh | python scripts/snapshot_to_json.py
```

Example JSON metadata:

```json
{
  "hostname": "example-node",
  "snapshot_type": "research-computing-health-snapshot",
  "timestamp_utc": "2026-09-08T20:00:00Z"
}
```

## 3. Monitoring / Dashboard Design

`monitoring/dashboard_design.md` describes a generic HPC operations dashboard organized around:

- availability;
- CPU and load;
- memory pressure;
- disk/filesystem health;
- scheduler/job signals;
- GPU signals where applicable; and
- alert-to-runbook links.

The design intentionally distinguishes **high utilization** from **unhealthy behavior**. In HPC, high CPU can be expected during productive workloads; useful monitoring requires context such as load duration, scheduler state, memory pressure, process ownership, and service impact.

## 4. Operational Runbooks

Two example runbooks show how to document investigation paths without jumping directly to remediation:

- `runbooks/high_cpu.md`
- `runbooks/failed_service.md`

Each runbook follows a consistent structure:

1. trigger / symptom;
2. scope and impact;
3. evidence to collect;
4. investigation steps;
5. decision points;
6. safe escalation guidance; and
7. post-incident documentation.

## 5. Tests and CI

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run tests:

```bash
pytest -q
```

CI checks:

- Python tests for the health collector and JSON parser;
- Bash syntax validation; and
- Ansible playbook syntax validation.

## Design Principles

### Idempotence
Automation should be safe to run repeatedly without causing unintended changes.

### Observability before intervention
Collect evidence first. Metrics need workload context, especially in HPC where high CPU or GPU utilization may be normal.

### Least surprise
Examples are intentionally simple, explicit, and non-destructive.

### Documentation as part of engineering
Runbooks and configuration notes are treated as version-controlled engineering artifacts, not afterthoughts.

### Sanitization
This repository uses generic hosts, paths, services, and examples. Production or employer-specific information should remain in approved internal systems.

## Skills Demonstrated

Ansible · Infrastructure as Code · Bash · Python · Linux · HPC concepts · monitoring/observability · troubleshooting · structured JSON output · runbook documentation · pytest · GitHub Actions · reproducible engineering practices

## Future Improvements

- Add Molecule-based Ansible role testing.
- Add a synthetic scheduler-metrics dataset and dashboard mockup.
- Add an example CI/CD workflow for validating infrastructure documentation and YAML.
- Add containerized local testing for the generic node configuration.

## Author

Hemalatha Ponnam  
M.S. Bioinformatics & Computational Biology  
HPC Engineering Intern / Research Computing & Scientific DevOps
