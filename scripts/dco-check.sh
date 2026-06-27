#!/usr/bin/env bash
# DCO check for pre-push hook
# Validates all commits being pushed have Signed-off-by trailer

set -e

# Get commits between remote and local
commits=$(git log --oneline @{push}..HEAD 2>/dev/null || git log --oneline HEAD)

if [ -z "$commits" ]; then
  exit 0
fi

echo "$commits" | while read -r hash msg; do
  if ! git log -1 --format="%(trailers)" "$hash" | grep -qi "Signed-off-by:"; then
    echo "❌ Commit $hash ($msg) missing Signed-off-by"
    exit 1
  fi
done
