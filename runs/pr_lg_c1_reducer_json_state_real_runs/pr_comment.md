## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_lg_c1_reducer_json_state_real_runs/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | post-accept | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 37436 | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 328142 | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 34562 | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | ❌ | ⚪ 0 | `success` | 475480 | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf/report.md` |

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
- node trace count 范围：min=16，max=92；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：4/4 success，rejected=0，budget_exhausted=0，total_tokens=875620。
  - SC-11 post-accept validation：0 run 触发；本组 evidence 只能证明 non-regression / budget-policy 口径，不能声称真实覆盖 post-accept branch。
- 主结果候选：当前 4/4 个非 infrastructure run 可进入 main_result_eligible；provider/network invalid=0 个，只能作为 infrastructure evidence。

### 主结果候选 vs Path2 ref-model 蓝本边界

- Path2 run-validity：1/1 个 Path2 run 的 `main_result_eligible=true`；这只表示 run/schema/secret/trace/final verdict 可进入主结果候选。
- Path2 blueprint-validity：0/1 个 Path2 run 当前可作为 `path2_ref_model_blueprint_eligible=true`；该字段比 `main_result_eligible` 更严格。
- `path2_lng_ems`：main_result_eligible=`true`，path2_ref_model_blueprint_eligible=`false`，state_mode_decorative=`true`；reason=state_mode_decorative: final DSL is dominated by root-level forced guard reclassification; valid as FE/BVS or dispatch-classifier stress evidence, but not a Path2 ref-model blueprint
- 解释：`path2_ref_model_blueprint_eligible=false` 不会把有效 run 改成 provider invalid；它只禁止把 state-mode-decorative / 条件分类式模型宣传为 Path2 ref-model 主蓝本。

### 主要失败模式

