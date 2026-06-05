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
| Git commit | `7aa90ff3f2b6d19cc67bee25f19c9b340fe925f4` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:96664ae396e6987ee2972e64c90f660b2ea3ffea03fc8df418d9aa53f932133e", "iteration": 3, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:6b670df7ed470bee2feb8d100c847b4ee02dcf1c89aa7822180b7c05fff5d25a", "iteration": 3, "repair_history_index": 3, "rework_instructions": ["Preserve the current candidate's removal of the four PumpFault-specific backManual self-transitions; do not reintroduce the PumpFault latch for `CA_backManual`, `CB_backManual`, `CP_backManual`, or `CC_backManual`, because the active hard scenario requires the global backManual fallback from PumpFault to reach `Manual`.", "Add a concrete fault-removal path that remains available after a backManual fallback has already moved the machine from `PumpFault` to `Manual`. Minimal acceptable edit: add a `Manual -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_signal = 0; display_error = 0; sound_error = 0; };` transition, or an equivalent DSL mechanism, so the NL-required caregiver fault-removal step can clear the active fault/alarm/error variables even after cross-component fallback enters Manual.", "Keep the existing `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_signal = 0; display_error = 0; sound_error = 0; };` path for the case where the caregiver removes the fault before any backManual fallback.", "Do not change or delete the required `[ * ] -> Manual;` initial transition, `AutocontrolNormal -> PumpFault : if [pump_fault > 0];` guard, required states, required variables, required events, Manual.during outputs, AutocontrolNormal nonnegative infusion-rate clamp, or the AutocontrolInit `TerminateAC` ordering repair."], "same_as_final": false, "sl10_decision": "rework"}, "matching_repair_history_indices": [4], "repair_history_index": 4, "selected_source_stage": "SD-6", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sl9_rework, ... +2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 705305, 'completion_tokens': 57487, 'total_tokens': 762792, 'estimated_prompt_tokens': 805129, 'estimated_completion_tokens': 42141, 'estimated_total_tokens': 847270, 'prompt_chars': 3220490, 'completion_chars': 168544, 'n_calls': 18, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`1101.866s` |
| run record | [`pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:8a55d8d0f3adad44c29a53285e6a176963db609f277dba447131e919deb1c4bb` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `100` |
| `langgraph_node_trace_hash` | `sha256:3e71c44f7a4a3acf7ca838eb901b2d1b9e5eb2ccf3cc56b41d87b67cf00caa65` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `100` |

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
def int algorithm_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int display_error = 0;
def int sound_error = 0;
def int log_count = 0;
def float blood_pressure = 120.0;
def float sensor_buffer_bp = 120.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float default_flow_rate = 1.0;
def float builtin_switch_speed = 0.0;
def float pump_speed = 0.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;

state CARA {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            algorithm_control = 0;
            control_voltage = 0.0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            pump_speed = builtin_switch_speed;
            infusion_rate = default_flow_rate;
        }
    }

    state Ask_StartAC {
        enter {
            algorithm_control = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    if [default_flow_rate - ((blood_pressure - target_bp) / 10.0) < 0.0] {
                        infusion_rate = 0.0;
                    } else {
                        infusion_rate = default_flow_rate - ((blood_pressure - target_bp) / 10.0);
                    }
                } else if [blood_pressure < target_bp] {
                    infusion_rate = default_flow_rate + ((target_bp - blood_pressure) / 10.0);
                } else {
                    infusion_rate = default_flow_rate;
                }
                control_voltage = infusion_rate;
                log_count = log_count + 1;
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            display_error = 1;
            sound_error = 1;
            algorithm_control = 0;
            control_voltage = 0.0;
            CA_mode = 0;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Manual -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
        display_error = 0;
        sound_error = 0;
    };
    Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
        target_bp = requested_target_bp;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
        display_error = 0;
        sound_error = 0;
    };
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=13445 | 生成初始 DSL 与 grounding seeds | initial len=2897 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=4, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138400 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=277823 | LLM per-request accept/reject + repair | candidate len=2897,3276,3272,3088,3243 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=273607 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=4, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138400 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=59517 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=277823 | LLM per-request accept/reject + repair | candidate len=2897,3276,3272,3088,3243 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=273607 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=4, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=277823 | LLM per-request accept/reject + repair | candidate len=2897,3276,3272,3088,3243 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=273607 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=4, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138400 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138400 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=277823 | LLM per-request accept/reject + repair | candidate len=2897,3276,3272,3088,3243 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=273607 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=277823 | LLM per-request accept/reject + repair | candidate len=2897,3276,3272,3088,3243 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=273607 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=4, advisory=24, info=1; blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=138400 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=59517 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-clean-20260606T050000Z-4d98fe33.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T20:28:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T20:28:18Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T20:28:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T20:28:18Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T20:30:27Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T20:30:27Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2897,hash=sha256:3bef316f8581 |
| 7 | `2026-06-05T20:30:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T20:30:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T20:30:27Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:3bef316f858170d94de421bb8cdff399d488b9b33e6de3fc9a9182e89b4f4892 |
| 10 | `2026-06-05T20:30:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T20:30:27Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2897,hash=sha256:3bef316f8581, current_hash=sha256:3bef316f858170d94de421bb8cdff399d488b9b33e6de3fc9a9182e89b4f4892 |
| 12 | `2026-06-05T20:30:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T20:30:27Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T20:30:27Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T20:30:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T20:30:27Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T20:30:27Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T20:30:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T20:30:27Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T20:30:27Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T20:30:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T20:30:27Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T20:31:59Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T20:31:59Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T20:32:00Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T20:32:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T20:32:00Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T20:32:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T20:32:00Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T20:32:00Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 31 | `2026-06-05T20:32:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T20:32:00Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 10, "n_scenarios_passed": 9, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 33 | `2026-06-05T20:32:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 34 | `2026-06-05T20:32:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T20:32:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 36 | `2026-06-05T20:32:00Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 10, "n_scenarios_passed": 9, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2897,hash=sha256:3bef316f8581 |
| 37 | `2026-06-05T20:32:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 38 | `2026-06-05T20:32:00Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 39 | `2026-06-05T20:32:00Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 40 | `2026-06-05T20:32:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T20:32:00Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2897,hash=sha256:3bef316f8581 |
| 42 | `2026-06-05T20:32:30Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 43 | `2026-06-05T20:32:30Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-384f788c73"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2897,hash=sha256:48ce567f26a8 |
| 44 | `2026-06-05T20:32:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T20:32:30Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 46 | `2026-06-05T20:32:30Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:48ce567f26a88754ade6860491bdaa7d3b81aaa05a8840142354e26511c6634f |
| 47 | `2026-06-05T20:32:51Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 48 | `2026-06-05T20:32:51Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 49 | `2026-06-05T20:32:51Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 50 | `2026-06-05T20:32:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 51 | `2026-06-05T20:32:51Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2897,hash=sha256:48ce567f26a8 |
| 52 | `2026-06-05T20:32:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 53 | `2026-06-05T20:32:51Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:48ce567f26a88754ade6860491bdaa7d3b81aaa05a8840142354e26511c6634f |
| 54 | `2026-06-05T20:32:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 55 | `2026-06-05T20:32:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 56 | `2026-06-05T20:32:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 57 | `2026-06-05T20:32:51Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:48ce567f26a88754ade6860491bdaa7d3b81aaa05a8840142354e26511c6634f |
| 58 | `2026-06-05T20:32:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 59 | `2026-06-05T20:32:51Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=2897,hash=sha256:48ce567f26a8, current_hash=sha256:48ce567f26a88754ade6860491bdaa7d3b81aaa05a8840142354e26511c6634f |
| 60 | `2026-06-05T20:32:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 61 | `2026-06-05T20:32:51Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 62 | `2026-06-05T20:32:51Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 63 | `2026-06-05T20:32:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 64 | `2026-06-05T20:32:51Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 65 | `2026-06-05T20:32:51Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 66 | `2026-06-05T20:32:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 67 | `2026-06-05T20:32:51Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 68 | `2026-06-05T20:32:51Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-5A", "ok": true, "status": "StageStatus.OK"} | <none> |
| 69 | `2026-06-05T20:32:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 70 | `2026-06-05T20:32:51Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 targeted_retry", "ok": false, "reason": "reuse_frozen_scenario_set"} | <none> |
| 71 | `2026-06-05T20:32:51Z` | `<control>` | `1` | `frozen_scenario_refresh_targeted_retry` | {} | <none> |
| 72 | `2026-06-05T20:32:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 73 | `2026-06-05T20:32:51Z` | `SL-5` | `1` | `stage_enter` | {"reason": "targeted_refresh_after_frozen_gap_or_dsl_change"} | <none> |
| 74 | `2026-06-05T20:34:10Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 75 | `2026-06-05T20:34:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 76 | `2026-06-05T20:34:10Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 77 | `2026-06-05T20:34:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 78 | `2026-06-05T20:34:10Z` | `SC-5F` | `1` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": "refreshed_scenario_set"} | <none> |
| 79 | `2026-06-05T20:34:10Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 80 | `2026-06-05T20:34:10Z` | `SD-6` | `1` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
- ……另有 `176` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-6` | yes | fixbatch-0-sha256-5adbf9ad4d9 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SL-7` | yes | fixbatch-1-sha256-cf1b721020a / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; forced_transition_count_drift; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SD-4` | yes | fixbatch-2-sha256-e21e419746a / n=4 | accept=4, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `SD-6` | yes | fixbatch-3-sha256-c6b1e41b901 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 4 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|
| `default_init_manual_outputs` | default-init: first empty cycle dispatches to Manual and checks manual-mode pump speed, default flow, and sensor buffer ...<truncated 12 chars> | ✅ | ✅ | ✅ | ✅ |
| `initiate_change_start_to_normal` | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC into AutocontrolInit, then comple...<truncated 67 chars> | ✅ | ✅ | ✅ | ✅ |
| `terminate_from_ask_and_init` | explicit-hot-start: TerminateAC returns both Ask_StartAC and AutocontrolInit paths to Manual and releases algorithmic co...<truncated 6 chars> | ❌ | ✅ | ✅ | ✅ |
| `terminate_from_normal_manual_recovery` | explicit-hot-start: TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-output behavior. | ✅ | ✅ | ✅ | ✅ |
| `autocontrol_no_fault_continues` | explicit-hot-start: with no pump-operation complication, AutocontrolNormal stays active, controls flow, writes sensor bu...<truncated 20 chars> | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_enters_alarm_state` | explicit-hot-start: pump_fault present at AutocontrolNormal cycle start triggers PumpFault, activates alarms/errors, and...<truncated 27 chars> | ✅ | ✅ | ✅ | ✅ |
| `fault_removed_returns_manual` | explicit-hot-start: after caregiver removes the pump fault, FaultRemoved returns to Manual and clears fault/alarm/error ...<truncated 8 chars> | ✅ | ✅ | ✅ | ✅ |
| `ca_forced_backmanual_from_init` | explicit-hot-start: CA_backManual is a cross-component forced fallback from AutocontrolInit to Manual with CA_mode becom...<truncated 11 chars> | ✅ | ✅ | ✅ | ✅ |
| `cb_cp_forced_backmanual_from_distinct_modes` | explicit-hot-start: CB_backManual and CP_backManual each force recovery to Manual from different concrete autocontrol-re...<truncated 13 chars> | ✅ | ✅ | ✅ | ✅ |
| `cc_forced_backmanual_from_pumpfault` | explicit-hot-start: CC_backManual forced fallback from PumpFault reaches the shared Manual recovery target and makes CA_...<truncated 12 chars> | ✅ | ✅ | ❌ | ✅ |
| `pump_fault_alarm_and_fault_removed_recovery` | explicit-hot-start: pump_fault at AutocontrolNormal cycle start triggers PumpFault alarms and FaultRemoved returns to Ma...<truncated 35 chars> | ⚪ | ✅ | ✅ | ✅ |
| `ca_cb_cp_forced_backmanual_from_distinct_modes` | explicit-hot-start: CA_backManual, CB_backManual, and CP_backManual each force recovery to Manual from distinct autocont...<truncated 19 chars> | ⚪ | ✅ | ✅ | ✅ |
| `direct_startac_wrong_target_probe` | explicit-hot-start: direct StartAC probe asserts the NL-required target AutocontrolInit, catching a wrong-target mutatio...<truncated 36 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `direct_forced_backmanual_missing_line_probe` | explicit-hot-start: direct forced-fallback probe from AutocontrolNormal asserts CB_backManual cannot be ignored and must...<truncated 23 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `direct_initiateac_wrong_target_probe` | explicit-hot-start: direct InitiateAC probe asserts Manual transitions specifically to Ask_StartAC, catching a wrong-tar...<truncated 58 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `cp_forced_backmanual_from_init_missing_line_probe` | explicit-hot-start: direct CP_backManual forced-line probe from AutocontrolInit must preempt normal completion and force...<truncated 60 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `manual_faultremoved_clears_fault_effect_probe` | explicit-hot-start: FaultRemoved in Manual must remain in Manual and clear pump fault, alarm, display, and sound flags, ...<truncated 73 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `change_setpoint_effect_value_probe` | explicit-hot-start: ChangeSetpoint self-transition in Ask_StartAC must copy requested_target_bp exactly into target_bp, ...<truncated 61 chars> | ⚪ | ⚪ | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_outputs` — default-init: first empty cycle dispatches to Manual and checks manual-mode pump speed, default flow, and sensor buffer obligations.</summary>

