# Claim-Warrant Validation Lab

**Public, independent, experimental research-claim and revision audit sandbox.**

**Research direction and project ownership:** Linda Thorstensen. AI assistance is limited to implementation, testing, drafting and verification support under her direction.

This public demonstrator is **not** the private Research Claim Governance implementation or a release of ArcTopia research, protocols, datasets or restricted keys.

## Core question

When a technical document fixes a weak citation or calculation, has the revision reduced its *unverified assumptions*, or merely replaced them with newer explanations and stronger labels?

### What v0.4 can do

1. **Structural claim checks:** flag missing evidence, declared applicability mismatches, and unjustified "proven" labels (author-supplied metadata only).
2. **Before/after comparison:** match stable IDs across snapshots; report added/removed claims, newly asserted closures, changed assumptions, relabeled evidence and status upgrades. Removed claims/assumptions are never counted as verified.
3. **Synthetic revision challenge:** an openly labeled, 28-case regression suite compares snapshot-only checking, any-field diffs, and targeted structural review. It contains deliberately exposed false positives and false negatives and is not an independent benchmark.
4. **External pilot toolkit (NOT yet executed):** a documented prospective protocol, equally informed generic-critic prompt, two-reviewer template and a local scorer that excludes disagreements and uncertainty rather than inventing negative labels. Demo reviewer ratings are fictional.
5. **Optional independent DOI metadata lookup:** explicitly opt in to querying Crossref's `/works/{doi}` endpoint. Compare the returned DOI, title, publication year and optional author, journal, volume, issue, pages against *declared bibliographic metadata*. This is **record identification**, not scientific verification.

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

# Open synthetic regression challenge (no network)
python -m auditlab.benchmark
python -m auditlab.benchmark --json

# Exploratory pilot SCORER DEMO: all case data and reviewer ratings are invented
python -m auditlab.pilot --cases pilot/demo/cases.json --reviewer-a pilot/demo/ratings_a.json --reviewer-b pilot/demo/ratings_b.json --generic pilot/demo/generic_predictions.json --json

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

For the interpretation and limitations, see [external pilot protocol](pilot/TRIAL-PROTOCOL.md), [pilot execution notes](pilot/README.md), [protocol](docs/PROTOCOL.md), [synthetic challenge](benchmarks/revision_challenge/README.md) and [external trial](docs/EXTERNAL-TRIAL.md).

## Public external candidate pool — collected 2026-10-29

A first, **retrospectively selected, unblinded** list of 10 actual upstream technical-document/code revisions from two independent open-source projects is available in [public candidate discovery](pilot/external_candidates/README.md), with [immutable source pointers](pilot/external_candidates/CANDIDATES.json). For every candidate, the selected file was successfully retrieved at its first-parent commit and at the merged commit, and the content differed.

**This is candidate discovery, not an external study result.** The selection was enriched for previously reported errors, no claim-level extraction has been locked, no independent reviewers have rated anything, and no external method comparison has been run. The source files remain in their upstream projects.

## Real upstream document extracts — unblinded feasibility

Nine of the ten public SciPy/PyTorch revision candidates have been converted into **source-pinned, AI-assisted, claim-level BEFORE/AFTER paraphrases**, following a rule documented in a separate GitHub commit **before the extraction records were committed**. One implementation-only change remains explicitly excluded from this textual-claim pilot; it has not been discarded.

See the [extraction ledger](pilot/external_candidates/SELECTION-LEDGER.json), [immutable source-pinned pairs](pilot/external_candidates/EXTRACTED-PAIRS.json), [extraction rule](pilot/external_candidates/EXTRACTION-RULE.md) and [input preflight checks](auditlab/external_preflight.py).

**Not independent validation.** The source revisions were selected and interpreted with knowledge of upstream correction discussions. Claim paraphrases, empty evidence lists and neutral API-status placeholders are **not** verified external evidence. No human reviewer ratings or equal-information generic-critic comparisons have yet been performed.

Run the offline integrity preflight:

```bash
python -m auditlab.external_preflight
```

## Unblinded real-source diagnostic (not a benchmark)

The nine source-pinned external paraphrases can now be passed through the **existing, unchanged** structural event rules without adding any human or assumed truth labels:

```bash
python -m auditlab.external_diagnostic
python -m auditlab.external_diagnostic --json
```

A review flag indicates an edit the deterministic structural rules choose to surface—not that an error was proved. An unflagged wording change is **not** an independently confirmed safe revision. This diagnostic does **not** compute effectiveness scores. See [methodological threats](pilot/external_candidates/METHOD-THREAT-REVIEW.md) and [diagnostic usage](pilot/external_candidates/DIAGNOSTIC.md).

The central research limitation remains: these real revisions have no independently constructed evidence-provenance trails or human reference ratings. Detecting public formula edits is not proof of detecting unsupported scientific claims.

## Historical evidence chains — source-backed discovery, not independent findings

To move beyond formula-edit detection, three public historical **evidence-change cases** now include 10 dated claim stages, 10 source records and 11 explicit open questions across economics, observational cosmology and particle-physics metrology:

- Reinhart–Rogoff debt/growth replication and erratum (2010–2013).
- BICEP2/Keck–Planck foreground re-analysis (2014–2015).
- OPERA neutrino timing and instrumental reassessment (2011–2012).

See [evidence chain dossiers](pilot/evidence_chains/README.md) and [methodological decision](pilot/evidence_chains/METHOD-DECISION.md). Their **source/time linkage** can be checked with `python -m auditlab.evidence_chains`. This does **not** check source truth, reproduce raw experiments or award scientific claim entitlement, and does not create an unbiased test cohort.

## Privacy and external collaboration

Everything committed here is synthetic or public documentation. Never commit unpublished third-party blueprints, private datasets, partner code, secrets, or any restricted ArcTopia work. If a partner wants to test the framework against their own proprietary documents, they can run it **locally** and share only a reviewed, sanitized report if they choose.

The online Crossref option sends only DOI identifiers (not claim text, blueprints or assumption descriptions). The tool will not make any network request without `--check-dois`.

## Status and intellectual property

**v0.4: structural prototype with a prepared external pilot scoring procedure (NOT YET EXECUTED), paired revision diffing, authored synthetic regression challenge and opt-in Crossref bibliographic checks.** The synthetic regression cases and automated tests are software tests, not empirical validation of research findings. The tool does not implement, supersede or claim to validate the locked private Research Claim Governance Study 1.

Copyright © 2026 Linda Thorstensen. No software license has been granted by this repository. Public visibility alone does not grant unrestricted rights to reproduce, redistribute or reuse the code. Licensing may be decided separately.
