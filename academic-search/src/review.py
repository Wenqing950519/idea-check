from __future__ import annotations

import re
from dataclasses import dataclass

from .contracts import ActionRecord, ActionType, ResearchClaim, stable_id, utc_now
from .integrity import ActionLedgerGuard
from .store import ResearchStore


REVIEW_MODES = frozenset({"quick", "evidence", "citation", "logic", "code", "reproducibility", "full"})


@dataclass(slots=True)
class ReviewFinding:
    severity: str
    code: str
    claim_id: str
    message: str


class ReviewEngine:
    def __init__(self, store: ResearchStore) -> None:
        self.store = store
        self.guard = ActionLedgerGuard(store)

    def review(self, claims: list[ResearchClaim], mode: str = "full") -> list[ReviewFinding]:
        if mode not in REVIEW_MODES:
            raise ValueError(f"Unknown review mode: {mode}")
        findings: list[ReviewFinding] = []
        for claim in claims:
            if claim.status.value == "UNRESOLVED":
                findings.append(ReviewFinding("HIGH", "UNSUPPORTED_CLAIM", claim.claim_id, "Claim remains unresolved."))
            if re.search(r"\b(causes?|proves?|always|never)\b|導致|證明|必然", claim.text, re.I) and claim.status.value != "SUPPORTED":
                findings.append(ReviewFinding("HIGH", "POTENTIAL_OVERCLAIM", claim.claim_id, "Strong causal or universal wording exceeds the recorded evidence state."))
            if mode in {"reproducibility", "full"} and "reproduc" in claim.text.casefold():
                for item in self.guard.audit([("reproducible", claim.claim_id)]):
                    findings.append(ReviewFinding("HIGH", item.code, claim.claim_id, item.message))
        self.store.log_action(ActionRecord(
            action_id=stable_id("ACT", ActionType.REVIEW_EXECUTED.value, mode, len(claims), utc_now()),
            action_type=ActionType.REVIEW_EXECUTED, status="SUCCESS", detail={"mode": mode, "findings": len(findings)},
        ))
        return findings
