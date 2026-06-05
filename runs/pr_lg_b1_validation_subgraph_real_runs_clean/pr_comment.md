## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_lg_b1_validation_subgraph_real_runs_clean/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 32959 | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ❌ | ⚪ | `success_but_weak_oracle_ineligible` | 622093 | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 33601 | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | ❌ | `success` | 154512 | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196/report.md` |

### 可复现性边界

- clean commit 绑定：4/4 run 的 `reproducibility.json` 记录 dirty=false。
- prompt snapshot hash 种类：1；用于确认同一轮 4 例是否共享同一 prompt/context 版本。
- 每个 run 的 `reproducibility.json` 保存 git commit、dirty flag、diff hash、prompt file hash、runner command/config 与 source/paper path。

### LangGraph runtime metadata / checkpoint 口径

- graph_runtime_backend：`langgraph`。
- graph_runtime_status：`enabled`。
- langgraph / checkpoint 版本：langgraph=`1.2.4`；langgraph-checkpoint=`4.1.1`。
- node_edge_schema_version：`pr-langgraph.stage-nodes.v1`；checkpoint_backend=`memory`；serde=`pickle`。
- graph_config_hash：4 种；该字段绑定 registry、planned graph、resolved config、condition hash、iteration/scenario policy 与 checkpoint config，用于区分 run-level graph config。
- node trace count 范围：min=14，max=37；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：4/4 success，rejected=0，budget_exhausted=0，total_tokens=843165。
- 主结果候选：当前 3/4 个非 infrastructure run 可进入 main_result_eligible；provider/network invalid=0 个，只能作为 infrastructure evidence。

### 主结果候选 vs Path2 ref-model 蓝本边界

- Path2 run-validity：1/1 个 Path2 run 的 `main_result_eligible=true`；这只表示 run/schema/secret/trace/final verdict 可进入主结果候选。
- Path2 blueprint-validity：0/1 个 Path2 run 当前可作为 `path2_ref_model_blueprint_eligible=true`；该字段比 `main_result_eligible` 更严格。
- `path2_lng_ems`：main_result_eligible=`true`，path2_ref_model_blueprint_eligible=`false`，state_mode_decorative=`true`；reason=state_mode_decorative: final DSL is dominated by root-level forced guard reclassification; valid as FE/BVS or dispatch-classifier stress evidence, but not a Path2 ref-model blueprint
- 解释：`path2_ref_model_blueprint_eligible=false` 不会把有效 run 改成 provider invalid；它只禁止把 state-mode-decorative / 条件分类式模型宣传为 Path2 ref-model 主蓝本。

### 主要失败模式

- `success`：3 run(s)。
- `success_but_weak_oracle_ineligible`：1 run(s)。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=success_but_weak_oracle_ineligible，最大 observed iteration_count=2。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=success，最大 observed iteration_count=1。
- 实证筛选更新：外部输入变量（plant/sensor/environment read-only）与内部状态变量必须分开标注；只读外部输入可接受，但不能被误写成‘变量参与充分’。
- 实证筛选更新：纯输出变量（只写不读）可用于 Path1 行为展示，但需要 admitted-abstraction / output-only 说明；不应拿来证明变量驱动控制流。
- 实证筛选更新：若最终 DSL 的状态主要由无记忆 `! *` 条件重选，状态只是分类标签，应标为 state_mode_decorative；可作 FE/BVS 压力测试，不宜作为 Path2 state-machine ref-model 主蓝本。

### Reviewer 追加审查项：禁止样本特判 / benchmark overfit

- 后续三路 reviewer 需显式检查 agent-loop / prompt / deterministic policy 是否包含针对 ABS、CARA、Elevator、LNG EMS 或本 PR 4 个样本的 lexical special-case、case_id 分支、hard-coded hint、结果导向参数。
- 允许的优化必须是普适、可解释、可迁移的机制；例如通过 prompt 要求 LLM 区分外部输入与内部状态，而不是在代码中写样本专用词表。
- 若发现样本特判影响 blocking/advisory、repair target、scenario oracle 或主结论归类，应至少按 I 级处理；若污染 main_result_eligible 或论文结论则按 C 级处理。

### 4 例详细输入 / 输出 / artifact

<details><summary>path1 / path1_abs / default / success</summary>

#### NL 输入（原文）

```text
The paper implements the single-wheel ABS hydraulic regulator as a three-state FSM coupled with a PID-based slip controller. Wheel speed and vehicle speed are used to compute the slip ratio, and the PID output drives the Stateflow supervisor instead of sending commands directly to the hydraulic valves.

The FSM contains the states `increase`, `hold`, and `decrease`, where `increase` sets `k1=1, k2=0, n=0`, `hold` neutralizes both valves with `k1=0, k2=0, n=0`, and `decrease` sets `k1=0, k2=1, n=500` to release pressure.

The transition guards split the slip-error space into four bands: `increase -> hold` when `slp <= 0.01`, `hold -> increase` when `slp > 0.01`, `hold -> decrease` when `slp < -0.01`, and `decrease -> hold` when `slp >= -0.01`.

This gives a concrete discrete supervisor that maps slip-error thresholds to inlet-valve, return-valve, and pump actions while the continuous wheel-slip dynamics remain in the plant model.
```

#### NL 输入中文翻译

```text
论文把单轮 ABS 液压调节器实现为一个三状态 FSM，并与基于滑移率的 PID 控制器耦合。轮速与车速用于计算滑移率，PID 输出驱动 Stateflow 监督器，而不是直接发送液压阀命令。

FSM 包含 `increase`、`hold`、`decrease` 三个状态：`increase` 设置 `k1=1, k2=0, n=0`，`hold` 设置 `k1=0, k2=0, n=0`，`decrease` 设置 `k1=0, k2=1, n=500` 以释放压力。

转移 guard 把滑移误差空间分成四个区间：`increase -> hold` 当 `slp <= 0.01`，`hold -> increase` 当 `slp > 0.01`，`hold -> decrease` 当 `slp < -0.01`，`decrease -> hold` 当 `slp >= -0.01`。

这给出了一个具体的离散监督器，把滑移误差阈值映射为进油阀、回油阀与泵动作，而连续轮胎滑移动力学仍留在被控对象模型中。
```

#### FCSTM 输出

