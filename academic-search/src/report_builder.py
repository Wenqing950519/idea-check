from __future__ import annotations

import json
from collections import Counter
from typing import Any

from .models import Claim, Evidence, Verdict


class ReportBuilder:
    def build_audit(
        self,
        claims: list[Claim],
        evidence: list[Evidence],
        verdicts: list[Verdict],
        citation_audit: dict[str, Any],
    ) -> dict[str, Any]:
        counts = Counter(item.verdict.value for item in verdicts)
        for label in ("VERIFIED", "SUPPORTED", "QUALIFIED", "UNVERIFIED", "CONTRADICTED", "ORIGINAL_HYPOTHESIS"):
            counts.setdefault(label, 0)
        high_risk = [item.claim_id for item in verdicts if item.human_review_required]
        queue = [
            {
                "claim_id": item.claim_id,
                "question": self._review_question(item),
                "recommended_action": item.recommended_action,
            }
            for item in verdicts if item.human_review_required
        ]
        return {
            "summary": {
                "total_claims": len(claims),
                "verification_required_claims": sum(1 for item in claims if item.verification_required),
                "verdict_counts": dict(counts),
                "high_risk_claims": high_risk,
            },
            "claims": [item.to_dict() for item in claims],
            "evidence": [item.to_dict() for item in evidence],
            "verdicts": [item.to_dict() for item in verdicts],
            "citation_audit": citation_audit,
            "human_review_queue": queue,
        }

    def to_json(self, audit: dict[str, Any]) -> str:
        return json.dumps(audit, ensure_ascii=False, indent=2)

    def to_markdown(self, audit: dict[str, Any]) -> str:
        summary = audit["summary"]
        claims = {item["claim_id"]: item for item in audit["claims"]}
        evidence = {item["evidence_id"]: item for item in audit["evidence"]}
        lines = [
            "# Executive Audit Summary",
            "",
            f"- Total claims: {summary['total_claims']}",
            f"- Verification-required claims: {summary['verification_required_claims']}",
        ]
        for label, count in summary["verdict_counts"].items():
            lines.append(f"- {label}: {count}")
        lines.extend(["", "# Evidence Matrix", "", "| Claim ID | Original claim | Verdict | Evidence | Relation | Quality | Problem | Recommendation |", "|---|---|---|---|---|---|---|---|"])
        for verdict in audit["verdicts"]:
            claim = claims[verdict["claim_id"]]
            evs = [evidence[eid] for eid in verdict["evidence_ids"] if eid in evidence]
            ev_names = "; ".join(item["source_title"] for item in evs) or "None"
            relations = "; ".join(item["relation"] for item in evs) or "—"
            qualities = "; ".join(item["source_quality"] for item in evs) or "—"
            problem = " ".join(verdict["inference_gaps"]) or "—"
            row = [verdict["claim_id"], claim["original_text"], verdict["verdict"], ev_names, relations, qualities, problem, verdict["recommended_action"]]
            lines.append("| " + " | ".join(self._cell(value) for value in row) + " |")

        lines.extend(["", "# High-Risk Claim Detail Cards", ""])
        for verdict in audit["verdicts"]:
            if not verdict["human_review_required"]:
                continue
            claim = claims[verdict["claim_id"]]
            lines.extend([
                f"## {verdict['claim_id']}", "",
                f"Original claim: {claim['original_text']}", "",
                f"Verdict: {verdict['verdict']}", "",
                f"Why: {verdict['reason']}", "",
                "Inference gap: " + (" ".join(verdict["inference_gaps"]) or "None recorded."), "",
                f"Recommended action: {verdict['recommended_action']}", "",
            ])
        lines.extend(["# Human Review Queue", ""])
        for item in audit["human_review_queue"]:
            lines.append(f"- {item['claim_id']}: {item['question']}")
        lines.extend(["", "# Citation Integrity Audit", "", f"- False support count: {audit['citation_audit']['false_support_count']}", f"- Uncited supported claims: {', '.join(audit['citation_audit']['uncited_claim_ids']) or 'None'}", f"- Unused evidence: {', '.join(audit['citation_audit']['unused_evidence_ids']) or 'None'}"])
        return "\n".join(lines) + "\n"

    @staticmethod
    def _cell(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    @staticmethod
    def _review_question(verdict: Verdict) -> str:
        if "CAUSAL_EVIDENCE_MISMATCH" in verdict.risk_flags:
            return "Does the theory turn correlation into causation, and what design could identify the causal effect?"
        if "BOUNDARY_CONDITION" in verdict.risk_flags:
            return "Which population, timeframe, definition, or system is actually supported?"
        if verdict.verdict.value == "ORIGINAL_HYPOTHESIS":
            return "Should this be labeled as the author's hypothesis and tested with an original sample or dataset?"
        return "What direct evidence or wording change is needed before this can be stated objectively?"
