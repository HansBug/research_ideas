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
| Git commit | `55507fdfe159d41fb3a5e96faa8423b914900b57` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:ce499624790550d734a59fdd9b6b28f8194710e89c85f739538372d5d8133081` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/automatic-elevator-controller`, paper=`project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/paper.pdf` |
| 样本筛选理由 | 楼层态、运动态、请求事件、到位传感事件与 reset 都明确，适合检验事件建模和 forced fallback。 |
| 变量参与说明 | `PS*`/`S*`/`reset` 更适合按事件建模；`hbrg` 是输出动作，变量压力低于 Path2 EFSM。 |
| run_id | `pr-e1-path1_elevator-default-round24deepghsstream-019c0d50` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| final.fcstm 来源 | `{"final_dsl_hash": "sha256:76df5e8453da8b87b9619f41f32d9080e688f9a48288584c310613d9dbf5e0d7", "source_kind": "initial_or_unrepaired"}` |
| FixLog next_action 序列 | `<none>` |
| iteration exit_reason 序列 | `full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0, 'prompt_chars': 140322, 'completion_chars': 27060, 'n_calls': 3}`, elapsed=`193.262s` |
| run record | [`pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
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
def int PS1 = 0;
def int PS2 = 0;
def int PS3 = 0;
def int S1 = 0;
def int S2 = 0;
def int S3 = 0;
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

    F1 -> MU2 : if [PS2 > 0];
    F1 -> MU3 : if [PS3 > 0];
    F2 -> MU3 : if [PS3 > 0];
    F2 -> MD1 : if [PS1 > 0];
    F3 -> MD1 : if [PS1 > 0];
    F3 -> MD2 : if [PS2 > 0];
    MU2 -> F2 : if [S2 > 0];
    MU3 -> F3 : if [S3 > 0];
    MD1 -> F1 : if [S1 > 0];
    MD2 -> F2 : if [S2 > 0];
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=0 | 生成初始 DSL 与 grounding seeds | initial len=848 | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=17, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=0 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=0 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round24deepghsstream-019c0d50.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T02:44:10Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 2 | `2026-06-04T02:44:10Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 3 | `2026-06-04T02:45:26Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 4 | `2026-06-04T02:45:26Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=848,hash=sha256:76df5e8453da |
| 5 | `2026-06-04T02:45:26Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:76df5e8453da8b87b9619f41f32d9080e688f9a48288584c310613d9dbf5e0d7 |
| 6 | `2026-06-04T02:45:26Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=848,hash=sha256:76df5e8453da, current_hash=sha256:76df5e8453da8b87b9619f41f32d9080e688f9a48288584c310613d9dbf5e0d7 |
| 7 | `2026-06-04T02:45:26Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 8 | `2026-06-04T02:45:26Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 9 | `2026-06-04T02:45:26Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 10 | `2026-06-04T02:45:26Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 11 | `2026-06-04T02:45:26Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 12 | `2026-06-04T02:45:26Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T02:45:26Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 14 | `2026-06-04T02:46:40Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T02:46:40Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 16 | `2026-06-04T02:46:40Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 17 | `2026-06-04T02:46:40Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 18 | `2026-06-04T02:46:40Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T02:46:40Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 20 | `2026-06-04T02:47:23Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-04T02:47:23Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T02:47:23Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 23 | `2026-06-04T02:47:23Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 24 | `2026-06-04T02:47:23Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=848,hash=sha256:76df5e8453da |
| 25 | `2026-06-04T02:47:23Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=848,hash=sha256:76df5e8453da |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_no_request_stays_stopped` | default-init verifies the initial transition lands on floor F1 with stopped hbrg, and with no requests the controller st...<truncated 18 chars> | ✅ |
| `f1_ps2_moves_up_to_f2` | explicit-hot-start probes F1 request PS2 causing upward MU2 drive, then S2 arrival stopping at requested floor F2. | ✅ |
| `f1_ps3_moves_up_to_f3_then_reset` | explicit-hot-start probes F1 request PS3 causing upward MU3 drive, S3 arrival at F3, and reset forcing back to F1 from a...<truncated 13 chars> | ✅ |
| `f2_ps3_moves_up_to_f3` | explicit-hot-start probes F2 request PS3 causing upward MU3 drive and S3 arrival stopping at F3. | ✅ |
| `f2_ps1_moves_down_to_f1` | explicit-hot-start probes F2 request PS1 causing downward MD1 drive and S1 arrival stopping at F1. | ✅ |
| `f3_ps1_moves_down_to_f1` | explicit-hot-start probes F3 request PS1 causing downward MD1 drive and S1 arrival stopping at F1. | ✅ |
| `f3_ps2_moves_down_to_f2` | explicit-hot-start probes F3 request PS2 causing downward MD2 drive and S2 arrival stopping at F2. | ✅ |
| `reset_forces_f1_from_motion_contexts` | explicit-hot-start probes reset forcing F1 from a downward motion state, then from an upward motion state reached after ...<truncated 51 chars> | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_f1_no_request_stays_stopped` — default-init verifies the initial transition lands on floor F1 with stopped hbrg, and with no requests the controller stays stopped at F1.</summary>

| Field | Value |
|---|---|
| description | default-init verifies the initial transition lands on floor F1 with stopped hbrg, and with no requests the controller stays stopped at F1. |
| initial_state | `<default-init>` |
| initial_vars | `{}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dispatch_to_f1` | `0` | `[]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |
| 1 `no_request_no_motion` | `0` | `[]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`f1_ps2_moves_up_to_f2` — explicit-hot-start probes F1 request PS2 causing upward MU2 drive, then S2 arrival stopping at requested floor F2.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes F1 request PS2 causing upward MU2 drive, then S2 arrival stopping at requested floor F2. |
| initial_state | `AutomaticElevatorController.F1` |
| initial_vars | `{"PS2": 1, "S2": 1, "hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ps2_request_enters_mu2` | `0` | `[]` | `AutomaticElevatorController.MU2` | `{"hbrg": 1}` |
| 1 `s2_arrival_stops_at_f2` | `0` | `[]` | `AutomaticElevatorController.F2` | `{"hbrg": 0}` |

</details>

<details><summary>`f1_ps3_moves_up_to_f3_then_reset` — explicit-hot-start probes F1 request PS3 causing upward MU3 drive, S3 arrival at F3, and reset forcing back to F1 from a floor state.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes F1 request PS3 causing upward MU3 drive, S3 arrival at F3, and reset forcing back to F1 from a floor state. |
| initial_state | `AutomaticElevatorController.F1` |
| initial_vars | `{"PS3": 1, "S3": 1, "hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ps3_request_enters_mu3` | `0` | `[]` | `AutomaticElevatorController.MU3` | `{"hbrg": 1}` |
| 1 `s3_arrival_stops_at_f3` | `0` | `[]` | `AutomaticElevatorController.F3` | `{"hbrg": 0}` |
| 2 `reset_from_f3_forces_f1` | `0` | `["AutomaticElevatorController.reset"]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`f2_ps3_moves_up_to_f3` — explicit-hot-start probes F2 request PS3 causing upward MU3 drive and S3 arrival stopping at F3.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes F2 request PS3 causing upward MU3 drive and S3 arrival stopping at F3. |
| initial_state | `AutomaticElevatorController.F2` |
| initial_vars | `{"PS3": 1, "S3": 1, "hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ps3_request_enters_mu3` | `0` | `[]` | `AutomaticElevatorController.MU3` | `{"hbrg": 1}` |
| 1 `s3_arrival_stops_at_f3` | `0` | `[]` | `AutomaticElevatorController.F3` | `{"hbrg": 0}` |

</details>

<details><summary>`f2_ps1_moves_down_to_f1` — explicit-hot-start probes F2 request PS1 causing downward MD1 drive and S1 arrival stopping at F1.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes F2 request PS1 causing downward MD1 drive and S1 arrival stopping at F1. |
| initial_state | `AutomaticElevatorController.F2` |
| initial_vars | `{"PS1": 1, "S1": 1, "hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ps1_request_enters_md1` | `0` | `[]` | `AutomaticElevatorController.MD1` | `{"hbrg": -1}` |
| 1 `s1_arrival_stops_at_f1` | `0` | `[]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`f3_ps1_moves_down_to_f1` — explicit-hot-start probes F3 request PS1 causing downward MD1 drive and S1 arrival stopping at F1.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes F3 request PS1 causing downward MD1 drive and S1 arrival stopping at F1. |
| initial_state | `AutomaticElevatorController.F3` |
| initial_vars | `{"PS1": 1, "S1": 1, "hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ps1_request_enters_md1` | `0` | `[]` | `AutomaticElevatorController.MD1` | `{"hbrg": -1}` |
| 1 `s1_arrival_stops_at_f1` | `0` | `[]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`f3_ps2_moves_down_to_f2` — explicit-hot-start probes F3 request PS2 causing downward MD2 drive and S2 arrival stopping at F2.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes F3 request PS2 causing downward MD2 drive and S2 arrival stopping at F2. |
| initial_state | `AutomaticElevatorController.F3` |
| initial_vars | `{"PS2": 1, "S2": 1, "hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ps2_request_enters_md2` | `0` | `[]` | `AutomaticElevatorController.MD2` | `{"hbrg": -1}` |
| 1 `s2_arrival_stops_at_f2` | `0` | `[]` | `AutomaticElevatorController.F2` | `{"hbrg": 0}` |

</details>

<details><summary>`reset_forces_f1_from_motion_contexts` — explicit-hot-start probes reset forcing F1 from a downward motion state, then from an upward motion state reached after the outstanding PS3 request context rema...<truncated 11 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes reset forcing F1 from a downward motion state, then from an upward motion state reached after the outstanding PS3 request context remains active. |
| initial_state | `AutomaticElevatorController.MD2` |
| initial_vars | `{"PS3": 1, "hbrg": -1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `reset_from_md2_forces_f1` | `0` | `["AutomaticElevatorController.reset"]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |
| 1 `outstanding_ps3_enters_mu3` | `0` | `[]` | `AutomaticElevatorController.MU3` | `{"hbrg": 1}` |
| 2 `reset_from_mu3_forces_f1` | `0` | `["AutomaticElevatorController.reset"]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>


### 7. Repair / blocking feedback 明细

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3600, 'completion_chars': 12064, 'completion_tokens': 0, 'elapsed_seconds': 75.97855450499628, 'first_chunk_seconds': 11.14856809999037, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 24850, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1930, 'completion_chars': 7447, 'completion_tokens': 0, 'elapsed_seconds': 73.65545767900767, 'first_chunk_seconds': 39.231897574005416, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 50995, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1794, 'completion_chars': 7549, 'completion_tokens': 0, 'elapsed_seconds': 43.09778998000547, 'first_chunk_seconds': 10.4514122170076, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 64477, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
