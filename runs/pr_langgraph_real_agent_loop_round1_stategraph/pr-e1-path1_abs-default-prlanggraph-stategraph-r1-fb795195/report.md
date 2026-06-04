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
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `d6f724e5739a8979f426efed06e33626e6953eed` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:993dd2a89560dc22cd287bbf50c2cbe6faab9e99a63729d53f02e0d42085b247` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control`, paper=`project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/paper.pdf` |
| 样本筛选理由 | 三态、guard、state action 均明确，适合检验 parse/semantic/design/sim 是否能走到后段。 |
| 变量参与说明 | `slp` 是外部/plant 输入型 guard 变量：standalone DSL 中通常只读，scenario 可通过 `initial_vars` 覆盖来测试阈值；`k1/k2/n` 是状态动作输出。 |
| run_id | `pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"final_dsl_hash": "sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726", "source_kind": "initial_or_unrepaired"}` |
| FixLog next_action 序列 | `<none>` |
| iteration exit_reason 序列 | `full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 27170, 'completion_tokens': 5959, 'total_tokens': 33129, 'estimated_prompt_tokens': 26480, 'estimated_completion_tokens': 3970, 'estimated_total_tokens': 30450, 'prompt_chars': 105916, 'completion_chars': 15875, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`117.224s` |
| run record | [`pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`flow_log.json`](./flow_log.json), [`fix_log.json`](./fix_log.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

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

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9116 | 生成初始 DSL 与 grounding seeds | initial len=634 | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=11912 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=12101 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-prlanggraph-stategraph-r1-fb795195.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T14:51:22Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T14:51:22Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T14:52:14Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T14:52:14Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 7 | `2026-06-04T14:52:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-04T14:52:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-04T14:52:14Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726 |
| 10 | `2026-06-04T14:52:14Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=634,hash=sha256:5a3dc31a6a97, current_hash=sha256:5a3dc31a6a9720ad0701d515d530f63a006e9ee655c5d5284ff63f179cdf6726 |
| 11 | `2026-06-04T14:52:14Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 12 | `2026-06-04T14:52:14Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T14:52:14Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 14 | `2026-06-04T14:52:14Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T14:52:14Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 16 | `2026-06-04T14:52:14Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-04T14:52:14Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 18 | `2026-06-04T14:52:46Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T14:52:47Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-04T14:52:47Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 21 | `2026-06-04T14:52:47Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 22 | `2026-06-04T14:52:47Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-04T14:52:47Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 24 | `2026-06-04T14:53:19Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T14:53:19Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-04T14:53:19Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 27 | `2026-06-04T14:53:19Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 28 | `2026-06-04T14:53:19Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-04T14:53:19Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 30 | `2026-06-04T14:53:19Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-04T14:53:19Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=634,hash=sha256:5a3dc31a6a97 |
| 32 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_enters_increase` | default-init probe: first empty cycle dispatches the initial transition to increase and asserts inlet-valve command outp...<truncated 4 chars> | ✅ |
| `increase_to_hold_at_upper_boundary` | explicit-hot-start probe: increase must transition to hold exactly at slp=0.01 and neutralize both valves. | ✅ |
| `increase_no_hold_above_upper_boundary` | explicit-hot-start no-fire probe: increase must stay increase when slp is just above 0.01. | ✅ |
| `hold_to_increase_above_upper_boundary` | explicit-hot-start probe: hold must transition to increase only when slp is greater than 0.01 and set increase outputs. | ✅ |
| `hold_no_increase_at_upper_boundary` | explicit-hot-start no-fire boundary probe: hold must not transition to increase at slp=0.01 because that guard is strict...<truncated 14 chars> | ✅ |
| `hold_to_decrease_below_lower_boundary` | explicit-hot-start probe: hold must transition to decrease when slp is below -0.01 and command pressure release. | ✅ |
| `hold_no_decrease_at_lower_boundary` | explicit-hot-start no-fire boundary probe: hold must not transition to decrease at slp=-0.01 because that guard is stric...<truncated 12 chars> | ✅ |
| `decrease_to_hold_at_lower_boundary` | explicit-hot-start probe: decrease must transition back to hold exactly at slp=-0.01 and neutralize valves and pump. | ✅ |
| `decrease_no_hold_below_lower_boundary` | explicit-hot-start no-fire probe: decrease must stay decrease when slp remains below -0.01. | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_enters_increase` — default-init probe: first empty cycle dispatches the initial transition to increase and asserts inlet-valve command outputs.</summary>

| Field | Value |
|---|---|
| description | default-init probe: first empty cycle dispatches the initial transition to increase and asserts inlet-valve command outputs. |
| initial_state | `<default-init>` |
| initial_vars | `{}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_transition_to_increase` | `0` | `[]` | `SingleWheelABSHydraulicRegulator.increase` | `{"k1": 1, "k2": 0, "n": 0}` |

</details>

<details><summary>`increase_to_hold_at_upper_boundary` — explicit-hot-start probe: increase must transition to hold exactly at slp=0.01 and neutralize both valves.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: increase must transition to hold exactly at slp=0.01 and neutralize both valves. |
| initial_state | `SingleWheelABSHydraulicRegulator.increase` |
| initial_vars | `{"k1": 1, "k2": 0, "n": 0, "slp": 0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `upper_boundary_fires_to_hold` | `0` | `[]` | `SingleWheelABSHydraulicRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`increase_no_hold_above_upper_boundary` — explicit-hot-start no-fire probe: increase must stay increase when slp is just above 0.01.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start no-fire probe: increase must stay increase when slp is just above 0.01. |
| initial_state | `SingleWheelABSHydraulicRegulator.increase` |
| initial_vars | `{"k1": 1, "k2": 0, "n": 0, "slp": 0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `above_upper_boundary_stays_increase` | `0` | `[]` | `SingleWheelABSHydraulicRegulator.increase` | `{"k1": 1, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_to_increase_above_upper_boundary` — explicit-hot-start probe: hold must transition to increase only when slp is greater than 0.01 and set increase outputs.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: hold must transition to increase only when slp is greater than 0.01 and set increase outputs. |
| initial_state | `SingleWheelABSHydraulicRegulator.hold` |
| initial_vars | `{"k1": 0, "k2": 0, "n": 0, "slp": 0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `positive_slip_error_fires_to_increase` | `0` | `[]` | `SingleWheelABSHydraulicRegulator.increase` | `{"k1": 1, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_no_increase_at_upper_boundary` — explicit-hot-start no-fire boundary probe: hold must not transition to increase at slp=0.01 because that guard is strict greater-than.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start no-fire boundary probe: hold must not transition to increase at slp=0.01 because that guard is strict greater-than. |
| initial_state | `SingleWheelABSHydraulicRegulator.hold` |
| initial_vars | `{"k1": 0, "k2": 0, "n": 0, "slp": 0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `upper_boundary_stays_hold` | `0` | `[]` | `SingleWheelABSHydraulicRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_to_decrease_below_lower_boundary` — explicit-hot-start probe: hold must transition to decrease when slp is below -0.01 and command pressure release.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: hold must transition to decrease when slp is below -0.01 and command pressure release. |
| initial_state | `SingleWheelABSHydraulicRegulator.hold` |
| initial_vars | `{"k1": 0, "k2": 0, "n": 0, "slp": -0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `negative_slip_error_fires_to_decrease` | `0` | `[]` | `SingleWheelABSHydraulicRegulator.decrease` | `{"k1": 0, "k2": 1, "n": 500}` |

</details>

<details><summary>`hold_no_decrease_at_lower_boundary` — explicit-hot-start no-fire boundary probe: hold must not transition to decrease at slp=-0.01 because that guard is strict less-than.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start no-fire boundary probe: hold must not transition to decrease at slp=-0.01 because that guard is strict less-than. |
| initial_state | `SingleWheelABSHydraulicRegulator.hold` |
| initial_vars | `{"k1": 0, "k2": 0, "n": 0, "slp": -0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lower_boundary_stays_hold` | `0` | `[]` | `SingleWheelABSHydraulicRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`decrease_to_hold_at_lower_boundary` — explicit-hot-start probe: decrease must transition back to hold exactly at slp=-0.01 and neutralize valves and pump.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: decrease must transition back to hold exactly at slp=-0.01 and neutralize valves and pump. |
| initial_state | `SingleWheelABSHydraulicRegulator.decrease` |
| initial_vars | `{"k1": 0, "k2": 1, "n": 500, "slp": -0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `lower_boundary_fires_to_hold` | `0` | `[]` | `SingleWheelABSHydraulicRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`decrease_no_hold_below_lower_boundary` — explicit-hot-start no-fire probe: decrease must stay decrease when slp remains below -0.01.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start no-fire probe: decrease must stay decrease when slp remains below -0.01. |
| initial_state | `SingleWheelABSHydraulicRegulator.decrease` |
| initial_vars | `{"k1": 0, "k2": 1, "n": 500, "slp": -0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `below_lower_boundary_stays_decrease` | `0` | `[]` | `SingleWheelABSHydraulicRegulator.decrease` | `{"k1": 0, "k2": 1, "n": 500}` |

</details>


### 7. Repair / blocking feedback 明细

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2155, 'completion_chars': 7176, 'completion_tokens': 2723, 'elapsed_seconds': 51.60875358400517, 'estimated_completion_tokens': 1794, 'estimated_prompt_tokens': 6493, 'estimated_total_tokens': 8287, 'first_chunk_seconds': 13.164385498996126, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25972, 'prompt_tokens': 6393, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 9116}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1144, 'completion_chars': 4142, 'completion_tokens': 1663, 'elapsed_seconds': 32.24296004200005, 'estimated_completion_tokens': 1036, 'estimated_prompt_tokens': 10041, 'estimated_total_tokens': 11077, 'first_chunk_seconds': 11.768933896004455, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 40163, 'prompt_tokens': 10249, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 11912}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1054, 'completion_chars': 4557, 'completion_tokens': 1573, 'elapsed_seconds': 32.29304820399557, 'estimated_completion_tokens': 1140, 'estimated_prompt_tokens': 9946, 'estimated_total_tokens': 11086, 'first_chunk_seconds': 11.940170136003871, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39781, 'prompt_tokens': 10528, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12101}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
