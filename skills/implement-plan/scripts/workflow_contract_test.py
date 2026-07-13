from pathlib import Path
import unittest


AGENTS_ROOT = Path(__file__).resolve().parents[3]


class WorkflowContractTest(unittest.TestCase):
    def test_create_plan_distinguishes_afk_and_interactive_checkpoints(self) -> None:
        contract = (AGENTS_ROOT / "skills/create-plan/SKILL.md").read_text()

        self.assertIn("Automation mode: afk", contract)
        self.assertIn("Never create a `manual_checkpoint` slice state", contract)
        self.assertIn("## Review-time manual validation", contract)
        self.assertIn("compatible with `plan_complete`", contract)
        self.assertIn("In `interactive` mode", contract)
        self.assertIn("may use `manual_checkpoint`", contract)

    def test_implement_plan_owns_all_report_boundaries(self) -> None:
        contract = (AGENTS_ROOT / "skills/implement-plan/SKILL.md").read_text()

        tags = [
            "<turnSummary>...</turnSummary>",
            "<turnErrors>...</turnErrors>",
            "<automatedValidation>...</automatedValidation>",
            "<manualValidation>...</manualValidation>",
            "<remainingSlices>...</remainingSlices>",
        ]
        positions = [contract.index(tag) for tag in tags]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("completed slice with another autonomous slice", contract)
        self.assertIn("interactive `manual_checkpoint`", contract)
        self.assertIn("`plan_complete`", contract)
        self.assertIn("AFK review-time checks", contract)
        self.assertIn("standalone skill use", contract)
        self.assertIn("Never put “no slices remain,”", contract)


if __name__ == "__main__":
    unittest.main()
