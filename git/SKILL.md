---
name: git
description: Git commit 操作輔助。觸發詞：「幫我 commit」、「commit 一版」、「commit」。
---

## commit

使用者要求 commit 時：

1. 執行 `git status --short`，取得所有 staged、unstaged 與 untracked 檔案。
2. 只檢查預計納入 commit 的實際內容：
   - tracked 且 unstaged：`git diff -- <files>`
   - staged：`git diff --cached -- <files>`
   - untracked：直接讀取檔案
3. 根據實際內容決定 commit 範圍與簡潔的英文 commit message。
4. 在同一則訊息列出變更摘要、檔案與 message，請使用者一次確認。
5. 確認後 stage 指定檔案，並以 `git diff --cached` 驗證 staged 內容。
6. staged 內容符合已確認的範圍時直接 commit；若範圍或 message 必須改變，再重新取得一次確認。
