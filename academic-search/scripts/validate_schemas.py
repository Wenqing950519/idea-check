#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    schemas = {path.name: load(path) for path in sorted((ROOT / "schemas").glob("*.schema.json"))}
    for schema in schemas.values():
        Draft202012Validator.check_schema(schema)

    claim_validator = Draft202012Validator(schemas["claim.schema.json"])
    evidence_validator = Draft202012Validator(schemas["evidence.schema.json"])
    fixtures = [
        path for path in sorted((ROOT / "tests" / "fixtures").glob("*.json"))
        if {"claim", "evidence"}.issubset(load(path))
    ]
    if len(fixtures) != 5:
        raise ValueError(f"Expected exactly five JSON fixtures; found {len(fixtures)}")
    for path in fixtures:
        fixture = load(path)
        claim_validator.validate(fixture["claim"])
        for evidence in fixture["evidence"]:
            evidence_validator.validate(evidence)
    print(f"Validated {len(schemas)} schemas and {len(fixtures)} legacy fixtures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
