# v0.3 Synthetic Revision Challenge — Recorded Run

**Recorded from GitHub Actions:** [Run 40785950674](https://github.com/Lydia-No/Claim-Warrant-Validation-Lab./actions/runs/40785950674), commit `8b09ce6aee5a4bd38542a2fe662eac908a008cfa`.

**WARNING:** These are openly labeled, **in-sample synthetic regression results**. Fixtures were authored alongside the rule engine. This does **not** establish external scientific validity, performance against a capable human auditor, or a generalizable advantage over a generic agent with complete records.

The binary target is **does the *revision* merit independent re-examination of its evidential warrant?**, not **is the claim false?**.

| Comparator | TP | FP | FN | TN | Precision | Recall |
|---|---:|---:|---:|---:|---:|---:|
| Snapshot-only structural review (AFTER) | 4 | 0 | 13 | 11 | 1.0000 | 0.2353 |
| Any-field full-record diff (BEFORE + AFTER) | 17 | 10 | 0 | 1 | 0.6296 | 1.0000 |
| Targeted revision events (BEFORE + AFTER) | 16 | 1 | 1 | 10 | 0.9412 | 0.9412 |

- 28 synthetic pairs: 17 author-labeled review-positive, 11 author-labeled controls.
- 37 automated tests passed in the recorded CI run.
- **Known miss R16:** a qualitative shift from one instrument to another changes the claim's meaning; current targeted rules record a textual edit but cannot classify the semantic shift.
- **Known false alarm N08:** capitalization-only DOI metadata change is treated as citation-metadata change, even when the normalized DOI is identical.

**Interpretation:** The tests demonstrate the difference between snapshot checks, unfiltered change reporting and targeted structural flags *on scenarios developed for those rules*. They do not establish a scientific method advantage. In particular, the snapshot comparator does not have BEFORE context, and the full diff comparator does not perform domain-specific reasoning. They are bounded baselines, not an equally informed generic critic.

## To reproduce

```bash
python -m auditlab.benchmark
python -m auditlab.benchmark --json
python -m unittest discover -s tests -v
```

## Next scientific gate

1. Obtain authorized external documents with before/after revisions.
2. Freeze case selection and reviewer criteria before inspecting model results.
3. Get independent specialist labels and record adjudicator disagreements.
4. Compare against **a generic full-record critic with the same sources, revision history and computational budget**, not merely a snapshot or naive diff.
5. Report both false positives and false negatives, including changes the current tool does not detect.
6. Separate the public exercise from the locked private Research Claim Governance Study 1 and avoid importing results into that study.

No third-party proprietary blueprint text or private research implementation was uploaded as part of this run.
