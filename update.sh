#!/usr/bin/env bash
set -euo pipefail

# Repository root (directory where this script lives)
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

# Commit message
MSG="${1:-"Update data: $(date '+%F %T')"}"

# Stage all changes
git add -A

# Commit if there are changes
if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "$MSG"
fi

# Pull (in case repo already exists remotely)
if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  git pull --rebase || git pull
else
  echo "No upstream branch set yet."
fi

# Push
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
git push -u origin "$CURRENT_BRANCH"