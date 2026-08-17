# Judge claim-passage entailment

Return JSON only. Judge only the exact atomic claim against the exact passage and supplied document metadata. Do not use outside memory. Source quality and entailment are separate. A prestigious but merely related source is `CONTEXT_ONLY`.

Input must contain:

- `claim`: exact atomic claim object
- `evidence_passage`: verbatim passage
- `document_metadata`: title, author, organization/publisher, year, source type, URL/DOI, locator, retrieval query

Output:

```json
{"claim_id":"C-001","evidence_id":"E-001","relation":"DIRECT_SUPPORT|PARTIAL_SUPPORT|CONTEXT_ONLY|QUALIFIES|CONTRADICTS|IRRELEVANT|UNRESOLVED","source_quality":"A|B|C|D|E","reason":"passage-scoped reasoning","inference_gap":"what the passage does not establish","causal_design":false,"scope_match":false,"boundary_condition":false}
```

Use `UNRESOLVED` if the passage or locator is missing. Never infer causality from correlation. Never treat an abstract or snippet as supporting details it does not state.
