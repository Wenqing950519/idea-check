from __future__ import annotations

from dataclasses import dataclass

from adapters.base import AdapterUnavailableError, RetrievalAdapter

from .models import Evidence, SearchTask, VerificationPlan


@dataclass
class RetrievalResult:
    evidence: list[Evidence]
    query_history: list[str]
    errors: list[str]
    stop_reason: str


@dataclass
class RetrievalState:
    evidence: list[Evidence]
    query_history: list[str]
    errors: list[str]
    fingerprints: set[tuple[str, str, str]]
    normalized_queries: set[str]
    duplicate_rounds: int = 0

    @classmethod
    def empty(cls) -> "RetrievalState":
        return cls([], [], [], set(), set(), 0)


class EvidenceRetriever:
    """Execute a bounded, deduplicated plan across replaceable adapters."""

    def __init__(self, adapters: list[RetrievalAdapter]) -> None:
        self.adapters = adapters

    def retrieve_next(self, task: SearchTask, state: RetrievalState) -> list[Evidence]:
        normalized = " ".join(task.query.casefold().split())
        if normalized in state.normalized_queries:
            state.duplicate_rounds += 1
            return []
        state.normalized_queries.add(normalized)
        state.query_history.append(task.query)
        added: list[Evidence] = []
        for adapter in self.adapters:
            try:
                results = adapter.search(task)
            except AdapterUnavailableError as exc:
                state.errors.append(f"{adapter.name}: {exc}")
                continue
            for item in results:
                fingerprint = self._fingerprint(item)
                if fingerprint in state.fingerprints:
                    continue
                state.fingerprints.add(fingerprint)
                state.evidence.append(item)
                added.append(item)
        state.duplicate_rounds = state.duplicate_rounds + 1 if not added else 0
        return added

    def retrieve(self, plan: VerificationPlan) -> RetrievalResult:
        state = RetrievalState.empty()
        attempts = 0
        for task in plan.tasks:
            attempts += 1
            self.retrieve_next(task, state)
            if attempts >= plan.max_search_budget:
                break
        stop_reason = "MAX_BUDGET" if attempts >= plan.max_search_budget else "PLAN_COMPLETE"
        if not state.evidence:
            stop_reason = "INSUFFICIENT_EVIDENCE"
        elif state.duplicate_rounds >= 2:
            stop_reason = "REPEATED_RESULTS"
        return RetrievalResult(state.evidence, state.query_history, state.errors, stop_reason)

    @staticmethod
    def _fingerprint(item: Evidence) -> tuple[str, str, str]:
        return (item.url_or_doi, item.document_locator, " ".join(item.passage.casefold().split()))
