## 四例真实运行 evidence（20f104e8，part 1/3）

身份：主 session / LG-M1-G runner。

本条为 PR #77 在最新 head `20f104e8` 上重跑 ABS / CARA / Elevator / LNG 四例的 evidence 分片；完整 artifact 目录：`runs/lg_m1_g_four_after_signature_gate_20260608_052552`。

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
