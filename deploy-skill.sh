#!/bin/bash

SKILL_NAME=$1

ln -sfn "/Users/lillard/side-project/agent-skills/$SKILL_NAME" "/Users/lillard/.agents/skills/$SKILL_NAME"
ln -sfn "/Users/lillard/side-project/agent-skills/$SKILL_NAME" "/Users/lillard/.claude/skills/$SKILL_NAME"
