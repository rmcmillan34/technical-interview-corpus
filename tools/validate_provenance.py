#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
QUESTION_ROOT = ROOT / "questions"
SOURCE_REGISTER_PATH = ROOT / "sources" / "source-register.yaml"
SOURCE_SCHEMA_PATH = ROOT / "schemas" / "source-register.schema.json"
NATIVE_LICENSE = "CC-BY-4.0"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_register(errors: list[str]) -> dict[str, dict]:
    data = load_yaml(SOURCE_REGISTER_PATH)
    schema = json.loads(SOURCE_SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        location = ".".join(str(p) for p in error.absolute_path) or "<root>"
        errors.append(f"{SOURCE_REGISTER_PATH}: schema {location}: {error.message}")

    if errors:
        return {}

    ids: set[str] = set()
    by_url: dict[str, dict] = {}
    for source in data["sources"]:
        source_id = source["id"]
        url = source["canonical_url"]
        if source_id in ids:
            errors.append(f"{SOURCE_REGISTER_PATH}: duplicate source id {source_id}")
        ids.add(source_id)
        if url in by_url:
            errors.append(f"{SOURCE_REGISTER_PATH}: duplicate canonical_url {url}")
        by_url[url] = source

        permitted = set(source["permitted_uses"])
        distribution = source["distribution"]

        if distribution == "core":
            if not permitted:
                errors.append(f"{SOURCE_REGISTER_PATH}: core source {source_id} requires permitted_uses")
            if source["review"] == "approved":
                if not source["license"]["spdx"] or not source["license"]["url"]:
                    errors.append(f"{SOURCE_REGISTER_PATH}: approved core source {source_id} requires explicit licence metadata")
                if not source["release_license_spdx"]:
                    errors.append(f"{SOURCE_REGISTER_PATH}: approved core source {source_id} requires release_license_spdx")
                if not source["attribution"]:
                    errors.append(f"{SOURCE_REGISTER_PATH}: approved core source {source_id} requires attribution")
        elif distribution == "research-only":
            if permitted != {"influence"}:
                errors.append(f"{SOURCE_REGISTER_PATH}: research-only source {source_id} must permit influence only")
            if source["release_license_spdx"] is not None:
                errors.append(f"{SOURCE_REGISTER_PATH}: research-only source {source_id} must not declare a release licence")
        elif distribution == "excluded":
            if permitted:
                errors.append(f"{SOURCE_REGISTER_PATH}: excluded source {source_id} must have no permitted uses")
            if source["release_license_spdx"] is not None:
                errors.append(f"{SOURCE_REGISTER_PATH}: excluded source {source_id} must not declare a release licence")

    return by_url


def validate_question(path: Path, question: dict, by_url: dict[str, dict], errors: list[str]) -> None:
    provenance = question["provenance"]
    origin = provenance["origin"]
    refs = provenance.get("sources", [])
    question_license = question["license"]["spdx"]
    authoring = provenance.get("authoring") or {}

    if origin in {"native", "synthetic"}:
        if refs:
            errors.append(f"{path}: {origin} questions must not carry external source snapshots")
        if question_license != NATIVE_LICENSE:
            errors.append(f"{path}: {origin} questions must use {NATIVE_LICENSE}")
        if origin == "synthetic" and authoring.get("method") != "llm-generated":
            errors.append(f"{path}: synthetic questions must declare authoring.method llm-generated")
        return

    if origin not in {"external-verbatim", "external-adapted"}:
        errors.append(f"{path}: unsupported provenance origin {origin}")
        return

    if not refs:
        errors.append(f"{path}: {origin} questions require at least one source")
        return

    required_use = "verbatim" if origin == "external-verbatim" else "adapted"

    for ref in refs:
        url = ref["url"]
        source = by_url.get(url)
        if source is None:
            errors.append(f"{path}: source is not registered: {url}")
            continue

        source_id = source["id"]
        if source["distribution"] != "core":
            errors.append(f"{path}: source {source_id} is {source['distribution']} and cannot back distributed external content")
        if source["review"] != "approved":
            errors.append(f"{path}: source {source_id} is not approved")
        if required_use not in source["permitted_uses"]:
            errors.append(f"{path}: source {source_id} does not permit {required_use} use")

        if ref["name"] != source["title"]:
            errors.append(f"{path}: source name snapshot does not match registered title for {source_id}")
        if ref["license"] != source["license"]["spdx"]:
            errors.append(f"{path}: source licence snapshot does not match registered licence for {source_id}")
        if not ref.get("attribution"):
            errors.append(f"{path}: source {source_id} requires attribution")
        if origin == "external-adapted" and not ref.get("modification"):
            errors.append(f"{path}: adapted source {source_id} requires a modification statement")

        release_license = source["release_license_spdx"]
        if release_license and question_license != release_license:
            errors.append(
                f"{path}: question licence {question_license} does not match source {source_id} release licence {release_license}"
            )


def main() -> int:
    errors: list[str] = []
    try:
        by_url = validate_register(errors)
    except Exception as exc:
        errors.append(f"source-register validation failed: {exc}")
        by_url = {}

    question_paths = sorted(QUESTION_ROOT.rglob("*.yaml"))
    for path in question_paths:
        try:
            question = load_yaml(path)
            validate_question(path, question, by_url, errors)
        except Exception as exc:
            errors.append(f"{path}: provenance validation error: {exc}")

    if errors:
        print("Licensing/provenance validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        f"Validated licensing/provenance for {len(question_paths)} question(s) "
        f"against {len(by_url)} registered external source(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
