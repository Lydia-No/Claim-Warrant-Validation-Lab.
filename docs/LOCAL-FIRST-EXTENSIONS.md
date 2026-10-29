# Local-first structural extensions (experimental)

These opt-in Python-standard-library tools extend the public sandbox without changing the existing v0.4 audit or comparison commands.

## Scope and boundaries

- These tools **never** independently verify research findings, theorem proofs, reported hardware performance, source content, regimes, or scientific novelty.
- Source and claim metadata are author-supplied, even when a field says `reviewed: true` or `applicability: matched`.
- No external services or network access are used by these extension commands.
- The claim identifier index only extracts literal `[CLAIM-...]` tags and local line numbers (excluding fenced Markdown code); it does not understand the claims or infer evidence.
- The arithmetic checker only computes explicitly supplied literal sums, products, differences, pairwise coprimality, and explicitly provided clock cycles / MHz to nanoseconds. A matching result is **not** formal proof or engineering verification.
- Dependency flags indicate possible downstream review requirements, not scientific falsity or causal certainty.
- Evidence scope labels are exact declarations: `principle`, `method`, `implementation`, `performance`. A paper supporting a principle is **not** automatically considered evidence of implementation or performance.
- Provenance fields are bookkeeping assertions, **not** independently authenticated custody.

## Commands (offline)

```bash
python -m auditlab.extensions --extract-markdown /path/to/authorized/source.md
python -m auditlab.extensions --records examples/synthetic_extended.json
python -m auditlab.extensions --compare examples/synthetic_revision_before.json examples/synthetic_revision_after.json
python -m unittest discover -s tests -v
```

Each command emits structured JSON to standard output. Run it locally. If redirecting the result to a file, choose a directory outside the public repository for restricted inputs. There is no automatic file upload or report commit.

## Optional extra fields in existing claim JSON

```json
{
  "claims": [{
    "id": "S-CALC-001",
    "statement": "An illustrative result has a documented justification.",
    "asserted_status": "supported",
    "required_evidence_scopes": ["principle", "performance"],
    "depends_on": [],
    "evidence": [{
      "id": "S-E-001",
      "kind": "publication",
      "locator": "synthetic://example",
      "reviewed": false,
      "applicability": "unknown",
      "declared_support_scopes": ["principle"],
      "provenance": {"source_id": "S-SOURCE-001", "record_id": "S-RECORD-001"}
    }],
    "assumptions": [],
    "arithmetic_checks": [{
      "id": "SUM-001",
      "operation": "sum",
      "values": [2, 3],
      "expected": 5
    }]
  }]
}
```

Source identifiers and record IDs are submitted assertions. A SHA-256 digest may be supplied as `provenance.sha256`; a valid-format digest is not proof of file custody. Missing scope declarations and incomplete provenance produce review flags, never auto-verification.

## Revision analysis

The new `--compare` command also emits extension metadata events for changed dependency links, requested support scopes, declared evidence coverage, arithmetic check definitions and provenance fields. The original revision differencer remains unchanged. No finding from the extension is included in empirical accuracy claims.

## Privacy rule

**Never commit proprietary documents, extracted claim text, private test manifests, or case-specific results to this public repository, including feature branches, pull requests or CI artifacts.** Keep local tests outside the repository; use only intentionally synthetic fixtures here. `.gitignore` is not an access-control mechanism.

## Limitations

These rules do not establish bibliographic support or automatically read scientific publications. Crossref remains a separate opt-in record-identification feature in the existing CLI. A literature connector is not required for these local structural checks.
