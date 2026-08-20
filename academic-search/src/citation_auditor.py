from __future__ import annotations

from collections import Counter
from typing import Any

from .models import Claim, Evidence, EvidenceRelation, Verdict, VerdictLabel


class CitationAuditor:
    """Audit claim-citation relationships after claim verification."""

    _invalid_support = {
        EvidenceRelation.CONTEXT_ONLY,
        EvidenceRelation.IRRELEVANT,
        EvidenceRelation.UNRESOLVED,
        EvidenceRelation.CONTRADICTS,
    }

    def audit(
        self,
        claims: list[Claim],
        evidence: list[Evidence],
        verdicts: list[Verdict],
        citations: dict[str, list[str]] | None = None,
    ) -> dict[str, Any]:
        citations = citations or {}
        evidence_by_id = {item.evidence_id: item for item in evidence}
        verdict_by_claim = {item.claim_id: item for item in verdicts}
        accuracy_issues: list[dict[str, str]] = []
        used: set[str] = set()
        source_counts: Counter[str] = Counter()

        for claim_id, evidence_ids in citations.items():
            for evidence_id in evidence_ids:
                used.add(evidence_id)
                item = evidence_by_id.get(evidence_id)
                if item is None:
                    accuracy_issues.append({"claim_id": claim_id, "evidence_id": evidence_id, "issue": "MISSING_EVIDENCE_OBJECT"})
                    continue
                source_counts[item.url_or_doi] += 1
                if item.claim_id != claim_id:
                    accuracy_issues.append({"claim_id": claim_id, "evidence_id": evidence_id, "issue": "CROSS_CLAIM_CITATION"})
                elif item.relation in self._invalid_support:
                    accuracy_issues.append({"claim_id": claim_id, "evidence_id": evidence_id, "issue": f"FALSE_SUPPORT_{item.relation.value}"})

        citable_verdicts = {VerdictLabel.VERIFIED, VerdictLabel.SUPPORTED, VerdictLabel.QUALIFIED}
        uncited = [
            claim.claim_id for claim in claims
            if claim.verification_required
            and verdict_by_claim.get(claim.claim_id)
            and verdict_by_claim[claim.claim_id].verdict in citable_verdicts
            and not citations.get(claim.claim_id)
        ]
        unused = [item.evidence_id for item in evidence if item.evidence_id not in used]
        total_uses = sum(source_counts.values())
        concentrated = {
            source: count for source, count in source_counts.items()
            if total_uses >= 3 and count / total_uses > 0.5
        }
        return {
            "accuracy_issues": accuracy_issues,
            "uncited_claim_ids": uncited,
            "unused_evidence_ids": unused,
            "citation_concentration": concentrated,
            "false_support_count": sum(1 for item in accuracy_issues if item["issue"].startswith("FALSE_SUPPORT_")),
        }
