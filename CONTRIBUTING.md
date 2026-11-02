# Contributing

Thanks for helping build a reusable technical and behavioural interview corpus. Contributions are welcome, but corpus quality depends on both technical review and defensible provenance.

## Before contributing a question

1. Search for an existing canonical question assessing the same construct.
2. Identify the primary competency and applicable roles.
3. Choose the D1–D5 difficulty based on assessment demand, not job title or obscurity.
4. Decide whether the question is `native`, `synthetic`, `external-verbatim`, or `external-adapted`.
5. If external material is involved, ensure the source is already approved in `sources/source-register.yaml` or include a source-register change in the same PR.
6. Do not contribute confidential, NDA-covered, leaked, proprietary, or otherwise non-redistributable interview material.

## Licensing

By intentionally submitting material for inclusion, you represent that you have the right to contribute it and accept the repository's licensing model:

- software/tooling contributions: Apache-2.0;
- original corpus/content contributions: CC BY 4.0; and
- compatible third-party material: its declared source licence, with complete provenance.

See `LICENSE.md` and `docs/licensing-and-provenance.md` before submitting imported or adapted material.

## Source policy

A source being publicly accessible does not make it eligible for redistribution. Project policy is:

- explicit compatible licence + approved source record -> eligible only for the registered uses;
- no explicit reusable licence -> research-only by default;
- ShareAlike/copyleft source -> research-only until a segregated distribution design is implemented and reviewed;
- unresolved/private/confidential material -> excluded.

For adapted material, describe what changed. For verbatim material, preserve required attribution. LLM use does not remove source obligations.

## AI-assisted contributions

Disclose authoring method accurately in `provenance.authoring`. LLM-assisted and LLM-generated questions are welcome, but they receive the same technical, taxonomy and provenance review as human-drafted material.

Do not ask an LLM to reproduce proprietary interview banks or to disguise copied questions as original work.

## Validation

Before requesting review, run:

```bash
python -m pip install -r requirements-dev.txt
python tools/validate.py
python tools/validate_provenance.py
python tools/build_release.py --version 0.1.0-dev --include-drafts --output build/release-preview
python tools/finalize_release_metadata.py --output build/release-preview
```

CI performs the same validation and preview-build checks.

## Review expectations

A question is not production-release eligible until:

- `status` is `reviewed`;
- technical review is approved;
- taxonomy review is approved;
- provenance review is approved; and
- all external sources pass source-register validation.

Keep pull requests focused. Taxonomy changes, new source approvals and new question batches should be easy for reviewers to reason about independently.
