## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | post-accept | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 32754 | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ❌ | ⚪ | ⚪ 0 | `success_but_weak_oracle_ineligible` | 503915 | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 34949 | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ❌ | ❌ | ⚪ 0 | `success_but_weak_oracle_ineligible` | 153417 | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae/report.md` |

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
- node trace count 范围：min=16，max=67；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：4/4 success，rejected=0，budget_exhausted=0，total_tokens=725035。
  - SC-11 post-accept validation：0 run 触发；本组 evidence 只能证明 non-regression / budget-policy 口径，不能声称真实覆盖 post-accept branch。
- 主结果候选：当前 2/4 个非 infrastructure run 可进入 main_result_eligible；provider/network invalid=0 个，只能作为 infrastructure evidence。

### 主结果候选 vs Path2 ref-model 蓝本边界

- Path2 run-validity：0/1 个 Path2 run 的 `main_result_eligible=true`；这只表示 run/schema/secret/trace/final verdict 可进入主结果候选。
- Path2 blueprint-validity：0/1 个 Path2 run 当前可作为 `path2_ref_model_blueprint_eligible=true`；该字段比 `main_result_eligible` 更严格。
- `path2_lng_ems`：main_result_eligible=`false`，path2_ref_model_blueprint_eligible=`false`，state_mode_decorative=`true`；reason=run_not_main_result_eligible
- 解释：`path2_ref_model_blueprint_eligible=false` 不会把有效 run 改成 provider invalid；它只禁止把 state-mode-decorative / 条件分类式模型宣传为 Path2 ref-model 主蓝本。

### 主要失败模式

