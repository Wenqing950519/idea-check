# Extract claims

Return JSON only. Extract every independently verifiable factual premise, including premises embedded in normative or interpretive conclusions. Do not turn opinions into facts. Preserve exact source text and location.

Input:

- `document_text`: the complete Markdown or text document

Output:

```json
{"claims":[{"claim_id":"C-001","parent_id":null,"source_location":"section-or-line","original_text":"exact source sentence","atomic_claim":"single candidate claim","claim_type":"FACTUAL|CAUSAL|COMPARATIVE|DEFINITIONAL|QUANTITATIVE|PREDICTIVE|GENERALIZATION|METHODOLOGICAL|INTERPRETIVE|NORMATIVE|ORIGINAL_HYPOTHESIS","verification_required":true,"dependencies":[],"author_assertion_level":"weak|moderate|strong","risk_flags":[],"notes":""}]}
```

Never omit a risky claim merely because it lacks a citation. Never strengthen the author's language.
