"""Exploratory external-pilot scorer (stdlib-only).

Requires two separate blinded reviewer files and generic-critic predictions.
Reports only agreed, determinate human labels as primary; abstentions are not
negative decisions. Does not validate the truth of human ratings.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .benchmark import RECHECK_CODES, metrics
from .compare import compare

LABELS = {"yes", "no", "uncertain"}
PREDICTIONS = {"yes", "no", "abstain"}


def _indexed(records: Any, label: str, key: str, allowed: set[str] | None = None) -> dict[str, dict]:
    if not isinstance(records, list):
        raise ValueError(f"{label}: expected records list")
    found: dict[str, dict] = {}
    for r in records:
        if not isinstance(r, dict):
            raise ValueError(f"{label}: every record must be an object")
        cid = r.get("case_id")
        if not isinstance(cid, str) or not cid:
            raise ValueError(f"{label}: nonempty case_id required")
        if cid in found:
            raise ValueError(f"{label}: duplicate case_id {cid}")
        if allowed is not None and r.get(key) not in allowed:
            raise ValueError(f"{label}/{cid}: invalid {key}")
        found[cid] = r
    return found


def _load_labeled(document: dict, field: str, allowed: set[str], name: str) -> dict[str, dict]:
    if not isinstance(document, dict):
        raise ValueError(f"{name}: document must be an object")
    return _indexed(document.get("ratings") if field == "label" else document.get("predictions"),
                    name, field, allowed)


def _metrics_with_abstain(truth: list[bool], predictions: list[str]) -> dict:
    if len(truth) != len(predictions):
        raise ValueError("Scoring inputs have unequal lengths")
    non_abstain = [(expected, prediction) for expected, prediction in zip(truth, predictions)
                   if prediction != "abstain"]
    measured = metrics([expected for expected, _ in non_abstain],
                       [prediction == "yes" for _, prediction in non_abstain])
    measured["abstained"] = len(predictions) - len(non_abstain)
    measured["scored"] = len(non_abstain)
    measured["total_eligible"] = len(predictions)
    measured["coverage"] = round(len(non_abstain) / len(predictions), 4) if predictions else None
    return measured


def assess(cases: dict, reviewer_a: dict, reviewer_b: dict, generic: dict) -> dict:
    """Compare paired tools against independent reviewer labels, without tuning.

    Two-rater agreement is a minimum procedural gate, not proof of
    independent adjudication or high quality ground truth.
    """
    if not isinstance(cases, dict) or not isinstance(cases.get("cases"), list):
        raise ValueError("cases: expected a cases list")
    selected = _indexed(cases["cases"], "cases", "case_id")
    if not selected:
        raise ValueError("cases: require at least one pair")
    a = _load_labeled(reviewer_a, "label", LABELS, "reviewer_a")
    b = _load_labeled(reviewer_b, "label", LABELS, "reviewer_b")
    model = _load_labeled(generic, "decision", PREDICTIONS, "generic_critic")
    expected = set(selected)
    for name, frame in (("reviewer_a", a), ("reviewer_b", b), ("generic_critic", model)):
        if set(frame) != expected:
            missing, extra = sorted(expected - set(frame)), sorted(set(frame) - expected)
            raise ValueError(f"{name} case IDs differ: missing={missing}, extra={extra}")

    matched: list[str] = []
    disagreements: list[str] = []
    unresolved: list[str] = []
    truth: list[bool] = []
    generic_calls: list[str] = []
    targeted_calls: list[str] = []
    case_reports = []

    for cid, pair in selected.items():
        if "before" not in pair or "after" not in pair:
            raise ValueError(f"{cid}: before and after snapshots required")
        change = compare(pair["before"], pair["after"])
        risks = sorted({e["code"] for e in change["events"]} & RECHECK_CODES)
        targeted = "yes" if risks else "no"
        ga = a[cid]["label"]
        gb = b[cid]["label"]
        agreement = ga == gb
        if not agreement:
            disagreements.append(cid)
        elif ga == "uncertain":
            unresolved.append(cid)
        else:
            matched.append(cid)
            truth.append(ga == "yes")
            generic_calls.append(model[cid]["decision"])
            targeted_calls.append(targeted)
        case_reports.append({
            "case_id": cid,
            "reviewer_agreement": agreement,
            "eligible_for_primary": agreement and ga != "uncertain",
            "generic_critic": model[cid]["decision"],
            "targeted_revision": targeted,
            "targeted_event_codes": risks,
        })

    determinate = len(matched)
    if determinate:
        gscore = _metrics_with_abstain(truth, generic_calls)
        tscore = _metrics_with_abstain(truth, targeted_calls)
    else:
        gscore = _metrics_with_abstain([], [])
        tscore = _metrics_with_abstain([], [])
    return {
        "pilot_status": "scoring only; not an independent scientific result",
        "cases_total": len(selected),
        "raw_exact_agreement": sum(a[k]["label"] == b[k]["label"] for k in selected),
        "adjudication_disagreements": disagreements,
        "both_uncertain": unresolved,
        "eligible_agreed_determinate_cases": determinate,
        "excluded_from_primary": sorted(set(selected) - set(matched)),
        "systems": {
            "generic_full_record_critic": gscore,
            "targeted_revision_engine": tscore,
        },
        "case_reports": case_reports,
        "caveats": [
            "Full-context and reviewer access equivalence must be checked outside this scorer.",
            "Human ratings need independent source inspection; this scorer cannot establish that.",
            "No claim of statistical significance or generalization from a small convenience pilot.",
            "DO NOT use synthetic demonstration ratings as empirical human judgments.",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Descriptive pilot comparison: two reviewers, one generic critic, one deterministic engine")
    p.add_argument("--cases", required=True, type=Path)
    p.add_argument("--reviewer-a", required=True, type=Path)
    p.add_argument("--reviewer-b", required=True, type=Path)
    p.add_argument("--generic", required=True, type=Path)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    def load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))
    result = assess(load(args.cases), load(args.reviewer_a), load(args.reviewer_b),
                    load(args.generic))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("EXPLORATORY PILOT — DESCRIPTIVE SCORING ONLY")
        print(f"Pairs: {result['cases_total']}; agreed and determinate: {result['eligible_agreed_determinate_cases']}")
        print(f"Reviewer disagreements: {result['adjudication_disagreements']}")
        for name, score in result["systems"].items():
            print(f"{name}: TP={score['tp']} FP={score['fp']} FN={score['fn']} TN={score['tn']}; "
                  f"abstained={score['abstained']}; coverage={score['coverage']}")
        print("No independent evidence validation or significance test was performed.")


if __name__ == "__main__":
    main()
