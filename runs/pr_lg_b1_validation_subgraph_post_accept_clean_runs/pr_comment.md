## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 35588 | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 1106376 | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 35169 | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | ❌ | `success` | 642421 | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947/report.md` |

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
- node trace count 范围：min=16，max=82；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：4/4 success，rejected=0，budget_exhausted=0，total_tokens=1819554。
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

state System {
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
| token / elapsed | `{'prompt_tokens': 29225, 'completion_tokens': 6363, 'total_tokens': 35588, 'estimated_prompt_tokens': 28470, 'estimated_completion_tokens': 4301, 'estimated_total_tokens': 32771, 'prompt_chars': 113877, 'completion_chars': 17199, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `123.154s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc/pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc/checks.json`, `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:27a997d32b4cb0eb9a1046da198ed5fd8a4242b54b9cb4ac5d3b2fff07fc54ca` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9052 | 生成初始 DSL 与 grounding seeds | initial len=611 | [`record`](./pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=17, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=12216 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=14320 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T12:51:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T12:51:26Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T12:51:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T12:51:26Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T12:52:16Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T12:52:16Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=611,hash=sha256:eb601fd52713 |
| 7 | `2026-06-05T12:52:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T12:52:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T12:52:16Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:eb601fd5271360f1eb69c4785591cd32235efbb7ea852751e00622134f4a3f28 |
| 10 | `2026-06-05T12:52:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T12:52:16Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=611,hash=sha256:eb601fd52713, current_hash=sha256:eb601fd5271360f1eb69c4785591cd32235efbb7ea852751e00622134f4a3f28 |
| 12 | `2026-06-05T12:52:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T12:52:16Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T12:52:16Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T12:52:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T12:52:16Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T12:52:17Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T12:52:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T12:52:17Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T12:52:17Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T12:52:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T12:52:17Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T12:52:49Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T12:52:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T12:52:50Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T12:52:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T12:52:50Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T12:52:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T12:52:50Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T12:52:50Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T12:52:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T12:52:50Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T12:53:29Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T12:53:29Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T12:53:29Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T12:53:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T12:53:29Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T12:53:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T12:53:29Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=611,hash=sha256:eb601fd52713 |
| 40 | `2026-06-05T12:53:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T12:53:29Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=611,hash=sha256:eb601fd52713 |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_increase_then_hold_at_default_slip` | default-init dispatches to increase and applies increase outputs, then default slp=0.0 satisfies increase->hold with hol...<truncated 10 chars> | ✅ |
| `increase_to_hold_at_upper_boundary` | explicit-hot-start in increase with slp exactly 0.01 should take increase->hold and neutralize outputs. | ✅ |
| `increase_no_fire_above_upper_boundary` | explicit-hot-start in increase with slp just above 0.01 should not take increase->hold and should keep increase outputs. | ✅ |
| `hold_to_increase_above_upper_boundary` | explicit-hot-start in hold with slp greater than 0.01 should take hold->increase and command inlet increase outputs. | ✅ |
| `hold_no_fire_at_positive_boundary` | explicit-hot-start in hold with slp exactly 0.01 should not satisfy hold->increase and should remain neutral. | ✅ |
| `hold_to_decrease_below_lower_boundary` | explicit-hot-start in hold with slp less than -0.01 should take hold->decrease and command pressure release outputs. | ✅ |
| `hold_no_fire_at_negative_boundary` | explicit-hot-start in hold with slp exactly -0.01 should not satisfy hold->decrease and should remain neutral. | ✅ |
| `decrease_to_hold_at_lower_boundary` | explicit-hot-start in decrease with slp exactly -0.01 should take decrease->hold and neutralize valve and pump outputs. | ✅ |
| `decrease_no_fire_below_lower_boundary` | explicit-hot-start in decrease with slp just below -0.01 should not take decrease->hold and should continue pressure rel...<truncated 13 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1976, 'completion_chars': 6674, 'completion_tokens': 2659, 'elapsed_seconds': 50.400894479011185, 'estimated_completion_tokens': 1669, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 8162, 'first_chunk_seconds': 14.77783381700283, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9052}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 954, 'completion_chars': 3699, 'completion_tokens': 1658, 'elapsed_seconds': 32.72629819699796, 'estimated_completion_tokens': 925, 'estimated_prompt_tokens': 10396, 'estimated_total_tokens': 11321, 'first_chunk_seconds': 15.950393929990241, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 41583, 'prompt_tokens': 10558, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12216}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1527, 'completion_chars': 6826, 'completion_tokens': 2046, 'elapsed_seconds': 38.9707711149822, 'estimated_completion_tokens': 1707, 'estimated_prompt_tokens': 11581, 'estimated_total_tokens': 13288, 'first_chunk_seconds': 11.849187413987238, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 46322, 'prompt_tokens': 12274, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14320}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_abs-default-lg-b1-post-accept-bc94bda6-da1bc7cc/report.md` §7。

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
def int target_bp = 80;
def int caregiver_target_bp = 80;
def int blood_pressure = 80;
def int shared_sensor_buffer = 0;
def int default_flow_rate = 10;
def int built_in_switch = 10;
def int control_voltage = 10;
def int pump_speed = 0;
def int flow_rate = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 1;
def int log_count = 0;
def int setpoint_changed = 0;

state CARA {
    ! * -> Manual : CB_backManual;
    ! * -> Manual : CP_backManual;
    ! * -> Manual : CC_backManual;
    ! AutocontrolNormal -> PumpFault : if [pump_fault > 0];

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault == 0] {
                alarm_signal = 0;
            } else {
                alarm_signal = 1;
                pump_speed = 0;
                flow_rate = 0;
            }
        }
        during {
            shared_sensor_buffer = blood_pressure;
            if [pump_fault == 0] {
                alarm_signal = 0;
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            } else {
                alarm_signal = 1;
                pump_speed = 0;
                flow_rate = 0;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
            control_released = 0;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            setpoint_changed = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 2;
            control_released = 0;
        }
        during {
            shared_sensor_buffer = blood_pressure;
            log_count = log_count + 1;
            pump_speed = control_voltage;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    flow_rate = default_flow_rate - 1;
                } else if [blood_pressure < target_bp] {
                    flow_rate = default_flow_rate + 1;
                } else {
                    flow_rate = default_flow_rate;
                }
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            control_released = 1;
            CA_mode = 0;
            pump_speed = 0;
            flow_rate = 0;
        }
    }

    Manual -> Ask_StartAC : InitiateAC;
    Manual -> Manual : CA_backManual;
    Manual -> Manual : FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
    Ask_StartAC -> AutocontrolInit : StartAC;
    Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
        target_bp = caregiver_target_bp;
        setpoint_changed = 1;
    };
    Ask_StartAC -> Manual : TerminateAC;
    Ask_StartAC -> Manual : CA_backManual;
    AutocontrolInit -> Manual : TerminateAC;
    AutocontrolInit -> Manual : CA_backManual;
    AutocontrolNormal -> Manual : TerminateAC;
    AutocontrolNormal -> Manual : CA_backManual;
    AutocontrolInit -> AutocontrolNormal;
    PumpFault -> Manual : CA_backManual;
    PumpFault -> Manual : FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `5` / `4` / `11` |
| token / elapsed | `{'prompt_tokens': 1035373, 'completion_tokens': 71003, 'total_tokens': 1106376, 'estimated_prompt_tokens': 1274175, 'estimated_completion_tokens': 52102, 'estimated_total_tokens': 1326277, 'prompt_chars': 5096664, 'completion_chars': 208375, 'n_calls': 21, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1371.799s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b/pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b/checks.json`, `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:a80e29ded728e74d8dfd1112901d5af2a0922d73a8fb9875a312458fde732ea0` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `82` |
| `langgraph_node_trace_hash` | `sha256:bc9ff336fce4723a0a2660f173f752029a9262886809b481f4c63e98a50022dd` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `82` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12280 | 生成初始 DSL 与 grounding seeds | initial len=2470 | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=488363 | LLM per-request accept/reject + repair | candidate len=2466,2921,3125,3267,3230 | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=351443 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=3, tokens=80976 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=488363 | LLM per-request accept/reject + repair | candidate len=2466,2921,3125,3267,3230 | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=351443 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=488363 | LLM per-request accept/reject + repair | candidate len=2466,2921,3125,3267,3230 | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=351443 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=488363 | LLM per-request accept/reject + repair | candidate len=2466,2921,3125,3267,3230 | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=351443 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=3, tokens=80976 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=488363 | LLM per-request accept/reject + repair | candidate len=2466,2921,3125,3267,3230 | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=351443 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=3, tokens=80976 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T12:51:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T12:51:26Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T12:51:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T12:51:26Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T12:53:14Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T12:53:14Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} |
... <truncated 9757 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|---|
| `default_init_enters_manual_and_sets_manual_outputs` | default-init verifies initial dispatch to Manual and manual operation sets pump speed from built-in switch, default flow...<truncated 44 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `initiate_change_setpoint_start_ac_to_normal_high_pressure` | default-init follows caregiver initiation through Ask_StartAC, setpoint change, StartAC, AutocontrolInit, and normal aut...<truncated 42 chars> | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `normal_autocontrol_low_pressure_raises_flow` | explicit-hot-start in AutocontrolNormal verifies normal autocontrol records data, uses control voltage, and raises flow ...<truncated 30 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `normal_autocontrol_no_fault_no_phantom_fault_transition` | explicit-hot-start in AutocontrolNormal with pump_fault clear verifies no fault transition occurs and equal pressure kee...<truncated 16 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_alarms_releases_control_then_fault_removed_manual` | explicit-hot-start in AutocontrolNormal with a pump fault verifies transition to PumpFault activates alarm and releases ...<truncated 46 chars> | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `terminate_ac_from_ask_and_init_returns_manual` | explicit-hot-start in Ask_StartAC verifies TerminateAC returns to Manual from Ask_StartAC, AutocontrolInit, and Autocont...<truncated 34 chars> | ⚪ | ✅ | ❌ | ✅ | ✅ |
| `back_manual_fallbacks_from_autocontrol_states` | explicit-hot-start in Ask_StartAC sweeps CA_backManual, CB_backManual, and CP_backManual fallbacks from distinct autocon...<truncated 30 chars> | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `cc_back_manual_fallback_from_pumpfault` | explicit-hot-start in PumpFault verifies CC_backManual shares Manual as recovery target while an uncleared fault keeps a...<truncated 31 chars> | ✅ | ✅ | ❌ | ✅ | ✅ |
| `ca_backmanual_from_pumpfault_forced_line_probe` | explicit-hot-start in PumpFault checks CA_backManual returns to Manual but does not by itself remove an active physical ...<truncated 71 chars> | ✅ | ✅ | ❌ | ✅ | ✅ |
| `terminate_ac_from_normal_returns_manual` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `direct_start_ac_wrong_target_and_effect_probe` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `direct_change_setpoint_self_transition_effect_probe` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `forced_backmanual_from_manual_reapplies_manual_outputs` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `direct_fault_removed_effect_value_probe` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `direct_initiate_ac_wrong_target_probe` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | initiate_change_setpoint_start_ac_to_normal_high_pressure, pump_fault_alarms_releases_control_then_fault_removed_manual, terminate_ac_from_ask_and_init_returns_manual, back_manual_fallbacks_from_autocontrol_states, direct_start_ac_wrong_target_and_effect_probe, ... +3 | accept=8, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:b33b133cba821c111f054a2fa54395c557d5c8d02a4ad00fe6eb009fbebe8fb1` |
| 2 | `1` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:61cd61b0a826f875c372d019f28b015e190455700584113ffdbf76fe40ead0f8` |
| 3 | `2` | ❌ | `SD-6` | terminate_ac_from_ask_and_init_returns_manual, cc_back_manual_fallback_from_pumpfault, ca_backmanual_from_pumpfault_forced_line_probe | accept=2, reject=1, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Resolve W_FORCED_OVERRIDES_NORMAL by eliminating the duplicate coverage between global forced CA_backManual and the source-specific PumpFault -> Manual : CA_backManual transiti...<truncated 749 chars> | `sha256:4e2c7794b7f3d7d4f0a53ce595461cb93e3e68723ba5bcd88b135ca5fea2ca90` |
| 4 | `2` | ✅ | `SD-6` | terminate_ac_from_ask_and_init_returns_manual, cc_back_manual_fallback_from_pumpfault, ca_backmanual_from_pumpfault_forced_line_probe | accept=3, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; forced_transition_count_drift; missing_required_grounding | `sha256:43f02231d93a2b1156f868a3906cfc7090d7450d3ef582f9fc8851317947b246` |
| 5 | `3` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:bf01076a8a36fd3168dd34e217b409eb1fba5c078b6c6c09b78f3eb607ff4dfd` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b/report.md` §7。

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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 27215, 'completion_tokens': 7954, 'total_tokens': 35169, 'estimated_prompt_tokens': 26632, 'estimated_completion_tokens': 6153, 'estimated_total_tokens': 32785, 'prompt_chars': 106522, 'completion_chars': 24609, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `150.641s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68/pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68/checks.json`, `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:70438247f63076c025a81d117762d939250aa97b788b38aef82c36e68af54bbd` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=10434 | 生成初始 DSL 与 grounding seeds | initial len=669 | [`record`](./pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13555 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=11180 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T12:51:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T12:51:26Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T12:51:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T12:51:26Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T12:52:40Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T12:52:40Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=669,hash=sha256:ffc4ea773d66 |
| 7 | `2026-06-05T12:52:40Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T12:52:40Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T12:52:40Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:ffc4ea773d6686384ce9f98fccefbeb9f4bc53fcb9928459112368750e06d971 |
| 10 | `2026-06-05T12:52:40Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T12:52:40Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=669,hash=sha256:ffc4ea773d66, current_hash=sha256:ffc4ea773d6686384ce9f98fccefbeb9f4bc53fcb9928459112368750e06d971 |
| 12 | `2026-06-05T12:52:40Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T12:52:40Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T12:52:40Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T12:52:40Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T12:52:40Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T12:52:40Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T12:52:40Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T12:52:40Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T12:52:40Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T12:52:40Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T12:52:40Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T12:53:20Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T12:53:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T12:53:21Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T12:53:21Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T12:53:21Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T12:53:21Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T12:53:21Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T12:53:21Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T12:53:21Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T12:53:21Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T12:53:56Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T12:53:56Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T12:53:56Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T12:53:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T12:53:56Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T12:53:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T12:53:56Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=669,hash=sha256:ffc4ea773d66 |
| 40 | `2026-06-05T12:53:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T12:53:56Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=669,hash=sha256:ffc4ea773d66 |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_floor1_no_request_stays_stopped` | default-init dispatches to floor F1 with stop output, then with no request event the controller remains stopped on F1. | ✅ |
| `f1_to_f2_then_f2_to_f3_upward_workflow` | default-init workflow covers F1 PS2 upward travel to F2, arrival stop, then F2 PS3 upward travel to F3 and stop. | ✅ |
| `f1_to_f3_then_down_to_f2_workflow` | default-init workflow covers F1 PS3 upward travel to F3, arrival stop, then F3 PS2 downward travel to F2 and stop. | ✅ |
| `f2_request_floor1_downward_arrival` | explicit-hot-start from reachable F2 probes PS1 selecting downward MD1 and S1 arrival back to stopped F1. | ✅ |
| `f3_request_floor1_downward_arrival` | explicit-hot-start from reachable F3 probes PS1 selecting downward MD1 and S1 arrival back to stopped F1. | ✅ |
| `reset_from_upward_motion_states` | explicit-hot-start probes forced Reset from upward motion, then re-enters another upward motion and confirms Reset again...<truncated 19 chars> | ✅ |
| `reset_from_floor_and_downward_motion` | explicit-hot-start probes forced Reset from a floor context and, after creating downward MD2 travel, from a downward mot...<truncated 12 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3477, 'completion_chars': 12024, 'completion_tokens': 3996, 'elapsed_seconds': 74.00963434798177, 'estimated_completion_tokens': 3006, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 9529, 'first_chunk_seconds': 11.58699238797999, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10434}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1554, 'completion_chars': 5844, 'completion_tokens': 2073, 'elapsed_seconds': 40.04364877101034, 'estimated_completion_tokens': 1461, 'estimated_prompt_tokens': 11248, 'estimated_total_tokens': 12709, 'first_chunk_seconds': 12.594270311004948, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 44990, 'prompt_tokens': 11482, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13555}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1524, 'completion_chars': 6741, 'completion_tokens': 1885, 'elapsed_seconds': 35.46502295698156, 'estimated_completion_tokens': 1686, 'estimated_prompt_tokens': 8861, 'estimated_total_tokens': 10547, 'first_chunk_seconds': 8.310213418997591, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 35443, 'prompt_tokens': 9295, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 11180}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path1_elevator-default-lg-b1-post-accept-bc94bda6-c9a25e68/report.md` §7。

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
def float Pbatt_dis_max = 0.0;
def float Pg_req = 0.0;
def float Pd1_req = 0.0;
def float Pd2_req = 0.0;
def float Pbat_dis = 0.0;
def float Pbat_chg = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 0;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 0;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 0;
def int cmd_load_cut_in = 0;
def int cmd_load_cut_out = 0;
def int illegal_overload_state = 0;

state LNGShipEMS {
    ! * -> PLZeroCharge : if [PL == 0 && SoC < 0.95];
    ! * -> PLZeroSpare : if [PL == 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> RESBatteryDischarge : if [Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbatt_dis_max];
    ! * -> LNGCoversDemand : if [Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbatt_dis_max && PL - Ppv - Pw <= eng3_Pmax];
    ! * -> LNGCoversAndChargesLowSoC : if [Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= eng3_Pmax];
    ! * -> LNGCoversDemand : if [Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= eng3_Pmax && PL - Ppv - Pw + Pgmax / 5 > eng3_Pmax];
    ! * -> LNGDG1CoversDemand : if [Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pd1max];
    ! * -> LNGDG1CoversAndChargesLowSoC : if [Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= eng3_Pmax + Pd1max];
    ! * -> LNGDG1CoversDemand : if [Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pd1max && PL - Ppv - Pw + Pd1max / 10 > eng3_Pmax + Pd1max];
    ! * -> LNGDG1DG2CoversDemand : if [Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > eng3_Pmax + Pd1max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max];
    ! * -> LNGDG1DG2CoversAndChargesLowSoC : if [Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > eng3_Pmax + Pd1max && PL - Ppv - Pw + Pd1max / 10 <= eng3_Pmax + Pd1max + Pd2max];
    ! * -> LNGDG1DG2CoversDemand : if [Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > eng3_Pmax + Pd1max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max && PL - Ppv - Pw + Pd1max / 10 > eng3_Pmax + Pd1max + Pd2max];
    ! * -> ExtremeDemandBatteryLack : if [Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax + Pd1max + Pd2max];

    [*] -> PLZeroCharge;

    state PLZeroCharge {
        enter {
            Pg_req = 0;
            Pd1_req = 0;
            Pd2_req = 0;
            Pbat_dis = 0;
            Pbat_chg = Ppv + Pw;
            Pspare = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
            illegal_overload_state = 0;
        }
    }

    state PLZeroSpare {
        enter {
            Pg_req = 0;
            Pd1_req = 0;
            Pd2_req = 0;
            Pbat_dis = 0;
            Pbat_chg = 0;
            Pspare = Ppv + Pw;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
            illegal_overload_state = 0;
        }
    }

    state RESCoversCharge {
        enter {
            Pg_req = 0;
            Pd1_req = 0;
            Pd2_req = 0;
            Pbat_dis = 0;
            Pbat_chg = Ppv + Pw - PL;
            Pspare = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
            illegal_overload_state = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pg_req = 0;
            Pd1_req = 0;
            Pd2_req = 0;
            Pbat_dis = 0;
            Pbat_chg = 0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
            illegal_overload_state = 0;
        }
    }

    state RESBatteryDischarge {
        enter {
            Pg_req = 0;
            Pd1_req = 0;
            Pd2_req = 0;
            Pbat_dis = PL - Ppv - Pw;
            Pbat_chg = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 0;
            cmd_LNG_cut_out = 1;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
            illegal_overload_state = 0;
        }
    }

    state LNGCoversDemand {
        enter {
            Pg_req = PL - Ppv - Pw;
            Pd1_req = 0;
            Pd2_req = 0;
            Pbat_dis = 0;
            Pbat_chg = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
            illegal_overload_state = 0;
        }
    }

    state LNGCoversAndChargesLowSoC {
        enter {
            Pg_req = PL - Ppv - Pw + Pgmax / 5;
            Pd1_req = 0;
            Pd2_req = 0;
            Pbat_dis = 0;
            Pbat_chg = Pgmax / 5;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 0;
            cmd_DG1_cut_out = 1;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
            illegal_overload_state = 0;
        }
    }

    state LNGDG1CoversDemand {
        enter {
            Pg_req = eng3_Pmax;
            Pd1_req = PL - Ppv - Pw - eng3_Pmax;
            Pd2_req = 0;
            Pbat_dis = 0;
            Pbat_chg = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
            illegal_overload_state = 0;
        }
    }

    state LNGDG1CoversAndChargesLowSoC {
        enter {
            Pg_req = eng3_Pmax;
            Pd1_req = PL - Ppv - Pw + Pd1max / 10 - eng3_Pmax;
            Pd2_req = 0;
            Pbat_dis = 0;
            Pbat_chg = Pd1max / 10;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 0;
            cmd_DG2_cut_out = 1;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
            illegal_overload_state = 0;
        }
    }

    state LNGDG1DG2CoversDemand {
        enter {
            Pg_req = eng3_Pmax;
            Pd1_req = Pd1max;
            Pd2_req = PL - Ppv - Pw - eng3_Pmax - Pd1max;
            Pbat_dis = 0;
            Pbat_chg = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
            illegal_overload_state = 0;
        }
    }

    state LNGDG1DG2CoversAndChargesLowSoC {
        enter {
            Pg_req = eng3_Pmax;
            Pd1_req = Pd1max;
            Pd2_req = PL - Ppv - Pw + Pd1max / 10 - eng3_Pmax - Pd1max;
            Pbat_dis = 0;
            Pbat_chg = Pd1max / 10;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
            illegal_overload_state = 0;
        }
    }

    state ExtremeDemandBatteryLack {
        enter {
            Pg_req = eng3_Pmax;
            Pd1_req = Pd1max;
            Pd2_req = Pd2max;
            Pbat_dis = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbat_chg = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
            cmd_load_cut_in = 1;
            cmd_load_cut_out = 0;
            illegal_overload_state = 1;
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `3` / `3` / `2` / `8` |
| token / elapsed | `{'prompt_tokens': 578162, 'completion_tokens': 64259, 'total_tokens': 642421, 'estimated_prompt_tokens': 563291, 'estimated_completion_tokens': 43081, 'estimated_total_tokens': 606372, 'prompt_chars': 2253138, 'completion_chars': 172301, 'n_calls': 16, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1232.922s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947/pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947/checks.json`, `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:4068272421a934ec432639f749b0326182e330a13a44f83941dd77fbbdc7de0e` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `54` |
| `langgraph_node_trace_hash` | `sha256:fa8465e9e75a1e5e29f7279d2c4fbdda21633baf66f1eaf9c37accd20e6d8101` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `54` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=13887 | 生成初始 DSL 与 grounding seeds | initial len=8111 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=183, info=0; blocking=0, advisory=219, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=171089 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=171089 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=171089 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=169037 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=188774 | LLM per-request accept/reject + repair | candidate len=8189,8627,9128 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=99634 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=188774 | LLM per-request accept/reject + repair | candidate len=8189,8627,9128 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=99634 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=183, info=0; blocking=0, advisory=219, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=171089 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=171089 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=169037 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=188774 | LLM per-request accept/reject + repair | candidate len=8189,8627,9128 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=99634 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=181, info=0; blocking=0, advisory=183, info=0; blocking=0, advisory=219, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=171089 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=169037 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T12:51:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T12:51:26Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T12:51:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T12:51:26Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T12:53:43Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T12:53:43Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=8111,hash=sha256:ed3b080f3cb6 |
| 7 | `2026-06-05T12:53:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T12:53:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T12:53:43Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:ed3b080f3cb69b474f26fd02d05661fc2cfa801e82e412b199f90c7ca9c4ebaf |
| 10 | `2026-06-05T12:53:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T12:53:43Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=8111,hash=sha256:ed3b080f3cb6, current_hash=sha256:ed3b080f3cb69b474f26fd02d05661fc2cfa801e82e412b199f90c7ca9c4ebaf |
| 12 | `2026-06-05T12:53:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T12:53:43Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T12:53:43Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T12:53:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T12:53:43Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T12:53:43Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T12:53:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T12:53:43Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T12:53:43Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T12:53:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T12:53:43Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T12:55:02Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T12:55:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T12:55:03Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T12:55:03Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T12:55:03Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T12:56:17Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T12:56:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T12:56:18Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T12:56:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T12:56:18Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T12:58:06Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T12:58:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T12:58:07Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T12:58:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T12:58:07Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T12:58:07Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T12:58:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T12:58:07Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T12:58:07Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-05T12:58:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T12:58:07Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 44 | `2026-06-05T12:59:05Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 45 | `2026-06-05T12:59:05Z` | `SL-7` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 46 | `2026-06-05T12:59:05Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 47 | `2026-06-05T12:59:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-05T12:59:05Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["NL: 'The overload completion state is illegal... and the state shall never occur in practice.'", "DSL guard makes the state reachable: '! * -> ExtremeDemandBatteryLack : if [Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax
... <truncated 5053 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| `default_init_pl_zero_charge_classification` | default-init: with PL=0, RES present, and SoC below 0.95, initial dispatch reaches PLZeroCharge and the classification g...<truncated 42 chars> | ✅ | ✅ | ✅ |
| `pl_zero_spare_soc_boundary` | explicit-hot-start: at PL=0 with RES present and SoC exactly 0.95, RES production should be spare rather than battery ch...<truncated 5 chars> | ✅ | ✅ | ✅ |
| `res_covers_charge_below_soc_boundary` | explicit-hot-start: when RES covers positive PL and SoC is just below 0.95, demand is served from RES and surplus charge...<truncated 14 chars> | ✅ | ✅ | ✅ |
| `res_covers_spare_at_soc_boundary` | explicit-hot-start: when RES covers positive PL and SoC is exactly 0.95, residual RES should be reported as spare power. | ✅ | ✅ | ✅ |
| `battery_discharge_at_soc_and_capacity_boundary` | explicit-hot-start: with RES below PL, SoC exactly 0.2, and deficit equal to battery discharge capacity, batteries shoul...<truncated 35 chars> | ✅ | ✅ | ✅ |
| `lng_covers_demand_at_engine_boundary` | explicit-hot-start: after battery capacity is insufficient, LNG should cover the remaining deficit when it is exactly wi...<truncated 15 chars> | ✅ | ✅ | ✅ |
| `low_soc_lng_margin_charge` | explicit-hot-start: with low SoC below 0.2, LNG should cover demand plus the Pgmax/5 charging margin when within eng3_Pm...<truncated 3 chars> | ✅ | ✅ | ✅ |
| `lng_dg1_covers_after_lng_capacity` | explicit-hot-start: when SoC is suitable and deficit exceeds LNG capacity but is within LNG plus DG1, LNG and DG1 should...<truncated 30 chars> | ✅ | ✅ | ✅ |
| `low_soc_lng_dg1_margin_charge` | explicit-hot-start: with low SoC, the later diesel-generator branch should include the Pd1max/10 charging margin while u...<truncated 17 chars> | ✅ | ✅ | ✅ |
| `lng_dg1_dg2_covers_after_dg1_capacity` | explicit-hot-start: when suitable-SoC deficit exceeds LNG plus DG1 but is within LNG plus DG1 plus DG2, all three therma...<truncated 28 chars> | ✅ | ✅ | ✅ |
| `low_soc_lng_dg1_dg2_margin_charge` | explicit-hot-start: in the low-SoC DG2 branch, all thermal units should cover demand and include the Pd1max/10 battery c...<truncated 15 chars> | ✅ | ✅ | ✅ |
| `extreme_demand_battery_lack_illegal_completion` | explicit-hot-start: although this overload completion state should not occur in practice, if extreme demand exceeds all ...<truncated 103 chars> | ✅ | ✅ | ✅ |
| `default_init_then_forced_reclassifies_to_res_spare` | default-init: after the initial leaf dispatch, current inputs with positive load, RES covering PL, and SoC at 0.95 must ...<truncated 97 chars> | ✅ | ✅ | ✅ |
| `forced_reclassification_from_extreme_to_pl_zero_spare` | explicit-hot-start: from the concrete ExtremeDemandBatteryLack leaf, PL=0 with full-SoC RES production must use the wild...<truncated 53 chars> | ✅ | ✅ | ✅ |
| `forced_reclassification_from_charge_to_lng_dg1` | explicit-hot-start: from PLZeroCharge, a changed positive-load deficit exceeding LNG but within LNG plus DG1 must use th...<truncated 66 chars> | ✅ | ✅ | ✅ |
| `forced_reclassification_from_lng_dg1_to_battery` | explicit-hot-start: from LNGDG1CoversDemand, a changed suitable-SoC deficit equal to battery discharge capacity must use...<truncated 75 chars> | ✅ | ✅ | ✅ |
| `forced_reclassification_from_spare_to_extreme_demand` | explicit-hot-start: from RESCoversSpare, an extreme demand input must be globally reclassified to the illegal completion...<truncated 63 chars> | ⚪ | ✅ | ✅ |
| `forced_reclassification_from_battery_to_low_soc_dg2_margin` | explicit-hot-start: from RESBatteryDischarge, a low-SoC deficit requiring LNG, DG1, DG2, and the Pd1max/10 charging marg...<truncated 58 chars> | ⚪ | ✅ | ✅ |
| `forced_reclassification_from_res_spare_to_pl_zero_charge` | explicit-hot-start: from RESCoversSpare, changed inputs with PL=0, RES present, and SoC below 0.95 must use the wildcard...<truncated 95 chars> | ⚪ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Repair the ExtremeDemandBatteryLack forced guard so the scenario `extreme_demand_battery_lack_illegal_completion` reaches `LNGShipEMS.ExtremeDemandBatteryLack` for PL=210, Ppv=...<truncated 684 chars> | `sha256:b3396f1ec57d9d2044735c1aea2c0f6315a06d10f17a55e93c9e2e2d733ef983` |
| 2 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:20198f3d70f865a8c3018807341140563003c19177ac48367663b0d9d713410d` |
| 3 | `1` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | `sha256:b299f55ba8d3f240806c4d8573579406250dcb0d00a840d50b42a4342711af3c` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_post_accept_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-post-accept-bc94bda6-515b0947/report.md` §7。

</details>
