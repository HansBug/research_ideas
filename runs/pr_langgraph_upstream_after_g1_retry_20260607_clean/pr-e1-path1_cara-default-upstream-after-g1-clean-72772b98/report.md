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
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `min_sl10_rework_attempts=1`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `84bdbbb87edaa0c9265f72e429ee95a0578993d1` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:e0d83a90e0bc0b26d3205dd82c250301d3787ea358564f23754fe4929a3ce867", "iteration": 3, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:bceb828a382a28ab702e9cfcc4529aec920eb9078d90fb26b856cb7702f2c9d4", "iteration": 0, "repair_history_index": 1, "rework_instructions": ["Keep the intended behavioral repair, but replace the parse-invalid line `Ask_StartAC.SetpointEditing -> AutocontrolInit : /Mode_Control_Algorithm.Ask_StartAC.StartAC;`. The local parser does not accept dotted state-source qualification at `Ask_StartAC.`.", "Do not return to the old composite-only `Ask_StartAC -> AutocontrolInit :: StartAC;` behavior if it reintroduces the hot-start scenario failure. The semantic requirement remains: active leaf `CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing` receiving the NL-grounded `StartAC` event must transition to `CARA.Mode_Control_Algorithm.AutocontrolInit`.", "Use a DSL-supported hierarchical transition form that avoids the invalid dotted source syntax. Prefer moving the transition into the `Ask_StartAC` scope and qualifying only the target with a parser-supported parent/absolute target form, or use whatever pyfcstm-supported path syntax exists for nested leaf source and sibling target; do not use `Ask_StartAC.SetpointEditing` if `.` is not accepted by the parser.", "Preserve `AutocontrolInit.enter` exactly so step 0 of `start_ac_to_normal_high_pressure_control` reaches AutocontrolInit with CA_mode=1, software_control=1, control_released=0, pump_speed_source=1, alarm_display=0, and alarm_sound=0.", "Preserve `AutocontrolInit -> NormalAutocontrol;` and `NormalAutocontrol.during` exactly so step 1 reaches NormalAutocontrol with sensor_buffer_bp=130.0, infusion_rate=1.0, pump_flow_rate=1.0, control_voltage=1.0, and log_records=1 for blood_pressure=130.0 and target_blood_pressure=100.0.", "Preserve all other NL-required elements and previously passing behavior, especially `Manual -> Ask_StartAC :: InitiateAC;`, `SetpointEditing -> SetpointEditing :: ChangeSetpoint`, the four forced `CA_backManual`, `CB_backManual`, `CP_backManual`, `CC_backManual` transitions to Manual, and `Manual.enter` recovery assignments."], "same_as_final": false, "sl10_decision": "rework"}, "matching_repair_history_indices": [5], "repair_history_index": 5, "selected_source_stage": "SD-6", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, ... +4` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 865250, 'completion_tokens': 59983, 'total_tokens': 925233, 'estimated_prompt_tokens': 961185, 'estimated_completion_tokens': 45927, 'estimated_total_tokens': 1007112, 'prompt_chars': 3844696, 'completion_chars': 183688, 'n_calls': 22, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`1179.38s` |
| run record | [`pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz`](./pr-e1-path1_cara-default-upstream-after-g1-clean-72772b98.agent_loop.json.gz) |
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

### 4. 全流程真实摘要表

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
| 6 | `2026-06-07T03:16:13Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 7 | `2026-06-07T03:16:13Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=3065,hash=sha256:e9f6dfced3e9 |
| 8 | `2026-06-07T03:16:13Z` | `SL-1` | `-` | `lg_d2_envelope_exit` | {} | <none> |
| 9 | `2026-06-07T03:16:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 10 | `2026-06-07T03:16:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-07T03:16:13Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:e9f6dfced3e99f9838ec259677a665c8096fb74c8d4e326b55f12a7e5768bc56 |
| 12 | `2026-06-07T03:16:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-07T03:16:13Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=3065,hash=sha256:e9f6dfced3e9, current_hash=sha256:e9f6dfced3e99f9838ec259677a665c8096fb74c8d4e326b55f12a7e5768bc56 |
| 14 | `2026-06-07T03:16:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 15 | `2026-06-07T03:16:13Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 16 | `2026-06-07T03:16:13Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-07T03:16:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 18 | `2026-06-07T03:16:13Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 19 | `2026-06-07T03:16:13Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-07T03:16:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 21 | `2026-06-07T03:16:13Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 22 | `2026-06-07T03:16:13Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-07T03:16:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-07T03:16:13Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 25 | `2026-06-07T03:16:13Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 26 | `2026-06-07T03:17:15Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 27 | `2026-06-07T03:17:15Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 28 | `2026-06-07T03:17:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-07T03:17:15Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 30 | `2026-06-07T03:17:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-07T03:17:15Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 32 | `2026-06-07T03:17:15Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 33 | `2026-06-07T03:18:21Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-07T03:18:21Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 35 | `2026-06-07T03:18:21Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 36 | `2026-06-07T03:18:22Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 37 | `2026-06-07T03:18:22Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 38 | `2026-06-07T03:18:22Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 39 | `2026-06-07T03:18:22Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 40 | `2026-06-07T03:19:41Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 41 | `2026-06-07T03:19:41Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 42 | `2026-06-07T03:19:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-07T03:19:41Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 44 | `2026-06-07T03:19:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-07T03:19:41Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 46 | `2026-06-07T03:19:41Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 47 | `2026-06-07T03:19:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-07T03:19:41Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 49 | `2026-06-07T03:19:42Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 50 | `2026-06-07T03:19:42Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 51 | `2026-06-07T03:19:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 52 | `2026-06-07T03:19:42Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 12, "n_scenarios_passed": 11, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 53 | `2026-06-07T03:19:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 54 | `2026-06-07T03:19:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 55 | `2026-06-07T03:19:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 56 | `2026-06-07T03:19:42Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 12, "n_scenarios_passed": 11, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=3065,hash=sha256:e9f6dfced3e9 |
| 57 | `2026-06-07T03:19:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 58 | `2026-06-07T03:19:42Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 59 | `2026-06-07T03:19:42Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 60 | `2026-06-07T03:19:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 61 | `2026-06-07T03:19:42Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=3065,hash=sha256:e9f6dfced3e9 |
| 62 | `2026-06-07T03:19:42Z` | `SL-9` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 63 | `2026-06-07T03:20:39Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 64 | `2026-06-07T03:20:39Z` | `SL-9` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 65 | `2026-06-07T03:20:39Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-70b23a1aa0"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=3072,hash=sha256:a46b4d58c6ff |
| 66 | `2026-06-07T03:20:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 67 | `2026-06-07T03:20:39Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 68 | `2026-06-07T03:20:39Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:a46b4d58c6ffd22203d6ed11462c086ca21576d26457b9edc3edda21fd3601b5 |
| 69 | `2026-06-07T03:20:39Z` | `SL-10` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 70 | `2026-06-07T03:21:06Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 71 | `2026-06-07T03:21:06Z` | `SL-10` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 72 | `2026-06-07T03:21:06Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 73 | `2026-06-07T03:21:06Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 74 | `2026-06-07T03:21:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 75 | `2026-06-07T03:21:06Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=3065,hash=sha256:e9f6dfced3e9 |
| 76 | `2026-06-07T03:21:06Z` | `SL-9` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 77 | `2026-06-07T03:21:51Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 78 | `2026-06-07T03:21:51Z` | `SL-9` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 79 | `2026-06-07T03:21:51Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-70b23a1aa0"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=3116,hash=sha256:bceb828a382a |
| 80 | `2026-06-07T03:21:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
- ……另有 `255` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-6` | yes | fixbatch-0-sha256-8bd9f01c6cc / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SL-7` | yes | fixbatch-1-sha256-452f95f7b7d / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=minor, local_stage=SD-10, reason=scenario_regression | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SD-6` | yes | fixbatch-2-sha256-83f4e7b3696 / n=1 | accept=1, reject=0, waiver=0 | ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `SD-6` | yes | fixbatch-3-sha256-83f4e7b3696 / n=1 | accept=1, reject=0, waiver=0 | ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 4 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

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

#### 6.2 Scenario definitions

<details><summary>`default_init_enters_manual_mode` — default-init: first empty cycle should dispatch to Manual and apply manual pump-switch/default-flow obligations.</summary>

| Field | Value |
|---|---|
| description | default-init: first empty cycle should dispatch to Manual and apply manual pump-switch/default-flow obligations. |
| initial_state | `<default-init>` |
| initial_vars | `{"manual_default_flow_rate": 1.5}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_after_initial_dispatch` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 0, "alarm_sound": 0, "control_released": 1, "pump_flow_rate": 1.5, "pump_speed_source": 0, "software_control": 0}` |

</details>

<details><summary>`initiate_ac_change_setpoint_then_cp_fallback` — default-init: caregiver initiates AC, edits setpoint in Ask_StartAC, then CP_backManual forces shared Manual recovery.</summary>

| Field | Value |
|---|---|
| description | default-init: caregiver initiates AC, edits setpoint in Ask_StartAC, then CP_backManual forces shared Manual recovery. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 95.0, "manual_default_flow_rate": 1.8, "requested_target_blood_pressure": 110.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_ready` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "pump_flow_rate": 1.8}` |
| 1 `entered_setpoint_editing` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing` | `{"sensor_buffer_bp": 95.0}` |
| 2 `setpoint_changed` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing` | `{"sensor_buffer_bp": 95.0, "target_blood_pressure": 110.0}` |
| 3 `cp_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 0, "alarm_sound": 0, "control_released": 1, "pump_flow_rate": 1.8, "pump_speed_source": 0, "software_control": 0}` |

</details>

<details><summary>`start_ac_to_normal_high_pressure_control` — explicit-hot-start: pressing StartAC from SetpointEditing enters AutocontrolInit, then normal autocontrol uses high BP to lower flow and log data.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: pressing StartAC from SetpointEditing enters AutocontrolInit, then normal autocontrol uses high BP to lower flow and log data. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing` |
| initial_vars | `{"CA_mode": 0, "blood_pressure": 130.0, "control_released": 1, "log_records": 0, "pump_speed_source": 0, "software_control": 0, "target_blood_pressure": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `start_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_display": 0, "alarm_sound": 0, "control_released": 0, "pump_speed_source": 1, "software_control": 1}` |
| 1 `normal_autocontrol_high_pressure_lower_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.NormalAutocontrol` | `{"control_released": 0, "control_voltage": 1.0, "infusion_rate": 1.0, "log_records": 1, "pump_flow_rate": 1.0, "pump_speed_source": 1, "sensor_buffer_bp": 130.0, "software_control": 1}` |
| 2 `ca_forces_manual_from_normal` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 0, "alarm_sound": 0, "control_released": 1, "pump_speed_source": 0, "software_control": 0}` |

</details>

<details><summary>`normal_autocontrol_low_pressure_then_terminate` — explicit-hot-start: with no fault event NormalAutocontrol stays active and lower BP produces higher flow, then TerminateAC returns to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: with no fault event NormalAutocontrol stays active and lower BP produces higher flow, then TerminateAC returns to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.NormalAutocontrol` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 80.0, "control_released": 0, "log_records": 5, "manual_default_flow_rate": 2.5, "pump_speed_source": 1, "software_control": 1, "target_blood_pressure": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `stays_normal_and_controls_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.NormalAutocontrol` | `{"control_released": 0, "control_voltage": 2.0, "infusion_rate": 2.0, "log_records": 6, "pump_flow_rate": 2.0, "pump_speed_source": 1, "sensor_buffer_bp": 80.0, "software_control": 1}` |
| 1 `terminate_lands_manual` | `0` | `["CARA.Mode_Control_Algorithm.NormalAutocontrol.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 0, "alarm_sound": 0, "control_released": 1, "pump_flow_rate": 2.5, "pump_speed_source": 0, "software_control": 0}` |

