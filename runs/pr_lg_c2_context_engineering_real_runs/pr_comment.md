## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_lg_c2_context_engineering_real_runs/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | post-accept | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 33805 | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8/report.md` |
| path1 | `path1_cara` | `default` | `not_converged` | `budget_exhausted` | ✅ | ❌ | ⚪ | ✅ 0/1; ❌ 1 | `design_or_variable_dynamics` | 883155 | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 34462 | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | ❌ | ⚪ 0 | `success` | 132370 | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b/report.md` |

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
- node trace count 范围：min=16，max=107；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：3/4 success，rejected=0，budget_exhausted=1，total_tokens=1083792。
  - SC-11 post-accept validation：triggered=1/4 run-level attempts，success=0，failure=1。
- 主结果候选：当前 3/4 个非 infrastructure run 可进入 main_result_eligible；provider/network invalid=0 个，只能作为 infrastructure evidence。

### 主结果候选 vs Path2 ref-model 蓝本边界

- Path2 run-validity：1/1 个 Path2 run 的 `main_result_eligible=true`；这只表示 run/schema/secret/trace/final verdict 可进入主结果候选。
- Path2 blueprint-validity：0/1 个 Path2 run 当前可作为 `path2_ref_model_blueprint_eligible=true`；该字段比 `main_result_eligible` 更严格。
- `path2_lng_ems`：main_result_eligible=`true`，path2_ref_model_blueprint_eligible=`false`，state_mode_decorative=`true`；reason=state_mode_decorative: final DSL is dominated by root-level forced guard reclassification; valid as FE/BVS or dispatch-classifier stress evidence, but not a Path2 ref-model blueprint
- 解释：`path2_ref_model_blueprint_eligible=false` 不会把有效 run 改成 provider invalid；它只禁止把 state-mode-decorative / 条件分类式模型宣传为 Path2 ref-model 主蓝本。

### 主要失败模式

- `success`：3 run(s)。
- `design_or_variable_dynamics`：1 run(s)。
- `design_or_variable_dynamics` 与变量只读不写、guard 变量永不变化等风险相关，需在样本筛选和 SL-9 prompt 中区分环境输入变量与内部状态变量。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=design_or_variable_dynamics，最大 observed iteration_count=5。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=success，最大 observed iteration_count=1。
- 实证筛选更新：若论文变量主要是外部传感/环境输入，应在样本记录中明确“只读输入”身份；若模型需要内部状态变量，则必须有 NL-grounded write/action，否则容易被 SD-4 阻断。
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
| SC-11 post-accept validation | `⚪ 0` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 26710, 'completion_tokens': 7095, 'total_tokens': 33805, 'estimated_prompt_tokens': 26161, 'estimated_completion_tokens': 4226, 'estimated_total_tokens': 30387, 'prompt_chars': 104639, 'completion_chars': 16899, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `135.45s` |
| full stage table | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8/report.md` §4 |
| run record | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8/pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz` |
| logs | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8/run_logs/stdout.txt`, `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8/checks.json`, `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:adc2c025f75c32c7c4c2121be5f192d82a55b1807b0a514054b0f7cf224593fd` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=8898 | 生成初始 DSL 与 grounding seeds | initial len=634 | [`record`](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=12984 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=11923 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T06:42:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T06:42:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T06:42:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T06:42:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T06:43:41Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T06:43:41Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 7 | `2026-06-06T06:43:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T06:43:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T06:43:41Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726 |
| 10 | `2026-06-06T06:43:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T06:43:41Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=634,hash=sha256:5a3dc31a6a97, current_hash=sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726 |
| 12 | `2026-06-06T06:43:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T06:43:41Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T06:43:41Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T06:43:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T06:43:41Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T06:43:41Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T06:43:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T06:43:41Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T06:43:41Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-06T06:43:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T06:43:41Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-06T06:44:36Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-06T06:44:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T06:44:36Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-06T06:44:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-06T06:44:36Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-06T06:44:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-06T06:44:36Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-06T06:44:36Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-06T06:44:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-06T06:44:36Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-06T06:45:08Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-06T06:45:08Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-06T06:45:08Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-06T06:45:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-06T06:45:08Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-06T06:45:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-06T06:45:08Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 40 | `2026-06-06T06:45:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-06T06:45:08Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 42 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 43 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 44 | `` | `<control>` | `-` | `lg_e3_toolnode_wrapper_trace` | {} | <none> |
| 45 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |
| 46 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 47 | `` | `<control>` | `-` | `pr_e1_quality_boundary` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_increase_then_hold_at_boundary` | default-init dispatches to increase with inlet-valve command active, then slp exactly 0.01 triggers increase-to-hold and...<truncated 20 chars> | ✅ |
| `hold_to_increase_then_increase_no_fire_above_boundary` | explicit-hot-start in hold with slp above 0.01 enters increase, and increase must not return to hold while slp remains a...<truncated 18 chars> | ✅ |
| `hold_stays_hold_at_positive_boundary` | explicit-hot-start in hold with slp exactly 0.01 must not take the strict hold-to-increase transition. | ✅ |
| `hold_to_decrease_then_decrease_no_fire_below_boundary` | explicit-hot-start in hold with slp below -0.01 enters decrease and commands pressure release, then decrease must not re...<truncated 43 chars> | ✅ |
| `hold_stays_hold_at_negative_boundary` | explicit-hot-start in hold with slp exactly -0.01 must not take the strict hold-to-decrease transition. | ✅ |
| `decrease_to_hold_at_negative_boundary` | explicit-hot-start in decrease with slp exactly -0.01 triggers decrease-to-hold and neutralizes the return valve and pum...<truncated 2 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1986, 'completion_chars': 6805, 'completion_tokens': 2505, 'elapsed_seconds': 47.949538765940815, 'estimated_completion_tokens': 1702, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 8195, 'first_chunk_seconds': 12.393631862010807, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 8898}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1381, 'completion_chars': 5174, 'completion_tokens': 2919, 'elapsed_seconds': 55.054485404863954, 'estimated_completion_tokens': 1294, 'estimated_prompt_tokens': 9930, 'estimated_total_tokens': 11224, 'first_chunk_seconds': 30.24277886096388, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39717, 'prompt_tokens': 10065, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12984}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1152, 'completion_chars': 4920, 'completion_tokens': 1671, 'elapsed_seconds': 31.388150065904483, 'estimated_completion_tokens': 1230, 'estimated_prompt_tokens': 9738, 'estimated_total_tokens': 10968, 'first_chunk_seconds': 10.624428398907185, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 38950, 'prompt_tokens': 10252, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 11923}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_abs-default-lg-c2-dotenv-7b488db8/report.md` §7。

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
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_display = 0;
def int error_sound = 0;
def int infusion_log_records = 0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_buffer_bp = 100.0;
def float patient_bp = 100.0;
def float default_flow_rate = 1.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Ask_StartAC -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! PumpFaultState -> Manual : CA_backManual;
        ! PumpFaultState -> Manual : CB_backManual;
        ! PumpFaultState -> Manual : CP_backManual;
        ! PumpFaultState -> Manual : CC_backManual;
        ! Ask_StartAC -> Manual :: CA_backManual;
        ! Ask_StartAC -> Manual :: CB_backManual;
        ! Ask_StartAC -> Manual :: CP_backManual;
        ! Ask_StartAC -> Manual :: CC_backManual;
        ! AutocontrolInit -> Manual :: CA_backManual;
        ! AutocontrolInit -> Manual :: CB_backManual;
        ! AutocontrolInit -> Manual :: CP_backManual;
        ! AutocontrolInit -> Manual :: CC_backManual;
        ! PumpFaultState -> Manual :: CA_backManual;
        ! PumpFaultState -> Manual :: CB_backManual;
        ! PumpFaultState -> Manual :: CP_backManual;
        ! PumpFaultState -> Manual :: CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_voltage = 0.0;
                if [pump_fault == 0] {
                    alarm_signal = 0;
                    error_display = 0;
                    error_sound = 0;
                } else {
                    alarm_signal = 1;
                    error_display = 1;
                    error_sound = 1;
                }
            }
            during {
                patient_bp = shared_buffer_bp;
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                patient_bp = shared_buffer_bp;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                patient_bp = shared_buffer_bp;
                if [pump_fault == 0] {
                    if [patient_bp > target_bp] {
                        infusion_rate = default_flow_rate - 1.0;
                    } else if [patient_bp < target_bp] {
                        infusion_rate = default_flow_rate + 1.0;
                    } else {
                        infusion_rate = default_flow_rate;
                    }
                    control_voltage = infusion_rate;
                    pump_speed = control_voltage;
                    infusion_log_records = infusion_log_records + 1;
                } else {
                    control_voltage = 0.0;
                    software_control = 0;
                }
            }
        }

        state PumpFaultState {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
                control_voltage = 0.0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> PumpFaultState :: PumpFault;
        PumpFaultState -> Manual :: RemoveFault effect { pump_fault = 0; };
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `budget_exhausted` |
| failure class | `design_or_variable_dynamics` |
| main_result_eligible | `false` |
| path2_ref_model_blueprint | `n/a`；not_applicable_to_path1 |
| state_mode_decorative | `false` |
| SC-11 post-accept validation | `✅ 0/1; ❌ 1` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `5` / `5` / `7` |
| token / elapsed | `{'prompt_tokens': 823330, 'completion_tokens': 59825, 'total_tokens': 883155, 'estimated_prompt_tokens': 1010729, 'estimated_completion_tokens': 46250, 'estimated_total_tokens': 1056979, 'prompt_chars': 4042892, 'completion_chars': 184971, 'n_calls': 17, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1156.796s` |
| full stage table | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9/report.md` §4 |
| run record | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9/pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz` |
| logs | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9/run_logs/stdout.txt`, `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9/checks.json`, `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:c9d98feb8828fa5819fb09d37a73af5453b4f5eeb9bf35089d977320a3639762` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `107` |
| `langgraph_node_trace_hash` | `sha256:c1668805e2d0a9b56ad9ee773ca94b2feef06b4d757cd59c57d5d514c2090338` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `107` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14048 | 生成初始 DSL 与 grounding seeds | initial len=3048 | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=12,  | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=129624 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=21429 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=358488 | LLM per-request accept/reject + repair | candidate len=3256,3884,3712,4340,4340 | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=359566 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=12,  | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=129624 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=129624 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=358488 | LLM per-request accept/reject + repair | candidate len=3256,3884,3712,4340,4340 | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=359566 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=0, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=12,  | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=358488 | LLM per-request accept/reject + repair | candidate len=3256,3884,3712,4340,4340 | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=359566 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=12,  | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=129624 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=129624 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=358488 | LLM per-request accept/reject + repair | candidate len=3256,3884,3712,4340,4340 | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=359566 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=0, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=12,  | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=358488 | LLM per-request accept/reject + repair | candidate len=3256,3884,3712,4340,4340 | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=359566 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=0, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=12,  | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SD-4 design diagnostics: W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWE | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T06:42:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T06:42:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T06:42:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T06:42:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T06:45:12Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T06:45:12Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=3048,hash=sha256:883949f7ca0b |
| 7 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T06:45:12Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:883949f7ca0bd9aedd641b53d3359d4932b07a40b67b826b6c401bfbb449e7ff |
| 10 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T06:45:12Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=3048,hash=sha256:883949f7ca0b, current_hash=sha256:883949f7ca0bd9aedd641b53d3359d4932b07a40b67b826b6c401bfbb449e7ff |
| 12 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T06:45:12Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T06:45:12Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T06:45:12Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T06:45:12Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T06:45:12Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T06:45:12Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "
... <truncated 8044 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 4 |
|---|---|---|---|---|
| `default_init_manual_mode_outputs` | default-init probe: CARA dispatches into Manual mode and manual operation uses the built-in switch speed and caregiver d...<truncated 12 chars> | ✅ | ✅ | ✅ |
| `initiate_change_setpoint_start_autocontrol_high_bp` | default-init probe: caregiver initiates AC, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit where ...<truncated 20 chars> | ✅ | ✅ | ✅ |
| `autocontrol_low_bp_then_terminate_manual` | explicit-hot-start probe: normal autocontrol with low BP raises flow, then TerminateAC returns to Manual recovery operat...<truncated 4 chars> | ✅ | ✅ | ✅ |
| `pump_fault_alarm_release_then_remove_fault` | explicit-hot-start probe: a pump fault from autocontrol enters PumpFaultState with alarms and released control, then car...<truncated 39 chars> | ✅ | ✅ | ✅ |
| `autocontrol_existing_pump_fault_releases_control` | explicit-hot-start probe: while in AutocontrolInit with a pump-operation complication already present, CARA releases sof...<truncated 42 chars> | ✅ | ✅ | ✅ |
| `ca_backmanual_forced_from_ask_startac` | explicit-hot-start probe: CA_backManual is a cross-component fallback from Ask_StartAC to Manual with CA_mode becoming M...<truncated 6 chars> | ✅ | ✅ | ✅ |
| `cb_backmanual_forced_from_autocontrol` | explicit-hot-start probe: CB_backManual is a cross-component fallback from AutocontrolInit to the shared Manual recovery...<truncated 8 chars> | ✅ | ✅ | ✅ |
| `cp_backmanual_forced_from_pump_fault` | explicit-hot-start probe: CP_backManual is a cross-component fallback from PumpFaultState to Manual, but it is not careg...<truncated 59 chars> | ✅ | ❌ | ✅ |
| `cc_backmanual_forced_from_autocontrol` | explicit-hot-start probe: CC_backManual is another cross-component fallback from active autocontrol to Manual with manua...<truncated 26 chars> | ✅ | ✅ | ✅ |
| `local_ca_backmanual_forced_line_missing_probe` | explicit-hot-start probe: CA_backManual local fallback from AutocontrolInit must force Manual; if the forced declaration...<truncated 48 chars> | ⚪ | ⚪ | ⚪ |
| `local_cb_cp_cc_backmanual_forced_lines_missing_probe` | explicit-hot-start probe: local CB_backManual, CP_backManual, and CC_backManual events must each use their forced declar...<truncated 43 chars> | ⚪ | ⚪ | ⚪ |
| `normal_transition_wrong_target_matrix` | explicit-hot-start probe: local normal events must hit their exact NL targets across Manual, Ask_StartAC, AutocontrolIni...<truncated 38 chars> | ⚪ | ⚪ | ✅ |
| `additional_forced_missing_lines_from_distinct_leaves` | explicit-hot-start probe: additional local backManual forced declarations from Ask_StartAC, AutocontrolInit, and PumpFau...<truncated 58 chars> | ⚪ | ⚪ | ⚪ |
| `qualified_forced_transition_missing_line_matrix` | explicit-hot-start probe: fully-qualified backManual forced events from multiple non-Manual leaves must all reach the ex...<truncated 65 chars> | ⚪ | ⚪ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:8a179db549bd24d3ce10980917b5585b4c678d10aaee17283990e155f5963af4` |
| 2 | `1` | ✅ | `SD-6` | cp_backmanual_forced_from_pump_fault, local_ca_backmanual_forced_line_missing_probe, local_cb_cp_cc_backmanual_forced_lines_missing_probe | accept=2, reject=1, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; scenario_regression; count_drift; forced_transition_c...<truncated 57 chars> | `sha256:e6a8d18daf59578866d1755941aed2570242002296a7deb907b5b0a19fd2b974` |
| 3 | `2` | ✅ | `SD-4` | W_SHADOWED_EVENT:9a2adf8046b5, W_SHADOWED_EVENT:c3a3d83d124f, W_SHADOWED_EVENT:f4a31c8cdc03, W_SHADOWED_EVENT:cea5fb9348b6, W_SHADOWED_EVENT:30c3e7e6cb03, ... +11 | accept=12, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; count_drift; forced_transition_count_drift; missing_required_gro...<truncated 6 chars> | `sha256:b7a0368ce4e1d2c0819a8cdbfbe0de1f7d3708ffcdcb0e3e8a92ffd94faabbdd` |
| 4 | `3` | ✅ | `SD-6` | local_ca_backmanual_forced_line_missing_probe, local_cb_cp_cc_backmanual_forced_lines_missing_probe, additional_forced_missing_lines_from_distinct_leaves | accept=3, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; count_drift; forced_transition_count_drift; missing_...<truncated 18 chars> | `sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a` |
| 5 | `4` | ✅ | `SD-4` | W_SHADOWED_EVENT:9a2adf8046b5, W_SHADOWED_EVENT:c3a3d83d124f, W_SHADOWED_EVENT:f4a31c8cdc03, W_SHADOWED_EVENT:cea5fb9348b6, W_SHADOWED_EVENT:30c3e7e6cb03, ... +11 | accept=12, reject=0, waiver=12 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=design_target_unresolved; missing_required_grounding | `sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9/report.md` §7。

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
| SC-11 post-accept validation | `⚪ 0` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 26636, 'completion_tokens': 7826, 'total_tokens': 34462, 'estimated_prompt_tokens': 26001, 'estimated_completion_tokens': 5909, 'estimated_total_tokens': 31910, 'prompt_chars': 103995, 'completion_chars': 23629, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `153.258s` |
| full stage table | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b/report.md` §4 |
| run record | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b/pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz` |
| logs | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b/run_logs/stdout.txt`, `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b/checks.json`, `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:26cdeda9b292941755315c26f2046b6a69b2366dc8e43d402e8b9524ff9f5d2d` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=10271 | 生成初始 DSL 与 grounding seeds | initial len=659 | [`record`](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13207 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10984 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T06:42:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T06:42:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T06:42:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T06:42:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T06:44:07Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T06:44:07Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=659,hash=sha256:fe4c13c35121 |
| 7 | `2026-06-06T06:44:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T06:44:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T06:44:07Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:fe4c13c35121a06dd37cf121809ebc4af1132bc518a51e0796c7a030c6b38dfc |
| 10 | `2026-06-06T06:44:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T06:44:07Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=659,hash=sha256:fe4c13c35121, current_hash=sha256:fe4c13c35121a06dd37cf121809ebc4af1132bc518a51e0796c7a030c6b38dfc |
| 12 | `2026-06-06T06:44:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T06:44:07Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T06:44:07Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T06:44:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T06:44:07Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T06:44:07Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T06:44:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T06:44:07Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T06:44:07Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-06T06:44:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T06:44:07Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-06T06:44:46Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-06T06:44:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T06:44:46Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-06T06:44:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-06T06:44:46Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-06T06:44:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-06T06:44:46Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-06T06:44:46Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-06T06:44:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-06T06:44:46Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-06T06:45:25Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-06T06:45:25Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-06T06:45:25Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-06T06:45:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-06T06:45:25Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-06T06:45:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-06T06:45:25Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=659,hash=sha256:fe4c13c35121 |
| 40 | `2026-06-06T06:45:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-06T06:45:25Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=659,hash=sha256:fe4c13c35121 |
| 42 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 43 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 44 | `` | `<control>` | `-` | `lg_e3_toolnode_wrapper_trace` | {} | <none> |
| 45 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |
| 46 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 47 | `` | `<control>` | `-` | `pr_e1_quality_boundary` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_then_up_to_f2_and_f3` | default-init probe: dispatches initial [*] to F1, then checks F1->MU2->F2 and immediate next request F2->MU3->F3 with hb...<truncated 19 chars> | ✅ |
| `f1_direct_to_f3_then_down_to_f2` | default-init probe: after initial F1 dispatch, PS3 selects MU3, S3 stops at F3, then PS2 selects downward MD2 and S2 sto...<truncated 9 chars> | ✅ |
| `f2_request_down_to_f1` | explicit-hot-start probe: from reachable floor F2, PS1 must select downward MD1 and S1 arrival must stop at F1. | ✅ |
| `f3_request_down_to_f1` | explicit-hot-start probe: from reachable floor F3, PS1 must select downward MD1 rather than MD2, and S1 arrival must sto...<truncated 8 chars> | ✅ |
| `reset_forces_f1_from_up_motion` | explicit-hot-start probe: Reset during an upward motion context must force F1 and stop hbrg regardless of outstanding re...<truncated 14 chars> | ✅ |
| `reset_forces_f1_from_down_motion` | explicit-hot-start probe: Reset during a downward motion context must force F1 and stop hbrg regardless of outstanding r...<truncated 15 chars> | ✅ |
| `reset_forces_f1_from_floor_context` | explicit-hot-start probe: Reset from a non-F1 floor context must still force the controller back to F1 with stop hbrg. | ✅ |
| `motion_states_wait_without_arrival_sensor` | explicit-hot-start no-fire probe: a motion state should not complete arrival without its required sensing input, so MU2 ...<truncated 42 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3314, 'completion_chars': 11279, 'completion_tokens': 3833, 'elapsed_seconds': 74.37413020711392, 'estimated_completion_tokens': 2820, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 9343, 'first_chunk_seconds': 14.33560342900455, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10271}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1431, 'completion_chars': 5469, 'completion_tokens': 1950, 'elapsed_seconds': 38.56681044911966, 'estimated_completion_tokens': 1368, 'estimated_prompt_tokens': 11013, 'estimated_total_tokens': 12381, 'first_chunk_seconds': 12.753812211100012, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 44049, 'prompt_tokens': 11257, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13207}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1524, 'completion_chars': 6881, 'completion_tokens': 2043, 'elapsed_seconds': 39.17143366206437, 'estimated_completion_tokens': 1721, 'estimated_prompt_tokens': 8465, 'estimated_total_tokens': 10186, 'first_chunk_seconds': 12.468146939063445, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 33857, 'prompt_tokens': 8941, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10984}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path1_elevator-default-lg-c2-dotenv-2009467b/report.md` §7。

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
def float SoC = 0.5;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbat_max = 0.0;
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG = 0;
def int cmd_DG1 = 0;
def int cmd_DG2 = 0;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> NoLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> NoLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> ResCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> ResCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > Ppv + Pw && SoC > 0.2 && PL - Ppv - Pw <= Pbat_max];
    ! * -> LNGOnly : if [PL > Ppv + Pw && SoC >= 0.2 && PL - Ppv - Pw > Pbat_max && PL - Ppv - Pw <= eng3_Pmax];
    ! * -> LNGChargeMargin : if [PL > Ppv + Pw && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= eng3_Pmax];
    ! * -> LNG_DG1 : if [PL > Ppv + Pw && SoC >= 0.2 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pd1max];
    ! * -> LNG_DG1_ChargeMargin : if [PL > Ppv + Pw && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= eng3_Pmax + Pd1max];
    ! * -> LNG_DG1_DG2 : if [PL > Ppv + Pw && PL - Ppv - Pw > eng3_Pmax + Pd1max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max];
    ! * -> AllThermalBatteryDischarge : if [PL > Ppv + Pw && PL - Ppv - Pw > eng3_Pmax + Pd1max + Pd2max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max + Pbat_max && SoC > 0.05];
    ! * -> IllegalOverloadCompletion : if [PL > Ppv + Pw && PL - Ppv - Pw > eng3_Pmax + Pd1max + Pd2max + Pbat_max || PL > Ppv + Pw && PL - Ppv - Pw > eng3_Pmax + Pd1max + Pd2max && SoC <= 0.05];

    [*] -> NoLoadCharge;

    state NoLoadCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state NoLoadSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state ResCoversCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state ResCoversSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state BatteryAssist {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 0;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGOnly {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 0;
            cmd_DG2 = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNG_DG1 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNG_DG1_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNG_DG1_DG2 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalBatteryDischarge {
        enter {
            Pgen_req = eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            Pgen_req = eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = Pbat_max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG = 1;
            cmd_DG1 = 1;
            cmd_DG2 = 1;
            cmd_load_cut_in = 0;
            cmd_load_cut_out = 1;
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
| SC-11 post-accept validation | `⚪ 0` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `3` |
| token / elapsed | `{'prompt_tokens': 107404, 'completion_tokens': 24966, 'total_tokens': 132370, 'estimated_prompt_tokens': 98255, 'estimated_completion_tokens': 16608, 'estimated_total_tokens': 114863, 'prompt_chars': 393014, 'completion_chars': 66424, 'n_calls': 5, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `466.116s` |
| full stage table | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b/report.md` §4 |
| run record | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b/pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz` |
| logs | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b/run_logs/stdout.txt`, `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b/checks.json`, `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:e555b8c724c1979f2d7c41f9470f0ea3ee0c0fd8e69e4a1fd19b12f1ffc75f68` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14121 | 生成初始 DSL 与 grounding seeds | initial len=5924 | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=171, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=70576 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=70576 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=70576 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=47673 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T06:42:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T06:42:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T06:42:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T06:42:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T06:45:13Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T06:45:13Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=5924,hash=sha256:896176f01fa4 |
| 7 | `2026-06-06T06:45:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T06:45:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T06:45:13Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:896176f01fa4370c52e35511fa22a748c0d14b4f11402199942356730003cf96 |
| 10 | `2026-06-06T06:45:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T06:45:13Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=5924,hash=sha256:896176f01fa4, current_hash=sha256:896176f01fa4370c52e35511fa22a748c0d14b4f11402199942356730003cf96 |
| 12 | `2026-06-06T06:45:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T06:45:13Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T06:45:13Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T06:45:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T06:45:13Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T06:45:13Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T06:45:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T06:45:13Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T06:45:14Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-06T06:45:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T06:45:14Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-06T06:46:46Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-06T06:46:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T06:46:47Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-06T06:46:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-06T06:46:47Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-06T06:48:14Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-06T06:48:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-06T06:48:15Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-06T06:48:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-06T06:48:15Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-06T06:49:46Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-06T06:49:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-06T06:49:48Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-06T06:49:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-06T06:49:48Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 38 | `2026-06-06T06:49:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-06T06:49:48Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 40 | `2026-06-06T06:49:48Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 41 | `2026-06-06T06:49:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-06T06:49:48Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 43 | `2026-06-06T06:50:38Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 44 | `2026-06-06T06:50:38Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 45 | `2026-06-06T06:50:38Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 46 | `2026-06-06T06:50:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 47 | `2026-06-06T06:50:38Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 48 | `2026-06-06T06:50:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 49 | `2026-06-06T06:50:38Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=5924,hash=sha256:896176f01fa4 |
| 50 | `2026-06-06T06:50:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 51 | `2026-06-06T06:50:38Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=5924,hash=sha256:896176f01fa4 |
| 52 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 53 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 54 | `` | `<control>` | `-` | `lg_e3_toolnode_wrapper_trace` | {} | <none> |
| 55 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |
| 56 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 57 | `` | `<control>` | `-` | `pr_e1_quality_boundary` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_no_load_charge` | default-init dispatches to NoLoadCharge for PL=0 and SoC below 0.95, charging batteries from any RES production. | ✅ |
| `no_load_soc_threshold_spare` | explicit-hot-start probes the SoC=0.95 boundary for PL=0, where RES production should become spare power rather than bat...<truncated 12 chars> | ✅ |
| `res_covers_charge_below_soc_threshold` | explicit-hot-start probes positive load fully covered by RES with SoC below 0.95, expecting residual RES to charge the b...<truncated 7 chars> | ✅ |
| `res_covers_spare_at_soc_threshold` | explicit-hot-start probes positive load fully covered by RES at SoC=0.95, expecting residual RES to be spare power. | ✅ |
| `battery_assist_for_res_deficit` | explicit-hot-start probes RES deficit within battery capacity and suitable SoC, expecting battery discharge before LNG o...<truncated 12 chars> | ✅ |
| `lng_only_after_battery_capacity_exceeded` | explicit-hot-start probes deficit above battery capacity but within LNG capacity at the SoC=0.2 boundary, expecting LNG ...<truncated 12 chars> | ✅ |
| `low_soc_lng_charge_margin` | explicit-hot-start probes low-SoC LNG-covered branch, expecting Pgmax/5 charging margin added to generator request and b...<truncated 14 chars> | ✅ |
| `lng_dg1_and_low_soc_dg_margin` | explicit-hot-start uses two local probes: DG1 joins after LNG capacity is exceeded, and the low-SoC diesel branch adds P...<truncated 23 chars> | ✅ |
| `low_soc_lng_dg1_charge_margin` | explicit-hot-start probes low-SoC diesel-generator margin case, expecting Pd1max/10 charging margin with LNG and DG1 cut...<truncated 4 chars> | ✅ |
| `lng_dg1_dg2_last_priority` | explicit-hot-start probes demand beyond LNG+DG1 but within LNG+DG1+DG2, expecting DG2 cut-in only as the last thermal pr...<truncated 7 chars> | ✅ |
| `all_thermal_battery_discharge_extreme_demand` | explicit-hot-start probes extreme demand beyond all thermal resources but within battery support, expecting all thermal ...<truncated 61 chars> | ✅ |
| `illegal_overload_completion_admitted_probe` | explicit-hot-start probes the modeled illegal overload-completion branch under infeasible residual overload inputs, expo...<truncated 72 chars> | ✅ |
| `forced_reselection_from_illegal_to_res_charge` | explicit-hot-start targets missing wildcard forced-transition coverage by starting in the illegal branch and requiring c...<truncated 67 chars> | ✅ |
| `forced_reselection_from_res_to_lng_only` | explicit-hot-start targets missing wildcard forced-transition coverage by starting in a RES spare state and requiring de...<truncated 45 chars> | ✅ |
| `forced_reselection_to_no_load_charge` | explicit-hot-start targets the missing wildcard forced-transition line for NoLoadCharge by starting outside the no-load ...<truncated 87 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5306, 'completion_chars': 17720, 'completion_tokens': 7652, 'elapsed_seconds': 140.3312771108467, 'estimated_completion_tokens': 4430, 'estimated_prompt_tokens': 6646, 'estimated_total_tokens': 11076, 'first_chunk_seconds': 44.71948690386489, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26582, 'prompt_tokens': 6469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14121}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3607, 'completion_chars': 11797, 'completion_tokens': 5028, 'elapsed_seconds': 92.14759829686955, 'estimated_completion_tokens': 2950, 'estimated_prompt_tokens': 15133, 'estimated_total_tokens': 18083, 'first_chunk_seconds': 27.59386129491031, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 60531, 'prompt_tokens': 15943, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20971}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4238, 'completion_chars': 13930, 'completion_tokens': 4711, 'elapsed_seconds': 86.82753982883878, 'estimated_completion_tokens': 3483, 'estimated_prompt_tokens': 18247, 'estimated_total_tokens': 21730, 'first_chunk_seconds': 10.284540727967396, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 72987, 'prompt_tokens': 19669, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24380}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4567, 'completion_chars': 15017, 'completion_tokens': 4925, 'elapsed_seconds': 91.12338273716159, 'estimated_completion_tokens': 3755, 'estimated_prompt_tokens': 18780, 'estimated_total_tokens': 22535, 'first_chunk_seconds': 8.848841716069728, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 75120, 'prompt_tokens': 20300, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25225}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1768, 'completion_chars': 7960, 'completion_tokens': 2650, 'elapsed_seconds': 49.77803839999251, 'estimated_completion_tokens': 1990, 'estimated_prompt_tokens': 39449, 'estimated_total_tokens': 41439, 'first_chunk_seconds': 17.779130802024156, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 157794, 'prompt_tokens': 45023, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 47673}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`16/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`3`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_c2_context_engineering_real_runs/pr-e1-path2_lng_ems-default-lg-c2-dotenv-4200b68b/report.md` §7。

</details>
