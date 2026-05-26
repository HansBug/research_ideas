#!/usr/bin/env bash
# Per-case codex draft runner.
# Usage:  run_codex_draft.sh <id>
#
# Reads pool.tsv + expansions/<id>.json, renders codex prompt,
# invokes codex with Bash tool access for self-validation,
# expects codex to write OUTPUT_FCSTM + OUTPUT_NOTES files.
# Final validation: re-run verify_pyfcstm on the output to confirm.

set -uo pipefail

ID="${1:-}"
[ -z "$ID" ] && { echo "usage: $0 <id>" >&2; exit 1; }

ROOT="$(cd "$(dirname "$0")/.." && pwd)"   # path2_selection/
REPO_ROOT="$(cd "$ROOT/../../../.." && pwd)"
POOL="$ROOT/pool.tsv"
TPL="$ROOT/ref_stms/prompts/codex_draft_template.md"
OUTPUT_FCSTM="$ROOT/ref_stms/codex_drafts/$ID.fcstm"
OUTPUT_SCENARIOS="$ROOT/ref_stms/codex_drafts/$ID.scenarios.json"
OUTPUT_NOTES="$ROOT/ref_stms/codex_drafts/$ID.notes.md"
LOG="$ROOT/ref_stms/verifier_logs/$ID.codex.log"
RAW="$ROOT/ref_stms/verifier_logs/$ID.codex.raw"
STATUS_FILE="$ROOT/ref_stms/status_codex.tsv"
FINAL_JSON="$ROOT/ref_stms/codex_drafts/$ID.result.json"
GRAMMAR_REF="$REPO_ROOT/project_1_llm_state_machine_modeling/method/prompts/_pyfcstm_grammar.md"

# Skip if cached + full-verified (smoke + scenarios)
if [ -f "$OUTPUT_FCSTM" ] && [ -f "$OUTPUT_SCENARIOS" ] && [ -f "$FINAL_JSON" ] && [ -f "$OUTPUT_NOTES" ]; then
  if cd "$REPO_ROOT" && source venv/bin/activate && \
     python3 "$ROOT/ref_stms/verify_pyfcstm_full.py" "$OUTPUT_FCSTM" "$OUTPUT_SCENARIOS" >/dev/null 2>&1; then
    echo "[$ID] CACHED OK"
    exit 0
  fi
fi
rm -f "$OUTPUT_FCSTM" "$OUTPUT_SCENARIOS" "$OUTPUT_NOTES" "$FINAL_JSON"

# Look up row
ROW=$(awk -F'\t' -v id="$ID" 'NR>1 && $1==id {print; exit}' "$POOL")
if [ -z "$ROW" ]; then
  echo "[$ID] ERROR: id not in pool" >&2; exit 2
fi
IFS=$'\t' read -r RID BUCKET SLUG CASENAME STM_REL PDF_REL TXT_REL PAPERNO DOMAIN <<< "$ROW"

STM="$REPO_ROOT/$STM_REL"
PDF="$REPO_ROOT/$PDF_REL"
TXT="$REPO_ROOT/$TXT_REL"
EXPANSION="$ROOT/expansions/$ID.json"

for f in "$STM" "$PDF" "$TXT" "$EXPANSION" "$TPL" "$GRAMMAR_REF"; do
  [ -f "$f" ] || { echo "[$ID] ERROR: missing $f" >&2; exit 3; }
done

CASENAME_ESC=$(printf '%s' "$CASENAME" | sed 's/[\\/&]/\\&/g')
DOMAIN_ESC=$(printf '%s' "$DOMAIN" | sed 's/[\\/&]/\\&/g')