</details>

<details><summary>`pump_fault_alarm_then_fault_removed_manual` — explicit-hot-start: pump fault during NormalAutocontrol activates alarms/releases control, then FaultRemoved returns to Manual with fault cleared.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: pump fault during NormalAutocontrol activates alarms/releases control, then FaultRemoved returns to Manual with fault cleared. |
| initial_state | `CARA.Mode_Control_Algorithm.NormalAutocontrol` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 125.0, "control_released": 0, "manual_default_flow_rate": 1.75, "pump_speed_source": 1, "software_control": 1, "target_blood_pressure": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_enters_pump_fault` | `0` | `["CARA.Mode_Control_Algorithm.NormalAutocontrol.PumpFaultDetected"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_display": 1, "alarm_sound": 1, "control_released": 1, "pump_complication": 1, "pump_flow_rate": 1.75, "pump_speed_source": 0, "software_control": 0}` |
| 1 `fault_removed_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 0, "alarm_sound": 0, "control_released": 1, "pump_complication": 0, "pump_flow_rate": 1.75, "pump_speed_source": 0, "software_control": 0}` |

</details>

<details><summary>`cb_backmanual_forces_manual_from_pump_fault` — explicit-hot-start: CB_backManual is a cross-component fallback to Manual, but an active uncleared pump fault should not be silently treated as fault removed.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CB_backManual is a cross-component fallback to Manual, but an active uncleared pump fault should not be silently treated as fault removed. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 0, "alarm_display": 1, "alarm_sound": 1, "control_released": 1, "manual_default_flow_rate": 3.0, "pump_complication": 1, "pump_speed_source": 0, "software_control": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_forces_manual_preserving_active_fault_alarm` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 1, "alarm_sound": 1, "control_released": 1, "pump_complication": 1, "pump_flow_rate": 3.0, "pump_speed_source": 0, "software_control": 0}` |

</details>

<details><summary>`cc_backmanual_forces_manual_from_autocontrol_init` — explicit-hot-start: CC_backManual should force AutocontrolInit to Manual rather than continuing toward NormalAutocontrol.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CC_backManual should force AutocontrolInit to Manual rather than continuing toward NormalAutocontrol. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "control_released": 0, "manual_default_flow_rate": 2.0, "pump_speed_source": 1, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 0, "alarm_sound": 0, "control_released": 1, "pump_flow_rate": 2.0, "pump_speed_source": 0, "software_control": 0}` |

</details>

<details><summary>`manual_initiate_ac_wrong_target_probe` — explicit-hot-start: InitiateAC from Manual must enter Ask_StartAC.SetpointEditing, catching wrong-target mutations of the initiation transition.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: InitiateAC from Manual must enter Ask_StartAC.SetpointEditing, catching wrong-target mutations of the initiation transition. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"CA_mode": 0, "blood_pressure": 102.0, "control_released": 1, "manual_default_flow_rate": 1.25, "pump_speed_source": 0, "software_control": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiate_ac_lands_in_setpoint_editing` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing` | `{"sensor_buffer_bp": 102.0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-6` | start_ac_to_normal_high_pressure_control | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=False, drift=major, rework=Keep the intended behavioral repair, but rewrite the StartAC transition with valid DSL scoping. Do not leave `SetpointEditing -> AutocontrolInit : StartAC;` inside `state Ask_...<truncated 523 chars> | `sha256:a46b4d58c6ffd22203d6ed11462c086ca21576d26457b9edc3edda21fd3601b5` |
| 2 | `0` | ❌ | `SD-6` | start_ac_to_normal_high_pressure_control | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=False, drift=major, rework=Keep the intended behavioral repair, but replace the parse-invalid line `Ask_StartAC.SetpointEditing -> AutocontrolInit : /Mode_Control_Algorithm.Ask_StartAC.StartAC;`. The lo...<truncated 556 chars> | `sha256:bceb828a382a28ab702e9cfcc4529aec920eb9078d90fb26b856cb7702f2c9d4` |
| 3 | `0` | ✅ | `SD-6` | start_ac_to_normal_high_pressure_control | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift | `sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20` |
| 4 | `1` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=minor, local_stage=SD-10, reason=scenario_regression | `sha256:1fa9f2728307c12bbbd8bf5368b4d28ee0fd840319b42c295410a75c4904ad3d` |
| 5 | `2` | ✅ | `SD-6` | cb_backmanual_forces_manual_from_pump_fault | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20` |
| 6 | `3` | ✅ | `SD-6` | cb_backmanual_forces_manual_from_pump_fault | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:e0d83a90e0bc0b26d3205dd82c250301d3787ea358564f23754fe4929a3ce867` |

<details><summary>Repair 1 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`start_ac_to_normal_high_pressure_control`。
- before_dsl_hash：`sha256:e9f6dfced3e99f9838ec259677a665c8096fb74c8d4e326b55f12a7e5768bc56`；candidate_dsl_hash：`sha256:a46b4d58c6ffd22203d6ed11462c086ca21576d26457b9edc3edda21fd3601b5`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-8bd9f01c6cc`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-70b23a1aa0` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: pressing StartAC from SetpointEditing enters AutocontrolInit, then normal autocontrol uses high BP to lower flow and log data.', 'name': 'start_ac_to_normal_high_pressure_control', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: pressing StartAC from SetpointEditing enters AutocontrolInit, then normal autocontrol uses high BP to lower flow and log data.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'actual_vars_focus': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'control_released': 0, 'pump_speed_source': 0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'alarm_display': 0, 'alarm_sound': 0, 'control_released': 0, 'pump_speed_source': 1, 'software_control': 1}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'start_enters_autocontrol_init', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 0, 'expected': 1}, 'pump_speed_source': {'actual': 0, 'expected': 1}, 'software_control': {'actual': 0, 'expected': 1}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'actual_vars_focus': {'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'pump_flow_rate': 0.0, 'sensor_buffer_bp': 130.0}, 'before_cycles': 0, 'events': [], 'expected_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'expected_vars': {'control_voltage': 1.0, 'infusion_rate': 1.0, 'log_records': 1, 'pump_flow_rate': 1.0, 'sensor_buffer_bp': 130.0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 1, 'step_name': 'normal_autocontrol_high_pressure_lower_flow', 'var_assertion_ok': False, 'var_mismatches': {'control_voltage': {'actual': 0.0, 'expected': 1.0}, 'infusion_rate': {'actual': 0.0, 'expected': 1.0}, 'log_records': {'actual': 0, 'expected': 1}, 'pump_flow_rate': {'actual': 0.0, 'expected': 1.0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'initial_vars': {'blood_pressure': 130.0, 'log_records': 0, 'target_blood_pressure': 100.0}, 'scenario_name': 'start_ac_to_normal_high_pressure_control', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'actual_vars': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'blood_pressure': 130.0, 'control_released': 0, 'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'manual_default_flow_rate': 1.0, 'pump_complication': 0, 'pump_flow_rate': 0.0, 'pump_speed_source': 0, 'requested_target_blood_pressure': 100.0, 'sensor_buffer_bp': 130.0, 'software_control': 0, 'target_blood_pressure': 100.0}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'start_enters_autocontrol_init', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 0, 'expected': 1}, 'pump_speed_source': {'actual': 0, 'expected': 1}, 'software_control': {'actual': 0, 'expected': 1}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'actual_vars': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'blood_pressure': 130.0, 'control_released': 0, 'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'manual_default_flow_rate': 1.0, 'pump_complication': 0, 'pump_flow_rate': 0.0, 'pump_speed_source': 0, 'requested_target_blood_pressure': 100.0, 'sensor_buffer_bp': 130.0, 'software_control': 0, 'target_blood_pressure': 100.0}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 1, 'step_name': 'normal_autocontrol_high_pressure_lower_flow', 'var_assertion_ok': False, 'var_mismatches': {'control_voltage': {'actual': 0.0, 'expected': 1.0}, 'infusion_rate': {'actual': 0.0, 'expected': 1.0}, 'log_records': {'actual': 0, 'expected': 1}, 'pump_flow_rate': {'actual': 0.0, 'expected': 1.0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'blood_pressure': 130.0, 'control_released': 1, 'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'manual_default_flow_rate': 1.0, 'pump_complication': 0, 'pump_flow_rate': 1.0, 'pump_speed_source': 0, 'requested_target_blood_pressure': 100.0, 'sensor_buffer_bp': 130.0, 'software_control': 0, 'target_blood_pressure': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'ca_forces_manual_from_normal', 'var_assertion_ok': True, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, hierarchical_state:Ask_StartAC, state:SetpointEditing, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, event:InitiateAC, event:StartAC, event:ChangeSetpoint, event:TerminateAC, ... +35`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3072`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-70b23a1aa0` | `accept` | ❌ | ❌ | The failing scenario start_ac_to_normal_high_pressure_control shows that injecting CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC while the active leaf is Ask_StartAC.SetpointEditing does not fire the existing composite-scope Ask_StartAC -> AutocontrolInit :: StartAC transition. The smallest safe repair is to place the StartAC transition on the active leaf ...<truncated 408 chars> |
- repair_rationale：Accepted hard sim request fixreq-0-sd6-0-70b23a1aa0.；For scenario start_ac_to_normal_high_pressure_control step 0 start_enters_autocontrol_init, expected state was CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1, software_control=1, control_released=0, pump_speed_source=1, alarm_di...<truncated 323 chars>；For scenario start_ac_to_normal_high_pressure_control step 1 normal_autocontrol_high_pressure_lower_flow, expected state was NormalAutocontrol with sensor_buffer_bp=130.0, infusion_rate=1.0, pump_flow_rate=1.0, control_voltage=1.0, and log_...<truncated 315 chars>；The event is encoded as SetpointEditing -> AutocontrolInit : StartAC so the active leaf observes the NL-grounded Ask_StartAC.StartAC trigger from its enclosing Ask_StartAC scope, rather than leaving an unevaluated composite-source transitio...<truncated 2 chars>；The already passing ca_forces_manual_from_normal scenario is preserved: the four forced backManual transitions remain in Mode_Control_Algorithm and Manual.enter still restores manual operation variables.
- diff_summary：`{"summary": "Replaced the composite-source Ask_StartAC -> AutocontrolInit :: StartAC transition with a leaf-source SetpointEditing -> AutocontrolInit : StartAC transition inside Ask_StartAC, preserving the Ask_StartAC.StartAC event semantics while allowing the hot-start active leaf scenario to fire."}`。

#### SL-9 candidate / 最终修改执行方案

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

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_released = 1;
                pump_speed_source = 0;
                pump_flow_rate = manual_default_flow_rate;
                alarm_display = 0;
                alarm_sound = 0;
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
            SetpointEditing -> AutocontrolInit : StartAC;
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

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -50,6 +50,7 @@
             SetpointEditing -> SetpointEditing :: ChangeSetpoint effect {
                 target_blood_pressure = requested_target_blood_pressure;
             };
+            SetpointEditing -> AutocontrolInit : StartAC;
         }
 
         state AutocontrolInit {
@@ -91,7 +92,6 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> AutocontrolInit :: StartAC;
         AutocontrolInit -> NormalAutocontrol;
         NormalAutocontrol -> Manual :: TerminateAC;
         NormalAutocontrol -> PumpFault :: PumpFaultDetected;
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:a719cdd22cc7111ae1007f4696393f67734f4235c10a4d8693c97479ff850937`。
  - SL-10 evidence 1: `{"summary": "SL-9 correctly identified the NL/simulation obligation: pressing Ask_StartAC.StartAC from the active Ask_StartAC.SetpointEditing leaf must enter AutocontrolInit, whose enter action sets CA_mode=1, software_control=1, control_released=0, pump_speed_source=1, alarm_display=0, and alarm_sound=0; then the existing AutocontrolInit -> NormalAutocontrol transition and NormalAutocontrol.during should compute high-pressure lower flow with infusion_rate=1.0, pump_flow_rate=1.0, control_voltage=1.0, and log_records=1."}`
  - SL-10 evidence 2: `{"summary": "However, the candidate DSL is semantically invalid according to local deterministic evidence: E_DANGLING_TRANSITION reports that `SetpointEditing -> AutocontrolInit : StartAC;` is inside `Ask_StartAC`, where `AutocontrolInit` is not a child state, so the target cannot be resolved. Because the candidate cannot pass semantic validation, the hard simulation repair cannot be accepted for top-down revalidation."}`
  - SL-10 evidence 3: `{"summary": "The diff preserves required states, variables, actions, and forced backManual transitions in intent, but the StartAC repair must be expressed with valid state scoping. The current invalid inner transition also removed the old composite-source transition, so StartAC has no valid concrete transition representation in the accepted semantic model."}`