- `success`：4 run(s)。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=success，最大 observed iteration_count=3。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=success，最大 observed iteration_count=4。
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
        enter { k1 = 1; k2 = 0; n = 0; }
        during { k1 = 1; k2 = 0; n = 0; }
    }

    state hold {
        enter { k1 = 0; k2 = 0; n = 0; }
        during { k1 = 0; k2 = 0; n = 0; }
    }

    state decrease {
        enter { k1 = 0; k2 = 1; n = 500; }
        during { k1 = 0; k2 = 1; n = 500; }
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
| token / elapsed | `{'prompt_tokens': 30637, 'completion_tokens': 6799, 'total_tokens': 37436, 'estimated_prompt_tokens': 29348, 'estimated_completion_tokens': 4628, 'estimated_total_tokens': 33976, 'prompt_chars': 117391, 'completion_chars': 18506, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `130.972s` |
| full stage table | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e/report.md` §4 |
| run record | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e/pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz` |
| logs | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e/run_logs/stdout.txt`, `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e/checks.json`, `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:2ab5a9be6909be3fcbe5310ae8fe7dd434205a63da86f5ed23567cb6f168adb8` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=8671 | 生成初始 DSL 与 grounding seeds | initial len=619 | [`record`](./pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=17, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13537 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=15228 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T04:34:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T04:34:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T04:34:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T04:34:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T04:35:37Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T04:35:37Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=619,hash=sha256:1eda27d531e2 |
| 7 | `2026-06-06T04:35:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T04:35:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T04:35:37Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:1eda27d531e2a9747b28bff4caf6fe7cc66695e1f3bb9b97606c5fb099eb1464 |
| 10 | `2026-06-06T04:35:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T04:35:37Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=619,hash=sha256:1eda27d531e2, current_hash=sha256:1eda27d531e2a9747b28bff4caf6fe7cc66695e1f3bb9b97606c5fb099eb1464 |
| 12 | `2026-06-06T04:35:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T04:35:37Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T04:35:37Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T04:35:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T04:35:37Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T04:35:37Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T04:35:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T04:35:37Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T04:35:37Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-06T04:35:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T04:35:37Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-06T04:36:25Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-06T04:36:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T04:36:25Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-06T04:36:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-06T04:36:25Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-06T04:36:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-06T04:36:25Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-06T04:36:25Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-06T04:36:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-06T04:36:25Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-06T04:37:04Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-06T04:37:04Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-06T04:37:04Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-06T04:37:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-06T04:37:04Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-06T04:37:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-06T04:37:04Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=619,hash=sha256:1eda27d531e2 |
| 40 | `2026-06-06T04:37:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-06T04:37:04Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=619,hash=sha256:1eda27d531e2 |
| 42 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 43 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 44 | `` | `<control>` | `-` | `lg_e3_toolnode_wrapper_trace` | {} | <none> |
| 45 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_increase_then_hold_at_upper_boundary` | default-init: first cycle dispatches to increase with inlet command, then slp=0.01 satisfies increase->hold and neutrali...<truncated 11 chars> | ✅ |
| `increase_no_hold_above_upper_boundary` | explicit-hot-start: increase must not transition to hold when slp is just above the slp<=0.01 guard boundary. | ✅ |
| `hold_to_increase_above_upper_boundary` | explicit-hot-start: hold transitions to increase when slp is just above 0.01 and commands inlet-valve increase behavior. | ✅ |
| `hold_no_increase_at_upper_boundary` | explicit-hot-start: hold must not take the strict slp>0.01 transition at exactly slp=0.01. | ✅ |
| `hold_to_decrease_below_lower_boundary` | explicit-hot-start: hold transitions to decrease when slp is just below -0.01 and commands pressure release. | ✅ |
| `hold_no_decrease_at_lower_boundary` | explicit-hot-start: hold must not take the strict slp<-0.01 transition at exactly slp=-0.01. | ✅ |
| `decrease_to_hold_at_lower_boundary` | explicit-hot-start: decrease transitions back to hold at exactly slp=-0.01 under the inclusive slp>=-0.01 guard. | ✅ |
| `decrease_no_hold_below_lower_boundary` | explicit-hot-start: decrease must stay in pressure-release mode when slp is still below -0.01. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1759, 'completion_chars': 5982, 'completion_tokens': 2278, 'elapsed_seconds': 43.66088135604514, 'estimated_completion_tokens': 1496, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 7989, 'first_chunk_seconds': 12.03962307504844, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 8671}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1560, 'completion_chars': 5574, 'completion_tokens': 2464, 'elapsed_seconds': 47.04257760802284, 'estimated_completion_tokens': 1394, 'estimated_prompt_tokens': 10746, 'estimated_total_tokens': 12140, 'first_chunk_seconds': 18.879133585025556, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 42983, 'prompt_tokens': 11073, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13537}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1538, 'completion_chars': 6950, 'completion_tokens': 2057, 'elapsed_seconds': 38.941040734993294, 'estimated_completion_tokens': 1738, 'estimated_prompt_tokens': 12109, 'estimated_total_tokens': 13847, 'first_chunk_seconds': 11.195485381002072, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 48436, 'prompt_tokens': 13171, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 15228}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_abs-default-lg-c1-dotenv-parallel-20260606T125500Z-643a007e/report.md` §7。

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
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float target_blood_pressure = 0.0;
def float requested_target_blood_pressure = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_message_displayed = 0;
def int software_control = 0;
def int log_entry_count = 0;
def int CA_mode = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! * -> Manual :: TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                pump_speed = built_in_switch_speed;
                flow_rate = default_flow_rate;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                    error_message_displayed = 1;
                } else {
                    alarm_signal = 0;
                    error_message_displayed = 0;
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
                error_message_displayed = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state NormalAutocontrol {
            enter {
                CA_mode = 3;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure < target_blood_pressure] {
                    flow_rate = target_blood_pressure - blood_pressure;
                } else {
                    flow_rate = 0.0;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_entry_count = log_entry_count + 1;
            }
        }

        state PumpFault {
            enter {
                CA_mode = 4;
                software_control = 0;
                alarm_signal = 1;
                error_message_displayed = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_blood_pressure = requested_target_blood_pressure; };
        Ask_StartAC -> AutocontrolInit : StartAC;
        AutocontrolInit -> NormalAutocontrol;
        NormalAutocontrol -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; };
    }
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `3` / `2` / `2` / `5` |
| token / elapsed | `{'prompt_tokens': 295953, 'completion_tokens': 32189, 'total_tokens': 328142, 'estimated_prompt_tokens': 329707, 'estimated_completion_tokens': 26008, 'estimated_total_tokens': 355715, 'prompt_chars': 1318813, 'completion_chars': 104013, 'n_calls': 10, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `610.401s` |
| full stage table | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32/report.md` §4 |
| run record | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32/pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz` |
| logs | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32/run_logs/stdout.txt`, `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32/checks.json`, `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:2eb71f932e5973e76ce9c7036d0167de4840fe2a086deb261eb7ca6cfc489635` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `57` |
| `langgraph_node_trace_hash` | `sha256:a933c1f1e8c23cdb3567ea93331d2fb98268127b7d9f33bdbbf6ebb3dfa3f66a` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `57` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12903 | 生成初始 DSL 与 grounding seeds | initial len=3174 | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=2, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=99663 | LLM per-request accept/reject + repair | candidate len=3227,3222 | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=103365 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=4, tokens=87975 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=4, tokens=87975 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=4, tokens=87975 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ⚠️ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=99663 | LLM per-request accept/reject + repair | candidate len=3227,3222 | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=103365 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=4, tokens=87975 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=1, tokens=24236 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T04:34:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T04:34:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T04:34:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T04:34:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T04:36:52Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T04:36:52Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=3174,hash=sha256:a4bfb2414c52 |
| 7 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T04:36:52Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:a4bfb2414c52c9d8ae8d62b1e0d11ad7cec3fe3824994940663a98a6b9f43bf9 |
| 10 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T04:36:52Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=3174,hash=sha256:a4bfb2414c52, current_hash=sha256:a4bfb2414c52c9d8ae8d62b1e0d11ad7cec3fe3824994940663a98a6b9f43bf9 |
| 12 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T04:36:52Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T04:36:52Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T04:36:52Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T04:36:52Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T04:36:52Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T04:36:52Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 21 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T04:36:52Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=pump_fault", "W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.NormalAutocontrol:to_path=CARA.Mode_Control_Algorithm.PumpFault"], "diagnostic_codes": ["W_UNWRITTEN_READ_VAR", "W_GUARD_VARS_NEVER_CHANGE", "W_HIGH_VAR_TO_LEAF_RATIO", "W_UNREFERENCED_VAR", "W_UNREFERENCED_VAR", "W_UNRE...<truncated 1024 chars> | <none> |
| 23 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 26 | `2026-06-06T04:36:52Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=pump_fault", "W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.NormalAutocontrol:to_path=CARA.Mode_Control_Algorithm.PumpFault"], "diagnostic_codes": ["W_UNWRITTEN_READ_VAR", "W_GUARD_VARS_NEVER_CHANGE", "W_HIGH_VAR_TO_LEAF_RATIO", "W_UNREFERENCED_VAR", "W_UNREFERENCED_VAR", "W_UNREFERENCE...<truncated 5443 chars> | current_dsl:len=3174,hash=sha256:a4bfb2414c52 |
| 27 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 28 | `2026-06-06T04:36:52Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-06T04:36:52Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 2} | <none> |
| 30 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-06T04:36:52Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=3174,hash=sha256:a4bfb2414c52 |
| 32 | `2026-06-06T04:37:28Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-06T04:37:28Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-6e7fd24414", "fixreq-0-sd4-1-b901baec1e"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=3227,hash=sha256:a8ac09db1c32 |
| 34 | `2026-06-06T04:37:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-06T04:37:28Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 36 | `2026-06-06T04:37:28Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564 |
| 37 | `2026-06-06T04:37:45Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 38 | `2026-06-06T04:37:45Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 39 | `2026-06-06T04:37:45Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 40 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-06T04:37:45Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=3227,hash=sha256:a8ac09db1c32 |
| 42 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-06T04:37:45Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564 |
| 44 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 47 | `2026-06-06T04:37:45Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564 |
| 48 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 49 | `2026-06-06T04:37:45Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=3227,hash=sha256:a8ac09db1c32, current_hash=sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564 |
| 50 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 51 | `2026-06-06T04:37:45Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 52 | `2026-06-06T04:37:45Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 53 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 54 | `2026-06-06T04:37:45Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 55 | `2026-06-06T04:37:45Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none
... <truncated 2821 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 2 | Iter 3 |
|---|---|---|---|
| `default_init_manual_outputs` | default-init: first cycle dispatches to Manual and verifies manual pump speed, default flow, and sensor-buffer behavior. | ✅ | ✅ |
| `initiate_change_start_to_normal_autocontrol` | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, then automatic init reaches Norm...<truncated 14 chars> | ⚪ | ✅ |
| `normal_pump_fault_and_fault_removed_recovery` | explicit-hot-start: PumpFaultDetected during NormalAutocontrol activates alarms and releases software control; FaultRemo...<truncated 22 chars> | ⚪ | ✅ |
| `terminate_ac_forces_manual_from_normal` | explicit-hot-start: TerminateAC from NormalAutocontrol forces the shared Manual recovery target and releases software co...<truncated 6 chars> | ✅ | ✅ |
| `ca_backmanual_forces_manual_from_ask` | explicit-hot-start: CA_backManual from Ask_StartAC forces Manual and makes CA_mode Manual. | ✅ | ✅ |
| `cb_backmanual_forces_manual_from_autocontrol_init` | explicit-hot-start: CB_backManual from AutocontrolInit forces the shared Manual recovery target. | ✅ | ✅ |
| `cp_backmanual_forces_manual_from_pump_fault` | explicit-hot-start: CP_backManual from PumpFault forces Manual while an unresolved pump fault still keeps alarms active. | ✅ | ✅ |
| `normal_autocontrol_high_pressure_then_cc_backmanual` | explicit-hot-start: NormalAutocontrol computes lower flow at higher pressure, logs data, then CC_backManual forces Manua...<truncated 2 chars> | ✅ | ✅ |
| `change_setpoint_effect_is_exact` | explicit-hot-start: ChangeSetpoint in Ask_StartAC must remain in Ask_StartAC and copy the requested setpoint exactly, ca...<truncated 55 chars> | ⚪ | ✅ |
| `pump_fault_detected_effect_is_exact` | explicit-hot-start: PumpFaultDetected from NormalAutocontrol must enter PumpFault and set pump_fault exactly to active w...<truncated 42 chars> | ⚪ | ✅ |
| `fault_removed_effect_is_exact_manual_recovery` | explicit-hot-start: FaultRemoved from PumpFault must target Manual and clear pump_fault exactly to zero while restoring ...<truncated 20 chars> | ⚪ | ✅ |
| `initiate_ac_target_and_entry_effects` | explicit-hot-start: InitiateAC from Manual must target Ask_StartAC exactly and apply Ask_StartAC entry obligations witho...<truncated 29 chars> | ⚪ | ✅ |
| `startac_target_and_autocontrolinit_entry_effects` | explicit-hot-start: StartAC from Ask_StartAC must target AutocontrolInit exactly and set software control while clearing...<truncated 18 chars> | ⚪ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=pump_fault, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.NormalAutocontrol:to_path=CARA.Mode_Control_Algorithm.PumpFault, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, ... +3 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564` |
| 2 | `1` | ✅ | `SD-6` | initiate_change_start_to_normal_autocontrol, normal_pump_fault_and_fault_removed_recovery, change_setpoint_effect_is_exact, pump_fault_detected_effect_is_exact, fault_removed_effect_is_exact_manual_recovery, ... +2 | accept=7, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:7ba3465db7f9cfad6e47d2197f8f36738faf616536ef2db0a58ff045387bd4b1` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32/report.md` §7。

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
    ! * -> F1 : reset;

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
| token / elapsed | `{'prompt_tokens': 25891, 'completion_tokens': 8671, 'total_tokens': 34562, 'estimated_prompt_tokens': 25228, 'estimated_completion_tokens': 5727, 'estimated_total_tokens': 30955, 'prompt_chars': 100908, 'completion_chars': 22908, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `165.234s` |
| full stage table | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c/report.md` §4 |
| run record | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c/pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz` |
| logs | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c/run_logs/stdout.txt`, `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c/checks.json`, `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:92f2384217a5b4e41a86e6db91b67ee3b67ba1a600118a42b888f568441096a2` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=10178 | 生成初始 DSL 与 grounding seeds | initial len=658 | [`record`](./pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=14326 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10058 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T04:34:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T04:34:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T04:34:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T04:34:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T04:36:04Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T04:36:04Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=658,hash=sha256:af4349932f7d |
| 7 | `2026-06-06T04:36:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T04:36:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T04:36:04Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:af4349932f7d9a422bdef8ed68324cf3dc251ecf6e13aec401bb37d00c313d1a |
| 10 | `2026-06-06T04:36:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T04:36:04Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=658,hash=sha256:af4349932f7d, current_hash=sha256:af4349932f7d9a422bdef8ed68324cf3dc251ecf6e13aec401bb37d00c313d1a |
| 12 | `2026-06-06T04:36:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T04:36:04Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T04:36:04Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T04:36:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T04:36:04Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T04:36:04Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T04:36:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T04:36:04Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T04:36:04Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-06T04:36:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T04:36:04Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-06T04:37:06Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-06T04:37:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T04:37:06Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-06T04:37:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-06T04:37:06Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-06T04:37:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-06T04:37:06Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-06T04:37:06Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-06T04:37:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-06T04:37:06Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-06T04:37:38Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-06T04:37:38Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-06T04:37:38Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-06T04:37:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-06T04:37:38Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-06T04:37:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-06T04:37:38Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=658,hash=sha256:af4349932f7d |
| 40 | `2026-06-06T04:37:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-06T04:37:38Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=658,hash=sha256:af4349932f7d |
| 42 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 43 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 44 | `` | `<control>` | `-` | `lg_e3_toolnode_wrapper_trace` | {} | <none> |
| 45 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_to_f2_then_f3` | default-init probe: dispatches to F1 stop, verifies no-request stay, then PS2 drives upward to F2 and next PS3 request d...<truncated 19 chars> | ✅ |
| `f1_direct_request_to_f3` | explicit-hot-start probe: from F1, PS3 must select MU3 upward travel and S3 must stop at F3. | ✅ |
| `f2_request_down_to_f1` | explicit-hot-start probe: from F2, PS1 must select MD1 downward travel and S1 must stop at F1. | ✅ |
| `f3_request_down_to_f1` | explicit-hot-start probe: from F3, PS1 must select MD1 downward travel and S1 must stop at F1. | ✅ |
| `f3_request_down_to_f2` | explicit-hot-start probe: from F3, PS2 must select MD2 downward travel and S2 must stop at F2. | ✅ |
| `reset_from_up_motion_forces_f1` | explicit-hot-start forced-transition probe: reset during upward MU3 motion must force F1 stop regardless of outstanding ...<truncated 16 chars> | ✅ |
| `reset_from_down_motion_forces_f1` | explicit-hot-start forced-transition probe: reset during downward MD2 motion must force F1 stop regardless of outstandin...<truncated 18 chars> | ✅ |
| `reset_from_floor_state_forces_f1` | explicit-hot-start forced-transition probe: reset from a stopped non-F1 floor must force F1 stop. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3094, 'completion_chars': 10400, 'completion_tokens': 3740, 'elapsed_seconds': 70.18084394402103, 'estimated_completion_tokens': 2600, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 9123, 'first_chunk_seconds': 13.833140512986574, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10178}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1938, 'completion_chars': 7744, 'completion_tokens': 3319, 'elapsed_seconds': 61.65045212203404, 'estimated_completion_tokens': 1936, 'estimated_prompt_tokens': 10755, 'estimated_total_tokens': 12691, 'first_chunk_seconds': 26.70451294700615, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 43020, 'prompt_tokens': 11007, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14326}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1162, 'completion_chars': 4764, 'completion_tokens': 1612, 'elapsed_seconds': 31.950735999969766, 'estimated_completion_tokens': 1191, 'estimated_prompt_tokens': 7950, 'estimated_total_tokens': 9141, 'first_chunk_seconds': 11.416666926001199, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 31799, 'prompt_tokens': 8446, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10058}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path1_elevator-default-lg-c1-dotenv-parallel-20260606T125500Z-a1bc6b6c/report.md` §7。

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
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float eng3_Pmax = 0.0;
def float Pbat_dismax = 0.0;
def float Pgen_req = 0.0;
def float Pbat_dis = 0.0;
def float Pbat_ch = 0.0;
def float Pspare = 0.0;
def int cmd_lng_cut_in = 0;
def int cmd_lng_cut_out = 1;
def int cmd_dg1_cut_in = 0;
def int cmd_dg1_cut_out = 1;
def int cmd_dg2_cut_in = 0;
def int cmd_dg2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_dismax];
    ! * -> LNGCoversDemand : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_dismax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGDG1CoversDemand : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + Pd1max];
    ! * -> LNGDG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + Pd1max];
    ! * -> LNGDG1DG2CoversDemand : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax + Pd1max && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax];
    ! * -> LNGDG1DG2LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax + Pd1max && PL - Ppv - Pw <= Pgmax + Pd1max + eng3_Pmax];
    ! * -> ExtremeAllThermalBattery : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + Pd1max + eng3_Pmax];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0;
            Pbat_dis = 0;
            Pbat_ch = Ppv + Pw;
            Pspare = 0;
            cmd_lng_cut_in = 0;
            cmd_lng_cut_out = 1;
            cmd_dg1_cut_in = 0;
            cmd_dg1_cut_out = 1;
            cmd_dg2_cut_in = 0;
            cmd_dg2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0;
            Pbat_dis = 0;
            Pbat_ch = 0;
            Pspare = Ppv + Pw;
            cmd_lng_cut_in = 0;
            cmd_lng_cut_out = 1;
            cmd_dg1_cut_in = 0;
            cmd_dg1_cut_out = 1;
            cmd_dg2_cut_in = 0;
            cmd_dg2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0;
            Pbat_dis = 0;
            Pbat_ch = Ppv + Pw - PL;
            Pspare = 0;
            cmd_lng_cut_in = 0;
            cmd_lng_cut_out = 1;
            cmd_dg1_cut_in = 0;
            cmd_dg1_cut_out = 1;
            cmd_dg2_cut_in = 0;
            cmd_dg2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0;
            Pbat_dis = 0;
            Pbat_ch = 0;
            Pspare = Ppv + Pw - PL;
            cmd_lng_cut_in = 0;
            cmd_lng_cut_out = 1;
            cmd_dg1_cut_in = 0;
            cmd_dg1_cut_out = 1;
            cmd_dg2_cut_in = 0;
            cmd_dg2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state RESBatteryDischarge {
        enter {
            Pgen_req = 0;
            Pbat_dis = PL - Ppv - Pw;
            Pbat_ch = 0;
            Pspare = 0;
            cmd_lng_cut_in = 0;
            cmd_lng_cut_out = 1;
            cmd_dg1_cut_in = 0;
            cmd_dg1_cut_out = 1;
            cmd_dg2_cut_in = 0;
            cmd_dg2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGCoversDemand {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_dis = 0;
            Pbat_ch = 0;
            Pspare = 0;
            cmd_lng_cut_in = 1;
            cmd_lng_cut_out = 0;
            cmd_dg1_cut_in = 0;
            cmd_dg1_cut_out = 1;
            cmd_dg2_cut_in = 0;
            cmd_dg2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGLowSoCChargeMargin {
        enter {
            if [PL - Ppv - Pw + Pgmax / 5 <= Pgmax] {
                Pgen_req = PL - Ppv - Pw + Pgmax / 5;
                Pbat_ch = Pgmax / 5;
            } else {
                Pgen_req = PL - Ppv - Pw;
                Pbat_ch = 0;
            }
            Pbat_dis = 0;
            Pspare = 0;
            cmd_lng_cut_in = 1;
            cmd_lng_cut_out = 0;
            cmd_dg1_cut_in = 0;
            cmd_dg1_cut_out = 1;
            cmd_dg2_cut_in = 0;
            cmd_dg2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1CoversDemand {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_dis = 0;
            Pbat_ch = 0;
            Pspare = 0;
            cmd_lng_cut_in = 1;
            cmd_lng_cut_out = 0;
            cmd_dg1_cut_in = 1;
            cmd_dg1_cut_out = 0;
            cmd_dg2_cut_in = 0;
            cmd_dg2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1LowSoCChargeMargin {
        enter {
            if [PL - Ppv - Pw + Pd1max / 10 <= Pgmax + Pd1max] {
                Pgen_req = PL - Ppv - Pw + Pd1max / 10;
                Pbat_ch = Pd1max / 10;
            } else {
                Pgen_req = PL - Ppv - Pw;
                Pbat_ch = 0;
            }
            Pbat_dis = 0;
            Pspare = 0;
            cmd_lng_cut_in = 1;
            cmd_lng_cut_out = 0;
            cmd_dg1_cut_in = 1;
            cmd_dg1_cut_out = 0;
            cmd_dg2_cut_in = 0;
            cmd_dg2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1DG2CoversDemand {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_dis = 0;
            Pbat_ch = 0;
            Pspare = 0;
            cmd_lng_cut_in = 1;
            cmd_lng_cut_out = 0;
            cmd_dg1_cut_in = 1;
            cmd_dg1_cut_out = 0;
            cmd_dg2_cut_in = 1;
            cmd_dg2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LNGDG1DG2LowSoCChargeMargin {
        enter {
            if [PL - Ppv - Pw + Pd1max / 10 <= Pgmax + Pd1max + eng3_Pmax] {
                Pgen_req = PL - Ppv - Pw + Pd1max / 10;
                Pbat_ch = Pd1max / 10;
            } else {
                Pgen_req = PL - Ppv - Pw;
                Pbat_ch = 0;
            }
            Pbat_dis = 0;
            Pspare = 0;
            cmd_lng_cut_in = 1;
            cmd_lng_cut_out = 0;
            cmd_dg1_cut_in = 1;
            cmd_dg1_cut_out = 0;
            cmd_dg2_cut_in = 1;
            cmd_dg2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state ExtremeAllThermalBattery {
        enter {
            Pgen_req = Pgmax + Pd1max + eng3_Pmax;
            Pbat_dis = PL - Ppv - Pw - Pgmax - Pd1max - eng3_Pmax;
            Pbat_ch = 0;
            Pspare = 0;
            cmd_lng_cut_in = 1;
            cmd_lng_cut_out = 0;
            cmd_dg1_cut_in = 1;
            cmd_dg1_cut_out = 0;
            cmd_dg2_cut_in = 1;
            cmd_dg2_cut_out = 0;
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `4` / `3` / `1` / `7` |
| token / elapsed | `{'prompt_tokens': 425610, 'completion_tokens': 49870, 'total_tokens': 475480, 'estimated_prompt_tokens': 394761, 'estimated_completion_tokens': 33828, 'estimated_total_tokens': 428589, 'prompt_chars': 1579026, 'completion_chars': 135296, 'n_calls': 13, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `953.778s` |
| full stage table | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf/report.md` §4 |
| run record | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf/pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz` |
| logs | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf/run_logs/stdout.txt`, `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf/checks.json`, `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:1bf4fc4280b89ef525d3fc767da610584026844ce5792a360c1ef2a0fb14a4b0` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `92` |
| `langgraph_node_trace_hash` | `sha256:063ef0dbec7d4ea5d8985496f77df6e613aeaabb4c70ce15f65f393cc2339ba6` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `92` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=15339 | 生成初始 DSL 与 grounding seeds | initial len=7313 | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=25, advisory=151, info=0; blocking=0, advisory=176, info=0; blocking=25, advisory=151, info=0; blocking=0, advisory=176, info=0; blocking=0, advisory=176, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=110702 | LLM per-request accept/reject + repair | candidate len=0,0,7811 | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=25, advisory=151, info=0; blocking=0, advisory=176, info=0; blocking=25, advisory=151, info=0; blocking=0, advisory=176, info=0; blocking=0, advisory=176, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=108474 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=108474 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=108474 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=220124 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=25, advisory=151, info=0; blocking=0, advisory=176, info=0; blocking=25, advisory=151, info=0; blocking=0, advisory=176, info=0; blocking=0, advisory=176, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=110702 | LLM per-request accept/reject + repair | candidate len=0,0,7811 | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=25, advisory=151, info=0; blocking=0, advisory=176, info=0; blocking=25, advisory=151, info=0; blocking=0, advisory=176, info=0; blocking=0, advisory=176, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=220124 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=25, advisory=151, info=0; blocking=0, advisory=176, info=0; blocking=25, advisory=151, info=0; blocking=0, advisory=176, info=0; blocking=0, advisory=176, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=220124 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=110702 | LLM per-request accept/reject + repair | candidate len=0,0,7811 | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-10` | 是 | 2 | ✅ | LLM calls=1, tokens=20841 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SC-11` | 否 | 2 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=25, advisory=151, info=0; blocking=0, advisory=176, info=0; blocking=25, advisory=151, info=0; blocking=0, advisory=176, info=0; blocking=0, advisory=176, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=108474 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=220124 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T04:34:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T04:34:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T04:34:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T04:34:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T04:37:35Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T04:37:35Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=7313,hash=sha256:61722f861ba4 |
| 7 | `2026-06-06T04:37:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T04:37:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T04:37:35Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:61722f861ba411647785b9ef250434a2f617638dd5d785c5237dd0caefbeec44 |
| 10 | `2026-06-06T04:37:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T04:37:35Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=7313,hash=sha256:61722f861ba4, current_hash=sha256:61722f861ba411647785b9ef250434a2f617638dd5d785c5237dd0caefbeec44 |
| 12 | `2026-06-06T04:37:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T04:37:35Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T04:37:35Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T04:37:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T04:37:35Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T04:37:36Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T04:37:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T04:37:36Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T04:37:36Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 21 | `2026-06-06T04:37:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T04:37:36Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pbat_dismax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoversDemand", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS...<truncated 9956 chars> | <none> |
| 23 | `2026-06-06T04:37:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-06T04:37:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T04:37:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 26 | `2026-06-06T04:37:36Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": [
... <truncated 7243 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 |
|---|---|---|---|---|---|
| `default_init_zero_load_charge` | default-init: with PL=0 and SoC below 0.95, first cycle dispatches to zero-load battery charging from RES production. | ✅ | ✅ | ✅ | ✅ |
| `zero_load_soc_full_spare_boundary` | explicit-hot-start: at the SoC=0.95 boundary with PL=0, RES production should become spare power rather than battery cha...<truncated 4 chars> | ✅ | ✅ | ✅ | ✅ |
| `res_covers_charge_below_full_soc` | explicit-hot-start: when RES covers positive PL and SoC is just below 0.95, serve load from RES and charge the surplus. | ✅ | ✅ | ✅ | ✅ |
| `res_covers_spare_at_full_soc` | explicit-hot-start: when RES covers positive PL and SoC is at least 0.95, surplus RES should be reported as spare power. | ✅ | ✅ | ✅ | ✅ |
| `battery_discharge_at_soc_suitable_boundary` | explicit-hot-start: at the SoC=0.2 suitability boundary, RES shortfall within battery discharge capacity should be suppl...<truncated 15 chars> | ✅ | ✅ | ✅ | ✅ |
| `lng_covers_after_battery_capacity_exceeded` | explicit-hot-start: with suitable SoC but residual demand above battery discharge capacity and within LNG capacity, LNG ...<truncated 34 chars> | ✅ | ✅ | ✅ | ✅ |
| `lng_low_soc_charge_margin` | explicit-hot-start: with low SoC and residual demand coverable by LNG plus Pgmax/5 margin, LNG should charge battery usi...<truncated 15 chars> | ✅ | ✅ | ✅ | ✅ |
| `lng_dg1_covers_after_lng_capacity_exceeded` | explicit-hot-start: with suitable SoC and residual demand exceeding LNG but within LNG+DG1 capacity, DG1 should cut in a...<truncated 28 chars> | ✅ | ✅ | ✅ | ✅ |
| `lng_dg1_low_soc_charge_margin` | explicit-hot-start: with low SoC in the LNG+DG1 region, add the Pd1max/10 charging margin while keeping DG2 out. | ✅ | ✅ | ✅ | ✅ |
| `lng_dg1_dg2_covers_after_dg1_capacity_exceeded` | explicit-hot-start: with suitable SoC and residual demand exceeding LNG+DG1 but within all thermal capacity, DG2 should ...<truncated 12 chars> | ✅ | ✅ | ✅ | ✅ |
| `lng_dg1_dg2_low_soc_charge_margin` | explicit-hot-start: with low SoC in the all-thermal covered region, add the Pd1max/10 charging margin while all thermal ...<truncated 17 chars> | ✅ | ✅ | ✅ | ✅ |
| `extreme_overload_all_thermal_battery_lack` | explicit-hot-start: when demand exceeds RES plus all thermal resources, activate all thermal units, cover the lack by ba...<truncated 71 chars> | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassify_extreme_to_res_spare` |  | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassify_zero_to_all_thermal_low_soc` |  | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassify_res_to_zero_load_charge` |  | ✅ | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pbat_dismax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoversDemand, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGCoversDemand, ... +24 | accept=0, reject=12, waiver=12 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 2 | `1` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pbat_dismax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGCoversDemand, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.RESBatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.LNGCoversDemand, ... +24 | accept=0, reject=12, waiver=12 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `2` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:400fbf78390cd85c167d007b32f0ae358cafd9054f99c65a369cba8c1bb1e8cf` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_c1_reducer_json_state_real_runs/pr-e1-path2_lng_ems-default-lg-c1-dotenv-parallel-20260606T125500Z-41494fdf/report.md` §7。

</details>