PROMPT_FILE="$ROOT/ref_stms/verifier_logs/$ID.codex.prompt"
sed \
  -e "s|{{CASE_ID}}|$ID|g" \
  -e "s|{{CASE_NAME}}|$CASENAME_ESC|g" \
  -e "s|{{BUCKET}}|$BUCKET|g" \
  -e "s|{{DOMAIN}}|$DOMAIN_ESC|g" \
  -e "s|{{STM_PATH}}|$STM|g" \
  -e "s|{{EXPANSION_PATH}}|$EXPANSION|g" \
  -e "s|{{PAPER_PDF}}|$PDF|g" \
  -e "s|{{PAPER_CONTENT}}|$TXT|g" \
  -e "s|{{GRAMMAR_REF_PATH}}|$GRAMMAR_REF|g" \
  -e "s|{{OUTPUT_FCSTM}}|$OUTPUT_FCSTM|g" \
  -e "s|{{OUTPUT_SCENARIOS}}|$OUTPUT_SCENARIOS|g" \
  -e "s|{{OUTPUT_NOTES}}|$OUTPUT_NOTES|g" \
  "$TPL" > "$PROMPT_FILE"

cd "$REPO_ROOT"
START=$(date +%s)
timeout 1800 codex exec --json --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox < "$PROMPT_FILE" 2>"$LOG" >"$RAW"
RC=$?
END=$(date +%s)
DUR=$((END-START))

if [ $RC -ne 0 ]; then
  echo "[$ID] FAIL rc=$RC dur=${DUR}s" >&2
  echo -e "$ID\tFAIL\t$DUR\trc=$RC" >> "$STATUS_FILE"
  exit 4
fi

# Extract codex's final JSON
python3 - "$RAW" "$FINAL_JSON" "$ID" <<'PY'
import json, sys
raw_path, out_path, cid = sys.argv[1:4]
final = ""
for line in open(raw_path):
    line = line.strip()
    if not line: continue
    try:
        evt = json.loads(line)
    except Exception:
        continue
    if evt.get("type") == "item.completed":
        item = evt.get("item", {}) or {}
        if item.get("type") == "agent_message":
            final = item.get("text", "")
if not final:
    sys.stderr.write(f"[{cid}] no agent_message\n")
    sys.exit(5)
text = final.strip()
if text.startswith("```"):
    nl = text.find("\n")
    if nl >= 0: text = text[nl+1:]
    if text.rstrip().endswith("```"): text = text.rstrip()[:-3]
text = text.strip()
try:
    data = json.loads(text)
except Exception as e:
    sys.stderr.write(f"[{cid}] JSON parse fail: {e}\nhead: {text[:300]}\n")
    sys.exit(7)
data["_meta"] = {"id": cid}
with open(out_path, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"[{cid}] codex JSON parsed")
PY
PARSE_RC=$?
if [ $PARSE_RC -ne 0 ]; then
  echo -e "$ID\tFAIL\t$DUR\tjson_rc=$PARSE_RC" >> "$STATUS_FILE"
  exit 6
fi

# Final independent verification of the written DSL
if [ ! -f "$OUTPUT_FCSTM" ]; then
  echo "[$ID] FAIL: codex didn't write $OUTPUT_FCSTM" >&2
  echo -e "$ID\tFAIL\t$DUR\tno_dsl_file" >> "$STATUS_FILE"
  exit 8
fi

source venv/bin/activate
if [ -f "$OUTPUT_SCENARIOS" ]; then
  VERIFY_OUT=$(python3 "$ROOT/ref_stms/verify_pyfcstm_full.py" "$OUTPUT_FCSTM" "$OUTPUT_SCENARIOS" 2>&1)
else
  VERIFY_OUT=$(python3 "$ROOT/ref_stms/verify_pyfcstm_full.py" "$OUTPUT_FCSTM" 2>&1)
fi
VERIFY_RC=$?
echo "$VERIFY_OUT" > "$ROOT/ref_stms/verifier_logs/$ID.final_verify.log"

if [ $VERIFY_RC -ne 0 ]; then
  echo "[$ID] WARN: final verify fail rc=$VERIFY_RC — output kept for inspection" >&2
  echo -e "$ID\tPARTIAL\t$DUR\tverify_rc=$VERIFY_RC" >> "$STATUS_FILE"
  # Don't exit non-zero — partial outputs may still be useful for human review
fi

echo -e "$ID\tOK\t$DUR\t-" >> "$STATUS_FILE"
echo "[$ID] codex OK dur=${DUR}s verify_rc=$VERIFY_RC"
