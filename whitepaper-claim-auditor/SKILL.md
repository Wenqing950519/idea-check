---
name: whitepaper-claim-auditor
description: Audit completed or in-progress whitepapers, research reports, papers, and Markdown/text chapters by extracting factual and inferential claims, atomizing dependencies, retrieving passage-level evidence, judging claim-source entailment, assigning conservative six-state verdicts, and checking citation integrity. Use when Codex or Claude Code needs to fact-check claims, detect causal overreach or citation laundering, distinguish external support from an author's original hypothesis, build an evidence matrix, or produce a human-review queue. Prioritize low False Support Rate over citation count.
---

# Whitepaper Claim Auditor

Audit what the author actually claims and how far the evidence truly reaches. Preserve `UNVERIFIED` and `ORIGINAL_HYPOTHESIS`; never turn a related source into proof.

## Load the method

Read [references/METHOD_NOTES.md](references/METHOD_NOTES.md) before auditing. Read [references/OPEN_SOURCE_REFERENCES.md](references/OPEN_SOURCE_REFERENCES.md), [references/LICENSE_AUDIT.md](references/LICENSE_AUDIT.md), and [NOTICE.md](NOTICE.md) before modifying implementation or reusing upstream material.

## Run the workflow

Execute this sequence without skipping entailment or the final citation audit:

`extract → atomize → plan → retrieve → judge → verdict → citation audit → report`

1. Extract claims from the complete document. Preserve exact sentence text and location. Extract factual premises embedded in normative conclusions, but do not fact-check the normative conclusion itself.
2. Atomize compound claims. Keep the parent and create explicit dependency edges. Do not allow verified background premises to imply an unverified causal or predictive conclusion.
3. Plan balanced searches. Include support, primary/direct source, contradiction, and boundary searches. Include alternative explanations for every causal claim.
4. Retrieve passages. Prefer primary research, official documentation, standards, government data, and first-party datasets. Store the exact passage, locator, query, and document metadata. Reject URL-only evidence.
5. Judge each exact atomic claim against each exact passage. Keep source quality separate from entailment. Use `CONTEXT_ONLY` for topic-adjacent evidence and `UNRESOLVED` when required context is missing.
6. Assign one verdict: `VERIFIED`, `SUPPORTED`, `QUALIFIED`, `UNVERIFIED`, `CONTRADICTED`, or `ORIGINAL_HYPOTHESIS`. Match evidence strength to causal, universal, quantitative, and predictive language.
7. Audit citations at document level. Flag inaccurate, missing, decorative, unused, and over-concentrated citations. Count context-only citations presented as support as false support.
8. Produce JSON plus Markdown: executive summary, evidence matrix, high-risk claim cards, and a focused human-review queue.

## Use deterministic components

Use schemas in `schemas/` as the data contract. Use modules in `src/` stage by stage or run:

```bash
python scripts/audit_document.py path/to/document.md --output-dir audit-output
```

Supply reviewed/manual passage evidence when available:

```bash
python scripts/audit_document.py document.md --evidence evidence.json --citations citations.json --output-dir audit-output
```

Treat the no-provider result as a safe baseline: factual claims remain `UNVERIFIED`, and explicitly local/testable research claims may remain `ORIGINAL_HYPOTHESIS`.

## Use LLM and retrieval adapters

Use prompts in `prompts/` for semantic stages and require JSON-only responses. Validate every response before passing it forward. For entailment, always provide the exact claim, exact passage, and full document metadata; never provide only a URL or abstract and ask the model to infer the rest.

Inject host search into `WebSearchAdapter` or `ScholarlyAdapter`. Use `LocalDocumentAdapter` for local corpora. Enable PaperQA or GROBID only when separately installed/configured; never vendor them or make them mandatory. Keep the implementation host-neutral so the same folder works under Codex or Claude Code; `agents/openai.yaml` is optional Codex UI metadata and does not affect the workflow.

## Enforce safety gates

- Never search with “prove the author's hypothesis” as the objective.
- Never upgrade a claim because no contradiction was found.
- Never verify causality from correlation or topical similarity.
- Never use another AI-generated summary as final evidence.
- Never hide an inference gap by adding more context-only citations.
- Never rewrite the author's theory into a different theory and call the audit complete.
- Stop at the MVP boundary: do not build a UI, autonomous article writer, custom scholarly index, fact-checking model, or PDF parser.

## Verify changes

Run all deterministic tests and the Skill validator after edits:

```bash
python -m unittest discover -s tests -v
uv run --with jsonschema python scripts/validate_schemas.py
python path/to/skill-creator/scripts/quick_validate.py .
```

Keep the five fixtures covering direct verification, citation laundering, original local hypothesis, contradiction with boundaries, and causal overreach passing.
