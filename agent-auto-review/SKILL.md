---
name: agent-auto-review
description: Use when a task output should be reviewed by another agent before the author finishes. Supports configurable author/reviewer agents, max rounds, audit files, and Stop hook gating.
---

# Agent Auto Review

用於單一任務或單一被審目標的跨 agent review gate。

## 啟動參數

- `topic`：本次 review 的人可讀名稱，用於 `.auto-review/<topic>/`。
- `target`：被審目標，可以是調查結論、設計、文件、程式碼、測試或分析結果。
- `max_rounds`：最多 review 輪數；未指定時使用 `3`。
- `reviewer_agent`：reviewer agent；未指定時使用另一個 agent。

作者與 reviewer 是角色，不綁定固定 agent。使用者明確指定 reviewer 時照指定；未指定時，Codex 作者使用 Claude reviewer，Claude 作者使用 Codex reviewer。只有使用者明確指定時才使用同型 review。

review 與 response 的語言及內容遵循 `agent-cross-review` 的「內容規範」；本 Skill 不重複定義。

## Harness 腳本

固定腳本位置：

```text
/Users/lillard/side-project/agent-skills/agent-auto-review/scripts/
```

- `stop_hook.py`：Stop hook gate。
- `start_reviewer_session.py`：協調 reviewer 啟動或續接，並寫入 reviewer audit 與 review state。
- `new_claude_session.py`：建立新的 Claude reviewer session。
- `new_codex_session.py`：建立新的 Codex reviewer session。
- `resume_claude_session.py`：續接既有 Claude reviewer session。
- `resume_codex_session.py`：續接既有 Codex reviewer session。

reviewer 不取得寫檔權限。Claude reviewer 停用 tools；Codex reviewer 使用 read-only sandbox。

## Runtime 檔案

每次啟動只建立同一組 runtime 檔案：

```text
.auto-review/<topic>/review.json
.auto-review/<topic>/target.md
.auto-review/<topic>/reviewed_by_<reviewer>.md
.auto-review/<topic>/responsed_by_<author>.md
```

`.auto-review/**` 是本 skill 的 runtime state / audit，不是正式交付內容。

`review.json` 範例：

```json
{
  "session_id": "<current-author-session-id>",
  "author_agent": "codex",
  "reviewer_agent": "claude",
  "topic": "...",
  "target": ".auto-review/<topic>/target.md",
  "status": "pending",
  "round": 1,
  "max_rounds": 3,
  "reviewer_session_id": "",
  "created_at": "...",
  "updated_at": "..."
}
```

`session_id` 是目前作者 session 的 harness 抽象，必須由作者在建立 runtime state 時寫入且不可為空。Codex 作者使用 `CODEX_THREAD_ID`；Claude 作者使用 `CLAUDE_CODE_SESSION_ID`。Stop hook 只處理 `session_id` 等於目前 session 的 review state。

## 流程

1. 建立 `.auto-review/<topic>/review.json`，`status` 為 `pending`。
2. 作者把本輪完整被審目標寫入 `.auto-review/<topic>/target.md`，並讓 `review.json.target` 指向此檔案。
   若 target 是計畫、文件、調查結論或回答草稿，`target.md` 直接包含完整內容。
   若 target 是程式碼或多檔案修改，`target.md` 作為 review manifest，列出修改目標、檔案清單、重要 diff / commit / 測試結果與 reviewer 審查重點。
3. 作者把 `target.md`、上下文、`agent-cross-review` 的內容規範與 `topic` 寫入 prompt file，執行 `start_reviewer_session.py <reviewer_agent> <topic> <prompt_file>`。
4. reviewer 依 prompt 回傳標準 review result，不直接修改 `.auto-review/**`。
5. `start_reviewer_session.py` 寫入 `reviewed_by_<reviewer>.md`、`review.json.status`、`reviewer_session_id` 與 `updated_at`。
6. `status` 為 `pending` 時，作者修改 `target.md`，並依 `agent-cross-review` 的內容規範更新 response audit；增加 `round` 後續接同一個 reviewer session。
7. 持續迭代，直到 reviewer 認可或達到 `max_rounds`。作者不得自行把 `status` 改成 `approved`。
8. Stop hook 依 review state 決定阻擋或放行。

## Reviewer Session

- `session_id` 是作者 session，供 Stop hook 判斷目前 review state 是否屬於當前作者；不可用來 resume reviewer。
- `reviewer_session_id` 是 reviewer session，由 `start_reviewer_session.py` 管理。
- 啟動 reviewer 時，呼叫端只傳 `<reviewer_agent> <topic> <prompt_file>`；不可傳外部 session id。
- launcher 參數的 reviewer 必須等於 `review.json.reviewer_agent`。
- `reviewer_session_id` 有值時呼叫對應的 resume helper；為空時呼叫對應的 new helper。
- new 與 resume helper 都必須回傳相同的標準 JSON：`{"session_id":"...","status":"approved|pending","review":"..."}`。
- resume helper 回傳的 `session_id` 必須等於既有 `reviewer_session_id`。
- 無法解析 result、欄位為空或 status 不合法時，launcher 必須失敗且不得更新 review state。
- Codex reviewer 與 Claude reviewer 使用相同 launcher contract；agent CLI 的差異只能封裝在各自 new / resume helper 內。

## Stop Hook Gate

作者 agent 要結束 turn 時，Stop hook 會讀 `.auto-review/*/review.json`，只處理 `session_id` 等於目前 session 的 review state。

- 找不到對應 review state：放行。
- `status` 不是 `approved` 或 `pending`：以不預期狀態失敗。
- `status = approved`：放行。
- `status = pending` 且 `round >= max_rounds`：放行。
- `status = pending` 且 `round < max_rounds`：block，要求作者回到 review 流程。

Stop hook 只負責阻擋與放行，不審查內容，也不修改 review state。

## Agent 對應

### Codex

- Codex 當作者時，`session_id` 使用 `CODEX_THREAD_ID`；用 Codex Stop hook 做 gate，hook 設定放 `~/.codex/hooks.json`。
- Codex 啟動 reviewer 時，用 `python3 /Users/lillard/side-project/agent-skills/agent-auto-review/scripts/start_reviewer_session.py <reviewer_agent> <topic> <prompt_file>`。
- `reviewer_agent` 是 `claude` 時，launcher process 必須用 `require_escalated` 執行；Claude reviewer 本身仍不取得 tools。

### Claude

- Claude 當作者時，`session_id` 使用 `CLAUDE_CODE_SESSION_ID`；用 Claude Stop hook 做 gate，hook 設定放 `~/.claude/settings.json`。
- Claude 啟動 reviewer 時，用 `python3 /Users/lillard/side-project/agent-skills/agent-auto-review/scripts/start_reviewer_session.py <reviewer_agent> <topic> <prompt_file>`。

## 正式內容

- 正式交付內容只保留最終可執行結論。
- audit 檔可保存 review 過程。
- 正式文件或 skill body 不可混入 review 過程。
