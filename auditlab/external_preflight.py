"""Preflight checks for openly unblinded, source-anchored claim extractions.

Checks internal consistency, not correctness of a scientific claim or the
faithfulness of a curator's paraphrase to upstream source text.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from .engine import audit

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "pilot" / "external_candidates"
HEX_SHA = re.compile(r"^[0-9a-f]{40}$")
FORBIDDEN = frozenset({
    "reference_label", "expected_review_required", "verified_truth",
    "human_rating", "human_ratings", "generic_prediction", "true_positive",
    "false_positive", "assay_reduction", "independent_adjudication_result",
})

def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def preflight(register: dict, extraction: dict, selection: dict) -> dict:
    original = register.get("candidates", [])
    cases = extraction.get("cases", [])
    rows = selection.get("entries", [])
    if len(original) != 10 or len(cases) != 9 or len(rows) != 10:
        raise ValueError("Expected frozen 10 candidates, 9 extractions and 10 ledger entries")
    def unique(collection: list[dict], idkey: str) -> dict[str, dict]:
        ids = [item[idkey] for item in collection]
        if len(set(ids)) != len(ids):
            raise ValueError("Duplicate candidate IDs")
        return dict(zip(ids, collection))

    candidates = unique(original, "case_id")
    chosen = unique(cases, "case_id")
    ledger = unique(rows, "case_id")
    if set(candidates) != set(ledger):
        raise ValueError("Ledger candidate universe differs from register")
    if set(chosen) != {k for k,v in ledger.items() if v["treatment"] == "include_claim_pair"}:
        raise ValueError("Included cases differ from frozen selection ledger")
    if selection.get("included") != len(chosen) or selection.get("excluded") != 1:
        raise ValueError("Incorrect selection counts")

    stable_claims = 0
    added_claims = 0
    for cid, case in chosen.items():
        if FORBIDDEN.intersection(case):
            raise ValueError(f"{cid}: outcome or rating key leaked into extraction")
        src = case["source"]
        c = candidates[cid]
        required = {
            "repository": "repository", "pr_number": "pr_number",
            "pr_url": "pr_url", "path": "source_path",
            "before_ref": "before_ref", "after_ref": "after_ref",
            "before_url": "before_url", "after_url": "after_url",
        }
        for field, source_key in required.items():
            if src[field] != c[source_key]:
                raise ValueError(f"{cid}: source pointer does not match registered commit")
        if not HEX_SHA.fullmatch(src["before_ref"]) or not HEX_SHA.fullmatch(src["after_ref"]):
            raise ValueError(f"{cid}: missing immutable 40-char commit SHA")
        if not src.get("selected_hunk"):
            raise ValueError(f"{cid}: source hunk selector missing")
        if case.get("phase") != "UNBLINDED_EXTERNAL_SOURCE_EXTRACTION_NOT_RATED":
            raise ValueError(f"{cid}: illegal rating/verification state")
        if case["extraction"].get("scientific_truth_assessed") is not False:
            raise ValueError(f"{cid}: unsupported verified-truth status")
        if case["extraction"].get("source_meaning_confirmed_independently") is not False:
            raise ValueError(f"{cid}: independent source confirmation falsely asserted")
        for stage in ("before", "after"):
            claimset = case[stage]
            audit(claimset)  # checks IDs and structure, without validating science
            for claim in claimset["claims"]:
                if claim.get("asserted_status") != "hypothesis":
                    raise ValueError(f"{cid}/{stage}: upstream claim strength must not be invented")
                if claim.get("evidence") != [] or claim.get("assumptions") != []:
                    raise ValueError(f"{cid}/{stage}: no evidence/assumptions can be fabricated")
        old = {x["id"] for x in case["before"]["claims"]}
        new = {x["id"] for x in case["after"]["claims"]}
        if old - new:
            raise ValueError(f"{cid}: excluded source deletes claim IDs without a mapping")
        stable_claims += len(old & new)
        added_claims += len(new - old)
    return {
        "status": "INPUT INTEGRITY CHECK ONLY; NO HUMAN RATINGS OR SOURCE-TRUTH CHECKS",
        "registered_candidates": len(candidates),
        "extracted_pairs": len(chosen),
        "excluded_candidates": len(candidates) - len(chosen),
        "unchanged_claim_ids_across_versions": stable_claims,
        "new_claim_ids_in_after": added_claims,
        "original_documents_rechecked_by_independent_reviewer": 0,
        "real_generic_critic_predictions": 0,
        "external_comparative_effectiveness_results": 0,
    }

def main() -> None:
    result = preflight(_load(DATA / "CANDIDATES.json"),
                       _load(DATA / "EXTRACTED-PAIRS.json"),
                       _load(DATA / "SELECTION-LEDGER.json"))
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
