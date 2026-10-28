# External Test Protocol (exploratory; not a study result)

## Purpose

Stress-test the difference between correcting a document and establishing that its claims have independently warranted support. This public sandbox is **not** the private Research Claim Governance Study 1 instrument; its results must not be attributed to or pooled with that study.

## Unit of audit

One concrete claim, its evidence items, target regime, and an explicit list of assumptions asserted to have been closed or removed. Distinguish a source's existence, source content, transfer validity, implementation and target performance.

## Separation of tasks

1. **Extract** each concrete assertion and its actual referenced evidence. Preserve exact quotations with identifiers, but only where permitted.
2. **Check existence and source accuracy** independently. Record a bibliographic confirmation separately from target applicability.
3. **Assess scope**: does the evidence address the exact representation, operating regime, materials, version, hardware and bounds asserted?
4. **Reproduce** derivations and implementation tests independently when practicable. Record reproducible artifacts and environments.
5. **Review revisions**: every patched claim and citation can introduce another assumption; capture it instead of automatically upgrading its status.
6. **Adjudicate** unresolved assumptions through an external independent review. Do not treat the tool's structurally eligible closures as validated ones.

## Controls and non-goals

- Compare a document before and after revision, preserving source hashes.
- Include known-valid and known-invalid synthetic cases as controls.
- Keep withdrawal/scope reduction distinct from assumption validation.
- No fixed 90% or 10x success target is imposed.
- Do not infer compliance with DO-254, DO-178C, or any physical, cryptographic, safety or regulatory standard from metadata checks.

## Output interpretation

`structurally_eligible_closures_not_verified` means that user-supplied metadata connects an assumption to a reviewed and reportedly applicable artifact. It does not establish the artifact is correct or truly independent.

`remaining_not_structurally_closed` excludes withdrawals from the active scope but does not certify anything. The `verified_empirical_reduction` field is always `null` in this version.

## Next falsifiable extension

Use a genuinely external dataset and independent subject-matter adjudicators. Evaluate precision/recall of the findings and compare the tool against a basic checklist under equal time/evidence access. Pre-register decision thresholds; report error and false-positive rates. No claims of added research value before that evaluation.
