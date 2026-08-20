# Providers

Provider status is stated literally; planned capability is not represented as implemented.

| Provider | Status | Capability | Authentication / fallback |
|---|---|---|---|
| Local SQLite/FTS | Implemented | Ingest, lexical/semantic/metadata/graph retrieval | Always available; local-first |
| OpenAlex HTTP | Implemented | Work search, metadata, DOI, authors, year, OA status, references, citation count | `OPENALEX_API_KEY`; offline fixture transport for tests; unavailable state without key |
| Generic web search | Implemented adapter | Host-injected passage results | Optional; rejects result without passage and locator |
| Generic scholarly search | Implemented adapter | Host-injected scholarly results | Optional |
| PaperQA2 | Optional external dependency | Full-text indexing, passage search, evidence gathering, evidence-backed Q&A, contradiction search | Separately install `paperqa` and inject an integration runner |
| GROBID | Optional external dependency | PDF-to-TEI parsing | Inject service/client parser |
| PyAlex | Optional external dependency | Alternative OpenAlex client | Not required by built-in provider |
| Zotero / Better BibTeX | Optional external dependency | Human citation library and stable keys | Research remains functional without it |
| Firecrawl | Optional external dependency | Official webpage search/scrape | No vendoring; respect site policies |
| arXiv | Planned adapter | Preprint discovery | Not implemented in this release |
| Crossref | Planned adapter | DOI and bibliographic verification | Not implemented in this release |
| Semantic Scholar | Planned adapter | Secondary verification, references/citations, recommendation | Not implemented in this release |
| OA resolver / Unpaywall | Planned adapter | Lawful full-text location | Not implemented in this release; never bypass paywalls |

## Add a provider

1. Implement `DiscoveryProvider.search(DiscoveryQuery) -> list[Source]`.
2. Declare accurate capability flags and `available()` behavior.
3. Normalize DOI, title, authors, year, publication/preprint state, URLs, and provider ID.
4. Use an injectable transport so tests do not require live network access.
5. Raise at the provider boundary; `DiscoveryRouter` records failure and tries the next provider.
6. Add normalization, dedupe, failure, and rate/authentication tests.
7. Update this matrix and the source/license audit.

OpenAlex official documentation read for this release states that API keys are required. The provider therefore fails explicitly rather than pretending a live search occurred.
