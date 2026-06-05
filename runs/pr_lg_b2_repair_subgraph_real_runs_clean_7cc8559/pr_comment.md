## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | post-accept | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 37667 | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ❌ | ⚪ | ⚪ 0 | `success_but_weak_oracle_ineligible` | 395737 | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 33942 | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | ❌ | ⚪ 0 | `success` | 523563 | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794/report.md` |

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
- node trace count 范围：min=16，max=91；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：4/4 success，rejected=0，budget_exhausted=0，total_tokens=990909。
  - SC-11 post-accept validation：0 run 触发；本组 evidence 只能证明 non-regression / budget-policy 口径，不能声称真实覆盖 post-accept branch。
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
- `path1_cara`：失败/成功类别=success_but_weak_oracle_ineligible，最大 observed iteration_count=3。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=success，最大 observed iteration_count=5。
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
| SC-11 post-accept validation | `⚪ 0` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 30839, 'completion_tokens': 6828, 'total_tokens': 37667, 'estimated_prompt_tokens': 29934, 'estimated_completion_tokens': 4682, 'estimated_total_tokens': 34616, 'prompt_chars': 119731, 'completion_chars': 18725, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `131.356s` |
| full stage table | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611/report.md` §4 |
| run record | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611/pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz` |
| logs | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611/run_logs/stdout.txt`, `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611/checks.json`, `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:7f636790c3dccb6be74881cc89e157fd4c4556a56b6a96ca72cc8529bb0a4b8a` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=8709 | 生成初始 DSL 与 grounding seeds | initial len=637 | [`record`](./pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=17, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13593 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=15365 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T17:34:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T17:34:06Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T17:34:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T17:34:06Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T17:34:50Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T17:34:50Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=637,hash=sha256:096cac387054 |
| 7 | `2026-06-05T17:34:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T17:34:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T17:34:50Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:096cac387054564a67539bd814a5fd0c4068174acd8ddf733c1f150b473ac22c |
| 10 | `2026-06-05T17:34:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T17:34:50Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=637,hash=sha256:096cac387054, current_hash=sha256:096cac387054564a67539bd814a5fd0c4068174acd8ddf733c1f150b473ac22c |
| 12 | `2026-06-05T17:34:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T17:34:50Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T17:34:50Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T17:34:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T17:34:50Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T17:34:50Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T17:34:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T17:34:50Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T17:34:50Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T17:34:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T17:34:50Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T17:35:38Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T17:35:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T17:35:38Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T17:35:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T17:35:38Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T17:35:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T17:35:38Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T17:35:38Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T17:35:38Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T17:35:38Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T17:36:16Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T17:36:16Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T17:36:16Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T17:36:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T17:36:16Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T17:36:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T17:36:16Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=637,hash=sha256:096cac387054 |
| 40 | `2026-06-05T17:36:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T17:36:16Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=637,hash=sha256:096cac387054 |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_reaches_increase_outputs` | default-init probe: first empty cycle dispatches to increase and asserts inlet-valve increase outputs k1=1, k2=0, n=0. | ✅ |
| `increase_to_hold_at_upper_boundary` | explicit-hot-start probe: increase transitions to hold exactly when slp <= 0.01 and hold neutralizes both valves. | ✅ |
| `increase_stays_above_upper_boundary` | explicit-hot-start no-fire probe: increase must not transition to hold when slp is just above 0.01. | ✅ |
| `hold_to_increase_above_upper_boundary` | explicit-hot-start probe: hold transitions to increase when slp > 0.01 and increase asserts pressure-increase outputs. | ✅ |
| `hold_stays_at_upper_boundary` | explicit-hot-start boundary no-fire probe: hold must not transition to increase when slp is exactly 0.01. | ✅ |
| `hold_to_decrease_below_lower_boundary` | explicit-hot-start probe: hold transitions to decrease when slp < -0.01 and decrease asserts return-valve and pump relea...<truncated 11 chars> | ✅ |
| `hold_stays_at_lower_boundary` | explicit-hot-start boundary no-fire probe: hold must not transition to decrease when slp is exactly -0.01. | ✅ |
| `decrease_lower_boundary_fire_and_no_fire` | explicit-hot-start boundary probes: decrease stays releasing below -0.01, but transitions to hold exactly when slp >= -0...<truncated 4 chars> | ✅ |
| `decrease_to_hold_at_lower_boundary` | explicit-hot-start probe: decrease transitions to hold when slp is exactly -0.01 and hold neutralizes both valves. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1672, 'completion_chars': 5940, 'completion_tokens': 2316, 'elapsed_seconds': 43.88130610799999, 'estimated_completion_tokens': 1485, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 7978, 'first_chunk_seconds': 14.976306515018223, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 8709}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1686, 'completion_chars': 6226, 'completion_tokens': 2564, 'elapsed_seconds': 47.97580967299291, 'estimated_completion_tokens': 1557, 'estimated_prompt_tokens': 10818, 'estimated_total_tokens': 12375, 'first_chunk_seconds': 17.59107273601694, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 43269, 'prompt_tokens': 11029, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13593}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1429, 'completion_chars': 6559, 'completion_tokens': 1948, 'elapsed_seconds': 38.166605293983594, 'estimated_completion_tokens': 1640, 'estimated_prompt_tokens': 12623, 'estimated_total_tokens': 14263, 'first_chunk_seconds': 12.366254308988573, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 50490, 'prompt_tokens': 13417, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 15365}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_abs-default-lg-b2-clean-7cc8559-88263611/report.md` §7。

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
def int log_entry_count = 0;
def float patient_bp = 0.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_buffer_bp = 0.0;
def float flow_rate = 0.0;
def float manual_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def float infusion_rate_log = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        >> during before {
            shared_buffer_bp = patient_bp;
        }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_signal = 0;
                pump_fault = 0;
            }
            during {
                pump_speed = built_in_switch_speed;
                flow_rate = manual_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                pump_fault = 0;
            }
        }

        state Autocontrol {
            during {
                if [pump_fault == 0] {
                    flow_rate = target_bp - patient_bp;
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    infusion_rate_log = flow_rate;
                    log_entry_count = log_entry_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
            target_bp = requested_target_bp;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> Manual : TerminateAC;
        AutocontrolInit -> Autocontrol;
        Autocontrol -> PumpFault : if [pump_fault != 0];
        Autocontrol -> Manual : TerminateAC;
        Autocontrol -> PumpFault :: PumpFaultOccurred effect {
            pump_fault = 1;
        };
        PumpFault -> Manual :: FaultRemoved;
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
| SC-11 post-accept validation | `⚪ 0` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `3` / `2` / `2` / `9` |
| token / elapsed | `{'prompt_tokens': 337946, 'completion_tokens': 57791, 'total_tokens': 395737, 'estimated_prompt_tokens': 353691, 'estimated_completion_tokens': 47417, 'estimated_total_tokens': 401108, 'prompt_chars': 1414749, 'completion_chars': 189654, 'n_calls': 14, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1090.605s` |
| full stage table | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d/report.md` §4 |
| run record | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d/pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz` |
| logs | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d/run_logs/stdout.txt`, `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d/checks.json`, `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:001ce94b2862f9cadc7fb08038f5cbe6c14669b26fa9bf63a609f7fdd75aaeff` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `67` |
| `langgraph_node_trace_hash` | `sha256:83e71f0e0d6e2a3b9e06e905e23adb9fb5075d8b1e4d8f990af084ab9c97302d` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `67` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14097 | 生成初始 DSL 与 grounding seeds | initial len=2633 | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=68955 | LLM per-request accept/reject + repair | candidate len=2633,2690 | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=70908 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=57428 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=68955 | LLM per-request accept/reject + repair | candidate len=2633,2690 | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=70908 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=57428 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T17:34:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T17:34:06Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T17:34:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T17:34:06Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T17:36:27Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T17:36:27Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2633,hash=sha256:e364b823420f |
| 7 | `2026-06-05T17:36:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T17:36:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T17:36:27Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:e364b823420f00d9965b304c24f127cbd463153e96248cd7351fc9e86f5949e9 |
| 10 | `2026-06-05T17:36:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T17:36:27Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2633,hash=sha256:e364b823420f, current_hash=sha256:e364b823420f00d9965b304c24f127cbd463153e96248cd7351fc9e86f5949e9 |
| 12 | `2026-06-05T17:36:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T17:36:27Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T17:36:27Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T17:36:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T17:36:27Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T17:36:28Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T17:36:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T17:36:28Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T17:36:28Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T17:36:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T17:36:28Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T17:37:59Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T17:37:59Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T17:38:00Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T17:38:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T17:38:00Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T17:39:24Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T17:39:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T17:39:24Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T17:39:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T17:39:24Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T17:41:03Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T17:41:03Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T17:41:04Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T17:41:04Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T17:41:04Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T17:41:04Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T17:41:04Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 42 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T17:41:04Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 12, "n_scenarios_passed": 11, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 44 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 47 | `2026-06-05T17:41:04Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 12, "n_scenarios_passed": 11, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2633,hash=sha256:e364b823420f |
| 48 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 49 | `2026-06-05T17:41:04Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 50 | `2026-06-05T17:41:04Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 51 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 52 | `2026-06-05T17:41:04Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2633,hash=sha256:e364b823420f |
| 53 | `2026-06-05T17:41:34Z` | `SL-9
... <truncated 3601 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| `default_init_enters_manual_and_uses_manual_inputs` | default-init: first empty cycle dispatches to Manual, stores BP in the shared buffer, and drives pump speed/flow from ma...<truncated 12 chars> | ✅ | ✅ | ✅ |
| `initiate_change_setpoint_start_and_enter_autocontrol` | default-init: caregiver initiates AC, changes the Ask_StartAC setpoint, presses StartAC, then the init state advances to...<truncated 20 chars> | ✅ | ✅ | ✅ |
| `terminate_from_ask_and_init_returns_manual` | explicit-hot-start: TerminateAC returns Ask_StartAC to Manual, and after re-entering AutocontrolInit it also returns to ...<truncated 7 chars> | ❌ | ✅ | ✅ |
| `autocontrol_fault_alarms_then_fault_removed_manual` | explicit-hot-start: normal Autocontrol computes/logs flow while fault-free, PumpFaultOccurred enters PumpFault with alar...<truncated 57 chars> | ✅ | ✅ | ✅ |
| `autocontrol_with_existing_complication_does_not_control_flow` | explicit-hot-start: when Autocontrol already has a pump-operation complication, a no-event cycle must take the safety re...<truncated 54 chars> | ✅ | ✅ | ✅ |
| `terminate_from_autocontrol_returns_manual` | explicit-hot-start: caregiver TerminateAC from normal Autocontrol releases algorithmic control and returns to Manual ope...<truncated 7 chars> | ✅ | ✅ | ✅ |
| `forced_ca_and_cb_back_manual_from_distinct_states` | explicit-hot-start: CA_backManual from Autocontrol and CB_backManual from Ask_StartAC both force the shared recovery tar...<truncated 11 chars> | ✅ | ✅ | ✅ |
| `forced_cp_and_cc_back_manual_from_fault_and_init` | explicit-hot-start: CP_backManual from PumpFault and CC_backManual from AutocontrolInit both force Manual as the recover...<truncated 9 chars> | ✅ | ✅ | ✅ |
| `change_setpoint_effect_value_direct_probe` | explicit-hot-start: ChangeSetpoint in Ask_StartAC must assign target_bp exactly from requested_target_bp, exposing missi...<truncated 37 chars> | ✅ | ✅ | ✅ |
| `changed_setpoint_drives_autocontrol_flow` | explicit-hot-start: after ChangeSetpoint then StartAC, Autocontrol must compute flow from the changed target, catching m...<truncated 67 chars> | ✅ | ✅ | ✅ |
| `startac_control_enable_effect_value_probe` | explicit-hot-start: StartAC entering AutocontrolInit must set algorithmic-control outputs exactly, exposing missing or w...<truncated 36 chars> | ✅ | ✅ | ✅ |
| `pump_fault_entry_effect_value_probe` | explicit-hot-start: PumpFaultOccurred from Autocontrol must assert the fault/alarm and release software control exactly,...<truncated 51 chars> | ✅ | ✅ | ✅ |
| `fault_removed_manual_recovery_exact_reset_probe` | explicit-hot-start: FaultRemoved from PumpFault must land in Manual with fault/alarm cleared and manual outputs restored...<truncated 56 chars> | ⚪ | ✅ | ✅ |
| `forced_backmanual_exact_reset_from_dirty_autocontrol` | explicit-hot-start: a backManual fallback from dirty Autocontrol must force Manual and assign the exact shared recovery ...<truncated 59 chars> | ⚪ | ✅ | ✅ |
| `change_setpoint_wrong_constant_sentinel_probe` | explicit-hot-start: ChangeSetpoint must copy a non-default requested target exactly, so missing effect or wrong constant...<truncated 58 chars> | ⚪ | ⚪ | ✅ |
| `pumpfault_existing_complication_guard_entry_effect_probe` | explicit-hot-start: an already-present pump fault in Autocontrol must enter PumpFault without an event and set alarm/rel...<truncated 54 chars> | ⚪ | ⚪ | ✅ |
| `initiateac_ask_entry_exact_reset_probe` | explicit-hot-start: InitiateAC from dirty Manual must enter Ask_StartAC with CA_mode/software_control exactly reset, exp...<truncated 46 chars> | ⚪ | ⚪ | ✅ |
| `terminate_from_dirty_init_manual_reset_probe` | explicit-hot-start: TerminateAC from dirty AutocontrolInit must enter Manual and clear fault/alarm/control outputs exact...<truncated 58 chars> | ⚪ | ⚪ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | terminate_from_ask_and_init_returns_manual | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:f04099ce732a370989d587eccf7681da3e383b00686d0aca51dab7365d5c8563` |
| 2 | `1` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:7b8ce3144e97ba307c15ae5a3bb922da8b77f89d1c0c60869f90bf6ba05397d1` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d/report.md` §7。

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
| SC-11 post-accept validation | `⚪ 0` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 26982, 'completion_tokens': 6960, 'total_tokens': 33942, 'estimated_prompt_tokens': 26349, 'estimated_completion_tokens': 5476, 'estimated_total_tokens': 31825, 'prompt_chars': 105388, 'completion_chars': 21901, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `140.57s` |
| full stage table | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0/report.md` §4 |
| run record | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0/pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz` |
| logs | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0/run_logs/stdout.txt`, `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0/checks.json`, `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:03b378d5c8dab063117d1bbd020d5a20a2a6d6b612bd337ff2f14098196ecebf` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9349 | 生成初始 DSL 与 grounding seeds | initial len=669 | [`record`](./pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13890 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10703 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T17:34:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T17:34:06Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T17:34:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T17:34:06Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T17:35:02Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T17:35:02Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=669,hash=sha256:ffc4ea773d66 |
| 7 | `2026-06-05T17:35:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T17:35:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T17:35:02Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:ffc4ea773d6686384ce9f98fccefbeb9f4bc53fcb9928459112368750e06d971 |
| 10 | `2026-06-05T17:35:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T17:35:02Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=669,hash=sha256:ffc4ea773d66, current_hash=sha256:ffc4ea773d6686384ce9f98fccefbeb9f4bc53fcb9928459112368750e06d971 |
| 12 | `2026-06-05T17:35:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T17:35:02Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T17:35:02Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T17:35:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T17:35:02Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T17:35:03Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T17:35:03Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T17:35:03Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T17:35:03Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T17:35:03Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T17:35:03Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T17:35:53Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T17:35:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T17:35:53Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T17:35:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T17:35:53Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T17:35:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T17:35:53Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T17:35:53Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T17:35:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T17:35:53Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T17:36:26Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T17:36:26Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T17:36:26Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T17:36:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T17:36:26Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T17:36:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T17:36:26Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=669,hash=sha256:ffc4ea773d66 |
| 40 | `2026-06-05T17:36:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T17:36:26Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=669,hash=sha256:ffc4ea773d66 |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_to_f2_then_up_to_f3` | default-init dispatches to F1 stopped, then PS2 moves upward to MU2, S2 stops at F2, and the next PS3 request immediatel...<truncated 22 chars> | ✅ |
| `f1_direct_to_f3_then_down_to_f2` | explicit-hot-start from F1 checks PS3 selects MU3, S3 stops at F3, then PS2 selects downward MD2 and S2 stops at F2. | ✅ |
| `f2_down_request_to_f1` | explicit-hot-start from F2 checks PS1 selects downward MD1 and S1 arrival stops at F1. | ✅ |
| `f3_down_request_reset_from_motion` | explicit-hot-start from F3 checks PS1 selects MD1, then Reset from a downward motion context forces F1 stopped. | ✅ |
| `reset_from_floor_context` | explicit-hot-start from F2 verifies the global Reset also forces F1 from a stopped floor context. | ✅ |
| `reset_from_upward_motion_context` | explicit-hot-start from MU3 verifies Reset forces F1 from an upward drive context and clears hbrg to stop. | ✅ |
| `no_fire_without_request_or_sensor` | explicit-hot-start probes absence of phantom transitions: F1 stays stopped with no request, and MU2 remains upward motio...<truncated 21 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2637, 'completion_chars': 9767, 'completion_tokens': 2911, 'elapsed_seconds': 56.60380737899686, 'estimated_completion_tokens': 2442, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 8965, 'first_chunk_seconds': 9.072639212012291, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9349}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1834, 'completion_chars': 7274, 'completion_tokens': 2353, 'elapsed_seconds': 50.5292967770074, 'estimated_completion_tokens': 1819, 'estimated_prompt_tokens': 11291, 'estimated_total_tokens': 13110, 'first_chunk_seconds': 17.43672559800325, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 45161, 'prompt_tokens': 11537, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13890}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1177, 'completion_chars': 4860, 'completion_tokens': 1696, 'elapsed_seconds': 32.20356188400183, 'estimated_completion_tokens': 1215, 'estimated_prompt_tokens': 8535, 'estimated_total_tokens': 9750, 'first_chunk_seconds': 10.95412455900805, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 34138, 'prompt_tokens': 9007, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10703}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path1_elevator-default-lg-b2-clean-7cc8559-3f327dc0/report.md` §7。

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
def float battery_Pmax = 0.0;
def float Plngmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charging_power = 0.0;
def float spare_power = 0.0;
def int cut_in_LNG = 0;
def int cut_out_LNG = 0;
def int cut_in_DG1 = 0;
def int cut_out_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_out_DG2 = 0;
def int cut_in_DG3 = 0;
def int cut_out_DG3 = 0;
def int cut_in_load = 0;
def int cut_out_load = 0;
def int illegal_overload = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw <= battery_Pmax];
    ! * -> LNGDispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > battery_Pmax && PL - Ppv - Pw <= Plngmax];
    ! * -> LNGChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pgmax / 5 <= Plngmax];
    ! * -> LNGDG3Dispatch : if [PL > 0 && Ppv + Pw < PL && SoC > 0.20 && PL - Ppv - Pw > Plngmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax];
    ! * -> LNGDG3ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC <= 0.20 && PL - Ppv - Pw + Pd1max / 10 > Plngmax && PL - Ppv - Pw + Pd1max / 10 <= Plngmax + eng3_Pmax];
    ! * -> AddDG1LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max];
    ! * -> AddDG2LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Plngmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> ExtremeOverloadBatteryLack : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Plngmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> InitialDispatchSelect;

    pseudo state InitialDispatchSelect;

    state RESCoversCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state RESCoversSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state ZeroLoadCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 0;
            cut_out_load = 1;
            illegal_overload = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 0;
            cut_out_load = 1;
            illegal_overload = 0;
        }
    }

    state BatteryAssist {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDispatch {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5;
            battery_discharge_power = 0.0;
            battery_charging_power = Pgmax / 5;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG3Dispatch {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG3ChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10;
            battery_discharge_power = 0.0;
            battery_charging_power = Pd1max / 10;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state AddDG1LastPriority {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state AddDG2LastPriority {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 0;
        }
    }

    state ExtremeOverloadBatteryLack {
        enter {
            requested_generator_power = Plngmax + eng3_Pmax + Pd1max + Pd2max;
            battery_discharge_power = PL - Ppv - Pw - Plngmax - eng3_Pmax - Pd1max - Pd2max;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_load = 1;
            cut_out_load = 0;
            illegal_overload = 1;
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `4` / `3` / `5` |
| token / elapsed | `{'prompt_tokens': 476895, 'completion_tokens': 46668, 'total_tokens': 523563, 'estimated_prompt_tokens': 528457, 'estimated_completion_tokens': 31990, 'estimated_total_tokens': 560447, 'prompt_chars': 2113812, 'completion_chars': 127941, 'n_calls': 12, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `891.898s` |
| full stage table | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794/report.md` §4 |
| run record | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794/pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz` |
| logs | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794/run_logs/stdout.txt`, `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794/checks.json`, `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:f2038a858061b9644334d6ccc5341e2235414617d5779c8634bdc1fb4d64257b` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `91` |
| `langgraph_node_trace_hash` | `sha256:4c76755b683d4b2185c6b7f5f13ede929f42752710a4f3eddf1cd243a5184e3a` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `91` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14661 | 生成初始 DSL 与 grounding seeds | initial len=8904 | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=100, advisory=86, info=0; blocking=99, advisory=86, info=0; blocking=0, advisory=185, info=0; blocking=0, advisory=185, info=0; blocking=28, advisory=206, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=229627 | LLM per-request accept/reject + repair | candidate len=8827,0,10454,8874 | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=144254 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=100, advisory=86, info=0; blocking=99, advisory=86, info=0; blocking=0, advisory=185, info=0; blocking=0, advisory=185, info=0; blocking=28, advisory=206, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=229627 | LLM per-request accept/reject + repair | candidate len=8827,0,10454,8874 | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=100, advisory=86, info=0; blocking=99, advisory=86, info=0; blocking=0, advisory=185, info=0; blocking=0, advisory=185, info=0; blocking=28, advisory=206, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=3, tokens=73728 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=3, tokens=73728 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ⚠️ | ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=100, advisory=86, info=0; blocking=99, advisory=86, info=0; blocking=0, advisory=185, info=0; blocking=0, advisory=185, info=0; blocking=28, advisory=206, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ⚠️ | ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=229627 | LLM per-request accept/reject + repair | candidate len=8827,0,10454,8874 | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=144254 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=100, advisory=86, info=0; blocking=99, advisory=86, info=0; blocking=0, advisory=185, info=0; blocking=0, advisory=185, info=0; blocking=28, advisory=206, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=229627 | LLM per-request accept/reject + repair | candidate len=8827,0,10454,8874 | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=144254 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=100, advisory=86, info=0; blocking=99, advisory=86, info=0; blocking=0, advisory=185, info=0; blocking=0, advisory=185, info=0; blocking=28, advisory=206, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=3, tokens=73728 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SL-7` | 是 | 4 | ✅ | LLM calls=1, tokens=61293 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T17:34:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T17:34:06Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T17:34:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T17:34:06Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T17:36:35Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T17:36:35Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=8904,hash=sha256:99fe6082d065 |
| 7 | `2026-06-05T17:36:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T17:36:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T17:36:35Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:99fe6082d0658600915be6b8f6a84fe180769746e3be3d660af3442a02f12228 |
| 10 | `2026-06-05T17:36:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T17:36:35Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=8904,hash=sha256:99fe6082d065, current_hash=sha256:99fe6082d0658600915be6b8f6a84fe180769746e3be3d660af3442a02f12228 |
| 12 | `2026-06-05T17:36:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T17:36:35Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T17:36:35Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T17:36:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T17:36:35Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T17:36:36Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T17:36:36Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T17:36:36Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 21 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T17:36:36Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=SoC_low_limit", "W_UNWRITTEN_READ_VAR:var_name=battery_Pmax", "W_UNWRITTEN_READ_VAR:var_name=Plngmax", "W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCover...<truncated 18411 chars> | <none> |
| 23 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 26 | `2026-06-05T17:36:36Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=SoC_low_limit", "W_UNWRITTEN_READ_VAR:var_name=battery_Pmax", "W_UNWRITTEN_READ_VAR:var_name=Plngmax", "W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge...<truncated 166777 chars> | current_dsl:len=8904,hash=sha256:99fe6082d065 |
| 27 | `2026-06-05T17:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 28 | `2026-06-05T17:36:36Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T17:36:36Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 12} | <none> |
| 30 | `2026-06-
... <truncated 8158 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 2 | Iter 3 | Iter 5 |
|---|---|---|---|---|
| `default_init_zero_load_charge` | default-init: with PL=0 and SoC below 0.95, the EMS should classify zero load RES into battery charging and cut out ship...<truncated 6 chars> | ❌ | ❌ | ✅ |
| `zero_load_soc_threshold_spare` | explicit-hot-start: at PL=0 and SoC exactly 0.95, RES production should become spare power rather than battery charge. | ✅ | ✅ | ✅ |
| `res_covers_charge_below_soc_threshold` | explicit-hot-start: with positive load covered by RES and SoC below 0.95, demand is served by RES and residual renewable...<truncated 27 chars> | ✅ | ✅ | ✅ |
| `res_covers_spare_at_soc_threshold` | explicit-hot-start: with positive load covered by RES and SoC exactly 0.95, residual renewable power should be reported ...<truncated 9 chars> | ✅ | ✅ | ✅ |
| `battery_assist_at_battery_capacity_boundary` | explicit-hot-start: when RES is short, SoC is suitable, and the deficit exactly equals battery_Pmax, batteries should co...<truncated 38 chars> | ✅ | ✅ | ✅ |
| `lng_dispatch_at_lng_capacity_boundary` | explicit-hot-start: when battery alone is insufficient and the deficit exactly equals LNG capacity, LNG should be cut in...<truncated 21 chars> | ✅ | ✅ | ✅ |
| `lng_charge_margin_low_soc_boundary` | explicit-hot-start: at low SoC exactly 0.20, the LNG-covered branch should add the Pgmax/5 charging margin. | ✅ | ✅ | ✅ |
| `lng_dg3_dispatch_at_eng3_boundary` | explicit-hot-start: when LNG alone is insufficient and the deficit exactly fits LNG plus DG3 capacity, LNG and DG3 shoul...<truncated 25 chars> | ✅ | ✅ | ✅ |
| `lng_dg3_charge_margin_pd1_margin` | explicit-hot-start: in a later low-SoC diesel-generator case, the Pd1max/10 charging margin should be added while using ...<truncated 12 chars> | ✅ | ✅ | ✅ |
| `add_dg1_last_priority_boundary` | explicit-hot-start: when the deficit exceeds LNG plus DG3 but exactly fits after adding DG1, DG1 is cut in and DG2 remai...<truncated 11 chars> | ✅ | ✅ | ✅ |
| `add_dg2_last_priority_boundary` | explicit-hot-start: when the deficit exceeds LNG plus DG3 plus DG1 but exactly fits after adding DG2, both DG1 and DG2 a...<truncated 33 chars> | ✅ | ✅ | ✅ |
| `extreme_overload_all_thermal_and_battery_lack` | explicit-hot-start: for demand exceeding all RES and thermal resources, all thermal units are activated and the remainin...<truncated 69 chars> | ✅ | ✅ | ✅ |
| `forced_reclass_zero_load_charge_from_overload` |  | ✅ | ✅ | ✅ |
| `forced_reclass_lng_dispatch_from_res_spare` |  | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=SoC_low_limit, W_UNWRITTEN_READ_VAR:var_name=battery_Pmax, W_UNWRITTEN_READ_VAR:var_name=Plngmax, W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist, ... +100 | accept=1, reject=11, waiver=11 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=none, local_stage=SD-10, reason=design_target_unresolved | `sha256:e4cf5afd22c71c13ec6bf27c1372b7fbca62216ddb49195ac0b757d4fe3ed1b9` |
| 2 | `1` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=battery_Pmax, W_UNWRITTEN_READ_VAR:var_name=Plngmax, W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.LNGDispatch, ... +99 | accept=0, reject=12, waiver=12 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `2` | ✅ | `SD-6` | default_init_zero_load_charge | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; forced_transition_count_drift | `sha256:9121b16d876b7385b65d3cf1f8060acd9e094046ce82de945e480c492432fa20` |
| 4 | `3` | ✅ | `SD-4` | W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGDispatch, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGDG3Dispatch, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.InitialDispatchSelect:to_path=LNGShipEMS.LNGDG3ChargeMargin, ... +23 | accept=4, reject=8, waiver=8 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:3454c23c9fdabd2846510c8225fe02a330f3f8fec051dee98e1de2f7ebab9fc1` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b2_repair_subgraph_real_runs_clean_7cc8559/pr-e1-path2_lng_ems-default-lg-b2-clean-7cc8559-14fae794/report.md` §7。

</details>
