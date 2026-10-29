import copy
import json
import unittest
from pathlib import Path
from auditlab.external_preflight import preflight
from auditlab.compare import compare

BASE = Path(__file__).resolve().parents[1] / "pilot" / "external_candidates"


class ExternalPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register = json.loads((BASE/"CANDIDATES.json").read_text())
        cls.extraction = json.loads((BASE/"EXTRACTED-PAIRS.json").read_text())
        cls.selection = json.loads((BASE/"SELECTION-LEDGER.json").read_text())

    def run_check(self, register=None, extracted=None, selection=None):
        return preflight(register if register is not None else self.register,
                         extracted if extracted is not None else self.extraction,
                         selection if selection is not None else self.selection)

    def test_all_ten_candidates_preserved(self):
        report = self.run_check()
        self.assertEqual(report["registered_candidates"], 10)
        self.assertEqual(report["extracted_pairs"], 9)
        self.assertEqual(report["excluded_candidates"], 1)

    def test_added_equivalence_not_backfilled_into_before(self):
        report = self.run_check()
        self.assertEqual(report["new_claim_ids_in_after"], 1)
        row = next(x for x in self.extraction["cases"] if x["case_id"] == "SCIPY-24518")
        self.assertEqual(len(row["before"]["claims"]), 1)
        self.assertEqual(len(row["after"]["claims"]), 2)

    def test_unknown_source_truth_is_never_reported_as_checked(self):
        report = self.run_check()
        self.assertEqual(report["original_documents_rechecked_by_independent_reviewer"], 0)
        self.assertEqual(report["external_comparative_effectiveness_results"], 0)

    def test_source_shas_are_crosschecked(self):
        data = copy.deepcopy(self.extraction)
        data["cases"][0]["source"]["before_ref"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "source pointer"):
            self.run_check(extracted=data)

    def test_no_ratings_in_case_data(self):
        data = copy.deepcopy(self.extraction)
        data["cases"][0]["human_rating"] = "yes"
        with self.assertRaisesRegex(ValueError, "outcome or rating"):
            self.run_check(extracted=data)

    def test_no_invented_reviewed_evidence(self):
        data = copy.deepcopy(self.extraction)
        data["cases"][0]["before"]["claims"][0]["evidence"] = [{"id":"E","kind":"experiment",
                  "locator":"synthetic://invented", "reviewed":True,"applicability":"matched"}]
        with self.assertRaisesRegex(ValueError, "fabricated"):
            self.run_check(extracted=data)

    def test_inclusion_ledger_is_not_overwritten(self):
        data = copy.deepcopy(self.selection)
        data["entries"][0]["treatment"] = "exclude_textual_claim_study"
        with self.assertRaisesRegex(ValueError, "frozen selection"):
            self.run_check(selection=data)

    def test_machine_readable_pairs_can_be_compared_without_scoring(self):
        for case in self.extraction["cases"]:
            result = compare(case["before"], case["after"])
            self.assertIsNone(result["verified_empirical_reduction"])
            self.assertNotIn("scientific_verification", result)

    def test_formatting_controls_use_identical_claim_paraphrases(self):
        for cid in ("PYTORCH-5679", "PYTORCH-134704"):
            row = next(x for x in self.extraction["cases"] if x["case_id"] == cid)
            self.assertEqual(row["before"]["claims"][0]["statement"],
                             row["after"]["claims"][0]["statement"])

    def test_cannot_call_internal_curator_labels_external_ground_truth(self):
        for row in self.extraction["cases"]:
            self.assertEqual(row["phase"], "UNBLINDED_EXTERNAL_SOURCE_EXTRACTION_NOT_RATED")
            self.assertIs(row["extraction"]["scientific_truth_assessed"], False)


if __name__ == "__main__":
    unittest.main()
