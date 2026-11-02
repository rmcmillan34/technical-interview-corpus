# SWE foundation and depth tranche

This tranche adds fifteen draft Software Engineering questions spanning D1 through D5.

## Why add D1 now?

The populated corpus had no D1 questions after the first system-design and coding/behavioural tranches. D1 is intended to assess recall, recognition and explanation of foundational concepts without disguising implementation or production reasoning as foundation-level difficulty.

The five D1 questions cover:
- algorithms and complexity
- HTTP/API semantics and idempotency
- database indexes
- race conditions and mutual exclusion
- logs, metrics and traces

## Depth coverage

The ten deeper questions cover:
- retry-safe mutating APIs
- public API evolution and deprecation
- transactional invariant enforcement under races
- query-plan and indexing diagnosis
- deadlock diagnosis
- at-least-once job processing
- overload containment and backpressure
- distributed observability design
- ambiguous tail-latency incident diagnosis
- strategic shared-database migration across teams

## Difficulty calibration

- D1: recall, recognise and explain foundational concepts.
- D3: production constraints, failure modes, testing, observability and operational trade-offs.
- D4: ambiguity, multi-consumer or multi-service complexity, and defended trade-off decisions.
- D5: long-running cross-system and cross-team migration with strategic sequencing and second-order consequences.

The tranche intentionally contains no D2 question because D2 coverage already exists in the coding tranche. Difficulty is not increased merely because a topic is specialised or obscure.

## Provenance

All questions in this tranche are native corpus questions created with LLM assistance and licensed CC BY 4.0. They remain `draft` with `technical` and `taxonomy` review pending. Merging the PR accepts the records into the repository; it does not promote them to reviewed/canonical status.
