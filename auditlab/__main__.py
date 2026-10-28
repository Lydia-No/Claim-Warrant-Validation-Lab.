"""Claim-Warrant Validation Lab CLI: structural checks, revision diff, opt-in DOI lookup."""
import argparse
import json
from .engine import audit, load_records
from .compare import compare
from .bibliography import check_bibliography


def main() -> None:
    parser = argparse.ArgumentParser(description="Experimental claim-warrant audit; never independently certifies scientific validity")
    parser.add_argument("file", nargs="?", help="Single claim record JSON (legacy v0.1 mode)")
    parser.add_argument("--compare", nargs=2, metavar=("BEFORE", "AFTER"),
                        help="Compare two versioned claim-record snapshots")
    parser.add_argument("--check-dois", action="store_true",
                        help="OPT-IN online Crossref bibliographic metadata checks (sends DOI identifiers)")
    parser.add_argument("--max-dois", type=int, default=25, help="Online lookup cap (1–100; default 25)")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args()

    if args.compare and args.file:
        parser.error("Use either a file OR --compare BEFORE AFTER")
    if not args.compare and not args.file:
        parser.error("Supply a claim JSON file or --compare BEFORE AFTER")
    if not 1 <= args.max_dois <= 100:
        parser.error("--max-dois must be between 1 and 100")

    if args.compare:
        before, after = map(load_records, args.compare)
        result = {"revision": compare(before, after)}
        target = after
    else:
        target = load_records(args.file)
        result = {"audit": audit(target)}

    if args.check_dois:
        result["bibliography"] = check_bibliography(target, online=True, max_lookups=args.max_dois)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print("CLAIM-WARRANT VALIDATION LAB — EXPERIMENTAL; NOT SCIENTIFIC VERIFICATION")
    if "audit" in result:
        a = result["audit"]
        print(f"Claims: {a['claims_examined']} | Structural findings: {a['issues_count']}")
        print(f"Candidate closures (not verified): {a['structurally_eligible_closures_not_verified']}")
        print(f"Withdrawals from scope (not proofs): {a['withdrawn_from_scope_not_verified']}")
        for claim in a["claim_results"]:
            print(f"\n{claim['id']} ({claim['asserted_status']}):")
            for issue in claim["issues"]:
                print("  - " + issue["code"])
    else:
        r = result["revision"]
        print(f"Revision changes: {r['event_count']} | Before/after fingerprints recorded")
        print(f"Before: {r['before_content_sha256']}")
        print(f"After:  {r['after_content_sha256']}")
        for ev in r["events"]:
            print(f"  - {ev['claim_id']}: {ev['code']}")
    if "bibliography" in result:
        b = result["bibliography"]
        print(f"Crossref DOI lookups: {b['external_lookups_attempted']} (metadata only)")
        for pub in b["results"]:
            print(f"  - {pub['claim_id']}/{pub['evidence_id']}: {pub['status']}")
    print("\nIndependent scientific/physical verification: NOT PERFORMED. Assay reduction: UNKNOWN.")


if __name__ == "__main__":
    main()
