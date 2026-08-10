"""把判定表渲染成 PR comment。**三张按资格分开的表，不是一张。**

## 为什么结构本身是个纪律问题

上一代次的格式是单表 34 行（`pr-comment-format-paper1`）。问题不在字段，在于**任何单表都会把
行数当成分母**：读者的默认阅读是「表里有多少行，就有多少条被度量」。而 v22 的可报记录只有 3
条，其余 30 条是共演化观测 —— 它们照常全量报出，但**不构成任何主张**。一张 33 行的表加一句
脚注解决不了这个，因为脚注会被跳过而表头不会。

所以：

  能力主张表（3 行）      —— 只有这张给 hit@1/@3/@all 三个比率
  达阈值的层（4 行，全 0）—— **空本身是结论**，必须是一张实体表，不能降级成脚注
  （hold-out 与分带机制已于 2026-08-09 永久移除；下面两带恒为空）

三条硬约束，落成断言而不是提醒：

1. `hit@` 比率只出现在第一张表。给了比率它就会被引用。
2. 头部速览不得出现任何 `n/33` 形式的分数。写「可报记录 3 条，达阈值层 0 层，本代次无能力主张」。
3. 「达阈值的层：0/4」那张表必须实体存在。§9 的结论是「v22 不产出任何能力主张」；一张写着 0
   的表能被看见，一句脚注会被跳过。

双报同理：`as published` 与 `re-derived` 必须**同表两列**，且 re-derived 列的表头就带界的说明，
否则那个数会被当成完整重表达。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import metrics_at_k as mk  # noqa: E402

#: 只剩一个分母。分带随 hold-out 于 2026-08-09 一并废止（docs/protocol/method_provenance_policy.md §一.1），
#: 台账全部记录同等参与度量，没有哪一条因为参与过规则编写而被单独成带或剔出分母。
BAND_TITLES = {"hold": "可报告记录（{n} 条）"}
LAYERS = ("wellformedness", "nl_named", "over_specification", "nl_contradiction")
THRESHOLD = 4


def _ledger() -> dict[str, dict]:
    payload = json.loads((HERE / "manual_review" / "expected_issue_set.json").read_text())
    records = payload.get("records")
    if not records:
        records = next(
            value
            for value in payload.values()
            if isinstance(value, list) and value and isinstance(value[0], dict) and "id" in value[0]
        )
    return {str(r["id"]): r for r in records}


def _mark(value) -> str:
    return {1: "✅", 0: "✗", None: "—"}.get(value, "?")


def _brief(record: dict, limit: int = 64) -> str:
    """缺陷简述。取 statement 首句，且**不在句中截断** —— 截断线切掉结论子句是有前科的。"""

    text = str(record.get("statement") or "").replace("\n", " ").strip()
    for stop in ("；", "。", "，"):
        head = text.split(stop, 1)[0]
        if len(head) <= limit:
            return head
    return text[:limit] + "…" if len(text) > limit else text


def _rows(verdicts: dict, ids: list[str], ledger: dict, rounds: int) -> list[list[str]]:
    rows = []
    for record_id in sorted(ids):
        record = ledger.get(record_id) or {}
        for arm, series in sorted(mk._arms(verdicts[record_id]).items()):
            label = record_id if arm == "-" else f"{record_id} · {arm}"
            cells = [_mark(series[i]) if i < len(series) else "—" for i in range(rounds)]
            note = mk.BLOCKED.get(record_id, "")
            rows.append(
                [label, str(record.get("layer") or "?"), _brief(record), *cells,
                 f"⚠️ {note}" if note else ""]
            )
    return rows


def _table(header: list[str], rows: list[list[str]]) -> str:
    align = ["| " + " | ".join(header) + " |",
             "| " + " | ".join("---" for _ in header) + " |"]
    align += ["| " + " | ".join(cell or "—" for cell in row) + " |" for row in rows]
    return "\n".join(align)


def _ratios(verdicts: dict, ids: list[str], rounds: int) -> dict:
    """`hit@k` 三口径。`rounds` 不是可选的 —— 见 `atall` 那行。

    `all(valid)` 在丢掉 `None` 之后回答的是「我观测到的那几轮都命中吗」，不是
    「三轮都命中吗」。v37 有一格耗尽重试没落盘，那个单元只剩两轮、两轮都中，于是
    被计成三轮全中，`hit@all` 报成 73/198 而真值是 72/198。缺测越多这个数字越好看，
    方向恰好是错的，所以判据必须同时约束元数与谓词。
    """

    triples = hits = items = at3 = atall = 0
    for record_id in ids:
        for _arm, series in mk._arms(verdicts[record_id]).items():
            valid = [x for x in series if x is not None]
            if not valid:
                continue
            items += 1
            triples += len(valid)
            hits += sum(valid)
            at3 += 1 if any(valid) else 0
            atall += 1 if len(valid) == rounds and all(valid) else 0
    if not items:
        return {}
    return {
        "hit@1": f"{hits}/{triples} = {hits / triples * 100:.1f}%",
        "hit@3": f"{at3}/{items} = {at3 / items * 100:.1f}%",
        "hit@all": f"{atall}/{items} = {atall / items * 100:.1f}%",
    }


def render(payload: dict, generation: str, rounds: int) -> str:
    verdicts = payload.get("verdicts") or {}
    problems = mk.validate(verdicts, payload.get("over") or {}, rounds)
    if problems:
        # 判定表不合格就不渲染。渲染出来的表会被引用，而它的分母是错的。
        raise SystemExit(
            "判定表未通过 metrics_at_k 的校验，拒绝渲染 comment：\n  - "
            + "\n  - ".join(problems)
        )
    ledger = _ledger()

    reportable = list(mk.REPORTABLE)
    coverage = collections.Counter(
        str((ledger.get(r) or {}).get("layer") or "?") for r in reportable
    )
    at_k = {layer: coverage.get(layer, 0) >= THRESHOLD for layer in LAYERS}
    blocked = [r for r in reportable if r in mk.BLOCKED]

    out = [f"# {generation} 运行结果\n"]
    # 约束 2：头部不出现任何 n/总数 形式的分数。
    out.append(
        f"**可报记录 {len(reportable)} 条**"
        + (f"（其中 {len(blocked)} 条结构性不可达）" if blocked else "")
        + f"，**达阈值（≥{THRESHOLD}）的层 {sum(at_k.values())} 层** —— "
        "本代次**不产出任何按层的能力主张**。\n"
    )
    out.append(
        "判定口径见 "
        "[`preregistered_calibre.md`](../../../project_1_llm_state_machine_modeling/"
        "paper_stm_issue_discover/discover_matrix/docs/generations/v21/preregistered_calibre.md)。\n"
    )

    header = ["记录", "层", "缺陷简述", *[f"r{i}" for i in range(1, rounds + 1)], "备注"]

    out.append(f"\n## {BAND_TITLES['hold'].format(n=len(reportable))}\n")
    out.append(_table(header, _rows(verdicts, reportable, ledger, rounds)))
    ratios = _ratios(verdicts, reportable, rounds)
    if ratios:
        out.append("\n" + " · ".join(f"**{k}** {v}" for k, v in ratios.items()) + "\n")

    # 约束 3：这张表必须实体存在。hold-out 移除后它不再恒为空，但仍必须实体给出 ——
    # 分层可报条目数是读者判断「某层的数字能不能引用」的唯一依据。
    out.append(f"\n## 达阈值的层：{sum(at_k.values())} / {len(LAYERS)}\n")
    out.append(_table(
        ["层", "可报条目", f"阈值", "可报？"],
        [[layer, str(coverage.get(layer, 0)), str(THRESHOLD),
          "✅" if at_k[layer] else "✗"] for layer in LAYERS],
    ))
    out.append(
        "\n本项目**不设 hold-out**：方法是在这批 pair 上迭代出来的，全部台账记录同等参与度量。"
        "上表给出每层的可报条目数与阈值，未达阈值的层其比率不得单独引用。\n"
        if sum(at_k.values()) else
        "\n**这张表是空的，空本身是结论** —— 没有任何一层达到阈值。\n"
    )

    dropped = sorted(r for r in verdicts if r not in set(reportable))
    if dropped:
        out.append(f"\n## 不计入分母（{len(dropped)} 条）\n")
        out.append("经边界裁定判为表示层产物而非作者缺陷，原始判定保留、不进能力分母。\n")
        out.append(_table(header, _rows(verdicts, dropped, ledger, rounds)))

    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("verdicts_json", type=pathlib.Path)
    parser.add_argument("--generation", default="v22")
    parser.add_argument("--rounds", type=int, default=3)
    args = parser.parse_args(argv)
    payload = json.loads(args.verdicts_json.read_text())
    print(render(payload, args.generation, args.rounds))
    return 0


if __name__ == "__main__":
    sys.exit(main())
