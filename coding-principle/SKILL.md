---
name: coding-principle
description: Use when writing or reviewing code structure, naming, function boundaries, method visibility, and class organization.
---

# Coding Principle

用於撰寫或 review 程式碼。

## 規則

- Follow clean code 原則，優先確保命名清楚、降層明確、程式由上往下像讀報紙一樣容易閱讀。
- Function / method 應只處理同一個抽象層次；高層 function 描述流程，低層 function 處理細節，避免在同一段程式混合流程控制、資料轉換、外部呼叫和低階實作。
- Function / method 應加上 typing，包含參數與 return type；若型別來自外部套件或動態物件，優先使用既有專案可 import 的具體型別。
- Function / method 原則上保持短小，約 20-30 行內較容易閱讀；超過 40 行時應檢查是否混合多個抽象層次或職責。
- 多條件判斷時，優先考慮用 guard clause 先處理可以直接結束的條件，避免不必要的巢狀流程。
- 單一檔案原則上保持聚焦，約 300 行內較容易維護；超過 500 行時應檢查是否需要依職責拆分。
- Class 內 method 擺放順序為 public 在上，protected / private 在下，並依閱讀順序排列被呼叫的細節。
- 預設不寫 function / method docstring；只有當程式碼本身難以直接看出行為、需要補充業務語意、限制、假設或副作用時才寫。
- 新增抽象前，先確認它能降低閱讀成本、移除實際重複或對齊既有架構。

## 命名規則

- Function / method 命名要表達同一層抽象的行為意圖，預設用動詞開頭。
- Class / file / module 命名要表達身份或職責，預設用名詞。
- Airflow `task_id` 表示 workflow step，預設用動詞開頭，例如 `build-*`、`create-*`、`run-*`。
