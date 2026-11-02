#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import copy
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
QUESTION_ROOT = ROOT / "questions"
TAXONOMY_ROOT = ROOT / "taxonomy"
VALIDATOR = ROOT / "tools" / "validate.py"
DIFFICULTIES = ("D1", "D2", "D3", "D4", "D5")


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def json_text(value, *, pretty: bool = True) -> str:
    if pretty:
        return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json_text(value), encoding="utf-8")


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json_text(record, pretty=False))
            handle.write("\n")


def iter_asset_records(question: dict):
    q = question.get("question", {})
    for asset in q.get("stimuli", []) or []:
        if "path" in asset:
            yield asset
    for stimulus_set in q.get("stimulus_sets", []) or []:
        for asset in stimulus_set.get("assets", []) or []:
            if "path" in asset:
                yield asset


def safe_repo_path(relative_path: str) -> Path:
    source = (ROOT / relative_path).resolve()
    root = ROOT.resolve()
    if source != root and root not in source.parents:
        raise ValueError(f"asset path escapes repository: {relative_path}")
    return source


def copy_assets(questions: list[dict], output: Path) -> list[str]:
    copied: set[str] = set()
    for question in questions:
        for asset in iter_asset_records(question):
            relative_path = asset["path"]
            if relative_path in copied:
                continue
            source = safe_repo_path(relative_path)
            if not source.is_file():
                raise FileNotFoundError(f"missing asset: {relative_path}")
            destination = output / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            copied.add(relative_path)
    return sorted(copied)


def embed_assets(question: dict) -> dict:
    embedded = copy.deepcopy(question)
    for asset in iter_asset_records(embedded):
        source = safe_repo_path(asset["path"])
        raw = source.read_bytes()
        try:
            asset["content"] = raw.decode("utf-8")
            asset["content_encoding"] = "utf-8"
        except UnicodeDecodeError:
            asset["content"] = base64.b64encode(raw).decode("ascii")
            asset["content_encoding"] = "base64"
    return embedded


def flatten_question(question: dict) -> dict[str, str | int]:
    classification = question["classification"]
    competencies = classification["competencies"]
    q = question["question"]
    provenance = question["provenance"]
    return {
        "id": question["id"],
        "revision": question["revision"],
        "status": question["status"],
        "prompt": q.get("prompt") or q.get("prompt_template") or "",
        "domain": q["domain"],
        "response_modes": "|".join(q.get("response_modes", [])),
        "difficulty": classification["difficulty"]["level"],
        "primary_competency": competencies["primary"],
        "secondary_competencies": "|".join(competencies.get("secondary", [])),
        "roles": "|".join(classification["roles"]),
        "aspects": "|".join(classification.get("aspects", [])),
        "tags": "|".join(classification.get("tags", [])),
        "technologies": "|".join(classification.get("technologies", [])),
        "provenance_origin": provenance["origin"],
        "license": question["license"]["spdx"],
    }


