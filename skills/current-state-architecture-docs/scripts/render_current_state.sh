#!/usr/bin/env bash
set -euo pipefail

mode="rolling"
days="14"
repo_root="$(pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      mode="$2"
      shift 2
      ;;
    --days)
      days="$2"
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

if [[ "$mode" != "rolling" && "$mode" != "full" ]]; then
  echo "mode must be 'rolling' or 'full'" >&2
  exit 2
fi

skill_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

services_tmp="$(mktemp)"
structure_tmp="$(mktemp)"
logs_tmp="$(mktemp)"
trap 'rm -f "$services_tmp" "$structure_tmp" "$logs_tmp"' EXIT

"$skill_root/scripts/collect_services.sh" "$repo_root" > "$services_tmp"
"$skill_root/scripts/collect_structure.sh" "$repo_root" > "$structure_tmp"
"$skill_root/scripts/collect_logs.sh" --mode "$mode" --days "$days" --repo-root "$repo_root" > "$logs_tmp"

out_dir="$repo_root/docs/architecture/current-state"
mkdir -p "$out_dir"

today="$(date -u +%F)"
generated_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
out_file="$out_dir/${today}_current-state.md"
latest_file="$out_dir/latest.md"
latest_tmp="$(mktemp "$out_dir/.latest.XXXXXX")"

backend_dirs="$(find "$repo_root/apps" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sed 's#.*/##' | grep -E 'pythia|api|backend' | LC_ALL=C sort | paste -sd ',' - | sed 's/,/, /g' || true)"
if [[ -z "$backend_dirs" ]]; then
  backend_state="- Backend service directories: (none detected)"
else
  backend_state="- Backend service directories: $backend_dirs"
fi

frontend_dirs="$(find "$repo_root/apps" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sed 's#.*/##' | grep -Ev 'pythia|api|backend' | LC_ALL=C sort | paste -sd ',' - | sed 's/,/, /g' || true)"
if [[ -z "$frontend_dirs" ]]; then
  frontend_state="- No frontend directories detected under apps/."
else
  frontend_state="- Frontend/admin service directories: $frontend_dirs"
fi

packages_dirs="$(find "$repo_root/packages" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sed 's#.*/##' | LC_ALL=C sort | paste -sd ',' - | sed 's/,/, /g' || true)"
tools_dirs="$(find "$repo_root/tools" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sed 's#.*/##' | LC_ALL=C sort | paste -sd ',' - | sed 's/,/, /g' || true)"

[[ -z "$packages_dirs" ]] && packages_dirs="(none)"
[[ -z "$tools_dirs" ]] && tools_dirs="(none)"

cat > "$out_file" <<DOC
# Current-State Architecture Snapshot

## Overview
This document is generated from repository evidence and is intended to describe current implementation state rather than future design intent.

## Generation Metadata
- Generated At (UTC): $generated_at
- Mode: $mode
- Rolling Window Days: $days
- Repository Root: $repo_root

## Monorepo Topology
$(cat "$structure_tmp")

## Service Registry Status
$(cat "$services_tmp")

## Backend Architecture State
$backend_state

## Frontend Architecture State
$frontend_state

## Shared Libraries and Tooling
- packages/: $packages_dirs
- tools/: $tools_dirs

## Recent Architecture-Impacting Changes
$(cat "$logs_tmp")

## Risks and Drift Notes
- Architecture narratives may drift if generation is not run regularly.
- Repositories without services.yaml will have limited service registry fidelity.
- Rolling mode intentionally omits older logs; use full mode for complete regeneration.

## Source Evidence
- services.yaml (when present)
- docs/YYYY-MM-DD_*.md and docs/*/YYYY-MM-DD_*.md
- README.md
- docs/01-argus.md
- apps/*/docs/*.md
DOC

cp "$out_file" "$latest_tmp"
mv "$latest_tmp" "$latest_file"

echo "Wrote: $out_file"
echo "Wrote: $latest_file"
