# Independent reviewer instructions

For a real pilot, use **two distinct human reviewers** competent to inspect the authorized underlying documents. Reviewers must not see tool predictions or each other's ratings until their answers are sealed.

Examine the original and revised technical claim, the actual references and the stated application constraints. Decide whether the *revision* warrants independent checking of its evidential support, rather than deciding whether the whole technological design is true.

Rate each case `yes`, `no`, or `uncertain`. Record document versions actually inspected and a concise rationale in privately retained records. Do not treat uncertainties as negative cases.

Minimal scoring file, stored locally:

```json
{"ratings":[{"case_id":"EXT-001","label":"uncertain"}]}
```

The files under `pilot/demo` contain **invented reviewer labels** for software testing only.
