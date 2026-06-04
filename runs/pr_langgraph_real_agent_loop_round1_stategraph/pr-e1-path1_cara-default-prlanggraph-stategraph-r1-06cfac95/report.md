## path1 / cara-infusion-pump-formal-spec__01 / default 真实运行结果：Path1 CARA representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`success`；record_status：`success`；result_status：`converged`。
- main_result_eligible：`false`。
- Path2 ref-model blueprint eligible：`n/a`；reason：not_applicable_to_path1。
- 一句话结论：`success_but_weak_oracle_ineligible`；停止原因：full_pass_all_required_feedback_ok。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `cara-infusion-pump-formal-spec__01` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `d6f724e5739a8979f426efed06e33626e6953eed` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:993dd2a89560dc22cd287bbf50c2cbe6faab9e99a63729d53f02e0d42085b247` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:ee24d33cefd4c6a306c51cba43096280ff0d137f9dad2ee9e56a34647b35b3a3", "iteration": 1, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:a079cfeba8dad62d9eebafabd0d4dbd560bd5f622a0c5534ba7a5cbc79f0c49d", "iteration": 1, "repair_history_index": 2, "rework_instructions": ["Fix `terminate_ac_from_init_returns_manual`: dispatching `CARA.Mode_Control_Algorithm.TerminateAC` from hot-start state `CARA.Mode_Control_Algorithm.AutocontrolInit` must transition to `CARA.Mode_Control_Algorithm.Manual`, not to `AutocontrolNormal`. Ensure Manual entry/during recovery then yields `CA_mode=0`, `software_control=0`, `alarm_signal=0`, `pump_fault=0`, `shared_buffer=blood_pressure`, `pump_speed=built_in_switch`, and `flow_rate=default_flow_rate`.", "Make the DSL event/transition mechanism ensure `AutocontrolInit -> Manual : TerminateAC` has priority over or is not bypassed by the unguarded `AutocontrolInit -> AutocontrolNormal;` transition when the TerminateAC event is injected. A minimal likely edit is to place the `AutocontrolInit -> Manual : TerminateAC` transition before the unguarded `AutocontrolInit -> AutocontrolNormal;`, if this DSL uses declaration order for transition selection; otherwise add the smallest DSL-supported guard/structure that prevents the unguarded completion transition from consuming a TerminateAC step.", "Preserve the parent-scoped event visibility repairs for `InitiateAC`, `ChangeSetpoint`, `StartAC`, `TerminateAC`, `PumpFaultDetected`, and `FaultRemoved`, because those resolved the prior unresolved-event-path failures.", "Preserve the NL-required concrete grounding for `action:set_target_blood_pressure` as `Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_blood_pressure = setpoint; }` and for `guard:pump_fault_positive` as `AutocontrolNormal -> PumpFault : if [pump_fault > 0];`. In the next SL-9 rationale, explicitly map these lines to the local missing-required-grounding IDs so SL-10 can evaluate or override that conservative local objection without cycling.", "Do not delete required states, variables, forced backManual transitions, Manual recovery outputs, PumpFaultDetected `pump_fault = 1`, FaultRemoved `pump_fault = 0`, alarm/software-control release behavior, shared-buffer updates, or the monotonic infusion-rate computation."], "same_as_final": false, "sl10_decision": "rework"}, "matching_repair_history_indices": [3], "repair_history_index": 3, "selected_source_stage": "SD-6", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 570304, 'completion_tokens': 47721, 'total_tokens': 618025, 'estimated_prompt_tokens': 628617, 'estimated_completion_tokens': 39016, 'estimated_total_tokens': 667633, 'prompt_chars': 2514450, 'completion_chars': 156043, 'n_calls': 15, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`923.086s` |
| run record | [`pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
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
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int log_count = 0;
def float built_in_switch = 0.0;
def float default_flow_rate = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float blood_pressure = 0.0;
def float target_blood_pressure = 0.0;
def float setpoint = 0.0;
def float infusion_rate = 0.0;
def float flow_rate = 0.0;
def float shared_buffer = 0.0;

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
                alarm_signal = 0;
                pump_fault = 0;
            }
            during {
                shared_buffer = blood_pressure;
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
            during {
                shared_buffer = blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                pump_speed = control_voltage;
            }
            during {
                shared_buffer = blood_pressure;
                log_count = log_count + 1;
            }
        }

        state AutocontrolNormal {
            during {
                shared_buffer = blood_pressure;
                infusion_rate = target_blood_pressure - blood_pressure;
                flow_rate = infusion_rate;
                pump_speed = control_voltage;
                log_count = log_count + 1;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
            during {
                shared_buffer = blood_pressure;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
            target_blood_pressure = setpoint;
        };
        Ask_StartAC -> AutocontrolInit : StartAC;
        AutocontrolInit -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> AutocontrolNormal : PumpFaultDetected effect {
            pump_fault = 1;
        };
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual : FaultRemoved effect {
            pump_fault = 0;
        };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12360 | 生成初始 DSL 与 grounding seeds | initial len=2671 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=2, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=261638 | LLM per-request accept/reject + repair | candidate len=2818,2886,2879,2879 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=4, tokens=198137 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=261638 | LLM per-request accept/reject + repair | candidate len=2818,2886,2879,2879 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=198137 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=5, tokens=122555 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=5, tokens=122555 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=5, tokens=122555 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ⚠️ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=261638 | LLM per-request accept/reject + repair | candidate len=2818,2886,2879,2879 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=198137 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=261638 | LLM per-request accept/reject + repair | candidate len=2818,2886,2879,2879 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=198137 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=5, tokens=122555 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=5, tokens=122555 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=1, tokens=23335 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r1-06cfac95.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T14:51:22Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T14:51:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T14:51:22Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T14:53:11Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T14:53:11Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2671,hash=sha256:d4eb38ad6318 |
| 7 | `2026-06-04T14:53:11Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-04T14:53:11Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-04T14:53:11Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:d4eb38ad63180890b8e61400bf55e7d4196c2463ce14ff69ac1a6b88542836c9 |
| 10 | `2026-06-04T14:53:11Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2671,hash=sha256:d4eb38ad6318, current_hash=sha256:d4eb38ad63180890b8e61400bf55e7d4196c2463ce14ff69ac1a6b88542836c9 |
| 11 | `2026-06-04T14:53:11Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 12 | `2026-06-04T14:53:12Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T14:53:12Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 14 | `2026-06-04T14:53:12Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T14:53:12Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 16 | `2026-06-04T14:53:12Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 17 | `2026-06-04T14:53:12Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=pump_fault", "W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault"], "diagnostic_codes": ["W_UNWRITTEN_READ_VAR", "W_GUARD_VARS_NEVER_CHANGE", "W_HIGH_VAR_TO_LEAF_RATIO", "W_UNREFERENCED_VAR", "W_UNREFERENCED_VAR", "W_UNRE...<truncated 1024 chars> | <none> |
| 18 | `2026-06-04T14:53:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-04T14:53:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 20 | `2026-06-04T14:53:12Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=pump_fault", "W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault"], "diagnostic_codes": ["W_UNWRITTEN_READ_VAR", "W_GUARD_VARS_NEVER_CHANGE", "W_HIGH_VAR_TO_LEAF_RATIO", "W_UNREFERENCED_VAR", "W_UNREFERENCED_VAR", "W_UNREFERENCE...<truncated 5329 chars> | current_dsl:len=2671,hash=sha256:d4eb38ad6318 |
| 21 | `2026-06-04T14:53:12Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T14:53:12Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 2} | <none> |
| 23 | `2026-06-04T14:53:12Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2671,hash=sha256:d4eb38ad6318 |
| 24 | `2026-06-04T14:53:47Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T14:53:47Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-6e7fd24414", "fixreq-0-sd4-1-8e1eb9dac6"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2818,hash=sha256:ee75f9b6f572 |
| 26 | `2026-06-04T14:53:47Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 27 | `2026-06-04T14:53:47Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:ee75f9b6f572d19faae19a0550300c64df2254d41a6031cc0bb8ee6c440c8d16 |
| 28 | `2026-06-04T14:54:07Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-04T14:54:07Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 30 | `2026-06-04T14:54:07Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 31 | `2026-06-04T14:54:07Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2671,hash=sha256:d4eb38ad6318 |
| 32 | `2026-06-04T14:54:49Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-04T14:54:49Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-6e7fd24414", "fixreq-0-sd4-1-8e1eb9dac6"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2886,hash=sha256:3d3419eeddd7 |
| 34 | `2026-06-04T14:54:49Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 35 | `2026-06-04T14:54:49Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63 |
| 36 | `2026-06-04T14:55:14Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 37 | `2026-06-04T14:55:14Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 38 | `2026-06-04T14:55:14Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 39 | `2026-06-04T14:55:14Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2886,hash=sha256:3d3419eeddd7 |
| 40 | `2026-06-04T14:55:14Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63 |
| 41 | `2026-06-04T14:55:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-04T14:55:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-04T14:55:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-04T14:55:14Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63 |
| 45 | `2026-06-04T14:55:14Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=2886,hash=sha256:3d3419eeddd7, current_hash=sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63 |
| 46 | `2026-06-04T14:55:14Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 47 | `2026-06-04T14:55:14Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 48 | `2026-06-04T14:55:14Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 49 | `2026-06-04T14:55:14Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 50 | `2026-06-04T14:55:14Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 51 | `2026-06-04T14:55:14Z` | `SD-4` | `1` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 52 | `2026-06-04T14:55:14Z` | `SL-5` | `1` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 53 | `2026-06-04T14:56:55Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 54 | `2026-06-04T14:56:56Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 55 | `2026-06-04T14:56:56Z` | `SL-5` | `1` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 56 | `2026-06-04T14:58:53Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 57 | `2026-06-04T14:58:53Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 58 | `2026-06-04T14:58:53Z` | `SL-5` | `1` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 59 | `2026-06-04T15:00:37Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 60 | `2026-06-04T15:00:37Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 61 | `2026-06-04T15:00:37Z` | `<control>` | `1` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 62 | `2026-06-04T15:00:37Z` | `SC-5F` | `1` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 63 | `2026-06-04T15:00:37Z` | `SD-6` | `1` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 64 | `2026-06-04T15:00:37Z` | `SD-6` | `1` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 65 | `2026-06-04T15:00:37Z` | `<control>` | `1` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 19, "n_scenarios_passed": 5, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 66 | `2026-06-04T15:00:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 67 | `2026-06-04T15:00:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 68 | `2026-06-04T15:00:37Z` | `SD-8` | `1` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 19, "n_scenarios_passed": 5, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2886,hash=sha256:3d3419eeddd7 |
| 69 | `2026-06-04T15:00:37Z` | `SD-8` | `1` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 70 | `2026-06-04T15:00:37Z` | `SD-8` | `1` | `fix_request_batch` | {"request_count": 12} | <none> |
| 71 | `2026-06-04T15:00:37Z` | `SL-9` | `1` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2886,hash=sha256:3d3419eeddd7 |
| 72 | `2026-06-04T15:01:48Z` | `SL-9` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 73 | `2026-06-04T15:01:48Z` | `SL-9` | `1` | `stage_result` | {"accepted_request_ids": ["fixreq-1-sd6-0-84b72ce8c3", "fixreq-1-sd6-1-b5cb7c375e", "fixreq-1-sd6-2-66435c0136", "fixreq-1-sd6-3-33babb71b1", "fixreq-1-sd6-4-df06be3fd5", "fixreq-1-sd6-5-8ba2140fd2", "fixreq-1-sd6-6-8641853111", "fixreq-1-sd6-7-99991315e0", "fixreq-1-sd6-8-fa28f205da", "fixreq-1-sd6-9-8a06e4dcc3", "fixreq-1-sd6-10-ec972d3007", "fixreq-1-sd6-11-3b2dfc2561"], "jump": "SL-10", "ok": true, "rejected_requ...<truncated 13 chars> | candidate_dsl:len=2879,hash=sha256:a079cfeba8da |
| 74 | `2026-06-04T15:01:48Z` | `SD-10` | `1` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 75 | `2026-06-04T15:01:48Z` | `SL-10` | `1` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:a079cfeba8dad62d9eebafabd0d4dbd560bd5f622a0c5534ba7a5cbc79f0c49d |
| 76 | `2026-06-04T15:02:19Z` | `SL-10` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 77 | `2026-06-04T15:02:19Z` | `SL-10` | `1` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 78 | `2026-06-04T15:02:19Z` | `SL-10` | `1` | `grounding_update_hints_recorded` | {} | <none> |
| 79 | `2026-06-04T15:02:19Z` | `SL-9` | `1` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2886,hash=sha256:3d3419eeddd7 |
| 80 | `2026-06-04T15:03:16Z` | `SL-9` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
- ……另有 `41` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-4` | yes | fixbatch-0-sha256-120a1d24192 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-6` | yes | fixbatch-1-sha256-4b80740816b / n=12 | accept=12, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 2 | Iter 3 |
|---|---|---|---|
| `effect_mutation_change_setpoint_exact_persistence` | explicit-hot-start probe: ChangeSetpoint's transition effect must copy setpoint exactly, not omit the effect or assign a...<truncated 75 chars> | ⚪ | ✅ |
| `effect_mutation_pumpfaultdetected_exact_flag` | explicit-hot-start probe: PumpFaultDetected's transition effect must set pump_fault exactly to 1 before the separate pos...<truncated 41 chars> | ⚪ | ✅ |
| `effect_mutation_faultremoved_recovery_outputs` | explicit-hot-start probe: FaultRemoved recovery to Manual must leave the fault flag exactly cleared and restore manual o...<truncated 80 chars> | ⚪ | ✅ |
| `default_init_startac_then_terminate_from_init` | default-init probe: first empty cycle must dispatch to Manual, InitiateAC must enter Ask_StartAC, StartAC must enter Aut...<truncated 74 chars> | ⚪ | ✅ |
| `normal_idle_then_terminate_to_manual` | explicit-hot-start probe: AutocontrolNormal with no pump fault must stay in normal autocontrol and compute commanded flo...<truncated 48 chars> | ⚪ | ✅ |
| `all_backmanual_forced_recovery_events` | explicit-hot-start probe: each cross-component BackManual forced event must work from a concrete non-Manual leaf and lan...<truncated 34 chars> | ⚪ | ✅ |
| `default_init_manual_mode_outputs` |  | ✅ | ⚪ |
| `initiate_change_setpoint_start_autocontrol` |  | ⚪ | ⚪ |
| `autocontrol_normal_lower_pressure_higher_flow` |  | ✅ | ⚪ |
| `autocontrol_normal_higher_pressure_lower_flow` |  | ✅ | ⚪ |
| `pump_fault_detected_then_alarm_state` |  | ⚪ | ⚪ |
| `fault_removed_returns_manual_and_clears_fault` |  | ⚪ | ⚪ |
| `terminate_ac_from_init_returns_manual` |  | ⚪ | ⚪ |
| `terminate_ac_from_normal_returns_manual` |  | ⚪ | ⚪ |
| `forced_backmanual_from_ask_and_init` |  | ⚪ | ⚪ |
| `forced_backmanual_from_normal_and_fault` |  | ⚪ | ⚪ |
| `atomic_startac_target_and_entry_effects` |  | ⚪ | ⚪ |
| `atomic_change_setpoint_effect_value` |  | ⚪ | ⚪ |
| `atomic_fault_detection_effect_and_guard_target` |  | ⚪ | ⚪ |
| `atomic_forced_backmanual_each_event` |  | ⚪ | ⚪ |
| `atomic_fault_removed_clears_exact_fault_flag` |  | ⚪ | ⚪ |
| `atomic_initiateac_exact_ask_target` |  | ⚪ | ⚪ |
| `atomic_autocontrolinit_advances_exact_normal_target` |  | ✅ | ⚪ |
| `atomic_forced_backmanual_from_fault_clears_alarm_fault` |  | ✅ | ⚪ |
| `atomic_terminate_normal_manual_enter_effects_from_dirty_flags` |  | ⚪ | ⚪ |

#### 6.2 Scenario definitions

<details><summary>`effect_mutation_change_setpoint_exact_persistence` — explicit-hot-start probe: ChangeSetpoint's transition effect must copy setpoint exactly, not omit the effect or assign an offset constant, and the value must pe...<truncated 35 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: ChangeSetpoint's transition effect must copy setpoint exactly, not omit the effect or assign an offset constant, and the value must persist while waiting in Ask_StartAC. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"blood_pressure": 79.0, "setpoint": 123.5, "target_blood_pressure": 60.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `change_setpoint_exact_copy_not_missing_or_offset` | `0` | `["CARA.Mode_Control_Algorithm.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"shared_buffer": 79.0, "target_blood_pressure": 123.5}` |
| 1 `target_pressure_persists_after_idle_ask_cycle` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"shared_buffer": 79.0, "target_blood_pressure": 123.5}` |

</details>

<details><summary>`effect_mutation_pumpfaultdetected_exact_flag` — explicit-hot-start probe: PumpFaultDetected's transition effect must set pump_fault exactly to 1 before the separate positive-fault guard cycle enters PumpFault...<truncated 1 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: PumpFaultDetected's transition effect must set pump_fault exactly to 1 before the separate positive-fault guard cycle enters PumpFault. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "blood_pressure": 92.0, "control_voltage": 4.0, "log_count": 0, "pump_fault": 0, "software_control": 1, "target_blood_pressure": 130.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_event_sets_exact_flag_not_missing_or_offset` | `0` | `["CARA.Mode_Control_Algorithm.PumpFaultDetected"]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"flow_rate": 38.0, "infusion_rate": 38.0, "log_count": 1, "pump_fault": 1, "pump_speed": 4.0, "shared_buffer": 92.0}` |
| 1 `positive_fault_guard_then_alarm_release` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "shared_buffer": 92.0, "software_control": 0}` |

</details>

<details><summary>`effect_mutation_faultremoved_recovery_outputs` — explicit-hot-start probe: FaultRemoved recovery to Manual must leave the fault flag exactly cleared and restore manual outputs, exposing wrong recovery effect v...<truncated 40 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: FaultRemoved recovery to Manual must leave the fault flag exactly cleared and restore manual outputs, exposing wrong recovery effect values even with Manual recovery actions. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 0, "alarm_signal": 1, "blood_pressure": 74.0, "built_in_switch": 1.25, "default_flow_rate": 2.75, "pump_fault": 1, "software_control": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `faultremoved_exact_clear_and_manual_outputs` | `0` | `["CARA.Mode_Control_Algorithm.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 2.75, "pump_fault": 0, "pump_speed": 1.25, "shared_buffer": 74.0, "software_control": 0}` |

</details>

<details><summary>`default_init_startac_then_terminate_from_init` — default-init probe: first empty cycle must dispatch to Manual, InitiateAC must enter Ask_StartAC, StartAC must enter AutocontrolInit, and TerminateAC from Autoc...<truncated 34 chars></summary>

| Field | Value |
|---|---|
| description | default-init probe: first empty cycle must dispatch to Manual, InitiateAC must enter Ask_StartAC, StartAC must enter AutocontrolInit, and TerminateAC from AutocontrolInit must recover to Manual. |
| initial_state | `<default-init>` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "blood_pressure": 80.0, "built_in_switch": 2.0, "control_voltage": 3.3, "default_flow_rate": 5.0, "log_count": 0, "pump_fault": 0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `default_dispatch_to_manual_with_manual_outputs` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 5.0, "pump_fault": 0, "pump_speed": 2.0, "shared_buffer": 80.0, "software_control": 0}` |
| 1 `initiate_ac_targets_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 0, "shared_buffer": 80.0, "software_control": 0}` |
| 2 `start_ac_targets_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "log_count": 1, "pump_speed": 3.3, "shared_buffer": 80.0, "software_control": 1}` |
| 3 `terminate_from_init_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 5.0, "pump_fault": 0, "pump_speed": 2.0, "shared_buffer": 80.0, "software_control": 0}` |

</details>

<details><summary>`normal_idle_then_terminate_to_manual` — explicit-hot-start probe: AutocontrolNormal with no pump fault must stay in normal autocontrol and compute commanded flow, then TerminateAC must target Manual r...<truncated 8 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: AutocontrolNormal with no pump fault must stay in normal autocontrol and compute commanded flow, then TerminateAC must target Manual recovery. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "blood_pressure": 90.0, "built_in_switch": 1.5, "control_voltage": 5.0, "default_flow_rate": 2.5, "log_count": 10, "pump_fault": 0, "software_control": 1, "target_blood_pressure": 130.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_fault_stays_normal_and_controls_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"flow_rate": 40.0, "infusion_rate": 40.0, "log_count": 11, "pump_speed": 5.0, "shared_buffer": 90.0}` |
| 1 `terminate_from_normal_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 2.5, "pump_fault": 0, "pump_speed": 1.5, "shared_buffer": 90.0, "software_control": 0}` |

