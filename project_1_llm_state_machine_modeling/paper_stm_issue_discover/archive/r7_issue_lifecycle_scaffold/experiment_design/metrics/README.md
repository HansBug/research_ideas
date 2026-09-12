# metrics/ — future source-level issue metrics placeholder

本目录当前只保留 metrics 入口占位。R5.7 的 `objective_metric_framework.md` 已随 Better STM 框架归档到 [../../archive/r5_7_better_stm_snapshot/experiment_design/metrics/objective_metric_framework.md](../../../r5_7_better_stm_snapshot/experiment_design/metrics/objective_metric_framework.md)，不得继续作为 active metric / rubric 真源。

## 1. 当前状态

| 项 | 状态 |
|---|---|
| final metrics | 未冻结 |
| primary / secondary endpoints | 未冻结 |
| numeric thresholds / statistical tests | 未冻结 |
| baseline contract | 未冻结 |
| LLM / human judge prompt | 未冻结 |

冻结这些内容的前置条件是：pilot 至少产出真实 issue ledger、repair/change ledger、validated post-Confirm semantic-root export bundle、fresh canonical raw/source `STM_k` 与 semantic change/correspondence ledger，并完成 closure / regression audit 的最小 dry-run。

## 2. 未来指标方向（候选，不是冻结协议）

后续 `PR-eval-rubric` 可考虑围绕以下对象重建指标：

1. issue discovery coverage / precision：Discover roots 是否有足够 NL/source/behavior 或 source-internal evidence 支撑其 assessment，且 candidate-only 不被误计为 repair-eligible。
2. confirmed issue closure：每个 confirmed issue 是否被修复、部分闭合、未闭合或 unknown。
3. regression：修复后是否引入新的 source-level behavioral issue。
4. canonical source export success：accepted semantic roots 是否被完整生成到 fresh raw/source `STM_k`，且 compiler-owned scaffold 为 `0`。
5. trace completeness：issue、accepted change、exported semantic root、closure 之间是否有可审计链路。
6. cost / stability：迭代次数、失败率、provider drift、人工仲裁负担等辅助指标。

这些只是设计方向，不能提前写成实验结论。

## 3. 禁止误读

- 不用 archived Better STM objective metrics 支撑当前 paper1 主张。
- 不用 parse ok、inspect ok、conversion success 或 `.fcstm` 可运行性单独证明修复有效。
- 不用 constructed `STM_k` / blind adjudication score 作为正式 metric。
- 不在 pilot 前设定为了迎合结果的阈值。

## 4. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-07 23:40:00 | `PR-better-archive` 后改为 future source-level issue metrics placeholder；旧 objective metric framework 指向 cold archive。 |
