# PR-E1 real agent-loop exploration summary

本文件由 `python -m method.pr_e1_real_runs` 生成，用于汇总 PR-E1 真实运行证据。非 default 条件均为显式 exploratory condition，不应直接计入 Path1/Path2 主结果。

## 1. 运行矩阵总览

| Path | case | config | verdict | record | eligible | failure class | iter | repairs | scenarios | tokens | elapsed | report |
|---|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---|
| path2 | `path2_lng_ems` | `default` | `not_converged` | `rejected` | ❌ | `design_or_variable_dynamics` | 1 | 1 | 0 | 32838 | 120.9s | [pr-e1-path2_lng_ems-default-promptfix3-84c81104](./pr-e1-path2_lng_ems-default-promptfix3-84c81104/report.md) |

## 2. 初步配置结论

- `default`：0/1 success，rejected=1，budget_exhausted=0，total_tokens=32838。
- 当前证据尚未显示单纯增加 `max_iterations` 足以解决问题；若 run 早停于 `rejected`，瓶颈更可能是 prompt/repair candidate quality 或样本变量语义，而不是迭代预算本身。

## 3. 主要失败模式

- `design_or_variable_dynamics`：1 run(s)。
- `design_or_variable_dynamics` 与变量只读不写、guard 变量永不变化等风险相关，需在样本筛选和 SL-9 prompt 中区分环境输入变量与内部状态变量。

## 4. Path1/Path2 样本筛选建议

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
