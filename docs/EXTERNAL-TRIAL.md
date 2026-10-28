# Optional external trial: privately run on your own material

This is an **invitation to test the public tool's limits**, not a claim that it can verify any proprietary architecture.

1. Clone or inspect this repository, then run `python -m unittest discover -s tests -v`.
2. Create two local JSON snapshots of a *small* authorized set of claims: before and after a revision. Keep exact original documents off this public repository.
3. Assign stable IDs to claims, cited evidence and assumptions. Use `after=open`, `claimed_closed` or `withdrawn` precisely; do not infer closure from a replacement citation.
4. Run `python -m auditlab --compare before.json after.json --json`. Inspect changes by claim, and note which ones would need actual independent confirmation.
5. For public DOIs only, optionally add bibliographic fields and `--check-dois`. This transmits DOI identifiers to Crossref, **not** proprietary claim texts.
6. Independently verify a tiny stratified subset by consulting original primary sources, running proof/checks, or obtaining specialist feedback. Only this external process can substantiate a scientific result.
7. If you share a result, remove proprietary text, identifiers and sensitive metadata first. Do not push private before/after documents, evidence dumps or detailed secret implementation parameters.

The software is not certified for high-assurance engineering use. A result labeled `bibliographic_metadata_match_only` or `CLOSURE_REQUIRES_INDEPENDENT_CONFIRMATION` is explicitly **not** a scientific verification result.

The private foundational research and protocols underlying Linda Thorstensen's research are not disclosed or licensed through this trial.
