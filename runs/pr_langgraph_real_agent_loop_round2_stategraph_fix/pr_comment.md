## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 33185 | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 564727 | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | `success` | 36658 | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ❌ | ❌ | `success_but_weak_oracle_ineligible` | 135983 | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299/report.md` |

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
- node trace count 范围：min=6，max=21；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：4/4 success，rejected=0，budget_exhausted=0，total_tokens=770553。
- 主结果候选：当前 3/4 个非 infrastructure run 可进入 main_result_eligible；provider/network invalid=0 个，只能作为 infrastructure evidence。

### 主结果候选 vs Path2 ref-model 蓝本边界

- Path2 run-validity：0/1 个 Path2 run 的 `main_result_eligible=true`；这只表示 run/schema/secret/trace/final verdict 可进入主结果候选。
- Path2 blueprint-validity：0/1 个 Path2 run 当前可作为 `path2_ref_model_blueprint_eligible=true`；该字段比 `main_result_eligible` 更严格。
- `path2_lng_ems`：main_result_eligible=`false`，path2_ref_model_blueprint_eligible=`false`，state_mode_decorative=`true`；reason=run_not_main_result_eligible
- 解释：`path2_ref_model_blueprint_eligible=false` 不会把有效 run 改成 provider invalid；它只禁止把 state-mode-decorative / 条件分类式模型宣传为 Path2 ref-model 主蓝本。

### 主要失败模式

- `success`：3 run(s)。
- `success_but_weak_oracle_ineligible`：1 run(s)。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=success，最大 observed iteration_count=4。
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

