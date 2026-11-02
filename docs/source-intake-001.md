# Source Intake 001 — SWE / System Design

Observed: 2026-11-02

This tranche tests the v0.1 source-governance process against real public interview-preparation repositories before any bulk ingestion.

## Approved core sources

### System Design Primer

- Repository: `donnemartin/system-design-primer`
- Licence: CC BY 4.0
- Decision: `core`
- Permitted in this corpus: influence, adapted, verbatim with attribution and modification notices
- Initial use: five adapted system-design questions (`tic-q-000006`–`tic-q-000010`)

The repository licence explicitly states that its code and resources are provided under CC BY 4.0.

### Tech Interview Handbook

- Repository: `yangshun/tech-interview-handbook`
- Licence: MIT
- Decision: `core`
- Permitted in this corpus: influence, adapted, verbatim with required MIT attribution
- Caveat: linked third-party practice questions and external resources are not assumed to inherit the repository licence.

## Research-only sources

### Coding Interview University

- Licence: CC BY-SA 4.0
- Decision: `research-only`
- Reason: ShareAlike obligations are intentionally excluded from the core mixed-license distribution until a segregated compatible export is designed.

### The Loop / interview-rounds

- Repository-level licence: CC BY-NC 4.0
- Decision: `research-only`
- Reason: noncommercial restriction conflicts with the corpus goal of unrestricted downstream commercial reuse.
- Note: repository documentation identifies some sub-banks as separately MIT-licensed; those require their own source records before use.

### Awesome Interview Questions

- Decision: `research-only`
- Reason: the archived repository exposes no repository licence file. Public visibility alone is not treated as permission to redistribute.

### The Coding Interview

- Licence file: MIT
- Decision: `research-only`
- Reason: the licence names a copyright holder that does not clearly match the repository authorship. Reuse is deferred pending provenance clarification.

## Initial ingestion rules exercised

The first five external questions are deliberately marked `draft` and `external-adapted`. They retain the System Design Primer licence, carry explicit attribution and modification statements, and must pass both the corpus validator and provenance validator before merge.

No research-only source content is copied into the corpus.
