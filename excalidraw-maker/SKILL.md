---
name: excalidraw-maker
description: Use when creating, editing, restructuring, reviewing, or validating Excalidraw files. Follow a single workflow from intent to delivery: understand intent, model semantics, compose layout, route relationships, then validate and deliver with the required review workflow before overwriting formal Excalidraw files.
---

# Excalidraw Maker

用於建立、修改、重構與驗證 Excalidraw 圖檔。核心任務不是移動元素，而是把使用者想表達的概念、流程、系統、關係或視覺重點，轉成語意清楚、版面可讀、可 review、可維護的 `.excalidraw` artifact。

## Workflow

處理 Excalidraw 時，使用同一套 workflow：

1. Understand Intent
2. Model Semantics
3. Compose Layout
4. Route Relationships
5. Validate And Deliver

不要另外建立平行的思考模型或流程。所有規則都應歸入這五步。

## 1. Understand Intent

先理解這張圖要完成什麼，而不是直接改元素。

必須釐清：

- 使用者要表達的業務、技術、流程、概念、關係或視覺重點
- 讀者是誰，以及讀者應該先看哪裡、再看哪裡
- 是要從零建立、修改既有圖、重構圖面，還是只做限定範圍調整
- 是否有指定限制，例如只改顏色、只改線條、只改 label、只調整特定區塊
- 是否有既有圖面規則需要沿用

需求不明確時先釐清，不要猜圖面語意，也不要只在既有圖上做局部搬移。

## 2. Model Semantics

先建立圖面的語意系統，再建立或修改元素。

必須定義或維持：

- 元素分類，例如節點、父框、子框、群組、泳道、legend、註解、label block
- 父子框關係，以及每個父框代表的範圍或分類
- 顏色、框線、線條樣式、箭頭樣式與位置規則的語意
- 連線方向代表資料流、控制流、關聯方向，或其他使用者指定語意
- label 命名規則與粒度，例如 driver path、DAG app name、分類名稱或使用者指定格式
- 字體統一使用 Comic Shanns；新增或修改文字元素時必須維持此字體，除非使用者明確指定其他字體。
- legend 和註解只解釋圖面規則，不應承載主流程

同類元素要使用一致的樣式或位置規則。父框、顏色、線條與 label 都應該有可說明的語意，不要只作裝飾。

## 3. Compose Layout

版面要服務閱讀順序與語意分層。

必須確保：

- 整體方向清楚，例如由左到右、由上到下，或符合使用者指定方向
- 主要流程、支線、例外、legend、註解各自有清楚區域
- 父框完整包住自己的子框、元素與文字
- 子圖、legend、文字或節點不跑出父框邊界
- 元素之間有足夠留白，避免視覺黏在一起
- 文字放得下，不截斷、不溢出、不被其他元素遮住
- 長 label 需要換行、加寬節點或調整版面
- 整體對齊與間距足夠穩定，讓使用者不用猜元素歸屬

如果圖面看起來已經混亂，應先重整版面，而不是繼續加元素。

## 4. Route Relationships

連線與箭頭要讓關係更清楚，不能製造新的混淆。

必須確保：

- 箭頭方向符合資料流、控制流、關聯方向或使用者指定語意
- 箭頭不穿過非目標元素內部
- 箭頭不穿過 label block
- 箭頭不造成節點歸屬或流程方向混淆
- 線路太複雜時，應重排元素、拆分區域、增加中繼節點，或改用更清楚的分流方式
- label 與箭頭保持可讀距離，不覆蓋節點或其他連線

連線不是單純把兩點接起來；它必須維持整張圖的語意與閱讀秩序。

## 5. Validate And Deliver

交付前必須同時做自動驗證與人工圖面檢查。不能只驗證 JSON 格式。

自動驗證至少檢查：

- `.excalidraw` JSON 格式有效
- 必要元素存在
- 父框與子元素的邊界關係合理
- 文字是否可能超出自身元素
- review 檔名編號是否符合目前目錄實際狀態
- 若是限定範圍修改，非目標元素或非目標屬性沒有變更

人工檢查至少確認：

- 圖面整體方向、分層、線路、留白、對齊與可讀性合理
- 父框完整包住自己的子框、元素與文字
- 文字沒有截斷、溢出或被遮住
- 箭頭沒有穿過不該穿過的元素或 label block
- legend、註解或說明文字位於獨立且足夠寬的區域
- legend 和註解不覆蓋主流程、不被截斷、不與父框交疊
- 每個 label 符合使用者指定格式

若自動驗證只能檢查部分條件，必須明確補上人工檢查。若無法可靠驗證圖面品質，必須先 raise issue，不可交付低品質圖檔。

## Formal File Review

修改正式 `.excalidraw` 前，必須先產生 review artifact，取得使用者明確同意後才可以覆蓋正式檔案。

review 前必須先列出：

- 目前正式圖檔檔名
- 同目錄既有、同 base name 的 review 圖檔

review 圖檔規則：

- 檔名格式為 `{原檔名}-review-{num}.excalidraw`
- 下一個編號只能根據目前目錄實際存在、同 base name 的 review 圖檔決定
- 若同目錄沒有既有 review 圖檔，下一版就是 `review-1`
- 不可根據對話歷史或已刪除檔案推算編號
- review 圖檔不可覆蓋上一版

diff review 規則：

- 先產生 review 用 before / after 暫存檔
- 用 `code --diff <before> <after>` 開啟 VSCode diff
- 不要只提供 unified diff 或同一畫面交錯的文字 diff
- 使用者明確同意後，才可以覆蓋正式 `.excalidraw`

## Delivery Report

交付 review 時，至少回報：

- 正式圖檔路徑
- 新產生的 review 圖檔路徑
- VSCode diff 是否已開啟
- 自動驗證結果
- 人工檢查結果
- 若是限定範圍修改，非目標元素或屬性是否保持不變
- 是否等待使用者同意後再覆蓋正式檔案
