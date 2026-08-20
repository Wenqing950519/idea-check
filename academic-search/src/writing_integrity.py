from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from .contracts import ResearchClaim, to_dict


@dataclass(slots=True)
class ClaimChange:
    claim_id: str
    field: str
    before: object
    after: object


class FactLock:
    """Immutable snapshot used to keep writing edits downstream from evidence state."""

    def __init__(self, claims: list[ResearchClaim]) -> None:
        self.snapshot = {claim.claim_id: to_dict(claim) for claim in claims}
        self.digest = self._digest(self.snapshot)

    def verify(self, claims: list[ResearchClaim]) -> bool:
        return self.digest == self._digest({claim.claim_id: to_dict(claim) for claim in claims})

    @staticmethod
    def _digest(data: dict[str, object]) -> str:
        return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def claim_diff(before: list[ResearchClaim], after: list[ResearchClaim]) -> list[ClaimChange]:
    left = {claim.claim_id: to_dict(claim) for claim in before}
    right = {claim.claim_id: to_dict(claim) for claim in after}
    changes: list[ClaimChange] = []
    for claim_id in sorted(set(left) | set(right)):
        if claim_id not in left:
            changes.append(ClaimChange(claim_id, "claim", None, right[claim_id]))
            continue
        if claim_id not in right:
            changes.append(ClaimChange(claim_id, "claim", left[claim_id], None))
            continue
        for field in ("text", "status", "evidence_ids", "counterevidence_ids", "hypothesis_id"):
            if left[claim_id][field] != right[claim_id][field]:
                changes.append(ClaimChange(claim_id, field, left[claim_id][field], right[claim_id][field]))
    return changes
