# Internship Offer Decision

給已完成面試、正在決定是否接受實習 Offer 的大學生使用的跨工具 Agent Skill。它可用於 Codex 與 Claude Code。

它不做企業級徵信，也不產生下一輪面試問題。它用現在已有的資料重建實習生實際可能做的工作，並以保守的 Base Case 做出可立即執行的 `Take`、`Conditional Take` 或 `Decline` 判斷。

## 它會產生什麼

- 一份完整的 `report.json`，作為唯一資料來源。
- 一份可閱讀的 `report.md` 與 30 秒能看懂的 `report.html`。
- 五項分數：工作內容含金量、學習增量、履歷成果潛力、團隊／公司加成、整體投入報酬。
- 三則可保守寫入履歷的實習經驗；每則附可量化線索、可偷師的方法與不可誇大的 Base Case 邊界。

未知資訊不會讓 Skill 拒絕決策，也不會轉成要求使用者回去問公司；它只會降低信心並限制正式評價。

## 使用方式

提供盡可能多的輸入：公司、職稱、JD、面試筆記、Offer 條件、學生背景與同期其他機會。

資料較少時仍會得到當前最佳 Verdict，但信心較低；面試與 Offer 資料只會提高判斷精度，不是產生決策的前提。

### Codex

將 [internship-offer-decision](internship-offer-decision) 資料夾放入 Codex 的 Skills 目錄，或從該目錄安裝。入口是 `SKILL.md`。

### Claude Code

Claude Code 使用同一份標準 `SKILL.md`，不需要轉換。把整個資料夾複製或建立 symbolic link 到下列其中一處：

```text
~/.claude/skills/internship-offer-decision/          # 個人層級
<project>/.claude/skills/internship-offer-decision/  # 專案層級
```

之後可直接用 `/internship-offer-decision` 呼叫，或以自然語言要求 Claude 協助判斷實習 Offer。Claude Code 依目錄名稱決定指令名稱，因此請保留 `internship-offer-decision` 這個資料夾名稱。

此專案的 frontmatter 只使用 Agent Skills／Claude Code 共同支援的 `name` 與 `description`；沒有依賴 Codex 專屬欄位或 Claude Code 專屬動態指令。

## 專案結構

```text
internship-offer-decision/       # 可由 Codex 與 Claude Code 共用的 Skill、規範、schema、驗證器與 HTML 模板
```

## 驗證與輸出

```bash
python internship-offer-decision/scripts/validate_report.py <report.json> --markdown <report.md> --html <report.html>
```

HTML 報告由同一份 `report.json` 產生：

```bash
python internship-offer-decision/scripts/render_html.py <report.json> <report.html>
```

## 核心原則

> 研究深度由資訊是否會改變 Offer Decision 決定，而不是由網路上還能找到多少資料決定。
