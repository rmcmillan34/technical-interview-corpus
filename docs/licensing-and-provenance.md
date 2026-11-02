# Licensing and provenance policy

This document defines the repository policy for creating, adapting, importing, reviewing and distributing interview corpus material. It is a project governance policy, not legal advice.

## 1. Default licenses

The repository deliberately separates software from corpus content:

| Material | Default licence |
| --- | --- |
| Tooling, schemas, CI/workflows | Apache-2.0 |
| Original questions, rubrics, taxonomies, documentation and native assets | CC BY 4.0 |
| Third-party material | The compatible source licence recorded for that item |

`LICENSE.md` defines the path-level defaults. Record-level licensing overrides the native content default for imported material.

## 2. Provenance classes

Canonical question records use four provenance origins:

- `native`: independently authored for this project. LLM assistance may be disclosed in `provenance.authoring`.
- `synthetic`: generated primarily by an LLM and subsequently reviewed by a human before release eligibility.
- `external-verbatim`: source expression is reproduced substantially as published. This requires an approved source that explicitly permits verbatim redistribution.
- `external-adapted`: source material is transformed into a corpus question. This requires an approved source that permits adaptation and a clear `modification` statement.

`native` and `synthetic` records must not use the source field to launder copied material. If expression is copied or adapted from an external source, use an external provenance class.

## 3. Source register

`sources/source-register.yaml` is the authoritative rights/provenance registry for material that may influence corpus ingestion. Each external question source must match an approved register entry by canonical URL.

The register records:

- stable source ID;
- canonical URL and publisher;
- date the licence/source status was observed;
- licence identifier and licence URL;
- permitted project uses;
- required downstream/release licence;
- attribution text; and
- maintainer review status.

Question records intentionally retain a small source snapshot (`name`, `url`, `license`, attribution/modification) so exported JSONL remains interpretable without the Git repository. CI verifies that this snapshot agrees with the authoritative register.

## 4. Distribution classifications

### `core`

The source has sufficiently clear rights for the uses explicitly listed in `permitted_uses` and is eligible for the main corpus distribution after maintainer approval.

A `core` source used by a released question must have:

- an explicit licence identifier and licence URL;
- an explicit `release_license_spdx`;
- attribution text; and
- `review: approved`.

### `research-only`

The source may be used to understand topics, competency coverage, terminology or market/interview patterns, but its expression must not be copied or adapted into distributed corpus records.

Project policy requires `permitted_uses` to be exactly `[influence]`. Research-only material is not referenced as the provenance basis for a released copied/adapted question; resulting native questions must be independently expressed.

Sources with no explicit reusable licence are treated as `research-only` by default until rights are established.

### `excluded`

The source is not eligible for corpus ingestion. `permitted_uses` must be empty.

## 5. Conservative compatibility policy

The project does not attempt to solve every possible licence-combination question in v0.1.

- Permissive material is reviewed case by case and must be explicitly registered before ingestion.
- ShareAlike/copyleft content defaults to `research-only` until the project implements and reviews a segregated distribution model that preserves all downstream obligations.
- Material with unclear ownership, missing licensing, private interview-process restrictions, NDA restrictions, paywall terms that prohibit redistribution, or other unresolved rights concerns does not enter the distributable corpus.

This conservative policy is intentional: a smaller corpus with defensible provenance is preferable to a larger corpus with uncertain reuse rights.

## 6. Attribution and modifications

For `external-verbatim` questions:

- at least one source is required;
- every source must be approved and permit `verbatim` use;
- source licence metadata in the question must match the register; and
- attribution is mandatory.

For `external-adapted` questions:

- at least one source is required;
- every source must be approved and permit `adapted` use;
- attribution is mandatory; and
- each source entry must explain the material modification.

For native CC BY 4.0 content, downstream users should attribute the Technical Interview Corpus contributors and indicate modifications when applicable.

## 7. AI-assisted authoring

LLM use is permitted but must be disclosed accurately:

- `human`: written without material LLM drafting;
- `llm-assisted`: a human remains the primary author but an LLM assisted with drafting, critique or refinement;
- `llm-generated`: the initial question was primarily generated by an LLM.

LLM output is not treated as proof of originality or licensing. Contributors remain responsible for avoiding copied source expression and for disclosing external material supplied to the model.

A `synthetic` question is not release-ready merely because it validates structurally; it still requires technical, taxonomy and provenance review.

## 8. Interview confidentiality and proprietary material

Do not contribute:

- confidential or NDA-covered interview questions;
- private recruiting packets or candidate materials;
- questions reconstructed from a closed interview process when redistribution rights are unclear;
- leaked assessment banks;
- employer content merely because it is publicly viewable; or
- material from a repository or website that lacks an explicit reuse licence, except as research-only evidence.

A public URL is not, by itself, sufficient evidence that the wording can be redistributed.

## 9. Review and release gates

A question can appear in a production release only when:

1. `status: reviewed`;
2. technical, taxonomy and provenance reviews are `approved`;
3. provenance rules pass CI;
4. external sources, if any, are approved `core` sources;
5. question/source licences are internally consistent; and
6. referenced assets exist and follow the same provenance policy.

Development preview artifacts may include drafts but remain non-release test output.

## 10. Source changes and withdrawals

Source rights can change or errors can be discovered. Source-register entries are therefore version-controlled evidence, not permanent claims about a website.

If a source becomes unsuitable:

1. change its review/distribution state in a PR;
2. identify dependent questions;
3. deprecate, rewrite independently, or remove affected distributed material as appropriate; and
4. document the change in release notes.

Historical Git tags remain historical records; new releases must use the corrected governance state.
