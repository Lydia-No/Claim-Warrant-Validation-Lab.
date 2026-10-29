"""Synthetic-only regression tests for optional local-first extension."""
import copy
import unittest
from auditlab.claim_extract import extract_claim_candidates
from auditlab.arithmetic import check_arithmetic
from auditlab.warrants import assess_warrants
from auditlab.extensions import inspect_records, compare_record_extensions


def specimen():
    return {"claims": [
        {"id": "C-BASE", "statement": "An example calculation is consistent",
         "asserted_status": "supported",
         "required_evidence_scopes": ["principle", "performance"],
         "evidence": [
             {"id": "E-1", "kind": "publication", "locator": "synthetic://record-1",
              "reviewed": False, "applicability": "unknown",
              "declared_support_scopes": ["principle"]}
         ], "assumptions": [],
         "arithmetic_checks": [
             {"id": "M-1", "operation": "product", "values": [65537, 65539],
              "expected": 4295229443},
             {"id": "M-2", "operation": "sum", "values": [2, 4], "expected": 7}
         ]},
        {"id": "C-DOWNSTREAM", "statement": "A derived numerical claim",
         "asserted_status": "hypothesis", "evidence": [], "assumptions": [],
         "required_evidence_scopes": [], "depends_on": ["C-BASE"]}
    ]}


class ExtensionTests(unittest.TestCase):
    def test_extractor_preserves_lines_without_interpreting_claims(self):
        data = "Before [CLAIM-FOO-001] and [CLAIM-FOO-001]\n" + (
            "```\n[CLAIM-FAKE-003]\n```\n") + "[CLAIM-BAR-002]"
        r = extract_claim_candidates(data)
        self.assertEqual(r["candidate_count"], 2)
        self.assertEqual(r["claims"]["CLAIM-FOO-001"], [1])
        self.assertTrue(r["candidate_only"])

    def test_arithmetic_detects_mismatch_without_verification(self):
        r = inspect_records(specimen())
        results = r["literal_arithmetic"]["C-BASE"]["results"]
        self.assertEqual(results[0]["status"], "match")
        self.assertEqual(results[1]["status"], "mismatch")
        self.assertFalse(r["automatically_verified"])

    def test_missing_scope_not_promoted(self):
        r = assess_warrants(specimen())
        issues = [x["code"] for x in r["claim_results"]["C-BASE"]["issues"]]
        self.assertIn("REQUIRED_SCOPE_WITHOUT_DECLARED_SUPPORT", issues)
        self.assertIn("DECLARED_SCOPE_REQUIRES_REVIEW", issues)
        self.assertIn("PROVENANCE_NOT_RECORDED", issues)

    def test_dependency_uncertainty_propagated(self):
        r = assess_warrants(specimen())
        self.assertIn("C-BASE", r["claim_results"]["C-DOWNSTREAM"]["upstream_review_required"])

    def test_reviewed_match_still_not_scientifically_verified(self):
        d = specimen()
        ev = d["claims"][0]["evidence"][0]
        ev.update({"reviewed": True, "applicability": "matched",
                   "declared_support_scopes": ["principle", "performance"],
                   "provenance": {"source_id": "S-1", "record_id": "R-1"}})
        r = assess_warrants(d)
        self.assertFalse(r["claim_results"]["C-BASE"]["automatically_verified"])

    def test_malformed_scope_fails_closed(self):
        d = specimen()
        d["claims"][0]["required_evidence_scopes"] = ["magic"]
        with self.assertRaises(ValueError):
            assess_warrants(d)

    def test_missing_dependency_flagged(self):
        d = specimen()
        d["claims"][1]["depends_on"] = ["NOT-A-CLAIM"]
        issues = assess_warrants(d)["claim_results"]["C-DOWNSTREAM"]["issues"]
        self.assertIn("UNKNOWN_DEPENDENCY", [x["code"] for x in issues])

    def test_cycle_is_reported_not_certified(self):
        d = specimen()
        d["claims"][0]["depends_on"] = ["C-DOWNSTREAM"]
        r = assess_warrants(d)
        self.assertIn("DEPENDENCY_CYCLE_REQUIRES_REVIEW",
                      [x["code"] for x in r["claim_results"]["C-BASE"]["issues"]])

    def test_revision_metadata_change_is_not_proof(self):
        a, b = specimen(), specimen()
        b["claims"][0]["required_evidence_scopes"] = ["principle"]
        b["claims"][0]["evidence"][0]["declared_support_scopes"] = ["principle", "method"]
        r = compare_record_extensions(a, b)
        self.assertEqual(r["event_count"], 2)
        self.assertIn("Metadata changes", r["limit"])

    def test_unknown_operator_fails_closed(self):
        r = check_arithmetic([{"id": "X", "operation": "eval", "values": [3, 4], "expected": 12}])
        self.assertEqual(r["results"][0]["status"], "not_evaluated")

    def test_coprime_pairs(self):
        r = check_arithmetic([{"id": "X", "operation": "pairwise_coprime",
                               "values": [5, 8, 9], "expected": True}])
        self.assertEqual(r["results"][0]["status"], "match")


if __name__ == "__main__":
    unittest.main()
