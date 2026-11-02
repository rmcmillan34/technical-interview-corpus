# Technical interview corpus workflow

Before populating SWE questions, read `coverage/swe.yaml`, `coverage/topics/swe.yaml`, the SWE role profile and source-register policies.

## Coverage and stopping

- Question-count minimums are warning thresholds. Preferred counts and difficulty bands are advisory, with no upper caps. Reaching any number does not complete a competency pass.
- Discover relevant source topics before population. Map them to canonical competencies; treat languages, frameworks, specialist tracks and interview formats as appropriate variants rather than inventing a competency for every heading.
- Reconcile every relevant topic in the declared pass scope. Record anchored assessment evidence, an open gap or a justified deferral. A gap/partial topic keeps that scope open.
- Add or extend questions whenever they introduce distinct concepts, implementation tasks, constraints, failure modes, stimuli, technology semantics or credible interview paths. Deduplicate by assessment value, not by matching competency labels.
- Secondary labels and the whole question's difficulty do not by themselves demonstrate separately assessed competence. Link the specific rubric criterion or assessment signal and explain its relation to the topic.
- Consider escalation, recovery and lateral deepening at the end of each topic pass. Reuse suitable descendants; every D1 does not need a separate D1–D5 ladder.

## Checkpoints and evidence

- At each pass close-out, record inspected source revisions, topics assessed, question additions/changes, no-add rationale, path changes, remaining gaps and next work. If the requested scope is unfinished, state that explicitly and leave a resumable checkpoint.
- Do not turn a token/time limit, count floor or green CI result into a claim that all relevant content is complete.
- Research-only sources permit topic discovery under project policy, not redistribution of their questions or linked third-party material. Follow `sources/source-register.yaml` for reuse.
- Keep technical/taxonomy approvals and lifecycle status honest. Structural validation is not content approval.

Run the schema, provenance, coverage/progression and source-topic validators, the test suite, and applicable release-preview checks before proposing corpus changes. Record remaining advisory gaps.
