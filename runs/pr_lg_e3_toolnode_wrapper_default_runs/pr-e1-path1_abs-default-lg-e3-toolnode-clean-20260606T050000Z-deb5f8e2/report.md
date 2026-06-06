## path1 / abs-fsm-brake-control / default 真实运行结果：Path1 ABS three-state brake supervisor

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`success`；record_status：`success`；result_status：`converged`。
- main_result_eligible：`true`。
- Path2 ref-model blueprint eligible：`n/a`；reason：not_applicable_to_path1。
- 一句话结论：`success`；停止原因：full_pass_all_required_feedback_ok。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `abs-fsm-brake-control` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `min_sl10_rework_attempts=1`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `7aa90ff3f2b6d19cc67bee25f19c9b340fe925f4` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control`, paper=`project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/paper.pdf` |
| 样本筛选理由 | 三态、guard、state action 均明确，适合检验 parse/semantic/design/sim 是否能走到后段。 |
| 变量参与说明 | `slp` 是外部/plant 输入型 guard 变量：standalone DSL 中通常只读，scenario 可通过 `initial_vars` 覆盖来测试阈值；`k1/k2/n` 是状态动作输出。 |
| run_id | `pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"final_dsl_hash": "sha256:daf0a2131e360a06d62ea8c0a5ba398ff01b5fc756b01374275405d75c36a70e", "source_kind": "initial_or_unrepaired"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `<none>` |
| iteration exit_reason 序列 | `full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 26722, 'completion_tokens': 7644, 'total_tokens': 34366, 'estimated_prompt_tokens': 26232, 'estimated_completion_tokens': 4893, 'estimated_total_tokens': 31125, 'prompt_chars': 104926, 'completion_chars': 19566, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`144.848s` |
| run record | [`pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz`](./pr-e1-path1_abs-default-lg-e3-toolnode-clean-20260606T050000Z-deb5f8e2.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`flow_log.json`](./flow_log.json), [`fix_log.json`](./fix_log.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

### 1.1 LangGraph runtime metadata / checkpoint 口径

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

### 2. 输入 NL（多行原文）

```text
The paper implements the single-wheel ABS hydraulic regulator as a three-state FSM coupled with a PID-based slip controller. Wheel speed and vehicle speed are used to compute the slip ratio, and the PID output drives the Stateflow supervisor instead of sending commands directly to the hydraulic valves.

The FSM contains the states `increase`, `hold`, and `decrease`, where `increase` sets `k1=1, k2=0, n=0`, `hold` neutralizes both valves with `k1=0, k2=0, n=0`, and `decrease` sets `k1=0, k2=1, n=500` to release pressure.

The transition guards split the slip-error space into four bands: `increase -> hold` when `slp <= 0.01`, `hold -> increase` when `slp > 0.01`, `hold -> decrease` when `slp < -0.01`, and `decrease -> hold` when `slp >= -0.01`.

This gives a concrete discrete supervisor that maps slip-error thresholds to inlet-valve, return-valve, and pump actions while the continuous wheel-slip dynamics remain in the plant model.
```

### 2.1 输入 NL 中文翻译

```text
论文把单轮 ABS 液压调节器实现为一个三状态 FSM，并与基于滑移率的 PID 控制器耦合。轮速与车速用于计算滑移率，PID 输出驱动 Stateflow 监督器，而不是直接发送液压阀命令。

FSM 包含 `increase`、`hold`、`decrease` 三个状态：`increase` 设置 `k1=1, k2=0, n=0`，`hold` 设置 `k1=0, k2=0, n=0`，`decrease` 设置 `k1=0, k2=1, n=500` 以释放压力。

转移 guard 把滑移误差空间分成四个区间：`increase -> hold` 当 `slp <= 0.01`，`hold -> increase` 当 `slp > 0.01`，`hold -> decrease` 当 `slp < -0.01`，`decrease -> hold` 当 `slp >= -0.01`。

