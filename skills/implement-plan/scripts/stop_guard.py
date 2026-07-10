#!/usr/bin/env python3
"""Continue Codex turns that try to stop before an implement-plan boundary."""

from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


PLAN_INVOCATION = re.compile(r"\$implement-plan\s+([^\r\n]+)")
LEDGER_SECTION = re.compile(
    r"^##\s+Status Ledger Path\s*$\n(?P<body>.*?)(?=^##\s|\Z)",
    re.MULTILINE | re.DOTALL,
)
BACKTICK_PATH = re.compile(r"`([^`]+\.status\.md)`")


def hook_response(*, block: bool, reason: str | None = None) -> dict[str, Any]:
    if block:
        return {"decision": "block", "reason": reason}
    return {"continue": True}


def latest_plan_argument(transcript: Path) -> str | None:
    latest: str | None = None
    try:
        lines = transcript.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return None

    for line in lines:
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("type") != "event_msg":
            continue
        payload = record.get("payload", {})
        if payload.get("type") != "user_message":
            continue
        message = payload.get("message")
        if not isinstance(message, str):
            continue
        match = PLAN_INVOCATION.search(message)
        if not match:
            continue
        try:
            arguments = shlex.split(match.group(1))
        except ValueError:
            continue
        if arguments:
            latest = arguments[0]
    return latest


def ledger_from_plan(plan: Path) -> Path | None:
    try:
        plan_text = plan.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    section = LEDGER_SECTION.search(plan_text)
    if section:
        ledger_match = BACKTICK_PATH.search(section.group("body"))
        if ledger_match:
            ledger = Path(ledger_match.group(1)).expanduser()
            return ledger if ledger.is_absolute() else plan.parent.parent.parent / ledger
    return plan.parent.parent / "plan-status" / f"{plan.stem}.status.md"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        print(json.dumps(hook_response(block=False)))
        return 0

    transcript_value = payload.get("transcript_path")
    cwd_value = payload.get("cwd")
    if not isinstance(transcript_value, str) or not isinstance(cwd_value, str):
        print(json.dumps(hook_response(block=False)))
        return 0

    plan_argument = latest_plan_argument(Path(transcript_value))
    if plan_argument is None:
        print(json.dumps(hook_response(block=False)))
        return 0

    cwd = Path(cwd_value)
    plan = Path(plan_argument).expanduser()
    if not plan.is_absolute():
        plan = cwd / plan
    ledger = ledger_from_plan(plan)
    if ledger is None:
        reason = (
            "Implement-plan stop blocked: the active plan's ledger path could not be "
            "resolved. Read the plan, initialize its ledger, and continue."
        )
        print(json.dumps(hook_response(block=True, reason=reason)))
        return 0

    checker = Path(__file__).with_name("plan_boundary_check.py")
    result = subprocess.run(
        [sys.executable, str(checker), "--plan", str(plan), "--ledger", str(ledger)],
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )
    if result.returncode == 0:
        print(json.dumps(hook_response(block=False)))
        return 0

    detail = (result.stderr or result.stdout).strip()
    reason = (
        "Implement-plan stop blocked: the ledger has not reached a permitted boundary. "
        "Continue the active slice now; do not send a status-only final response. "
        "Read the next unchecked requirement and make the next concrete tool call. "
        "If the user explicitly cancelled, record the cancelled boundary first."
    )
    if detail:
        reason = f"{reason}\n\nBoundary check output:\n{detail}"
    print(json.dumps(hook_response(block=True, reason=reason)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
