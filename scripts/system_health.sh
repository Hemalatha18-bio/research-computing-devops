#!/usr/bin/env bash
set -euo pipefail

print_section() {
  printf '\n## %s\n' "$1"
}

printf 'research-computing-health-snapshot\n'
printf 'timestamp_utc=%s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
printf 'hostname=%s\n' "$(hostname)"

print_section "uptime_and_load"
if command -v uptime >/dev/null 2>&1; then
  uptime
else
  echo "uptime command unavailable"
fi

print_section "cpu"
if command -v nproc >/dev/null 2>&1; then
  printf 'logical_cpu_count=%s\n' "$(nproc)"
elif command -v getconf >/dev/null 2>&1; then
  printf 'logical_cpu_count=%s\n' "$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo unknown)"
else
  echo "logical_cpu_count=unknown"
fi

print_section "memory"
if command -v free >/dev/null 2>&1; then
  free -h
else
  echo "free command unavailable"
fi

print_section "filesystems"
df -hP 2>/dev/null || echo "filesystem information unavailable"

print_section "top_cpu_processes"
if command -v ps >/dev/null 2>&1; then
  ps -eo pid,user,comm,%cpu,%mem --sort=-%cpu 2>/dev/null | head -n 6 || \
    ps -eo pid,user,comm,%cpu,%mem 2>/dev/null | head -n 6 || \
    echo "process information unavailable"
else
  echo "ps command unavailable"
fi
