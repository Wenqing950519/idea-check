from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResearchProfile:
    name: str
    description: str
    preferred_sources: tuple[str, ...]
    required_steps: tuple[str, ...]
    coaching_questions: tuple[str, ...] = ()


PROFILES = {
    "geo-whitepaper": ResearchProfile(
        name="geo-whitepaper",
        description="Academic plus official-web evidence for GEO and citation-selection whitepapers.",
        preferred_sources=("peer_reviewed", "preprint", "official_documentation", "first_party_dataset"),
        required_steps=("local_kb", "academic_discovery", "official_web", "counterevidence", "citation_audit"),
    ),
    "olist-business-analysis": ResearchProfile(
        name="olist-business-analysis",
        description="Dataset-first business analysis with explicit execution evidence and Socratic coaching.",
        preferred_sources=("local_dataset", "data_dictionary", "analysis_artifact", "peer_reviewed"),
        required_steps=("dataset_intake", "question_definition", "analysis_execution", "claim_mapping", "review"),
        coaching_questions=(
            "你要解釋的是描述性差異、預測關係，還是因果效果？",
            "哪些欄位與時間範圍真正能回答這個問題？",
            "什麼替代解釋會讓目前結論不成立？",
            "哪一個輸出檔或查詢結果能讓別人重跑這個判斷？",
        ),
    ),
}


def get_profile(name: str) -> ResearchProfile:
    try:
        return PROFILES[name]
    except KeyError as exc:
        raise ValueError(f"Unknown research profile: {name}") from exc
