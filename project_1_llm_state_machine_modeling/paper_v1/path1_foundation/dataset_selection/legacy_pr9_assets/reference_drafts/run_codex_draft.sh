#!/usr/bin/env bash
# PATH1 — Per-case codex ref-DSL draft runner.
# Usage:  run_codex_draft.sh <sample_id>
#
# Reads pool.tsv (in ../expansion/) + expansions/<id>.json (the expanded NL),
# renders codex prompt, invokes codex with Bash tool access so it can
# iteratively verify via verify_pyfcstm.py + extract_components.py.
# Expects codex to write OUTPUT_FCSTM + OUTPUT_COMPONENTS + OUTPUT_NOTES,
# then re-runs final independent verification.

set -uo pipefail

ID="${1:-}"
[ -z "$ID" ] && { echo "usage: $0 <sample_id>" >&2; exit 1; }

ROOT="$(cd "$(dirname "$0")" && pwd)"          # selection/ref_stms/
SEL_ROOT="$(cd "$ROOT/.." && pwd)"             # selection/
EXP_ROOT="$SEL_ROOT/expansion"                 # selection/expansion/
REPO_ROOT="$(cd "$ROOT/../../../.." && pwd)"   # repo root

POOL="$EXP_ROOT/pool.tsv"
TPL="$ROOT/prompts/codex_draft_template.md"
OUTPUT_FCSTM="$ROOT/codex_drafts/$ID.fcstm"
OUTPUT_COMPONENTS="$ROOT/codex_drafts/$ID.ref_components.json"
OUTPUT_NOTES="$ROOT/codex_drafts/$ID.notes.md"
OUTPUT_RESULT="$ROOT/codex_drafts/$ID.result.json"
LOG="$ROOT/verifier_logs/$ID.codex.log"
RAW="$ROOT/verifier_logs/$ID.codex.raw"
STATUS_FILE="$ROOT/status_codex.tsv"
GRAMMAR_REF="$REPO_ROOT/project_1_llm_state_machine_modeling/method/prompts/_pyfcstm_grammar.md"
EXPANSION="$EXP_ROOT/expansions/$ID.json"

# Skip if cached + verified
if [ -f "$OUTPUT_FCSTM" ] && [ -f "$OUTPUT_COMPONENTS" ] && [ -f "$OUTPUT_RESULT" ] && [ -f "$OUTPUT_NOTES" ]; then
  if cd "$REPO_ROOT" && source venv/bin/activate && \
     python3 "$ROOT/verify_pyfcstm.py" "$OUTPUT_FCSTM" >/dev/null 2>&1; then
    echo "[$ID] CACHED OK"
    exit 0
  fi
fi
rm -f "$OUTPUT_FCSTM" "$OUTPUT_COMPONENTS" "$OUTPUT_NOTES" "$OUTPUT_RESULT"

# Look up pool row
ROW=$(awk -F'\t' -v id="$ID" 'NR>1 && $1==id {print; exit}' "$POOL")
if [ -z "$ROW" ]; then
  echo "[$ID] ERROR: id not in pool ($POOL)" >&2; exit 2
fi
IFS=$'\t' read -r RID BUCKET SLUG CASENAME STM_REL PDF_REL TXT_REL PAPERNO DOMAIN <<< "$ROW"

STM="$REPO_ROOT/$STM_REL"
PDF="$REPO_ROOT/$PDF_REL"
TXT="$REPO_ROOT/$TXT_REL"

for f in "$STM" "$PDF" "$TXT" "$EXPANSION" "$TPL" "$GRAMMAR_REF"; do
  [ -f "$f" ] || { echo "[$ID] ERROR: missing $f" >&2; exit 3; }
done

CASENAME_ESC=$(printf '%s' "$CASENAME" | sed 's/[\\/&]/\\&/g')
DOMAIN_ESC=$(printf '%s' "$DOMAIN" | sed 's/[\\/&]/\\&/g')

PROMPT_FILE="$ROOT/verifier_logs/$ID.codex.prompt"
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
  -e "s|{{REPO_ROOT}}|$REPO_ROOT|g" \
  -e "s|{{OUTPUT_FCSTM}}|$OUTPUT_FCSTM|g" \
  -e "s|{{OUTPUT_COMPONENTS}}|$OUTPUT_COMPONENTS|g" \
  -e "s|{{OUTPUT_NOTES}}|$OUTPUT_NOTES|g" \
  -e "s|{{OUTPUT_RESULT}}|$OUTPUT_RESULT|g" \
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

# Extract codex's final JSON to OUTPUT_RESULT
python3 - "$RAW" "$OUTPUT_RESULT" "$ID" <<'PY'
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
    sys.stderr.write(f"[{cid}] no agent_message\n"); sys.exit(5)
text = final.strip()
if text.startswith("```"):
    nl = text.find("\n")
    if nl >= 0: text = text[nl+1:]
    if text.rstrip().endswith("```"): text = text.rstrip()[:-3]
text = text.strip()
try:
    data = json.loads(text)
except Exception as e:
    sys.stderr.write(f"[{cid}] JSON parse fail: {e}\nhead: {text[:300]}\n"); sys.exit(7)
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

if [ ! -f "$OUTPUT_FCSTM" ]; then
  echo "[$ID] FAIL: codex didn't write $OUTPUT_FCSTM" >&2
  echo -e "$ID\tFAIL\t$DUR\tno_dsl_file" >> "$STATUS_FILE"
  exit 8
fi

# Independent final verification (parse + sem + sim_smoke)
source venv/bin/activate
VERIFY_OUT=$(python3 "$ROOT/verify_pyfcstm.py" "$OUTPUT_FCSTM" 2>&1)
VERIFY_RC=$?
echo "$VERIFY_OUT" > "$ROOT/verifier_logs/$ID.final_verify.log"

# Independent 5-component IR extraction
if [ $VERIFY_RC -eq 0 ]; then
  EXTRACT_OUT=$(python3 "$ROOT/extract_components.py" "$ID" "$OUTPUT_FCSTM" "$OUTPUT_COMPONENTS" 2>&1)
  EXTRACT_RC=$?
  echo "$EXTRACT_OUT" >> "$ROOT/verifier_logs/$ID.final_verify.log"
else
  EXTRACT_RC=99
fi

if [ $VERIFY_RC -ne 0 ] || [ $EXTRACT_RC -ne 0 ]; then
  echo "[$ID] WARN: final verify/extract fail verify_rc=$VERIFY_RC extract_rc=$EXTRACT_RC — output kept for inspection" >&2
  echo -e "$ID\tPARTIAL\t$DUR\tverify_rc=$VERIFY_RC,extract_rc=$EXTRACT_RC" >> "$STATUS_FILE"
fi

echo -e "$ID\tOK\t$DUR\t-" >> "$STATUS_FILE"
echo "[$ID] codex OK dur=${DUR}s verify_rc=$VERIFY_RC extract_rc=$EXTRACT_RC"
