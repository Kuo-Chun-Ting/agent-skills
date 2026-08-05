---
name: unit-test-principle
description: Use when writing or reviewing unit tests. Enforce project unit test naming, structure, fixture usage, and test scope rules.
---

# Unit Test Principle

用於撰寫或 review unit test。

## 規則

- 測試函式命名使用 `test_{function_name}_when_{condition}_then_{expected_result}`。
- 預設使用 top-level function 寫測項；除非使用者指定，才使用 `class TestXxx` grouping。
- 每個測試優先用 3A 註解分段：`# Arrange`、`# Act`、`# Assert`。
- 若測試本身就是驗證例外或 context manager 行為，Act 與 Assert 可以合併成 `# Act & Assert`，避免只有 `# Act` 而漏掉 Assert。
- 優先測有邏輯的 function / method，例如條件判斷、資料轉換、transaction / 呼叫順序、error handling。
- 單純組裝型 function 不需要測內部細節，只要確認 component 被呼叫、重要參數有正確傳遞、對外 contract 沒有斷。
- 只測本次實作的程式邏輯，不測外部工具自己的行為。
- 如果程式會用到外部套件、框架、資料庫、Airflow、Kubernetes、SQL driver 或既有共用元件，只確認本次程式有沒有正確呼叫它們、傳入正確參數或處理回傳結果。
- unit test 不驗證 SQL 檔內容；SQL placeholder、查詢條件和查詢結果應透過 SQL review、DB integration test 或 staging 驗證。
- 測試需要解除外部依賴時，要區分 stub 和 mock：
  - 只需要外部依賴提供回傳值或狀態時，使用 stub，變數命名使用 `stub_` 前綴。
  - 需要驗證外部依賴的呼叫次數、呼叫順序或傳入參數時，使用 mock，變數命名使用 `mock_` 前綴。
  - 解除外部依賴時，優先用 `MagicMock` 建立 stub / mock；命名仍依測試目的使用 `stub_` 或 `mock_` 前綴。
- 如果待測物件在每個測項都需要 stub 或 mock 某些欄位，可以寫 fixture 統一處理，再透過 dependency injection 傳進 test function。
