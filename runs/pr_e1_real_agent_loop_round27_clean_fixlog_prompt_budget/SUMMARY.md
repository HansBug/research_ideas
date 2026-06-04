# PR-E1 real agent-loop exploration summary

本文件由 `python -m method.pr_e1_real_runs` 生成，用于汇总 PR-E1 真实运行证据。非 default 条件均为显式 exploratory condition，不应直接计入 Path1/Path2 主结果。

## 0. 可复现性边界

- clean commit 绑定：6/6 run 的 `reproducibility.json` 记录 dirty=false。
- prompt snapshot hash 种类：1；用于确认同一轮 4 例是否共享同一 prompt/context 版本。
- 每个 run 的 `reproducibility.json` 保存 git commit、dirty flag、diff hash、prompt file hash、runner command/config 与 source/paper path。

## 1. 运行矩阵总览

| Path | case | config | verdict | record | clean | eligible | failure class | iter | repairs | scenarios | tokens | elapsed | report |
|---|---|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | `success` | 1 | 0 | 1 | 33488 | 128.8s | [pr-e1-path1_abs-default-round27cleanbudget-9ecd07b0](./pr-e1-path1_abs-default-round27cleanbudget-9ecd07b0/report.md) |
| path1 | `path1_cara` | `default` | `provider_error` | `error` | ✅ | ❌ | `provider_or_retry` | 1 | 0 | 0 | ~11600 est (usage unavailable; chars=25924/20476) | 263.6s | [pr-e1-path1_cara-default-round27cleanbudget-a69af242](./pr-e1-path1_cara-default-round27cleanbudget-a69af242/report.md) |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | `success` | 1 | 0 | 1 | 34688 | 158.2s | [pr-e1-path1_elevator-default-round27cleanbudget-c4fe0761](./pr-e1-path1_elevator-default-round27cleanbudget-c4fe0761/report.md) |
| path2 | `path2_lng_ems` | `default` | `provider_error` | `error` | ✅ | ❌ | `provider_or_retry` | 1 | 1 | 0 | ~50739 est (usage unavailable; chars=179994/22957) | 263.8s | [pr-e1-path2_lng_ems-default-round27cleanbudget-1debbf4e](./pr-e1-path2_lng_ems-default-round27cleanbudget-1debbf4e/report.md) |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ✅ | `success` | 2 | 2 | 3 | 186803 | 485.7s | [pr-e1-path1_cara-default-round27rerun-71a4416d](./pr-e1-path1_cara-default-round27rerun-71a4416d/report.md) |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | `success` | 3 | 2 | 7 | 555370 | 1052.4s | [pr-e1-path2_lng_ems-default-round27rerun-a8182d03](./pr-e1-path2_lng_ems-default-round27rerun-a8182d03/report.md) |

## 2. 初步配置结论

- `default`：4/6 success，rejected=0，budget_exhausted=0，total_tokens=810349。
- 主结果候选：当前 4/6 run 可进入 main_result_eligible；其余只能作为 exploratory / infrastructure evidence。

## 3. 主要失败模式

- `success`：4 run(s)。
- `provider_or_retry`：2 run(s)。

## 4. Path1/Path2 样本筛选建议

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=provider_or_retry, success，最大 observed iteration_count=2。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=provider_or_retry, success，最大 observed iteration_count=3。

| 维度 | 推荐纳入 | 降优先级 / 排除 |
|---|---|---|
| 状态机结构 | 有明确 states/events/transitions/modes/hierarchy，且 NL 能支持这些元素 | 只有流程叙述或连续优化公式，离散状态边界不清 |
| 变量参与度 | 变量进入 guard/action/invariant/output decision，并存在事件或动作可更新变量值 | 变量只在背景中出现，或仅作为 guard 常量被读取但从不写入，即“吉祥物变量” |
| 事件/触发 | 有外部事件、内部事件、故障/恢复、cut-in/out 等触发 | 纯连续控制或静态功率分配，缺少事件驱动逻辑 |
| 论文证据 | `paper_content.txt` 可追溯支持 NL，必要图表可由 `paper.pdf` 核对 | 关键逻辑只在难解析图中，或抽取文本不足以复核 |
| 复杂度 | 中等复杂度，足以展示层次/guard/action，但每轮可诊断 | 过小 toy case；或超大系统导致预算内无法形成有效诊断 |
| Path1 需求 | 有 reference/signed behavior，适合和 ref model 比较 | gold/ref 过弱或人工标注不可复核 |
| Path2 需求 | 能体现变量、guard、scenario、repair/review 的利用价值 | baseline 靠状态名即可猜对，或变量/guard 不影响运行 |

筛选原则：先定义标准，再筛样本；被排除样本必须记录原因，不能为了结果好看事后 cherry-pick。

## 5. 后续 reviewer 关注点

- 是否已有足够 run record/report 证明 PR-E1 达成“实测 agent-loop 参数探索与问题闭环”的目标。
- C/I 级问题只应指向学术可靠性、可复现性、run-record/secret/schema 污染或主结论越界；纯工程 polish 默认 M。
- 若 reviewer 建议 micro-fix，必须不改变 SC/SD/SL stage graph，并用 paired rerun 对比。
- 必须审查是否存在针对 ABS/CARA/Elevator/LNG 等具体样本的 lexical special-case、hard-coded hint、case_id 分支或 benchmark overfit；这类不具备普适性/学术解释力的优化应按 C/I 级处理。
