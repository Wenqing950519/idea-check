---
name: academic-search
description: Search, organize, verify, and review academic or research evidence with a persistent local evidence database. Use for literature discovery, evidence-grounded whitepapers, citation verification, claim and counterevidence audits, research reviews, reproducibility checks, GEO research, Olist business analysis, or migration from whitepaper-claim-auditor. Works in Codex and Claude Code; searches the local KB before external providers and never treats topical relevance as entailment.
---

# Academic Search

Research Evidence Engine for local-first discovery, passage-level evidence, conservative claim judgment, and integrity-aware reporting.

## Non-negotiable rule

Optimize for low False Support Rate, not citation count. A title, URL, abstract, search snippet, related passage, or model recollection is not direct support unless the recorded passage entails the claim at the stated scope.

Use `UNRESOLVED` when evidence is insufficient. Keep a novel explanation as a `Hypothesis`; never relabel it as an established literature claim.

## Route the request

Infer the smallest workflow that satisfies the user's natural-language request:

| User intent | Workflow |
|---|---|
| Find papers, build a reading list, map a field | Discovery and screening |
| Answer a research question from known documents | Local full-text retrieval, then external discovery only if needed |
| Check a whitepaper, report, or manuscript | Legacy claim audit plus research claim/evidence ledger |
| Verify citations or detect citation laundering | Evidence and citation review |
| Review research quality | One of `quick`, `evidence`, `citation`, `logic`, `code`, `reproducibility`, or `full` |
| GEO / generative search research | `geo-whitepaper` profile |
| Olist dataset or business analysis | `olist-business-analysis` profile; use coaching questions before causal interpretation |

If the research question, population, timeframe, or requested evidence standard would materially change the result, confirm it with the user. Otherwise proceed with explicit assumptions.

## Evidence-first workflow

Run these stages in order and persist each completed action:

1. **Frame** — state the question, scope, profile, inclusion criteria, and what would count as counterevidence.
2. **Search local KB** — query the canonical SQLite store before external discovery.
3. **Discover** — use OpenAlex when local coverage is insufficient. Use another provider only as an explicit adapter or documented fallback.
4. **Screen and deduplicate** — merge DOI duplicates, preserve preprint status, and distinguish metadata-only records from acquired full text.
5. **Acquire and parse** — accept local text, Markdown, HTML, CSV, or JSON. For PDF, require a configured PaperQA, GROBID, or injected parser; otherwise report unavailable.
6. **Retrieve** — combine lexical, lightweight semantic, metadata, and graph signals. Return exact passages with stable locators.
7. **Judge** — classify evidence polarity as `SUPPORT`, `PARTIAL`, `CONTRADICT`, or `CONTEXT`. Search for counterevidence explicitly.
8. **Update claims** — use only `SUPPORTED`, `PARTIAL`, `CONTRADICTED`, or `UNRESOLVED` for the new research claim contract.
9. **Review integrity** — reconcile every statement such as “searched,” “parsed,” “verified,” “executed,” “reviewed,” or “reproducible” with a successful action-ledger event.
10. **Report** — generate prose only from accepted evidence state. Include limitations, counterevidence, unresolved items, and human-review decisions.

Do not claim that an external search ran if the provider was unavailable. Do not claim that code is reproducible unless it was actually executed and its output locator was recorded.

## Persistence contracts

The SQLite store is canonical. Persist:

- `Source`: normalized identity, DOI/provider IDs, authors, year, publication/preprint status, OA metadata, and citation graph IDs.
- `Document`: content hash, source link, MIME type, and stable locator.
- `ResearchEvidence`: exact passage, locator, polarity, query, score, source quality, and claim link.
- `ResearchClaim`: strict four-state status, supporting evidence IDs, counterevidence IDs, rationale, and review flag.
- `Hypothesis`: explicitly open explanation, separate from verified claims.
- `AnalysisArtifact`: planned/executed/failed state and input/output locators.
- `ActionRecord`: actual search, fetch, parse, index, retrieve, citation, analysis, and review events.

