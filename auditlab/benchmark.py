"""Synthetic regression challenge, NOT an independent scientific validation.

Cases and expected flags were authored alongside this implementation. Outcomes
demonstrate specified rule behavior, not generalization to real research.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from .compare import compare
from .engine import audit

RECHECK_CODES = frozenset({
    "ASSERTED_STATUS_UPGRADED_NOT_PROVEN",
    "REVIEW_STATUS_SELF_UPGRADED",
    "REVIEW_STATUS_DOWNGRADED",
    "APPLICABILITY_SELF_UPGRADED",
    "APPLICABILITY_REGRESSED",
    "EVIDENCE_ID_REUSED_FOR_DIFFERENT_SOURCE",
    "BIBLIOGRAPHIC_METADATA_CHANGED",
    "NEW_CLOSURE_ASSERTION_NOT_VERIFIED",
    "ASSUMPTION_CLOSURE_LINK_CHANGED",
    "ASSUMPTION_REMOVED_NOT_CLOSED",
    "ASSUMPTION_MEANING_CHANGED",
    "NEW_ASSUMPTION_INTRODUCED",
    "ASSUMPTION_WITHDRAWN_NOT_VERIFIED",
    "ASSUMPTION_REOPENED",
    "CLAIM_REMOVED_NOT_VERIFIED",
    "CLAIM_ADDED_REQUIRES_REVIEW",
    "EVIDENCE_ADDED_NOT_INDEPENDENTLY_VERIFIED",
    "EVIDENCE_REMOVED",
    "NUMERIC_CLAIM_LITERAL_CHANGED_REQUIRES_REVIEW",
})

def metrics(truth: list[bool], guess: list[bool]) -> dict:
    if len(truth) != len(guess):
        raise ValueError("Mismatched truth/prediction lengths")
    tp = sum(t and g for t, g in zip(truth, guess))
    fp = sum(not t and g for t, g in zip(truth, guess))
    fn = sum(t and not g for t, g in zip(truth, guess))
    tn = sum(not t and not g for t, g in zip(truth, guess))
    def div(n: int, d: int) -> float | None:
        return round(n / d, 4) if d else None
    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": div(tp, tp + fp),
        "recall": div(tp, tp + fn),
        "specificity": div(tn, tn + fp),
    }

def evaluate(dataset: dict) -> dict:
    cases = dataset.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Expected nonempty cases array")
    ids: set[str] = set()
    outcomes: list[dict] = []
    for item in cases:
        cid = item["id"]
        if cid in ids:
            raise ValueError(f"Duplicate benchmark case ID: {cid}")
        ids.add(cid)
        if type(item.get("expected_review_required")) is not bool:
            raise ValueError(f"{cid}: expected_review_required must be boolean")
        before, after = item["before"], item["after"]
        change = compare(before, after)
        # Snapshot comparator is shown the complete AFTER metadata and can
        # apply all v0.1 issue rules; it cannot infer which assertions changed.
        snapshot = audit(after)
        snapshot_flag = snapshot["issues_count"] > 0
        # General full-record diff gets BOTH records; it is deliberately
        # high-sensitivity and flags cosmetic changes too.
        full_diff_flag = before != after
        risk_codes = sorted({e["code"] for e in change["events"]}
                            & RECHECK_CODES)
        targeted_flag = bool(risk_codes)
        outcomes.append({
            "id": cid,
            "expected_review_required": item["expected_review_required"],
            "reason": item.get("reason", ""),
            "snapshot_only_review": snapshot_flag,
            "any_field_diff_review": full_diff_flag,
            "targeted_revision_review": targeted_flag,
            "trigger_codes": risk_codes,
            "all_revision_events": [e["code"] for e in change["events"]],
        })
    truth = [x["expected_review_required"] for x in outcomes]
    systems = {
        "snapshot_only_review": metrics(truth, [x["snapshot_only_review"] for x in outcomes]),
        "any_field_diff_review": metrics(truth, [x["any_field_diff_review"] for x in outcomes]),
        "targeted_revision_review": metrics(truth, [x["targeted_revision_review"] for x in outcomes]),
    }
    return {
        "dataset": dataset.get("dataset"),
        "scope": "Synthetic regression cases authored with tool; no independent adjudication or external holdout.",
        "claim": "Rule behavior only; no empirical evidence of superiority or scientific validity.",
        "positive_cases": sum(truth),
        "negative_cases": len(truth) - sum(truth),
        "systems": systems,
        "cases": outcomes,
    }

def main() -> None:
    parser = argparse.ArgumentParser(description="Run the openly labelled synthetic regression challenge")
    default_path = Path(__file__).resolve().parents[1] / "benchmarks" / "revision_challenge" / "cases.json"
    parser.add_argument("--cases", type=Path, default=default_path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    output = evaluate(json.loads(args.cases.read_text(encoding="utf-8")))
    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return
    print("SYNTHETIC REGRESSION CHALLENGE — NOT SCIENTIFIC VALIDATION")
    print(f"Cases: {len(output['cases'])}; review labels: {output['positive_cases']}; controls: {output['negative_cases']}")
    for name, m in output["systems"].items():
        print(f"{name}: TP={m['tp']} FP={m['fp']} FN={m['fn']} TN={m['tn']} precision={m['precision']} recall={m['recall']}")
    print("Observed rule errors:")
    for case in output["cases"]:
        if case["expected_review_required"] != case["targeted_revision_review"]:
            print(f" - {case['id']}: expected={case['expected_review_required']}, predicted={case['targeted_revision_review']}")
    print("All results are in-sample and synthetic; external reliability UNKNOWN.")


if __name__ == "__main__":
    main()
