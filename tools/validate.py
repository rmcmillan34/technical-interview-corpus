#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
QUESTION_ROOT = ROOT / "questions"
TAXONOMY_ROOT = ROOT / "taxonomy"
SCHEMA_PATH = ROOT / "schemas" / "question.schema.json"
TEMPLATE_RE = re.compile(r"\{\{([a-zA-Z0-9_-]+)\}\}")


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def taxonomy_ids(filename: str, key: str):
    data = load_yaml(TAXONOMY_ROOT / filename)
    values = data[key]
    if values and isinstance(values[0], dict):
        return {item["id"] for item in values}
    return set(values)


def technology_registry():
    data = load_yaml(TAXONOMY_ROOT / "technologies.yaml")
    return {item["id"]: set(item.get("categories", [])) for item in data["technologies"]}


def iter_asset_paths(question):
    for item in question.get("question", {}).get("stimuli", []) or []:
        if "path" in item:
            yield item["path"]
    for stimulus_set in question.get("question", {}).get("stimulus_sets", []) or []:
        for item in stimulus_set.get("assets", []):
            if "path" in item:
                yield item["path"]


def validate_semantics(path: Path, q: dict, seen_ids: set[str], errors: list[str]):
    qid = q["id"]
    if qid in seen_ids:
        errors.append(f"{path}: duplicate question id {qid}")
    seen_ids.add(qid)

    roles = taxonomy_ids("roles.yaml", "roles")
    competencies = taxonomy_ids("competencies.yaml", "competencies")
    domains = taxonomy_ids("domains.yaml", "domains")
    aspects = taxonomy_ids("assessment-aspects.yaml", "aspects")
    technologies = technology_registry()

    if q["question"]["domain"] not in domains:
        errors.append(f"{path}: unknown domain {q['question']['domain']}")

    for role in q["classification"]["roles"]:
        if role not in roles:
            errors.append(f"{path}: unknown role {role}")

    competency_values = [q["classification"]["competencies"]["primary"]] + q["classification"]["competencies"].get("secondary", [])
    for competency in competency_values:
        if competency not in competencies:
            errors.append(f"{path}: unknown competency {competency}")

    for aspect in q["classification"].get("aspects", []):
        if aspect not in aspects:
            errors.append(f"{path}: unknown assessment aspect {aspect}")

    for technology in q["classification"].get("technologies", []):
        if technology not in technologies:
            errors.append(f"{path}: unknown technology {technology}")

    parameters = q.get("parameters", {})
    prompt_template = q["question"].get("prompt_template")
    template_slots = set(TEMPLATE_RE.findall(prompt_template or ""))
    unknown_slots = template_slots - set(parameters)
    for slot in sorted(unknown_slots):
        errors.append(f"{path}: prompt template references undeclared parameter {slot}")

    required_slots = {name for name, parameter in parameters.items() if parameter.get("policy") == "parameterised"}
    missing_slots = required_slots - template_slots
    for slot in sorted(missing_slots):
        errors.append(f"{path}: parameterised binding {slot} is missing from prompt_template")

    for name, parameter in parameters.items():
        if parameter["type"] != "technology":
            continue
        category = parameter["category"]
        for technology in parameter.get("allowed", []):
            if technology not in technologies:
                errors.append(f"{path}: parameter {name} references unknown technology {technology}")
            elif category not in technologies[technology]:
                errors.append(f"{path}: technology {technology} is not registered for parameter category {category}")

    overlay_ids = set(q.get("assessment", {}).get("technology_overlays", {}))
    parameter_techs = {tech for parameter in parameters.values() if parameter["type"] == "technology" for tech in parameter.get("allowed", [])}
    unknown_overlays = overlay_ids - parameter_techs - set(q["classification"].get("technologies", []))
    for technology in sorted(unknown_overlays):
        errors.append(f"{path}: technology overlay {technology} is not bound to the question")

    rubric_ids = {item["id"] for item in q.get("assessment", {}).get("rubric", [])}
    for followup in q.get("followups", []) or []:
        criterion = (followup.get("trigger") or {}).get("criterion")
        if criterion and criterion not in rubric_ids:
            errors.append(f"{path}: follow-up {followup['id']} references unknown rubric criterion {criterion}")

    for asset in iter_asset_paths(q):
        candidate = (ROOT / asset).resolve()
        if ROOT.resolve() not in candidate.parents:
            errors.append(f"{path}: asset path escapes repository: {asset}")
        elif not candidate.is_file():
            errors.append(f"{path}: missing asset {asset}")


def main():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    paths = sorted(QUESTION_ROOT.rglob("*.yaml"))
    errors = []
    seen_ids = set()

    if not paths:
        errors.append("No question YAML files found.")

    for path in paths:
        try:
            question = load_yaml(path)
        except Exception as exc:
            errors.append(f"{path}: YAML parse error: {exc}")
            continue

        schema_errors = list(validator.iter_errors(question))
        for error in sorted(schema_errors, key=lambda e: list(e.absolute_path)):
            location = ".".join(str(p) for p in error.absolute_path) or "<root>"
            errors.append(f"{path}: schema {location}: {error.message}")

        if not schema_errors:
            validate_semantics(path, question, seen_ids, errors)

    if errors:
        print("Corpus validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Validated {len(paths)} question(s) successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
