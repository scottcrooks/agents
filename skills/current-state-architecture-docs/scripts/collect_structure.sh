#!/usr/bin/env bash
set -euo pipefail

repo_root="${1:-$(pwd)}"

collect_block() {
  local base="$1"
  if [[ -d "$base" ]]; then
    find "$base" -mindepth 1 -maxdepth 1 -type d | sed "s#^$repo_root/##" | LC_ALL=C sort
  fi
}

echo "Top-level directories:"
find "$repo_root" -mindepth 1 -maxdepth 1 -type d | sed "s#^$repo_root/##" | LC_ALL=C sort

echo
echo "apps/*:"
collect_block "$repo_root/apps"

echo
echo "packages/*:"
collect_block "$repo_root/packages"

echo
echo "tools/*:"
collect_block "$repo_root/tools"

echo
echo "docs/*:"
collect_block "$repo_root/docs"
