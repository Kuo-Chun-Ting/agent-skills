---
name: agent-instructions-writing
description: Use when writing or editing instructions for agents, including AGENTS.md, CLAUDE.md, SKILL.md, project rules, or reusable agent prompts.
---

寫給 agent 的指令時，先套用 `concise-writing`。

1. 每條指令都要指定 agent 何時要做什麼。
2. 不寫「保持品質」、「注意一致性」、「避免錯誤」這類無法直接執行的提醒。
3. 如果規則需要判斷，直接寫判斷條件。
4. 如果規則有例外，直接寫例外條件。
5. 不重複系統層、developer 層或既有 skill 已經規定的通用行為。
6. 在 `SKILL.md` 中，frontmatter 的 `name` 或 `description` 已說明用途時，直接從會改變 agent 行為的內容開始；不要用 H1 或 section 重述。
7. 如果只是偏好而不是硬性規則，寫成偏好；不要偽裝成必須。
8. 如果只適用某種檔案、工具或流程，把適用範圍寫在同一條規則裡。
9. 不寫「為什麼要這樣」；除非原因會影響 agent 選擇。
10. 不寫一次性任務指令；只寫未來會重複使用的規則。
11. 寫完後逐條檢查：如果 agent 看了這條不會改變行為，就刪掉。
