## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_lg_b1_validation_subgraph_final_clean_runs/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | post-accept | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 33364 | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87/report.md` |
| path1 | `path1_cara` | `default` | `not_converged` | `rejected` | ✅ | ❌ | ⚪ | ⚪ 0 | `repair_review_rework_budget` | 812107 | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 36497 | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262/report.md` |
| path2 | `path2_lng_ems` | `default` | `not_converged` | `budget_exhausted` | ✅ | ❌ | ❌ | ✅ 0/1; ❌ 1 | `model_review_or_quality` | 715729 | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13/report.md` |

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
- node trace count 范围：min=16，max=101；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：2/4 success，rejected=1，budget_exhausted=1，total_tokens=1597697。
  - SC-11 post-accept validation：triggered=1/4 run-level attempts，success=0，failure=1。
- 主结果候选：当前 2/4 个非 infrastructure run 可进入 main_result_eligible；provider/network invalid=0 个，只能作为 infrastructure evidence。

### 主结果候选 vs Path2 ref-model 蓝本边界

- Path2 run-validity：0/1 个 Path2 run 的 `main_result_eligible=true`；这只表示 run/schema/secret/trace/final verdict 可进入主结果候选。
- Path2 blueprint-validity：0/1 个 Path2 run 当前可作为 `path2_ref_model_blueprint_eligible=true`；该字段比 `main_result_eligible` 更严格。
- `path2_lng_ems`：main_result_eligible=`false`，path2_ref_model_blueprint_eligible=`false`，state_mode_decorative=`true`；reason=run_not_main_result_eligible
- 解释：`path2_ref_model_blueprint_eligible=false` 不会把有效 run 改成 provider invalid；它只禁止把 state-mode-decorative / 条件分类式模型宣传为 Path2 ref-model 主蓝本。

### 主要失败模式

