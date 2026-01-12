#!/usr/bin/env bash
set -euo pipefail

# Commit message (default: timestamp)
MSG="${1:-"Update: $(date '+%F %T')"}"

# Stage all changes
git add -A

# Commit if there are staged changes
if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "$MSG"
fi

# Push to current branch
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
git push -u origin "$CURRENT_BRANCH"
