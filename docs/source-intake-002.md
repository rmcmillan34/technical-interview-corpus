# Source intake 002: SWE coding and behavioural tranche

Observed: 2026-11-02

## Source

This tranche uses the already-approved `src-tech-interview-handbook` source record for material contained in the Tech Interview Handbook repository under its MIT licence.

Relevant repository material reviewed for this tranche:

- `apps/website/contents/coding-interview-rubrics.md`
- `apps/website/contents/coding-interview-cheatsheet.md`
- `apps/website/contents/behavioral-interview.md`
- `apps/website/contents/behavioral-interview-questions.md`

## Coding intake decision

The handbook's own coding guidance describes assessment across communication, problem solving, technical implementation and testing, including clarification, complexity reasoning, trade-offs, clean code, edge cases and self-correction.

The corpus does not copy third-party coding problem statements linked from the handbook. Instead, this tranche authors new scenarios and adapts the assessment methodology into corpus rubrics.

Added draft questions:

- `tic-q-000011`: merge maintenance windows
- `tic-q-000012`: dependency build order and cycle diagnostics
- `tic-q-000013`: bounded LRU cache with TTL
- `tic-q-000014`: streaming top-k values
- `tic-q-000015`: binary-search debugging stimulus

The set intentionally covers multiple problem shapes and includes one debugging task so that the coding tranche does not collapse into algorithm-puzzle repetition.

## Behavioural intake decision

The handbook's own behavioural preparation material describes STAR/STAR(R)-style evidence, selecting high-impact/high-complexity stories, conflict, ambiguity, leadership moments, learning experiences and reflection.

The handbook's company-specific question sections cite external sources such as Glassdoor. Those lists are not treated as MIT-licensed source material for this corpus and are not copied here.

Added draft questions:

- `tic-q-000016`: technical disagreement and constructive influence
- `tic-q-000017`: ambiguity and changing requirements
- `tic-q-000018`: delivery risk or missed target
- `tic-q-000019`: constructive feedback and changed behaviour
- `tic-q-000020`: cross-team influence without authority

Behavioural rubrics assess the quality of evidence, the candidate's own actions, judgement, outcomes and reflection. STAR structure is useful organisation, not itself a sufficient positive signal.

## Difficulty calibration

- D2 questions remain bounded and primarily test application plus explanation.
- D3 coding questions add robustness, diagnostics, time-dependent behaviour or production-oriented edge cases.
- D3 behavioural questions require meaningful uncertainty, ownership or trade-off reasoning.
- D4 is reserved here for cross-team influence across competing objectives and organisational boundaries.

All ten records remain `draft` pending technical and taxonomy review. Provenance is approved because the source is already registered as an approved core MIT source and every record contains attribution and a modification statement.
