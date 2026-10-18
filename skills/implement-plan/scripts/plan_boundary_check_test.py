from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


SCRIPT_DIRECTORY = Path(__file__).resolve().parent


class PlanBoundaryCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = TemporaryDirectory(prefix="plan-boundary-test-")
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.plan = self.root / "example.md"
        self.ledger = self.root / "example.status.md"

    def write_artifacts(
        self,
        *,
        plan_entries: list[tuple[int, str, str]] | None = None,
        ledger_entries: list[tuple[int, str, str]] | None = None,
        metadata: dict[str, str | None] | None = None,
        plan_mode: str | None = "interactive",
        requirements: str = "- [x] Acceptance behavior and validation complete.",
    ) -> None:
        if plan_entries is None:
            plan_entries = [(1, "Owner updates", "none"), (2, "Reject non-owners", "none")]
        if ledger_entries is None:
            ledger_entries = [(number, name, "complete") for number, name, _ in plan_entries]
        plan_lines = ["# Implementation Plan: Ownership", "", "## Execution Context"]
        if plan_mode is not None:
            plan_lines.append(f"- Automation mode: {plan_mode}")
        plan_lines.extend([
            "", "## Status Ledger Path", f"- `{self.ledger}`", "", "## Execution Slices",
        ])
        for number, name, checkpoint in plan_entries:
            plan_lines.extend([
                f"{number}. {name}",
                "   - Automated validation: From the root, run the ownership checks.",
                f"   - Manual verification checkpoint: {checkpoint}",
            ])
        self.plan.write_text("\n".join(plan_lines) + "\n", encoding="utf-8")

        values = {
            "Plan": str(self.plan),
            "Automation mode": "interactive",
            "Overall status": "complete",
            "Execution mode": "boundary-driven",
            "Boundary state": "plan_complete",
            "Boundary evidence": "Both ownership acceptance cases passed.",
            "Validation": "Ownership and regression checks passed from the repository root.",
            "Blocker attempts": "none",
            "Unblock condition": "none",
            "Next action": "Review the completed change.",
        }
        for name, value in (metadata or {}).items():
            if value is None:
                values.pop(name, None)
            else:
                values[name] = value
        ledger_lines = ["# Plan Status: Ownership", "", "## Metadata"]
        ledger_lines.extend(f"- {name}: {value}" for name, value in values.items())
        ledger_lines.extend(["", "## Remaining Requirements", requirements, "", "## Slice Status"])
        for number, name, status in ledger_entries:
            ledger_lines.extend([f"{number}. {name}", f"   - Status: `{status}`"])
        self.ledger.write_text("\n".join(ledger_lines) + "\n", encoding="utf-8")

    def check(self, *, error: str | None = None) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIRECTORY / "plan_boundary_check.py"),
             "--plan", str(self.plan), "--ledger", str(self.ledger)],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        if error is None:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn(error, result.stderr)

    def test_complete_plan_is_accepted_in_each_execution_mode(self) -> None:
        for mode in ("boundary-driven", "single-slice", "continuous"):
            with self.subTest(mode=mode):
                self.write_artifacts(metadata={"Execution mode": mode})
                self.check()

    def test_slice_handoff_preserves_pending_slice(self) -> None:
        self.write_artifacts(
            ledger_entries=[(1, "Owner updates", "complete"), (2, "Reject non-owners", "pending")],
            metadata={"Overall status": "in_progress", "Boundary state": "slice_complete",
                      "Next action": "Implement slice 2."},
        )
        self.check()

    def test_missing_extra_renamed_reordered_or_renumbered_slices_are_rejected(self) -> None:
        entries = [
            [(1, "Owner updates", "complete")],
            [(1, "Owner updates", "complete"), (2, "Reject non-owners", "complete"),
             (3, "Unplanned change", "complete")],
            [(1, "Owner updates", "complete"), (2, "Different behavior", "complete")],
            [(2, "Reject non-owners", "complete"), (1, "Owner updates", "complete")],
            [(1, "Owner updates", "complete"), (3, "Reject non-owners", "complete")],
        ]
        for boundary in ("plan_complete", "slice_complete"):
            for ledger_entries in entries:
                with self.subTest(boundary=boundary, entries=ledger_entries):
                    self.write_artifacts(ledger_entries=ledger_entries,
                                         metadata={"Boundary state": boundary})
                    self.check(error="ledger slices must match plan")

    def test_plan_with_duplicate_or_skipped_numbers_is_rejected(self) -> None:
        for number in (1, 3):
            with self.subTest(number=number):
                self.write_artifacts(plan_entries=[(1, "Owner updates", "none"),
                                                    (number, "Reject non-owners", "none")])
                self.check(error="consecutive numbers starting at 1")

    def test_empty_or_missing_slice_sections_are_rejected(self) -> None:
        self.write_artifacts(plan_entries=[])
        self.check(error="plan must define numbered entries")
        self.write_artifacts(ledger_entries=[])
        self.check(error="ledger slices must match plan")

    def test_pending_or_active_slice_prevents_plan_completion(self) -> None:
        for status in ("pending", "in_progress", "blocked", "manual_checkpoint", "cancelled"):
            with self.subTest(status=status):
                self.write_artifacts(ledger_entries=[(1, "Owner updates", "complete"),
                                                     (2, "Reject non-owners", status)])
                self.check(error="every slice status to be `complete`")

    def test_invalid_missing_and_duplicate_slice_status_are_rejected(self) -> None:
        self.write_artifacts(ledger_entries=[(1, "Owner updates", "done"),
                                             (2, "Reject non-owners", "complete")])
        self.check(error="requires one valid Status")
        for replacement in ("", "   - Status: `complete`\n   - Status: `pending`"):
            with self.subTest(replacement=replacement):
                self.write_artifacts()
                text = self.ledger.read_text().replace("   - Status: `complete`", replacement, 1)
                self.ledger.write_text(text)
                self.check(error="requires one valid Status")

    def test_completion_requires_evidence_validation_and_overall_status(self) -> None:
        for metadata, error in (
            ({"Boundary evidence": "none"}, "requires concrete Boundary evidence"),
            ({"Validation": "not run"}, "requires recorded validation results"),
            ({"Overall status": "in_progress"}, "requires Overall status `complete`"),
        ):
            with self.subTest(metadata=metadata):
                self.write_artifacts(metadata=metadata)
                self.check(error=error)

    def test_slice_completion_requires_boundary_evidence(self) -> None:
        self.write_artifacts(metadata={"Boundary state": "slice_complete", "Boundary evidence": "none"})
        self.check(error="slice_complete requires concrete Boundary evidence")

    def test_unchecked_requirement_prevents_completion(self) -> None:
        self.write_artifacts(requirements="- [ ] Verify stored data is unchanged on rejection.")
        self.check(error="unchecked Remaining requirements")

    def test_automation_mode_must_be_present_valid_and_consistent(self) -> None:
        for plan_mode, ledger_mode in ((None, "interactive"), ("interactive", None),
                                       ("afk", "interactive"), ("unexpected", "unexpected")):
            with self.subTest(plan=plan_mode, ledger=ledger_mode):
                self.write_artifacts(plan_mode=plan_mode, metadata={"Automation mode": ledger_mode})
                self.check(error="same Automation mode")

    def test_afk_completion_allows_nonblocking_review_notes(self) -> None:
        self.write_artifacts(plan_mode="afk", metadata={"Automation mode": "afk"})
        self.plan.write_text(self.plan.read_text() + "\n## Review-time manual validation\n"
                             "- Optionally inspect the PR screenshots.\n")
        self.check()

    def test_afk_rejects_planned_blocking_checkpoint(self) -> None:
        self.write_artifacts(plan_mode="afk", metadata={"Automation mode": "afk"},
                             plan_entries=[(1, "Review UI", "Inspect the permission error screen.")])
        self.check(error="AFK mode forbids blocking manual checkpoints")

    def test_interactive_checkpoint_is_accepted_only_for_its_own_slice(self) -> None:
        for checkpoint_slice in (1, 2):
            with self.subTest(checkpoint_slice=checkpoint_slice):
                self.write_artifacts(
                    plan_entries=[(1, "Owner updates", "Inspect screen." if checkpoint_slice == 1 else "none"),
                                  (2, "Reject non-owners", "Inspect screen." if checkpoint_slice == 2 else "none")],
                    ledger_entries=[(1, "Owner updates", "complete"), (2, "Reject non-owners", "manual_checkpoint")],
                    metadata={"Boundary state": "manual_checkpoint", "Overall status": "manual_checkpoint"},
                )
                self.check(error="checkpoint slice must define" if checkpoint_slice == 1 else None)

    def test_afk_cannot_stop_at_manual_checkpoint(self) -> None:
        self.write_artifacts(
            plan_mode="afk",
            ledger_entries=[(1, "Owner updates", "complete"), (2, "Reject non-owners", "manual_checkpoint")],
            metadata={"Automation mode": "afk", "Boundary state": "manual_checkpoint"},
        )
        self.check(error="manual_checkpoint requires interactive")

    def test_hard_blocker_requires_attempts_and_unblock_condition(self) -> None:
        metadata = {"Boundary state": "hard_blocker", "Overall status": "blocked",
                    "Blocker attempts": "Attempted local fixture startup; required service is unavailable.",
                    "Unblock condition": "Restore the local fixture service."}
        entries = [(1, "Owner updates", "complete"), (2, "Reject non-owners", "blocked")]
        self.write_artifacts(ledger_entries=entries, metadata=metadata)
        self.check()
        for field in ("Blocker attempts", "Unblock condition"):
            with self.subTest(field=field):
                self.write_artifacts(ledger_entries=entries, metadata={**metadata, field: "none"})
                self.check(error=f"hard_blocker requires a concrete {field}")

    def test_cancelled_plan_with_remaining_slices_is_accepted(self) -> None:
        self.write_artifacts(
            ledger_entries=[(1, "Owner updates", "cancelled"), (2, "Reject non-owners", "pending")],
            metadata={"Boundary state": "cancelled", "Overall status": "cancelled",
                      "Boundary evidence": "User explicitly cancelled this plan."},
            requirements="- [ ] Finish implementation (cancelled).",
        )
        self.check()

    def test_continuous_mode_rejects_intermediate_slice_handoff(self) -> None:
        self.write_artifacts(metadata={"Execution mode": "continuous", "Boundary state": "slice_complete"})
        self.check(error="slice_complete handoff is not allowed in continuous mode")

    def test_active_boundary_cannot_end_turn(self) -> None:
        self.write_artifacts(metadata={"Boundary state": "active"})
        self.check(error="Boundary state must be")

    def test_code_examples_do_not_supply_control_fields_or_slices(self) -> None:
        self.write_artifacts()
        self.plan.write_text(self.plan.read_text() + "\n```markdown\n## Execution Slices\n"
                             "1. Example only\n```\n")
        self.ledger.write_text(self.ledger.read_text() + "\n~~~markdown\n3. Example only\n"
                               "   - Status: `in_progress`\n- [ ] Example requirement\n~~~\n")
        self.check()

    def test_stop_hook_blocks_omitted_slice_and_accepts_corrected_ledger(self) -> None:
        transcript = self.root / "transcript.jsonl"
        transcript.write_text(json.dumps({"type": "event_msg", "payload": {
            "type": "user_message", "message": f"$implement-plan {self.plan}",
        }}) + "\n")
        for omitted in (True, False):
            with self.subTest(omitted=omitted):
                entries = [(1, "Owner updates", "complete")] if omitted else None
                self.write_artifacts(ledger_entries=entries)
                result = subprocess.run(
                    [sys.executable, str(SCRIPT_DIRECTORY / "stop_guard.py")],
                    input=json.dumps({"transcript_path": str(transcript), "cwd": str(self.root)}),
                    capture_output=True, text=True, check=False, timeout=10,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                response = json.loads(result.stdout)
                if omitted:
                    self.assertEqual(response["decision"], "block")
                    self.assertIn("ledger slices must match plan", response["reason"])
                else:
                    self.assertTrue(response["continue"])


if __name__ == "__main__":
    unittest.main()
