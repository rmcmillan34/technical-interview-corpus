# technical-interview-corpus

Open, competency-mapped technical and behavioural interview question corpus for Software Engineering, Data Engineering, Data Science, Machine Learning Engineering, AI Engineering, Security Engineering, AI Security, Penetration Testing / Red Team, AI Red Team, and Quantitative Development.

## Project model

The corpus is competency-first rather than role-first. Canonical YAML questions are mapped to stable competencies, roles, D1–D5 assessment difficulty, assessment signals, provenance and licensing metadata. Release tooling generates JSONL, JSON, CSV, per-role and per-role/difficulty views without duplicating canonical source records.

Difficulty uses the project-wide progression:

**D1 Foundation → D2 Applied → D3 Production → D4 Complex → D5 Strategic**

Difficulty describes assessment demand, not employment seniority.

## Repository status

The v0.1 specification currently includes:

- 95 canonical draft competencies across 13 families;
- 10 evidence-backed draft role profiles;
- canonical question and role-profile schemas;
- parameterised technologies, multiple assets and stimulus variants;
- semantic validation in CI; and
- deterministic preview release builds.

The current questions are reference fixtures used to validate the specification. Bulk corpus ingestion follows the licensing/provenance governance defined below.

## Licensing and provenance

This repository uses a mixed-license model:

- software/tooling: **Apache-2.0**;
- original corpus content: **CC BY 4.0**; and
- approved third-party material: the compatible licence recorded for that source/question.

External material must pass the central source-register policy before it can enter the distributable corpus. Sources without clear reuse rights are treated as research-only by default.

See [LICENSE.md](LICENSE.md), [docs/licensing-and-provenance.md](docs/licensing-and-provenance.md), and [CONTRIBUTING.md](CONTRIBUTING.md).

## Validation

```bash
python -m pip install -r requirements-dev.txt
python tools/validate.py
python tools/validate_provenance.py
```

To prove the distribution pipeline with current draft fixtures:

```bash
python tools/build_release.py \
  --version 0.1.0-dev \
  --include-drafts \
  --output build/release-preview
python tools/finalize_release_metadata.py --output build/release-preview
```