- SL-10 rework_instructions：Keep the intended behavioral repair, but rewrite the StartAC transition with valid DSL scoping. Do not leave `SetpointEditing -> AutocontrolInit : StartAC;` inside `state Ask_StartAC` unless the target is expressed in a DSL-supported qualified form.；Preferred minimal edit: place the leaf-source StartAC transition at the `Mode_Control_Algorithm` scope, alongside `Manual -> Ask_StartAC :: InitiateAC;`, using a qualified source path to the active leaf and sibling target, e.g. `Ask_StartAC.SetpointEditing -> AutocontrolInit :: StartAC;` if this is the DSL-supported syntax.；If the DSL requires another qualification form for nested leaf sources or parent/sibling targets, use that supported form, but the semantic result must be: active leaf `CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing` receiving the NL-grounded StartAC event transitions to `CARA.Mode_Control_Algorithm.AutocontrolInit`.；Preserve the existing `AutocontrolInit.enter` action and unguarded `AutocontrolInit -> NormalAutocontrol;` transition so the scenario `start_ac_to_normal_high_pressure_control` step 0 reaches AutocontrolInit with CA_mode=1, software_control=1, pump_speed_source=1, control_released=0, alarms off, and step 1 reaches NormalAutocontrol with sensor_buffer_bp=130....<truncated 81 chars>；Preserve all other NL-required elements and previously passing behavior, especially the four forced `CA_backManual`, `CB_backManual`, `CP_backManual`, and `CC_backManual` transitions to Manual and `Manual.enter` recovery assignments.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`candidate semantic failed`，rejected_by_stage=`SD-10`。
    - local evidence 1: `<unknown>` {"code": "E_DANGLING_TRANSITION", "message": "Unknown to state 'AutocontrolInit' of transition:\nSetpointEditing -> AutocontrolInit : StartAC;", "refs": {"reason": "tgt_not_found", "src": "SetpointEditing", "tgt": "AutocontrolInit"}, "severity": "error", "span": {"column": 13, "end_column": 58, "end_line": 53, "line": 53}}

</details>

<details><summary>Repair 2 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`start_ac_to_normal_high_pressure_control`。
- before_dsl_hash：`sha256:e9f6dfced3e99f9838ec259677a665c8096fb74c8d4e326b55f12a7e5768bc56`；candidate_dsl_hash：`sha256:bceb828a382a28ab702e9cfcc4529aec920eb9078d90fb26b856cb7702f2c9d4`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-8bd9f01c6cc`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-70b23a1aa0` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: pressing StartAC from SetpointEditing enters AutocontrolInit, then normal autocontrol uses high BP to lower flow and log data.', 'name': 'start_ac_to_normal_high_pressure_control', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: pressing StartAC from SetpointEditing enters AutocontrolInit, then normal autocontrol uses high BP to lower flow and log data.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'actual_vars_focus': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'control_released': 0, 'pump_speed_source': 0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'alarm_display': 0, 'alarm_sound': 0, 'control_released': 0, 'pump_speed_source': 1, 'software_control': 1}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'start_enters_autocontrol_init', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 0, 'expected': 1}, 'pump_speed_source': {'actual': 0, 'expected': 1}, 'software_control': {'actual': 0, 'expected': 1}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'actual_vars_focus': {'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'pump_flow_rate': 0.0, 'sensor_buffer_bp': 130.0}, 'before_cycles': 0, 'events': [], 'expected_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'expected_vars': {'control_voltage': 1.0, 'infusion_rate': 1.0, 'log_records': 1, 'pump_flow_rate': 1.0, 'sensor_buffer_bp': 130.0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 1, 'step_name': 'normal_autocontrol_high_pressure_lower_flow', 'var_assertion_ok': False, 'var_mismatches': {'control_voltage': {'actual': 0.0, 'expected': 1.0}, 'infusion_rate': {'actual': 0.0, 'expected': 1.0}, 'log_records': {'actual': 0, 'expected': 1}, 'pump_flow_rate': {'actual': 0.0, 'expected': 1.0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'initial_vars': {'blood_pressure': 130.0, 'log_records': 0, 'target_blood_pressure': 100.0}, 'scenario_name': 'start_ac_to_normal_high_pressure_control', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'actual_vars': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'blood_pressure': 130.0, 'control_released': 0, 'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'manual_default_flow_rate': 1.0, 'pump_complication': 0, 'pump_flow_rate': 0.0, 'pump_speed_source': 0, 'requested_target_blood_pressure': 100.0, 'sensor_buffer_bp': 130.0, 'software_control': 0, 'target_blood_pressure': 100.0}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'start_enters_autocontrol_init', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 0, 'expected': 1}, 'pump_speed_source': {'actual': 0, 'expected': 1}, 'software_control': {'actual': 0, 'expected': 1}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'actual_vars': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'blood_pressure': 130.0, 'control_released': 0, 'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'manual_default_flow_rate': 1.0, 'pump_complication': 0, 'pump_flow_rate': 0.0, 'pump_speed_source': 0, 'requested_target_blood_pressure': 100.0, 'sensor_buffer_bp': 130.0, 'software_control': 0, 'target_blood_pressure': 100.0}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 1, 'step_name': 'normal_autocontrol_high_pressure_lower_flow', 'var_assertion_ok': False, 'var_mismatches': {'control_voltage': {'actual': 0.0, 'expected': 1.0}, 'infusion_rate': {'actual': 0.0, 'expected': 1.0}, 'log_records': {'actual': 0, 'expected': 1}, 'pump_flow_rate': {'actual': 0.0, 'expected': 1.0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'blood_pressure': 130.0, 'control_released': 1, 'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'manual_default_flow_rate': 1.0, 'pump_complication': 0, 'pump_flow_rate': 1.0, 'pump_speed_source': 0, 'requested_target_blood_pressure': 100.0, 'sensor_buffer_bp': 130.0, 'software_control': 0, 'target_blood_pressure': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'ca_forces_manual_from_normal', 'var_assertion_ok': True, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, hierarchical_state:Ask_StartAC, state:SetpointEditing, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, event:InitiateAC, event:StartAC, event:ChangeSetpoint, event:TerminateAC, ... +35`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3116`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-70b23a1aa0` | `accept` | ❌ | ✅ | Accepted because the request is a hard simulation failure and is rework-locked by SL-10. In scenario start_ac_to_normal_high_pressure_control, step 0 expected StartAC from active leaf CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing to enter CARA.Mode_Control_Algorithm.AutocontrolInit and set CA_mode=1, software_control=1, control_released=0, pump_spe...<truncated 916 chars> |
- repair_rationale：For scenario start_ac_to_normal_high_pressure_control step 0 start_enters_autocontrol_init, the expected state was CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1, software_control=1, control_released=0, pump_speed_source=1, alar...<truncated 323 chars>；For step 1 normal_autocontrol_high_pressure_lower_flow, the expected state was NormalAutocontrol with sensor_buffer_bp=130.0, infusion_rate=1.0, pump_flow_rate=1.0, control_voltage=1.0, and log_records=1; the actual state remained SetpointE...<truncated 273 chars>；This specifically addresses the SL-10 local objection E_DANGLING_TRANSITION from the previous rejected candidate: the invalid inner `SetpointEditing -> AutocontrolInit : StartAC;` is not repeated. The new transition is written at Mode_Contr...<truncated 139 chars>；The StartAC event remains NL-grounded to `CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC` by using the absolute event path `: /Mode_Control_Algorithm.Ask_StartAC.StartAC`; the root name CARA is not repeated after `/`, matching pyfcstm abso...<truncated 16 chars>；The latest non-regressive frontier behavior is preserved without returning the same rejected DSL hash: all required states, variables, actions, and transitions remain represented, including the four forced CA_backManual/CB_backManual/CP_bac...<truncated 151 chars>
- diff_summary：`{"summary": "Removed the unresolved composite-scope StartAC transition form and added a valid Mode_Control_Algorithm-scope transition `Ask_StartAC.SetpointEditing -> AutocontrolInit : /Mode_Control_Algorithm.Ask_StartAC.StartAC;` so StartAC from the active SetpointEditing leaf reaches AutocontrolInit without the prior dangling target error."}`。

#### SL-9 candidate / 最终修改执行方案

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

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_released = 1;
                pump_speed_source = 0;
                pump_flow_rate = manual_default_flow_rate;
                alarm_display = 0;
                alarm_sound = 0;
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
        Ask_StartAC.SetpointEditing -> AutocontrolInit : /Mode_Control_Algorithm.Ask_StartAC.StartAC;
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

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -91,7 +91,7 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> AutocontrolInit :: StartAC;
+        Ask_StartAC.SetpointEditing -> AutocontrolInit : /Mode_Control_Algorithm.Ask_StartAC.StartAC;
         AutocontrolInit -> NormalAutocontrol;
         NormalAutocontrol -> Manual :: TerminateAC;
         NormalAutocontrol -> PumpFault :: PumpFaultDetected;
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:446b92f6a9c687fd3c2a529714e23f88ff17803d53df6a08e3a2bacd2f29804b`。
  - SL-10 evidence 1: `{"summary": "The NL requires that within Ask_StartAC the setpoint can be changed and pressing StartAC enters AutocontrolInit; the failing scenario start_ac_to_normal_high_pressure_control specifically expects StartAC from active leaf CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing to reach AutocontrolInit with CA_mode=1, software_control=1, control_released=0, pump_speed_source=1, alarms off, then proceed to NormalAutocontrol and compute/log high-pressure lower flow."}`
  - SL-10 evidence 2: `{"summary": "SL-9 correctly preserved the intended behavioral repair from the non-regressive frontier and addressed the previous E_DANGLING_TRANSITION by moving the transition out of Ask_StartAC, but the new DSL line `Ask_StartAC.SetpointEditing -> AutocontrolInit : /Mode_Control_Algorithm.Ask_StartAC.StartAC;` introduces a parse error."}`
  - SL-10 evidence 3: `{"summary": "Local deterministic evidence reports `candidate parse failed` with SyntaxFailError at line 94 column 19, `got: .`, raw message `no viable alternative at input 'Ask_StartAC.'`. Because the candidate cannot parse, it cannot be accepted for the next top-down revalidation pass despite matching the intended NL behavior."}`
  - SL-10 evidence 4: `{"summary": "The diff otherwise preserves the required states, variables, AutocontrolInit.enter action, NormalAutocontrol.during action, PumpFault.enter action, and the four forced backManual recovery transitions. Rework should therefore be limited to expressing the leaf-source StartAC transition in a pyfcstm-supported syntax, without changing the preserved behavior."}`
