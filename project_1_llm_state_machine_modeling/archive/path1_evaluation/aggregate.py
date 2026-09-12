"""From signed reviewed.parquet → per case × condition × component P/R/F1 + macro.

Only `user_final_status` rows are counted. Unsigned rows (user_choice == "unsigned")
are reported separately so we can refuse to compute final metrics when
review is incomplete.

Counting rule per component_kind:
- TP rows count toward `tp`
- FP rows count toward `fp`
- FN rows count toward `fn`
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def _prf(tp: int, fp: int, fn: int) -> dict[str, float]:
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": p, "recall": r, "f1": f1}


def aggregate(reviewed_parquet: Path) -> dict[str, Any]:
    df = pd.read_parquet(reviewed_parquet)

    unsigned = df[df["user_choice"] == "unsigned"]
    signed = df[df["user_choice"] != "unsigned"]

    # per case × condition × component
    detail: list[dict[str, Any]] = []
    for (case, cond, kind), grp in signed.groupby(["case_id", "condition", "component_kind"]):
        counts = grp["user_final_status"].value_counts().to_dict()
        tp = int(counts.get("TP", 0))
        fp = int(counts.get("FP", 0))
        fn = int(counts.get("FN", 0))
        m = _prf(tp, fp, fn)
        detail.append({
            "case_id": case,
            "condition": cond,
            "component_kind": kind,
            **m,
        })

    detail_df = pd.DataFrame(detail)

    # per case × condition macro
    macro: list[dict[str, Any]] = []
    if len(detail_df):
        for (case, cond), grp in detail_df.groupby(["case_id", "condition"]):
            macro.append({
                "case_id": case,
                "condition": cond,
                "macro_f1_5component": float(grp["f1"].mean()),
                "components_scored": len(grp),
            })
    macro_df = pd.DataFrame(macro)

    # overall (aggregate TP/FP/FN across components per condition)
    overall: list[dict[str, Any]] = []
    if len(detail_df):
        for cond, grp in detail_df.groupby("condition"):
            tp = int(grp["tp"].sum())
            fp = int(grp["fp"].sum())
            fn = int(grp["fn"].sum())
            overall.append({
                "condition": cond,
                **_prf(tp, fp, fn),
            })
    overall_df = pd.DataFrame(overall)

    return {
        "detail": detail_df,
        "macro_per_case": macro_df,
        "overall_per_condition": overall_df,
        "n_signed": len(signed),
        "n_unsigned": len(unsigned),
        "n_total": len(df),
    }


def write_results(reviewed_parquet: Path, out_dir: Path) -> dict[str, Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    res = aggregate(reviewed_parquet)
    paths = {}
    for k in ("detail", "macro_per_case", "overall_per_condition"):
        p = out_dir / f"{k}.parquet"
        res[k].to_parquet(p, index=False)
        paths[k] = p
    # also a csv summary
    csv_path = out_dir / "summary.csv"
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("# n_signed,n_unsigned,n_total\n")
        f.write(f"{res['n_signed']},{res['n_unsigned']},{res['n_total']}\n\n")
        f.write("# detail per case × condition × component\n")
        res["detail"].to_csv(f, index=False)
        f.write("\n# macro per case × condition\n")
        res["macro_per_case"].to_csv(f, index=False)
        f.write("\n# overall per condition\n")
        res["overall_per_condition"].to_csv(f, index=False)
    paths["summary_csv"] = csv_path
    return paths
