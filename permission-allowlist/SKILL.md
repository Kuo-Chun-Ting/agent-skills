---
name: permission-allowlist
description: 在撰寫或整理 agent、工具或服務的權限白名單時使用。
---

- 白名單分兩層由通用到特定排序：
  1. 不同工具或指令依適用範圍排序，例如 `WebFetch` → `ls` → Git → `npm` → Vitest。
  2. 同一工具或指令依匹配範圍排序，例如 `Bash(git *)` → `Bash(git status *)` → `Bash(git status)`。
- `Bash(...)` 的第一層以括號內指令判斷；無法比較時維持原順序。
- 未要求清理時，只排序，不刪除或改寫規則。
