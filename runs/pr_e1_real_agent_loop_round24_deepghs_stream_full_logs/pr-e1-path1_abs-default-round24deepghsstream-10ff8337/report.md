## path1 / abs-fsm-brake-control / default 真实运行结果：Path1 ABS three-state brake supervisor

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`success`；record_status：`success`；result_status：`converged`。
- main_result_eligible：`true`。
- 一句话结论：`success`；停止原因：full_pass_all_required_feedback_ok。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `abs-fsm-brake-control` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `55507fdfe159d41fb3a5e96faa8423b914900b57` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:ce499624790550d734a59fdd9b6b28f8194710e89c85f739538372d5d8133081` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control`, paper=`project_1_llm_state_machine_modeling/sources/abs-fsm-brake-control/paper.pdf` |
| 样本筛选理由 | 三态、guard、state action 均明确，适合检验 parse/semantic/design/sim 是否能走到后段。 |
| 变量参与说明 | `slp` 是 guard 变量；`k1/k2/n` 是状态动作输出，变量不是纯吉祥物。 |
| run_id | `pr-e1-path1_abs-default-round24deepghsstream-10ff8337` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| final.fcstm 来源 | `{"final_dsl_hash": "sha256:0ff533591cd822e725a61c9195048564db54f5ec98714e77e86d6a4df8c472a9", "source_kind": "initial_or_unrepaired"}` |
| FixLog next_action 序列 | `<none>` |
| iteration exit_reason 序列 | `full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0, 'prompt_chars': 103473, 'completion_chars': 20956, 'n_calls': 3}`, elapsed=`126.162s` |
| run record | [`pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
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

state ABSHydraulicRegulator {
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
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=0 | 生成初始 DSL 与 grounding seeds | initial len=623 | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=0 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=0 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-round24deepghsstream-10ff8337.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T02:44:10Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 2 | `2026-06-04T02:44:10Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 3 | `2026-06-04T02:44:55Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 4 | `2026-06-04T02:44:55Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=623,hash=sha256:0ff533591cd8 |
| 5 | `2026-06-04T02:44:55Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:0ff533591cd822e725a61c9195048564db54f5ec98714e77e86d6a4df8c472a9 |
| 6 | `2026-06-04T02:44:55Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=623,hash=sha256:0ff533591cd8, current_hash=sha256:0ff533591cd822e725a61c9195048564db54f5ec98714e77e86d6a4df8c472a9 |
| 7 | `2026-06-04T02:44:55Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 8 | `2026-06-04T02:44:55Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 9 | `2026-06-04T02:44:55Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 10 | `2026-06-04T02:44:55Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 11 | `2026-06-04T02:44:55Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 12 | `2026-06-04T02:44:55Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T02:44:55Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 14 | `2026-06-04T02:45:36Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T02:45:36Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 16 | `2026-06-04T02:45:36Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 17 | `2026-06-04T02:45:36Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 18 | `2026-06-04T02:45:36Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T02:45:36Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 20 | `2026-06-04T02:46:16Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-04T02:46:16Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T02:46:16Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 23 | `2026-06-04T02:46:16Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 24 | `2026-06-04T02:46:16Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=623,hash=sha256:0ff533591cd8 |
| 25 | `2026-06-04T02:46:16Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=623,hash=sha256:0ff533591cd8 |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_enters_increase` | default-init verifies the initial transition enters increase and applies the increase valve and pump outputs | ✅ |
| `increase_to_hold_at_positive_boundary` | explicit-hot-start probes increase -> hold exactly at slp=0.01 and checks hold neutralizes both valves | ✅ |
| `increase_stays_above_positive_boundary` | explicit-hot-start no-fire probe verifies increase does not transition to hold when slp is just above 0.01 | ✅ |
| `hold_to_increase_above_positive_boundary` | explicit-hot-start probes hold -> increase when slp is greater than 0.01 and checks increase output commands | ✅ |
| `hold_stays_at_positive_boundary` | explicit-hot-start boundary no-fire probe verifies hold does not transition to increase at slp=0.01 | ✅ |
| `hold_to_decrease_below_negative_boundary` | explicit-hot-start probes hold -> decrease when slp is less than -0.01 and checks pressure-release outputs | ✅ |
| `hold_stays_at_negative_boundary` | explicit-hot-start boundary no-fire probe verifies hold does not transition to decrease at slp=-0.01 | ✅ |
| `decrease_to_hold_at_negative_boundary` | explicit-hot-start probes decrease -> hold exactly at slp=-0.01 and checks hold neutralizes pressure-release outputs | ✅ |
| `decrease_stays_below_negative_boundary` | explicit-hot-start no-fire probe verifies decrease does not transition to hold when slp is just below -0.01 | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_enters_increase` — default-init verifies the initial transition enters increase and applies the increase valve and pump outputs</summary>

| Field | Value |
|---|---|
| description | default-init verifies the initial transition enters increase and applies the increase valve and pump outputs |
| initial_state | `<default-init>` |
| initial_vars | `{}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_increase` | `0` | `[]` | `ABSHydraulicRegulator.increase` | `{"k1": 1, "k2": 0, "n": 0}` |

</details>

<details><summary>`increase_to_hold_at_positive_boundary` — explicit-hot-start probes increase -> hold exactly at slp=0.01 and checks hold neutralizes both valves</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes increase -> hold exactly at slp=0.01 and checks hold neutralizes both valves |
| initial_state | `ABSHydraulicRegulator.increase` |
| initial_vars | `{"k1": 1, "k2": 0, "n": 0, "slp": 0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `boundary_transitions_to_hold` | `0` | `[]` | `ABSHydraulicRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`increase_stays_above_positive_boundary` — explicit-hot-start no-fire probe verifies increase does not transition to hold when slp is just above 0.01</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start no-fire probe verifies increase does not transition to hold when slp is just above 0.01 |
| initial_state | `ABSHydraulicRegulator.increase` |
| initial_vars | `{"k1": 1, "k2": 0, "n": 0, "slp": 0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_hold_transition_above_boundary` | `0` | `[]` | `ABSHydraulicRegulator.increase` | `{"k1": 1, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_to_increase_above_positive_boundary` — explicit-hot-start probes hold -> increase when slp is greater than 0.01 and checks increase output commands</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes hold -> increase when slp is greater than 0.01 and checks increase output commands |
| initial_state | `ABSHydraulicRegulator.hold` |
| initial_vars | `{"k1": 0, "k2": 0, "n": 0, "slp": 0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `positive_error_transitions_to_increase` | `0` | `[]` | `ABSHydraulicRegulator.increase` | `{"k1": 1, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_stays_at_positive_boundary` — explicit-hot-start boundary no-fire probe verifies hold does not transition to increase at slp=0.01</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start boundary no-fire probe verifies hold does not transition to increase at slp=0.01 |
| initial_state | `ABSHydraulicRegulator.hold` |
| initial_vars | `{"k1": 0, "k2": 0, "n": 0, "slp": 0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_increase_transition_at_boundary` | `0` | `[]` | `ABSHydraulicRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`hold_to_decrease_below_negative_boundary` — explicit-hot-start probes hold -> decrease when slp is less than -0.01 and checks pressure-release outputs</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes hold -> decrease when slp is less than -0.01 and checks pressure-release outputs |
| initial_state | `ABSHydraulicRegulator.hold` |
| initial_vars | `{"k1": 0, "k2": 0, "n": 0, "slp": -0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `negative_error_transitions_to_decrease` | `0` | `[]` | `ABSHydraulicRegulator.decrease` | `{"k1": 0, "k2": 1, "n": 500}` |

</details>

<details><summary>`hold_stays_at_negative_boundary` — explicit-hot-start boundary no-fire probe verifies hold does not transition to decrease at slp=-0.01</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start boundary no-fire probe verifies hold does not transition to decrease at slp=-0.01 |
| initial_state | `ABSHydraulicRegulator.hold` |
| initial_vars | `{"k1": 0, "k2": 0, "n": 0, "slp": -0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_decrease_transition_at_boundary` | `0` | `[]` | `ABSHydraulicRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`decrease_to_hold_at_negative_boundary` — explicit-hot-start probes decrease -> hold exactly at slp=-0.01 and checks hold neutralizes pressure-release outputs</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes decrease -> hold exactly at slp=-0.01 and checks hold neutralizes pressure-release outputs |
| initial_state | `ABSHydraulicRegulator.decrease` |
| initial_vars | `{"k1": 0, "k2": 1, "n": 500, "slp": -0.01}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `boundary_recovers_to_hold` | `0` | `[]` | `ABSHydraulicRegulator.hold` | `{"k1": 0, "k2": 0, "n": 0}` |

</details>

<details><summary>`decrease_stays_below_negative_boundary` — explicit-hot-start no-fire probe verifies decrease does not transition to hold when slp is just below -0.01</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start no-fire probe verifies decrease does not transition to hold when slp is just below -0.01 |
| initial_state | `ABSHydraulicRegulator.decrease` |
| initial_vars | `{"k1": 0, "k2": 1, "n": 500, "slp": -0.0101}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_hold_transition_below_boundary` | `0` | `[]` | `ABSHydraulicRegulator.decrease` | `{"k1": 0, "k2": 1, "n": 500}` |

</details>


### 7. Repair / blocking feedback 明细

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2220, 'completion_chars': 7546, 'completion_tokens': 0, 'elapsed_seconds': 44.84681225499662, 'first_chunk_seconds': 5.093303221001406, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 24733, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1613, 'completion_chars': 5978, 'completion_tokens': 0, 'elapsed_seconds': 41.132566328000394, 'first_chunk_seconds': 12.516240073993686, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39413, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1639, 'completion_chars': 7432, 'completion_tokens': 0, 'elapsed_seconds': 39.703866252995795, 'first_chunk_seconds': 10.100131073006196, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 39327, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
