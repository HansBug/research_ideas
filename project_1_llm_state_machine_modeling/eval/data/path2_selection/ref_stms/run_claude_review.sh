#!/usr/bin/env bash
# Per-case claude cross-review runner.
# Usage:  run_claude_review.sh <id>

set -uo pipefail

ID="${1:-}"
[ -z "$ID" ] && { echo "usage: $0 <id>" >&2; exit 1; }

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/../../../.." && pwd)"
POOL="$ROOT/pool.tsv"
TPL="$ROOT/ref_stms/prompts/claude_review_template.md"
REF_FCSTM="$ROOT/ref_stms/codex_drafts/$ID.fcstm"
REF_SCENARIOS="$ROOT/ref_stms/codex_drafts/$ID.scenarios.json"
REF_NOTES="$ROOT/ref_stms/codex_drafts/$ID.notes.md"
OUT="$ROOT/ref_stms/claude_reviews/$ID.json"
LOG="$ROOT/ref_stms/verifier_logs/$ID.claude.log"
RAW="$ROOT/ref_stms/verifier_logs/$ID.claude.raw"
STATUS_FILE="$ROOT/ref_stms/status_claude.tsv"

if [ -f "$OUT" ] && jq -e '.case_id and .verdict' "$OUT" >/dev/null 2>&1; then
  echo "[$ID] CACHED OK"
  exit 0
fi
rm -f "$OUT"

# Pre-conditions
for f in "$REF_FCSTM" "$REF_SCENARIOS" "$REF_NOTES" "$TPL"; do
  [ -f "$f" ] || { echo "[$ID] ERROR: missing $f (codex draft not done)" >&2; exit 2; }
done

# Look up row
ROW=$(awk -F'\t' -v id="$ID" 'NR>1 && $1==id {print; exit}' "$POOL")
[ -z "$ROW" ] && { echo "[$ID] not in pool" >&2; exit 3; }
IFS=$'\t' read -r RID BUCKET SLUG CASENAME STM_REL PDF_REL TXT_REL PAPERNO DOMAIN <<< "$ROW"
STM="$REPO_ROOT/$STM_REL"
PDF="$REPO_ROOT/$PDF_REL"
EXPANSION="$ROOT/expansions/$ID.json"

CASENAME_ESC=$(printf '%s' "$CASENAME" | sed 's/[\\/&]/\\&/g')

PROMPT_FILE="$ROOT/ref_stms/verifier_logs/$ID.claude.prompt"
sed \
  -e "s|{{CASE_ID}}|$ID|g" \
  -e "s|{{CASE_NAME}}|$CASENAME_ESC|g" \
  -e "s|{{STM_PATH}}|$STM|g" \
  -e "s|{{EXPANSION_PATH}}|$EXPANSION|g" \
  -e "s|{{PAPER_PDF}}|$PDF|g" \
  -e "s|{{REF_FCSTM}}|$REF_FCSTM|g" \
  -e "s|{{REF_SCENARIOS}}|$REF_SCENARIOS|g" \
  -e "s|{{REF_NOTES}}|$REF_NOTES|g" \
  "$TPL" > "$PROMPT_FILE"

cd "$REPO_ROOT"
START=$(date +%s)
# claude -p (non-interactive). Use --output-format json. Increase tool budget so
# Claude can read the referenced files itself.
timeout 900 claude -p "$(cat "$PROMPT_FILE")" --output-format json --permission-mode acceptEdits 2>"$LOG" >"$RAW"
RC=$?
END=$(date +%s)
DUR=$((END-START))

if [ $RC -ne 0 ]; then
  echo "[$ID] FAIL rc=$RC dur=${DUR}s" >&2
  echo -e "$ID\tFAIL\t$DUR\trc=$RC" >> "$STATUS_FILE"
  exit 4
fi

# Extract result from claude envelope
python3 - "$RAW" "$OUT" "$ID" <<'PY'
import json, sys
raw_path, out_path, cid = sys.argv[1:4]
envelope_text = open(raw_path).read().strip()
try:
    envelope = json.loads(envelope_text)
except Exception as e:
    sys.stderr.write(f"[{cid}] envelope JSON parse fail: {e}\nhead: {envelope_text[:500]}\n")
    sys.exit(5)
if envelope.get("is_error"):
    sys.stderr.write(f"[{cid}] claude reported is_error: {envelope.get('result')}\n")
    sys.exit(6)
raw_text = envelope.get("result", "")
text = raw_text.strip()
# Strip ``` fence if any
if text.startswith("```"):
    nl = text.find("\n")
    if nl >= 0: text = text[nl+1:]
    if text.rstrip().endswith("```"): text = text.rstrip()[:-3]
text = text.strip()

data = None
# Try direct parse first
try:
    data = json.loads(text)
except Exception:
    pass

# Fallback 0.5: append missing close braces if claude truncated
if data is None:
    opens = text.count("{")
    closes = text.count("}")
    if opens > closes:
        try:
            data = json.loads(text + "}" * (opens - closes))
        except Exception:
            pass

# Fallback 1: look for JSON starting with {"case_id" (anchor pattern)
if data is None:
    import re as _re
    m = _re.search(r'\{\s*"case_id"\s*:', text)
    if m:
        s = m.start()
        depth = 0
        end = None
        for i in range(s, len(text)):
            c = text[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end:
            try:
                data = json.loads(text[s:end])
            except Exception as e:
                sys.stderr.write(f"[{cid}] anchored extract failed: {e}\n")

# Fallback 2: try last {...} block via rfind
if data is None:
    end = text.rfind("}")
    if end > 0:
        # walk back to matching '{'
        depth = 0
        start = None
        for i in range(end, -1, -1):
            c = text[i]
            if c == "}": depth += 1
            elif c == "{":
                depth -= 1
                if depth == 0:
                    start = i
                    break
        if start is not None:
            try:
                data = json.loads(text[start:end+1])
            except Exception as e:
                sys.stderr.write(f"[{cid}] rfind extract failed: {e}\n")

if data is None:
    sys.stderr.write(f"[{cid}] result JSON parse fail; head: {text[:300]}\ntail: {text[-300:]}\n")
    sys.exit(7)
data["_meta"] = {
    "id": cid,
    "claude_model": envelope.get("model", "?"),
    "duration_ms": envelope.get("duration_ms"),
    "cost_usd": envelope.get("total_cost_usd"),
}
with open(out_path, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"[{cid}] claude verdict: {data.get('verdict','?')}")
PY
PARSE_RC=$?

if [ $PARSE_RC -ne 0 ]; then
  echo -e "$ID\tFAIL\t$DUR\tjson_rc=$PARSE_RC" >> "$STATUS_FILE"
  exit 8
fi

echo -e "$ID\tOK\t$DUR\t-" >> "$STATUS_FILE"
echo "[$ID] claude OK dur=${DUR}s"
