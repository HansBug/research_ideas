#!/usr/bin/env bash
# Reference STM generation orchestrator.
#
# Stages per case:
#   A) codex draft (parse + sem + sim smoke + scenarios full coverage)
#   B) claude cross-review (semantic / faithfulness / C-axis / NL-coverage)
#   D) bundle .md generation
#
# Stage C (revision loop) currently not auto-iterated — claude REVISE comments
# are surfaced in bundle for human audit instead. To re-run after manual
# revision, just re-invoke this script (cache will skip done cases).

set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RS="$ROOT/ref_stms"
SELECTION="$ROOT/selection.json"
JOBS_DRAFT="${JOBS_DRAFT:-4}"
JOBS_REVIEW="${JOBS_REVIEW:-6}"
ONLY=""
STAGE="all"   # all | draft | review | bundle

while [ $# -gt 0 ]; do
  case "$1" in
    -j) JOBS_DRAFT="$2"; JOBS_REVIEW="$2"; shift 2 ;;
    --stage) STAGE="$2"; shift 2 ;;
    --only) ONLY="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

mkdir -p "$RS"/{codex_drafts,claude_reviews,verifier_logs,bundles,audited,prompts}

# Resolve id list
if [ -n "$ONLY" ]; then
  ID_LIST=$(echo "$ONLY" | tr ',' '\n')
else
  ID_LIST=$(python3 -c "
import json
m = json.load(open('$SELECTION'))
for r in m['candidates']:
    print(r['id'])
")
fi
TOTAL=$(echo "$ID_LIST" | grep -c .)

# Stage A: codex draft
if [ "$STAGE" = "all" ] || [ "$STAGE" = "draft" ]; then
  echo "==== Stage A: codex draft ($TOTAL cases, jobs=$JOBS_DRAFT) ===="
  echo "$ID_LIST" | xargs -n1 -P"$JOBS_DRAFT" -I{} bash "$RS/run_codex_draft.sh" "{}"
  echo ""
fi

# Stage B: claude review
if [ "$STAGE" = "all" ] || [ "$STAGE" = "review" ]; then
  echo "==== Stage B: claude review ($TOTAL cases, jobs=$JOBS_REVIEW) ===="
  echo "$ID_LIST" | xargs -n1 -P"$JOBS_REVIEW" -I{} bash "$RS/run_claude_review.sh" "{}"
  echo ""
fi

# Stage D: bundle
if [ "$STAGE" = "all" ] || [ "$STAGE" = "bundle" ]; then
  echo "==== Stage D: bundle generation ($TOTAL cases) ===="
  while IFS= read -r id; do
    python3 "$RS/build_bundle.py" "$id" 2>&1
  done <<< "$ID_LIST"
  echo ""
fi

# Final status dashboard
echo "==== final tally ===="
echo "draft .fcstm: $(find $RS/codex_drafts -name '*.fcstm' | wc -l) / $TOTAL"
echo "draft .scenarios.json: $(find $RS/codex_drafts -name '*.scenarios.json' | wc -l) / $TOTAL"
echo "claude reviews: $(find $RS/claude_reviews -name '*.json' | wc -l) / $TOTAL"
echo "bundles: $(find $RS/bundles -name '*.md' | wc -l) / $TOTAL"
echo "audited (user signed): $(find $RS/audited -name '*.fcstm' 2>/dev/null | wc -l) / $TOTAL"
