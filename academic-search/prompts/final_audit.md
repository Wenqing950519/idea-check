# Audit citation integrity

Return JSON only. Run after all claim verdicts. Compare every in-text citation with the claim it appears to support and the stored passage-level evidence.

Output:

```json
{"accuracy_issues":[{"claim_id":"C-001","evidence_id":"E-001","issue":"FALSE_SUPPORT_CONTEXT_ONLY|FALSE_SUPPORT_IRRELEVANT|MISSING_EVIDENCE_OBJECT|CROSS_CLAIM_CITATION","explanation":"..."}],"uncited_claim_ids":[],"unused_evidence_ids":[],"citation_concentration":{"source":"use-count"},"false_support_count":0,"human_review_questions":[]}
```

Count `CONTEXT_ONLY` or `IRRELEVANT` citations used as support as false support. Prioritize lowering false support over increasing citation count.
