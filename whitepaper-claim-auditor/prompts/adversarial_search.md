# Generate adversarial searches

Return JSON only. Seek evidence that could falsify, narrow, or explain away the exact atomic claim. For causal claims, search for confounding, reverse causality, null results, and incompatible designs. For generalizations, vary population, geography, timeframe, and definition.

Output:

```json
{"claim_id":"C-001","queries":[{"intent":"CONTRADICTION|BOUNDARY|ALTERNATIVE_EXPLANATION","query":"...","target_gap":"..."}]}
```

Do not search for generic criticism. Each query must target a specific inference step.
