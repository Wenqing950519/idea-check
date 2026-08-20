# Academic Search Upgrade Audit

Date: 2026-08-20
Baseline: `main` at the pre-upgrade working tree
Scope: Phase 0 architecture audit required by `ACADEMIC_SEARCH_SKILL_UPGRADE_SPEC.md`

## Executive finding

The current skill is a deterministic, conservative whitepaper claim-auditing pipeline. Its strongest reusable assets are the explicit `extract -> atomize -> plan -> retrieve -> judge -> verdict -> citation audit -> report` stages, passage-level evidence contract, counter-search planning, false-support detection, and injected adapter boundaries. It is not yet a general academic research system: it has no canonical research database, source/evidence/action ledgers, academic discovery provider, cross-document hybrid retrieval, research profiles, review modes, or integrity reconciliation between reported claims and executed actions.

The upgrade should therefore wrap and preserve the legacy audit pipeline while adding a new research evidence backbone beside it. The legacy six-label verdict model must remain available for compatibility, but the new research claim contract must use only `SUPPORTED`, `PARTIAL`, `CONTRADICTED`, and `UNRESOLVED`.

## Current architecture

| Layer | Current implementation | Inputs | Outputs | Determinism / boundary |
|---|---|---|---|---|
| Skill orchestration | `SKILL.md` | User document and audit intent | Stage-by-stage audit instructions | Provider-neutral; no runtime state |
| Claim extraction | `src/claim_extractor.py` | Markdown/plain text | Candidate `Claim` objects | Regex and line-number based |
| Claim atomization | `src/claim_atomizer.py` | Parent claim | Parent/child dependency graph | Deterministic conjunction splitting |
| Verification planning | `src/verification_planner.py` | Atomic claim | Balanced support, direct-source, contradiction, boundary, and causal-alternative tasks | Deterministic; explicitly avoids proof-seeking framing |
| Retrieval loop | `src/evidence_retriever.py` | Search tasks and adapters | Deduplicated passage evidence | Adapter injection; query/passage dedupe |
| Entailment judgment | `src/entailment_judge.py` | Claim and passage | Evidence relation and inference gap | Conservative causal and missing-passage gates |
| Verdict | `src/verdict_engine.py` | Claim and judged evidence | Legacy six-state `Verdict` | Conservative quality, contradiction, scope, and causal gates |
| Citation audit | `src/citation_auditor.py` | Claims, evidence, verdicts, citation map | False-support, missing/unused citation, and concentration findings | Deterministic |
| Reporting | `src/report_builder.py` | Complete audit object | JSON and Markdown evidence matrix | Deterministic |
| CLI | `scripts/audit_document.py` | Document, optional evidence and citations | `audit.json`, `audit.md` | Offline-capable |
| Contracts | `src/models.py`, `schemas/*.schema.json` | Serialized claims/evidence/verdicts | Python dataclasses and JSON Schema | Four legacy schemas |
| Optional integrations | `adapters/*.py` | Injected callables or optional packages | Normalized passage-level evidence | Graceful `AdapterUnavailableError` boundary |

## Existing adapters and dependency boundaries

| Adapter | Status | Dependency boundary | Upgrade decision |
|---|---|---|---|
| `StaticEvidenceAdapter` | Implemented | None | Preserve for fixtures and offline evaluation |
| `LocalDocumentAdapter` | Implemented | None | Preserve, then route indexed local content through the new canonical store |
| `WebSearchAdapter` | Implemented injection boundary | Host-provided callable | Preserve as generic fallback; never treat snippets without locators as evidence |
| `ScholarlyAdapter` | Implemented injection boundary | Host-provided callable | Preserve for compatibility; supersede discovery with typed academic providers |
| `PaperQAAdapter` | Optional | Separately installed `paperqa` plus injected runner | Preserve and expand as an optional full-text/RAG adapter; do not fork PaperQA |
| `GrobidAdapter` | Optional | Injected parser/service | Preserve as optional PDF-to-TEI boundary |
| `LLMJsonAdapter` | Implemented injection boundary | Host-provided completion callable | Preserve; use only behind deterministic contracts and validation |

The current runtime itself uses only the Python standard library. Schema validation uses `jsonschema` as a development dependency. PaperQA and GROBID are optional and fail closed when unavailable. No API key loading or provider configuration is currently implemented.

## Data contracts

### Contracts to preserve

- Legacy `Claim`, `Evidence`, `SearchTask`, `VerificationPlan`, `EntailmentJudgment`, and `Verdict` dataclasses.
- Passage-level evidence fields: source identity, stable locator, exact passage, relation, quality, retrieval query, causal/scope/boundary flags, and retrieval timestamp.
- Existing JSON schemas and five safety fixtures as compatibility assets.

### Contracts to add

- Canonical `Source` and `Document` records with normalized DOI, title, authors, year, provider IDs, access state, and provenance.
- Research `Evidence` records with immutable source/document linkage, passage locator, polarity, retrieval lineage, and integrity state.
- Research `Claim` records with the strict four-state status vocabulary only.
- `Hypothesis` records that remain explicitly distinct from verified literature claims.
- `AnalysisArtifact` records that distinguish planned from actually executed analysis.
- `ActionRecord` entries for search, fetch, parse, index, retrieve, citation verification, analysis, and review events.
- Graph edges connecting sources, documents, claims, evidence, hypotheses, and analyses.

## Current test and fixture baseline

