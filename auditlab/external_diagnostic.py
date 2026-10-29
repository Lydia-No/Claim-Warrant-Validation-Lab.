"""Exploratory diagnostic of real-source *paraphrases*, not a validity benchmark.

This module deliberately does not use, generate, or infer any human reference
labels. It only tests what the existing v0.3 structural rules can observe when
source-derived candidate records contain no extracted evidential provenance.
"""
from __future__ import annotations

import json
from pathlib import Path
from .benchmark import RECHECK_CODES
from .compare import compare

DEFAULT = (Path(__file__).resolve().parents[1]
           / "pilot" / "external_candidates" / "EXTRACTED-PAIRS.json")


def diagnose(dataset: dict) -> dict:
    """Use frozen rules without changing the public cases or calling an AI."""
    if not isinstance(dataset, dict) or not isinstance(dataset.get("cases"), list):
        raise ValueError("Expected a cases array")
    out: list[dict] = []
    ids: set[str] = set()
    for item in dataset["cases"]:
        cid = item.get("case_id")
        if not isinstance(cid, str) or not cid:
            raise ValueError("Nonempty case_id required")
        if cid in ids:
            raise ValueError(f"Duplicate case_id: {cid}")
        ids.add(cid)
        if item.get("phase") != "UNBLINDED_EXTERNAL_SOURCE_EXTRACTION_NOT_RATED":
            raise ValueError(f"{cid}: external candidate must not be rated")
        before, after = item["before"], item["after"]
        for stage in (before, after):
            for claim in stage["claims"]:
                if claim["evidence"] or claim["assumptions"]:
                    raise ValueError(f"{cid}: expected unassessed evidence/assumptions")
        report = compare(before, after)
        events = sorted({r["code"] for r in report["events"]})
        triggers = sorted(set(events) & RECHECK_CODES)
        changed_text = ("CLAIM_TEXT_CHANGED" in events)
        newly_added = ("CLAIM_ADDED_REQUIRES_REVIEW" in events)
        out.append({
            "case_id": cid,
            "curation_change_type": item.get("curation_change_type"),
            "record_text_changed_or_added": changed_text or newly_added,
            "fixed_rules_request_review": bool(triggers),
            "trigger_codes": triggers,
            "notified_events": events,
            "unflagged_materiality_unknown": (changed_text and not triggers),
            "human_ground_truth": None,
            "source_correctness_verified": False,
        })
    if not out:
        raise ValueError("No external candidate cases")
    return {
        "status": "UNBLINDED EXPLORATORY SOFTWARE DIAGNOSTIC; NO EXTERNAL VALIDITY LABELS",
        "case_count": len(out),
        "flagged_for_review_by_existing_rules": sum(row["fixed_rules_request_review"] for row in out),
        "changed_paraphrases_unflagged_by_existing_rules": sum(
            row["unflagged_materiality_unknown"] for row in out),
        "metric_eligible": False,
        "precision": None,
        "recall": None,
        "specificity": None,
        "reason": ("Ground-truth human labels and genuine evidence-provenance fields do "
                   "not exist. A changed equation may be a bugfix, semantic shift, "
                   "or equivalent notation; flags are not measures of correctness."),
        "cases": out,
    }


def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description="Unblinded diagnostic; no human labels or scores")
    p.add_argument("--cases", type=Path, default=DEFAULT)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    result = diagnose(json.loads(args.cases.read_text(encoding="utf-8")))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result["status"])
        print(f"Paraphrase pairs: {result['case_count']}")
        print(f"Structural review flags (NOT verified errors): {result['flagged_for_review_by_existing_rules']}")
        print(f"Changed wording without structural risk flags: {result['changed_paraphrases_unflagged_by_existing_rules']}")
        for r in result["cases"]:
            print(f"  {r['case_id']}: {'RECHECK' if r['fixed_rules_request_review'] else 'NO RISK FLAG'} "
                  f"[{', '.join(r['trigger_codes']) or 'none'}]")
        print("No external reviewer labels, precision, recall or independent finding.")


if __name__ == "__main__":
    main()
