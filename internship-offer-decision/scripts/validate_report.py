#!/usr/bin/env python3
"""Validate actionable-now Internship Offer Decision reports without dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


INPUT_LEVELS = {"company_title", "jd", "interview", "full"}
VERDICTS = {"take", "conditional_take", "decline"}
SCORE_KEYS = {"role_substance", "learning_gain", "resume_outcome_potential", "team_company_leverage", "overall_roi"}
TIERS = {"strong", "signal", "weak"}
DIRECTIONS = {"positive", "negative", "unknown"}
REQUIRED_HEADINGS = [
    "# 結論", "## 實際工作", "## 是否接近核心業務", "## 3–6 個月後能帶走什麼",
    "## 公司與團隊是否支撐這個機會", "## 最大風險", "## 適合／不適合什麼人",
    "## 評分與最終判斷", "## 主要決策不確定性", "## Evidence Index",
]
FORBIDDEN_OUTPUT_PATTERNS = {
    "過時狀態 preliminary_only": r"preliminary[_ ]only",
    "過時狀態資訊不足": r"insufficient_information",
    "繼續面試指令": r"繼續\s*面試",
    "面試建議區塊": r"面試建議",
    "Offer 前確認區塊": r"offer\s*前\s*確認",
    "提問清單": r"值得\s*詢問|下一輪.*(?:面試|談話).*問題|questions?\s*to\s*verify",
    "要求回問公司": r"回去問|(?:向|跟|去)公司.*(?:確認|詢問|提問)|(?:請|建議).{0,100}(?:確認|詢問|提問)|(?:詢問|提問).{0,100}(?:公司|雇主)",
    "舊未知欄位": r'"(?:unknowns|conditions|is_provisional|how_to_verify|question)"',
}


def canonical_hash(report: dict[str, Any]) -> str:
    payload = json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def require_object(parent: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key}: must be an object")
        return {}
    return value


def require_list(parent: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = parent.get(key)
    if not isinstance(value, list):
        errors.append(f"{key}: must be an array")
        return []
    return value


def walk_evidence_refs(value: Any, path: str = "$") -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key == "evidence_ids":
                yield child_path, child
            else:
                yield from walk_evidence_refs(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_evidence_refs(child, f"{path}[{index}]")


def find_forbidden(text: str) -> list[str]:
    return [name for name, pattern in FORBIDDEN_OUTPUT_PATTERNS.items() if re.search(pattern, text, re.IGNORECASE)]


def validate_report(report: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(report, dict):
        return ["root: must be a JSON object"], warnings

    required_top = {"schema_version", "generated_at", "language", "input_level", "subject", "decision", "actual_work", "core_proximity", "takeaways", "support", "risks", "fit", "scores", "decision_uncertainties", "limitations", "evidence"}
    missing, extra = sorted(required_top - report.keys()), sorted(report.keys() - required_top)
    if missing:
        errors.append("root: missing keys: " + ", ".join(missing))
    if extra:
        errors.append("root: unexpected keys: " + ", ".join(extra))
    if report.get("schema_version") != "2.0":
        errors.append("schema_version: must equal '2.0'")
    if report.get("language") != "zh-Hant":
        errors.append("language: must equal 'zh-Hant'")
    if report.get("input_level") not in INPUT_LEVELS:
        errors.append(f"input_level: expected one of {sorted(INPUT_LEVELS)}")

    subject = require_object(report, "subject", errors)
    for field in ("company", "job_title"):
        if not isinstance(subject.get(field), str) or not subject.get(field, "").strip():
            errors.append(f"subject.{field}: non-empty string required")

    decision = require_object(report, "decision", errors)
    verdict, score = decision.get("verdict"), decision.get("recommendation_score")
    if verdict not in VERDICTS:
        errors.append("decision.verdict: must be take, conditional_take, or decline")
    if not is_number(score) or not 0 <= score <= 10:
        errors.append("decision.recommendation_score: must be a number from 0 to 10")
    if decision.get("confidence") not in {"low", "medium", "high"}:
        errors.append("decision.confidence: must be low, medium, or high")
    for field in ("one_line_conclusion", "base_case", "verdict_rationale"):
        if not isinstance(decision.get(field), str) or not decision.get(field, "").strip():
            errors.append(f"decision.{field}: non-empty string required")
    for field in ("reasons_for", "reasons_against"):
        reasons = require_list(decision, field, errors)
        if not 1 <= len(reasons) <= 2:
            errors.append(f"decision.{field}: requires one or two items")
    if decision.get("score_method") != "judgment_not_average":
        errors.append("decision.score_method: must equal 'judgment_not_average'")
    if is_number(score) and verdict in VERDICTS:
        expected = "take" if score >= 8 else "conditional_take" if score >= 6 else "decline"
        if verdict != expected and not str(decision.get("score_alignment_note") or "").strip():
            errors.append(f"decision: score {score} normally maps to {expected}; provide score_alignment_note for an exception")

    scores = require_object(report, "scores", errors)
    if set(scores) != SCORE_KEYS:
        errors.append("scores: must contain exactly the five contracted score keys")
    for key in SCORE_KEYS:
        item = scores.get(key)
        if not isinstance(item, dict):
            errors.append(f"scores.{key}: must be an object")
            continue
        value = item.get("score")
        if not is_number(value) or not 0 <= value <= 10:
            errors.append(f"scores.{key}.score: must be a number from 0 to 10")
        if not str(item.get("rationale") or "").strip():
            errors.append(f"scores.{key}.rationale: non-empty string required")

    takeaways = require_object(report, "takeaways", errors)
    resume_experiences = require_list(takeaways, "resume_experiences", errors)
    if len(resume_experiences) != 3:
        errors.append("takeaways.resume_experiences: exactly three entries required")
    for index, item in enumerate(resume_experiences):
        if not isinstance(item, dict):
            errors.append(f"takeaways.resume_experiences[{index}]: must be an object")
            continue
        for field in ("title", "resume_bullet", "base_case_boundary"):
            if not isinstance(item.get(field), str) or not item.get(field, "").strip():
                errors.append(f"takeaways.resume_experiences[{index}].{field}: non-empty string required")
        for field in ("quantification_clues", "learning_to_capture"):
            values = item.get(field)
            if not isinstance(values, list) or not values or not all(isinstance(value, str) and value.strip() for value in values):
                errors.append(f"takeaways.resume_experiences[{index}].{field}: non-empty string array required")
        if item.get("confidence") not in {"low", "medium", "high"}:
            errors.append(f"takeaways.resume_experiences[{index}].confidence: invalid confidence")

    evidence_list = require_list(report, "evidence", errors)
    evidence_map: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(evidence_list):
        path = f"evidence[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{path}: must be an object")
            continue
        evidence_id = item.get("id")
        if not isinstance(evidence_id, str) or not re.fullmatch(r"E\d{3,}", evidence_id):
            errors.append(f"{path}.id: expected E followed by at least three digits")
            continue
        if evidence_id in evidence_map:
            errors.append(f"{path}.id: duplicate {evidence_id}")
        evidence_map[evidence_id] = item
        if item.get("tier") not in TIERS:
            errors.append(f"{path}.tier: invalid tier")
        if item.get("direction") not in DIRECTIONS:
            errors.append(f"{path}.direction: invalid direction")
        if item.get("source_type") == "anonymous_review" and item.get("anonymous") is not True:
            errors.append(f"{path}: anonymous_review must set anonymous=true")

    for ref_path, refs in walk_evidence_refs({k: v for k, v in report.items() if k != "evidence"}):
        if not isinstance(refs, list):
            errors.append(f"{ref_path}: must be an array")
            continue
        for evidence_id in refs:
            if evidence_id not in evidence_map:
                errors.append(f"{ref_path}: unknown evidence id {evidence_id!r}")

    risks = require_list(report, "risks", errors)
    risk_ids: set[str] = set()
    for index, risk in enumerate(risks):
        if not isinstance(risk, dict):
            errors.append(f"risks[{index}]: must be an object")
            continue
        risk_id = risk.get("id")
        if risk_id in risk_ids:
            errors.append(f"risks[{index}].id: duplicate {risk_id}")
        risk_ids.add(risk_id)
        if risk.get("severity") == "high":
            supporting = [evidence_map.get(ref) for ref in risk.get("evidence_ids", []) if evidence_map.get(ref)]
            if not any(item.get("tier") in {"strong", "signal"} for item in supporting):
                errors.append(f"risks[{index}]: high-severity risk cannot rely only on Weak Evidence")

    uncertainties = require_list(report, "decision_uncertainties", errors)
    for index, item in enumerate(uncertainties):
        if not isinstance(item, dict):
            errors.append(f"decision_uncertainties[{index}]: must be an object")
            continue
        for field in ("title", "missing_evidence", "score_effect", "base_case_assumption"):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"decision_uncertainties[{index}].{field}: non-empty string required")
            elif "?" in value or "？" in value:
                errors.append(f"decision_uncertainties[{index}].{field}: must not be phrased as a question")

    forbidden = find_forbidden(json.dumps(report, ensure_ascii=False))
    if forbidden:
        errors.append("report: contains forbidden decision-timing output: " + ", ".join(forbidden))
    if not evidence_list:
        warnings.append("evidence: empty Evidence Index; confidence should normally be low")
    if report.get("input_level") == "company_title" and decision.get("confidence") != "low":
        warnings.append("company_title: sparse input normally warrants low confidence")
    if not uncertainties:
        warnings.append("decision_uncertainties: empty; confirm that material gaps were not omitted")
    return errors, warnings


def validate_markdown(path: Path, expected_hash: str) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    marker = re.search(r"<!--\s*report-json-sha256:\s*([0-9a-f]{64})\s*-->", text)
    if not marker:
        errors.append(f"{path}: missing report-json-sha256 marker")
    elif marker.group(1) != expected_hash:
        errors.append(f"{path}: JSON fingerprint does not match report.json")
    lines, positions = text.splitlines(), []
    for heading in REQUIRED_HEADINGS:
        matches = [i for i, line in enumerate(lines) if line.strip() == heading]
        if len(matches) != 1:
            errors.append(f"{path}: expected heading exactly once: {heading}")
        else:
            positions.append(matches[0])
    if len(positions) == len(REQUIRED_HEADINGS) and positions != sorted(positions):
        errors.append(f"{path}: required headings are out of order")
    forbidden = find_forbidden(text)
    if forbidden:
        errors.append(f"{path}: contains forbidden decision-timing output: " + ", ".join(forbidden))
    return errors


def validate_html(path: Path, expected_hash: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    meta = re.search(r'<meta\s+name=["\']report-json-sha256["\']\s+content=["\']([0-9a-f]{64})["\']', text, re.IGNORECASE)
    if not meta:
        errors.append(f"{path}: missing report-json-sha256 meta tag")
    elif meta.group(1) != expected_hash:
        errors.append(f"{path}: JSON fingerprint does not match report.json")
    if 'id="report-data"' not in text:
        errors.append(f"{path}: missing embedded report-data payload")
    forbidden = find_forbidden(text)
    if forbidden:
        errors.append(f"{path}: contains forbidden decision-timing output: " + ", ".join(forbidden))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Path to report.json")
    parser.add_argument("--markdown", type=Path, help="Optional report.md to verify")
    parser.add_argument("--html", type=Path, help="Optional report.html to verify")
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read report JSON: {exc}", file=sys.stderr)
        return 2
    errors, warnings = validate_report(report)
    fingerprint = canonical_hash(report)
    if args.markdown:
        try:
            errors.extend(validate_markdown(args.markdown, fingerprint))
        except OSError as exc:
            errors.append(f"{args.markdown}: cannot read file: {exc}")
    if args.html:
        try:
            errors.extend(validate_html(args.html, fingerprint))
        except OSError as exc:
            errors.append(f"{args.html}: cannot read file: {exc}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: valid report ({fingerprint})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