- `success`：2 run(s)。
- `success_but_weak_oracle_ineligible`：2 run(s)。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=success_but_weak_oracle_ineligible，最大 observed iteration_count=4。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=success_but_weak_oracle_ineligible，最大 observed iteration_count=1。
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
        enter { k1 = 1; k2 = 0; n = 0; }
    }

    state hold {
        enter { k1 = 0; k2 = 0; n = 0; }
    }

    state decrease {
        enter { k1 = 0; k2 = 1; n = 500; }
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
| token / elapsed | `{'prompt_tokens': 25876, 'completion_tokens': 6878, 'total_tokens': 32754, 'estimated_prompt_tokens': 25371, 'estimated_completion_tokens': 4943, 'estimated_total_tokens': 30314, 'prompt_chars': 101481, 'completion_chars': 19767, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `138.842s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2/pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2/checks.json`, `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:f73f41ef934f7d0398a87e33f714fb279f523cdf1d1458086a4d1d049d063c74` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=8790 | 生成初始 DSL 与 grounding seeds | initial len=476 | [`record`](./pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=12057 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=11907 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T14:38:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T14:38:49Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T14:38:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T14:38:49Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T14:39:36Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T14:39:36Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=476,hash=sha256:63f75637003a |
| 7 | `2026-06-05T14:39:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T14:39:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T14:39:36Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:63f75637003abfa638ffbe17c57f773411fbffbf694d3b3b8850efb728b3f8b8 |
| 10 | `2026-06-05T14:39:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T14:39:36Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=476,hash=sha256:63f75637003a, current_hash=sha256:63f75637003abfa638ffbe17c57f773411fbffbf694d3b3b8850efb728b3f8b8 |
| 12 | `2026-06-05T14:39:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T14:39:36Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T14:39:36Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T14:39:36Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T14:39:36Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T14:39:37Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T14:39:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T14:39:37Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T14:39:37Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T14:39:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T14:39:37Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T14:40:21Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T14:40:21Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T14:40:22Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T14:40:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T14:40:22Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T14:40:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T14:40:22Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T14:40:22Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T14:40:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T14:40:22Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T14:41:07Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T14:41:07Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T14:41:07Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T14:41:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T14:41:07Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T14:41:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T14:41:07Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=476,hash=sha256:63f75637003a |
| 40 | `2026-06-05T14:41:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T14:41:07Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=476,hash=sha256:63f75637003a |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_enters_increase_outputs` | default-init dispatches the root initial transition to increase and asserts the inlet-valve/pump command outputs require...<truncated 15 chars> | ✅ |
| `increase_to_hold_at_slp_upper_boundary` | explicit-hot-start in increase probes the inclusive slp <= 0.01 boundary and verifies hold neutralizes both valves. | ✅ |
| `increase_no_fire_just_above_upper_boundary` | explicit-hot-start in increase probes just above slp 0.01 so the increase-to-hold guard must not fire. | ✅ |
| `hold_to_increase_above_upper_boundary` | explicit-hot-start in hold probes slp > 0.01 and verifies transition target increase with inlet valve commanded on. | ✅ |
| `hold_no_fire_at_upper_boundary` | explicit-hot-start in hold probes the non-inclusive slp > 0.01 threshold so exactly 0.01 must not enter increase. | ✅ |
| `hold_to_decrease_below_lower_boundary` | explicit-hot-start in hold probes slp < -0.01 and verifies transition target decrease with return valve and pump release...<truncated 9 chars> | ✅ |
| `hold_no_fire_at_lower_boundary` | explicit-hot-start in hold probes the non-inclusive slp < -0.01 threshold so exactly -0.01 must not enter decrease. | ✅ |
| `decrease_to_hold_at_lower_boundary` | explicit-hot-start in decrease probes the inclusive slp >= -0.01 boundary and verifies hold neutralizes valves and pump. | ✅ |
| `decrease_no_fire_below_lower_boundary` | explicit-hot-start in decrease probes just below slp -0.01 so the decrease-to-hold guard must not fire. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1878, 'completion_chars': 6374, 'completion_tokens': 2397, 'elapsed_seconds': 47.15611094702035, 'estimated_completion_tokens': 1594, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 8087, 'first_chunk_seconds': 12.27588276102324, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 8790}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1561, 'completion_chars': 5792, 'completion_tokens': 2263, 'elapsed_seconds': 44.88314315199386, 'estimated_completion_tokens': 1448, 'estimated_prompt_tokens': 9662, 'estimated_total_tokens': 11110, 'first_chunk_seconds': 16.783032156992704, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 38648, 'prompt_tokens': 9794, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12057}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1699, 'completion_chars': 7601, 'completion_tokens': 2218, 'elapsed_seconds': 45.76300821400946, 'estimated_completion_tokens': 1901, 'estimated_prompt_tokens': 9216, 'estimated_total_tokens': 11117, 'first_chunk_seconds': 15.084571847022744, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 36861, 'prompt_tokens': 9689, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 11907}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_abs-default-lg-b1-prompt-scope-07bd58c1-4edd0af2/report.md` §7。

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
def int alarm_active = 0;
def int control_released = 1;
def int infusion_log_records = 0;
def float patient_bp = 0.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_sensor_buffer = 0.0;
def float manual_default_flow_rate = 1.0;
def float default_flow_rate = 1.0;
def float pressure_gain = 0.01;
def float flow_rate = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! * -> Manual :: TerminateAC;

        >> during before { shared_sensor_buffer = patient_bp; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                if [pump_fault > 0] {
                    alarm_active = 1;
                } else {
                    alarm_active = 0;
                }
                control_released = 1;
            }
            during {
                pump_speed = manual_switch_speed;
                flow_rate = manual_default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 1;
                if [pump_fault > 0] {
                    alarm_active = 1;
                    control_released = 1;
                } else {
                    alarm_active = 0;
                }
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 2;
                if [pump_fault > 0] {
                    control_released = 1;
                    alarm_active = 1;
                } else {
                    control_released = 0;
                    alarm_active = 0;
                    flow_rate = default_flow_rate;
                }
            }
        }

        state Autocontrol {
            enter {
                CA_mode = 3;
                control_released = 0;
                alarm_active = 0;
            }
            during {
                if [pump_fault == 0] {
                    if [patient_bp > target_bp] {
                        flow_rate = default_flow_rate - ((patient_bp - target_bp) * pressure_gain);
                    } else {
                        flow_rate = default_flow_rate + ((target_bp - patient_bp) * pressure_gain);
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    infusion_log_records = infusion_log_records + 1;
                }
            }
        }

        state PumpFault {
            enter {
                CA_mode = 4;
                alarm_active = 1;
                control_released = 1;
            }
        }

        Manual -> Manual : /Mode_Control_Algorithm.PumpFault.FaultRemoved effect { pump_fault = 0; alarm_active = 0; };
        Manual -> Manual : if [pump_fault > 0] effect { alarm_active = 1; control_released = 1; };
        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> PumpFault : if [pump_fault > 0];
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> PumpFault : if [pump_fault > 0];
        AutocontrolInit -> Autocontrol;
        Autocontrol -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `4` / `3` / `3` / `9` |
| token / elapsed | `{'prompt_tokens': 450873, 'completion_tokens': 53042, 'total_tokens': 503915, 'estimated_prompt_tokens': 476642, 'estimated_completion_tokens': 42129, 'estimated_total_tokens': 518771, 'prompt_chars': 1906538, 'completion_chars': 168498, 'n_calls': 16, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1020.578s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216/pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216/checks.json`, `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:da30a6c4b1a20de3548241767d6c27b40f011c2d6238c9cc64991eb8518cd99e` |
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
| `langgraph_node_trace_hash` | `sha256:059f8d273595b859e15b7cce0f2aff428bc9864b86b859ad2b67292ed3469c76` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=13835 | 生成初始 DSL 与 grounding seeds | initial len=2821 | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=153860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=79170 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=133063 | LLM per-request accept/reject + repair | candidate len=2944,3064,3617 | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=123987 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=153860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=153860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=133063 | LLM per-request accept/reject + repair | candidate len=2944,3064,3617 | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=123987 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=153860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=79170 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=133063 | LLM per-request accept/reject + repair | candidate len=2944,3064,3617 | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=123987 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=153860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=153860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=79170 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T14:38:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T14:38:49Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T14:38:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T14:38:49Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T14:41:05Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T14:41:05Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2821,hash=sha256:482015188fe1 |
| 7 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T14:41:05Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:482015188fe1f54616d4b49e12679f832c1bafb562ab1960150d6a29964e23ee |
| 10 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T14:41:05Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2821,hash=sha256:482015188fe1, current_hash=sha256:482015188fe1f54616d4b49e12679f832c1bafb562ab1960150d6a29964e23ee |
| 12 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T14:41:05Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T14:41:05Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T14:41:05Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T14:41:05Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T14:41:05Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T14:41:05Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T14:41:05Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T14:42:24Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T14:42:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T14:42:25Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T14:42:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T14:42:25Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T14:42:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T14:42:25Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T14:42:25Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T14:42:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T14:42:25Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T14:43:21Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T14:43:21Z` | `SL-7` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T14:43:21Z` | `SL-7` | `0` | `grounding_update_hints_rec
... <truncated 6585 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 |
|---|---|---|---|---|---|
| `default_init_manual_operation_outputs` | default-init dispatches into Manual and verifies manual switch speed, manual default flow, and sensor buffering obligati...<truncated 4 chars> | ✅ | ✅ | ✅ | ✅ |
| `initiate_change_setpoint_start_autocontrol` | default-init reaches Manual, then caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, and reaches ...<truncated 19 chars> | ✅ | ✅ | ✅ | ✅ |
| `autocontrol_no_fault_low_pressure_stays_controlled` | explicit-hot-start in Autocontrol with no pump fault verifies no phantom fault transition and higher flow for below-targ...<truncated 12 chars> | ✅ | ✅ | ✅ | ✅ |
| `autocontrol_fault_enters_pumpfault` | explicit-hot-start in Autocontrol with pump_fault present verifies fault transition to PumpFault, alarm activation, and ...<truncated 25 chars> | ✅ | ✅ | ✅ | ✅ |
| `fault_removed_returns_manual` | explicit-hot-start in PumpFault verifies caregiver fault removal returns to Manual and clears the fault for manual recov...<truncated 4 chars> | ✅ | ✅ | ✅ | ✅ |
| `ca_and_cb_forced_back_manual` | explicit-hot-start probes two cross-component backManual forced fallbacks from Autocontrol and Ask_StartAC to the shared...<truncated 15 chars> | ✅ | ✅ | ✅ | ✅ |
| `cp_and_cc_forced_back_manual` | explicit-hot-start probes CP_backManual from PumpFault with a still-present fault and CC_backManual from AutocontrolInit...<truncated 49 chars> | ✅ | ❌ | ✅ | ✅ |
| `terminate_ac_forced_manual_recovery` | explicit-hot-start in Autocontrol verifies caregiver TerminateAC releases algorithmic control and returns to Manual. | ✅ | ✅ | ✅ | ✅ |
| `manual_self_forced_backmanual_reentry` | explicit-hot-start in Manual with stale mode/control flags verifies CA_backManual is still a forced fallback that re-ent...<truncated 88 chars> | ⚪ | ✅ | ✅ | ✅ |
| `manual_self_terminate_forced_reentry` | explicit-hot-start in Manual with stale mode/control flags verifies TerminateAC is a forced fallback to Manual, detectin...<truncated 79 chars> | ⚪ | ✅ | ✅ | ✅ |
| `ask_startac_fault_guard_targets_pumpfault` | explicit-hot-start in Ask_StartAC with unresolved pump fault verifies the fault guard targets PumpFault and applies alar...<truncated 26 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `changesetpoint_unique_effect_value` | explicit-hot-start in Ask_StartAC verifies ChangeSetpoint self-transition preserves Ask_StartAC and assigns target_bp fr...<truncated 64 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `pumpfault_faultremoved_unique_clear_effect` | explicit-hot-start in PumpFault verifies FaultRemoved targets Manual and clears a nonzero pump_fault value, catching wro...<truncated 45 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `startac_isolated_target_and_init_outputs` | explicit-hot-start in Ask_StartAC without a fault verifies StartAC targets AutocontrolInit and applies initialization ou...<truncated 29 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `initiateac_isolated_target_and_entry_outputs` | explicit-hot-start in Manual verifies caregiver InitiateAC targets Ask_StartAC exactly and applies the Ask_StartAC mode/...<truncated 20 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `autocontrolinit_to_autocontrol_unique_outputs` | explicit-hot-start in AutocontrolInit without a fault verifies the automatic transition targets Autocontrol and computes...<truncated 51 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `autocontrolinit_fault_guard_targets_pumpfault` | explicit-hot-start in AutocontrolInit with unresolved pump fault verifies the fault guard targets PumpFault rather than ...<truncated 61 chars> | ⚪ | ⚪ | ⚪ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:54fcdf1734e5639aa745de3c8846c7e22b53507fb28768bc8d6a2d53846a301c` |
| 2 | `1` | ✅ | `SD-6` | cp_and_cc_forced_back_manual | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:5ff9d43b7100f6a2a25bd3b281247b1d0f8978779233f97647f7342ab4639666` |
| 3 | `2` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:d48663b271a8682c7ee1717bf559731df76d03215d4145494e6940c0c7416d7a` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216/report.md` §7。

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
| token / elapsed | `{'prompt_tokens': 26751, 'completion_tokens': 8198, 'total_tokens': 34949, 'estimated_prompt_tokens': 26098, 'estimated_completion_tokens': 6202, 'estimated_total_tokens': 32300, 'prompt_chars': 104388, 'completion_chars': 24806, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `157.723s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450/pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450/checks.json`, `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:9cd415beb6c70e957bd7c2fd5ba0c79db6cc1dcb96bb43c8c1ffd1b41dac3582` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=10385 | 生成初始 DSL 与 grounding seeds | initial len=669 | [`record`](./pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13876 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10688 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T14:38:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T14:38:49Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T14:38:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T14:38:49Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T14:40:02Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T14:40:02Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=669,hash=sha256:f01d793ff735 |
| 7 | `2026-06-05T14:40:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T14:40:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T14:40:02Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:f01d793ff73542443089e3b4ce8b98c438d4cd4be9a79525664c83dccc1e4c1c |
| 10 | `2026-06-05T14:40:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T14:40:02Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=669,hash=sha256:f01d793ff735, current_hash=sha256:f01d793ff73542443089e3b4ce8b98c438d4cd4be9a79525664c83dccc1e4c1c |
| 12 | `2026-06-05T14:40:02Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T14:40:02Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T14:40:03Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T14:40:03Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T14:40:03Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T14:40:03Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T14:40:03Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T14:40:03Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T14:40:03Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T14:40:03Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T14:40:03Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T14:40:50Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T14:40:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T14:40:50Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T14:40:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T14:40:50Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T14:40:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T14:40:50Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T14:40:50Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T14:40:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T14:40:50Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T14:41:26Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T14:41:26Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T14:41:26Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T14:41:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T14:41:26Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T14:41:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T14:41:26Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=669,hash=sha256:f01d793ff735 |
| 40 | `2026-06-05T14:41:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T14:41:26Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=669,hash=sha256:f01d793ff735 |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_then_up_to_f2_and_f3` | default-init verifies initial floor 1 stop, F1 PS2 upward travel to MU2, arrival at F2 stop, then immediate next request...<truncated 41 chars> | ✅ |
| `f1_direct_request_to_f3` | explicit-hot-start from F1 verifies PS3 selects direct upward MU3 travel and S3 arrival stops at F3 | ✅ |
| `f2_request_down_to_f1` | explicit-hot-start from F2 verifies PS1 selects downward MD1 travel and S1 arrival returns to F1 stop | ✅ |
| `f3_request_down_to_f2` | explicit-hot-start from F3 verifies PS2 selects downward MD2 travel and S2 arrival stops at F2 | ✅ |
| `f3_request_down_to_f1` | explicit-hot-start from F3 verifies PS1 selects downward MD1 travel and S1 arrival stops at F1 | ✅ |
| `reset_forces_motion_state_to_f1` | explicit-hot-start from an upward motion state verifies reset forces the controller back to floor 1 stop regardless of o...<truncated 25 chars> | ✅ |
| `reset_forces_floor_state_to_f1` | explicit-hot-start from a non-F1 floor state verifies reset forces the controller back to floor 1 stop regardless of out...<truncated 24 chars> | ✅ |
| `no_request_stays_stopped_on_f1` | explicit-hot-start from F1 verifies that without any request or reset event the controller remains stopped on floor 1 | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3428, 'completion_chars': 11696, 'completion_tokens': 3947, 'elapsed_seconds': 73.39987104700413, 'estimated_completion_tokens': 2924, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 9447, 'first_chunk_seconds': 12.229581997002242, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10385}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1894, 'completion_chars': 7538, 'completion_tokens': 2413, 'elapsed_seconds': 47.45598614102346, 'estimated_completion_tokens': 1885, 'estimated_prompt_tokens': 11203, 'estimated_total_tokens': 13088, 'first_chunk_seconds': 13.309675937023712, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 44812, 'prompt_tokens': 11463, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13876}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1319, 'completion_chars': 5572, 'completion_tokens': 1838, 'elapsed_seconds': 35.80994834902231, 'estimated_completion_tokens': 1393, 'estimated_prompt_tokens': 8372, 'estimated_total_tokens': 9765, 'first_chunk_seconds': 12.01527761502075, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 33487, 'prompt_tokens': 8850, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10688}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path1_elevator-default-lg-b1-prompt-scope-07bd58c1-8e511450/report.md` §7。

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
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charging_power = 0.0;
def float spare_power = 0.0;
def int cmd_LNG_cutin = 0;
def int cmd_LNG_cutout = 1;
def int cmd_DG1_cutin = 0;
def int cmd_DG1_cutout = 1;
def int cmd_DG2_cutin = 0;
def int cmd_DG2_cutout = 1;
def int cmd_load_cutin = 0;
def int cmd_load_cutout = 1;
def int illegal_overload = 0;

state LNGShipEMS {
    ! * -> ZeroLoadNoRES : if [PL == 0 && Ppv + Pw <= 0];
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RESCoverCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoverSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGCoverLowSoCCharge : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= eng3_Pmax];
    ! * -> LNGCover : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= eng3_Pmax];
    ! * -> LNGDG1LowSoCCharge : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pd1max];
    ! * -> LNGDG1 : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pd1max];
    ! * -> LNGDG1DG2 : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax + Pd1max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max];
    ! * -> ExtremeOverloadBatterySupport : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoadNoRES;

    state ZeroLoadNoRES {
        during {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 0;
            cmd_load_cutout = 1;
            illegal_overload = 0;
        }
    }

    state ZeroLoadCharge {
        during {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw;
            spare_power = 0.0;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 0;
            cmd_load_cutout = 1;
            illegal_overload = 0;
        }
    }

    state ZeroLoadSpare {
        during {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 0;
            cmd_load_cutout = 1;
            illegal_overload = 0;
        }
    }

    state RESCoverCharge {
        during {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state RESCoverSpare {
        during {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state BatteryDischarge {
        during {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LNGCoverLowSoCCharge {
        during {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5;
            battery_discharge_power = 0.0;
            battery_charging_power = Pgmax / 5;
            spare_power = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LNGCover {
        during {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG1LowSoCCharge {
        during {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10;
            battery_discharge_power = 0.0;
            battery_charging_power = Pd1max / 10;
            spare_power = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 1;
            cmd_DG1_cutout = 0;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG1 {
        during {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 1;
            cmd_DG1_cutout = 0;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state LNGDG1DG2 {
        during {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 1;
            cmd_DG1_cutout = 0;
            cmd_DG2_cutin = 1;
            cmd_DG2_cutout = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 0;
        }
    }

    state ExtremeOverloadBatterySupport {
        during {
            requested_generator_power = eng3_Pmax + Pd1max + Pd2max;
            battery_discharge_power = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            battery_charging_power = 0.0;
            spare_power = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 1;
            cmd_DG1_cutout = 0;
            cmd_DG2_cutin = 1;
            cmd_DG2_cutout = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_overload = 1;
        }
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success_but_weak_oracle_ineligible` |
| main_result_eligible | `false` |
| path2_ref_model_blueprint | `false`；run_not_main_result_eligible |
| state_mode_decorative | `true` |
| SC-11 post-accept validation | `⚪ 0` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `3` |
| token / elapsed | `{'prompt_tokens': 128170, 'completion_tokens': 25247, 'total_tokens': 153417, 'estimated_prompt_tokens': 116927, 'estimated_completion_tokens': 18261, 'estimated_total_tokens': 135188, 'prompt_chars': 467702, 'completion_chars': 73036, 'n_calls': 5, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `481.091s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae/pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae/checks.json`, `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:b223e9c007f0e6bf994a73422bf90924144b919a3d25259b4c0d3253d303baaa` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14684 | 生成初始 DSL 与 grounding seeds | initial len=8162 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=320, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=72016 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=72016 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=72016 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=66717 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T14:38:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T14:38:49Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T14:38:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T14:38:49Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T14:41:22Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T14:41:22Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=8162,hash=sha256:c3b33abde729 |
| 7 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T14:41:22Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:c3b33abde7296af28e4d0495e1ec9ba95e3746ead6202a7d179de197bda7b236 |
| 10 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T14:41:22Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=8162,hash=sha256:c3b33abde729, current_hash=sha256:c3b33abde7296af28e4d0495e1ec9ba95e3746ead6202a7d179de197bda7b236 |
| 12 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T14:41:22Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T14:41:22Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T14:41:22Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T14:41:22Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T14:41:22Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T14:41:22Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T14:41:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T14:41:22Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T14:42:52Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T14:42:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T14:42:53Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T14:42:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T14:42:53Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T14:44:19Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T14:44:19Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T14:44:20Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T14:44:20Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T14:44:20Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T14:46:00Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T14:46:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T14:46:01Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T14:46:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T14:46:01Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T14:46:01Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T14:46:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T14:46:01Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T14:46:01Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-05T14:46:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T14:46:01Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 44 | `2026-06-05T14:46:49Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 45 | `2026-06-05T14:46:49Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 46 | `2026-06-05T14:46:49Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 47 | `2026-06-05T14:46:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-05T14:46:49Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 49 | `2026-06-05T14:46:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 50 | `2026-06-05T14:46:49Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=8162,hash=sha256:c3b33abde729 |
| 51 | `2026-06-05T14:46:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 52 | `2026-06-05T14:46:49Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=8162,hash=sha256:c3b33abde729 |
| 53 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 54 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_zero_load_no_res` | default-init dispatch with PL=0 and no RES should select ZeroLoadNoRES and cut out loads/generators. | ✅ |
| `zero_load_res_charges_battery_below_full_soc` | explicit-hot-start wildcard classification: with PL=0, RES>0, and SoC below 0.95, RES should charge the battery. | ✅ |
| `zero_load_res_spare_at_full_soc_boundary` | explicit-hot-start SoC boundary probe: with PL=0, RES>0, and SoC exactly 0.95, RES should be spare, not battery charge. | ✅ |
| `res_covers_load_charges_battery_below_full_soc` | explicit-hot-start SoC below-boundary probe: when RES covers positive PL and SoC is below 0.95, residual RES should char...<truncated 13 chars> | ✅ |
| `res_covers_load_spare_at_full_soc_boundary` | explicit-hot-start SoC boundary probe: when RES covers positive PL and SoC is exactly 0.95, residual RES should become s...<truncated 11 chars> | ✅ |
| `battery_discharge_at_suitable_soc_and_pgmax_boundary` | explicit-hot-start SoC suitability and capacity boundary probe: with SoC exactly 0.2 and deficit within Pgmax, batteries...<truncated 37 chars> | ✅ |
| `lng_cover_low_soc_adds_pgmax_charging_margin` | explicit-hot-start low-SoC probe: when deficit is LNG-coverable and SoC is below 0.2, LNG should cover load plus Pgmax/5...<truncated 17 chars> | ✅ |
| `lng_cover_without_battery_when_deficit_exceeds_pgmax` | explicit-hot-start priority probe: with suitable SoC but deficit greater than Pgmax and within LNG capacity, LNG should ...<truncated 26 chars> | ✅ |
| `lng_dg1_low_soc_adds_pd1_charging_margin` | explicit-hot-start diesel low-SoC probe: when LNG alone cannot cover and SoC is below 0.2, LNG+DG1 should cover load plu...<truncated 28 chars> | ✅ |
| `lng_dg1_at_suitable_soc_without_charging_margin` | explicit-hot-start SoC suitability boundary probe: with SoC exactly 0.2 and deficit needing DG1 but not DG2, LNG+DG1 sho...<truncated 46 chars> | ✅ |
| `lng_dg1_dg2_last_priority_within_all_thermal_capacity` | explicit-hot-start last-priority probe: when deficit exceeds LNG+DG1 but is within LNG+DG1+DG2, all thermal units should...<truncated 43 chars> | ✅ |
| `extreme_overload_uses_all_thermal_and_battery_support` | explicit-hot-start overload probe: when demand exceeds all RES and thermal resources, all thermal units should activate ...<truncated 85 chars> | ✅ |
| `forced_reclassification_from_zero_load_to_res_cover_spare` | explicit-hot-start forced-transition probe: from ZeroLoadNoRES, global guard classification must switch to RESCoverSpare...<truncated 65 chars> | ✅ |
| `forced_reclassification_from_zero_load_to_extreme_overload` | explicit-hot-start forced-transition probe: from ZeroLoadNoRES, global guard classification must switch to overload supp...<truncated 55 chars> | ✅ |
| `forced_reclassification_from_res_cover_to_battery_discharge` | explicit-hot-start forced-transition missing-line probe: from RESCoverCharge, changed demand with RES below PL and suita...<truncated 53 chars> | ✅ |
| `forced_reclassification_from_extreme_overload_to_zero_load_charge` | explicit-hot-start forced-transition missing-line probe: from ExtremeOverloadBatterySupport, zero load with RES and SoC ...<truncated 54 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6142, 'completion_chars': 20820, 'completion_tokens': 8215, 'elapsed_seconds': 152.5634076879942, 'estimated_completion_tokens': 5205, 'estimated_prompt_tokens': 6646, 'estimated_total_tokens': 11851, 'first_chunk_seconds': 41.80550393500016, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26582, 'prompt_tokens': 6469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14684}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3565, 'completion_chars': 12162, 'completion_tokens': 4602, 'elapsed_seconds': 89.97811380799976, 'estimated_completion_tokens': 3041, 'estimated_prompt_tokens': 15622, 'estimated_total_tokens': 18663, 'first_chunk_seconds': 25.738196175021585, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 62488, 'prompt_tokens': 16488, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21090}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4237, 'completion_chars': 14517, 'completion_tokens': 4658, 'elapsed_seconds': 86.4473202250083, 'estimated_completion_tokens': 3630, 'estimated_prompt_tokens': 18828, 'estimated_total_tokens': 22458, 'first_chunk_seconds': 10.27077630898566, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 75309, 'prompt_tokens': 20172, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24830}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4913, 'completion_chars': 16872, 'completion_tokens': 5252, 'elapsed_seconds': 99.88783190000686, 'estimated_completion_tokens': 4218, 'estimated_prompt_tokens': 19416, 'estimated_total_tokens': 23634, 'first_chunk_seconds': 10.78901525400579, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 77664, 'prompt_tokens': 20844, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26096}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1898, 'completion_chars': 8665, 'completion_tokens': 2520, 'elapsed_seconds': 47.987880693981424, 'estimated_completion_tokens': 2167, 'estimated_prompt_tokens': 56415, 'estimated_total_tokens': 58582, 'first_chunk_seconds': 13.998346330976347, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 225659, 'prompt_tokens': 64197, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 66717}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success_but_weak_oracle_ineligible`。
- required stages executed：`16/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`3`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_prompt_scope_final_runs/pr-e1-path2_lng_ems-default-lg-b1-prompt-scope-07bd58c1-4fd485ae/report.md` §7。

</details>
