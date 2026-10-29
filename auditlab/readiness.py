"""Fail-closed readiness check for PUBLIC historical evidence-chain discovery.

This is project management and protocol-integrity code, not a classifier or
scientific warrant evaluator. Never infer truth or independence from links.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from .evidence_chains import validate_chains, DEFAULT as DOSSIERS

LEDGER = Path(__file__).resolve().parents[1] / "pilot" / "evidence_chains" / "ELIGIBILITY-LEDGER.json"
PROVISIONAL = "documented_in_record"
MISSING = "not_established"
NON_SELF_CERTIFIABLE = frozenset({
    "evidence_actually_used_verified",
    "source_support_independently_checked",
    "same_terminal_comparator",
    "independent_reference_ratings",
    "equal_information_generic_baseline",
})

def assess_readiness(dossiers: dict, ledger: dict) -> dict:
    """Report what still blocks external claims; do not assign source-level truth."""
    temporal = validate_chains(dossiers)
    if not isinstance(ledger, dict) or not isinstance(ledger.get("criteria"), list):
        raise ValueError("Readiness ledger requires criteria")
    if not isinstance(ledger.get("cases"), list):
        raise ValueError("Readiness ledger requires cases")

    criteria = {c["id"]: c for c in ledger["criteria"]}
    if len(criteria) != len(ledger["criteria"]):
        raise ValueError("Duplicate criterion")
    if set(criteria) != {
        "dated_source_inventory", "chronology_and_source_ids",
        "evidence_actually_used_verified", "source_support_independently_checked",
        "same_terminal_comparator", "independent_reference_ratings",
        "equal_information_generic_baseline",
    }:
        raise ValueError("Unexpected/absent readiness criterion")
    if any(c.get("required_for_comparative_test") is not True for c in criteria.values()):
        raise ValueError("All stated evaluation prerequisites must be required")
    ids = {c["case_id"] for c in dossiers["cases"]}
    records = ledger["cases"]
    if len({r.get("case_id") for r in records}) != len(records):
        raise ValueError("Duplicate readiness case ID")
    if {r.get("case_id") for r in records} != ids:
        raise ValueError("Readiness case IDs diverge from historical dossiers")
    if ledger.get("expected_candidate_count") != len(ids):
        raise ValueError("Candidate count differs from ledger")

    summary = []
    for record in records:
        cid = record["case_id"]
        statuses = record.get("statuses")
        if not isinstance(statuses, dict) or set(statuses) != set(criteria):
            raise ValueError(f"{cid}: incomplete or unexpected readiness statuses")
        if any(v not in {PROVISIONAL, MISSING} for v in statuses.values()):
            raise ValueError(f"{cid}: unsupported status")
        # The dossier contains dated, attributable references and mechanically
        # valid links; this does NOT verify the real scientific content.
        for mechanical in ("dated_source_inventory", "chronology_and_source_ids"):
            if statuses[mechanical] != PROVISIONAL:
                raise ValueError(f"{cid}: mechanical integrity status inconsistent")
        # An owner-authored JSON cell is not a specialist attestation. No
        # external proof bundle is supported by v0.1, so fail closed instead
        # of accepting a self-certified success flag.
        for criterion in NON_SELF_CERTIFIABLE:
            if statuses[criterion] == PROVISIONAL:
                raise ValueError(f"{cid}/{criterion}: independent external evidence cannot be self-certified")
        if not record.get("scope_note"):
            raise ValueError(f"{cid}: missing scope explanation")
        summary.append({
            "case_id": cid,
            "documented_referential_prerequisites": 2,
            "unmet_independent_prerequisites": sorted(NON_SELF_CERTIFIABLE),
            "same_terminal_evidence_established": False,
            "ready_for_comparative_performance_test": False,
            "scientific_warrant_established": None,
            "scope_note": record["scope_note"],
        })
    return {
        "gate": "HISTORICAL SOURCES: FAIL-CLOSED SCIENTIFIC READINESS",
        "dossiers_checked": len(summary),
        "mechanically_valid_source_histories": temporal["case_count"],
        "independently_source_verified_histories": 0,
        "established_matched_terminal_pairs": 0,
        "independently_rated_cases": 0,
        "equal_information_critic_executions": 0,
        "eligible_for_external_effectiveness_claims": 0,
        "originality_established": False,
        "interpretation": ("A chronological source inventory is not evidence-used provenance, "
                           "independent source verification or a matched comparison. "
                           "No truth, superiority or statistical result is produced."),
        "cases": summary,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="External claim-comparison readiness check (fail closed)")
    p.add_argument("--dossiers", type=Path, default=DOSSIERS)
    p.add_argument("--ledger", type=Path, default=LEDGER)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    result = assess_readiness(
        json.loads(args.dossiers.read_text(encoding="utf-8")),
        json.loads(args.ledger.read_text(encoding="utf-8")))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    print(result["gate"])
    print(f"Chronology-checked histories: {result['mechanically_valid_source_histories']}")
    print(f"Independently validated source histories: {result['independently_source_verified_histories']}")
    print(f"Same-terminal evidence matched pairs: {result['established_matched_terminal_pairs']}")
    print(f"Cases eligible for comparative claims: {result['eligible_for_external_effectiveness_claims']}")
    for case in result["cases"]:
        print(f"  {case['case_id']}: NOT READY — five independent requirements unmet")
    print("No scientific validity or originality claim is licensed.")


if __name__ == "__main__":
    main()
