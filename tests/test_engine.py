import copy
import unittest
from pathlib import Path
from auditlab.engine import audit, load_records

SAMPLE = Path(__file__).resolve().parents[1] / "examples" / "synthetic_claims.json"


class AuditEngineTests(unittest.TestCase):
    def setUp(self):
        self.data = load_records(SAMPLE)

    def test_sample_detects_mismatch(self):
        r = audit(self.data)
        issues = r["claim_results"][1]["issues"]
        self.assertIn("REGIME_MISMATCH", [x["code"] for x in issues])
        self.assertIn("UNSUPPORTED_ASSUMPTION_CLOSURE", [x["code"] for x in issues])

    def test_missing_evidence_flagged(self):
        r = audit(self.data)
        self.assertIn("STRONG_CLAIM_WITHOUT_REVIEWED_MATCHED_EVIDENCE",
                      [x["code"] for x in r["claim_results"][2]["issues"]])

    def test_no_claim_automatically_verified(self):
        r = audit(self.data)
        self.assertTrue(all(x["automatically_verified"] is False for x in r["claim_results"]))
        self.assertIsNone(r["verified_empirical_reduction"])

    def test_withdrawal_not_closure(self):
        r = audit(self.data)
        self.assertEqual(r["structurally_eligible_closures_not_verified"], 1)
        self.assertEqual(r["withdrawn_from_scope_not_verified"], 1)
        self.assertEqual(r["remaining_not_structurally_closed"], 2)

    def test_unreviewed_cannot_close(self):
        data = copy.deepcopy(self.data)
        data["claims"][0]["evidence"][0]["reviewed"] = False
        r = audit(data)
        self.assertEqual(r["structurally_eligible_closures_not_verified"], 0)

    def test_no_derivation_for_proven_claim(self):
        data = copy.deepcopy(self.data)
        data["claims"][0]["evidence"][0]["kind"] = "publication"
        r = audit(data)
        self.assertIn("PROOF_ASSERTED_WITHOUT_MATCHED_DERIVATION",
                      [x["code"] for x in r["claim_results"][0]["issues"]])

    def test_duplicate_claim_rejected(self):
        data = copy.deepcopy(self.data)
        data["claims"].append(copy.deepcopy(data["claims"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate claim"):
            audit(data)

    def test_duplicate_evidence_rejected(self):
        data = copy.deepcopy(self.data)
        data["claims"][0]["evidence"].append(copy.deepcopy(data["claims"][0]["evidence"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate evidence"):
            audit(data)

    def test_incorrect_boolean_rejected(self):
        data = copy.deepcopy(self.data)
        data["claims"][0]["evidence"][0]["reviewed"] = "yes"
        with self.assertRaisesRegex(ValueError, "boolean"):
            audit(data)

    def test_no_assay_reduction_target_is_forced(self):
        r = audit(self.data)
        self.assertNotIn("target_met", r)
        self.assertNotIn("assay_reduction_percent", r)


if __name__ == "__main__":
    unittest.main()
