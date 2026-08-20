#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from adapters.static import StaticEvidenceAdapter
from src.models import Evidence
from src.pipeline import AuditPipeline


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the legacy deterministic claim-audit compatibility workflow.")
    parser.add_argument("document", type=Path, help="Markdown or text document")
    parser.add_argument("--evidence", type=Path, help="Optional JSON array or object containing an evidence array")
    parser.add_argument("--citations", type=Path, help="Optional JSON mapping from claim IDs to evidence IDs")
    parser.add_argument("--output-dir", type=Path, default=Path("audit-output"))
    args = parser.parse_args()

    document = args.document.read_text(encoding="utf-8")
    adapters = []
    if args.evidence:
        raw = json.loads(args.evidence.read_text(encoding="utf-8"))
        rows = raw.get("evidence", []) if isinstance(raw, dict) else raw
        adapters.append(StaticEvidenceAdapter([Evidence.from_dict(item) for item in rows]))
    citations = json.loads(args.citations.read_text(encoding="utf-8")) if args.citations else None
    pipeline = AuditPipeline(adapters)
    audit = pipeline.run(document, citations=citations)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "audit.json").write_text(pipeline.report_builder.to_json(audit) + "\n", encoding="utf-8")
    (args.output_dir / "audit.md").write_text(pipeline.report_builder.to_markdown(audit), encoding="utf-8")
    print(args.output_dir / "audit.json")
    print(args.output_dir / "audit.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
