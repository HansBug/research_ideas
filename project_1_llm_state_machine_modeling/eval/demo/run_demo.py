"""演习：2 cases × 2 conditions × 1 component (states) × 2 annotators = 8 LLM calls。

流程：
1. 加载 ref + pred JSON
2. 调 ``annotate.orchestrate.annotate_pair`` 并行（顺序）跑 claude + codex
3. ``review/render.render_pack`` 输出中文 markdown 包到 ``eval/review/packs/...``
4. 打印每个 pack 的路径让用户去签字

签完字后跑 ``demo/aggregate_after_signoff.py``（用户手动）即可看 metric。
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# Add project root to path so `from eval...` works
HERE = Path(__file__).resolve()
PROJ = HERE.parent.parent.parent
sys.path.insert(0, str(PROJ))

from eval.annotate.orchestrate import annotate_pair  # noqa: E402
from eval.review.render import render_pack  # noqa: E402


EVAL_ROOT = PROJ / "eval"
DATA = EVAL_ROOT / "data"
RAW_DIR = EVAL_ROOT / "review" / "raw"
PACKS_DIR = EVAL_ROOT / "review" / "packs"

CASES = [
    "automatic-elevator-controller",
    "abs-fsm-brake-control",
]
CONDITIONS = ["pred_perfect", "pred_buggy"]
COMPONENT_KINDS = ["states", "transitions", "guards", "actions", "hierarchical_states"]


def _load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    print(f"\n{'#' * 70}\n# Phase A 演习 — eval pipeline end-to-end\n{'#' * 70}")
    print(f"cases: {CASES}")
    print(f"conditions: {CONDITIONS}")
    print(f"components: {COMPONENT_KINDS}")
    print()
    t0 = time.time()
    n_skip_empty = 0
    n_skip_cached = 0
    n_done = 0

    for case_id in CASES:
        nl_path = DATA / "sources" / case_id / "nl.md"
        nl_text = nl_path.read_text(encoding="utf-8")

        ref_path = DATA / "refs" / case_id / "ref_components.json"
        ref = _load_json(ref_path)
        ref_model_text = (DATA / "refs" / case_id / ref["model_text_path"]).read_text(encoding="utf-8")

        for condition in CONDITIONS:
            pred_path = DATA / "preds" / case_id / f"{condition}.json"
            pred = _load_json(pred_path)
            pred_model_text = (DATA / "preds" / case_id / pred["model_text_path"]).read_text(encoding="utf-8")

            for component_kind in COMPONENT_KINDS:
                ref_instances = ref.get(component_kind, [])
                pred_instances = pred.get(component_kind, [])

                if not ref_instances and not pred_instances:
                    n_skip_empty += 1
                    continue  # nothing to annotate

                raw_claude = RAW_DIR / case_id / condition / component_kind / "claude.json"
                raw_codex = RAW_DIR / case_id / condition / component_kind / "codex.json"
                if raw_claude.exists() and raw_codex.exists():
                    n_skip_cached += 1
                    # Re-render only from cached raws (cheap)
                    cres = _load_json(raw_claude) if raw_claude.exists() else None
                    gres = _load_json(raw_codex) if raw_codex.exists() else None
                else:
                    print(f"-> annotating {case_id} / {condition} / {component_kind} ({len(ref_instances)} ref, {len(pred_instances)} pred) ...")
                    sys.stdout.flush()
                    ts = time.time()
                    results = annotate_pair(
                        case_id=case_id,
                        condition=condition,
                        component_kind=component_kind,
                        nl_text=nl_text,
                        ref_text=ref_model_text,
                        pred_text=pred_model_text,
                        ref_instances=ref_instances,
                        pred_instances=pred_instances,
                        raw_dir=RAW_DIR,
                    )
                    dt = time.time() - ts
                    cres = results.get("claude")
                    gres = results.get("codex")
                    cs_ok = cres and "annotations" in cres and "error" not in cres
                    gs_ok = gres and "annotations" in gres and "error" not in gres
                    cs_tp = (cres or {}).get("summary", {}).get("tp", "?") if cs_ok else (cres or {}).get("error", "")
                    gs_tp = (gres or {}).get("summary", {}).get("tp", "?") if gs_ok else (gres or {}).get("error", "")
                    print(f"   claude: {'OK ' + str(cs_tp) + 'TP' if cs_ok else 'ERR ' + str(cs_tp)[:80]}")
                    print(f"   codex : {'OK ' + str(gs_tp) + 'TP' if gs_ok else 'ERR ' + str(gs_tp)[:80]}")
                    print(f"   wall: {dt:.1f}s")
                    n_done += 1

                out_md = PACKS_DIR / case_id / condition / f"{component_kind}.md"
                render_pack(
                    case_id=case_id,
                    condition=condition,
                    component_kind=component_kind,
                    ref_instances=ref_instances,
                    pred_instances=pred_instances,
                    claude_result=cres,
                    codex_result=gres,
                    out_path=out_md,
                    nl_text=nl_text,
                    ref_model_text=ref_model_text,
                    pred_model_text=pred_model_text,
                )
                print(f"   pack: {out_md.relative_to(PROJ)}")
    print()
    print(f"summary: {n_done} new LLM call sets, {n_skip_cached} cached (re-rendered), {n_skip_empty} empty (skipped)")

    print(f"\nDONE in {time.time()-t0:.1f}s.")
    print(f"\nReview packs are in: {PACKS_DIR.relative_to(PROJ)}")
    print(f"Raw annotator JSON: {RAW_DIR.relative_to(PROJ)}")
    print("\nNext step: open each .md, sign the rows that need 复议, then run:")
    print(f"  python {(EVAL_ROOT / 'demo' / 'finalize_after_signoff.py').relative_to(PROJ)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
