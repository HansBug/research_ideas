## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/`。

| Path | case | config | verdict | status | clean | eligible | path2 blueprint | post-accept | failure class | token usage | report |
|---|---|---|---|---|---:|---:|---|---|---|---|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 32797 | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 35093 | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ✅ | ⚪ | ⚪ 0 | `success` | 925233 | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | ❌ | ⚪ 0 | `success` | 220578 | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949/report.md` |

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
- node trace count 范围：min=16，max=109；每个 run 的详细 trace 见 report §1.1、run record `run_config.langgraph_node_trace` 与 final_artifacts。
- checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`；real_agent_loop_resume_supported=`False`。
- 重要边界：本 PR 当前只宣称 LangGraph interrupt/resume API 与 toy FixLog-like ledger smoke；不宣称真实 agent-loop 主图的跨进程/中断恢复已进入主结果证据。

### 初步观察

- `default`：4/4 success，rejected=0，budget_exhausted=0，total_tokens=1213701。
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
- `path2_lng_ems`：失败/成功类别=success，最大 observed iteration_count=2。
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
| token / elapsed | `{'prompt_tokens': 26656, 'completion_tokens': 6141, 'total_tokens': 32797, 'estimated_prompt_tokens': 26045, 'estimated_completion_tokens': 4256, 'estimated_total_tokens': 30301, 'prompt_chars': 104176, 'completion_chars': 17019, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `120.301s` |
| full stage table | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f/report.md` §4 |
| run record | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f/pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz` |
| logs | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f/run_logs/stdout.txt`, `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f/run_logs/stderr.txt` |
| checks / repro | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f/checks.json`, `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:743143bb37bb7bd140fc7106e35bae40c25f7d2c69b11daca3fe44c633df78c9` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=8969 | 生成初始 DSL 与 grounding seeds | initial len=608 | [`record`](./pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=12280 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=11548 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-07T03:09:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-07T03:09:34Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-07T03:09:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-07T03:09:34Z` | `SL-1` | `-` | `lg_d2_envelope_enter` | {} | <none> |
| 5 | `2026-06-07T03:09:34Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 6 | `2026-06-07T03:10:24Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 7 | `2026-06-07T03:10:24Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=608,hash=sha256:6067f2d95bd7 |
| 8 | `2026-06-07T03:10:24Z` | `SL-1` | `-` | `lg_d2_envelope_exit` | {} | <none> |
| 9 | `2026-06-07T03:10:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 10 | `2026-06-07T03:10:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-07T03:10:24Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:6067f2d95bd7e8dd8d2c337c8a42947a8dc500e3fb2939dfbff6c2ebba9d971c |
| 12 | `2026-06-07T03:10:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-07T03:10:24Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=608,hash=sha256:6067f2d95bd7, current_hash=sha256:6067f2d95bd7e8dd8d2c337c8a42947a8dc500e3fb2939dfbff6c2ebba9d971c |
| 14 | `2026-06-07T03:10:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 15 | `2026-06-07T03:10:24Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 16 | `2026-06-07T03:10:24Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-07T03:10:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 18 | `2026-06-07T03:10:24Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 19 | `2026-06-07T03:10:25Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-07T03:10:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 21 | `2026-06-07T03:10:25Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 22 | `2026-06-07T03:10:25Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-07T03:10:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-07T03:10:25Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 25 | `2026-06-07T03:10:25Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 26 | `2026-06-07T03:11:07Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 27 | `2026-06-07T03:11:07Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 28 | `2026-06-07T03:11:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-07T03:11:08Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 30 | `2026-06-07T03:11:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-07T03:11:08Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 32 | `2026-06-07T03:11:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 33 | `2026-06-07T03:11:08Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 34 | `2026-06-07T03:11:08Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 35 | `2026-06-07T03:11:08Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-07T03:11:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-07T03:11:08Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 38 | `2026-06-07T03:11:08Z` | `SL-7` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 39 | `2026-06-07T03:11:34Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 40 | `2026-06-07T03:11:34Z` | `SL-7` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 41 | `2026-06-07T03:11:34Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-07T03:11:34Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 43 | `2026-06-07T03:11:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-07T03:11:34Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 45 | `2026-06-07T03:11:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-07T03:11:34Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=608,hash=sha256:6067f2d95bd7 |
| 47 | `2026-06-07T03:11:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-07T03:11:34Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=608,hash=sha256:6067f2d95bd7 |
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
| `default_init_enters_increase_outputs` | default-init probe: first empty cycle dispatches the initial transition to increase and applies inlet-valve command k1=1...<truncated 12 chars> | ✅ |
| `increase_to_hold_at_slp_upper_boundary` | explicit-hot-start boundary probe: increase must transition to hold when slp is exactly 0.01 and neutralize both valves. | ✅ |
| `increase_no_fire_above_slp_upper_boundary` | explicit-hot-start no-fire probe: increase must not transition to hold when slp is just above 0.01. | ✅ |
| `hold_to_increase_positive_slip_band` | explicit-hot-start boundary probe: hold must stay at slp=0.01 but transition to increase when slp is greater than 0.01. | ✅ |
| `hold_to_increase_above_positive_boundary` | explicit-hot-start transition probe: hold transitions to increase when slp is just above 0.01 and sets k1=1, k2=0, n=0. | ✅ |
| `hold_to_decrease_negative_slip_band` | explicit-hot-start boundary probe: hold must stay at slp=-0.01 but transition to decrease when slp is less than -0.01. | ✅ |
| `hold_to_decrease_below_negative_boundary` | explicit-hot-start transition probe: hold transitions to decrease when slp is just below -0.01 and commands pressure rel...<truncated 17 chars> | ✅ |
| `decrease_to_hold_negative_boundary` | explicit-hot-start boundary probe: decrease must stay below -0.01 but return to hold when slp reaches -0.01. | ✅ |
| `decrease_to_hold_at_negative_boundary` | explicit-hot-start transition probe: decrease transitions to hold when slp is exactly -0.01 and neutralizes valves and p...<truncated 4 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2140, 'completion_chars': 7230, 'completion_tokens': 2576, 'elapsed_seconds': 49.85326341493055, 'estimated_completion_tokens': 1808, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 8301, 'first_chunk_seconds': 11.336613323073834, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 8969}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1687, 'completion_chars': 6079, 'completion_tokens': 2206, 'elapsed_seconds': 42.74897796101868, 'estimated_completion_tokens': 1520, 'estimated_prompt_tokens': 9912, 'estimated_total_tokens': 11432, 'first_chunk_seconds': 12.30567632894963, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39646, 'prompt_tokens': 10074, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12280}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 840, 'completion_chars': 3710, 'completion_tokens': 1359, 'elapsed_seconds': 26.48241439415142, 'estimated_completion_tokens': 928, 'estimated_prompt_tokens': 9640, 'estimated_total_tokens': 10568, 'first_chunk_seconds': 11.258228293154389, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 38558, 'prompt_tokens': 10189, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 11548}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_abs-default-upstream-after-g1-clean-2e0e294f/report.md` §7。

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
| token / elapsed | `{'prompt_tokens': 26932, 'completion_tokens': 8161, 'total_tokens': 35093, 'estimated_prompt_tokens': 26378, 'estimated_completion_tokens': 5616, 'estimated_total_tokens': 31994, 'prompt_chars': 105505, 'completion_chars': 22459, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `156.899s` |
| full stage table | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067/report.md` §4 |
| run record | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067/pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz` |
| logs | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067/run_logs/stdout.txt`, `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067/run_logs/stderr.txt` |
| checks / repro | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067/checks.json`, `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:f364a3a292aed89a9e14d814d06474a3953b39cc44df460d507272a3693dfd73` |
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=10583 | 生成初始 DSL 与 grounding seeds | initial len=659 | [`record`](./pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13706 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10804 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-07T03:11:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-07T03:11:35Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-07T03:11:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-07T03:11:35Z` | `SL-1` | `-` | `lg_d2_envelope_enter` | {} | <none> |
| 5 | `2026-06-07T03:11:35Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 6 | `2026-06-07T03:12:54Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 7 | `2026-06-07T03:12:54Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=659,hash=sha256:a0b11c24e587 |
| 8 | `2026-06-07T03:12:54Z` | `SL-1` | `-` | `lg_d2_envelope_exit` | {} | <none> |
| 9 | `2026-06-07T03:12:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 10 | `2026-06-07T03:12:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-07T03:12:54Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:a0b11c24e58704e6a2e93a84991bf1241e7524ee107639a6504576e458270c99 |
| 12 | `2026-06-07T03:12:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-07T03:12:54Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=659,hash=sha256:a0b11c24e587, current_hash=sha256:a0b11c24e58704e6a2e93a84991bf1241e7524ee107639a6504576e458270c99 |
| 14 | `2026-06-07T03:12:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 15 | `2026-06-07T03:12:54Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 16 | `2026-06-07T03:12:54Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-07T03:12:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 18 | `2026-06-07T03:12:54Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 19 | `2026-06-07T03:12:54Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-07T03:12:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 21 | `2026-06-07T03:12:54Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 22 | `2026-06-07T03:12:54Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-07T03:12:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-07T03:12:54Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 25 | `2026-06-07T03:12:54Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 26 | `2026-06-07T03:13:37Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 27 | `2026-06-07T03:13:37Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 28 | `2026-06-07T03:13:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-07T03:13:37Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 30 | `2026-06-07T03:13:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-07T03:13:37Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 32 | `2026-06-07T03:13:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 33 | `2026-06-07T03:13:37Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 34 | `2026-06-07T03:13:37Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 35 | `2026-06-07T03:13:37Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-07T03:13:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-07T03:13:37Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 38 | `2026-06-07T03:13:37Z` | `SL-7` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 39 | `2026-06-07T03:14:11Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 40 | `2026-06-07T03:14:11Z` | `SL-7` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 41 | `2026-06-07T03:14:11Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-07T03:14:11Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 43 | `2026-06-07T03:14:11Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-07T03:14:11Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 45 | `2026-06-07T03:14:11Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-07T03:14:11Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=659,hash=sha256:a0b11c24e587 |
| 47 | `2026-06-07T03:14:11Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-07T03:14:11Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=659,hash=sha256:a0b11c24e587 |
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
| `default_init_f1_to_f2_then_continue_up` | default-init: dispatches to F1 stopped, then PS2 drives upward to MU2, S2 stops at F2, and the immediate next PS3 reques...<truncated 26 chars> | ✅ |
| `default_init_f1_to_f3_then_down_to_f2` | default-init: from F1, PS3 drives upward to MU3, S3 stops at F3, then PS2 requests downward travel to MD2 and S2 stops a...<truncated 5 chars> | ✅ |
| `hot_start_f2_down_to_f1` | explicit-hot-start: from reachable stopped F2, PS1 must enter downward MD1 and S1 arrival must stop at F1. | ✅ |
| `hot_start_f3_direct_down_to_f1` | explicit-hot-start: from reachable stopped F3, PS1 must choose MD1 downward travel rather than the MD2/F2 branch. | ✅ |
| `reset_forces_motion_up_to_f1` | explicit-hot-start: reset from an upward motion state must force F1 stopped regardless of outstanding request context. | ✅ |
| `reset_forces_motion_down_to_f1` | explicit-hot-start: reset from a downward motion state must force F1 stopped regardless of outstanding request context. | ✅ |
| `reset_forces_floor_state_to_f1` | explicit-hot-start: reset from a non-F1 stopped floor state must force the controller back to F1 stopped. | ✅ |
| `no_event_stays_stopped_at_floor` | explicit-hot-start: with no request or arrival event, a stopped floor state should not make a phantom transition and sho...<truncated 36 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3497, 'completion_chars': 12150, 'completion_tokens': 4145, 'elapsed_seconds': 78.45320341782644, 'estimated_completion_tokens': 3038, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 9561, 'first_chunk_seconds': 15.50553652504459, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10583}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1317, 'completion_chars': 5054, 'completion_tokens': 2236, 'elapsed_seconds': 43.05050334567204, 'estimated_completion_tokens': 1264, 'estimated_prompt_tokens': 11268, 'estimated_total_tokens': 12532, 'first_chunk_seconds': 18.687361572869122, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 45070, 'prompt_tokens': 11470, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13706}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1261, 'completion_chars': 5255, 'completion_tokens': 1780, 'elapsed_seconds': 34.44846665812656, 'estimated_completion_tokens': 1314, 'estimated_prompt_tokens': 8587, 'estimated_total_tokens': 9901, 'first_chunk_seconds': 13.129944015294313, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 34346, 'prompt_tokens': 9024, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10804}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_elevator-default-upstream-after-g1-clean-10972067/report.md` §7。

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
def int pump_speed_source = 0;
def int software_control = 0;
def int control_released = 0;
def int pump_complication = 0;
def int alarm_display = 0;
def int alarm_sound = 0;
def int log_records = 0;
def float manual_default_flow_rate = 1.0;
def float pump_flow_rate = 0.0;
def float control_voltage = 0.0;
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float target_blood_pressure = 100.0;
def float requested_target_blood_pressure = 100.0;
def float infusion_rate = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! Ask_StartAC -> AutocontrolInit :: StartAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_released = 1;
                pump_speed_source = 0;
                pump_flow_rate = manual_default_flow_rate;
                if [pump_complication > 0] {
                    alarm_display = 1;
                    alarm_sound = 1;
                } else {
                    alarm_display = 0;
                    alarm_sound = 0;
                }
            }
        }

        state Ask_StartAC {
            [*] -> SetpointEditing;

            state SetpointEditing {
                during {
                    sensor_buffer_bp = blood_pressure;
                }
            }

            SetpointEditing -> SetpointEditing :: ChangeSetpoint effect {
                target_blood_pressure = requested_target_blood_pressure;
            };
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                control_released = 0;
                pump_speed_source = 1;
                alarm_display = 0;
                alarm_sound = 0;
            }
        }

        state NormalAutocontrol {
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure > target_blood_pressure] {
                    infusion_rate = 1.0;
                } else {
                    infusion_rate = 2.0;
                }
                pump_flow_rate = infusion_rate;
                control_voltage = infusion_rate;
                log_records = log_records + 1;
            }
        }

        state PumpFault {
            enter {
                pump_complication = 1;
                alarm_display = 1;
                alarm_sound = 1;
                software_control = 0;
                control_released = 1;
                CA_mode = 0;
                pump_flow_rate = manual_default_flow_rate;
                pump_speed_source = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        AutocontrolInit -> NormalAutocontrol;
        NormalAutocontrol -> Manual :: TerminateAC;
        NormalAutocontrol -> PumpFault :: PumpFaultDetected;
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `6` / `4` / `11` |
| token / elapsed | `{'prompt_tokens': 865250, 'completion_tokens': 59983, 'total_tokens': 925233, 'estimated_prompt_tokens': 961185, 'estimated_completion_tokens': 45927, 'estimated_total_tokens': 1007112, 'prompt_chars': 3844696, 'completion_chars': 183688, 'n_calls': 22, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `1179.38s` |
| full stage table | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98/report.md` §4 |
| run record | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98/pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz` |
| logs | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98/run_logs/stdout.txt`, `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98/run_logs/stderr.txt` |
| checks / repro | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98/checks.json`, `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:9eadf3465ababf85e7182c07bc852974fc72cec520a007792dc394322e9442ff` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `109` |
| `langgraph_node_trace_hash` | `sha256:1c046682cec8dc6993bef61e653946cbcfffcf14b0c816d9cc19a827877c67dd` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `109` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=13054 | 生成初始 DSL 与 grounding seeds | initial len=3065 | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=27, info=1; blocking=0, advisory=27, info=1; blocking=0, advisory=26, info=1; blocking=0, advisory=27, info=1; blocking=0, advisory=26, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=161307 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=161307 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=161307 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=373389 | LLM per-request accept/reject + repair | candidate len=3072,3116,3067,3143,3067,3239 | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=6, tokens=325876 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=373389 | LLM per-request accept/reject + repair | candidate len=3072,3116,3067,3143,3067,3239 | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=6, tokens=325876 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=373389 | LLM per-request accept/reject + repair | candidate len=3072,3116,3067,3143,3067,3239 | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=6, tokens=325876 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=27, info=1; blocking=0, advisory=27, info=1; blocking=0, advisory=26, info=1; blocking=0, advisory=27, info=1; blocking=0, advisory=26, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=161307 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=51607 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=373389 | LLM per-request accept/reject + repair | candidate len=3072,3116,3067,3143,3067,3239 | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=6, tokens=325876 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=27, info=1; blocking=0, advisory=27, info=1; blocking=0, advisory=26, info=1; blocking=0, advisory=27, info=1; blocking=0, advisory=26, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=161307 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=373389 | LLM per-request accept/reject + repair | candidate len=3072,3116,3067,3143,3067,3239 | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=6, tokens=325876 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=27, info=1; blocking=0, advisory=27, info=1; blocking=0, advisory=26, info=1; blocking=0, advisory=27, info=1; blocking=0, advisory=26, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=161307 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=373389 | LLM per-request accept/reject + repair | candidate len=3072,3116,3067,3143,3067,3239 | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=6, tokens=325876 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=27, info=1; blocking=0, advisory=27, info=1; blocking=0, advisory=26, info=1; blocking=0, advisory=27, info=1; blocking=0, advisory=26, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=161307 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=51607 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-07T03:14:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-07T03:14:12Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-07T03:14:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-07T03:14:12Z` | `SL-1` | `-` | `lg_d2_envelope_enter` | {} | <none> |
| 5 | `2026-06-07T03:14:12Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 6 | `2026-06-07T03:16:13Z` | `SL-1
... <truncated 9019 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|---|
| `default_init_enters_manual_mode` | default-init: first empty cycle should dispatch to Manual and apply manual pump-switch/default-flow obligations. | ✅ | ✅ | ✅ | ✅ | ✅ |
| `initiate_ac_change_setpoint_then_cp_fallback` | default-init: caregiver initiates AC, edits setpoint in Ask_StartAC, then CP_backManual forces shared Manual recovery. | ✅ | ✅ | ✅ | ✅ | ✅ |
| `start_ac_to_normal_high_pressure_control` | explicit-hot-start: pressing StartAC from SetpointEditing enters AutocontrolInit, then normal autocontrol uses high BP t...<truncated 26 chars> | ❌ | ✅ | ✅ | ✅ | ✅ |
| `normal_autocontrol_low_pressure_then_terminate` | explicit-hot-start: with no fault event NormalAutocontrol stays active and lower BP produces higher flow, then Terminate...<truncated 21 chars> | ⚪ | ⚪ | ⚪ | ⚪ | ✅ |
| `pump_fault_alarm_then_fault_removed_manual` | explicit-hot-start: pump fault during NormalAutocontrol activates alarms/releases control, then FaultRemoved returns to ...<truncated 26 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `cb_backmanual_forces_manual_from_pump_fault` | explicit-hot-start: CB_backManual is a cross-component fallback to Manual, but an active uncleared pump fault should not...<truncated 38 chars> | ✅ | ✅ | ❌ | ❌ | ✅ |
| `cc_backmanual_forces_manual_from_autocontrol_init` | explicit-hot-start: CC_backManual should force AutocontrolInit to Manual rather than continuing toward NormalAutocontrol...<truncated 1 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `manual_initiate_ac_wrong_target_probe` | explicit-hot-start: InitiateAC from Manual must enter Ask_StartAC.SetpointEditing, catching wrong-target mutations of th...<truncated 24 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `normal_autocontrol_low_pressure_higher_flow_no_fire` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `terminate_ac_returns_to_manual` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `ca_backmanual_forces_manual_from_setpoint_editing` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `autocontrol_init_wrong_target_probe` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `fault_removed_wrong_target_probe` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `cp_backmanual_forces_manual_from_normal_autocontrol` |  | ⚪ | ⚪ | ✅ | ✅ | ✅ |
| `cb_backmanual_forces_manual_from_setpoint_editing` |  | ⚪ | ⚪ | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-6` | start_ac_to_normal_high_pressure_control | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=False, drift=major, rework=Keep the intended behavioral repair, but rewrite the StartAC transition with valid DSL scoping. Do not leave `SetpointEditing -> AutocontrolInit : StartAC;` inside `state Ask_...<truncated 523 chars> | `sha256:a46b4d58c6ffd22203d6ed11462c086ca21576d26457b9edc3edda21fd3601b5` |
| 2 | `0` | ❌ | `SD-6` | start_ac_to_normal_high_pressure_control | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=False, drift=major, rework=Keep the intended behavioral repair, but replace the parse-invalid line `Ask_StartAC.SetpointEditing -> AutocontrolInit : /Mode_Control_Algorithm.Ask_StartAC.StartAC;`. The lo...<truncated 556 chars> | `sha256:bceb828a382a28ab702e9cfcc4529aec920eb9078d90fb26b856cb7702f2c9d4` |
| 3 | `0` | ✅ | `SD-6` | start_ac_to_normal_high_pressure_control | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift | `sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20` |
| 4 | `1` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=minor, local_stage=SD-10, reason=scenario_regression | `sha256:1fa9f2728307c12bbbd8bf5368b4d28ee0fd840319b42c295410a75c4904ad3d` |
| 5 | `2` | ✅ | `SD-6` | cb_backmanual_forces_manual_from_pump_fault | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20` |
| 6 | `3` | ✅ | `SD-6` | cb_backmanual_forces_manual_from_pump_fault | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:e0d83a90e0bc0b26d3205dd82c250301d3787ea358564f23754fe4929a3ce867` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98/report.md` §7。

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
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cmd_LNG_cutin = 0;
def int cmd_LNG_cutout = 0;
def int cmd_DG1_cutin = 0;
def int cmd_DG1_cutout = 0;
def int cmd_DG2_cutin = 0;
def int cmd_DG2_cutout = 0;
def int cmd_load_cutin = 1;
def int cmd_load_cutout = 0;
def int illegal_state = 0;

state LNGShipEMS {
    ! * -> ZeroLoad_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoad_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> ZeroLoad_NoRES : if [PL == 0 && Ppv + Pw == 0];
    ! * -> RES_Covers_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RES_Covers_Spare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> Battery_Assist : if [PL > Ppv + Pw && SoC >= 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNG_Covers_Normal : if [PL > Ppv + Pw && SoC >= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= eng3_Pmax];
    ! * -> LNG_Covers_LowSoC_ChargeMargin : if [PL > Ppv + Pw && SoC < 0.2 && PL - Ppv - Pw + Pgmax / 5 <= eng3_Pmax];
    ! * -> DG1_Covers_Normal : if [PL > Ppv + Pw && SoC >= 0.2 && PL - Ppv - Pw > eng3_Pmax && PL - Ppv - Pw <= eng3_Pmax + Pd1max];
    ! * -> DG1_LowSoC_ChargeMargin : if [PL > Ppv + Pw && SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= eng3_Pmax + Pd1max];
    ! * -> DG2_Covers_Normal : if [PL > Ppv + Pw && SoC >= 0.2 && PL - Ppv - Pw > eng3_Pmax + Pd1max && PL - Ppv - Pw <= eng3_Pmax + Pd1max + Pd2max];
    ! * -> Extreme_Overload_Illegal : if [PL > Ppv + Pw && PL - Ppv - Pw > eng3_Pmax + Pd1max + Pd2max];

    [*] -> ZeroLoad_NoRES;

    state ZeroLoad_Charge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_state = 0;
        }
    }

    state ZeroLoad_Spare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_state = 0;
        }
    }

    state ZeroLoad_NoRES {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_state = 0;
        }
    }

    state RES_Covers_Charge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_state = 0;
        }
    }

    state RES_Covers_Spare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_state = 0;
        }
    }

    state Battery_Assist {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cutin = 0;
            cmd_LNG_cutout = 1;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_state = 0;
        }
    }

    state LNG_Covers_Normal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = eng3_Pmax - PL + Ppv + Pw;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_state = 0;
        }
    }

    state LNG_Covers_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5;
            Pspare = eng3_Pmax - PL + Ppv + Pw - Pgmax / 5;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 0;
            cmd_DG1_cutout = 1;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_state = 0;
        }
    }

    state DG1_Covers_Normal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = eng3_Pmax + Pd1max - PL + Ppv + Pw;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 1;
            cmd_DG1_cutout = 0;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_state = 0;
        }
    }

    state DG1_LowSoC_ChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10;
            Pspare = eng3_Pmax + Pd1max - PL + Ppv + Pw - Pd1max / 10;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 1;
            cmd_DG1_cutout = 0;
            cmd_DG2_cutin = 0;
            cmd_DG2_cutout = 1;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_state = 0;
        }
    }

    state DG2_Covers_Normal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = eng3_Pmax + Pd1max + Pd2max - PL + Ppv + Pw;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 1;
            cmd_DG1_cutout = 0;
            cmd_DG2_cutin = 1;
            cmd_DG2_cutout = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
            illegal_state = 0;
        }
    }

    state Extreme_Overload_Illegal {
        enter {
            Pgen_req = eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = PL - Ppv - Pw - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cmd_LNG_cutin = 1;
            cmd_LNG_cutout = 0;
            cmd_DG1_cutin = 1;
            cmd_DG1_cutout = 0;
            cmd_DG2_cutin = 1;
            cmd_DG2_cutout = 0;
            cmd_load_cutin = 1;
            cmd_load_cutout = 0;
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
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `2` / `1` / `1` / `5` |
| token / elapsed | `{'prompt_tokens': 187636, 'completion_tokens': 32942, 'total_tokens': 220578, 'estimated_prompt_tokens': 170200, 'estimated_completion_tokens': 22264, 'estimated_total_tokens': 192464, 'prompt_chars': 680787, 'completion_chars': 89050, 'n_calls': 8, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}` / `635.253s` |
| full stage table | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949/report.md` §4 |
| run record | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949/pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz` |
| logs | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949/run_logs/stdout.txt`, `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949/run_logs/stderr.txt` |
| checks / repro | `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949/checks.json`, `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949/reproducibility.json` |

#### LangGraph runtime metadata 摘要（report §1.1 摘录）

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.2.4` |
| `langgraph_checkpoint_version` | `4.1.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:e2d3a29a62fae25fb7e3acbb4b25404d4ee923a75d80581a16d49df56586d548` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `41` |
| `langgraph_node_trace_hash` | `sha256:a2a4c687ed9ce4825494cbd25db6f4343eeeb5a442f4dd63327f6510190f4f39` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `41` |

- checkpoint 口径：This smoke validates LangGraph interrupt/resume API shape and append-only ledger behavior on a minimal FixLog-like state only. It is not evidence that an interrupted real agent-loop run can be resumed for main-result statistics.
- 注意：`real_agent_loop_resume_supported=false` 时，只能宣称 LangGraph checkpoint API / toy FixLog-like ledger smoke 通过；不能把它写成真实 agent-loop 中断恢复已用于主结果统计。

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14293 | 生成初始 DSL 与 grounding seeds | initial len=7813 | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=178, info=0; blocking=0, advisory=178, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=98473 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=98473 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=98473 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=1, tokens=26937 | LLM per-request accept/reject + repair | candidate len=7812 | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=1, tokens=28451 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=178, info=0; blocking=0, advisory=178, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=98473 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=1, tokens=52424 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-07T03:33:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-07T03:33:54Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-07T03:33:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-07T03:33:54Z` | `SL-1` | `-` | `lg_d2_envelope_enter` | {} | <none> |
| 5 | `2026-06-07T03:33:54Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 6 | `2026-06-07T03:36:18Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 7 | `2026-06-07T03:36:18Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=7813,hash=sha256:fba649434ded |
| 8 | `2026-06-07T03:36:18Z` | `SL-1` | `-` | `lg_d2_envelope_exit` | {} | <none> |
| 9 | `2026-06-07T03:36:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 10 | `2026-06-07T03:36:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-07T03:36:18Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:fba649434ded245d7b3d911c0d772214a5a1a517adf6d9f92e91309716b61d3a |
| 12 | `2026-06-07T03:36:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-07T03:36:18Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=7813,hash=sha256:fba649434ded, current_hash=sha256:fba649434ded245d7b3d911c0d772214a5a1a517adf6d9f92e91309716b61d3a |
| 14 | `2026-06-07T03:36:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 15 | `2026-06-07T03:36:18Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 16 | `2026-06-07T03:36:19Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-07T03:36:19Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 18 | `2026-06-07T03:36:19Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 19 | `2026-06-07T03:36:19Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-07T03:36:19Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 21 | `2026-06-07T03:36:19Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 22 | `2026-06-07T03:36:19Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-07T03:36:19Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-07T03:36:19Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 25 | `2026-06-07T03:36:19Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 26 | `2026-06-07T03:37:50Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 27 | `2026-06-07T03:37:50Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 28 | `2026-06-07T03:37:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-07T03:37:51Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 30 | `2026-06-07T03:37:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-07T03:37:51Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 32 | `2026-06-07T03:37:51Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 33 | `2026-06-07T03:38:55Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-07T03:38:55Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 35 | `2026-06-07T03:38:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 36 | `2026-06-07T03:38:56Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 37 | `2026-06-07T03:38:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 38 | `2026-06-07T03:38:56Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 39 | `2026-06-07T03:38:56Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 40 | `2026-06-07T03:40:34Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 41 | `2026-06-07T03:40:34Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 42 | `2026-06-07T03:40:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-07T03:40:35Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 44 | `2026-06-07T03:40:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-07T03:40:35Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 46 | `2026-06-07T03:40:35Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 47 | `2026-06-07T03:40:35Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-07T03:40:35Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 49 | `2026-06-07T03:40:37Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 50 | `2026-06-07T03:40:37Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 51 | `2026-06-07T03:40:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 52 | `2026-06-07T03:40:37Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 15, "n_scenarios_passed": 14, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 53 | `2026-06-07T03:40:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 54 | `2026-06-07T03:40:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 55 | `2026-06-07T03:40:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 56 | `2026-06-07T03:40:37Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 15, "n_scenarios_passed": 14, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=7813,hash=sha256:fba649434ded |
| 57 | `2026-06-07T03:40:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 58 | `2026-06-07T03:40:37Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 59 | `2026-06-07T03:40:37Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 60 | `2026-06-07T03:40:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 61 | `2026-06-07T03:40:37Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=7813,hash=sha256:fba649434ded |
| 62 | `2026-06-07T03:40:37Z` | `SL-9` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 63 | `2026-06-07T03:41:45Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 64 | `2026-06-07T03:41:45Z` | `SL-9` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 65 | `2026-06-07T03:41:45Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-d7e4f2e8d5"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=7812,hash=sha256:6db200044827 |
| 66 | `2026-06-07T03:41:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 67 | `2026-06-07T03:41:46Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 68 | `2026-06-07T03:41:46Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:6db2000448279754de047248a70856cf083bd022c31259b074b67ef79dac16fe |
| 69 | `2026-06-07T03:41:46Z` | `SL-10` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 70 | `2026-06-07T03:42:10Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 71 | `2026-06-07T03:42:10Z` | `SL-10` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 72 | `2026-06-07T03:42:10Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 73 | `2026-06-07T03:42:10Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 74 | `2026-06-07T03:42:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 75 | `2026-06-07T03:42:10Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=7812,hash=sha256:6db200044827 |
| 76 | `2026-06-07T03:42:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 77 | `2026-06-07T03:42:10Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:6db2000448279754de047248a70856cf083bd022c31259b074b67ef79dac16fe |
| 78 | `2026-06-07T03:42:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 79 | `2026-06-07T03:42:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 80 | `2026-06-07T03:42:10Z` | `<cont
... <truncated 120 chars in PR comment; see report.md>

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 |
|---|---|---|---|
| `default_init_zero_load_no_res_classification` | default-init probe with default PL=0 and no RES: EMS should classify zero-load/no-renewable operation with no charge, sp...<truncated 21 chars> | ❌ | ✅ |
| `zero_load_res_charges_battery` | explicit-hot-start probe: with PL=0, positive RES, and SoC below 0.95, renewable production should be sent to battery ch...<truncated 7 chars> | ✅ | ✅ |
| `zero_load_full_soc_res_to_spare` | explicit-hot-start boundary probe: with PL=0, positive RES, and SoC exactly 0.95, renewable production should become spa...<truncated 29 chars> | ✅ | ✅ |
| `res_covers_load_charges_battery_below_full` | explicit-hot-start probe: when RES covers positive load and SoC is below 0.95, load is served by RES and surplus charges...<truncated 13 chars> | ✅ | ✅ |
| `res_covers_load_spare_at_full_soc` | explicit-hot-start boundary probe: when RES covers positive load and SoC is exactly 0.95, surplus RES should be spare ra...<truncated 19 chars> | ✅ | ✅ |
| `battery_assist_at_soc_and_pgmax_boundary` | explicit-hot-start boundary probe: when RES is below load, SoC is exactly suitable at 0.2, and deficit equals Pgmax, bat...<truncated 32 chars> | ✅ | ✅ |
| `lng_covers_normal_after_battery_limit` | explicit-hot-start probe: with suitable SoC but deficit greater than battery limit and within LNG capacity, LNG should c...<truncated 26 chars> | ✅ | ✅ |
| `lng_low_soc_charge_margin` | explicit-hot-start low-SoC probe: when LNG can cover deficit plus Pgmax/5 charging margin, EMS should request LNG power ...<truncated 34 chars> | ✅ | ✅ |
| `dg1_covers_normal_after_lng_limit` | explicit-hot-start probe: when suitable-SoC deficit exceeds LNG capacity but is within LNG plus DG1 capacity, DG1 should...<truncated 34 chars> | ✅ | ✅ |
| `dg1_low_soc_charge_margin` | explicit-hot-start low-SoC probe: when diesel stage is needed and Pd1max/10 margin fits within LNG plus DG1 capacity, EM...<truncated 29 chars> | ✅ | ✅ |
| `dg2_covers_normal_after_dg1_limit` | explicit-hot-start probe: when suitable-SoC deficit exceeds LNG plus DG1 but is within DG2 addition, DG2 should cut in a...<truncated 29 chars> | ✅ | ✅ |
| `extreme_overload_activates_all_thermal_and_battery` | explicit-hot-start illegal-overload probe: when demand exceeds all RES and thermal resources, all thermal units should b...<truncated 57 chars> | ✅ | ✅ |
| `forced_reclassification_illegal_to_zero_load_spare` | explicit-hot-start forced-transition probe: from the illegal overload leaf, changing inputs to PL=0 with positive RES an...<truncated 116 chars> | ✅ | ✅ |
| `forced_reclassification_res_charge_to_battery_assist` | explicit-hot-start forced-transition probe: from a RES-covering leaf, changed inputs with RES below load, suitable SoC, ...<truncated 146 chars> | ✅ | ✅ |
| `forced_reclassification_dg2_to_res_covers_spare` | explicit-hot-start forced-transition probe: from a DG2 thermal leaf, changed inputs where RES covers load and SoC is at ...<truncated 117 chars> | ✅ | ✅ |
| `forced_reclassification_dg1_to_zero_load_no_res` | explicit-hot-start forced-transition probe added for missing-forced-line detection: from a thermal DG1 leaf, changed inp...<truncated 107 chars> | ⚪ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | default_init_zero_load_no_res_classification | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:6db2000448279754de047248a70856cf083bd022c31259b074b67ef79dac16fe` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_langgraph_upstream_after_g1_retry_20260607_clean/pr-e1-path2_lng_ems-default-upstream-after-g1-clean-59977949/report.md` §7。

</details>
