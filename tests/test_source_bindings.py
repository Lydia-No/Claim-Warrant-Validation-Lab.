import hashlib
import tempfile
import unittest
from pathlib import Path

from auditlab.source_bindings import verify_sources
from auditlab.reviewer_panel import review_source_bindings
from auditlab.source_revision import source_revision_events
import copy


class SourcePilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.text = "A fictional note says that two and three total five.\n"
        (self.root / "note.txt").write_text(self.text, encoding="utf-8")
        self.records = {"claims": [{"id": "C1", "statement": "An illustrative sum is five.",
             "asserted_status": "hypothesis", "assumptions": [],
             "evidence": [{"id": "E1", "kind": "publication", "locator": "synthetic://x",
                            "reviewed": False, "applicability": "unknown",
                            "declared_support_scopes": ["principle"]}]}]}
        self.bundle = {
            "sources": [{"source_id": "S1", "path": "note.txt",
                         "sha256": hashlib.sha256(self.text.encode()).hexdigest()}],
            "anchors": [{"anchor_id": "A1", "source_id": "S1", "line_start": 1,
                         "line_end": 1, "quote": "two and three total five"}],
            "bindings": [{"claim_id": "C1", "evidence_id": "E1",
                          "anchor_id": "A1", "scope": "principle"}]}

    def tearDown(self):
        self.tmp.cleanup()

    def verify(self):
        return verify_sources(self.records, self.bundle, self.root)

    def test_exact_source_is_not_scientific_support(self):
        report = self.verify()
        self.assertEqual(report["sources"]["S1"]["status"], "SOURCE_BYTES_MATCH_PIN")
        self.assertEqual(report["anchors"]["A1"]["status"], "EXACT_QUOTE_MATCH")
        self.assertTrue(report["no_scientific_verification"])

    def test_edited_source_fails_pin(self):
        (self.root / "note.txt").write_text("An entirely different note.\n", encoding="utf-8")
        self.assertEqual(self.verify()["sources"]["S1"]["status"], "SOURCE_DIGEST_MISMATCH")

    def test_wrong_quote_fails(self):
        self.bundle["anchors"][0]["quote"] = "unsupported synthetic quote"
        self.assertEqual(self.verify()["anchors"]["A1"]["status"], "EXACT_QUOTE_MISMATCH")

    def test_unrecorded_support_scope(self):
        self.bundle["bindings"][0]["scope"] = "performance"
        self.assertEqual(self.verify()["bindings"][0]["status"], "SCOPE_NOT_DECLARED_FOR_EVIDENCE")

    def test_reported_two_reviewers_do_not_verify_science(self):
        def rating(name, verdict):
            return {"claim_id": "C1", "evidence_id": "E1", "anchor_id": "A1",
                    "scope": "principle", "reviewer_id": name, "verdict": verdict,
                    "rationale": "Fictional reviewer opinion, not independent evidence."}
        report = review_source_bindings(self.verify(), {"ratings": [
            rating("A", "supports"), rating("B", "supports")]})
        self.assertEqual(report["binding_assessments"][0]["status"],
                         "REVIEWERS_REPORT_SUPPORT_NOT_VERIFIED")
        self.assertFalse(report["binding_assessments"][0]["independently_verified"])

    def test_source_binding_scope_drift_flagged(self):
        previous = copy.deepcopy(self.bundle)
        updated = copy.deepcopy(self.bundle)
        updated["bindings"].append({"claim_id": "C1", "evidence_id": "E1",
                                    "anchor_id": "A1", "scope": "performance"})
        codes = [x["code"] for x in source_revision_events(previous, updated)["events"]]
        self.assertIn("SOURCE_BINDING_ADDED_NOT_VERIFIED", codes)
        self.assertIn("SCOPE_BROADENED_SAME_ANCHOR_REVIEW", codes)

    def test_changed_quote_under_reused_id_flagged(self):
        updated = copy.deepcopy(self.bundle)
        updated["anchors"][0]["quote"] = "a different claim"
        codes = [x["code"] for x in source_revision_events(self.bundle, updated)["events"]]
        self.assertIn("ANCHOR_ID_REUSED_WITH_CHANGED_CONTENT", codes)

    def test_no_private_source_text_echoed(self):
        import json
        self.assertNotIn(self.text, json.dumps(self.verify()))

    def test_source_origin_is_not_support(self):
        self.bundle["claim_origins"] = [{"claim_id": "C1", "anchor_id": "A1"}]
        report = self.verify()
        self.assertEqual(report["claim_origins"][0]["status"],
                         "CLAIM_ORIGIN_MATCH_NOT_EVIDENCE")
        self.assertEqual(report["bindings"][0]["status"],
                         "SOURCE_ANCHOR_MATCH_NOT_SEMANTIC_SUPPORT")

    def test_invalid_reviewer_label_rejected(self):
        report = self.verify()
        with self.assertRaises(ValueError):
            review_source_bindings(report, {"ratings": [{"claim_id": "C1",
                    "evidence_id": "E1", "anchor_id": "A1", "scope": "principle",
                    "reviewer_id": "A", "verdict": "proved", "rationale": "test"}]})


if __name__ == "__main__":
    unittest.main()
