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
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `delta_review_mode=blocking_major_only` |
| Git commit | `024d87ea7ccf963350683efa08337a26a85c7b1d` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:0297eca601185761f335df788fe652c9a55156fa8e8100374f7291bbfc86e10b` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/automatic-elevator-controller`, paper=`project_1_llm_state_machine_modeling/sources/automatic-elevator-controller/paper.pdf` |
| 样本筛选理由 | 楼层态、运动态、请求事件、到位传感事件与 reset 都明确，适合检验事件建模和 forced fallback。 |
| 变量参与说明 | `PS*`/`S*`/`reset` 更适合按事件建模；`hbrg` 是输出动作，变量压力低于 Path2 EFSM。 |
| run_id | `pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| token/cost/time | tokens=`{'prompt_tokens': 26372, 'completion_tokens': 7265, 'total_tokens': 33637, 'n_calls': 3}`, elapsed=`399.823s` |
| run record | [`pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

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

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9182 | 生成初始 DSL 与 grounding seeds | initial len=669 | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13753 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10702 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | SD-10 | SL-10B | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|
| 0 | `<none>` | no | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_to_floor1_stopped` | default-init verifies the initial transition dispatches to floor F1 with stopped hbrg output, then an empty cycle does n...<truncated 25 chars> | ✅ |
| `f1_request_f2_then_continue_to_f3` | default-init covers F1 PS2 upward motion to MU2, S2 arrival at F2, immediate PS3 check to continue upward to MU3, and S3...<truncated 15 chars> | ✅ |
| `f1_direct_request_f3` | default-init verifies PS3 from F1 targets direct upward motion MU3, then S3 stops at F3. | ✅ |
| `f3_request_f2_then_continue_to_f1` | explicit-hot-start at F3 covers PS2 downward motion to MD2, S2 arrival at F2, immediate PS1 check to continue downward t...<truncated 28 chars> | ✅ |
| `f3_direct_request_f1` | explicit-hot-start at F3 verifies PS1 targets direct downward motion MD1 and S1 stops at F1. | ✅ |
| `reset_forces_floor1_from_up_motion` | explicit-hot-start from upward motion MU3 verifies Reset forces floor F1 and stopped hbrg regardless of outstanding upwa...<truncated 19 chars> | ✅ |
| `reset_forces_floor1_from_down_motion` | explicit-hot-start from downward motion MD2 verifies Reset forces floor F1 and stopped hbrg regardless of outstanding do...<truncated 23 chars> | ✅ |
| `reset_forces_floor1_from_floor_state` | explicit-hot-start from floor state F2 verifies Reset forces floor F1 and stopped hbrg even when already stopped at a no...<truncated 11 chars> | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_to_floor1_stopped` — default-init verifies the initial transition dispatches to floor F1 with stopped hbrg output, then an empty cycle does not create a phantom move.</summary>

| Field | Value |
|---|---|
| description | default-init verifies the initial transition dispatches to floor F1 with stopped hbrg output, then an empty cycle does not create a phantom move. |
| initial_state | `<default-init>` |
| initial_vars | `{}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_f1` | `0` | `[]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |
| 1 `no_request_stays_f1` | `0` | `[]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`f1_request_f2_then_continue_to_f3` — default-init covers F1 PS2 upward motion to MU2, S2 arrival at F2, immediate PS3 check to continue upward to MU3, and S3 arrival at F3.</summary>

| Field | Value |
|---|---|
| description | default-init covers F1 PS2 upward motion to MU2, S2 arrival at F2, immediate PS3 check to continue upward to MU3, and S3 arrival at F3. |
| initial_state | `<default-init>` |
| initial_vars | `{}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `default_dispatch_to_f1` | `0` | `[]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |
| 1 `ps2_from_f1_enters_mu2` | `0` | `["AutomaticElevatorController.F1.PS2"]` | `AutomaticElevatorController.MU2` | `{"hbrg": 1}` |
| 2 `s2_arrival_enters_f2` | `0` | `["AutomaticElevatorController.MU2.S2"]` | `AutomaticElevatorController.F2` | `{"hbrg": 0}` |
| 3 `ps3_from_f2_enters_mu3` | `0` | `["AutomaticElevatorController.F2.PS3"]` | `AutomaticElevatorController.MU3` | `{"hbrg": 1}` |
| 4 `s3_arrival_enters_f3` | `0` | `["AutomaticElevatorController.MU3.S3"]` | `AutomaticElevatorController.F3` | `{"hbrg": 0}` |

</details>

<details><summary>`f1_direct_request_f3` — default-init verifies PS3 from F1 targets direct upward motion MU3, then S3 stops at F3.</summary>

