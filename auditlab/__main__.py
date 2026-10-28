"""Usage: python -m auditlab examples/synthetic_claims.json"""
import argparse
import json
from .engine import audit, load_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Structural claim & revision audit (not scientific verification)")
    parser.add_argument("file", help="Path to claim records JSON")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()
    result = audit(load_records(args.file))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("CLAIM-WARRANT VALIDATION LAB — STRUCTURAL AUDIT ONLY")
        print(f"Claims: {result['claims_examined']} | Findings: {result['issues_count']}")
        print(f"Initial open assumptions: {result['assumptions_initially_open']}")
        print(f"Closures with matching reviewed *metadata* (not verified): {result['structurally_eligible_closures_not_verified']}")
        print(f"Withdrawals (not counted as proof): {result['withdrawn_from_scope_not_verified']}")
        for claim in result["claim_results"]:
            print(f"\n{claim['id']} ({claim['asserted_status']}):")
            for finding in claim["issues"]:
                print(f"  - {finding['code']}" + (f" [{finding['evidence_id']}]" if 'evidence_id' in finding else ""))
        print("\nNo empirical or formal verification was performed by this program.")


if __name__ == "__main__":
    main()
