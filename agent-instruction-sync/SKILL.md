---
name: agent-instruction-sync
description: Use when creating, editing, or deploying custom agent instructions or skills shared by Codex and Claude.
---

## Agent 指令

- Project-level 指令同步同一個 project 的 `AGENTS.md` 與 `CLAUDE.md`。
- Global-level 指令同步 `~/.codex/AGENTS.md` 與 `~/.claude/CLAUDE.md`。
- 兩個 agent 需要不同內容時，先提出差異並取得使用者同意。

## 自定義 skill

- 唯一實體來源是 `/Users/lillard/side-project/agent-skills/{skill_name}`。
- Codex 使用 `~/.agents/skills/{skill_name}` 指向實體來源的 symlink。
- Claude 使用 `~/.claude/skills/{skill_name}` 指向實體來源的 symlink。
- 新增或部署 skill 時，在 repo 執行 `./deploy-skill.sh {skill_name}`。
- 修改 skill 時直接修改實體來源；部署路徑只需確認 symlink。

## 驗證

- Agent 指令：讀回兩個目標並確認內容符合各自格式。
- 自定義 skill：確認兩個 symlink 指向實體來源，並從兩個部署路徑讀回相同內容。
- 回報實際修改的檔案與驗證結果。
