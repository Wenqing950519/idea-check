# Output Contract

## One source of truth

Create `report.json` first and validate it against `schemas/report.schema.json` plus `scripts/validate_report.py`. Generate all human-facing outputs from this same data. Do not add claims to Markdown or HTML that are absent from JSON.

Compute the source fingerprint as SHA-256 of canonical JSON encoded as UTF-8 with sorted keys and compact separators.

## Hard output rules

- Every report has numeric five-score output and exactly one current `take`, `conditional_take`, or `decline` verdict.
- The formal verdict must use the Base Case, not Best Case or a future employer response.
- Never output `Preliminary Only`, `資訊不足`, `繼續面試`, `Offer 前確認`, `值得詢問的問題`, or equivalent follow-up instructions.
- Never include an interview-question, employer-question, or verification checklist.
- Replace all unknown/verification sections with **主要決策不確定性**.

## `report.md`

Write a complete Traditional Chinese report and place this marker near the top:

```text
<!-- report-json-sha256: HEX_DIGEST -->
```

Use these exact headings in order:

```markdown
# 結論
## 實際工作
## 是否接近核心業務
## 3–6 個月後能帶走什麼
## 公司與團隊是否支撐這個機會
## 最大風險
## 適合／不適合什麼人
## 評分與最終判斷
## 主要決策不確定性
## Evidence Index
```

Within `# 結論`, state the final verdict, score, confidence, one-line conclusion, two strongest positives, two strongest negatives, and Base Case. If relevant, show Best / Base / Worst as explanatory scenarios, with Base Case explicitly controlling the formal decision.

The **主要決策不確定性** section must describe missing evidence → score effect → conservative Base Case assumption. It must not use question form, tell the user to ask anyone, or frame a later answer as required for the verdict.

At the very start of `## 3–6 個月後能帶走什麼`, add `### 實習結束後可能寫在履歷上的三個經驗`. Render exactly three numbered entries. Each entry must include:

- **履歷寫法:** one conservative, truthful bullet;
- **可量化線索:** evidence the student can personally retain, clearly separated from unproven business results;
- **可偷師的方法:** a repeatable workflow, review standard, or collaboration practice;
- **Base Case 邊界:** what is not being claimed because ownership, attribution, data access, or portfolio rights are unknown.

## `report.html`

Render with:

```bash
python scripts/render_html.py report.json report.html
```

The self-contained, responsive Traditional Chinese page must show on the first screen:

- numeric recommendation score;
- `Take`, `Conditional Take`, or `Decline`;
- one-line conclusion;
- Base Case summary;
- two strongest positives;
- two strongest negatives.

After the first screen, show five scores, then the three resume experiences at the front of the 3–6 month outcomes, followed by other outcomes, primary risks, 主要決策不確定性, fit, and collapsed Evidence. Use English only where natural, such as BD, B2B, Offer, SEO, or AI.

Embed the fingerprint as a meta tag and data attribute. Escape JSON and render input text with DOM `textContent`, not `innerHTML`.

## `report.json` behavior

`input_level` is descriptive only. Every level requires numeric scores, a current verdict, Base Case summary, `decision_uncertainties`, and exactly three `takeaways.resume_experiences`. Use `confidence` to express evidence limitations.

## Validation commands

```bash
python scripts/validate_report.py report.json
python scripts/validate_report.py report.json --markdown report.md
python scripts/render_html.py report.json report.html
python scripts/validate_report.py report.json --markdown report.md --html report.html
```

Treat errors as blockers. Warnings may describe sparse evidence, but must never tell the user to get more evidence from the employer.
