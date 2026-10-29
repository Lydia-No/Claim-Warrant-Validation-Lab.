"""Offline source-byte, digest and exact-quote anchoring.

This authenticates only agreement between local bytes and supplied metadata.
A matching excerpt never implies that the excerpt supports a scientific claim.
No network I/O; no source passages are returned in the report.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

HEX = re.compile(r"^[0-9a-fA-F]{64}$")
ALLOWED = {".md", ".txt", ".rst"}
MAX_BYTES = 2_000_000


def _entries(value, key):
    items = value.get(key)
    if not isinstance(items, list) or len(items) > 10000:
        raise ValueError(key + " must be a list of <=10000 entries")
    return items


def _unique(items, key):
    indexed = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get(key), str) or not item[key].strip():
            raise ValueError(key + ": nonempty string required")
        if item[key] in indexed:
            raise ValueError(key + ": duplicate " + item[key])
        indexed[item[key]] = item
    return indexed


def _read_source(root: Path, source: dict):
    rel = source.get("path")
    digest = source.get("sha256")
    if not isinstance(rel, str) or not rel or not isinstance(digest, str) or not HEX.fullmatch(digest):
        return "INVALID_SOURCE_DESCRIPTOR", None, None
    if Path(rel).is_absolute() or "\\" in rel or ".." in Path(rel).parts or Path(rel).suffix.lower() not in ALLOWED:
        return "SOURCE_PATH_REJECTED", None, None
    target = (root / rel).resolve()
    if not target.is_relative_to(root):
        return "SOURCE_PATH_REJECTED", None, None
    try:
        if not target.is_file() or target.stat().st_size > MAX_BYTES:
            return "SOURCE_NOT_FOUND_OR_TOO_LARGE", None, None
        raw = target.read_bytes()
        if len(raw) > MAX_BYTES:
            return "SOURCE_NOT_FOUND_OR_TOO_LARGE", None, None
        observed = hashlib.sha256(raw).hexdigest()
        if observed != digest.lower():
            return "SOURCE_DIGEST_MISMATCH", None, observed
        return "SOURCE_BYTES_MATCH_PIN", raw.decode("utf-8"), observed
    except (OSError, UnicodeError, ValueError):
        return "SOURCE_UNREADABLE", None, None


def verify_sources(records: dict, bundle: dict, source_root: str | Path) -> dict:
    """Verify supplied exact source passages and optional evidence bindings.

    Input JSON: sources [{source_id,path,sha256}],
    anchors [{anchor_id,source_id,line_start,line_end,quote}],
    bindings [{claim_id,evidence_id,anchor_id,scope}].
    """
    from .engine import audit
    from .warrants import SCOPES
    audit(records)
    root = Path(source_root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("source_root must be a directory")
    sources = _unique(_entries(bundle, "sources"), "source_id")
    anchors = _unique(_entries(bundle, "anchors"), "anchor_id")
    bindings = _entries(bundle, "bindings")
    claims = {c["id"]: c for c in records["claims"]}
    source_reports, anchor_reports, binding_reports = {}, {}, []
    text_by_source = {}
    for sid, source in sources.items():
        state, content, actual_digest = _read_source(root, source)
        source_reports[sid] = {"status": state, "sha256_observed": actual_digest}
        if content is not None:
            text_by_source[sid] = content.splitlines()

    for aid, anchor in anchors.items():
        sid = anchor.get("source_id")
        start, end, quote = anchor.get("line_start"), anchor.get("line_end"), anchor.get("quote")
        status = "SOURCE_NOT_PINNED"
        if sid in sources and source_reports[sid]["status"] == "SOURCE_BYTES_MATCH_PIN":
            lines = text_by_source[sid]
            if (type(start) is int and type(end) is int and isinstance(quote, str)
                    and 1 <= start <= end <= len(lines) and end - start <= 30
                    and 8 <= len(quote) <= 4000):
                excerpt = "\n".join(lines[start - 1:end])
                status = "EXACT_QUOTE_MATCH" if quote in excerpt else "EXACT_QUOTE_MISMATCH"
            else:
                status = "INVALID_LINE_ANCHOR"
        anchor_reports[aid] = {"source_id": sid, "line_start": start, "line_end": end, "status": status}

    for entry in bindings:
        if not isinstance(entry, dict):
            raise ValueError("binding must be a dictionary")
        cid, eid, aid, scope = (entry.get(k) for k in ("claim_id", "evidence_id", "anchor_id", "scope"))
        if not all(isinstance(v, str) and v for v in (cid, eid, aid, scope)):
            raise ValueError("binding IDs and scope must be nonempty strings")
        if scope not in SCOPES:
            raise ValueError("unknown evidence scope")
        claim = claims.get(cid)
        ev = next((e for e in claim.get("evidence", []) if e["id"] == eid), None) if claim else None
        if ev is None:
            status = "UNKNOWN_CLAIM_OR_EVIDENCE"
        elif aid not in anchor_reports:
            status = "ANCHOR_NOT_FOUND"
        elif anchor_reports[aid]["status"] != "EXACT_QUOTE_MATCH":
            status = "ANCHOR_NOT_AUTHENTICATED"
        elif scope not in ev.get("declared_support_scopes", []):
            status = "SCOPE_NOT_DECLARED_FOR_EVIDENCE"
        else:
            status = "SOURCE_ANCHOR_MATCH_NOT_SEMANTIC_SUPPORT"
        binding_reports.append({"claim_id": cid, "evidence_id": eid,
                                "anchor_id": aid, "scope": scope, "status": status})

    return {
        "limit": "Local bytes and literal excerpts only; no independent scientific support",
        "no_scientific_verification": True,
        "sources": source_reports, "anchors": anchor_reports,
        "bindings": binding_reports,
        "verified_empirical_reduction": None,
    }