- `success`：2 run(s)。
- `model_review_or_quality`：1 run(s)。
- `repair_review_rework_budget`：1 run(s)。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=repair_review_rework_budget，最大 observed iteration_count=1。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=model_review_or_quality，最大 observed iteration_count=5。
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
| token / elapsed | `{'prompt_tokens': 26887, 'completion_tokens': 6477, 'total_tokens': 33364, 'estimated_prompt_tokens': 26212, 'estimated_completion_tokens': 4218, 'estimated_total_tokens': 30430, 'prompt_chars': 104847, 'completion_chars': 16866, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `127.147s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87/pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87/checks.json`, `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:294dffb55f92a1d35affbc768bab8925f6e97201d0757047371509c50cdc64fc` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=8499 | 生成初始 DSL 与 grounding seeds | initial len=625 | [`record`](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=12904 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=11961 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T13:58:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T13:58:46Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T13:58:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T13:58:46Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T13:59:26Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T13:59:26Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=625,hash=sha256:daf0a2131e36 |
| 7 | `2026-06-05T13:59:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T13:59:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T13:59:26Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:daf0a2131e360a06d62ea8c0a5ba398ff01b5fc756b01374275405d75c36a70e |
| 10 | `2026-06-05T13:59:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T13:59:26Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=625,hash=sha256:daf0a2131e36, current_hash=sha256:daf0a2131e360a06d62ea8c0a5ba398ff01b5fc756b01374275405d75c36a70e |
| 12 | `2026-06-05T13:59:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T13:59:26Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T13:59:26Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T13:59:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T13:59:26Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T13:59:26Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T13:59:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T13:59:26Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T13:59:26Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T13:59:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T13:59:26Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T14:00:18Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T14:00:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T14:00:18Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T14:00:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T14:00:18Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T14:00:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T14:00:18Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T14:00:18Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T14:00:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T14:00:18Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T14:00:52Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T14:00:52Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T14:00:52Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T14:00:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T14:00:52Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T14:00:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T14:00:52Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=625,hash=sha256:daf0a2131e36 |
| 40 | `2026-06-05T14:00:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T14:00:52Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=625,hash=sha256:daf0a2131e36 |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_increase_then_default_slip_hold` | default-init dispatches to increase with inlet valve command active, then default slp=0.0 satisfies increase->hold and n...<truncated 18 chars> | ✅ |
| `increase_to_hold_at_upper_boundary` | explicit-hot-start tests that increase transitions to hold exactly at slp=0.01 and applies hold neutral valve outputs. | ✅ |
| `increase_no_hold_above_upper_boundary` | explicit-hot-start tests that increase does not transition to hold when slp is just above 0.01. | ✅ |
| `hold_to_increase_strict_upper_fire` | explicit-hot-start tests that hold transitions to increase only when slp is strictly greater than 0.01 and applies incre...<truncated 12 chars> | ✅ |
| `hold_stays_at_upper_boundary` | explicit-hot-start tests that hold does not transition to increase at the strict-boundary value slp=0.01. | ✅ |
| `hold_to_decrease_strict_lower_fire` | explicit-hot-start tests that hold transitions to decrease only when slp is strictly less than -0.01 and applies pressur...<truncated 18 chars> | ✅ |
| `hold_stays_at_lower_boundary` | explicit-hot-start tests that hold does not transition to decrease at the strict-boundary value slp=-0.01. | ✅ |
| `decrease_to_hold_boundary_and_below_no_fire` | explicit-hot-start probes decrease->hold at slp=-0.01 separately from a below-boundary no-fire decrease case. | ✅ |
| `decrease_stays_below_lower_boundary` | explicit-hot-start tests that decrease does not return to hold while slp remains below -0.01, preserving pressure-releas...<truncated 10 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1671, 'completion_chars': 5744, 'completion_tokens': 2106, 'elapsed_seconds': 40.38555176198133, 'estimated_completion_tokens': 1436, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 7929, 'first_chunk_seconds': 10.226484359998722, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 8499}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1747, 'completion_chars': 6405, 'completion_tokens': 2784, 'elapsed_seconds': 51.94689822100918, 'estimated_completion_tokens': 1602, 'estimated_prompt_tokens': 9912, 'estimated_total_tokens': 11514, 'first_chunk_seconds': 20.451193037006306, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39648, 'prompt_tokens': 10120, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12904}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1068, 'completion_chars': 4717, 'completion_tokens': 1587, 'elapsed_seconds': 33.78077490601572, 'estimated_completion_tokens': 1180, 'estimated_prompt_tokens': 9807, 'estimated_total_tokens': 10987, 'first_chunk_seconds': 15.268064550007693, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39227, 'prompt_tokens': 10374, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 11961}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_abs-default-lg-b1-final-3794aa41-19e95a87/report.md` §7。

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
def int patient_bp = 120;
def int target_bp = 120;
def int requested_target_bp = 120;
def int infusion_rate = 0;
def int default_flow_rate = 0;
def int manual_switch_speed = 0;
def int pump_speed = 0;
def int pump_control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int display_error = 0;
def int sound_alarm = 0;
def int software_control = 0;
def int infusion_log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
            during {
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            [*] -> AwaitStart;

            state AwaitStart;

            AwaitStart -> AwaitStart :: ChangeSetpoint effect {
                target_bp = requested_target_bp;
            };
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_fault == 0] {
                    infusion_rate = target_bp - patient_bp;
                    pump_control_voltage = infusion_rate;
                    infusion_log_count = infusion_log_count + 1;
                } else {
                    pump_control_voltage = 0;
                }
            }
        }

        state PumpFault {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 1;
                display_error = 1;
                sound_alarm = 1;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolNormal -> Manual :: TerminateAC;
        AutocontrolNormal -> PumpFault :: OcclusionFault effect {
            pump_fault = 1;
        };
        PumpFault -> Manual :: FaultRemoved effect {
            pump_fault = 0;
        };
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `rejected` |
| failure class | `repair_review_rework_budget` |
| main_result_eligible | `false` |
| path2_ref_model_blueprint | `n/a`；not_applicable_to_path1 |
| state_mode_decorative | `false` |
| SC-11 post-accept validation | `⚪ 0` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `5` / `0` / `3` |
| token / elapsed | `{'prompt_tokens': 766602, 'completion_tokens': 45505, 'total_tokens': 812107, 'estimated_prompt_tokens': 865697, 'estimated_completion_tokens': 34171, 'estimated_total_tokens': 899868, 'prompt_chars': 3462765, 'completion_chars': 136662, 'n_calls': 14, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `886.309s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e/pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e/checks.json`, `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:d1a1b9c0eb2d38611770409d0f628779e01d52a37d53acab5680cb4debee5438` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `21` |
| `langgraph_node_trace_hash` | `sha256:2ee9ba0f28eb3bd6ceaa61221cefa25f97e04a01c3a29007325ca202f38f7a6a` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `21` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14448 | 生成初始 DSL 与 grounding seeds | initial len=2702 | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=65221 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=65221 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=65221 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=444816 | LLM per-request accept/reject + repair | candidate len=2702,2709,2697,3560,2882 | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=287622 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=444816 | LLM per-request accept/reject + repair | candidate len=2702,2709,2697,3560,2882 | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=287622 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=444816 | LLM per-request accept/reject + repair | candidate len=2702,2709,2697,3560,2882 | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=287622 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=444816 | LLM per-request accept/reject + repair | candidate len=2702,2709,2697,3560,2882 | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=287622 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=444816 | LLM per-request accept/reject + repair | candidate len=2702,2709,2697,3560,2882 | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=287622 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SD-6 sim failure: 8/14 scenarios passed | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T13:58:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T13:58:46Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T13:58:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T13:58:46Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T14:01:13Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T14:01:13Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2702,hash=sha256:3fbbdf9ad90a |
| 7 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T14:01:13Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:3fbbdf9ad90a60957e2527a007b291fb9036bb1ac49e8bfbe004c84ca1f5854f |
| 10 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T14:01:13Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2702,hash=sha256:3fbbdf9ad90a, current_hash=sha256:3fbbdf9ad90a60957e2527a007b291fb9036bb1ac49e8bfbe004c84ca1f5854f |
| 12 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T14:01:13Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T14:01:13Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T14:01:13Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T14:01:13Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T14:01:13Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T14:01:13Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T14:01:13Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T14:02:28Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T14:02:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T14:02:28Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T14:02:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T14:02:28Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T14:03:42Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T14:03:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T14:03:43Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T14:03:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T14:03:43Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T14:05:00Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T14:05:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T14:05:00Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T14:05:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T14:05:00Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T14:05:00Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T14:05:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T14:05:00Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T14:05:00Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 42 | `2026-06-05T14:05:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T14:05:00Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 14, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 44 | `2026-06-05T14:05:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T14:05:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-05T14:05:00Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 14, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2702,hash=sha256:3fbbdf9ad90a |
| 47 | `2026-06-05T14:05:00Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 48 | `2026-06-05T14:05:00Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 6} | <none> |
| 49 | `2026-06-05T14:05:00Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2702,hash=sha256:3fbbdf9ad90a |
| 50 | `2026-06-05T14:06:16Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 51 | `2026-06-05T14:06:16Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-09d3998124", "fixreq-0-sd6-1-2244c80013", "fixreq-0-sd6-2-0b7ad9e35b", "fixreq-0-sd6-3-989dda703e", "fixreq-0-sd6-4-775e5adc2d", "fixreq-0-sd6-5-1e8441f72f"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2702,hash=sha256:afd645ff2326 |
| 52 | `2026-06-05T14:06:16Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 53 | `2026-06-05T14:06:16Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:afd645ff2326b1f3d5efd929079528585f115dbbf4775fbf1b92e78188f2e18a |
| 54 | `2026-06-05T14:06:43Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 55 | `2026-06-05T14:06:43Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 56 | `2026-06-05T14:06:43Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2702,hash=sha256:3fbbdf9ad90a |
| 57 | `2026-06-05T14:07:29Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 58 | `2026-06-05T14:07:29Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-09d3998124", "fixreq-0-sd6-1-2244c80013", "fixreq-0-sd6-2-0b7ad9e35b", "fixreq-0-sd6-3-989dda703e", "fixreq-0-sd6-4-775e5adc2d", "fixreq-0-sd6-5-1e8441f72f"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2709,hash=sha256:dff1fe0e2a5e |
| 59 | `2026-06-05T14:07:29Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 60 | `2026-06-05T14:07:29Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:dff1fe0e2a5e437d0f7b3ee9c9a9ae74dcd6bd82233a8c90adf7bff3dec3a669 |
| 61 | `2026-06-05T14:07:57Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 62 | `2026-06-05T14:07:57Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 63 | `2026-06-05T14:07:57Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 64 | `2026-06-05T14:07:57Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2702,hash=sha256:3fbbdf9ad90a |
| 65 | `2026-06-05T14:08:44Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 66 | `2026-06-05T14:08:44Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-09d3998124", "fixreq-0-sd6-1-2244c80013", "fixreq-0-sd6-2-0b7ad9e35b", "fixreq-0-sd6-3-989dda703e", "fixreq-0-sd6-4-775e5adc2d", "fixreq-0-sd6-5-1e8441f72f"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2697,hash=sha256:cb98c02d15b6 |
| 67 | `2026-06-05T14:08:44Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 68 | `2026-06-05T14:08:44Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:cb98c02d15b6d76d55750a603a7ed90a8c109137c97a5acc7c2fb9b7db95e703 |
| 69 | `2026-06-05T14:09:18Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 70 | `2026-06-05T14:09:18Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <non
... <truncated 1647 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_manual_operation_outputs` | default-init: first cycle dispatches to Manual, where manual switch speed and default flow rate drive pump_speed and inf...<truncated 11 chars> | ✅ |
| `initiate_ac_change_setpoint_and_start` | default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters Autocontrol...<truncated 5 chars> | ⚪ |
| `autocontrol_init_advances_to_normal_and_computes_flow` | explicit-hot-start: AutocontrolInit completes to AutocontrolNormal, which computes lower flow from higher patient pressu...<truncated 38 chars> | ✅ |
| `normal_autocontrol_high_pressure_lower_flow` | explicit-hot-start: AutocontrolNormal uses patient blood pressure to compute infusion rate, with higher pressure produci...<truncated 14 chars> | ✅ |
| `occlusion_fault_activates_alarm_and_releases_control` | explicit-hot-start: OcclusionFault during normal autocontrol enters PumpFault, activates alarms and error indications, a...<truncated 29 chars> | ✅ |
| `fault_removed_returns_to_manual_recovery` | explicit-hot-start: after caregiver removes the fault, CARA returns to Manual recovery with alarms cleared and manual pu...<truncated 19 chars> | ✅ |
| `terminate_ac_from_init_and_normal` | explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control. | ❌ |
| `terminate_ac_from_autocontrol_normal` | explicit-hot-start: caregiver TerminateAC from normal autocontrol returns to the shared Manual target and releases softw...<truncated 12 chars> | ✅ |
| `forced_back_manual_events_from_distinct_states` | explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mo...<truncated 10 chars> | ⚪ |
| `forced_back_manual_event_variants` | explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery tar...<truncated 24 chars> | ⚪ |
| `cp_back_manual_forces_from_ask_start` | explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, de...<truncated 52 chars> | ⚪ |
| `cc_back_manual_forces_from_autocontrol_init` | explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery tar...<truncated 33 chars> | ⚪ |
| `occlusion_fault_effect_sets_fault_flag` | explicit-hot-start: OcclusionFault must both target PumpFault and set pump_fault before PumpFault alarm/release actions,...<truncated 54 chars> | ✅ |
| `fault_removed_effect_clears_fault_flag` | explicit-hot-start: FaultRemoved must target Manual and clear pump_fault, detecting a missing transition effect even tho...<truncated 32 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-6` | initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, ... +1 | accept=6, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=False, drift=major, rework=Repair the dangling StartAC transition while preserving the intended SL-9 behavior. Do not leave `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC` unless ...<truncated 580 chars> | `sha256:afd645ff2326b1f3d5efd929079528585f115dbbf4775fbf1b92e78188f2e18a` |
| 2 | `0` | ❌ | `SD-6` | initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, ... +1 | accept=6, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=False, drift=major, rework=Fix the parse error by removing the unsupported dotted source transition `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;`., Do not revert to the previously rejected nes...<truncated 299 chars> | `sha256:dff1fe0e2a5e437d0f7b3ee9c9a9ae74dcd6bd82233a8c90adf7bff3dec3a669` |
| 3 | `0` | ❌ | `SD-6` | initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, ... +1 | accept=6, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Repair StartAC visibility from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart while keeping AutocontrolInit as a sibling of Ask_StartAC under Mode_Control_Algorithm. Do not...<truncated 967 chars> | `sha256:cb98c02d15b6d76d55750a603a7ed90a8c109137c97a5acc7c2fb9b7db95e703` |
| 4 | `0` | ❌ | `SD-6` | initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, ... +1 | accept=6, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Repair only the remaining StartAC visibility failure unless the full local brief shows additional scenario failures. Preserve `AutocontrolInit` as `CARA.Mode_Control_Algorithm....<truncated 753 chars> | `sha256:0ff7fe87ef63a59441ab611029685acf2ad9c0b8636053998f540052bfce9b43` |
| 5 | `0` | ❌ | `SD-6` | initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, ... +1 | accept=6, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Repair StartAC visibility from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart to CARA.Mode_Control_Algorithm.AutocontrolInit. The current line `! Ask_StartAC -> Autocontrol...<truncated 692 chars> | `sha256:e5e4732ddabeadd184806360d715999a302cfb465ecda022876f12fbe08a2d14` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e/report.md` §7。

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
| token / elapsed | `{'prompt_tokens': 26908, 'completion_tokens': 9589, 'total_tokens': 36497, 'estimated_prompt_tokens': 26261, 'estimated_completion_tokens': 6686, 'estimated_total_tokens': 32947, 'prompt_chars': 105038, 'completion_chars': 26740, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `181.82s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262/pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262/checks.json`, `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:0e22f516a46526ab5ba094f270c499af39ce128fa19dc35b9071aa4c5e96887d` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=10415 | 生成初始 DSL 与 grounding seeds | initial len=658 | [`record`](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=15053 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=11029 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T13:58:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T13:58:46Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T13:58:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T13:58:46Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T14:00:00Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T14:00:00Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=658,hash=sha256:6b02aa0b651f |
| 7 | `2026-06-05T14:00:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T14:00:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T14:00:00Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:6b02aa0b651f657a4b69e59da1e30c6ba2bed44ab0b8f429babbf3112ad83754 |
| 10 | `2026-06-05T14:00:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T14:00:00Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=658,hash=sha256:6b02aa0b651f, current_hash=sha256:6b02aa0b651f657a4b69e59da1e30c6ba2bed44ab0b8f429babbf3112ad83754 |
| 12 | `2026-06-05T14:00:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T14:00:00Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T14:00:00Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T14:00:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T14:00:00Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T14:00:01Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T14:00:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T14:00:01Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T14:00:01Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T14:00:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T14:00:01Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T14:01:08Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T14:01:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T14:01:08Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T14:01:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T14:01:08Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T14:01:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T14:01:08Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T14:01:08Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T14:01:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T14:01:08Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T14:01:47Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T14:01:47Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T14:01:47Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T14:01:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T14:01:47Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 38 | `2026-06-05T14:01:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T14:01:47Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=658,hash=sha256:6b02aa0b651f |
| 40 | `2026-06-05T14:01:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T14:01:47Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=658,hash=sha256:6b02aa0b651f |
| 42 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 43 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_f2_then_down_to_f1` | default-init verifies start at F1 stopped, no-request no-fire, F1 PS2 upward to MU2, arrival at F2, then next PS1 reques...<truncated 17 chars> | ✅ |
| `f1_direct_to_f3_and_reset_from_floor` | explicit-hot-start verifies F1 PS3 chooses direct upward MU3, S3 stops at F3, and Reset from a floor context forces F1. | ✅ |
| `f2_to_f3_upward_request` | explicit-hot-start verifies PS3 from F2 transitions to upward MU3 and S3 arrival stops at F3. | ✅ |
| `f3_to_f1_downward_request` | explicit-hot-start verifies PS1 from F3 transitions to downward MD1 and S1 arrival stops at F1. | ✅ |
| `f3_to_f2_downward_request` | explicit-hot-start verifies PS2 from F3 transitions to downward MD2 and S2 arrival stops at F2. | ✅ |
| `reset_from_upward_motion` | explicit-hot-start verifies the forced Reset rule from an upward motion state returns to F1 and stop output. | ✅ |
| `reset_from_downward_motion` | explicit-hot-start verifies the forced Reset rule from a downward motion state returns to F1 and stop output. | ✅ |
| `wrong_arrival_sensor_does_not_complete_motion` | explicit-hot-start probes that MU3 only completes on S3, so an S2 arrival signal must not stop the upward-to-F3 motion. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3476, 'completion_chars': 11899, 'completion_tokens': 3977, 'elapsed_seconds': 74.67990231499425, 'estimated_completion_tokens': 2975, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 9498, 'first_chunk_seconds': 12.233427380007925, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10415}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2074, 'completion_chars': 8279, 'completion_tokens': 3589, 'elapsed_seconds': 67.44609811998089, 'estimated_completion_tokens': 2070, 'estimated_prompt_tokens': 11224, 'estimated_total_tokens': 13294, 'first_chunk_seconds': 29.605902751005488, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 44894, 'prompt_tokens': 11464, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 15053}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1504, 'completion_chars': 6562, 'completion_tokens': 2023, 'elapsed_seconds': 38.64080964997993, 'estimated_completion_tokens': 1641, 'estimated_prompt_tokens': 8514, 'estimated_total_tokens': 10155, 'first_chunk_seconds': 11.916073140979279, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 34055, 'prompt_tokens': 9006, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 11029}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path1_elevator-default-lg-b1-final-3794aa41-21835262/report.md` §7。

</details>

<details><summary>path2 / path2_lng_ems / default / not_converged</summary>

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
def float Pbat_max = 0.0;
def float Pgmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pg_req = 0.0;
def float Peng3_req = 0.0;
def float Pd1_req = 0.0;
def float Pd2_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int LNG_cut_in = 0;
def int LNG_cut_out = 1;
def int DG3_cut_in = 0;
def int DG3_cut_out = 1;
def int DG1_cut_in = 0;
def int DG1_cut_out = 1;
def int DG2_cut_in = 0;
def int DG2_cut_out = 1;
def int Load_cut_in = 0;
def int Load_cut_out = 1;
def int overload_illegal = 0;

state LNGShipEMS {
    ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0.0 && (Ppv + Pw <= 0.0 || SoC >= 0.95)];
    ! * -> RESCoversCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [PL > Ppv + Pw && SoC > 0.2 && PL - Ppv - Pw <= Pbat_max];
    ! * -> LNGCoveredChargeLowSoC : if [PL > Ppv + Pw && SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= Pgmax];
    ! * -> LNGCovered : if [PL > Ppv + Pw && PL - Ppv - Pw <= Pgmax && ! (SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= Pgmax)];
    ! * -> LNGDG3ChargeLowSoC : if [PL > Ppv + Pw && SoC <= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw + Pd1max / 10.0 <= Pgmax + eng3_Pmax];
    ! * -> LNGDG3Covered : if [PL > Ppv + Pw && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax && ! (SoC <= 0.2 && PL - Ppv - Pw + Pd1max / 10.0 <= Pgmax + eng3_Pmax)];
    ! * -> LNGDG3DG1ChargeLowSoC : if [PL > Ppv + Pw && SoC <= 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> LNGDG3DG1Covered : if [PL > Ppv + Pw && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max && ! (SoC <= 0.2 && PL - Ppv - Pw + Pd1max / 10.0 <= Pgmax + eng3_Pmax + Pd1max)];
    ! * -> AllThermalAndOverloadMitigation : if [PL > Ppv + Pw && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && ! (SoC <= 0.2 && PL - Ppv - Pw + Pd1max / 10.0 <= Pgmax + eng3_Pmax + Pd1max) && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max + Pbat_max && (PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max || SoC > 0.2)];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            Pg_req = 0.0;
            Peng3_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            LNG_cut_in = 0;
            LNG_cut_out = 1;
            DG3_cut_in = 0;
            DG3_cut_out = 1;
            DG1_cut_in = 0;
            DG1_cut_out = 1;
            DG2_cut_in = 0;
            DG2_cut_out = 1;
            Load_cut_in = 0;
            Load_cut_out = 1;
            overload_illegal = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pg_req = 0.0;
            Peng3_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            LNG_cut_in = 0;
            LNG_cut_out = 1;
            DG3_cut_in = 0;
            DG3_cut_out = 1;
            DG1_cut_in = 0;
            DG1_cut_out = 1;
            DG2_cut_in = 0;
            DG2_cut_out = 1;
            Load_cut_in = 0;
            Load_cut_out = 1;
            overload_illegal = 0;
        }
    }

    state RESCoversCharge {
        enter {
            Pg_req = 0.0;
            Peng3_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            LNG_cut_in = 0;
            LNG_cut_out = 1;
            DG3_cut_in = 0;
            DG3_cut_out = 1;
            DG1_cut_in = 0;
            DG1_cut_out = 1;
            DG2_cut_in = 0;
            DG2_cut_out = 1;
            Load_cut_in = 1;
            Load_cut_out = 0;
            overload_illegal = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pg_req = 0.0;
            Peng3_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            LNG_cut_in = 0;
            LNG_cut_out = 1;
            DG3_cut_in = 0;
            DG3_cut_out = 1;
            DG1_cut_in = 0;
            DG1_cut_out = 1;
            DG2_cut_in = 0;
            DG2_cut_out = 1;
            Load_cut_in = 1;
            Load_cut_out = 0;
            overload_illegal = 0;
        }
    }

    state BatteryDischarge {
        enter {
            Pg_req = 0.0;
            Peng3_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            LNG_cut_in = 0;
            LNG_cut_out = 1;
            DG3_cut_in = 0;
            DG3_cut_out = 1;
            DG1_cut_in = 0;
            DG1_cut_out = 1;
            DG2_cut_in = 0;
            DG2_cut_out = 1;
            Load_cut_in = 1;
            Load_cut_out = 0;
            overload_illegal = 0;
        }
    }

    state LNGCoveredChargeLowSoC {
        enter {
            Pg_req = PL - Ppv - Pw + Pgmax / 5.0;
            Peng3_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5.0;
            Pspare = 0.0;
            LNG_cut_in = 1;
            LNG_cut_out = 0;
            DG3_cut_in = 0;
            DG3_cut_out = 1;
            DG1_cut_in = 0;
            DG1_cut_out = 1;
            DG2_cut_in = 0;
            DG2_cut_out = 1;
            Load_cut_in = 1;
            Load_cut_out = 0;
            overload_illegal = 0;
        }
    }

    state LNGCovered {
        enter {
            Pg_req = PL - Ppv - Pw;
            Peng3_req = 0.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            LNG_cut_in = 1;
            LNG_cut_out = 0;
            DG3_cut_in = 0;
            DG3_cut_out = 1;
            DG1_cut_in = 0;
            DG1_cut_out = 1;
            DG2_cut_in = 0;
            DG2_cut_out = 1;
            Load_cut_in = 1;
            Load_cut_out = 0;
            overload_illegal = 0;
        }
    }

    state LNGDG3ChargeLowSoC {
        enter {
            Pg_req = Pgmax;
            Peng3_req = PL - Ppv - Pw - Pgmax + Pd1max / 10.0;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10.0;
            Pspare = 0.0;
            LNG_cut_in = 1;
            LNG_cut_out = 0;
            DG3_cut_in = 1;
            DG3_cut_out = 0;
            DG1_cut_in = 0;
            DG1_cut_out = 1;
            DG2_cut_in = 0;
            DG2_cut_out = 1;
            Load_cut_in = 1;
            Load_cut_out = 0;
            overload_illegal = 0;
        }
    }

    state LNGDG3Covered {
        enter {
            Pg_req = Pgmax;
            Peng3_req = PL - Ppv - Pw - Pgmax;
            Pd1_req = 0.0;
            Pd2_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            LNG_cut_in = 1;
            LNG_cut_out = 0;
            DG3_cut_in = 1;
            DG3_cut_out = 0;
            DG1_cut_in = 0;
            DG1_cut_out = 1;
            DG2_cut_in = 0;
            DG2_cut_out = 1;
            Load_cut_in = 1;
            Load_cut_out = 0;
            overload_illegal = 0;
        }
    }

    state LNGDG3DG1ChargeLowSoC {
        enter {
            Pg_req = Pgmax;
            Peng3_req = eng3_Pmax;
            Pd1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax + Pd1max / 10.0;
            Pd2_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10.0;
            Pspare = 0.0;
            LNG_cut_in = 1;
            LNG_cut_out = 0;
            DG3_cut_in = 1;
            DG3_cut_out = 0;
            DG1_cut_in = 1;
            DG1_cut_out = 0;
            DG2_cut_in = 0;
            DG2_cut_out = 1;
            Load_cut_in = 1;
            Load_cut_out = 0;
            overload_illegal = 0;
        }
    }

    state LNGDG3DG1Covered {
        enter {
            Pg_req = Pgmax;
            Peng3_req = eng3_Pmax;
            Pd1_req = PL - Ppv - Pw - Pgmax - eng3_Pmax;
            Pd2_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            LNG_cut_in = 1;
            LNG_cut_out = 0;
            DG3_cut_in = 1;
            DG3_cut_out = 0;
            DG1_cut_in = 1;
            DG1_cut_out = 0;
            DG2_cut_in = 0;
            DG2_cut_out = 1;
            Load_cut_in = 1;
            Load_cut_out = 0;
            overload_illegal = 0;
        }
    }

    state AllThermalAndOverloadMitigation {
        enter {
            Pg_req = Pgmax;
            Peng3_req = eng3_Pmax;
            Pd1_req = Pd1max;
            if [PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max] {
                Pd2_req = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max;
                Pbat_discharge = 0.0;
                Load_cut_in = 1;
                Load_cut_out = 0;
                overload_illegal = 0;
            } else {
                Pd2_req = Pd2max;
                Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
                Load_cut_in = 0;
                Load_cut_out = 1;
                overload_illegal = 1;
            }
            Pbat_charge = 0.0;
            Pspare = 0.0;
            LNG_cut_in = 1;
            LNG_cut_out = 0;
            DG3_cut_in = 1;
            DG3_cut_out = 0;
            DG1_cut_in = 1;
            DG1_cut_out = 0;
            DG2_cut_in = 1;
            DG2_cut_out = 0;
        }
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `budget_exhausted` |
| failure class | `model_review_or_quality` |
| main_result_eligible | `false` |
| path2_ref_model_blueprint | `false`；run_not_main_result_eligible |
| state_mode_decorative | `true` |
| SC-11 post-accept validation | `✅ 0/1; ❌ 1` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `5` / `3` / `13` |
| token / elapsed | `{'prompt_tokens': 630319, 'completion_tokens': 85410, 'total_tokens': 715729, 'estimated_prompt_tokens': 596646, 'estimated_completion_tokens': 54923, 'estimated_total_tokens': 651569, 'prompt_chars': 2386540, 'completion_chars': 219661, 'n_calls': 20, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1707.359s` |
| full stage table | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13/report.md` §4 |
| run record | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13/pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz` |
| logs | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13/run_logs/stdout.txt`, `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13/run_logs/stderr.txt` |
| checks / repro | `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13/checks.json`, `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:cdd3050204a9f8a0ec0c8f8966751f735e519cd4776bf748b8ca549a7a4eb981` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `101` |
| `langgraph_node_trace_hash` | `sha256:1bb694ca5d94b5ef946028792dd9b1c7cc9df646528df76829a63f7409a4753d` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `101` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=15589 | 生成初始 DSL 与 grounding seeds | initial len=9281 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=197357 | LLM per-request accept/reject + repair | candidate len=0,0,9362,9500,10055 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=8, tokens=230867 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=8, tokens=230867 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=8, tokens=230867 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=197357 | LLM per-request accept/reject + repair | candidate len=0,0,9362,9500,10055 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=8, tokens=230867 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=8, tokens=230867 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=197357 | LLM per-request accept/reject + repair | candidate len=0,0,9362,9500,10055 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-10` | 是 | 2 | ✅ | LLM calls=3, tokens=98425 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SC-11` | 否 | 2 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=8, tokens=230867 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-7` | 是 | 3 | ✅ | LLM calls=3, tokens=173491 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=197357 | LLM per-request accept/reject + repair | candidate len=0,0,9362,9500,10055 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-10` | 是 | 2 | ✅ | LLM calls=3, tokens=98425 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SC-11` | 否 | 2 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=13, advisory=175, info=0; blocking=0, advisory=188, info=0; blocking=0, advisory=188, info=0; blocking | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=8, tokens=230867 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-7` | 是 | 3 | ✅ | LLM calls=3, tokens=173491 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=197357 | LLM per-request accept/reject + repair | candidate len=0,0,9362,9500,10055 | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SL-10` | 是 | 2 | ✅ | LLM calls=3, tokens=98425 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SC-11` | 否 | 2 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=13, advisory=175, info=0; blocking=0, advisory=188, i
... <truncated 13561 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|---|
| `default_zero_load_res_charges_battery` | default-init probe: with PL=0, positive RES, and SoC below 0.95, first empty cycle dispatches to zero-load battery charg...<truncated 4 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `res_covers_soc_boundary_charge_then_spare` | explicit-hot-start probes: SoC just below 0.95 should charge from surplus RES, while the exact 0.95 boundary should rout...<truncated 29 chars> | ⚪ | ⚪ | ⚪ | ⚪ | ✅ |
| `res_covers_spare_at_full_soc_boundary` | explicit-hot-start probe: at SoC=0.95 with RES exceeding positive load, residual renewable power should be spare rather ...<truncated 20 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `battery_supplies_deficit_when_soc_suitable` | explicit-hot-start probe: when RES is below load, SoC is above the low threshold, and the deficit fits battery capacity,...<truncated 61 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `low_soc_lng_covered_adds_pgmax_margin` | explicit-hot-start probe: at SoC=0.2, an LNG-covered deficit should include the Pgmax/5 charging margin while staying wi...<truncated 18 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `lng_dg3_covers_deficit_above_low_soc` | explicit-hot-start probe: above low SoC, when the deficit exceeds LNG but fits LNG plus DG3, EMS should request LNG firs...<truncated 49 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `low_soc_lng_dg3_dg1_adds_pd1_margin` | explicit-hot-start probe: at low SoC, when LNG plus DG3 are insufficient but adding DG1 with the Pd1max/10 charging marg...<truncated 93 chars> | ❌ | ❌ | ❌ | ✅ | ✅ |
| `extreme_demand_all_thermal_and_battery_mitigation` | explicit-hot-start probe: if demand exceeds RES and all thermal capacity but the remaining lack is battery-coverable, al...<truncated 143 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `zero_load_full_soc_routes_res_to_spare` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `res_covers_charge_below_full_soc` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `lng_covers_deficit_above_low_soc` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `low_soc_lng_dg3_adds_pd1_margin` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `lng_dg3_dg1_covers_deficit_above_low_soc` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_escapes_overload_to_res_spare` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_from_zero_load_to_battery` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_from_res_spare_to_lng_dg3_dg1` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_from_lng_dg3_to_zero_load_spare` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_from_battery_to_lng_low_soc` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `forced_reclassification_to_zero_load_charge` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pbat_max, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversSpare:to_path=LNGShipEMS.BatteryDischarge, ... +13 | accept=0, reject=12, waiver=12 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 2 | `1` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pbat_max, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.BatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadSpare:to_path=LNGShipEMS.BatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversCharge:to_path=LNGShipEMS.BatteryDischarge, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.RESCoversSpare:to_path=LNGShipEMS.BatteryDischarge, ... +13 | accept=0, reject=12, waiver=12 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 3 | `2` | ✅ | `SD-6` | low_soc_lng_dg3_dg1_adds_pd1_margin | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:f0cdcc6a66a2e178a2578e6e1d863816d3c648b6934c30a701cd2d9008a31b83` |
| 4 | `3` | ✅ | `SL-7` | 0, 1, 2 | accept=3, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:74996d3923fb34f802dade0c76dd36dd3b1d3b9bd6ba58dded0a7de85602c65a` |
| 5 | `4` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:a3292b224769d6c870233d5f55ad440f3793b90c6b43bfa0f3b9eca810ee5ada` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_lg_b1_validation_subgraph_final_clean_runs/pr-e1-path2_lng_ems-default-lg-b1-final-3794aa41-afa2ae13/report.md` §7。

</details>
