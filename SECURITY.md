# Security, privacy and external input

Public repository and CI logs are public. Never commit private research materials, unpublished third-party blueprints, secrets, restricted research keys, authentication tokens or raw proprietary corpora.

Offline audit and comparison commands read local JSON and do not make network requests.

**Explicit network option:** `--check-dois` queries the public Crossref REST API over HTTPS. Only the DOI identifier is included in the request URL. Crossref may log the requested DOI and client network metadata. Claim text and assumption descriptions are not transmitted by this implementation. Do not run this option on private identifiers unless permitted to do so.

DOI lookups are capped; timeouts, missing registry records and schema errors fail closed as unknown/unconfirmed. JSON handling is basic data processing, not a security sandbox. Do not run this program with elevated privileges on untrusted machines.

Report suspected disclosures privately to the repository owner before opening a public issue, without repeating sensitive content.
