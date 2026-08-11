# Scoring

## Purpose

Every Offer Decision report must contain five numeric scores and a current verdict. Scores visualize a reasoned Base Case; they are never a mechanical average and never await a future answer.

Use evidence this way:

- **Confirmed:** may raise or lower the Base Case.
- **Plausible but unverified:** upside only; do not raise the official score.
- **Unknown:** lower confidence. If high value depends on the unknown, do not award that high value; use a conservative middle-to-low assessment.
- **Negative Evidence:** lower the relevant score or raise a separate risk.

## Shared scale

| Score | Meaning |
| --- | --- |
| 8.0–10 | 優先接受：Base Case already contains strong, portable outcomes and acceptable downside. |
| 6.0–7.9 | 有條件推薦：Base Case has useful value, but tradeoffs or opportunity cost materially matter. |
| 4.0–5.9 | 推薦度偏低：some value exists, but Base Case is not compelling for the time. |
| 0–3.9 | 不建議投入：Base Case learning/output is weak or downside dominates. |

## Five scores

### 工作內容含金量 (`role_substance`)

Measure meaningful problems, defined ownership, judgment, and proximity to value creation.

- 8–10: confirmed bounded, consequential work in or near the core loop.
- 6–7.9: confirmed meaningful contribution, but partial ownership or mixed support work.
- 4–5.9: mostly execution/support, or ownership is not evidenced.
- 0–3.9: repetitive capacity filling, misleading scope, or no credible deliverable.

### 學習增量 (`learning_gain`)

Measure growth beyond the student’s baseline through task difficulty, Feedback, Mentorship, and Methodology.

- 8–10: confirmed stretch work plus repeated high-quality feedback.
- 6–7.9: useful learning is evidenced but support is uneven.
- 4–5.9: exposure or self-directed practice dominates; mentor/review quality is unproven.
- 0–3.9: little new learning or weak methods are reinforced.

### 履歷成果潛力 (`resume_outcome_potential`)

Measure the Base Case probability of finished, explainable projects, metrics, artifacts, references, or resume bullets.

- 8–10: confirmed ability to own, measure, and demonstrate multiple outcomes.
- 6–7.9: at least one credible outcome is likely, with bounded access limitations.
- 4–5.9: work may be real but completion, attribution, metrics, or portfolio rights are unproven.
- 0–3.9: fragmented, confidential-without-substitute, or chore-like output dominates.

For the required three resume experiences, distinguish a truthful **scope metric** from an unavailable business result. Count only evidence the student can retain without inventing it: number of briefs, content assets, workflow versions, stakeholders, review cycles, turnaround time, error reduction, adoption, or attributable KPI. State a reusable method worth learning from, but do not score an unproven metric, attribution, or portfolio right as if it were already obtained.

### 團隊／公司加成 (`team_company_leverage`)

Measure added value from people, product/customer context, methods, network, and company trajectory. Do not reward brand size alone.

- 8–10: confirmed strong practitioners, credible context, and future signaling.
- 6–7.9: some evidence of strong people or context, but benefit is role-dependent.
- 4–5.9: limited external signal or team support is unproven.
- 0–3.9: evidence indicates the environment reduces learning or credibility.

### 整體投入報酬 (`overall_roi`)

Judge independently from Base Case outcomes, time, pay, schedule, risk, student goals, and known alternatives. Explain why it is not the mean of other scores.

## Verdict mapping

Use the current Base Case by default:

- 8.0–10 → `take`
- 6.0–7.9 → `conditional_take`
- 0–5.9 → `decline`

When a verdict differs, add a specific `score_alignment_note`; the explanation must rest on present facts, not a planned employer conversation. Examples include an already-known superior alternative, an irreversible timing constraint, or a documented short trial arrangement.

## Risks are not a sixth score

List risks independently with likelihood, severity, student impact, and current mitigation only when it already exists. Do not use “ask the company” as a mitigation. A high score can coexist with a high but contained risk; explain the tradeoff in the Base Case verdict.
