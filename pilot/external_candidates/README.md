# External evidence pilot: public candidate discovery v0.1

**Feasibility discovery completed; external pilot NOT started.** This folder contains public upstream GitHub **metadata only** for 10 independently versioned changes, from two unrelated software/scientific projects. It contains no copied third-party source code, no privately held data, no claim-level annotations and no reviewer ratings.

[Machine-readable candidate register](CANDIDATES.json)

## Discovery observations (29 October 2026)

- 5 candidate revisions are from [SciPy](https://github.com/scipy/scipy), 5 from [PyTorch](https://github.com/pytorch/pytorch).
- Every selected PR was merged at the recorded commit; a first parent ref was resolved.
- The selected technical file was present in the upstream change.
- The public original file was fetched independently at the parent ref and the resulting commit. **All ten pairs were accessible and non-identical at that file path.**
- Commit refs and project links are recorded in the JSON register, not branch-relative URLs.
- The pool was found by searching for *known* documentation/equation fixes. **This is deliberate convenience sampling, enriched for revisions with reported problems**, not a prospective representative sample. It cannot establish method superiority.

## Before the material can be used in a real pilot

1. Apply the [pilot protocol](../TRIAL-PROTOCOL.md) independently of this discovery. Decide whether to use this retrospective pool for **feasibility only** or select an entirely new prospective sample for a fair comparison.
2. Define how a PR involving multiple edits maps to a single claim before extracting. For every retained candidate, select exactly one independently intelligible claim and record the selected source lines and extraction rationale. Record all exclusions.
3. Have source owners' licenses and allowed usage assessed for any copied content; the current register provides links only.
4. Create local structured BEFORE and AFTER JSON for each claim. Preserve literal changes in meaning, documented applicability, evidence *actually used*, and assumptions *actually mentioned*; **never invent independent proof, citation metadata or review status**.
5. Produce blind reviewer packets that **do not expose PR titles, merged status, GitHub issue discussions, case labels or system outputs**. Keep the mapping to public PRs in a separate file accessible only to the study coordinator.
6. Use at least two independent competent reviewers with independent access to underlying sources. The reviewer question concerns **whether the revision warrants evidential review**, not whether an upstream maintainer approved a PR.
7. Run the same paired structured records through the targeted tool and the [full-context generic critic](../GENERIC-CRITIC.md). The latter may receive any materials used by the former and sufficient context to assess the technical claim. Log unequal access.
8. Retain independent reviewer disagreements, meaningful false negatives, and inconclusive results. Do not tune the tools against this pool and later present its results as blind evaluation.

## Why this set is useful but not a breakthrough

Documentation fixes often correct formula notation, algebraic signs, support conditions or dimension descriptions. They are a useful stress test of **change detection**. They are not equivalent to evidence-laundering in long research blueprints, second-order claim verification or high-assurance hardware engineering. Some are explicitly cosmetic or code-only revisions, and formula changes alone do not establish whether an underlying scientific theory is true.

A PR merged upstream can still be wrong, incomplete or superseded. Treat a merged pull request as public **version provenance**, never as independent scientific proof. In particular, the public SciPy rotation documentation underwent multiple related changes; correlated edits must not be double-counted as independent cases.

## Source and IP boundaries

Everything in this folder is bibliographic metadata, technical paths, commit identifiers or original project links. No confidential research, personal correspondence, author materials, claim-level source excerpts or licensed bodies of documentation are stored here. **Do not upload private ArcTopia work or a partner's unpublished blueprints.**

## Current external results

- Candidate document pairs located: **10**
- Verified changed public file paths: **10**
- Extracted and locked claim pairs: **0**
- Independent human reviewer ratings: **0**
- Generic critic predictions on real external cases: **0**
- Valid external comparative effectiveness findings: **0**

## Claim-level preparation status

The [fixed extraction procedure](EXTRACTION-RULE.md) is recorded at commit `0c384e871a65ffa10e6917e472dc5b9fdd81b6ae`. It was written **after examining PR diffs** (unblinded). The subsequent [9 paired paraphrases](EXTRACTED-PAIRS.json) and [complete 10-item selection ledger](SELECTION-LEDGER.json) are inspectable, but neither independent scientific validation nor human rating.

`python -m auditlab.external_preflight` checks ID and source-ref consistency, neutral status, and absence of fabricated evidence/ratings. It **does not** check whether the paraphrases faithfully reproduce the full upstream mathematics.

The implementation-only C++ shape change was retained as an exclusion, not rewritten as a documentation statement. The formatting-only edits are preserved as unchanged-meaning controls. No changed formula has been labelled correct or incorrect by an independent reviewer.