- `python -m unittest discover -s tests -v`: **14 tests passed** on 2026-08-20.
- Five JSON fixtures cover direct verification, causal overreach, citation laundering, contradiction/boundary conditions, and original local hypothesis handling.
- Existing tests protect atomization, passage requirements, contradiction search, causal/scope gates, duplicate retrieval suppression, false-support auditing, full stage execution, schemas, and hypothesis labeling.

These tests must remain green after the rename. New tests must not silently rewrite the legacy expected labels; they should exercise the new research contracts separately.

## Gap analysis against the upgrade specification

| Required capability | Baseline state | Upgrade requirement |
|---|---|---|
| Product identity `academic-search` | Missing | Rename directory, skill metadata, prompts, docs, and root catalog |
| Persistent evidence backbone | Missing | Add SQLite canonical store and exportable manifests/ledgers |
| Academic discovery | Missing | Implement at least one real provider (OpenAlex) with normalized results and dedupe |
| Local-first retrieval | Partial | Index local evidence and search it before external providers |
| Hybrid retrieval | Missing | Combine lexical, lightweight semantic, metadata, and graph signals with provenance |
| Full-text acquisition/parsing | Optional parser boundary only | Add local ingestion path and explicit unavailable states; keep PaperQA/GROBID optional |
| Source manifest | Missing | Persist and export source inventory |
| Evidence ledger | Audit report only | Persist evidence with exact passage and locator |
| Action ledger | Missing | Log actual actions and reconcile completion claims against the ledger |
| Strict four-state research claims | Missing | Add new contract without breaking legacy six-label audit output |
| Counterevidence | Search task exists | Persist as first-class evidence polarity and require it in evaluations |
| Research profiles | Missing | Add `geo-whitepaper` and `olist-business-analysis` policies and workflows |
| Review modes | Missing | Add quick/evidence/citation/logic/code/reproducibility/full modes |
| Natural-language entry | Skill instructions only | Add intent routing plus a power-user CLI |
| Reproducibility truthfulness | Partial | Require execution action and artifact before claiming reproducibility |
| Writing downstream | Audit report only | Add fact-lock and claim-diff interfaces; do not let prose overwrite evidence state |

## Preserve, adapt, replace

### Preserve unchanged where possible

- Conservative evidence policy: relevance is not entailment.
- The full legacy whitepaper audit pipeline and its fixtures.
- Counter-search planning and causal/scope safety gates.
- Citation auditing, especially false-support accounting.
- Injected provider and LLM boundaries with graceful unavailable errors.
- JSON/Markdown deterministic reporting.

### Adapt behind new interfaces

- Route local documents and accepted external records into the canonical store.
- Translate legacy verdicts into the new four-state research claim view only at a documented compatibility boundary.
- Reuse citation audit findings as integrity events in the action/evidence ledgers.
- Expand PaperQA and GROBID through adapters rather than direct vendoring or forking.
- Keep old schemas for compatibility and add new schema files for the research contracts.

### Add as new modules

- Typed contracts and JSON schemas for sources, documents, research evidence, research claims, hypotheses, analyses, and actions.
- SQLite store, migrations/initialization, FTS-backed lexical search, graph edges, and ledger exports.
- Academic provider protocol, OpenAlex implementation, normalization, dedupe, and fallback router.
- Hybrid retrieval coordinator and ranked result explanation.
- Research workflow coordinator enforcing local-first and evidence-before-prose behavior.
- Profile policies, review modes, integrity reconciliation, fact lock, and claim diff.
- Offline provider fixtures and end-to-end evaluations.

## Migration risks and controls

1. **Verdict vocabulary conflict.** The legacy audit has six labels while the new research contract permits four. Control: keep legacy models isolated and expose an explicit, tested mapping at the compatibility boundary.
2. **False completion claims.** A report could imply that search, parsing, analysis, or review happened when only planned. Control: action-ledger reconciliation must fail closed.
3. **Metadata mistaken for evidence.** Academic APIs often return titles and abstracts, not exact full-text support. Control: source discovery and evidence acceptance remain separate states.
4. **Dependency inflation.** Full vector databases and autonomous-agent frameworks would increase fragility. Control: SQLite plus standard-library implementations first; optional adapters advertise capability and availability.
5. **Network nondeterminism.** Live academic APIs cannot be the only test path. Control: recorded provider payload fixtures and injectable transports.
6. **Rename regression.** Imports and legacy commands may break. Control: preserve package layout inside the renamed directory, update metadata atomically, and run all baseline tests.
7. **Licensing drift.** New upstream inspiration may have changed since the prior audit. Control: re-read current upstream repositories, record commit SHAs/licenses/paths, and prohibit direct code adaptation without confirmed compatible licensing.

## Phase 1 implementation order

1. Re-audit the specification's current upstream repositories and licenses.
2. Rename the skill and update product metadata without changing behavior.
3. Add and validate contracts, fixtures, SQLite store, and action-ledger integrity rules.
4. Add academic provider interfaces and an actual OpenAlex implementation with offline fixtures.
5. Add hybrid local retrieval and exact-locator evidence outputs.
6. Add profile and review policies, then research workflow orchestration.
7. Connect optional LLM, PaperQA, GROBID, and other providers only through adapters.
8. Run baseline, schema, integration, and end-to-end evaluations before publishing.

This audit authorizes no architecture fork and no upstream code copying. It establishes the compatibility boundary and the evidence-first implementation sequence for the upgrade.
