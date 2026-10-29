# Source-bound local pilot — experimental

The public lab's next capability is an **offline, source-bound warrant trail**. It checks exact local source bytes and quoted passages before asking reviewers for claim-specific judgments. It does **not** evaluate semantic entailment automatically.

## What the tool can establish

- A local UTF-8 text/Markdown/RST file's SHA-256 bytes match a supplied pin.
- A quotation actually occurs within the stated line range of those bytes.
- An optional `claim_origins` entry identifies where an author wrote a claim, **not** where it was independently supported.
- An explicitly provided claim/evidence/scope/anchor link references a real claim and declared evidence scope.
- Two or more *declared* reviewers agree, disagree, or remain uncertain on a source-anchored claim.
- Before/after revision differences reveal reused anchors, altered source digests, removed/added bindings, and broadened support scope attached to unchanged anchors.

A matching hash **is not an independently authenticated provenance chain**. An exact source quotation **is not scientific support**. Two matching reviewer ratings **do not establish reviewer independence, expertise, truth or external validity**.

The user alone controls any non-public input and its output. Do not upload or commit private documents, their extracted claims, hash inventories, output, or derived case identifiers to public branches, pull requests, CI artifacts, or issues.

## Local inputs

- `claims.json`: the existing auditlab record format. Optional evidence `declared_support_scopes` in `principle`, `method`, `implementation`, `performance`.
- `bundle.json`: optional `claim_origins` with `claim_id,anchor_id` (author-text provenance only); `sources` with `source_id,path,sha256`; `anchors` with `anchor_id,source_id,line_start,line_end,quote`; `bindings` with `claim_id,evidence_id,anchor_id,scope`.
- `ratings.json` (optional): `ratings`, each with the binding's four IDs, `reviewer_id`, `verdict` (`supports`, `does_not_support`, `uncertain`), and nonempty `rationale`.

Only plain-text sources are supported. External PDFs must first be lawfully converted into authorized local source text, with transformation provenance documented separately. Reference passage exact matching operates on local text only.

## Public synthetic demonstration

```bash
python -m auditlab.extensions --source-check \
  examples/source_pilot/claims.json \
  examples/source_pilot/bundle.json examples/source_pilot \
  --ratings examples/source_pilot/ratings.json

python -m auditlab.extensions --source-compare \
  examples/source_pilot/claims.json examples/source_pilot/bundle.json \
  examples/source_pilot/claims.json examples/source_pilot/bundle.json \
  examples/source_pilot
```

The second command should report zero source-binding revision events, and both record snapshots remain scientifically unverified.

## Real-world research methodology

1. Fix a local source snapshot and claim IDs before assessment; record where the source bytes came from.
2. Create evidence-specific quotes for **each required evidentiary scope**. Missing passages are recorded as unresolved.
3. Get two independently solicited specialist assessments. The script cannot establish reviewers' independence.
4. Give a generic critic the **same source passages, metadata and time budget**; retain disagreement and abstention.
5. Use prospective matched revision pairs, locked inclusion decisions and independent adjudication before calculating any comparative metrics.

This repository **has not executed** that independent study. These scripts are test infrastructure, not empirical effectiveness evidence.

## Threats that remain

Self-selected quotes, omission, selective excerpt boundaries, misleading metadata, strong declarations unsupported by the full paper, domain-transfer gaps, incorrect semantic conclusions, invented reviewer identities, unblinded retrospective case curation, and incomplete source custody.

**Fail-closed rule:** Missing/unreadable/changed source bytes block source-anchored opinions from being presented as checked source links. No path or report can cause `automatically_verified=true`.
