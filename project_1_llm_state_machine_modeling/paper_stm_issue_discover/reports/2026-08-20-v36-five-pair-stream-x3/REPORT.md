# v36 用户点名五格 x3 独立语义审计报告

本报告是 v36 默认 stream 传输版本的用户点名五格诊断，不是全量 headline。比较对象为 gpt-5.6-luna 下的新方法与 X1v2 baseline，pair 为 `0004、0023、0029、0046、0053`，每臂每 pair 三轮，共 21 条台账、63 个运行位置；命中由独立 gpt-5.6-luna 语义评审依据同一位置与同一性质判定，不使用关键词、字符串包含、编辑距离、embedding 或其他词法捷径。方法记录均为 `adapter=openai-responses` 且 `streaming=true`，5/5 个 judge pair 均为 `status=ok`。

## 方法侧覆盖

| 子集 | 条目数 | hit@1 | hit@3 | hit@all |
|---|---|---|---|---|
| 整体 | 21 | 35/63 | 16/21 | 6/21 |
| L2 | 11 | 18/33 | 8/11 | 2/11 |
| D2×L2 | 11 | 18/33 | 8/11 | 2/11 |

## X1v2 baseline 覆盖

| 子集 | 条目数 | hit@1 | hit@3 | hit@all |
|---|---|---|---|---|
| 整体 | 21 | 12/63 | 7/21 | 2/21 |
| L2 | 11 | 4/33 | 2/11 | 1/11 |
| D2×L2 | 11 | 4/33 | 2/11 | 1/11 |

## 质量、错误与成本

方法侧 finding 的 W/D/L 分布、accepted/confirmed 数、schema/provider/local failure 数以及每次 attempt 的计费明细见 `metrics.json`；provider retry exemption 只统计 `billing_disposition=provider_error_retry_exempt`，所有其他 attempt 都计费。该五格诊断子集的方法生成成本为 `$0.639953`，baseline 为 `$0.022600`，子集倍率为 `28.32x`，高于 25x 研究 gate；该值受五格 baseline 上下文短以及当前方法仍保留多阶段 grounding 影响，不能替代全量成本结论。独立 judge 审计成本不进入 method/baseline 倍率。

## 逐条台账对照

方法与 baseline 的逐条台账表物理分开，分别见 `ledger_method.md` 与 `ledger_baseline.md`；每个单元格是三轮中该轮的语义命中结果。正式结果要求 judge 对全部 pair 给出完整裁定，不能用全 miss 代替失败。

## 可复现边界

原始重点运行目录位于 `runs/paper1/witness-search/v36-default-stream-x3-20260820/run{1,2,3}/`；method 与 baseline 的独立 judge 原始结果位于本报告旁的 `judge-luna/`，每个 pair 均保留 ledger/emission 的自然语言 reason、confidence 与 exact supporting finding IDs。历史全量 x3 目录 `runs/paper1/luna-full-x3-20260819-v1/` 只用于 baseline 对照，不与本轮 v36 method raw record 混写。
