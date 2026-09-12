# Idea Check

**創業點子與產品構想的壓力測試 Agent Skill**，可用於 Codex 與 Claude Code。

用一致、可重複、以證據為基礎的方法檢驗一個點子：市場需求、競品與替代方案、商業化與定價、護城河、二階風險、go/no-go 判斷，並設計低成本的驗證實驗。

核心原則是：**把點子視為待驗證的假說，而非待鼓勵的故事。** 主動尋找反證，明確區分「事實」、「推論」、「假設」與「未知」，不替使用者做最終決策。

## 安裝

本 skill 是標準 `SKILL.md` 格式，不依賴任一平台的專屬欄位。入口是 `SKILL.md`，Codex 中介資料在 `agents/openai.yaml`。

**Codex**：把這個資料夾放進 Codex 的 Skills 目錄。

**Claude Code**：複製或建立 symbolic link 到下列其中一處，資料夾名稱即指令名稱，必須是 `idea-check`：

```text
~/.claude/skills/idea-check/          # 個人層級
<project>/.claude/skills/idea-check/  # 專案層級
```

## 內容

| 路徑 | 用途 |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Skill 主體：任務原則與評估流程 |
| [`references/evaluation-frameworks.md`](references/evaluation-frameworks.md) | 評估框架 |
| [`references/research-playbook.md`](references/research-playbook.md) | 調研執行手冊 |
| [`references/report-template.md`](references/report-template.md) | 報告範本 |
| [`agents/openai.yaml`](agents/openai.yaml) | Codex 介面中介資料 |

## 相關 Skill

各 skill 皆為獨立 repository：

- [academic-search](https://github.com/Wenqing950519/academic-search) — 學術證據引擎（原 `whitepaper-claim-auditor`）
- [ga4-analyzing](https://github.com/Wenqing950519/ga4-analyzing) — GA4 數據分析

求職相關：

- [career-tools](https://github.com/Wenqing950519/career-tools) — 給大學生的求職工具箱，平台總庫
- [career-offercheck](https://github.com/Wenqing950519/career-offercheck) — 實習 offer 去留決策
- [career-skill-gap](https://github.com/Wenqing950519/career-skill-gap) ／ [career-resume-composer](https://github.com/Wenqing950519/career-resume-composer) ／ [career-opportunity-catch](https://github.com/Wenqing950519/career-opportunity-catch)
