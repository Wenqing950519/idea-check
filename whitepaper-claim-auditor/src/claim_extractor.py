from __future__ import annotations

import re

from .models import Claim, ClaimType


_CAUSAL = re.compile(r"\b(causes?|caused|increases?|decreases?|leads? to|results? in)\b|導致|造成|直接提高|直接增加", re.I)
_UNIVERSAL = re.compile(r"\b(always|all|never|universally)\b|必然|所有|普遍|一律", re.I)
_QUANT = re.compile(r"\d+(?:\.\d+)?\s*(?:%|％|倍|個|人|年|元)?")
_NORMATIVE = re.compile(r"\b(should|must|ought to|need to)\b|應該|必須|不得忽視|有必要", re.I)
_PREDICTIVE = re.compile(r"\b(will|forecast|predict)\b|將會|預測|預計", re.I)
_COMPARATIVE = re.compile(r"\b(more|less|higher|lower|better|worse)\b|高於|低於|優於|較高|較低", re.I)


class ClaimExtractor:
    """Extract candidate claims conservatively from Markdown or plain text."""

    def extract(self, document: str) -> list[Claim]:
        claims: list[Claim] = []
        in_fence = False
        counter = 1
        for line_number, raw_line in enumerate(document.splitlines(), start=1):
            line = raw_line.strip()
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence or not line or line.startswith("#"):
                continue
            line = re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+|>\s*)", "", line)
            for sentence in self._sentences(line):
                if not self._is_candidate(sentence):
                    continue
                claim_type = self.classify(sentence)
                flags = self.risk_flags(sentence, claim_type)
                claims.append(Claim(
                    claim_id=f"C-{counter:03d}",
                    parent_id=None,
                    source_location=f"line-{line_number}",
                    original_text=sentence,
                    atomic_claim=sentence,
                    claim_type=claim_type,
                    verification_required=claim_type not in {ClaimType.NORMATIVE, ClaimType.INTERPRETIVE},
                    dependencies=[],
                    author_assertion_level="strong" if flags else "moderate",
                    risk_flags=flags,
                ))
                counter += 1
        return claims

    @staticmethod
    def _sentences(line: str) -> list[str]:
        return [part.strip() for part in re.split(r"(?<=[。！？.!?])\s*", line) if part.strip()]

    @staticmethod
    def _is_candidate(sentence: str) -> bool:
        if len(sentence) < 8 or sentence.endswith("?") or sentence.endswith("？"):
            return False
        return bool(re.search(r"[A-Za-z\u3400-\u9fff]", sentence))

    @staticmethod
    def classify(text: str) -> ClaimType:
        if _NORMATIVE.search(text):
            return ClaimType.NORMATIVE
        if _CAUSAL.search(text):
            return ClaimType.CAUSAL
        if _QUANT.search(text):
            return ClaimType.QUANTITATIVE
        if _PREDICTIVE.search(text):
            return ClaimType.PREDICTIVE
        if _UNIVERSAL.search(text):
            return ClaimType.GENERALIZATION
        if _COMPARATIVE.search(text):
            return ClaimType.COMPARATIVE
        if re.search(r"\b(is defined as|means|refers to)\b|定義為|係指|意指", text, re.I):
            return ClaimType.DEFINITIONAL
        return ClaimType.FACTUAL

    @staticmethod
    def risk_flags(text: str, claim_type: ClaimType) -> list[str]:
        flags: list[str] = []
        if claim_type == ClaimType.CAUSAL:
            flags.append("CAUSAL_LANGUAGE")
        if _UNIVERSAL.search(text):
            flags.append("UNIVERSAL_LANGUAGE")
        if re.search(r"\b(proves?|conclusively|significantly)\b|已證明|顯著|核心原因", text, re.I):
            flags.append("STRONG_ASSERTION")
        return flags
