# Review and Integrity

## Modes

`quick`, `evidence`, `citation`, `logic`, `code`, `reproducibility`, and `full` are separate modes. Use the smallest mode that answers the request; `full` does not constitute a correctness certificate.

## Claim discipline

Review unresolved headline claims, causal wording, mechanism-as-fact, generalization beyond sample/time/population, unsupported priority/novelty, missing counterevidence, and citation-to-claim mismatch. A citation that is merely topical counts toward false support, not citation success.

## Action-ledger reconciliation

| Assertion | Required event |
|---|---|
| searched | `SEARCH_EXECUTED` |
| fetched | `SOURCE_FETCHED` |
| parsed | `FULLTEXT_PARSED` |
| indexed | `SOURCE_INDEXED` |
| retrieved | `EVIDENCE_RETRIEVED` |
| citation verified | `CITATION_VERIFIED` |
| analyzed / reproducible | `ANALYSIS_EXECUTED` |
| reviewed | `REVIEW_EXECUTED` |

Missing events produce `ACTION_LEDGER_MISMATCH`. Provider failure is recorded; it is never rewritten as a completed search.

## Fact lock and claim diff

Treat accepted claim status, evidence IDs, counterevidence IDs, exact locators, and analysis execution state as locked facts. A writing pass may improve prose but must not change these values. Before publishing a revised report, compare extracted claims and their evidence links to the locked state; surface additions, deletions, stronger wording, and citation changes for review.
