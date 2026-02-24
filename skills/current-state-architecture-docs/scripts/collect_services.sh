#!/usr/bin/env bash
set -euo pipefail

repo_root="${1:-$(pwd)}"
services_file="$repo_root/services.yaml"

if [[ ! -f "$services_file" ]]; then
  echo "Service registry unavailable: services.yaml not found."
  exit 0
fi

awk '
BEGIN {
  in_services = 0
  in_commands = 0
  name = ""
  path = ""
  desc = ""
  cmd_count = 0
}

function trim(s) {
  sub(/^[[:space:]]+/, "", s)
  sub(/[[:space:]]+$/, "", s)
  return s
}

function reset_service() {
  name = ""
  path = ""
  desc = ""
  cmd_count = 0
  delete cmds
}

function flush_service() {
  if (name == "") return
  printf("- **%s**\n", name)
  printf("  - Path: %s\n", path == "" ? "(missing)" : path)
  printf("  - Description: %s\n", desc == "" ? "(missing)" : desc)

  if (cmd_count == 0) {
    printf("  - Commands: (none declared)\n")
  } else {
    out = ""
    for (i = 1; i <= cmd_count; i++) {
      out = out (i == 1 ? "" : ", ") cmds[i]
    }
    printf("  - Commands: %s\n", out)
  }

  reset_service()
}

/^services:[[:space:]]*$/ {
  in_services = 1
  next
}

in_services && /^local:[[:space:]]*$/ {
  flush_service()
  in_services = 0
  in_commands = 0
  next
}

in_services && /^[[:space:]]*-[[:space:]]name:[[:space:]]*/ {
  flush_service()
  in_commands = 0
  line = $0
  sub(/^[[:space:]]*-[[:space:]]name:[[:space:]]*/, "", line)
  name = trim(line)
  next
}

in_services && /^[[:space:]]*path:[[:space:]]*/ {
  line = $0
  sub(/^[[:space:]]*path:[[:space:]]*/, "", line)
  path = trim(line)
  next
}

in_services && /^[[:space:]]*description:[[:space:]]*/ {
  line = $0
  sub(/^[[:space:]]*description:[[:space:]]*/, "", line)
  desc = trim(line)
  next
}

in_services && /^[[:space:]]*commands:[[:space:]]*$/ {
  in_commands = 1
  next
}

in_services && in_commands && /^[[:space:]]{6}[a-z0-9-]+:[[:space:]]*/ {
  line = $0
  sub(/^[[:space:]]*/, "", line)
  split(line, parts, ":")
  cmd_count++
  cmds[cmd_count] = parts[1]
  next
}

in_services && in_commands && /^[[:space:]]{2}[a-z]/ {
  in_commands = 0
}

END {
  flush_service()
}
' "$services_file"