| Field | Value |
|---|---|
| description | default-init verifies PS3 from F1 targets direct upward motion MU3, then S3 stops at F3. |
| initial_state | `<default-init>` |
| initial_vars | `{}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `default_dispatch_to_f1` | `0` | `[]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |
| 1 `ps3_from_f1_enters_mu3` | `0` | `["AutomaticElevatorController.F1.PS3"]` | `AutomaticElevatorController.MU3` | `{"hbrg": 1}` |
| 2 `s3_arrival_enters_f3` | `0` | `["AutomaticElevatorController.MU3.S3"]` | `AutomaticElevatorController.F3` | `{"hbrg": 0}` |

</details>

<details><summary>`f3_request_f2_then_continue_to_f1` — explicit-hot-start at F3 covers PS2 downward motion to MD2, S2 arrival at F2, immediate PS1 check to continue downward to MD1, and S1 arrival at F1.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start at F3 covers PS2 downward motion to MD2, S2 arrival at F2, immediate PS1 check to continue downward to MD1, and S1 arrival at F1. |
| initial_state | `AutomaticElevatorController.F3` |
| initial_vars | `{"hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ps2_from_f3_enters_md2` | `0` | `["AutomaticElevatorController.F3.PS2"]` | `AutomaticElevatorController.MD2` | `{"hbrg": -1}` |
| 1 `s2_arrival_enters_f2` | `0` | `["AutomaticElevatorController.MD2.S2"]` | `AutomaticElevatorController.F2` | `{"hbrg": 0}` |
| 2 `ps1_from_f2_enters_md1` | `0` | `["AutomaticElevatorController.F2.PS1"]` | `AutomaticElevatorController.MD1` | `{"hbrg": -1}` |
| 3 `s1_arrival_enters_f1` | `0` | `["AutomaticElevatorController.MD1.S1"]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`f3_direct_request_f1` — explicit-hot-start at F3 verifies PS1 targets direct downward motion MD1 and S1 stops at F1.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start at F3 verifies PS1 targets direct downward motion MD1 and S1 stops at F1. |
| initial_state | `AutomaticElevatorController.F3` |
| initial_vars | `{"hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ps1_from_f3_enters_md1` | `0` | `["AutomaticElevatorController.F3.PS1"]` | `AutomaticElevatorController.MD1` | `{"hbrg": -1}` |
| 1 `s1_arrival_enters_f1` | `0` | `["AutomaticElevatorController.MD1.S1"]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`reset_forces_floor1_from_up_motion` — explicit-hot-start from upward motion MU3 verifies Reset forces floor F1 and stopped hbrg regardless of outstanding upward request context.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from upward motion MU3 verifies Reset forces floor F1 and stopped hbrg regardless of outstanding upward request context. |
| initial_state | `AutomaticElevatorController.MU3` |
| initial_vars | `{"hbrg": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `reset_from_mu3_enters_f1` | `0` | `["AutomaticElevatorController.Reset"]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`reset_forces_floor1_from_down_motion` — explicit-hot-start from downward motion MD2 verifies Reset forces floor F1 and stopped hbrg regardless of outstanding downward request context.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from downward motion MD2 verifies Reset forces floor F1 and stopped hbrg regardless of outstanding downward request context. |
| initial_state | `AutomaticElevatorController.MD2` |
| initial_vars | `{"hbrg": -1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `reset_from_md2_enters_f1` | `0` | `["AutomaticElevatorController.Reset"]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>

<details><summary>`reset_forces_floor1_from_floor_state` — explicit-hot-start from floor state F2 verifies Reset forces floor F1 and stopped hbrg even when already stopped at a non-F1 floor.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from floor state F2 verifies Reset forces floor F1 and stopped hbrg even when already stopped at a non-F1 floor. |
| initial_state | `AutomaticElevatorController.F2` |
| initial_vars | `{"hbrg": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `reset_from_f2_enters_f1` | `0` | `["AutomaticElevatorController.Reset"]` | `AutomaticElevatorController.F1` | `{"hbrg": 0}` |

</details>


### 7. Repair / blocking feedback 明细

- 本 run 未进入 `SD-8/SL-9/SD-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3000, 'model': 'gpt-5.5', 'prompt_tokens': 6182, 'total_tokens': 9182}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2561, 'model': 'gpt-5.5', 'prompt_tokens': 11192, 'total_tokens': 13753}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1704, 'model': 'gpt-5.5', 'prompt_tokens': 8998, 'total_tokens': 10702}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/17`，missing=`SD-8, SL-9, SD-10, SL-10B, SC-11`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
