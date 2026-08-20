# Research Workflows

## Discovery and screening

1. Frame query, years, evidence standard, inclusion/exclusion criteria, and profile.
2. Search local indexed documents.
3. If local coverage is below the configured threshold, query the discovery router.
4. Normalize and merge DOI duplicates; retain preprint and retraction state.
5. Persist candidate sources as metadata-only until full text is actually acquired.
6. Screen titles/abstracts, then acquire lawful full text for included items.

## Evidence retrieval and claims

1. Retrieve exact passages with lexical, lightweight semantic, metadata, and graph signals.
2. Accept passages into the evidence ledger only with source/document identity and locator.
3. Run support and contradiction queries separately.
4. Judge polarity; context-only results cannot support claims.
5. Update the strict four-state claim and send causal, disputed, or unresolved claims to human review.

## Review and report

Choose the smallest applicable review mode. Reconcile statements about completed work with the action ledger. Generate source manifest, evidence ledger, claim table, hypotheses, limitations, and unresolved decisions before narrative prose.

## Legacy whitepaper migration

The former `extract -> atomize -> plan -> retrieve -> judge -> verdict -> citation audit -> report` command remains available. For new projects, store final research claims in the new four-state contract. Do not silently reinterpret a legacy `VERIFIED`, `QUALIFIED`, `UNVERIFIED`, or `ORIGINAL_HYPOTHESIS` label; preserve the legacy output and create a separately justified new research claim.

## Power-user workflow

Use `scripts/academic_search.py` for database initialization, ingestion, local search, discovery, and exports. Natural-language users do not need to know these commands; the skill routes their request to the same deterministic interfaces.

## Add a profile

1. Add an immutable `ResearchProfile` entry in `src/profiles.py` with preferred sources, required steps, and optional coaching questions.
2. Keep evidence and claim contracts unchanged; a profile changes policy, not truth labels.
3. Add a dedicated profile document covering scope, evidence hierarchy, failure modes, and human decisions.
4. Add tests for routing, required steps, graceful provider fallback, counterevidence, and at least one end-to-end scenario.
5. Update `SKILL.md` and the profile selection choices in the CLI only after the profile is implemented.
