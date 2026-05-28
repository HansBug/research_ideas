#!/usr/bin/env bash
# Per-case codex NL expansion runner.
#
# Usage:  run_expand.sh <id>
#
# Reads pool.tsv + selection.json (only runs ids in candidates+backup),
# renders prompt with STM/PDF/briefs paths, calls codex,
# validates JSON, writes expansions/<id>.json on success.

set -uo pipefail

ID="${1:-}"
[ -z "$ID" ] && { echo "usage: $0 <id>" >&2; exit 1; }

ROOT="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$ROOT/../../../.." && pwd)"
POOL="$ROOT/pool.tsv"
TPL="$ROOT/prompts/expand_template.md"
BRIEF_BASE="$ROOT/briefs/baselines_nl_style.md"
BRIEF_PYFC="$ROOT/briefs/pyfcstm_grounding.md"
OUT="$ROOT/expansions/$ID.json"
LOG="$ROOT/logs_expand/$ID.log"
RAW="$ROOT/logs_expand/$ID.raw"
STATUS_FILE="$ROOT/status_expand.tsv"

# Skip if already done & valid
if [ -f "$OUT" ] && jq -e '.case_id and .expanded_nl and .axis_coverage.H_hierarchical and .axis_coverage.bd_baseline_traps and .axis_coverage.ft_fcstm_fit' "$OUT" >/dev/null 2>&1; then
  echo "[$ID] OK (cached)"
  exit 0
fi
rm -f "$OUT"

# Look up row
ROW=$(awk -F'\t' -v id="$ID" 'NR>1 && $1==id {print; exit}' "$POOL")
if [ -z "$ROW" ]; then
  echo "[$ID] ERROR: id not in pool" >&2
  exit 2
fi
IFS=$'\t' read -r RID BUCKET SLUG CASENAME STM_REL PDF_REL TXT_REL PAPERNO DOMAIN <<< "$ROW"

STM="$REPO_ROOT/$STM_REL"
PDF="$REPO_ROOT/$PDF_REL"
TXT="$REPO_ROOT/$TXT_REL"

for f in "$STM" "$PDF" "$TXT" "$TPL" "$BRIEF_BASE" "$BRIEF_PYFC"; do
  [ -f "$f" ] || { echo "[$ID] ERROR: missing file $f" >&2; exit 3; }
done

CASENAME_ESC=$(printf '%s' "$CASENAME" | sed 's/[\\/&]/\\&/g')
DOMAIN_ESC=$(printf '%s' "$DOMAIN" | sed 's/[\\/&]/\\&/g')

PROMPT_FILE="$ROOT/logs_expand/$ID.prompt"
sed \
  -e "s|{{CASE_ID}}|$ID|g" \
  -e "s|{{BUCKET}}|$BUCKET|g" \
  -e "s|{{DOMAIN}}|$DOMAIN_ESC|g" \
  -e "s|{{PAPER_SLUG}}|$SLUG|g" \
  -e "s|{{CASE_NAME}}|$CASENAME_ESC|g" \
  -e "s|{{STM_PATH}}|$STM|g" \
  -e "s|{{PAPER_PDF}}|$PDF|g" \
  -e "s|{{PAPER_CONTENT}}|$TXT|g" \
  -e "s|{{BRIEF_BASELINES}}|$BRIEF_BASE|g" \
  -e "s|{{BRIEF_PYFCSTM}}|$BRIEF_PYFC|g" \
  "$TPL" > "$PROMPT_FILE"

cd "$REPO_ROOT"
START=$(date +%s)
timeout 1200 codex exec --json --skip-git-repo-check < "$PROMPT_FILE" 2>"$LOG" >"$RAW"
RC=$?
END=$(date +%s)
DUR=$((END-START))

if [ $RC -ne 0 ]; then
  echo "[$ID] FAIL rc=$RC dur=${DUR}s" >&2
  echo -e "$ID\tFAIL\t$DUR\trc=$RC" >> "$STATUS_FILE"
  exit 4
fi

python3 - "$RAW" "$OUT" "$ID" <<'PY'
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
    if nl >= 0:
        text = text[nl+1:]
    if text.rstrip().endswith("```"):
        text = text.rstrip()[:-3]
text = text.strip()

try:
    data = json.loads(text)
except Exception as e:
    sys.stderr.write(f"[{cid}] JSON parse fail: {e}\nhead: {text[:400]}\n")
    sys.exit(7)

required = ["case_id","case_name","expanded_nl","provenance","axis_coverage","word_count_estimate"]
for k in required:
    if k not in data:
        sys.stderr.write(f"[{cid}] missing field {k}\n")
        sys.exit(8)
for axkey in ["H_hierarchical","G_guards_arith","A_actions_nontrivial","F_fault_recovery","bd_baseline_traps","ft_fcstm_fit"]:
    if axkey not in data.get("axis_coverage", {}):
        sys.stderr.write(f"[{cid}] missing axis_coverage.{axkey}\n")
        sys.exit(9)

# Sanity check word count
wc = data.get("word_count_estimate", 0)
actual = len(data["expanded_nl"].split())
if actual < 120 or actual > 320:
    sys.stderr.write(f"[{cid}] WARN word count out of range: declared={wc} actual={actual}\n")

# Provenance sanity: every [En] in expanded_nl must have matching marker; warn if mismatch
import re
markers_in_nl = set(re.findall(r"\[E(\d+)\]", data["expanded_nl"]))
markers_in_prov = set()
for p in data.get("provenance", []):
    m = p.get("marker", "")
    mm = re.match(r"E?(\d+)$", m)
    if mm:
        markers_in_prov.add(mm.group(1))
missing_prov = markers_in_nl - markers_in_prov
orphan_prov = markers_in_prov - markers_in_nl
if missing_prov:
    sys.stderr.write(f"[{cid}] WARN markers in NL with no provenance: {sorted(missing_prov)}\n")
if orphan_prov:
    sys.stderr.write(f"[{cid}] WARN provenance entries unused in NL: {sorted(orphan_prov)}\n")
if len(data.get("provenance", [])) < 3:
    sys.stderr.write(f"[{cid}] WARN only {len(data.get('provenance',[]))} provenance entries (expect >=3)\n")

data["_meta"] = {
    "id": cid,
    "actual_word_count": actual,
    "markers_count": len(markers_in_nl),
    "provenance_count": len(data.get("provenance", [])),
}
with open(out_path, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"[{cid}] WROTE words={actual}")
PY
PARSE_RC=$?

if [ $PARSE_RC -ne 0 ]; then
  echo -e "$ID\tFAIL\t$DUR\tparse_rc=$PARSE_RC" >> "$STATUS_FILE"
  exit 6
fi

echo -e "$ID\tOK\t$DUR\t-" >> "$STATUS_FILE"
echo "[$ID] OK dur=${DUR}s"