```pyfcstm
def float slp = 0.0;
def int k1 = 0;
def int k2 = 0;
def int n = 0;

state SingleWheelABSHydraulicRegulator {
    [*] -> increase;

    state increase {
        enter {
            k1 = 1;
            k2 = 0;
            n = 0;
        }
    }

    state hold {
        enter {
            k1 = 0;
            k2 = 0;
            n = 0;
        }
    }

    state decrease {
        enter {
            k1 = 0;
            k2 = 1;
            n = 500;
        }
    }

    increase -> hold : if [slp <= 0.01];
    hold -> increase : if [slp > 0.01];
    hold -> decrease : if [slp < -0.01];
    decrease -> hold : if [slp >= -0.01];
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| main_result_eligible | `true` |
| path2_ref_model_blueprint | `n/a`；not_applicable_to_path1 |
| state_mode_decorative | `false` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 26850, 'completion_tokens': 6109, 'total_tokens': 32959, 'estimated_prompt_tokens': 26215, 'estimated_completion_tokens': 3679, 'estimated_total_tokens': 29894, 'prompt_chars': 104855, 'completion_chars': 14710, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `118.252s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726/pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726/checks.json`, `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:c01b7a9a31de821d92677137626b6c9d7a60eabb58111747c65688e2934e0576` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `16` |
| `langgraph_node_trace_hash` | `sha256:fb96b701bb9df74ebe9108c05996a7d6f6a443a5ae41b9e57d2ce16d3307f474` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `16` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=8608 | 生成初始 DSL 与 grounding seeds | initial len=634 | [`record`](./pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=12361 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=11990 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T04:16:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T04:16:54Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T04:16:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T04:16:54Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T04:17:37Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T04:17:37Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 7 | `2026-06-05T04:17:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T04:17:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T04:17:37Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726 |
| 10 | `2026-06-05T04:17:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T04:17:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 12 | `2026-06-05T04:17:37Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=634,hash=sha256:5a3dc31a6a97, current_hash=sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726 |
| 13 | `2026-06-05T04:17:37Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T04:17:37Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T04:17:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T04:17:37Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T04:17:37Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T04:17:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T04:17:37Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T04:17:37Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T04:17:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T04:17:37Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T04:18:20Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T04:18:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T04:18:20Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T04:18:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T04:18:20Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T04:18:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T04:18:20Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T04:18:20Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T04:18:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T04:18:20Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T04:18:52Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T04:18:52Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T04:18:52Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T04:18:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T04:18:52Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T04:18:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T04:18:52Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 40 | `2026-06-05T04:18:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T04:18:52Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_increase_then_hold_at_boundary` | default-init dispatches to increase with inlet-valve command, then at slp=0.01 the increase-to-hold boundary guard neutr...<truncated 14 chars> | ✅ |
| `increase_no_fire_above_upper_boundary` | explicit-hot-start in increase with slp just above 0.01 must not take the increase-to-hold guard. | ✅ |
| `hold_to_increase_above_upper_boundary` | explicit-hot-start in hold with slp greater than 0.01 must transition to increase and set inlet-valve outputs. | ✅ |
| `hold_no_fire_at_upper_boundary` | explicit-hot-start in hold with slp exactly 0.01 must not satisfy the strict hold-to-increase guard. | ✅ |
| `hold_to_decrease_below_lower_boundary` | explicit-hot-start in hold with slp below -0.01 must transition to decrease and command pressure release. | ✅ |
| `hold_no_fire_at_lower_boundary` | explicit-hot-start in hold with slp exactly -0.01 must not satisfy the strict hold-to-decrease guard. | ✅ |
| `decrease_to_hold_at_lower_boundary` | explicit-hot-start in decrease with slp exactly -0.01 must transition to hold and neutralize both valves. | ✅ |
| `decrease_no_fire_below_lower_boundary` | explicit-hot-start in decrease with slp below -0.01 must not satisfy the decrease-to-hold guard and must keep pressure-r...<truncated 15 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1593, 'completion_chars': 5676, 'completion_tokens': 2215, 'elapsed_seconds': 43.010411252005724, 'estimated_completion_tokens': 1419, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 7912, 'first_chunk_seconds': 14.525703488005092, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 8608}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1075, 'completion_chars': 3813, 'completion_tokens': 2240, 'elapsed_seconds': 42.542794746987056, 'estimated_completion_tokens': 954, 'estimated_prompt_tokens': 9952, 'estimated_total_tokens': 10906, 'first_chunk_seconds': 23.36069489197689, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39805, 'prompt_tokens': 10121, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12361}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1135, 'completion_chars': 5221, 'completion_tokens': 1654, 'elapsed_seconds': 31.65918519499246, 'estimated_completion_tokens': 1306, 'estimated_prompt_tokens': 9770, 'estimated_total_tokens': 11076, 'first_chunk_seconds': 11.193569430994103, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39078, 'prompt_tokens': 10336, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 11990}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_abs-default-lg-b1-clean-20260605-121653-020bd726/report.md` §7。

</details>

<details><summary>path1 / path1_cara / default / success</summary>

#### NL 输入（原文）

```text
At run time, CARA coordinates the Caregiver Interface, Blood Pressure Monitor, Algorithm, and Pump Monitors around an infusion pump that moves fluid into the patient, while sensor readings are stored in a shared buffer for software access. The pump has manual and autocontrol modes. In manual mode, pump speed is set with the built-in switch and the caregiver sets a default flow rate directly on the pump for manual operation, while in autocontrol mode pump speed is set by a control voltage from an external source. The Algorithm component controls infusion rate and records infusion-related data in log files; patient blood pressure is used to compute the infusion rate, with higher pressure producing a lower flow rate. The Caregiver Interface lets the caregiver modify target blood pressure and initiate or terminate algorithmic pump control, and it also displays and sounds error messages. In the Mode_Control_Algorithm hierarchy, CARA has manual and autocontrol-related mode-control states plus an Ask_StartAC submode; within Ask_StartAC, the setpoint can be changed and pressing StartAC enters AutocontrolInit. During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications. If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. As a cross-component fallback, CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual, making manual operation the shared recovery target.
```

#### NL 输入中文翻译

