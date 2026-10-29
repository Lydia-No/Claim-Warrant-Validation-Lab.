"""Conservative paired revision of source bindings; no automatic warrant promotion."""
from __future__ import annotations


def source_revision_events(before_bundle: dict, after_bundle: dict) -> dict:
    def unique_map(bundle, field, key):
        items = bundle.get(field)
        if not isinstance(items, list):
            raise ValueError(field + " must be a list")
        result = {}
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get(key), str):
                raise ValueError("invalid " + field + " entry")
            if item[key] in result:
                raise ValueError("duplicate " + field + " ID")
            result[item[key]] = item
        return result

    old_sources = unique_map(before_bundle, "sources", "source_id")
    new_sources = unique_map(after_bundle, "sources", "source_id")
    old_anchors = unique_map(before_bundle, "anchors", "anchor_id")
    new_anchors = unique_map(after_bundle, "anchors", "anchor_id")

    def binding_set(bundle):
        bindings = bundle.get("bindings")
        if not isinstance(bindings, list):
            raise ValueError("bindings must be a list")
        keys = []
        for b in bindings:
            if not isinstance(b, dict):
                raise ValueError("invalid binding")
            fields = tuple(b.get(k) for k in ("claim_id", "evidence_id", "anchor_id", "scope"))
            if not all(isinstance(v, str) and v for v in fields):
                raise ValueError("invalid binding key")
            keys.append(fields)
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate binding")
        return set(keys)

    def origin_set(bundle):
        origins = bundle.get("claim_origins", [])
        if not isinstance(origins, list):
            raise ValueError("claim_origins must be a list")
        points = []
        for origin in origins:
            if not isinstance(origin, dict) or not isinstance(origin.get("claim_id"), str) or not isinstance(origin.get("anchor_id"), str):
                raise ValueError("invalid claim origin")
            points.append((origin["claim_id"], origin["anchor_id"]))
        if len(set(points)) != len(points):
            raise ValueError("duplicate claim origin")
        return set(points)

    old_origins, new_origins = origin_set(before_bundle), origin_set(after_bundle)
    before = binding_set(before_bundle)
    after = binding_set(after_bundle)
    events = []

    def event(code, **details):
        events.append({"code": code, **details})

    for sid in sorted(new_sources.keys() - old_sources.keys()):
        event("SOURCE_RECORD_ADDED_NOT_VERIFIED", source_id=sid)
    for sid in sorted(old_sources.keys() - new_sources.keys()):
        event("SOURCE_RECORD_REMOVED_NOT_RESOLVED", source_id=sid)
    for aid in sorted(new_anchors.keys() - old_anchors.keys()):
        event("ANCHOR_ADDED_NOT_VERIFIED", anchor_id=aid)
    for aid in sorted(old_anchors.keys() - new_anchors.keys()):
        event("ANCHOR_REMOVED_NOT_RESOLVED", anchor_id=aid)

    for sid in sorted(old_sources.keys() & new_sources.keys()):
        if old_sources[sid].get("sha256") != new_sources[sid].get("sha256"):
            event("SOURCE_DIGEST_CHANGED_RECHECK_REQUIRED", source_id=sid)
        if old_sources[sid].get("path") != new_sources[sid].get("path"):
            event("SOURCE_PATH_CHANGED_RECHECK_REQUIRED", source_id=sid)
    for aid in sorted(old_anchors.keys() & new_anchors.keys()):
        if old_anchors[aid] != new_anchors[aid]:
            event("ANCHOR_ID_REUSED_WITH_CHANGED_CONTENT", anchor_id=aid)

    for cid, aid in sorted(new_origins - old_origins):
        event("CLAIM_ORIGIN_LINK_ADDED_NOT_EVIDENCE", claim_id=cid, anchor_id=aid)
    for cid, aid in sorted(old_origins - new_origins):
        event("CLAIM_ORIGIN_LINK_REMOVED_NOT_RESOLVED", claim_id=cid, anchor_id=aid)

    for key in sorted(after - before):
        event("SOURCE_BINDING_ADDED_NOT_VERIFIED", claim_id=key[0],
              evidence_id=key[1], anchor_id=key[2], scope=key[3])
    for key in sorted(before - after):
        event("SOURCE_BINDING_REMOVED_NOT_RESOLVED", claim_id=key[0],
              evidence_id=key[1], anchor_id=key[2], scope=key[3])

    # An added scope over unchanged source and unchanged anchor is a review
    # trigger, not proof of unwarranted transfer.
    for cid, eid, aid, scope in sorted(after - before):
        prior = {(x[0], x[1], x[2]) for x in before}
        if (cid, eid, aid) not in prior:
            continue
        source_id = new_anchors.get(aid, {}).get("source_id")
        if (source_id and aid in old_anchors and
                old_anchors[aid] == new_anchors[aid] and
                old_sources.get(source_id) == new_sources.get(source_id)):
            event("SCOPE_BROADENED_SAME_ANCHOR_REVIEW", claim_id=cid,
                  evidence_id=eid, anchor_id=aid, scope=scope)

    return {
        "events": events, "event_count": len(events),
        "limit": "Provenance/binding revision events only; no source truth or semantic entailment",
        "verified_empirical_reduction": None,
    }
