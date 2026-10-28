"""Conservative structural checks for claims, evidence, and revision assumptions.

No source is fetched or scientifically validated by this package. A submitter's
'reviewed' marking is NOT proof of independent verification.
"""
from __future__ import annotations

import json
from pathlib import Path

KINDS = {"publication", "standard", "derivation", "hardware_report", "experiment"}
LEVELS = {"hypothesis", "supported", "verified", "proven"}
MATCH = {"matched", "mismatch", "unknown"}
ASSUMPTION_AFTER = {"open", "claimed_closed", "withdrawn"}


def _error(condition: bool, message: str) -> None:
    if condition:
        raise ValueError(message)


def load_records(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    _error(not isinstance(data, dict) or not isinstance(data.get("claims"), list),
           "Input must be a JSON object containing a claims array")
    return data


def audit(data: dict) -> dict:
    """Inspect evidence metadata and report issues; never certify a claim."""
    _error(not isinstance(data, dict) or not isinstance(data.get("claims"), list),
           "Input must contain claims list")
    claims_out = []
    seen_claims: set[str] = set()
    total_before = eligible_closures = withdrawn = 0
    issues_total = 0

    for claim in data["claims"]:
        _error(not isinstance(claim, dict), "Each claim must be an object")
        cid = claim.get("id")
        _error(not isinstance(cid, str) or not cid.strip(), "Claim id must be nonempty")
        _error(cid in seen_claims, f"Duplicate claim id: {cid}")
        seen_claims.add(cid)
        _error(not isinstance(claim.get("statement"), str) or not claim["statement"].strip(),
               f"{cid}: statement must be nonempty")
        status = claim.get("asserted_status", "hypothesis")
        _error(status not in LEVELS, f"{cid}: invalid asserted_status")
        evidences = claim.get("evidence", [])
        assumptions = claim.get("assumptions", [])
        _error(not isinstance(evidences, list) or not isinstance(assumptions, list),
               f"{cid}: evidence and assumptions must be arrays")
        issues = []
        ev_by_id: dict[str, dict] = {}

        for ev in evidences:
            _error(not isinstance(ev, dict), f"{cid}: evidence entry must be an object")
            eid = ev.get("id")
            _error(not isinstance(eid, str) or not eid, f"{cid}: evidence id required")
            _error(eid in ev_by_id, f"{cid}: duplicate evidence id {eid}")
            _error(ev.get("kind") not in KINDS, f"{cid}/{eid}: invalid kind")
            _error(ev.get("applicability") not in MATCH,
                   f"{cid}/{eid}: invalid applicability")
            _error(type(ev.get("reviewed")) is not bool, f"{cid}/{eid}: reviewed must be boolean")
            _error(not isinstance(ev.get("locator"), str) or not ev["locator"].strip(),
                   f"{cid}/{eid}: locator is required")
            ev_by_id[eid] = ev
            if ev["applicability"] == "mismatch":
                issues.append({"code": "REGIME_MISMATCH", "evidence_id": eid})
            elif ev["applicability"] == "unknown":
                issues.append({"code": "REGIME_NOT_ESTABLISHED", "evidence_id": eid})
            if not ev["reviewed"]:
                issues.append({"code": "REVIEW_NOT_DOCUMENTED", "evidence_id": eid})

        qualifying = {eid for eid, ev in ev_by_id.items()
                      if ev["reviewed"] and ev["applicability"] == "matched"}
        if status in {"verified", "proven"} and not qualifying:
            issues.append({"code": "STRONG_CLAIM_WITHOUT_REVIEWED_MATCHED_EVIDENCE"})
        if status == "proven" and not any(
            ev["kind"] == "derivation" and eid in qualifying
            for eid, ev in ev_by_id.items()
        ):
            issues.append({"code": "PROOF_ASSERTED_WITHOUT_MATCHED_DERIVATION"})
        if status in {"supported", "verified", "proven"} and not evidences:
            issues.append({"code": "NO_EVIDENCE_REFERENCED"})

        assumed_ids: set[str] = set()
        claim_before = claim_closures = claim_withdrawn = 0
        for item in assumptions:
            _error(not isinstance(item, dict), f"{cid}: assumption must be an object")
            aid = item.get("id")
            _error(not isinstance(aid, str) or not aid,
                   f"{cid}: assumption id required")
            _error(aid in assumed_ids, f"{cid}: duplicate assumption id {aid}")
            assumed_ids.add(aid)
            _error(item.get("after") not in ASSUMPTION_AFTER,
                   f"{cid}/{aid}: invalid after status")
            _error(not isinstance(item.get("description"), str) or not item["description"].strip(),
                   f"{cid}/{aid}: assumption description required")
            claim_before += 1
            if item["after"] == "claimed_closed":
                closure_id = item.get("closure_evidence_id")
                if closure_id in qualifying:
                    claim_closures += 1
                    issues.append({"code": "CLOSURE_REQUIRES_INDEPENDENT_CONFIRMATION",
                                   "assumption_id": aid, "evidence_id": closure_id})
                else:
                    issues.append({"code": "UNSUPPORTED_ASSUMPTION_CLOSURE",
                                   "assumption_id": aid})
            elif item["after"] == "withdrawn":
                claim_withdrawn += 1
                if not item.get("withdrawal_reason"):
                    issues.append({"code": "WITHDRAWAL_REASON_MISSING", "assumption_id": aid})

        total_before += claim_before
        eligible_closures += claim_closures
        withdrawn += claim_withdrawn
        issues_total += len(issues)
        claims_out.append({
            "id": cid,
            "asserted_status": status,
            "automatically_verified": False,
            "structurally_eligible_closures": claim_closures,
            "withdrawn_from_scope": claim_withdrawn,
            "issues": issues,
        })

    # These counts are metadata integrity indicators, NOT empirical proof.
    # Withdrawals must never be credited as verified closures.
    return {
        "tool_limit": "Structural audit only; does not fetch sources, prove mathematics, run RTL or validate physics.",
        "claims_examined": len(claims_out),
        "issues_count": issues_total,
        "assumptions_initially_open": total_before,
        "structurally_eligible_closures_not_verified": eligible_closures,
        "withdrawn_from_scope_not_verified": withdrawn,
        "remaining_not_structurally_closed": total_before - eligible_closures - withdrawn,
        "verified_empirical_reduction": None,
        "claim_results": claims_out,
    }
