# Method-threat review — external pilot development

**Assessment date: 29 October 2026. Status: negative/limited feasibility observations, not independent research results.**

## Central problem

The nine extracted SciPy and PyTorch claim pairs are genuine upstream revisions, but **their source records contain no extracted evidence-provenance trails, alternative explanations, or assumptions that can be evaluated**. Empty `evidence` and `assumptions` fields mean "not extracted / not independently assessed", not "the original claim had no evidence."

The existing engine was designed for structured evidence/assumption metadata. This public upstream corpus currently evaluates mostly **whether formulas, numeric literals, and new claim IDs change**. It cannot yet test the distinguishing scientific question: whether apparently successful revisions preserve or introduce *unjustified evidential warrant*.

Do not interpret these nine records as a test of the private Research Claim Governance hypotheses or as a validation of epistemic sovereignty, MHC or ArcTopia.

## Known methodological threats

1. **Enrichment / hindsight.** The set was found through public merged PRs describing known corrections. No untreated prospective sample, unknown truth, or independent selection.
2. **Unblinded curation.** The same AI-assisted process saw PR titles and patches and constructed the paraphrases. Even though an extraction rule was committed first, it is retrospective and cannot become a blinded pre-registration.
3. **Missing underlying evidence.** Neither attached mathematical proofs nor primary experimental sources nor independent feasibility tests are included in the structured records. The corpus cannot evaluate real assumption closure.
4. **Control dependence.** The two formatting controls are useful smoke checks but their meanings were preserved by paraphrasing; they do not test whether an algorithm can distinguish substantive changes from raw markup differences.
5. **Conflated questions.** "Does the edit warrant review?" is not "Is this claim wrong?" and not "Does source provenance change the highest warranted claim level?" Treat them as separate research questions.
6. **Information inequality.** A snapshot-only critic sees less history than a revision-aware tool. Any evaluation of added value requires an equally informed generic critic and human reviewers with actual sources.
7. **Identity leakage.** Commit URLs and PR titles expose known correction outcomes to reviewers. Use sealed reference mapping and permitted source extracts; if source tracing prevents blindness, explicitly report the limit.
8. **Authorship / IP.** Public upstream links are not permission to republish complete code/docstrings. No other user's private research is included here.
9. **No independent adjudication.** Human specialist reviewers have not inspected or rated these cases. Coordinator paraphrases have not been externally validated.

## Actionable discriminating test

Find a separate prospectively selected cohort of *versioned scientific/technical assertions with explicit evidence citations or test artifacts*, not only mathematical formula repairs. Before any system sees outcomes, record a reproducible candidate-sampling rule, capture claim-relevant source artifacts under proper permission and construct matched cases with evidence IDs and alternative explanations.

For the actual methodological question, require at least one pair in which **the visible terminal claim and evidence summary are equivalent**, while evidence provenance or revision history genuinely differs (with independent documented support). Include invariance controls in which provenance does **not** matter. Such pairs are currently **absent** from this public external cohort; do not fabricate them from the existing sources.

Use independent human experts to decide what external source material supports, then compare:
- a generic critic given the same full provenance and accessible evidence;
- the fixed targeted auditor;
- a trivial full-diff baseline as a debugging control only.

Record over-flagging and under-flagging. Do not retune rules on the external evaluation set. If there is no interpretable evidential history or ratings, the result must be an honest feasibility failure, not a positive study.

## What is permitted to claim now

- A runnable public structural claim-metadata checker exists.
- Source-pinned paraphrases of nine real code/documentation revisions have been prepared.
- It can report whether existing static rules flag those records.
- It cannot independently verify those source claims, justify a 90% reduction, or demonstrate superiority over generic full-context review.
