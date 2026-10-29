"""Time-order and provenance-reference tests. No claims about scientific truth."""
import copy
import json
import unittest
from pathlib import Path
from auditlab.evidence_chains import DEFAULT, validate_chains


class EvidenceChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DEFAULT.read_text(encoding="utf-8"))

    def checked(self, data=None):
        return validate_chains(self.data if data is None else data)

    def test_three_independent_historical_topics(self):
        x = self.checked()
        self.assertEqual(x["case_count"], 3)
        self.assertEqual(x["stage_count"], 10)
        self.assertEqual(x["linked_source_records"], 10)
        self.assertEqual(x["assumption_questions"], 11)

    def test_no_false_independent_review_claim(self):
        r = self.checked()
        self.assertEqual(r["independent_domain_reproduction"], 0)
        self.assertEqual(r["independent_reviewer_ratings"], 0)
        self.assertEqual(r["comparative_validity_findings"], 0)

    def test_future_source_usage_is_rejected(self):
        d = copy.deepcopy(self.data)
        d["cases"][0]["stages"][0]["source_ids"].append("DEBT-E3")
        with self.assertRaisesRegex(ValueError, "future evidence"):
            self.checked(d)

    def test_out_of_order_stages_rejected(self):
        d = copy.deepcopy(self.data)
        d["cases"][0]["stages"][1]["as_of"] = "2009-01-01"
        with self.assertRaisesRegex(ValueError, "chronological"):
            self.checked(d)

    def test_unknown_source_rejected(self):
        d = copy.deepcopy(self.data)
        d["cases"][0]["stages"][0]["source_ids"] = ["DEBT-NO"]
        with self.assertRaisesRegex(ValueError, "unknown evidence"):
            self.checked(d)

    def test_unknown_assumption_rejected(self):
        d = copy.deepcopy(self.data)
        d["cases"][0]["stages"][0]["active_assumption_ids"] = ["DEBT-UNKNOWN"]
        with self.assertRaisesRegex(ValueError, "unknown assumption"):
            self.checked(d)

    def test_duplicate_stage_rejected(self):
        d = copy.deepcopy(self.data)
        d["cases"][1]["stages"][1]["id"] = d["cases"][1]["stages"][0]["id"]
        with self.assertRaisesRegex(ValueError, "stage ID"):
            self.checked(d)

    def test_duplicate_evidence_rejected(self):
        d = copy.deepcopy(self.data)
        d["cases"][2]["evidence"][1]["id"] = d["cases"][2]["evidence"][0]["id"]
        with self.assertRaisesRegex(ValueError, "evidence ID"):
            self.checked(d)

    def test_non_https_source_rejected(self):
        d = copy.deepcopy(self.data)
        d["cases"][2]["evidence"][0]["url"] = "http://insecure.invalid"
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            self.checked(d)

    def test_claim_certification_field_rejected(self):
        d = copy.deepcopy(self.data)
        d["cases"][0]["verified_scientifically"] = True
        with self.assertRaisesRegex(ValueError, "forbidden"):
            self.checked(d)

    def test_unrecorded_residual_question_rejected(self):
        d = copy.deepcopy(self.data)
        d["cases"][1]["residual_question"] = ""
        with self.assertRaisesRegex(ValueError, "residual"):
            self.checked(d)

    def test_no_source_can_time_travel(self):
        result = self.checked()
        d = {x["case_id"]: x for x in result["cases"]}
        self.assertEqual(d["OPERA-2011-2012"]["source_additions_by_stage"]["OPERA-S2"], ["OPERA-E2"])
        self.assertEqual(d["BICEP2-2014-2015"]["source_additions_by_stage"]["BICEP-S3"], ["BICEP-E3"])


if __name__ == "__main__":
    unittest.main()
