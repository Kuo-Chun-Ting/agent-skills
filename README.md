# agent-skills

A collection of skills for Claude Code and Codex.

## Deploy a skill

```bash
./deploy-skill.sh <skill-name>
```

Example:

```bash
./deploy-skill.sh skill-writer
```

This creates symlinks in `~/.agents/skills/` and `~/.claude/skills/` that point to the skill folder in this repository.
