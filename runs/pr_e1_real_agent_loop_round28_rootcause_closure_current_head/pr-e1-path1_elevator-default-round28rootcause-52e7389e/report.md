## path1 / automatic-elevator-controller / default 真实运行结果：Path1 automatic elevator controller

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
| case_id | `automatic-elevator-controller` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `132721b4da597071d7874597e3293f003cd8f890` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:993dd2a89560dc22cd287bbf50c2cbe6faab9e99a63729d53f02e0d42085b247` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/automatic-elevator-controller`, paper=`project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/paper.pdf` |
| 样本筛选理由 | 楼层态、运动态、请求事件、到位传感事件与 reset 都明确，适合检验事件建模和 forced fallback。 |
| 变量参与说明 | `PS*`/`S*`/`reset` 更适合按事件建模；`hbrg` 是纯输出动作，用于表达上行/下行/停止，不反向影响控制流。 |
| run_id | `pr-e1-path1_elevator-default-round28rootcause-52e7389e` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| final.fcstm 来源 | `{"final_dsl_hash": "sha256:a0b11c24e58704e6a2e93a84991bf1241e7524ee107639a6504576e458270c99", "source_kind": "initial_or_unrepaired"}` |
| FixLog next_action 序列 | `<none>` |
| iteration exit_reason 序列 | `full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 26987, 'completion_tokens': 8055, 'total_tokens': 35042, 'estimated_prompt_tokens': 26285, 'estimated_completion_tokens': 5900, 'estimated_total_tokens': 32185, 'prompt_chars': 105132, 'completion_chars': 23593, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`153.05s` |
| run record | [`pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`flow_log.json`](./flow_log.json), [`fix_log.json`](./fix_log.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

### 2. 输入 NL（多行原文）

```text
The automatic elevator controller is built as a finite-state machine whose state space combines floor states `F1`, `F2`, and `F3` with motion states `MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel.

In the normal workflow, the system starts from an ideal state on floor 1, chooses either the up or down branch according to floor requests, stops at the requested floor, and then immediately checks the next destination before deciding whether to continue moving.

The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as sensing inputs for arrival. From `F1`, `PS2` triggers `MU2` and `PS3` triggers `MU3`. From `F2`, `PS3` triggers `MU3` and `PS1` triggers `MD1`. From `F3`, `PS1` triggers `MD1` and `PS2` triggers `MD2`. Arrival sensors complete motion transitions: `MU2 + S2 -> F2`, `MU3 + S3 -> F3`, `MD1 + S1 -> F1`, and `MD2 + S2 -> F2`.

The `hbrg` output distinguishes upward drive, downward drive, and stop conditions. A reset signal forces the controller back to floor 1 regardless of the outstanding request context.
```

### 2.1 输入 NL 中文翻译

```text
自动电梯控制器被构建为有限状态机，其状态空间由楼层状态 `F1`、`F2`、`F3` 与上/下行运动状态 `MU2`、`MU3`、`MD1`、`MD2` 组合而成。

正常流程中，系统从 1 楼理想状态开始，根据楼层请求选择上行或下行分支，在请求楼层停止，然后立即检查下一目的地以决定是否继续移动。

控制器使用 `PS1/PS2/PS3` 作为楼层请求输入，使用 `S1/S2/S3` 作为到位传感输入。从 `F1`，`PS2` 触发 `MU2`，`PS3` 触发 `MU3`；从 `F2`，`PS3` 触发 `MU3`，`PS1` 触发 `MD1`；从 `F3`，`PS1` 触发 `MD1`，`PS2` 触发 `MD2`。到位传感器完成运动转移：`MU2 + S2 -> F2`，`MU3 + S3 -> F3`，`MD1 + S1 -> F1`，`MD2 + S2 -> F2`。

`hbrg` 输出区分上行驱动、下行驱动和停止状态。复位信号会无视当前请求上下文，强制控制器回到 1 楼。
```

### 3. 最终产出的 FCSTM DSL

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

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=10522 | 生成初始 DSL 与 grounding seeds | initial len=659 | [`record`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=14284 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10236 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round28rootcause-52e7389e.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T06:58:43Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 2 | `2026-06-04T06:58:43Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 3 | `2026-06-04T06:59:59Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 4 | `2026-06-04T06:59:59Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=659,hash=sha256:a0b11c24e587 |
| 5 | `2026-06-04T06:59:59Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:a0b11c24e58704e6a2e93a84991bf1241e7524ee107639a6504576e458270c99 |
| 6 | `2026-06-04T06:59:59Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=659,hash=sha256:a0b11c24e587, current_hash=sha256:a0b11c24e58704e6a2e93a84991bf1241e7524ee107639a6504576e458270c99 |
| 7 | `2026-06-04T06:59:59Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 8 | `2026-06-04T06:59:59Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 9 | `2026-06-04T06:59:59Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 10 | `2026-06-04T06:59:59Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 11 | `2026-06-04T06:59:59Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 12 | `2026-06-04T06:59:59Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T06:59:59Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 14 | `2026-06-04T07:00:51Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T07:00:51Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 16 | `2026-06-04T07:00:51Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 17 | `2026-06-04T07:00:51Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 18 | `2026-06-04T07:00:51Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T07:00:51Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 20 | `2026-06-04T07:01:16Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-04T07:01:16Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T07:01:16Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 23 | `2026-06-04T07:01:16Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 24 | `2026-06-04T07:01:16Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=659,hash=sha256:a0b11c24e587 |
| 25 | `2026-06-04T07:01:16Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=659,hash=sha256:a0b11c24e587 |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_up_to_f2_then_f3` | default-init: dispatches to floor 1 stopped, then PS2 drives upward to MU2, S2 stops at F2, PS3 immediately drives upwar...<truncated 29 chars> | ✅ |
| `f1_request_f3_direct_up_path` | explicit-hot-start: from F1, PS3 must target MU3 exactly and S3 must complete arrival at F3 with stop output. | ✅ |
| `f2_request_f1_down_path` | explicit-hot-start: from F2, PS1 must target MD1 exactly with downward drive, and S1 must complete arrival at F1 stopped...<truncated 1 chars> | ✅ |
| `f3_request_f2_down_path` | explicit-hot-start: from F3, PS2 must target MD2 exactly with downward drive, and S2 must complete arrival at F2 stopped...<truncated 1 chars> | ✅ |
| `f3_request_f1_down_path` | explicit-hot-start: from F3, PS1 must target MD1 exactly with downward drive, and S1 must complete arrival at F1 stopped...<truncated 1 chars> | ✅ |
| `reset_forces_f1_from_up_motion` | explicit-hot-start: reset from an upward travel state must force F1 regardless of motion/request context and set stop ou...<truncated 5 chars> | ✅ |
| `reset_forces_f1_from_down_motion` | explicit-hot-start: reset from a downward travel state must force F1 regardless of motion/request context and set stop o...<truncated 6 chars> | ✅ |
| `wrong_arrival_sensor_does_not_complete_motion` | explicit-hot-start: while moving upward to F2, an unrelated S1 arrival sensor must not complete the MU2 motion transitio...<truncated 2 chars> | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_f1_up_to_f2_then_f3` — default-init: dispatches to floor 1 stopped, then PS2 drives upward to MU2, S2 stops at F2, PS3 immediately drives upward to MU3, and S3 stops at F3.</summary>

| Field | Value |
|---|---|
| description | default-init: dispatches to floor 1 stopped, then PS2 drives upward to MU2, S2 stops at F2, PS3 immediately drives upward to MU3, and S3 stops at F3. |
| initial_state | `<default-init>` |
| initial_vars | `{}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_f1_stopped` | `0` | `[]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |
| 1 `ps2_from_f1_starts_up_to_f2` | `0` | `["AutomaticElevatorController.PS2"]` | `AutomaticElevatorController.MU2` | `{"hbrg": 1}` |
| 2 `s2_arrival_stops_at_f2` | `0` | `["AutomaticElevatorController.S2"]` | `AutomaticElevatorController.F2` | `{"hbrg": 0}` |
| 3 `ps3_from_f2_starts_up_to_f3` | `0` | `["AutomaticElevatorController.PS3"]` | `AutomaticElevatorController.MU3` | `{"hbrg": 1}` |
| 4 `s3_arrival_stops_at_f3` | `0` | `["AutomaticElevatorController.S3"]` | `AutomaticElevatorController.F3` | `{"hbrg": 0}` |

</details>

<details><summary>`f1_request_f3_direct_up_path` — explicit-hot-start: from F1, PS3 must target MU3 exactly and S3 must complete arrival at F3 with stop output.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from F1, PS3 must target MU3 exactly and S3 must complete arrival at F3 with stop output. |
| initial_state | `AutomaticElevatorController.F1` |
| initial_vars | `{"hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ps3_from_f1_starts_up_to_f3` | `0` | `["AutomaticElevatorController.PS3"]` | `AutomaticElevatorController.MU3` | `{"hbrg": 1}` |
| 1 `s3_arrival_stops_at_f3` | `0` | `["AutomaticElevatorController.S3"]` | `AutomaticElevatorController.F3` | `{"hbrg": 0}` |

</details>

<details><summary>`f2_request_f1_down_path` — explicit-hot-start: from F2, PS1 must target MD1 exactly with downward drive, and S1 must complete arrival at F1 stopped.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from F2, PS1 must target MD1 exactly with downward drive, and S1 must complete arrival at F1 stopped. |
| initial_state | `AutomaticElevatorController.F2` |
| initial_vars | `{"hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ps1_from_f2_starts_down_to_f1` | `0` | `["AutomaticElevatorController.PS1"]` | `AutomaticElevatorController.MD1` | `{"hbrg": -1}` |
| 1 `s1_arrival_stops_at_f1` | `0` | `["AutomaticElevatorController.S1"]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`f3_request_f2_down_path` — explicit-hot-start: from F3, PS2 must target MD2 exactly with downward drive, and S2 must complete arrival at F2 stopped.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from F3, PS2 must target MD2 exactly with downward drive, and S2 must complete arrival at F2 stopped. |
| initial_state | `AutomaticElevatorController.F3` |
| initial_vars | `{"hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ps2_from_f3_starts_down_to_f2` | `0` | `["AutomaticElevatorController.PS2"]` | `AutomaticElevatorController.MD2` | `{"hbrg": -1}` |
| 1 `s2_arrival_stops_at_f2` | `0` | `["AutomaticElevatorController.S2"]` | `AutomaticElevatorController.F2` | `{"hbrg": 0}` |

</details>

<details><summary>`f3_request_f1_down_path` — explicit-hot-start: from F3, PS1 must target MD1 exactly with downward drive, and S1 must complete arrival at F1 stopped.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from F3, PS1 must target MD1 exactly with downward drive, and S1 must complete arrival at F1 stopped. |
| initial_state | `AutomaticElevatorController.F3` |
| initial_vars | `{"hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ps1_from_f3_starts_down_to_f1` | `0` | `["AutomaticElevatorController.PS1"]` | `AutomaticElevatorController.MD1` | `{"hbrg": -1}` |
| 1 `s1_arrival_stops_at_f1` | `0` | `["AutomaticElevatorController.S1"]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`reset_forces_f1_from_up_motion` — explicit-hot-start: reset from an upward travel state must force F1 regardless of motion/request context and set stop output.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: reset from an upward travel state must force F1 regardless of motion/request context and set stop output. |
| initial_state | `AutomaticElevatorController.MU3` |
| initial_vars | `{"hbrg": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `reset_from_mu3_lands_f1` | `0` | `["AutomaticElevatorController.reset"]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`reset_forces_f1_from_down_motion` — explicit-hot-start: reset from a downward travel state must force F1 regardless of motion/request context and set stop output.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: reset from a downward travel state must force F1 regardless of motion/request context and set stop output. |
| initial_state | `AutomaticElevatorController.MD2` |
| initial_vars | `{"hbrg": -1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `reset_from_md2_lands_f1` | `0` | `["AutomaticElevatorController.reset"]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`wrong_arrival_sensor_does_not_complete_motion` — explicit-hot-start: while moving upward to F2, an unrelated S1 arrival sensor must not complete the MU2 motion transition.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: while moving upward to F2, an unrelated S1 arrival sensor must not complete the MU2 motion transition. |
| initial_state | `AutomaticElevatorController.MU2` |
| initial_vars | `{"hbrg": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `s1_ignored_while_in_mu2` | `0` | `["AutomaticElevatorController.S1"]` | `AutomaticElevatorController.MU2` | `{"hbrg": 1}` |
| 1 `correct_s2_arrival_stops_at_f2` | `0` | `["AutomaticElevatorController.S2"]` | `AutomaticElevatorController.F2` | `{"hbrg": 0}` |

</details>


### 7. Repair / blocking feedback 明细

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3565, 'completion_chars': 12173, 'completion_tokens': 4084, 'elapsed_seconds': 76.59971758098982, 'estimated_completion_tokens': 3044, 'estimated_prompt_tokens': 6523, 'estimated_total_tokens': 9567, 'first_chunk_seconds': 12.71895954098727, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26089, 'prompt_tokens': 6438, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10522}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1966, 'completion_chars': 7829, 'completion_tokens': 2746, 'elapsed_seconds': 51.83316927100532, 'estimated_completion_tokens': 1958, 'estimated_prompt_tokens': 11274, 'estimated_total_tokens': 13232, 'first_chunk_seconds': 16.714560688007623, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 45093, 'prompt_tokens': 11538, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14284}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 826, 'completion_chars': 3591, 'completion_tokens': 1225, 'elapsed_seconds': 24.131629377996433, 'estimated_completion_tokens': 898, 'estimated_prompt_tokens': 8488, 'estimated_total_tokens': 9386, 'first_chunk_seconds': 9.724528842998552, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 33950, 'prompt_tokens': 9011, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 10236}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
