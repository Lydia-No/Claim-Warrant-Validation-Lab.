"""Opt-in bibliographic metadata checking against Crossref.

Crossref registration is not peer-review certification, retraction clearance,
mechanism verification, domain applicability, or reproducibility. Offline by
default. No submitted source text is transmitted; only DOI identifiers.
"""
from __future__ import annotations

import json
import re
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from .engine import audit

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s?#]+", re.IGNORECASE)
PREFIX_RE = re.compile(r"^(?:https?://(?:dx\.)?doi\.org/|doi:)\s*", re.IGNORECASE)


def normalize_doi(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    doi = PREFIX_RE.sub("", value.strip()).strip().lower()
    return doi if DOI_RE.fullmatch(doi) else None


def _simplify(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return "".join(ch for ch in value.casefold() if ch.isalnum())


def _one(value: object) -> str:
    return value[0] if isinstance(value, list) and value and isinstance(value[0], str) else ""


def _record_year(record: dict) -> int | None:
    # Publication year, not deposition or Crossref indexing year.
    for key in ("published", "issued", "published-online", "published-print"):
        parts = record.get(key, {}).get("date-parts", []) if isinstance(record.get(key), dict) else []
        if parts and isinstance(parts[0], list) and parts[0] and type(parts[0][0]) is int:
            return parts[0][0]
    return None


def _crossref_record(doi: str) -> dict | None:
    # Fixed host prevents user-provided URLs from becoming arbitrary fetch targets.
    url = "https://api.crossref.org/works/" + quote(doi, safe="/")
    request = Request(url, headers={"User-Agent": "ClaimWarrantValidationLab/0.2 (research; Crossref metadata only)"})
    try:
        with urlopen(request, timeout=12) as response:
            payload = json.loads(response.read(2_000_001))
    except HTTPError as err:
        if err.code == 404:
            return None
        raise
    if not isinstance(payload, dict) or not isinstance(payload.get("message"), dict):
        raise ValueError("Invalid Crossref response")
    return payload["message"]


def check_bibliography(data: dict, *, online: bool = False, fetcher=None,
                       max_lookups: int = 25) -> dict:
    """Compare explicitly declared bibliographic fields with independent DOI metadata.

    Tests may pass a fake fetcher; actual network access is only via online=True.
    """
    audit(data)  # strict structural validation first
    if type(max_lookups) is not int or not 1 <= max_lookups <= 100:
        raise ValueError("max_lookups must be an integer from 1 to 100")
    publications = [(c["id"], e) for c in data["claims"]
                    for e in c.get("evidence", []) if e["kind"] == "publication"]
    results = []
    lookups = 0
    lookup = _crossref_record if fetcher is None else fetcher
    cache: dict[str, dict | None | Exception] = {}

    for cid, item in publications:
        eid = item["id"]
        expected = item.get("bibliography", {})
        if not isinstance(expected, dict):
            raise ValueError(f"{cid}/{eid}: bibliography must be an object")
        explicit = expected.get("doi")
        if explicit is not None and not isinstance(explicit, str):
            raise ValueError(f"{cid}/{eid}: bibliography.doi must be text")
        doi_locator = normalize_doi(item["locator"])
        doi_expected = normalize_doi(explicit)
        entry = {"claim_id": cid, "evidence_id": eid,
                 "scientific_claim_verified": False,
                 "provider": "Crossref REST /works/{doi}"}
        if explicit is not None and doi_locator and doi_expected != doi_locator:
            entry["status"] = "doi_conflict_in_record"
        elif explicit is not None and not doi_expected:
            entry["status"] = "invalid_doi"
        elif not (doi_expected or doi_locator):
            entry["status"] = "unsupported_locator"
        else:
            doi = doi_expected or doi_locator
            entry["doi"] = doi
            if not online:
                entry["status"] = "not_checked_offline"
            elif doi not in cache and lookups >= max_lookups:
                entry["status"] = "lookup_limit_reached"
            else:
                if doi not in cache:
                    try:
                        cache[doi] = lookup(doi)
                    except Exception as exc:
                        cache[doi] = exc
                    lookups += 1
                record = cache[doi]
                if isinstance(record, Exception):
                    entry["status"] = "lookup_error"
                    entry["error_type"] = type(record).__name__
                elif record is None:
                    entry["status"] = "not_found_in_crossref"
                elif not isinstance(record, dict):
                    entry["status"] = "lookup_error"
                    entry["error_type"] = "InvalidResponse"
                elif normalize_doi(record.get("DOI")) != doi:
                    entry["status"] = "metadata_mismatch"
                    entry["fields_mismatched"] = ["doi"]
                else:
                    mismatched = []
                    supplied = []
                    compare_fields = [
                        ("title", _one(record.get("title"))),
                        ("first_author", (record.get("author") or [{}])[0].get("family", "")
                         if isinstance(record.get("author"), list) and record["author"]
                         and isinstance(record["author"][0], dict) else ""),
                        ("container_title", _one(record.get("container-title"))),
                        ("volume", record.get("volume")),
                        ("issue", record.get("issue")),
                        ("page", record.get("page")),
                    ]
                    for field, actual in compare_fields:
                        if expected.get(field) is not None:
                            if not isinstance(expected[field], str):
                                raise ValueError(f"{cid}/{eid}: {field} must be text")
                            supplied.append(field)
                            if _simplify(actual) != _simplify(expected[field]):
                                mismatched.append(field)
                    if "year" in expected:
                        if type(expected["year"]) is not int:
                            raise ValueError(f"{cid}/{eid}: year must be an integer")
                        supplied.append("year")
                        if _record_year(record) != expected["year"]:
                            mismatched.append("year")
                    if mismatched:
                        entry["status"] = "metadata_mismatch"
                        entry["fields_mismatched"] = mismatched
                    elif {"title", "year"}.issubset(supplied):
                        entry["status"] = "bibliographic_metadata_match_only"
                    else:
                        entry["status"] = "record_found_insufficient_expected_metadata"
        results.append(entry)

    return {"mode": "opt-in online Crossref" if online else "offline (no requests)",
            "external_lookups_attempted": lookups,
            "publications": len(publications),
            "results": results,
            "caveat": "DOI registration and metadata agreement do not establish scientific validity, suitability, safety, or absence of retraction.",
            "verified_empirical_reduction": None}
