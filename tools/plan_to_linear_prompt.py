#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys


EXECUTION_RULES = """Execute the implementation plan below.

Execution rules:
- Treat the embedded implementation plan as the source of truth for scope, sequencing, and validation.
- Execute one slice at a time, starting with the earliest incomplete slice.
- Do not re-plan or broaden scope.
- Run the automated validation listed for each slice before moving to the next one.
- If a manual verification checkpoint is listed, stop and wait after automated checks pass.
- If the plan is ambiguous in a way that affects execution, stop and ask instead of guessing.
- If the codebase materially contradicts the plan, stop and report the contradiction with concrete file references.
- Keep progress updates concise and tied to slice completion, validation status, blockers, or explicit pause points.
"""


REQUIRED_HINTS = (
    "## Scope",
    "## Execution Context",
    "## Execution Strategy",
    "## Execution Slices",
)


def build_prompt(plan_text: str) -> str:
    plan_text = plan_text.strip()
    return (
        "# Execution Prompt\n\n"
        f"{EXECUTION_RULES}\n"
        "## Embedded Implementation Plan\n\n"
        f"{plan_text}\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert an implementation plan into a Linear-ready execution prompt."
    )
    parser.add_argument("--plan", required=True, help="Path to the implementation plan markdown file.")
    parser.add_argument(
        "--out",
        required=True,
        help="Ticket output name. The prompt is always written to thoughts/tickets/{name}.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan_path = Path(args.plan).expanduser().resolve()
    out_name = args.out
    if "/" in out_name or "\\" in out_name:
        print("error: --out must be a file name, not a path", file=sys.stderr)
        return 1
    if not out_name.endswith(".md"):
        out_name = f"{out_name}.md"
    out_path = Path.cwd() / "thoughts" / "tickets" / out_name

    if not plan_path.is_file():
        print(f"error: plan file not found: {plan_path}", file=sys.stderr)
        return 1

    plan_text = plan_path.read_text(encoding="utf-8").strip()
    if not plan_text:
        print(f"error: plan file is empty: {plan_path}", file=sys.stderr)
        return 1

    missing_hints = [hint for hint in REQUIRED_HINTS if hint not in plan_text]
    if missing_hints:
        hints = ", ".join(missing_hints)
        print(
            "warning: plan is missing expected implementation-plan sections: "
            f"{hints}",
            file=sys.stderr,
        )

    prompt = build_prompt(plan_text)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(prompt, encoding="utf-8")
    print(f"wrote Linear prompt to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