- SL-10 rework_instructions：Keep the intended behavioral repair, but replace the parse-invalid line `Ask_StartAC.SetpointEditing -> AutocontrolInit : /Mode_Control_Algorithm.Ask_StartAC.StartAC;`. The local parser does not accept dotted state-source qualification at `Ask_StartAC.`.；Do not return to the old composite-only `Ask_StartAC -> AutocontrolInit :: StartAC;` behavior if it reintroduces the hot-start scenario failure. The semantic requirement remains: active leaf `CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing` receiving the NL-grounded `StartAC` event must transition to `CARA.Mode_Control_Algorithm.AutocontrolInit`.；Use a DSL-supported hierarchical transition form that avoids the invalid dotted source syntax. Prefer moving the transition into the `Ask_StartAC` scope and qualifying only the target with a parser-supported parent/absolute target form, or use whatever pyfcstm-supported path syntax exists for nested leaf source and sibling target; do not use `Ask_StartAC.Set...<truncated 51 chars>；Preserve `AutocontrolInit.enter` exactly so step 0 of `start_ac_to_normal_high_pressure_control` reaches AutocontrolInit with CA_mode=1, software_control=1, control_released=0, pump_speed_source=1, alarm_display=0, and alarm_sound=0.；Preserve `AutocontrolInit -> NormalAutocontrol;` and `NormalAutocontrol.during` exactly so step 1 reaches NormalAutocontrol with sensor_buffer_bp=130.0, infusion_rate=1.0, pump_flow_rate=1.0, control_voltage=1.0, and log_records=1 for blood_pressure=130.0 and target_blood_pressure=100.0.；Preserve all other NL-required elements and previously passing behavior, especially `Manual -> Ask_StartAC :: InitiateAC;`, `SetpointEditing -> SetpointEditing :: ChangeSetpoint`, the four forced `CA_backManual`, `CB_backManual`, `CP_backManual`, `CC_backManual` transitions to Manual, and `Manual.enter` recovery assignments.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`candidate parse failed`，rejected_by_stage=`SD-10`。
    - local evidence 1: `<unknown>` {"code": "SyntaxFailError", "col": 19, "got": ".", "line": 94, "message": "Invalid syntax - check for missing semicolons, braces, or operators", "raw_message": "no viable alternative at input 'Ask_StartAC.'"}

</details>

<details><summary>Repair 3 / iteration `0` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`start_ac_to_normal_high_pressure_control`。
- before_dsl_hash：`sha256:e9f6dfced3e99f9838ec259677a665c8096fb74c8d4e326b55f12a7e5768bc56`；candidate_dsl_hash：`sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-8bd9f01c6cc`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-70b23a1aa0` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: pressing StartAC from SetpointEditing enters AutocontrolInit, then normal autocontrol uses high BP to lower flow and log data.', 'name': 'start_ac_to_normal_high_pressure_control', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: pressing StartAC from SetpointEditing enters AutocontrolInit, then normal autocontrol uses high BP to lower flow and log data.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'actual_vars_focus': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'control_released': 0, 'pump_speed_source': 0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'alarm_display': 0, 'alarm_sound': 0, 'control_released': 0, 'pump_speed_source': 1, 'software_control': 1}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'start_enters_autocontrol_init', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 0, 'expected': 1}, 'pump_speed_source': {'actual': 0, 'expected': 1}, 'software_control': {'actual': 0, 'expected': 1}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'actual_vars_focus': {'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'pump_flow_rate': 0.0, 'sensor_buffer_bp': 130.0}, 'before_cycles': 0, 'events': [], 'expected_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'expected_vars': {'control_voltage': 1.0, 'infusion_rate': 1.0, 'log_records': 1, 'pump_flow_rate': 1.0, 'sensor_buffer_bp': 130.0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 1, 'step_name': 'normal_autocontrol_high_pressure_lower_flow', 'var_assertion_ok': False, 'var_mismatches': {'control_voltage': {'actual': 0.0, 'expected': 1.0}, 'infusion_rate': {'actual': 0.0, 'expected': 1.0}, 'log_records': {'actual': 0, 'expected': 1}, 'pump_flow_rate': {'actual': 0.0, 'expected': 1.0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'initial_vars': {'blood_pressure': 130.0, 'log_records': 0, 'target_blood_pressure': 100.0}, 'scenario_name': 'start_ac_to_normal_high_pressure_control', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'actual_vars': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'blood_pressure': 130.0, 'control_released': 0, 'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'manual_default_flow_rate': 1.0, 'pump_complication': 0, 'pump_flow_rate': 0.0, 'pump_speed_source': 0, 'requested_target_blood_pressure': 100.0, 'sensor_buffer_bp': 130.0, 'software_control': 0, 'target_blood_pressure': 100.0}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'start_enters_autocontrol_init', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 0, 'expected': 1}, 'pump_speed_source': {'actual': 0, 'expected': 1}, 'software_control': {'actual': 0, 'expected': 1}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing', 'actual_vars': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'blood_pressure': 130.0, 'control_released': 0, 'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'manual_default_flow_rate': 1.0, 'pump_complication': 0, 'pump_flow_rate': 0.0, 'pump_speed_source': 0, 'requested_target_blood_pressure': 100.0, 'sensor_buffer_bp': 130.0, 'software_control': 0, 'target_blood_pressure': 100.0}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 1, 'step_name': 'normal_autocontrol_high_pressure_lower_flow', 'var_assertion_ok': False, 'var_mismatches': {'control_voltage': {'actual': 0.0, 'expected': 1.0}, 'infusion_rate': {'actual': 0.0, 'expected': 1.0}, 'log_records': {'actual': 0, 'expected': 1}, 'pump_flow_rate': {'actual': 0.0, 'expected': 1.0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'blood_pressure': 130.0, 'control_released': 1, 'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'manual_default_flow_rate': 1.0, 'pump_complication': 0, 'pump_flow_rate': 1.0, 'pump_speed_source': 0, 'requested_target_blood_pressure': 100.0, 'sensor_buffer_bp': 130.0, 'software_control': 0, 'target_blood_pressure': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'ca_forces_manual_from_normal', 'var_assertion_ok': True, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, hierarchical_state:Ask_StartAC, state:SetpointEditing, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, event:InitiateAC, event:StartAC, event:ChangeSetpoint, event:TerminateAC, ... +35`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3067`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-70b23a1aa0` | `accept` | ❌ | ✅ | Accepted because this is a hard, rework-locked simulation failure. The scenario start_ac_to_normal_high_pressure_control step 0 expects the NL-grounded StartAC trigger while the active leaf is CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing to enter CARA.Mode_Control_Algorithm.AutocontrolInit and run its enter action, but the original composite-sourc...<truncated 981 chars> |
- repair_rationale：For scenario start_ac_to_normal_high_pressure_control step 0, expected_state is CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1, software_control=1, control_released=0, pump_speed_source=1, alarm_display=0, and alarm_sound=0; act...<truncated 373 chars>；For scenario start_ac_to_normal_high_pressure_control step 1, expected_state is NormalAutocontrol with sensor_buffer_bp=130.0, infusion_rate=1.0, pump_flow_rate=1.0, control_voltage=1.0, and log_records=1. The existing AutocontrolInit.enter...<truncated 231 chars>；This addresses the latest repair_memory guidance without repeating rejected hashes: it does not use the semantically invalid inner `SetpointEditing -> AutocontrolInit : StartAC;` and does not use parse-invalid dotted source syntax such as `...<truncated 36 chars>；The StartAC event remains NL-grounded to pressing StartAC within Ask_StartAC by using `:: StartAC` on the composite forced source Ask_StartAC, while still firing from active descendants by forced-transition expansion.；Previously passing manual fallback behavior is preserved: the four forced CA_backManual, CB_backManual, CP_backManual, and CC_backManual transitions still target Manual, and Manual.enter still restores CA_mode=0, software_control=0, control...<truncated 62 chars>
- diff_summary：`{"summary": "Removed the original non-firing composite-source `Ask_StartAC -> AutocontrolInit :: StartAC;` transition and added the parseable/scope-safe forced transition `! Ask_StartAC -> AutocontrolInit :: StartAC;` at Mode_Control_Algorithm scope so StartAC from the active SetpointEditing descendant reaches AutocontrolInit while preserving all other required behavior."}`。

#### SL-9 candidate / 最终修改执行方案

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
                alarm_display = 0;
                alarm_sound = 0;
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

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -23,6 +23,7 @@
         ! * -> Manual :: CB_backManual;
         ! * -> Manual :: CP_backManual;
         ! * -> Manual :: CC_backManual;
+        ! Ask_StartAC -> AutocontrolInit :: StartAC;
 
         [*] -> Manual;
 
@@ -91,7 +92,6 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> AutocontrolInit :: StartAC;
         AutocontrolInit -> NormalAutocontrol;
         NormalAutocontrol -> Manual :: TerminateAC;
         NormalAutocontrol -> PumpFault :: PumpFaultDetected;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:94f560012a3d2d1bfcc6487c2c74d62ceb1911834ea4005668bef8c99bd53fe1`。
  - SL-10 evidence 1: `{"summary": "The NL requires that within Ask_StartAC, pressing StartAC enters AutocontrolInit, and the failing scenario start_ac_to_normal_high_pressure_control required StartAC from the active leaf CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing to reach AutocontrolInit with CA_mode=1, software_control=1, control_released=0, pump_speed_source=1, alarms off, then proceed to NormalAutocontrol and compute/log the high-pressure lower flow."}`
  - SL-10 evidence 2: `{"summary": "The candidate DSL preserves all required states, variables, actions, and transitions except for replacing the old non-firing composite transition `Ask_StartAC -> AutocontrolInit :: StartAC;` with `! Ask_StartAC -> AutocontrolInit :: StartAC;`. This keeps StartAC scoped to Ask_StartAC while making it apply to active descendants such as SetpointEditing, which is the exact scenario obligation."}`
  - SL-10 evidence 3: `{"summary": "The complete FixLog shows two prior rejected repair forms: `SetpointEditing -> AutocontrolInit : StartAC;` inside Ask_StartAC failed semantic validation because AutocontrolInit was out of scope, and `Ask_StartAC.SetpointEditing -> AutocontrolInit : /Mode_Control_Algorithm.Ask_StartAC.StartAC;` failed parsing because the DSL rejected dotted source qualification. The current candidate avoids both remembered objections: it uses no dangling inner target and no dotted source syntax."}`
  - SL-10 evidence 4: `{"summary": "The FixLog also records a non_regressive_local_only_frontier and instructs not to abandon behavior that fixes the hot-start scenario unless there is real scenario or NL-fidelity regression. Current local evidence reports no scenario_regression and no parse or semantic error; the only objection is forced_transition_count_drift."}`
  - SL-10 evidence 5: `{"summary": "The forced transition count increase is a local design/count matcher objection caused by representing the NL-required descendant-sensitive StartAC behavior as a forced transition over Ask_StartAC. This is a minimal NL-grounded mechanism rather than a dropped or invented behavior, and it preserves the previously passing manual fallback forced transitions and Manual.enter recovery assignments."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20", "covered_local_objection_kinds": ["forced_transition_count_drift"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:73a83549e74c0e0379fb1f8061460f09765a939c4274c02ecf5ad50ae44fe77e", "local_override_rationale_count": 4, "local_override_rationale_hash": "sha256:d8fa4ab3d807d54281c19e4f73f3f08e4f6ababc0b89e71a66c1552b81a435c1", "local_rejection_evidence_hash": "sha256:f3d100b2ad6025c33068798ed109b1bba5154bfeeb324d5ee7d07a2b3494eb43", "local_rejection_reason": "forced_transition_count_drift", "missing_local_objection_kinds": [], "policy": "SL-10 may override conserv...<truncated 302 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`forced_transition_count_drift`，rejected_by_stage=`SD-10`。
    - local evidence 1: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 26, "old": 24}

</details>

<details><summary>Repair 4 / iteration `1` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20`；candidate_dsl_hash：`sha256:1fa9f2728307c12bbbd8bf5368b4d28ee0fd840319b42c295410a75c4904ad3d`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Cross-component backManual recovery can mask an active pump fault by entering Manual, clearing alarms, and restoring manual flow while pump_complication remains set.
- 2. `<unknown>` `` policy=``：The PumpFault recovery semantics permit alarms to be disabled before the NL-described caregiver fault removal step.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-452f95f7b7d`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sl7-0-3096823055` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL global forced transitions allow backManual events from PumpFault to Manual.', 'Manual.enter clears `alarm_display` and `alarm_sound` and restores `pump_flow_rate`.', 'Only `FaultRemoved` clears `pump_complication`; global backManual recovery does not.', 'Simulation confirms `CB_backManual` from PumpFault lands in Manual with `pump_complication: 1`, `alarm_display: 0`, and `alarm_sound: 0`.'], 'severity': 'major', 'summary': 'Cross-component backManual recovery can mask an active pump fault by entering Manual, clearing alarms, and restoring manual flow while pump_complication remains set.'}` |
| `fixreq-1-sl7-1-f1f2c62158` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL says pump faults activate alarm signals and the caregiver removes the fault.', 'DSL allows wildcard fallback from PumpFault to Manual without `FaultRemoved` while Manual.enter disables alarms.'], 'severity': 'major', 'summary': 'The PumpFault recovery semantics permit alarms to be disabled before the NL-described caregiver fault removal step.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, hierarchical_state:Ask_StartAC, state:SetpointEditing, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, event:InitiateAC, event:StartAC, event:ChangeSetpoint, event:TerminateAC, ... +35`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3143`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sl7-0-3096823055` | `accept` | ❌ | ❌ | Accepted because the unsafe_recovery evidence is a hard model-review finding: global backManual events can enter Manual from PumpFault while pump_complication remains 1, and the previous Manual.enter unconditionally cleared alarms and restored manual flow. The smallest safe edit is to keep the required shared Manual recovery target and all backManual events,...<truncated 299 chars> |
| `fixreq-1-sl7-1-f1f2c62158` | `accept` | ❌ | ❌ | Accepted because the NL says pump faults activate alarm signals and the caregiver removes the fault before recovery. The edit preserves PumpFault and FaultRemoved semantics: only FaultRemoved clears pump_complication and alarms; Manual.enter no longer disables alarms before that caregiver fault-removal step.；intent=Preserve FaultRemoved as the only transitio...<truncated 104 chars> |
- repair_rationale：For fixreq-1-sl7-0, the expected safe behavior is that a backManual event from PumpFault may make CA_mode Manual as the shared recovery target, but must not mask an active fault. The reported actual behavior was Manual with pump_complicatio...<truncated 234 chars>；For fixreq-1-sl7-1, the NL-required caregiver fault-removal step remains represented by PumpFault -> Manual :: FaultRemoved, whose effect clears pump_complication, alarm_display, and alarm_sound. A wildcard backManual from PumpFault no long...<truncated 123 chars>；The previous accepted StartAC repair is preserved: `! Ask_StartAC -> AutocontrolInit :: StartAC;`, `AutocontrolInit.enter`, `AutocontrolInit -> NormalAutocontrol;`, and `NormalAutocontrol.during` are unchanged, preserving the prior hot-star...<truncated 20 chars>；All required grounded elements are preserved: CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, SetpointEditing, AutocontrolInit, NormalAutocontrol, PumpFault, all required events and variables, the four backManual forced transitions, Faul...<truncated 70 chars>
- diff_summary：`{"summary": "Changed only Manual.enter: alarm clearing and manual-flow restoration are now guarded by `if [pump_complication == 0]`, so backManual recovery from PumpFault keeps alarms active while preserving Manual as the shared fallback and preserving the prior StartAC forced-transition repair."}`。

#### SL-9 candidate / 最终修改执行方案

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
                if [pump_complication == 0] {
                    pump_flow_rate = manual_default_flow_rate;
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

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -33,9 +33,11 @@
                 software_control = 0;
                 control_released = 1;
                 pump_speed_source = 0;
-                pump_flow_rate = manual_default_flow_rate;
-                alarm_display = 0;
-                alarm_sound = 0;
+                if [pump_complication == 0] {
+                    pump_flow_rate = manual_default_flow_rate;
+                    alarm_display = 0;
+                    alarm_sound = 0;
+                }
             }
         }
 
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:1045e03747437198de4055b4b55bbbe0957e3d893489ece9001f92ebb0606706`。
  - SL-10 evidence 1: `{"summary": "Both current hard SL-7 model-review requests were accepted by SL-9 and are resolved by the candidate DSL. The unsafe_recovery finding said backManual from PumpFault could enter Manual while pump_complication remained 1, then Manual.enter cleared alarm_display/alarm_sound and restored pump_flow_rate. The candidate changes only Manual.enter so CA_mode/software_control/control_released/pump_speed_source still move to Manual recovery, but pump_flow_rate restoration and alarm clearing occur only when pump_complication == 0."}`
  - SL-10 evidence 2: `{"summary": "The NL says pump faults activate alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. The candidate preserves PumpFault.enter alarm activation and software-control release, preserves FaultRemoved as the transition that clears pump_complication and alarms, and prevents a cross-component backManual fallback from disabling alarms before the caregiver fault-removal step."}`
  - SL-10 evidence 3: `{"summary": "The cross-component fallback NL obligation is still represented: CA_backManual, CB_backManual, CP_backManual, and CC_backManual remain forced transitions to Manual, and Manual.enter still sets CA_mode=0, software_control=0, control_released=1, and pump_speed_source=0. The repair narrows only the unsafe side effects during an active pump complication."}`
  - SL-10 evidence 4: `{"summary": "The complete FixLog shows a prior hard hot-start simulation repair and subsequent SL-10 pass for the forced StartAC transition `! Ask_StartAC -> AutocontrolInit :: StartAC;`, with forced_transition_count_drift explicitly overridden as an audit-only local objection. The candidate preserves that accepted StartAC behavior, AutocontrolInit.enter, AutocontrolInit -> NormalAutocontrol, and NormalAutocontrol.during; the local evidence confirms the hot-start scenario still passes."}`
  - SL-10 evidence 5: `{"summary": "No required NL-grounded state, event, variable, action, or transition obligation is dropped. Manual, Ask_StartAC.SetpointEditing, AutocontrolInit, NormalAutocontrol, PumpFault, InitiateAC, StartAC, ChangeSetpoint, TerminateAC, PumpFaultDetected, FaultRemoved, all backManual events, required variables, Manual.enter, NormalAutocontrol.during, and PumpFault.enter remain represented."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`minor`。
  - local_rejection：reason=`scenario_regression`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 12, "n_scenarios_passed": 11, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: first empty cycle should dispatch to Manual and apply manual pump-switch/default-flow obligations.", "name": "default_init_enters_manual_mode", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_display": 0, "alarm_sound":...<truncated 14689 chars>

</details>

<details><summary>Repair 5 / iteration `2` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`cb_backmanual_forces_manual_from_pump_fault`。
- before_dsl_hash：`sha256:1fa9f2728307c12bbbd8bf5368b4d28ee0fd840319b42c295410a75c4904ad3d`；candidate_dsl_hash：`sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-83f4e7b3696`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sd6-0-fcaed05e1a` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CB_backManual is a cross-component fallback that should force PumpFault to the shared Manual recovery target.', 'name': 'cb_backmanual_forces_manual_from_pump_fault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CB_backManual is a cross-component fallback that should force PumpFault to the shared Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_display': 1, 'alarm_sound': 1, 'control_released': 1, 'pump_flow_rate': 0.0, 'pump_speed_source': 0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'control_released': 1, 'pump_flow_rate': 3.0, 'pump_speed_source': 0, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'cb_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_display': {'actual': 1, 'expected': 0}, 'alarm_sound': {'actual': 1, 'expected': 0}, 'pump_flow_rate': {'actual': 0.0, 'expected': 3.0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'alarm_display': 1, 'alarm_sound': 1, 'control_released': 1, 'manual_default_flow_rate': 3.0, 'pump_complication': 1, 'software_control': 0}, 'scenario_name': 'cb_backmanual_forces_manual_from_pump_fault', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_display': 1, 'alarm_sound': 1, 'blood_pressure': 0.0, 'control_released': 1, 'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'manual_default_flow_rate': 3.0, 'pump_complication': 1, 'pump_flow_rate': 0.0, 'pump_speed_source': 0, 'requested_target_blood_pressure': 100.0, 'sensor_buffer_bp': 0.0, 'software_control': 0, 'target_blood_pressure': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'cb_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_display': {'actual': 1, 'expected': 0}, 'alarm_sound': {'actual': 1, 'expected': 0}, 'pump_flow_rate': {'actual': 0.0, 'expected': 3.0}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, hierarchical_state:Ask_StartAC, state:SetpointEditing, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, event:InitiateAC, event:StartAC, event:ChangeSetpoint, event:TerminateAC, ... +35`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3067`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sd6-0-fcaed05e1a` | `accept` | ❌ | ❌ | Accepted because the current SD-6 hard simulation request reopens cb_backmanual_forces_manual_from_pump_fault with explicit expected-vs-actual evidence. In step cb_forces_manual, the state already reaches CARA.Mode_Control_Algorithm.Manual, but expected pump_flow_rate=3.0, alarm_display=0, and alarm_sound=0 while the current guarded Manual.enter leaves pump_...<truncated 780 chars> |
- repair_rationale：For scenario cb_backmanual_forces_manual_from_pump_fault, step cb_forces_manual, expected_state and actual_state both are CARA.Mode_Control_Algorithm.Manual, so no transition target edit is needed.；The failing gap is only variables: expected pump_flow_rate=3.0, alarm_display=0, alarm_sound=0, but actual pump_flow_rate=0.0, alarm_display=1, alarm_sound=1 because Manual.enter skipped those assignments under pump_complication == 1.；The smallest repair removes that guard and restores the Manual shared recovery target behavior so entering Manual always sets the manual default flow and clears display/sound alarms, matching the current hard SD-6 scenario.；The prior StartAC repair is preserved exactly as the parseable forced transition ! Ask_StartAC -> AutocontrolInit :: StartAC;, avoiding the previously rejected dangling inner target and parse-invalid dotted-source forms while keeping StartA...<truncated 30 chars>；AutocontrolInit.enter, AutocontrolInit -> NormalAutocontrol, NormalAutocontrol.during, ChangeSetpoint, InitiateAC, TerminateAC, PumpFaultDetected, FaultRemoved, and all four backManual forced transitions are preserved, so the previously pas...<truncated 84 chars>
- diff_summary：`{"summary": "Changed only Manual.enter: removed the pump_complication guard around pump_flow_rate, alarm_display, and alarm_sound assignments so any backManual fallback into Manual restores manual_default_flow_rate and clears alarms, resolving cb_backmanual_forces_manual_from_pump_fault while preserving the accepted forced StartAC repair and all required grounded elements."}`。

#### SL-9 candidate / 最终修改执行方案

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
                alarm_display = 0;
                alarm_sound = 0;
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

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -33,11 +33,9 @@
                 software_control = 0;
                 control_released = 1;
                 pump_speed_source = 0;
-                if [pump_complication == 0] {
-                    pump_flow_rate = manual_default_flow_rate;
-                    alarm_display = 0;
-                    alarm_sound = 0;
-                }
+                pump_flow_rate = manual_default_flow_rate;
+                alarm_display = 0;
+                alarm_sound = 0;
             }
         }
 
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:8f24b0d17cfa8f7d6c271ff995b6e853564b058f0a4496d7bb74980dedd8fd96`。
  - SL-10 evidence 1: `{"summary": "The current hard SD-6 request fixreq-2-sd6-0-fcaed05e1a targeted scenario cb_backmanual_forces_manual_from_pump_fault. The failing step expected CB_backManual from CARA.Mode_Control_Algorithm.PumpFault to land in Manual with CA_mode=0, software_control=0, control_released=1, pump_speed_source=0, pump_flow_rate=3.0, alarm_display=0, and alarm_sound=0; the old guarded Manual.enter landed in Manual but left pump_flow_rate=0.0 and alarms asserted. The candidate changes only Manual.enter to assign pump_flow_rate=manual_default_flow_rate and clear alarm_display/alarm_sound unconditionally, which directly resolves the requested expected-vs-actual mismatch."}`
  - SL-10 evidence 2: `{"summary": "Local deterministic repair review for the candidate is OK: target_resolved=true, regression_detected=false, drift_risk=none, with no local_rejection. The scenario summary reports 14 scenarios with no coverage gap and no weak oracle, so there is no unresolved local parse, semantic, design, or simulation blocker requiring an override."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves the NL-required Mode_Control_Algorithm hierarchy and required states Manual, Ask_StartAC.SetpointEditing, AutocontrolInit, NormalAutocontrol, and PumpFault. It also preserves InitiateAC, StartAC, ChangeSetpoint, TerminateAC, PumpFaultDetected, FaultRemoved, and all four cross-component backManual forced transitions to Manual."}`
  - SL-10 evidence 4: `{"summary": "The previously accepted StartAC repair remains intact as `! Ask_StartAC -> AutocontrolInit :: StartAC;`, preserving the FixLog-resolved obligation that pressing StartAC from active SetpointEditing enters AutocontrolInit without returning to prior dangling-target or parse-invalid forms."}`
  - SL-10 evidence 5: `{"summary": "The complete FixLog shows a prior tension between the SL-7 unsafe_recovery repair, which guarded Manual.enter alarm clearing during active pump_complication, and the reopened hard SD-6 simulation obligation, which requires shared Manual fallback from PumpFault to restore manual flow and clear caregiver-facing alarms. The current candidate intentionally returns Manual.enter to the previously passing shared recovery behavior while preserving FaultRemoved, PumpFault alarm activation, software-control release, and the Manual recovery target. Because the current local check passes and the active hard request is exactly resolved, the candidate is acceptable for the next full top-down ...<truncated 195 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。

</details>

<details><summary>Repair 6 / iteration `3` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`cb_backmanual_forces_manual_from_pump_fault`。
- before_dsl_hash：`sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20`；candidate_dsl_hash：`sha256:e0d83a90e0bc0b26d3205dd82c250301d3787ea358564f23754fe4929a3ce867`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-83f4e7b3696`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sd6-0-89e34b93a6` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CB_backManual is a cross-component fallback to Manual, but an active uncleared pump fault should not be silently treated as fault removed.', 'name': 'cb_backmanual_forces_manual_from_pump_fault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CB_backManual is a cross-component fallback to Manual, but an active uncleared pump fault should not be silently treated as fault removed.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'control_released': 1, 'pump_complication': 1, 'pump_speed_source': 0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_display': 1, 'alarm_sound': 1, 'control_released': 1, 'pump_complication': 1, 'pump_speed_source': 0, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'cb_forces_manual_preserving_active_fault_alarm', 'var_assertion_ok': False, 'var_mismatches': {'alarm_display': {'actual': 0, 'expected': 1}, 'alarm_sound': {'actual': 0, 'expected': 1}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 0, 'alarm_display': 1, 'alarm_sound': 1, 'control_released': 1, 'manual_default_flow_rate': 3.0, 'pump_complication': 1, 'pump_speed_source': 0, 'software_control': 0}, 'scenario_name': 'cb_backmanual_forces_manual_from_pump_fault', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_display': 0, 'alarm_sound': 0, 'blood_pressure': 0.0, 'control_released': 1, 'control_voltage': 0.0, 'infusion_rate': 0.0, 'log_records': 0, 'manual_default_flow_rate': 3.0, 'pump_complication': 1, 'pump_flow_rate': 3.0, 'pump_speed_source': 0, 'requested_target_blood_pressure': 100.0, 'sensor_buffer_bp': 0.0, 'software_control': 0, 'target_blood_pressure': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'cb_forces_manual_preserving_active_fault_alarm', 'var_assertion_ok': False, 'var_mismatches': {'alarm_display': {'actual': 0, 'expected': 1}, 'alarm_sound': {'actual': 0, 'expected': 1}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, hierarchical_state:Ask_StartAC, state:SetpointEditing, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, event:InitiateAC, event:StartAC, event:ChangeSetpoint, event:TerminateAC, ... +35`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3239`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sd6-0-89e34b93a6` | `accept` | ❌ | ❌ | Accepted because the hard SD-6 simulation evidence for scenario cb_backmanual_forces_manual_from_pump_fault shows the transition target is already correct: CB_backManual from PumpFault reaches CARA.Mode_Control_Algorithm.Manual. The only failing variables are alarm_display and alarm_sound: expected 1/1 while actual is 0/0 because Manual.enter unconditionally...<truncated 773 chars> |
- repair_rationale：For scenario cb_backmanual_forces_manual_from_pump_fault, step cb_forces_manual, the expected state is CARA.Mode_Control_Algorithm.Manual and the actual state is already CARA.Mode_Control_Algorithm.Manual, so no transition target edit is ne...<truncated 5 chars>；The current failing gap is alarm variables: expected pump_complication=1, alarm_display=1, and alarm_sound=1, but actual alarm_display=0 and alarm_sound=0 because Manual.enter unconditionally cleared alarms after the CB_backManual forced tr...<truncated 9 chars>；The repair changes only Manual.enter alarm handling: if pump_complication > 0, Manual keeps/asserts alarm_display=1 and alarm_sound=1; otherwise Manual clears them. This matches the NL that pump faults activate alarm signals and avoids sile...<truncated 48 chars>；Manual.enter still sets CA_mode=0, software_control=0, control_released=1, pump_speed_source=0, and pump_flow_rate=manual_default_flow_rate, preserving the cross-component shared Manual recovery target and the manual pump default-flow oblig...<truncated 6 chars>；FaultRemoved remains the caregiver fault-removal event. Its effect clears pump_complication and alarms before entering Manual, so after FaultRemoved the repaired Manual.enter takes the no-complication branch and keeps alarms cleared.
- diff_summary：`{"summary": "Changed only Manual.enter alarm assignments: pump_flow_rate remains unconditionally restored to manual_default_flow_rate, but alarm_display/alarm_sound are now set to 1 when pump_complication > 0 and cleared only when no pump complication is active. All states, events, variables, StartAC forced repair, autocontrol behavior, fault behavior, and backManual recovery transitions are preserved."}`。

#### SL-9 candidate / 最终修改执行方案

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

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -34,8 +34,13 @@
                 control_released = 1;
                 pump_speed_source = 0;
                 pump_flow_rate = manual_default_flow_rate;
-                alarm_display = 0;
-                alarm_sound = 0;
+                if [pump_complication > 0] {
+                    alarm_display = 1;
+                    alarm_sound = 1;
+                } else {
+                    alarm_display = 0;
+                    alarm_sound = 0;
+                }
             }
         }
 
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:e9b26c30e4522e759c0fc15edb206db7cf9e2bcf7cc815dc643c108cb6a7c3c0`。
  - SL-10 evidence 1: `{"summary": "The active hard SD-6 request fixreq-3-sd6-0-89e34b93a6 targets scenario cb_backmanual_forces_manual_from_pump_fault. The failing step expected CB_backManual from CARA.Mode_Control_Algorithm.PumpFault to reach Manual while preserving an active uncleared fault: CA_mode=0, software_control=0, control_released=1, pump_speed_source=0, pump_complication=1, alarm_display=1, and alarm_sound=1. The candidate keeps the forced CB_backManual transition to Manual and changes Manual.enter so pump_complication > 0 asserts alarm_display=1 and alarm_sound=1 instead of clearing them."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves the shared Manual recovery target required by the NL: CA_backManual, CB_backManual, CP_backManual, and CC_backManual remain forced transitions to Manual, and Manual.enter still sets CA_mode=0, software_control=0, control_released=1, pump_speed_source=0, and pump_flow_rate=manual_default_flow_rate."}`
  - SL-10 evidence 3: `{"summary": "The candidate is higher NL fidelity than the old DSL because the NL says pump faults activate alarm signals and the caregiver removes the fault. With pump_complication still active and no FaultRemoved event, Manual.enter now keeps caregiver-facing alarms asserted; after FaultRemoved clears pump_complication and alarms, Manual.enter takes the no-complication branch and leaves alarms cleared."}`
  - SL-10 evidence 4: `{"summary": "The DSL diff is minimal and localized to Manual.enter alarm assignments. It does not drop NL-required states, events, variables, or actions: CARA, Mode_Control_Algorithm, Manual, Ask_StartAC.SetpointEditing, AutocontrolInit, NormalAutocontrol, PumpFault, InitiateAC, StartAC, ChangeSetpoint, TerminateAC, PumpFaultDetected, FaultRemoved, all four backManual events, and required variables remain represented."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic SL-10/SD-10 evidence is OK: target_resolved=true, regression_detected=false, drift_risk=none, no local_rejection, and the scenario summary reports 14 scenarios with no coverage gap and no weak oracle."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-8bd9f01c6cc` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-8bd9f01c6cc` | accept=1, reject=0 | `sl10_review` | `sha256:a46b4d58c6ffd22203d6ed11462c086ca21576d26457b9edc3edda21fd3601b5` | Accepted hard sim request fixreq-0-sd6-0-70b23a1aa0., For scenario start_ac_to_normal_high_pressure_control step 0 start_enters_autocontrol_init, expected state was CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1, software_control=1, control_released=0, pump_speed_source=1, alarm_display=0, and alarm_sound=0, but actual state remained CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing with CA_mode=0, software_control=0, and pump_speed_source=0. The repair makes StartAC fire from the active SetpointEditing leaf and enter AutocontrolInit, whose existing enter action sets those expected variables., For scenario start_ac_to_normal_high_pressure_control step 1 normal_autocontrol_high_pressure_lower_flow, expected state was NormalAutocontrol with sensor_buffer_bp=130.0, infusion_rate=1.0, pump_flow_rate=1.0, control_voltage=1.0, and log_records=1, but actual state was still SetpointEditing with those control outputs at 0. After the repaired StartAC transition enters AutocontrolInit, the existing unguarded AutocontrolInit -> NormalAutocontrol transition and NormalAutocontrol during action compute the lower high-pressure flow and increment the log., ... +3 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-8bd9f01c6cc` | accept=1, reject=0 | `sl9_rework` | `sha256:a46b4d58c6ffd22203d6ed11462c086ca21576d26457b9edc3edda21fd3601b5` | Keep the intended behavioral repair, but rewrite the StartAC transition with valid DSL scoping. Do not leave `SetpointEditing -> AutocontrolInit : StartAC;` inside `state Ask_StartAC` unless the target is expressed in a DSL-supported qualified form., Preferred minimal edit: place the leaf-source StartAC transition at the `Mode_Control_Algorithm` scope, alongside `Manual -> Ask_StartAC :: InitiateAC;`, using a qualified source path to the active leaf and sibling target, e.g. `Ask_StartAC.SetpointEditing -> AutocontrolInit :: StartAC;` if this is the DSL-supported syntax., If the DSL requires another qualification form for nested leaf sources or parent/sibling targets, use that supported form, but the semantic result must be: active leaf `CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing` receiving the NL-grounded StartAC event transitions to `CARA.Mode_Control_Algorithm.AutocontrolInit`., ... +14 |
| 4 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-8bd9f01c6cc` | accept=1, reject=0 | `sl10_review` | `sha256:bceb828a382a28ab702e9cfcc4529aec920eb9078d90fb26b856cb7702f2c9d4` | For scenario start_ac_to_normal_high_pressure_control step 0 start_enters_autocontrol_init, the expected state was CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1, software_control=1, control_released=0, pump_speed_source=1, alarm_display=0, and alarm_sound=0; the actual state stayed CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing with CA_mode=0, software_control=0, and pump_speed_source=0. The repair makes StartAC fire from the active SetpointEditing leaf and enter AutocontrolInit, whose existing enter action sets the expected variables., For step 1 normal_autocontrol_high_pressure_lower_flow, the expected state was NormalAutocontrol with sensor_buffer_bp=130.0, infusion_rate=1.0, pump_flow_rate=1.0, control_voltage=1.0, and log_records=1; the actual state remained SetpointEditing with control outputs/logs at 0. Once the repaired transition enters AutocontrolInit, the preserved unguarded AutocontrolInit -> NormalAutocontrol transition and preserved NormalAutocontrol.during action compute the lower high-pressure flow and increment log_records., This specifically addresses the SL-10 local objection E_DANGLING_TRANSITION from the previous rejected candidate: the invalid inner `SetpointEditing -> AutocontrolInit : StartAC;` is not repeated. The new transition is written at Mode_Control_Algorithm scope, where `AutocontrolInit` is a resolvable sibling target, while the source is qualified as `Ask_StartAC.SetpointEditing`., ... +3 |
| 5 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-8bd9f01c6cc` | accept=1, reject=0 | `sl9_rework` | `sha256:bceb828a382a28ab702e9cfcc4529aec920eb9078d90fb26b856cb7702f2c9d4` | Keep the intended behavioral repair, but replace the parse-invalid line `Ask_StartAC.SetpointEditing -> AutocontrolInit : /Mode_Control_Algorithm.Ask_StartAC.StartAC;`. The local parser does not accept dotted state-source qualification at `Ask_StartAC.`., Do not return to the old composite-only `Ask_StartAC -> AutocontrolInit :: StartAC;` behavior if it reintroduces the hot-start scenario failure. The semantic requirement remains: active leaf `CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing` receiving the NL-grounded `StartAC` event must transition to `CARA.Mode_Control_Algorithm.AutocontrolInit`., Use a DSL-supported hierarchical transition form that avoids the invalid dotted source syntax. Prefer moving the transition into the `Ask_StartAC` scope and qualifying only the target with a parser-supported parent/absolute target form, or use whatever pyfcstm-supported path syntax exists for nested leaf source and sibling target; do not use `Ask_StartAC.SetpointEditing` if `.` is not accepted by the parser., ... +17 |
| 6 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-8bd9f01c6cc` | accept=1, reject=0 | `sl10_review` | `sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20` | For scenario start_ac_to_normal_high_pressure_control step 0, expected_state is CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1, software_control=1, control_released=0, pump_speed_source=1, alarm_display=0, and alarm_sound=0; actual_state remained CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointEditing with CA_mode/software_control/pump_speed_source still 0. The new forced transition `! Ask_StartAC -> AutocontrolInit :: StartAC;` is written in the Mode_Control_Algorithm scope, so AutocontrolInit is a resolvable sibling target and the transition applies from the active SetpointEditing descendant., For scenario start_ac_to_normal_high_pressure_control step 1, expected_state is NormalAutocontrol with sensor_buffer_bp=130.0, infusion_rate=1.0, pump_flow_rate=1.0, control_voltage=1.0, and log_records=1. The existing AutocontrolInit.enter and unguarded AutocontrolInit -> NormalAutocontrol transition are preserved, as is NormalAutocontrol.during, so after StartAC reaches AutocontrolInit the next cycle computes the lower high-pressure flow and increments log_records., This addresses the latest repair_memory guidance without repeating rejected hashes: it does not use the semantically invalid inner `SetpointEditing -> AutocontrolInit : StartAC;` and does not use parse-invalid dotted source syntax such as `Ask_StartAC.SetpointEditing -> ...`., ... +4 |
| 7 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-8bd9f01c6cc` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 8 | `1` | `request_batch` | `fixbatch-1-sha256-452f95f7b7d` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 9 | `1` | `sl9_decision` | `fixbatch-1-sha256-452f95f7b7d` | accept=2, reject=0 | `sl10_review` | `sha256:1fa9f2728307c12bbbd8bf5368b4d28ee0fd840319b42c295410a75c4904ad3d` | For fixreq-1-sl7-0, the expected safe behavior is that a backManual event from PumpFault may make CA_mode Manual as the shared recovery target, but must not mask an active fault. The reported actual behavior was Manual with pump_complication=1, alarm_display=0, and alarm_sound=0. The repaired Manual.enter always sets CA_mode=0, software_control=0, control_released=1, and pump_speed_source=0, but clears alarms and restores pump_flow_rate only when pump_complication == 0., For fixreq-1-sl7-1, the NL-required caregiver fault-removal step remains represented by PumpFault -> Manual :: FaultRemoved, whose effect clears pump_complication, alarm_display, and alarm_sound. A wildcard backManual from PumpFault no longer disables alarms before FaultRemoved because Manual.enter sees pump_complication == 1 and skips the alarm-clearing block., The previous accepted StartAC repair is preserved: `! Ask_StartAC -> AutocontrolInit :: StartAC;`, `AutocontrolInit.enter`, `AutocontrolInit -> NormalAutocontrol;`, and `NormalAutocontrol.during` are unchanged, preserving the prior hot-start scenario behavior., ... +1 |
| 10 | `1` | `sl10_review` | `fixbatch-1-sha256-452f95f7b7d` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:1fa9f2728307c12bbbd8bf5368b4d28ee0fd840319b42c295410a75c4904ad3d` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 11 | `2` | `request_batch` | `fixbatch-2-sha256-83f4e7b3696` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 12 | `2` | `sl9_decision` | `fixbatch-2-sha256-83f4e7b3696` | accept=1, reject=0 | `sl10_review` | `sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20` | For scenario cb_backmanual_forces_manual_from_pump_fault, step cb_forces_manual, expected_state and actual_state both are CARA.Mode_Control_Algorithm.Manual, so no transition target edit is needed., The failing gap is only variables: expected pump_flow_rate=3.0, alarm_display=0, alarm_sound=0, but actual pump_flow_rate=0.0, alarm_display=1, alarm_sound=1 because Manual.enter skipped those assignments under pump_complication == 1., The smallest repair removes that guard and restores the Manual shared recovery target behavior so entering Manual always sets the manual default flow and clears display/sound alarms, matching the current hard SD-6 scenario., ... +3 |
| 13 | `2` | `sl10_review` | `fixbatch-2-sha256-83f4e7b3696` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:26573d9837baa3068a0da811b6d56f4da43a669b832d82c8eb42734481b44c20` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +4 |
| 14 | `3` | `request_batch` | `fixbatch-3-sha256-83f4e7b3696` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 15 | `3` | `sl9_decision` | `fixbatch-3-sha256-83f4e7b3696` | accept=1, reject=0 | `sl10_review` | `sha256:e0d83a90e0bc0b26d3205dd82c250301d3787ea358564f23754fe4929a3ce867` | For scenario cb_backmanual_forces_manual_from_pump_fault, step cb_forces_manual, the expected state is CARA.Mode_Control_Algorithm.Manual and the actual state is already CARA.Mode_Control_Algorithm.Manual, so no transition target edit is needed., The current failing gap is alarm variables: expected pump_complication=1, alarm_display=1, and alarm_sound=1, but actual alarm_display=0 and alarm_sound=0 because Manual.enter unconditionally cleared alarms after the CB_backManual forced transition., The repair changes only Manual.enter alarm handling: if pump_complication > 0, Manual keeps/asserts alarm_display=1 and alarm_sound=1; otherwise Manual clears them. This matches the NL that pump faults activate alarm signals and avoids silently treating an uncleared PumpFault as removed., ... +5 |
| 16 | `3` | `sl10_review` | `fixbatch-3-sha256-83f4e7b3696` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:e0d83a90e0bc0b26d3205dd82c250301d3787ea358564f23754fe4929a3ce867` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5385, 'completion_chars': 21712, 'completion_tokens': 6604, 'elapsed_seconds': 121.21371774794534, 'estimated_completion_tokens': 5428, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 12085, 'first_chunk_seconds': 24.11100761871785, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13054}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1695, 'completion_chars': 6878, 'completion_tokens': 3250, 'elapsed_seconds': 61.37203811574727, 'estimated_completion_tokens': 1720, 'estimated_prompt_tokens': 15558, 'estimated_total_tokens': 17278, 'first_chunk_seconds': 31.58375660702586, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 62230, 'prompt_tokens': 15083, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 18333}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2998, 'completion_chars': 12300, 'completion_tokens': 3517, 'elapsed_seconds': 65.63977183308452, 'estimated_completion_tokens': 3075, 'estimated_prompt_tokens': 18302, 'estimated_total_tokens': 21377, 'first_chunk_seconds': 12.69018861092627, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 73207, 'prompt_tokens': 17711, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21228}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3542, 'completion_chars': 14496, 'completion_tokens': 4257, 'elapsed_seconds': 79.14967142697424, 'estimated_completion_tokens': 3624, 'estimated_prompt_tokens': 18797, 'estimated_total_tokens': 22421, 'first_chunk_seconds': 15.301231630146503, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 75186, 'prompt_tokens': 18204, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22461}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1526, 'completion_chars': 6560, 'completion_tokens': 2978, 'elapsed_seconds': 57.14866770710796, 'estimated_completion_tokens': 1640, 'estimated_prompt_tokens': 25669, 'estimated_total_tokens': 27309, 'first_chunk_seconds': 29.605819917749614, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 102673, 'prompt_tokens': 23532, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26510}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 742, 'completion_chars': 3176, 'completion_tokens': 1261, 'elapsed_seconds': 26.603217829950154, 'estimated_completion_tokens': 794, 'estimated_prompt_tokens': 24624, 'estimated_total_tokens': 25418, 'first_chunk_seconds': 13.267400939017534, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 98493, 'prompt_tokens': 21758, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23019}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1692, 'completion_chars': 7272, 'completion_tokens': 2316, 'elapsed_seconds': 45.29346523992717, 'estimated_completion_tokens': 1818, 'estimated_prompt_tokens': 56159, 'estimated_total_tokens': 57977, 'first_chunk_seconds': 14.741181008983403, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 224636, 'prompt_tokens': 51294, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 53610}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 859, 'completion_chars': 3707, 'completion_tokens': 1347, 'elapsed_seconds': 28.537945541087538, 'estimated_completion_tokens': 927, 'estimated_prompt_tokens': 55031, 'estimated_total_tokens': 55958, 'first_chunk_seconds': 13.364320452790707, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 220121, 'prompt_tokens': 49248, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 50595}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1737, 'completion_chars': 7466, 'completion_tokens': 2774, 'elapsed_seconds': 55.557499814778566, 'estimated_completion_tokens': 1867, 'estimated_prompt_tokens': 88999, 'estimated_total_tokens': 90866, 'first_chunk_seconds': 24.156523962970823, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 355993, 'prompt_tokens': 81174, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 83948}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 879, 'completion_chars': 4179, 'completion_tokens': 1398, 'elapsed_seconds': 28.81650162488222, 'estimated_completion_tokens': 1045, 'estimated_prompt_tokens': 87854, 'estimated_total_tokens': 88899, 'first_chunk_seconds': 13.138500318862498, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 351415, 'prompt_tokens': 79065, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 80463}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1773, 'completion_chars': 7149, 'completion_tokens': 2642, 'elapsed_seconds': 51.043826618697494, 'estimated_completion_tokens': 1788, 'estimated_prompt_tokens': 20014, 'estimated_total_tokens': 21802, 'first_chunk_seconds': 18.861918824724853, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 80055, 'prompt_tokens': 19494, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22136}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1991, 'completion_chars': 9235, 'completion_tokens': 3028, 'elapsed_seconds': 59.23014299198985, 'estimated_completion_tokens': 2309, 'estimated_prompt_tokens': 22558, 'estimated_total_tokens': 24867, 'first_chunk_seconds': 23.060645482037216, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 90229, 'prompt_tokens': 22212, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25240}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1506, 'completion_chars': 6568, 'completion_tokens': 2025, 'elapsed_seconds': 41.53613248793408, 'estimated_completion_tokens': 1642, 'estimated_prompt_tokens': 122710, 'estimated_total_tokens': 124352, 'first_chunk_seconds': 14.282760856673121, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 490840, 'prompt_tokens': 110224, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 112249}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 889, 'completion_chars': 4229, 'completion_tokens': 1142, 'elapsed_seconds': 24.93827811209485, 'estimated_completion_tokens': 1058, 'estimated_prompt_tokens': 118556, 'estimated_total_tokens': 119614, 'first_chunk_seconds': 9.358850880991668, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 474222, 'prompt_tokens': 104682, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 105824}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4269, 'completion_chars': 17346, 'completion_tokens': 4788, 'elapsed_seconds': 88.54612472001463, 'estimated_completion_tokens': 4337, 'estimated_prompt_tokens': 21970, 'estimated_total_tokens': 26307, 'first_chunk_seconds': 12.184232395142317, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 87877, 'prompt_tokens': 21308, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26096}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1461, 'completion_chars': 6401, 'completion_tokens': 2375, 'elapsed_seconds': 46.884112446103245, 'estimated_completion_tokens': 1601, 'estimated_prompt_tokens': 57942, 'estimated_total_tokens': 59543, 'first_chunk_seconds': 20.383028416894376, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 231767, 'prompt_tokens': 49006, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 51381}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 614, 'completion_chars': 2864, 'completion_tokens': 1614, 'elapsed_seconds': 31.6979064270854, 'estimated_completion_tokens': 716, 'estimated_prompt_tokens': 42260, 'estimated_total_tokens': 42976, 'first_chunk_seconds': 20.582275486085564, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 169040, 'prompt_tokens': 34442, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 36056}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2722, 'completion_chars': 11088, 'completion_tokens': 3759, 'elapsed_seconds': 71.27212612889707, 'estimated_completion_tokens': 2772, 'estimated_prompt_tokens': 22465, 'estimated_total_tokens': 25237, 'first_chunk_seconds': 22.214585510082543, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 89858, 'prompt_tokens': 21898, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25657}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1611, 'completion_chars': 7268, 'completion_tokens': 2130, 'elapsed_seconds': 42.83220653235912, 'estimated_completion_tokens': 1817, 'estimated_prompt_tokens': 51847, 'estimated_total_tokens': 53664, 'first_chunk_seconds': 13.741748459171504, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 207385, 'prompt_tokens': 43561, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 45691}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 771, 'completion_chars': 3527, 'completion_tokens': 1047, 'elapsed_seconds': 21.98019450902939, 'estimated_completion_tokens': 882, 'estimated_prompt_tokens': 36183, 'estimated_total_tokens': 37065, 'first_chunk_seconds': 8.0223568379879, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 144729, 'prompt_tokens': 28872, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 29919}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2829, 'completion_chars': 11520, 'completion_tokens': 3348, 'elapsed_seconds': 62.70978464093059, 'estimated_completion_tokens': 2880, 'estimated_prompt_tokens': 22620, 'estimated_total_tokens': 25500, 'first_chunk_seconds': 11.4794512828812, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 90477, 'prompt_tokens': 22048, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25396}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1864, 'completion_chars': 8747, 'completion_tokens': 2383, 'elapsed_seconds': 47.78343749605119, 'estimated_completion_tokens': 2187, 'estimated_prompt_tokens': 24410, 'estimated_total_tokens': 26597, 'first_chunk_seconds': 14.156339621171355, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 97637, 'prompt_tokens': 23984, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26367}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`69/16`，missing=`<none>`。
- repairs：`4/6` accepted；scenario_history=`11`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
