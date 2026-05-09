"""验证 21 parquet 中所有路径字段都指向仓库内真实存在的文件。

策略：
1. 找到含 path 关键词的字段
2. 逐行读取每个字段值
3. 对非空值，按"相对 parquet 文件"的语义解析为绝对路径
4. 检查文件是否存在
5. 输出统计：总记录 / 空值 / 命中 / 失败 + 失败示例
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

REPO = Path("/home/zhangshaoang/oo-projects/research_ideas")
DATA = REPO / "project_1_llm_state_machine_modeling/data/baselines_double_green"

PATH_KEYWORDS = ("path", "_uri", "artifact", "local")
EXCLUDE_FIELDS = ("public_artifact_limitations", "artifact_under_review")


def values_iter(value):
    """统一展开值：单字符串、JSON list 字符串、Python list 都展开为字符串。"""
    if value is None:
        return
    try:
        if pd.isna(value):
            return
    except (TypeError, ValueError):
        pass
    s = str(value).strip()
    if not s:
        return
    if s.startswith("[") and s.endswith("]"):
        try:
            arr = json.loads(s)
            if isinstance(arr, list):
                for x in arr:
                    if x:
                        yield str(x).strip()
                return
        except Exception:
            pass
    yield s


def verify():
    summary = []
    for pq in sorted(DATA.rglob("*.parquet")):
        df = pd.read_parquet(pq)
        path_cols = [c for c in df.columns
                     if any(k in c.lower() for k in PATH_KEYWORDS) and c not in EXCLUDE_FIELDS]
        if not path_cols:
            continue

        for col in path_cols:
            total = len(df)
            empty = 0
            hit = 0
            miss = 0
            miss_examples = []

            for v in df[col]:
                items = list(values_iter(v))
                if not items:
                    empty += 1
                    continue
                # 一行可能展开多个值，每个都要验证
                for s in items:
                    target = (pq.parent / s).resolve()
                    if target.exists():
                        hit += 1
                    else:
                        miss += 1
                        if len(miss_examples) < 3:
                            miss_examples.append(s)

            summary.append({
                "parquet": str(pq.relative_to(DATA)),
                "col": col,
                "rows": total,
                "empty_rows": empty,
                "hit": hit,
                "miss": miss,
                "miss_examples": miss_examples,
            })
    return summary


def main():
    rows = verify()
    print(f"{'parquet':50s} {'col':35s} {'行':>6s} {'空':>6s} {'命中':>8s} {'缺失':>6s}")
    print("-" * 130)
    total_hit = 0
    total_miss = 0
    fail_rows = []
    for r in rows:
        flag = "❌" if r["miss"] > 0 else "✅"
        print(f"{flag} {r['parquet']:48s} {r['col']:35s} {r['rows']:>6d} {r['empty_rows']:>6d} {r['hit']:>8d} {r['miss']:>6d}")
        total_hit += r["hit"]
        total_miss += r["miss"]
        if r["miss"] > 0:
            fail_rows.append(r)

    print("-" * 130)
    print(f"\n总命中: {total_hit}    总缺失: {total_miss}")
    if fail_rows:
        print("\n=== 失败字段示例 ===")
        for r in fail_rows:
            print(f"\n▸ {r['parquet']} [{r['col']}] 缺 {r['miss']}")
            for ex in r["miss_examples"]:
                print(f"    {ex}")
        return 1
    else:
        print("\n✅ 全部路径都指向真实文件")
        return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
