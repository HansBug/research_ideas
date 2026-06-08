## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/lg_m1_g_four_after_signature_gate_20260608_052552/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | post-accept | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 35264 | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 269773 | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 34256 | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | ❌ | ✅ 1/1; ❌ 0 | `success` | 862820 | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/report.md` |

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
- node trace count 范围：min=16，max=135；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：4/4 success，rejected=0，budget_exhausted=0，total_tokens=1202113。
  - SC-11 post-accept validation：triggered=1/4 run-level attempts，success=1，failure=0。
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
| token / elapsed | `{'prompt_tokens': 27272, 'completion_tokens': 7992, 'total_tokens': 35264, 'estimated_prompt_tokens': 26567, 'estimated_completion_tokens': 5073, 'estimated_total_tokens': 31640, 'prompt_chars': 106264, 'completion_chars': 20292, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `160.364s` |
| full stage table | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970/report.md` §4 |
| run record | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970/pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz` |
| logs | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970/run_logs/stdout.txt`, `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970/run_logs/stderr.txt` |
| checks / repro | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970/checks.json`, `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:3fb6cbe79a31b9e5a6087909951a4ee4f9c8e5d2bac441adbf5772bcd4e1c16b` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9096 | 生成初始 DSL 与 grounding seeds | initial len=634 | [`record`](./pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13440 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=12728 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-07T21:25:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-07T21:25:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-07T21:25:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-07T21:25:53Z` | `SL-1` | `-` | `lg_d2_envelope_enter` | {} | <none> |
| 5 | `2026-06-07T21:25:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 6 | `2026-06-07T21:26:49Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 7 | `2026-06-07T21:26:49Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 8 | `2026-06-07T21:26:49Z` | `SL-1` | `-` | `lg_d2_envelope_exit` | {} | <none> |
| 9 | `2026-06-07T21:26:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 10 | `2026-06-07T21:26:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-07T21:26:49Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726 |
| 12 | `2026-06-07T21:26:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-07T21:26:49Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=634,hash=sha256:5a3dc31a6a97, current_hash=sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726 |
| 14 | `2026-06-07T21:26:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 15 | `2026-06-07T21:26:49Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 16 | `2026-06-07T21:26:49Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-07T21:26:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 18 | `2026-06-07T21:26:49Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 19 | `2026-06-07T21:26:49Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-07T21:26:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 21 | `2026-06-07T21:26:49Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 22 | `2026-06-07T21:26:49Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-07T21:26:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-07T21:26:49Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 25 | `2026-06-07T21:26:49Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 26 | `2026-06-07T21:27:50Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 27 | `2026-06-07T21:27:50Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 28 | `2026-06-07T21:27:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-07T21:27:50Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 30 | `2026-06-07T21:27:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-07T21:27:50Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 32 | `2026-06-07T21:27:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 33 | `2026-06-07T21:27:50Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 34 | `2026-06-07T21:27:50Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 35 | `2026-06-07T21:27:50Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-07T21:27:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-07T21:27:50Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 38 | `2026-06-07T21:27:50Z` | `SL-7` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 39 | `2026-06-07T21:28:33Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 40 | `2026-06-07T21:28:33Z` | `SL-7` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 41 | `2026-06-07T21:28:33Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-07T21:28:33Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 43 | `2026-06-07T21:28:33Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-07T21:28:33Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 45 | `2026-06-07T21:28:33Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-07T21:28:33Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 47 | `2026-06-07T21:28:33Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-07T21:28:33Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 49 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 50 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 51 | `` | `<control>` | `-` | `lg_e3_toolnode_wrapper_trace` | {} | <none> |
| 52 | `` | `<control>` | `-` | `lg_e2_send_parallel_trace` | {} | <none> |
| 53 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |
| 54 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 55 | `` | `<control>` | `-` | `pr_e1_quality_boundary` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_increase_then_hold_at_boundary` | default-init: dispatches to increase with inlet valve active, then slp=0.01 boundary triggers increase->hold with neutra...<truncated 14 chars> | ✅ |
| `increase_no_fire_above_positive_boundary` | explicit-hot-start: increase must not transition to hold when slp is just above 0.01. | ✅ |
| `hold_no_fire_at_positive_boundary` | explicit-hot-start: hold must not transition to increase at slp=0.01 because hold->increase is strict slp > 0.01. | ✅ |
| `hold_to_increase_above_positive_boundary` | explicit-hot-start: hold transitions to increase when slp is just above 0.01 and increase sets k1=1, k2=0, n=0. | ✅ |
| `hold_no_fire_at_negative_boundary` | explicit-hot-start: hold must not transition to decrease at slp=-0.01 because hold->decrease is strict slp < -0.01. | ✅ |
| `hold_to_decrease_below_negative_boundary` | explicit-hot-start: hold transitions to decrease when slp is just below -0.01 and decrease commands pressure release. | ✅ |
| `decrease_to_hold_at_negative_boundary` | explicit-hot-start: decrease transitions to hold at slp=-0.01 because decrease->hold is slp >= -0.01. | ✅ |
| `decrease_no_fire_below_negative_boundary` | explicit-hot-start: decrease must stay in pressure-release mode when slp is still below -0.01. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2177, 'completion_chars': 7308, 'completion_tokens': 2699, 'elapsed_seconds': 55.37477531400509, 'estimated_completion_tokens': 1827, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 8320, 'first_chunk_seconds': 17.80534112796886, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6397, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9096}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1607, 'completion_chars': 5844, 'completion_tokens': 3165, 'elapsed_seconds': 60.85670464200666, 'estimated_completion_tokens': 1461, 'estimated_prompt_tokens': 10074, 'estimated_total_tokens': 11535, 'first_chunk_seconds': 31.492235056997743, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 40295, 'prompt_tokens': 10275, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13440}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1606, 'completion_chars': 7140, 'completion_tokens': 2128, 'elapsed_seconds': 43.09498048899695, 'estimated_completion_tokens': 1785, 'estimated_prompt_tokens': 10000, 'estimated_total_tokens': 11785, 'first_chunk_seconds': 14.033392486977391, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39997, 'prompt_tokens': 10600, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12728}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_abs-default-lg_m1_g_signature_gate_20f104e8-43fe4970/report.md` §7。

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
def int patient_bp = 120;
def int shared_buffer_bp = 120;
def int target_bp = 120;
def int requested_target_bp = 120;
def int flow_rate = 0;
def int default_flow_rate = 1;
def int built_in_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int display_error = 0;
def int sound_error = 0;
def int control_released = 1;
def int log_count = 0;

state CARA_Mode_Control_Algorithm {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    >> during before { shared_buffer_bp = patient_bp; }

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault > 0] {
                alarm_signal = 1;
                display_error = 1;
                sound_error = 1;
            } else {
                alarm_signal = 0;
                display_error = 0;
                sound_error = 0;
            }
        }
        during {
            if [pump_fault == 0] {
                pump_speed = built_in_switch_speed;
                flow_rate = default_flow_rate;
            } else {
                alarm_signal = 1;
                display_error = 1;
                sound_error = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }
    }

    state Ask_StartAC;

    state AutocontrolInit {
        enter {
            CA_mode = 1;
            control_released = 0;
            alarm_signal = 0;
            display_error = 0;
            sound_error = 0;
        }
    }

    state AutocontrolNormal {
        during {
            if [pump_fault == 0] {
                if [patient_bp > target_bp] {
                    flow_rate = 1;
                } else if [patient_bp == target_bp] {
                    flow_rate = 3;
                } else {
                    flow_rate = 5;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_count = log_count + 1;
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            display_error = 1;
            sound_error = 1;
            control_released = 1;
            CA_mode = 0;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    AutocontrolInit -> PumpFault : if [pump_fault > 0];
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    AutocontrolNormal -> Manual :: TerminateAC;
    Ask_StartAC -> Manual :: TerminateAC;
    PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `3` / `2` / `2` / `5` |
| token / elapsed | `{'prompt_tokens': 240064, 'completion_tokens': 29709, 'total_tokens': 269773, 'estimated_prompt_tokens': 255105, 'estimated_completion_tokens': 23556, 'estimated_total_tokens': 278661, 'prompt_chars': 1020404, 'completion_chars': 94213, 'n_calls': 10, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `593.523s` |
| full stage table | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210/report.md` §4 |
| run record | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210/pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz` |
| logs | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210/run_logs/stdout.txt`, `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210/run_logs/stderr.txt` |
| checks / repro | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210/checks.json`, `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:c0a5bc7f03814a273bd09483e877729634899eaded22e0068de8da394a1a25d0` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `59` |
| `langgraph_node_trace_hash` | `sha256:f4e1db64d62c813fae1a464fcd3d5f7feda381ec4c904765066c6ccfd6305c35` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `59` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12623 | 生成初始 DSL 与 grounding seeds | initial len=2490 | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=1; blocking=0, advisory=23, info=1; blocking=0, advisory=23, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=66958 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=72166 | LLM per-request accept/reject + repair | candidate len=2490,2920 | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=67194 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=1; blocking=0, advisory=23, info=1; blocking=0, advisory=23, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=66958 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=50832 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=72166 | LLM per-request accept/reject + repair | candidate len=2490,2920 | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=67194 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=1; blocking=0, advisory=23, info=1; blocking=0, advisory=23, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=66958 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=50832 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-07T21:25:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-07T21:25:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-07T21:25:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-07T21:25:53Z` | `SL-1` | `-` | `lg_d2_envelope_enter` | {} | <none> |
| 5 | `2026-06-07T21:25:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 6 | `2026-06-07T21:27:52Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 7 | `2026-06-07T21:27:52Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2490,hash=sha256:4cfdceaa2ee8 |
| 8 | `2026-06-07T21:27:52Z` | `SL-1` | `-` | `lg_d2_envelope_exit` | {} | <none> |
| 9 | `2026-06-07T21:27:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 10 | `2026-06-07T21:27:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-07T21:27:52Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:4cfdceaa2ee83167bc51907548c39f086230e7dcdf3be195528645bb7e6b56e0 |
| 12 | `2026-06-07T21:27:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-07T21:27:52Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2490,hash=sha256:4cfdceaa2ee8, current_hash=sha256:4cfdceaa2ee83167bc51907548c39f086230e7dcdf3be195528645bb7e6b56e0 |
| 14 | `2026-06-07T21:27:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 15 | `2026-06-07T21:27:52Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 16 | `2026-06-07T21:27:52Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-07T21:27:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 18 | `2026-06-07T21:27:52Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 19 | `2026-06-07T21:27:53Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-07T21:27:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 21 | `2026-06-07T21:27:53Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 22 | `2026-06-07T21:27:53Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-07T21:27:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-07T21:27:53Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 25 | `2026-06-07T21:27:53Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 26 | `2026-06-07T21:29:06Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 27 | `2026-06-07T21:29:06Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 28 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-07T21:29:06Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 30 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-07T21:29:06Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 32 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 33 | `2026-06-07T21:29:06Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 34 | `2026-06-07T21:29:06Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 35 | `2026-06-07T21:29:06Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 36 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-07T21:29:06Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 10, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 38 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-07T21:29:06Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 10, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2490,hash=sha256:4cfdceaa2ee8 |
| 42 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-07T21:29:06Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 44 | `2026-06-07T21:29:06Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 2} | <none> |
| 45 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-07T21:29:06Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2490,hash=sha256:4cfdceaa2ee8 |
| 47 | `2026-06-07T21:29:06Z` | `SL-9` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 48 | `2026-06-07T21:29:41Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 49 | `2026-06-07T21:29:41Z` | `SL-9` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 50 | `2026-06-07T21:29:41Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-92f946153f", "fixreq-0-sd6-1-2244c80013"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2490,hash=sha256:6448459b7345 |
| 51 | `2026-06-07T21:29:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 52 | `2026-06-07T21:29:41Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 53 | `2026-06-07T21:29:41Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:6448459b73453475d51ae3f572df1ea7482c6730750fa2b744a9cc498d5f0f4f |
| 54 | `2026-06-07T21:29:41Z` | `SL-10` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 55 | `2026-06-07T21:30:01Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 56 | `2026-06-07T21:30:01Z` | `SL-10` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 57 | `2026-06-07T21:30:01Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 58 | `2026-06-07T21:30:01Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 59 | `2026-06-07T21:30:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 60 | `2026-06-07T21:30:01Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at S
... <truncated 2508 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| `default_init_manual_outputs` | default-init: first cycle dispatches to Manual and manual operation sets pump speed from the built-in switch and flow fr...<truncated 25 chars> | ✅ | ✅ | ✅ |
| `initiate_change_setpoint_and_start_ac` | default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters Autocontrol...<truncated 5 chars> | ✅ | ✅ | ✅ |
| `autocontrol_init_advances_to_normal_high_bp` | explicit-hot-start: AutocontrolInit without a pump fault advances to normal autocontrol, where high blood pressure produ...<truncated 24 chars> | ✅ | ✅ | ✅ |
| `normal_autocontrol_equal_and_low_bp_flow` | explicit-hot-start: normal autocontrol computes medium flow at target pressure and, in a separate low-pressure hot-start...<truncated 31 chars> | ✅ | ✅ | ✅ |
| `normal_autocontrol_low_bp_high_flow` | explicit-hot-start: normal autocontrol with blood pressure below target produces a higher flow rate than at or above tar...<truncated 4 chars> | ⚪ | ✅ | ✅ |
| `pump_fault_boundary_and_recovery` | explicit-hot-start: pump_fault=0 is the no-fire boundary in normal autocontrol; pump_fault>0 enters PumpFault, and Fault...<truncated 26 chars> | ⚪ | ⚪ | ✅ |
| `autocontrol_fault_paths_release_control` | explicit-hot-start: faults from AutocontrolNormal and AutocontrolInit enter PumpFault with alarm/display/sound active an...<truncated 28 chars> | ⚪ | ⚪ | ✅ |
| `autocontrol_init_fault_priority` | explicit-hot-start: if a pump fault is already present in AutocontrolInit, the fault path should win over normal-autocon...<truncated 17 chars> | ❌ | ✅ | ✅ |
| `terminate_ac_from_control_states` | explicit-hot-start: caregiver TerminateAC from Ask_StartAC returns to Manual as the recovery mode. | ✅ | ✅ | ✅ |
| `terminate_ac_from_init_and_normal` | explicit-hot-start: local TerminateAC from AutocontrolInit releases control and returns to Manual. | ❌ | ✅ | ✅ |
| `terminate_ac_from_normal` | explicit-hot-start: local TerminateAC from AutocontrolNormal releases control and returns to Manual without requiring a ...<truncated 11 chars> | ⚪ | ✅ | ✅ |
| `forced_backmanual_events_from_distinct_states` | explicit-hot-start: cross-component CA/CB/CP/CC backManual events force recovery to Manual with CA_mode Manual and relea...<truncated 12 chars> | ✅ | ✅ | ✅ |
| `forced_backmanual_during_unresolved_fault_preserves_alarm` | explicit-hot-start: a cross-component backManual fallback during an unresolved pump fault reaches Manual but should not ...<truncated 55 chars> | ⚪ | ⚪ | ✅ |
| `autocontrol_normal_pump_fault_boundary` |  | ✅ | ✅ | ✅ |
| `autocontrol_normal_fault_enters_pumpfault` |  | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | autocontrol_init_fault_priority, terminate_ac_from_init_and_normal | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:6448459b73453475d51ae3f572df1ea7482c6730750fa2b744a9cc498d5f0f4f` |
| 2 | `1` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:f705ac69b45689b590ac83622b5e87c8e46943c1aaeb6c6b4d4c7294afb0558b` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210/report.md` §7。

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
    ! * -> F1 : Reset;

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
| token / elapsed | `{'prompt_tokens': 27092, 'completion_tokens': 7164, 'total_tokens': 34256, 'estimated_prompt_tokens': 26327, 'estimated_completion_tokens': 5546, 'estimated_total_tokens': 31873, 'prompt_chars': 105302, 'completion_chars': 22178, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `144.075s` |
| full stage table | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175/report.md` §4 |
| run record | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz` |
| logs | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175/run_logs/stdout.txt`, `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175/run_logs/stderr.txt` |
| checks / repro | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175/checks.json`, `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:9341198a81a116688f6f98b2882ff9a29a3a8bcd62cf964751b73148587e3eba` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9575 | 生成初始 DSL 与 grounding seeds | initial len=658 | [`record`](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=14097 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10584 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-07T21:25:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-07T21:25:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-07T21:25:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-07T21:25:53Z` | `SL-1` | `-` | `lg_d2_envelope_enter` | {} | <none> |
| 5 | `2026-06-07T21:25:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 6 | `2026-06-07T21:26:56Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 7 | `2026-06-07T21:26:56Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=658,hash=sha256:6b02aa0b651f |
| 8 | `2026-06-07T21:26:56Z` | `SL-1` | `-` | `lg_d2_envelope_exit` | {} | <none> |
| 9 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 10 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-07T21:26:56Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:6b02aa0b651f657a4b69e59da1e30c6ba2bed44ab0b8f429babbf3112ad83754 |
| 12 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-07T21:26:56Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=658,hash=sha256:6b02aa0b651f, current_hash=sha256:6b02aa0b651f657a4b69e59da1e30c6ba2bed44ab0b8f429babbf3112ad83754 |
| 14 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 15 | `2026-06-07T21:26:56Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 16 | `2026-06-07T21:26:56Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 18 | `2026-06-07T21:26:56Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 19 | `2026-06-07T21:26:56Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 21 | `2026-06-07T21:26:56Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 22 | `2026-06-07T21:26:56Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-07T21:26:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-07T21:26:56Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 25 | `2026-06-07T21:26:56Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 26 | `2026-06-07T21:27:48Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 27 | `2026-06-07T21:27:48Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 28 | `2026-06-07T21:27:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-07T21:27:48Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 30 | `2026-06-07T21:27:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-07T21:27:48Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 32 | `2026-06-07T21:27:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 33 | `2026-06-07T21:27:48Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 34 | `2026-06-07T21:27:48Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 35 | `2026-06-07T21:27:48Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-07T21:27:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-07T21:27:48Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 38 | `2026-06-07T21:27:48Z` | `SL-7` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 39 | `2026-06-07T21:28:17Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 40 | `2026-06-07T21:28:17Z` | `SL-7` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 41 | `2026-06-07T21:28:17Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-07T21:28:17Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 43 | `2026-06-07T21:28:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-07T21:28:17Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 45 | `2026-06-07T21:28:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-07T21:28:17Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=658,hash=sha256:6b02aa0b651f |
| 47 | `2026-06-07T21:28:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-07T21:28:17Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=658,hash=sha256:6b02aa0b651f |
| 49 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 50 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 51 | `` | `<control>` | `-` | `lg_e3_toolnode_wrapper_trace` | {} | <none> |
| 52 | `` | `<control>` | `-` | `lg_e2_send_parallel_trace` | {} | <none> |
| 53 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |
| 54 | `` | `<control>` | `-` | `lg_c1_graph_state_readiness` | {} | <none> |
| 55 | `` | `<control>` | `-` | `pr_e1_quality_boundary` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_and_up_to_f2_then_f3` | default-init dispatches to F1 stopped, then PS2 drives upward to MU2, S2 arrives at F2, PS3 drives upward to MU3, and S3...<truncated 15 chars> | ✅ |
| `f1_direct_to_f3_then_down_to_f1` | explicit-hot-start from F1 checks PS3 selects MU3, arrival at F3 stops, then PS1 selects MD1 and S1 returns to F1. | ✅ |
| `f2_request_down_to_f1` | explicit-hot-start from F2 checks PS1 selects downward MD1 and S1 arrival stops at F1. | ✅ |
| `f3_request_down_to_f2` | explicit-hot-start from F3 checks PS2 selects downward MD2 and S2 arrival stops at F2. | ✅ |
| `immediate_next_destination_after_f2_stop` | explicit-hot-start in MU2 verifies arrival at F2 stops, then the next-cycle PS1 request is immediately checked and start...<truncated 6 chars> | ✅ |
| `reset_from_upward_motion_to_f1` | explicit-hot-start from upward motion MU3 checks Reset forces the controller back to F1 with stop output. | ✅ |
| `reset_from_downward_motion_to_f1` | explicit-hot-start from downward motion MD2 checks Reset forces the controller back to F1 with stop output. | ✅ |
| `reset_from_floor_context_to_f1` | explicit-hot-start from floor F3 checks Reset forces floor contexts as well as motion contexts back to F1 with stop outp...<truncated 3 chars> | ✅ |
| `no_request_holds_floor_state` | explicit-hot-start from F2 checks an empty cycle with no request or arrival event leaves the elevator stopped at the sam...<truncated 8 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2611, 'completion_chars': 9326, 'completion_tokens': 3133, 'elapsed_seconds': 62.313252235006075, 'estimated_completion_tokens': 2332, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 8855, 'first_chunk_seconds': 15.145741614047438, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6442, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9575}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2138, 'completion_chars': 8527, 'completion_tokens': 2660, 'elapsed_seconds': 52.202931402018294, 'estimated_completion_tokens': 2132, 'estimated_prompt_tokens': 11129, 'estimated_total_tokens': 13261, 'first_chunk_seconds': 13.38903169304831, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 44515, 'prompt_tokens': 11437, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14097}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1000, 'completion_chars': 4325, 'completion_tokens': 1371, 'elapsed_seconds': 28.38900795398513, 'estimated_completion_tokens': 1082, 'estimated_prompt_tokens': 8675, 'estimated_total_tokens': 9757, 'first_chunk_seconds': 10.097893744998146, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 34698, 'prompt_tokens': 9213, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10584}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path1_elevator-default-lg_m1_g_signature_gate_20f104e8-d5b14175/report.md` §7。

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
def float Plng_req = 0.0;
def float Pd1_req = 0.0;
def float Pd2_req = 0.0;
def float Pbat_dis = 0.0;
def float Pbat_ch = 0.0;
def float spare_power = 0.0;
def int cut_in_LNG = 0;
def int cut_out_LNG = 0;
def int cut_in_DG1 = 0;
def int cut_out_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_out_DG2 = 0;
def int cut_in_loads = 0;
def int cut_out_loads = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> ResCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> ResCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
    ! * -> LngWithBattery : if [Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_Pmax && PL - Ppv - Pw - Pbat_Pmax <= eng3_Pmax];
    ! * -> LngLowSocCharge : if [Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= eng3_Pmax];
    ! * -> Dg1WithBattery : if [Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw - Pbat_Pmax > eng3_Pmax && PL - Ppv - Pw - Pbat_Pmax - eng3_Pmax <= Pd1max];
    ! * -> Dg1LowSocCharge : if [Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 - eng3_Pmax <= Pd1max];
    ! * -> Dg2WithBattery : if [Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw - Pbat_Pmax - eng3_Pmax > Pd1max && PL - Ppv - Pw - Pbat_Pmax - eng3_Pmax - Pd1max <= Pd2max];
    ! * -> Dg2LowSocCharge : if [Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 - eng3_Pmax > Pd1max && PL - Ppv - Pw + Pd1max / 10 - eng3_Pmax - Pd1max <= Pd2max];
    ! * -> OverloadCompletionIllegal : if [PL > Ppv + Pw + eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            Plng_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = 0.0;
            Pbat_ch = Ppv + Pw;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 0;
            cut_out_loads = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            Plng_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = 0.0;
            Pbat_ch = 0.0;
            spare_power = Ppv + Pw;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 0;
            cut_out_loads = 1;
        }
    }

    state ResCoversCharge {
        enter {
            Plng_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = 0.0;
            Pbat_ch = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state ResCoversSpare {
        enter {
            Plng_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = 0.0;
            Pbat_ch = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state BatteryDischarge {
        enter {
            Plng_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = PL - Ppv - Pw;
            Pbat_ch = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state LngWithBattery {
        enter {
            Plng_req = PL - Ppv - Pw - Pbat_Pmax;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = Pbat_Pmax;
            Pbat_ch = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state LngLowSocCharge {
        enter {
            Plng_req = PL - Ppv - Pw + Pgmax / 5;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_dis = 0.0;
            Pbat_ch = Pgmax / 5;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state Dg1WithBattery {
        enter {
            Plng_req = eng3_Pmax;
            Pd1_req = PL - Ppv - Pw - Pbat_Pmax - eng3_Pmax;
            Pd2_req = 0.0;
            Pbat_dis = Pbat_Pmax;
            Pbat_ch = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state Dg1LowSocCharge {
        enter {
            Plng_req = eng3_Pmax;
            Pd1_req = PL - Ppv - Pw + Pd1max / 10 - eng3_Pmax;
            Pd2_req = 0.0;
            Pbat_dis = 0.0;
            Pbat_ch = Pd1max / 10;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state Dg2WithBattery {
        enter {
            Plng_req = eng3_Pmax;
            Pd1_req = Pd1max;
            Pd2_req = PL - Ppv - Pw - Pbat_Pmax - eng3_Pmax - Pd1max;
            Pbat_dis = Pbat_Pmax;
            Pbat_ch = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state Dg2LowSocCharge {
        enter {
            Plng_req = eng3_Pmax;
            Pd1_req = Pd1max;
            Pd2_req = PL - Ppv - Pw + Pd1max / 10 - eng3_Pmax - Pd1max;
            Pbat_dis = 0.0;
            Pbat_ch = Pd1max / 10;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_loads = 1;
            cut_out_loads = 0;
        }
    }

    state OverloadCompletionIllegal {
        enter {
            Plng_req = eng3_Pmax;
            Pd1_req = Pd1max;
            Pd2_req = Pd2max;
            Pbat_dis = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbat_ch = 0.0;
            spare_power = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_loads = 1;
            cut_out_loads = 0;
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
| SC-11 post-accept validation | `✅ 1/1; ❌ 0` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SD-6 -> SL-7 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SD-6 -> SL-7 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SD-6 -> SL-7 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `5` / `2` / `14` |
| token / elapsed | `{'prompt_tokens': 800496, 'completion_tokens': 62324, 'total_tokens': 862820, 'estimated_prompt_tokens': 753833, 'estimated_completion_tokens': 42541, 'estimated_total_tokens': 796374, 'prompt_chars': 3015303, 'completion_chars': 170144, 'n_calls': 18, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1252.863s` |
| full stage table | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/report.md` §4 |
| run record | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz` |
| logs | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/run_logs/stdout.txt`, `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/run_logs/stderr.txt` |
| checks / repro | `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/checks.json`, `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:811174be19c7d2f84070f5d6b9601ca160abd0b7f67d61dbfcd0121079d4cba9` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `135` |
| `langgraph_node_trace_hash` | `sha256:4e163fb20d847cd0f4cfa67d5d9dea6697aed9028afbb1338fac7383d14defdf` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `135` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=15141 | 生成初始 DSL 与 grounding seeds | initial len=7852 | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=146283 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=146283 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=146283 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=5, tokens=285883 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=362186 | LLM per-request accept/reject + repair | candidate len=7944,0,0,0,7852 | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=53327 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=146283 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=362186 | LLM per-request accept/reject + repair | candidate len=7944,0,0,0,7852 | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=5, tokens=285883 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=362186 | LLM per-request accept/reject + repair | candidate len=7944,0,0,0,7852 | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=5, tokens=285883 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=362186 | LLM per-request accept/reject + repair | candidate len=7944,0,0,0,7852 | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=5, tokens=285883 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0, advisory=180, info=0; blocking=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=362186 | LLM per-request accept/reject + repair | candidate len=7944,0,0,0,7852 | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=53327 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=T
... <truncated 12275 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|---|
| `default_init_zero_load_charge` | default-init: with PL=0 and SoC below 0.95, EMS should initialize/classify to ZeroLoadCharge and route renewable product...<truncated 24 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `zero_load_soc_threshold_spare` | explicit-hot-start: at the exact SoC 0.95 threshold with PL=0, EMS should send renewable production to spare power rathe...<truncated 16 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `res_covers_charge_below_soc_threshold` | explicit-hot-start: with positive load covered by renewables and SoC just below 0.95, EMS should serve load from RES and...<truncated 38 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `res_covers_spare_at_soc_threshold` | explicit-hot-start: with positive load covered by renewables and SoC at 0.95, EMS should treat residual renewable power ...<truncated 9 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `battery_discharge_at_soc_suitable_boundary` | explicit-hot-start: when RES is below demand, SoC is exactly 0.2, and deficit fits battery capacity, EMS should use batt...<truncated 19 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `lng_with_battery_priority_before_diesel` | explicit-hot-start: with suitable SoC, battery capacity insufficient, and remaining deficit within LNG capacity, EMS sho...<truncated 32 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `lng_low_soc_charge_margin` | explicit-hot-start: with low SoC below 0.2, EMS should avoid battery discharge and add the Pgmax/5 charging margin in th...<truncated 19 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `dg1_with_battery_after_lng_capacity` | explicit-hot-start: with suitable SoC, battery and LNG insufficient but DG1 capacity sufficient, EMS should cut in DG1 w...<truncated 21 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `dg1_low_soc_pd1_margin` | explicit-hot-start: with low SoC, LNG capacity insufficient, and DG1 sufficient after Pd1max/10 margin, EMS should charg...<truncated 22 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `dg2_with_battery_last_priority` | explicit-hot-start: with suitable SoC, battery, LNG, and DG1 insufficient but DG2 sufficient, EMS should cut in DG2 as t...<truncated 27 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `dg2_low_soc_pd1_margin` | explicit-hot-start: with low SoC and demand extending beyond LNG and DG1 after the Pd1max/10 charging margin, EMS should...<truncated 32 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `overload_completion_illegal_extreme_demand` | explicit-hot-start: for extreme demand exceeding all RES and thermal resources, the illegal overload-completion case sho...<truncated 88 chars> | ✅ | ❌ | ❌ | ❌ | ✅ |
| `forced_reclassification_from_zero_spare_to_battery_discharge` | explicit-hot-start: from a concrete ZeroLoadSpare leaf, changing operating conditions to RES-below-load with suitable So...<truncated 131 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_from_overload_to_res_spare` | explicit-hot-start: from the concrete illegal overload leaf, a later RES-covered high-SoC condition must be reclassified...<truncated 114 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_from_dg2_to_zero_load_charge` | explicit-hot-start: from a concrete Dg2WithBattery leaf, changing to PL=0 with SoC below 0.95 must use the wildcard forc...<truncated 140 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=minor, local_stage=SD-10, reason=scenario_regression | `sha256:86b140b2c984f57a4a6b8ab1b608ad4875ee49a90e6e5ce5c4a2de7347e7b05d` |
| 2 | `1` | ❌ | `SD-6` | overload_completion_illegal_extreme_demand | accept=0, reject=1, waiver=0 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `2` | ❌ | `SD-6` | overload_completion_illegal_extreme_demand | accept=0, reject=1, waiver=0 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 4 | `3` | ❌ | `SD-6` | overload_completion_illegal_extreme_demand | accept=0, reject=1, waiver=0 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 5 | `4` | ✅ | `SD-6` | overload_completion_illegal_extreme_demand | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:5f773338ae6e3d85f4e4dc198016f6f241f6ec3d2d6e8f2aa8e3c871035ba195` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/lg_m1_g_four_after_signature_gate_20260608_052552/pr-e1-path2_lng_ems-default-lg_m1_g_signature_gate_20f104e8-c311405f/report.md` §7。

</details>
