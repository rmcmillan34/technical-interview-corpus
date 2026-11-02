#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Add licensing and provenance metadata to a built release bundle.")
    parser.add_argument("--output", default="build/release", help="Existing release bundle directory.")
    args = parser.parse_args()

    output = (ROOT / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output).resolve()
    if not output.is_dir():
        raise SystemExit(f"release output does not exist: {output}")

    shutil.copy2(ROOT / "LICENSE.md", output / "LICENSE.md")
    destination = output / "LICENSES"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(ROOT / "LICENSES", destination)

    source_register = yaml.safe_load((ROOT / "sources" / "source-register.yaml").read_text(encoding="utf-8"))
    (output / "source-register.json").write_text(
        json.dumps(source_register, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    manifest_path = output / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["registered_source_count"] = len(source_register["sources"])
    manifest["licensing"] = {
        "software_default": "Apache-2.0",
        "native_content_default": "CC-BY-4.0",
        "policy": "LICENSE.md",
        "license_material": "LICENSES/",
        "source_register": "source-register.json",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    checksum_path = output / "checksums.txt"
    targets = sorted(path for path in output.rglob("*") if path.is_file() and path != checksum_path)
    with checksum_path.open("w", encoding="utf-8", newline="\n") as handle:
        for path in targets:
            handle.write(f"{sha256_file(path)}  {path.relative_to(output).as_posix()}\n")

    print(
        f"Finalized release metadata: {len(source_register['sources'])} registered external source(s), "
        f"licensing policy and licence material included."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
