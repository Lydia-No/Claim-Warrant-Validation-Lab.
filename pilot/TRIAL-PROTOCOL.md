# External Pilot Protocol — Draft v0.1

**Status: design and synthetic software checks only. No external evidence was evaluated.**
This public pilot is separate from any private research protocol.

## Question

For the same versioned technical claim, can a targeted revision checker correctly identify material changes that warrant independent evidential re-examination, compared with a generic critic given both versions and equal supporting materials?

## Before testing

Select 8–12 accessible claim revisions under a fixed inclusion rule. Log every included or excluded candidate. Obtain permission for any nonpublic work; keep nonpublic data outside this repository.

Prepare two structured snapshots per claim with the same stable claim, evidence and assumption IDs. Preserve original document versions, source references and hashes in a private manifest. Both systems must receive equivalent evidence and revision context.

Freeze the case selection, scoring rules, model and prompt settings, versioned software and source manifest before reviewing predictions. Do not claim this protocol has been pre-registered merely because it is public.

## Independent reference labels

Two qualified reviewers examine the same authorized supporting documents independently, without seeing system predictions or each other's answers.

They answer: **Does the revision warrant independent re-examination of evidential support?**

Each provides one of `yes`, `no`, `uncertain`, together with evidence inspected and reasoning. Uncertain does not mean no. Do not substitute consensus for the original individual ratings.

## Comparator conditions

1. Targeted engine: deterministic revision-event review in this repository.
2. Generic critic: assess both complete structured snapshots and the same evidence with a fixed prompt. Record model version, settings and actual source access.

A snapshot-only checker can be reported as a diagnostic baseline but **not** as a fair, equally informed generic critic.

## Outcomes and limits

Report TP, FP, FN, TN, precision, recall, specificity and abstention coverage for each method against exact, determinate reviewer agreement. Exclude and disclose reviewer disagreements and unresolved labels. Keep all cases and errors.

Small sample outcomes are **descriptive only**, without significance, novelty, scientific certification or assay-reduction claims. If sources or independent reviewers are unavailable, report feasibility constraints instead of fabricated results.

Only synthetic fixtures and general software may be committed publicly. External source data and reviewer details remain private unless authorized.
