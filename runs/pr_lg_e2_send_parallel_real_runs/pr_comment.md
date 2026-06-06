## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_lg_e2_send_parallel_real_runs/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | post-accept | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 34811 | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 264232 | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 34307 | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | ❌ | ⚪ 0 | `success` | 325382 | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5/report.md` |

### 可复现性边界

- clean commit 绑定：4/4 run 的 `reproducibility.json` 记录 dirty=false。
- prompt snapshot hash 种类：1；用于确认同一轮 4 例是否共享同一 prompt/context 版本。
- 每个 run 的 `reproducibility.json` 保存 git commit、dirty flag、diff hash、prompt file hash、runner command/config 与 source/paper path。

### LangGraph runtime metadata / checkpoint 口径

- graph_runtime_backend：`langgraph`。
- graph_runtime_status：`enabled`。
- langgraph / checkpoint 版本：langgraph=`1.1.6`；langgraph-checkpoint=`4.0.1`。
- node_edge_schema_version：`pr-langgraph.stage-nodes.v1`；checkpoint_backend=`memory`；serde=`pickle`。
- graph_config_hash：4 种；该字段绑定 registry、planned graph、resolved config、condition hash、iteration/scenario policy 与 checkpoint config，用于区分 run-level graph config。
- node trace count 范围：min=16，max=60；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：4/4 success，rejected=0，budget_exhausted=0，total_tokens=658732。
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
- `path2_lng_ems`：失败/成功类别=success，最大 observed iteration_count=3。
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
| token / elapsed | `{'prompt_tokens': 27084, 'completion_tokens': 7727, 'total_tokens': 34811, 'estimated_prompt_tokens': 26409, 'estimated_completion_tokens': 4403, 'estimated_total_tokens': 30812, 'prompt_chars': 105634, 'completion_chars': 17608, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `150.029s` |
| full stage table | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c/report.md` §4 |
| run record | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c/pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz` |
| logs | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c/run_logs/stdout.txt`, `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c/checks.json`, `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.1.6` |
| `langgraph_checkpoint_version` | `4.0.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:9880cf68a7922a14e156ed0212a1c6f5757e5ae4a250e08d5f759a9874ae7a11` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9021 | 生成初始 DSL 与 grounding seeds | initial len=634 | [`record`](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13646 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=12144 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T08:05:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T08:05:29Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T08:05:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T08:05:29Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T08:06:20Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T08:06:20Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 7 | `2026-06-06T08:06:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T08:06:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T08:06:20Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726 |
| 10 | `2026-06-06T08:06:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T08:06:20Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=634,hash=sha256:5a3dc31a6a97, current_hash=sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726 |
| 12 | `2026-06-06T08:06:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T08:06:20Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T08:06:20Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T08:06:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T08:06:20Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T08:06:20Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T08:06:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T08:06:20Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T08:06:20Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-06T08:06:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T08:06:20Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-06T08:07:26Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-06T08:07:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T08:07:26Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-06T08:07:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-06T08:07:26Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-06T08:07:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-06T08:07:26Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-06T08:07:26Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 31 | `2026-06-06T08:07:26Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 32 | `2026-06-06T08:07:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 33 | `2026-06-06T08:07:26Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 34 | `2026-06-06T08:07:59Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-06T08:07:59Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-06T08:07:59Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 37 | `2026-06-06T08:07:59Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 38 | `2026-06-06T08:07:59Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 39 | `2026-06-06T08:07:59Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-06T08:07:59Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 41 | `2026-06-06T08:07:59Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-06T08:07:59Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 43 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 44 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 45 | `` | `<control>` | `-` | `lg_e3_toolnode_wrapper_trace` | {} | <none> |
| 46 | `` | `<control>` | `-` | `lg_e2_send_parallel_trace` | {} | <none> |
| 47 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |
| 48 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 49 | `` | `<control>` | `-` | `pr_e1_quality_boundary` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_enters_increase_outputs` | default-init verifies the initial transition dispatches to increase and sets inlet/return/pump outputs for pressure incr...<truncated 5 chars> | ✅ |
| `increase_to_hold_at_positive_boundary` | explicit-hot-start probes the inclusive slp <= 0.01 guard from increase to hold and then verifies hold does not leave at...<truncated 14 chars> | ✅ |
| `hold_to_increase_above_positive_boundary` | explicit-hot-start probes the strict slp > 0.01 guard from hold to increase and confirms increase does not transition to...<truncated 34 chars> | ✅ |
| `hold_to_decrease_below_negative_boundary` | explicit-hot-start probes the strict slp < -0.01 guard from hold to decrease and confirms decrease does not transition t...<truncated 37 chars> | ✅ |
| `decrease_to_hold_at_negative_boundary` | explicit-hot-start probes the inclusive slp >= -0.01 guard from decrease to hold and then verifies hold does not enter d...<truncated 25 chars> | ✅ |
| `hold_deadband_zero_stays_neutral` | explicit-hot-start verifies the deadband case slp=0.0 keeps the supervisor in hold with both valves and pump neutralized...<truncated 1 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2109, 'completion_chars': 7042, 'completion_tokens': 2628, 'elapsed_seconds': 50.538315093843266, 'estimated_completion_tokens': 1761, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 8254, 'first_chunk_seconds': 11.626630547922105, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9021}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1463, 'completion_chars': 5500, 'completion_tokens': 3458, 'elapsed_seconds': 65.68616673885845, 'estimated_completion_tokens': 1375, 'estimated_prompt_tokens': 9989, 'estimated_total_tokens': 11364, 'first_chunk_seconds': 39.62607252993621, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39954, 'prompt_tokens': 10188, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13646}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1122, 'completion_chars': 5066, 'completion_tokens': 1641, 'elapsed_seconds': 32.2103210540954, 'estimated_completion_tokens': 1267, 'estimated_prompt_tokens': 9927, 'estimated_total_tokens': 11194, 'first_chunk_seconds': 11.792378282174468, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39708, 'prompt_tokens': 10503, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12144}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_abs-default-lg-e2-dotenv-clean2-f153405c/report.md` §7。

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
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float target_blood_pressure = 100.0;
def float caregiver_target_blood_pressure = 100.0;
def float infusion_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int pump_complication = 0;
def int alarm_display = 0;
def int alarm_sound = 0;
def int control_released = 1;
def int log_record_count = 0;

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
                control_released = 1;
                if [pump_complication == 0] {
                    alarm_display = 0;
                    alarm_sound = 0;
                } else {
                    alarm_display = 1;
                    alarm_sound = 1;
                }
            }
            during {
                pump_speed = built_in_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                control_released = 1;
            }
            during {
                target_blood_pressure = caregiver_target_blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                if [pump_complication == 0] {
                    CA_mode = 1;
                    control_released = 0;
                    alarm_display = 0;
                    alarm_sound = 0;
                } else {
                    CA_mode = 0;
                    control_released = 1;
                    alarm_display = 1;
                    alarm_sound = 1;
                }
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                control_released = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [pump_complication == 0] {
                    infusion_rate = target_blood_pressure - sensor_buffer_bp;
                    control_voltage = infusion_rate;
                    pump_speed = control_voltage;
                    log_record_count = log_record_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                alarm_display = 1;
                alarm_sound = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> PumpFault : if [pump_complication > 0];
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> PumpFault : if [pump_complication > 0];
        AutocontrolInit -> AutocontrolNormal :: InitComplete;
        AutocontrolNormal -> PumpFault : if [pump_complication > 0];
        PumpFault -> Manual :: FaultRemoved effect {
            pump_complication = 0;
            alarm_display = 0;
            alarm_sound = 0;
        };
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `3` / `2` / `2` / `5` |
| token / elapsed | `{'prompt_tokens': 231241, 'completion_tokens': 32991, 'total_tokens': 264232, 'estimated_prompt_tokens': 243455, 'estimated_completion_tokens': 25440, 'estimated_total_tokens': 268895, 'prompt_chars': 973804, 'completion_chars': 101739, 'n_calls': 11, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `647.519s` |
| full stage table | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd/report.md` §4 |
| run record | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd/pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz` |
| logs | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd/run_logs/stdout.txt`, `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd/checks.json`, `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.1.6` |
| `langgraph_checkpoint_version` | `4.0.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:85759c160e384ecfc9d360a5d66c68038e93757600633cf92a0b46e61d2ba8b2` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `60` |
| `langgraph_node_trace_hash` | `sha256:cddc8e87fe685e25138f3324751edc492edd20944e8708f38dfa66f577694f53` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `60` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12741 | 生成初始 DSL 与 grounding seeds | initial len=2820 | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=20, info=0; blocking=0, advisory=20, info=0; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=65449 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=68846 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=61855 | LLM per-request accept/reject + repair | candidate len=2993,3379 | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=55341 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=20, info=0; blocking=0, advisory=20, info=0; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=65449 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=68846 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=61855 | LLM per-request accept/reject + repair | candidate len=2993,3379 | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=55341 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=20, info=0; blocking=0, advisory=20, info=0; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=65449 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=68846 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T08:05:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T08:05:29Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T08:05:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T08:05:29Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T08:07:39Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T08:07:39Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2820,hash=sha256:f8fc7fc18409 |
| 7 | `2026-06-06T08:07:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T08:07:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T08:07:39Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:f8fc7fc18409497e332adb20735d5529f3adee54c81966345c7e22c1f4f258d9 |
| 10 | `2026-06-06T08:07:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T08:07:39Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2820,hash=sha256:f8fc7fc18409, current_hash=sha256:f8fc7fc18409497e332adb20735d5529f3adee54c81966345c7e22c1f4f258d9 |
| 12 | `2026-06-06T08:07:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T08:07:39Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T08:07:39Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T08:07:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T08:07:39Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T08:07:39Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T08:07:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T08:07:40Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T08:07:40Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-06T08:07:40Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T08:07:40Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-06T08:09:07Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-06T08:09:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T08:09:07Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-06T08:09:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-06T08:09:07Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-06T08:09:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-06T08:09:07Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-06T08:09:08Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 31 | `2026-06-06T08:09:08Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 32 | `2026-06-06T08:09:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 33 | `2026-06-06T08:09:08Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 34 | `2026-06-06T08:10:01Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-06T08:10:01Z` | `SL-7` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-06T08:10:01Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 37 | `2026-06-06T08:10:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 38 | `2026-06-06T08:10:01Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["`! * -> Manual` transitions are available for backManual and TerminateAC from any substate, including PumpFault.", "`Manual.enter` unconditionally sets `alarm_display = 0` and `alarm_sound = 0`.", "`pump_complication` is only cleared by the explicit `FaultRemoved` effect, so a forced tra...<truncated 514 chars> | <none> |
| 39 | `2026-06-06T08:10:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-06T08:10:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-06T08:10:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-06T08:10:01Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["`! * -> Manual` transitions are available for backManual and TerminateAC from any substate, including PumpFault.", "`Manual.enter` unconditionally sets `alarm_display = 0` and `alarm_sound = 0`.", "`pump_complication` is only cleared by the explicit `FaultRemoved` effect, so a forced transition...<truncated 507 chars> | current_dsl:len=2820,hash=sha256:f8fc7fc18409 |
| 43 | `2026-06-06T08:10:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-06T08:10:01Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 45 | `2026-06-06T08:10:01Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 46 | `2026-06-06T08:10:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 47 | `2026-06-06T08:10:01Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2820,hash=sha256:f8fc7fc18409 |
| 48 | `2026-06-06T08:10:33Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 49 | `2026-06-06T08:10:33Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2993,hash=sha256:8e7a16c271d7 |
| 50 | `2026-06-06T08:10:33Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 51 | `2026-06-06T08:10:34Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": true, "status": "StageStatus.OK"} | <none> |
| 52 | `2026-06-06T08:10:34Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:8e7a16c271d73f0bcf56927fc93c4ce5920460dc3fe3058174c9c68c988b67e8 |
| 53 | `2026-06-06T08:10:44Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 54 | `2026-06-06T08:10:44Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 55 | `2026-06-06T08:10:44Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 56 | `2026-06-06T08:10:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 57 | `2026-06-06T08:10:44Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2993,hash=sha256:8e7a16c271d7 |
| 58 | `2026-06-06T08:10:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 59 | `2026-06-06T08:10:44Z` |
... <truncated 2675 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| `default_init_manual_then_ask_startac` | default-init dispatches to Manual, then caregiver InitiateAC enters Ask_StartAC where the caregiver setpoint is copied t...<truncated 24 chars> | ✅ | ✅ | ✅ |
| `start_ac_then_init_complete_normal_control` | explicit-hot-start in Ask_StartAC probes StartAC to AutocontrolInit, then InitComplete to AutocontrolNormal with control...<truncated 38 chars> | ✅ | ✅ | ✅ |
| `normal_autocontrol_no_fault_boundary` | explicit-hot-start in AutocontrolNormal with pump_complication at the no-fault boundary 0 should not enter PumpFault and...<truncated 32 chars> | ✅ | ✅ | ✅ |
| `normal_autocontrol_fault_boundary_and_removed` | explicit-hot-start in AutocontrolNormal with pump_complication positive should enter PumpFault, alarm/release control, t...<truncated 35 chars> | ✅ | ✅ | ✅ |
| `manual_mode_uses_switch_and_default_flow` | explicit-hot-start in Manual verifies manual operation uses the built-in switch for pump speed and default flow rate for...<truncated 10 chars> | ✅ | ✅ | ✅ |
| `forced_ca_and_cb_back_manual` | explicit-hot-start in AutocontrolInit verifies CA_backManual forces Manual, then CB_backManual also forces Manual from A...<truncated 11 chars> | ✅ | ✅ | ✅ |
| `forced_cp_cc_and_terminate_back_manual` | explicit-hot-start in PumpFault verifies CP_backManual, CC_backManual, and TerminateAC each force the shared Manual reco...<truncated 53 chars> | ✅ | ✅ | ✅ |
| `forced_back_manual_from_active_fault_preserves_alarms` | explicit-hot-start in PumpFault with an unresolved pump complication verifies forced Manual recovery releases software c...<truncated 65 chars> | ⚪ | ✅ | ✅ |
| `ask_startac_fault_wrong_target_probe` | explicit-hot-start in Ask_StartAC with an existing pump complication verifies the safety guard targets PumpFault rather ...<truncated 26 chars> | ⚪ | ⚪ | ✅ |
| `autocontrol_init_fault_wrong_target_probe` | explicit-hot-start in AutocontrolInit with a pump complication verifies the safety guard targets PumpFault before normal...<truncated 20 chars> | ⚪ | ⚪ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:8e7a16c271d73f0bcf56927fc93c4ce5920460dc3fe3058174c9c68c988b67e8` |
| 2 | `1` | ✅ | `SL-7` | 0, 1, 2 | accept=3, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:8e233622c2e3e55e2f1f038be5b3f9660f43a30a451fe052399864155456cb81` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd/report.md` §7。

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
| SC-11 post-accept validation | `⚪ 0` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 27049, 'completion_tokens': 7258, 'total_tokens': 34307, 'estimated_prompt_tokens': 26372, 'estimated_completion_tokens': 5820, 'estimated_total_tokens': 32192, 'prompt_chars': 105482, 'completion_chars': 23275, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `142.694s` |
| full stage table | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26/report.md` §4 |
| run record | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26/pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz` |
| logs | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26/run_logs/stdout.txt`, `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26/checks.json`, `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.1.6` |
| `langgraph_checkpoint_version` | `4.0.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:7a714237a71102239863d5f82017eb1d6ab94bb76f10d49663ed12924d524b88` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9408 | 生成初始 DSL 与 grounding seeds | initial len=669 | [`record`](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=14072 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10827 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T08:05:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T08:05:29Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T08:05:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T08:05:29Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T08:06:28Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T08:06:28Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=669,hash=sha256:f01d793ff735 |
| 7 | `2026-06-06T08:06:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T08:06:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T08:06:28Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:f01d793ff73542443089e3b4ce8b98c438d4cd4be9a79525664c83dccc1e4c1c |
| 10 | `2026-06-06T08:06:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T08:06:28Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=669,hash=sha256:f01d793ff735, current_hash=sha256:f01d793ff73542443089e3b4ce8b98c438d4cd4be9a79525664c83dccc1e4c1c |
| 12 | `2026-06-06T08:06:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T08:06:28Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T08:06:28Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T08:06:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T08:06:28Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T08:06:28Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T08:06:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T08:06:28Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T08:06:28Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-06T08:06:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T08:06:28Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-06T08:07:18Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-06T08:07:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T08:07:18Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-06T08:07:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-06T08:07:18Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-06T08:07:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-06T08:07:18Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-06T08:07:18Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 31 | `2026-06-06T08:07:18Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 32 | `2026-06-06T08:07:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 33 | `2026-06-06T08:07:18Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 34 | `2026-06-06T08:07:51Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-06T08:07:51Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-06T08:07:51Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 37 | `2026-06-06T08:07:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 38 | `2026-06-06T08:07:51Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 39 | `2026-06-06T08:07:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-06T08:07:51Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=669,hash=sha256:f01d793ff735 |
| 41 | `2026-06-06T08:07:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-06T08:07:51Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=669,hash=sha256:f01d793ff735 |
| 43 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 44 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 45 | `` | `<control>` | `-` | `lg_e3_toolnode_wrapper_trace` | {} | <none> |
| 46 | `` | `<control>` | `-` | `lg_e2_send_parallel_trace` | {} | <none> |
| 47 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |
| 48 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 49 | `` | `<control>` | `-` | `pr_e1_quality_boundary` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_then_f2_f3_up_sequence` | default-init probe: dispatches to F1 stop, then F1 PS2 drives up to MU2, S2 stops at F2, F2 PS3 drives up to MU3, and S3...<truncated 13 chars> | ✅ |
| `f1_direct_request_to_f3` | explicit-hot-start probe: from F1, PS3 must target MU3 with upward hbrg, then S3 must stop at F3. | ✅ |
| `f2_request_down_to_f1` | explicit-hot-start probe: from F2, PS1 must target MD1 with downward hbrg, then S1 must stop at F1. | ✅ |
| `f3_request_down_to_f1` | explicit-hot-start probe: from F3, PS1 must target MD1 with downward hbrg, then S1 must stop at F1. | ✅ |
| `f3_request_down_to_f2` | explicit-hot-start probe: from F3, PS2 must target MD2 with downward hbrg, then S2 must stop at F2. | ✅ |
| `reset_from_upward_motion_forces_f1` | explicit-hot-start probe: reset from an upward motion state must force F1 and restore stop hbrg regardless of outstandin...<truncated 10 chars> | ✅ |
| `reset_from_downward_motion_forces_f1` | explicit-hot-start probe: reset from a downward motion state must force F1 and restore stop hbrg regardless of outstandi...<truncated 11 chars> | ✅ |
| `no_request_or_no_arrival_no_phantom_transition` | explicit-hot-start probe: without floor requests or arrival sensors, the controller should stay in its current leaf and ...<truncated 41 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2603, 'completion_chars': 9590, 'completion_tokens': 2970, 'elapsed_seconds': 58.4412410359364, 'estimated_completion_tokens': 2398, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 8921, 'first_chunk_seconds': 11.722960454877466, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9408}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2050, 'completion_chars': 8007, 'completion_tokens': 2569, 'elapsed_seconds': 49.81934745586477, 'estimated_completion_tokens': 2002, 'estimated_prompt_tokens': 11246, 'estimated_total_tokens': 13248, 'first_chunk_seconds': 12.477214975981042, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 44984, 'prompt_tokens': 11503, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14072}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1286, 'completion_chars': 5678, 'completion_tokens': 1719, 'elapsed_seconds': 32.7276700171642, 'estimated_completion_tokens': 1420, 'estimated_prompt_tokens': 8603, 'estimated_total_tokens': 10023, 'first_chunk_seconds': 9.896435018163174, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 34409, 'prompt_tokens': 9108, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10827}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path1_elevator-default-lg-e2-dotenv-clean2-40069e26/report.md` §7。

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
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbdismax = 0.0;
def float Pgmax = 0.0;
def float Pg_req = 0.0;
def float Pbd_req = 0.0;
def float Pbc_req = 0.0;
def float spare_power = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
    ! * -> ResCoversCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> ResCoversSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryOnly : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbdismax];
    ! * -> BatteryLng : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbdismax && PL - Ppv - Pw <= Pbdismax + eng3_Pmax];
    ! * -> BatteryLngDg1 : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbdismax + eng3_Pmax && PL - Ppv - Pw <= Pbdismax + eng3_Pmax + Pd1max];
    ! * -> AllThermalNormalSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbdismax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pbdismax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> LngChargeLowSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= eng3_Pmax];
    ! * -> LngDg1ChargeLowSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5.0 > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= eng3_Pmax + Pd1max];
    ! * -> LngDg1Dg2ChargeLowSoc : if [PL > 0.0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10.0 > eng3_Pmax + Pd1max && PL - Ppv - Pw + Pd1max / 10.0 <= eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadCompletionIllegal : if [PL > 0.0 && Ppv + Pw < PL && ((SoC >= 0.2 && PL - Ppv - Pw > Pbdismax + eng3_Pmax + Pd1max + Pd2max) || (SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10.0 > eng3_Pmax + Pd1max + Pd2max))];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = Ppv + Pw;
            spare_power = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state ZeroLoadSpare {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = 0.0;
            spare_power = Ppv + Pw;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state ResCoversCharge {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = Ppv + Pw - PL;
            spare_power = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state ResCoversSpare {
        during {
            Pg_req = 0.0;
            Pbd_req = 0.0;
            Pbc_req = 0.0;
            spare_power = Ppv + Pw - PL;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state BatteryOnly {
        during {
            Pg_req = 0.0;
            Pbd_req = PL - Ppv - Pw;
            Pbc_req = 0.0;
            spare_power = 0.0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state BatteryLng {
        during {
            Pg_req = PL - Ppv - Pw - Pbdismax;
            Pbd_req = Pbdismax;
            Pbc_req = 0.0;
            spare_power = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state BatteryLngDg1 {
        during {
            Pg_req = PL - Ppv - Pw - Pbdismax;
            Pbd_req = Pbdismax;
            Pbc_req = 0.0;
            spare_power = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state AllThermalNormalSoc {
        during {
            Pg_req = PL - Ppv - Pw - Pbdismax;
            Pbd_req = Pbdismax;
            Pbc_req = 0.0;
            spare_power = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LngChargeLowSoc {
        during {
            Pg_req = PL - Ppv - Pw + Pgmax / 5.0;
            Pbd_req = 0.0;
            Pbc_req = Pgmax / 5.0;
            spare_power = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LngDg1ChargeLowSoc {
        during {
            Pg_req = PL - Ppv - Pw + Pd1max / 10.0;
            Pbd_req = 0.0;
            Pbc_req = Pd1max / 10.0;
            spare_power = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state LngDg1Dg2ChargeLowSoc {
        during {
            Pg_req = PL - Ppv - Pw + Pd1max / 10.0;
            Pbd_req = 0.0;
            Pbc_req = Pd1max / 10.0;
            spare_power = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
        }
    }

    state OverloadCompletionIllegal {
        during {
            Pg_req = eng3_Pmax + Pd1max + Pd2max;
            Pbd_req = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbc_req = 0.0;
            spare_power = 0.0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `3` / `2` / `2` / `2` |
| token / elapsed | `{'prompt_tokens': 291841, 'completion_tokens': 33541, 'total_tokens': 325382, 'estimated_prompt_tokens': 300427, 'estimated_completion_tokens': 23394, 'estimated_total_tokens': 323821, 'prompt_chars': 1201695, 'completion_chars': 93561, 'n_calls': 8, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `664.304s` |
| full stage table | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5/report.md` §4 |
| run record | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5/pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz` |
| logs | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5/run_logs/stdout.txt`, `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5/checks.json`, `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.1.6` |
| `langgraph_checkpoint_version` | `4.0.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:c30f60349ac9c3b6f4a6c3dcceb3696e6f553ab11d7c93de8ac2ed969306ce7f` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `50` |
| `langgraph_node_trace_hash` | `sha256:c95b8b7d8f7ca4463610743df96a0426603274ad00e5a67b6b2c5eaa14a209bc` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `50` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14747 | 生成初始 DSL 与 grounding seeds | initial len=7711 | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=74, advisory=228, info=0; blocking=74, advisory=228, info=0; blocking=0, advisory=302, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=106200 | LLM per-request accept/reject + repair | candidate len=7711,7711 | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=85070 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=74, advisory=228, info=0; blocking=74, advisory=228, info=0; blocking=0, advisory=302, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=106200 | LLM per-request accept/reject + repair | candidate len=7711,7711 | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=85070 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=74, advisory=228, info=0; blocking=74, advisory=228, info=0; blocking=0, advisory=302, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=2, tokens=48413 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=2, tokens=48413 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=1, tokens=70952 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T08:05:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T08:05:29Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T08:05:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T08:05:29Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T08:08:05Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T08:08:05Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=7711,hash=sha256:a94551f06242 |
| 7 | `2026-06-06T08:08:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T08:08:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T08:08:05Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 10 | `2026-06-06T08:08:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T08:08:05Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=7711,hash=sha256:a94551f06242, current_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 12 | `2026-06-06T08:08:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T08:08:05Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T08:08:05Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T08:08:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T08:08:05Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T08:08:05Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T08:08:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T08:08:05Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T08:08:06Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 21 | `2026-06-06T08:08:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T08:08:06Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_UNWRITTEN_READ_VAR:var_name=Pbdismax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad...<truncated 19863 chars> | <none> |
| 23 | `2026-06-06T08:08:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-06T08:08:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T08:08:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 26 | `2026-06-06T08:08:06Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_UNWRITTEN_READ_VAR:var_name=Pbdismax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:...<truncated 248320 chars> | current_dsl:len=7711,hash=sha256:a94551f06242 |
| 27 | `2026-06-06T08:08:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 28 | `2026-06-06T08:08:06Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-06T08:08:06Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 12} | <none> |
| 30 | `2026-06-06T08:08:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-06T08:08:06Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=7711,hash=sha256:a94551f06242 |
| 32 | `2026-06-06T08:09:44Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-06T08:09:44Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-004a2744db", "fixreq-0-sd4-1-ac19caf402", "fixreq-0-sd4-2-a85904e5ae", "fixreq-0-sd4-3-63111cf4c5", "fixreq-0-sd4-4-1c37eb99a0", "fixreq-0-sd4-5-684ca59bf4", "fixreq-0-sd4-6-53b0ac9354", "fixreq-0-sd4-7-7996b67982", "fixreq-0-sd4-8-eb7c8ae12b", "fixreq-0-sd4-9-3c1a198645", "fixreq-0-sd4-10-7e80c093d6", "fixreq-0-sd4-11-2b935a4955"], "jump": "SL-10", "ok": true, "rejected_requ...<truncated 13 chars> | candidate_dsl:len=7711,hash=sha256:a94551f06242 |
| 34 | `2026-06-06T08:09:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-06T08:09:45Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 36 | `2026-06-06T08:09:45Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 37 | `2026-06-06T08:10:04Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 38 | `2026-06-06T08:10:04Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 39 | `2026-06-06T08:10:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-06T08:10:04Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=7711,hash=sha256:a94551f06242 |
| 41 | `2026-06-06T08:10:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-06T08:10:04Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 43 | `2026-06-06T08:10:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-06T08:10:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-06T08:10:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-06T08:10:05Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 47 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-06T08:10:05Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=7711,hash=sha256:a94551f06242, current_hash=sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a |
| 49 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 50 | `2026-06-06T08:10:05Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 51 | `2026-06-06T08:10:05Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 52 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 53 | `2026-06-06T08:10:05Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 54 | `2026-06-06T08:10:05Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 55 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 56 | `2026-06-06T08:10:05Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 57 | `2026-06-06T08:10:05Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 58 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 59 | `2026-06-06T08:10:05Z` | `<control>` | `1` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_UNWRITTEN_READ_VAR:var_name=Pbdismax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoad...<truncated 19863 chars> | <none> |
| 60 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 61 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 62 | `2026-06-06T08:10:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 63 | `2026-06-06T08:10:05Z` | `SD-8` | `1` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=Pd2max", "W_UNWRITTEN_READ_VAR:var_name=Pbdismax", "W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly", "
... <truncated 2948 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 3 |
|---|---|---|
| `default_init_zero_load_charge` | default-init dispatches to the zero-load charging mode when PL is zero and renewable production is available below the 0...<truncated 18 chars> | ✅ |
| `zero_load_soc_boundary_spare` | explicit-hot-start probes the SoC=0.95 boundary for PL=0, where renewable production should become spare power rather th...<truncated 20 chars> | ✅ |
| `res_covers_charge_below_soc_boundary` | explicit-hot-start probes RES covering positive load with SoC just below 0.95, expecting residual renewable power to cha...<truncated 16 chars> | ✅ |
| `res_covers_soc_boundary_spare` | explicit-hot-start probes RES covering positive load at SoC=0.95, expecting residual renewable power to be reported as s...<truncated 5 chars> | ✅ |
| `battery_only_soc_and_capacity_boundary` | explicit-hot-start probes suitable SoC at exactly 0.2 and deficit exactly equal to battery discharge capacity, expecting...<truncated 23 chars> | ✅ |
| `battery_lng_capacity_boundary` | explicit-hot-start probes deficit above battery capacity but exactly covered by battery plus LNG, expecting LNG cut-in a...<truncated 20 chars> | ✅ |
| `battery_lng_dg1_capacity_boundary` | explicit-hot-start probes deficit above battery plus LNG but exactly covered after DG1, expecting DG1 cut-in while DG2 r...<truncated 11 chars> | ✅ |
| `all_thermal_normal_soc_capacity_boundary` | explicit-hot-start probes normal-SoC deficit above battery plus LNG plus DG1 but exactly covered once DG2 is added. | ✅ |
| `low_soc_lng_charge_margin` | explicit-hot-start probes low SoC below 0.2 where LNG can cover load plus the Pgmax/5 charging margin. | ✅ |
| `low_soc_lng_dg1_pd1_margin` | explicit-hot-start probes low SoC where LNG alone cannot cover the charging margin and DG1 is added using the Pd1max/10 ...<truncated 7 chars> | ✅ |
| `low_soc_lng_dg1_dg2_pd1_margin` | explicit-hot-start probes low SoC where DG2 is last-priority and needed to cover the Pd1max/10 charging-margin branch. | ✅ |
| `overload_illegal_all_thermal_and_battery_lack` | explicit-hot-start probes the admitted illegal overload-completion branch: extreme demand exceeds RES and thermal resour...<truncated 81 chars> | ✅ |
| `forced_zero_load_charge_from_thermal_leaf` | explicit-hot-start targets the wildcard forced reclassification rule: from an unrelated thermal leaf, PL=0 with RES and ...<truncated 76 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbdismax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLngDg1, ... +74 | accept=12, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=none, local_stage=SD-10, reason=design_target_unresolved | `sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a` |
| 2 | `1` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbdismax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryOnly, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLng, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryLngDg1, ... +74 | accept=12, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:a94551f062423d91b55b99075201100b6caf098b41ba33f7779df2d3ca5a111a` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_e2_send_parallel_real_runs/pr-e1-path2_lng_ems-default-lg-e2-dotenv-clean2-945dc6e5/report.md` §7。

</details>
