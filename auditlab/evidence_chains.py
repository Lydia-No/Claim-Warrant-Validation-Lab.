"""Source-temporal integrity checks for candidate evidence histories.

The programme validates time-order, source IDs, assumption links and scope.
It does NOT reproduce science or certify that a cited source supports a claim.
"""
from __future__ import annotations

import json
from pathlib import Path
from datetime import date
from urllib.parse import urlparse

DEFAULT = Path(__file__).resolve().parents[1] / "pilot" / "evidence_chains" / "HISTORICAL-DOSSIERS.json"
BANNED = {"verified_scientifically", "independently_adjudicated", "human_ground_truth",
          "claim_proven", "performance_improvement", "highest_warranted_claim_level"}

def _date(v: object) -> date:
    if not isinstance(v, str):
        raise ValueError("Stage or evidence date must be ISO YYYY-MM-DD")
    try:
        result = date.fromisoformat(v)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Invalid date: {v}") from error
    if result.isoformat() != v:
        raise ValueError(f"Date must be YYYY-MM-DD: {v}")
    return result


def validate_chains(data: dict) -> dict:
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        raise ValueError("Expected cases list")
    if not data["cases"]:
        raise ValueError("Cannot validate empty evidence-chain cohort")
    cases = []
    ids = set()
    for case in data["cases"]:
        cid = case.get("case_id")
        if not isinstance(cid, str) or not cid or cid in ids:
            raise ValueError(f"Duplicate or missing case_id: {cid!r}")
        ids.add(cid)
        if BANNED & set(case):
            raise ValueError(f"{cid}: forbidden scientific verification status")
        evidence = case.get("evidence")
        assumptions = case.get("assumptions")
        stages = case.get("stages")
        if not isinstance(evidence, list) or not isinstance(assumptions, list):
            raise ValueError(f"{cid}: expected evidence and assumptions lists")
        if not isinstance(stages, list) or len(stages) < 2:
            raise ValueError(f"{cid}: two or more stages required")
        eids = set()
        evidence_index = {}
        for ev in evidence:
            eid = ev.get("id")
            if not isinstance(eid, str) or not eid or eid in eids:
                raise ValueError(f"{cid}: duplicate or missing evidence ID")
            eids.add(eid)
            evidence_index[eid] = ev
            _date(ev.get("date"))
            u = urlparse(ev.get("url", ""))
            if u.scheme != "https" or not u.netloc:
                raise ValueError(f"{cid}/{eid}: requires a public HTTPS evidence locator")
            if ev.get("date_precision") not in {"day", "month", "year"}:
                raise ValueError(f"{cid}/{eid}: unsupported precision")
            if not ev.get("summary") or not ev.get("organization"):
                raise ValueError(f"{cid}/{eid}: missing source attribution")
        aids = set()
        for a in assumptions:
            aid = a.get("id")
            if not isinstance(aid, str) or not aid or aid in aids:
                raise ValueError(f"{cid}: duplicate or missing assumption ID")
            aids.add(aid)
            if not a.get("question"):
                raise ValueError(f"{cid}/{aid}: missing question")
        known_stages = set()
        previous_date = None
        previously_available = set()
        new_evidence_per_stage = {}
        for stage in stages:
            sid = stage.get("id")
            if not isinstance(sid, str) or not sid or sid in known_stages:
                raise ValueError(f"{cid}: duplicate or missing stage ID")
            known_stages.add(sid)
            when = _date(stage.get("as_of"))
            if previous_date is not None and when <= previous_date:
                raise ValueError(f"{cid}/{sid}: stages not strictly chronological")
            previous_date = when
            if not isinstance(stage.get("claim"), str) or not stage["claim"].strip():
                raise ValueError(f"{cid}/{sid}: claim statement required")
            used = stage.get("source_ids")
            if not isinstance(used, list) or not used:
                raise ValueError(f"{cid}/{sid}: source_ids must be nonempty")
            if len(set(used)) != len(used):
                raise ValueError(f"{cid}/{sid}: repeated evidence ID")
            for eid in used:
                if eid not in evidence_index:
                    raise ValueError(f"{cid}/{sid}: unknown evidence reference {eid}")
                if _date(evidence_index[eid]["date"]) > when:
                    raise ValueError(f"{cid}/{sid}: future evidence {eid} used before publication")
            active = stage.get("active_assumption_ids")
            if not isinstance(active, list) or len(set(active)) != len(active):
                raise ValueError(f"{cid}/{sid}: invalid assumption list")
            if not set(active).issubset(aids):
                raise ValueError(f"{cid}/{sid}: unknown assumption ID")
            if not stage.get("observation") or not stage.get("claim_kind"):
                raise ValueError(f"{cid}/{sid}: missing interpretation notes")
            new_evidence_per_stage[sid] = sorted(set(used) - previously_available)
            previously_available |= set(used)
        if not case.get("residual_question") or not case.get("limits"):
            raise ValueError(f"{cid}: residual question and limitations required")
        cases.append({
            "case_id": cid,
            "stages": len(stages),
            "source_records": len(evidence),
            "assumption_questions": len(assumptions),
            "source_additions_by_stage": new_evidence_per_stage,
            "scientific_verification": "NOT PERFORMED",
            "reviewer_adjudication": "NOT PERFORMED",
        })
    return {
        "audit_type": "temporal and referential integrity ONLY",
        "case_count": len(cases),
        "stage_count": sum(x["stages"] for x in cases),
        "linked_source_records": sum(x["source_records"] for x in cases),
        "assumption_questions": sum(x["assumption_questions"] for x in cases),
        "independent_domain_reproduction": 0,
        "independent_reviewer_ratings": 0,
        "comparative_validity_findings": 0,
        "limitations": "Historical source narrations were reviewed, but source records and underlying empirical analyses were not reproduced. No evidential entitlement is certified.",
        "cases": cases,
    }


def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description="Time-order source-chain lint; no scientific verification")
    p.add_argument("--cases", type=Path, default=DEFAULT)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    report = validate_chains(json.loads(args.cases.read_text(encoding="utf-8")))
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("PUBLIC EVIDENCE-CHAIN CANDIDATE INTEGRITY — NO SCIENTIFIC VERIFICATION")
        for c in report["cases"]:
            print(f"{c['case_id']}: {c['stages']} stages; {c['source_records']} source records; {c['assumption_questions']} open questions")
        print(f"Totals: {report['case_count']} histories; {report['linked_source_records']} source records.")
        print("Independent reference ratings: 0; comparative evaluation: NOT PERFORMED.")


if __name__ == "__main__":
    main()
