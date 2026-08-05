---
name: modify-content
description: Use before modifying any persistent file or resource.
---

以下會改變正式檔案或持久化資源的操作視為修改：新增、編輯、刪除、覆蓋、搬移或重新命名檔案，變更設定、skill、文件或程式碼，以及透過 connector 建立、更新、刪除或送出持久化資源。

## 免確認產物

以下寫入不需準備 diff 或取得使用者同意：

- 僅供修改預覽使用的私人暫存檔，包括 before / after 檔案。
- Agent review 的通訊與執行紀錄：
  - `*_reviewed_by_<agent>.md`
  - `*_responsed_by_<agent>.md`
  - `.auto-review/**`

## 修改前

- 說明正式目標、預計變更與完成後的樣子。
- 修改文字檔時，將修改前內容寫入 before 暫存檔，將預計修改後內容寫入 after 暫存檔，再執行 `code --diff <before> <after>`。
- 新增文字檔時，before 暫存檔留白；刪除文字檔時，after 暫存檔留白。
- 同一批有多個文字檔時，所有 before 與 after 檔案放在同一個暫存目錄並使用不同檔名；前一個 diff 開啟完成後，再依序為其餘檔案各執行一次 `code --diff <before> <after>`。
- 無法以文字 diff 呈現時，說明原因並提供可確認的替代方式。
- 顯示 diff 後，取得使用者對該 diff 的明確同意；先前對計畫、方向或檔案範圍的同意不能取代這一步。

## 修改與驗證

- 同意前，不得變更正式目標或執行會間接寫入它的操作。
- 同意後，只套用已確認的變更；發現額外需求時，重新確認。
- 完成後，確認結果符合已同意的內容，且沒有額外變更；回報目標與驗證結果。
