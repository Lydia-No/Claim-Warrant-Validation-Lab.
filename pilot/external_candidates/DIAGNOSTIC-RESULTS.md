# Real upstream-source paraphrase diagnostic: first execution

**Recorded:** 29 October 2026, [GitHub Actions run 40800147389](https://github.com/Lydia-No/Claim-Warrant-Validation-Lab./actions/runs/40800147389), commit `d091a3aebff3de1fde624a83afcdb6e5b20981db`.

**This is NOT an independently labeled evaluation, proof of correctness, or benchmark result.** Nine source-pinned records were retrospectively selected from known merged SciPy / PyTorch fixes. Their statements are AI-assisted paraphrases with empty, unassessed evidence and assumption inventories. The tool's deterministic rules were left unchanged.

## Executed diagnostic

| Case | Coordinator-selected change | Rule output | Status |
|---|---|---|---|
| SCIPY-17922 | Bilinear substitution factor | Numeric literal changed → recheck | **Not rated** |
| SCIPY-24110 | Airy identity prefactor | Numeric literal changed → recheck | **Not rated** |
| SCIPY-24480 | Negative-hypergeometric index upper bound | No structural risk flag | **Not rated** |
| SCIPY-22579 | Correlation index conventions | Numeric literal changed → recheck | **Not rated** |
| SCIPY-24518 | New single-rotation equivalence | New claim ID → recheck | **Not rated** |
| PYTORCH-7383 | MultiMarginLoss sign change | No structural risk flag | **Not rated** |
| PYTORCH-5679 | Hardshrink equation delimiter formatting | No structural risk flag | **Not rated** |
| PYTORCH-1921 | GRU weight-subscript change | No structural risk flag | **Not rated** |
| PYTORCH-134704 | Nuttall window equation rendering | No structural risk flag | **Not rated** |

**Counts:** 9 source-pinned paraphrase pairs; 4 structural review flags; 3 changed paraphrases without a structural risk flag; 2 unchanged-meaning formatting controls without flags.

**These are neither TP/FP/FN/TN nor performance scores.** No independent reviewer has classified whether each revision materially changes evidential warrant. The absence of a flag for a changed sign, symbol or bound does not prove a false negative *against an external scientific rating*, though it exposes a clear operational blind spot: the current rule set has no general domain semantics.

## Negative methodological finding

The public source-derived records contain `evidence: []` and `assumptions: []` by design because those attributes were not independently extracted. Thus, on this corpus the engine **does not use evidence provenance**, cannot detect second-order assumption closure and is mostly performing structural edit triage. The nine cases cannot answer whether provenance-aware research-claim auditing provides added value over a generic critic that sees both versions.

In particular, a formula correction does not imply that the repaired claim is experimentally or mathematically verified. A stable equation expression does not imply that no scientific condition changed. The current numerical-literal trigger is a heuristic and must not be upgraded into a proof engine.

## Decision

**Do not tune the fixed evaluator to these nine publicly identified corrections and then claim this corpus as independent validation.** Keep it as exploratory diagnostic data and documented failure analysis.

The next discriminating external test needs (a) genuine source-linked evidential histories and nontrivial assumption alternatives, (b) independent domain review of permitted primary sources, and (c) an equally informed generic critic under frozen inputs. If those materials are absent, report a feasibility limitation, not a superiority claim.

**Software validation:** 73 unit tests passed in the referenced CI run. These are implementation checks, not independent research results.
