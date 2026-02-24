#!/usr/bin/env bash
set -euo pipefail

max_age_days="7"
repo_root="$(pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-age-days)
      max_age_days="$2"
      shift 2
      ;;
    --repo-root)
      repo_root="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

latest="$repo_root/docs/architecture/current-state/latest.md"

if [[ ! -f "$latest" ]]; then
  echo "FAIL: $latest is missing"
  exit 1
fi

generated_line="$(grep -E '^- Generated At \(UTC\): ' "$latest" | head -n1 || true)"
if [[ -z "$generated_line" ]]; then
  echo "FAIL: Generated timestamp not found in $latest"
  exit 1
fi

ts="${generated_line#- Generated At (UTC): }"
gen_epoch="$(date -u -d "$ts" +%s)"
now_epoch="$(date -u +%s)"
age_days="$(( (now_epoch - gen_epoch) / 86400 ))"

if (( age_days > max_age_days )); then
  echo "FAIL: latest.md is stale (${age_days}d > ${max_age_days}d)"
  exit 1
fi

echo "PASS: latest.md freshness OK (${age_days}d <= ${max_age_days}d)"