JSONL and Markdown files are export views, not competing sources of truth.

## Profiles

### geo-whitepaper

Combine peer-reviewed papers and preprints with official documentation and first-party evidence. Treat vendor claims as claims, not proof. Search for boundary conditions and evidence that structured data, ranking, retrieval, or citation-selection effects do not generalize. Run citation audit before final prose.

Read [PROFILE_GEO_WHITEPAPER.md](docs/PROFILE_GEO_WHITEPAPER.md) when this profile is selected.

### olist-business-analysis

Start from dataset identity, data dictionary, time coverage, unit of analysis, missingness, and leakage. Separate descriptive, predictive, and causal questions. Ask the coaching questions in [PROFILE_OLIST_BUSINESS_ANALYSIS.md](docs/PROFILE_OLIST_BUSINESS_ANALYSIS.md) before choosing an analysis. Never call an analysis reproducible until its execution action and artifact are recorded.

## Review modes

- `quick`: unresolved headline claims and obvious overclaiming.
- `evidence`: passage entailment, scope, source fitness, and counterevidence.
- `citation`: existence, locator accuracy, citation-to-claim mapping, unused sources, and false support.
- `logic`: causal, mechanism, generalization, novelty, and internal-consistency claims.
- `code`: paper-code claim mapping, dependencies, paths, and output provenance.
- `reproducibility`: actual execution, environment, input/output artifacts, and rerun status.
- `full`: all applicable modes; still report calibrated findings rather than a blanket correctness certificate.

## Optional integrations

- **PaperQA2**: optional full-text index/evidence engine via adapter. Convert results into local evidence records; never accept its generated answer as the final conclusion.
- **GROBID**: optional PDF-to-TEI parser service.
- **PyAlex**: optional alternative OpenAlex client; the built-in provider uses standard-library HTTP.
- **Zotero / Better BibTeX**: optional human-facing citation library and BibTeX export.
- **Firecrawl**: optional official-web fetch/scrape provider. Respect website policies and preserve source URL/locator.
- **LLM**: optional structured judgment helper behind validated interfaces. Deterministic safety gates remain authoritative.

Missing optional dependencies must produce an actionable unavailable state and leave local workflows working.

## Power-user commands

```text
python scripts/academic_search.py --db research/research.db init
python scripts/academic_search.py --db research/research.db ingest path/to/document.md
python scripts/academic_search.py --db research/research.db search "citation selection"
python scripts/academic_search.py --db research/research.db discover "LLM citation selection" --year-from 2025 --year-to 2026
python scripts/academic_search.py --db research/research.db export
```

Set `OPENALEX_API_KEY` for live OpenAlex discovery. Without it, local search remains available and the provider reports `UNAVAILABLE`.

The former deterministic whitepaper workflow remains available through `python scripts/audit_document.py ...` and retains its six legacy output labels. That compatibility output is not the new four-state research claim contract.

## Output requirements

Lead with the evidence state, not fluent prose. Include:

1. Research question, scope, and profile.
2. Actions actually completed and provider failures.
3. Source manifest with metadata/full-text acquisition state.
4. Evidence ledger with exact locator and polarity.
5. Claim table with strict status and counterevidence.
6. Hypotheses kept separate from established claims.
7. Review/integrity findings.
8. Limitations, unresolved questions, and decisions requiring human review.

Never say “the literature proves” when the accepted evidence is partial, scope-mismatched, metadata-only, or merely related.

## Further documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Evidence model](docs/EVIDENCE_MODEL.md)
- [Providers](docs/PROVIDERS.md)
- [Research workflows](docs/RESEARCH_WORKFLOWS.md)
- [Review and integrity](docs/REVIEW_AND_INTEGRITY.md)
- [Upgrade audit](docs/ACADEMIC_SEARCH_UPGRADE_AUDIT.md)
- [Open-source references](references/OPEN_SOURCE_REFERENCES.md)
- [License audit](references/LICENSE_AUDIT.md)
