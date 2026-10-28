import copy
import unittest

from auditlab.bibliography import check_bibliography, normalize_doi

def sample():
    return {"claims": [{
        "id": "C1", "statement": "Toy science claim", "asserted_status": "verified",
        "evidence": [{
            "id": "E1", "kind": "publication", "locator": "https://doi.org/10.1234/ABCD",
            "reviewed": True, "applicability": "matched",
            "bibliography": {"doi": "10.1234/abcd", "title": "Synthetic publication",
                             "year": 2020, "first_author": "Example"}
        }],
        "assumptions": []
    }]}

def record():
    return {"DOI": "10.1234/abcd", "title": ["Synthetic publication"],
            "issued": {"date-parts": [[2020, 5, 3]]},
            "author": [{"family": "Example"}]}

class BibliographyTests(unittest.TestCase):
    def test_offline_is_the_default(self):
        r = check_bibliography(sample())
        self.assertEqual(r["external_lookups_attempted"], 0)
        self.assertEqual(r["results"][0]["status"], "not_checked_offline")

    def test_independent_bibliographic_match_not_scientific_verification(self):
        r = check_bibliography(sample(), online=True, fetcher=lambda doi: record())
        self.assertEqual(r["results"][0]["status"], "bibliographic_metadata_match_only")
        self.assertFalse(r["results"][0]["scientific_claim_verified"])
        self.assertIsNone(r["verified_empirical_reduction"])

    def test_false_title_caught_even_for_correct_doi(self):
        data = sample()
        data["claims"][0]["evidence"][0]["bibliography"]["title"] = "Another publication"
        r = check_bibliography(data, online=True, fetcher=lambda doi: record())
        self.assertIn("title", r["results"][0]["fields_mismatched"])

    def test_year_mismatch(self):
        data = sample()
        data["claims"][0]["evidence"][0]["bibliography"]["year"] = 2019
        r = check_bibliography(data, online=True, fetcher=lambda doi: record())
        self.assertEqual(r["results"][0]["status"], "metadata_mismatch")

    def test_missing_record_is_not_nonexistence_proof(self):
        r = check_bibliography(sample(), online=True, fetcher=lambda doi: None)
        self.assertEqual(r["results"][0]["status"], "not_found_in_crossref")

    def test_api_error_fails_closed(self):
        def fail(_doi):
            raise TimeoutError("simulate failed lookup")
        r = check_bibliography(sample(), online=True, fetcher=fail)
        self.assertEqual(r["results"][0]["status"], "lookup_error")
        self.assertEqual(r["results"][0]["error_type"], "TimeoutError")

    def test_conflicting_doi_is_not_queried(self):
        data = sample()
        data["claims"][0]["evidence"][0]["bibliography"]["doi"] = "10.2222/other"
        r = check_bibliography(data, online=True, fetcher=lambda _: self.fail("should not fetch"))
        self.assertEqual(r["results"][0]["status"], "doi_conflict_in_record")
        self.assertEqual(r["external_lookups_attempted"], 0)

    def test_no_doi_support_does_not_mean_fake_paper(self):
        data = sample()
        data["claims"][0]["evidence"][0]["locator"] = "synthetic://paper"
        data["claims"][0]["evidence"][0].pop("bibliography")
        r = check_bibliography(data, online=True, fetcher=lambda _: self.fail("must not fetch"))
        self.assertEqual(r["results"][0]["status"], "unsupported_locator")

    def test_doi_normalization(self):
        self.assertEqual(normalize_doi("DOI:10.1234/ABC"), "10.1234/abc")
        self.assertIsNone(normalize_doi("https://example.com/10.1234/no"))

    def test_no_title_means_no_metadata_match(self):
        data = sample()
        data["claims"][0]["evidence"][0]["bibliography"].pop("title")
        r = check_bibliography(data, online=True, fetcher=lambda _: record())
        self.assertEqual(r["results"][0]["status"], "record_found_insufficient_expected_metadata")

    def test_duplicate_doi_deduplicates_requests(self):
        data = sample()
        ev2 = copy.deepcopy(data["claims"][0]["evidence"][0])
        ev2["id"] = "E2"
        data["claims"][0]["evidence"].append(ev2)
        calls = []
        def fetch(doi):
            calls.append(doi)
            return record()
        r = check_bibliography(data, online=True, fetcher=fetch)
        self.assertEqual(len(calls), 1)
        self.assertEqual(len(r["results"]), 2)


if __name__ == "__main__":
    unittest.main()