</details>

<details><summary>`all_backmanual_forced_recovery_events` — explicit-hot-start probe: each cross-component BackManual forced event must work from a concrete non-Manual leaf and land in Manual with recovery outputs.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: each cross-component BackManual forced event must work from a concrete non-Manual leaf and land in Manual with recovery outputs. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "blood_pressure": 88.0, "built_in_switch": 1.1, "control_voltage": 4.4, "default_flow_rate": 2.2, "log_count": 0, "pump_fault": 0, "software_control": 1, "target_blood_pressure": 128.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_forces_normal_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 2.2, "pump_fault": 0, "pump_speed": 1.1, "shared_buffer": 88.0, "software_control": 0}` |
| 1 `prepare_ask_for_cb_forced_probe` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"shared_buffer": 88.0}` |
| 2 `cb_backmanual_forces_ask_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 2.2, "pump_fault": 0, "pump_speed": 1.1, "shared_buffer": 88.0, "software_control": 0}` |
| 3 `prepare_init_for_cp_forced_probe` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"shared_buffer": 88.0}` |
| 4 `enter_init_before_cp_forced_probe` | `0` | `["CARA.Mode_Control_Algorithm.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "log_count": 1, "pump_speed": 4.4, "shared_buffer": 88.0, "software_control": 1}` |
| 5 `cp_backmanual_forces_init_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 2.2, "pump_fault": 0, "pump_speed": 1.1, "shared_buffer": 88.0, "software_control": 0}` |
| 6 `prepare_normal_for_cc_forced_probe_ask` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"shared_buffer": 88.0}` |
| 7 `prepare_normal_for_cc_forced_probe_init` | `0` | `["CARA.Mode_Control_Algorithm.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "log_count": 2, "pump_speed": 4.4, "shared_buffer": 88.0, "software_control": 1}` |
| 8 `unguarded_init_completes_to_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"flow_rate": 40.0, "infusion_rate": 40.0, "log_count": 3, "pump_speed": 4.4, "shared_buffer": 88.0}` |
| 9 `cc_backmanual_forces_normal_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 2.2, "pump_fault": 0, "pump_speed": 1.1, "shared_buffer": 88.0, "software_control": 0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=pump_fault, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, ... +3 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 658 chars> | `sha256:ee75f9b6f572d19faae19a0550300c64df2254d41a6031cc0bb8ee6c440c8d16` |
| 2 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=pump_fault, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, ... +3 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63` |
| 3 | `1` | ❌ | `SD-6` | initiate_change_setpoint_start_autocontrol, pump_fault_detected_then_alarm_state, fault_removed_returns_manual_and_clears_fault, terminate_ac_from_init_returns_manual, terminate_ac_from_normal_returns_manual, ... +9 | accept=12, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Fix `terminate_ac_from_init_returns_manual`: dispatching `CARA.Mode_Control_Algorithm.TerminateAC` from hot-start state `CARA.Mode_Control_Algorithm.AutocontrolInit` must trans...<truncated 1022 chars> | `sha256:a079cfeba8dad62d9eebafabd0d4dbd560bd5f622a0c5534ba7a5cbc79f0c49d` |
| 4 | `1` | ✅ | `SD-6` | initiate_change_setpoint_start_autocontrol, pump_fault_detected_then_alarm_state, fault_removed_returns_manual_and_clears_fault, terminate_ac_from_init_returns_manual, terminate_ac_from_normal_returns_manual, ... +9 | accept=12, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:ee24d33cefd4c6a306c51cba43096280ff0d137f9dad2ee9e56a34647b35b3a3` |

<details><summary>Repair 1 / iteration `0` / source `SD-4` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'pump_fault' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=pump_fault, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT, I_TRANSITION_NEVER_EVENT_TRIGGERED`。
- before_dsl_hash：`sha256:d4eb38ad63180890b8e61400bf55e7d4196c2463ce14ff69ac1a6b88542836c9`；candidate_dsl_hash：`sha256:ee75f9b6f572d19faae19a0550300c64df2254d41a6031cc0bb8ee6c440c8d16`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=pump_fault` policy=`budgeted_repair`：Variable 'pump_fault' is read but never written by any action or transition effect.；refs=`{"init_value": "0", "read_states": ["CARA.Mode_Control_Algorithm.AutocontrolNormal"], "var_name": "pump_fault"}`
- 2. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "CARA.Mode_Control_Algorithm.AutocontrolNormal", "guard_vars": ["pump_fault"], "to_path": "CARA.Mode_Control_Algorithm.PumpFault"}`

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `CA_mode` | `unknown` | ✅ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `alarm_signal` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `blood_pressure` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `built_in_switch` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `control_voltage` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `default_flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `infusion_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `log_count` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `pump_fault` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE` |
| `pump_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `setpoint` | `unknown` | ✅ | `W_UNREFERENCED_VAR` |
| `shared_buffer` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `software_control` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `target_blood_pressure` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-120a1d24192`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd4-0-6e7fd24414` | `blocking_warning` | ❌ | ✅ | Variable 'pump_fault' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects. | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-1-8e1eb9dac6` | `blocking_warning` | ❌ | ✅ | Variable 'pump_fault' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects. | `W_GUARD_VARS_NEVER_CHANGE` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:blood_pressure, variable:target_blood_pressure, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2818`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd4-0-6e7fd24414` | `accept` | ❌ | ❌ | The NL explicitly describes a pump fault occurring and later being removed. A meaningful NL-grounded write to pump_fault is therefore appropriate, rather than a self-assignment or deleting the required guard.；intent=Add a PumpFaultDetected event transition from AutocontrolNormal to PumpFault that sets pump_fault = 1, Clear pump_fault when returning to Manual...<truncated 48 chars> |
| `fixreq-0-sd4-1-8e1eb9dac6` | `accept` | ❌ | ❌ | The required AutocontrolNormal-to-PumpFault guard [pump_fault > 0] is preserved, and pump_fault now has NL-grounded writes for fault occurrence and fault removal, so the guard no longer depends only on an unchanged initial value.；intent=Preserve the guarded pump_fault_positive transition, Add NL-grounded pump_fault writes so the guard variable can evolve at ...<truncated 7 chars> |
- repair_rationale：Accepted both design repair requests because the selected diagnostics identify the same root issue: pump_fault was read in the required fault guard but was never written.；The repair preserves the required guard [pump_fault > 0] and the required AutocontrolNormal -> PumpFault transition instead of replacing them with a constant or deleting the fault branch.；The added PumpFaultDetected event is grounded in the NL statement that a pump fault such as tubing occlusion can occur; its effect records that occurrence by setting pump_fault = 1.；The added pump_fault clearing is grounded in the NL statement that the caregiver removes the fault and recovery returns to manual operation.；All required preserved states, variables, events, transitions, guards, and actions remain represented; no unrelated grounded branch was deleted.
- diff_summary：`{"summary": "Added NL-grounded writes to pump_fault: Manual.enter clears it, a new AutocontrolNormal -> PumpFault :: PumpFaultDetected transition sets it to 1, and FaultRemoved clears it while returning to Manual. Preserved the existing guarded AutocontrolNormal -> PumpFault transition."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int log_count = 0;
def float built_in_switch = 0.0;
def float default_flow_rate = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float blood_pressure = 0.0;
def float target_blood_pressure = 0.0;
def float setpoint = 0.0;
def float infusion_rate = 0.0;
def float flow_rate = 0.0;
def float shared_buffer = 0.0;

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
                alarm_signal = 0;
                pump_fault = 0;
            }
            during {
                shared_buffer = blood_pressure;
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
            during {
                shared_buffer = blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                pump_speed = control_voltage;
            }
            during {
                shared_buffer = blood_pressure;
                log_count = log_count + 1;
            }
        }

        state AutocontrolNormal {
            during {
                shared_buffer = blood_pressure;
                infusion_rate = target_blood_pressure - blood_pressure;
                flow_rate = infusion_rate;
                pump_speed = control_voltage;
                log_count = log_count + 1;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
            during {
                shared_buffer = blood_pressure;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_blood_pressure = setpoint; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolNormal -> Manual :: TerminateAC;
        AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_fault = 1; };
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -30,6 +30,7 @@
                 CA_mode = 0;
                 software_control = 0;
                 alarm_signal = 0;
+                pump_fault = 0;
             }
             during {
                 shared_buffer = blood_pressure;
@@ -88,7 +89,8 @@
         AutocontrolInit -> AutocontrolNormal;
         AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolNormal -> Manual :: TerminateAC;
+        AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_fault = 1; };
         AutocontrolNormal -> PumpFault : if [pump_fault > 0];
-        PumpFault -> Manual :: FaultRemoved;
+        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:7c6cb1d4c1b202677b1593aacf79f2e80e77e846dd94beef73ba695329773d34`。
  - SL-10 evidence 1: `{"summary": "The two SL-9 accepted requests both concern the same root issue: pump_fault was read by the required AutocontrolNormal-to-PumpFault guard but was never written. The candidate adds NL-grounded writes: AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_fault = 1; }, Manual.enter clears pump_fault to 0, and PumpFault -> Manual :: FaultRemoved clears pump_fault to 0. This directly addresses W_UNWRITTEN_READ_VAR and W_GUARD_VARS_NEVER_CHANGE without deleting the required pump_fault variable or guarded fault transition."}`
  - SL-10 evidence 2: `{"summary": "The NL explicitly says a pump fault such as tubing occlusion can occur, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. The added PumpFaultDetected event is a small NL-grounded representation of fault occurrence, and the FaultRemoved/Manual clearing effects are grounded in fault removal and recovery to manual operation."}`
  - SL-10 evidence 3: `{"summary": "Required preserved states, variables, transitions, and actions remain represented in the candidate: Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault; CA_mode, software_control, pump_fault, alarm_signal, blood_pressure, target_blood_pressure, infusion_rate, flow_rate, pump_speed, built_in_switch, default_flow_rate, control_voltage, shared_buffer, log_count; InitiateAC, ChangeSetpoint, StartAC, TerminateAC, FaultRemoved, and the backManual transitions. The candidate does not drop any NL-required mode-control obligation."}`
  - SL-10 evidence 4: `{"summary": "The diff is narrowly scoped to pump_fault lifecycle handling. It preserves the existing guarded AutocontrolNormal -> PumpFault : if [pump_fault > 0] transition and adds a separate PumpFaultDetected event transition to set the variable when the external fault occurrence is observed. No scenario regression is reported in the local evidence."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.；For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-ground...<truncated 152 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["action:set_target_blood_pressure", "guard:pump_fault_positive"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `0` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'pump_fault' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=pump_fault, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT, I_TRANSITION_NEVER_EVENT_TRIGGERED`。
- before_dsl_hash：`sha256:d4eb38ad63180890b8e61400bf55e7d4196c2463ce14ff69ac1a6b88542836c9`；candidate_dsl_hash：`sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=pump_fault` policy=`budgeted_repair`：Variable 'pump_fault' is read but never written by any action or transition effect.；refs=`{"init_value": "0", "read_states": ["CARA.Mode_Control_Algorithm.AutocontrolNormal"], "var_name": "pump_fault"}`
- 2. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "CARA.Mode_Control_Algorithm.AutocontrolNormal", "guard_vars": ["pump_fault"], "to_path": "CARA.Mode_Control_Algorithm.PumpFault"}`

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `CA_mode` | `unknown` | ✅ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `alarm_signal` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `blood_pressure` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `built_in_switch` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `control_voltage` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `default_flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `infusion_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `log_count` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `pump_fault` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE` |
| `pump_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `setpoint` | `unknown` | ✅ | `W_UNREFERENCED_VAR` |
| `shared_buffer` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `software_control` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `target_blood_pressure` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-120a1d24192`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd4-0-6e7fd24414` | `blocking_warning` | ❌ | ✅ | Variable 'pump_fault' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects. | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-1-8e1eb9dac6` | `blocking_warning` | ❌ | ✅ | Variable 'pump_fault' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects. | `W_GUARD_VARS_NEVER_CHANGE` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:blood_pressure, variable:target_blood_pressure, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2886`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd4-0-6e7fd24414` | `accept` | ❌ | ✅ | Accepted because the NL explicitly describes pump-fault occurrence and later caregiver fault removal. The repair adds meaningful NL-grounded writes to pump_fault rather than using a self-assignment, deleting the required variable, or treating the guard as a constant.；intent=Add a PumpFaultDetected event while in AutocontrolNormal that records the observed fa...<truncated 200 chars> |
| `fixreq-0-sd4-1-8e1eb9dac6` | `accept` | ❌ | ✅ | Accepted because the AutocontrolNormal -> PumpFault guard reads pump_fault, and pump_fault now has NL-grounded writes for fault occurrence and removal. The required positive guard [pump_fault > 0] remains intact, so the guard no longer depends only on the initial value.；intent=Keep AutocontrolNormal -> PumpFault : if [pump_fault > 0], Make pump_fault evolve ...<truncated 70 chars> |
- repair_rationale：Both accepted requests address the same root design warning: pump_fault was read by the required AutocontrolNormal-to-PumpFault guard but was never written by any action/effect.；The repair uses the NL-grounded event PumpFaultDetected to represent occurrence of a pump fault such as tubing occlusion. It records that occurrence by setting pump_fault = 1 while CARA remains in AutocontrolNormal; the already-required gua...<truncated 48 chars>；The required guard:pump_fault_positive is explicitly preserved as `AutocontrolNormal -> PumpFault : if [pump_fault > 0];`. This avoids deleting or replacing the required guarded fault transition and avoids mixing event and guard on the same...<truncated 12 chars>；The local objection for action:set_target_blood_pressure is addressed by preserving and making explicit the concrete action `target_blood_pressure = setpoint;` in the `Ask_StartAC -> Ask_StartAC :: ChangeSetpoint` effect. This directly repr...<truncated 129 chars>；The local objection for guard:pump_fault_positive is addressed by preserving the concrete positive pump_fault guard exactly. Unlike the previously rejected candidate, the new event write is on an AutocontrolNormal self-transition rather tha...<truncated 171 chars>
- diff_summary：`{"summary": "Added NL-grounded pump_fault lifecycle handling while preserving required grounding: Manual.enter clears pump_fault; AutocontrolNormal has a PumpFaultDetected self-transition that sets pump_fault = 1; the original AutocontrolNormal -> PumpFault : if [pump_fault > 0] guard remains intact; FaultRemoved clears pump_fault on return to Manual; ChangeSetpoint effect is expanded into an explicit effect block for target_blood_pressure = setpoint."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int log_count = 0;
def float built_in_switch = 0.0;
def float default_flow_rate = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float blood_pressure = 0.0;
def float target_blood_pressure = 0.0;
def float setpoint = 0.0;
def float infusion_rate = 0.0;
def float flow_rate = 0.0;
def float shared_buffer = 0.0;

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
                alarm_signal = 0;
                pump_fault = 0;
            }
            during {
                shared_buffer = blood_pressure;
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
            during {
                shared_buffer = blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                pump_speed = control_voltage;
            }
            during {
                shared_buffer = blood_pressure;
                log_count = log_count + 1;
            }
        }

        state AutocontrolNormal {
            during {
                shared_buffer = blood_pressure;
                infusion_rate = target_blood_pressure - blood_pressure;
                flow_rate = infusion_rate;
                pump_speed = control_voltage;
                log_count = log_count + 1;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
            during {
                shared_buffer = blood_pressure;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
            target_blood_pressure = setpoint;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolNormal -> Manual :: TerminateAC;
        AutocontrolNormal -> AutocontrolNormal :: PumpFaultDetected effect {
            pump_fault = 1;
        };
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect {
            pump_fault = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -30,6 +30,7 @@
                 CA_mode = 0;
                 software_control = 0;
                 alarm_signal = 0;
+                pump_fault = 0;
             }
             during {
                 shared_buffer = blood_pressure;
@@ -83,12 +84,19 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_blood_pressure = setpoint; };
+        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
+            target_blood_pressure = setpoint;
+        };
         Ask_StartAC -> AutocontrolInit :: StartAC;
         AutocontrolInit -> AutocontrolNormal;
         AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolNormal -> Manual :: TerminateAC;
+        AutocontrolNormal -> AutocontrolNormal :: PumpFaultDetected effect {
+            pump_fault = 1;
+        };
         AutocontrolNormal -> PumpFault : if [pump_fault > 0];
-        PumpFault -> Manual :: FaultRemoved;
+        PumpFault -> Manual :: FaultRemoved effect {
+            pump_fault = 0;
+        };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:617dbf8693564862d10b289eba06b8c4f3f81a9a808229d51e613c6268ef8ede`。
  - SL-10 evidence 1: `{"summary": "The two SL-9 accepted requests address the same SD-4 design issue: pump_fault was read by the required AutocontrolNormal-to-PumpFault guard but was never written. The candidate adds meaningful NL-grounded writes: Manual.enter clears pump_fault to 0, AutocontrolNormal -> AutocontrolNormal :: PumpFaultDetected sets pump_fault = 1, and PumpFault -> Manual :: FaultRemoved clears pump_fault = 0. This resolves W_UNWRITTEN_READ_VAR and W_GUARD_VARS_NEVER_CHANGE without deleting pump_fault or replacing the required positive guard with a constant."}`
  - SL-10 evidence 2: `{"summary": "The repair is grounded in the NL: a pump fault such as tubing occlusion can occur, alarms activate, the caregiver removes the fault, and recovery returns to manual operation with software control released. The PumpFaultDetected self-transition represents observation of the fault occurrence while preserving the existing guarded fault-entry transition; FaultRemoved and Manual.enter clearing represent removal and recovery."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is narrowly scoped and improves on the previously rejected candidate. Instead of adding a second AutocontrolNormal -> PumpFault event transition that could obscure the required guarded transition, the current candidate uses an AutocontrolNormal self-transition to set pump_fault, leaving the single concrete fault-entry transition as AutocontrolNormal -> PumpFault : if [pump_fault > 0]. The candidate hash is new and not the previously rejected hash."}`
  - SL-10 evidence 4: `{"summary": "All NL-required states, variables, transitions, guards, and actions remain represented: Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault; CA_mode, software_control, pump_fault, alarm_signal, blood_pressure, target_blood_pressure, infusion_rate, flow_rate, pump_speed, built_in_switch, default_flow_rate, control_voltage, shared_buffer, log_count; InitiateAC, ChangeSetpoint, StartAC, TerminateAC, FaultRemoved, and CA/CB/CP/CC backManual recovery transitions. Manual pump commands, autocontrol rate computation, shared buffer writes, logging, alarm activation, and software-control release remain present."}`
  - SL-10 evidence 5: `{"summary": "No scenario regression is reported. The local deterministic rejection is limited to missing_required_grounding for action:set_target_blood_pressure and guard:pump_fault_positive, both of which are visibly present in the candidate DSL."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["action:set_target_blood_pressure", "guard:pump_fault_positive"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `1` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_change_setpoint_start_autocontrol, pump_fault_detected_then_alarm_state, fault_removed_returns_manual_and_clears_fault, terminate_ac_from_init_returns_manual, terminate_ac_from_normal_returns_manual, forced_backmanual_from_ask_and_init, forced_backmanual_from_normal_and_fault, atomic_startac_target_and_entry_effects, atomic_change_setpoint_effect_value, atomic_fault_detection_effect_and_guard_target, atomic_forced_backmanual_each_event, atomic_fault_removed_clears_exact_fault_flag, ... +2`。
- before_dsl_hash：`sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63`；candidate_dsl_hash：`sha256:a079cfeba8dad62d9eebafabd0d4dbd560bd5f622a0c5534ba7a5cbc79f0c49d`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：
- 7. `<unknown>` `` policy=``：
- 8. `<unknown>` `` policy=``：
- ……另有 `6` 条 evidence 见 run record。

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-4b80740816b`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-84b72ce8c3` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init probe: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC into AutocontrolInit, then reaches normal autocontrol.', 'name': 'initiate_change_setpoint_start_autocontrol', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init probe: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC into AutocontrolInit, then reaches normal autocontrol.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'shared_buffer': 80.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'CA_mode': 0, 'shared_buffer': 80.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'initiate_enters_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'blood_pressure': 80.0, 'control_voltage': 3.2, 'log_count': 0, 'setpoint': 95.0}, 'scenario_name': 'initiate_change_setpoint_start_autocontrol', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 80.0, 'built_in_switch': 0.0, 'control_voltage': 3.2, 'default_flow_rate': 0.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 95.0, 'shared_buffer': 80.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'dispatch_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 80.0, 'built_in_switch': 0.0, 'control_voltage': 3.2, 'default_flow_rate': 0.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 95.0, 'shared_buffer': 80.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'initiate_enters_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-1-b5cb7c375e` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: fault occurrence during normal autocontrol records pump_fault, then the positive fault condition enters PumpFault and releases software control.', 'name': 'pump_fault_detected_then_alarm_state', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: fault occurrence during normal autocontrol records pump_fault, then the positive fault condition enters PumpFault and releases software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'shared_buffer': 0.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'expected_vars': {'flow_rate': 20.0, 'infusion_rate': 20.0, 'log_count': 1, 'pump_fault': 1, 'shared_buffer': 90.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_detected_sets_fault_flag', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 90.0, 'control_voltage': 2.0, 'log_count': 0, 'pump_fault': 0, 'software_control': 1, 'target_blood_pressure': 110.0}, 'scenario_name': 'pump_fault_detected_then_alarm_state', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 90.0, 'built_in_switch': 0.0, 'control_voltage': 2.0, 'default_flow_rate': 0.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 0.0, 'shared_buffer': 0.0, 'software_control': 1, 'target_blood_pressure': 110.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_detected_sets_fault_flag', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-2-66435c0136` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: caregiver removes a pump fault, causing recovery to Manual with pump fault cleared and manual commands restored.', 'name': 'fault_removed_returns_manual_and_clears_fault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: caregiver removes a pump fault, causing recovery to Manual with pump fault cleared and manual commands restored.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'flow_rate': 0.0, 'pump_fault': 1, 'pump_speed': 0.0, 'shared_buffer': 0.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.FaultRemoved'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'flow_rate': 3.5, 'pump_fault': 0, 'pump_speed': 1.8, 'shared_buffer': 76.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.FaultRemoved', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_removed_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 76.0, 'built_in_switch': 1.8, 'default_flow_rate': 3.5, 'pump_fault': 1, 'software_control': 0}, 'scenario_name': 'fault_removed_returns_manual_and_clears_fault', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 76.0, 'built_in_switch': 1.8, 'control_voltage': 0.0, 'default_flow_rate': 3.5, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 0.0, 'setpoint': 0.0, 'shared_buffer': 0.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_removed_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-3-33babb71b1` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: caregiver termination during AutocontrolInit should return to Manual and release software control.', 'name': 'terminate_ac_from_init_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: caregiver termination during AutocontrolInit should return to Manual and release software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'flow_rate': 0.0, 'pump_fault': 0, 'pump_speed': 0.0, 'shared_buffer': 0.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'flow_rate': 5.0, 'pump_fault': 0, 'pump_speed': 2.2, 'shared_buffer': 70.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolInit.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Terminate", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_init_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 70.0, 'built_in_switch': 2.2, 'default_flow_rate': 5.0, 'pump_fault': 0, 'software_control': 1}, 'scenario_name': 'terminate_ac_from_init_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 70.0, 'built_in_switch': 2.2, 'control_voltage': 0.0, 'default_flow_rate': 5.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 0.0, 'shared_buffer': 0.0, 'software_control': 1, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolInit.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Terminate", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_init_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-4-df06be3fd5` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: caregiver termination during normal autocontrol should return to Manual and restore manual pump commands.', 'name': 'terminate_ac_from_normal_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: caregiver termination during normal autocontrol should return to Manual and restore manual pump commands.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'flow_rate': 0.0, 'pump_fault': 0, 'pump_speed': 0.0, 'shared_buffer': 0.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'flow_rate': 4.4, 'pump_fault': 0, 'pump_speed': 2.7, 'shared_buffer': 88.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Termina", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_normal_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 88.0, 'built_in_switch': 2.7, 'default_flow_rate': 4.4, 'pump_fault': 0, 'software_control': 1}, 'scenario_name': 'terminate_ac_from_normal_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 88.0, 'built_in_switch': 2.7, 'control_voltage': 0.0, 'default_flow_rate': 4.4, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 0.0, 'shared_buffer': 0.0, 'software_control': 1, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Termina", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_normal_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-5-8ba2140fd2` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init probe: cross-component backManual events from Ask_StartAC and AutocontrolInit should force the shared recovery target Manual.', 'name': 'forced_backmanual_from_ask_and_init', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init probe: cross-component backManual events from Ask_StartAC and AutocontrolInit should force the shared recovery target Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'shared_buffer': 84.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'shared_buffer': 84.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'enter_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'blood_pressure': 84.0, 'built_in_switch': 1.5, 'control_voltage': 6.0, 'default_flow_rate': 3.0}, 'scenario_name': 'forced_backmanual_from_ask_and_init', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 84.0, 'built_in_switch': 1.5, 'control_voltage': 6.0, 'default_flow_rate': 3.0, 'flow_rate': 3.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 1.5, 'setpoint': 0.0, 'shared_buffer': 84.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'dispatch_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 84.0, 'built_in_switch': 1.5, 'control_voltage': 6.0, 'default_flow_rate': 3.0, 'flow_rate': 3.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 1.5, 'setpoint': 0.0, 'shared_buffer': 84.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'enter_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-6-8641853111` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: CA_backManual from normal autocontrol and CP_backManual from PumpFault both force Manual as the recovery target.', 'name': 'forced_backmanual_from_normal_and_fault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: CA_backManual from normal autocontrol and CP_backManual from PumpFault both force Manual as the recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'shared_buffer': 91.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'shared_buffer': 91.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'initiate_again', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 91.0, 'built_in_switch': 2.0, 'control_voltage': 5.5, 'default_flow_rate': 4.8, 'log_count': 0, 'pump_fault': 0, 'software_control': 1, 'target_blood_pressure': 120.0}, 'scenario_name': 'forced_backmanual_from_normal_and_fault', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 91.0, 'built_in_switch': 2.0, 'control_voltage': 5.5, 'default_flow_rate': 4.8, 'flow_rate': 4.8, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 2.0, 'setpoint': 0.0, 'shared_buffer': 91.0, 'software_control': 0, 'target_blood_pressure': 120.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'ca_backmanual_forces_manual_from_normal', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 91.0, 'built_in_switch': 2.0, 'control_voltage': 5.5, 'default_flow_rate': 4.8, 'flow_rate': 4.8, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 2.0, 'setpoint': 0.0, 'shared_buffer': 91.0, 'software_control': 0, 'target_blood_pressure': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'initiate_again', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-7-99991315e0` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: from Ask_StartAC, StartAC must target AutocontrolInit exactly and apply autocontrol entry command effects.', 'name': 'atomic_startac_target_and_entry_effects', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: from Ask_StartAC, StartAC must target AutocontrolInit exactly and apply autocontrol entry command effects.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'log_count': 0, 'pump_speed': 0.0, 'shared_buffer': 0.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'alarm_signal': 0, 'log_count': 1, 'pump_speed': 7.25, 'shared_buffer': 87.0, 'software_control': 1}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'startac_exact_init_target', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 87.0, 'control_voltage': 7.25, 'log_count': 0, 'software_control': 0}, 'scenario_name': 'atomic_startac_target_and_entry_effects', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 87.0, 'built_in_switch': 0.0, 'control_voltage': 7.25, 'default_flow_rate': 0.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 0.0, 'shared_buffer': 0.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'startac_exact_init_target', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-8-fa28f205da` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: ChangeSetpoint must remain in Ask_StartAC and copy the caregiver setpoint into target_blood_pressure exactly.', 'name': 'atomic_change_setpoint_effect_value', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: ChangeSetpoint must remain in Ask_StartAC and copy the caregiver setpoint into target_blood_pressure exactly.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'shared_buffer': 0.0, 'target_blood_pressure': 60.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.ChangeSetpoint'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'shared_buffer': 79.0, 'target_blood_pressure': 123.5}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.ChangeSetpoint', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'change_setpoint_exact_copy', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'blood_pressure': 79.0, 'setpoint': 123.5, 'target_blood_pressure': 60.0}, 'scenario_name': 'atomic_change_setpoint_effect_value', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 79.0, 'built_in_switch': 0.0, 'control_voltage': 0.0, 'default_flow_rate': 0.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 123.5, 'shared_buffer': 0.0, 'software_control': 0, 'target_blood_pressure': 60.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'change_setpoint_exact_copy', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-9-8a06e4dcc3` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: PumpFaultDetected must set pump_fault to 1, and the next guard cycle must target PumpFault with alarm/release outputs.', 'name': 'atomic_fault_detection_effect_and_guard_target', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: PumpFaultDetected must set pump_fault to 1, and the next guard cycle must target PumpFault with alarm/release outputs.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'shared_buffer': 0.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'expected_vars': {'flow_rate': 38.0, 'infusion_rate': 38.0, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 4.0, 'shared_buffer': 92.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'pumpfaultdetected_sets_exact_flag', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 92.0, 'control_voltage': 4.0, 'log_count': 0, 'pump_fault': 0, 'software_control': 1, 'target_blood_pressure': 130.0}, 'scenario_name': 'atomic_fault_detection_effect_and_guard_target', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 92.0, 'built_in_switch': 0.0, 'control_voltage': 4.0, 'default_flow_rate': 0.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 0.0, 'shared_buffer': 0.0, 'software_control': 1, 'target_blood_pressure': 130.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'pumpfaultdetected_sets_exact_flag', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
- ……另有 `2` 个 request 见 run record。

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:blood_pressure, variable:target_blood_pressure, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2879`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-84b72ce8c3` | `accept` | ❌ | ❌ | The initiate_change_setpoint_start_autocontrol scenario failed because the injected parent-scoped event CARA.Mode_Control_Algorithm.InitiateAC did not resolve against a local Manual.InitiateAC event. The caregiver command is NL-grounded as a Mode_Control_Algorithm-level command, so changing the ordinary caregiver-command transitions to chain-scope parent eve...<truncated 176 chars> |
| `fixreq-1-sd6-1-b5cb7c375e` | `accept` | ❌ | ❌ | The pump_fault_detected_then_alarm_state scenario failed because CARA.Mode_Control_Algorithm.PumpFaultDetected did not resolve. PumpFaultDetected represents a mode-control-level observed pump complication, so the self-transition is changed to parent event scope while preserving the pump_fault write and normal autocontrol during actions.；intent=Make PumpFault...<truncated 87 chars> |
| `fixreq-1-sd6-2-66435c0136` | `accept` | ❌ | ❌ | The fault_removed_returns_manual_and_clears_fault scenario failed because CARA.Mode_Control_Algorithm.FaultRemoved did not resolve from PumpFault. FaultRemoved is an NL-grounded caregiver recovery command in the mode-control hierarchy, so it is changed to parent event scope while preserving the transition effect clearing pump_fault and Manual recovery action...<truncated 100 chars> |
| `fixreq-1-sd6-3-33babb71b1` | `accept` | ❌ | ❌ | The terminate_ac_from_init_returns_manual scenario failed because CARA.Mode_Control_Algorithm.TerminateAC did not resolve from AutocontrolInit. TerminateAC is a caregiver command shared by autocontrol states, so parent event scope is appropriate and preserves the required Manual recovery target.；intent=Make AutocontrolInit -> Manual TerminateAC parent-scoped |
| `fixreq-1-sd6-4-df06be3fd5` | `accept` | ❌ | ❌ | The terminate_ac_from_normal_returns_manual scenario failed for the same unresolved parent-scoped TerminateAC event from AutocontrolNormal. The repair makes the shared termination command visible at Mode_Control_Algorithm scope without changing recovery actions.；intent=Make AutocontrolNormal -> Manual TerminateAC parent-scoped |
| `fixreq-1-sd6-5-8ba2140fd2` | `accept` | ❌ | ❌ | The forced_backmanual_from_ask_and_init scenario failed while trying to re-enter Ask_StartAC via CARA.Mode_Control_Algorithm.InitiateAC. The repair fixes InitiateAC event visibility while leaving the existing forced backManual transitions intact.；intent=Repair InitiateAC parent-scope visibility and preserve forced backManual recovery |
| `fixreq-1-sd6-6-8641853111` | `accept` | ❌ | ❌ | The forced_backmanual_from_normal_and_fault scenario passed the CA_backManual recovery but failed on the subsequent parent-scoped InitiateAC event. The repair fixes InitiateAC visibility and does not alter the passing forced backManual behavior.；intent=Repair InitiateAC parent-scope visibility after Manual recovery |
| `fixreq-1-sd6-7-99991315e0` | `accept` | ❌ | ❌ | The atomic_startac_target_and_entry_effects scenario failed because CARA.Mode_Control_Algorithm.StartAC did not resolve from Ask_StartAC. StartAC is explicitly an Ask_StartAC caregiver command in the NL, and parent event scope matches the test event while preserving the exact AutocontrolInit target and entry effects.；intent=Make StartAC parent-scoped and pre...<truncated 35 chars> |
| `fixreq-1-sd6-8-fa28f205da` | `accept` | ❌ | ❌ | The atomic_change_setpoint_effect_value scenario failed because CARA.Mode_Control_Algorithm.ChangeSetpoint did not resolve from Ask_StartAC. The repair makes ChangeSetpoint parent-scoped and preserves the concrete action target_blood_pressure = setpoint, addressing the repair_memory grounding objection for action:set_target_blood_pressure.；intent=Make Change...<truncated 64 chars> |
| `fixreq-1-sd6-9-8a06e4dcc3` | `accept` | ❌ | ❌ | The atomic_fault_detection_effect_and_guard_target scenario failed because the parent-scoped PumpFaultDetected event did not resolve. The repair makes the event visible, keeps the self-transition effect pump_fault = 1, and preserves the required guarded AutocontrolNormal -> PumpFault : if [pump_fault > 0] transition, addressing the repair_memory grounding ob...<truncated 125 chars> |
| `fixreq-1-sd6-10-ec972d3007` | `accept` | ❌ | ❌ | The atomic_forced_backmanual_each_event scenario passed the first forced recovery and failed while re-entering Ask_StartAC with parent-scoped InitiateAC. The repair fixes that re-entry event without changing the forced CA/CB/CP/CC backManual declarations.；intent=Repair InitiateAC parent-scope visibility and preserve all forced backManual events |
| `fixreq-1-sd6-11-3b2dfc2561` | `accept` | ❌ | ❌ | The atomic_fault_removed_clears_exact_fault_flag scenario failed because CARA.Mode_Control_Algorithm.FaultRemoved did not resolve. The repair makes FaultRemoved parent-scoped and preserves pump_fault = 0 before Manual entry/during recovery outputs run.；intent=Make FaultRemoved parent-scoped and preserve exact pump_fault clearing |
- repair_rationale：Primary repair target: all failing SD-6 steps report SimulationRuntimeEventError for fully qualified parent events such as CARA.Mode_Control_Algorithm.InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, and FaultRemoved. Th...<truncated 82 chars>；Smallest safe edit: change only the ordinary caregiver/fault event transitions from local scope (:: Event) to Mode_Control_Algorithm parent scope (: Event). This makes the injected paths resolve while preserving targets, guards, effects, st...<truncated 67 chars>；initiate_change_setpoint_start_autocontrol and the backManual re-entry probes now allow InitiateAC to move Manual to Ask_StartAC, ChangeSetpoint to keep Ask_StartAC while setting target_blood_pressure = setpoint, StartAC to enter Autocontro...<truncated 67 chars>；pump_fault_detected_then_alarm_state and atomic_fault_detection_effect_and_guard_target now allow PumpFaultDetected to set pump_fault = 1 on the AutocontrolNormal self-transition; the required guard AutocontrolNormal -> PumpFault : if [pump...<truncated 61 chars>；terminate_ac_from_init_returns_manual and terminate_ac_from_normal_returns_manual now resolve the shared TerminateAC event from both autocontrol states and return to Manual, where Manual.enter and Manual.during release software control and ...<truncated 29 chars>
- diff_summary：`{"summary": "Changed ordinary caregiver/fault event transitions InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, and FaultRemoved from local :: events to Mode_Control_Algorithm parent-scope : events so the failing fully qualified scenario events resolve. Preserved all states, variables, Manual recovery actions, ChangeSetpoint target_blood_pressure = setpoint action, PumpFaultDetected pump_fault write, the pump_fault_positive guard, and forced backManual transitions."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int log_count = 0;
def float built_in_switch = 0.0;
def float default_flow_rate = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float blood_pressure = 0.0;
def float target_blood_pressure = 0.0;
def float setpoint = 0.0;
def float infusion_rate = 0.0;
def float flow_rate = 0.0;
def float shared_buffer = 0.0;

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
                alarm_signal = 0;
                pump_fault = 0;
            }
            during {
                shared_buffer = blood_pressure;
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
            during {
                shared_buffer = blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                pump_speed = control_voltage;
            }
            during {
                shared_buffer = blood_pressure;
                log_count = log_count + 1;
            }
        }

        state AutocontrolNormal {
            during {
                shared_buffer = blood_pressure;
                infusion_rate = target_blood_pressure - blood_pressure;
                flow_rate = infusion_rate;
                pump_speed = control_voltage;
                log_count = log_count + 1;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
            during {
                shared_buffer = blood_pressure;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
            target_blood_pressure = setpoint;
        };
        Ask_StartAC -> AutocontrolInit : StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolInit -> Manual : TerminateAC;
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> AutocontrolNormal : PumpFaultDetected effect {
            pump_fault = 1;
        };
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual : FaultRemoved effect {
            pump_fault = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -83,19 +83,19 @@
             }
         }
 
-        Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
+        Manual -> Ask_StartAC : InitiateAC;
+        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
             target_blood_pressure = setpoint;
         };
-        Ask_StartAC -> AutocontrolInit :: StartAC;
+        Ask_StartAC -> AutocontrolInit : StartAC;
         AutocontrolInit -> AutocontrolNormal;
-        AutocontrolInit -> Manual :: TerminateAC;
-        AutocontrolNormal -> Manual :: TerminateAC;
-        AutocontrolNormal -> AutocontrolNormal :: PumpFaultDetected effect {
+        AutocontrolInit -> Manual : TerminateAC;
+        AutocontrolNormal -> Manual : TerminateAC;
+        AutocontrolNormal -> AutocontrolNormal : PumpFaultDetected effect {
             pump_fault = 1;
         };
         AutocontrolNormal -> PumpFault : if [pump_fault > 0];
-        PumpFault -> Manual :: FaultRemoved effect {
+        PumpFault -> Manual : FaultRemoved effect {
             pump_fault = 0;
         };
     }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:d27ac5fc0174fb37090154b828dc116a1fdcabeb3957c05835d69a5615756379`。
  - SL-10 evidence 1: `{"summary": "The candidate correctly addresses the dominant SD-6 unresolved-event-path failures by changing InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, and FaultRemoved from local `::` events to Mode_Control_Algorithm-scoped `:` events, which is grounded in the NL because these are caregiver/fault commands in the Mode_Control_Algorithm hierarchy."}`
  - SL-10 evidence 2: `{"summary": "However, local deterministic evidence reports a hard scenario regression: 18 of 19 scenarios now pass, but `terminate_ac_from_init_returns_manual` fails. From initial state `CARA.Mode_Control_Algorithm.AutocontrolInit` with `software_control=1`, `CA_mode=1`, `blood_pressure=70.0`, `built_in_switch=2.2`, and `default_flow_rate=5.0`, dispatching `CARA.Mode_Control_Algorithm.TerminateAC` was expected to enter `CARA.Mode_Control_Algorithm.Manual` with `CA_mode=0`, `software_control=0`, `alarm_signal=0`, `pump_fault=0`, `shared_buffer=70.0`, `pump_speed=2.2`, and `flow_rate=5.0`. Actual state was `CARA.Mode_Control_Algorithm.AutocontrolNormal` with `CA_mode=1`, `software_control=1`, ...<truncated 218 chars>`
  - SL-10 evidence 3: `{"summary": "The likely DSL mechanism is transition priority/order or event handling in `AutocontrolInit`: the unguarded `AutocontrolInit -> AutocontrolNormal;` transition is being taken instead of the parent-scoped `AutocontrolInit -> Manual : TerminateAC;` during the TerminateAC step. The repair cannot be accepted until TerminateAC from AutocontrolInit preempts or otherwise blocks the unguarded initialization-completion transition when the caregiver termination event is present."}`
  - SL-10 evidence 4: `{"summary": "The complete FixLog and repair_memory also require preserving the previously repaired grounding for `action:set_target_blood_pressure` and `guard:pump_fault_positive`. The candidate still visibly contains `target_blood_pressure = setpoint;` on ChangeSetpoint and `AutocontrolNormal -> PumpFault : if [pump_fault > 0];`, but local evidence continues to report `missing_required_grounding` for those IDs. Since this review requests rework for an actual scenario regression, the next SL-9 pass should both fix the TerminateAC regression and keep an explicit rationale mapping these concrete DSL lines to the required grounding IDs."}`
- SL-10 rework_instructions：Fix `terminate_ac_from_init_returns_manual`: dispatching `CARA.Mode_Control_Algorithm.TerminateAC` from hot-start state `CARA.Mode_Control_Algorithm.AutocontrolInit` must transition to `CARA.Mode_Control_Algorithm.Manual`, not to `AutocontrolNormal`. Ensure Manual entry/during recovery then yields `CA_mode=0`, `software_control=0`, `alarm_signal=0`, `pump_fa...<truncated 104 chars>；Make the DSL event/transition mechanism ensure `AutocontrolInit -> Manual : TerminateAC` has priority over or is not bypassed by the unguarded `AutocontrolInit -> AutocontrolNormal;` transition when the TerminateAC event is injected. A minimal likely edit is to place the `AutocontrolInit -> Manual : TerminateAC` transition before the unguarded `AutocontrolIn...<truncated 229 chars>；Preserve the parent-scoped event visibility repairs for `InitiateAC`, `ChangeSetpoint`, `StartAC`, `TerminateAC`, `PumpFaultDetected`, and `FaultRemoved`, because those resolved the prior unresolved-event-path failures.；Preserve the NL-required concrete grounding for `action:set_target_blood_pressure` as `Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_blood_pressure = setpoint; }` and for `guard:pump_fault_positive` as `AutocontrolNormal -> PumpFault : if [pump_fault > 0];`. In the next SL-9 rationale, explicitly map these lines to the local missing-required-gr...<truncated 96 chars>；Do not delete required states, variables, forced backManual transitions, Manual recovery outputs, PumpFaultDetected `pump_fault = 1`, FaultRemoved `pump_fault = 0`, alarm/software-control release behavior, shared-buffer updates, or the monotonic infusion-rate computation.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 19, "n_scenarios_passed": 18, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init probe: first runtime cycle should dispatch into Manual and apply manual pump-speed, default-flow, shared-buffer, and recovery outputs.", "name": "default_init_manual_mode_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0...<truncated 30386 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["action:set_target_blood_pressure", "guard:pump_fault_positive"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `1` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_change_setpoint_start_autocontrol, pump_fault_detected_then_alarm_state, fault_removed_returns_manual_and_clears_fault, terminate_ac_from_init_returns_manual, terminate_ac_from_normal_returns_manual, forced_backmanual_from_ask_and_init, forced_backmanual_from_normal_and_fault, atomic_startac_target_and_entry_effects, atomic_change_setpoint_effect_value, atomic_fault_detection_effect_and_guard_target, atomic_forced_backmanual_each_event, atomic_fault_removed_clears_exact_fault_flag, ... +2`。
- before_dsl_hash：`sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63`；candidate_dsl_hash：`sha256:ee24d33cefd4c6a306c51cba43096280ff0d137f9dad2ee9e56a34647b35b3a3`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：
- 7. `<unknown>` `` policy=``：
- 8. `<unknown>` `` policy=``：
- ……另有 `6` 条 evidence 见 run record。

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-4b80740816b`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-84b72ce8c3` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init probe: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC into AutocontrolInit, then reaches normal autocontrol.', 'name': 'initiate_change_setpoint_start_autocontrol', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init probe: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC into AutocontrolInit, then reaches normal autocontrol.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'shared_buffer': 80.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'CA_mode': 0, 'shared_buffer': 80.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'initiate_enters_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'blood_pressure': 80.0, 'control_voltage': 3.2, 'log_count': 0, 'setpoint': 95.0}, 'scenario_name': 'initiate_change_setpoint_start_autocontrol', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 80.0, 'built_in_switch': 0.0, 'control_voltage': 3.2, 'default_flow_rate': 0.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 95.0, 'shared_buffer': 80.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'dispatch_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 80.0, 'built_in_switch': 0.0, 'control_voltage': 3.2, 'default_flow_rate': 0.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 95.0, 'shared_buffer': 80.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'initiate_enters_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-1-b5cb7c375e` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: fault occurrence during normal autocontrol records pump_fault, then the positive fault condition enters PumpFault and releases software control.', 'name': 'pump_fault_detected_then_alarm_state', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: fault occurrence during normal autocontrol records pump_fault, then the positive fault condition enters PumpFault and releases software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'shared_buffer': 0.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'expected_vars': {'flow_rate': 20.0, 'infusion_rate': 20.0, 'log_count': 1, 'pump_fault': 1, 'shared_buffer': 90.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_detected_sets_fault_flag', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 90.0, 'control_voltage': 2.0, 'log_count': 0, 'pump_fault': 0, 'software_control': 1, 'target_blood_pressure': 110.0}, 'scenario_name': 'pump_fault_detected_then_alarm_state', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 90.0, 'built_in_switch': 0.0, 'control_voltage': 2.0, 'default_flow_rate': 0.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 0.0, 'shared_buffer': 0.0, 'software_control': 1, 'target_blood_pressure': 110.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_detected_sets_fault_flag', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-2-66435c0136` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: caregiver removes a pump fault, causing recovery to Manual with pump fault cleared and manual commands restored.', 'name': 'fault_removed_returns_manual_and_clears_fault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: caregiver removes a pump fault, causing recovery to Manual with pump fault cleared and manual commands restored.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'flow_rate': 0.0, 'pump_fault': 1, 'pump_speed': 0.0, 'shared_buffer': 0.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.FaultRemoved'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'flow_rate': 3.5, 'pump_fault': 0, 'pump_speed': 1.8, 'shared_buffer': 76.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.FaultRemoved', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_removed_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 76.0, 'built_in_switch': 1.8, 'default_flow_rate': 3.5, 'pump_fault': 1, 'software_control': 0}, 'scenario_name': 'fault_removed_returns_manual_and_clears_fault', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 76.0, 'built_in_switch': 1.8, 'control_voltage': 0.0, 'default_flow_rate': 3.5, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 0.0, 'setpoint': 0.0, 'shared_buffer': 0.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_removed_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-3-33babb71b1` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: caregiver termination during AutocontrolInit should return to Manual and release software control.', 'name': 'terminate_ac_from_init_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: caregiver termination during AutocontrolInit should return to Manual and release software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'flow_rate': 0.0, 'pump_fault': 0, 'pump_speed': 0.0, 'shared_buffer': 0.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'flow_rate': 5.0, 'pump_fault': 0, 'pump_speed': 2.2, 'shared_buffer': 70.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolInit.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Terminate", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_init_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 70.0, 'built_in_switch': 2.2, 'default_flow_rate': 5.0, 'pump_fault': 0, 'software_control': 1}, 'scenario_name': 'terminate_ac_from_init_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 70.0, 'built_in_switch': 2.2, 'control_voltage': 0.0, 'default_flow_rate': 5.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 0.0, 'shared_buffer': 0.0, 'software_control': 1, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolInit.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Terminate", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_init_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-4-df06be3fd5` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: caregiver termination during normal autocontrol should return to Manual and restore manual pump commands.', 'name': 'terminate_ac_from_normal_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: caregiver termination during normal autocontrol should return to Manual and restore manual pump commands.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'flow_rate': 0.0, 'pump_fault': 0, 'pump_speed': 0.0, 'shared_buffer': 0.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'flow_rate': 4.4, 'pump_fault': 0, 'pump_speed': 2.7, 'shared_buffer': 88.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Termina", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_normal_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 88.0, 'built_in_switch': 2.7, 'default_flow_rate': 4.4, 'pump_fault': 0, 'software_control': 1}, 'scenario_name': 'terminate_ac_from_normal_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 88.0, 'built_in_switch': 2.7, 'control_voltage': 0.0, 'default_flow_rate': 4.4, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 0.0, 'shared_buffer': 0.0, 'software_control': 1, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Termina", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_normal_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-5-8ba2140fd2` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init probe: cross-component backManual events from Ask_StartAC and AutocontrolInit should force the shared recovery target Manual.', 'name': 'forced_backmanual_from_ask_and_init', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init probe: cross-component backManual events from Ask_StartAC and AutocontrolInit should force the shared recovery target Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'shared_buffer': 84.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'shared_buffer': 84.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'enter_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'blood_pressure': 84.0, 'built_in_switch': 1.5, 'control_voltage': 6.0, 'default_flow_rate': 3.0}, 'scenario_name': 'forced_backmanual_from_ask_and_init', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 84.0, 'built_in_switch': 1.5, 'control_voltage': 6.0, 'default_flow_rate': 3.0, 'flow_rate': 3.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 1.5, 'setpoint': 0.0, 'shared_buffer': 84.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'dispatch_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 84.0, 'built_in_switch': 1.5, 'control_voltage': 6.0, 'default_flow_rate': 3.0, 'flow_rate': 3.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 1.5, 'setpoint': 0.0, 'shared_buffer': 84.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'enter_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-6-8641853111` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: CA_backManual from normal autocontrol and CP_backManual from PumpFault both force Manual as the recovery target.', 'name': 'forced_backmanual_from_normal_and_fault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: CA_backManual from normal autocontrol and CP_backManual from PumpFault both force Manual as the recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'shared_buffer': 91.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'shared_buffer': 91.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'initiate_again', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 91.0, 'built_in_switch': 2.0, 'control_voltage': 5.5, 'default_flow_rate': 4.8, 'log_count': 0, 'pump_fault': 0, 'software_control': 1, 'target_blood_pressure': 120.0}, 'scenario_name': 'forced_backmanual_from_normal_and_fault', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 91.0, 'built_in_switch': 2.0, 'control_voltage': 5.5, 'default_flow_rate': 4.8, 'flow_rate': 4.8, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 2.0, 'setpoint': 0.0, 'shared_buffer': 91.0, 'software_control': 0, 'target_blood_pressure': 120.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'ca_backmanual_forces_manual_from_normal', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 91.0, 'built_in_switch': 2.0, 'control_voltage': 5.5, 'default_flow_rate': 4.8, 'flow_rate': 4.8, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 2.0, 'setpoint': 0.0, 'shared_buffer': 91.0, 'software_control': 0, 'target_blood_pressure': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'initiate_again', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-7-99991315e0` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: from Ask_StartAC, StartAC must target AutocontrolInit exactly and apply autocontrol entry command effects.', 'name': 'atomic_startac_target_and_entry_effects', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: from Ask_StartAC, StartAC must target AutocontrolInit exactly and apply autocontrol entry command effects.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'log_count': 0, 'pump_speed': 0.0, 'shared_buffer': 0.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'alarm_signal': 0, 'log_count': 1, 'pump_speed': 7.25, 'shared_buffer': 87.0, 'software_control': 1}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'startac_exact_init_target', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 87.0, 'control_voltage': 7.25, 'log_count': 0, 'software_control': 0}, 'scenario_name': 'atomic_startac_target_and_entry_effects', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 87.0, 'built_in_switch': 0.0, 'control_voltage': 7.25, 'default_flow_rate': 0.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 0.0, 'shared_buffer': 0.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'startac_exact_init_target', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-8-fa28f205da` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: ChangeSetpoint must remain in Ask_StartAC and copy the caregiver setpoint into target_blood_pressure exactly.', 'name': 'atomic_change_setpoint_effect_value', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: ChangeSetpoint must remain in Ask_StartAC and copy the caregiver setpoint into target_blood_pressure exactly.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'shared_buffer': 0.0, 'target_blood_pressure': 60.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.ChangeSetpoint'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'shared_buffer': 79.0, 'target_blood_pressure': 123.5}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.ChangeSetpoint', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'change_setpoint_exact_copy', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'blood_pressure': 79.0, 'setpoint': 123.5, 'target_blood_pressure': 60.0}, 'scenario_name': 'atomic_change_setpoint_effect_value', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 79.0, 'built_in_switch': 0.0, 'control_voltage': 0.0, 'default_flow_rate': 0.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 123.5, 'shared_buffer': 0.0, 'software_control': 0, 'target_blood_pressure': 60.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'change_setpoint_exact_copy', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-9-8a06e4dcc3` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: PumpFaultDetected must set pump_fault to 1, and the next guard cycle must target PumpFault with alarm/release outputs.', 'name': 'atomic_fault_detection_effect_and_guard_target', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: PumpFaultDetected must set pump_fault to 1, and the next guard cycle must target PumpFault with alarm/release outputs.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'shared_buffer': 0.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'expected_vars': {'flow_rate': 38.0, 'infusion_rate': 38.0, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 4.0, 'shared_buffer': 92.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'pumpfaultdetected_sets_exact_flag', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 92.0, 'control_voltage': 4.0, 'log_count': 0, 'pump_fault': 0, 'software_control': 1, 'target_blood_pressure': 130.0}, 'scenario_name': 'atomic_fault_detection_effect_and_guard_target', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 92.0, 'built_in_switch': 0.0, 'control_voltage': 4.0, 'default_flow_rate': 0.0, 'flow_rate': 0.0, 'infusion_rate': 0.0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'setpoint': 0.0, 'shared_buffer': 0.0, 'software_control': 1, 'target_blood_pressure': 130.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'pumpfaultdetected_sets_exact_flag', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
- ……另有 `2` 个 request 见 run record。

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:blood_pressure, variable:target_blood_pressure, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2879`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-84b72ce8c3` | `accept` | ❌ | ✅ | Accepted: InitiateAC, ChangeSetpoint, and StartAC are NL-grounded caregiver/mode-control commands and must be visible as Mode_Control_Algorithm-scoped events for the scenario path.；intent=Use parent-scope event transitions for InitiateAC, ChangeSetpoint, and StartAC |
| `fixreq-1-sd6-1-b5cb7c375e` | `accept` | ❌ | ✅ | Accepted: PumpFaultDetected is an observed pump-operation complication in normal autocontrol and must resolve as a Mode_Control_Algorithm-scoped event while preserving the pump_fault write and the guarded PumpFault entry.；intent=Use parent-scope PumpFaultDetected self-transition and preserve pump_fault = 1 |
| `fixreq-1-sd6-2-66435c0136` | `accept` | ❌ | ✅ | Accepted: FaultRemoved is the caregiver recovery command after a pump fault and must resolve from PumpFault while clearing pump_fault and entering Manual recovery.；intent=Use parent-scope FaultRemoved transition and preserve pump_fault clearing |
| `fixreq-1-sd6-3-33babb71b1` | `accept` | ❌ | ✅ | Accepted: repair_memory identifies terminate_ac_from_init_returns_manual as the current regression. The TerminateAC transition from AutocontrolInit must preempt the unguarded initialization-complete transition.；intent=Place AutocontrolInit -> Manual : TerminateAC before AutocontrolInit -> AutocontrolNormal |
| `fixreq-1-sd6-4-df06be3fd5` | `accept` | ❌ | ✅ | Accepted: TerminateAC from AutocontrolNormal is a shared caregiver termination command and remains parent-scoped to restore Manual operation.；intent=Use parent-scope TerminateAC from AutocontrolNormal to Manual |
| `fixreq-1-sd6-5-8ba2140fd2` | `accept` | ❌ | ✅ | Accepted: preserve passing backManual behavior while keeping InitiateAC visible for re-entry into Ask_StartAC.；intent=Preserve forced backManual transitions and parent-scope InitiateAC |
| `fixreq-1-sd6-6-8641853111` | `accept` | ❌ | ✅ | Accepted: preserve forced recovery from normal/fault states and keep the repaired InitiateAC event visibility after Manual recovery.；intent=Preserve forced backManual behavior and parent-scope re-entry events |
| `fixreq-1-sd6-7-99991315e0` | `accept` | ❌ | ✅ | Accepted: StartAC must target AutocontrolInit exactly and AutocontrolInit entry/during actions must apply autocontrol effects.；intent=Use parent-scope StartAC to AutocontrolInit and preserve entry/during effects |
| `fixreq-1-sd6-8-fa28f205da` | `accept` | ❌ | ✅ | Accepted: ChangeSetpoint must remain in Ask_StartAC and copy setpoint into target_blood_pressure. This explicitly preserves action:set_target_blood_pressure.；intent=Preserve Ask_StartAC self-transition effect target_blood_pressure = setpoint |
| `fixreq-1-sd6-9-8a06e4dcc3` | `accept` | ❌ | ✅ | Accepted: PumpFaultDetected must set pump_fault to 1, and the separate positive guard must remain the concrete PumpFault entry. This explicitly preserves guard:pump_fault_positive.；intent=Preserve PumpFaultDetected pump_fault write and AutocontrolNormal -> PumpFault : if [pump_fault > 0] |
| `fixreq-1-sd6-10-ec972d3007` | `accept` | ❌ | ✅ | Accepted: all named cross-component backManual forced events must be preserved while repaired parent-scoped events support re-entry probes.；intent=Preserve CA/CB/CP/CC backManual forced transitions |
| `fixreq-1-sd6-11-3b2dfc2561` | `accept` | ❌ | ✅ | Accepted: FaultRemoved must target Manual and clear pump_fault before Manual recovery outputs run.；intent=Preserve FaultRemoved effect pump_fault = 0 and Manual recovery actions |
- repair_rationale：Primary repair target from repair_memory: terminate_ac_from_init_returns_manual expected TerminateAC from hot-start AutocontrolInit to enter Manual with CA_mode=0, software_control=0, pump_fault=0, alarm_signal=0, shared_buffer=blood_pressu...<truncated 333 chars>；The previously successful parent-scoped event visibility repair is preserved for InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, and FaultRemoved; this avoids regressing the unresolved-event-path scenarios that were alr...<truncated 13 chars>；The local missing_required_grounding objection for action:set_target_blood_pressure is addressed by the concrete line Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_blood_pressure = setpoint; }, which directly implements the NL...<truncated 83 chars>；The local missing_required_grounding objection for guard:pump_fault_positive is addressed by the concrete line AutocontrolNormal -> PumpFault : if [pump_fault > 0];, which remains the guarded transition into PumpFault after PumpFaultDetecte...<truncated 22 chars>；No required states, variables, Manual recovery outputs, forced CA/CB/CP/CC backManual transitions, PumpFaultDetected pump_fault write, FaultRemoved pump_fault clear, alarm/software-control release behavior, shared-buffer updates, or infusio...<truncated 32 chars>
- diff_summary：`{"summary": "Kept the parent-scoped Mode_Control_Algorithm events from the prior repair and made the minimal rework edit requested by repair_memory: moved/placed AutocontrolInit -> Manual : TerminateAC before the unguarded AutocontrolInit -> AutocontrolNormal transition so TerminateAC from AutocontrolInit recovers to Manual instead of advancing to AutocontrolNormal. Preserved ChangeSetpoint target_blood_pressure = setpoint and the pump_fault_positive guard."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int log_count = 0;
def float built_in_switch = 0.0;
def float default_flow_rate = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float blood_pressure = 0.0;
def float target_blood_pressure = 0.0;
def float setpoint = 0.0;
def float infusion_rate = 0.0;
def float flow_rate = 0.0;
def float shared_buffer = 0.0;

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
                alarm_signal = 0;
                pump_fault = 0;
            }
            during {
                shared_buffer = blood_pressure;
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
            during {
                shared_buffer = blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                pump_speed = control_voltage;
            }
            during {
                shared_buffer = blood_pressure;
                log_count = log_count + 1;
            }
        }

        state AutocontrolNormal {
            during {
                shared_buffer = blood_pressure;
                infusion_rate = target_blood_pressure - blood_pressure;
                flow_rate = infusion_rate;
                pump_speed = control_voltage;
                log_count = log_count + 1;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
            during {
                shared_buffer = blood_pressure;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
            target_blood_pressure = setpoint;
        };
        Ask_StartAC -> AutocontrolInit : StartAC;
        AutocontrolInit -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> AutocontrolNormal : PumpFaultDetected effect {
            pump_fault = 1;
        };
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual : FaultRemoved effect {
            pump_fault = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -83,19 +83,19 @@
             }
         }
 
-        Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
+        Manual -> Ask_StartAC : InitiateAC;
+        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
             target_blood_pressure = setpoint;
         };
-        Ask_StartAC -> AutocontrolInit :: StartAC;
+        Ask_StartAC -> AutocontrolInit : StartAC;
+        AutocontrolInit -> Manual : TerminateAC;
         AutocontrolInit -> AutocontrolNormal;
-        AutocontrolInit -> Manual :: TerminateAC;
-        AutocontrolNormal -> Manual :: TerminateAC;
-        AutocontrolNormal -> AutocontrolNormal :: PumpFaultDetected effect {
+        AutocontrolNormal -> Manual : TerminateAC;
+        AutocontrolNormal -> AutocontrolNormal : PumpFaultDetected effect {
             pump_fault = 1;
         };
         AutocontrolNormal -> PumpFault : if [pump_fault > 0];
-        PumpFault -> Manual :: FaultRemoved effect {
+        PumpFault -> Manual : FaultRemoved effect {
             pump_fault = 0;
         };
     }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:75871c592a7430db7f5c4c357f5807c25bd1c5eade05d5278ebf1df2ff1e6f9c`。
  - SL-10 evidence 1: `{"summary": "The candidate implements the SL-9 accepted repair intents for all 12 locked requests: caregiver/fault events InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, and FaultRemoved are Mode_Control_Algorithm-scoped using ':' so the previously failing fully qualified scenario events can resolve from Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault."}`
  - SL-10 evidence 2: `{"summary": "The candidate directly addresses the repair_memory regression for terminate_ac_from_init_returns_manual by placing `AutocontrolInit -> Manual : TerminateAC;` before the unguarded `AutocontrolInit -> AutocontrolNormal;`. This is the DSL-actionable priority/order edit requested by SL-10: a TerminateAC event hot-started in AutocontrolInit should recover to Manual instead of being bypassed by initialization completion."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves the Manual recovery obligations from the NL and FixLog: Manual entry clears CA_mode/software_control/alarm_signal/pump_fault, and Manual during writes shared_buffer=blood_pressure, pump_speed=built_in_switch, and flow_rate=default_flow_rate. Thus TerminateAC, FaultRemoved, and CA/CB/CP/CC backManual recover to the shared Manual target required by the NL."}`
  - SL-10 evidence 4: `{"summary": "The candidate preserves all NL-required mode-control states and variables: Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault; CA_mode, software_control, pump_fault, alarm_signal, blood_pressure, target_blood_pressure, infusion_rate, flow_rate, pump_speed, built_in_switch, default_flow_rate, control_voltage, shared_buffer, and log_count."}`
  - SL-10 evidence 5: `{"summary": "The candidate preserves autocontrol behavior required by the NL: StartAC enters AutocontrolInit; AutocontrolInit/AutocontrolNormal set software control and pump speed from control_voltage; AutocontrolNormal computes infusion_rate and flow_rate as target_blood_pressure - blood_pressure, so higher pressure gives lower flow rate; shared_buffer and log_count are updated during autocontrol."}`
  - SL-10 evidence 6: `{"summary": "The candidate preserves pump fault handling from the NL and prior FixLog: PumpFaultDetected in AutocontrolNormal sets pump_fault=1; the separate guarded transition `AutocontrolNormal -> PumpFault : if [pump_fault > 0];` remains the concrete PumpFault entry; PumpFault entry activates alarm_signal and releases software control; FaultRemoved clears pump_fault and returns to Manual."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["action:set_target_blood_pressure", "guard:pump_fault_positive"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-120a1d24192` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-120a1d24192` | accept=2, reject=0 | `sl10_review` | `sha256:ee75f9b6f572d19faae19a0550300c64df2254d41a6031cc0bb8ee6c440c8d16` | Accepted both design repair requests because the selected diagnostics identify the same root issue: pump_fault was read in the required fault guard but was never written., The repair preserves the required guard [pump_fault > 0] and the required AutocontrolNormal -> PumpFault transition instead of replacing them with a constant or deleting the fault branch., The added PumpFaultDetected event is grounded in the NL statement that a pump fault such as tubing occlusion can occur; its effect records that occurrence by setting pump_fault = 1., ... +2 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-120a1d24192` | accept=2, reject=0 | `sl9_rework` | `sha256:ee75f9b6f572d19faae19a0550300c64df2254d41a6031cc0bb8ee6c440c8d16` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling., repair_memory:SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., ... +10 |
