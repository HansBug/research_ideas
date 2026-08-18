#!/usr/bin/env bash
# Orchestrator: runs run_review.sh in parallel over all pool ids.
#
# Idempotent: skips already-valid results/<id>.json.
# Retries: pass --retry to re-attempt any FAIL rows once.
#
# Usage:
#   orchestrate.sh [-j N] [--retry] [--only ID1,ID2,...]

set -uo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
POOL="$ROOT/pool.tsv"
JOBS="${JOBS:-6}"
ONLY=""
RETRY=0

while [ $# -gt 0 ]; do
  case "$1" in
    -j) JOBS="$2"; shift 2 ;;
    --retry) RETRY=1; shift ;;
    --only) ONLY="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

mkdir -p "$ROOT/results" "$ROOT/logs"

# Build id list
if [ -n "$ONLY" ]; then
  ID_LIST=$(echo "$ONLY" | tr ',' '\n')
else
  ID_LIST=$(awk -F'\t' 'NR>1 {print $1}' "$POOL")
fi

# Filter: skip ids whose result already valid (unless --retry to force re-process FAIL)
PENDING=$(while IFS= read -r id; do
  out="$ROOT/results/$id.json"
  if [ -f "$out" ] && jq -e '.case_id and .axes.C1_dead_end_potential.score and .verdict' "$out" >/dev/null 2>&1; then
    continue
  fi
  echo "$id"
done <<< "$ID_LIST")

TOTAL_PENDING=$(echo "$PENDING" | grep -c .)
TOTAL_ALL=$(echo "$ID_LIST" | grep -c .)
DONE_BEFORE=$((TOTAL_ALL - TOTAL_PENDING))

echo "==== orchestrate: $TOTAL_ALL total / $DONE_BEFORE already done / $TOTAL_PENDING pending / jobs=$JOBS ===="

if [ "$TOTAL_PENDING" -eq 0 ]; then
  echo "All done. Nothing to do."
  exit 0
fi

# Run in parallel
echo "$PENDING" | xargs -n1 -P"$JOBS" -I{} bash "$ROOT/run_review.sh" "{}"

# Final tally
DONE_AFTER=$(find "$ROOT/results" -name "*.json" 2>/dev/null | wc -l)
echo "==== orchestrate done: results = $DONE_AFTER / $TOTAL_ALL ===="
