# Method Notes

## Non-negotiable rules

1. Optimize for low False Support Rate, not citation volume.
2. Preserve `UNVERIFIED` and `ORIGINAL_HYPOTHESIS` as valid outcomes.
3. Store exact passages and locators; a URL alone is not evidence.
4. Separate source quality from claim-passage entailment.
5. Search for contradiction and boundaries even after finding support.
6. Never use another AI-generated summary as final evidence.

## Pipeline contract

`extract → atomize → plan → retrieve → judge → verdict → citation audit → report`

Each stage must accept and return serializable objects. Keep adapters replaceable. Never let retrieval silently decide entailment, or let source reputation silently decide relation.

## Search policy

Run, within budget:

1. Initial support search.
2. Direct primary/official source search.
3. Contradiction/null-result search.
4. Boundary-condition search.
5. Alternative-explanation search for causal claims.

Stop when direct evidence exists and contradiction search is complete, results or queries repeat, the budget is exhausted, evidence clearly remains insufficient, or original research is required. Absence of contradiction is not positive evidence.

## Evidence relations

- `DIRECT_SUPPORT`: the passage entails the claim at its stated strength.
- `PARTIAL_SUPPORT`: the passage supports only part or a weaker version.
- `CONTEXT_ONLY`: same topic or mechanism, but not the asserted proposition.
- `QUALIFIES`: support only under explicit limits.
- `CONTRADICTS`: the passage is incompatible with the claim.
- `IRRELEVANT`: no material bearing on the claim.
- `UNRESOLVED`: missing passage/metadata or genuinely ambiguous relation.

Never cite `CONTEXT_ONLY`, `IRRELEVANT`, or `UNRESOLVED` as support.

## Source quality

- A: primary peer-reviewed research, official standard/documentation/statistics, first-party dataset.
- B: systematic review, transparent institute or industry research.
- C: reputable professional media, company whitepaper, technical research article.
- D: secondary blog or general synthesis.
- E: anonymous, forum, content farm, or unverifiable source.

A-level quality cannot upgrade a context-only passage.

## Verdict gates

- `VERIFIED`: high-quality direct entailment, strength matched, contradiction check complete.
- `SUPPORTED`: multiple convergent but indirect/observational sources.
- `QUALIFIED`: support is conditional on definition, population, system, or timeframe.
- `UNVERIFIED`: direct evidence is absent or the reasoning chain has a gap.
- `CONTRADICTED`: high-quality evidence materially refutes the claim.
- `ORIGINAL_HYPOTHESIS`: external literature does not directly answer a testable author claim.

For causal claims, require a design capable of causal identification. Correlation cannot verify “causes,” “directly increases,” or equivalent language.

## Citation audit

Check accuracy, completeness, unsupported objective statements, decorative/unused citations, and concentration on one secondary source. Report false-support incidents explicitly. Do not repair them by attaching additional context-only citations.
