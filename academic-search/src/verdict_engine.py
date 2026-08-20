from __future__ import annotations

from .models import Claim, ClaimType, Evidence, EvidenceRelation, SourceQuality, Verdict, VerdictLabel


class VerdictEngine:
    """Return the most conservative verdict justified by passage-level evidence."""

    def decide(self, claim: Claim, evidence: list[Evidence], contradiction_search_completed: bool = False) -> Verdict:
        relevant = [item for item in evidence if item.claim_id == claim.claim_id]
        direct = [item for item in relevant if item.relation == EvidenceRelation.DIRECT_SUPPORT and item.source_quality in {SourceQuality.A, SourceQuality.B}]
        partial = [item for item in relevant if item.relation == EvidenceRelation.PARTIAL_SUPPORT]
        contradictions = [item for item in relevant if item.relation == EvidenceRelation.CONTRADICTS and item.source_quality in {SourceQuality.A, SourceQuality.B}]
        qualifications = [item for item in relevant if item.relation == EvidenceRelation.QUALIFIES or item.boundary_condition]
        ids = [item.evidence_id for item in relevant]
        flags = list(dict.fromkeys(claim.risk_flags))
        gaps: list[str] = []

        if claim.claim_type == ClaimType.ORIGINAL_HYPOTHESIS and not direct:
            return self._verdict(claim, VerdictLabel.ORIGINAL_HYPOTHESIS, ids, ["No representative external evidence directly answers this local research claim."], "Retain explicitly as an author hypothesis and test it with a documented sample or dataset.", flags, True)

        if contradictions:
            if direct and qualifications:
                flags.append("BOUNDARY_CONDITION")
                return self._verdict(claim, VerdictLabel.QUALIFIED, ids, ["Support and contradiction apply under different populations, definitions, or conditions."], "Narrow the claim to the supported boundary conditions and cite both sides.", flags, True)
            return self._verdict(claim, VerdictLabel.CONTRADICTED, ids, ["High-quality evidence directly contradicts the claim."], "Remove, reverse, or materially rewrite the claim after human review.", flags, True)

        if claim.claim_type == ClaimType.CAUSAL:
            causal_direct = [item for item in direct if item.causal_design]
            if not causal_direct:
                flags.extend(["CAUSAL_EVIDENCE_MISMATCH", "INFERENCE_GAP"])
                gaps.append("Available evidence does not establish the causal step asserted by the claim.")
                return self._verdict(claim, VerdictLabel.UNVERIFIED, ids, gaps, "Weaken to association language or obtain causal evidence.", flags, True)
            direct = causal_direct

        strength_sensitive = {
            ClaimType.CAUSAL,
            ClaimType.COMPARATIVE,
            ClaimType.QUANTITATIVE,
            ClaimType.PREDICTIVE,
            ClaimType.GENERALIZATION,
        }
        if direct and claim.author_assertion_level == "strong" and claim.claim_type in strength_sensitive:
            if not any(item.scope_match for item in direct):
                flags.extend(["SCOPE_EVIDENCE_MISMATCH", "INFERENCE_GAP"])
                return self._verdict(
                    claim,
                    VerdictLabel.UNVERIFIED,
                    ids,
                    ["Evidence scope does not match the claim's population, timeframe, metric, or universality."],
                    "Narrow the wording or obtain evidence whose scope matches the strong claim.",
                    flags,
                    True,
                )

        if direct and not qualifications:
            if not contradiction_search_completed:
                flags.append("CONTRADICTION_SEARCH_MISSING")
                return self._verdict(claim, VerdictLabel.SUPPORTED, ids, ["Direct support exists, but the required contradiction search is incomplete."], "Complete contradiction and boundary searches before using VERIFIED.", flags, True)
            return self._verdict(claim, VerdictLabel.VERIFIED, ids, [], "Keep the claim with the direct passage citation and its scope intact.", flags, False)
        if direct and qualifications:
            flags.append("BOUNDARY_CONDITION")
            return self._verdict(claim, VerdictLabel.QUALIFIED, ids, ["Direct support is limited by stated boundary conditions."], "State the supported population, timeframe, definition, and system.", flags, True)
        if len(partial) >= 2:
            return self._verdict(claim, VerdictLabel.SUPPORTED, ids, ["Evidence is convergent but indirect or observational."], "Use calibrated language such as 'is associated with' or 'evidence suggests'.", flags, False)

        flags.append("INFERENCE_GAP")
        gaps.append("No high-quality passage directly entails the atomic claim.")
        return self._verdict(claim, VerdictLabel.UNVERIFIED, ids, gaps, "Find direct evidence, weaken the wording, or label the statement as a hypothesis.", flags, True)

    @staticmethod
    def _verdict(claim: Claim, label: VerdictLabel, ids: list[str], gaps: list[str], action: str, flags: list[str], review: bool) -> Verdict:
        reasons = {
            VerdictLabel.VERIFIED: "At least one high-quality passage directly entails the claim with no unresolved high-quality contradiction.",
            VerdictLabel.SUPPORTED: "Multiple sources point in the same direction, but direct proof is absent.",
            VerdictLabel.QUALIFIED: "The claim is supportable only within explicit boundary conditions.",
            VerdictLabel.UNVERIFIED: "Current evidence is insufficient for the claim's wording and strength.",
            VerdictLabel.CONTRADICTED: "High-quality evidence materially contradicts the claim.",
            VerdictLabel.ORIGINAL_HYPOTHESIS: "The claim is a plausible author hypothesis that external literature does not directly establish.",
        }
        return Verdict(claim.claim_id, label, reasons[label], ids, gaps, action, review, list(dict.fromkeys(flags)))
