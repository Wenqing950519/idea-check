# Open Source References

Audit date: 2026-08-14

This file records the source material actually inspected before implementation. Commit SHAs are immutable audit anchors, not statements that later upstream changes were reviewed. No upstream implementation code was copied into this skill.

## Usage categories

- `DIRECT_CODE_ADAPTATION`: copied or modified upstream implementation. None at this audit.
- `ARCHITECTURAL_INSPIRATION`: behavior, data model, evaluation idea, or interface learned from source without copying implementation.
- `OPTIONAL_EXTERNAL_DEPENDENCY`: invoked through an adapter when separately installed or deployed; no vendoring.

## Audited sources

| Repository | Commit SHA | Source file/path read | Borrowed concept | License | Usage |
|---|---|---|---|---|---|
| [shmsw25/FActScore](https://github.com/shmsw25/FActScore) | `f28272deffcf33efc1f1117d5479c10bb75221a9` | `factscore/atomic_facts.py`; `factscore/factscorer.py` | Preserve sentence-to-atomic-fact structure; treat decomposition as a first-class stage rather than scoring a whole document at once. | MIT | `ARCHITECTURAL_INSPIRATION` |
| [google-deepmind/long-form-factuality](https://github.com/google-deepmind/long-form-factuality) | `9d27158d198ced0a9d8271a80147cae580614601` | `third_party/factscore/atomic_facts.py`; `eval/safe/get_atomic_facts.py`; `eval/safe/rate_atomic_fact.py`; `eval/safe/search_augmented_factuality_eval.py` | Cross-check sentence-scoped atomic facts, self-contained reformulation, relevance classification, and search-augmented rating boundaries. | MIT for `third_party/factscore/*`; Apache-2.0 for `eval/*` | `ARCHITECTURAL_INSPIRATION` |
| [mbzuai-nlp/ProgramFC](https://github.com/mbzuai-nlp/ProgramFC) | `5957016c1556dc5a2a6ea92c7b1ab68d289f8911` | `models/program_generator.py`; `models/program_execution.py`; `models/prompts.py`; `models/retriever.py`; `models/question_answering.py` | Represent complex verification as explicit dependent operations; keep program generation, retrieval, QA, and execution separable. | MIT | `ARCHITECTURAL_INSPIRATION` |
| [mbzuai-nlp/fire](https://github.com/mbzuai-nlp/fire) | `cd7cb4af8dab00b1ab4bd78197a52e052203873d` | `eval/fire/verify_atomic_claim.py`; `eval/fire/query_serper.py`; `eval/fire/config.py`; root tree | Iterate search and judgment; retain query/search history; detect repeated queries/results; stop or reformulate when evidence remains insufficient. | No root license found at audited commit | `ARCHITECTURAL_INSPIRATION` |
| [Future-House/paper-qa](https://github.com/Future-House/paper-qa) | `57e89f7223b0960d5ee5ea048c69e3c47e088572` | `src/paperqa/agents/search.py`; `agents/tools.py`; `agents/main.py`; `prompts.py`; `docs.py`; `readers.py`; `settings.py` | Permit cannot-answer on insufficient context; bind generated statements to citation keys actually present in context; retain passage-level context and relevance/source metadata. | Apache-2.0 | `ARCHITECTURAL_INSPIRATION` |
| [Future-House/paper-qa](https://github.com/Future-House/paper-qa) | `57e89f7223b0960d5ee5ea048c69e3c47e088572` | Package boundary under `src/paperqa/` | Provide a disabled-by-default adapter boundary for a separately installed PaperQA package. | Apache-2.0 | `OPTIONAL_EXTERNAL_DEPENDENCY` |
| [AkariAsai/OpenScholar](https://github.com/AkariAsai/OpenScholar) | `0e9b8fb912273d3dae39e593da86e4f6d3bf8de1` | `retriever/README.md`; `retriever/api/passage_utils.py`; `retriever/api/serve_pes2o.py`; `retriever/src/search.py`; `src/open_scholar.py`; `src/use_search_apis.py` | Separate scholarly retrieval, passage assembly, reranking, and generation; support existing indexes/APIs instead of rebuilding the PES2O-scale datastore; deduplicate and preserve passage metadata. | Apache-2.0 | `ARCHITECTURAL_INSPIRATION` |
| [allenai/scifact](https://github.com/allenai/scifact) | `68b98a56d93e0f9da0d2aab4e6c3294699a0f72e` | `doc/data.md`; `verisci/` including retrieval, rationale-selection, label-prediction, merge, and evaluation modules | Keep claim, document, rationale sentences, and label distinct; make evidence rationale an auditable object rather than only returning a label. | Code: Apache-2.0; claims/evidence annotations: CC BY 4.0; abstracts: ODC-By 1.0 | `ARCHITECTURAL_INSPIRATION` |
| [SalesforceAIResearch/answer-engine-eval](https://github.com/SalesforceAIResearch/answer-engine-eval) | `c73639edfa1ca81b3da96a2dd4e4f33d1a64d651` | `Venkit.et.al.2024/Answer_Engine_Eval.ipynb` | Add a document-level citation audit after claim verdicts: unsupported statements, inaccurate citations, citation thoroughness, source necessity, and uncited sources. | Apache-2.0 | `ARCHITECTURAL_INSPIRATION` |
| [grobidOrg/grobid](https://github.com/grobidOrg/grobid) | `0148dea637cfe4acb364a9d2ef22aca82d9b5035` | `doc/Grobid-service.md`; `doc/TEI-encoding-of-results.md` | Treat structured TEI XML as an optional scholarly-PDF intermediate; use services such as `processHeaderDocument`, `processFulltextDocument`, and `processReferences` rather than building a PDF parser. | Apache-2.0 | `OPTIONAL_EXTERNAL_DEPENDENCY` |
| [grobidOrg/grobid-client-python](https://github.com/grobidOrg/grobid-client-python) | `a9792d851f89e4dfd7ab8e9c9360fdfe4870246f` | `grobid_client/client.py`; `grobid_client/grobid_client.py` | Define an optional HTTP/client adapter for GROBID service calls, timeouts, retries, and TEI output. | Apache-2.0 | `OPTIONAL_EXTERNAL_DEPENDENCY` |
| [stanford-oval/storm](https://github.com/stanford-oval/storm) | `fb951af7744dab086e34962e9bc6fe878e145f83` | `knowledge_storm/rm.py`; `knowledge_storm/interface.py`; `knowledge_storm/storm_wiki/modules/retriever.py`; `knowledge_curation.py`; `knowledge_storm/collaborative_storm/modules/grounded_question_answering.py`; `costorm_expert_utterance_generator.py` | Keep retrieval providers replaceable; preserve source information objects; use perspectives to broaden contradiction/boundary searches without adopting autonomous article generation. | MIT | `ARCHITECTURAL_INSPIRATION` |

## Implementation boundary

The local implementation must be original and deterministic at its core. Upstream names, control flow, prompts, and code are not to be copied. Any future direct adaptation requires a new row with the exact upstream path, commit, license, local derivative path, and retained notices before the adaptation is merged.
