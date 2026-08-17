# Skills

兩個獨立的 Agent Skill，可用於 Codex 與 Claude Code。

| Skill | 做什麼 |
| --- | --- |
| [`idea-check`](idea-check) | 用一致、可重複、以證據為基礎的方法壓力測試創業點子與產品構想：市場需求、競品與替代方案、商業化與定價、護城河、二階風險、go/no-go 判斷，並設計低成本驗證實驗。 |
| [`whitepaper-claim-auditor`](whitepaper-claim-auditor) | 稽核白皮書、研究報告與論文：抽取主張、拆解依賴、檢索段落級證據、判斷主張與來源的蘊涵關係、給出保守的六態判定，並檢查引用完整性。以壓低 False Support Rate 為優先，而非引用數量。 |

## 安裝

兩者都是標準 `SKILL.md` 格式，不依賴任一平台的專屬欄位。

**Codex**：把 skill 資料夾放進 Codex 的 Skills 目錄，入口是 `SKILL.md`。

**Claude Code**：複製或建立 symbolic link 到下列其中一處，資料夾名稱即指令名稱，請勿更動：

```text
~/.claude/skills/<skill-name>/          # 個人層級
<project>/.claude/skills/<skill-name>/  # 專案層級
```

## 相關專案

求職相關的 skill 已獨立，不在此 repo：

- [career-tools](https://github.com/Wenqing950519/career-tools) — 給大學生的求職工具箱，平台總庫
- [career-offercheck](https://github.com/Wenqing950519/career-offercheck) — 實習 offer 去留決策（原 `internship-offer-decision`，已更名並移出本 repo）
- [career-skill-gap](https://github.com/Wenqing950519/career-skill-gap) ／ [career-resume-composer](https://github.com/Wenqing950519/career-resume-composer) ／ [career-opportunity-catch](https://github.com/Wenqing950519/career-opportunity-catch)
