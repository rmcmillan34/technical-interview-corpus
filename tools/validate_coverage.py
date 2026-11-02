#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
QUESTION_ROOT = ROOT / "questions"
ROLE_PROFILE_ROOT = ROOT / "evidence" / "role-profiles"
COVERAGE_ROOT = ROOT / "coverage"
PATH_ROOT = ROOT / "paths"
DIFFICULTIES = ("D1", "D2", "D3", "D4", "D5")
DIFFICULTY_RANK = {value: index for index, value in enumerate(DIFFICULTIES, start=1)}
RELATIONS = {"escalate", "recover", "deepen"}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_questions() -> dict[str, dict]:
    records: dict[str, dict] = {}
    for path in sorted(QUESTION_ROOT.rglob("*.yaml")):
        question = load_yaml(path)
        records[question["id"]] = question
    return records


def profile_for(role: str) -> dict | None:
    path = ROLE_PROFILE_ROOT / f"{role}.yaml"
    return load_yaml(path) if path.is_file() else None


def validate_target_block(path: Path, label: str, block: dict, errors: list[str]) -> None:
    for difficulty in DIFFICULTIES:
        target = block.get(difficulty)
        if not isinstance(target, dict):
            errors.append(f"{path}: {label}.{difficulty} must be an object")
            continue
        minimum = target.get("min")
        preferred = target.get("preferred")
        if not isinstance(minimum, int) or minimum < 0:
            errors.append(f"{path}: {label}.{difficulty}.min must be a non-negative integer")
        if not isinstance(preferred, int) or preferred < 0:
            errors.append(f"{path}: {label}.{difficulty}.preferred must be a non-negative integer")
        if isinstance(minimum, int) and isinstance(preferred, int) and minimum > preferred:
            errors.append(f"{path}: {label}.{difficulty}.min cannot exceed preferred")


def validate_coverage(path: Path, data: dict, questions: dict[str, dict], errors: list[str], advisories: list[str]) -> None:
    role = data.get("role")
    profile = profile_for(role) if isinstance(role, str) else None
    if profile is None:
        errors.append(f"{path}: unknown role/profile {role!r}")
        return

    targets = data.get("coverage_targets", {})
    core = targets.get("core", {})
    important = targets.get("important", {})
    core_competencies = core.get("competencies", [])
    important_competencies = important.get("competencies", [])

    expected_core = set(profile["calibration"]["role_importance"]["core"])
    expected_important = set(profile["calibration"]["role_importance"]["important"])
    if set(core_competencies) != expected_core:
        missing = sorted(expected_core - set(core_competencies))
        extra = sorted(set(core_competencies) - expected_core)
        errors.append(f"{path}: core competency plan differs from role profile; missing={missing}, extra={extra}")
    if set(important_competencies) != expected_important:
        missing = sorted(expected_important - set(important_competencies))
        extra = sorted(set(important_competencies) - expected_important)
        errors.append(f"{path}: important competency plan differs from role profile; missing={missing}, extra={extra}")
    overlap = set(core_competencies) & set(important_competencies)
    if overlap:
        errors.append(f"{path}: competencies appear in both core and important plans: {sorted(overlap)}")

    validate_target_block(path, "coverage_targets.core.default", core.get("default", {}), errors)
    validate_target_block(path, "coverage_targets.important.default", important.get("default", {}), errors)

    mix = data.get("policy", {}).get("difficulty_mix_target", {})
    min_total = 0
    max_total = 0
    for difficulty in DIFFICULTIES:
        band = mix.get(difficulty)
        if not isinstance(band, dict):
            errors.append(f"{path}: difficulty_mix_target.{difficulty} must be an object")
            continue
        minimum = band.get("min_percent")
        maximum = band.get("max_percent")
        if not isinstance(minimum, (int, float)) or not 0 <= minimum <= 100:
            errors.append(f"{path}: invalid min_percent for {difficulty}")
            continue
        if not isinstance(maximum, (int, float)) or not 0 <= maximum <= 100:
            errors.append(f"{path}: invalid max_percent for {difficulty}")
            continue
        if minimum > maximum:
            errors.append(f"{path}: min_percent exceeds max_percent for {difficulty}")
        min_total += minimum
        max_total += maximum
    if min_total > 100 or max_total < 100:
        errors.append(f"{path}: difficulty bands cannot contain a 100% distribution (min_total={min_total}, max_total={max_total})")

    role_questions = [q for q in questions.values() if role in q["classification"]["roles"]]
    counts: dict[str, Counter] = defaultdict(Counter)
    overall = Counter()
    for question in role_questions:
        difficulty = question["classification"]["difficulty"]["level"]
        overall[difficulty] += 1
        competencies = question["classification"]["competencies"]
        for competency in [competencies["primary"], *competencies.get("secondary", [])]:
            counts[competency][difficulty] += 1

    for importance, block in (("core", core), ("important", important)):
        defaults = block.get("default", {})
        for competency in block.get("competencies", []):
            for difficulty in DIFFICULTIES:
                minimum = defaults[difficulty]["min"]
                actual = counts[competency][difficulty]
                if actual < minimum:
                    advisories.append(
                        f"{role}:{competency}:{difficulty} has {actual}, below planning minimum {minimum} ({importance})"
                    )

    total = sum(overall.values())
    if total:
        for difficulty in DIFFICULTIES:
            percent = 100 * overall[difficulty] / total
            band = mix[difficulty]
            if percent < band["min_percent"] or percent > band["max_percent"]:
                advisories.append(
                    f"{role}:{difficulty} is {percent:.1f}% ({overall[difficulty]}/{total}), outside soft target "
                    f"{band['min_percent']}-{band['max_percent']}%"
                )

        ratio_target = data.get("policy", {}).get("expected_shape", {}).get("D1_to_D5_min_ratio")
        if isinstance(ratio_target, (int, float)) and overall["D5"]:
            ratio = overall["D1"] / overall["D5"]
            if ratio < ratio_target:
                advisories.append(
                    f"{role}: D1:D5 ratio is {ratio:.1f}:1, below soft minimum {ratio_target}:1"
                )

    print(f"Coverage snapshot for {role}: " + ", ".join(f"{d}={overall[d]}" for d in DIFFICULTIES))


