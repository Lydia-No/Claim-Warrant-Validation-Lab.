# Claim-Warrant Validation Lab

**Public, independent, experimental research-claim and revision audit sandbox.**

**Research direction and project ownership:** Linda Thorstensen. AI assistance is limited to implementation, testing, drafting and verification support under her direction.

This public demonstrator is **not** the private Research Claim Governance implementation or a release of ArcTopia research, protocols, datasets or restricted keys.

## Why this exists

Technical and research claims can become stronger on paper without acquiring stronger evidence. A revised citation, more confident wording or a removed assumption does not by itself show that a claim has been verified. This **public, experimental tool** makes selected claim/evidence/assumption records and document revisions easier to inspect, so that missing support can be left unresolved instead of silently treated as closed.

It is **not** an automatic scientific truth checker, a certified review service, or evidence that the separate private Research Claim Governance method has been validated.

## See the idea in a minute — fictional example

Imagine a completely fictional technical report:

1. **Claim:** "This equipment is proven to work in our operating environment."
2. **Available evidence:** A laboratory test was conducted under different conditions.
3. **Revision:** The report changes the claim to "verified" but introduces no independent evidence that the test transfers to the target environment.

The useful question is not whether the new sentence *sounds* more convincing. It is whether the underlying evidence is applicable, which assumptions remain open, and whether a status upgrade has been justified. The public lab can **flag structural mismatches and record changes**; only appropriate independent assessment could establish whether the real-world claim is scientifically true.

This example is invented, outside every private blinded Study 1 case. It **does not reproduce or reveal the L0–L5 rubric**.

### Try the existing public sandbox locally

The repository already contains Python code, invented sample records, a revision comparator and tests; there is no need to wait for the separate blinded study to run it. With Python 3.10+ from the repository root:

```bash
# Inspect three explicitly synthetic claim records (including an applicability mismatch).
python -m auditlab examples/synthetic_claims.json

# Inspect what changes between two synthetic document versions.
python -m auditlab --compare examples/synthetic_revision_before.json examples/synthetic_revision_after.json

# Run code-level checks; these are not scientific validation.
python -m unittest discover -s tests -v
```

See [the synthetic input](examples/synthetic_claims.json), [the independent external pilot limitations](pilot/README.md), and [source-bound local checking](docs/SOURCE-BOUND-PILOT.md). No private case packet or personal data is required. Use only authorized local inputs; do not commit sensitive material to the public repository.

## Public sandbox versus private Study 1

| | Public Claim–Warrant Validation Lab | Separate, blinded Research Claim Governance Study 1 |
|---|---|---|
| **Available now** | Experimental CLI, synthetic examples, structural checks, documentation and a prepared but unexecuted external pilot | [Volunteer invitation](INDEPENDENT-REVIEWERS.md) describing the participation request |
| **Not established** | Independent scientific validity, generalization or superior auditing effectiveness | Independent reviewer agreement or validation; human review has not been completed |
| **Disclosure** | Public code and deliberately bounded examples | Six-level L0–L5 rubric, 16 locked vignettes, pairing key, expected outcomes and individual ratings remain private |

### What happens next (conditional, not a release promise)

1. **Now:** Keep the public lab runnable and recruit eligible independent reviewers for the separate, locked Study 1.
2. **After a properly completed human-review gate:** Evaluate agreement, uncertainty, disagreements and null outcomes, then decide what findings can responsibly be reported. There is **no inter-rater reliability result to report yet**.
3. **Only after explicit disclosure, participant-privacy and IP review:** Consider a bounded methodological report, authorized illustrative materials or further tools. The locked rubric and case set **are not scheduled for automatic public release**.

Interested in independent review? Read [the full voluntary invitation](INDEPENDENT-REVIEWERS.md). The verified contact address is **linda@arctopia.no** (subject: **Independent reviewer – Claim Warrant Study 1**). The work is unpaid; eligibility and consent are checked before any private study materials are shared. Reviewers are **not** being asked to endorse ArcTopia.

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

## Scientific readiness and originality gate — 2026

A **fail-closed readiness gate** now checks whether the three historical source-linked correction narratives can actually support a same-terminal-evidence, independent comparative study. **They cannot yet.** The tool checks source chronology and dossier structure, not scientific validity. It explicitly refuses to treat self-marked statuses as independent source verification.

```bash
python -m auditlab.readiness
python -m auditlab.readiness --json
```

See [readiness assessment](pilot/evidence_chains/READINESS-RESULT.md), [machine-readable evidence gap ledger](pilot/evidence_chains/ELIGIBILITY-LEDGER.json) and the [updated 2026 prior-art check](pilot/evidence_chains/PRIOR-ART-2026.md). Related 2026 literature already studies agentic forking paths, evidence chains and correct-value/wrong-source semantic binding. No originality or comparative accuracy claim has been established for this public lab.

## Privacy and external collaboration

Everything committed here is synthetic or public documentation. Never commit unpublished third-party blueprints, private datasets, partner code, secrets, or any restricted ArcTopia work. If a partner wants to test the framework against their own proprietary documents, they can run it **locally** and share only a reviewed, sanitized report if they choose.

The online Crossref option sends only DOI identifiers (not claim text, blueprints or assumption descriptions). The tool will not make any network request without `--check-dois`.

## Status and intellectual property

**v0.4: structural prototype with a prepared external pilot scoring procedure (NOT YET EXECUTED), paired revision diffing, authored synthetic regression challenge and opt-in Crossref bibliographic checks.** The synthetic regression cases and automated tests are software tests, not empirical validation of research findings. The tool does not implement, supersede or claim to validate the locked private Research Claim Governance Study 1.

Copyright © 2026 Linda Thorstensen. No software license has been granted by this repository. Public visibility alone does not grant unrestricted rights to reproduce, redistribute or reuse the code. Licensing may be decided separately.

## Optional local-first structural extensions (experimental)

A separate offline CLI provides **literal claim-ID indexing**, explicit **evidence-support scope review**, **dependency review**, **provenance-field integrity checks**, and **submitted-literal arithmetic checks**. These features do **not** establish scientific truth, assess external papers, or certify engineering results. They use only author-supplied metadata and require independent adjudication. The existing CLI, pilot and baseline remain unchanged.

```bash
python -m auditlab.extensions --records examples/synthetic_extended.json
python -m auditlab.extensions --extract-markdown /path/to/authorized/local.md
```

Details: [local-first extensions](docs/LOCAL-FIRST-EXTENSIONS.md). Never place restricted inputs or their derived outputs in this public repository or any public GitHub branch.

## Source-bound local pilot (offline; no scientific verification)

A separate, opt-in experimental source-anchoring layer checks that **authorized local text files** match pinned SHA-256 digests and that an explicitly supplied quotation appears at specified line numbers. It can link an anchor to declared claim/evidence scope, record reviewer judgments without treating reviewer agreement as proof, and flag scope-widening or source changes across revisions. It does not read or interpret PDFs, validate scientific conclusions, or establish independence of external reviewers.

```bash
python -m auditlab.extensions --source-check examples/source_pilot/claims.json examples/source_pilot/bundle.json examples/source_pilot --ratings examples/source_pilot/ratings.json
```

See [source-bound pilot](docs/SOURCE-BOUND-PILOT.md) for source format, limitations and private-data handling. The synthetic test material is fictional. **Never include proprietary source files, extracted claim data or their results in this public repository.**
