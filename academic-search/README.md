# Academic Search

**Research Evidence Engine** for Codex and Claude Code.

Academic Search keeps scholarly discovery, local full text, exact-locator evidence, claims, hypotheses, analyses, and executed actions in one local SQLite evidence backbone. It searches local material first, uses OpenAlex only when needed, and preserves the former Whitepaper Claim Auditor as a compatibility workflow.

The governing quality rule is: **False Support Rate > Citation Count**. Related material is not automatically support; insufficient evidence remains `UNRESOLVED`.

## Install

Copy or symlink this directory into your agent's skills directory as `academic-search`. The folder includes Codex metadata in `agents/openai.yaml` and portable instructions in `SKILL.md`.

Runtime requirements are Python 3.11+ and SQLite. The core has no third-party runtime dependency. Live OpenAlex discovery requires `OPENALEX_API_KEY`. PaperQA, GROBID, PyAlex, Zotero Better BibTeX, Firecrawl, and LLM calls are optional adapters.

## Quick start

```powershell
python scripts/academic_search.py --db research/research.db init
python scripts/academic_search.py --db research/research.db ingest .\notes.md
python scripts/academic_search.py --db research/research.db search "citation selection"
python scripts/academic_search.py --db research/research.db discover "LLM citation selection" --year-from 2025 --year-to 2026
python scripts/academic_search.py --db research/research.db export
```

Legacy claim audit:

```powershell
python scripts/audit_document.py report.md --output-dir audit-output
```

## Verify

```powershell
python -m unittest discover -s tests -v
uv run --with jsonschema python scripts/validate_schemas.py
```

See [SKILL.md](SKILL.md), [architecture](docs/ARCHITECTURE.md), [providers](docs/PROVIDERS.md), and the [upgrade audit](docs/ACADEMIC_SEARCH_UPGRADE_AUDIT.md).
