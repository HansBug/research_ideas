"""签字完成后调这个：

1. 解析 review packs → ``review/loaded/reviewed.parquet``
2. 构建 audit-trail full_annotations（含双 annotator 完整意见 + 你签字 + 反向指针）
3. **硬检查未签字行**，有则 raise UnsignedRowsError 并列出 .md 路径
4. 生成 ``results/REPORT.md``（中文 audit-trail 报告）
5. 生成 ``results/{detail,macro_per_case,overall_per_condition}.parquet``+ ``summary.csv``
   （derived view，与 §4 报告口径一致）

任何 reviewer 复盘整条评测：从 ``REPORT.md`` 起 → 通过 (case, condition, kind, row_id)
追到 ``full_annotations.parquet`` 单行 → 通过 pack_path/raw_*_path 追到 markdown +
raw annotator JSON。
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve()
PROJ = HERE.parent.parent.parent.parent   # 归档下沉一层：archive/path1_evaluation/demo -> project_1
sys.path.insert(0, str(PROJ))

from archive.path1_evaluation.aggregate import write_results  # noqa: E402
from archive.path1_evaluation.report import UnsignedRowsError, finalize_all  # noqa: E402
from archive.path1_evaluation.review.load import load_packs  # noqa: E402


EVAL_ROOT = PROJ / "archive" / "path1_evaluation"
PACKS_DIR = EVAL_ROOT / "review" / "packs"
RAW_DIR = EVAL_ROOT / "review" / "raw"
DATA = EVAL_ROOT / "data"
LOADED_PARQUET = EVAL_ROOT / "review" / "loaded" / "reviewed.parquet"
RESULTS_DIR = EVAL_ROOT / "results"


def main() -> int:
    print(f"[1/3] loading packs from {PACKS_DIR}")
    df = load_packs(PACKS_DIR, out_parquet=LOADED_PARQUET)
    print(f"      parsed {len(df)} rows → {LOADED_PARQUET.relative_to(PROJ)}")
    if len(df):
        signed = df[df["user_choice"] != "unsigned"]
        print(
            f"      signed: {len(signed)} / {len(df)} "
            f"(auto_marked: {int(df['auto_marked'].sum())}, "
            f"manual: {int(((~df['auto_marked']) & (df['user_choice']!='unsigned')).sum())}, "
            f"unsigned: {int((df['user_choice']=='unsigned').sum())})"
        )

    print(f"\n[2/3] building audit-trail full_annotations → {RESULTS_DIR}")
    try:
        paths = finalize_all(
            reviewed_parquet=LOADED_PARQUET,
            raw_dir=RAW_DIR,
            refs_dir=DATA / "refs",
            preds_dir=DATA / "preds",
            packs_dir=PACKS_DIR,
            out_dir=RESULTS_DIR,
        )
    except UnsignedRowsError as e:
        print()
        print(str(e))
        return 1
    for k, v in paths.items():
        print(f"      {k}: {v.relative_to(PROJ)}")

    print(f"\n[3/3] derived P/R/F1 view → {RESULTS_DIR}")
    derived = write_results(LOADED_PARQUET, RESULTS_DIR)
    for k, v in derived.items():
        print(f"      {k}: {v.relative_to(PROJ)}")

    print("\n✅ finalize 完成。建议阅读顺序：")
    print(f"   1) {(RESULTS_DIR / 'REPORT.md').relative_to(PROJ)}  # 中文 audit-trail 总报告")
    print(f"   2) {(RESULTS_DIR / 'full_annotations.csv').relative_to(PROJ)}  # 每行完整双 annotator + 你签字")
    print(f"   3) {(RESULTS_DIR / 'summary.csv').relative_to(PROJ)}  # P/R/F1 浓缩版")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
