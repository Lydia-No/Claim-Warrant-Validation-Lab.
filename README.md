# Claim-Warrant Validation Lab

**Public, independent, experimental research-claim and revision audit sandbox.**

**Research direction and project ownership:** Linda Thorstensen. AI assistance is limited to implementation, testing, drafting and verification support under her direction.

This public demonstrator is **not** the private Research Claim Governance implementation or a release of ArcTopia research, protocols, datasets or restricted keys.

## Core question

When a technical document fixes a weak citation or calculation, has the revision reduced its *unverified assumptions*, or merely replaced them with newer explanations and stronger labels?

### What v0.2 can do

1. **Structural claim checks:** flag missing evidence, declared applicability mismatches, and unjustified "proven" labels (author-supplied metadata only).
2. **Before/after comparison:** match stable IDs across snapshots; report added/removed claims, newly asserted closures, changed assumptions, relabeled evidence and status upgrades. Removed claims/assumptions are never counted as verified.
3. **Optional independent DOI metadata lookup:** explicitly opt in to querying Crossref's `/works/{doi}` endpoint. Compare the returned DOI, title, publication year and optional author, journal, volume, issue, pages against *declared bibliographic metadata*. This is **record identification**, not scientific verification.

**It does not** validate physical regimes, prove hardware timing or mathematical identities, verify standards compliance, detect all retractions, establish independence of reviewers, or justify any numeric assay reduction.

## Install / run (Python 3.10+; standard library only)

```bash
# Single-record audit (offline)
python -m auditlab examples/synthetic_claims.json

# Revision analysis: what did the new version actually change?
python -m auditlab --compare examples/synthetic_revision_before.json examples/synthetic_revision_after.json

# Machine-readable revision report
python -m auditlab --compare examples/synthetic_revision_before.json examples/synthetic_revision_after.json --json

# OPTIONAL: query Crossref using DOIs in AFTER (sends DOI identifiers to Crossref)
python -m auditlab --compare examples/synthetic_revision_before.json examples/synthetic_revision_after.json --check-dois --json

# Local automated checks (no network)
python -m unittest discover -s tests -v
```

The synthetic examples have no real scholarly DOIs. To try the optional metadata lookup, prepare **your own authorized** JSON records using registered publication DOIs. Non-DOI or synthetic locators return `unsupported_locator`, not "phantom."

## Minimal data format

```json
{
  "claims": [{
    "id": "C-001",
    "statement": "An example numerical method satisfies a claimed bound.",
    "asserted_status": "supported",
    "evidence": [{
      "id": "E-001",
      "kind": "publication",
      "locator": "10.1234/placeholder",
      "reviewed": false,
      "applicability": "unknown",
      "bibliography": {
        "doi": "10.1234/placeholder",
        "title": "Expected exact title",
        "year": 2024,
        "first_author": "Example"
      }
    }],
    "assumptions": [{
      "id": "A-001",
      "description": "Published operating regime transfers to target hardware",
      "after": "open"
    }]
  }]
}
```

The DOI above is **only a placeholder**. `reviewed` and `applicability` are asserted *input labels*, not audited results. The `bibliography` object is optional, but a Crossref metadata-match result requires at least a matching title and publication year. Optional `first_author`, `container_title`, `volume`, `issue`, and `page` are checked when supplied.

Stable claim/evidence/assumption IDs across snapshots are essential. Reusing an ID for new content is flagged. JSON content fingerprints support audit bookkeeping; they do not prove a file's external provenance.

For the interpretation and limitations, see [protocol](docs/PROTOCOL.md) and [external trial](docs/EXTERNAL-TRIAL.md).

## Privacy and external collaboration

Everything committed here is synthetic or public documentation. Never commit unpublished third-party blueprints, private datasets, partner code, secrets, or any restricted ArcTopia work. If a partner wants to test the framework against their own proprietary documents, they can run it **locally** and share only a reviewed, sanitized report if they choose.

The online Crossref option sends only DOI identifiers (not claim text, blueprints or assumption descriptions). The tool will not make any network request without `--check-dois`.

## Status and intellectual property

**v0.2: structural prototype with opt-in independent bibliographic metadata lookup and paired revision differencing.** The synthetic automated tests are software tests, not empirical validation of research findings. The tool does not implement, supersede or claim to validate the locked private Research Claim Governance Study 1.

Copyright © 2026 Linda Thorstensen. No software license has been granted by this repository. Public visibility alone does not grant unrestricted rights to reproduce, redistribute or reuse the code. Licensing may be decided separately.