| 4 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-120a1d24192` | accept=2, reject=0 | `sl10_review` | `sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63` | Both accepted requests address the same root design warning: pump_fault was read by the required AutocontrolNormal-to-PumpFault guard but was never written by any action/effect., The repair uses the NL-grounded event PumpFaultDetected to represent occurrence of a pump fault such as tubing occlusion. It records that occurrence by setting pump_fault = 1 while CARA remains in AutocontrolNormal; the already-required guard then routes to PumpFault when pump_fault > 0., The required guard:pump_fault_positive is explicitly preserved as `AutocontrolNormal -> PumpFault : if [pump_fault > 0];`. This avoids deleting or replacing the required guarded fault transition and avoids mixing event and guard on the same transition., ... +6 |
| 5 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-120a1d24192` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:3d3419eeddd77f91e940999a2aae1ec708a42f4ef4a1b1cfb02f335fe51a6f63` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +6 |
| 6 | `1` | `request_batch` | `fixbatch-1-sha256-4b80740816b` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 7 | `1` | `sl9_decision` | `fixbatch-1-sha256-4b80740816b` | accept=12, reject=0 | `sl10_review` | `sha256:a079cfeba8dad62d9eebafabd0d4dbd560bd5f622a0c5534ba7a5cbc79f0c49d` | Primary repair target: all failing SD-6 steps report SimulationRuntimeEventError for fully qualified parent events such as CARA.Mode_Control_Algorithm.InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, and FaultRemoved. The actual states and variables stayed unchanged because the events did not resolve., Smallest safe edit: change only the ordinary caregiver/fault event transitions from local scope (:: Event) to Mode_Control_Algorithm parent scope (: Event). This makes the injected paths resolve while preserving targets, guards, effects, state bodies, variables, and forced backManual recovery declarations., initiate_change_setpoint_start_autocontrol and the backManual re-entry probes now allow InitiateAC to move Manual to Ask_StartAC, ChangeSetpoint to keep Ask_StartAC while setting target_blood_pressure = setpoint, StartAC to enter AutocontrolInit, and the existing bare transition to reach AutocontrolNormal., ... +6 |
| 8 | `1` | `sl10_review` | `fixbatch-1-sha256-4b80740816b` | accept=12, reject=0 | `sl9_rework` | `sha256:a079cfeba8dad62d9eebafabd0d4dbd560bd5f622a0c5534ba7a5cbc79f0c49d` | Fix `terminate_ac_from_init_returns_manual`: dispatching `CARA.Mode_Control_Algorithm.TerminateAC` from hot-start state `CARA.Mode_Control_Algorithm.AutocontrolInit` must transition to `CARA.Mode_Control_Algorithm.Manual`, not to `AutocontrolNormal`. Ensure Manual entry/during recovery then yields `CA_mode=0`, `software_control=0`, `alarm_signal=0`, `pump_fault=0`, `shared_buffer=blood_pressure`, `pump_speed=built_in_switch`, and `flow_rate=default_flow_rate`., Make the DSL event/transition mechanism ensure `AutocontrolInit -> Manual : TerminateAC` has priority over or is not bypassed by the unguarded `AutocontrolInit -> AutocontrolNormal;` transition when the TerminateAC event is injected. A minimal likely edit is to place the `AutocontrolInit -> Manual : TerminateAC` transition before the unguarded `AutocontrolInit -> AutocontrolNormal;`, if this DSL uses declaration order for transition selection; otherwise add the smallest DSL-supported guard/structure that prevents the unguarded completion transition from consuming a TerminateAC step., Preserve the parent-scoped event visibility repairs for `InitiateAC`, `ChangeSetpoint`, `StartAC`, `TerminateAC`, `PumpFaultDetected`, and `FaultRemoved`, because those resolved the prior unresolved-event-path failures., ... +16 |
| 9 | `1` | `sl9_rework_decision` | `fixbatch-1-sha256-4b80740816b` | accept=12, reject=0 | `sl10_review` | `sha256:ee24d33cefd4c6a306c51cba43096280ff0d137f9dad2ee9e56a34647b35b3a3` | Primary repair target from repair_memory: terminate_ac_from_init_returns_manual expected TerminateAC from hot-start AutocontrolInit to enter Manual with CA_mode=0, software_control=0, pump_fault=0, alarm_signal=0, shared_buffer=blood_pressure, pump_speed=built_in_switch, and flow_rate=default_flow_rate; the previous candidate instead took the unguarded AutocontrolInit -> AutocontrolNormal path. The smallest DSL edit is to declare AutocontrolInit -> Manual : TerminateAC before the unguarded completion transition so event handling can preempt initialization completion., The previously successful parent-scoped event visibility repair is preserved for InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, and FaultRemoved; this avoids regressing the unresolved-event-path scenarios that were already passing., The local missing_required_grounding objection for action:set_target_blood_pressure is addressed by the concrete line Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_blood_pressure = setpoint; }, which directly implements the NL obligation that the caregiver can modify target blood pressure within Ask_StartAC., ... +3 |
| 10 | `1` | `sl10_rework_review` | `fixbatch-1-sha256-4b80740816b` | accept=12, reject=0 | `sc11_accept_then_sd2` | `sha256:ee24d33cefd4c6a306c51cba43096280ff0d137f9dad2ee9e56a34647b35b3a3` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +7 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4493, 'completion_chars': 18066, 'completion_tokens': 5910, 'elapsed_seconds': 109.1333190749865, 'estimated_completion_tokens': 4517, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11174, 'first_chunk_seconds': 30.578674755990505, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12360}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1246, 'completion_chars': 5319, 'completion_tokens': 1765, 'elapsed_seconds': 35.3248105780076, 'estimated_completion_tokens': 1330, 'estimated_prompt_tokens': 27437, 'estimated_total_tokens': 28767, 'first_chunk_seconds': 13.27697343401087, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 109748, 'prompt_tokens': 24935, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26700}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 750, 'completion_chars': 3602, 'completion_tokens': 936, 'elapsed_seconds': 20.1551998359937, 'estimated_completion_tokens': 901, 'estimated_prompt_tokens': 25465, 'estimated_total_tokens': 26366, 'first_chunk_seconds': 6.896660889004124, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 101858, 'prompt_tokens': 22261, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23197}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1631, 'completion_chars': 7232, 'completion_tokens': 2081, 'elapsed_seconds': 41.3181880050106, 'estimated_completion_tokens': 1808, 'estimated_prompt_tokens': 55373, 'estimated_total_tokens': 57181, 'first_chunk_seconds': 12.07075978400826, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 221491, 'prompt_tokens': 48943, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 51024}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1010, 'completion_chars': 4894, 'completion_tokens': 1235, 'elapsed_seconds': 25.187028212007135, 'estimated_completion_tokens': 1224, 'estimated_prompt_tokens': 56029, 'estimated_total_tokens': 57253, 'first_chunk_seconds': 6.954983895004261, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 224115, 'prompt_tokens': 48349, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 49584}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3937, 'completion_chars': 15903, 'completion_tokens': 5492, 'elapsed_seconds': 101.1196717940038, 'estimated_completion_tokens': 3976, 'estimated_prompt_tokens': 16020, 'estimated_total_tokens': 19996, 'first_chunk_seconds': 31.573215926997364, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 64079, 'prompt_tokens': 15587, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21079}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6073, 'completion_chars': 24533, 'completion_tokens': 6373, 'elapsed_seconds': 117.0964773070009, 'estimated_completion_tokens': 6134, 'estimated_prompt_tokens': 20231, 'estimated_total_tokens': 26365, 'first_chunk_seconds': 8.071898812995641, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 80922, 'prompt_tokens': 19723, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26096}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4829, 'completion_chars': 18950, 'completion_tokens': 5575, 'elapsed_seconds': 103.22624217199336, 'estimated_completion_tokens': 4738, 'estimated_prompt_tokens': 22388, 'estimated_total_tokens': 27126, 'first_chunk_seconds': 17.089039325990598, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 89552, 'prompt_tokens': 21859, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 27434}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2925, 'completion_chars': 12787, 'completion_tokens': 3802, 'elapsed_seconds': 71.12880392000079, 'estimated_completion_tokens': 3197, 'estimated_prompt_tokens': 42657, 'estimated_total_tokens': 45854, 'first_chunk_seconds': 18.368827283004066, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 170628, 'prompt_tokens': 39675, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 43477}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1106, 'completion_chars': 4730, 'completion_tokens': 1576, 'elapsed_seconds': 30.95186242600903, 'estimated_completion_tokens': 1183, 'estimated_prompt_tokens': 38342, 'estimated_total_tokens': 39525, 'first_chunk_seconds': 11.390804203998414, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 153366, 'prompt_tokens': 35694, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 37270}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2466, 'completion_chars': 10260, 'completion_tokens': 2862, 'elapsed_seconds': 56.25545091199456, 'estimated_completion_tokens': 2565, 'estimated_prompt_tokens': 160828, 'estimated_total_tokens': 163393, 'first_chunk_seconds': 11.422121347000939, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 643312, 'prompt_tokens': 137575, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 140437}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1031, 'completion_chars': 4820, 'completion_tokens': 1226, 'elapsed_seconds': 25.482767449997482, 'estimated_completion_tokens': 1205, 'estimated_prompt_tokens': 93669, 'estimated_total_tokens': 94874, 'first_chunk_seconds': 7.320748290003394, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 374673, 'prompt_tokens': 86860, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 88086}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 677, 'completion_chars': 2761, 'completion_tokens': 1196, 'elapsed_seconds': 37.17206855099357, 'estimated_completion_tokens': 691, 'estimated_prompt_tokens': 24287, 'estimated_total_tokens': 24978, 'first_chunk_seconds': 13.12688183899445, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 97148, 'prompt_tokens': 23745, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24941}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3305, 'completion_chars': 13275, 'completion_tokens': 5349, 'elapsed_seconds': 98.87618478199875, 'estimated_completion_tokens': 3319, 'estimated_prompt_tokens': 18162, 'estimated_total_tokens': 21481, 'first_chunk_seconds': 39.29266275600821, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 72645, 'prompt_tokens': 17656, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23005}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1824, 'completion_chars': 8911, 'completion_tokens': 2343, 'elapsed_seconds': 44.87427679299435, 'estimated_completion_tokens': 2228, 'estimated_prompt_tokens': 21072, 'estimated_total_tokens': 23300, 'first_chunk_seconds': 11.984220197002287, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 84287, 'prompt_tokens': 20992, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23335}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success_but_weak_oracle_ineligible`。
- required stages executed：`41/16`，missing=`<none>`。
- repairs：`2/4` accepted；scenario_history=`6`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
