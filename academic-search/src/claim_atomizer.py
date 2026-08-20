from __future__ import annotations

import re
from dataclasses import replace

from .claim_extractor import ClaimExtractor
from .models import AtomizationResult, Claim


class ClaimAtomizer:
    """Create explicit child claims without discarding parent provenance."""

    _splitter = re.compile(r"\s*(?:；|;|而且|並且|以及|\band\b)\s*", re.I)

    def atomize(self, claim: Claim) -> AtomizationResult:
        parts = [part.strip(" ，,") for part in self._splitter.split(claim.atomic_claim) if part.strip(" ，,")]
        if len(parts) <= 1:
            return AtomizationResult(parent=claim, children=[])
        children: list[Claim] = []
        child_ids: list[str] = []
        for index, part in enumerate(parts):
            child_id = f"{claim.claim_id}-{chr(65 + index)}"
            child_ids.append(child_id)
            claim_type = ClaimExtractor.classify(part)
            children.append(Claim(
                claim_id=child_id,
                parent_id=claim.claim_id,
                source_location=claim.source_location,
                original_text=claim.original_text,
                atomic_claim=part,
                claim_type=claim_type,
                verification_required=True,
                dependencies=[],
                author_assertion_level=claim.author_assertion_level,
                risk_flags=ClaimExtractor.risk_flags(part, claim_type),
            ))
        return AtomizationResult(parent=replace(claim, dependencies=child_ids), children=children)
