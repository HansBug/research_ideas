"""不再调 LLM，仅用 eval/review/raw/ 下已有的 annotator JSON 重新渲染评审包。

用于：调整 markdown 排版 / 增减字段（如本次新增 NL 原文 + ref/pred 模型全文）后，
不浪费 token 重新生成 packs。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
PROJ = HERE.parent.parent.parent.parent   # 归档下沉一层：archive/path1_evaluation/demo -> project_1
sys.path.insert(0, str(PROJ))

from archive.path1_evaluation.review.render import render_pack  # noqa: E402


EVAL_ROOT = PROJ / "archive" / "path1_evaluation"
DATA = EVAL_ROOT / "data"
RAW_DIR = EVAL_ROOT / "review" / "raw"
PACKS_DIR = EVAL_ROOT / "review" / "packs"


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    if not RAW_DIR.exists():
        print(f"no raw dir at {RAW_DIR}")
        return 1
    n = 0
    for case_dir in sorted(RAW_DIR.iterdir()):
        if not case_dir.is_dir():
            continue
        case_id = case_dir.name
        nl_text = (DATA / "sources" / case_id / "nl.md").read_text(encoding="utf-8")
        ref_blob = _load(DATA / "refs" / case_id / "ref_components.json")
        ref_model_text = (DATA / "refs" / case_id / ref_blob["model_text_path"]).read_text(encoding="utf-8")
        for cond_dir in sorted(case_dir.iterdir()):
            condition = cond_dir.name
            pred_blob = _load(DATA / "preds" / case_id / f"{condition}.json")
            pred_model_text = (
                DATA / "preds" / case_id / pred_blob["model_text_path"]
            ).read_text(encoding="utf-8")
            for kind_dir in sorted(cond_dir.iterdir()):
                kind = kind_dir.name
                claude_p = kind_dir / "claude.json"
                codex_p = kind_dir / "codex.json"
                cres = _load(claude_p) if claude_p.exists() else None
                gres = _load(codex_p) if codex_p.exists() else None
                ref_inst = ref_blob.get(kind, [])
                pred_inst = pred_blob.get(kind, [])
                out_md = PACKS_DIR / case_id / condition / f"{kind}.md"
                render_pack(
                    case_id=case_id,
                    condition=condition,
                    component_kind=kind,
                    ref_instances=ref_inst,
                    pred_instances=pred_inst,
                    claude_result=cres,
                    codex_result=gres,
                    out_path=out_md,
                    nl_text=nl_text,
                    ref_model_text=ref_model_text,
                    pred_model_text=pred_model_text,
                )
                print(f"rerendered: {out_md.relative_to(PROJ)}")
                n += 1
    print(f"\ntotal {n} pack(s) re-rendered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
