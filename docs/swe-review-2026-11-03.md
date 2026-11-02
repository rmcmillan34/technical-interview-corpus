# SWE review of the 2–3 November 2026 PR session

## Verdict

The session built a useful D1-heavy backend/infrastructure SWE corpus, but the original stack did not complete its own important-tier coverage plan. All 13 core competencies cleared tagged planning minimums; 18 of 24 important competencies did. Counts alone do not establish comprehensive assessment coverage.

This review covers PRs #1–35, their branch changes and supporting schemas, role profile, assessments, coverage validator, progression graph and release tooling. The session ran from 22:02 on 2 November to 01:21 on 3 November 2026 (Australia/Sydney). PRs #1–4 were merged; #5–35 were open drafts in one dependent stack. Review baseline: `356082cda81e3d12b81d95d0de5f80a0dc0a6c5f` (#35).

All 35 PR head commits had a successful validation workflow in the observed GitHub run inventory. Local validation of the combined original stack also passed schema, provenance and progression checks. These checks do not constitute technical content approval.

## Findings

1. **P1 — secondary labels can overstate assessment coverage.** `tools/validate_coverage.py` gives primary and secondary competency labels equal count credit at the whole question difficulty. For example, `tic-q-000039` has communication as a secondary competency, but its explicit criterion checks graph-traversal concepts. `tic-q-000080` counts as D2 programming although it requests test design rather than executable implementation. Shared assessment is legitimate when observable evidence supports it; a label is not that evidence. The original communication no-add decision (#14) should be treated as provisional. Communication, service operations, security architecture and application security had no primary questions. That is a review signal, not proof of absent coverage. Add explicit criterion-to-competency mappings before using these counts as scored competence.

2. **P1 — six important competencies were below their own planning minimums.** The stack stopped after application security. Secrets management, leadership/influence, stakeholder management, ambiguity/adaptability, prioritisation and learning/reflection account for ten per-difficulty shortfalls. The corrective tranche below closes those tagged-count shortfalls with distinct prompts, observable rubric criteria and explicit draft status.

3. **P2 — progression construction stopped after API design.** `paths/swe.yaml` had 61 edges and 87 of 110 D1 questions had no incident edge. PRs #9–35 added questions/audits without extending the graph. The follow-up adds representative escalation/recovery routes across all 37 competencies, with existing questions reused as descendants. This is not a requirement for every D1 question to have a complete D1–D5 ladder.

4. **P2 — competency totals hide distinct topic gaps.** Review against `taxonomy/competencies.yaml` identified the targeted follow-up topics below. The role profile explicitly favours backend/infrastructure and performance. It should not be described as universal SWE coverage or an employer-validated frontend/mobile interview profile.

5. **P2 — assessment and lifecycle readiness remain provisional.** The original SWE bank had 203 questions, 63 explicit rubrics, 22 embedded follow-up sets and zero reviewed/fully approved records. Many other questions have useful `must_surface` guidance, so absence of a rubric does not itself invalidate them; it does limit criterion-addressable follow-ups and consistent score mapping. The question schema does not require a rubric, and `build_release.py` selects `status: reviewed` without checking all review approvals. `validate.py` currently does not enforce that question-status transition. A guarded review/promotion rule should precede a production reviewed-only release. No records are promoted by this review.

6. **P3 — D4/D5 remain sparse under the soft mix policy.** The original distribution was 110 / 57 / 30 / 5 / 1. The corrective distribution is 123 / 66 / 30 / 5 / 1. The D1:D5 ratio comfortably exceeds 5:1, but this does not by itself validate the whole distribution. Four soft mix advisories remain (D1 above its band, D3/D4/D5 below theirs). Do not add strategic questions just to hit a percentage; add distinct senior-level decisions where warranted.

## Distinct topics to address before comprehensive coverage sign-off

These are qualitative review findings, not additional numerical floors. Existing adjacent questions can be extended when they can elicit and assess the missing evidence.

| Competency area | Missing or thin direct assessment | Suggested next bounded exercise |
|---|---|---|
| Software delivery | Git history/branching, merge conflicts, reproducible dependency locks | Resolve a conflicting change; review a dependency/configuration upgrade and rollback |
| Programming | Types, abstraction choices and a practical refactoring exercise beyond functions/control flow | Refactor a small module around a clear interface and test the contract |
| Communication | Audience adaptation and actual written output rather than incidental explanation labels | Explain an outage to a non-technical stakeholder; write an engineering handover |
| Reliability/operations | Explicit SLIs/error budgets, backup/restore verification and runbook use | Choose an SLI/SLO, then execute a recovery tabletop with success criteria |
| Application security | Distinct injection, output encoding/XSS and CSRF defensive reasoning | Review a vulnerable handler/template and justify mitigation plus regression tests |
| Algorithms/data structures | Limited implemented problem variety; overlapping cache/graph scenarios dominate practical coding | Add a genuinely distinct bounded string/sequence or dynamic-programming implementation if supported by role evidence |
| Scope boundary | Frontend, mobile and accessibility are outside the current backend-biased role profile | Add evidence-backed specialist profiles rather than silently claiming these are covered |

## Corrective tranche

Adds `tic-q-000207`–`tic-q-000228`: 13 D1 and 9 D2 questions. Every new question has observable rubric criteria, honest synthetic/LLM-generated provenance, CC-BY-4.0 licensing, technical/taxonomy review pending, and draft lifecycle status. No personal interview records or STAR stories are included.

| Competency | New D1 IDs | New D2 IDs |
|---|---|---|
| ambiguity-and-adaptability | tic-q-000219, tic-q-000220, tic-q-000221 | tic-q-000222, tic-q-000223 |
| leadership-and-influence | tic-q-000211, tic-q-000212, tic-q-000213 | tic-q-000214, tic-q-000215, tic-q-000216 |
| learning-and-reflection |  | tic-q-000228 |
| prioritisation | tic-q-000224, tic-q-000225, tic-q-000226 | tic-q-000227 |
| secrets-management | tic-q-000207, tic-q-000208 | tic-q-000209, tic-q-000210 |
| stakeholder-management | tic-q-000217, tic-q-000218 | existing coverage sufficient |

Adds 162 directed edges: 80 escalation and 82 recovery links. The combined graph has 223 edges (115 escalate, 107 recover, 1 deepen). All 37 competencies now have at least one shared-competency D1 escalation with its paired recovery edge. 60 D1 nodes remain isolated; this is reported explicitly. Paths remain draft editorial choices and need calibration with actual interview outcomes.

`tools/audit_role_coverage.py` reports primary versus tagged counts, review status, rubrics, embedded follow-ups and graph isolation. It excludes deprecated and other-role records. CI runs its regression tests, publishes the inventory in the job summary and includes JSON in the preview bundle before checksum finalisation. The existing advisory floors and caps policy are unchanged.

| Measure | Original stack | Corrective branch |
|---|---:|---:|
| SWE questions | 203 | 225 |
| Core competencies meeting tagged floors | 13/13 | 13/13 |
| Important competencies meeting tagged floors | 18/24 | 24/24 |
| Competencies with D1 escalation and recovery | 14/37 | 37/37 |
| Reviewed / fully approved SWE records | 0 / 0 | 0 / 0 |

See [original inventory](swe-coverage-before-2026-11-03.md) and [corrective inventory](swe-coverage-inventory-2026-11-03.md) for all 37 competency rows. Regenerate with `python tools/audit_role_coverage.py`; use `--json` for structured output.

## PR-by-PR inventory

The assessment of an audit-only PR is its reasoning and evidence, not an expectation that every competency needs duplicate primary questions. All rows had successful CI at the observed head.

| PR | Scope | Question additions | Review assessment |
|---|---|---:|---|
| [#1](https://github.com/rmcmillan34/technical-interview-corpus/pull/1) | Define v0.1 corpus schema, taxonomy, role profiles and release pipeline | 5 | Schema/taxonomy and distribution baseline; reviewed-question promotion guard remains follow-up work. |
| [#2](https://github.com/rmcmillan34/technical-interview-corpus/pull/2) | Lock v0.1 licensing and provenance governance | 0 | Provenance gate is present; no external content added by this PR. |
| [#3](https://github.com/rmcmillan34/technical-interview-corpus/pull/3) | Add first reviewed source intake and system-design tranche | 5 | Draft system-design adaptation with attribution; content calibration remains pending. |
| [#4](https://github.com/rmcmillan34/technical-interview-corpus/pull/4) | Add SWE coding and behavioural interview tranche | 10 | Useful coding/behavioural tranche; disagreement prompt overlaps reference #2. |
| [#5](https://github.com/rmcmillan34/technical-interview-corpus/pull/5) | Add SWE foundation, systematic coverage and algorithms expansion | 27 | Useful distinct additions; technical/taxonomy approval remains pending. |
| [#6](https://github.com/rmcmillan34/technical-interview-corpus/pull/6) | Expand SWE data-structures coverage | 8 | Useful distinct additions; technical/taxonomy approval remains pending. |
| [#7](https://github.com/rmcmillan34/technical-interview-corpus/pull/7) | Expand SWE programming foundation coverage | 5 | Useful distinct additions; technical/taxonomy approval remains pending. |
| [#8](https://github.com/rmcmillan34/technical-interview-corpus/pull/8) | Expand SWE API design coverage | 12 | Useful distinct additions; technical/taxonomy approval remains pending. |
| [#9](https://github.com/rmcmillan34/technical-interview-corpus/pull/9) | Expand SWE testing coverage | 8 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#10](https://github.com/rmcmillan34/technical-interview-corpus/pull/10) | Expand SWE debugging coverage | 5 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#11](https://github.com/rmcmillan34/technical-interview-corpus/pull/11) | Expand SWE software architecture coverage | 10 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#12](https://github.com/rmcmillan34/technical-interview-corpus/pull/12) | Expand SWE distributed systems coverage | 9 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#13](https://github.com/rmcmillan34/technical-interview-corpus/pull/13) | Complete SWE reliability engineering coverage floor | 1 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#14](https://github.com/rmcmillan34/technical-interview-corpus/pull/14) | Audit SWE communication coverage | 0 | No-add reasoning relies on aggregate secondary-tag counts; keep qualitative review open. |
| [#15](https://github.com/rmcmillan34/technical-interview-corpus/pull/15) | Expand SWE ownership and delivery coverage | 13 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#16](https://github.com/rmcmillan34/technical-interview-corpus/pull/16) | Expand SWE collaboration and conflict coverage | 13 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#17](https://github.com/rmcmillan34/technical-interview-corpus/pull/17) | Audit SWE technical judgement coverage | 0 | No-add reasoning relies on aggregate secondary-tag counts; keep qualitative review open. |
| [#18](https://github.com/rmcmillan34/technical-interview-corpus/pull/18) | Expand SWE operating systems coverage | 6 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#19](https://github.com/rmcmillan34/technical-interview-corpus/pull/19) | Expand SWE networking coverage | 6 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#20](https://github.com/rmcmillan34/technical-interview-corpus/pull/20) | Expand SWE concurrency coverage | 3 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#21](https://github.com/rmcmillan34/technical-interview-corpus/pull/21) | Expand SWE software delivery practices coverage | 6 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#22](https://github.com/rmcmillan34/technical-interview-corpus/pull/22) | Complete SWE performance engineering coverage floor | 2 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#23](https://github.com/rmcmillan34/technical-interview-corpus/pull/23) | Audit SWE observability coverage | 0 | No-add reasoning relies on aggregate secondary-tag counts; keep qualitative review open. |
| [#24](https://github.com/rmcmillan34/technical-interview-corpus/pull/24) | Expand SWE cloud architecture coverage | 8 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#25](https://github.com/rmcmillan34/technical-interview-corpus/pull/25) | Expand SWE containerisation coverage | 8 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#26](https://github.com/rmcmillan34/technical-interview-corpus/pull/26) | Expand SWE CI/CD coverage | 5 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#27](https://github.com/rmcmillan34/technical-interview-corpus/pull/27) | Expand SWE infrastructure as code coverage | 8 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#28](https://github.com/rmcmillan34/technical-interview-corpus/pull/28) | Audit SWE service operations coverage | 0 | No-add reasoning relies on aggregate secondary-tag counts; keep qualitative review open. |
| [#29](https://github.com/rmcmillan34/technical-interview-corpus/pull/29) | Expand SWE SQL coverage | 8 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#30](https://github.com/rmcmillan34/technical-interview-corpus/pull/30) | Complete SWE data modelling foundation coverage | 2 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#31](https://github.com/rmcmillan34/technical-interview-corpus/pull/31) | Audit SWE databases coverage | 0 | No-add reasoning relies on aggregate secondary-tag counts; keep qualitative review open. |
| [#32](https://github.com/rmcmillan34/technical-interview-corpus/pull/32) | Expand SWE threat modelling coverage | 8 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#33](https://github.com/rmcmillan34/technical-interview-corpus/pull/33) | Audit SWE security architecture coverage | 0 | No-add reasoning relies on aggregate secondary-tag counts; keep qualitative review open. |
| [#34](https://github.com/rmcmillan34/technical-interview-corpus/pull/34) | Expand SWE identity and access control coverage | 5 | Useful distinct additions; technical/taxonomy approval remains pending. No path changes in this PR; representative routes added by the corrective branch. |
| [#35](https://github.com/rmcmillan34/technical-interview-corpus/pull/35) | Audit SWE application security coverage | 0 | No-add reasoning relies on aggregate secondary-tag counts; keep qualitative review open. |

## Validation

Original combined stack: schema, provenance and coverage/progression validators passed; 14 coverage advisories (ten competency-depth gaps and four mix advisories).

Corrective branch: all three validators pass for 228 total / 225 SWE records; three coverage-inventory regression tests pass; preview bundle builds and all finalised SHA-256 checksums verify. Four difficulty-mix advisories intentionally remain. No claim of independent technical review, employer approval or comprehensive subtopic coverage is made.

## Merge handling

The follow-up is based on #35, preserving the stack. Merge/rebase in dependency order and let CI rerun after base changes; do not merge the tip into main as an accidental substitute for reviewing the stack. Merging draft content does not change its per-record technical/taxonomy status.
