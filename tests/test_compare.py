import copy
import unittest
from pathlib import Path
from auditlab.engine import load_records
from auditlab.compare import compare

BASE = Path(__file__).resolve().parents[1] / "examples"


class CompareTests(unittest.TestCase):
    def setUp(self):
        self.before = load_records(BASE / "synthetic_revision_before.json")
        self.after = load_records(BASE / "synthetic_revision_after.json")

    def test_paired_revision_flags_laundering(self):
        r = compare(self.before, self.after)
        codes = [e["code"] for e in r["events"]]
        for code in (
            "ASSERTED_STATUS_UPGRADED_NOT_PROVEN",
            "REVIEW_STATUS_SELF_UPGRADED",
            "APPLICABILITY_SELF_UPGRADED",
            "NEW_CLOSURE_ASSERTION_NOT_VERIFIED",
            "NEW_ASSUMPTION_INTRODUCED",
            "CLAIM_REMOVED_NOT_VERIFIED",
            "ASSUMPTION_REMOVED_NOT_CLOSED",
            "CLAIM_ADDED_REQUIRES_REVIEW",
        ):
            self.assertIn(code, codes)

    def test_stable_hash_and_no_empirical_claim(self):
        a = compare(self.before, self.after)
        b = compare(copy.deepcopy(self.before), copy.deepcopy(self.after))
        self.assertEqual(a["before_content_sha256"], b["before_content_sha256"])
        self.assertIsNone(a["verified_empirical_reduction"])

    def test_identical_records_have_zero_events(self):
        r = compare(self.before, copy.deepcopy(self.before))
        self.assertEqual(r["event_count"], 0)

    def test_reused_evidence_id_flagged(self):
        after = copy.deepcopy(self.before)
        after["claims"][0]["evidence"][0]["locator"] = "synthetic://different-artifact"
        r = compare(self.before, after)
        self.assertIn("EVIDENCE_ID_REUSED_FOR_DIFFERENT_SOURCE",
                      [x["code"] for x in r["events"]])

    def test_assumption_renamed_under_same_id_flagged(self):
        after = copy.deepcopy(self.before)
        after["claims"][0]["assumptions"][0]["description"] = "Entirely different condition"
        r = compare(self.before, after)
        self.assertIn("ASSUMPTION_MEANING_CHANGED",
                      [x["code"] for x in r["events"]])

    def test_invalid_duplicate_claim_rejected(self):
        after = copy.deepcopy(self.after)
        after["claims"].append(copy.deepcopy(after["claims"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate claim"):
            compare(self.before, after)


if __name__ == "__main__":
    unittest.main()
