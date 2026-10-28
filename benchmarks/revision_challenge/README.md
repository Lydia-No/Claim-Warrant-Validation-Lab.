# Synthetic Revision Challenge — v0.3

**Important: authored and labeled in the same development process as the engine. This is a public regression suite, not an independent benchmark, not a blind holdout, and not evidence of superiority over other auditors.**

## Fixed task

For each before/after claim record, decide whether the *change* needs independent re-evaluation of the evidential warrant. This is **not** the question of whether the scientific claim is true. A case may need review even when the final revised claim is correct.

A yes-label means some change to evidence identity, claim strength, source applicability, assumption inventory or inference substance warrants review. A no-label means records are identical or the change is strictly cosmetic or conservative.

Truth labels and their rationales appear openly in `cases.json`. They are **constructed expectations**, not independent adjudicator ratings.

## Comparators

**Snapshot-only review:** runs the existing structural claim/consistency audit on the complete final record. It has the complete AFTER evidence metadata but not provenance from the BEFORE record. This is an intentionally bounded cross-sectional comparator, not a full reviewer.

**Any-field diff:** sees BOTH full records and flags every difference. It cannot miss a literal change but may flag cosmetic edits. This is a change-detection baseline, not a skilled domain critic.

**Targeted revision review:** sees BOTH full records, runs the existing before/after differencer, and classifies pre-declared structural events as requiring review. Pure text edits without numeric-literal changes remain recorded but are **not** automatically classified high-risk, since punctuation is a common source of false alarms. Qualitative semantic changes may consequently be missed. Cases R16 and N08 intentionally expose a false negative and a false positive.

All three use exactly the **same case files**. However, they differ in the information and task framing they are designed to use, so comparing scores does **not** establish additional value over a trained or prompted generic critic with full provenance access.

## Run

```bash
python -m auditlab.benchmark
python -m auditlab.benchmark --json
python -m unittest discover -s tests -v
```

Outputs include explicit TP / FP / FN / TN, precision, recall and specificity. No confidence intervals or effect sizes are justified by this authored synthetic suite.

## Known limitations

- Risk labels are review decisions, not scientific judgments.
- The tool reads declared metadata. It does not inspect the actual contents of cited papers or independent timing/physics reports.
- No held-out external documents, specialist ratings, or evidence of calibration exists yet.
- Rule design and fixture design were co-developed. Passing these tests demonstrates **specified behavior only**.
- An ordinary diff is highly conservative; a full-context generic reviewer could match or outperform the targeted engine.

## Next rigorous evaluation

Acquire permitted material and independent reviewer judgments *before* tuning rules. Set a frozen sample and sampling plan with cosmetic controls, legitimate scope reductions, actual provenance changes, mechanism transfers, and new assumptions introduced during fixes. Compare against an **equally informed generic full-record critic** under matched budget. Pre-register what constitutes an independent verification of citation, derivation and implementation; preserve disagreement, false negatives and false alarms.

Do not import this result into private Research Claim Governance Study 1 or claim it passed any part of that protocol.