```text
运行时，CARA 围绕一台向患者输液的输液泵协调 Caregiver Interface、Blood Pressure Monitor、Algorithm 与 Pump Monitors，传感器读数会写入共享缓冲区供软件访问。泵具有手动和自动控制两种模式。手动模式下，泵速由内置开关设置，护理人员直接在泵上设置默认流量；自动控制模式下，泵速由外部控制电压设置。Algorithm 组件控制输液速率并记录输液相关日志；患者血压用于计算输液速率，血压越高流量越低。Caregiver Interface 允许护理人员修改目标血压，并启动或终止算法泵控制，同时显示和发出错误消息。在 Mode_Control_Algorithm 层次中，CARA 具有手动与自动控制相关的模式控制状态以及 Ask_StartAC 子模式；在 Ask_StartAC 中可以修改设定点，按下 StartAC 会进入 AutocontrolInit。正常自动控制期间，只有没有泵操作并发症时 CARA 才控制流量。如果出现输液管堵塞等泵故障，泵会激活报警信号，护理人员排除故障；当 CARA 正在控制泵时，软件会释放控制。作为跨组件回退，CA_backManual 或 CB_backManual、CP_backManual、CC_backManual 中任一事件都会使 CA_mode 变为 Manual，使手动操作成为共享恢复目标。
```

#### FCSTM 输出

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_message = 0;
def int log_records = 0;
def float bp_reading = 120.0;
def float target_bp = 120.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float built_in_switch_speed = 1.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def float sensor_buffer_bp = 120.0;

