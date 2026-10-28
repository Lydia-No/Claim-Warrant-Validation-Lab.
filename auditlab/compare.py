"""Pairwise before/after audit, with stable IDs and no automatic proof promotion.

Metadata supplied by a document author is not independent verification.
A removed assumption or narrower claim is not a successfully tested assumption.
"""
from __future__ import annotations
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation
from .engine import audit

STATUS_ORDER = {"hypothesis": 0, "supported": 1, "verified": 2, "proven": 3}

NUMBER = re.compile(r"(?<![A-Za-z0-9_])[-+]?(?:\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)")


def _numeric_signature(text: str) -> tuple[str, ...]:
    """Detect changes to ordinary numeric literals; NOT a mathematical parser."""
    try:
        return tuple(str(Decimal(token).normalize()) for token in NUMBER.findall(text))
    except InvalidOperation:
        return tuple(NUMBER.findall(text))



def _map(items: list[dict]) -> dict[str, dict]:
    return {item["id"]: item for item in items}


def _hash(data: dict) -> str:
    canonical = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def compare(before: dict, after: dict) -> dict:
    """Compare two full claim-record sets. All detected changes require external adjudication."""
    # Validate BOTH independently; duplicates or malformed data cannot be silently overwritten.
    before_audit, after_audit = audit(before), audit(after)
    earlier, later = _map(before["claims"]), _map(after["claims"])
    events = []

    def event(code: str, claim_id: str, **extra) -> None:
        events.append({"code": code, "claim_id": claim_id, **extra})

    for cid in sorted(earlier.keys() - later.keys()):
        event("CLAIM_REMOVED_NOT_VERIFIED", cid)
    for cid in sorted(later.keys() - earlier.keys()):
        event("CLAIM_ADDED_REQUIRES_REVIEW", cid)

    for cid in sorted(earlier.keys() & later.keys()):
        old, new = earlier[cid], later[cid]
        if old["statement"] != new["statement"]:
            event("CLAIM_TEXT_CHANGED", cid)
            if _numeric_signature(old["statement"]) != _numeric_signature(new["statement"]):
                event("NUMERIC_CLAIM_LITERAL_CHANGED_REQUIRES_REVIEW", cid)
        old_status = old.get("asserted_status", "hypothesis")
        new_status = new.get("asserted_status", "hypothesis")
        if STATUS_ORDER[new_status] > STATUS_ORDER[old_status]:
            event("ASSERTED_STATUS_UPGRADED_NOT_PROVEN", cid, before=old_status, after=new_status)

        old_ev, new_ev = _map(old.get("evidence", [])), _map(new.get("evidence", []))
        for eid in sorted(old_ev.keys() - new_ev.keys()):
            event("EVIDENCE_REMOVED", cid, evidence_id=eid)
        for eid in sorted(new_ev.keys() - old_ev.keys()):
            event("EVIDENCE_ADDED_NOT_INDEPENDENTLY_VERIFIED", cid, evidence_id=eid)
        for eid in sorted(old_ev.keys() & new_ev.keys()):
            a, b = old_ev[eid], new_ev[eid]
            if (a["locator"], a["kind"]) != (b["locator"], b["kind"]):
                event("EVIDENCE_ID_REUSED_FOR_DIFFERENT_SOURCE", cid, evidence_id=eid)
            if not a["reviewed"] and b["reviewed"]:
                event("REVIEW_STATUS_SELF_UPGRADED", cid, evidence_id=eid)
            elif a["reviewed"] and not b["reviewed"]:
                event("REVIEW_STATUS_DOWNGRADED", cid, evidence_id=eid)
            if a["applicability"] != "matched" and b["applicability"] == "matched":
                event("APPLICABILITY_SELF_UPGRADED", cid, evidence_id=eid)
            elif a["applicability"] == "matched" and b["applicability"] != "matched":
                event("APPLICABILITY_REGRESSED", cid, evidence_id=eid)
            if a.get("bibliography") != b.get("bibliography"):
                event("BIBLIOGRAPHIC_METADATA_CHANGED", cid, evidence_id=eid)

        old_as, new_as = _map(old.get("assumptions", [])), _map(new.get("assumptions", []))
        for aid in sorted(old_as.keys() - new_as.keys()):
            event("ASSUMPTION_REMOVED_NOT_CLOSED", cid, assumption_id=aid)
        for aid in sorted(new_as.keys() - old_as.keys()):
            event("NEW_ASSUMPTION_INTRODUCED", cid, assumption_id=aid)
        for aid in sorted(old_as.keys() & new_as.keys()):
            a, b = old_as[aid], new_as[aid]
            if a["description"] != b["description"]:
                event("ASSUMPTION_MEANING_CHANGED", cid, assumption_id=aid)
            if a["after"] != b["after"]:
                if b["after"] == "claimed_closed":
                    event("NEW_CLOSURE_ASSERTION_NOT_VERIFIED", cid, assumption_id=aid)
                elif b["after"] == "withdrawn":
                    event("ASSUMPTION_WITHDRAWN_NOT_VERIFIED", cid, assumption_id=aid)
                else:
                    event("ASSUMPTION_REOPENED", cid, assumption_id=aid)
            if a.get("closure_evidence_id") != b.get("closure_evidence_id"):
                event("ASSUMPTION_CLOSURE_LINK_CHANGED", cid, assumption_id=aid)

    counts = {}
    for entry in events:
        counts[entry["code"]] = counts.get(entry["code"], 0) + 1

    return {
        "limit": "Revision differencing, not proof of correctness, safety, or assay reduction.",
        "before_content_sha256": _hash(before),
        "after_content_sha256": _hash(after),
        "before_structural_audit": before_audit,
        "after_structural_audit": after_audit,
        "event_count": len(events),
        "event_counts": dict(sorted(counts.items())),
        "events": events,
        "verified_empirical_reduction": None,
    }
