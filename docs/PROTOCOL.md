# External Test Protocol — v0.2 (exploratory, not a study result)

## Scope

The objective is to detect **claim-laundering risks** in revisions, not to produce a certificate. The public tool is separate from private Research Claim Governance instruments. The independent scientific evidence evaluation required to establish truth is *not automated* here.

### Required distinctions

- **Bibliographic existence:** the DOI resolves to a deposited metadata record (Crossref coverage is not universal).
- **Metadata agreement:** reported bibliographic fields agree with Crossref deposit metadata. This does not assess the paper's content.
- **Mechanism support:** a published method actually establishes the stated mechanism under relevant boundary conditions.
- **Transfer validity:** the method remains valid for the actual target regime, representation and hardware.
- **Formal proof / hardware result:** the exact design satisfies the property; a plausible equation or RTL description is not enough.
- **Assay closure:** an empirical assumption can be considered resolved only after independently reviewed applicable evidence and explicit failure criteria.

### Revisions

Use stable IDs to map the same claim, source and assumption across snapshots. The `--compare` command reports:

- newly asserted claim-strength upgrades;
- changed evidence locators with reused IDs;
- claimed changes from unknown/mismatched to matched applicability;
- assumptions newly claimed closed (not evidence of closure);
- assumptions removed or newly introduced;
- deleted claims, withdrawn assumptions, and changed assumption meanings.

Count source withdrawals and deletions as **scope changes, never verified resolutions**. A change report is not an assay-contraction scorecard. Do not claim 10x or 90% reduction based on these counters.

### External bibliographic checks

The optional Crossref lookup uses the publicly documented `/works/{doi}` metadata endpoint. Only DOI identifiers are sent; run only with authorization to use the listed identifiers. DOI, title, year and optional bibliographic fields are checked independently of the document's own declarations. A matching record means **metadata match only**; it does not imply peer review, non-retraction, correct equations, domain applicability, valid engineering design or safe operation.

Invalid DOI, Crossref-not-found, lookup errors and incomplete metadata all have different statuses. Absence from Crossref does **not** imply that a publication is fabricated; other registries and offline historical works exist.

### Independent evaluation (future work)

1. Obtain authorized, fixed versions of the original and revised artifacts.
2. Pre-register precise factual assertions to test and explicit pass/fail thresholds.
3. Include known-valid, known-invalid and ambiguous cases; record domain and boundary conditions.
4. Use external specialist reviewers (blind where feasible), independently reproduce derivations, and verify source content directly.
5. Compare paired audits against generic checklist controls under matched evidence and time budgets.
6. Track both false approvals and unjustified denials. Preserve all disagreement and null outcomes.

Do not present software-unit-test success as evidence of improved scientific validity or independent reviewer agreement.
