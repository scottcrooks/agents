#!/usr/bin/env python3
"""Reject implement-plan handoffs that are not recorded plan boundaries."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FIELD_PATTERN = re.compile(r"^- (?P<name>[^:]+):\s*(?P<value>.*)\s*$", re.MULTILINE)
SLICE_STATUS_PATTERN = re.compile(r"^\s+- Status:\s*`(?P<status>[^`]+)`\s*$", re.MULTILINE)
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

    plan_text = args.plan.read_text(encoding="utf-8")
    ledger_text = args.ledger.read_text(encoding="utf-8")
    metadata = fields(ledger_text)
    mode = metadata.get("execution mode", "")
    boundary = metadata.get("boundary state", "")
    evidence = metadata.get("boundary evidence", "")
    attempts = metadata.get("blocker attempts", "")
    unblock = metadata.get("unblock condition", "")
    next_action = metadata.get("next action", "")
    ledger_plan = metadata.get("plan", "")
    statuses = SLICE_STATUS_PATTERN.findall(ledger_text)
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
        if "manual_checkpoint" not in statuses:
            errors.append("manual_checkpoint requires a slice with that status")
        checkpoints = [
            line for line in plan_text.splitlines()
            if "manual verification checkpoint:" in line.lower()
            and not re.search(r"checkpoint:\s*none\b", line, re.IGNORECASE)
        ]
        if not checkpoints:
            errors.append("the plan does not define a manual verification checkpoint")
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