def write_csv(path: Path, questions: list[dict]) -> None:
    rows = [flatten_question(question) for question in questions]
    fieldnames = [
        "id",
        "revision",
        "status",
        "prompt",
        "domain",
        "response_modes",
        "difficulty",
        "primary_competency",
        "secondary_competencies",
        "roles",
        "aspects",
        "tags",
        "technologies",
        "provenance_origin",
        "license",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_questions(include_drafts: bool) -> list[dict]:
    records = [load_yaml(path) for path in sorted(QUESTION_ROOT.rglob("*.yaml"))]
    if include_drafts:
        selected = [record for record in records if record["status"] in {"draft", "reviewed"}]
    else:
        selected = [record for record in records if record["status"] == "reviewed"]
    return sorted(selected, key=lambda record: record["id"])


def build(args: argparse.Namespace) -> int:
    if not args.skip_validation:
        subprocess.run([sys.executable, str(VALIDATOR)], cwd=ROOT, check=True)

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output = output.resolve()

    if output == ROOT.resolve() or ROOT.resolve() not in output.parents:
        raise ValueError("output must be a directory inside the repository")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    questions = load_questions(args.include_drafts)
    if not questions:
        mode = "draft/reviewed" if args.include_drafts else "reviewed"
        raise RuntimeError(f"no {mode} questions available for export")

    roles_taxonomy = load_yaml(TAXONOMY_ROOT / "roles.yaml")
    competencies_taxonomy = load_yaml(TAXONOMY_ROOT / "competencies.yaml")
    role_ids = [entry["id"] if isinstance(entry, dict) else entry for entry in roles_taxonomy["roles"]]

    write_jsonl(output / "all.jsonl", questions)
    write_jsonl(output / "all-embedded.jsonl", [embed_assets(question) for question in questions])
    write_json(
        output / "corpus.json",
        {
            "corpus_version": args.version,
            "schema_version": questions[0]["schema_version"],
            "question_count": len(questions),
            "questions": questions,
        },
    )
    write_csv(output / "corpus.csv", questions)
    write_json(output / "competencies.json", competencies_taxonomy)
    write_json(output / "roles.json", roles_taxonomy)

    role_counts: dict[str, int] = {}
    role_difficulty_counts: dict[str, int] = {}
    for role in role_ids:
        role_questions = [question for question in questions if role in question["classification"]["roles"]]
        role_counts[role] = len(role_questions)
        write_jsonl(output / "roles" / f"{role}.jsonl", role_questions)

        for difficulty in DIFFICULTIES:
            filtered = [
                question
                for question in role_questions
                if question["classification"]["difficulty"]["level"] == difficulty
            ]
            key = f"{role}-{difficulty.lower()}"
            role_difficulty_counts[key] = len(filtered)
            write_jsonl(output / "role-difficulty" / f"{key}.jsonl", filtered)

    asset_paths = copy_assets(questions, output)
    difficulty_counts = Counter(
        question["classification"]["difficulty"]["level"] for question in questions
    )

    manifest = {
        "corpus_version": args.version,
        "schema_version": questions[0]["schema_version"],
        "taxonomy_version": competencies_taxonomy.get("taxonomy_version"),
        "question_count": len(questions),
        "included_statuses": ["draft", "reviewed"] if args.include_drafts else ["reviewed"],
        "asset_count": len(asset_paths),
        "exports": {
            "all_jsonl": "all.jsonl",
            "all_embedded_jsonl": "all-embedded.jsonl",
            "json": "corpus.json",
            "csv": "corpus.csv",
            "competencies": "competencies.json",
            "roles": "roles.json",
            "per_role_directory": "roles/",
            "role_difficulty_directory": "role-difficulty/",
            "assets_directory": "assets/",
        },
        "counts": {
            "difficulty": {difficulty: difficulty_counts.get(difficulty, 0) for difficulty in DIFFICULTIES},
            "roles": role_counts,
            "role_difficulty": role_difficulty_counts,
        },
        "checksums": "checksums.txt",
    }
    write_json(output / "manifest.json", manifest)

    checksum_targets = sorted(
        path for path in output.rglob("*") if path.is_file() and path.name != "checksums.txt"
    )
    with (output / "checksums.txt").open("w", encoding="utf-8", newline="\n") as handle:
        for path in checksum_targets:
            relative = path.relative_to(output).as_posix()
            handle.write(f"{sha256_file(path)}  {relative}\n")

    print(
        f"Built release bundle {args.version}: {len(questions)} question(s), "
        f"{len(asset_paths)} asset(s), {len(role_ids)} role view(s)."
    )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build deterministic corpus distribution artifacts.")
    parser.add_argument("--version", required=True, help="Corpus version embedded in the manifest.")
    parser.add_argument("--output", default="build/release", help="Output directory inside the repository.")
    parser.add_argument(
        "--include-drafts",
        action="store_true",
        help="Include draft reference questions for development/CI preview builds.",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip tools/validate.py. Intended only for callers that already validated.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    try:
        raise SystemExit(build(parse_args()))
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Release build failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
