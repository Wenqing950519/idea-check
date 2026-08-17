# License Audit

Audit date: 2026-08-14

## Decision summary

No upstream code is directly adapted in this version. All implementation will be written independently from the specification and the behavior-level findings in `OPEN_SOURCE_REFERENCES.md`. PaperQA and GROBID integrations are optional adapters only.

| Repository | Commit SHA | License evidence inspected | Audit result | Allowed use in this skill |
|---|---|---|---|---|
| `shmsw25/FActScore` | `f28272deffcf33efc1f1117d5479c10bb75221a9` | Root `LICENSE` | MIT | Architectural inspiration. Direct adaptation would require copyright and permission notice retention, but none is used. |
| `google-deepmind/long-form-factuality` | `9d27158d198ced0a9d8271a80147cae580614601` | Root `LICENSE`; `third_party/factscore/LICENSE` | File-scoped: MIT for `third_party/factscore/*`; Apache-2.0 for `common/*`, `data_creation/*`, `eval/*`, `longfact/*`, `main/*` | Architectural inspiration only. Preserve file-scope distinction if future adaptation occurs. |
| `mbzuai-nlp/ProgramFC` | `5957016c1556dc5a2a6ea92c7b1ab68d289f8911` | Root `LICENSE` | MIT | Architectural inspiration. No copied program parser, prompt, or execution code. |
| `mbzuai-nlp/fire` | `cd7cb4af8dab00b1ab4bd78197a52e052203873d` | Root tree and repository files | **No root license found** | Architectural inspiration only. Direct copying or modification is prohibited unless a valid license is later confirmed. |
| `Future-House/paper-qa` | `57e89f7223b0960d5ee5ea048c69e3c47e088572` | Root `LICENSE` | Apache-2.0 | Architectural inspiration and optional external dependency. No vendoring. |
| `AkariAsai/OpenScholar` | `0e9b8fb912273d3dae39e593da86e4f6d3bf8de1` | Root `LICENSE` | Apache-2.0 | Architectural inspiration only. No model, index, datastore, or source code vendored. |
| `allenai/scifact` | `68b98a56d93e0f9da0d2aab4e6c3294699a0f72e` | Root `LICENSE.md` | Code: Apache-2.0; claims/evidence annotations: CC BY 4.0; abstracts: ODC-By 1.0 | Schema philosophy only. No dataset records, annotations, abstracts, or code copied. Test fixtures are newly authored. |
| `SalesforceAIResearch/answer-engine-eval` | `c73639edfa1ca81b3da96a2dd4e4f33d1a64d651` | Root `LICENSE` | Apache-2.0 | Metric concepts only. Notebook code and benchmark data are not copied. |
| `grobidOrg/grobid` | `0148dea637cfe4acb364a9d2ef22aca82d9b5035` | Root `LICENSE` | Apache-2.0 | Optional external service. No server code or models vendored. |
| `grobidOrg/grobid-client-python` | `a9792d851f89e4dfd7ab8e9c9360fdfe4870246f` | Root `LICENSE` | Apache-2.0 | Optional external package/service reference. Local adapter will use an independently written minimal protocol. |
| `stanford-oval/storm` | `fb951af7744dab086e34962e9bc6fe878e145f83` | Root `LICENSE` | MIT | Architectural inspiration only. No retriever implementations or prompts copied. |

## Compliance rules

1. Treat repository licenses as commit-specific evidence; re-audit before changing the pinned commit or adding a new path.
2. Do not infer a license from a paper, package metadata, organization, or neighboring repository.
3. Do not copy code from FIRE at the audited commit.
4. Do not copy SciFact data records into fixtures; its code and data have different licenses.
5. Keep optional dependencies optional and fail with an actionable unavailable status rather than silently installing or vendoring them.
6. Record any future direct adaptation in both `NOTICE.md` and `OPEN_SOURCE_REFERENCES.md` before release.

This audit records repository evidence and implementation policy; it is not legal advice.
