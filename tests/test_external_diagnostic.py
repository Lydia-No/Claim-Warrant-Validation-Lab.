"""Regression tests for descriptive diagnostics, not external ground truth."""
import copy
import json
import unittest
from pathlib import Path
from auditlab.external_diagnostic import diagnose

FIXTURE = (Path(__file__).resolve().parents[1] / "pilot"
           / "external_candidates" / "EXTRACTED-PAIRS.json")


class UnblindedDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_nine_source_pinned_pairs(self):
        self.assertEqual(diagnose(self.data)["case_count"], 9)

    def test_no_external_metric_is_computed(self):
        report = diagnose(self.data)
        self.assertIs(report["metric_eligible"], False)
        for key in ("precision", "recall", "specificity"):
            self.assertIsNone(report[key])
        self.assertTrue(all(x["human_ground_truth"] is None for x in report["cases"]))
        self.assertTrue(all(x["source_correctness_verified"] is False for x in report["cases"]))

    def test_fixed_rule_outputs_recorded_without_truth_labels(self):
        report = diagnose(self.data)
        by_id = {x["case_id"]: x for x in report["cases"]}
        self.assertTrue(by_id["SCIPY-17922"]["fixed_rules_request_review"])
        self.assertFalse(by_id["PYTORCH-7383"]["fixed_rules_request_review"])
        self.assertTrue(by_id["PYTORCH-7383"]["unflagged_materiality_unknown"])

    def test_pure_formatting_controls_not_invented_as_verified(self):
        report = diagnose(self.data)
        by_id = {x["case_id"]: x for x in report["cases"]}
        for cid in ("PYTORCH-5679", "PYTORCH-134704"):
            self.assertFalse(by_id[cid]["record_text_changed_or_added"])
            self.assertFalse(by_id[cid]["source_correctness_verified"])

    def test_added_claim_is_detected(self):
        result = diagnose(self.data)
        row = next(x for x in result["cases"] if x["case_id"] == "SCIPY-24518")
        self.assertIn("CLAIM_ADDED_REQUIRES_REVIEW", row["trigger_codes"])

    def test_evidence_is_not_fabricated(self):
        data = copy.deepcopy(self.data)
        data["cases"][0]["after"]["claims"][0]["evidence"] = [{
            "id": "E01", "kind": "publication", "locator": "synthetic://not-real",
            "reviewed": True, "applicability": "matched",
        }]
        with self.assertRaisesRegex(ValueError, "expected unassessed"):
            diagnose(data)

    def test_rated_cases_rejected(self):
        data = copy.deepcopy(self.data)
        data["cases"][0]["phase"] = "independently_adjudicated"
        with self.assertRaisesRegex(ValueError, "must not be rated"):
            diagnose(data)

    def test_duplicate_case_ids_rejected(self):
        data = copy.deepcopy(self.data)
        data["cases"].append(copy.deepcopy(data["cases"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate case_id"):
            diagnose(data)


if __name__ == "__main__":
    unittest.main()
