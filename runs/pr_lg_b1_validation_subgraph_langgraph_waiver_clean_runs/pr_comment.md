## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 37178 | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711/report.md` |
| path1 | `path1_cara` | `default` | `not_converged` | `budget_exhausted` | ✅ | ❌ | ⚪ | `scenario_or_sim_oracle` | ~1812054 est (usage unavailable; chars=7023391/224755) | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 44462 | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | ❌ | `success` | 113764 | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17/report.md` |

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
- node trace count 范围：min=16，max=78；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：3/4 success，rejected=0，budget_exhausted=1，total_tokens=195404。
- 主结果候选：当前 3/4 个非 infrastructure run 可进入 main_result_eligible；provider/network invalid=0 个，只能作为 infrastructure evidence。

### 主结果候选 vs Path2 ref-model 蓝本边界

- Path2 run-validity：1/1 个 Path2 run 的 `main_result_eligible=true`；这只表示 run/schema/secret/trace/final verdict 可进入主结果候选。
- Path2 blueprint-validity：0/1 个 Path2 run 当前可作为 `path2_ref_model_blueprint_eligible=true`；该字段比 `main_result_eligible` 更严格。
- `path2_lng_ems`：main_result_eligible=`true`，path2_ref_model_blueprint_eligible=`false`，state_mode_decorative=`true`；reason=state_mode_decorative: final DSL is dominated by root-level forced guard reclassification; valid as FE/BVS or dispatch-classifier stress evidence, but not a Path2 ref-model blueprint
- 解释：`path2_ref_model_blueprint_eligible=false` 不会把有效 run 改成 provider invalid；它只禁止把 state-mode-decorative / 条件分类式模型宣传为 Path2 ref-model 主蓝本。

### 主要失败模式

- `success`：3 run(s)。
- `scenario_or_sim_oracle`：1 run(s)。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=scenario_or_sim_oracle，最大 observed iteration_count=5。
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
| token / elapsed | `{'prompt_tokens': 30181, 'completion_tokens': 6997, 'total_tokens': 37178, 'estimated_prompt_tokens': 29111, 'estimated_completion_tokens': 4493, 'estimated_total_tokens': 33604, 'prompt_chars': 116442, 'completion_chars': 17972, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `135.152s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711/pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711/checks.json`, `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:00aa5dd4b9a81cffad350a596d90b55b0506b57edb3a52bbb90b2d47698d63f0` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9208 | 生成初始 DSL 与 grounding seeds | initial len=626 | [`record`](./pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=17, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13310 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=14660 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T10:34:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T10:34:52Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T10:34:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T10:34:52Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T10:35:46Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T10:35:46Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=626,hash=sha256:6f8c43c7583c |
| 7 | `2026-06-05T10:35:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T10:35:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T10:35:46Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:6f8c43c7583c52ce2c2665db62939451bff6e1b64f01ca9858e83f5501e80dac |
| 10 | `2026-06-05T10:35:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T10:35:46Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=626,hash=sha256:6f8c43c7583c, current_hash=sha256:6f8c43c7583c52ce2c2665db62939451bff6e1b64f01ca9858e83f5501e80dac |
| 12 | `2026-06-05T10:35:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T10:35:46Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T10:35:46Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T10:35:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T10:35:46Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T10:35:46Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T10:35:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T10:35:46Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T10:35:46Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T10:35:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T10:35:46Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T10:36:33Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T10:36:33Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T10:36:33Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T10:36:33Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T10:36:33Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T10:36:33Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T10:36:33Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T10:36:33Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T10:36:33Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T10:36:33Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T10:37:06Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T10:37:06Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T10:37:06Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T10:37:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T10:37:06Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T10:37:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T10:37:06Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=626,hash=sha256:6f8c43c7583c |
| 40 | `2026-06-05T10:37:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T10:37:06Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=626,hash=sha256:6f8c43c7583c |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_increase_then_boundary_hold` | default-init with slp at the increase->hold boundary: first dispatches to increase outputs, then slp <= 0.01 transitions...<truncated 25 chars> | ✅ |
| `increase_no_fire_above_hold_threshold` | explicit-hot-start in increase with slp just above 0.01 should not take increase->hold and should keep increase valve ou...<truncated 6 chars> | ✅ |
| `hold_no_fire_at_positive_boundary` | explicit-hot-start in hold with slp exactly 0.01 should not satisfy hold->increase because that guard is slp > 0.01. | ✅ |
| `hold_to_increase_above_positive_boundary` | explicit-hot-start in hold with slp just above 0.01 should transition to increase and command inlet-valve increase outpu...<truncated 3 chars> | ✅ |
| `hold_no_fire_at_negative_boundary` | explicit-hot-start in hold with slp exactly -0.01 should not satisfy hold->decrease because that guard is slp < -0.01. | ✅ |
| `hold_to_decrease_below_negative_boundary` | explicit-hot-start in hold with slp just below -0.01 should transition to decrease and command pressure-release outputs. | ✅ |
| `decrease_to_hold_at_negative_boundary` | explicit-hot-start in decrease with slp exactly -0.01 should satisfy decrease->hold because that guard is slp >= -0.01. | ✅ |
| `decrease_no_fire_below_negative_boundary` | explicit-hot-start in decrease with slp just below -0.01 should not take decrease->hold and should keep pressure-release...<truncated 9 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2071, 'completion_chars': 6920, 'completion_tokens': 2815, 'elapsed_seconds': 53.70481988301617, 'estimated_completion_tokens': 1730, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 8223, 'first_chunk_seconds': 16.422663688019384, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9208}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1400, 'completion_chars': 5324, 'completion_tokens': 2437, 'elapsed_seconds': 46.68991239898605, 'estimated_completion_tokens': 1331, 'estimated_prompt_tokens': 10629, 'estimated_total_tokens': 11960, 'first_chunk_seconds': 21.235833354992792, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 42515, 'prompt_tokens': 10873, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13310}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1273, 'completion_chars': 5728, 'completion_tokens': 1745, 'elapsed_seconds': 33.63557193800807, 'estimated_completion_tokens': 1432, 'estimated_prompt_tokens': 11989, 'estimated_total_tokens': 13421, 'first_chunk_seconds': 11.000066420005169, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 47955, 'prompt_tokens': 12915, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14660}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_abs-default-lg-b1-waiver-4304eb65-f572f711/report.md` §7。

</details>

<details><summary>path1 / path1_cara / default / not_converged</summary>

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
def int target_bp = 100;
def int requested_target_bp = 100;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int infusion_rate = 0;
def int pump_speed = 0;
def int switch_speed = 0;
def int default_flow_rate = 0;
def int control_voltage = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_fault = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Manual -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolNormal -> Manual : CA_backManual;
        ! Manual -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolNormal -> Manual : CB_backManual;
        ! Manual -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolNormal -> Manual : CP_backManual;
        ! Manual -> Manual : CC_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! AutocontrolNormal -> Manual : CC_backManual;
        ! Manual -> Manual : TerminateAC;
        ! Ask_StartAC -> Manual : TerminateAC;
        ! AutocontrolInit -> Manual : TerminateAC;
        ! AutocontrolNormal -> Manual : TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
                }
            }
            during {
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
                }
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 1;
                software_control = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 2;
                software_control = 1;
                alarm_signal = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 2;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure >= target_bp] {
                    infusion_rate = 0;
                } else {
                    infusion_rate = target_bp - blood_pressure;
                }
                control_voltage = infusion_rate;
                pump_speed = control_voltage;
                log_count = log_count + 1;
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
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual : CA_backManual;
        PumpFault -> Manual : CB_backManual;
        PumpFault -> Manual : CP_backManual;
        PumpFault -> Manual : CC_backManual;
        PumpFault -> Manual : TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `budget_exhausted` |
