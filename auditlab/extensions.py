"""Local-first optional extension CLI; all operations offline and stdlib-only.

Usage:
  python -m auditlab.extensions --extract-markdown LOCAL.md
  python -m auditlab.extensions --records claims.json
  python -m auditlab.extensions --compare before.json after.json
"""
import argparse
import json
from .engine import audit, load_records
from .compare import compare
from .claim_extract import extract_file
from .arithmetic import check_arithmetic
from .warrants import assess_warrants
from .source_bindings import verify_sources
from .reviewer_panel import review_source_bindings


def inspect_records(data):
    math = {}
    for c in data["claims"]:
        checks = c.get("arithmetic_checks", [])
        if not isinstance(checks, list):
            raise ValueError(c["id"] + ": arithmetic_checks must be list")
        math[c["id"]] = check_arithmetic(checks)
    return {"structural": audit(data), "warrants": assess_warrants(data),
            "literal_arithmetic": math,
            "automatically_verified": False}


def compare_record_extensions(before, after):
    old = {c["id"]: c for c in before["claims"]}
    new = {c["id"]: c for c in after["claims"]}
    events = []
    fields = {
        "required_evidence_scopes": "SCOPE_REQUIREMENTS_CHANGED",
        "depends_on": "DEPENDENCY_LINKS_CHANGED",
        "arithmetic_checks": "ARITHMETIC_CHECK_SPEC_CHANGED",
    }
    for cid in sorted(old.keys() & new.keys()):
        a, b = old[cid], new[cid]
        for field, code in fields.items():
            if a.get(field) != b.get(field):
                events.append({"claim_id": cid, "code": code})
        sources_a = {e["id"]: e for e in a.get("evidence", [])}
        sources_b = {e["id"]: e for e in b.get("evidence", [])}
        for eid in sorted(sources_a.keys() & sources_b.keys()):
            x, y = sources_a[eid], sources_b[eid]
            for field, code in [
                ("declared_support_scopes", "EVIDENCE_SUPPORT_SCOPE_CHANGED"),
                ("provenance", "PROVENANCE_METADATA_CHANGED"),
            ]:
                if x.get(field) != y.get(field):
                    events.append({"claim_id": cid, "evidence_id": eid, "code": code})
    return {"events": events, "event_count": len(events),
            "limit": "Metadata changes; no scientific validation"}


def main():
    parser = argparse.ArgumentParser(description="Local-only experimental structural extensions")
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--extract-markdown", metavar="FILE")
    choice.add_argument("--records", metavar="JSON")
    choice.add_argument("--compare", nargs=2, metavar=("BEFORE", "AFTER"))
    choice.add_argument("--source-check", nargs=3, metavar=("RECORDS", "BUNDLE", "ROOT"))
    parser.add_argument("--ratings", metavar="LOCAL_JSON", help="Optional local reviewer ratings; valid only with --source-check")
    args = parser.parse_args()
    if args.ratings and not args.source_check:
        parser.error("--ratings requires --source-check")
    if args.source_check:
        records, bundle_path, root = args.source_check
        with open(bundle_path, encoding="utf-8") as stream:
            bundle = json.load(stream)
        report = verify_sources(load_records(records), bundle, root)
        result = {"source_attestation": report}
        if args.ratings:
            with open(args.ratings, encoding="utf-8") as stream:
                ratings = json.load(stream)
            result["reviewer_opinions"] = review_source_bindings(report, ratings)
    elif args.extract_markdown:
        result = {"candidate_index": extract_file(args.extract_markdown)}
    elif args.records:
        result = {"extended_audit": inspect_records(load_records(args.records))}
    else:
        before, after = [load_records(p) for p in args.compare]
        result = {"revision": compare(before, after),
                  "extended_before": inspect_records(before),
                  "extended_after": inspect_records(after),
                  "extension_changes": compare_record_extensions(before, after)}
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
