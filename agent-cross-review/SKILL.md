---
name: agent-cross-review
description: 用於 Codex 與 Claude 互相 review 內容並來回回應。觸發語：「review {agent} 的 {主題}」、「看一下 {agent} 的 review」、「他回你了」。涵蓋 review/回應檔的命名、讀寫路由與後續來回更新。
---

# Agent 互相 review（Codex / Claude 互審）

兩個 agent 針對某主題互審並來回回應。原則：一律「讀對方負責的檔、寫自己負責的檔」，後續來回不另開新檔。

## 觸發語與角色
- 「review {agent} 的 {主題}」→ 被指示的 agent 當 reviewer，審該 {agent} 的 {主題} 內容。
- 「看一下 {agent} 的 review」「他回你了」→ 被指示的 agent 去讀「對方最近更新的檔案」後回應。
- 「自己」＝執行此 skill 的 agent；指令中提到的另一個 agent ＝「對方」。

## 內容規範

- review 與 response 預設使用中文；只有使用者明確指定其他語言時才改用指定語言。
- review 除了正確性，也必須檢查簡單性、一致性與 clean code，包含過度抽象、過度通用化、重複結構、既有架構一致性與可讀性。
- review 只寫觀察到的事實與確信程度，分成「必改／建議／可保留／待確認」；問題附出處（檔名:行號）。
- response 逐點說明已修改內容，或清楚記錄不修改的理由。

## 檔名

- reviewer 寫 `{主題}_reviewed_by_{自己}.md`，例如 `sql_design_reviewed_by_claude.md`。
- 被 review 方回應寫 `{主題}_responsed_by_{自己}.md`，例如 `sql_design_responsed_by_codex.md`。
- （`responsed` 為指定拼法，照用。）

## 讀寫路由（讀對方的檔、寫自己的檔）

- reviewer：讀對方的 `_responsed_by_` 檔（若已存在）、寫自己的 `_reviewed_by_` 檔。
- 被 review 方：讀對方的 `_reviewed_by_` 檔、寫自己的 `_responsed_by_` 檔。

## 後續來回
- 不另開新檔：各自持續更新自己負責的那個檔。
- 每輪視情況：內容大改用覆寫，逐點補充用 append。

## 檔案位置
- 放在被 review 內容所屬目錄；ticket 相關者放進對應 ticket 的設計資料夾，例如 `design/{ticket-id}`。
