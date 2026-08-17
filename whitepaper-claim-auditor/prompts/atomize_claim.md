# Atomize a claim

Return JSON only. Split the claim into self-contained propositions that can be verified independently. Preserve the parent. Create dependency edges when the conclusion requires multiple premises; do not treat adjacent background facts as proof of a causal or predictive conclusion.

Input:

- `claim`: one complete claim object

Output:

```json
{"parent":{},"children":[{"claim_id":"C-001-A","parent_id":"C-001","source_location":"...","original_text":"...","atomic_claim":"...","claim_type":"FACTUAL","verification_required":true,"dependencies":[],"author_assertion_level":"moderate","risk_flags":[],"notes":""}],"dependency_edges":[{"from":"C-001-A","to":"C-001","role":"required_premise"}]}
```

If the claim is already atomic, return an empty `children` array.
