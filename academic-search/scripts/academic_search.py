#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from providers import DiscoveryRouter, OpenAlexProvider
from src.research_engine import ResearchEngine
from src.store import ResearchStore


def main() -> int:
    parser = argparse.ArgumentParser(description="Academic Search research evidence engine")
    parser.add_argument("--db", type=Path, default=Path("research/research.db"), help="Canonical SQLite database")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="Initialize the research database")
    ingest = sub.add_parser("ingest", help="Parse and index a local document")
    ingest.add_argument("path", type=Path)
    ingest.add_argument("--title")
    search = sub.add_parser("search", help="Search the local evidence database")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)
    discover = sub.add_parser("discover", help="Search local KB first, then OpenAlex if needed")
    discover.add_argument("query")
    discover.add_argument("--limit", type=int, default=10)
    discover.add_argument("--year-from", type=int)
    discover.add_argument("--year-to", type=int)
    discover.add_argument("--profile", choices=["geo-whitepaper", "olist-business-analysis"], default="geo-whitepaper")
    export = sub.add_parser("export", help="Export source, evidence, and action ledgers")
    export.add_argument("--output-dir", type=Path, default=Path("research/exports"))

    args = parser.parse_args()
    with ResearchStore(args.db) as store:
        engine = ResearchEngine(store, DiscoveryRouter([OpenAlexProvider()]))
        if args.command == "init":
            payload = {"database": str(args.db), "fts_available": store.fts_available}
        elif args.command == "ingest":
            source, document = engine.ingest_file(args.path, args.title)
            payload = {"source_id": source.source_id, "document_id": document.document_id, "locator": document.locator}
        elif args.command == "search":
            payload = {"query": args.query, "hits": [asdict(hit) for hit in engine.retriever.search(args.query, args.limit)]}
        elif args.command == "discover":
            result = engine.discover(args.query, args.limit, args.year_from, args.year_to, args.profile)
            payload = {
                "query": result["query"], "profile": result["profile"],
                "local_hits": [asdict(hit) for hit in result["local_hits"]],
                "external_sources": [asdict(source) for source in result["external_sources"]],
                "provider_failures": result["provider_failures"],
            }
        else:
            args.output_dir.mkdir(parents=True, exist_ok=True)
            exports = {
                table: str(store.export_jsonl(table, args.output_dir / f"{table}.jsonl"))
                for table in ("sources", "evidence", "claims", "hypotheses", "analyses", "actions")
            }
            exports["evidence_markdown"] = str(store.export_markdown_ledger(args.output_dir / "EVIDENCE_LEDGER.md"))
            payload = exports
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
