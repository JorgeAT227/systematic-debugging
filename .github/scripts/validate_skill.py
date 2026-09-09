#!/usr/bin/env python3
"""CI validation for skill repositories.

Validates:
  1. metadata.json is valid JSON with the required manifest fields.
  2. SKILL.md has YAML frontmatter with the required fields.
  3. metadata.json and SKILL.md frontmatter are mutually consistent
     (name, version, license, author).

Exit code 0 on success, 1 on any validation error.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REQUIRED_METADATA_FIELDS = ("name", "version", "description", "license", "author", "category", "tags")
REQUIRED_FRONTMATTER_FIELDS = ("name", "description", "license")
REQUIRED_FRONTMATTER_METADATA = ("version", "author")

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


def parse_frontmatter(text: str) -> dict | None:
    """Parse the minimal YAML frontmatter subset used by SKILL.md files."""
    if not text.startswith("---\n"):
        return None
    frontmatter: dict = {}
    section: str | None = None
    for line in text.splitlines()[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if indent == 0:
            section = key
            frontmatter[key] = value if value else {}
        elif indent > 0 and section is not None and isinstance(frontmatter.get(section), dict):
            frontmatter[section][key] = value
    return frontmatter


def validate(repo_root: Path, expected_name: str | None) -> int:
    errors: list[str] = []
    info: list[str] = []

    metadata_path = repo_root / "metadata.json"
    skill_path = repo_root / "SKILL.md"

    if not metadata_path.is_file():
        errors.append("Falta metadata.json")
    if not skill_path.is_file():
        errors.append("Falta SKILL.md")
    if errors:
        return _report(errors, info)

    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"metadata.json no es JSON válido: {exc}")
        return _report(errors, info)

    frontmatter = parse_frontmatter(skill_path.read_text(encoding="utf-8"))
    if frontmatter is None:
        errors.append("SKILL.md no tiene frontmatter YAML (debe empezar con '---')")

    # 1. metadata.json fields
    for field in REQUIRED_METADATA_FIELDS:
        if field not in metadata:
            errors.append(f"metadata.json: falta el campo '{field}'")
    if "tags" in metadata and (not isinstance(metadata["tags"], list) or not metadata["tags"]):
        errors.append("metadata.json: 'tags' debe ser una lista no vacía")
    if "version" in metadata and not SEMVER_RE.match(str(metadata["version"])):
        errors.append(f"metadata.json: 'version' '{metadata['version']}' no sigue semver (X.Y.Z)")
    info.append(
        f"metadata.json: name={metadata.get('name')} version={metadata.get('version')} "
        f"license={metadata.get('license')}"
    )

    # 2. SKILL.md frontmatter fields
    if frontmatter is not None:
        for field in REQUIRED_FRONTMATTER_FIELDS:
            if field not in frontmatter:
                errors.append(f"SKILL.md frontmatter: falta el campo '{field}'")
        md_block = frontmatter.get("metadata")
        if not isinstance(md_block, dict):
            errors.append("SKILL.md frontmatter: falta el bloque 'metadata:'")
        else:
            for field in REQUIRED_FRONTMATTER_METADATA:
                if field not in md_block:
                    errors.append(f"SKILL.md frontmatter metadata: falta el campo '{field}'")
        fm_version = (frontmatter.get("metadata") or {}).get("version")
        info.append(f"SKILL.md frontmatter: name={frontmatter.get('name')} version={fm_version}")

    # 3. Cross-consistency between metadata.json and SKILL.md
    if frontmatter is not None and isinstance(frontmatter.get("metadata"), dict):
        fm_md = frontmatter["metadata"]
        for field, meta_val, fm_val in (
            ("name", metadata.get("name"), frontmatter.get("name")),
            ("version", metadata.get("version"), fm_md.get("version")),
            ("license", metadata.get("license"), frontmatter.get("license")),
            ("author", metadata.get("author"), fm_md.get("author")),
        ):
            if meta_val != fm_val:
                errors.append(
                    f"Inconsistencia en '{field}': metadata.json='{meta_val}' vs SKILL.md='{fm_val}'"
                )

    # 4. Repo name check (SKILL_NAME env, injected by GitHub Actions)
    if expected_name and metadata.get("name") != expected_name:
        errors.append(
            f"'name' en metadata.json ('{metadata.get('name')}') no coincide con el repo '{expected_name}'"
        )

    return _report(errors, info)


def _report(errors: list[str], info: list[str]) -> int:
    for line in info:
        print(f"ℹ️  {line}")
    if errors:
        print("❌ Validación fallida:")
        for err in errors:
            print(f"   - {err}")
        return 1
    print("✅ Validación correcta: metadata.json y SKILL.md son consistentes.")
    return 0


def main() -> int:
    repo_root = Path(os.environ.get("REPO_ROOT", ".")).resolve()
    expected_name = os.environ.get("SKILL_NAME") or None
    return validate(repo_root, expected_name)


if __name__ == "__main__":
    sys.exit(main())