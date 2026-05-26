#!/usr/bin/env bash
# Per-case codex revision runner — fed previous draft + claude REVISE feedback.
# Usage:  run_codex_revise.sh <id>
#
# Outputs revised draft/scenarios/notes IN PLACE (overwrites codex_drafts/<id>.*).
# Previous version archived to codex_drafts/<id>.v1.{fcstm,scenarios.json,notes.md,result.json}.

set -uo pipefail

ID="${1:-}"
[ -z "$ID" ] && { echo "usage: $0 <id>" >&2; exit 1; }

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/../../../.." && pwd)"
POOL="$ROOT/pool.tsv"
TPL="$ROOT/ref_stms/prompts/codex_revise_template.md"
OUTPUT_FCSTM="$ROOT/ref_stms/codex_drafts/$ID.fcstm"
OUTPUT_SCENARIOS="$ROOT/ref_stms/codex_drafts/$ID.scenarios.json"
OUTPUT_NOTES="$ROOT/ref_stms/codex_drafts/$ID.notes.md"
FINAL_JSON="$ROOT/ref_stms/codex_drafts/$ID.result.json"
CLAUDE_REVIEW="$ROOT/ref_stms/claude_reviews/$ID.json"
LOG="$ROOT/ref_stms/verifier_logs/$ID.codex_revise.log"
RAW="$ROOT/ref_stms/verifier_logs/$ID.codex_revise.raw"
STATUS_FILE="$ROOT/ref_stms/status_codex_revise.tsv"
GRAMMAR_REF="$REPO_ROOT/project_1_llm_state_machine_modeling/method/prompts/_pyfcstm_grammar.md"

# Pre-conditions
for f in "$OUTPUT_FCSTM" "$OUTPUT_SCENARIOS" "$OUTPUT_NOTES" "$FINAL_JSON" "$CLAUDE_REVIEW" "$TPL"; do
  [ -f "$f" ] || { echo "[$ID] missing $f" >&2; exit 2; }
done

# Archive previous version
PREV_FCSTM="$ROOT/ref_stms/codex_drafts/$ID.v1.fcstm"
PREV_SCEN="$ROOT/ref_stms/codex_drafts/$ID.v1.scenarios.json"
PREV_NOTES="$ROOT/ref_stms/codex_drafts/$ID.v1.notes.md"
PREV_RES="$ROOT/ref_stms/codex_drafts/$ID.v1.result.json"
[ ! -f "$PREV_FCSTM" ] && cp "$OUTPUT_FCSTM" "$PREV_FCSTM"
[ ! -f "$PREV_SCEN" ] && cp "$OUTPUT_SCENARIOS" "$PREV_SCEN"
[ ! -f "$PREV_NOTES" ] && cp "$OUTPUT_NOTES" "$PREV_NOTES"
[ ! -f "$PREV_RES" ] && cp "$FINAL_JSON" "$PREV_RES"

# Look up row
ROW=$(awk -F'\t' -v id="$ID" 'NR>1 && $1==id {print; exit}' "$POOL")
[ -z "$ROW" ] && { echo "[$ID] not in pool" >&2; exit 3; }
IFS=$'\t' read -r RID BUCKET SLUG CASENAME STM_REL PDF_REL TXT_REL PAPERNO DOMAIN <<< "$ROW"
STM="$REPO_ROOT/$STM_REL"
PDF="$REPO_ROOT/$PDF_REL"
EXPANSION="$ROOT/expansions/$ID.json"

CASENAME_ESC=$(printf '%s' "$CASENAME" | sed 's/[\\/&]/\\&/g')

PROMPT_FILE="$ROOT/ref_stms/verifier_logs/$ID.codex_revise.prompt"
sed \
  -e "s|{{CASE_ID}}|$ID|g" \
  -e "s|{{CASE_NAME}}|$CASENAME_ESC|g" \
  -e "s|{{STM_PATH}}|$STM|g" \
  -e "s|{{EXPANSION_PATH}}|$EXPANSION|g" \
  -e "s|{{PAPER_PDF}}|$PDF|g" \
  -e "s|{{PREVIOUS_FCSTM}}|$PREV_FCSTM|g" \
  -e "s|{{PREVIOUS_SCENARIOS}}|$PREV_SCEN|g" \
  -e "s|{{PREVIOUS_NOTES}}|$PREV_NOTES|g" \
  -e "s|{{CLAUDE_REVIEW}}|$CLAUDE_REVIEW|g" \
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
except Exception:
    # missing close brace?
    opens = text.count("{"); closes = text.count("}")
    if opens > closes:
        try:
            data = json.loads(text + "}"*(opens-closes))
        except Exception as e:
            sys.stderr.write(f"[{cid}] JSON fail even after brace fix: {e}\nhead: {text[:300]}\n")
            sys.exit(7)
    else:
        sys.stderr.write(f"[{cid}] JSON parse fail\nhead: {text[:300]}\n")
        sys.exit(7)
data["_meta"] = {"id": cid, "revision": True}
with open(out_path, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"[{cid}] codex revise OK; revision_round={data.get('revision_round')}")
PY
PARSE_RC=$?
if [ $PARSE_RC -ne 0 ]; then
  echo -e "$ID\tFAIL\t$DUR\tjson_rc=$PARSE_RC" >> "$STATUS_FILE"
  exit 6
fi

# Final independent verification
source venv/bin/activate
if [ -f "$OUTPUT_SCENARIOS" ]; then
  VERIFY_OUT=$(python3 "$ROOT/ref_stms/verify_pyfcstm_full.py" "$OUTPUT_FCSTM" "$OUTPUT_SCENARIOS" 2>&1)
else
  VERIFY_OUT=$(python3 "$ROOT/ref_stms/verify_pyfcstm_full.py" "$OUTPUT_FCSTM" 2>&1)
fi
VERIFY_RC=$?
echo "$VERIFY_OUT" > "$ROOT/ref_stms/verifier_logs/$ID.final_verify.log"

if [ $VERIFY_RC -ne 0 ]; then
  echo "[$ID] WARN: final verify fail rc=$VERIFY_RC" >&2
  echo -e "$ID\tPARTIAL\t$DUR\tverify_rc=$VERIFY_RC" >> "$STATUS_FILE"
fi

echo -e "$ID\tOK\t$DUR\t-" >> "$STATUS_FILE"
echo "[$ID] revise OK dur=${DUR}s verify_rc=$VERIFY_RC"
