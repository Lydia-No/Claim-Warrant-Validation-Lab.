import copy
import json
import unittest
from auditlab.readiness import LEDGER, DOSSIERS, assess_readiness


class ReadinessGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = json.loads(DOSSIERS.read_text(encoding="utf-8"))
        cls.ledger = json.loads(LEDGER.read_text(encoding="utf-8"))

    def check(self, sources=None, ledger=None):
        return assess_readiness(
            sources if sources is not None else self.sources,
            ledger if ledger is not None else self.ledger)

    def test_three_histories_structurally_valid_but_no_external_warrant(self):
        result = self.check()
        self.assertEqual(result["dossiers_checked"], 3)
        self.assertEqual(result["mechanically_valid_source_histories"], 3)
        self.assertEqual(result["independently_source_verified_histories"], 0)
        self.assertEqual(result["established_matched_terminal_pairs"], 0)
        self.assertEqual(result["eligible_for_external_effectiveness_claims"], 0)
        self.assertFalse(result["originality_established"])

    def test_no_claim_about_scientific_truth_from_metadata(self):
        result = self.check()
        self.assertTrue(all(c["scientific_warrant_established"] is None for c in result["cases"]))
        self.assertTrue(all(not c["ready_for_comparative_performance_test"]
                            for c in result["cases"]))

    def test_author_cannot_flip_human_review_to_pass(self):
        altered = copy.deepcopy(self.ledger)
        altered["cases"][0]["statuses"]["source_support_independently_checked"] = "documented_in_record"
        with self.assertRaisesRegex(ValueError, "cannot be self-certified"):
            self.check(ledger=altered)

    def test_author_cannot_invent_matched_terminal_control(self):
        altered = copy.deepcopy(self.ledger)
        altered["cases"][0]["statuses"]["same_terminal_comparator"] = "documented_in_record"
        with self.assertRaisesRegex(ValueError, "cannot be self-certified"):
            self.check(ledger=altered)

    def test_author_cannot_invent_generic_baseline(self):
        altered = copy.deepcopy(self.ledger)
        altered["cases"][2]["statuses"]["equal_information_generic_baseline"] = "documented_in_record"
        with self.assertRaisesRegex(ValueError, "cannot be self-certified"):
            self.check(ledger=altered)

    def test_all_candidate_ids_must_be_preserved(self):
        altered = copy.deepcopy(self.ledger)
        altered["cases"].pop()
        with self.assertRaisesRegex(ValueError, "diverge"):
            self.check(ledger=altered)

    def test_unknown_extra_criterion_rejected(self):
        altered = copy.deepcopy(self.ledger)
        altered["criteria"].append({"id": "guaranteed_success", "required_for_comparative_test": True})
        with self.assertRaisesRegex(ValueError, "Unexpected/absent"):
            self.check(ledger=altered)

    def test_missing_scope_note_rejected(self):
        altered = copy.deepcopy(self.ledger)
        altered["cases"][0]["scope_note"] = ""
        with self.assertRaisesRegex(ValueError, "scope"):
            self.check(ledger=altered)

    def test_future_source_does_not_pass_prerequisites(self):
        altered = copy.deepcopy(self.sources)
        altered["cases"][0]["stages"][0]["source_ids"].append("DEBT-E3")
        with self.assertRaisesRegex(ValueError, "future evidence"):
            self.check(sources=altered)

    def test_arbitrary_unknown_status_is_not_accepted(self):
        altered = copy.deepcopy(self.ledger)
        altered["cases"][1]["statuses"]["independent_reference_ratings"] = "probably"
        with self.assertRaisesRegex(ValueError, "unsupported status"):
            self.check(ledger=altered)


if __name__ == "__main__":
    unittest.main()