| Field | Value |
|---|---|
| description | default-init: first empty cycle dispatches to Manual and checks manual-mode pump speed, default flow, and sensor buffer obligations. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 130.0, "builtin_switch_speed": 2.5, "default_flow_rate": 3.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_after_initial_dispatch` | `0` | `[]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 3.0, "pump_speed": 2.5, "sensor_buffer_bp": 130.0}` |

</details>

<details><summary>`initiate_change_start_to_normal` — default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC into AutocontrolInit, then completion reaches AutocontrolNormal with lowe...<truncated 27 chars></summary>

| Field | Value |
|---|---|
| description | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC into AutocontrolInit, then completion reaches AutocontrolNormal with lower flow for higher pressure. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 120.0, "default_flow_rate": 2.0, "log_count": 0, "pump_fault": 0, "requested_target_bp": 110.0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_ready` | `0` | `[]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0}` |
| 1 `initiate_enters_ask_startac` | `0` | `["InitiateAC"]` | `CARA.Ask_StartAC` | `{"algorithm_control": 0, "sensor_buffer_bp": 120.0}` |
| 2 `change_setpoint_updates_target` | `0` | `["ChangeSetpoint"]` | `CARA.Ask_StartAC` | `{"sensor_buffer_bp": 120.0, "target_bp": 110.0}` |
| 3 `startac_enters_autocontrol_init` | `0` | `["StartAC"]` | `CARA.AutocontrolInit` | `{"CA_mode": 1, "algorithm_control": 1, "sensor_buffer_bp": 120.0}` |
| 4 `completion_enters_autocontrol_normal` | `0` | `[]` | `CARA.AutocontrolNormal` | `{"CA_mode": 1, "algorithm_control": 1, "control_voltage": 1.0, "infusion_rate": 1.0, "log_count": 1, "sensor_buffer_bp": 120.0}` |

</details>

<details><summary>`terminate_from_ask_and_init` — explicit-hot-start: TerminateAC returns both Ask_StartAC and AutocontrolInit paths to Manual and releases algorithmic control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: TerminateAC returns both Ask_StartAC and AutocontrolInit paths to Manual and releases algorithmic control. |
| initial_state | `CARA.Ask_StartAC` |
| initial_vars | `{"algorithm_control": 0, "blood_pressure": 118.0, "builtin_switch_speed": 1.5, "default_flow_rate": 2.2}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_from_ask_to_manual` | `0` | `["TerminateAC"]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 2.2, "pump_speed": 1.5}` |
| 1 `reenter_ask` | `0` | `["InitiateAC"]` | `CARA.Ask_StartAC` | `{"algorithm_control": 0, "sensor_buffer_bp": 118.0}` |
| 2 `start_to_init` | `0` | `["StartAC"]` | `CARA.AutocontrolInit` | `{"CA_mode": 1, "algorithm_control": 1}` |
| 3 `terminate_from_init_to_manual` | `0` | `["TerminateAC"]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 2.2, "pump_speed": 1.5}` |

</details>

<details><summary>`terminate_from_normal_manual_recovery` — explicit-hot-start: TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-output behavior.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-output behavior. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "algorithm_control": 1, "blood_pressure": 90.0, "builtin_switch_speed": 4.0, "control_voltage": 2.0, "default_flow_rate": 1.0, "pump_fault": 0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_normal_to_manual` | `0` | `["TerminateAC"]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 1.0, "pump_speed": 4.0, "sensor_buffer_bp": 90.0}` |

</details>

<details><summary>`autocontrol_no_fault_continues` — explicit-hot-start: with no pump-operation complication, AutocontrolNormal stays active, controls flow, writes sensor buffer, and logs data.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: with no pump-operation complication, AutocontrolNormal stays active, controls flow, writes sensor buffer, and logs data. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"blood_pressure": 100.0, "default_flow_rate": 1.0, "log_count": 5, "pump_fault": 0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_fault_no_transition` | `0` | `[]` | `CARA.AutocontrolNormal` | `{"control_voltage": 1.0, "infusion_rate": 1.0, "log_count": 6, "sensor_buffer_bp": 100.0}` |

</details>

