# Claim-Warrant Validation Lab

**Public, independent, experimental sandbox for structural claim, evidence and correction audits.**

**Research direction and project ownership:** Linda Thorstensen. AI assistance is limited to implementation, testing, drafting and verification support under her direction.

This repository is a deliberately narrow public demonstrator. It is **not** the implementation of any private research framework and does **not** disclose ArcTopia or Research Claim Governance architectures, protocols, datasets or restricted keys.

## Question

When a technical document replaces a weak citation or revises a calculation, has it actually closed the assumption it relied on—or merely moved that assumption into a new explanation?

This baseline tool checks *declared metadata*, not scientific truth. It can identify missing or mismatched support, overly strong claim labels, and unsupported closure declarations. It does **not** independently verify publications, reproduce equations, simulate hardware, validate physical behavior, or establish epistemic entitlement.

## Quick start (Python 3.10+, standard library only)

```bash
python -m auditlab examples/synthetic_claims.json
python -m auditlab examples/synthetic_claims.json --json
python -m unittest discover -s tests -v
```

The provided data are entirely fictional. No source material from Genesis Genome or any other external project is included.

## Input contract

A JSON object with `claims` list. Each claim has an `id`, `statement`, and optional `asserted_status` (`hypothesis`, `supported`, `verified`, `proven`), plus `evidence` and `assumptions` arrays.

Evidence fields: `id`, `kind` (`publication`, `standard`, `derivation`, `hardware_report`, `experiment`), `locator`, `reviewed` (boolean **supplied by the record author**), and `applicability` (`matched`, `mismatch`, `unknown`).

Assumption fields: `id`, `description`, `after` (`open`, `claimed_closed`, `withdrawn`), optional `closure_evidence_id`, and `withdrawal_reason` when withdrawn.

A structurally eligible closure requires referenced evidence marked reviewed and matched. **That is only a candidate for independent examination**. The tool never marks a scientific claim verified and never credits a withdrawn assumption as proof. Any test-surface reduction remains undefined until independently adjudicated.

## Safety and use boundaries

- Do not upload private research, unpublished partner documents or restricted code without permission.
- Do not claim that a verified bibliographic reference establishes target-domain applicability.
- Do not optimize the audit to achieve a pre-selected reduction percentage.
- Keep raw evidence, independent reviewer decisions and change history outside self-scored summaries.
- No personal, partner or third-party project is endorsed or evaluated by this sample.

See [protocol](docs/PROTOCOL.md), [contributing](CONTRIBUTING.md), and [security](SECURITY.md).

## Project status

**v0.1 structural pilot, synthetic-only. No empirical validation or original-method superiority claimed.**

## Rights

Copyright © 2026 Linda Thorstensen. No software license has been granted by this repository. Public visibility alone does not grant rights to reproduce, redistribute or reuse the code. Licensing can be decided separately.
