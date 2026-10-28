import copy
import json
import unittest
from pathlib import Path

from auditlab.benchmark import evaluate, metrics, RECHECK_CODES
from auditlab.compare import compare

FIXTURE = Path(__file__).resolve().parents[1] / "benchmarks" / "revision_challenge" / "cases.json"


class SyntheticBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_dataset_is_balanced_enough_for_a_smoke_challenge(self):
        n = len(self.dataset["cases"])
        positives = sum(x["expected_review_required"] for x in self.dataset["cases"])
        self.assertGreaterEqual(n, 20)
        self.assertGreaterEqual(positives, 8)
        self.assertGreaterEqual(n - positives, 8)

    def test_same_results_under_repeated_evaluation(self):
        self.assertEqual(evaluate(self.dataset), evaluate(copy.deepcopy(self.dataset)))

    def test_all_comparators_are_reported(self):
        report = evaluate(self.dataset)
        self.assertEqual(set(report["systems"]), {
            "snapshot_only_review", "any_field_diff_review", "targeted_revision_review"
        })
        for result in report["systems"].values():
            self.assertEqual(sum(result[k] for k in ("tp", "fp", "tn", "fn")),
                             len(self.dataset["cases"]))

    def test_no_inference_of_external_superiority(self):
        self.assertIn("no empirical evidence", evaluate(self.dataset)["claim"])

    def test_known_semantic_shift_miss_is_preserved(self):
        report = evaluate(self.dataset)
        case = next(x for x in report["cases"] if x["id"] == "R16")
        self.assertTrue(case["expected_review_required"])
        self.assertFalse(case["targeted_revision_review"])
        self.assertIn("CLAIM_TEXT_CHANGED", case["all_revision_events"])

    def test_cosmetic_doi_case_is_reported_as_false_alarm(self):
        report = evaluate(self.dataset)
        case = next(x for x in report["cases"] if x["id"] == "N08")
        self.assertFalse(case["expected_review_required"])
        self.assertTrue(case["targeted_revision_review"])

    def test_numeric_bound_change_is_caught(self):
        report = evaluate(self.dataset)
        risk = next(x for x in report["cases"] if x["id"] == "R17")
        self.assertIn("NUMERIC_CLAIM_LITERAL_CHANGED_REQUIRES_REVIEW", risk["trigger_codes"])
        neutral = next(x for x in report["cases"] if x["id"] == "N11")
        self.assertFalse(neutral["targeted_revision_review"])

    def test_changed_bibliography_is_caught(self):
        report = evaluate(self.dataset)
        case = next(x for x in report["cases"] if x["id"] == "R08")
        self.assertIn("BIBLIOGRAPHIC_METADATA_CHANGED", case["trigger_codes"])

    def test_empty_metrics_do_not_invent_rates(self):
        m = metrics([], [])
        self.assertIsNone(m["precision"])
        self.assertIsNone(m["recall"])
        self.assertIsNone(m["specificity"])

    def test_invalid_truth_label_is_rejected(self):
        broken = copy.deepcopy(self.dataset)
        broken["cases"][0]["expected_review_required"] = "true"
        with self.assertRaisesRegex(ValueError, "boolean"):
            evaluate(broken)


if __name__ == "__main__":
    unittest.main()
