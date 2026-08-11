#!/usr/bin/env python3
"""Render a self-contained Traditional Chinese Offer Decision brief."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from validate_report import canonical_hash, validate_report


def safe_json_payload(report: dict) -> str:
    payload = json.dumps(report, ensure_ascii=False, separators=(",", ":"))
    return (
        payload.replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Path to report.json")
    parser.add_argument("output", type=Path, nargs="?", default=Path("report.html"))
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "report-template.html",
    )
    args = parser.parse_args()

    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        template = args.template.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate_report(report)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    for token in ("{{REPORT_JSON}}", "{{REPORT_HASH}}"):
        if token not in template:
            print(f"ERROR: template missing placeholder {token}", file=sys.stderr)
            return 2

    fingerprint = canonical_hash(report)
    html = template.replace("{{REPORT_HASH}}", fingerprint).replace(
        "{{REPORT_JSON}}", safe_json_payload(report)
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8", newline="\n")
    print(f"OK: wrote {args.output} ({fingerprint})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
