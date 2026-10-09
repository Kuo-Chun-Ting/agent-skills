---
name: test-principle
description: Use when writing or reviewing tests at any level.
---

- 選擇測試層級時，使用能重現問題並驗證結果的最低層級；需要真實視窗、焦點或滑鼠操作時，才使用 GUI／E2E。
- 重複同一操作前，確認後續操作能驗證什麼額外問題；沒有明確目的時，只執行一次。
- 等待非同步結果時，以結果成立為條件並設定逾時，不用固定延遲判定成功。
