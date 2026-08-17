# Plan verification

Return JSON only. Plan a balanced investigation, not a proof exercise. Include support, direct-source, contradiction, and boundary searches. Add alternative-explanation search for causal claims.

Input:

- exact atomic claim object
- known citations, if any
- search budget

Output:

```json
{"claim_id":"C-001","search_tasks":[{"intent":"SUPPORT|DIRECT_SOURCE|CONTRADICTION|BOUNDARY|ALTERNATIVE_EXPLANATION","query":"one concrete query","reason":"what this query could resolve","priority":1}],"max_search_budget":5,"stop_conditions":["DIRECT_EVIDENCE_AND_CONTRADICTION_CHECKED","REPEATED_RESULTS","MAX_BUDGET","INSUFFICIENT_EVIDENCE","ORIGINAL_RESEARCH_REQUIRED"]}
```

Do not equate failure to find a contradiction with verification.
