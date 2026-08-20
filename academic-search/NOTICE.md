# Notices and Open-Source Reuse

Source audit dates: 2026-08-14 and 2026-08-20

## DIRECT_CODE_ADAPTATION

None. This version contains no copied or modified upstream implementation code.

## ARCHITECTURAL_INSPIRATION

- FActScore (`shmsw25/FActScore`, `f28272deffcf33efc1f1117d5479c10bb75221a9`, MIT): atomic fact decomposition and sentence-to-atom provenance.
- Long-form Factuality / SAFE (`google-deepmind/long-form-factuality`, `9d27158d198ced0a9d8271a80147cae580614601`, Apache-2.0 for `eval/*`, MIT for vendored `third_party/factscore/*`): self-contained facts and search-augmented rating boundaries.
- ProgramFC (`mbzuai-nlp/ProgramFC`, `5957016c1556dc5a2a6ea92c7b1ab68d289f8911`, MIT): explicit dependent verification programs.
- FIRE (`mbzuai-nlp/fire`, `cd7cb4af8dab00b1ab4bd78197a52e052203873d`, no root license found): iterative retrieve/judge/search behavior and repetition stopping. No code copied.
- PaperQA (`Future-House/paper-qa`, `57e89f7223b0960d5ee5ea048c69e3c47e088572`, Apache-2.0): passage-grounded evidence, citation-key constraints, and abstention on insufficient context.
- OpenScholar (`AkariAsai/OpenScholar`, `0e9b8fb912273d3dae39e593da86e4f6d3bf8de1`, Apache-2.0): scholarly retrieval/generation separation, passage reranking, and existing-index integration.
- SciFact (`allenai/scifact`, `68b98a56d93e0f9da0d2aab4e6c3294699a0f72e`; code Apache-2.0, annotations CC BY 4.0, abstracts ODC-By 1.0): claim/rationale/label separation. No data copied.
- Answer Engine Evaluation / DeepTRACE (`SalesforceAIResearch/answer-engine-eval`, `c73639edfa1ca81b3da96a2dd4e4f33d1a64d651`, Apache-2.0): unsupported-statement, citation-accuracy, thoroughness, source-necessity, and uncited-source audit concepts.
- STORM / Co-STORM (`stanford-oval/storm`, `fb951af7744dab086e34962e9bc6fe878e145f83`, MIT): replaceable retrievers and perspective coverage. Autonomous article generation is not adopted.
- Academic Research Skills and its Codex distribution (`Imbad0202`, commits `7ef93e0cb52b93f9909e163aad912255d4471850` and `d5e66fb0d9e4a5bc44f26e9a619fa0e4455ba79c`, CC BY-NC 4.0): intent routing, integrity, reproducibility, and domain-profile concepts only. No text or code copied.
- Scientific Agent Skills (`K-Dense-AI/scientific-agent-skills`, `390f5146bf3c1877cf15636a3dd7b775e4f0f185`, MIT): provider registry and source/evidence ledger concepts.
- AI Research Feedback (`claesbackman/AI-research-feedback`, `d39b192304121836cd2587a625fa7b7c0ed11963`, MIT): calibrated review modes and overclaim checks.
- Claude Skills (`lcrawfurd/claude-skills`, `1d76ecca95b691d1aac05b81741bdde64cc91f50`, no license found): reproducibility review concepts only; no content copied.
- Anything-to-Journal (`howardtuan/Anything-to-Journal`, `a80a08cd89bc9e9393f9fe197a523898405dc81b`, MIT): recoverable source manifest and writing-integrity boundaries.
- Harness Starter Kit (`agentcrew-academy/harness-starter-kit`, `8c0765a30bf11a66bdae46447f0fa79322aef222`, MIT): evidence/action-ledger guard philosophy only; claim-guard scripts were not copied.
- PyAlex (`J535D165/pyalex`, `875c708cbb6e449feebc46d2a7a26af8ed8b2fdd`, MIT): OpenAlex client interface concepts; local HTTP implementation is independent.

## OPTIONAL_EXTERNAL_DEPENDENCY

- PaperQA (`Future-House/paper-qa`, commit inspected: `57e89f7223b0960d5ee5ea048c69e3c47e088572`, Apache-2.0): may be called by an adapter only when separately installed.
- GROBID (`grobidOrg/grobid`, commit inspected: `0148dea637cfe4acb364a9d2ef22aca82d9b5035`, Apache-2.0): may be called as an external service to produce TEI XML.
- GROBID Python client (`grobidOrg/grobid-client-python`, commit inspected: `a9792d851f89e4dfd7ab8e9c9360fdfe4870246f`, Apache-2.0): may be used when separately installed; it is not vendored.
- PyAlex (`J535D165/pyalex`, commit inspected: `875c708cbb6e449feebc46d2a7a26af8ed8b2fdd`, MIT): may replace the built-in OpenAlex HTTP provider if separately installed.
- Zotero Better BibTeX (`retorquere/zotero-better-bibtex`, commit inspected: `1dbec988112ab55d646eb0e486b6a805b8f9f480`, MIT): optional citation-library integration only.
- Firecrawl (`firecrawl/firecrawl`, commit inspected: `c76f4fd20044b4d60e289559bb029422ae1e6540`; server AGPL-3.0, Python SDK MIT): optional webpage provider only; nothing is vendored.

See `references/OPEN_SOURCE_REFERENCES.md` for exact source paths and borrowed concepts, and `references/LICENSE_AUDIT.md` for license evidence and restrictions.
