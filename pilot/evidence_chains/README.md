# Historical evidence-chain candidates (source-checked, **not independently validated**)

Three real, cross-domain **case histories** replace formula-only edits as the next *discovery* unit. Each history separates a source's claim, the evidence available at that time, relevant alternative explanations, and what new evidence subsequently addressed. The reports are original concise paraphrases with links to primary material; no articles, raw datasets or partner IP are copied.

This discovery work is separate from the private Research Claim Governance Study 1. **It cannot measure whether the public engine outperforms generic scientific review.**

## Candidate cases and source structure

### 1. Reinhart–Rogoff debt/growth (2010–2013)

An original debt–growth association, an outside replication identifying an omitted spreadsheet range and methodological disagreements, and an authors' erratum. The corrected spreadsheet does not settle the appropriateness of alternative country weighting, historical samples, or any causal debt threshold.

Primary and directly involved sources:
- Original 2010 paper (Harvard): https://rogoff.scholars.harvard.edu/publications/growth-time-debt
- Herndon–Ash–Pollin critique and replication/data links (UMass): https://peri.umass.edu/publication/does-high-public-debt-consistently-stifle-economic-growth-a-critique-of-reinhart-and-rogoff/
- Reinhart–Rogoff authors' erratum (5 May 2013): https://carmenreinhart.com/wp-content/uploads/2020/02/36_data.pdf

**Important distinction:** The critics' 2.2% postwar mean and the authors' erratum corrections are different analytical treatments; do not splice them into one supposed consensus estimate. The source spreadsheet and analysis were **not rerun**.

### 2. BICEP2/Keck and Planck (2014–2015)

A reported sky-polarization excess was initially attributed to primordial waves; an independent foreground analysis raised a viable dust alternative. The 2015 joint multi-frequency analysis found strong evidence for dust and no statistically significant tensor detection. The original measurement is not the same claim as the primordial-wave attribution.

Primary research sources:
- Original BICEP2 paper: https://pubmed.ncbi.nlm.nih.gov/24996078/
- Independent dust/foreground analysis: https://doi.org/10.1088/1475-7516/2014/08/039
- BICEP2/Keck–Planck joint analysis: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.114.101301
- Original university announcement with a correction note: https://www.cfa.harvard.edu/news/first-direct-evidence-cosmic-inflation

**Important distinction:** No significant tensor detection is **not** proof that the primordial tensor contribution equals zero. No independent sky-map/likelihood fitting was performed.

### 3. OPERA neutrino timing (2011–2012)

An anomalous time-of-flight measurement was followed by discovery of *two potential timing-chain faults that shifted the estimate in opposite directions*, cross-experiment checks, and a dedicated recalibrated measurement. The evidence is more granular than simply "bad cable corrected."

Primary sources:
- Dated CERN release and updates (September 2011, February and June 2012): https://home.cern/opera-experiment-reports-anomaly-in-flight-time-of-neutrinos-from-cern-to-gran-sasso/
- OPERA's dedicated 2012 measurements: https://arxiv.org/abs/1212.1276

**Important distinction:** Compatibility with light-speed within experimental uncertainty is not a proof of exact identity. The CERN web page is retrospectively updated; its historical sections are dated, but the whole page is *not* an immutable 2011 snapshot.

## Files and technical gate

`HISTORICAL-DOSSIERS.json` stores evidence IDs, dated stage-by-stage claims, temporal source dependencies, assumption questions and residual interpretive limits.

```bash
python -m auditlab.evidence_chains
python -m auditlab.evidence_chains --json
python -m unittest discover -s tests -v
```

This checks only referential integrity, chronology, URLs and explicit uncertainty; it **cannot** verify the truth of the sources' substantive conclusions.

## Why this is closer to the actual research question

Unlike a trivial formula patch, all three cases show different ways that **new evidence changes what claims an investigator can justify**. Yet these are highly familiar historical examples selected **with hindsight**. They do not isolate a same-terminal-state, different-provenance treatment, a controlled invariance condition, or a blinded empirical outcome.

**Current state:** 3 research candidates, 10 narrated stages, 10 source records and 11 assumption questions; zero independently adjudicated claim histories, zero quantitative performance results.

**Next discriminating gate:** Independently audit the source-to-claim links and alternative explanations, then construct a separately sampled claim-provenance cohort. Do not relabel this retrospective sample as an independent or novel research finding.