state CARA {
    [*] -> Mode_Control_Algorithm effect {
        sensor_buffer_bp = bp_reading;
    };

    state Mode_Control_Algorithm {
        [*] -> Manual effect {
            CA_mode = 0;
            software_control = 0;
            control_voltage = 0.0;
        };

        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_voltage = 0.0;
            }
            during {
                sensor_buffer_bp = bp_reading;
                flow_rate = default_flow_rate;
                pump_speed = built_in_switch_speed;
            }
        }

        state Ask_StartAC {
            during {
                sensor_buffer_bp = bp_reading;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = bp_reading;
            }
        }

        state AutocontrolNormal {
            during {
                sensor_buffer_bp = bp_reading;
                if [pump_fault == 0] {
                    if [bp_reading > target_bp] {
                        flow_rate = flow_rate - 1.0;
                    } else if [bp_reading < target_bp] {
                        flow_rate = flow_rate + 1.0;
                    } else {
                        flow_rate = flow_rate;
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_records = log_records + 1;
                }
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                error_message = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit : StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal : if [software_control > 0];
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success_but_weak_oracle_ineligible` |
| main_result_eligible | `false` |
| path2_ref_model_blueprint | `n/a`；not_applicable_to_path1 |
| state_mode_decorative | `false` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `2` / `4` / `1` / `6` |
| token / elapsed | `{'prompt_tokens': 564485, 'completion_tokens': 57608, 'total_tokens': 622093, 'estimated_prompt_tokens': 612205, 'estimated_completion_tokens': 48731, 'estimated_total_tokens': 660936, 'prompt_chars': 2448793, 'completion_chars': 194897, 'n_calls': 15, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1089.098s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d/pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d/checks.json`, `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:d7423720ad4a2ca8ba2e862ccbd11e8e1e86f81ecb7c0b82513e93fd0e750b46` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `37` |
| `langgraph_node_trace_hash` | `sha256:de41a0deafe958300dd558bb2c086d84a638ffcedbe5790ee6a259a86fbc1d9b` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `37` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12517 | 生成初始 DSL 与 grounding seeds | initial len=2800 | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=0; blocking=0, advisory=19, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=127630 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=127630 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=127630 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=234337 | LLM per-request accept/reject + repair | candidate len=2789,2789,2944,2956 | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=4, tokens=223258 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=234337 | LLM per-request accept/reject + repair | candidate len=2789,2789,2944,2956 | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=4, tokens=223258 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=234337 | LLM per-request accept/reject + repair | candidate len=2789,2789,2944,2956 | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=4, tokens=223258 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=234337 | LLM per-request accept/reject + repair | candidate len=2789,2789,2944,2956 | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=223258 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=0; blocking=0, advisory=19, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=127630 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=127630 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=1, tokens=24351 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T04:16:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T04:16:54Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T04:16:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T04:16:54Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T04:18:47Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T04:18:47Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2800,hash=sha256:6856744fb026 |
| 7 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T04:18:47Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:6856744fb026d92edfa34dfb0a784ee639344b5f61d3895ce6fbee6217164637 |
| 10 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 12 | `2026-06-05T04:18:47Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2800,hash=sha256:6856744fb026, current_hash=sha256:6856744fb026d92edfa34dfb0a784ee639344b5f61d3895ce6fbee6217164637 |
| 13 | `2026-06-05T04:18:47Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T04:18:47Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T04:18:47Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T04:18:47Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T04:18:47Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T04:18:47Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T04:18:47Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T04:20:04Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T04:20:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T04:20:04Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T04:20:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T04:20:04Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T04:21:37Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T04:21:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T04:21:37Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T04:21:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T04:21:37Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T04:23:43Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T04:23:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T04:23:43Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T04:23:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T04:23:43Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T04:23:43Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T04:23:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T04:23:43Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T04:23:43Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 42 | `2026-06-05T04:23:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T04:23:43Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 21, "n_scenarios_passed": 12, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 44 | `2026-06-05T04:23:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T04:23:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-05T04:23:43Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 21, "n_scenarios_passed": 12, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2800,hash=sha256:6856744fb026 |
| 47 | `2026-06-05T04:23:43Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 48 | `2026-06-05T04:23:43Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 9} | <none> |
| 49 | `2026-06-05T04:23:43Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2800,hash=sha256:6856744fb026 |
| 50 | `2026-06-05T04:24:41Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 51 | `2026-06-05T04:24:41Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-d861f18d08", "fixreq-0-sd6-1-b89694a3d8", "fixreq-0-sd6-2-6c81985d39", "fixreq-0-sd6-3-1378209e1f", "fixreq-0-sd6-4-f6b978093f", "fixreq-0-sd6-5-0a776f9d52", "fixreq-0-sd6-6-f42b9b46c4", "fixreq-0-sd6-7-daa3842279", "fixreq-0-sd6-8-5b0d4084ef"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2789,hash=sha256:933d32f6f2b7 |
| 52 | `2026-06-05T04:24:41Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 53 | `2026-06-05T04:24:41Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:933d32f6f2b756fb04e951511407508e0121e37fcc9cd5bdb9814d0584b46108 |
| 54 | `2026-06-05T04:25:05Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 55 | `2026-06-05T04:25:05Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 56 | `2026-06-05T04:25:05Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 57 | `2026-06-05T04:25:05Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2800,hash=sha256:6856744fb026 |
| 58 | `2026-06-05T04:26:08Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 59 | `2026-06-05T04:26:08Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-d861f18d08", "f
... <truncated 3941 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 |
|---|---|---|---|
| `default_init_manual_outputs` | default-init verifies CARA dispatches into Manual and manual operation uses caregiver/default pump settings. | ✅ | ✅ |
| `initiate_change_setpoint_start_autocontrol` | default-init exercises InitiateAC, ChangeSetpoint in Ask_StartAC, and StartAC entering AutocontrolInit. | ⚪ | ✅ |
| `terminate_from_ask_returns_manual` | explicit-hot-start verifies caregiver TerminateAC from Ask_StartAC returns to the Manual recovery target. | ⚪ | ✅ |
| `autocontrol_high_pressure_lowers_flow` | explicit-hot-start verifies normal autocontrol lowers flow when patient blood pressure is above target. | ✅ | ✅ |
| `autocontrol_low_pressure_raises_flow` | explicit-hot-start verifies normal autocontrol raises flow when patient blood pressure is below target. | ✅ | ✅ |
| `autocontrol_pump_fault_and_removal` | explicit-hot-start verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved returns to Manual releasing ...<truncated 17 chars> | ⚪ | ✅ |
| `terminate_from_normal_returns_manual` | explicit-hot-start verifies caregiver TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-spee...<truncated 11 chars> | ⚪ | ✅ |
| `normal_autocontrol_no_control_when_fault_present` | explicit-hot-start no-fire probe verifies normal autocontrol does not adjust flow/log when pump-operation complications ...<truncated 6 chars> | ✅ | ✅ |
| `forced_back_manual_events_from_distinct_states` | explicit-hot-start probes cross-component fallback events from multiple non-manual leaves, all forcing Manual. | ✅ | ✅ |
| `forced_back_manual_ca_cp_cc_coverage` | explicit-hot-start probes remaining cross-component fallback events CA_backManual, CP_backManual, and CC_backManual to M...<truncated 6 chars> | ✅ | ✅ |
| `cp_back_manual_from_pump_fault_target_and_effects` | explicit-hot-start strengthens forced CP_backManual from PumpFault, asserting wrong-target mutations and Manual enter re...<truncated 15 chars> | ✅ | ✅ |
| `cc_back_manual_from_init_target_and_effects` | explicit-hot-start strengthens forced CC_backManual from AutocontrolInit, asserting Manual as exact target and software-...<truncated 16 chars> | ✅ | ✅ |
| `change_setpoint_effect_exact_value` | explicit-hot-start isolates ChangeSetpoint self-transition and checks the target_bp effect is exactly a one-unit increas...<truncated 2 chars> | ⚪ | ✅ |
| `pump_fault_detected_effect_exact_value` | explicit-hot-start isolates PumpFaultDetected and checks both the PumpFault target and the pump/alarm/software-control e...<truncated 7 chars> | ⚪ | ✅ |
| `fault_removed_effect_exact_reset_values` | explicit-hot-start isolates FaultRemoved and checks fault/alarm/error reset values plus Manual recovery target. | ⚪ | ✅ |
| `initiate_ac_exact_target_from_manual` | explicit-hot-start isolates caregiver InitiateAC from Manual and asserts the exact Ask_StartAC target rather than anothe...<truncated 20 chars> | ⚪ | ✅ |
| `start_ac_enter_effects_exact_values` | explicit-hot-start isolates StartAC from Ask_StartAC and checks the exact AutocontrolInit target plus software-control e...<truncated 14 chars> | ⚪ | ✅ |
| `autocontrol_init_guard_to_normal_target_and_outputs` | explicit-hot-start probes the software_control guard from AutocontrolInit to the exact AutocontrolNormal target and norm...<truncated 26 chars> | ✅ | ✅ |
| `autocontrol_init_no_guard_when_control_not_enabled` | explicit-hot-start no-fire probe verifies AutocontrolInit does not enter normal autocontrol when software_control is not...<truncated 9 chars> | ✅ | ✅ |
| `ca_back_manual_from_ask_exact_target_and_manual_effects` | explicit-hot-start isolates CA_backManual from Ask_StartAC and checks exact Manual target plus Manual recovery output ef...<truncated 6 chars> | ✅ | ✅ |
| `cb_back_manual_from_normal_exact_target_and_manual_effects` | explicit-hot-start isolates CB_backManual from AutocontrolNormal and checks exact Manual target plus Manual recovery out...<truncated 12 chars> | ✅ | ✅ |
| `change_setpoint_overwrites_with_exact_increment_from_low_setpoint` | explicit-hot-start adds an effect-mutation probe for ChangeSetpoint: missing or wrong +100-style effect must not pass th...<truncated 36 chars> | ⚪ | ✅ |
| `pump_fault_detected_overwrites_stale_fault_value` | explicit-hot-start adds an effect-mutation probe for PumpFaultDetected: the transition effect must set pump_fault exactl...<truncated 61 chars> | ⚪ | ✅ |
| `fault_removed_overwrites_nonbinary_fault_alarm_error_values` | explicit-hot-start adds an effect-mutation probe for FaultRemoved: fault, alarm, and error outputs must reset exactly to...<truncated 48 chars> | ⚪ | ✅ |
| `start_ac_overwrites_stale_control_flags_exactly` | explicit-hot-start adds an effect-value probe for StartAC/AutocontrolInit entry: stale nonbinary control flags must be o...<truncated 45 chars> | ⚪ | ✅ |
| `manual_entry_
... <truncated 202 chars in PR comment; see report.md>

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-6` | initiate_change_setpoint_start_autocontrol, terminate_from_ask_returns_manual, autocontrol_pump_fault_and_removal, terminate_from_normal_returns_manual, change_setpoint_effect_exact_value, ... +4 | accept=9, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 658 chars> | `sha256:933d32f6f2b756fb04e951511407508e0121e37fcc9cd5bdb9814d0584b46108` |
| 2 | `0` | ❌ | `SD-6` | initiate_change_setpoint_start_autocontrol, terminate_from_ask_returns_manual, autocontrol_pump_fault_and_removal, terminate_from_normal_returns_manual, change_setpoint_effect_exact_value, ... +4 | accept=9, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 658 chars> | `sha256:29cc18bfbd8a369371b45238eda558b9556ee0e0ca68d1fbcf09b26de497a206` |
| 3 | `0` | ❌ | `SD-6` | initiate_change_setpoint_start_autocontrol, terminate_from_ask_returns_manual, autocontrol_pump_fault_and_removal, terminate_from_normal_returns_manual, change_setpoint_effect_exact_value, ... +4 | accept=9, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 658 chars> | `sha256:99ae00ad0dfe4674b9646e0d8f36ebf13bd9c8c2d06a8d7a58e902ef3e2923af` |
| 4 | `0` | ✅ | `SD-6` | initiate_change_setpoint_start_autocontrol, terminate_from_ask_returns_manual, autocontrol_pump_fault_and_removal, terminate_from_normal_returns_manual, change_setpoint_effect_exact_value, ... +4 | accept=9, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:ce72c8d44b302dadf9c88f390efa482afacd8764f5a6e38e3daea29e5bd8651d` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d/report.md` §7。

</details>

<details><summary>path1 / path1_elevator / default / success</summary>

#### NL 输入（原文）

```text
The automatic elevator controller is built as a finite-state machine whose state space combines floor states `F1`, `F2`, and `F3` with motion states `MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel.

In the normal workflow, the system starts from an ideal state on floor 1, chooses either the up or down branch according to floor requests, stops at the requested floor, and then immediately checks the next destination before deciding whether to continue moving.

The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as sensing inputs for arrival. From `F1`, `PS2` triggers `MU2` and `PS3` triggers `MU3`. From `F2`, `PS3` triggers `MU3` and `PS1` triggers `MD1`. From `F3`, `PS1` triggers `MD1` and `PS2` triggers `MD2`. Arrival sensors complete motion transitions: `MU2 + S2 -> F2`, `MU3 + S3 -> F3`, `MD1 + S1 -> F1`, and `MD2 + S2 -> F2`.

The `hbrg` output distinguishes upward drive, downward drive, and stop conditions. A reset signal forces the controller back to floor 1 regardless of the outstanding request context.
```

#### NL 输入中文翻译

```text
自动电梯控制器被构建为有限状态机，其状态空间由楼层状态 `F1`、`F2`、`F3` 与上/下行运动状态 `MU2`、`MU3`、`MD1`、`MD2` 组合而成。

正常流程中，系统从 1 楼理想状态开始，根据楼层请求选择上行或下行分支，在请求楼层停止，然后立即检查下一目的地以决定是否继续移动。

控制器使用 `PS1/PS2/PS3` 作为楼层请求输入，使用 `S1/S2/S3` 作为到位传感输入。从 `F1`，`PS2` 触发 `MU2`，`PS3` 触发 `MU3`；从 `F2`，`PS3` 触发 `MU3`，`PS1` 触发 `MD1`；从 `F3`，`PS1` 触发 `MD1`，`PS2` 触发 `MD2`。到位传感器完成运动转移：`MU2 + S2 -> F2`，`MU3 + S3 -> F3`，`MD1 + S1 -> F1`，`MD2 + S2 -> F2`。

`hbrg` 输出区分上行驱动、下行驱动和停止状态。复位信号会无视当前请求上下文，强制控制器回到 1 楼。
```

#### FCSTM 输出

```pyfcstm
def int hbrg = 0;

state AutomaticElevatorController {
    ! * -> F1 :: Reset;

    [*] -> F1;

    state F1 {
        enter { hbrg = 0; }
    }

    state F2 {
        enter { hbrg = 0; }
    }

    state F3 {
        enter { hbrg = 0; }
    }

    state MU2 {
        enter { hbrg = 1; }
    }

    state MU3 {
        enter { hbrg = 1; }
    }

    state MD1 {
        enter { hbrg = -1; }
    }

    state MD2 {
        enter { hbrg = -1; }
    }

    F1 -> MU2 : PS2;
    F1 -> MU3 : PS3;
    F2 -> MU3 : PS3;
    F2 -> MD1 : PS1;
    F3 -> MD1 : PS1;
    F3 -> MD2 : PS2;
    MU2 -> F2 : S2;
    MU3 -> F3 : S3;
    MD1 -> F1 : S1;
    MD2 -> F2 : S2;
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| main_result_eligible | `true` |
| path2_ref_model_blueprint | `n/a`；not_applicable_to_path1 |
| state_mode_decorative | `false` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 25978, 'completion_tokens': 7623, 'total_tokens': 33601, 'estimated_prompt_tokens': 25361, 'estimated_completion_tokens': 5723, 'estimated_total_tokens': 31084, 'prompt_chars': 101438, 'completion_chars': 22885, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `146.216s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047/pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047/checks.json`, `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:4f7b5f4c9c31487939f21b4618459774000b3fdbe81e81ca780cd0004b64d003` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `16` |
| `langgraph_node_trace_hash` | `sha256:fb96b701bb9df74ebe9108c05996a7d6f6a443a5ae41b9e57d2ce16d3307f474` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `16` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=10034 | 生成初始 DSL 与 grounding seeds | initial len=659 | [`record`](./pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13494 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10073 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T04:16:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T04:16:54Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T04:16:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T04:16:54Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T04:18:02Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T04:18:02Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=659,hash=sha256:fe4c13c35121 |
| 7 | `2026-06-05T04:18:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T04:18:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T04:18:02Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:fe4c13c35121a06dd37cf121809ebc4af1132bc518a51e0796c7a030c6b38dfc |
| 10 | `2026-06-05T04:18:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T04:18:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 12 | `2026-06-05T04:18:02Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=659,hash=sha256:fe4c13c35121, current_hash=sha256:fe4c13c35121a06dd37cf121809ebc4af1132bc518a51e0796c7a030c6b38dfc |
| 13 | `2026-06-05T04:18:02Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T04:18:02Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T04:18:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T04:18:02Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T04:18:02Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T04:18:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T04:18:02Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T04:18:02Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T04:18:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T04:18:02Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T04:18:49Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T04:18:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T04:18:49Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T04:18:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T04:18:49Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T04:18:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T04:18:49Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T04:18:49Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T04:18:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T04:18:49Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T04:19:20Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T04:19:20Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T04:19:20Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T04:19:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T04:19:20Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T04:19:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T04:19:20Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=659,hash=sha256:fe4c13c35121 |
| 40 | `2026-06-05T04:19:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T04:19:20Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=659,hash=sha256:fe4c13c35121 |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_then_up_to_f2_and_f3` | default-init probe for initial F1 stop, then request-up workflow F1->MU2->F2 and immediate next request F2->MU3->F3 with...<truncated 21 chars> | ✅ |
| `default_init_direct_request_to_f3` | default-init probe that dispatches to F1, then PS3 must choose direct upward motion MU3 and S3 must stop at F3 | ✅ |
| `hot_start_f2_down_to_f1` | explicit-hot-start probe from reachable F2: PS1 must select downward MD1 and S1 arrival must stop at F1 | ✅ |
| `hot_start_f3_down_to_f2` | explicit-hot-start probe from reachable F3: PS2 must select downward MD2 and S2 arrival must stop at F2 | ✅ |
| `hot_start_f3_down_to_f1` | explicit-hot-start probe from reachable F3: PS1 must target MD1 rather than MD2, and S1 must stop at F1 | ✅ |
| `reset_from_up_motion_forces_f1` | explicit-hot-start forced-reset probe from upward motion MU3; Reset must force F1 stop regardless of outstanding request...<truncated 8 chars> | ✅ |
| `reset_from_down_motion_forces_f1` | explicit-hot-start forced-reset probe from downward motion MD2; Reset must force F1 stop regardless of outstanding reque...<truncated 10 chars> | ✅ |
| `reset_from_floor_and_no_event_stability` | explicit-hot-start probe from floor F2: no event should leave the stopped floor unchanged, and Reset from a floor must f...<truncated 12 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3079, 'completion_chars': 10451, 'completion_tokens': 3596, 'elapsed_seconds': 67.85041947002173, 'estimated_completion_tokens': 2613, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 9136, 'first_chunk_seconds': 12.727822451008251, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10034}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1983, 'completion_chars': 7913, 'completion_tokens': 2502, 'elapsed_seconds': 47.084346313989954, 'estimated_completion_tokens': 1979, 'estimated_prompt_tokens': 10767, 'estimated_total_tokens': 12746, 'first_chunk_seconds': 11.302594626002247, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 43067, 'prompt_tokens': 10992, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13494}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1006, 'completion_chars': 4521, 'completion_tokens': 1525, 'elapsed_seconds': 30.248052367998753, 'estimated_completion_tokens': 1131, 'estimated_prompt_tokens': 8071, 'estimated_total_tokens': 9202, 'first_chunk_seconds': 13.05327587001375, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 32282, 'prompt_tokens': 8548, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10073}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path1_elevator-default-lg-b1-clean-20260605-121653-719ad047/report.md` §7。

</details>

<details><summary>path2 / path2_lng_ems / default / success</summary>

#### NL 输入（原文）

```text
The LNG-ship EMS manages a ship energy system with PVs, WECs, DGs, LNG, batteries, and time-varying ship loads, issuing cut-in and cut-out commands for generating units and loads. It controls power dispatch between generating units and load demand during changing time periods and operating conditions, dynamically switching states to maintain power balance as resources and demands vary. The FSM reads load demand PL, renewable contributions Ppv and Pw, battery state of charge SoC, and engine capacity bounds such as eng3_Pmax, then returns requested generator power, battery discharge or charging power, and spare power. The twelve finite states are selected by logical transition conditions over demand, generation, capacity, and SoC. When Ppv + Pw covers PL, the EMS serves all ship demand from RES and charges batteries while SoC is below 0.95, or treats residual renewable power as spare once SoC is at least 0.95. When Ppv + Pw is below PL, dispatch follows the stated priority: RES first, batteries when SoC is suitable, LNG before diesel units, and DG1/DG2 only as the last priority. Low-SoC branches add explicit charging margins, including Pgmax/5 in an LNG-covered case and Pd1max/10 in later diesel-generator cases. When PL = 0, RES production is sent to battery charging or to spare power according to SoC thresholds. The overload completion state is illegal: if extreme demand exceeds all RES and thermal resources, EMS activates all thermal generating units, covers the lack by battery discharge, and the state shall never occur in practice.
```

#### NL 输入中文翻译

```text
LNG 船 EMS 管理一个包含光伏、波浪能、柴油机、LNG、电池和随时间变化船舶负载的船舶能源系统，并向发电单元与负载发出切入/切出命令。它在变化的时段和运行条件下控制发电单元与负载需求之间的功率调度，随着资源和需求变化动态切换状态以保持功率平衡。FSM 读取负载需求 PL、可再生贡献 Ppv 和 Pw、电池荷电状态 SoC，以及 eng3_Pmax 等发动机容量边界，然后返回请求的发电机功率、电池放电或充电功率以及备用功率。十二个有限状态由需求、发电、容量和 SoC 上的逻辑转移条件选择。当 Ppv + Pw 覆盖 PL 时，EMS 用 RES 满足全部船舶需求，并在 SoC 低于 0.95 时给电池充电，或在 SoC 至少为 0.95 时把剩余可再生功率视为备用功率。当 Ppv + Pw 低于 PL 时，调度遵循优先级：RES 优先，SoC 合适时使用电池，LNG 先于柴油机，DG1/DG2 只作为最后优先级。低 SoC 分支加入明确充电裕量，包括 LNG 覆盖场景中的 Pgmax/5，以及后续柴油发电机场景中的 Pd1max/10。当 PL = 0 时，RES 产出根据 SoC 阈值送往电池充电或备用功率。过载完成状态是非法状态：若极端需求超过全部 RES 与热力资源，EMS 会激活全部热发电单元并用电池放电弥补缺口，该状态实践中不应发生。
```

#### FCSTM 输出

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float eng3_Pmax = 0.0;
def float Pbat_Pmax = 0.0;
def float Pg_LNG_req = 0.0;
def float Pg_DG1_req = 0.0;
def float Pg_DG2_req = 0.0;
def float Pb_discharge = 0.0;
def float Pb_charge = 0.0;
def float Pspare = 0.0;
def int cutin_LNG = 0;
def int cutout_LNG = 0;
def int cutin_DG1 = 0;
def int cutout_DG1 = 0;
def int cutin_DG2 = 0;
def int cutout_DG2 = 0;
def int cutin_load = 0;
def int cutout_load = 0;
def int overload_illegal = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoverCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoverSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischargeOnly : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
    ! * -> LNGCoverChargeMargin : if [PL > 0 && Ppv + Pw < PL && (SoC < 0.2 || PL - Ppv - Pw > Pbat_Pmax) && SoC < 0.95 && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LNGCoverNoCharge : if [PL > 0 && Ppv + Pw < PL && (SoC >= 0.95 || PL - Ppv - Pw + Pgmax / 5 > Pgmax) && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGDG1ChargeMargin : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && SoC < 0.95 && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + Pd1max];
    ! * -> LNGDG1NoCharge : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && (SoC >= 0.95 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + Pd1max) && PL - Ppv - Pw <= Pgmax + Pd1max];
    ! * -> LNGDG1DG2ChargeMargin : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + Pd1max && SoC < 0.95 && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + Pd1max + eng3_Pmax];
    ! * -> LNGDG1DG2NoCharge : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + Pd1max && (SoC >= 0.95 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + Pd1max + eng3_Pmax) && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax];
    ! * -> ExtremeOverloadIllegal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + Pd1max + eng3_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            Pg_LNG_req = 0;
            Pg_DG1_req = 0;
            Pg_DG2_req = 0;
            Pb_discharge = 0;
            Pb_charge = Ppv + Pw;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            cutin_load = 0;
            cutout_load = 1;
            overload_illegal = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pg_LNG_req = 0;
            Pg_DG1_req = 0;
            Pg_DG2_req = 0;
            Pb_discharge = 0;
            Pb_charge = 0;
            Pspare = Ppv + Pw;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            cutin_load = 0;
            cutout_load = 1;
            overload_illegal = 0;
        }
    }

    state RESCoverCharge {
        enter {
            Pg_LNG_req = 0;
            Pg_DG1_req = 0;
            Pg_DG2_req = 0;
            Pb_discharge = 0;
            Pb_charge = Ppv + Pw - PL;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            cutin_load = 1;
            cutout_load = 0;
            overload_illegal = 0;
        }
    }

    state RESCoverSpare {
        enter {
            Pg_LNG_req = 0;
            Pg_DG1_req = 0;
            Pg_DG2_req = 0;
            Pb_discharge = 0;
            Pb_charge = 0;
            Pspare = Ppv + Pw - PL;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            cutin_load = 1;
            cutout_load = 0;
            overload_illegal = 0;
        }
    }

    state BatteryDischargeOnly {
        enter {
            Pg_LNG_req = 0;
            Pg_DG1_req = 0;
            Pg_DG2_req = 0;
            Pb_discharge = PL - Ppv - Pw;
            Pb_charge = 0;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            cutin_load = 1;
            cutout_load = 0;
            overload_illegal = 0;
        }
    }

    state LNGCoverChargeMargin {
        enter {
            Pg_LNG_req = PL - Ppv - Pw + Pgmax / 5;
            Pg_DG1_req = 0;
            Pg_DG2_req = 0;
            Pb_discharge = 0;
            Pb_charge = Pgmax / 5;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            cutin_load = 1;
            cutout_load = 0;
            overload_illegal = 0;
        }
    }

    state LNGCoverNoCharge {
        enter {
            Pg_LNG_req = PL - Ppv - Pw;
            Pg_DG1_req = 0;
            Pg_DG2_req = 0;
            Pb_discharge = 0;
            Pb_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            cutin_load = 1;
            cutout_load = 0;
            overload_illegal = 0;
        }
    }

    state LNGDG1ChargeMargin {
        enter {
            Pg_LNG_req = Pgmax;
            Pg_DG1_req = PL - Ppv - Pw - Pgmax + Pd1max / 10;
            Pg_DG2_req = 0;
            Pb_discharge = 0;
            Pb_charge = Pd1max / 10;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            cutin_load = 1;
            cutout_load = 0;
            overload_illegal = 0;
        }
    }

    state LNGDG1NoCharge {
        enter {
            Pg_LNG_req = Pgmax;
            Pg_DG1_req = PL - Ppv - Pw - Pgmax;
            Pg_DG2_req = 0;
            Pb_discharge = 0;
            Pb_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            cutin_load = 1;
            cutout_load = 0;
            overload_illegal = 0;
        }
    }

    state LNGDG1DG2ChargeMargin {
        enter {
            Pg_LNG_req = Pgmax;
            Pg_DG1_req = Pd1max;
            Pg_DG2_req = PL - Ppv - Pw - Pgmax - Pd1max + Pd1max / 10;
            Pb_discharge = 0;
            Pb_charge = Pd1max / 10;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            cutin_load = 1;
            cutout_load = 0;
            overload_illegal = 0;
        }
    }

    state LNGDG1DG2NoCharge {
        enter {
            Pg_LNG_req = Pgmax;
            Pg_DG1_req = Pd1max;
            Pg_DG2_req = PL - Ppv - Pw - Pgmax - Pd1max;
            Pb_discharge = 0;
            Pb_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            cutin_load = 1;
            cutout_load = 0;
            overload_illegal = 0;
        }
    }

    state ExtremeOverloadIllegal {
        enter {
            Pg_LNG_req = Pgmax;
            Pg_DG1_req = Pd1max;
            Pg_DG2_req = eng3_Pmax;
            Pb_discharge = PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax;
            Pb_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            cutin_load = 1;
            cutout_load = 0;
            overload_illegal = 1;
        }
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| main_result_eligible | `true` |
| path2_ref_model_blueprint | `false`；state_mode_decorative: final DSL is dominated by root-level forced guard reclassification; valid as FE/BVS or dispatch-classifier stress evidence, but not a Path2 ref-model blueprint |
| state_mode_decorative | `true` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `1` / `0` / `2` |
| token / elapsed | `{'prompt_tokens': 131630, 'completion_tokens': 22882, 'total_tokens': 154512, 'estimated_prompt_tokens': 124016, 'estimated_completion_tokens': 14503, 'estimated_total_tokens': 138519, 'prompt_chars': 496058, 'completion_chars': 58005, 'n_calls': 5, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `435.261s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196/pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196/checks.json`, `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:ac6af153624be5e42f2aa895ef7222cbed63a8d4f0a5f6797c9a99516b95736a` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `14` |
| `langgraph_node_trace_hash` | `sha256:085d322947849a0edbf8d2f32f355444fffaf04b7da6e5bba6c35260cda3c159` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `14` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14940 | 生成初始 DSL 与 grounding seeds | initial len=8251 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=25, advisory=157, info=0; blocking=0, advisory=182, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=1, tokens=39630 | LLM per-request accept/reject + repair | candidate len=0 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=25, advisory=157, info=0; blocking=0, advisory=182, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=2, tokens=47520 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=2, tokens=47520 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=52422 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok_after_waiver_continue | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T04:16:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T04:16:54Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T04:16:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T04:16:54Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T04:19:31Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T04:19:31Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=8251,hash=sha256:be034e424454 |
| 7 | `2026-06-05T04:19:31Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T04:19:31Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T04:19:31Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:be034e424454b545e5f2286007c98302d86e905fc724b345a2ecbcde44f20611 |
| 10 | `2026-06-05T04:19:31Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T04:19:31Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 12 | `2026-06-05T04:19:31Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=8251,hash=sha256:be034e424454, current_hash=sha256:be034e424454b545e5f2286007c98302d86e905fc724b345a2ecbcde44f20611 |
| 13 | `2026-06-05T04:19:31Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T04:19:31Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T04:19:31Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T04:19:31Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T04:19:31Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T04:19:31Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T04:19:31Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T04:19:31Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 21 | `2026-06-05T04:19:31Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T04:19:31Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryDischargeOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoverChargeMargin", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShi...<truncated 10271 chars> | <none> |
| 23 | `2026-06-05T04:19:31Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-05T04:19:31Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T04:19:31Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryDischargeOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoverChargeMargin", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.Ba...<truncated 293332 chars> | current_dsl:len=8251,hash=sha256:be034e424454 |
| 26 | `2026-06-05T04:19:31Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 27 | `2026-06-05T04:19:31Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 12} | <none> |
| 28 | `2026-06-05T04:19:31Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=8251,hash=sha256:be034e424454 |
| 29 | `2026-06-05T04:20:12Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 30 | `2026-06-05T04:20:12Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": [], "jump": "waiver_continue_or_exit", "ok": false, "rejected_request_ids": ["fixreq-0-sd4-0-0fe77c4f8c", "fixreq-0-sd4-1-547d900884", "fixreq-0-sd4-2-eea5a4ace9", "fixreq-0-sd4-3-dd20243cf4", "fixreq-0-sd4-4-edba505ed3", "fixreq-0-sd4-5-2511cc052f", "fixreq-0-sd4-6-6434b1bcb1", "fixreq-0-sd4-7-b360164c1e", "fixreq-0-sd4-8-1a7ae0eea8", "fixreq-0-sd4-9-00424b59a6", "fixreq-0-sd4-10-d1fefcc306"...<truncated 32 chars> | <none> |
| 31 | `2026-06-05T04:20:12Z` | `SL-9` | `0` | `sl9_all_rejected_waiver_continue` | {"jump": "continue_after_current_stage"} | <none> |
| 32 | `2026-06-05T04:20:12Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": false, "jump": "waiver_continue"} | current_hash=sha256:be034e424454b545e5f2286007c98302d86e905fc724b345a2ecbcde44f20611 |
| 33 | `2026-06-05T04:20:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 34 | `2026-06-05T04:20:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T04:20:12Z` | `<control>` | `0` | `waiver_continue_validation_enter` | {"reason": "SL-9 rejected/waived non-hard SD-4 requests; continue downstream without SC-11 DSL edit"} | current_dsl:len=8251,hash=sha256:be034e424454 |
| 36 | `2026-06-05T04:20:12Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "reason": "waiver_continue_design_items_marked_non_blocking_for_downstream_validation"} | <none> |
| 37 | `2026-06-05T04:20:12Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 38 | `2026-06-05T04:21:53Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 39 | `2026-06-05T04:21:53Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 40 | `2026-06-05T04:21:53Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 41 | `2026-06-05T04:23:12Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-05T04:23:12Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 43 | `2026-06-05T04:23:12Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 44 | `2026-06-05T04:23:12Z` | `SD-6` | `0` | `stage_enter` | {"reason": "waiver_continue_scenario_set_ready"} | <none> |
| 45 | `2026-06-05T04:23:13Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 46 | `2026-06-05T04:23:13Z` | `SL-7` | `0` | `stage_enter` | {"reason": "waiver_continue_SD-6 ok"} | <none> |
| 47 | `2026-06-05T04:24:08Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 48 | `2026-06-05T04:24:08Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true} | <none> |
| 49 | `2026-06-05T04:24:08Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 50 | `2026-06-05T04:24:08Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok_after_waiver_continue", "verdict": "success"} | final_dsl:len=8251,hash=sha256:be034e424454 |
| 51 | `2026-06-05T04:24:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 52 | `2026-06-05T04:24:08Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=8251,hash=sha256:be034e424454 |
| 53 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_zero_load_charge` | default-init verifies the initial leaf for PL=0 and SoC below 0.95 sends available RES to battery charging and cuts out ...<truncated 16 chars> | ✅ |
| `zero_load_full_soc_spare_boundary` | explicit-hot-start probes the SoC=0.95 boundary for PL=0: RES must become spare power rather than battery charge. | ✅ |
| `res_covers_load_charge_below_soc_boundary` | explicit-hot-start probes Ppv+Pw covering positive PL with SoC just below 0.95: surplus RES charges the battery. | ✅ |
| `res_covers_load_spare_at_soc_boundary` | explicit-hot-start probes Ppv+Pw covering positive PL at SoC=0.95: surplus RES is spare, not charging. | ✅ |
| `battery_discharge_only_at_suitable_soc_boundary` | explicit-hot-start probes the suitable-SoC battery branch at SoC=0.2 when RES deficit is within battery power capacity. | ✅ |
| `lng_cover_low_soc_charge_margin` | explicit-hot-start probes LNG priority under low SoC: LNG covers the deficit plus Pgmax/5 charging margin. | ✅ |
| `lng_cover_full_soc_no_charge` | explicit-hot-start probes LNG-only dispatch at SoC=0.95: LNG covers the deficit with no battery charging margin. | ✅ |
| `lng_dg1_low_soc_charge_margin` | explicit-hot-start probes DG1 as next priority after LNG with low-SoC Pd1max/10 charging margin. | ✅ |
| `lng_dg1_full_soc_no_charge` | explicit-hot-start probes DG1 after LNG at SoC=0.95: DG1 covers the remaining deficit with no charging margin. | ✅ |
| `lng_dg1_dg2_low_soc_charge_margin` | explicit-hot-start probes DG2 as last priority with low-SoC Pd1max/10 charging margin after LNG and DG1 are used. | ✅ |
| `lng_dg1_dg2_full_soc_no_charge` | explicit-hot-start probes all thermal units at SoC=0.95: DG2 covers only the remaining deficit and no charging occurs. | ✅ |
| `extreme_overload_illegal_completion_probe` | explicit-hot-start probes the illegal extreme-demand completion case: all thermal units are activated and remaining lack...<truncated 22 chars> | ✅ |
| `forced_reclassify_overload_to_zero_load_charge` | explicit-hot-start targets missing wildcard forced guards by starting in overload and requiring global reclassification ...<truncated 38 chars> | ✅ |
| `forced_reclassify_zero_load_to_extreme_overload` | explicit-hot-start targets missing wildcard forced guards by starting in zero-load mode and requiring global reclassific...<truncated 52 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryDischargeOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoverChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryDischargeOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGCoverChargeMargin, ... +24 | accept=0, reject=12, waiver=12 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_real_runs_clean/pr-e1-path2_lng_ems-default-lg-b1-clean-20260605-121653-38d72196/report.md` §7。

</details>
