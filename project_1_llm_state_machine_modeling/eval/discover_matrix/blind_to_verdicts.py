"""把盲判结果（按 `unit_id`）转成判定表（按台账 id + 臂），供 `metrics_at_k.py` 消费。

## 为什么需要一个显式的转换步骤

盲判样本以 `unit_id`（`U001`…）为键，这是**故意的**：`unit_id` 不含 pair、不含记录 id、不含带，
所以判定者拿到的东西无法反推分组。而 `metrics_at_k.py` 要的是 `{台账 id: {臂: [轮次...]}}`。

两边的键空间不同，中间必须有一次映射 —— 而映射表（`key.json`）正是盲判者看不到的那份。把这一步
写成脚本而不是手工拼，理由有三条，每条都已经出过一次事：

1. **`sample_id` 必须校验。** `unit_id` 是位置编号，换 `--size` 或 `--seed` 就换一套映射。一次实测：
   40 单元的结果配 68 单元的 key，算出 $\\kappa = -0.2$ —— 一个看起来像「判定完全不可靠」的真发现。
2. **两位判定者的分歧必须显式处理，不能静默取一个。** 本工具要求 `--on-disagree` 明确指定策略，
   缺省报错。默认取谁都是在替判定者做决定。
3. **轮次数必须与 key 一致。** 判定者若少写一轮，`metrics_at_k` 的校验会报「有 2 轮，应为 3」，
   但那时已经不知道是判定者漏填还是转换丢失。这里当场对齐并报出。

## 分歧策略

| `--on-disagree` | 含义 | 何时用 |
| :-- | :-- | :-- |
| `error` | 有分歧就报错并列出（**缺省**） | 分歧需要人工裁定时 |
| `conservative` | 取 0（两人都判 1 才算命中） | 要一个下界 |
| `optimistic` | 取 1（任一判 1 即算命中） | 要一个上界 |
| `null` | 写 `None`（该位不进分母） | 分歧留待外部裁定 |

**四种都会在输出里记下策略与逐条分歧**，因为「用哪个策略」本身是口径选择，必须可审计。
`conservative` 与 `optimistic` 应当**双报**，与 `hit@k` 的双分母同理。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent


def _load(path: pathlib.Path) -> tuple[dict, str | None]:
    payload = json.loads(path.read_text())
    verdicts = payload.get("blind_verdicts") or {
        k: v for k, v in payload.items() if not k.startswith("_") and isinstance(v, list)
    }
    if not verdicts:
        raise SystemExit(f"ERROR: no unit verdicts in {path}")
    return verdicts, payload.get("sample_id")


def convert(blind_paths: list[pathlib.Path], key_path: pathlib.Path,
            on_disagree: str) -> dict:
    key = json.loads(key_path.read_text())
    expected_sid = key.get("sample_id")
    items = {i["unit_id"]: i for i in key["items"]}

    per_judge: list[dict] = []
    for path in blind_paths:
        verdicts, sid = _load(path)
        if expected_sid and sid and sid != expected_sid:
            raise SystemExit(
                f"ERROR: {path} 的 sample_id={sid} 与 key 的 {expected_sid} 不符，拒绝转换。"
                "换过 --size / --seed / --generation 就会这样。"
            )
        if expected_sid and not sid:
            print(f"⚠️ {path} 未声明 sample_id，无法验证它答的是这份 key。", file=sys.stderr)
        per_judge.append(verdicts)

    unknown = sorted({u for v in per_judge for u in v} - set(items))
    if unknown:
        raise SystemExit(f"ERROR: 盲判结果里有 key 中不存在的 unit_id：{unknown[:8]}")

    disagreements = []
    out: dict[str, dict[str, list]] = collections.defaultdict(dict)
    round_mismatch = []
    for unit_id, item in sorted(items.items()):
        want = len(item["original_series"])
        series_list = []
        for verdicts in per_judge:
            s = verdicts.get(unit_id)
            if s is None:
                continue
            if len(s) != want:
                round_mismatch.append(f"{unit_id}: 判定给了 {len(s)} 轮，key 说 {want} 轮")
                continue
            series_list.append(s)
        if not series_list:
            continue
        merged = []
        for index in range(want):
            values = {s[index] for s in series_list}
            if len(values) == 1:
                merged.append(values.pop())
                continue
            disagreements.append({
                "unit_id": unit_id, "round": index + 1,
                "record_id": item["record_id"], "arm": item["arm"], "band": item["band"],
                "values": [s[index] for s in series_list],
            })
            merged.append({"conservative": 0, "optimistic": 1, "null": None}.get(on_disagree))
        out[item["record_id"]][item["arm"]] = merged

    if round_mismatch:
        raise SystemExit("ERROR: 轮次数与 key 不符，拒绝转换：\n  " + "\n  ".join(round_mismatch))
    if disagreements and on_disagree == "error":
        lines = [
            f"  {d['unit_id']} r{d['round']} ({d['record_id']}[{d['arm']}], {d['band']}): "
            f"{d['values']}"
            for d in disagreements
        ]
        raise SystemExit(
            f"ERROR: {len(disagreements)} 处判定者分歧，而 --on-disagree=error。\n"
            + "\n".join(lines)
            + "\n\n选一个策略并说明理由：conservative（取 0，下界）/ optimistic（取 1，上界）/ "
              "null（不进分母，留待外部裁定）。**conservative 与 optimistic 应当双报。**"
        )
    return {
        "_source": f"blind_to_verdicts.py from {[str(p.name) for p in blind_paths]}",
        "sample_id": expected_sid,
        "judges": len(per_judge),
        "on_disagree": on_disagree,
        "disagreement_count": len(disagreements),
        "disagreements": disagreements,
        "_calibre_note": (
            "分歧处理策略本身是口径选择。conservative 与 optimistic 的两份结果应当并列报出，"
            "与 hit@k 的双分母同理 —— 只报一个等于替判定者做了决定而不说。"
        ),
        "verdicts": {k: dict(v) for k, v in sorted(out.items())},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("blind", nargs="+", type=pathlib.Path)
    parser.add_argument("--key", type=pathlib.Path, default=HERE / "blind_sample" / "key.json")
    parser.add_argument("--on-disagree", choices=("error", "conservative", "optimistic", "null"),
                        default="error")
    parser.add_argument("-o", "--out", type=pathlib.Path)
    args = parser.parse_args(argv)

    result = convert(args.blind, args.key, args.on_disagree)
    text = json.dumps(result, ensure_ascii=False, indent=1)
    if args.out:
        args.out.write_text(text)
        print(f"写入 {args.out}：{len(result['verdicts'])} 条记录，"
              f"{result['judges']} 位判定者，{result['disagreement_count']} 处分歧"
              f"（策略 {result['on_disagree']}）")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
