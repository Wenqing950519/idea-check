# Research Playbook

## 目錄

1. 研究問題
2. 搜尋矩陣
3. 來源優先順序
4. 證據帳本
5. 反證流程
6. 研究停止條件

## 1. 研究問題

研究不是為了證明「有人做過」，而是回答：

- 目標客群是否已花時間、金錢、風險或組織成本處理這件事？
- 他們在什麼事件發生時開始尋找解法？
- 不處理的後果是否足以驅動採用與付款？
- 現行替代方案在哪些情境下已經足夠好？
- 市場正在形成、成熟、整併，還是被平台吸收？
- 新產品必須贏過的是哪個行為、工作流程或預算，而不只是另一套軟體？

對會變動的主張使用最新資料；記錄查詢日與資料本身的日期。優先開啟原始頁面，不只依賴搜尋摘要。

## 2. 搜尋矩陣

不要只搜尋產品名稱。把 `[problem]`、`[customer]`、`[job]`、`[trigger]` 與 `[category]` 替換成實際內容，交叉搜尋下列區塊。

### 需求與語言

- `"[problem]" workflow`
- `"[problem]" spreadsheet OR template OR checklist`
- `"how do you" "[job]"`
- `"[problem]" reddit OR forum OR community`
- `"[problem]" consultant OR agency OR service`
- `"[problem]" budget OR RFP OR procurement`
- `"[category]" review complaints`
- `"[category]" churn OR cancel OR alternative`

### 直接與間接競爭

至少涵蓋：

- 相同產品類別。
- 鄰近類別或用不同機制完成同一工作。
- 手工作業、試算表、Notion、email、顧問、代理商及內部人員。
- 開源專案、GitHub 工具與 self-hosted 解法。
- 大型平台的內建功能與 bundle。
- Enterprise suite、垂直 SaaS 與系統整合商。
- 美國、歐洲、中國、日本及目標市場的區域性產品；依點子調整地區。
- 不採取行動，以及「忍受問題」本身。

可用查詢：

- `"[job]" software OR platform OR tool`
- `"[category]" alternatives`
- `site:github.com "[problem]"`
- `"[problem]" open source`
- `"[problem]" enterprise`
- `"[problem]" API`
- `"[problem]" 中文 工具 OR 软件 OR SaaS`
- `"[problem]" acquisition OR funding OR shutdown`

### 市場與商業化

- 競品官方 pricing、方案邊界、免費層及 enterprise CTA。
- 評論中提到的購買理由、取消原因、導入時間和切換成本。
- 招聘職缺、RFP、顧問服務與既有軟體預算，確認誰擁有問題。
- acquisition、融資、關閉、pivot 與失敗案例，判斷類別經濟性。
- 通路關鍵字的 CPC/搜尋量只能當輔助訊號，不得直接等同需求。

### 平台與二階風險

- 主要平台 roadmap、官方 API 條款、費率、配額與棄用公告。
- 平台已內建或可能 bundle 的功能。
- 主要輸入成本趨勢、開源替代品與 commoditization。
- 隱私、著作權、資料存放、爬蟲、廣告及產業法規。

## 3. 來源優先順序

依主張選擇最接近原始事實的來源：

1. **第一方行為資料**：付款、留存、流失、產品使用、銷售紀錄、實際工作流程。
2. **原始官方資料**：產品文件、pricing、條款、公告、財報、政府或監管資料。
3. **可核實市場資料**：客戶案例、RFP、職缺、公開採購、可信研究或資料集。
4. **使用者生成資料**：具體評論、社群討論、issue tracker；用於發現語言與假說，不單獨推估市場。
5. **彙整資料**：Product Hunt、G2、Capterra、Crunchbase 類資料庫及新聞；回到原始來源核對重要主張。
6. **思想框架與案例庫**：YC Startup Library、Paul Graham Essays、Lean Startup、The Mom Test、Crossing the Chasm、Failory、CB Insights 等；用於改善問題，不把名言當市場證據。

對每個關鍵主張盡量取得兩種不同證據。競品自己的文案只能證明它如何定位自己，不能證明客戶得到結果。

## 4. 證據帳本

使用下列表格或同等結構：

| ID | 主張 | 證據摘要 | 類型 | 支持/反駁 | 日期 | 可信度 | 來源 |
|---|---|---|---|---|---|---|---|
| E1 | 例：團隊每週人工追蹤品牌提及 | 5/8 位目標買家展示現有報表 | 第一方行為 | 支持 | YYYY-MM-DD | 中 | 訪談筆記 |

證據類型可標記為：觀察行為、交易、產品數據、官方資料、第三方案例、使用者陳述、模型推論。可信度使用高/中/低並說明關鍵限制。

## 5. 反證流程

至少完成一輪 adversarial search：

1. 寫出目前最想相信的三個主張。
2. 為每個主張寫出「若它是錯的，世界會呈現什麼樣子？」
3. 搜尋 category failure、shutdown、pivot、free alternative、low adoption、complaints、platform feature。
4. 找出一個合理的「現在已足夠好」替代方案。
5. 找出一個客戶不採取行動仍沒有重大後果的情境。
6. 將最強反證放入主結論，不藏在附註。

常見假訊號：

- 很多人說「很酷」但沒有提供時間、資料、介紹或付款。
- 社群聲量高但使用頻率低。
- 大市場報告卻無法指出實際買家與預算科目。
- 競品融資多但留存、毛利或銷售效率未知。
- 搜尋結果少，被錯誤解讀為藍海。
- 高流量免費工具，被錯誤解讀為強付費意願。

## 6. 研究停止條件

符合下列條件後停止廣泛搜尋，轉入判斷與實驗：

- 每個主要替代方案類別至少找到一個具體例子。
- 定位、核心能力與價格已由官方或同等可靠來源核實。
- 至少取得一項需求支持證據與一項反證。
- 已辨識付費者、使用者、觸發事件及現有預算的已知或未知狀態。
- 新來源主要重複既有發現，且不再改變 decision-critical 假設。

若尚未達標但受工具、付費牆或資料限制，列出缺口，不以推測補齊。
