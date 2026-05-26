#!/usr/bin/env bash
# Per-sample codex review runner.
#
# Usage:  run_review.sh <id>
#
# Idempotent: skip if results/<id>.json already exists and is valid.

set -uo pipefail

ID="${1:-}"
[ -z "$ID" ] && { echo "usage: $0 <id>" >&2; exit 1; }

ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../../../.." && pwd)"
POOL="$ROOT/pool.tsv"
TPL="$ROOT/prompts/review_template.md"
OUT="$ROOT/results/$ID.json"
LOG="$ROOT/logs/$ID.log"
RAW="$ROOT/logs/$ID.raw"
FINAL_TXT="$ROOT/logs/$ID.final"
STATUS_FILE="$ROOT/status.tsv"

# Skip if already done & valid
if [ -f "$OUT" ] && jq -e '.case_id and .axes.C1_dead_end_potential.score and .verdict' "$OUT" >/dev/null 2>&1; then
  echo "[$ID] OK (cached)"
  exit 0
fi
rm -f "$OUT"

# Look up row
ROW=$(awk -F'\t' -v id="$ID" 'NR>1 && $1==id {print; exit}' "$POOL")
if [ -z "$ROW" ]; then
  echo "[$ID] ERROR: id not found in pool" >&2
  exit 2
fi
IFS=$'\t' read -r RID BUCKET SLUG CASENAME STM_REL PDF_REL TXT_REL PAPERNO <<< "$ROW"

STM="$REPO_ROOT/$STM_REL"
PDF="$REPO_ROOT/$PDF_REL"
TXT="$REPO_ROOT/$TXT_REL"

for f in "$STM" "$PDF" "$TXT" "$TPL"; do
  [ -f "$f" ] || { echo "[$ID] ERROR: missing file $f" >&2; exit 3; }
done

# Escape case name for sed (it may contain / or &)
CASENAME_ESC=$(printf '%s' "$CASENAME" | sed 's/[\\/&]/\\&/g')

PROMPT_FILE="$ROOT/logs/$ID.prompt"
sed \
  -e "s|{{CASE_ID}}|$ID|g" \
  -e "s|{{BUCKET}}|$BUCKET|g" \
  -e "s|{{PAPER_SLUG}}|$SLUG|g" \
  -e "s|{{CASE_NAME}}|$CASENAME_ESC|g" \
  -e "s|{{STM_PATH}}|$STM|g" \
  -e "s|{{PAPER_PDF}}|$PDF|g" \
  -e "s|{{PAPER_CONTENT}}|$TXT|g" \
  "$TPL" > "$PROMPT_FILE"

cd "$REPO_ROOT"
START=$(date +%s)
timeout 900 codex exec --json --skip-git-repo-check < "$PROMPT_FILE" 2>"$LOG" >"$RAW"
RC=$?
END=$(date +%s)
DUR=$((END-START))

if [ $RC -ne 0 ]; then
  echo "[$ID] FAIL rc=$RC dur=${DUR}s" >&2
  echo -e "$ID\tFAIL\t$DUR\trc=$RC" >> "$STATUS_FILE"
  exit 4
fi

# Extract final agent_message + validate JSON
python3 - "$RAW" "$OUT" "$ID" "$FINAL_TXT" <<'PY'
import json, sys
raw_path, out_path, cid, final_txt_path = sys.argv[1:5]

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

with open(final_txt_path, "w") as f:
    f.write(final)

if not final:
    sys.stderr.write(f"[{cid}] no agent_message\n")
    sys.exit(5)

text = final.strip()
if text.startswith("```"):
    nl = text.find("\n")
    if nl >= 0:
        text = text[nl+1:]
    if text.rstrip().endswith("```"):
        text = text.rstrip()[:-3]
text = text.strip()

try:
    data = json.loads(text)
except Exception as e:
    sys.stderr.write(f"[{cid}] JSON parse fail: {e}\nhead: {text[:300]}\n")
    sys.exit(7)

required = ["case_id","case_name","bucket","what_it_is","scale","axes","verdict"]
for k in required:
    if k not in data:
        sys.stderr.write(f"[{cid}] missing field {k}\n")
        sys.exit(8)
for axkey in ["C1_dead_end_potential","C2_numerical_guard_richness","C3_forced_fault_recovery","C4_hardware_decoupling"]:
    if axkey not in data.get("axes", {}) or "score" not in data["axes"][axkey]:
        sys.stderr.write(f"[{cid}] missing axis {axkey}\n")
        sys.exit(9)

data["_meta"] = {"id": cid}
with open(out_path, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"[{cid}] WROTE")
PY
PARSE_RC=$?

if [ $PARSE_RC -ne 0 ]; then
  echo -e "$ID\tFAIL\t$DUR\tparse_rc=$PARSE_RC" >> "$STATUS_FILE"
  exit 6
fi

echo -e "$ID\tOK\t$DUR\t-" >> "$STATUS_FILE"
echo "[$ID] OK dur=${DUR}s"
