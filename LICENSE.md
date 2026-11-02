# Licensing

This repository uses a mixed-license model so that software tooling and corpus content can be reused under terms appropriate to each kind of work.

## Software and tooling — Apache-2.0

Unless a file says otherwise, the following repository paths are licensed under the Apache License 2.0:

- `tools/**`
- `schemas/**`
- `.github/**`
- `requirements-dev.txt`

The full Apache-2.0 text is in `LICENSES/Apache-2.0.txt`.

## Native corpus content — CC BY 4.0

Original project content is licensed under the Creative Commons Attribution 4.0 International license (CC BY 4.0), unless a record explicitly declares a different third-party license. This includes:

- `questions/**`
- `assets/**` when created specifically for a native question
- `taxonomy/**`
- `evidence/**`
- `sources/**`
- `docs/**`
- `README.md`
- `CONTRIBUTING.md`

Official license information and legal code:

- https://creativecommons.org/licenses/by/4.0/
- https://creativecommons.org/licenses/by/4.0/legalcode

Suggested attribution for native corpus content:

> Technical Interview Corpus contributors, `rmcmillan34/technical-interview-corpus`, CC BY 4.0. Changes indicated where applicable.

## Third-party corpus material

A question or asset derived from third-party material is **not relicensed by this repository merely because it appears here**. Its record-level `license.spdx` field and the corresponding entry in `sources/source-register.yaml` govern its reuse.

Third-party material is accepted into the distributable corpus only after its source register entry is approved and the validator confirms that the declared use is allowed by project policy.

Sources classified as `research-only` or `excluded` are not redistributed as question text or assets.

## Contributions

By intentionally submitting a contribution for inclusion in this repository, you represent that you have the right to submit it and agree that:

- software/tooling contributions are provided under Apache-2.0; and
- original corpus/content contributions are provided under CC BY 4.0,

unless the contribution is clearly identified as compatible third-party material with complete provenance and licensing metadata.

See `docs/licensing-and-provenance.md` and `CONTRIBUTING.md` for the repository's ingestion and attribution rules.