<details><summary>`pump_fault_enters_alarm_state` — explicit-hot-start: pump_fault present at AutocontrolNormal cycle start triggers PumpFault, activates alarms/errors, and releases software control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: pump_fault present at AutocontrolNormal cycle start triggers PumpFault, activates alarms/errors, and releases software control. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "algorithm_control": 1, "control_voltage": 3.0, "display_error": 0, "pump_fault": 1, "sound_error": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_transition_to_pumpfault` | `0` | `[]` | `CARA.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "algorithm_control": 0, "control_voltage": 0.0, "display_error": 1, "sound_error": 1}` |

</details>

<details><summary>`fault_removed_returns_manual` — explicit-hot-start: after caregiver removes the pump fault, FaultRemoved returns to Manual and clears fault/alarm/error outputs.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: after caregiver removes the pump fault, FaultRemoved returns to Manual and clears fault/alarm/error outputs. |
| initial_state | `CARA.PumpFault` |
| initial_vars | `{"alarm_signal": 1, "blood_pressure": 115.0, "builtin_switch_speed": 1.8, "default_flow_rate": 2.4, "display_error": 1, "pump_fault": 1, "sound_error": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_removed_manual` | `0` | `["FaultRemoved"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "algorithm_control": 0, "control_voltage": 0.0, "display_error": 0, "infusion_rate": 2.4, "pump_fault": 0, "pump_speed": 1.8, "sensor_buffer_bp": 115.0, "sound_error": 0}` |

</details>

<details><summary>`ca_forced_backmanual_from_init` — explicit-hot-start: CA_backManual is a cross-component forced fallback from AutocontrolInit to Manual with CA_mode becoming Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CA_backManual is a cross-component forced fallback from AutocontrolInit to Manual with CA_mode becoming Manual. |
| initial_state | `CARA.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "algorithm_control": 1, "blood_pressure": 122.0, "builtin_switch_speed": 2.1, "control_voltage": 5.0, "default_flow_rate": 1.7}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_forces_manual` | `0` | `["CARA.CA_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 1.7, "pump_speed": 2.1, "sensor_buffer_bp": 122.0}` |

</details>

<details><summary>`cb_cp_forced_backmanual_from_distinct_modes` — explicit-hot-start: CB_backManual and CP_backManual each force recovery to Manual from different concrete autocontrol-related leaves.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CB_backManual and CP_backManual each force recovery to Manual from different concrete autocontrol-related leaves. |
| initial_state | `CARA.Ask_StartAC` |
| initial_vars | `{"blood_pressure": 119.0, "builtin_switch_speed": 2.0, "default_flow_rate": 1.3, "log_count": 0, "pump_fault": 0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_from_ask` | `0` | `["CARA.CB_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 1.3, "pump_speed": 2.0}` |
| 1 `initiate_again` | `0` | `["InitiateAC"]` | `CARA.Ask_StartAC` | `{"algorithm_control": 0}` |
| 2 `start_again_to_init` | `0` | `["StartAC"]` | `CARA.AutocontrolInit` | `{"CA_mode": 1, "algorithm_control": 1}` |
| 3 `complete_to_normal` | `0` | `[]` | `CARA.AutocontrolNormal` | `{"CA_mode": 1, "algorithm_control": 1, "log_count": 1, "sensor_buffer_bp": 119.0}` |
| 4 `cp_backmanual_from_normal` | `0` | `["CARA.CP_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 1.3, "pump_speed": 2.0}` |

</details>

<details><summary>`cc_forced_backmanual_from_pumpfault` — explicit-hot-start: CC_backManual forced fallback from PumpFault reaches the shared Manual recovery target and makes CA_mode Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CC_backManual forced fallback from PumpFault reaches the shared Manual recovery target and makes CA_mode Manual. |
| initial_state | `CARA.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "algorithm_control": 1, "blood_pressure": 125.0, "builtin_switch_speed": 3.3, "control_voltage": 4.0, "default_flow_rate": 2.6, "display_error": 1, "pump_fault": 1, "sound_error": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_backmanual_forces_manual` | `0` | `["CARA.CC_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 2.6, "pump_speed": 3.3, "sensor_buffer_bp": 125.0}` |

</details>

<details><summary>`pump_fault_alarm_and_fault_removed_recovery` — explicit-hot-start: pump_fault at AutocontrolNormal cycle start triggers PumpFault alarms and FaultRemoved returns to Manual with fault and errors cleared.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: pump_fault at AutocontrolNormal cycle start triggers PumpFault alarms and FaultRemoved returns to Manual with fault and errors cleared. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "algorithm_control": 1, "blood_pressure": 115.0, "builtin_switch_speed": 1.8, "control_voltage": 3.0, "default_flow_rate": 2.4, "display_error": 0, "pump_fault": 1, "sound_error": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_transition_to_pumpfault` | `0` | `[]` | `CARA.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "algorithm_control": 0, "control_voltage": 0.0, "display_error": 1, "sound_error": 1}` |
| 1 `fault_removed_manual` | `0` | `["FaultRemoved"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "algorithm_control": 0, "control_voltage": 0.0, "display_error": 0, "infusion_rate": 2.4, "pump_fault": 0, "pump_speed": 1.8, "sensor_buffer_bp": 115.0, "sound_error": 0}` |

</details>

<details><summary>`ca_cb_cp_forced_backmanual_from_distinct_modes` — explicit-hot-start: CA_backManual, CB_backManual, and CP_backManual each force recovery to Manual from distinct autocontrol-related leaves.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CA_backManual, CB_backManual, and CP_backManual each force recovery to Manual from distinct autocontrol-related leaves. |
| initial_state | `CARA.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "algorithm_control": 1, "blood_pressure": 122.0, "builtin_switch_speed": 2.1, "control_voltage": 5.0, "default_flow_rate": 1.7, "log_count": 0, "pump_fault": 0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_from_init` | `0` | `["CARA.CA_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 1.7, "pump_speed": 2.1, "sensor_buffer_bp": 122.0}` |
| 1 `initiate_to_ask_for_cb` | `0` | `["InitiateAC"]` | `CARA.Ask_StartAC` | `{"algorithm_control": 0, "sensor_buffer_bp": 122.0}` |
| 2 `cb_backmanual_from_ask` | `0` | `["CARA.CB_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 1.7, "pump_speed": 2.1}` |
| 3 `initiate_again` | `0` | `["InitiateAC"]` | `CARA.Ask_StartAC` | `{"algorithm_control": 0}` |
| 4 `start_again_to_init` | `0` | `["StartAC"]` | `CARA.AutocontrolInit` | `{"CA_mode": 1, "algorithm_control": 1}` |
| 5 `complete_to_normal` | `0` | `[]` | `CARA.AutocontrolNormal` | `{"CA_mode": 1, "algorithm_control": 1, "log_count": 1, "sensor_buffer_bp": 122.0}` |
| 6 `cp_backmanual_from_normal` | `0` | `["CARA.CP_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 1.7, "pump_speed": 2.1}` |

</details>

<details><summary>`direct_startac_wrong_target_probe` — explicit-hot-start: direct StartAC probe asserts the NL-required target AutocontrolInit, catching a wrong-target mutation from Ask_StartAC to another state.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: direct StartAC probe asserts the NL-required target AutocontrolInit, catching a wrong-target mutation from Ask_StartAC to another state. |
| initial_state | `CARA.Ask_StartAC` |
| initial_vars | `{"CA_mode": 0, "algorithm_control": 0, "blood_pressure": 121.0, "requested_target_bp": 105.0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `startac_target_is_autocontrol_init` | `0` | `["StartAC"]` | `CARA.AutocontrolInit` | `{"CA_mode": 1, "algorithm_control": 1, "sensor_buffer_bp": 121.0}` |

</details>

<details><summary>`direct_forced_backmanual_missing_line_probe` — explicit-hot-start: direct forced-fallback probe from AutocontrolNormal asserts CB_backManual cannot be ignored and must force Manual recovery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: direct forced-fallback probe from AutocontrolNormal asserts CB_backManual cannot be ignored and must force Manual recovery. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "algorithm_control": 1, "blood_pressure": 116.0, "builtin_switch_speed": 2.7, "control_voltage": 4.5, "default_flow_rate": 1.9, "log_count": 3, "pump_fault": 0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_from_normal_forces_manual` | `0` | `["CARA.CB_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 1.9, "pump_speed": 2.7, "sensor_buffer_bp": 116.0}` |

</details>

<details><summary>`direct_initiateac_wrong_target_probe` — explicit-hot-start: direct InitiateAC probe asserts Manual transitions specifically to Ask_StartAC, catching a wrong-target mutation of the caregiver initiate-c...<truncated 18 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: direct InitiateAC probe asserts Manual transitions specifically to Ask_StartAC, catching a wrong-target mutation of the caregiver initiate-control transition. |
| initial_state | `CARA.Manual` |
| initial_vars | `{"CA_mode": 0, "algorithm_control": 0, "blood_pressure": 117.0, "builtin_switch_speed": 2.4, "default_flow_rate": 1.6}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiateac_target_is_ask_startac` | `0` | `["InitiateAC"]` | `CARA.Ask_StartAC` | `{"algorithm_control": 0, "sensor_buffer_bp": 117.0}` |

</details>

<details><summary>`cp_forced_backmanual_from_init_missing_line_probe` — explicit-hot-start: direct CP_backManual forced-line probe from AutocontrolInit must preempt normal completion and force Manual recovery, exposing a missing for...<truncated 20 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: direct CP_backManual forced-line probe from AutocontrolInit must preempt normal completion and force Manual recovery, exposing a missing forced transition line. |
| initial_state | `CARA.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "algorithm_control": 1, "blood_pressure": 123.0, "builtin_switch_speed": 2.8, "control_voltage": 6.0, "default_flow_rate": 2.0, "log_count": 7, "pump_fault": 0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_from_init_forces_manual` | `0` | `["CARA.CP_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "algorithm_control": 0, "control_voltage": 0.0, "infusion_rate": 2.0, "pump_speed": 2.8, "sensor_buffer_bp": 123.0}` |

</details>

<details><summary>`manual_faultremoved_clears_fault_effect_probe` — explicit-hot-start: FaultRemoved in Manual must remain in Manual and clear pump fault, alarm, display, and sound flags, catching missing or wrong effect constan...<truncated 33 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: FaultRemoved in Manual must remain in Manual and clear pump fault, alarm, display, and sound flags, catching missing or wrong effect constants on the Manual self-transition. |
| initial_state | `CARA.Manual` |
| initial_vars | `{"CA_mode": 0, "alarm_signal": 1, "algorithm_control": 0, "blood_pressure": 112.0, "builtin_switch_speed": 2.2, "control_voltage": 9.0, "default_flow_rate": 1.4, "display_error": 1, "pump_fault": 1, "sound_error": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_faultremoved_effect_clears_flags` | `0` | `["FaultRemoved"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "algorithm_control": 0, "control_voltage": 0.0, "display_error": 0, "infusion_rate": 1.4, "pump_fault": 0, "pump_speed": 2.2, "sensor_buffer_bp": 112.0, "sound_error": 0}` |

</details>

<details><summary>`change_setpoint_effect_value_probe` — explicit-hot-start: ChangeSetpoint self-transition in Ask_StartAC must copy requested_target_bp exactly into target_bp, catching missing effect or wrong assigne...<truncated 21 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: ChangeSetpoint self-transition in Ask_StartAC must copy requested_target_bp exactly into target_bp, catching missing effect or wrong assigned constant mutations. |
| initial_state | `CARA.Ask_StartAC` |
| initial_vars | `{"CA_mode": 0, "algorithm_control": 0, "blood_pressure": 126.0, "requested_target_bp": 137.0, "target_bp": 95.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `changesetpoint_copies_requested_target_exactly` | `0` | `["ChangeSetpoint"]` | `CARA.Ask_StartAC` | `{"algorithm_control": 0, "sensor_buffer_bp": 126.0, "target_bp": 137.0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | terminate_from_ask_and_init | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:48ce567f26a88754ade6860491bdaa7d3b81aaa05a8840142354e26511c6634f` |
| 2 | `1` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; forced_transition_count_drift; missing_required_grou...<truncated 5 chars> | `sha256:7bf779e133e6924bf5662682bf3dfe13dc8dd437631c907942aa8b12a49f56b2` |
| 3 | `2` | ✅ | `SD-4` | W_SHADOWED_EVENT:c60af7e5d001, W_SHADOWED_EVENT:f4bb66e5dced, W_SHADOWED_EVENT:a96a0048e482, W_SHADOWED_EVENT:d2bae58d678f, W_SHADOWED_EVENT, ... +4 | accept=4, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:13a9d992112a6e2e753dd8c3ad4307b4319b669cbdb096d56eece1ababe3c3cd` |
| 4 | `3` | ❌ | `SD-6` | cc_forced_backmanual_from_pumpfault | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=True, drift=major, rework=Preserve the current candidate's removal of the four PumpFault-specific backManual self-transitions; do not reintroduce the PumpFault latch for `CA_backManual`, `CB_backManual`,...<truncated 784 chars> | `sha256:6b670df7ed470bee2feb8d100c847b4ee02dcf1c89aa7822180b7c05fff5d25a` |
| 5 | `3` | ✅ | `SD-6` | cc_forced_backmanual_from_pumpfault | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | `sha256:96664ae396e6987ee2972e64c90f660b2ea3ffea03fc8df418d9aa53f932133e` |

<details><summary>Repair 1 / iteration `0` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`terminate_from_ask_and_init`。
- before_dsl_hash：`sha256:3bef316f858170d94de421bb8cdff399d488b9b33e6de3fc9a9182e89b4f4892`；candidate_dsl_hash：`sha256:48ce567f26a88754ade6860491bdaa7d3b81aaa05a8840142354e26511c6634f`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-5adbf9ad4d9`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-384f788c73` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: TerminateAC returns both Ask_StartAC and AutocontrolInit paths to Manual and releases algorithmic control.', 'name': 'terminate_from_ask_and_init', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: TerminateAC returns both Ask_StartAC and AutocontrolInit paths to Manual and releases algorithmic control.', 'failing_steps': [{'actual_state': 'CARA.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'algorithm_control': 1, 'control_voltage': 0.40000000000000013, 'infusion_rate': 0.40000000000000013, 'pump_speed': 1.5}, 'before_cycles': 0, 'events': ['TerminateAC'], 'expected_state': 'CARA.Manual', 'expected_vars': {'CA_mode': 0, 'algorithm_control': 0, 'control_voltage': 0.0, 'infusion_rate': 2.2, 'pump_speed': 1.5}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 3, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'algorithm_control': {'actual': 1, 'expected': 0}, 'control_voltage': {'actual': 0.40000000000000013, 'expected': 0.0}, 'infusion_rate': {'actual': 0.40000000000000013, 'expected': 2.2}}}], 'initial_state': 'CARA.Ask_StartAC', 'initial_vars': {'algorithm_control': 0, 'blood_pressure': 118.0, 'builtin_switch_speed': 1.5, 'default_flow_rate': 2.2}, 'scenario_name': 'terminate_from_ask_and_init', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'algorithm_control': 0, 'blood_pressure': 118.0, 'builtin_switch_speed': 1.5, 'control_voltage': 0.0, 'default_flow_rate': 2.2, 'display_error': 0, 'infusion_rate': 2.2, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 1.5, 'requested_target_bp': 100.0, 'sensor_buffer_bp': 118.0, 'sound_error': 0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'terminate_from_ask_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'algorithm_control': 0, 'blood_pressure': 118.0, 'builtin_switch_speed': 1.5, 'control_voltage': 0.0, 'default_flow_rate': 2.2, 'display_error': 0, 'infusion_rate': 2.2, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 1.5, 'requested_target_bp': 100.0, 'sensor_buffer_bp': 118.0, 'sound_error': 0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'reenter_ask', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'algorithm_control': 1, 'blood_pressure': 118.0, 'builtin_switch_speed': 1.5, 'control_voltage': 0.0, 'default_flow_rate': 2.2, 'display_error': 0, 'infusion_rate': 2.2, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 1.5, 'requested_target_bp': 100.0, 'sensor_buffer_bp': 118.0, 'sound_error': 0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'start_to_init', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'algorithm_control': 1, 'blood_pressure': 118.0, 'builtin_switch_speed': 1.5, 'control_voltage': 0.40000000000000013, 'default_flow_rate': 2.2, 'display_error': 0, 'infusion_rate': 0.40000000000000013, 'log_count': 1, 'pump_fault': 0, 'pump_speed': 1.5, 'requested_target_bp': 100.0, 'sensor_buffer_bp': 118.0, 'sound_error': 0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 3, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'algorithm_control': {'actual': 1, 'expected': 0}, 'control_voltage': {'actual': 0.40000000000000013, 'expected': 0.0}, 'infusion_rate': {'actual': 0.40000000000000013, 'expected': 2.2}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:algorithm_control, variable:pump_fault, variable:alarm_signal, variable:display_error, variable:sound_error, variable:blood_pressure, ... +33`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2897`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-384f788c73` | `accept` | ❌ | ❌ | The failing scenario terminate_from_ask_and_init shows that a TerminateAC event injected while in CARA.AutocontrolInit is being preempted by the unconditional AutocontrolInit -> AutocontrolNormal completion transition, so the model enters AutocontrolNormal and keeps algorithmic control active instead of returning to Manual.；intent=Prioritize AutocontrolInit ...<truncated 98 chars> |
- repair_rationale：Accepted the hard simulation request for scenario terminate_from_ask_and_init.；Failing step terminate_from_init_to_manual expected CARA.Manual with CA_mode = 0, algorithm_control = 0, control_voltage = 0.0, pump_speed = 1.5, and infusion_rate = 2.2 when TerminateAC occurs in AutocontrolInit; actual behavior went to CA...<truncated 109 chars>；The smallest safe edit is to move the existing AutocontrolInit -> Manual :: TerminateAC transition before the unconditional AutocontrolInit -> AutocontrolNormal transition so the explicit termination event is honored before default completi...<truncated 3 chars>；This preserves all required grounded states, variables, events, actions, forced backManual transitions, pump fault handling, Ask_StartAC setpoint behavior, StartAC entry into AutocontrolInit, and the required AutocontrolInit -> AutocontrolN...<truncated 22 chars>；Previously passing terminate_from_ask_to_manual, reenter_ask, and start_to_init behavior is not regressed: Ask_StartAC -> Manual :: TerminateAC is unchanged, Manual -> Ask_StartAC :: InitiateAC is unchanged, and Ask_StartAC -> AutocontrolIn...<truncated 27 chars>
- diff_summary：`{"summary": "Reordered the AutocontrolInit outgoing transitions so TerminateAC to Manual is listed before the unconditional completion to AutocontrolNormal."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int algorithm_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int display_error = 0;
def int sound_error = 0;
def int log_count = 0;
def float blood_pressure = 120.0;
def float sensor_buffer_bp = 120.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float default_flow_rate = 1.0;
def float builtin_switch_speed = 0.0;
def float pump_speed = 0.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;

state CARA {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            algorithm_control = 0;
            control_voltage = 0.0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            pump_speed = builtin_switch_speed;
            infusion_rate = default_flow_rate;
        }
    }

    state Ask_StartAC {
        enter {
            algorithm_control = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    infusion_rate = default_flow_rate - ((blood_pressure - target_bp) / 10.0);
                } else if [blood_pressure < target_bp] {
                    infusion_rate = default_flow_rate + ((target_bp - blood_pressure) / 10.0);
                } else {
                    infusion_rate = default_flow_rate;
                }
                control_voltage = infusion_rate;
                log_count = log_count + 1;
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            display_error = 1;
            sound_error = 1;
            algorithm_control = 0;
            control_voltage = 0.0;
            CA_mode = 0;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
        target_bp = requested_target_bp;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
        display_error = 0;
        sound_error = 0;
    };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -93,8 +93,8 @@
     };
     Ask_StartAC -> AutocontrolInit :: StartAC;
     Ask_StartAC -> Manual :: TerminateAC;
+    AutocontrolInit -> Manual :: TerminateAC;
     AutocontrolInit -> AutocontrolNormal;
-    AutocontrolInit -> Manual :: TerminateAC;
     AutocontrolNormal -> Manual :: TerminateAC;
     AutocontrolNormal -> PumpFault : if [pump_fault > 0];
     PumpFault -> Manual :: FaultRemoved effect {
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:b910c6b96aeb4aca1956feb13b6338341699895bbe9aa9e573141b2c42309b6a`。
  - SL-10 evidence 1: `{"summary": "The hard SD-6 simulation request fixreq-0-sd6-0-384f788c73 was accepted by SL-9 and the candidate implements the accepted minimal edit: in AutocontrolInit, the explicit AutocontrolInit -> Manual :: TerminateAC transition is now listed before the unconditional AutocontrolInit -> AutocontrolNormal completion transition. This directly addresses scenario terminate_from_ask_and_init step terminate_from_init_to_manual, where TerminateAC in AutocontrolInit previously lost to the unconditional completion and produced CARA.AutocontrolNormal with CA_mode=1, algorithm_control=1, control_voltage=0.4, infusion_rate=0.4 instead of expected CARA.Manual with CA_mode=0, algorithm_control=0, cont...<truncated 53 chars>`
  - SL-10 evidence 2: `{"summary": "The edit is behaviorally narrow and preserves the NL-required structure: all required states Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault remain; all required variables remain; the required InitiateAC, ChangeSetpoint, StartAC, TerminateAC, FaultRemoved, and CA/CB/CP/CC_backManual events remain; the Manual actions for switch speed/default flow, Ask_StartAC setpoint change, StartAC entry to AutocontrolInit, normal autocontrol blood-pressure-to-flow computation, pump fault alarm/error behavior, and forced backManual shared recovery transitions are unchanged."}`
  - SL-10 evidence 3: `{"summary": "No NL-fidelity regression is introduced by the transition reordering. The NL requires that the caregiver can terminate algorithmic pump control and that manual operation is the recovery target; prioritizing TerminateAC over an unguarded completion from AutocontrolInit is consistent with that requirement and prevents the software from continuing algorithmic control after termination."}`
  - SL-10 evidence 4: `{"summary": "The local deterministic check reports no scenario regression, but rejects the candidate for missing_required_grounding on transition:initial:Manual and guard:AutocontrolNormal:pump_fault. These are not actual DSL omissions: the candidate still contains '[*] -> Manual;' and 'AutocontrolNormal -> PumpFault : if [pump_fault > 0];' exactly representing the required initial transition and pump_fault guard."}`
  - SL-10 evidence 5: `{"candidate_dsl_hash": "sha256:48ce567f26a88754ade6860491bdaa7d3b81aaa05a8840142354e26511c6634f", "covered_local_objection_kinds": ["missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:94ca51fc94c4a31e6107bc9c6e063e8ec178dc2b40e9e1d3b2b1d8cf2d21b86b", "local_override_rationale_count": 3, "local_override_rationale_hash": "sha256:f5e44d205a484a90d779f94679e24e55880f0ec2dbab7a66a3b433f7b17d22ce", "local_rejection_evidence_hash": "sha256:26affebc7fea28edf9290cca4aa870f213f0ea845b75189e0da90ba0beb7af63", "local_rejection_reason": "missing_required_grounding", "missing_local_objection_kinds": [], "policy": "SL-10 may override conservative ...<truncated 296 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial:Manual", "guard:AutocontrolNormal:pump_fault"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `1` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:48ce567f26a88754ade6860491bdaa7d3b81aaa05a8840142354e26511c6634f`；candidate_dsl_hash：`sha256:7bf779e133e6924bf5662682bf3dfe13dc8dd437631c907942aa8b12a49f56b2`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Autocontrol infusion-rate abstraction can produce negative infusion_rate/control_voltage, which is not faithful to an infusion pump that moves fluid into the patient and only states that higher pressure produces a lower flow rate.
- 2. `<unknown>` `` policy=``：Global backManual recovery can move from PumpFault to Manual without fault removal, leaving pump_fault and alarms active while Manual resumes manual pump-speed and flow behavior.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-cf1b721020a`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sl7-0-3096823055` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: "an infusion pump that moves fluid into the patient"', 'DSL AutocontrolNormal computes default_flow_rate - ((blood_pressure - target_bp) / 10.0) without lower bound.', 'sim_summary scenario cb_cp_forced_backmanual_from_distinct_modes step complete_to_normal: infusion_rate = -0.5999999999999999, control_voltage = -0.5999999999999999'], 'severity': 'major', 'summary': 'Autocontrol infusion-rate abstraction can produce negative infusion_rate/control_voltage, which is not faithful to an infusion pump that moves fluid into the patient and only states that higher pressure produces a lower flow rate.'}` |
| `fixreq-1-sl7-1-f1f2c62158` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL forced transitions: ! * -> Manual :: CA_backManual/CB_backManual/CP_backManual/CC_backManual', 'DSL Manual.during sets pump_speed and infusion_rate from manual controls.', 'sim_summary cc_forced_backmanual_from_pumpfault: Manual with pump_fault = 1 and alarm/error outputs = 1 while pump_speed = 3.3 and infusion_rate = 2.6', 'NL fault sequence requires caregiver fault removal before recovery from the pump fault path.'], 'severity': 'major', 'summary': 'Global backManual recovery can move from PumpFault to Manual without fault removal, leaving pump_fault and alarms active while Manual resumes manual pump-speed and flow behavior.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:algorithm_control, variable:pump_fault, variable:alarm_signal, variable:display_error, variable:sound_error, variable:blood_pressure, ... +33`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3276`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sl7-0-3096823055` | `accept` | ❌ | ❌ | The evidence shows AutocontrolNormal can compute a negative infusion_rate and control_voltage when blood_pressure is sufficiently above target_bp. That conflicts with the NL description of an infusion pump moving fluid into the patient and only requires higher pressure to produce a lower, not negative, flow rate.；intent=Add an explicit nonnegative lower boun...<truncated 162 chars> |
| `fixreq-1-sl7-1-f1f2c62158` | `accept` | ❌ | ❌ | The evidence shows a backManual event from PumpFault can force Manual before the caregiver removes the fault, leaving pump_fault and alarms active while Manual.during resumes manual pump-speed and flow updates. The NL fault sequence requires caregiver fault removal before recovery from the pump fault path.；intent=Add PumpFault-specific forced self-transition...<truncated 152 chars> |
- repair_rationale：For fixreq-1-sl7-0-3096823055, AutocontrolNormal still uses blood_pressure and target_bp so higher pressure lowers flow, but the high-pressure branch now saturates at infusion_rate = 0.0 when the simple abstraction would otherwise go negati...<truncated 96 chars>；For fixreq-1-sl7-1-f1f2c62158, PumpFault now has event-specific forced self-transitions for CA_backManual, CB_backManual, CP_backManual, and CC_backManual placed before the global forced recovery transitions. This prevents backManual from b...<truncated 155 chars>；The prior SD-6 repair is preserved: AutocontrolInit -> Manual :: TerminateAC remains before the unconditional AutocontrolInit -> AutocontrolNormal completion, so terminate_from_ask_and_init step terminate_from_init_to_manual should continue...<truncated 55 chars>；All required grounded states, variables, events, the initial [*] -> Manual transition, the AutocontrolNormal pump_fault guard transition, Manual.during, AutocontrolNormal.during, PumpFault.enter, and the original global forced backManual tr...<truncated 208 chars>
- diff_summary：`{"summary": "Added PumpFault-specific forced self-transitions for all backManual events before the global backManual transitions, and bounded the AutocontrolNormal high-pressure flow calculation so infusion_rate/control_voltage cannot become negative. Preserved the previous AutocontrolInit TerminateAC transition ordering fix."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int algorithm_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int display_error = 0;
def int sound_error = 0;
def int log_count = 0;
def float blood_pressure = 120.0;
def float sensor_buffer_bp = 120.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float default_flow_rate = 1.0;
def float builtin_switch_speed = 0.0;
def float pump_speed = 0.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;

state CARA {
    ! PumpFault -> PumpFault :: CA_backManual;
    ! PumpFault -> PumpFault :: CB_backManual;
    ! PumpFault -> PumpFault :: CP_backManual;
    ! PumpFault -> PumpFault :: CC_backManual;
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            algorithm_control = 0;
            control_voltage = 0.0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            pump_speed = builtin_switch_speed;
            infusion_rate = default_flow_rate;
        }
    }

    state Ask_StartAC {
        enter {
            algorithm_control = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    if [default_flow_rate - ((blood_pressure - target_bp) / 10.0) < 0.0] {
                        infusion_rate = 0.0;
                    } else {
                        infusion_rate = default_flow_rate - ((blood_pressure - target_bp) / 10.0);
                    }
                } else if [blood_pressure < target_bp] {
                    infusion_rate = default_flow_rate + ((target_bp - blood_pressure) / 10.0);
                } else {
                    infusion_rate = default_flow_rate;
                }
                control_voltage = infusion_rate;
                log_count = log_count + 1;
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            display_error = 1;
            sound_error = 1;
            algorithm_control = 0;
            control_voltage = 0.0;
            CA_mode = 0;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
        target_bp = requested_target_bp;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
        display_error = 0;
        sound_error = 0;
    };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -16,6 +16,10 @@
 def float control_voltage = 0.0;
 
 state CARA {
+    ! PumpFault -> PumpFault :: CA_backManual;
+    ! PumpFault -> PumpFault :: CB_backManual;
+    ! PumpFault -> PumpFault :: CP_backManual;
+    ! PumpFault -> PumpFault :: CC_backManual;
     ! * -> Manual :: CA_backManual;
     ! * -> Manual :: CB_backManual;
     ! * -> Manual :: CP_backManual;
@@ -64,7 +68,11 @@
             sensor_buffer_bp = blood_pressure;
             if [pump_fault == 0] {
                 if [blood_pressure > target_bp] {
-                    infusion_rate = default_flow_rate - ((blood_pressure - target_bp) / 10.0);
+                    if [default_flow_rate - ((blood_pressure - target_bp) / 10.0) < 0.0] {
+                        infusion_rate = 0.0;
+                    } else {
+                        infusion_rate = default_flow_rate - ((blood_pressure - target_bp) / 10.0);
+                    }
                 } else if [blood_pressure < target_bp] {
                     infusion_rate = default_flow_rate + ((target_bp - blood_pressure) / 10.0);
                 } else {
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:3c700de5a50778761a32363826c84908a54b1160b52c3504c9c74d5e0d2481d4`。
  - SL-10 evidence 1: `{"summary": "SL-9 accepted both hard SL-7 model-review requests, and the candidate implements the accepted edit intents. For fixreq-1-sl7-0-3096823055, AutocontrolNormal now clamps the high-pressure branch at infusion_rate = 0.0 when the prior linear abstraction would go negative, while still making higher blood pressure lower flow and still assigning control_voltage = infusion_rate and incrementing log_count. This resolves the NL-fidelity issue that an infusion pump moving fluid into the patient should not command negative infusion_rate/control_voltage."}`
  - SL-10 evidence 2: `{"summary": "For fixreq-1-sl7-1-f1f2c62158, the candidate adds PumpFault-specific forced self-transitions for CA_backManual, CB_backManual, CP_backManual, and CC_backManual before the global forced backManual transitions. This preserves all four cross-component backManual events while preventing backManual from bypassing the NL fault sequence in which the caregiver removes the fault before recovery from the pump-fault path. PumpFault -> Manual :: FaultRemoved remains the transition that clears pump_fault and alarm/error outputs."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is narrow and preserves prior accepted behavior: the earlier SD-6 repair remains in place because AutocontrolInit -> Manual :: TerminateAC is still ordered before the unconditional AutocontrolInit -> AutocontrolNormal completion. Required states Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault remain; required variables remain; required events InitiateAC, ChangeSetpoint, StartAC, TerminateAC, FaultRemoved, and all four backManual events remain; required actions for Manual, AutocontrolNormal, and PumpFault remain."}`
  - SL-10 evidence 4: `{"summary": "The local deterministic check reports no scenario regression, and the scenario set reports non-weak coverage. Its rejection is based on design/count/grounding objections rather than observed scenario failure. The substantive NL-driven hard targets are resolved by the candidate edits."}`
  - SL-10 evidence 5: `{"summary": "The complete FixLog and repair_memory show a prior SL-10 override for missing_required_grounding on transition:initial:Manual and guard:AutocontrolNormal:pump_fault. The current candidate still contains '[*] -> Manual;' and 'AutocontrolNormal -> PumpFault : if [pump_fault > 0];', so the remembered objection remains a matcher false positive, not a dropped NL-required element."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:7bf779e133e6924bf5662682bf3dfe13dc8dd437631c907942aa8b12a49f56b2", "covered_local_objection_kinds": ["new_blocking_design_diagnostic", "forced_transition_count_drift", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:9b482c1b7909e1c9c62cdf5a2ed8a18adc291acc3759911b0174af2af4672c8a", "local_override_rationale_count": 5, "local_override_rationale_hash": "sha256:af2a189b345bf949e916b2b212a9660c7ecc51b70af8f88608549d0eb76e93e8", "local_rejection_evidence_hash": "sha256:a3085d21cc0baf443f96bce14eecb903cc4257767c954ef3ff518806bcb4af46", "local_rejection_reason": "new_blocking_design_diagnostic; forced_tra...<truncated 426 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_SHADOWED_EVENT", "instance_key": "W_SHADOWED_EVENT:c60af7e5d001", "message": "Local event 'CARA.PumpFault.CA_backManual' shadows a chain event named 'CA_backManual'.", "policy_action": "requires_policy_classification", "pyfcstm_severity": "warning", "rationale": "", "refs": {"chain_path": "CARA.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.PumpFault.CA_backManual"}, "suggested_fix_hints": [{"do_not": ["...<truncated 3433 chars>
    - local evidence 2: `forced_transition_count_drift` {"fix_target": "model_review", "kind": "forced_transition_count_drift", "new": 24, "old": 20}
    - local evidence 3: `missing_required_grounding` {"element_ids": ["transition:initial:Manual", "guard:AutocontrolNormal:pump_fault"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `2` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`False`。
- problem_summary：Local event 'CARA.PumpFault.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.PumpFault.CB_backManual' shadows a chain event named 'CB_backManual'.; Local event 'CARA.PumpFault.CC_backManual' shadows a chain event named 'CC_backManual'.
- diagnostic ids：`W_SHADOWED_EVENT:c60af7e5d001, W_SHADOWED_EVENT:f4bb66e5dced, W_SHADOWED_EVENT:a96a0048e482, W_SHADOWED_EVENT:d2bae58d678f, W_SHADOWED_EVENT, W_HIGH_VAR_TO_LEAF_RATIO, W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT, I_TRANSITION_NEVER_EVENT_TRIGGERED`。
- before_dsl_hash：`sha256:7bf779e133e6924bf5662682bf3dfe13dc8dd437631c907942aa8b12a49f56b2`；candidate_dsl_hash：`sha256:13a9d992112a6e2e753dd8c3ad4307b4319b669cbdb096d56eece1ababe3c3cd`。

#### 错误证据 / diagnostics

- 1. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:c60af7e5d001` policy=`requires_policy_classification`：Local event 'CARA.PumpFault.CA_backManual' shadows a chain event named 'CA_backManual'.；refs=`{"chain_path": "CARA.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.PumpFault.CA_backManual"}`
- 2. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:f4bb66e5dced` policy=`requires_policy_classification`：Local event 'CARA.PumpFault.CB_backManual' shadows a chain event named 'CB_backManual'.；refs=`{"chain_path": "CARA.CB_backManual", "event_name": "CB_backManual", "local_path": "CARA.PumpFault.CB_backManual"}`
- 3. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:a96a0048e482` policy=`requires_policy_classification`：Local event 'CARA.PumpFault.CC_backManual' shadows a chain event named 'CC_backManual'.；refs=`{"chain_path": "CARA.CC_backManual", "event_name": "CC_backManual", "local_path": "CARA.PumpFault.CC_backManual"}`
- 4. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:d2bae58d678f` policy=`requires_policy_classification`：Local event 'CARA.PumpFault.CP_backManual' shadows a chain event named 'CP_backManual'.；refs=`{"chain_path": "CARA.CP_backManual", "event_name": "CP_backManual", "local_path": "CARA.PumpFault.CP_backManual"}`

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `CA_mode` | `unknown` | ✅ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `alarm_signal` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `algorithm_control` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `blood_pressure` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `builtin_switch_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `control_voltage` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `default_flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `display_error` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `infusion_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `log_count` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `pump_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `requested_target_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `sensor_buffer_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `sound_error` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `target_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-e21e419746a`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`4`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sd4-0-7ea5955207` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.PumpFault.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.PumpFault.CB_backManual' shadows a chain event named 'CB_backManual'.; Local event 'CARA.PumpFault.CC_backManual'...<truncated 45 chars> | `W_SHADOWED_EVENT` |
| `fixreq-2-sd4-1-2870c0a691` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.PumpFault.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.PumpFault.CB_backManual' shadows a chain event named 'CB_backManual'.; Local event 'CARA.PumpFault.CC_backManual'...<truncated 45 chars> | `W_SHADOWED_EVENT` |
| `fixreq-2-sd4-2-12bbc0ad64` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.PumpFault.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.PumpFault.CB_backManual' shadows a chain event named 'CB_backManual'.; Local event 'CARA.PumpFault.CC_backManual'...<truncated 45 chars> | `W_SHADOWED_EVENT` |
| `fixreq-2-sd4-3-6b751a6b19` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.PumpFault.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.PumpFault.CB_backManual' shadows a chain event named 'CB_backManual'.; Local event 'CARA.PumpFault.CC_backManual'...<truncated 45 chars> | `W_SHADOWED_EVENT` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 2：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 3：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 4：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:algorithm_control, variable:pump_fault, variable:alarm_signal, variable:display_error, variable:sound_error, variable:blood_pressure, ... +33`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3272`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sd4-0-7ea5955207` | `accept` | ❌ | ❌ | The diagnostic is valid for CA_backManual: the PumpFault-specific self-transition used a local event CARA.PumpFault.CA_backManual while the global recovery transition uses the broader CARA.CA_backManual event. The NL describes one cross-component CA_backManual recovery trigger, so the PumpFault latch should intercept the same root-scope event rather than int...<truncated 190 chars> |
| `fixreq-2-sd4-1-2870c0a691` | `accept` | ❌ | ❌ | The diagnostic is valid for CB_backManual: the PumpFault-specific self-transition used a local event CARA.PumpFault.CB_backManual while the global recovery transition uses the broader CARA.CB_backManual event. The NL describes one CB_backManual cross-component fallback trigger, so the PumpFault latch should intercept that same event.；intent=Change the PumpFa...<truncated 134 chars> |
| `fixreq-2-sd4-2-12bbc0ad64` | `accept` | ❌ | ❌ | The diagnostic is valid for CC_backManual: the PumpFault-specific self-transition used a local event CARA.PumpFault.CC_backManual while the global recovery transition uses the broader CARA.CC_backManual event. The NL describes one CC_backManual cross-component fallback trigger, so the PumpFault latch should intercept that same event.；intent=Change the PumpFa...<truncated 134 chars> |
| `fixreq-2-sd4-3-6b751a6b19` | `accept` | ❌ | ❌ | The diagnostic is valid for CP_backManual: the PumpFault-specific self-transition used a local event CARA.PumpFault.CP_backManual while the global recovery transition uses the broader CARA.CP_backManual event. The NL describes one CP_backManual cross-component fallback trigger, so the PumpFault latch should intercept that same event.；intent=Change the PumpFa...<truncated 134 chars> |
- repair_rationale：The smallest design repair is to keep the PumpFault-specific latch transitions but change only their trigger scope from local `::` to chain `:` for CA_backManual, CB_backManual, CP_backManual, and CC_backManual.；This resolves the W_SHADOWED_EVENT diagnostics because the PumpFault self-transitions no longer create local CARA.PumpFault.* event names that shadow the root-scope cross-component backManual events.；The previous SL-7 unsafe-recovery repair is preserved: the PumpFault-specific self-transitions remain ordered before the global forced backManual transitions, so a backManual command while in PumpFault still remains in PumpFault until Fault...<truncated 37 chars>；The prior SD-6 simulation repair is preserved: AutocontrolInit -> Manual :: TerminateAC remains before the unconditional AutocontrolInit -> AutocontrolNormal transition.；The prior NL-fidelity repair is preserved: AutocontrolNormal still clamps the high-pressure infusion-rate calculation at 0.0 so infusion_rate and control_voltage do not become negative.
- diff_summary：`{"summary": "Changed the four PumpFault-specific backManual forced self-transitions from local event scope `:: Event` to chain event scope `: Event`, eliminating shadowed local events while preserving the PumpFault latch behavior and all previous accepted repairs."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int algorithm_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int display_error = 0;
def int sound_error = 0;
def int log_count = 0;
def float blood_pressure = 120.0;
def float sensor_buffer_bp = 120.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float default_flow_rate = 1.0;
def float builtin_switch_speed = 0.0;
def float pump_speed = 0.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;

state CARA {
    ! PumpFault -> PumpFault : CA_backManual;
    ! PumpFault -> PumpFault : CB_backManual;
    ! PumpFault -> PumpFault : CP_backManual;
    ! PumpFault -> PumpFault : CC_backManual;
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            algorithm_control = 0;
            control_voltage = 0.0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            pump_speed = builtin_switch_speed;
            infusion_rate = default_flow_rate;
        }
    }

    state Ask_StartAC {
        enter {
            algorithm_control = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    if [default_flow_rate - ((blood_pressure - target_bp) / 10.0) < 0.0] {
                        infusion_rate = 0.0;
                    } else {
                        infusion_rate = default_flow_rate - ((blood_pressure - target_bp) / 10.0);
                    }
                } else if [blood_pressure < target_bp] {
                    infusion_rate = default_flow_rate + ((target_bp - blood_pressure) / 10.0);
                } else {
                    infusion_rate = default_flow_rate;
                }
                control_voltage = infusion_rate;
                log_count = log_count + 1;
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            display_error = 1;
            sound_error = 1;
            algorithm_control = 0;
            control_voltage = 0.0;
            CA_mode = 0;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
        target_bp = requested_target_bp;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
        display_error = 0;
        sound_error = 0;
    };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -16,10 +16,10 @@
 def float control_voltage = 0.0;
 
 state CARA {
-    ! PumpFault -> PumpFault :: CA_backManual;
-    ! PumpFault -> PumpFault :: CB_backManual;
-    ! PumpFault -> PumpFault :: CP_backManual;
-    ! PumpFault -> PumpFault :: CC_backManual;
+    ! PumpFault -> PumpFault : CA_backManual;
+    ! PumpFault -> PumpFault : CB_backManual;
+    ! PumpFault -> PumpFault : CP_backManual;
+    ! PumpFault -> PumpFault : CC_backManual;
     ! * -> Manual :: CA_backManual;
     ! * -> Manual :: CB_backManual;
     ! * -> Manual :: CP_backManual;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:18190cf2a7a733407bdb0b6e16fe370f5353ab14f3dbdcf55d4a916b6f8387eb`。
  - SL-10 evidence 1: `{"summary": "SL-9 accepted all four SD-4 W_SHADOWED_EVENT design requests, and the candidate implements the accepted edit intent exactly: the PumpFault-specific backManual latch transitions for CA_backManual, CB_backManual, CP_backManual, and CC_backManual were changed from local event scope `::` to chain/root event scope `:`. This removes the local CARA.PumpFault.* event shadowing while preserving the same four NL-required cross-component backManual trigger names."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves the prior hard SL-7 unsafe-recovery repair: PumpFault-specific forced self-transitions remain ordered before the global `! * -> Manual` transitions, so a backManual command received while in PumpFault is intercepted and PumpFault remains latched until `FaultRemoved` clears `pump_fault`, `alarm_signal`, `display_error`, and `sound_error`. This is grounded in the NL fault sequence: if a pump fault occurs, alarms activate, the caregiver removes the fault, and only then recovery from the pump-fault path is safe."}`
  - SL-10 evidence 3: `{"summary": "The candidate also preserves prior accepted repairs: AutocontrolInit still prioritizes `AutocontrolInit -> Manual :: TerminateAC` before the unconditional completion to AutocontrolNormal, resolving the earlier terminate_from_ask_and_init failure; AutocontrolNormal still clamps the high-pressure flow computation at 0.0, preventing negative infusion_rate/control_voltage while preserving the NL-required inverse blood-pressure-to-flow relationship."}`
  - SL-10 evidence 4: `{"summary": "All required NL-grounded structural elements remain represented: states Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault; variables including CA_mode, algorithm_control, pump_fault, alarms/errors, blood_pressure, sensor_buffer_bp, target/default flow, pump_speed, infusion_rate, control_voltage, and log_count; events InitiateAC, ChangeSetpoint, StartAC, TerminateAC, FaultRemoved, and all four backManual events; the initial transition `[ * ] -> Manual`; the AutocontrolNormal pump fault guard; Manual.during, AutocontrolNormal.during, and PumpFault.enter actions."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic evidence now reports one scenario regression, `cc_forced_backmanual_from_pumpfault`: expected `CARA.Manual` with manual pump outputs after `CARA.CC_backManual` from PumpFault, but actual was `CARA.PumpFault` with CA_mode=0, algorithm_control=0, control_voltage=0.0, fault/alarm outputs still active, and no manual pump-output update. This is the intended effect of the earlier hard NL-fidelity/unsafe-recovery repair, not a true NL-fidelity regression: the local scenario expectation reflects the pre-repair unsafe behavior that allowed backManual to bypass caregiver fault removal."}`
  - SL-10 evidence 6: `{"summary": "Local deterministic evidence also repeats missing_required_grounding for transition:initial:Manual and guard:AutocontrolNormal:pump_fault. The candidate DSL explicitly retains `[ * ] -> Manual;` and `AutocontrolNormal -> PumpFault : if [pump_fault > 0];`, so this remains the already-audited matcher false negative recorded in FixLog repair_memory rather than a dropped required element."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 12, "n_scenarios_passed": 11, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: first empty cycle dispatches to Manual and checks manual-mode pump speed, default flow, and sensor buffer obligations.", "name": "default_init_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Manual", "actual_vars": {"CA_mode": 0, "alarm_signal": 0, "algorithm_control": 0...<truncated 20367 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial:Manual", "guard:AutocontrolNormal:pump_fault"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `3` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`cc_forced_backmanual_from_pumpfault`。
- before_dsl_hash：`sha256:13a9d992112a6e2e753dd8c3ad4307b4319b669cbdb096d56eece1ababe3c3cd`；candidate_dsl_hash：`sha256:6b670df7ed470bee2feb8d100c847b4ee02dcf1c89aa7822180b7c05fff5d25a`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-c6b1e41b901`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sd6-0-102207a431` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual forced fallback from PumpFault reaches the shared Manual recovery target and makes CA_mode Manual.', 'name': 'cc_forced_backmanual_from_pumpfault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CC_backManual forced fallback from PumpFault reaches the shared Manual recovery target and makes CA_mode Manual.', 'failing_steps': [{'actual_state': 'CARA.PumpFault', 'actual_vars_focus': {'CA_mode': 0, 'algorithm_control': 0, 'control_voltage': 0.0, 'infusion_rate': 1.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0}, 'before_cycles': 0, 'events': ['CARA.CC_backManual'], 'expected_state': 'CARA.Manual', 'expected_vars': {'CA_mode': 0, 'algorithm_control': 0, 'control_voltage': 0.0, 'infusion_rate': 2.6, 'pump_speed': 3.3, 'sensor_buffer_bp': 125.0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'cc_backmanual_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'infusion_rate': {'actual': 1.0, 'expected': 2.6}, 'pump_speed': {'actual': 0.0, 'expected': 3.3}, 'sensor_buffer_bp': {'actual': 120.0, 'expected': 125.0}}}], 'initial_state': 'CARA.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 1, 'algorithm_control': 1, 'blood_pressure': 125.0, 'builtin_switch_speed': 3.3, 'control_voltage': 4.0, 'default_flow_rate': 2.6, 'display_error': 1, 'pump_fault': 1, 'sound_error': 1}, 'scenario_name': 'cc_forced_backmanual_from_pumpfault', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'algorithm_control': 0, 'blood_pressure': 125.0, 'builtin_switch_speed': 3.3, 'control_voltage': 0.0, 'default_flow_rate': 2.6, 'display_error': 1, 'infusion_rate': 1.0, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 0.0, 'requested_target_bp': 100.0, 'sensor_buffer_bp': 120.0, 'sound_error': 1, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'cc_backmanual_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'infusion_rate': {'actual': 1.0, 'expected': 2.6}, 'pump_speed': {'actual': 0.0, 'expected': 3.3}, 'sensor_buffer_bp': {'actual': 120.0, 'expected': 125.0}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:algorithm_control, variable:pump_fault, variable:alarm_signal, variable:display_error, variable:sound_error, variable:blood_pressure, ... +33`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3088`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sd6-0-102207a431` | `accept` | ❌ | ❌ | The current hard SD-6 simulation evidence reopens `cc_forced_backmanual_from_pumpfault`: with initial_state `CARA.PumpFault` and event `CARA.CC_backManual`, the scenario expects the shared Manual recovery target with `CA_mode=0`, `algorithm_control=0`, `control_voltage=0.0`, and Manual.during outputs (`sensor_buffer_bp=125.0`, `pump_speed=3.3`, `infusion_rat...<truncated 582 chars> |
- repair_rationale：Accepted the current hard simulation request `cc_forced_backmanual_from_pumpfault` despite earlier audit-only SL-10 overrides because this batch provides the active expected-vs-actual repair target. The failing step `cc_backmanual_forces_ma...<truncated 112 chars>；The variable mismatches are a consequence of staying in PumpFault: `sensor_buffer_bp` stayed 120.0 instead of updating from `blood_pressure=125.0`, `pump_speed` stayed 0.0 instead of `builtin_switch_speed=3.3`, and `infusion_rate` stayed 1....<truncated 227 chars>；The edit is minimal: it removes only the four PumpFault-specific backManual self-transitions. It preserves the required global cross-component fallback events `CA_backManual`, `CB_backManual`, `CP_backManual`, and `CC_backManual`, the initi...<truncated 266 chars>；Removing the PumpFault-specific self-interceptors also avoids the prior local shadowing/count-drift concern rather than reintroducing it. No unrelated grounded branch is deleted.
- diff_summary：`{"summary": "Removed the four PumpFault-specific forced self-transitions for backManual events so `CC_backManual` and the other cross-component backManual fallbacks from PumpFault reach the shared `Manual` recovery target via the existing global forced transitions."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int algorithm_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int display_error = 0;
def int sound_error = 0;
def int log_count = 0;
def float blood_pressure = 120.0;
def float sensor_buffer_bp = 120.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float default_flow_rate = 1.0;
def float builtin_switch_speed = 0.0;
def float pump_speed = 0.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;

state CARA {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            algorithm_control = 0;
            control_voltage = 0.0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            pump_speed = builtin_switch_speed;
            infusion_rate = default_flow_rate;
        }
    }

    state Ask_StartAC {
        enter {
            algorithm_control = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    if [default_flow_rate - ((blood_pressure - target_bp) / 10.0) < 0.0] {
                        infusion_rate = 0.0;
                    } else {
                        infusion_rate = default_flow_rate - ((blood_pressure - target_bp) / 10.0);
                    }
                } else if [blood_pressure < target_bp] {
                    infusion_rate = default_flow_rate + ((target_bp - blood_pressure) / 10.0);
                } else {
                    infusion_rate = default_flow_rate;
                }
                control_voltage = infusion_rate;
                log_count = log_count + 1;
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            display_error = 1;
            sound_error = 1;
            algorithm_control = 0;
            control_voltage = 0.0;
            CA_mode = 0;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
        target_bp = requested_target_bp;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
        display_error = 0;
        sound_error = 0;
    };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -16,10 +16,6 @@
 def float control_voltage = 0.0;
 
 state CARA {
-    ! PumpFault -> PumpFault : CA_backManual;
-    ! PumpFault -> PumpFault : CB_backManual;
-    ! PumpFault -> PumpFault : CP_backManual;
-    ! PumpFault -> PumpFault : CC_backManual;
     ! * -> Manual :: CA_backManual;
     ! * -> Manual :: CB_backManual;
     ! * -> Manual :: CP_backManual;
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:f04f3ec618b1b102a8b18ac03200e5a05f9e6f554e612c9f90e1333592523421`。
  - SL-10 evidence 1: `{"summary": "The active hard SD-6 request `cc_forced_backmanual_from_pumpfault` is behaviorally addressed by the candidate: removing the four PumpFault-specific backManual self-transitions allows the existing global `! * -> Manual` fallbacks to take `CARA.CC_backManual` from `CARA.PumpFault` to `CARA.Manual`, so Manual.enter/Manual.during can set `CA_mode=0`, release algorithmic control, set `control_voltage=0.0`, update `sensor_buffer_bp` from `blood_pressure=125.0`, set `pump_speed=3.3`, and set `infusion_rate=2.6` as the scenario expected."}`
  - SL-10 evidence 2: `{"summary": "The local deterministic rejection is not itself a reason to rework: `forced_transition_count_drift` from 24 to 20 is the expected result of removing the four PumpFault-specific forced self-transitions for the active sim repair, and the repeated `missing_required_grounding` for `transition:initial:Manual` and `guard:AutocontrolNormal:pump_fault` is still a matcher false negative because the candidate explicitly retains `[ * ] -> Manual;` and `AutocontrolNormal -> PumpFault : if [pump_fault > 0];`."}`
  - SL-10 evidence 3: `{"summary": "However, the candidate introduces an NL-fidelity regression relative to the fault-removal obligation and the prior FixLog safety discussion. If a backManual event occurs in `PumpFault`, the candidate now enters `Manual` while `pump_fault`, `alarm_signal`, `display_error`, and `sound_error` remain set, and after that transition the only existing `FaultRemoved` transition (`PumpFault -> Manual :: FaultRemoved`) is no longer reachable. This means the caregiver fault-removal step required by the NL can be lost after cross-component fallback from PumpFault."}`
  - SL-10 evidence 4: `{"summary": "The complete FixLog shows earlier SL-10 overrides treated immediate backManual-from-PumpFault recovery as unsafe because it bypassed caregiver fault removal. The current hard sim batch reopens the Manual recovery target and should be preserved, but the repaired DSL must also preserve a concrete way for the caregiver to remove/clear the fault after that fallback. The current candidate does not yet do so."}`
- SL-10 rework_instructions：Preserve the current candidate's removal of the four PumpFault-specific backManual self-transitions; do not reintroduce the PumpFault latch for `CA_backManual`, `CB_backManual`, `CP_backManual`, or `CC_backManual`, because the active hard scenario requires the global backManual fallback from PumpFault to reach `Manual`.；Add a concrete fault-removal path that remains available after a backManual fallback has already moved the machine from `PumpFault` to `Manual`. Minimal acceptable edit: add a `Manual -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_signal = 0; display_error = 0; sound_error = 0; };` transition, or an equivalent DSL mechanism, so the NL-required care...<truncated 124 chars>；Keep the existing `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_signal = 0; display_error = 0; sound_error = 0; };` path for the case where the caregiver removes the fault before any backManual fallback.；Do not change or delete the required `[ * ] -> Manual;` initial transition, `AutocontrolNormal -> PumpFault : if [pump_fault > 0];` guard, required states, required variables, required events, Manual.during outputs, AutocontrolNormal nonnegative infusion-rate clamp, or the AutocontrolInit `TerminateAC` ordering repair.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 20, "old": 24}
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial:Manual", "guard:AutocontrolNormal:pump_fault"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 5 / iteration `3` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`cc_forced_backmanual_from_pumpfault`。
- before_dsl_hash：`sha256:13a9d992112a6e2e753dd8c3ad4307b4319b669cbdb096d56eece1ababe3c3cd`；candidate_dsl_hash：`sha256:96664ae396e6987ee2972e64c90f660b2ea3ffea03fc8df418d9aa53f932133e`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-c6b1e41b901`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sd6-0-102207a431` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual forced fallback from PumpFault reaches the shared Manual recovery target and makes CA_mode Manual.', 'name': 'cc_forced_backmanual_from_pumpfault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CC_backManual forced fallback from PumpFault reaches the shared Manual recovery target and makes CA_mode Manual.', 'failing_steps': [{'actual_state': 'CARA.PumpFault', 'actual_vars_focus': {'CA_mode': 0, 'algorithm_control': 0, 'control_voltage': 0.0, 'infusion_rate': 1.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0}, 'before_cycles': 0, 'events': ['CARA.CC_backManual'], 'expected_state': 'CARA.Manual', 'expected_vars': {'CA_mode': 0, 'algorithm_control': 0, 'control_voltage': 0.0, 'infusion_rate': 2.6, 'pump_speed': 3.3, 'sensor_buffer_bp': 125.0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'cc_backmanual_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'infusion_rate': {'actual': 1.0, 'expected': 2.6}, 'pump_speed': {'actual': 0.0, 'expected': 3.3}, 'sensor_buffer_bp': {'actual': 120.0, 'expected': 125.0}}}], 'initial_state': 'CARA.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 1, 'algorithm_control': 1, 'blood_pressure': 125.0, 'builtin_switch_speed': 3.3, 'control_voltage': 4.0, 'default_flow_rate': 2.6, 'display_error': 1, 'pump_fault': 1, 'sound_error': 1}, 'scenario_name': 'cc_forced_backmanual_from_pumpfault', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'algorithm_control': 0, 'blood_pressure': 125.0, 'builtin_switch_speed': 3.3, 'control_voltage': 0.0, 'default_flow_rate': 2.6, 'display_error': 1, 'infusion_rate': 1.0, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 0.0, 'requested_target_bp': 100.0, 'sensor_buffer_bp': 120.0, 'sound_error': 1, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'cc_backmanual_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'infusion_rate': {'actual': 1.0, 'expected': 2.6}, 'pump_speed': {'actual': 0.0, 'expected': 3.3}, 'sensor_buffer_bp': {'actual': 120.0, 'expected': 125.0}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:algorithm_control, variable:pump_fault, variable:alarm_signal, variable:display_error, variable:sound_error, variable:blood_pressure, ... +33`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3243`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sd6-0-102207a431` | `accept` | ❌ | ✅ | The active hard scenario `cc_forced_backmanual_from_pumpfault` expects event `CARA.CC_backManual` from initial state `CARA.PumpFault` to reach `CARA.Manual`, with Manual.enter/Manual.during setting `CA_mode=0`, `algorithm_control=0`, `control_voltage=0.0`, `sensor_buffer_bp=125.0`, `pump_speed=3.3`, and `infusion_rate=2.6`. The prior candidate removed the Pu...<truncated 784 chars> |
- repair_rationale：For `cc_forced_backmanual_from_pumpfault`, the failing step `cc_backmanual_forces_manual` had expected state `CARA.Manual` but actual state `CARA.PumpFault`; it expected Manual outputs `sensor_buffer_bp=125.0`, `pump_speed=3.3`, and `infusi...<truncated 325 chars>；The rework guidance is preserved: the PumpFault-specific latch for `CA_backManual`, `CB_backManual`, `CP_backManual`, and `CC_backManual` is not reintroduced, so the active hard scenario remains fixed.；To preserve the NL-required caregiver fault-removal obligation after an immediate backManual fallback, the candidate adds `Manual -> Manual :: FaultRemoved` with the same clearing effect as the existing PumpFault fault-removal path. This me...<truncated 215 chars>；The existing `PumpFault -> Manual :: FaultRemoved` path is kept unchanged for the case where the caregiver removes the fault before any backManual fallback.；The local `forced_transition_count_drift` is an NL-grounded minimal structural change: the four PumpFault-specific forced self-transitions are intentionally removed to satisfy the hard Manual fallback scenario, and one ordinary Manual self-...<truncated 100 chars>
- diff_summary：`{"summary": "Removed the four PumpFault-specific forced backManual self-transitions, kept the global backManual forced fallbacks to Manual, and added a Manual self-transition on FaultRemoved to clear pump fault and alarm/error variables after fallback has already entered Manual."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int algorithm_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int display_error = 0;
def int sound_error = 0;
def int log_count = 0;
def float blood_pressure = 120.0;
def float sensor_buffer_bp = 120.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float default_flow_rate = 1.0;
def float builtin_switch_speed = 0.0;
def float pump_speed = 0.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;

state CARA {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            algorithm_control = 0;
            control_voltage = 0.0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            pump_speed = builtin_switch_speed;
            infusion_rate = default_flow_rate;
        }
    }

    state Ask_StartAC {
        enter {
            algorithm_control = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 1;
            algorithm_control = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    if [default_flow_rate - ((blood_pressure - target_bp) / 10.0) < 0.0] {
                        infusion_rate = 0.0;
                    } else {
                        infusion_rate = default_flow_rate - ((blood_pressure - target_bp) / 10.0);
                    }
                } else if [blood_pressure < target_bp] {
                    infusion_rate = default_flow_rate + ((target_bp - blood_pressure) / 10.0);
                } else {
                    infusion_rate = default_flow_rate;
                }
                control_voltage = infusion_rate;
                log_count = log_count + 1;
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            display_error = 1;
            sound_error = 1;
            algorithm_control = 0;
            control_voltage = 0.0;
            CA_mode = 0;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Manual -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
        display_error = 0;
        sound_error = 0;
    };
    Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
        target_bp = requested_target_bp;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
        display_error = 0;
        sound_error = 0;
    };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -16,10 +16,6 @@
 def float control_voltage = 0.0;
 
 state CARA {
-    ! PumpFault -> PumpFault : CA_backManual;
-    ! PumpFault -> PumpFault : CB_backManual;
-    ! PumpFault -> PumpFault : CP_backManual;
-    ! PumpFault -> PumpFault : CC_backManual;
     ! * -> Manual :: CA_backManual;
     ! * -> Manual :: CB_backManual;
     ! * -> Manual :: CP_backManual;
@@ -96,6 +92,12 @@
     }
 
     Manual -> Ask_StartAC :: InitiateAC;
+    Manual -> Manual :: FaultRemoved effect {
+        pump_fault = 0;
+        alarm_signal = 0;
+        display_error = 0;
+        sound_error = 0;
+    };
     Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
         target_bp = requested_target_bp;
     };
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:178952e0a9322dfd316ec90b4d37a69a6b91ef0acc19f2ef297b43262ed9eb02`。
  - SL-10 evidence 1: `{"summary": "The active hard request `cc_forced_backmanual_from_pumpfault` is resolved by the candidate diff: the four PumpFault-specific backManual self-transitions were removed, so the existing global forced fallbacks `! * -> Manual :: CA_backManual/CB_backManual/CP_backManual/CC_backManual` now apply from `CARA.PumpFault`. This matches the NL fallback requirement that `CA_backManual` or any of `CB_backManual`, `CP_backManual`, or `CC_backManual` causes `CA_mode` to become Manual and makes Manual the shared recovery target."}`
  - SL-10 evidence 2: `{"summary": "The prior SL-10 rework objection is directly addressed. SL-10 required preserving the PumpFault-to-Manual backManual behavior while adding a concrete way for the caregiver to clear the active fault after fallback had already moved the machine to Manual. The candidate adds `Manual -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_signal = 0; display_error = 0; sound_error = 0; };`, so the NL-required caregiver fault-removal step remains available after cross-component fallback enters Manual."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves the existing `PumpFault -> Manual :: FaultRemoved` transition with the same clearing effect, so the original fault-removal path remains available when the caregiver removes the pump fault before any backManual fallback. This preserves both NL obligations: pump fault alarms activate, the caregiver can remove the fault, and Manual remains the shared recovery target."}`
  - SL-10 evidence 4: `{"summary": "The required grounded states and variables remain present: `Manual`, `Ask_StartAC`, `AutocontrolInit`, `AutocontrolNormal`, `PumpFault`, `CA_mode`, `algorithm_control`, `pump_fault`, alarm/error variables, `blood_pressure`, `sensor_buffer_bp`, `target_bp`, `requested_target_bp`, `default_flow_rate`, `builtin_switch_speed`, `pump_speed`, `infusion_rate`, `control_voltage`, and `log_count` are all retained."}`
  - SL-10 evidence 5: `{"summary": "The required events and mode-control behavior remain present: `InitiateAC`, `ChangeSetpoint`, `StartAC`, `TerminateAC`, `FaultRemoved`, and all four backManual events remain represented; `Ask_StartAC` still permits setpoint change and StartAC entry to `AutocontrolInit`; `AutocontrolInit -> Manual :: TerminateAC` remains ordered before the unguarded completion to `AutocontrolNormal`; and `AutocontrolNormal` still clamps high-pressure flow to a nonnegative value while preserving the inverse blood-pressure-to-flow relationship."}`
  - SL-10 evidence 6: `{"summary": "Local deterministic evidence reports no scenario regression for this candidate. Its rejection is based on forced-transition count drift and repeated missing-grounding matcher objections, not on a failing simulation scenario. The behavioral repair requested by the active hard SD-6 scenario and the previous SL-10 rework guidance is implemented."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 20, "old": 24}
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial:Manual", "guard:AutocontrolNormal:pump_fault"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-5adbf9ad4d9` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-5adbf9ad4d9` | accept=1, reject=0 | `sl10_review` | `sha256:48ce567f26a88754ade6860491bdaa7d3b81aaa05a8840142354e26511c6634f` | Accepted the hard simulation request for scenario terminate_from_ask_and_init., Failing step terminate_from_init_to_manual expected CARA.Manual with CA_mode = 0, algorithm_control = 0, control_voltage = 0.0, pump_speed = 1.5, and infusion_rate = 2.2 when TerminateAC occurs in AutocontrolInit; actual behavior went to CARA.AutocontrolNormal with CA_mode = 1, algorithm_control = 1, control_voltage = 0.4, and infusion_rate = 0.4., The smallest safe edit is to move the existing AutocontrolInit -> Manual :: TerminateAC transition before the unconditional AutocontrolInit -> AutocontrolNormal transition so the explicit termination event is honored before default completion., ... +2 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-5adbf9ad4d9` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:48ce567f26a88754ade6860491bdaa7d3b81aaa05a8840142354e26511c6634f` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-cf1b721020a` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-cf1b721020a` | accept=2, reject=0 | `sl10_review` | `sha256:7bf779e133e6924bf5662682bf3dfe13dc8dd437631c907942aa8b12a49f56b2` | For fixreq-1-sl7-0-3096823055, AutocontrolNormal still uses blood_pressure and target_bp so higher pressure lowers flow, but the high-pressure branch now saturates at infusion_rate = 0.0 when the simple abstraction would otherwise go negative. control_voltage remains assigned from infusion_rate, so it is also nonnegative in that case., For fixreq-1-sl7-1-f1f2c62158, PumpFault now has event-specific forced self-transitions for CA_backManual, CB_backManual, CP_backManual, and CC_backManual placed before the global forced recovery transitions. This prevents backManual from bypassing the NL-required caregiver fault-removal step; PumpFault -> Manual :: FaultRemoved remains the path that clears pump_fault and alarm/error outputs., The prior SD-6 repair is preserved: AutocontrolInit -> Manual :: TerminateAC remains before the unconditional AutocontrolInit -> AutocontrolNormal completion, so terminate_from_ask_and_init step terminate_from_init_to_manual should continue to return to Manual with algorithmic control released., ... +1 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-cf1b721020a` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:7bf779e133e6924bf5662682bf3dfe13dc8dd437631c907942aa8b12a49f56b2` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +6 |
| 7 | `2` | `request_batch` | `fixbatch-2-sha256-e21e419746a` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 8 | `2` | `sl9_decision` | `fixbatch-2-sha256-e21e419746a` | accept=4, reject=0 | `sl10_review` | `sha256:13a9d992112a6e2e753dd8c3ad4307b4319b669cbdb096d56eece1ababe3c3cd` | The smallest design repair is to keep the PumpFault-specific latch transitions but change only their trigger scope from local `::` to chain `:` for CA_backManual, CB_backManual, CP_backManual, and CC_backManual., This resolves the W_SHADOWED_EVENT diagnostics because the PumpFault self-transitions no longer create local CARA.PumpFault.* event names that shadow the root-scope cross-component backManual events., The previous SL-7 unsafe-recovery repair is preserved: the PumpFault-specific self-transitions remain ordered before the global forced backManual transitions, so a backManual command while in PumpFault still remains in PumpFault until FaultRemoved clears pump_fault and alarms., ... +3 |
| 9 | `2` | `sl10_review` | `fixbatch-2-sha256-e21e419746a` | accept=4, reject=0 | `sc11_accept_then_sd2` | `sha256:13a9d992112a6e2e753dd8c3ad4307b4319b669cbdb096d56eece1ababe3c3cd` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +6 |
| 10 | `3` | `request_batch` | `fixbatch-3-sha256-c6b1e41b901` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 11 | `3` | `sl9_decision` | `fixbatch-3-sha256-c6b1e41b901` | accept=1, reject=0 | `sl10_review` | `sha256:6b670df7ed470bee2feb8d100c847b4ee02dcf1c89aa7822180b7c05fff5d25a` | Accepted the current hard simulation request `cc_forced_backmanual_from_pumpfault` despite earlier audit-only SL-10 overrides because this batch provides the active expected-vs-actual repair target. The failing step `cc_backmanual_forces_manual` expected `CARA.Manual` after `CARA.CC_backManual` from `CARA.PumpFault`; actual remained `CARA.PumpFault`., The variable mismatches are a consequence of staying in PumpFault: `sensor_buffer_bp` stayed 120.0 instead of updating from `blood_pressure=125.0`, `pump_speed` stayed 0.0 instead of `builtin_switch_speed=3.3`, and `infusion_rate` stayed 1.0 instead of `default_flow_rate=2.6`. By allowing the global backManual forced transition to enter Manual, `Manual.enter` releases algorithmic control and `Manual.during` updates those manual-output variables in the same cycle., The edit is minimal: it removes only the four PumpFault-specific backManual self-transitions. It preserves the required global cross-component fallback events `CA_backManual`, `CB_backManual`, `CP_backManual`, and `CC_backManual`, the initial `[ * ] -> Manual` behavior, all required states and variables, the `AutocontrolNormal -> PumpFault : if [pump_fault > 0]` complication guard, the `FaultRemoved` recovery path, the TerminateAC ordering repair, and the nonnegative high-pressure infusion-rate clamp., ... +1 |
| 12 | `3` | `sl10_review` | `fixbatch-3-sha256-c6b1e41b901` | accept=1, reject=0 | `sl9_rework` | `sha256:6b670df7ed470bee2feb8d100c847b4ee02dcf1c89aa7822180b7c05fff5d25a` | Preserve the current candidate's removal of the four PumpFault-specific backManual self-transitions; do not reintroduce the PumpFault latch for `CA_backManual`, `CB_backManual`, `CP_backManual`, or `CC_backManual`, because the active hard scenario requires the global backManual fallback from PumpFault to reach `Manual`., Add a concrete fault-removal path that remains available after a backManual fallback has already moved the machine from `PumpFault` to `Manual`. Minimal acceptable edit: add a `Manual -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_signal = 0; display_error = 0; sound_error = 0; };` transition, or an equivalent DSL mechanism, so the NL-required caregiver fault-removal step can clear the active fault/alarm/error variables even after cross-component fallback enters Manual., Keep the existing `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_signal = 0; display_error = 0; sound_error = 0; };` path for the case where the caregiver removes the fault before any backManual fallback., ... +13 |
| 13 | `3` | `sl9_rework_decision` | `fixbatch-3-sha256-c6b1e41b901` | accept=1, reject=0 | `sl10_review` | `sha256:96664ae396e6987ee2972e64c90f660b2ea3ffea03fc8df418d9aa53f932133e` | For `cc_forced_backmanual_from_pumpfault`, the failing step `cc_backmanual_forces_manual` had expected state `CARA.Manual` but actual state `CARA.PumpFault`; it expected Manual outputs `sensor_buffer_bp=125.0`, `pump_speed=3.3`, and `infusion_rate=2.6`, but actual values stayed stale because PumpFault was still active. Removing the four PumpFault-specific backManual self-transitions lets the existing global `! * -> Manual :: CC_backManual` fallback reach Manual from PumpFault, causing Manual.enter and Manual.during to produce the expected state and variables., The rework guidance is preserved: the PumpFault-specific latch for `CA_backManual`, `CB_backManual`, `CP_backManual`, and `CC_backManual` is not reintroduced, so the active hard scenario remains fixed., To preserve the NL-required caregiver fault-removal obligation after an immediate backManual fallback, the candidate adds `Manual -> Manual :: FaultRemoved` with the same clearing effect as the existing PumpFault fault-removal path. This means that if fallback enters Manual while `pump_fault` and alarm/error indicators are still active, the caregiver can still remove the fault and clear `pump_fault`, `alarm_signal`, `display_error`, and `sound_error`., ... +6 |
| 14 | `3` | `sl10_rework_review` | `fixbatch-3-sha256-c6b1e41b901` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:96664ae396e6987ee2972e64c90f660b2ea3ffea03fc8df418d9aa53f932133e` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4977, 'completion_chars': 19289, 'completion_tokens': 6995, 'elapsed_seconds': 128.56063999599428, 'estimated_completion_tokens': 4823, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11480, 'first_chunk_seconds': 38.82253131098696, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13445}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3304, 'completion_chars': 13040, 'completion_tokens': 4859, 'elapsed_seconds': 91.75104961299803, 'estimated_completion_tokens': 3260, 'estimated_prompt_tokens': 14756, 'estimated_total_tokens': 18016, 'first_chunk_seconds': 32.22256154200295, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 59021, 'prompt_tokens': 14535, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 19394}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1290, 'completion_chars': 5138, 'completion_tokens': 1505, 'elapsed_seconds': 29.85898829199141, 'estimated_completion_tokens': 1285, 'estimated_prompt_tokens': 24198, 'estimated_total_tokens': 25483, 'first_chunk_seconds': 6.62985203898279, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 96789, 'prompt_tokens': 22759, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24264}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 751, 'completion_chars': 3472, 'completion_tokens': 983, 'elapsed_seconds': 21.22771897999337, 'estimated_completion_tokens': 868, 'estimated_prompt_tokens': 22182, 'estimated_total_tokens': 23050, 'first_chunk_seconds': 7.622811181994621, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 88728, 'prompt_tokens': 20353, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21336}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3180, 'completion_chars': 12550, 'completion_tokens': 4217, 'elapsed_seconds': 78.42305350999231, 'estimated_completion_tokens': 3138, 'estimated_prompt_tokens': 18793, 'estimated_total_tokens': 21931, 'first_chunk_seconds': 21.084508683998138, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 75169, 'prompt_tokens': 18837, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23054}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2124, 'completion_chars': 9859, 'completion_tokens': 3161, 'elapsed_seconds': 59.68222833200707, 'estimated_completion_tokens': 2465, 'estimated_prompt_tokens': 22614, 'estimated_total_tokens': 25079, 'first_chunk_seconds': 21.370641943998635, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 90456, 'prompt_tokens': 22886, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26047}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1591, 'completion_chars': 6718, 'completion_tokens': 2618, 'elapsed_seconds': 52.382802972977515, 'estimated_completion_tokens': 1680, 'estimated_prompt_tokens': 48653, 'estimated_total_tokens': 50333, 'first_chunk_seconds': 23.678696616989328, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 194611, 'prompt_tokens': 45010, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 47628}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 978, 'completion_chars': 4803, 'completion_tokens': 2015, 'elapsed_seconds': 40.5550736959849, 'estimated_completion_tokens': 1201, 'estimated_prompt_tokens': 51027, 'estimated_total_tokens': 52228, 'first_chunk_seconds': 22.839005634974455, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 204105, 'prompt_tokens': 46065, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 48080}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1882, 'completion_chars': 7822, 'completion_tokens': 2266, 'elapsed_seconds': 44.51654496698757, 'estimated_completion_tokens': 1956, 'estimated_prompt_tokens': 107228, 'estimated_total_tokens': 109184, 'first_chunk_seconds': 10.506504816992674, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 428912, 'prompt_tokens': 92005, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 94271}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1161, 'completion_chars': 5426, 'completion_tokens': 2132, 'elapsed_seconds': 42.183473492012126, 'estimated_completion_tokens': 1357, 'estimated_prompt_tokens': 121688, 'estimated_total_tokens': 123045, 'first_chunk_seconds': 21.11740766200819, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 486750, 'prompt_tokens': 101857, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 103989}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4996, 'completion_chars': 19704, 'completion_tokens': 5515, 'elapsed_seconds': 101.5773913890007, 'estimated_completion_tokens': 4926, 'estimated_prompt_tokens': 26225, 'estimated_total_tokens': 31151, 'first_chunk_seconds': 11.480444137006998, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 104900, 'prompt_tokens': 26416, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 31931}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3614, 'completion_chars': 13828, 'completion_tokens': 4512, 'elapsed_seconds': 83.70846537698526, 'estimated_completion_tokens': 3457, 'estimated_prompt_tokens': 26709, 'estimated_total_tokens': 30166, 'first_chunk_seconds': 18.490487154980656, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 106833, 'prompt_tokens': 26910, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 31422}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1546, 'completion_chars': 6224, 'completion_tokens': 2430, 'elapsed_seconds': 47.46692917798646, 'estimated_completion_tokens': 1556, 'estimated_prompt_tokens': 63038, 'estimated_total_tokens': 64594, 'first_chunk_seconds': 19.54909754698747, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 252150, 'prompt_tokens': 49726, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 52156}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 860, 'completion_chars': 3708, 'completion_tokens': 3451, 'elapsed_seconds': 65.96630697499495, 'estimated_completion_tokens': 927, 'estimated_prompt_tokens': 58405, 'estimated_total_tokens': 59332, 'first_chunk_seconds': 50.34600716398563, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 233620, 'prompt_tokens': 45170, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 48621}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1809, 'completion_chars': 7560, 'completion_tokens': 2214, 'elapsed_seconds': 42.67592369701015, 'estimated_completion_tokens': 1890, 'estimated_prompt_tokens': 71313, 'estimated_total_tokens': 73203, 'first_chunk_seconds': 9.96181487600552, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 285251, 'prompt_tokens': 57290, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 59504}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1111, 'completion_chars': 5273, 'completion_tokens': 1395, 'elapsed_seconds': 27.711849233019166, 'estimated_completion_tokens': 1319, 'estimated_prompt_tokens': 63821, 'estimated_total_tokens': 65140, 'first_chunk_seconds': 7.630621414020425, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 255283, 'prompt_tokens': 50186, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 51581}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3984, 'completion_chars': 15307, 'completion_tokens': 4309, 'elapsed_seconds': 79.98283997600083, 'estimated_completion_tokens': 3827, 'estimated_prompt_tokens': 27931, 'estimated_total_tokens': 31758, 'first_chunk_seconds': 8.928747769008623, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 111724, 'prompt_tokens': 28290, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 32599}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1873, 'completion_chars': 8823, 'completion_tokens': 2910, 'elapsed_seconds': 54.66412681402289, 'estimated_completion_tokens': 2206, 'estimated_prompt_tokens': 29891, 'estimated_total_tokens': 32097, 'first_chunk_seconds': 20.85205332300393, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 119562, 'prompt_tokens': 30560, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 33470}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`60/16`，missing=`<none>`。
- repairs：`4/5` accepted；scenario_history=`8`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
