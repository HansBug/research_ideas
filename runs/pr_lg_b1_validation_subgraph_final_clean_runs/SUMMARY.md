# PR-E1 real agent-loop exploration summary

本文件由 `python -m method.pr_e1_real_runs` 生成，用于汇总 PR-E1 真实运行证据。非 default 条件均为显式 exploratory condition，不应直接计入 Path1/Path2 主结果。

## 0. 可复现性边界

- clean commit 绑定：4/4 run 的 `reproducibility.json` 记录 dirty=false。
- prompt snapshot hash 种类：1；用于确认同一轮 4 例是否共享同一 prompt/context 版本。
- 每个 run 的 `reproducibility.json` 保存 git commit、dirty flag、diff hash、prompt file hash、runner command/config 与 source/paper path。

## 0.1 LangGraph runtime / checkpoint 口径

- graph_runtime_backend：`langgraph`。
- graph_runtime_status：`enabled`。
- langgraph / checkpoint 版本：langgraph=`1.2.4`；langgraph-checkpoint=`4.1.1`。
- node_edge_schema_version：`pr-langgraph.stage-nodes.v1`；checkpoint_backend=`memory`；serde=`pickle`。
- graph_config_hash：4 种；该字段绑定 registry、planned graph、resolved config、condition hash、iteration/scenario policy 与 checkpoint config，用于区分 run-level graph config。
- node trace count 范围：min=16，max=101；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

## 1. 运行矩阵总览

| Path | case | config | verdict | record | clean | eligible | path2 blueprint | failure class | iter | repairs | post-accept | scenarios | tokens | elapsed | report |
|---|---|---|---|---|---:|---:|---|---|---:|---:|---|---:|---:|---:|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 1 | 0 | ⚪ 0 | 1 | 33364 | 127.1s | [pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87/report.md) |
| path1 | `path1_cara` | `default` | `not_converged` | `rejected` | ✅ | ❌ | ⚪ | `repair_review_rework_budget` | 1 | 5 | ⚪ 0 | 3 | 812107 | 886.3s | [pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e/report.md) |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 1 | 0 | ⚪ 0 | 1 | 36497 | 181.8s | [pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262/report.md) |
| path2 | `path2_lng_ems` | `default` | `not_converged` | `budget_exhausted` | ✅ | ❌ | ❌ | `model_review_or_quality` | 5 | 5 | ✅ 0/1; ❌ 1 | 13 | 715729 | 1707.4s | [pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13/report.md) |

## 2. 初步配置结论

- `default`：2/4 success，rejected=1，budget_exhausted=1，total_tokens=1597697。
  - SC-11 post-accept validation：triggered=1/4 run-level attempts，success=0，failure=1。
- 主结果候选：当前 2/4 个非 infrastructure run 可进入 main_result_eligible；provider/network invalid=0 个，只能作为 infrastructure evidence。

## 2.1 主结果候选 vs Path2 ref-model 蓝本边界

- Path2 run-validity：0/1 个 Path2 run 的 `main_result_eligible=true`；这只表示 run/schema/secret/trace/final verdict 可进入主结果候选。
- Path2 blueprint-validity：0/1 个 Path2 run 当前可作为 `path2_ref_model_blueprint_eligible=true`；该字段比 `main_result_eligible` 更严格。
- `path2_lng_ems`：main_result_eligible=`false`，path2_ref_model_blueprint_eligible=`false`，state_mode_decorative=`true`；reason=run_not_main_result_eligible
- 解释：`path2_ref_model_blueprint_eligible=false` 不会把有效 run 改成 provider invalid；它只禁止把 state-mode-decorative / 条件分类式模型宣传为 Path2 ref-model 主蓝本。

## 3. 主要失败模式

- `success`：2 run(s)。
- `model_review_or_quality`：1 run(s)。
- `repair_review_rework_budget`：1 run(s)。

## 4. Path1/Path2 样本筛选建议

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=repair_review_rework_budget，最大 observed iteration_count=1。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=model_review_or_quality，最大 observed iteration_count=5。
- 实证筛选更新：外部输入变量（plant/sensor/environment read-only）与内部状态变量必须分开标注；只读外部输入可接受，但不能被误写成‘变量参与充分’。
- 实证筛选更新：纯输出变量（只写不读）可用于 Path1 行为展示，但需要 admitted-abstraction / output-only 说明；不应拿来证明变量驱动控制流。
- 实证筛选更新：若最终 DSL 的状态主要由无记忆 `! *` 条件重选，状态只是分类标签，应标为 state_mode_decorative；可作 FE/BVS 压力测试，不宜作为 Path2 state-machine ref-model 主蓝本。

| 维度 | 推荐纳入 | 降优先级 / 排除 |
|---|---|---|
| 状态机结构 | 有明确 states/events/transitions/modes/hierarchy，且 NL 能支持这些元素 | 只有流程叙述或连续优化公式，离散状态边界不清 |
| 变量参与度 | 变量进入 guard/action/invariant/output decision；外部输入需显式标注 read-only 边界，内部状态变量需有 NL-grounded 写入 | 变量只在背景中出现（吉祥物变量）、只读但无 external-input rationale、或纯输出变量未解释其不影响控制流 |
| 事件/触发 | 有外部事件、内部事件、故障/恢复、cut-in/out 等触发 | 纯连续控制或静态功率分配，缺少事件驱动逻辑 |
| 论文证据 | `paper_content.txt` 可追溯支持 NL，必要图表可由 `paper.pdf` 核对 | 关键逻辑只在难解析图中，或抽取文本不足以复核 |
| 复杂度 | 中等复杂度，足以展示层次/guard/action，但每轮可诊断 | 过小 toy case；或超大系统导致预算内无法形成有效诊断 |
| Path1 需求 | 有 reference/signed behavior，适合和 ref model 比较 | gold/ref 过弱或人工标注不可复核 |
| Path2 需求 | 能体现变量、guard、scenario、repair/review 与 state-dependent mode memory 的利用价值 | baseline 靠状态名即可猜对，变量/guard 不影响运行，或状态只是 `! *` 条件分类标签 |

筛选原则：先定义标准，再筛样本；被排除样本必须记录原因，不能为了结果好看事后 cherry-pick。

## 5. 后续 reviewer 关注点

- 是否已有足够 run record/report 证明 PR-E1 达成“实测 agent-loop 参数探索与问题闭环”的目标。
- C/I 级问题只应指向学术可靠性、可复现性、run-record/secret/schema 污染或主结论越界；纯工程 polish 默认 M。
- 若 reviewer 建议 micro-fix，必须不改变 SC/SD/SL stage graph，并用 paired rerun 对比。
- 必须审查是否存在针对 ABS/CARA/Elevator/LNG 等具体样本的 lexical special-case、hard-coded hint、case_id 分支或 benchmark overfit；这类不具备普适性/学术解释力的优化应按 C/I 级处理。
