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

logs_root="$repo_root/docs"
if [[ ! -d "$logs_root" ]]; then
  echo "No implementation logs found: docs/ directory missing."
  exit 0
fi

cutoff=""
if [[ "$mode" == "rolling" ]]; then
  cutoff="$(date -u -d "-$days days" +%F)"
fi

find "$logs_root" -type f -name '*.md' \
  | sed "s#^$repo_root/##" \
  | LC_ALL=C sort \
  | while IFS= read -r rel; do
      [[ "$rel" == docs/architecture/current-state/* ]] && continue
      base="$(basename "$rel")"
      if [[ ! "$base" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})_(.+)\.md$ ]]; then
        continue
      fi

      log_date="${BASH_REMATCH[1]}"
      raw_title="${BASH_REMATCH[2]}"

      if [[ "$mode" == "rolling" && "$log_date" < "$cutoff" ]]; then
        continue
      fi

      title="$(printf '%s' "$raw_title" | tr '_' ' ')"
      abs="$repo_root/$rel"

      files_changed="$(awk '
        BEGIN { in_section = 0; out = "" }
        /^## Files Changed/ { in_section = 1; next }
        /^## / && in_section { in_section = 0 }
        in_section && /^- / {
          sub(/^- /, "")
          out = out (out == "" ? "" : ", ") $0
        }
        END { print out }
      ' "$abs")"

      summary_bullets="$(awk '
        BEGIN { in_section = 0 }
        /^## Summary/ { in_section = 1; next }
        /^## / && in_section { in_section = 0 }
        in_section && /^- / { sub(/^- /, ""); print }
      ' "$abs")"

      echo "### $log_date - $title"
      echo "- Path: $rel"
      if [[ -n "$files_changed" ]]; then
        echo "- Files Changed: $files_changed"
      else
        echo "- Files Changed: (not listed)"
      fi
      if [[ -n "$summary_bullets" ]]; then
        while IFS= read -r line; do
          echo "- Summary: $line"
        done <<< "$summary_bullets"
      else
        echo "- Summary: (not listed)"
      fi
      echo
    done
