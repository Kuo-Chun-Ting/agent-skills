---
name: git
description: Git commit 操作輔助。觸發詞：「幫我 commit」、「commit 一版」、「commit」。
---

## commit

使用者要求 commit 時：

1. 先列出本次可能要 commit 的變更與檔案，請使用者確認範圍。
2. 使用者確認後，stage 該範圍。
3. 執行 `git diff --cached`，根據 staged diff 提供簡潔的英文 commit message。
4. 使用者確認 commit message 後，執行 commit。