state ABSHydraulicRegulator {
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'completion_chars': 18548, 'completion_tokens': 6597, 'estimated_completion_tokens': 4638, 'estimated_prompt_tokens': 25746, 'estimated_total_tokens': 30384, 'n_calls': 3, 'prompt_chars': 102981, 'prompt_tokens': 26588, 'token_usage_available': True, 'token_usage_unavailable_calls': 0, 'total_tokens': 33185}` / `126.877s` |
| full stage table | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4/report.md` §4 |
| run record | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz` |
| logs | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4/run_logs/stdout.txt`, `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4/run_logs/stderr.txt` |
| checks / repro | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4/checks.json`, `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:6e90ca33d1664c94396e2145605c8fbaff2199c4ee93bd396ae3a332561cedb1` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `6` |
| `langgraph_node_trace_hash` | `sha256:551ce01053da9bba711a382101de4235854e15508f8676d16863cb2b1134067d` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `6` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9112 | 生成初始 DSL 与 grounding seeds | initial len=491 | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=12118 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=11955 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T16:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T16:42:54Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T16:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T16:42:54Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T16:43:45Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T16:43:45Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=491,hash=sha256:a895b7dee2e6 |
| 7 | `2026-06-04T16:43:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-04T16:43:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-04T16:43:45Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:a895b7dee2e6db8e3ccac499fd4b601a22e601427bb3da2234657a3d18b71df4 |
| 10 | `2026-06-04T16:43:45Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=491,hash=sha256:a895b7dee2e6, current_hash=sha256:a895b7dee2e6db8e3ccac499fd4b601a22e601427bb3da2234657a3d18b71df4 |
| 11 | `2026-06-04T16:43:45Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 12 | `2026-06-04T16:43:45Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T16:43:45Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 14 | `2026-06-04T16:43:46Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T16:43:46Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 16 | `2026-06-04T16:43:46Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-04T16:43:46Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 18 | `2026-06-04T16:44:24Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T16:44:24Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-04T16:44:24Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 21 | `2026-06-04T16:44:24Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 22 | `2026-06-04T16:44:24Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-04T16:44:24Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 24 | `2026-06-04T16:45:00Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T16:45:00Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-04T16:45:00Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 27 | `2026-06-04T16:45:00Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 28 | `2026-06-04T16:45:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-04T16:45:00Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=491,hash=sha256:a895b7dee2e6 |
| 30 | `2026-06-04T16:45:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-04T16:45:00Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=491,hash=sha256:a895b7dee2e6 |
| 32 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_enters_increase_outputs` | default-init probe: first empty cycle dispatches initial transition to increase and applies inlet-valve command k1=1,k2=...<truncated 6 chars> | ✅ |
| `increase_to_hold_at_upper_boundary` | explicit-hot-start probe: increase must transition to hold exactly at slp=0.01 and neutralize valves. | ✅ |
| `increase_no_fire_above_upper_boundary` | explicit-hot-start no-fire probe: increase must remain increase when slp is just above 0.01. | ✅ |
| `hold_to_increase_above_upper_boundary` | explicit-hot-start probe: hold must transition to increase when slp is greater than 0.01 and set inlet-valve command. | ✅ |
| `hold_no_fire_at_upper_boundary` | explicit-hot-start no-fire probe: hold must not transition to increase at exactly slp=0.01 because the guard is strict g...<truncated 12 chars> | ✅ |
| `hold_to_decrease_below_lower_boundary` | explicit-hot-start probe: hold must transition to decrease when slp is less than -0.01 and command pressure release k2=1...<truncated 7 chars> | ✅ |
| `hold_no_fire_at_lower_boundary` | explicit-hot-start no-fire probe: hold must not transition to decrease at exactly slp=-0.01 because the guard is strict ...<truncated 10 chars> | ✅ |
| `decrease_to_hold_at_lower_boundary` | explicit-hot-start probe: decrease must transition to hold exactly at slp=-0.01 and neutralize valves and pump. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2062, 'completion_chars': 6799, 'completion_tokens': 2719, 'elapsed_seconds': 51.346280961995944, 'estimated_completion_tokens': 1700, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 8193, 'first_chunk_seconds': 14.12808608301566, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9112}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1481, 'completion_chars': 5334, 'completion_tokens': 2000, 'elapsed_seconds': 38.29454934000387, 'estimated_completion_tokens': 1334, 'estimated_prompt_tokens': 9881, 'estimated_total_tokens': 11215, 'first_chunk_seconds': 12.412582627992379, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39523, 'prompt_tokens': 10118, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12118}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1483, 'completion_chars': 6415, 'completion_tokens': 1878, 'elapsed_seconds': 36.333662268996704, 'estimated_completion_tokens': 1604, 'estimated_prompt_tokens': 9372, 'estimated_total_tokens': 10976, 'first_chunk_seconds': 9.595717585005332, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 37486, 'prompt_tokens': 10077, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 11955}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_abs-default-prlanggraph-stategraph-r2-e849dad4/report.md` §7。

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
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 0;
def float buffer_bp = 0.0;
def float log_infusion_rate = 0.0;

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
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
                }
            }
            during {
                pump_speed = built_in_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                if [pump_fault > 0] {
                    CA_mode = 0;
                    control_released = 1;
                    alarm_signal = 1;
                } else {
                    CA_mode = 1;
                    control_released = 0;
                    alarm_signal = 0;
                }
            }
        }

        state AutocontrolNormal {
            during {
                buffer_bp = blood_pressure;
                if [blood_pressure > target_bp] {
                    flow_rate = flow_rate - 1.0;
                } else if [blood_pressure < target_bp] {
                    flow_rate = flow_rate + 1.0;
                } else {
                    flow_rate = flow_rate;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_infusion_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: SetpointChanged effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> PumpFault : if [pump_fault > 0];
        AutocontrolInit -> AutocontrolNormal : if [pump_fault == 0];
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `4` / `4` / `3` / `7` |
| token / elapsed | `{'completion_chars': 134322, 'completion_tokens': 44509, 'estimated_completion_tokens': 33587, 'estimated_prompt_tokens': 544600, 'estimated_total_tokens': 578187, 'n_calls': 17, 'prompt_chars': 2178376, 'prompt_tokens': 520218, 'token_usage_available': True, 'token_usage_unavailable_calls': 0, 'total_tokens': 564727}` / `865.721s` |
| full stage table | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c/report.md` §4 |
| run record | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c/pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz` |
| logs | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c/run_logs/stdout.txt`, `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c/run_logs/stderr.txt` |
| checks / repro | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c/checks.json`, `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:dc5b944f171d8a7e812e83bf63456d149da939d74db976c3e43bb25d870df2fd` |
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
| `langgraph_node_trace_hash` | `sha256:882d0407c200131292f62fb6e94e6f801941edc6b71d41db564ee5d1275ea22f` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12703 | 生成初始 DSL 与 grounding seeds | initial len=2318 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=93029 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=101283 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=184771 | LLM per-request accept/reject + repair | candidate len=2345,2468,2923,2757 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=172941 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=93029 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=101283 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=184771 | LLM per-request accept/reject + repair | candidate len=2345,2468,2923,2757 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=172941 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=93029 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=101283 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=184771 | LLM per-request accept/reject + repair | candidate len=2345,2468,2923,2757 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=4, tokens=172941 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=184771 | LLM per-request accept/reject + repair | candidate len=2345,2468,2923,2757 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=172941 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=93029 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=101283 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T16:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T16:42:54Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T16:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T16:42:54Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T16:44:49Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T16:44:49Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2318,hash=sha256:43713af1d56b |
| 7 | `2026-06-04T16:44:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-04T16:44:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-04T16:44:49Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:43713af1d56bda024bb0ebc14e14e97da1de77eb364dd7aad87eecf7bfa366db |
| 10 | `2026-06-04T16:44:49Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2318,hash=sha256:43713af1d56b, current_hash=sha256:43713af1d56bda024bb0ebc14e14e97da1de77eb364dd7aad87eecf7bfa366db |
| 11 | `2026-06-04T16:44:49Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 12 | `2026-06-04T16:44:49Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T16:44:49Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 14 | `2026-06-04T16:44:49Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T16:44:49Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 16 | `2026-06-04T16:44:49Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-04T16:44:49Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 18 | `2026-06-04T16:45:58Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T16:45:58Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-04T16:45:58Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 21 | `2026-06-04T16:45:58Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 22 | `2026-06-04T16:45:58Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-04T16:45:58Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 24 | `2026-06-04T16:46:52Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T16:46:52Z` | `SL-7` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-04T16:46:52Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 27 | `2026-06-04T16:46:52Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["DSL: PumpFault -> Manual :: FaultRemoved; with no guard/effect on pump_fault.", "DSL: Manual.enter clears alarm_signal to 0.", "Simulation: after FaultRemoved, state is Manual with pump_fault = 1 and alarm_signal = 0."], "severity": "major", "summary": "Fault recovery can clear the alarm...<truncated 222 chars> | <none> |
| 28 | `2026-06-04T16:46:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-04T16:46:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-04T16:46:52Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["DSL: PumpFault -> Manual :: FaultRemoved; with no guard/effect on pump_fault.", "DS
... <truncated 7987 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 |
|---|---|---|---|---|---|
| `default_init_enters_manual_and_sets_manual_outputs` | default-init: first empty cycle dispatches to Manual and manual operation uses the built-in switch speed and caregiver d...<truncated 17 chars> | ✅ | ✅ | ✅ | ✅ |
| `initiate_setpoint_start_ac_to_normal_high_pressure` | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC to enter AutocontrolInit, then no...<truncated 70 chars> | ✅ | ✅ | ✅ | ✅ |
| `autocontrol_normal_no_fault_low_pressure_increases_flow` | explicit-hot-start: from reachable AutocontrolNormal with no pump fault, CARA remains in normal autocontrol and raises f...<truncated 34 chars> | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_enters_alarm_state_then_fault_removed_returns_manual` | explicit-hot-start: pump fault during normal autocontrol enters PumpFault with alarm/control release, then FaultRemoved ...<truncated 56 chars> | ✅ | ✅ | ✅ | ✅ |
| `ca_and_cb_backmanual_force_manual_from_ask_and_init` | explicit-hot-start: cross-component CA_backManual and CB_backManual force Manual from distinct autocontrol-related leave...<truncated 28 chars> | ✅ | ✅ | ✅ | ✅ |
| `cp_backmanual_forces_manual_from_autocontrol_normal` | explicit-hot-start: CP_backManual forces Manual from AutocontrolNormal as the shared recovery target. | ✅ | ✅ | ✅ | ✅ |
| `cc_backmanual_forces_manual_from_pump_fault` | explicit-hot-start: CC_backManual forces Manual from PumpFault as the shared recovery target, but with an unresolved act...<truncated 40 chars> | ✅ | ✅ | ✅ | ✅ |
| `terminate_ac_forces_manual_from_autocontrol_init` | explicit-hot-start: caregiver TerminateAC during algorithmic control forces Manual and releases software control. | ✅ | ✅ | ✅ | ✅ |
| `fault_removed_clears_pump_fault_effect` | explicit-hot-start: directly probes the FaultRemoved transition effect so missing or wrong pump_fault clearing fails. | ⚪ | ✅ | ✅ | ✅ |
| `setpoint_changed_effect_uses_requested_target` | explicit-hot-start: directly probes the SetpointChanged effect so missing or wrong target_bp assignment fails. | ⚪ | ✅ | ✅ | ✅ |
| `start_ac_with_active_fault_routes_to_pump_fault` | explicit-hot-start: active pump fault while starting autocontrol should not proceed to normal control; AutocontrolInit r...<truncated 59 chars> | ⚪ | ⚪ | ⚪ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:8d8bee3d93ca11a6f72e62f677cf8efec1d48133d8ee73ceeef315da4e74ef9a` |
| 2 | `1` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:74b4333340ba8396c1696cf465c02e6614ac2b582ad47631a8bf8a7d47e26680` |
| 3 | `2` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 689 chars> | `sha256:c7b912815fce0736811c5a1361188b7cb22d932c2ba455ec05433adac293ffb1` |
| 4 | `2` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:55db32db5a501930ea9caacc612bf09595ad3465ad588dfebdd27c8de7eeebea` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c/report.md` §7。

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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'completion_chars': 28002, 'completion_tokens': 9585, 'estimated_completion_tokens': 7001, 'estimated_prompt_tokens': 26617, 'estimated_total_tokens': 33618, 'n_calls': 3, 'prompt_chars': 106463, 'prompt_tokens': 27073, 'token_usage_available': True, 'token_usage_unavailable_calls': 0, 'total_tokens': 36658}` / `181.035s` |
| full stage table | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1/report.md` §4 |
| run record | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1/pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz` |
| logs | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1/run_logs/stdout.txt`, `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1/run_logs/stderr.txt` |
| checks / repro | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1/checks.json`, `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:008fff319b0ce5a0b3a82eca0c63324797601d9b1e5435e698385ea6ba66c14b` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `6` |
| `langgraph_node_trace_hash` | `sha256:551ce01053da9bba711a382101de4235854e15508f8676d16863cb2b1134067d` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `6` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=10643 | 生成初始 DSL 与 grounding seeds | initial len=669 | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=14584 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=11431 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T16:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T16:42:54Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T16:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T16:42:54Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T16:44:12Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T16:44:12Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=669,hash=sha256:f01d793ff735 |
| 7 | `2026-06-04T16:44:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-04T16:44:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-04T16:44:12Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:f01d793ff73542443089e3b4ce8b98c438d4cd4be9a79525664c83dccc1e4c1c |
| 10 | `2026-06-04T16:44:12Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=669,hash=sha256:f01d793ff735, current_hash=sha256:f01d793ff73542443089e3b4ce8b98c438d4cd4be9a79525664c83dccc1e4c1c |
| 11 | `2026-06-04T16:44:12Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 12 | `2026-06-04T16:44:13Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T16:44:13Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 14 | `2026-06-04T16:44:13Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T16:44:13Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 16 | `2026-06-04T16:44:13Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-04T16:44:13Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 18 | `2026-06-04T16:45:12Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T16:45:12Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-04T16:45:12Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 21 | `2026-06-04T16:45:12Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 22 | `2026-06-04T16:45:12Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-04T16:45:12Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 24 | `2026-06-04T16:45:54Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T16:45:54Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-04T16:45:54Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 27 | `2026-06-04T16:45:54Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 28 | `2026-06-04T16:45:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-04T16:45:54Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=669,hash=sha256:f01d793ff735 |
| 30 | `2026-06-04T16:45:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-04T16:45:54Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=669,hash=sha256:f01d793ff735 |
| 32 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_idle_then_f2_request` | default-init verifies initial dispatch to F1, no-request idle at F1, then PS2 starts upward travel to MU2 and S2 arrival...<truncated 12 chars> | ✅ |
| `default_init_f1_to_mu3_then_reset` | default-init reaches F1 first, then PS3 starts upward travel to MU3 and reset forces return to stopped F1 from motion | ✅ |
| `f2_to_f3_then_down_to_f1_chain` | explicit-hot-start at F2 checks immediate next-destination workflow: PS3 to MU3, S3 to F3, PS1 to MD1, S1 to F1 | ✅ |
| `f2_request_floor1_then_reset_from_md1` | explicit-hot-start at F2 verifies PS1 selects downward MD1 drive and reset also forces stopped F1 from downward motion | ✅ |
| `f3_request_floor2_via_md2` | explicit-hot-start at F3 verifies PS2 selects downward MD2 drive and S2 arrival stops at F2 | ✅ |
| `reset_from_stopped_floor3` | explicit-hot-start at F3 verifies the global reset forces stopped F1 even from a stopped floor context | ✅ |
| `md2_ignores_no_arrival_then_reset` | explicit-hot-start at MD2 checks no phantom transition without an arrival sensor, then reset forces stopped F1 from MD2 | ✅ |
| `mu2_ignores_no_arrival_then_reset` | explicit-hot-start at MU2 checks no phantom transition without an arrival sensor, then reset forces stopped F1 from MU2 | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3399, 'completion_chars': 11972, 'completion_tokens': 4205, 'elapsed_seconds': 78.51136213197606, 'estimated_completion_tokens': 2993, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 9516, 'first_chunk_seconds': 17.23658820198034, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10643}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2113, 'completion_chars': 8422, 'completion_tokens': 3150, 'elapsed_seconds': 58.80799321900122, 'estimated_completion_tokens': 2106, 'estimated_prompt_tokens': 11272, 'estimated_total_tokens': 13378, 'first_chunk_seconds': 20.665226371987956, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 45088, 'prompt_tokens': 11434, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14584}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1711, 'completion_chars': 7608, 'completion_tokens': 2230, 'elapsed_seconds': 42.78150214598281, 'estimated_completion_tokens': 1902, 'estimated_prompt_tokens': 8822, 'estimated_total_tokens': 10724, 'first_chunk_seconds': 13.677543956990121, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 35286, 'prompt_tokens': 9201, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 11431}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path1_elevator-default-prlanggraph-stategraph-r2-64d316c1/report.md` §7。

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
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbatt_dis_max = 0.0;
def float Pbatt_ch_max = 0.0;
def float Pgen_req = 0.0;
def float Pbatt_discharge = 0.0;
def float Pbatt_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cut_in = 0;
def int cmd_LNG_cut_out = 1;
def int cmd_DG1_cut_in = 0;
def int cmd_DG1_cut_out = 1;
def int cmd_DG2_cut_in = 0;
def int cmd_DG2_cut_out = 1;
def int cmd_load_cut_in = 1;
def int cmd_load_cut_out = 0;

state LNGShipEMS {
    ! * -> ZeroIdle : if [PL <= 0 && Ppv + Pw <= 0];
    ! * -> ZeroLoadCharge : if [PL <= 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL <= 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RESCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.3 && PL - Ppv - Pw <= Pbatt_dis_max];
    ! * -> LNGOnlyNormal : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.3 && PL - Ppv - Pw > Pbatt_dis_max && PL - Ppv - Pw <= eng3_Pmax];
    ! * -> LNGChargeLowSoC : if [PL > 0 && Ppv + Pw < PL && SoC < 0.3 && PL - Ppv - Pw + Pgmax / 5 <= eng3_Pmax];
    ! * -> LNGDG1Normal : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.3 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pd1max];
    ! * -> LNGDG1ChargeLowSoC : if [PL > 0 && Ppv + Pw < PL && SoC < 0.3 && PL - Ppv - Pw + Pgmax / 5 > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= eng3_Pmax + Pd1max];
    ! * -> LNGDG1DG2 : if [PL > 0 && Ppv + Pw < PL && ((SoC >= 0.3 && PL - Ppv - Pw > eng3_Pmax + Pd1max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max) || (SoC < 0.3 && PL - Ppv - Pw + Pd1max / 10 > eng3_Pmax + Pd1max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max))];
    ! * -> IllegalOverloadAllThermalBattery : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroIdle;

    state ZeroIdle {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = 0;
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

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = Ppv + Pw;
            Pspare = 0;
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
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = Ppv + Pw;
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

    state RESCharge {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = Ppv + Pw - PL;
            Pspare = 0;
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

    state RESSpare {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = Ppv + Pw - PL;
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

    state BatteryAssist {
        enter {
            Pgen_req = 0;
            Pbatt_discharge = PL - Ppv - Pw;
            Pbatt_charge = 0;
            Pspare = 0;
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

    state LNGOnlyNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = 0;
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

    state LNGChargeLowSoC {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbatt_discharge = 0;
            Pbatt_charge = Pgmax / 5;
            Pspare = 0;
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

    state LNGDG1Normal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = 0;
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

    state LNGDG1ChargeLowSoC {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbatt_discharge = 0;
            Pbatt_charge = Pd1max / 10;
            Pspare = 0;
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

    state LNGDG1DG2 {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbatt_discharge = 0;
            Pbatt_charge = 0;
            Pspare = 0;
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

    state IllegalOverloadAllThermalBattery {
        enter {
            Pgen_req = eng3_Pmax + Pd1max + Pd2max;
            Pbatt_discharge = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbatt_charge = 0;
            Pspare = 0;
            cmd_LNG_cut_in = 1;
            cmd_LNG_cut_out = 0;
            cmd_DG1_cut_in = 1;
            cmd_DG1_cut_out = 0;
            cmd_DG2_cut_in = 1;
            cmd_DG2_cut_out = 0;
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
| failure class | `success_but_weak_oracle_ineligible` |
| main_result_eligible | `false` |
| path2_ref_model_blueprint | `false`；run_not_main_result_eligible |
| state_mode_decorative | `true` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `3` |
| token / elapsed | `{'completion_chars': 66259, 'completion_tokens': 23950, 'estimated_completion_tokens': 16568, 'estimated_prompt_tokens': 102561, 'estimated_total_tokens': 119129, 'n_calls': 5, 'prompt_chars': 410234, 'prompt_tokens': 112033, 'token_usage_available': True, 'token_usage_unavailable_calls': 0, 'total_tokens': 135983}` / `450.258s` |
| full stage table | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299/report.md` §4 |
| run record | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz` |
| logs | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299/run_logs/stdout.txt`, `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299/run_logs/stderr.txt` |
| checks / repro | `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299/checks.json`, `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:2ecf39a258621bb38220988fb434202b7cb28684cbb1e16613a3e42957599fb4` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `6` |
| `langgraph_node_trace_hash` | `sha256:551ce01053da9bba711a382101de4235854e15508f8676d16863cb2b1134067d` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `6` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14312 | 生成初始 DSL 与 grounding seeds | initial len=7453 | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=179, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=71263 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=71263 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=71263 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=50408 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T16:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T16:42:54Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T16:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T16:42:54Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T16:45:18Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T16:45:18Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=7453,hash=sha256:320beb5058ff |
| 7 | `2026-06-04T16:45:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-04T16:45:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-04T16:45:18Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:320beb5058ff8e8e82c3e3219e118f64e4254e10fd6c325031622a0a6953a1d5 |
| 10 | `2026-06-04T16:45:18Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=7453,hash=sha256:320beb5058ff, current_hash=sha256:320beb5058ff8e8e82c3e3219e118f64e4254e10fd6c325031622a0a6953a1d5 |
| 11 | `2026-06-04T16:45:18Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 12 | `2026-06-04T16:45:18Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T16:45:18Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 14 | `2026-06-04T16:45:18Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T16:45:18Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 16 | `2026-06-04T16:45:18Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-04T16:45:18Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 18 | `2026-06-04T16:46:41Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T16:46:42Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 20 | `2026-06-04T16:46:42Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 21 | `2026-06-04T16:47:48Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T16:47:48Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 23 | `2026-06-04T16:47:48Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 24 | `2026-06-04T16:49:30Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T16:49:31Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-04T16:49:31Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 27 | `2026-06-04T16:49:31Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 28 | `2026-06-04T16:49:31Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 29 | `2026-06-04T16:49:31Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 30 | `2026-06-04T16:49:31Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 31 | `2026-06-04T16:50:24Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 32 | `2026-06-04T16:50:24Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-04T16:50:24Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 34 | `2026-06-04T16:50:24Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 35 | `2026-06-04T16:50:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 36 | `2026-06-04T16:50:24Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=7453,hash=sha256:320beb5058ff |
| 37 | `2026-06-04T16:50:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 38 | `2026-06-04T16:50:24Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=7453,hash=sha256:320beb5058ff |
| 39 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_zero_idle` | default-init probe: with zero load and no renewable production, the initial dispatch should land in ZeroIdle with no gen...<truncated 54 chars> | ✅ |
| `zero_load_res_charges_battery_below_full_soc` | explicit-hot-start probe: with PL=0, positive RES, and SoC below 0.95, renewable production should be sent to battery ch...<truncated 7 chars> | ✅ |
| `zero_load_res_spare_at_full_soc_boundary` | explicit-hot-start boundary probe: with PL=0, positive RES, and SoC exactly 0.95, renewable production should become spa...<truncated 30 chars> | ✅ |
| `res_covers_load_charges_battery_below_full_soc` | explicit-hot-start probe: when RES covers positive load and SoC is below 0.95, all load should be served from RES and re...<truncated 35 chars> | ✅ |
| `res_covers_load_spare_at_full_soc_boundary` | explicit-hot-start boundary probe: when RES covers positive load and SoC is exactly 0.95, residual RES should be spare p...<truncated 32 chars> | ✅ |
| `battery_assist_at_soc_and_discharge_capacity_boundary` | explicit-hot-start boundary probe: with RES below load, SoC exactly 0.3, and deficit equal to battery discharge capacity...<truncated 55 chars> | ✅ |
| `lng_only_after_battery_capacity_exceeded` | explicit-hot-start boundary probe: when RES and battery are insufficient but deficit is exactly within LNG capacity, LNG...<truncated 76 chars> | ✅ |
| `low_soc_lng_charge_margin` | explicit-hot-start low-SoC probe: when SoC is below 0.3 and LNG can cover deficit plus Pgmax/5 charging margin, LNG shou...<truncated 42 chars> | ✅ |
| `lng_dg1_normal_after_lng_capacity_exceeded` | explicit-hot-start boundary probe: with suitable SoC and deficit above LNG capacity but within LNG plus DG1, LNG and DG1...<truncated 40 chars> | ✅ |
| `low_soc_lng_dg1_charge_margin` | explicit-hot-start low-SoC probe: when LNG alone cannot cover the low-SoC charging case, DG1 should be added and Pd1max/...<truncated 44 chars> | ✅ |
| `lng_dg1_dg2_last_priority` | explicit-hot-start probe: when RES, battery, LNG, and DG1 are insufficient but deficit is within LNG+DG1+DG2, DG2 should...<truncated 32 chars> | ✅ |
| `illegal_overload_all_thermal_and_battery_lack` | explicit-hot-start overload probe: when extreme demand exceeds all RES and thermal resources, the illegal overload compl...<truncated 108 chars> | ✅ |
| `forced_reclassification_from_default_zero_idle_to_res_charge` | default-init forced-transition probe: after the default initial cycle parks in ZeroIdle, nonzero load fully covered by R...<truncated 84 chars> | ✅ |
| `forced_reclassification_from_default_zero_idle_to_illegal_overload` | default-init forced-transition probe: after the default initial cycle parks in ZeroIdle, extreme demand beyond all RES a...<truncated 98 chars> | ✅ |
| `forced_reclassification_from_res_charge_to_dg2_mode` | explicit-hot-start forced-transition probe: from an already active RESCharge leaf, changed operating conditions requirin...<truncated 80 chars> | ✅ |
| `forced_reclassification_from_overload_to_zero_load_spare` | explicit-hot-start forced-transition probe: from the illegal overload leaf, zero load with positive RES and SoC at least...<truncated 107 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5897, 'completion_chars': 19601, 'completion_tokens': 7843, 'elapsed_seconds': 144.0797747040051, 'estimated_completion_tokens': 4901, 'estimated_prompt_tokens': 6646, 'estimated_total_tokens': 11547, 'first_chunk_seconds': 37.796556725981645, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26582, 'prompt_tokens': 6469, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14312}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3434, 'completion_chars': 11909, 'completion_tokens': 4471, 'elapsed_seconds': 82.9552443959983, 'estimated_completion_tokens': 2978, 'estimated_prompt_tokens': 15723, 'estimated_total_tokens': 18701, 'first_chunk_seconds': 23.108589836978354, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 62889, 'prompt_tokens': 16682, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21153}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2952, 'completion_chars': 9747, 'completion_tokens': 3471, 'elapsed_seconds': 65.18610518900095, 'estimated_completion_tokens': 2437, 'estimated_prompt_tokens': 18865, 'estimated_total_tokens': 21302, 'first_chunk_seconds': 13.073469503986416, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 75457, 'prompt_tokens': 20235, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23706}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4897, 'completion_chars': 17169, 'completion_tokens': 5416, 'elapsed_seconds': 101.7040383759886, 'estimated_completion_tokens': 4293, 'estimated_prompt_tokens': 19565, 'estimated_total_tokens': 23858, 'first_chunk_seconds': 12.399578518001363, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 78260, 'prompt_tokens': 20988, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26404}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1712, 'completion_chars': 7833, 'completion_tokens': 2749, 'elapsed_seconds': 52.38402196101379, 'estimated_completion_tokens': 1959, 'estimated_prompt_tokens': 41762, 'estimated_total_tokens': 43721, 'first_chunk_seconds': 21.39768795101554, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 167046, 'prompt_tokens': 47659, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 50408}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success_but_weak_oracle_ineligible`。
- required stages executed：`16/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`3`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_langgraph_real_agent_loop_round2_stategraph_fix/pr-e1-path2_lng_ems-default-prlanggraph-stategraph-r2-664c3299/report.md` §7。

</details>
