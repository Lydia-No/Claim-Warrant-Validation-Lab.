"""Optional author-metadata warrant and dependency review.

Declared applicability, review and source provenance are not independent proof.
"""
from __future__ import annotations
import re
from .engine import audit

SCOPES = {"principle", "method", "implementation", "performance"}
SHA256 = re.compile(r"^[a-fA-F0-9]{64}$")


def assess_warrants(data: dict) -> dict:
    baseline = audit(data)
    claims = {c["id"]: c for c in data["claims"]}
    results = {}
    for claim in data["claims"]:
        cid = claim["id"]
        issues = []
        required = claim.get("required_evidence_scopes")
        if required is None:
            issues.append({"code": "REQUIRED_SCOPES_UNDECLARED"})
            required = []
        if not isinstance(required, list) or any(x not in SCOPES for x in required):
            raise ValueError(cid + ": invalid required_evidence_scopes")
        declared_coverage = set()
        for ev in claim.get("evidence", []):
            scopes = ev.get("declared_support_scopes", [])
            if not isinstance(scopes, list) or any(x not in SCOPES for x in scopes):
                raise ValueError(cid + ": invalid declared_support_scopes")
            if required and not scopes:
                issues.append({"code": "EVIDENCE_SCOPE_UNDECLARED", "evidence_id": ev["id"]})
            if scopes:
                declared_coverage.update(scopes)
                provenance = ev.get("provenance")
                if not isinstance(provenance, dict):
                    issues.append({"code": "PROVENANCE_NOT_RECORDED", "evidence_id": ev["id"]})
                else:
                    if not provenance.get("source_id") or not provenance.get("record_id"):
                        issues.append({"code": "PROVENANCE_FIELDS_INCOMPLETE", "evidence_id": ev["id"]})
                    digest = provenance.get("sha256")
                    if digest is not None and (not isinstance(digest, str) or not SHA256.fullmatch(digest)):
                        issues.append({"code": "INVALID_PROVENANCE_DIGEST", "evidence_id": ev["id"]})
                if not ev["reviewed"] or ev["applicability"] != "matched":
                    issues.append({"code": "DECLARED_SCOPE_REQUIRES_REVIEW", "evidence_id": ev["id"]})
        for scope in sorted(set(required) - declared_coverage):
            issues.append({"code": "REQUIRED_SCOPE_WITHOUT_DECLARED_SUPPORT", "scope": scope})
        dependencies = claim.get("depends_on", [])
        if not isinstance(dependencies, list) or any(not isinstance(x, str) for x in dependencies):
            raise ValueError(cid + ": depends_on must be list of IDs")
        for target in set(dependencies):
            if target not in claims:
                issues.append({"code": "UNKNOWN_DEPENDENCY", "dependency_id": target})
            elif target == cid:
                issues.append({"code": "SELF_DEPENDENCY"})
        results[cid] = {
            "issues": issues,
            "required_scopes": sorted(set(required)),
            "declared_scopes": sorted(declared_coverage),
            "depends_on": sorted(set(dependencies)),
            "automatically_verified": False,
        }

    # Graph cycles are flagged, not treated as logical impossibilities.
    visiting, visited, cyclical = set(), set(), set()
    def visit(node, path):
        if node in visiting:
            cyclical.update(path[path.index(node):])
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in results[node]["depends_on"]:
            if dependency in claims:
                visit(dependency, path + [dependency])
        visiting.remove(node)
        visited.add(node)
    for node in claims:
        visit(node, [node])
    for node in cyclical:
        results[node]["issues"].append({"code": "DEPENDENCY_CYCLE_REQUIRES_REVIEW"})

    # Propagate uncertainty, not falsity: issues cannot prove downstream claims false.
    unresolved = {c["id"] for c in baseline["claim_results"] if c["issues"]}
    unresolved.update(cid for cid, item in results.items() if item["issues"])
    changed = True
    while changed:
        changed = False
        for cid, item in results.items():
            if cid not in unresolved and any(dep in unresolved for dep in item["depends_on"]):
                unresolved.add(cid)
                changed = True
    for cid, item in results.items():
        item["upstream_review_required"] = sorted(
            dep for dep in item["depends_on"] if dep in unresolved
        )
    return {
        "limit": "Author-supplied evidence scope and graph metadata; never independently validated",
        "claims_examined": len(claims),
        "review_required_claims": sorted(unresolved),
        "claim_results": results,
        "verified_empirical_reduction": None,
    }
