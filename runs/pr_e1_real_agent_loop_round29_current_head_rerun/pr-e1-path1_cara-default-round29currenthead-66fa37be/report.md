## path1 / cara-infusion-pump-formal-spec__01 / default 真实运行结果：Path1 CARA representative NL

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
| case_id | `cara-infusion-pump-formal-spec__01` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `4605f0473152018e556332ce4349f6efbc7e1d75` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:993dd2a89560dc22cd287bbf50c2cbe6faab9e99a63729d53f02e0d42085b247` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-round29currenthead-66fa37be` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"final_dsl_hash": "sha256:b1f7d59403696a96c1e1bfc84c2b282342792b41cd5f5c49f36ebe632d383352", "source_kind": "initial_or_unrepaired"}` |
| FixLog next_action 序列 | `<none>` |
| iteration exit_reason 序列 | `full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 39455, 'completion_tokens': 12603, 'total_tokens': 52058, 'estimated_prompt_tokens': 39884, 'estimated_completion_tokens': 9297, 'estimated_total_tokens': 49181, 'prompt_chars': 159532, 'completion_chars': 37184, 'n_calls': 3, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`235.729s` |
| run record | [`pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`flow_log.json`](./flow_log.json), [`fix_log.json`](./fix_log.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

### 2. 输入 NL（多行原文）

```text
At run time, CARA coordinates the Caregiver Interface, Blood Pressure Monitor, Algorithm, and Pump Monitors around an infusion pump that moves fluid into the patient, while sensor readings are stored in a shared buffer for software access. The pump has manual and autocontrol modes. In manual mode, pump speed is set with the built-in switch and the caregiver sets a default flow rate directly on the pump for manual operation, while in autocontrol mode pump speed is set by a control voltage from an external source. The Algorithm component controls infusion rate and records infusion-related data in log files; patient blood pressure is used to compute the infusion rate, with higher pressure producing a lower flow rate. The Caregiver Interface lets the caregiver modify target blood pressure and initiate or terminate algorithmic pump control, and it also displays and sounds error messages. In the Mode_Control_Algorithm hierarchy, CARA has manual and autocontrol-related mode-control states plus an Ask_StartAC submode; within Ask_StartAC, the setpoint can be changed and pressing StartAC enters AutocontrolInit. During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications. If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. As a cross-component fallback, CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual, making manual operation the shared recovery target.
```

### 2.1 输入 NL 中文翻译

```text
运行时，CARA 围绕一台向患者输液的输液泵协调 Caregiver Interface、Blood Pressure Monitor、Algorithm 与 Pump Monitors，传感器读数会写入共享缓冲区供软件访问。泵具有手动和自动控制两种模式。手动模式下，泵速由内置开关设置，护理人员直接在泵上设置默认流量；自动控制模式下，泵速由外部控制电压设置。Algorithm 组件控制输液速率并记录输液相关日志；患者血压用于计算输液速率，血压越高流量越低。Caregiver Interface 允许护理人员修改目标血压，并启动或终止算法泵控制，同时显示和发出错误消息。在 Mode_Control_Algorithm 层次中，CARA 具有手动与自动控制相关的模式控制状态以及 Ask_StartAC 子模式；在 Ask_StartAC 中可以修改设定点，按下 StartAC 会进入 AutocontrolInit。正常自动控制期间，只有没有泵操作并发症时 CARA 才控制流量。如果出现输液管堵塞等泵故障，泵会激活报警信号，护理人员排除故障；当 CARA 正在控制泵时，软件会释放控制。作为跨组件回退，CA_backManual 或 CB_backManual、CP_backManual、CC_backManual 中任一事件都会使 CA_mode 变为 Manual，使手动操作成为共享恢复目标。
```

### 3. 最终产出的 FCSTM DSL

```pyfcstm
def float patient_bp = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float builtin_switch_speed = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float shared_buffer_bp = 0.0;
def int CA_mode = 0;
def int alarm_signal = 0;
def int control_released = 0;
def int infusion_log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! * -> Manual :: TerminateAC;

        >> during before { shared_buffer_bp = patient_bp; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                alarm_signal = 0;
                control_released = 1;
            }
            during {
                flow_rate = default_flow_rate;
                pump_speed = builtin_switch_speed;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                control_released = 0;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                control_released = 0;
            }
            during {
                if [patient_bp > target_bp] {
                    flow_rate = flow_rate - 1.0;
                } else if [patient_bp < target_bp] {
                    flow_rate = flow_rate + 1.0;
                } else {
                    flow_rate = flow_rate;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                infusion_log_count = infusion_log_count + 1;
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
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault :: PumpFault;
        PumpFault -> Manual :: FaultRemoved;
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12773 | 生成初始 DSL 与 grounding seeds | initial len=2373 | [`record`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=18752 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=20533 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-round29currenthead-66fa37be.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T08:37:21Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 2 | `2026-06-04T08:37:21Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 3 | `2026-06-04T08:39:17Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 4 | `2026-06-04T08:39:17Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2373,hash=sha256:b1f7d5940369 |
| 5 | `2026-06-04T08:39:17Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:b1f7d59403696a96c1e1bfc84c2b282342792b41cd5f5c49f36ebe632d383352 |
| 6 | `2026-06-04T08:39:17Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2373,hash=sha256:b1f7d5940369, current_hash=sha256:b1f7d59403696a96c1e1bfc84c2b282342792b41cd5f5c49f36ebe632d383352 |
| 7 | `2026-06-04T08:39:17Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 8 | `2026-06-04T08:39:18Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 9 | `2026-06-04T08:39:18Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 10 | `2026-06-04T08:39:18Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 11 | `2026-06-04T08:39:18Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 12 | `2026-06-04T08:39:18Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T08:39:18Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 14 | `2026-06-04T08:40:37Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T08:40:37Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 16 | `2026-06-04T08:40:37Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 17 | `2026-06-04T08:40:37Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 18 | `2026-06-04T08:40:37Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T08:40:37Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 20 | `2026-06-04T08:41:16Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-04T08:41:16Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T08:41:16Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 23 | `2026-06-04T08:41:16Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 24 | `2026-06-04T08:41:16Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=2373,hash=sha256:b1f7d5940369 |
| 25 | `2026-06-04T08:41:16Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=2373,hash=sha256:b1f7d5940369 |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_enters_manual_and_uses_manual_outputs` | default-init probe: first empty cycle dispatches to Manual, sets CA_mode to Manual/released, and manual operation uses d...<truncated 38 chars> | ✅ |
| `initiate_setpoint_start_sequence_to_normal` | explicit-hot-start probe: from Manual, caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC to enter...<truncated 50 chars> | ✅ |
| `autocontrol_high_pressure_lowers_flow_and_logs` | explicit-hot-start probe: in AutocontrolNormal, blood pressure above target lowers flow rate, stores BP in the shared bu...<truncated 60 chars> | ✅ |
| `autocontrol_low_pressure_raises_flow_and_logs` | explicit-hot-start probe: in AutocontrolNormal, blood pressure below target raises flow rate and the pump speed follows ...<truncated 30 chars> | ✅ |
| `pump_fault_alarm_release_then_fault_removed_manual` | explicit-hot-start probe: from normal autocontrol, PumpFault activates alarm and releases software control; FaultRemoved...<truncated 38 chars> | ✅ |
| `ca_backmanual_forces_manual_from_ask` | explicit-hot-start probe: CA_backManual is a cross-component fallback from Ask_StartAC to the shared Manual recovery tar...<truncated 4 chars> | ✅ |
| `cb_backmanual_forces_manual_from_autocontrol_normal` | explicit-hot-start probe: CB_backManual forces recovery from AutocontrolNormal to Manual and releases algorithmic pump c...<truncated 7 chars> | ✅ |
| `cp_cc_and_terminate_forced_recovery_targets` | explicit-hot-start probe: CP_backManual from PumpFault, CC_backManual from Ask_StartAC, and TerminateAC from Autocontrol...<truncated 49 chars> | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_enters_manual_and_uses_manual_outputs` — default-init probe: first empty cycle dispatches to Manual, sets CA_mode to Manual/released, and manual operation uses default flow and built-in switch speed.</summary>

| Field | Value |
|---|---|
| description | default-init probe: first empty cycle dispatches to Manual, sets CA_mode to Manual/released, and manual operation uses default flow and built-in switch speed. |
| initial_state | `<default-init>` |
| initial_vars | `{"builtin_switch_speed": 2.0, "default_flow_rate": 5.0, "patient_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `default_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 5.0, "pump_speed": 2.0}` |

</details>

<details><summary>`initiate_setpoint_start_sequence_to_normal` — explicit-hot-start probe: from Manual, caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC to enter AutocontrolInit, then reaches normal au...<truncated 10 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: from Manual, caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC to enter AutocontrolInit, then reaches normal autocontrol. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"flow_rate": 4.0, "patient_bp": 70.0, "requested_target_bp": 90.0, "target_bp": 80.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiate_reaches_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 1 `setpoint_changed_updates_target_and_stays_in_ask` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointChanged"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 90.0}` |
| 2 `startac_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "control_released": 0}` |
| 3 `transient_init_advances_to_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 1, "control_released": 0, "control_voltage": 5.0, "flow_rate": 5.0, "infusion_log_count": 1, "pump_speed": 5.0}` |

</details>

<details><summary>`autocontrol_high_pressure_lowers_flow_and_logs` — explicit-hot-start probe: in AutocontrolNormal, blood pressure above target lowers flow rate, stores BP in the shared buffer, drives pump speed from control vol...<truncated 20 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: in AutocontrolNormal, blood pressure above target lowers flow rate, stores BP in the shared buffer, drives pump speed from control voltage, and logs data. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"flow_rate": 10.0, "infusion_log_count": 7, "patient_bp": 130.0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `high_bp_decreases_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 9.0, "flow_rate": 9.0, "infusion_log_count": 8, "pump_speed": 9.0, "shared_buffer_bp": 130.0}` |

</details>

<details><summary>`autocontrol_low_pressure_raises_flow_and_logs` — explicit-hot-start probe: in AutocontrolNormal, blood pressure below target raises flow rate and the pump speed follows the resulting control voltage.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: in AutocontrolNormal, blood pressure below target raises flow rate and the pump speed follows the resulting control voltage. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"flow_rate": 3.0, "infusion_log_count": 2, "patient_bp": 80.0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `low_bp_increases_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 4.0, "flow_rate": 4.0, "infusion_log_count": 3, "pump_speed": 4.0}` |

</details>

<details><summary>`pump_fault_alarm_release_then_fault_removed_manual` — explicit-hot-start probe: from normal autocontrol, PumpFault activates alarm and releases software control; FaultRemoved returns to Manual recovery operation.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: from normal autocontrol, PumpFault activates alarm and releases software control; FaultRemoved returns to Manual recovery operation. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "builtin_switch_speed": 1.5, "control_released": 0, "default_flow_rate": 6.0, "flow_rate": 6.0, "patient_bp": 100.0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `pump_fault_enters_fault_state` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolNormal.PumpFault"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1}` |
| 1 `fault_removed_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 6.0, "pump_speed": 1.5}` |

</details>

<details><summary>`ca_backmanual_forces_manual_from_ask` — explicit-hot-start probe: CA_backManual is a cross-component fallback from Ask_StartAC to the shared Manual recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: CA_backManual is a cross-component fallback from Ask_StartAC to the shared Manual recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "builtin_switch_speed": 2.5, "control_released": 0, "default_flow_rate": 4.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_lands_manual` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 4.0, "pump_speed": 2.5}` |

</details>

<details><summary>`cb_backmanual_forces_manual_from_autocontrol_normal` — explicit-hot-start probe: CB_backManual forces recovery from AutocontrolNormal to Manual and releases algorithmic pump control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: CB_backManual forces recovery from AutocontrolNormal to Manual and releases algorithmic pump control. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "builtin_switch_speed": 3.0, "control_released": 0, "default_flow_rate": 7.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_lands_manual` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 7.0, "pump_speed": 3.0}` |

</details>

<details><summary>`cp_cc_and_terminate_forced_recovery_targets` — explicit-hot-start probe: CP_backManual from PumpFault, CC_backManual from Ask_StartAC, and TerminateAC from AutocontrolInit all force the shared Manual recover...<truncated 9 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: CP_backManual from PumpFault, CC_backManual from Ask_StartAC, and TerminateAC from AutocontrolInit all force the shared Manual recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "builtin_switch_speed": 2.0, "control_released": 0, "default_flow_rate": 8.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_from_pumpfault_lands_manual` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 8.0, "pump_speed": 2.0}` |
| 1 `reenter_ask_for_cc_probe` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 2 `cc_backmanual_from_ask_lands_manual` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "flow_rate": 8.0, "pump_speed": 2.0}` |
| 3 `reenter_ask_for_terminate_probe` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 4 `startac_enters_init_for_terminate_probe` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "control_released": 0}` |
| 5 `terminate_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 8.0, "pump_speed": 2.0}` |

</details>


### 7. Repair / blocking feedback 明细

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4905, 'completion_chars': 19182, 'completion_tokens': 6323, 'elapsed_seconds': 116.6578646949929, 'estimated_completion_tokens': 4796, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11453, 'first_chunk_seconds': 28.978850703992066, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12773}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2709, 'completion_chars': 10859, 'completion_tokens': 4247, 'elapsed_seconds': 78.84763268299866, 'estimated_completion_tokens': 2715, 'estimated_prompt_tokens': 14798, 'estimated_total_tokens': 17513, 'first_chunk_seconds': 32.30041575299401, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 59191, 'prompt_tokens': 14505, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 18752}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1514, 'completion_chars': 7143, 'completion_tokens': 2033, 'elapsed_seconds': 39.486899509996874, 'estimated_completion_tokens': 1786, 'estimated_prompt_tokens': 18429, 'estimated_total_tokens': 20215, 'first_chunk_seconds': 12.342636825007503, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 73715, 'prompt_tokens': 18500, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20533}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
