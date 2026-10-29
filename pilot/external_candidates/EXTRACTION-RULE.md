# Source-anchored claim extraction rule — feasibility phase 0.1

**Prepared 29 October 2026 by AI-assisted project development under Linda Thorstensen's direction. NOT pre-registered, independently adjudicated, or blinded.** All upstream pull-request diffs were inspected before this rule was written. The source pool is a deliberately correction-enriched convenience sample. Do not claim a prospective untouched holdout.

## Frozen candidate universe

Exactly the ten entries in `pilot/external_candidates/CANDIDATES.json` at commit `cb5dcf25a8eb3147744708d9f4a8a2568f389beb`. Preserve order and IDs; record inclusion and exclusion without dropping rows. No substitution after seeing results.

## Extraction target

Select **one atomic technical assertion from the selected changed path** per upstream revision. Prioritize the first locally complete equation, parameter-bound or declared function behavior directly affected by the patch; for multi-hunk changes, document any reason to choose another. Do not use the PR's assertion of correctness as ground truth.

Treat a newly introduced assertion as a new claim with its own ID in AFTER and no corresponding invented BEFORE assertion. If the change is formatting-only, preserve the same claim paraphrase and record that the surface representation changed without claiming verified equivalence. If the selected path contains only an implementation change and **no extractable proposition addressed to readers**, exclude from the textual-claim pilot and retain it in the selection ledger as an eligible candidate for a later implementation study.

Use plain-language **original paraphrases** or minimal mathematical expressions to avoid copying upstream code or documentation. The two claim texts should be comparably scoped, even if mathematically inconsistent; never silently correct the source. The public source links point to immutable commit SHAs. Track the selected hunk or symbol and why it is the appropriate extraction.

## Evidence and assumptions

- Populate `evidence: []` and `assumptions: []` unless the **selected source hunk explicitly names** a supporting source or assumption that can be faithfully represented. Empty means **not extracted / unknown**, NOT evidence of no underlying support or absence of assumptions.
- Use `asserted_status: hypothesis` as a **neutral schema placeholder** only. It is NOT a report that upstream authors called the material a hypothesis. Do not use this field for downstream claim-strength conclusions.
- Record public `source_ref` and `origin` outside the evidence list. A merged PR is version provenance, not scientific verification.
- Do not invent reviewer decisions, generic-critic outputs, closure labels, reference work, citations, empirical validation, or quantitative success rates.
- Preserve all uncertainties explicitly in a separate selection ledger, not hidden inside self-certified evidence metadata.

## Inclusion and exclusions (declared before writing claim pairs)

| Case | Treatment | Selected unit |
|---|---|---|
| SCIPY-17922 | Include | First bilinear docstring substitution formula, not duplicated `bilinear_zpk` hunk |
| SCIPY-24110 | Include | First modified Airy-Ai / modified-Bessel prefactor identity |
| SCIPY-24480 | Include | Negative hypergeometric tutorial support upper bound |
| SCIPY-22579 | Include | One-dimensional signal-correlation expression and output indexing |
| SCIPY-24518 | Include | Newly stated single-rotation row-vector equivalence; retain preceding statement as existing context |
| PYTORCH-7383 | Include | MultiMarginLoss documentation sign of competitor term |
| PYTORCH-5679 | Include | Hardshrink piecewise function; rendered delimiter is a formatting control |
| PYTORCH-1921 | Include | GRU reset gate hidden-state weight subscript (select one hunk from multi-hunk PR) |
| PYTORCH-134704 | Include | Nuttall-window parameter definition; MathML/rendering edit is a formatting control |
| PYTORCH-66397 | **Exclude from textual-claim scoring** | Changes returned shape in C++ implementation, not a paired textual assertion; track as an implementation-study candidate |

Inclusion does not imply that any change is scientifically significant or warrants review. Formatting controls are included intentionally. The extracted claims do not reconstruct real experiments, numerical tests or the true mechanisms behind the patches.

## Critical limitations

- The source selection and extraction were done with knowledge of correction-focused PR titles and content, so neither the extraction nor the cohort is blinded or statistically representative.
- A source code/docstring change is **not** automatically a change of scientific evidential warrant.
- An AI-authored paraphrase is not independently verified source transcription. All extracted claims require independent source-checking before being scored.
- For a confirmatory comparison, use fresh cases chosen independently by a frozen sampling rule and sealed human source adjudication. This public feasibility packet must stay exploratory and must not be pooled with private Research Claim Governance Study 1.
