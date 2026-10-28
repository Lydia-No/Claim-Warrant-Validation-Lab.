"""Tests for the *pilot tooling*, not tests of external evidence validity."""
import copy
import json
import unittest
from pathlib import Path

from auditlab.pilot import assess, _metrics_with_abstain

BASE = Path(__file__).resolve().parents[1] / "pilot" / "demo"


class PilotScorerTests(unittest.TestCase):
    def setUp(self):
        def load(name):
            return json.loads((BASE / name).read_text(encoding="utf-8"))
        self.cases = load("cases.json")
        self.a = load("ratings_a.json")
        self.b = load("ratings_b.json")
        self.g = load("generic_predictions.json")

    def test_reproducible_synthetic_demo(self):
        a = assess(self.cases, self.a, self.b, self.g)
        b = assess(copy.deepcopy(self.cases), copy.deepcopy(self.a),
                   copy.deepcopy(self.b), copy.deepcopy(self.g))
        self.assertEqual(a, b)
        self.assertEqual(a["cases_total"], 6)

    def test_unresolved_and_disagreed_are_excluded(self):
        output = assess(self.cases, self.a, self.b, self.g)
        self.assertEqual(output["raw_exact_agreement"], 5)
        self.assertEqual(output["adjudication_disagreements"], ["DEMO-05"])
        self.assertEqual(output["both_uncertain"], ["DEMO-06"])
        self.assertEqual(output["eligible_agreed_determinate_cases"], 4)
        self.assertEqual(output["excluded_from_primary"], ["DEMO-05", "DEMO-06"])

    def test_risk_engine_can_fail_on_semantic_shift(self):
        output = assess(self.cases, self.a, self.b, self.g)
        item = next(x for x in output["case_reports"] if x["case_id"] == "DEMO-03")
        self.assertEqual(item["targeted_revision"], "no")
        self.assertTrue(item["eligible_for_primary"])

    def test_baselines_and_engine_are_scored_separately(self):
        output = assess(self.cases, self.a, self.b, self.g)
        engine = output["systems"]["targeted_revision_engine"]
        generic = output["systems"]["generic_full_record_critic"]
        self.assertEqual((engine["tp"], engine["fp"], engine["fn"], engine["tn"]), (1, 1, 1, 1))
        self.assertEqual((generic["tp"], generic["fp"], generic["fn"], generic["tn"]), (2, 0, 0, 2))

    def test_abstention_is_not_no(self):
        score = _metrics_with_abstain([True, False], ["abstain", "no"])
        self.assertEqual(score["scored"], 1)
        self.assertEqual(score["abstained"], 1)
        self.assertEqual(score["coverage"], 0.5)
        self.assertEqual(score["fn"], 0)

    def test_missing_generic_prediction_rejected(self):
        self.g["predictions"].pop()
        with self.assertRaisesRegex(ValueError, "case IDs differ"):
            assess(self.cases, self.a, self.b, self.g)

    def test_duplicate_ratings_rejected(self):
        self.a["ratings"].append(copy.deepcopy(self.a["ratings"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate case_id"):
            assess(self.cases, self.a, self.b, self.g)

    def test_invalid_reviewer_label_rejected(self):
        self.b["ratings"][0]["label"] = "probably"
        with self.assertRaisesRegex(ValueError, "invalid label"):
            assess(self.cases, self.a, self.b, self.g)

    def test_invalid_generic_label_rejected(self):
        self.g["predictions"][0]["decision"] = "probably"
        with self.assertRaisesRegex(ValueError, "invalid decision"):
            assess(self.cases, self.a, self.b, self.g)

    def test_all_disagreement_does_not_create_positive_results(self):
        for x in self.b["ratings"]:
            x["label"] = "uncertain"
        output = assess(self.cases, self.a, self.b, self.g)
        self.assertEqual(output["eligible_agreed_determinate_cases"], 0)
        self.assertIsNone(output["systems"]["targeted_revision_engine"]["precision"])
        self.assertIsNone(output["systems"]["generic_full_record_critic"]["coverage"])

    def test_swapped_unknown_case_rejected(self):
        self.cases["cases"][0].pop("after")
        with self.assertRaisesRegex(ValueError, "before and after"):
            assess(self.cases, self.a, self.b, self.g)

    def test_unsupported_claim_does_not_become_proven(self):
        report = assess(self.cases, self.a, self.b, self.g)
        self.assertIn("No claim of statistical significance", report["caveats"][2])


if __name__ == "__main__":
    unittest.main()
