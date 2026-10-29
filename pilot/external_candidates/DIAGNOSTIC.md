# Real-source candidate diagnostic (no reference labels)

The following command evaluates the already-frozen, unblinded nine source-pinned **paraphrases** using the existing structural event rules.

```bash
python -m auditlab.external_preflight
python -m auditlab.external_diagnostic
python -m auditlab.external_diagnostic --json
```

**It does not assess scientific validity, calibration, precision, recall, or claim correctness.** The nine cases were selected knowing the public correction history, contain no independently verified evidence traces, and cannot demonstrate the method's claimed unique value.

Review the [method-threat assessment](METHOD-THREAT-REVIEW.md) before making any claims from the output. Both the selection and sources remain publicly identified, so this is not a blind challenge.

**Freeze the existing rules rather than tuning to the nine cases.** When an unsupported change passes unflagged, record the failure mode and use future *separate* development data for a proposed fix. Do not label the source claims incorrect simply because a revision occurred.

No independent human reviewers have rated the source documents.
