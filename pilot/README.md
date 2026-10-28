# External pilot package

**Current status: prepared pilot procedure; real-data pilot not started.**

Included: [protocol](TRIAL-PROTOCOL.md), [generic critic candidate](GENERIC-CRITIC.md), [independent reviewer instructions](REVIEWER-INSTRUCTIONS.md), a Python scorer and invented demonstration files.

The targeted engine and generic critic answer **the same question**: whether the *change* needs independent re-examination. The generic critic must receive both versions and equivalent reference material.

Run the entirely synthetic software demonstration (no network, no real reviewer ratings):

```bash
python -m auditlab.pilot --cases pilot/demo/cases.json --reviewer-a pilot/demo/ratings_a.json --reviewer-b pilot/demo/ratings_b.json --generic pilot/demo/generic_predictions.json --json
python -m unittest discover -s tests -v
```

Only externally sourced, permission-cleared cases with independently collected blinded human labels can produce an external pilot result. Do not upload proprietary third-party material into a public repository or an unapproved cloud service.
