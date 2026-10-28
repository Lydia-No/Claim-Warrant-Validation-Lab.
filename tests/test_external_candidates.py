import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlparse

MANIFEST = Path(__file__).resolve().parents[1] / "pilot" / "external_candidates" / "CANDIDATES.json"

class ExternalCandidateRegisterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.rows = cls.dataset["candidates"]

    def test_ten_source_candidates_two_projects(self):
        self.assertEqual(len(self.rows), 10)
        self.assertEqual({r["repository"] for r in self.rows}, {"scipy/scipy", "pytorch/pytorch"})
        self.assertEqual(sum(r["repository"] == "scipy/scipy" for r in self.rows), 5)

    def test_all_references_have_immutable_hashes(self):
        seen = set()
        for row in self.rows:
            self.assertNotIn(row["case_id"], seen)
            seen.add(row["case_id"])
            for name in ("before_ref", "after_ref"):
                self.assertRegex(row[name], r"^[0-9a-f]{40}$")
            self.assertNotEqual(row["before_ref"], row["after_ref"])

    def test_access_and_diff_were_prechecked(self):
        for row in self.rows:
            self.assertIs(row["verified_public_before_after_access"], True)
            self.assertIs(row["verified_changed_at_selected_path"], True)
            self.assertIs(row["candidate_only"], True)
            self.assertIn(f"/blob/{row['before_ref']}/", row["before_url"])
            self.assertIn(f"/blob/{row['after_ref']}/", row["after_url"])

    def test_does_not_include_claim_truth_or_reviewer_labels(self):
        forbidden = {"expected_review_required", "reviewer_rating", "truth_label",
                     "reviewer_labels", "assessed_correct", "predicted_outcome"}
        for row in self.rows:
            self.assertFalse(forbidden & set(row), row["case_id"])
            self.assertNotIn("before", row)
            self.assertNotIn("after", row)
        self.assertIn("NOT BLINDED", self.dataset["status"])

    def test_only_expected_upstream_domains(self):
        for row in self.rows:
            for key in ("pr_url", "before_url", "after_url"):
                self.assertEqual(urlparse(row[key]).netloc, "github.com")
                self.assertIn(f"/{row['repository']}/", row[key])

    def test_manifest_explicitly_rejects_confirmatory_inference(self):
        text = self.dataset["selection_method"].lower()
        self.assertIn("convenience", text)
        self.assertIn("not representative", text)


if __name__ == "__main__":
    unittest.main()
