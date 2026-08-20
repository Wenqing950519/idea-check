# Evidence Model

## Canonical records

| Record | Purpose | Integrity rule |
|---|---|---|
| Source | Normalized scholarly, official, local, or dataset identity | DOI is normalized; metadata-only is not full text |
| Document | Parsed/indexed content linked to a source | Content hash deduplicates identical text; locator is required |
| ResearchEvidence | Exact passage linked to a document and optional claim | Passage and stable locator are mandatory |
| ResearchClaim | Auditable proposition | Status is exactly `SUPPORTED`, `PARTIAL`, `CONTRADICTED`, or `UNRESOLVED` |
| Hypothesis | Proposed explanation or original idea | Never becomes support merely by being linked to a claim |
| AnalysisArtifact | Planned or executed computational work | `EXECUTED` requires an actual run and output provenance |
| ActionRecord | Append-only account of work actually performed | Completion assertions reconcile against successful actions |

## Evidence polarity

- `SUPPORT`: the passage entails the claim at the recorded scope.
- `PARTIAL`: only a subclaim or qualified form is supported.
- `CONTRADICT`: the passage supplies counterevidence.
- `CONTEXT`: relevant background without entailment.

Metadata, abstracts, and snippets may help discovery but do not automatically become high-confidence evidence. A claim with support and counterevidence is `PARTIAL`, not silently promoted to `SUPPORTED`.

## Storage and exports

SQLite is canonical. `sources`, `documents`, `evidence`, `claims`, `hypotheses`, `analyses`, `actions`, and `edges` are persistent tables. FTS5 is used when available; deterministic fallback remains possible.

JSONL source/action exports and `EVIDENCE_LEDGER.md` are generated views. Editing an export does not update the canonical database.

Legacy `Claim`, `Evidence`, and `Verdict` schemas remain for the former claim-audit CLI and are explicitly marked as legacy IDs.
