#!/usr/bin/env python3
"""Reject implement-plan handoffs that are not recorded plan boundaries."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FIELD_PATTERN = re.compile(r"^- (?P<name>[^:]+):\s*(?P<value>.*)\s*$", re.MULTILINE)
SLICE_STATUS_PATTERN = re.compile(r"^\s+- Status:\s*`(?P<status>[^`]+)`\s*$", re.MULTILINE)
SLICE_PATTERN = re.compile(r"^(?P<number>[1-9]\d*)\. (?P<name>\S[^\n]*)$", re.MULTILINE)
ALLOWED_STATUSES = {
    "pending",
    "in_progress",
    "complete",
    "manual_checkpoint",
    "blocked",
    "cancelled",
}
ALLOWED_BOUNDARIES = {
    "slice_complete",
    "manual_checkpoint",
    "hard_blocker",
    "plan_complete",
    "cancelled",
}


def normalize(value: str) -> str:
    return value.strip().strip("`").strip()


def fields(text: str) -> dict[str, str]:
    return {
        match.group("name").strip().lower(): normalize(match.group("value"))
        for match in FIELD_PATTERN.finditer(text)
    }


def without_code_blocks(text: str) -> str:
    """Exclude examples and code from the Markdown control fields."""
    lines: list[str] = []
    fence_marker = ""
    fence_length = 0
    for line in text.splitlines():
        fence = re.match(r"^[ \t]*(`{3,}|~{3,})(.*)$", line)
        if fence:
            marker, suffix = fence.groups()
            if not fence_marker:
                fence_marker, fence_length = marker[0], len(marker)
            elif (
                marker[0] == fence_marker
                and len(marker) >= fence_length
                and not suffix.strip()
            ):
                fence_marker = ""
            lines.append("")
        else:
            lines.append("" if fence_marker else line)
    return "\n".join(lines)


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^##[ \t]+{re.escape(heading)}[ \t]*\n(?P<body>.*?)(?=^##[ \t]+|\Z)",
        text,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    return match.group("body") if match else ""


def slices(text: str, heading: str) -> list[tuple[int, str, str]]:
    body = section(text, heading)
    matches = list(SLICE_PATTERN.finditer(body))
    entries: list[tuple[int, str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        entries.append((int(match.group("number")), match.group("name").strip(),
                        body[match.end():end]))
    return entries


def has_checkpoint(body: str) -> bool:
    matches = re.findall(
        r"^[ \t]*-[ \t]+Manual verification checkpoint:[ \t]*(.*)$",
        body,
        re.MULTILINE | re.IGNORECASE,
    )
    return any(normalize(value).lower().rstrip(".") not in {"", "none"} for value in matches)


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"boundary check failed: {error}", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--ledger", required=True, type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    if not args.plan.is_file():
        errors.append(f"plan does not exist: {args.plan}")
    if not args.ledger.is_file():
        errors.append(f"ledger does not exist: {args.ledger}")
    if errors:
        return fail(errors)

    plan_text = without_code_blocks(args.plan.read_text(encoding="utf-8"))
    ledger_text = without_code_blocks(args.ledger.read_text(encoding="utf-8"))
    metadata = fields(section(ledger_text, "Metadata"))
    plan_slices = slices(plan_text, "Execution Slices")
    ledger_slices = slices(ledger_text, "Slice Status")
    plan_identity = [(number, name) for number, name, _ in plan_slices]
    ledger_identity = [(number, name) for number, name, _ in ledger_slices]
    if not plan_slices:
        errors.append("plan must define numbered entries under Execution Slices")
    elif [number for number, _, _ in plan_slices] != list(range(1, len(plan_slices) + 1)):
        errors.append("Execution Slices must use consecutive numbers starting at 1")
    if not ledger_slices or ledger_identity != plan_identity:
        errors.append("ledger slices must match plan Execution Slices in number, name, and order")

    statuses: list[str] = []
    checkpoint_slices: list[int] = []
    for number, name, body in ledger_slices:
        entry_statuses = SLICE_STATUS_PATTERN.findall(body)
        if len(entry_statuses) != 1 or entry_statuses[0] not in ALLOWED_STATUSES:
            errors.append(f"ledger slice {number}. {name} requires one valid Status")
        statuses.extend(entry_statuses)
        if "manual_checkpoint" in entry_statuses:
            checkpoint_slices.append(number)

    automation = metadata.get("automation mode", "")
    plan_automation = fields(section(plan_text, "Execution Context")).get("automation mode", "")
    if automation not in {"afk", "interactive"} or plan_automation != automation:
        errors.append("plan and ledger must record the same Automation mode: afk or interactive")
    planned_checkpoints = {number for number, _, body in plan_slices if has_checkpoint(body)}
    if automation == "afk" and (planned_checkpoints or checkpoint_slices):
        errors.append("AFK mode forbids blocking manual checkpoints")
    mode = metadata.get("execution mode", "")
    boundary = metadata.get("boundary state", "")
    evidence = metadata.get("boundary evidence", "")
    attempts = metadata.get("blocker attempts", "")
    unblock = metadata.get("unblock condition", "")
    next_action = metadata.get("next action", "")
    ledger_plan = metadata.get("plan", "")
    unchecked_requirements = re.findall(r"^\s*- \[ \] ", ledger_text, re.MULTILINE)

    if mode not in {"boundary-driven", "single-slice", "continuous"}:
        errors.append(
            "Execution mode must be `boundary-driven`, `single-slice`, or `continuous`"
        )
    if boundary not in ALLOWED_BOUNDARIES:
        errors.append(
            "Boundary state must be slice_complete, manual_checkpoint, "
            "hard_blocker, plan_complete, or cancelled"
        )
    if "in_progress" in statuses:
        errors.append("a slice is still `in_progress`")
    if not next_action or next_action.lower() == "none":
        errors.append("Next action must describe the resume or completion action")
    if not ledger_plan:
        errors.append("ledger must identify its Plan")
    elif Path(ledger_plan).name != args.plan.name:
        errors.append("ledger Plan does not match --plan")

    if boundary == "slice_complete":
        if mode == "continuous":
            errors.append("slice_complete handoff is not allowed in continuous mode")
        if "complete" not in statuses:
            errors.append("slice_complete requires at least one completed slice")
        if not evidence or evidence.lower() == "none":
            errors.append("slice_complete requires concrete Boundary evidence")
        if "remaining requirements" not in ledger_text.lower():
            errors.append("slice_complete requires a Remaining requirements checklist")
        if unchecked_requirements:
            errors.append("slice_complete has unchecked Remaining requirements")
        validation = metadata.get("validation", "")
        if not validation or validation.lower() in {"none", "not run"}:
            errors.append("slice_complete requires recorded validation results")

    if boundary == "manual_checkpoint":
        if automation != "interactive":
            errors.append("manual_checkpoint requires interactive Automation mode")
        if len(checkpoint_slices) != 1:
            errors.append("manual_checkpoint requires exactly one slice with that status")
        elif checkpoint_slices[0] not in planned_checkpoints:
            errors.append("the checkpoint slice must define Manual verification checkpoint instructions")
        if not evidence or evidence.lower() == "none":
            errors.append("manual_checkpoint requires Boundary evidence/instructions")

    if boundary == "hard_blocker":
        if "blocked" not in statuses:
            errors.append("hard_blocker requires a blocked slice")
        for label, value in (
            ("Boundary evidence", evidence),
            ("Blocker attempts", attempts),
            ("Unblock condition", unblock),
        ):
            if not value or value.lower() == "none":
                errors.append(f"hard_blocker requires a concrete {label}")

    if boundary == "plan_complete":
        if metadata.get("overall status", "") != "complete":
            errors.append("plan_complete requires Overall status `complete`")
        incomplete = [status for status in statuses if status != "complete"]
        if incomplete or not statuses:
            errors.append("plan_complete requires every slice status to be `complete`")
        if not evidence or evidence.lower() == "none":
            errors.append("plan_complete requires concrete Boundary evidence")
        if unchecked_requirements:
            errors.append("plan_complete has unchecked Remaining requirements")
        validation = metadata.get("validation", "")
        if not validation or validation.lower() in {"none", "not run"}:
            errors.append("plan_complete requires recorded validation results")

    if boundary == "cancelled":
        if metadata.get("overall status", "") != "cancelled":
            errors.append("cancelled requires Overall status `cancelled`")
        if "cancelled" not in statuses:
            errors.append("cancelled requires a cancelled slice")
        if not evidence or evidence.lower() == "none":
            errors.append("cancelled requires concrete Boundary evidence")

    if errors:
        return fail(errors)

    print(f"boundary check passed: {boundary} ({mode})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
