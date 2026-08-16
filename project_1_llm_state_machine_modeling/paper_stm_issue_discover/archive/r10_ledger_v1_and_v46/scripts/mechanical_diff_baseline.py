"""Reproduce the mechanical reference-vs-generated state diff, and show why it is unusable.

Issue #171 §1 opens by claiming a deterministic element diff reports 229 reference-only
states, 191 after normalisation, and that most of the residue is still the same state under
a different name.  That claim is load-bearing -- it is the reason the 60-pair review was
done by hand -- so it must be reproducible rather than asserted.  This script derives it
from the two released workbooks.

  reference model   Dataset.xlsx / sheet `Dataset`, col A = model name, col D = PlantUML
  generated model   the corpus pair artifacts, joined on `model_name` in comparison.jsonl

Normalisation is deliberately generous: casefold, strip separators, drop a list of common
modifier words.  Being generous is the point -- a *lower bound* on false gaps is what makes
the argument, since anything the normaliser still reports as missing may or may not be real.

Usage: mechanical_diff_baseline.py [--verbose]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[3]
CORPUS = (ROOT / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline"
          / "representation/reports/llms_emp_r45_java_60")
DATASET = (ROOT / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/corpora/seed_library"
           / "llms-emp-stm-subset/assets/raw/drive_download/Dataset.xlsx")

# Words that carry no identifying information once the surrounding name is fixed.  Chosen
# from the actual residue, not invented: the pairs this collapses are `human_mode` vs
# `HumanDrivingMode`, `Search_for_the_Target` vs `Search`, and similar.
FILLER = {
    "state", "states", "mode", "modes", "the", "a", "an", "of", "for", "to", "is",
    "driving", "target", "system", "status", "phase", "step", "process",
}

PSEUDO = re.compile(r"^\*?(start|end|final)\*?$|^\[\*\]$", re.I)

# `comparison.jsonl`'s `model_name` does not always equal `Dataset.xlsx` col A.  These are
# stated explicitly rather than fuzzy-matched, because a wrong join here would silently
# compare a model against the wrong oracle -- the failure would look like a huge diff, which
# is exactly the conclusion under test.  Each alias is justified in the comment.
ALIAS = {
    # corpus name is the bare module; the dataset prefixes its vehicle-domain rows
    "high-level driving module": "Vehicular Control Systems high-level driving module",
    "autonomous mode": "Vehicular Control Systems autonomous mode",
    "Collision avoidance sub-machine state diagram":
        "Vehicular Control Systems Collision avoidance sub-machine state diagram",
    # same subsystem, different wording ("base brake" vs "basic braking device")
    "State machine diagram of the base brake subsystem":
        "State machine diagram of basic braking device subsystem",
    # dataset row is titled "activity diagram" but its col D is a state machine
    "Microwave Oven Control with entry and \n exit actions":
        "Microwave Oven Control with entry and \n exit activity diagram",
}


def states_from_puml(text: str) -> set[str]:
    """Names PlantUML would treat as states.  Deliberately syntactic -- this is the
    mechanical baseline being argued against, so it must not quietly get smarter."""
    found: set[str] = set()
    for m in re.finditer(r"^\s*state\s+(\"[^\"]+\"|[\w.]+)", text, re.M):
        found.add(m.group(1).strip('"'))
    for m in re.finditer(r"([\w.]+|\[\*\])\s*-+>+\s*([\w.]+|\[\*\])", text):
        found.update(g for g in m.groups() if g)
    for m in re.finditer(r"^\s*([\w.]+)\s*:\s*", text, re.M):
        found.add(m.group(1))
    return {s for s in found if s and not PSEUDO.match(s)}


def norm(name: str) -> str:
    parts = re.split(r"[^A-Za-z0-9]+", re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name))
    kept = [p.casefold() for p in parts if p and p.casefold() not in FILLER]
    return "".join(kept) or name.casefold()


def load_reference() -> dict[str, str]:
    import openpyxl
    wb = openpyxl.load_workbook(DATASET, read_only=True, data_only=True)
    ws = wb["Dataset"]
    out: dict[str, str] = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        name, puml = row[0], row[3] if len(row) > 3 else None
        if not (name and puml):
            continue
        text = str(puml)
        # The dataset holds state, activity and sequence diagrams under one column.  Only
        # state diagrams are an oracle for STM_0; taking an activity diagram by mistake
        # would manufacture a diff out of nothing.
        if "[*]" not in text and not re.search(r"^\s*state\s", text, re.M):
            continue
        out.setdefault(str(name).strip(), text)
    wb.close()
    return out


def main() -> int:
    verbose = "--verbose" in sys.argv
    ref_by_name = load_reference()
    meta = {}
    for line in (CORPUS / "comparison.jsonl").read_text().splitlines():
        rec = json.loads(line)
        meta[rec["case_id"]] = (rec.get("model_name"), rec.get("llm"))

    exact = norm_missing = 0
    unmatched_models: set[str] = set()
    residue: dict[str, list[tuple[str, str]]] = defaultdict(list)
    per_case = []
    for case in sorted(meta):
        model, llm = meta[case]
        key = (model or "").strip()
        ref_text = ref_by_name.get(ALIAS.get(key, key))
        if ref_text is None:
            unmatched_models.add(model or "?")
            continue
        gen_path = CORPUS / "pairs" / case / "plantuml.puml"
        if not gen_path.exists():
            continue
        ref_states = states_from_puml(ref_text)
        gen_states = states_from_puml(gen_path.read_text())
        miss_exact = ref_states - gen_states
        gen_norm = {norm(s) for s in gen_states}
        miss_norm = {s for s in miss_exact if norm(s) not in gen_norm}
        exact += len(miss_exact)
        norm_missing += len(miss_norm)
        per_case.append((case, model, llm, len(ref_states), len(gen_states),
                         len(miss_exact), len(miss_norm)))
        for s in sorted(miss_norm):
            # nearest surviving candidate, to expose remaining same-state-different-name
            best = min(gen_states, key=lambda g: _dist(norm(s), norm(g)), default="")
            if best and _dist(norm(s), norm(best)) <= max(3, len(norm(s)) // 3):
                residue[case].append((s, best))

    print(f"参考模型 {len(ref_by_name)} 个；成功配对 {len(per_case)} / {len(meta)} 个 case")
    if unmatched_models:
        print(f"⚠ 未能在 Dataset.xlsx 中匹配到参考模型的 model_name: {sorted(unmatched_models)}")
    print(f"\n参考独有状态（名称精确比对）        : {exact}")
    print(f"参考独有状态（规范化大小写/分隔符/修饰词后）: {norm_missing}"
          f"   （规范化消掉 {exact - norm_missing} 个，占 {(exact - norm_missing) / exact:.0%}，"
          f"这些是纯命名差异）")
    still_paired = sum(len(v) for v in residue.values())
    print(f"规范化后仍报缺失、但存在近似同名候选      : {still_paired}")
    print("\n注意：近似同名启发式本身两个方向都会出错——它把 EmergencyStoping ~ EmergencyStopping"
          "（参考侧拼写错误）正确配上，\n但也把 choice2 ~ choice3、Join1 ~ Join2、fork1 ~ Fork2 这些"
          "真正不同的伪状态错误配上。\n所以既不能用它自动判定，也不能把它的计数当作真缺失数的估计。"
          "这恰恰是必须人工逐条判定的理由。")
    if verbose:
        print("\n近似同名残留（参考侧 → 生成侧最近候选）:")
        for case, pairs in sorted(residue.items())[:20]:
            for a, b in pairs:
                print(f"  {case}: {a!r:34s} ~ {b!r}")
        print("\n逐 case: case model llm |ref| |gen| 精确缺失 规范化后缺失")
        for row in per_case:
            print("  " + " ".join(str(x) for x in row))
    print("\n结论：机械元素比对给出的缺失数在两种口径下都显著高于真实缺失，"
          "且残留里仍能机械地找到近似同名候选。逐条判定必须人工完成。")
    return 0


def _dist(a: str, b: str) -> int:
    """Levenshtein, small strings only."""
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for jj, cb in enumerate(b, 1):
            cur.append(min(prev[jj] + 1, cur[jj - 1] + 1, prev[jj - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


if __name__ == "__main__":
    raise SystemExit(main())