这给出了一个具体的离散监督器，把滑移误差阈值映射为进油阀、回油阀与泵动作，而连续轮胎滑移动力学仍留在被控对象模型中。
```

### 3. 最终产出的 FCSTM DSL

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

### 4. 全流程真实摘要表

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

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

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

#### 6.2 Scenario definitions

<details><summary>`default_init_enters_increase_then_low_slip_holds` — default-init probe: first empty cycle dispatches to increase with inlet command, then default slp=0.0 satisfies increase->hold and neutralizes valves.</summary>

| Field | Value |
|---|---|
| description | default-init probe: first empty cycle dispatches to increase with inlet command, then default slp=0.0 satisfies increase->hold and neutralizes valves. |
| initial_state | `<default-init>` |
| initial_vars | `{}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_increase` | `0` | `[]` | `SingleWheelABSRegulator.increase` | `{"k1": 1, "k2": 0, "n": 0}` |
| 1 `low_slip_moves_to_hold` | `0` | `[]` | `SingleWheelABSRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`increase_to_hold_at_positive_boundary` — explicit-hot-start probe: increase must transition to hold exactly at slp=0.01 and set neutral valve and pump commands.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: increase must transition to hold exactly at slp=0.01 and set neutral valve and pump commands. |
| initial_state | `SingleWheelABSRegulator.increase` |
| initial_vars | `{"k1": 1, "k2": 0, "n": 0, "slp": 0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `boundary_slip_enters_hold` | `0` | `[]` | `SingleWheelABSRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`increase_no_fire_above_positive_boundary` — explicit-hot-start no-fire probe: increase must remain increase when slp is just above 0.01.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start no-fire probe: increase must remain increase when slp is just above 0.01. |
| initial_state | `SingleWheelABSRegulator.increase` |
| initial_vars | `{"k1": 1, "k2": 0, "n": 0, "slp": 0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `above_boundary_stays_increase` | `0` | `[]` | `SingleWheelABSRegulator.increase` | `{"k1": 1, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_no_fire_at_positive_boundary` — explicit-hot-start boundary probe: hold must not transition to increase at slp=0.01 because the guard is strictly greater than 0.01.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start boundary probe: hold must not transition to increase at slp=0.01 because the guard is strictly greater than 0.01. |
| initial_state | `SingleWheelABSRegulator.hold` |
| initial_vars | `{"k1": 0, "k2": 0, "n": 0, "slp": 0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `positive_boundary_stays_hold` | `0` | `[]` | `SingleWheelABSRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_to_increase_above_positive_boundary` — explicit-hot-start probe: hold must transition to increase when slp is greater than 0.01 and set inlet valve command k1=1.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: hold must transition to increase when slp is greater than 0.01 and set inlet valve command k1=1. |
| initial_state | `SingleWheelABSRegulator.hold` |
| initial_vars | `{"k1": 0, "k2": 0, "n": 0, "slp": 0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `above_positive_boundary_enters_increase` | `0` | `[]` | `SingleWheelABSRegulator.increase` | `{"k1": 1, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_no_fire_at_negative_boundary` — explicit-hot-start boundary probe: hold must not transition to decrease at slp=-0.01 because the guard is strictly less than -0.01.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start boundary probe: hold must not transition to decrease at slp=-0.01 because the guard is strictly less than -0.01. |
| initial_state | `SingleWheelABSRegulator.hold` |
| initial_vars | `{"k1": 0, "k2": 0, "n": 0, "slp": -0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `negative_boundary_stays_hold` | `0` | `[]` | `SingleWheelABSRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_to_decrease_below_negative_boundary` — explicit-hot-start probe: hold must transition to decrease when slp is below -0.01, command return valve k2=1 and pump n=500, then remain decrease while still b...<truncated 24 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: hold must transition to decrease when slp is below -0.01, command return valve k2=1 and pump n=500, then remain decrease while still below recovery threshold. |
| initial_state | `SingleWheelABSRegulator.hold` |
| initial_vars | `{"k1": 0, "k2": 0, "n": 0, "slp": -0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `below_negative_boundary_enters_decrease` | `0` | `[]` | `SingleWheelABSRegulator.decrease` | `{"k1": 0, "k2": 1, "n": 500}` |
| 1 `still_below_recovery_stays_decrease` | `0` | `[]` | `SingleWheelABSRegulator.decrease` | `{"k1": 0, "k2": 1, "n": 500}` |

</details>

<details><summary>`decrease_to_hold_at_negative_boundary` — explicit-hot-start recovery boundary probe: decrease must transition to hold exactly at slp=-0.01 and neutralize both valves and pump.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start recovery boundary probe: decrease must transition to hold exactly at slp=-0.01 and neutralize both valves and pump. |
| initial_state | `SingleWheelABSRegulator.decrease` |
| initial_vars | `{"k1": 0, "k2": 1, "n": 500, "slp": -0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `negative_boundary_recovers_to_hold` | `0` | `[]` | `SingleWheelABSRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>


### 7. Repair / blocking feedback 明细

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
