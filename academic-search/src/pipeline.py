from __future__ import annotations

from dataclasses import replace
from typing import Any

from adapters.base import RetrievalAdapter

from .citation_auditor import CitationAuditor
from .claim_atomizer import ClaimAtomizer
from .claim_extractor import ClaimExtractor
from .entailment_judge import EntailmentJudge
from .evidence_retriever import EvidenceRetriever, RetrievalState
from .models import Claim, Evidence, SearchIntent
from .report_builder import ReportBuilder
from .verification_planner import VerificationPlanner
from .verdict_engine import VerdictEngine


class AuditPipeline:
    """Orchestrate extract → atomize → plan → retrieve → judge → verdict → audit → report."""

    def __init__(self, adapters: list[RetrievalAdapter] | None = None) -> None:
        self.extractor = ClaimExtractor()
        self.atomizer = ClaimAtomizer()
        self.planner = VerificationPlanner()
        self.retriever = EvidenceRetriever(adapters or [])
        self.judge = EntailmentJudge()
        self.verdict_engine = VerdictEngine()
        self.citation_auditor = CitationAuditor()
        self.report_builder = ReportBuilder()

    def prepare_claims(self, document: str) -> list[Claim]:
        prepared: list[Claim] = []
        for claim in self.extractor.extract(document):
            result = self.atomizer.atomize(claim)
            if result.children:
                prepared.append(replace(result.parent, verification_required=False, notes="Structural parent; decide from dependency verdicts."))
                prepared.extend(result.children)
            else:
                prepared.append(result.parent)
        return prepared

    def run(self, document: str, citations: dict[str, list[str]] | None = None) -> dict[str, Any]:
        claims = self.prepare_claims(document)
        all_evidence: list[Evidence] = []
        verdicts = []
        for claim in claims:
            if not claim.verification_required:
                continue
            plan = self.planner.plan(claim)
            judged: list[Evidence] = []
            state = RetrievalState.empty()
            contradiction_completed = False
            for task in plan.tasks:
                new_evidence = self.retriever.retrieve_next(task, state)
                if task.intent == SearchIntent.CONTRADICTION:
                    contradiction_completed = True
                for item in new_evidence:
                    judgment = self.judge.judge(claim, item)
                    notes = item.notes
                    if judgment.inference_gap:
                        notes = (notes + " " + judgment.inference_gap).strip()
                    judged.append(replace(item, relation=judgment.relation, notes=notes))
                if contradiction_completed and state.duplicate_rounds >= 2:
                    break
            all_evidence.extend(judged)
            verdicts.append(self.verdict_engine.decide(claim, judged, contradiction_completed))
        citation_audit = self.citation_auditor.audit(claims, all_evidence, verdicts, citations)
        return self.report_builder.build_audit(claims, all_evidence, verdicts, citation_audit)
