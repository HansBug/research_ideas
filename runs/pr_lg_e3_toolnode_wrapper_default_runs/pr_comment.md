## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_lg_e3_toolnode_wrapper_default_runs/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | post-accept | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 34366 | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 762792 | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 33517 | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | ❌ | ⚪ 0 | `success` | 465451 | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d/report.md` |

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
- node trace count 范围：min=16，max=100；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：4/4 success，rejected=0，budget_exhausted=0，total_tokens=1296126。
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
- `path1_cara`：失败/成功类别=success，最大 observed iteration_count=5。
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

state SingleWheelABSRegulator {
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
| token / elapsed | `{'prompt_tokens': 26722, 'completion_tokens': 7644, 'total_tokens': 34366, 'estimated_prompt_tokens': 26232, 'estimated_completion_tokens': 4893, 'estimated_total_tokens': 31125, 'prompt_chars': 104926, 'completion_chars': 19566, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `144.848s` |
| full stage table | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2/report.md` §4 |
| run record | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2/pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz` |
| logs | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2/run_logs/stdout.txt`, `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2/checks.json`, `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:5a8b72e52eb12b84ba5f3168b5bec9b207180bda8750a0c6152ee0b4bed9603f` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=8939 | 生成初始 DSL 与 grounding seeds | initial len=625 | [`record`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13115 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=12312 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T20:28:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T20:28:18Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T20:28:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T20:28:18Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T20:29:06Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T20:29:06Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=625,hash=sha256:daf0a2131e36 |
| 7 | `2026-06-05T20:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T20:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T20:29:06Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:daf0a2131e360a06d62ea8c0a5ba398ff01b5fc756b01374275405d75c36a70e |
| 10 | `2026-06-05T20:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T20:29:06Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=625,hash=sha256:daf0a2131e36, current_hash=sha256:daf0a2131e360a06d62ea8c0a5ba398ff01b5fc756b01374275405d75c36a70e |
| 12 | `2026-06-05T20:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T20:29:06Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T20:29:07Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T20:29:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T20:29:07Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T20:29:07Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T20:29:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T20:29:07Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T20:29:07Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T20:29:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T20:29:07Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T20:30:04Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T20:30:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T20:30:04Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T20:30:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T20:30:04Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T20:30:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T20:30:04Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T20:30:04Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T20:30:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T20:30:04Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T20:30:43Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T20:30:43Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T20:30:43Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T20:30:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T20:30:43Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T20:30:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T20:30:43Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=625,hash=sha256:daf0a2131e36 |
| 40 | `2026-06-05T20:30:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T20:30:43Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=625,hash=sha256:daf0a2131e36 |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_e3_toolnode_wrapper_trace` | {} | <none> |
| 44 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_enters_increase_then_low_slip_holds` | default-init probe: first empty cycle dispatches to increase with inlet command, then default slp=0.0 satisfies increase...<truncated 30 chars> | ✅ |
| `increase_to_hold_at_positive_boundary` | explicit-hot-start probe: increase must transition to hold exactly at slp=0.01 and set neutral valve and pump commands. | ✅ |
| `increase_no_fire_above_positive_boundary` | explicit-hot-start no-fire probe: increase must remain increase when slp is just above 0.01. | ✅ |
| `hold_no_fire_at_positive_boundary` | explicit-hot-start boundary probe: hold must not transition to increase at slp=0.01 because the guard is strictly greate...<truncated 12 chars> | ✅ |
| `hold_to_increase_above_positive_boundary` | explicit-hot-start probe: hold must transition to increase when slp is greater than 0.01 and set inlet valve command k1=...<truncated 2 chars> | ✅ |
| `hold_no_fire_at_negative_boundary` | explicit-hot-start boundary probe: hold must not transition to decrease at slp=-0.01 because the guard is strictly less ...<truncated 11 chars> | ✅ |
| `hold_to_decrease_below_negative_boundary` | explicit-hot-start probe: hold must transition to decrease when slp is below -0.01, command return valve k2=1 and pump n...<truncated 64 chars> | ✅ |
| `decrease_to_hold_at_negative_boundary` | explicit-hot-start recovery boundary probe: decrease must transition to hold exactly at slp=-0.01 and neutralize both va...<truncated 14 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2027, 'completion_chars': 6889, 'completion_tokens': 2546, 'elapsed_seconds': 48.01047840699903, 'estimated_completion_tokens': 1723, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 8216, 'first_chunk_seconds': 11.439101432013558, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 8939}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1634, 'completion_chars': 6140, 'completion_tokens': 3084, 'elapsed_seconds': 57.37103375099832, 'estimated_completion_tokens': 1535, 'estimated_prompt_tokens': 9895, 'estimated_total_tokens': 11430, 'first_chunk_seconds': 27.882075255009113, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39580, 'prompt_tokens': 10031, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13115}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1495, 'completion_chars': 6537, 'completion_tokens': 2014, 'elapsed_seconds': 38.41822252399288, 'estimated_completion_tokens': 1635, 'estimated_prompt_tokens': 9844, 'estimated_total_tokens': 11479, 'first_chunk_seconds': 11.41681051699561, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39374, 'prompt_tokens': 10298, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12312}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2/report.md` §7。

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
def int algorithm_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int display_error = 0;
def int sound_error = 0;
def int log_count = 0;
def float blood_pressure = 120.0;
def float sensor_buffer_bp = 120.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float default_flow_rate = 1.0;
def float builtin_switch_speed = 0.0;
def float pump_speed = 0.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;

state CARA {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            algorithm_control = 0;
            control_voltage = 0.0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            pump_speed = builtin_switch_speed;
            infusion_rate = default_flow_rate;
        }
    }

    state Ask_StartAC {
        enter {
            algorithm_control = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    if [default_flow_rate - ((blood_pressure - target_bp) / 10.0) < 0.0] {
                        infusion_rate = 0.0;
                    } else {
                        infusion_rate = default_flow_rate - ((blood_pressure - target_bp) / 10.0);
                    }
                } else if [blood_pressure < target_bp] {
                    infusion_rate = default_flow_rate + ((target_bp - blood_pressure) / 10.0);
                } else {
                    infusion_rate = default_flow_rate;
                }
                control_voltage = infusion_rate;
                log_count = log_count + 1;
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            display_error = 1;
            sound_error = 1;
            algorithm_control = 0;
            control_voltage = 0.0;
            CA_mode = 0;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Manual -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
        display_error = 0;
        sound_error = 0;
    };
    Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
        target_bp = requested_target_bp;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
        display_error = 0;
        sound_error = 0;
    };
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `5` / `4` / `8` |
| token / elapsed | `{'prompt_tokens': 705305, 'completion_tokens': 57487, 'total_tokens': 762792, 'estimated_prompt_tokens': 805129, 'estimated_completion_tokens': 42141, 'estimated_total_tokens': 847270, 'prompt_chars': 3220490, 'completion_chars': 168544, 'n_calls': 18, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1101.866s` |
| full stage table | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33/report.md` §4 |
| run record | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33/pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz` |
| logs | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33/run_logs/stdout.txt`, `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33/checks.json`, `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:8a55d8d0f3adad44c29a53285e6a176963db609f277dba447131e919deb1c4bb` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `100` |
| `langgraph_node_trace_hash` | `sha256:3e71c44f7a4a3acf7ca838eb901b2d1b9e5eb2ccf3cc56b41d87b67cf00caa65` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `100` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=13445 | 生成初始 DSL 与 grounding seeds | initial len=2897 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=4, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138400 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=277823 | LLM per-request accept/reject + repair | candidate len=2897,3276,3272,3088,3243 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=273607 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=4, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138400 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=59517 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=277823 | LLM per-request accept/reject + repair | candidate len=2897,3276,3272,3088,3243 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=273607 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=4, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=277823 | LLM per-request accept/reject + repair | candidate len=2897,3276,3272,3088,3243 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=273607 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=4, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138400 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138400 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=277823 | LLM per-request accept/reject + repair | candidate len=2897,3276,3272,3088,3243 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=273607 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=277823 | LLM per-request accept/reject + repair | candidate len=2897,3276,3272,3088,3243 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=273607 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=4, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138400 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=59517 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T20:28:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T20:28:18Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T20:28:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T20:28:18Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T20:30:27Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T20:30:27Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2897,hash=sha256:3bef316f8581 |
| 7 | `2026-06-05T20:30:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T20:30:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T20:30:27Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:3bef316f858170d94de421bb8cdff399d488b9b33e6de3fc9a9182e89b4f4892 |
| 10 | `2026-06-05T20:30:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T20:30:27Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2897,hash=sha256:3bef316f8581, current_hash=sha256:3bef316f858170d94de421bb8cdff399d488b9b33e6de3fc9a9182e89b4f4892 |
| 12 | `2026-06-05T20:30:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T20:30:27Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_valid
... <truncated 8539 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|
| `default_init_manual_outputs` | default-init: first empty cycle dispatches to Manual and checks manual-mode pump speed, default flow, and sensor buffer ...<truncated 12 chars> | ✅ | ✅ | ✅ | ✅ |
| `initiate_change_start_to_normal` | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC into AutocontrolInit, then comple...<truncated 67 chars> | ✅ | ✅ | ✅ | ✅ |
| `terminate_from_ask_and_init` | explicit-hot-start: TerminateAC returns both Ask_StartAC and AutocontrolInit paths to Manual and releases algorithmic co...<truncated 6 chars> | ❌ | ✅ | ✅ | ✅ |
| `terminate_from_normal_manual_recovery` | explicit-hot-start: TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-output behavior. | ✅ | ✅ | ✅ | ✅ |
| `autocontrol_no_fault_continues` | explicit-hot-start: with no pump-operation complication, AutocontrolNormal stays active, controls flow, writes sensor bu...<truncated 20 chars> | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_enters_alarm_state` | explicit-hot-start: pump_fault present at AutocontrolNormal cycle start triggers PumpFault, activates alarms/errors, and...<truncated 27 chars> | ✅ | ✅ | ✅ | ✅ |
| `fault_removed_returns_manual` | explicit-hot-start: after caregiver removes the pump fault, FaultRemoved returns to Manual and clears fault/alarm/error ...<truncated 8 chars> | ✅ | ✅ | ✅ | ✅ |
| `ca_forced_backmanual_from_init` | explicit-hot-start: CA_backManual is a cross-component forced fallback from AutocontrolInit to Manual with CA_mode becom...<truncated 11 chars> | ✅ | ✅ | ✅ | ✅ |
| `cb_cp_forced_backmanual_from_distinct_modes` | explicit-hot-start: CB_backManual and CP_backManual each force recovery to Manual from different concrete autocontrol-re...<truncated 13 chars> | ✅ | ✅ | ✅ | ✅ |
| `cc_forced_backmanual_from_pumpfault` | explicit-hot-start: CC_backManual forced fallback from PumpFault reaches the shared Manual recovery target and makes CA_...<truncated 12 chars> | ✅ | ✅ | ❌ | ✅ |
| `pump_fault_alarm_and_fault_removed_recovery` | explicit-hot-start: pump_fault at AutocontrolNormal cycle start triggers PumpFault alarms and FaultRemoved returns to Ma...<truncated 35 chars> | ⚪ | ✅ | ✅ | ✅ |
| `ca_cb_cp_forced_backmanual_from_distinct_modes` | explicit-hot-start: CA_backManual, CB_backManual, and CP_backManual each force recovery to Manual from distinct autocont...<truncated 19 chars> | ⚪ | ✅ | ✅ | ✅ |
| `direct_startac_wrong_target_probe` | explicit-hot-start: direct StartAC probe asserts the NL-required target AutocontrolInit, catching a wrong-target mutatio...<truncated 36 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `direct_forced_backmanual_missing_line_probe` | explicit-hot-start: direct forced-fallback probe from AutocontrolNormal asserts CB_backManual cannot be ignored and must...<truncated 23 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `direct_initiateac_wrong_target_probe` | explicit-hot-start: direct InitiateAC probe asserts Manual transitions specifically to Ask_StartAC, catching a wrong-tar...<truncated 58 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `cp_forced_backmanual_from_init_missing_line_probe` | explicit-hot-start: direct CP_backManual forced-line probe from AutocontrolInit must preempt normal completion and force...<truncated 60 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `manual_faultremoved_clears_fault_effect_probe` | explicit-hot-start: FaultRemoved in Manual must remain in Manual and clear pump fault, alarm, display, and sound flags, ...<truncated 73 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `change_setpoint_effect_value_probe` | explicit-hot-start: ChangeSetpoint self-transition in Ask_StartAC must copy requested_target_bp exactly into target_bp, ...<truncated 61 chars> | ⚪ | ⚪ | ⚪ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | terminate_from_ask_and_init | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:48ce567f26a88754ade6860491bdaa7d3b81aaa05a8840142354e26511c6634f` |
| 2 | `1` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; forced_transition_count_drift; missing_required_grou...<truncated 5 chars> | `sha256:7bf779e133e6924bf5662682bf3dfe13dc8dd437631c907942aa8b12a49f56b2` |
| 3 | `2` | ✅ | `SD-4` | W_SHADOWED_EVENT:c60af7e5d001, W_SHADOWED_EVENT:f4bb66e5dced, W_SHADOWED_EVENT:a96a0048e482, W_SHADOWED_EVENT:d2bae58d678f, W_SHADOWED_EVENT, ... +4 | accept=4, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:13a9d992112a6e2e753dd8c3ad4307b4319b669cbdb096d56eece1ababe3c3cd` |
| 4 | `3` | ❌ | `SD-6` | cc_forced_backmanual_from_pumpfault | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=True, drift=major, rework=Preserve the current candidate's removal of the four PumpFault-specific backManual self-transitions; do not reintroduce the PumpFault latch for `CA_backManual`, `CB_backManual`,...<truncated 784 chars> | `sha256:6b670df7ed470bee2feb8d100c847b4ee02dcf1c89aa7822180b7c05fff5d25a` |
| 5 | `3` | ✅ | `SD-6` | cc_forced_backmanual_from_pumpfault | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | `sha256:96664ae396e6987ee2972e64c90f660b2ea3ffea03fc8df418d9aa53f932133e` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33/report.md` §7。

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
| token / elapsed | `{'prompt_tokens': 26940, 'completion_tokens': 6577, 'total_tokens': 33517, 'estimated_prompt_tokens': 26153, 'estimated_completion_tokens': 4702, 'estimated_total_tokens': 30855, 'prompt_chars': 104604, 'completion_chars': 18803, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `125.829s` |
| full stage table | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a/report.md` §4 |
| run record | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a/pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz` |
| logs | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a/run_logs/stdout.txt`, `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a/checks.json`, `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:e68317fc592cf870f5b117b1299f497ef08b330355f95e17a1fba83bc1edd93b` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9594 | 生成初始 DSL 与 grounding seeds | initial len=659 | [`record`](./pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13329 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10594 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T20:28:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T20:28:18Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T20:28:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T20:28:18Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T20:29:17Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T20:29:17Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=659,hash=sha256:a0b11c24e587 |
| 7 | `2026-06-05T20:29:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T20:29:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T20:29:17Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:a0b11c24e58704e6a2e93a84991bf1241e7524ee107639a6504576e458270c99 |
| 10 | `2026-06-05T20:29:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T20:29:17Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=659,hash=sha256:a0b11c24e587, current_hash=sha256:a0b11c24e58704e6a2e93a84991bf1241e7524ee107639a6504576e458270c99 |
| 12 | `2026-06-05T20:29:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T20:29:17Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T20:29:18Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T20:29:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T20:29:18Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T20:29:18Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T20:29:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T20:29:18Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T20:29:18Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T20:29:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T20:29:18Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T20:29:54Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T20:29:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T20:29:54Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T20:29:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T20:29:54Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T20:29:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T20:29:54Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T20:29:54Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T20:29:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T20:29:54Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T20:30:24Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T20:30:24Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T20:30:24Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T20:30:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T20:30:24Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T20:30:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T20:30:24Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=659,hash=sha256:a0b11c24e587 |
| 40 | `2026-06-05T20:30:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T20:30:24Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=659,hash=sha256:a0b11c24e587 |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_e3_toolnode_wrapper_trace` | {} | <none> |
| 44 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_then_up_to_f2_and_f3` | default-init verifies initial floor 1 stop output, then requests F2 and F3 with upward-drive and stop hbrg obligations. | ✅ |
| `f1_direct_request_to_f3` | explicit-hot-start probes F1 PS3 wrong-target risk: request for floor 3 must enter MU3 with upward-drive hbrg. | ✅ |
| `f2_request_down_to_f1` | explicit-hot-start probes F2 PS1 downward branch and MD1 arrival at F1 with stop hbrg restored. | ✅ |
| `f3_request_down_to_f1` | explicit-hot-start probes F3 PS1 must target MD1 rather than MD2, then S1 arrival returns to floor 1 stop. | ✅ |
| `f3_request_down_to_f2` | explicit-hot-start probes F3 PS2 must enter MD2 with downward hbrg and S2 arrival must stop at F2. | ✅ |
| `reset_from_upward_motion_forces_f1` | explicit-hot-start probes global reset from an upward-motion leaf, requiring F1 stop regardless of outstanding context. | ✅ |
| `reset_from_downward_motion_forces_f1` | explicit-hot-start probes global reset from a downward-motion leaf, requiring F1 stop regardless of outstanding context. | ✅ |
| `reset_from_floor_context_forces_f1` | explicit-hot-start probes global reset from a non-F1 stopped floor context, requiring F1 stop output. | ✅ |
| `no_request_stays_stopped_at_f2` | explicit-hot-start no-fire probe: with no request or arrival event, stopped floor 2 remains F2 with stop hbrg. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2637, 'completion_chars': 9361, 'completion_tokens': 3156, 'elapsed_seconds': 59.02566440400551, 'estimated_completion_tokens': 2341, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 8864, 'first_chunk_seconds': 11.4614993740106, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9594}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1351, 'completion_chars': 5215, 'completion_tokens': 1870, 'elapsed_seconds': 36.04678891701042, 'estimated_completion_tokens': 1304, 'estimated_prompt_tokens': 11138, 'estimated_total_tokens': 12442, 'first_chunk_seconds': 11.256581116991583, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 44550, 'prompt_tokens': 11459, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13329}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1077, 'completion_chars': 4227, 'completion_tokens': 1551, 'elapsed_seconds': 29.59703988698311, 'estimated_completion_tokens': 1057, 'estimated_prompt_tokens': 8492, 'estimated_total_tokens': 9549, 'first_chunk_seconds': 10.155502170004183, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 33965, 'prompt_tokens': 9043, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10594}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path1_elevator-default-lg-e3-toolnode-clean-20260606T050000Z-4b8cfc8a/report.md` §7。

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
def float SoC = 1.0;
def float Pbmax = 0.0;
def float Pgmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charging_power = 0.0;
def float spare_power = 0.0;
def float P_LNG_req = 0.0;
def float P_DG3_req = 0.0;
def float P_DG1_req = 0.0;
def float P_DG2_req = 0.0;
def int cut_in_LNG = 0;
def int cut_out_LNG = 1;
def int cut_in_DG3 = 0;
def int cut_out_DG3 = 1;
def int cut_in_DG1 = 0;
def int cut_out_DG1 = 1;
def int cut_in_DG2 = 0;
def int cut_out_DG2 = 1;
def int cut_in_loads = 0;
def int cut_out_loads = 0;
def int illegal_state = 0;

state LNGShipEMS {
    ! * -> PLZeroCharge : if [(PL == 0.0) && (SoC < 0.95)];
    ! * -> PLZeroSpare : if [(PL == 0.0) && (SoC >= 0.95)];
    ! * -> RESCharge : if [(PL > 0.0) && ((Ppv + Pw) >= PL) && (SoC < 0.95)];
    ! * -> RESSpare : if [(PL > 0.0) && ((Ppv + Pw) >= PL) && (SoC >= 0.95)];
    ! * -> RESBattery : if [(PL > (Ppv + Pw)) && (SoC >= 0.2) && ((PL - Ppv - Pw) <= Pbmax)];
    ! * -> RESLNG : if [(PL > (Ppv + Pw)) && (SoC >= 0.2) && ((PL - Ppv - Pw) > Pbmax) && ((PL - Ppv - Pw) <= Pgmax)];
    ! * -> RESLNGChargeMargin : if [(PL > (Ppv + Pw)) && (SoC < 0.2) && (((PL - Ppv - Pw) + (Pgmax / 5.0)) <= Pgmax)];
    ! * -> RESLNGDG3 : if [(PL > (Ppv + Pw)) && (((SoC >= 0.2) && ((PL - Ppv - Pw) > Pgmax) && ((PL - Ppv - Pw) <= (Pgmax + eng3_Pmax))) || ((SoC < 0.2) && (((PL - Ppv - Pw) + (Pgmax / 5.0)) > Pgmax) && (((PL - Ppv - Pw) + (Pd1max / 10.0)) <= (Pgmax + eng3_Pmax))))];
    ! * -> RESLNGDG3DG1 : if [(PL > (Ppv + Pw)) && (SoC >= 0.2) && ((PL - Ppv - Pw) > (Pgmax + eng3_Pmax)) && ((PL - Ppv - Pw) <= (Pgmax + eng3_Pmax + Pd1max))];
    ! * -> RESLNGDG3DG1ChargeMargin : if [(PL > (Ppv + Pw)) && (SoC < 0.2) && (((PL - Ppv - Pw) + (Pd1max / 10.0)) > (Pgmax + eng3_Pmax)) && (((PL - Ppv - Pw) + (Pd1max / 10.0)) <= (Pgmax + eng3_Pmax + Pd1max))];
    ! * -> RESLNGDG3DG1DG2 : if [(PL > (Ppv + Pw)) && (((SoC >= 0.2) && ((PL - Ppv - Pw) > (Pgmax + eng3_Pmax + Pd1max)) && ((PL - Ppv - Pw) <= (Pgmax + eng3_Pmax + Pd1max + Pd2max))) || ((SoC < 0.2) && (((PL - Ppv - Pw) + (Pd1max / 10.0)) > (Pgmax + eng3_Pmax + Pd1max)) && ((PL - Ppv - Pw) <= (Pgmax + eng3_Pmax + Pd1max + Pd2max))))];
    ! * -> OverloadCompletionIllegal : if [(PL > (Ppv + Pw)) && ((PL - Ppv - Pw) > (Pgmax + eng3_Pmax + Pd1max + Pd2max))];

    [*] -> PLZeroSpare;

    state PLZeroCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw;
            spare_power = 0.0;
            P_LNG_req = 0.0;
            P_DG3_req = 0.0;
            P_DG1_req = 0.0;
            P_DG2_req = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 0;
            cut_out_loads = 0;
            illegal_state = 0;
        }
    }

    state PLZeroSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw;
            P_LNG_req = 0.0;
            P_DG3_req = 0.0;
            P_DG1_req = 0.0;
            P_DG2_req = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 0;
            cut_out_loads = 0;
            illegal_state = 0;
        }
    }

    state RESCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw - PL;
            spare_power = 0.0;
            P_LNG_req = 0.0;
            P_DG3_req = 0.0;
            P_DG1_req = 0.0;
            P_DG2_req = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
            illegal_state = 0;
        }
    }

    state RESSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw - PL;
            P_LNG_req = 0.0;
            P_DG3_req = 0.0;
            P_DG1_req = 0.0;
            P_DG2_req = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
            illegal_state = 0;
        }
    }

    state RESBattery {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            P_LNG_req = 0.0;
            P_DG3_req = 0.0;
            P_DG1_req = 0.0;
            P_DG2_req = 0.0;
            cut_in_LNG = 0;
            cut_out_LNG = 1;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
            illegal_state = 0;
        }
    }

    state RESLNG {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            P_LNG_req = PL - Ppv - Pw;
            P_DG3_req = 0.0;
            P_DG1_req = 0.0;
            P_DG2_req = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
            illegal_state = 0;
        }
    }

    state RESLNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + (Pgmax / 5.0);
            battery_discharge_power = 0.0;
            battery_charging_power = Pgmax / 5.0;
            spare_power = 0.0;
            P_LNG_req = PL - Ppv - Pw + (Pgmax / 5.0);
            P_DG3_req = 0.0;
            P_DG1_req = 0.0;
            P_DG2_req = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG3 = 0;
            cut_out_DG3 = 1;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
            illegal_state = 0;
        }
    }

    state RESLNGDG3 {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            P_LNG_req = Pgmax;
            P_DG3_req = PL - Ppv - Pw - Pgmax;
            P_DG1_req = 0.0;
            P_DG2_req = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_DG1 = 0;
            cut_out_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
            illegal_state = 0;
        }
    }

    state RESLNGDG3DG1 {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            P_LNG_req = Pgmax;
            P_DG3_req = eng3_Pmax;
            P_DG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax;
            P_DG2_req = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
            illegal_state = 0;
        }
    }

    state RESLNGDG3DG1ChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + (Pd1max / 10.0);
            battery_discharge_power = 0.0;
            battery_charging_power = Pd1max / 10.0;
            spare_power = 0.0;
            P_LNG_req = Pgmax;
            P_DG3_req = eng3_Pmax;
            P_DG1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax + (Pd1max / 10.0);
            P_DG2_req = 0.0;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_DG2 = 1;
            cut_in_loads = 1;
            cut_out_loads = 0;
            illegal_state = 0;
        }
    }

    state RESLNGDG3DG1DG2 {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            P_LNG_req = Pgmax;
            P_DG3_req = eng3_Pmax;
            P_DG1_req = Pd1max;
            P_DG2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_loads = 1;
            cut_out_loads = 0;
            illegal_state = 0;
        }
    }

    state OverloadCompletionIllegal {
        enter {
            requested_generator_power = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            battery_discharge_power = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            P_LNG_req = Pgmax;
            P_DG3_req = eng3_Pmax;
            P_DG1_req = Pd1max;
            P_DG2_req = Pd2max;
            cut_in_LNG = 1;
            cut_out_LNG = 0;
            cut_in_DG3 = 1;
            cut_out_DG3 = 0;
            cut_in_DG1 = 1;
            cut_out_DG1 = 0;
            cut_in_DG2 = 1;
            cut_out_DG2 = 0;
            cut_in_loads = 1;
            cut_out_loads = 0;
            illegal_state = 1;
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `3` / `2` / `2` / `7` |
| token / elapsed | `{'prompt_tokens': 409647, 'completion_tokens': 55804, 'total_tokens': 465451, 'estimated_prompt_tokens': 361646, 'estimated_completion_tokens': 37143, 'estimated_total_tokens': 398789, 'prompt_chars': 1446568, 'completion_chars': 148555, 'n_calls': 12, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1058.106s` |
| full stage table | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d/report.md` §4 |
| run record | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d/pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz` |
| logs | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d/run_logs/stdout.txt`, `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d/checks.json`, `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:88280846c39099fc3113dce96def89a312d11e111bd1bb1450a1a378632abf9e` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `63` |
| `langgraph_node_trace_hash` | `sha256:d6446cfa2d294c74de886fedf010c27d3a480d836d06cfd0291e704d913f3d72` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `63` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=16159 | 生成初始 DSL 与 grounding seeds | initial len=10689 | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=192, info=0; blocking=0, advisory=192, info=0; blocking=0, advisory=192, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138879 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138879 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138879 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=95087 | LLM per-request accept/reject + repair | candidate len=10688,10820 | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=101397 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=192, info=0; blocking=0, advisory=192, info=0; blocking=0, advisory=192, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138879 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=113929 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=95087 | LLM per-request accept/reject + repair | candidate len=10688,10820 | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=101397 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=192, info=0; blocking=0, advisory=192, info=0; blocking=0, advisory=192, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138879 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=113929 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T20:28:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T20:28:18Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T20:28:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T20:28:18Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T20:31:15Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T20:31:15Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=10689,hash=sha256:54bf8ef78b81 |
| 7 | `2026-06-05T20:31:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T20:31:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T20:31:15Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:54bf8ef78b81fc8516ef1a88a0c93cd190a373977dcc35bfc6698cdc3dab8603 |
| 10 | `2026-06-05T20:31:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T20:31:15Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=10689,hash=sha256:54bf8ef78b81, current_hash=sha256:54bf8ef78b81fc8516ef1a88a0c93cd190a373977dcc35bfc6698cdc3dab8603 |
| 12 | `2026-06-05T20:31:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T20:31:15Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T20:31:15Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T20:31:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T20:31:15Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T20:31:15Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T20:31:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T20:31:15Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T20:31:16Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T20:31:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T20:31:16Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T20:32:58Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T20:32:58Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T20:32:59Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T20:32:59Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T20:32:59Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T20:34:42Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T20:34:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T20:34:43Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T20:34:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T20:34:43Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T20:36:35Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T20:36:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T20:36:36Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-05T20:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T20:36:36Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 38 | `2026-06-05T20:36:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T20:36:36Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 40 | `2026-06-05T20:36:37Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 41 | `2026-06-05T20:36:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-05T20:36:37Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 16, "n_scenarios_passed": 15, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 43 | `2026-06-05T20:36:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-05T20:36:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T20:36:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-05T20:36:37Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 16, "n_scenarios_passed": 15, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=10689,hash=sha256:54bf8ef78b81 |
| 47 | `2026-06-05T20:36:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-05T20:36:37Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 49 | `2026-06-05T20:36:37Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 50 | `2026-06-05T20:36:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 51 | `2026-06-05T20:36:37Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old
... <truncated 3851 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| `default_init_pl_zero_high_soc_spare` | default-init probe: with PL=0 and default SoC at/above 0.95, RES production should be treated as spare rather than batte...<truncated 10 chars> | ❌ | ✅ | ✅ |
| `pl_zero_low_soc_charges_battery` | explicit-hot-start probe: when PL=0 and SoC is below 0.95, renewable production should go to battery charging. | ✅ | ✅ | ✅ |
| `res_covers_load_below_soc_threshold_charges` | explicit-hot-start probe: with PL>0, RES covering demand, and SoC below 0.95, surplus RES should charge the battery. | ✅ | ✅ | ✅ |
| `res_covers_load_at_soc_threshold_spares` | explicit-hot-start boundary probe: at SoC=0.95 exactly, surplus RES should become spare power, not battery charging. | ✅ | ✅ | ✅ |
| `battery_supplies_deficit_at_low_soc_suitable_boundary` | explicit-hot-start boundary probe: at SoC=0.2 and deficit within Pbmax, batteries should cover the RES shortfall. | ✅ | ✅ | ✅ |
| `lng_supplies_deficit_at_pgmax_boundary` | explicit-hot-start boundary probe: with SoC suitable and deficit above battery capacity but equal to Pgmax, LNG should s...<truncated 40 chars> | ✅ | ✅ | ✅ |
| `low_soc_lng_charge_margin_pgmax_fifth` | explicit-hot-start low-SoC probe: LNG-covered low-SoC branch should add Pgmax/5 charging margin. | ✅ | ✅ | ✅ |
| `low_soc_lng_dg3_intermediate_gap` | explicit-hot-start regression probe: low-SoC intermediate deficit after the Pgmax/5 LNG charge-margin range but before l...<truncated 55 chars> | ⚪ | ⚪ | ✅ |
| `lng_and_dg3_cover_at_combined_boundary` | explicit-hot-start boundary probe: with deficit equal to Pgmax+eng3_Pmax, LNG and DG3 should be active while DG1/DG2 rem...<truncated 8 chars> | ✅ | ✅ | ✅ |
| `dg1_added_after_lng_and_dg3` | explicit-hot-start priority probe: when deficit exceeds LNG+DG3 but remains within DG1 capacity, DG1 should be cut in an...<truncated 24 chars> | ✅ | ✅ | ✅ |
| `low_soc_dg1_charge_margin_pd1_tenth` | explicit-hot-start low-SoC probe: later diesel-generator low-SoC branch should add Pd1max/10 charging margin. | ✅ | ✅ | ✅ |
| `dg2_added_last_at_all_thermal_boundary` | explicit-hot-start priority boundary probe: when deficit exceeds LNG+DG3+DG1 but is within DG2 capacity, DG2 is the last...<truncated 18 chars> | ✅ | ✅ | ✅ |
| `extreme_overload_illegal_all_thermal_and_battery` | explicit-hot-start illegal-state probe: if extreme demand exceeds all RES and thermal resources, all thermal units are a...<truncated 46 chars> | ✅ | ✅ | ✅ |
| `forced_reclassification_from_illegal_to_res_spare` | explicit-hot-start forced-transition probe: from an illegal leaf, changed RES-covering conditions at the SoC=0.95 bounda...<truncated 40 chars> | ✅ | ✅ | ✅ |
| `forced_reclassification_to_dg2_all_thermal_boundary` | explicit-hot-start forced-transition and unreachable-target probe: from a RESCharge leaf, deficit at the all-thermal bou...<truncated 49 chars> | ✅ | ✅ | ✅ |
| `forced_reclassification_from_battery_to_lng_dg3_threshold` | explicit-hot-start added M3/M4 probe: from a battery-serving leaf, a deficit exactly at Pgmax+eng3_Pmax must globally re...<truncated 102 chars> | ✅ | ✅ | ✅ |
| `forced_reclassification_from_dg2_to_pl_zero_soc_threshold` | explicit-hot-start added M3/M4 probe: from the all-thermal DG2 leaf, PL=0 at SoC=0.95 must globally reclassify to PLZero...<truncated 84 chars> | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | default_init_pl_zero_high_soc_spare | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:61b98f0f25ef3ab3f7abbbe979103b649d532d205dd8f4367acef66388341a9a` |
| 2 | `1` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:e860dce9fd0809dcd2bd93c1fd7ab50ce484cafc7aa2adb2e6443ce2b7c95b5d` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_e3_toolnode_wrapper_default_runs/pr-e1-path2_lng_ems-default-lg-e3-toolnode-clean-20260606T050000Z-f82a7b6d/report.md` §7。

</details>
