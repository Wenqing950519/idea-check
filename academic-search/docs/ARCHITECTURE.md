# Architecture

## System boundary

`academic-search` is a research evidence engine, not a general autonomous research agent and not a writing UI. Natural-language intent selects a bounded workflow. Evidence is persisted before conclusions or prose are produced.

```text
Natural-language request
        |
Profile + workflow routing
        |
Local SQLite KB -- insufficient --> DiscoveryRouter --> OpenAlex / optional providers
        |                                  |
        +-------------- screening + normalized Source records
                                           |
Local/optional full-text parsing --> Document index
                                           |
Hybrid retrieval (FTS + semantic + metadata + graph)
                                           |
Evidence + counterevidence --> strict Claim status
                                           |
Review + action-ledger integrity --> report/export
```

## Canonical modules

- `src/contracts.py`: new research contracts and strict status enums.
- `src/store.py`: SQLite source of truth, FTS index, edges, and exports.
- `providers/base.py`: provider capability and fallback router.
- `providers/openalex.py`: implemented live OpenAlex API provider with injected offline transport.
- `src/hybrid_retrieval.py`: deterministic multi-signal retrieval with score explanation.
- `src/research_engine.py`: local-first coordinator and evidence acceptance.
- `src/integrity.py`: guards claims about actions actually completed.
- `src/review.py`: calibrated review modes and overclaim checks.
- `src/profiles.py`: GEO and Olist workflow policy.
- `src/fulltext.py`: local parsers and optional PDF boundary.

The existing `src/pipeline.py` and legacy models remain intact for whitepaper-audit compatibility. Translation between legacy six-label verdicts and new four-state claims is deliberately not implicit.

## Dependency policy

Core runtime is Python standard library plus SQLite. Optional systems are injected through adapters. Missing providers do not disable local ingestion, retrieval, claim management, review, or export.

No upstream source code is vendored. See `references/OPEN_SOURCE_REFERENCES.md` and `references/LICENSE_AUDIT.md`.