| failure class | `scenario_or_sim_oracle` |
| main_result_eligible | `false` |
| path2_ref_model_blueprint | `n/a`；not_applicable_to_path1 |
| state_mode_decorative | `false` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `8` / `5` / `9` |
| token / elapsed | `{'prompt_tokens': None, 'completion_tokens': None, 'total_tokens': None, 'estimated_prompt_tokens': 1755858, 'estimated_completion_tokens': 56196, 'estimated_total_tokens': 1812054, 'prompt_chars': 7023391, 'completion_chars': 224755, 'n_calls': 24, 'token_usage_available': False, 'token_usage_unavailable_calls': 1}` / `1444.281s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e/pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e/checks.json`, `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:6ecd52ebd944b26023390b892f680e22984f2a1905a99d8b254cc816e7ae86d8` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `78` |
| `langgraph_node_trace_hash` | `sha256:ef1dec353dd339195e8e39c649eb6c9d9b0f831a64f270ce9066c8169a76bbb3` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `78` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=13835 | 生成初始 DSL 与 grounding seeds | initial len=2826 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=141279 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=2, tokens=50271 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=141279 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=141279 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=141279 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=2, tokens=50271 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=141279 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5 | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `
... <truncated 10677 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|---|
| `default_init_manual_sets_manual_outputs` | default-init verifies the Mode_Control_Algorithm initial leaf is Manual and manual operation uses switch speed/default f...<truncated 23 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `initiate_change_setpoint_start_autocontrol` | explicit-hot-start from Manual probes InitiateAC to Ask_StartAC, setpoint change there, StartAC to AutocontrolInit, then...<truncated 30 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `normal_autocontrol_low_pressure_positive_flow` | explicit-hot-start in AutocontrolNormal verifies BP below target produces a positive infusion rate, matching control vol...<truncated 28 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `normal_autocontrol_high_pressure_zero_flow` | explicit-hot-start in AutocontrolNormal verifies higher/equal BP produces lower flow, here zero rate and zero pump comma...<truncated 18 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_boundary_no_fire_at_zero` | explicit-hot-start in AutocontrolNormal probes pump_fault boundary: with no complication indicated, normal autocontrol m...<truncated 18 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_boundary_fire_and_fault_removed` | explicit-hot-start in AutocontrolNormal probes pump_fault boundary: a complication enters PumpFault, alarms/releases sof...<truncated 48 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_back_manual_from_ask_init_and_normal` | explicit-hot-start from Ask_StartAC probes CB_backManual, CP_backManual, CA_backManual, and CC_backManual as shared Manu...<truncated 42 chars> | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `forced_back_manual_from_pump_fault_preserves_active_alarm` | explicit-hot-start in PumpFault probes that shared backManual/TerminateAC recover to Manual while an unresolved pump fau...<truncated 41 chars> | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `forced_back_manual_from_ask_and_init` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_ca_terminate_cc_back_manual_from_normal` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `isolated_wrong_target_mode_path_probes` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `forced_self_back_manual_from_manual_resets_outputs` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `isolated_wrong_target_fault_path_probes` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `forced_back_manual_from_pump_fault_leaf` |  | ⚪ | ❌ | ✅ | ❌ | ❌ |
| `forced_missing_line_matrix_from_manual` |  | ⚪ | ⚪ | ✅ | ✅ | ✅ |
| `forced_missing_line_matrix_from_ask` |  | ⚪ | ⚪ | ✅ | ✅ | ✅ |
| `forced_missing_line_matrix_from_init` |  | ⚪ | ⚪ | ✅ | ✅ | ✅ |
| `forced_and_fault_event_targets_from_pump_fault` |  | ⚪ | ⚪ | ✅ | ❌ | ❌ |
| `forced_missing_line_matrix_from_normal` |  | ⚪ | ⚪ | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Repair the fallback event representation so CARA.Mode_Control_Algorithm.CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC are again resolvable as pare...<truncated 758 chars> | `sha256:d13b720f647947765800eba3d078515a5fb42b1edd862d5496a2307469102258` |
| 2 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | `sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39` |
| 3 | `1` | ❌ | `SD-6` | forced_back_manual_from_pump_fault_leaf | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Keep the five parent-level PumpFault fallback/termination transitions so `CARA.Mode_Control_Algorithm.CA_backManual`, `CB_backManual`, `CP_backManual`, `CC_backManual`, and `Te...<truncated 477 chars> | `sha256:7210b3208097b368871ee1fd999eab559dfebd3caa802ea2c295d30441e0acf9` |
| 4 | `1` | ✅ | `SD-6` | forced_back_manual_from_pump_fault_leaf | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:0c453825a7e1638f62cf9c8f073d1dc0eaf11a6fcdec70b61dd74c72ce74073d` |
| 5 | `2` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c` |
| 6 | `3` | ❌ | `SD-6` | forced_back_manual_from_pump_fault_leaf, forced_and_fault_event_targets_from_pump_fault | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Return a raw parseable pyfcstm DSL model only. Do not wrap it in JSON, do not include a `decisions` array, and do not put the DSL inside a quoted `candidate_dsl` string. The fi...<truncated 550 chars> | `sha256:4b7ddbbc35781ef3abb32c1b383b0c3781a16fd087b76b085b8a58b22fa99b7b` |
| 7 | `3` | ✅ | `SD-6` | forced_back_manual_from_pump_fault_leaf, forced_and_fault_event_targets_from_pump_fault | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c` |
| 8 | `4` | ✅ | `SD-6` | forced_back_manual_from_pump_fault_leaf, forced_and_fault_event_targets_from_pump_fault | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e/report.md` §7。

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
def int PS1 = 0;
def int PS2 = 0;
def int PS3 = 0;
def int S1 = 0;
def int S2 = 0;
def int S3 = 0;
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

    F1 -> MU2 : if [PS2 > 0];
    F1 -> MU3 : if [PS3 > 0];
    F2 -> MU3 : if [PS3 > 0];
    F2 -> MD1 : if [PS1 > 0];
    F3 -> MD1 : if [PS1 > 0];
    F3 -> MD2 : if [PS2 > 0];
    MU2 -> F2 : if [S2 > 0];
    MU3 -> F3 : if [S3 > 0];
    MD1 -> F1 : if [S1 > 0];
    MD2 -> F2 : if [S2 > 0];
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
| token / elapsed | `{'prompt_tokens': 35863, 'completion_tokens': 8599, 'total_tokens': 44462, 'estimated_prompt_tokens': 34683, 'estimated_completion_tokens': 5222, 'estimated_total_tokens': 39905, 'prompt_chars': 138726, 'completion_chars': 20885, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `162.721s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e/pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e/checks.json`, `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:a036a1b5b5e4da312fa2c7c44e4aea7fef499fe47580db6024080611f8ba1519` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9441 | 生成初始 DSL 与 grounding seeds | initial len=848 | [`record`](./pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=17, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=16821 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=18200 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T10:34:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T10:34:52Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T10:34:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T10:34:52Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T10:35:48Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T10:35:48Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=848,hash=sha256:0b46749143c4 |
| 7 | `2026-06-05T10:35:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T10:35:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T10:35:48Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:0b46749143c436868602d4fa34ce580a18bb4fac9ab9d72ea13e1074548b8b00 |
| 10 | `2026-06-05T10:35:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T10:35:48Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=848,hash=sha256:0b46749143c4, current_hash=sha256:0b46749143c436868602d4fa34ce580a18bb4fac9ab9d72ea13e1074548b8b00 |
| 12 | `2026-06-05T10:35:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T10:35:48Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T10:35:48Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T10:35:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T10:35:48Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T10:35:48Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T10:35:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T10:35:48Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T10:35:48Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T10:35:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T10:35:48Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T10:37:03Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T10:37:03Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T10:37:03Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T10:37:03Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T10:37:03Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T10:37:03Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T10:37:03Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T10:37:03Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T10:37:03Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T10:37:03Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T10:37:34Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T10:37:34Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T10:37:34Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T10:37:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T10:37:34Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T10:37:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T10:37:34Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=848,hash=sha256:0b46749143c4 |
| 40 | `2026-06-05T10:37:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T10:37:34Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=848,hash=sha256:0b46749143c4 |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_initial_floor1_idle_no_request` | default-init: verifies initial dispatch lands on F1 with stop output, and with no requests the controller remains stoppe...<truncated 8 chars> | ✅ |
| `f1_request_f2_arrive_then_request_f1` | explicit-hot-start: PS2 from F1 drives upward to MU2, S2 stops at F2, then outstanding PS1 immediately drives downward t...<truncated 27 chars> | ✅ |
| `f1_request_f3_arrival` | explicit-hot-start: PS3 from F1 must target MU3 for upward travel to floor 3, and S3 arrival must stop at F3. | ✅ |
| `f2_request_f3_arrival` | explicit-hot-start: PS3 from F2 must select upward MU3, and S3 arrival must complete at F3 with stop output. | ✅ |
| `f3_request_f1_arrival` | explicit-hot-start: PS1 from F3 must select downward MD1, and S1 arrival must complete at F1 with stop output. | ✅ |
| `f3_request_f2_arrival` | explicit-hot-start: PS2 from F3 must select downward MD2, and S2 arrival must complete at F2 with stop output. | ✅ |
| `motion_without_arrival_sensor_does_not_stop` | explicit-hot-start: while in upward MU3, absence of S3 must not falsely complete arrival, and upward drive output remain...<truncated 11 chars> | ✅ |
| `reset_from_up_motion_forces_floor1` | explicit-hot-start: Reset from an upward motion context must force the controller to F1 and stop the drive. | ✅ |
| `reset_from_floor3_forces_floor1` | explicit-hot-start: Reset from a floor context other than F1 must force the controller back to F1 with stop output. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2484, 'completion_chars': 8815, 'completion_tokens': 3003, 'elapsed_seconds': 56.08678445301484, 'estimated_completion_tokens': 2204, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 8727, 'first_chunk_seconds': 11.289915090019349, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9441}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1905, 'completion_chars': 7366, 'completion_tokens': 3978, 'elapsed_seconds': 74.45593264198396, 'estimated_completion_tokens': 1842, 'estimated_prompt_tokens': 12560, 'estimated_total_tokens': 14402, 'first_chunk_seconds': 40.10194762298488, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 50238, 'prompt_tokens': 12843, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 16821}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1099, 'completion_chars': 4704, 'completion_tokens': 1618, 'elapsed_seconds': 31.061012068996206, 'estimated_completion_tokens': 1176, 'estimated_prompt_tokens': 15600, 'estimated_total_tokens': 16776, 'first_chunk_seconds': 11.45724493698799, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 62399, 'prompt_tokens': 16582, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 18200}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path1_elevator-default-lg-b1-waiver-4304eb65-09cede1e/report.md` §7。

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
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbat_Pmax = 0.0;
def float Pg_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG = 0;
def int cmd_DG1 = 0;
def int cmd_DG2 = 0;
def int cmd_load_cutin = 0;
def int cmd_load_cutout = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
    ! * -> LNGWithChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= eng3_Pmax];
    ! * -> LNGOnly : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw <= eng3_Pmax && (SoC < 0.2 || PL - Ppv - Pw > Pbat_Pmax) && (SoC >= 0.2 || PL - Ppv - Pw + Pgmax / 5 > eng3_Pmax)];
    ! * -> LNGBattery : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pbat_Pmax];
    ! * -> LNGDG1WithChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= eng3_Pmax + Pd1max];
    ! * -> LNGDG1 : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > eng3_Pmax + Pd1max) && (SoC < 0.2 || PL - Ppv - Pw > eng3_Pmax + Pbat_Pmax)];
    ! * -> AllThermal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax + Pd1max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadBatteryCover : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state ZeroLoadSpare {
        during {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state RESCoversCharge {
        during {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state RESCoversSpare {
        during {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state BatteryDischarge {
        during {
            Pg_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state LNGWithChargeMargin {
        during {
            Pg_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state LNGOnly {
        during {
            Pg_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state LNGBattery {
        during {
            Pg_req = eng3_Pmax;
            Pbat_discharge = PL - Ppv - Pw - eng3_Pmax;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state LNGDG1WithChargeMargin {
        during {
            Pg_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state LNGDG1 {
        during {
            Pg_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state AllThermal {
        during {
            Pg_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
        }
    }

    state OverloadBatteryCover {
        during {
            Pg_req = eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `2` |
| token / elapsed | `{'prompt_tokens': 95801, 'completion_tokens': 17963, 'total_tokens': 113764, 'estimated_prompt_tokens': 86746, 'estimated_completion_tokens': 11306, 'estimated_total_tokens': 98052, 'prompt_chars': 346978, 'completion_chars': 45221, 'n_calls': 4, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `335.857s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17/pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17/checks.json`, `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:a314e7cff8c31f79129c7ed4d04607277cccf133bb12ac7ce1cd1898aededeb7` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `18` |
| `langgraph_node_trace_hash` | `sha256:550677296248593e992beaec225ade90d235784e83d89c1794dbc8f3f908dbf5` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `18` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14139 | 生成初始 DSL 与 grounding seeds | initial len=5979 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=263, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=2, tokens=42603 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=2, tokens=42603 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=57022 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T10:34:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T10:34:52Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T10:34:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T10:34:52Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T10:37:12Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T10:37:12Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=5979,hash=sha256:1d80d7eae005 |
| 7 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T10:37:12Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:1d80d7eae005c34773c326cd018af9662fe914a8c85b7fe6f64489b305335edf |
| 10 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T10:37:12Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=5979,hash=sha256:1d80d7eae005, current_hash=sha256:1d80d7eae005c34773c326cd018af9662fe914a8c85b7fe6f64489b305335edf |
| 12 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T10:37:12Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T10:37:12Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T10:37:12Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T10:37:12Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T10:37:12Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T10:37:12Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T10:37:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T10:37:12Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T10:38:42Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T10:38:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T10:38:42Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T10:38:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T10:38:42Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T10:39:38Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T10:39:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T10:39:38Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T10:39:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T10:39:38Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 33 | `2026-06-05T10:39:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 34 | `2026-06-05T10:39:38Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 35 | `2026-06-05T10:39:38Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-05T10:39:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T10:39:38Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 38 | `2026-06-05T10:40:27Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 39 | `2026-06-05T10:40:27Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 40 | `2026-06-05T10:40:27Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 41 | `2026-06-05T10:40:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-05T10:40:27Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 43 | `2026-06-05T10:40:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-05T10:40:27Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=5979,hash=sha256:1d80d7eae005 |
| 45 | `2026-06-05T10:40:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-05T10:40:27Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=5979,hash=sha256:1d80d7eae005 |
| 47 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 48 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_zero_load_charge` | default-init: with default PL=0 and SoC below 0.95, EMS initializes/selects zero-load battery charging from available RE...<truncated 2 chars> | ✅ |
| `zero_load_soc_full_spare_boundary` | explicit-hot-start: at the SoC=0.95 boundary with PL=0, RES production should go to spare rather than battery charging. | ✅ |
| `res_covers_charge_below_full_soc` | explicit-hot-start: when renewable power exceeds load and SoC is below 0.95, all load is RES-served and residual RES cha...<truncated 17 chars> | ✅ |
| `res_covers_spare_at_full_soc_boundary` | explicit-hot-start: at SoC=0.95 with renewable power exceeding load, residual RES should be treated as spare power. | ✅ |
| `battery_discharge_at_low_soc_boundary` | explicit-hot-start: when RES is below load, SoC exactly 0.2 is suitable for battery use and deficit within battery capac...<truncated 18 chars> | ✅ |
| `low_soc_lng_charge_margin` | explicit-hot-start: with SoC below 0.2, LNG should cover the RES deficit plus the Pgmax/5 charging margin when within LN...<truncated 11 chars> | ✅ |
| `lng_only_when_battery_capacity_insufficient` | explicit-hot-start: with suitable SoC but battery capacity insufficient and LNG capacity enough, LNG alone should be cut...<truncated 18 chars> | ✅ |
| `lng_battery_when_deficit_exceeds_lng` | explicit-hot-start: with suitable SoC and deficit above LNG capacity but within LNG plus battery capacity, dispatch LNG ...<truncated 22 chars> | ✅ |
| `low_soc_lng_dg1_charge_margin` | explicit-hot-start: with low SoC and deficit above LNG, LNG plus DG1 should include the Pd1max/10 charging margin when w...<truncated 15 chars> | ✅ |
| `lng_dg1_without_battery_or_margin` | explicit-hot-start: when deficit exceeds LNG and battery contribution is not enough, but fits LNG plus DG1, DG1 is cut i...<truncated 14 chars> | ✅ |
| `all_thermal_dg2_last_priority` | explicit-hot-start: when deficit exceeds LNG plus DG1 but is within LNG plus DG1 plus DG2, all thermal units including D...<truncated 14 chars> | ✅ |
| `overload_battery_cover_extreme_demand` | explicit-hot-start: for extreme demand beyond all RES and thermal resources, all thermal units are activated and remaini...<truncated 40 chars> | ✅ |
| `forced_reselect_to_zero_load_charge_from_overload` | explicit-hot-start: from a nonzero dispatch leaf, the global forced guard for PL=0 and SoC<0.95 must reselect ZeroLoadCh...<truncated 53 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5321, 'completion_chars': 17659, 'completion_tokens': 7670, 'elapsed_seconds': 140.1158511620015, 'estimated_completion_tokens': 4415, 'estimated_prompt_tokens': 6646, 'estimated_total_tokens': 11061, 'first_chunk_seconds': 44.29359240701888, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26582, 'prompt_tokens': 6469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14139}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3304, 'completion_chars': 10919, 'completion_tokens': 4813, 'elapsed_seconds': 89.09077987799537, 'estimated_completion_tokens': 2730, 'estimated_prompt_tokens': 14774, 'estimated_total_tokens': 17504, 'first_chunk_seconds': 29.67595773699577, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 59094, 'prompt_tokens': 15709, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20522}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2552, 'completion_chars': 7732, 'completion_tokens': 2949, 'elapsed_seconds': 55.14282820900553, 'estimated_completion_tokens': 1933, 'estimated_prompt_tokens': 17668, 'estimated_total_tokens': 19601, 'first_chunk_seconds': 9.124066238000523, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 70672, 'prompt_tokens': 19132, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22081}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2012, 'completion_chars': 8911, 'completion_tokens': 2531, 'elapsed_seconds': 48.449066289991606, 'estimated_completion_tokens': 2228, 'estimated_prompt_tokens': 47658, 'estimated_total_tokens': 49886, 'first_chunk_seconds': 12.166396329994313, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 190630, 'prompt_tokens': 54491, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 57022}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`14/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`2`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_langgraph_waiver_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-waiver-4304eb65-79654f17/report.md` §7。

</details>
