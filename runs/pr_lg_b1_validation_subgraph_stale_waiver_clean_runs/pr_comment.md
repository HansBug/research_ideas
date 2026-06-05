## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 40576 | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ❌ | ⚪ | `success_but_weak_oracle_ineligible` | 99383 | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 34330 | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f/report.md` |
| path2 | `path2_lng_ems` | `default` | `not_converged` | `budget_exhausted` | ✅ | ❌ | ❌ | `scenario_or_sim_oracle` | 606386 | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34/report.md` |

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
- node trace count 范围：min=16，max=87；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：3/4 success，rejected=0，budget_exhausted=1，total_tokens=780675。
- 主结果候选：当前 2/4 个非 infrastructure run 可进入 main_result_eligible；provider/network invalid=0 个，只能作为 infrastructure evidence。

### 主结果候选 vs Path2 ref-model 蓝本边界

- Path2 run-validity：0/1 个 Path2 run 的 `main_result_eligible=true`；这只表示 run/schema/secret/trace/final verdict 可进入主结果候选。
- Path2 blueprint-validity：0/1 个 Path2 run 当前可作为 `path2_ref_model_blueprint_eligible=true`；该字段比 `main_result_eligible` 更严格。
- `path2_lng_ems`：main_result_eligible=`false`，path2_ref_model_blueprint_eligible=`false`，state_mode_decorative=`true`；reason=run_not_main_result_eligible
- 解释：`path2_ref_model_blueprint_eligible=false` 不会把有效 run 改成 provider invalid；它只禁止把 state-mode-decorative / 条件分类式模型宣传为 Path2 ref-model 主蓝本。

### 主要失败模式

- `success`：2 run(s)。
- `scenario_or_sim_oracle`：1 run(s)。
- `success_but_weak_oracle_ineligible`：1 run(s)。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=success_but_weak_oracle_ineligible，最大 observed iteration_count=1。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=scenario_or_sim_oracle，最大 observed iteration_count=5。
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
def float wheel_speed = 0.0;
def float vehicle_speed = 0.0;
def float pid_output = 0.0;
def int k1 = 0;
def int k2 = 0;
def int n = 0;

state ABSHydraulicRegulator {
    [*] -> increase;

    state increase {
        during {
            k1 = 1;
            k2 = 0;
            n = 0;
        }
    }

    state hold {
        during {
            k1 = 0;
            k2 = 0;
            n = 0;
        }
    }

    state decrease {
        during {
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
| token / elapsed | `{'prompt_tokens': 32792, 'completion_tokens': 7784, 'total_tokens': 40576, 'estimated_prompt_tokens': 31679, 'estimated_completion_tokens': 5422, 'estimated_total_tokens': 37101, 'prompt_chars': 126713, 'completion_chars': 21679, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `149.693s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1/pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1/checks.json`, `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:62c9e05994a7b1fc3af689a8c07a74a248362891ddadcc2c0b66b8e7b3aaac16` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9285 | 生成初始 DSL 与 grounding seeds | initial len=714 | [`record`](./pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=24, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13776 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=17515 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T09:37:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T09:37:30Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T09:37:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T09:37:30Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T09:38:24Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T09:38:24Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=714,hash=sha256:6e32dbdb863a |
| 7 | `2026-06-05T09:38:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T09:38:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T09:38:24Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:6e32dbdb863a17476b96099056015c41b17a171d93ab0fc7f3da6a92fb25d65b |
| 10 | `2026-06-05T09:38:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T09:38:24Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=714,hash=sha256:6e32dbdb863a, current_hash=sha256:6e32dbdb863a17476b96099056015c41b17a171d93ab0fc7f3da6a92fb25d65b |
| 12 | `2026-06-05T09:38:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T09:38:24Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T09:38:24Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T09:38:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T09:38:24Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T09:38:24Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T09:38:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T09:38:24Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T09:38:24Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T09:38:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T09:38:24Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T09:39:10Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T09:39:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T09:39:10Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T09:39:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T09:39:10Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T09:39:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T09:39:10Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T09:39:10Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T09:39:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T09:39:10Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T09:39:59Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T09:39:59Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T09:39:59Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T09:39:59Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T09:39:59Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T09:39:59Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T09:39:59Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=714,hash=sha256:6e32dbdb863a |
| 40 | `2026-06-05T09:39:59Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T09:39:59Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=714,hash=sha256:6e32dbdb863a |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_enters_increase_outputs` | default-init verifies the assumed initial leaf is increase and its valve/pump outputs are applied after the first dispat...<truncated 9 chars> | ✅ |
| `increase_to_hold_boundary` | explicit-hot-start probes the increase->hold guard boundary: slp just above 0.01 must not fire, while slp exactly 0.01 m...<truncated 9 chars> | ✅ |
| `increase_to_hold_at_threshold` | explicit-hot-start verifies increase transitions exactly to hold when slp <= 0.01 and hold neutralizes both valves. | ✅ |
| `hold_to_increase_boundary` | explicit-hot-start probes hold->increase guard: slp equal to 0.01 must stay hold, but slp above 0.01 must transition to ...<truncated 9 chars> | ✅ |
| `hold_to_increase_above_threshold` | explicit-hot-start verifies hold transitions exactly to increase when slp > 0.01 and increase commands inlet pressure. | ✅ |
| `hold_to_decrease_boundary` | explicit-hot-start probes hold->decrease guard: slp equal to -0.01 must stay hold, but slp below -0.01 must transition t...<truncated 11 chars> | ✅ |
| `hold_to_decrease_below_threshold` | explicit-hot-start verifies hold transitions exactly to decrease when slp < -0.01 and decrease releases pressure with pu...<truncated 13 chars> | ✅ |
| `decrease_to_hold_boundary` | explicit-hot-start probes decrease->hold guard: slp below -0.01 must not fire, while slp exactly -0.01 must return to ho...<truncated 3 chars> | ✅ |
| `decrease_to_hold_at_threshold` | explicit-hot-start verifies decrease transitions exactly to hold when slp >= -0.01 and hold neutralizes both valves and ...<truncated 5 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2388, 'completion_chars': 8053, 'completion_tokens': 2892, 'elapsed_seconds': 54.5580154620111, 'estimated_completion_tokens': 2014, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 8507, 'first_chunk_seconds': 13.664160971005913, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9285}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1768, 'completion_chars': 6453, 'completion_tokens': 2287, 'elapsed_seconds': 45.140531288983766, 'estimated_completion_tokens': 1614, 'estimated_prompt_tokens': 11263, 'estimated_total_tokens': 12877, 'first_chunk_seconds': 13.2826738129952, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 45049, 'prompt_tokens': 11489, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13776}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1568, 'completion_chars': 7173, 'completion_tokens': 2605, 'elapsed_seconds': 48.92870709000272, 'estimated_completion_tokens': 1794, 'estimated_prompt_tokens': 13923, 'estimated_total_tokens': 15717, 'first_chunk_seconds': 21.964407302992186, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 55692, 'prompt_tokens': 14910, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 17515}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-stale-waiver-2a93a82c-89ec9fd1/report.md` §7。

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
def int pump_fault = 0;
def int alarm_signal = 0;
def int software_control = 0;
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float target_bp = 100.0;
def float target_bp_command = 100.0;
def float flow_rate = 0.0;
def float default_manual_flow_rate = 0.0;
def float builtin_switch_speed = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float infusion_log_rate = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_voltage = 0.0;
                flow_rate = default_manual_flow_rate;
                pump_speed = builtin_switch_speed;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                flow_rate = default_manual_flow_rate;
                pump_speed = builtin_switch_speed;
            }
        }

        state Ask_StartAC {
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            during {
                sensor_buffer_bp = blood_pressure;
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    infusion_log_rate = flow_rate;
                }
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        Manual -> Ask_StartAC :: InitiateAlgorithmicControl;
        Ask_StartAC -> Ask_StartAC :: SetpointChanged effect {
            target_bp = target_bp_command;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC effect {
            software_control = 1;
            CA_mode = 1;
        };
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual :: TerminateAlgorithmicControl;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: CaregiverRemovesFault effect {
            pump_fault = 0;
            alarm_signal = 0;
        };
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `3` |
| token / elapsed | `{'prompt_tokens': 79209, 'completion_tokens': 20174, 'total_tokens': 99383, 'estimated_prompt_tokens': 81094, 'estimated_completion_tokens': 16018, 'estimated_total_tokens': 97112, 'prompt_chars': 324365, 'completion_chars': 64067, 'n_calls': 5, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `379.371s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78/pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78/checks.json`, `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:5c962c628cf4722c88349e5a920dd11465e76171f36e6b0e8a1b21b76fac8185` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `20` |
| `langgraph_node_trace_hash` | `sha256:0275a55617f1fbea9405e3ae8b4ef64da7b526ab57d2e353aebdb2200aa99d67` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `20` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12256 | 生成初始 DSL 与 grounding seeds | initial len=2843 | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=20, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=63595 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=63595 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=63595 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=23532 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T09:37:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T09:37:30Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T09:37:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T09:37:30Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T09:39:17Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T09:39:17Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2843,hash=sha256:691c0b28fabc |
| 7 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T09:39:17Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:691c0b28fabc7e9dbe3443abafac6dda253d354c480d9f1670e6257a5bf3e921 |
| 10 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T09:39:17Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2843,hash=sha256:691c0b28fabc, current_hash=sha256:691c0b28fabc7e9dbe3443abafac6dda253d354c480d9f1670e6257a5bf3e921 |
| 12 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T09:39:17Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T09:39:17Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T09:39:17Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T09:39:17Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T09:39:17Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T09:39:17Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T09:39:17Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T09:40:37Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T09:40:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T09:40:37Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T09:40:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T09:40:37Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T09:41:31Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T09:41:31Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T09:41:32Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T09:41:32Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T09:41:32Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T09:42:54Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T09:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T09:42:54Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T09:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T09:42:54Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T09:42:54Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T09:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T09:42:54Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T09:42:54Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-05T09:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T09:42:54Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 44 | `2026-06-05T09:43:48Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 45 | `2026-06-05T09:43:48Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 46 | `2026-06-05T09:43:48Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 47 | `2026-06-05T09:43:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-05T09:43:48Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 49 | `2026-06-05T09:43:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 50 | `2026-06-05T09:43:48Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=2843,hash=sha256:691c0b28fabc |
| 51 | `2026-06-05T09:43:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 52 | `2026-06-05T09:43:48Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=2843,hash=sha256:691c0b28fabc |
| 53 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 54 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_manual_outputs` | default-init dispatches into Manual and checks manual pump speed/flow come from the built-in switch and default manual f...<truncated 9 chars> | ✅ |
| `initiate_and_change_setpoint_in_ask_startac` | default-init first reaches Manual, then caregiver initiates algorithmic control and changes the setpoint within Ask_Star...<truncated 4 chars> | ✅ |
| `start_ac_init_then_normal_control` | explicit-hot-start in Ask_StartAC checks StartAC enters AutocontrolInit, then automatic progression reaches normal autoc...<truncated 30 chars> | ✅ |
| `autocontrol_no_fault_boundary_stays_normal` | explicit-hot-start in AutocontrolNormal with pump_fault at the no-fault boundary verifies no fault transition fires and ...<truncated 24 chars> | ✅ |
| `pump_fault_boundary_enters_fault_and_alarms` | explicit-hot-start in AutocontrolNormal with pump_fault present verifies transition to PumpFault activates alarm and rel...<truncated 23 chars> | ✅ |
| `caregiver_removes_fault_returns_manual` | explicit-hot-start in PumpFault checks caregiver fault removal returns to Manual, clears the fault/alarm, and keeps soft...<truncated 22 chars> | ✅ |
| `terminate_autocontrol_returns_manual` | explicit-hot-start in AutocontrolNormal checks caregiver termination of algorithmic control returns to Manual and restor...<truncated 24 chars> | ✅ |
| `forced_back_manual_events_from_distinct_modes` | explicit-hot-start probes wildcard backManual recovery from several concrete leaves, each requiring Manual as the shared...<truncated 17 chars> | ✅ |
| `forced_cp_back_manual_from_pump_fault` | explicit-hot-start in PumpFault checks CP_backManual also forces Manual as the shared recovery target. | ✅ |
| `forced_cc_back_manual_from_autocontrol_init` | explicit-hot-start in AutocontrolInit checks CC_backManual overrides autocontrol initialization and forces Manual recove...<truncated 3 chars> | ✅ |
| `setpoint_effect_used_by_autocontrol_flow` | explicit-hot-start in Ask_StartAC strengthens the SetpointChanged effect probe by requiring the changed target setpoint ...<truncated 52 chars> | ✅ |
| `fault_removal_effect_clears_fault_and_alarm_values` | explicit-hot-start in PumpFault isolates the CaregiverRemovesFault transition effect so missing or wrong constant assign...<truncated 44 chars> | ✅ |
| `start_ac_effect_sets_autocontrol_flags_from_dirty_values` | explicit-hot-start in Ask_StartAC uses dirty Manual-like flag values so StartAC must produce autocontrol ownership value...<truncated 33 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4264, 'completion_chars': 18751, 'completion_tokens': 5806, 'elapsed_seconds': 107.3992232879973, 'estimated_completion_tokens': 4688, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11345, 'first_chunk_seconds': 30.585581863997504, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12256}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2777, 'completion_chars': 11243, 'completion_tokens': 4332, 'elapsed_seconds': 79.70446880901, 'estimated_completion_tokens': 2811, 'estimated_prompt_tokens': 15612, 'estimated_total_tokens': 18423, 'first_chunk_seconds': 31.698067143006483, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 62446, 'prompt_tokens': 15182, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 19514}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2413, 'completion_chars': 9719, 'completion_tokens': 2772, 'elapsed_seconds': 53.86932339100167, 'estimated_completion_tokens': 2430, 'estimated_prompt_tokens': 18609, 'estimated_total_tokens': 21039, 'first_chunk_seconds': 11.638113139022607, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 74434, 'prompt_tokens': 18106, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20878}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3865, 'completion_chars': 15666, 'completion_tokens': 4384, 'elapsed_seconds': 82.14176354301162, 'estimated_completion_tokens': 3917, 'estimated_prompt_tokens': 19335, 'estimated_total_tokens': 23252, 'first_chunk_seconds': 14.96689268501359, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 77337, 'prompt_tokens': 18819, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23203}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1843, 'completion_chars': 8688, 'completion_tokens': 2880, 'elapsed_seconds': 53.949247070006095, 'estimated_completion_tokens': 2172, 'estimated_prompt_tokens': 20881, 'estimated_total_tokens': 23053, 'first_chunk_seconds': 21.561357510014204, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 83522, 'prompt_tokens': 20652, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23532}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success_but_weak_oracle_ineligible`。
- required stages executed：`16/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`3`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78/report.md` §7。

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

state ElevatorController {
    ! * -> F1 :: reset;

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

    F1 -> MU2 :: PS2;
    F1 -> MU3 :: PS3;
    F2 -> MU3 :: PS3;
    F2 -> MD1 :: PS1;
    F3 -> MD1 :: PS1;
    F3 -> MD2 :: PS2;
    MU2 -> F2 :: S2;
    MU3 -> F3 :: S3;
    MD1 -> F1 :: S1;
    MD2 -> F2 :: S2;
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
| token / elapsed | `{'prompt_tokens': 26136, 'completion_tokens': 8194, 'total_tokens': 34330, 'estimated_prompt_tokens': 25354, 'estimated_completion_tokens': 4800, 'estimated_total_tokens': 30154, 'prompt_chars': 101410, 'completion_chars': 19194, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `157.795s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f/pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f/checks.json`, `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:d6b850cdf8cfcf9209ca455559a616c7d60a15c0f28bb81b5e83028daabc604d` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9895 | 生成初始 DSL 与 grounding seeds | initial len=660 | [`record`](./pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13944 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10491 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T09:37:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T09:37:30Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T09:37:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T09:37:30Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T09:38:34Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T09:38:34Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=660,hash=sha256:4bf71ee94cd3 |
| 7 | `2026-06-05T09:38:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T09:38:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T09:38:34Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:4bf71ee94cd38f8a34bef6be4e1427ccf4b322e00593bd3794b47d1121df39be |
| 10 | `2026-06-05T09:38:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T09:38:34Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=660,hash=sha256:4bf71ee94cd3, current_hash=sha256:4bf71ee94cd38f8a34bef6be4e1427ccf4b322e00593bd3794b47d1121df39be |
| 12 | `2026-06-05T09:38:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T09:38:34Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T09:38:35Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T09:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T09:38:35Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T09:38:35Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T09:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T09:38:35Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T09:38:35Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T09:38:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T09:38:35Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T09:39:32Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T09:39:32Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T09:39:32Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T09:39:32Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T09:39:32Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T09:39:32Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T09:39:32Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T09:39:32Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T09:39:32Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T09:39:32Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T09:40:07Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T09:40:07Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T09:40:07Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T09:40:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T09:40:07Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T09:40:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T09:40:07Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=660,hash=sha256:4bf71ee94cd3 |
| 40 | `2026-06-05T09:40:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T09:40:07Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=660,hash=sha256:4bf71ee94cd3 |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_then_up_to_f3_via_f2` | default-init verifies initial F1 stop, F1 request to F2 drives up, arrival stops at F2, then next request to F3 drives u...<truncated 18 chars> | ✅ |
| `default_init_direct_to_f3_then_down_to_f2` | default-init dispatches before the first request; F1 request to F3 enters MU3, arrival stops at F3, then PS2 selects MD2...<truncated 12 chars> | ✅ |
| `hot_start_f2_down_to_f1` | explicit-hot-start at F2 probes PS1 selecting downward MD1 and S1 arrival stopping at F1. | ✅ |
| `hot_start_f3_down_to_f1` | explicit-hot-start at F3 probes PS1 selecting MD1 downward travel and S1 arrival stopping at floor 1. | ✅ |
| `reset_from_up_motion_forces_f1` | explicit-hot-start in upward motion MU2 verifies reset forces floor 1 and stop output regardless of outstanding request ...<truncated 8 chars> | ✅ |
| `reset_from_down_motion_forces_f1` | explicit-hot-start in downward motion MD2 verifies reset forces floor 1 and stop output regardless of outstanding reques...<truncated 10 chars> | ✅ |
| `reset_from_floor_context_forces_f1` | explicit-hot-start at floor F3 verifies reset also forces floor 1 from a stopped floor context. | ✅ |
| `no_cross_scope_request_or_sensor_from_f1` | default-init reaches F1, then events belonging to other contexts should not cause phantom motion from F1. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3062, 'completion_chars': 10189, 'completion_tokens': 3457, 'elapsed_seconds': 64.82635537799797, 'estimated_completion_tokens': 2548, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 9071, 'first_chunk_seconds': 9.648074649012415, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9895}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1424, 'completion_chars': 5160, 'completion_tokens': 2932, 'elapsed_seconds': 56.72006034600781, 'estimated_completion_tokens': 1290, 'estimated_prompt_tokens': 10695, 'estimated_total_tokens': 11985, 'first_chunk_seconds': 31.053588470997056, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 42780, 'prompt_tokens': 11012, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13944}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 985, 'completion_chars': 3845, 'completion_tokens': 1805, 'elapsed_seconds': 35.13341766700614, 'estimated_completion_tokens': 962, 'estimated_prompt_tokens': 8136, 'estimated_total_tokens': 9098, 'first_chunk_seconds': 17.794243392010685, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 32541, 'prompt_tokens': 8686, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10491}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-stale-waiver-2a93a82c-9860650f/report.md` §7。

</details>

<details><summary>path2 / path2_lng_ems / default / not_converged</summary>

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
def float SoC_low = 0.2;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float battery_Pmax = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cutin_LNG = 0;
def int cutout_LNG = 0;
def int cutin_eng3 = 0;
def int cutout_eng3 = 0;
def int cutin_DG1 = 0;
def int cutout_DG1 = 0;
def int cutin_DG2 = 0;
def int cutout_DG2 = 0;
def int load_cutin = 1;
def int load_cutout = 0;
def int illegal_overload = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> ResCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> ResCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> ResBatteryOnly : if [PL > 0 && Ppv + Pw < PL && SoC >= SoC_low && PL - Ppv - Pw <= battery_Pmax];
    ! * -> LngCovers : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > battery_Pmax && SoC >= SoC_low && PL - Ppv - Pw <= Pgmax];
    ! * -> LngLowSocChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < SoC_low && PL - Ppv - Pw + Pgmax / 5 <= Pgmax];
    ! * -> LngEng3Covers : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> Diesel1LowSocMargin : if [PL > 0 && Ppv + Pw < PL && SoC < SoC_low && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> Diesel1Covers : if [PL > 0 && Ppv + Pw < PL && SoC >= SoC_low && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> Diesel2Covers : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> ExtremeOverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max && SoC >= SoC_low && PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max <= battery_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = Ppv + Pw;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_eng3 = 0;
            cutout_eng3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutin = 1;
            load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state ZeroLoadSpare {
        during {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = Ppv + Pw;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_eng3 = 0;
            cutout_eng3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutin = 1;
            load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state ResCoversCharge {
        during {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = Ppv + Pw - PL;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_eng3 = 0;
            cutout_eng3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutin = 1;
            load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state ResCoversSpare {
        during {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = Ppv + Pw - PL;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_eng3 = 0;
            cutout_eng3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutin = 1;
            load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state ResBatteryOnly {
        during {
            Pgen_req = 0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0;
            Pspare = 0;
            cutin_LNG = 0;
            cutout_LNG = 1;
            cutin_eng3 = 0;
            cutout_eng3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutin = 1;
            load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LngCovers {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_eng3 = 0;
            cutout_eng3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutin = 1;
            load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LngLowSocChargeMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0;
            Pbatt_charge = Pgmax / 5;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_eng3 = 0;
            cutout_eng3 = 1;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutin = 1;
            load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LngEng3Covers {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_eng3 = 1;
            cutout_eng3 = 0;
            cutin_DG1 = 0;
            cutout_DG1 = 1;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutin = 1;
            load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state Diesel1LowSocMargin {
        during {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_eng3 = 1;
            cutout_eng3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutin = 1;
            load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state Diesel1Covers {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_eng3 = 1;
            cutout_eng3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 0;
            cutout_DG2 = 1;
            load_cutin = 1;
            load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state Diesel2Covers {
        during {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_eng3 = 1;
            cutout_eng3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            load_cutin = 1;
            load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state ExtremeOverloadBatteryLack {
        during {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            Pbatt_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            Pbatt_charge = 0;
            Pspare = 0;
            cutin_LNG = 1;
            cutout_LNG = 0;
            cutin_eng3 = 1;
            cutout_eng3 = 0;
            cutin_DG1 = 1;
            cutout_DG1 = 0;
            cutin_DG2 = 1;
            cutout_DG2 = 0;
            load_cutin = 0;
            load_cutout = 1;
            illegal_overload = 1;
        }
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `budget_exhausted` |
| failure class | `scenario_or_sim_oracle` |
| main_result_eligible | `false` |
| path2_ref_model_blueprint | `false`；run_not_main_result_eligible |
| state_mode_decorative | `true` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `5` / `1` / `15` |
| token / elapsed | `{'prompt_tokens': 556045, 'completion_tokens': 50341, 'total_tokens': 606386, 'estimated_prompt_tokens': 542856, 'estimated_completion_tokens': 35238, 'estimated_total_tokens': 578094, 'prompt_chars': 2171399, 'completion_chars': 140940, 'n_calls': 13, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `964.674s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34/pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34/checks.json`, `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:87d591841ce36a753ff4d76a6ec3e68bb8ebdce4253ac5cac3e5c65dd97820f5` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `87` |
| `langgraph_node_trace_hash` | `sha256:03fd7c0a14c2e4319e72bde2d52b83ca871aa179a9bbbc2b171620335dce41d7` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `87` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14892 | 生成初始 DSL 与 grounding seeds | initial len=7697 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=335, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=139205 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=139205 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=139205 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=67811 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=347884 | LLM per-request accept/reject + repair | candidate len=8224,0,0,0,0 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=1, tokens=36594 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=335, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=139205 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=139205 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=347884 | LLM per-request accept/reject + repair | candidate len=8224,0,0,0,0 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=335, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=347884 | LLM per-request accept/reject + repair | candidate len=8224,0,0,0,0 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=335, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=347884 | LLM per-request accept/reject + repair | candidate len=8224,0,0,0,0 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=335, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0, advisory=350, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=347884 | LLM per-request accept/reject + repair | candidate len=8224,0,0,0,0 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SD-6 sim failure: 17/18 scenarios passed | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T09:37:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T09:37:30Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T09:37:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T09:37:30Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T09:40:04Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T09:40:04Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=7697,hash=sha256:afe3fdcbd8ab |
| 7 | `2026-06-05T09:40:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T09:40:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T09:40:04Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:afe3fdcbd8ab3e10728c5e185649591c0dbfd51324726dd5aa37e21815531419 |
| 10 | `2026-06-05T09:40:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T09:40:04Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=7697,hash=sha256:afe3fdcbd8ab, current_hash=sha256:afe3fdcbd8ab3e10728c5e185649591c0dbfd51324726dd5aa37e21815531419 |
| 12 | `2026-06-05T09:40:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T09:40:04Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14
... <truncated 8928 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|---|
| `default_init_zero_load_charge` | default-init verifies the initial leaf and PL=0 with SoC below 0.95 sends renewable production to battery charging. | ✅ | ✅ | ✅ | ✅ | ✅ |
| `zero_load_soc_full_spare` | explicit-hot-start verifies the SoC=0.95 boundary for PL=0 routes renewable production to spare power rather than chargi...<truncated 3 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `res_covers_charge_below_full_soc` | explicit-hot-start verifies RES covers positive load and SoC below 0.95 charges the battery with residual renewable powe...<truncated 2 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `res_covers_spare_at_full_soc` | explicit-hot-start verifies RES covers positive load and SoC at the 0.95 boundary makes residual renewable power spare. | ✅ | ✅ | ✅ | ✅ | ✅ |
| `battery_only_at_battery_capacity_boundary` | explicit-hot-start verifies the battery-priority branch at the exact battery_Pmax deficit boundary with no thermal cut-i...<truncated 2 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `lng_covers_at_lng_capacity_boundary` | explicit-hot-start verifies LNG is selected before diesel when the remaining deficit exceeds battery capacity but equals...<truncated 7 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `lng_low_soc_charge_margin_boundary` | explicit-hot-start verifies the low-SoC LNG branch adds the Pgmax/5 charging margin at its exact capacity boundary. | ✅ | ✅ | ✅ | ✅ | ✅ |
| `lng_eng3_covers_at_eng3_boundary` | explicit-hot-start verifies the eng3 capacity branch when LNG alone is insufficient and deficit equals Pgmax plus eng3_P...<truncated 4 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `diesel1_low_soc_margin_boundary` | explicit-hot-start verifies the later low-SoC diesel-generator branch adds the Pd1max/10 charging margin at its boundary...<truncated 1 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `diesel1_covers_at_dg1_boundary` | explicit-hot-start verifies DG1 is used as a last-priority unit when suitable-SoC deficit equals LNG plus eng3 plus DG1 ...<truncated 9 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `diesel2_covers_at_dg2_boundary` | explicit-hot-start verifies DG2 is the final diesel priority when deficit exceeds DG1 capacity and equals all thermal ca...<truncated 7 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `extreme_overload_all_thermal_and_battery_lack` | explicit-hot-start verifies extreme demand above all thermal capacity activates all thermal units and covers the remaini...<truncated 29 chars> | ✅ | ❌ | ❌ | ❌ | ❌ |
| `forced_reclassification_extreme_to_res_spare` | explicit-hot-start probes the wildcard forced guard reclassification from a concrete extreme-overload leaf to RES-covere...<truncated 60 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_zero_to_diesel2` | explicit-hot-start probes the wildcard forced guard reclassification from a concrete zero-load leaf to final-priority DG...<truncated 56 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `default_init_then_forced_reclassification_to_lng` | default-init first dispatches to the initial leaf, then a second cycle must use the wildcard forced guard to reclassify ...<truncated 44 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_lng_to_battery_only` | explicit-hot-start targets missing wildcard forced reclassification by starting in LNG dispatch while inputs require the...<truncated 30 chars> | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_diesel1_to_zero_spare` | explicit-hot-start targets missing wildcard forced reclassification by starting in a DG1 leaf while inputs require zero-...<truncated 29 chars> | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_diesel2_to_zero_charge` | explicit-hot-start adds a missing-forced-transition probe for the ZeroLoadCharge wildcard guard by starting in a DG2 lea...<truncated 55 chars> | ⚪ | ✅ | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=minor, local_stage=SD-10, reason=scenario_regression | `sha256:de86ec6b9a8125f180b8323f1dcd7686ebbe92d4844c809c2cdb05709884b152` |
| 2 | `1` | ❌ | `SD-6` | extreme_overload_all_thermal_and_battery_lack | accept=0, reject=1, waiver=0 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `2` | ❌ | `SD-6` | extreme_overload_all_thermal_and_battery_lack | accept=0, reject=1, waiver=0 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 4 | `3` | ❌ | `SD-6` | extreme_overload_all_thermal_and_battery_lack | accept=0, reject=1, waiver=0 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 5 | `4` | ❌ | `SD-6` | extreme_overload_all_thermal_and_battery_lack | accept=0, reject=1, waiver=0 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_stale_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-stale-waiver-2a93a82c-a8b5fa34/report.md` §7。

</details>
