"""Source-linked reviewer opinion ledger; never creates truth labels.

External reviewer identity, independence and expertise are not authenticated.
The scorer does not treat agreement as scientific validation.
"""
from __future__ import annotations

VALID = {"supports", "does_not_support", "uncertain"}


def review_source_bindings(source_report: dict, rating_data: dict) -> dict:
    bindings = {
        (b["claim_id"], b["evidence_id"], b["anchor_id"], b["scope"]): b
        for b in source_report["bindings"]
    }
    items = rating_data.get("ratings")
    if not isinstance(items, list) or len(items) > 20000:
        raise ValueError("ratings must be a list of <=20000 records")
    collected = {key: {} for key in bindings}
    for rating in items:
        if not isinstance(rating, dict):
            raise ValueError("rating must be an object")
        keys = ("claim_id", "evidence_id", "anchor_id", "scope")
        key = tuple(rating.get(k) for k in keys)
        if key not in bindings:
            raise ValueError("rating references unknown claim/evidence/anchor/scope binding")
        reviewer = rating.get("reviewer_id")
        verdict = rating.get("verdict")
        rationale = rating.get("rationale")
        if not isinstance(reviewer, str) or not reviewer.strip() or len(reviewer) > 100:
            raise ValueError("nonempty reviewer_id required")
        if verdict not in VALID:
            raise ValueError("invalid reviewer verdict")
        if not isinstance(rationale, str) or not rationale.strip() or len(rationale) > 2000:
            raise ValueError("reviewer rationale required")
        if reviewer in collected[key]:
            raise ValueError("duplicate reviewer rating for binding")
        collected[key][reviewer] = verdict

    results = []
    for key, binding in bindings.items():
        vals = list(collected[key].values())
        if binding["status"] != "SOURCE_ANCHOR_MATCH_NOT_SEMANTIC_SUPPORT":
            status = "BLOCKED_SOURCE_NOT_AUTHENTICATED"
        elif len(vals) < 2:
            status = "NO_TWO_REVIEWER_RATINGS"
        elif "uncertain" in vals:
            status = "REVIEWER_UNCERTAINTY"
        elif len(set(vals)) > 1:
            status = "REVIEWER_DISAGREEMENT"
        elif vals[0] == "supports":
            status = "REVIEWERS_REPORT_SUPPORT_NOT_VERIFIED"
        else:
            status = "REVIEWERS_REPORT_NO_SUPPORT_NOT_VERIFIED"
        results.append({
            "claim_id": key[0], "evidence_id": key[1], "anchor_id": key[2], "scope": key[3],
            "rating_count": len(vals), "reviewer_identities_not_authenticated": True,
            "status": status, "independently_verified": False,
        })
    return {
        "limit": "Recorded reviewer judgments; no independence, expertise or truth verification",
        "ratings_received": len(items),
        "binding_assessments": results,
        "verified_empirical_reduction": None,
    }
