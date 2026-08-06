---
name: modify-content
description: Use before modifying persistent files or resources that are not tracked by Git.
---

## 適用範圍

不套用本 skill：

- 修改前已被 Git 追蹤的檔案
- 用於本 skill diff 預覽的 before / after 暫存檔
- Agent review 的通訊與執行紀錄：
  - `*_reviewed_by_<agent>.md`
  - `*_responsed_by_<agent>.md`
  - `.auto-review/**`

必須套用本 skill：

- 修改前未被 Git 追蹤的檔案
- 不屬於 Git worktree 的持久化檔案或資源
- 透過 connector、API 或 UI 建立、更新、刪除或送出的外部持久化資源，包括文件、表單、Sheet 與設定

同一批修改有多種目標時，只對必須套用本 skill 的目標執行本流程。

## 確認前

- 說明修改目標、預計變更與完成後的結果。
- 建立 before / after 暫存檔時，使用 `/private/tmp/modify-content-*/`。
- 修改文字檔時，將目前內容寫入 before 暫存檔，將預計內容寫入 after 暫存檔，再執行 `code --diff <before> <after>`。
- 新增文字檔時，before 暫存檔留白；刪除文字檔時，after 暫存檔留白。
- 同一批有多個文字檔時，將所有暫存檔放在同一個目錄並使用不同檔名，再依序開啟每個 diff。
- 無法以文字 diff 呈現時，說明原因並提供可確認的替代方式。
- 開啟所有 diff 後，取得使用者對該 diff 的明確同意再修改正式目標；對計畫、方向或檔案範圍的同意不能取代此同意。

## 確認後

- 只套用已確認的變更；發現額外需求時，重新執行確認流程。
- 完成後驗證正式目標符合 diff，並回報驗證結果。
