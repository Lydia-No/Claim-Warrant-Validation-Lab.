# Generic full-context critic — candidate fixed prompt

**Draft for a future external pilot. Not executed on real source material.**

> You are assessing one technical claim as revised from BEFORE to AFTER. Both snapshots and permitted supporting references are provided. Determine whether changes to the claim, evidence, applicability, assumptions or strength of assertion warrant **independent re-examination of evidential support**.
>
> You have access to both versions and the same authorized source materials as the targeted comparison tool. Consider source relevance and limitations as well as material changes to claim meaning. Do not mistake bibliographic existence for proof, or a removed assumption for a verified one. Distinguish cosmetic edits and conservative claim narrowing from material changes.
>
> Return JSON: `{"decision":"yes","rationale":"..."}`.
> The decision must be `yes`, `no`, or `abstain`. If the available records cannot support a determination, abstain rather than silently answer no.

Freeze the exact prompt, model identity, token/effort settings and source availability before testing. Do not expose reviewer labels or targeted-tool answers to the generic critic. Convert its recorded responses into a local `{"predictions":[{"case_id":"EXT-001","decision":"yes"}]}` file for scoring.

A difference caused by unequal input access is **not** evidence of a method advantage.
