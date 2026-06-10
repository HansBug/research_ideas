#!/usr/bin/env bash
# Expansion orchestrator: runs run_expand.sh in parallel over selection.json (15+15).
#
# Usage: orchestrate_expand.sh [-j N]

set -uo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SELECTION="$ROOT/selection.json"
JOBS="${JOBS:-6}"

while [ $# -gt 0 ]; do
  case "$1" in
    -j) JOBS="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

mkdir -p "$ROOT/expansions" "$ROOT/logs_expand"

# Pull 30 ids out of selection.json
ID_LIST=$(python3 -c "
import json
m = json.load(open('$SELECTION'))
for r in m['candidates'] + m['backup']:
    print(r['id'])
")

TOTAL=$(echo "$ID_LIST" | grep -c .)
DONE=0
PENDING_LIST=""
while IFS= read -r id; do
  out="$ROOT/expansions/$id.json"
  if [ -f "$out" ] && jq -e '.case_id and .expanded_nl and .axis_coverage.C1' "$out" >/dev/null 2>&1; then
    DONE=$((DONE+1))
  else
    PENDING_LIST="$PENDING_LIST $id"
  fi
done <<< "$ID_LIST"

PENDING=$((TOTAL - DONE))
echo "==== expand orchestrator: $TOTAL total / $DONE done / $PENDING pending / jobs=$JOBS ===="

[ $PENDING -eq 0 ] && { echo "All done"; exit 0; }

echo "$PENDING_LIST" | tr ' ' '\n' | grep -v '^$' | xargs -n1 -P"$JOBS" -I{} bash "$ROOT/run_expand.sh" "{}"

DONE_AFTER=$(find "$ROOT/expansions" -name "*.json" 2>/dev/null | wc -l)
echo "==== expand done: $DONE_AFTER / $TOTAL ===="
