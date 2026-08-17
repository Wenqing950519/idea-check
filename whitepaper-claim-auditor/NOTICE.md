# Notices and Open-Source Reuse

Source audit date: 2026-08-14

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

## OPTIONAL_EXTERNAL_DEPENDENCY

- PaperQA (`Future-House/paper-qa`, commit inspected: `57e89f7223b0960d5ee5ea048c69e3c47e088572`, Apache-2.0): may be called by an adapter only when separately installed.
- GROBID (`grobidOrg/grobid`, commit inspected: `0148dea637cfe4acb364a9d2ef22aca82d9b5035`, Apache-2.0): may be called as an external service to produce TEI XML.
- GROBID Python client (`grobidOrg/grobid-client-python`, commit inspected: `a9792d851f89e4dfd7ab8e9c9360fdfe4870246f`, Apache-2.0): may be used when separately installed; it is not vendored.

See `references/OPEN_SOURCE_REFERENCES.md` for exact source paths and borrowed concepts, and `references/LICENSE_AUDIT.md` for license evidence and restrictions.