def validate_paths(path: Path, data: dict, questions: dict[str, dict], errors: list[str]) -> None:
    role = data.get("role")
    if profile_for(role) is None:
        errors.append(f"{path}: unknown role/profile {role!r}")
        return

    seen: set[tuple[str, str, str]] = set()
    for index, edge in enumerate(data.get("edges", []), start=1):
        source_id = edge.get("from")
        target_id = edge.get("to")
        relation = edge.get("relation")
        label = f"{path}: edge {index}"

        if relation not in RELATIONS:
            errors.append(f"{label}: invalid relation {relation!r}")
            continue
        if source_id == target_id:
            errors.append(f"{label}: self-edge is not allowed")
            continue
        if source_id not in questions:
            errors.append(f"{label}: unknown source question {source_id}")
            continue
        if target_id not in questions:
            errors.append(f"{label}: unknown target question {target_id}")
            continue
        key = (source_id, target_id, relation)
        if key in seen:
            errors.append(f"{label}: duplicate edge {key}")
        seen.add(key)

        source = questions[source_id]
        target = questions[target_id]
        if role not in source["classification"]["roles"] or role not in target["classification"]["roles"]:
            errors.append(f"{label}: both questions must include role {role}")

        source_difficulty = source["classification"]["difficulty"]["level"]
        target_difficulty = target["classification"]["difficulty"]["level"]
        source_rank = DIFFICULTY_RANK[source_difficulty]
        target_rank = DIFFICULTY_RANK[target_difficulty]
        if relation == "escalate" and target_rank <= source_rank:
            errors.append(f"{label}: escalate must increase difficulty ({source_difficulty} -> {target_difficulty})")
        elif relation == "recover" and target_rank >= source_rank:
            errors.append(f"{label}: recover must decrease difficulty ({source_difficulty} -> {target_difficulty})")
        elif relation == "deepen" and target_rank != source_rank:
            errors.append(f"{label}: deepen must remain at the same difficulty ({source_difficulty} -> {target_difficulty})")

        rationale = edge.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            errors.append(f"{label}: rationale is required")


def main() -> int:
    questions = load_questions()
    errors: list[str] = []
    advisories: list[str] = []

    coverage_paths = sorted(COVERAGE_ROOT.glob("*.yaml")) if COVERAGE_ROOT.is_dir() else []
    graph_paths = sorted(PATH_ROOT.glob("*.yaml")) if PATH_ROOT.is_dir() else []
    if not coverage_paths:
        errors.append("No role coverage plans found under coverage/")
    if not graph_paths:
        errors.append("No assessment progression graphs found under paths/")

    for path in coverage_paths:
        try:
            validate_coverage(path, load_yaml(path), questions, errors, advisories)
        except Exception as exc:
            errors.append(f"{path}: coverage validation error: {exc}")

    for path in graph_paths:
        try:
            validate_paths(path, load_yaml(path), questions, errors)
        except Exception as exc:
            errors.append(f"{path}: progression validation error: {exc}")

    if errors:
        print("Coverage/progression validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Coverage/progression validation passed with {len(advisories)} advisory coverage gap(s).")
    for advisory in advisories:
        print(f"  advisory: {advisory}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
