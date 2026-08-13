#!/bin/sh

set -eu

skill_name=$1
zip -r "${skill_name}.zip" "$skill_name"
