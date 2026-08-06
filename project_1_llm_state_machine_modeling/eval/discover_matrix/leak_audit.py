"""Cross-check every string literal that can reach the model against the whole ledger.

Not a probe list -- the previous four attempts each grepped for the strings the last audit had
named, and each time the next leak was in a form nobody had grepped for. This walks the AST,
takes every string literal that is not a docstring, and matches it against every identifier and
characteristic phrase in the pairs that are actually being measured.

Which pairs those are is read from `holdout.json`, not hardcoded. The first version pinned the
four historical cells, so the audit that was declared a pre-run gate had never once run against
the pairs a coverage number would be reported from -- it audited only the pairs already known to
be burned. Auditing the burned cells tells you nothing you did not already know; auditing the
held-out ones is the whole point.
"""
import ast, json, pathlib, re, collections

ROOT = pathlib.Path("project_1_llm_state_machine_modeling")
LEDGER = ROOT / "eval/discover_matrix/manual_review/expected_issue_set.json"
SRC = ROOT / "paper_stm_repair/pipeline/feedback_loop/src/paper_stm_feedback_loop"
HOLDOUT_FILE = ROOT / "eval/discover_matrix/holdout.json"
#: Held-out pairs first -- those are the ones a reported number depends on -- plus the four
#: historical cells, which are audited too so a regression there is still visible.
HISTORICAL = {"0000", "0006", "0029", "0050"}
AUDITED = set(json.loads(HOLDOUT_FILE.read_text())["holdout"]) | HISTORICAL
GENERIC = {
    "source","target","trigger","scope","child","parent","variable","count","kind","sign","phase",
    "within_cycles","bound","release","condition","composite","state","event","True","False","None",
    "any","leaf","negative","positive","structure","behavior","property","initial","Initial",
    "predicate","assertion","requirement","cardinality","containment","terminates","reaches",
    "stays_in","occupancy_after","persists_until","invariant","edge_declared","effect_declared",
    "state_declared","event_declared","variable_declared","transition_declared","region_declared",
    "initial_target","guard_distinguishable","response_within","variable_delta_after",
}

led = json.loads(LEDGER.read_text())
tokens = set()
for rec in led.get("records", []):
    if str(rec.get("pair"))[-4:] not in AUDITED:
        continue
    # `statement` was missing: it is where the defect is described in prose, i.e. exactly the
    # form the answer-shape leaks took.
    fields = [
        rec.get("reference_side"), rec.get("generated_side"), rec.get("nl_evidence"),
        rec.get("statement"),
    ]
    for a in rec.get("assertions") or []:
        fields.append(a.get("expression"))
        fields.extend(a.get("elements") or [])
    for f in fields:
        for m in re.findall(r"[A-Za-z_][A-Za-z_0-9]{4,}", str(f or "")):
            if m in GENERIC or m.startswith("llms_emp"):
                continue
            tokens.add(m)

def literals(path):
    """Every string literal that is not a module/class/function docstring."""
    tree = ast.parse(path.read_text())
    doc_nodes = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = getattr(node, "body", [])
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
               and isinstance(body[0].value.value, str):
                doc_nodes.add(id(body[0].value))
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in doc_nodes:
            yield node.lineno, node.value

hits = collections.defaultdict(list)
for f in sorted(SRC.rglob("*.py")):
    for lineno, text in literals(f):
        for tok in tokens:
            if re.search(r"\b" + re.escape(tok) + r"\b", text):
                hits[tok].append(f"{f.name}:{lineno}")

print(f"台账四格提取到 {len(tokens)} 个非通用标识符")
print(f"在可进入模型的字符串字面量里命中: {len(hits)} 个\n")
if not hits:
    print("  ✅ 无命中 —— 进入模型的文本里没有台账内容")
for tok, locs in sorted(hits.items(), key=lambda kv: -len(kv[1])):
    print(f"  {tok:24} {len(locs):3} 处   {sorted(set(locs))[:4]}")
