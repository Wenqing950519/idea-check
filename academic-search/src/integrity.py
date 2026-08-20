from __future__ import annotations

from dataclasses import dataclass

from .contracts import ActionType
from .store import ResearchStore


class IntegrityError(RuntimeError):
    pass


@dataclass(slots=True)
class IntegrityFinding:
    code: str
    message: str
    target_id: str | None = None


class ActionLedgerGuard:
    REQUIRED_ACTIONS = {
        "searched": ActionType.SEARCH_EXECUTED,
        "fetched": ActionType.SOURCE_FETCHED,
        "parsed": ActionType.FULLTEXT_PARSED,
        "indexed": ActionType.SOURCE_INDEXED,
        "retrieved": ActionType.EVIDENCE_RETRIEVED,
        "citation_verified": ActionType.CITATION_VERIFIED,
        "analyzed": ActionType.ANALYSIS_EXECUTED,
        "reviewed": ActionType.REVIEW_EXECUTED,
        "reproducible": ActionType.ANALYSIS_EXECUTED,
    }

    def __init__(self, store: ResearchStore) -> None:
        self.store = store

    def require(self, assertion: str, target_id: str | None = None) -> None:
        try:
            action_type = self.REQUIRED_ACTIONS[assertion]
        except KeyError as exc:
            raise ValueError(f"Unknown integrity assertion: {assertion}") from exc
        if not self.store.successful_actions(action_type, target_id):
            raise IntegrityError(
                f"Cannot claim '{assertion}': no successful {action_type.value} action exists"
                + (f" for {target_id}." if target_id else ".")
            )

    def audit(self, assertions: list[tuple[str, str | None]]) -> list[IntegrityFinding]:
        findings: list[IntegrityFinding] = []
        for assertion, target_id in assertions:
            try:
                self.require(assertion, target_id)
            except IntegrityError as exc:
                findings.append(IntegrityFinding("ACTION_LEDGER_MISMATCH", str(exc), target_id))
        return findings
