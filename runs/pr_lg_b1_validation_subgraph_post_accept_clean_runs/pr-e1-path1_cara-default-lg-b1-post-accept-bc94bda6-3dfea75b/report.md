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
| Git commit | `bc94bda6bfcdb952b0661a0c71d91d17174d1373` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:e2cfdd7ab1fd43540a75a5216158706cc6809d0eb975e3731e90124b8a1ff158` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:bf01076a8a36fd3168dd34e217b409eb1fba5c078b6c6c09b78f3eb607ff4dfd", "iteration": 3, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:4e2c7794b7f3d7d4f0a53ce595461cb93e3e68723ba5bcd88b135ca5fea2ca90", "iteration": 2, "repair_history_index": 2, "rework_instructions": ["Resolve W_FORCED_OVERRIDES_NORMAL by eliminating the duplicate coverage between global forced CA_backManual and the source-specific PumpFault -> Manual : CA_backManual transition. Do not keep both transitions covering CARA.PumpFault on the same CA_backManual event.", "Preserve the intended CA_backManual behavior deterministically by replacing the single global '! * -> Manual : CA_backManual;' with explicit CA_backManual fallback transitions for the concrete non-PumpFault states that need the shared recovery target, e.g. Manual, Ask_StartAC, AutocontrolInit, and AutocontrolNormal, while keeping a single PumpFault -> Manual : CA_backManual transition with the intended fault-clearing effect if that is the chosen repair for the CA-specific probe.", "Keep the CB_backManual, CP_backManual, and CC_backManual fallbacks represented and preserve the current safe behavior for CC_backManual from PumpFault: it may enter Manual with pump_fault still active, alarm_signal=1, pump_speed=0, and flow_rate=0 until FaultRemoved occurs.", "Keep the new Manual -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; } so that FaultRemoved after an already-reached Manual state restores the expected manual outputs through Manual enter/during actions.", "Do not change the autocontrol low-pressure formula to make flow_rate=11 in terminate_ac_from_ask_and_init_returns_manual. Preserve the accepted monotonic abstraction: below target pressure raises flow_rate by one unit, so default_flow_rate=9 produces flow_rate=10.", "Preserve all NL-required states, variables, '[*] -> Manual;', '! AutocontrolNormal -> PumpFault : if [pump_fault > 0];', InitiateAC, StartAC, ChangeSetpoint with target_bp=caregiver_target_bp, TerminateAC transitions, FaultRemoved recovery, and the manual/autocontrol pump-output actions."], "same_as_final": false, "sl10_decision": "rework"}, "matching_repair_history_indices": [4], "repair_history_index": 4, "selected_source_stage": "SL-7", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, ... +2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 1035373, 'completion_tokens': 71003, 'total_tokens': 1106376, 'estimated_prompt_tokens': 1274175, 'estimated_completion_tokens': 52102, 'estimated_total_tokens': 1326277, 'prompt_chars': 5096664, 'completion_chars': 208375, 'n_calls': 21, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`1371.799s` |
| run record | [`pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:a80e29ded728e74d8dfd1112901d5af2a0922d73a8fb9875a312458fde732ea0` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `82` |
| `langgraph_node_trace_hash` | `sha256:bc9ff336fce4723a0a2660f173f752029a9262886809b481f4c63e98a50022dd` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `82` |

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
def int target_bp = 80;
def int caregiver_target_bp = 80;
def int blood_pressure = 80;
def int shared_sensor_buffer = 0;
def int default_flow_rate = 10;
def int built_in_switch = 10;
def int control_voltage = 10;
def int pump_speed = 0;
def int flow_rate = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 1;
def int log_count = 0;
def int setpoint_changed = 0;

state CARA {
    ! * -> Manual : CB_backManual;
    ! * -> Manual : CP_backManual;
    ! * -> Manual : CC_backManual;
    ! AutocontrolNormal -> PumpFault : if [pump_fault > 0];

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault == 0] {
                alarm_signal = 0;
            } else {
                alarm_signal = 1;
                pump_speed = 0;
                flow_rate = 0;
            }
        }
        during {
            shared_sensor_buffer = blood_pressure;
            if [pump_fault == 0] {
                alarm_signal = 0;
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            } else {
                alarm_signal = 1;
                pump_speed = 0;
                flow_rate = 0;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
            control_released = 0;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            setpoint_changed = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 2;
            control_released = 0;
        }
        during {
            shared_sensor_buffer = blood_pressure;
            log_count = log_count + 1;
            pump_speed = control_voltage;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    flow_rate = default_flow_rate - 1;
                } else if [blood_pressure < target_bp] {
                    flow_rate = default_flow_rate + 1;
                } else {
                    flow_rate = default_flow_rate;
                }
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            control_released = 1;
            CA_mode = 0;
            pump_speed = 0;
            flow_rate = 0;
        }
    }

    Manual -> Ask_StartAC : InitiateAC;
    Manual -> Manual : CA_backManual;
    Manual -> Manual : FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
    Ask_StartAC -> AutocontrolInit : StartAC;
    Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
        target_bp = caregiver_target_bp;
        setpoint_changed = 1;
    };
    Ask_StartAC -> Manual : TerminateAC;
    Ask_StartAC -> Manual : CA_backManual;
    AutocontrolInit -> Manual : TerminateAC;
    AutocontrolInit -> Manual : CA_backManual;
    AutocontrolNormal -> Manual : TerminateAC;
    AutocontrolNormal -> Manual : CA_backManual;
    AutocontrolInit -> AutocontrolNormal;
    PumpFault -> Manual : CA_backManual;
    PumpFault -> Manual : FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12280 | 生成初始 DSL 与 grounding seeds | initial len=2470 | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=488363 | LLM per-request accept/reject + repair | candidate len=2466,2921,3125,3267,3230 | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=351443 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=3, tokens=80976 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=488363 | LLM per-request accept/reject + repair | candidate len=2466,2921,3125,3267,3230 | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=351443 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=488363 | LLM per-request accept/reject + repair | candidate len=2466,2921,3125,3267,3230 | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=351443 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=488363 | LLM per-request accept/reject + repair | candidate len=2466,2921,3125,3267,3230 | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=351443 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=3, tokens=80976 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=488363 | LLM per-request accept/reject + repair | candidate len=2466,2921,3125,3267,3230 | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=351443 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=173314 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=3, tokens=80976 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-post-accept-bc94bda6-3dfea75b.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T12:51:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T12:51:26Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T12:51:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T12:51:26Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T12:53:14Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T12:53:14Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2470,hash=sha256:c5110d09bafd |
| 7 | `2026-06-05T12:53:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T12:53:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T12:53:14Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:c5110d09bafd36aa60100d87ddf686c6e6ec096d76c22ce2818d4920553e65fc |
| 10 | `2026-06-05T12:53:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T12:53:14Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2470,hash=sha256:c5110d09bafd, current_hash=sha256:c5110d09bafd36aa60100d87ddf686c6e6ec096d76c22ce2818d4920553e65fc |
| 12 | `2026-06-05T12:53:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T12:53:14Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T12:53:14Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T12:53:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T12:53:14Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T12:53:15Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T12:53:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T12:53:15Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T12:53:15Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T12:53:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T12:53:15Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T12:54:58Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T12:54:58Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T12:54:59Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T12:54:59Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T12:54:59Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T12:56:30Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T12:56:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T12:56:31Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T12:56:31Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T12:56:31Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T12:58:15Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T12:58:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T12:58:15Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T12:58:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T12:58:15Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T12:58:15Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T12:58:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T12:58:15Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T12:58:15Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 42 | `2026-06-05T12:58:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T12:58:15Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 15, "n_scenarios_passed": 7, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 44 | `2026-06-05T12:58:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T12:58:15Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-05T12:58:15Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 15, "n_scenarios_passed": 7, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2470,hash=sha256:c5110d09bafd |
| 47 | `2026-06-05T12:58:15Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 48 | `2026-06-05T12:58:15Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 8} | <none> |
| 49 | `2026-06-05T12:58:15Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2470,hash=sha256:c5110d09bafd |
| 50 | `2026-06-05T12:59:11Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 51 | `2026-06-05T12:59:11Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-882634d574", "fixreq-0-sd6-1-5a0b11c3c0", "fixreq-0-sd6-2-6e58fa677a", "fixreq-0-sd6-3-ca14ae79d4", "fixreq-0-sd6-4-3389524377", "fixreq-0-sd6-5-c2231e32f6", "fixreq-0-sd6-6-2a2d1bb5f1", "fixreq-0-sd6-7-63f677f273"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2466,hash=sha256:b33b133cba82 |
| 52 | `2026-06-05T12:59:11Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 53 | `2026-06-05T12:59:11Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:b33b133cba821c111f054a2fa54395c557d5c8d02a4ad00fe6eb009fbebe8fb1 |
| 54 | `2026-06-05T12:59:37Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 55 | `2026-06-05T12:59:37Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 56 | `2026-06-05T12:59:37Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 57 | `2026-06-05T12:59:37Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2466,hash=sha256:b33b133cba82 |
| 58 | `2026-06-05T12:59:37Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:b33b133cba821c111f054a2fa54395c557d5c8d02a4ad00fe6eb009fbebe8fb1 |
| 59 | `2026-06-05T12:59:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 60 | `2026-06-05T12:59:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 61 | `2026-06-05T12:59:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 62 | `2026-06-05T12:59:37Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:b33b133cba821c111f054a2fa54395c557d5c8d02a4ad00fe6eb009fbebe8fb1 |
| 63 | `2026-06-05T12:59:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 64 | `2026-06-05T12:59:37Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=2466,hash=sha256:b33b133cba82, current_hash=sha256:b33b133cba821c111f054a2fa54395c557d5c8d02a4ad00fe6eb009fbebe8fb1 |
| 65 | `2026-06-05T12:59:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 66 | `2026-06-05T12:59:37Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 67 | `2026-06-05T12:59:37Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 68 | `2026-06-05T12:59:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 69 | `2026-06-05T12:59:37Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 70 | `2026-06-05T12:59:37Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 71 | `2026-06-05T12:59:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 72 | `2026-06-05T12:59:37Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 73 | `2026-06-05T12:59:37Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-5A", "ok": true, "status": "StageStatus.OK"} | <none> |
| 74 | `2026-06-05T12:59:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 75 | `2026-06-05T12:59:37Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 targeted_retry", "ok": false, "reason": "reuse_frozen_scenario_set"} | <none> |
| 76 | `2026-06-05T12:59:37Z` | `<control>` | `1` | `frozen_scenario_refresh_targeted_retry` | {} | <none> |
| 77 | `2026-06-05T12:59:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 78 | `2026-06-05T12:59:37Z` | `SL-5` | `1` | `stage_enter` | {"reason": "targeted_refresh_after_frozen_gap_or_dsl_change"} | <none> |
| 79 | `2026-06-05T13:01:04Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 80 | `2026-06-05T13:01:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
- ……另有 `172` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-6` | yes | fixbatch-0-sha256-eef005362b4 / n=8 | accept=8, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SL-7` | yes | fixbatch-1-sha256-afcf071a815 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SD-6` | yes | fixbatch-2-sha256-be0bd2c6ce4 / n=3 | accept=3, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; forced_transition_count_drift; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `SL-7` | yes | fixbatch-3-sha256-0ee61448bc6 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 4 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|---|
| `default_init_enters_manual_and_sets_manual_outputs` | default-init verifies initial dispatch to Manual and manual operation sets pump speed from built-in switch, default flow...<truncated 44 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `initiate_change_setpoint_start_ac_to_normal_high_pressure` | default-init follows caregiver initiation through Ask_StartAC, setpoint change, StartAC, AutocontrolInit, and normal aut...<truncated 42 chars> | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `normal_autocontrol_low_pressure_raises_flow` | explicit-hot-start in AutocontrolNormal verifies normal autocontrol records data, uses control voltage, and raises flow ...<truncated 30 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `normal_autocontrol_no_fault_no_phantom_fault_transition` | explicit-hot-start in AutocontrolNormal with pump_fault clear verifies no fault transition occurs and equal pressure kee...<truncated 16 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_alarms_releases_control_then_fault_removed_manual` | explicit-hot-start in AutocontrolNormal with a pump fault verifies transition to PumpFault activates alarm and releases ...<truncated 46 chars> | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `terminate_ac_from_ask_and_init_returns_manual` | explicit-hot-start in Ask_StartAC verifies TerminateAC returns to Manual from Ask_StartAC, AutocontrolInit, and Autocont...<truncated 34 chars> | ⚪ | ✅ | ❌ | ✅ | ✅ |
| `back_manual_fallbacks_from_autocontrol_states` | explicit-hot-start in Ask_StartAC sweeps CA_backManual, CB_backManual, and CP_backManual fallbacks from distinct autocon...<truncated 30 chars> | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `cc_back_manual_fallback_from_pumpfault` | explicit-hot-start in PumpFault verifies CC_backManual shares Manual as recovery target while an uncleared fault keeps a...<truncated 31 chars> | ✅ | ✅ | ❌ | ✅ | ✅ |
| `ca_backmanual_from_pumpfault_forced_line_probe` | explicit-hot-start in PumpFault checks CA_backManual returns to Manual but does not by itself remove an active physical ...<truncated 71 chars> | ✅ | ✅ | ❌ | ✅ | ✅ |
| `terminate_ac_from_normal_returns_manual` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `direct_start_ac_wrong_target_and_effect_probe` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `direct_change_setpoint_self_transition_effect_probe` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `forced_backmanual_from_manual_reapplies_manual_outputs` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `direct_fault_removed_effect_value_probe` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `direct_initiate_ac_wrong_target_probe` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_enters_manual_and_sets_manual_outputs` — default-init verifies initial dispatch to Manual and manual operation sets pump speed from built-in switch, default flow rate, sensor buffer, and safe manual fl...<truncated 4 chars></summary>

| Field | Value |
|---|---|
| description | default-init verifies initial dispatch to Manual and manual operation sets pump speed from built-in switch, default flow rate, sensor buffer, and safe manual flags. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 75, "built_in_switch": 12, "default_flow_rate": 10, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_cycle_dispatches_to_manual` | `0` | `[]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 10, "pump_speed": 12, "shared_sensor_buffer": 75}` |

</details>

<details><summary>`initiate_change_setpoint_start_ac_to_normal_high_pressure` — default-init follows caregiver initiation through Ask_StartAC, setpoint change, StartAC, AutocontrolInit, and normal autocontrol with high pressure lowering flo...<truncated 2 chars></summary>

| Field | Value |
|---|---|
| description | default-init follows caregiver initiation through Ask_StartAC, setpoint change, StartAC, AutocontrolInit, and normal autocontrol with high pressure lowering flow. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 90, "built_in_switch": 11, "caregiver_target_bp": 85, "control_voltage": 7, "default_flow_rate": 10, "log_count": 0, "pump_fault": 0, "target_bp": 80}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dispatch_to_manual_before_events` | `0` | `[]` | `CARA.Manual` | `{"CA_mode": 0, "control_released": 1, "flow_rate": 10, "pump_speed": 11, "shared_sensor_buffer": 90}` |
| 1 `initiate_ac_enters_ask_startac` | `0` | `["CARA.InitiateAC"]` | `CARA.Ask_StartAC` | `{"CA_mode": 1, "control_released": 0}` |
| 2 `change_setpoint_stays_in_ask_and_updates_target` | `0` | `["CARA.ChangeSetpoint"]` | `CARA.Ask_StartAC` | `{"CA_mode": 1, "control_released": 0, "setpoint_changed": 1, "target_bp": 85}` |
| 3 `start_ac_enters_autocontrol_init` | `0` | `["CARA.StartAC"]` | `CARA.AutocontrolInit` | `{"CA_mode": 2, "control_released": 0, "setpoint_changed": 0}` |
| 4 `completion_enters_normal_and_controls_flow` | `0` | `[]` | `CARA.AutocontrolNormal` | `{"CA_mode": 2, "control_released": 0, "flow_rate": 9, "log_count": 1, "pump_speed": 7, "shared_sensor_buffer": 90}` |

</details>

<details><summary>`normal_autocontrol_low_pressure_raises_flow` — explicit-hot-start in AutocontrolNormal verifies normal autocontrol records data, uses control voltage, and raises flow when pressure is below target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal verifies normal autocontrol records data, uses control voltage, and raises flow when pressure is below target. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 2, "blood_pressure": 70, "control_released": 0, "control_voltage": 5, "default_flow_rate": 10, "log_count": 3, "pump_fault": 0, "target_bp": 80}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `low_pressure_normal_control_cycle` | `0` | `[]` | `CARA.AutocontrolNormal` | `{"control_released": 0, "flow_rate": 11, "log_count": 4, "pump_speed": 5, "shared_sensor_buffer": 70}` |

</details>

<details><summary>`normal_autocontrol_no_fault_no_phantom_fault_transition` — explicit-hot-start in AutocontrolNormal with pump_fault clear verifies no fault transition occurs and equal pressure keeps default flow.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal with pump_fault clear verifies no fault transition occurs and equal pressure keeps default flow. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 2, "alarm_signal": 0, "blood_pressure": 80, "control_released": 0, "control_voltage": 6, "default_flow_rate": 10, "log_count": 0, "pump_fault": 0, "target_bp": 80}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `stays_normal_with_no_complication` | `0` | `[]` | `CARA.AutocontrolNormal` | `{"alarm_signal": 0, "control_released": 0, "flow_rate": 10, "log_count": 1, "pump_speed": 6, "shared_sensor_buffer": 80}` |

</details>

<details><summary>`pump_fault_alarms_releases_control_then_fault_removed_manual` — explicit-hot-start in AutocontrolNormal with a pump fault verifies transition to PumpFault activates alarm and releases control, then FaultRemoved recovers to M...<truncated 6 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal with a pump fault verifies transition to PumpFault activates alarm and releases control, then FaultRemoved recovers to Manual. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 2, "alarm_signal": 0, "blood_pressure": 85, "built_in_switch": 13, "control_released": 0, "control_voltage": 6, "default_flow_rate": 10, "flow_rate": 10, "pump_fault": 1, "target_bp": 80}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_enters_pumpfault` | `0` | `[]` | `CARA.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1, "flow_rate": 0, "pump_speed": 0}` |
| 1 `fault_removed_recovers_to_manual` | `0` | `["CARA.FaultRemoved"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 10, "pump_fault": 0, "pump_speed": 13, "shared_sensor_buffer": 85}` |

</details>

<details><summary>`terminate_ac_from_ask_and_init_returns_manual` — explicit-hot-start in Ask_StartAC verifies TerminateAC returns to Manual from Ask_StartAC, AutocontrolInit, and AutocontrolNormal while releasing control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Ask_StartAC verifies TerminateAC returns to Manual from Ask_StartAC, AutocontrolInit, and AutocontrolNormal while releasing control. |
| initial_state | `CARA.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 78, "built_in_switch": 14, "control_released": 0, "control_voltage": 4, "default_flow_rate": 9, "log_count": 0, "pump_fault": 0, "target_bp": 80}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_from_ask_to_manual` | `0` | `["CARA.TerminateAC"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 9, "pump_speed": 14, "shared_sensor_buffer": 78}` |
| 1 `reinitiate_to_ask` | `0` | `["CARA.InitiateAC"]` | `CARA.Ask_StartAC` | `{"CA_mode": 1, "control_released": 0}` |
| 2 `start_ac_to_init` | `0` | `["CARA.StartAC"]` | `CARA.AutocontrolInit` | `{"CA_mode": 2, "control_released": 0, "setpoint_changed": 0}` |
| 3 `terminate_from_init_to_manual` | `0` | `["CARA.TerminateAC"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 9, "pump_speed": 14, "shared_sensor_buffer": 78}` |
| 4 `reinitiate_to_ask_for_normal_terminate` | `0` | `["CARA.InitiateAC"]` | `CARA.Ask_StartAC` | `{"CA_mode": 1, "control_released": 0}` |
| 5 `start_ac_to_init_for_normal_terminate` | `0` | `["CARA.StartAC"]` | `CARA.AutocontrolInit` | `{"CA_mode": 2, "control_released": 0}` |
| 6 `completion_to_normal_for_terminate` | `0` | `[]` | `CARA.AutocontrolNormal` | `{"CA_mode": 2, "control_released": 0, "flow_rate": 10, "log_count": 1, "pump_speed": 4, "shared_sensor_buffer": 78}` |
| 7 `terminate_from_normal_to_manual` | `0` | `["CARA.TerminateAC"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 9, "pump_speed": 14, "shared_sensor_buffer": 78}` |

</details>

<details><summary>`back_manual_fallbacks_from_autocontrol_states` — explicit-hot-start in Ask_StartAC sweeps CA_backManual, CB_backManual, and CP_backManual fallbacks from distinct autocontrol-related states to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Ask_StartAC sweeps CA_backManual, CB_backManual, and CP_backManual fallbacks from distinct autocontrol-related states to Manual. |
| initial_state | `CARA.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 76, "built_in_switch": 16, "control_released": 0, "control_voltage": 4, "default_flow_rate": 12, "log_count": 0, "pump_fault": 0, "target_bp": 80}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_from_ask_to_manual` | `0` | `["CARA.CA_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 12, "pump_speed": 16, "shared_sensor_buffer": 76}` |
| 1 `go_to_ask_again` | `0` | `["CARA.InitiateAC"]` | `CARA.Ask_StartAC` | `{"CA_mode": 1, "control_released": 0}` |
| 2 `go_to_init_for_cb_fallback` | `0` | `["CARA.StartAC"]` | `CARA.AutocontrolInit` | `{"CA_mode": 2, "control_released": 0, "setpoint_changed": 0}` |
| 3 `cb_backmanual_from_init_to_manual` | `0` | `["CARA.CB_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 12, "pump_speed": 16, "shared_sensor_buffer": 76}` |
| 4 `go_to_ask_for_normal_path` | `0` | `["CARA.InitiateAC"]` | `CARA.Ask_StartAC` | `{"CA_mode": 1, "control_released": 0}` |
| 5 `go_to_init_before_normal` | `0` | `["CARA.StartAC"]` | `CARA.AutocontrolInit` | `{"CA_mode": 2, "control_released": 0}` |
| 6 `completion_to_normal` | `0` | `[]` | `CARA.AutocontrolNormal` | `{"CA_mode": 2, "control_released": 0, "flow_rate": 13, "log_count": 1, "pump_speed": 4, "shared_sensor_buffer": 76}` |
| 7 `cp_backmanual_from_normal_to_manual` | `0` | `["CARA.CP_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 12, "pump_speed": 16, "shared_sensor_buffer": 76}` |

</details>

<details><summary>`cc_back_manual_fallback_from_pumpfault` — explicit-hot-start in PumpFault verifies CC_backManual shares Manual as recovery target while an uncleared fault keeps alarm active until FaultRemoved.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in PumpFault verifies CC_backManual shares Manual as recovery target while an uncleared fault keeps alarm active until FaultRemoved. |
| initial_state | `CARA.PumpFault` |
| initial_vars | `{"CA_mode": 0, "alarm_signal": 1, "blood_pressure": 77, "built_in_switch": 17, "control_released": 1, "default_flow_rate": 6, "flow_rate": 0, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_backmanual_from_pumpfault_to_manual_with_fault_still_active` | `0` | `["CARA.CC_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1, "flow_rate": 0, "pump_fault": 1, "pump_speed": 0, "shared_sensor_buffer": 77}` |
| 1 `fault_removed_then_manual_outputs_restore` | `0` | `["CARA.FaultRemoved"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 6, "pump_fault": 0, "pump_speed": 17, "shared_sensor_buffer": 77}` |

</details>

<details><summary>`ca_backmanual_from_pumpfault_forced_line_probe` — explicit-hot-start in PumpFault checks CA_backManual returns to Manual but does not by itself remove an active physical pump fault; alarm and stopped pump behav...<truncated 31 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in PumpFault checks CA_backManual returns to Manual but does not by itself remove an active physical pump fault; alarm and stopped pump behavior remain until fault removal. |
| initial_state | `CARA.PumpFault` |
| initial_vars | `{"CA_mode": 0, "alarm_signal": 1, "blood_pressure": 79, "built_in_switch": 18, "control_released": 1, "default_flow_rate": 7, "flow_rate": 0, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_from_pumpfault_to_manual_with_fault_still_active` | `0` | `["CARA.CA_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1, "flow_rate": 0, "pump_fault": 1, "pump_speed": 0, "shared_sensor_buffer": 79}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | initiate_change_setpoint_start_ac_to_normal_high_pressure, pump_fault_alarms_releases_control_then_fault_removed_manual, terminate_ac_from_ask_and_init_returns_manual, back_manual_fallbacks_from_autocontrol_states, direct_start_ac_wrong_target_and_effect_probe, ... +3 | accept=8, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:b33b133cba821c111f054a2fa54395c557d5c8d02a4ad00fe6eb009fbebe8fb1` |
| 2 | `1` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:61cd61b0a826f875c372d019f28b015e190455700584113ffdbf76fe40ead0f8` |
| 3 | `2` | ❌ | `SD-6` | terminate_ac_from_ask_and_init_returns_manual, cc_back_manual_fallback_from_pumpfault, ca_backmanual_from_pumpfault_forced_line_probe | accept=2, reject=1, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Resolve W_FORCED_OVERRIDES_NORMAL by eliminating the duplicate coverage between global forced CA_backManual and the source-specific PumpFault -> Manual : CA_backManual transiti...<truncated 749 chars> | `sha256:4e2c7794b7f3d7d4f0a53ce595461cb93e3e68723ba5bcd88b135ca5fea2ca90` |
| 4 | `2` | ✅ | `SD-6` | terminate_ac_from_ask_and_init_returns_manual, cc_back_manual_fallback_from_pumpfault, ca_backmanual_from_pumpfault_forced_line_probe | accept=3, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; forced_transition_count_drift; missing_required_grounding | `sha256:43f02231d93a2b1156f868a3906cfc7090d7450d3ef582f9fc8851317947b246` |
| 5 | `3` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:bf01076a8a36fd3168dd34e217b409eb1fba5c078b6c6c09b78f3eb607ff4dfd` |

<details><summary>Repair 1 / iteration `0` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_change_setpoint_start_ac_to_normal_high_pressure, pump_fault_alarms_releases_control_then_fault_removed_manual, terminate_ac_from_ask_and_init_returns_manual, back_manual_fallbacks_from_autocontrol_states, direct_start_ac_wrong_target_and_effect_probe, direct_change_setpoint_self_transition_effect_probe, direct_fault_removed_effect_value_probe, direct_initiate_ac_wrong_target_probe`。
- before_dsl_hash：`sha256:c5110d09bafd36aa60100d87ddf686c6e6ec096d76c22ce2818d4920553e65fc`；candidate_dsl_hash：`sha256:b33b133cba821c111f054a2fa54395c557d5c8d02a4ad00fe6eb009fbebe8fb1`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：
- 7. `<unknown>` `` policy=``：
- 8. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-eef005362b4`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`8`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-882634d574` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init follows caregiver initiation through Ask_StartAC, setpoint change, StartAC, AutocontrolInit, and normal autocontrol with high pressure lowering flow.', 'name': 'initiate_change_setpoint_start_ac_to_normal_high_pressure', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init follows caregiver initiation through Ask_StartAC, setpoint change, StartAC, AutocontrolInit, and normal autocontrol with high pressure lowering flow.', 'failing_steps': [{'actual_state': 'CARA.Manual', 'actual_vars_focus': {'CA_mode': 0, 'control_released': 1}, 'before_cycles': 0, 'events': ['CARA.InitiateAC'], 'expected_state': 'CARA.Ask_StartAC', 'expected_vars': {'CA_mode': 1, 'control_released': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'initiate_ac_enters_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'blood_pressure': 90, 'built_in_switch': 11, 'control_voltage': 7, 'default_flow_rate': 10, 'log_count': 0, 'target_bp': 80}, 'scenario_name': 'initiate_change_setpoint_start_ac_to_normal_high_pressure', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 90, 'built_in_switch': 11, 'control_released': 1, 'control_voltage': 7, 'default_flow_rate': 10, 'flow_rate': 10, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 11, 'setpoint_changed': 0, 'shared_sensor_buffer': 90, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'dispatch_to_manual_before_events', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 90, 'built_in_switch': 11, 'control_released': 1, 'control_voltage': 7, 'default_flow_rate': 10, 'flow_rate': 10, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 11, 'setpoint_changed': 0, 'shared_sensor_buffer': 90, 'target_bp': 80}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'initiate_ac_enters_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-5a0b11c3c0` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in AutocontrolNormal with a pump fault verifies transition to PumpFault activates alarm and releases control, then FaultRemoved recovers to Manual.', 'name': 'pump_fault_alarms_releases_control_then_fault_removed_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in AutocontrolNormal with a pump fault verifies transition to PumpFault activates alarm and releases control, then FaultRemoved recovers to Manual.', 'failing_steps': [{'actual_state': 'CARA.PumpFault', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'control_released': 1, 'flow_rate': 0, 'pump_fault': 1, 'pump_speed': 0, 'shared_sensor_buffer': 0}, 'before_cycles': 0, 'events': ['CARA.FaultRemoved'], 'expected_state': 'CARA.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'control_released': 1, 'flow_rate': 10, 'pump_fault': 0, 'pump_speed': 13, 'shared_sensor_buffer': 85}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.FaultRemoved'", 'runtime_error_hint': {'event_path': 'CARA.FaultRemoved', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'fault_removed_recovers_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.AutocontrolNormal', 'initial_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 85, 'built_in_switch': 13, 'control_released': 0, 'control_voltage': 6, 'default_flow_rate': 10, 'flow_rate': 10, 'pump_fault': 1, 'target_bp': 80}, 'scenario_name': 'pump_fault_alarms_releases_control_then_fault_removed_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 85, 'built_in_switch': 13, 'control_released': 1, 'control_voltage': 6, 'default_flow_rate': 10, 'flow_rate': 0, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 0, 'setpoint_changed': 0, 'shared_sensor_buffer': 0, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'fault_enters_pumpfault', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 85, 'built_in_switch': 13, 'control_released': 1, 'control_voltage': 6, 'default_flow_rate': 10, 'flow_rate': 0, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 0, 'setpoint_changed': 0, 'shared_sensor_buffer': 0, 'target_bp': 80}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.FaultRemoved'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'fault_removed_recovers_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-2-6e58fa677a` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in Ask_StartAC verifies TerminateAC returns to Manual from Ask_StartAC and from AutocontrolInit before normal control begins.', 'name': 'terminate_ac_from_ask_and_init_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in Ask_StartAC verifies TerminateAC returns to Manual from Ask_StartAC and from AutocontrolInit before normal control begins.', 'failing_steps': [{'actual_state': 'CARA.Manual', 'actual_vars_focus': {'CA_mode': 0, 'control_released': 1}, 'before_cycles': 0, 'events': ['CARA.InitiateAC'], 'expected_state': 'CARA.Ask_StartAC', 'expected_vars': {'CA_mode': 1, 'control_released': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'reinitiate_to_ask', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'blood_pressure': 78, 'built_in_switch': 14, 'control_released': 0, 'default_flow_rate': 9}, 'scenario_name': 'terminate_ac_from_ask_and_init_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'control_released': 1, 'control_voltage': 10, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'terminate_from_ask_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'control_released': 1, 'control_voltage': 10, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'reinitiate_to_ask', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-ca14ae79d4` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in Ask_StartAC sweeps CA_backManual, CB_backManual, and CP_backManual forced fallbacks from distinct autocontrol-related states to Manual.', 'name': 'back_manual_fallbacks_from_autocontrol_states', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in Ask_StartAC sweeps CA_backManual, CB_backManual, and CP_backManual forced fallbacks from distinct autocontrol-related states to Manual.', 'failing_steps': [{'actual_state': 'CARA.Manual', 'actual_vars_focus': {'CA_mode': 0, 'control_released': 1}, 'before_cycles': 0, 'events': ['CARA.InitiateAC'], 'expected_state': 'CARA.Ask_StartAC', 'expected_vars': {'CA_mode': 1, 'control_released': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'go_to_ask_again', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'blood_pressure': 76, 'built_in_switch': 16, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 12, 'pump_fault': 0, 'target_bp': 80}, 'scenario_name': 'back_manual_fallbacks_from_autocontrol_states', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 76, 'built_in_switch': 16, 'control_released': 1, 'control_voltage': 4, 'default_flow_rate': 12, 'flow_rate': 12, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 16, 'setpoint_changed': 0, 'shared_sensor_buffer': 76, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'ca_backmanual_from_ask_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 76, 'built_in_switch': 16, 'control_released': 1, 'control_voltage': 4, 'default_flow_rate': 12, 'flow_rate': 12, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 16, 'setpoint_changed': 0, 'shared_sensor_buffer': 76, 'target_bp': 80}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'go_to_ask_again', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-3389524377` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in Ask_StartAC directly checks StartAC targets AutocontrolInit and resets setpoint_changed while entering active autocontrol setup.', 'name': 'direct_start_ac_wrong_target_and_effect_probe', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in Ask_StartAC directly checks StartAC targets AutocontrolInit and resets setpoint_changed while entering active autocontrol setup.', 'failing_steps': [{'actual_state': 'CARA.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'setpoint_changed': 1}, 'before_cycles': 0, 'events': ['CARA.StartAC'], 'expected_state': 'CARA.AutocontrolInit', 'expected_vars': {'CA_mode': 2, 'control_released': 0, 'setpoint_changed': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.StartAC'", 'runtime_error_hint': {'event_path': 'CARA.StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'start_ac_exactly_enters_init_and_clears_setpoint_flag', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'blood_pressure': 81, 'control_released': 0, 'control_voltage': 5, 'default_flow_rate': 10, 'setpoint_changed': 1, 'target_bp': 80}, 'scenario_name': 'direct_start_ac_wrong_target_and_effect_probe', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 81, 'built_in_switch': 10, 'control_released': 0, 'control_voltage': 5, 'default_flow_rate': 10, 'flow_rate': 0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0, 'setpoint_changed': 1, 'shared_sensor_buffer': 0, 'target_bp': 80}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'start_ac_exactly_enters_init_and_clears_setpoint_flag', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-5-c2231e32f6` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in Ask_StartAC directly checks ChangeSetpoint remains in Ask_StartAC and sets the setpoint_changed flag.', 'name': 'direct_change_setpoint_self_transition_effect_probe', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in Ask_StartAC directly checks ChangeSetpoint remains in Ask_StartAC and sets the setpoint_changed flag.', 'failing_steps': [{'actual_state': 'CARA.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'setpoint_changed': 0}, 'before_cycles': 0, 'events': ['CARA.ChangeSetpoint'], 'expected_state': 'CARA.Ask_StartAC', 'expected_vars': {'CA_mode': 1, 'control_released': 0, 'setpoint_changed': 1}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.ChangeSetpoint'", 'runtime_error_hint': {'event_path': 'CARA.ChangeSetpoint', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'change_setpoint_keeps_ask_and_sets_flag', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'setpoint_changed': 0, 'target_bp': 80}, 'scenario_name': 'direct_change_setpoint_self_transition_effect_probe', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 80, 'built_in_switch': 10, 'control_released': 0, 'control_voltage': 10, 'default_flow_rate': 10, 'flow_rate': 0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0, 'setpoint_changed': 0, 'shared_sensor_buffer': 0, 'target_bp': 80}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.ChangeSetpoint'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'change_setpoint_keeps_ask_and_sets_flag', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-6-2a2d1bb5f1` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault with stale fault values checks FaultRemoved targets Manual and its effect clears pump_fault and alarm_signal to zero before manual operation resumes.', 'name': 'direct_fault_removed_effect_value_probe', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault with stale fault values checks FaultRemoved targets Manual and its effect clears pump_fault and alarm_signal to zero before manual operation resumes.', 'failing_steps': [{'actual_state': 'CARA.PumpFault', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 5, 'control_released': 1, 'flow_rate': 0, 'pump_fault': 99, 'pump_speed': 0, 'shared_sensor_buffer': 0}, 'before_cycles': 0, 'events': ['CARA.FaultRemoved'], 'expected_state': 'CARA.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'control_released': 1, 'flow_rate': 4, 'pump_fault': 0, 'pump_speed': 20, 'shared_sensor_buffer': 84}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.FaultRemoved'", 'runtime_error_hint': {'event_path': 'CARA.FaultRemoved', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_removed_clears_fault_and_alarm_exactly', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.PumpFault', 'initial_vars': {'CA_mode': 0, 'alarm_signal': 5, 'blood_pressure': 84, 'built_in_switch': 20, 'control_released': 1, 'default_flow_rate': 4, 'flow_rate': 0, 'pump_fault': 99}, 'scenario_name': 'direct_fault_removed_effect_value_probe', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 5, 'blood_pressure': 84, 'built_in_switch': 20, 'control_released': 1, 'control_voltage': 10, 'default_flow_rate': 4, 'flow_rate': 0, 'log_count': 0, 'pump_fault': 99, 'pump_speed': 0, 'setpoint_changed': 0, 'shared_sensor_buffer': 0, 'target_bp': 80}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.FaultRemoved'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_removed_clears_fault_and_alarm_exactly', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-7-63f677f273` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in Manual directly checks caregiver InitiateAC targets Ask_StartAC, not another autocontrol state, and takes software control.', 'name': 'direct_initiate_ac_wrong_target_probe', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in Manual directly checks caregiver InitiateAC targets Ask_StartAC, not another autocontrol state, and takes software control.', 'failing_steps': [{'actual_state': 'CARA.Manual', 'actual_vars_focus': {'CA_mode': 0, 'control_released': 1}, 'before_cycles': 0, 'events': ['CARA.InitiateAC'], 'expected_state': 'CARA.Ask_StartAC', 'expected_vars': {'CA_mode': 1, 'control_released': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'initiate_ac_exactly_enters_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Manual', 'initial_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 86, 'built_in_switch': 21, 'control_released': 1, 'default_flow_rate': 10}, 'scenario_name': 'direct_initiate_ac_wrong_target_probe', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 86, 'built_in_switch': 21, 'control_released': 1, 'control_voltage': 10, 'default_flow_rate': 10, 'flow_rate': 0, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 0, 'setpoint_changed': 0, 'shared_sensor_buffer': 0, 'target_bp': 80}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'initiate_ac_exactly_enters_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:blood_pressure, variable:shared_sensor_buffer, variable:built_in_switch, variable:control_voltage, variable:pump_speed, ... +22`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2466`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-882634d574` | `accept` | ❌ | ❌ | The failing initiate_change_setpoint_start_ac_to_normal_high_pressure step injects CARA.InitiateAC and expected CARA.Ask_StartAC with CA_mode=1 and control_released=0, but the event was only local to Manual and could not resolve from the scenario path.；intent=Make InitiateAC visible as a CARA-scope event while preserving the Manual to Ask_StartAC transition ...<truncated 30 chars> |
| `fixreq-0-sd6-1-5a0b11c3c0` | `accept` | ❌ | ❌ | The pump_fault_alarms_releases_control_then_fault_removed_manual scenario passed entry to PumpFault, then failed because CARA.FaultRemoved could not resolve; expected recovery to Manual with pump fault and alarm cleared and Manual during actions restored.；intent=Make FaultRemoved visible as a CARA-scope event while preserving its clear-fault effect and the M...<truncated 22 chars> |
| `fixreq-0-sd6-2-6e58fa677a` | `accept` | ❌ | ❌ | The terminate_ac_from_ask_and_init_returns_manual scenario first passed TerminateAC to Manual, then failed reinitiation because CARA.InitiateAC could not resolve.；intent=Use the same CARA-scope InitiateAC repair so reinitiation from Manual reaches Ask_StartAC. |
| `fixreq-0-sd6-3-ca14ae79d4` | `accept` | ❌ | ❌ | The back_manual_fallbacks_from_autocontrol_states scenario preserved the CA_backManual forced fallback behavior but then failed when CARA.InitiateAC could not resolve for the next Ask_StartAC entry.；intent=Preserve existing backManual forced transitions and repair only InitiateAC event visibility. |
| `fixreq-0-sd6-4-3389524377` | `accept` | ❌ | ❌ | The direct_start_ac_wrong_target_and_effect_probe scenario injects CARA.StartAC from Ask_StartAC and expected AutocontrolInit with CA_mode=2, control_released=0, and setpoint_changed=0, but StartAC was local and unresolved.；intent=Make StartAC visible as a CARA-scope event while preserving the Ask_StartAC to AutocontrolInit target and AutocontrolInit entry r...<truncated 25 chars> |
| `fixreq-0-sd6-5-c2231e32f6` | `accept` | ❌ | ❌ | The direct_change_setpoint_self_transition_effect_probe scenario injects CARA.ChangeSetpoint and expected to remain in Ask_StartAC with setpoint_changed=1, but ChangeSetpoint was local and unresolved.；intent=Make ChangeSetpoint visible as a CARA-scope event while preserving the self-transition and setpoint_changed=1 effect. |
| `fixreq-0-sd6-6-2a2d1bb5f1` | `accept` | ❌ | ❌ | The direct_fault_removed_effect_value_probe scenario injects CARA.FaultRemoved from PumpFault and expected Manual with pump_fault=0, alarm_signal=0, and Manual during values restored, but FaultRemoved was local and unresolved.；intent=Make FaultRemoved visible as a CARA-scope event while preserving the fault-clearing effect and Manual target. |
| `fixreq-0-sd6-7-63f677f273` | `accept` | ❌ | ❌ | The direct_initiate_ac_wrong_target_probe scenario injects CARA.InitiateAC from Manual and expected Ask_StartAC, but InitiateAC was local and unresolved.；intent=Make InitiateAC visible as a CARA-scope event while preserving the Ask_StartAC target and software-control entry actions. |
- repair_rationale：Primary gap across the failing repair_briefs is unresolved event paths such as CARA.InitiateAC, CARA.StartAC, CARA.ChangeSetpoint, and CARA.FaultRemoved. The existing transitions used local :: events, which are source-state namespace events...<truncated 173 chars>；For initiate_change_setpoint_start_ac_to_normal_high_pressure, step initiate_ac_enters_ask_startac expected CARA.Ask_StartAC with CA_mode=1 and control_released=0 but stayed in CARA.Manual due to unresolved CARA.InitiateAC. Manual -> Ask_St...<truncated 86 chars>；For direct_initiate_ac_wrong_target_probe, the same InitiateAC repair targets Ask_StartAC, not another autocontrol state, preserving the NL-grounded caregiver initiation behavior.；For direct_start_ac_wrong_target_and_effect_probe, Ask_StartAC -> AutocontrolInit : StartAC now resolves CARA.StartAC. AutocontrolInit.enter still sets CA_mode=2, keeps control_released=0, and clears setpoint_changed=0.；For direct_change_setpoint_self_transition_effect_probe, Ask_StartAC -> Ask_StartAC : ChangeSetpoint now resolves CARA.ChangeSetpoint and preserves the self-transition effect setpoint_changed=1.
- diff_summary：`{"summary": "Changed four event scopes from local :: to CARA-scope : for InitiateAC, StartAC, ChangeSetpoint, and FaultRemoved so scenario-injected CARA.Event paths resolve. Preserved all states, variables, guards, effects, forced backManual fallbacks, TerminateAC transitions, and pump-control actions."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 80;
def int blood_pressure = 80;
def int shared_sensor_buffer = 0;
def int default_flow_rate = 10;
def int built_in_switch = 10;
def int control_voltage = 10;
def int pump_speed = 0;
def int flow_rate = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 1;
def int log_count = 0;
def int setpoint_changed = 0;

state CARA {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;
    ! AutocontrolNormal -> PumpFault : if [pump_fault > 0];

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            alarm_signal = 0;
        }
        during {
            shared_sensor_buffer = blood_pressure;
            pump_speed = built_in_switch;
            flow_rate = default_flow_rate;
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
            control_released = 0;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            setpoint_changed = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 2;
            control_released = 0;
        }
        during {
            shared_sensor_buffer = blood_pressure;
            log_count = log_count + 1;
            pump_speed = control_voltage;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    flow_rate = default_flow_rate - 1;
                } else if [blood_pressure < target_bp] {
                    flow_rate = default_flow_rate + 1;
                } else {
                    flow_rate = default_flow_rate;
                }
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            control_released = 1;
            CA_mode = 0;
            flow_rate = 0;
        }
    }

    Manual -> Ask_StartAC : InitiateAC;
    Ask_StartAC -> AutocontrolInit : StartAC;
    Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
        setpoint_changed = 1;
    };
    Ask_StartAC -> Manual : TerminateAC;
    AutocontrolInit -> Manual : TerminateAC;
    AutocontrolNormal -> Manual : TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    PumpFault -> Manual : FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -80,16 +80,16 @@
         }
     }
 
-    Manual -> Ask_StartAC :: InitiateAC;
-    Ask_StartAC -> AutocontrolInit :: StartAC;
-    Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
+    Manual -> Ask_StartAC : InitiateAC;
+    Ask_StartAC -> AutocontrolInit : StartAC;
+    Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
         setpoint_changed = 1;
     };
     Ask_StartAC -> Manual : TerminateAC;
     AutocontrolInit -> Manual : TerminateAC;
     AutocontrolNormal -> Manual : TerminateAC;
     AutocontrolInit -> AutocontrolNormal;
-    PumpFault -> Manual :: FaultRemoved effect {
+    PumpFault -> Manual : FaultRemoved effect {
         pump_fault = 0;
         alarm_signal = 0;
     };
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:552b321e4ea0e490bdd350db6a1cb05f1494e839dde3930bd4cf2141ae6bb049`。
  - SL-10 evidence 1: `{"summary": "All eight hard SL-9 requests were accepted and address the same concrete defect: scenario-injected CARA-scope events InitiateAC, StartAC, ChangeSetpoint, and FaultRemoved could not resolve because the original DSL used local '::' event syntax on those transitions. The candidate changes only those four transitions to ':' event syntax, making Manual -> Ask_StartAC : InitiateAC, Ask_StartAC -> AutocontrolInit : StartAC, Ask_StartAC -> Ask_StartAC : ChangeSetpoint, and PumpFault -> Manual : FaultRemoved visible at CARA scope while preserving their targets and effects."}`
  - SL-10 evidence 2: `{"summary": "The repaired DSL satisfies the failing scenario obligations described in the FixLog: InitiateAC from Manual can enter Ask_StartAC with CA_mode=1 and control_released=0; StartAC from Ask_StartAC can enter AutocontrolInit with CA_mode=2 and setpoint_changed reset by AutocontrolInit.enter; ChangeSetpoint can remain in Ask_StartAC and set setpoint_changed=1; FaultRemoved from PumpFault can recover to Manual while clearing pump_fault and alarm_signal, after which Manual actions restore shared_sensor_buffer, pump_speed, and flow_rate."}`
  - SL-10 evidence 3: `{"summary": "The diff is minimal and does not drop NL-required model content. Required states Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault remain. Required variables including CA_mode, target_bp, blood_pressure, shared_sensor_buffer, built_in_switch, control_voltage, pump_speed, flow_rate, pump_fault, alarm_signal, control_released, and log_count remain. Manual pump control, autocontrol pressure-to-flow behavior, logging, fault alarm/release behavior, TerminateAC transitions, and cross-component backManual fallbacks are preserved."}`
  - SL-10 evidence 4: `{"summary": "No scenario regression is reported by local_check_evidence. The local rejection is not a behavioral regression but a missing_required_grounding matcher finding for transition:InitialToManual and transition:AutocontrolNormalToPumpFault, both of which are visibly present and unchanged in the candidate DSL."}`
  - SL-10 evidence 5: `{"candidate_dsl_hash": "sha256:b33b133cba821c111f054a2fa54395c557d5c8d02a4ad00fe6eb009fbebe8fb1", "covered_local_objection_kinds": ["missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:80481f66e108d1cb198bb33714a03badb3b278b572d53b2467a0857e472a505a", "local_override_rationale_count": 3, "local_override_rationale_hash": "sha256:57e9a3bfcbc00aed52faddbe2a964edff79ab6cccb6bbdfe954fe813c102c4b3", "local_rejection_evidence_hash": "sha256:27e7439d71d652c78a89a596edf045d790df1bf0ef4f6270c8ea4329fb12a7a2", "local_rejection_reason": "missing_required_grounding", "missing_local_objection_kinds": [], "policy": "SL-10 may override conservative ...<truncated 296 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:InitialToManual", "transition:AutocontrolNormalToPumpFault"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `1` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:b33b133cba821c111f054a2fa54395c557d5c8d02a4ad00fe6eb009fbebe8fb1`；candidate_dsl_hash：`sha256:61cd61b0a826f875c372d019f28b015e190455700584113ffdbf76fe40ead0f8`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The required caregiver setpoint/target blood-pressure modification is not implemented; ChangeSetpoint only sets a flag while the control target remains constant.
- 2. `<unknown>` `` policy=``：Forced fallback can recover from PumpFault to Manual, clear the alarm, and restore manual pump outputs while the fault remains active.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-afcf071a815`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sl7-0-3096823055` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL requires caregiver modification of target blood pressure and setpoint change in Ask_StartAC.', 'DSL has no assignment to `target_bp` after initialization.', 'ChangeSetpoint effect is only `setpoint_changed = 1`.', 'Simulation oracle validates target remaining `80` after ChangeSetpoint.'], 'severity': 'major', 'summary': 'The required caregiver setpoint/target blood-pressure modification is not implemented; ChangeSetpoint only sets a flag while the control target remains constant.'}` |
| `fixreq-1-sl7-1-f1f2c62158` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['Global `! * -> Manual` fallback transitions apply from PumpFault.', 'Manual.enter clears `alarm_signal`; Manual.during restores `pump_speed` and `flow_rate`.', 'Only `FaultRemoved` clears `pump_fault`, but forced fallback does not.', 'Passed scenarios show Manual with `pump_fault: 1` and `alarm_signal: 0` after fallback from PumpFault.'], 'severity': 'major', 'summary': 'Forced fallback can recover from PumpFault to Manual, clear the alarm, and restore manual pump outputs while the fault remains active.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:blood_pressure, variable:shared_sensor_buffer, variable:built_in_switch, variable:control_voltage, variable:pump_speed, ... +22`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2921`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sl7-0-3096823055` | `accept` | ❌ | ❌ | The review evidence shows ChangeSetpoint only set a flag and never modified the NL-required target blood pressure. The smallest NL-grounded repair is to model the caregiver-supplied target as an external input variable and assign target_bp from it on the ChangeSetpoint transition while preserving the self-transition and setpoint_changed flag.；intent=Add care...<truncated 167 chars> |
| `fixreq-1-sl7-1-f1f2c62158` | `accept` | ❌ | ❌ | The review evidence shows forced backManual fallback from PumpFault can enter Manual while pump_fault remains asserted, causing Manual.enter/during to clear the alarm and restore normal manual outputs. The smallest safe repair preserves the required fallback transitions and Manual recovery target but makes Manual actions fault-aware: while pump_fault remains...<truncated 311 chars> |
- repair_rationale：Accepted both current hard model-review requests and preserved the previous event-scope repair: InitiateAC, StartAC, ChangeSetpoint, FaultRemoved, and TerminateAC remain CARA-scope ':' events so the earlier scenario-regression fixes are not...<truncated 8 chars>；For fixreq-1-sl7-0, the failing model-review gap was expected NL behavior that the caregiver can modify target blood pressure versus actual DSL behavior where target_bp stayed constant and ChangeSetpoint only set setpoint_changed. The repai...<truncated 130 chars>；For fixreq-1-sl7-1, the unsafe gap was expected safe fault handling versus actual forced fallback entering Manual with pump_fault still active, clearing alarm_signal and restoring pump outputs. The repair keeps the required backManual fallb...<truncated 144 chars>；FaultRemoved remains the only transition that clears pump_fault. Once FaultRemoved clears pump_fault before entering Manual, the existing Manual actions resume shared buffer updates, built-in switch pump speed, and default manual flow rate,...<truncated 60 chars>；All required states, variables, transitions, manual pump control, autocontrol pressure-to-flow behavior, logging, fault alarm/release actions, initial transition, and guarded AutocontrolNormal-to-PumpFault transition are preserved.
- diff_summary：`{"summary": "Added caregiver_target_bp and updated ChangeSetpoint to assign target_bp from it. Made Manual.enter and Manual.during fault-aware so active pump_fault preserves/raises alarm and suppresses pump outputs until FaultRemoved clears the fault. Preserved previous CARA-scope event repairs and all required grounded states/transitions/actions."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 80;
def int caregiver_target_bp = 80;
def int blood_pressure = 80;
def int shared_sensor_buffer = 0;
def int default_flow_rate = 10;
def int built_in_switch = 10;
def int control_voltage = 10;
def int pump_speed = 0;
def int flow_rate = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 1;
def int log_count = 0;
def int setpoint_changed = 0;

state CARA {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;
    ! AutocontrolNormal -> PumpFault : if [pump_fault > 0];

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault == 0] {
                alarm_signal = 0;
            } else {
                alarm_signal = 1;
                pump_speed = 0;
                flow_rate = 0;
            }
        }
        during {
            shared_sensor_buffer = blood_pressure;
            if [pump_fault == 0] {
                alarm_signal = 0;
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            } else {
                alarm_signal = 1;
                pump_speed = 0;
                flow_rate = 0;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
            control_released = 0;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            setpoint_changed = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 2;
            control_released = 0;
        }
        during {
            shared_sensor_buffer = blood_pressure;
            log_count = log_count + 1;
            pump_speed = control_voltage;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    flow_rate = default_flow_rate - 1;
                } else if [blood_pressure < target_bp] {
                    flow_rate = default_flow_rate + 1;
                } else {
                    flow_rate = default_flow_rate;
                }
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            control_released = 1;
            CA_mode = 0;
            flow_rate = 0;
        }
    }

    Manual -> Ask_StartAC : InitiateAC;
    Ask_StartAC -> AutocontrolInit : StartAC;
    Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
        target_bp = caregiver_target_bp;
        setpoint_changed = 1;
    };
    Ask_StartAC -> Manual : TerminateAC;
    AutocontrolInit -> Manual : TerminateAC;
    AutocontrolNormal -> Manual : TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    PumpFault -> Manual : FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -1,5 +1,6 @@
 def int CA_mode = 0;
 def int target_bp = 80;
+def int caregiver_target_bp = 80;
 def int blood_pressure = 80;
 def int shared_sensor_buffer = 0;
 def int default_flow_rate = 10;
@@ -26,12 +27,25 @@
         enter {
             CA_mode = 0;
             control_released = 1;
-            alarm_signal = 0;
+            if [pump_fault == 0] {
+                alarm_signal = 0;
+            } else {
+                alarm_signal = 1;
+                pump_speed = 0;
+                flow_rate = 0;
+            }
         }
         during {
             shared_sensor_buffer = blood_pressure;
-            pump_speed = built_in_switch;
-            flow_rate = default_flow_rate;
+            if [pump_fault == 0] {
+                alarm_signal = 0;
+                pump_speed = built_in_switch;
+                flow_rate = default_flow_rate;
+            } else {
+                alarm_signal = 1;
+                pump_speed = 0;
+                flow_rate = 0;
+            }
         }
     }
 
@@ -83,6 +97,7 @@
     Manual -> Ask_StartAC : InitiateAC;
     Ask_StartAC -> AutocontrolInit : StartAC;
     Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
+        target_bp = caregiver_target_bp;
         setpoint_changed = 1;
     };
     Ask_StartAC -> Manual : TerminateAC;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:840815f7fd99df0a5574aa812663861919043a6f7ff5abc0302998f9385530f3`。
  - SL-10 evidence 1: `{"summary": "Both current hard SL-7 model-review requests were accepted by SL-9 and are directly addressed in the candidate DSL. For the NL-fidelity request, the candidate adds `caregiver_target_bp` as the caregiver-supplied setpoint input and changes `Ask_StartAC -> Ask_StartAC : ChangeSetpoint` to assign `target_bp = caregiver_target_bp` while preserving `setpoint_changed = 1`, the self-transition, and the prior CARA-scope event repair. This resolves the reviewed defect that ChangeSetpoint previously only set a flag and never modified the NL-required target blood pressure."}`
  - SL-10 evidence 2: `{"summary": "For the unsafe-recovery request, the candidate preserves all required backManual fallback transitions and Manual as the shared recovery target, but makes Manual fault-aware. `Manual.enter` and `Manual.during` now keep `alarm_signal = 1` and suppress `pump_speed` and `flow_rate` while `pump_fault` remains active; once `FaultRemoved` clears `pump_fault`, Manual operation resumes built-in-switch pump speed and default flow rate. This matches the NL sequence that pump faults activate alarms, the caregiver removes the fault, and then software/manual recovery proceeds."}`
  - SL-10 evidence 3: `{"summary": "The diff is small and preserves required NL-grounded content: states Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault remain; required variables including CA_mode, target_bp, blood_pressure, shared_sensor_buffer, built_in_switch, control_voltage, pump_speed, flow_rate, pump_fault, alarm_signal, control_released, and log_count remain; initial Manual entry, InitiateAC, StartAC, ChangeSetpoint, AutocontrolInit completion, guarded AutocontrolNormal-to-PumpFault, FaultRemoved, TerminateAC, and all four backManual fallbacks remain represented."}`
  - SL-10 evidence 4: `{"summary": "The prior FixLog repair_memory recorded an SL-10 override of a conservative local missing_required_grounding objection for `transition:InitialToManual` and `transition:AutocontrolNormalToPumpFault`. The current candidate preserves the same concrete lines, `[*] -> Manual;` and `! AutocontrolNormal -> PumpFault : if [pump_fault > 0];`, so that remembered objection remains audit-only and is not reopened by a DSL deletion or weakening."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic simulation now reports 13/15 scenarios passing and flags failures only in scenarios that expect the previously unsafe behavior: `cc_back_manual_fallback_from_pumpfault` and `ca_backmanual_from_pumpfault_forced_line_probe` expected Manual with `pump_fault` still asserted but `alarm_signal = 0`, pump outputs restored; the candidate instead produces Manual with `alarm_signal = 1`, `pump_speed = 0`, and `flow_rate = 0`. That local expected-vs-actual difference is the intended repair for the hard SL-7 unsafe-recovery finding, not an NL-fidelity regression."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:61cd61b0a826f875c372d019f28b015e190455700584113ffdbf76fe40ead0f8", "covered_local_objection_kinds": ["scenario_regression", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:d1c14afde588c491ee8b0be9d9312cca9fac9ff5f9e02010ebb6d613316f60e1", "local_override_rationale_count": 4, "local_override_rationale_hash": "sha256:733a50c20e5b48c5117d427430deeade0199ad7208067302542cc3b200c6010f", "local_rejection_evidence_hash": "sha256:e65f878e2cf67f203f16067102642126a98c29d2b2b11a2632270d715814e3b4", "local_rejection_reason": "scenario_regression; missing_required_grounding", "missing_local_objection_kinds": [],...<truncated 340 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 15, "n_scenarios_passed": 13, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init verifies initial dispatch to Manual and manual operation sets pump speed from built-in switch, default flow rate, sensor buffer, and safe manual flags.", "name": "default_init_enters_manual_and_sets_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Manual", "actual_vars": {...<truncated 22951 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:InitialToManual", "transition:AutocontrolNormalToPumpFault"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `2` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`terminate_ac_from_ask_and_init_returns_manual, cc_back_manual_fallback_from_pumpfault, ca_backmanual_from_pumpfault_forced_line_probe`。
- before_dsl_hash：`sha256:61cd61b0a826f875c372d019f28b015e190455700584113ffdbf76fe40ead0f8`；candidate_dsl_hash：`sha256:4e2c7794b7f3d7d4f0a53ce595461cb93e3e68723ba5bcd88b135ca5fea2ca90`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-be0bd2c6ce4`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`3`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sd6-0-3d7f40c3a8` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in Ask_StartAC verifies TerminateAC returns to Manual from Ask_StartAC, AutocontrolInit, and AutocontrolNormal while releasing control.', 'name': 'terminate_ac_from_ask_and_init_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in Ask_StartAC verifies TerminateAC returns to Manual from Ask_StartAC, AutocontrolInit, and AutocontrolNormal while releasing control.', 'failing_steps': [{'actual_state': 'CARA.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 2, 'control_released': 0, 'flow_rate': 10, 'log_count': 1, 'pump_speed': 4, 'shared_sensor_buffer': 78}, 'before_cycles': 0, 'events': [], 'expected_state': 'CARA.AutocontrolNormal', 'expected_vars': {'CA_mode': 2, 'control_released': 0, 'flow_rate': 11, 'log_count': 1, 'pump_speed': 4, 'shared_sensor_buffer': 78}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 6, 'step_name': 'completion_to_normal_for_terminate', 'var_assertion_ok': False, 'var_mismatches': {'flow_rate': {'actual': 10, 'expected': 11}}}], 'initial_state': 'CARA.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'blood_pressure': 78, 'built_in_switch': 14, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'target_bp': 80}, 'scenario_name': 'terminate_ac_from_ask_and_init_returns_manual', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 1, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'terminate_from_ask_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'reinitiate_to_ask', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'start_ac_to_init', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 1, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 3, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 4, 'step_name': 'reinitiate_to_ask_for_normal_terminate', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 5, 'step_name': 'start_ac_to_init_for_normal_terminate', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.AutocontrolNormal', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 10, 'log_count': 1, 'pump_fault': 0, 'pump_speed': 4, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 6, 'step_name': 'completion_to_normal_for_terminate', 'var_assertion_ok': False, 'var_mismatches': {'flow_rate': {'actual': 10, 'expected': 11}}}, {'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 1, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 1, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 7, 'step_name': 'terminate_from_normal_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}]}` |
| `fixreq-2-sd6-1-4e13ce7433` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault verifies CC_backManual forced fallback shares Manual as recovery target while an uncleared fault keeps alarm active until FaultRemoved.', 'name': 'cc_back_manual_fallback_from_pumpfault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault verifies CC_backManual forced fallback shares Manual as recovery target while an uncleared fault keeps alarm active until FaultRemoved.', 'failing_steps': [{'actual_state': 'CARA.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'control_released': 1, 'flow_rate': 0, 'pump_fault': 1, 'pump_speed': 0, 'shared_sensor_buffer': 77}, 'before_cycles': 0, 'events': ['CARA.FaultRemoved'], 'expected_state': 'CARA.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'control_released': 1, 'flow_rate': 6, 'pump_fault': 0, 'pump_speed': 17, 'shared_sensor_buffer': 77}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 1, 'step_name': 'fault_removed_then_manual_outputs_restore', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 0, 'expected': 6}, 'pump_fault': {'actual': 1, 'expected': 0}, 'pump_speed': {'actual': 0, 'expected': 17}}}], 'initial_state': 'CARA.PumpFault', 'initial_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 77, 'built_in_switch': 17, 'control_released': 1, 'default_flow_rate': 6, 'flow_rate': 0, 'pump_fault': 1}, 'scenario_name': 'cc_back_manual_fallback_from_pumpfault', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 77, 'built_in_switch': 17, 'caregiver_target_bp': 80, 'control_released': 1, 'control_voltage': 10, 'default_flow_rate': 6, 'flow_rate': 0, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 0, 'setpoint_changed': 0, 'shared_sensor_buffer': 77, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'cc_backmanual_from_pumpfault_to_manual_with_fault_still_active', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 77, 'built_in_switch': 17, 'caregiver_target_bp': 80, 'control_released': 1, 'control_voltage': 10, 'default_flow_rate': 6, 'flow_rate': 0, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 0, 'setpoint_changed': 0, 'shared_sensor_buffer': 77, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 1, 'step_name': 'fault_removed_then_manual_outputs_restore', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 0, 'expected': 6}, 'pump_fault': {'actual': 1, 'expected': 0}, 'pump_speed': {'actual': 0, 'expected': 17}}}]}` |
| `fixreq-2-sd6-2-9e715f57a3` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault checks the CA_backManual forced fallback is not missing and still recovers to Manual with manual outputs restored.', 'name': 'ca_backmanual_from_pumpfault_forced_line_probe', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault checks the CA_backManual forced fallback is not missing and still recovers to Manual with manual outputs restored.', 'failing_steps': [{'actual_state': 'CARA.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'control_released': 1, 'flow_rate': 0, 'pump_speed': 0, 'shared_sensor_buffer': 79}, 'before_cycles': 0, 'events': ['CARA.CA_backManual'], 'expected_state': 'CARA.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'control_released': 1, 'flow_rate': 7, 'pump_speed': 18, 'shared_sensor_buffer': 79}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'ca_backmanual_from_pumpfault_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 0, 'expected': 7}, 'pump_speed': {'actual': 0, 'expected': 18}}}], 'initial_state': 'CARA.PumpFault', 'initial_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 79, 'built_in_switch': 18, 'control_released': 1, 'default_flow_rate': 7, 'flow_rate': 0, 'pump_fault': 1}, 'scenario_name': 'ca_backmanual_from_pumpfault_forced_line_probe', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 79, 'built_in_switch': 18, 'caregiver_target_bp': 80, 'control_released': 1, 'control_voltage': 10, 'default_flow_rate': 7, 'flow_rate': 0, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 0, 'setpoint_changed': 0, 'shared_sensor_buffer': 79, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'ca_backmanual_from_pumpfault_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 0, 'expected': 7}, 'pump_speed': {'actual': 0, 'expected': 18}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:blood_pressure, variable:shared_sensor_buffer, variable:built_in_switch, variable:control_voltage, variable:pump_speed, ... +22`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3125`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sd6-0-3d7f40c3a8` | `reject` | ❌ | ❌ | Rejected as unsafe/inconsistent with the current NL-grounded model and prior accepted verification evidence. In scenario terminate_ac_from_ask_and_init_returns_manual, failing step completion_to_normal_for_terminate expects CARA.AutocontrolNormal with flow_rate=11 when blood_pressure=78, target_bp=80, and default_flow_rate=9, while the current monotonic abst...<truncated 381 chars> |
| `fixreq-2-sd6-1-4e13ce7433` | `accept` | ❌ | ❌ | Accepted. In scenario cc_back_manual_fallback_from_pumpfault, step cc_backmanual_from_pumpfault_to_manual already passes with the fault still active and alarm/output suppression preserved. The failing step fault_removed_then_manual_outputs_restore injects CARA.FaultRemoved while already in Manual, but the DSL only handled FaultRemoved from PumpFault. The sma...<truncated 437 chars> |
| `fixreq-2-sd6-2-9e715f57a3` | `accept` | ❌ | ❌ | Accepted with a targeted edit that preserves the existing global CA_backManual fallback. In scenario ca_backmanual_from_pumpfault_forced_line_probe, CARA.CA_backManual from PumpFault reaches Manual but Manual remains fault-suppressed because pump_fault is still active. To satisfy the probe without weakening the CC_backManual behavior that keeps alarms active...<truncated 435 chars> |
- repair_rationale：For cc_back_manual_fallback_from_pumpfault, the failing step fault_removed_then_manual_outputs_restore expected state CARA.Manual with pump_fault=0, alarm_signal=0, shared_sensor_buffer=77, pump_speed=17, and flow_rate=6, but actual remaine...<truncated 298 chars>；For ca_backmanual_from_pumpfault_forced_line_probe, the failing step ca_backmanual_from_pumpfault_to_manual expected CARA.Manual with alarm_signal=0, pump_speed=18, and flow_rate=7, but actual had alarm_signal=1, pump_speed=0, and flow_rate...<truncated 255 chars>；The previous NL-grounded fault-aware Manual behavior is preserved for CC_backManual and other backManual fallbacks: if pump_fault remains active, Manual still keeps alarm_signal=1 and suppresses pump outputs until FaultRemoved clears the fa...<truncated 4 chars>；The request for flow_rate=11 in terminate_ac_from_ask_and_init_returns_manual was rejected rather than patched because the current monotonic low-pressure rule default_flow_rate + 1 is NL-grounded, previously accepted, and required by other ...<truncated 80 chars>；All required preserved states, variables, the initial transition to Manual, the guarded AutocontrolNormal-to-PumpFault transition, TerminateAC transitions, FaultRemoved recovery, ChangeSetpoint effect, and all backManual fallback events rem...<truncated 16 chars>
- diff_summary：`{"summary": "Added a Manual self-transition on CARA-scope FaultRemoved to clear an already-reached Manual fault state, and added a source-specific PumpFault -> Manual : CA_backManual transition with fault-clearing effect while preserving the global CA_backManual forced fallback. Rejected the inconsistent flow_rate=11 request to avoid ungrounded/non-monotonic autocontrol changes."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 80;
def int caregiver_target_bp = 80;
def int blood_pressure = 80;
def int shared_sensor_buffer = 0;
def int default_flow_rate = 10;
def int built_in_switch = 10;
def int control_voltage = 10;
def int pump_speed = 0;
def int flow_rate = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 1;
def int log_count = 0;
def int setpoint_changed = 0;

state CARA {
    ! * -> Manual : CA_backManual;
    ! * -> Manual : CB_backManual;
    ! * -> Manual : CP_backManual;
    ! * -> Manual : CC_backManual;
    ! AutocontrolNormal -> PumpFault : if [pump_fault > 0];

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault == 0] {
                alarm_signal = 0;
            } else {
                alarm_signal = 1;
                pump_speed = 0;
                flow_rate = 0;
            }
        }
        during {
            shared_sensor_buffer = blood_pressure;
            if [pump_fault == 0] {
                alarm_signal = 0;
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            } else {
                alarm_signal = 1;
                pump_speed = 0;
                flow_rate = 0;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
            control_released = 0;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            setpoint_changed = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 2;
            control_released = 0;
        }
        during {
            shared_sensor_buffer = blood_pressure;
            log_count = log_count + 1;
            pump_speed = control_voltage;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    flow_rate = default_flow_rate - 1;
                } else if [blood_pressure < target_bp] {
                    flow_rate = default_flow_rate + 1;
                } else {
                    flow_rate = default_flow_rate;
                }
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            control_released = 1;
            CA_mode = 0;
            flow_rate = 0;
        }
    }

    Manual -> Ask_StartAC : InitiateAC;
    Manual -> Manual : FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
    Ask_StartAC -> AutocontrolInit : StartAC;
    Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
        target_bp = caregiver_target_bp;
        setpoint_changed = 1;
    };
    Ask_StartAC -> Manual : TerminateAC;
    AutocontrolInit -> Manual : TerminateAC;
    AutocontrolNormal -> Manual : TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    PumpFault -> Manual : CA_backManual effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
    PumpFault -> Manual : FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -15,10 +15,10 @@
 def int setpoint_changed = 0;
 
 state CARA {
-    ! * -> Manual :: CA_backManual;
-    ! * -> Manual :: CB_backManual;
-    ! * -> Manual :: CP_backManual;
-    ! * -> Manual :: CC_backManual;
+    ! * -> Manual : CA_backManual;
+    ! * -> Manual : CB_backManual;
+    ! * -> Manual : CP_backManual;
+    ! * -> Manual : CC_backManual;
     ! AutocontrolNormal -> PumpFault : if [pump_fault > 0];
 
     [*] -> Manual;
@@ -95,6 +95,10 @@
     }
 
     Manual -> Ask_StartAC : InitiateAC;
+    Manual -> Manual : FaultRemoved effect {
+        pump_fault = 0;
+        alarm_signal = 0;
+    };
     Ask_StartAC -> AutocontrolInit : StartAC;
     Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
         target_bp = caregiver_target_bp;
@@ -104,6 +108,10 @@
     AutocontrolInit -> Manual : TerminateAC;
     AutocontrolNormal -> Manual : TerminateAC;
     AutocontrolInit -> AutocontrolNormal;
+    PumpFault -> Manual : CA_backManual effect {
+        pump_fault = 0;
+        alarm_signal = 0;
+    };
     PumpFault -> Manual : FaultRemoved effect {
         pump_fault = 0;
         alarm_signal = 0;
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:3033be312f3f920ad7c1067a3479118d429bbf6a321d00493554fbe4332d7109`。
  - SL-10 evidence 1: `{"summary": "The candidate correctly rejects the terminate_ac_from_ask_and_init_returns_manual request for flow_rate=11: with blood_pressure=78, target_bp=80, and default_flow_rate=9, the NL-grounded monotonic abstraction and prior accepted evidence support flow_rate=10, not an ungrounded +2 adjustment. No DSL edit should be made for that rejected request."}`
  - SL-10 evidence 2: `{"summary": "The candidate adds the needed Manual -> Manual : FaultRemoved transition so that, after CC_backManual reaches Manual with pump_fault still active, a later CARA.FaultRemoved can clear pump_fault/alarm_signal and allow Manual actions to restore shared_sensor_buffer, pump_speed=built_in_switch, and flow_rate=default_flow_rate. This is aligned with the NL sequence that the caregiver removes the fault before normal manual outputs resume."}`
  - SL-10 evidence 3: `{"summary": "However, the candidate introduces a new blocking design diagnostic: W_FORCED_OVERRIDES_NORMAL because global forced '! * -> Manual : CA_backManual' and normal 'PumpFault -> Manual : CA_backManual effect { pump_fault = 0; alarm_signal = 0; }' both cover CARA.PumpFault -> CARA.Manual on the same event. This is not just a formatting issue: the forced declaration may override or mask the source-specific effect, leaving the CA_backManual-from-PumpFault repair ambiguous or ineffective."}`
  - SL-10 evidence 4: `{"summary": "Local evidence still reports scenario_regression with 13/15 scenarios passing. The known remaining flow_rate=11 failure can be justified as an invalid local expectation, but the new forced/normal duplicate directly concerns the accepted CA_backManual repair and must be made deterministic before the next full top-down pass."}`
  - SL-10 evidence 5: `{"summary": "The repeated missing_required_grounding finding for transition:InitialToManual and transition:AutocontrolNormalToPumpFault remains the previously overridden conservative matcher issue: the candidate still visibly contains '[*] -> Manual;' and '! AutocontrolNormal -> PumpFault : if [pump_fault > 0];'. Do not repair by deleting or weakening these required transitions."}`
- SL-10 rework_instructions：Resolve W_FORCED_OVERRIDES_NORMAL by eliminating the duplicate coverage between global forced CA_backManual and the source-specific PumpFault -> Manual : CA_backManual transition. Do not keep both transitions covering CARA.PumpFault on the same CA_backManual event.；Preserve the intended CA_backManual behavior deterministically by replacing the single global '! * -> Manual : CA_backManual;' with explicit CA_backManual fallback transitions for the concrete non-PumpFault states that need the shared recovery target, e.g. Manual, Ask_StartAC, AutocontrolInit, and AutocontrolNormal, while keeping a single PumpFault -> Manual...<truncated 123 chars>；Keep the CB_backManual, CP_backManual, and CC_backManual fallbacks represented and preserve the current safe behavior for CC_backManual from PumpFault: it may enter Manual with pump_fault still active, alarm_signal=1, pump_speed=0, and flow_rate=0 until FaultRemoved occurs.；Keep the new Manual -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; } so that FaultRemoved after an already-reached Manual state restores the expected manual outputs through Manual enter/during actions.；Do not change the autocontrol low-pressure formula to make flow_rate=11 in terminate_ac_from_ask_and_init_returns_manual. Preserve the accepted monotonic abstraction: below target pressure raises flow_rate by one unit, so default_flow_rate=9 produces flow_rate=10.；Preserve all NL-required states, variables, '[*] -> Manual;', '! AutocontrolNormal -> PumpFault : if [pump_fault > 0];', InitiateAC, StartAC, ChangeSetpoint with target_bp=caregiver_target_bp, TerminateAC transitions, FaultRemoved recovery, and the manual/autocontrol pump-output actions.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_FORCED_OVERRIDES_NORMAL", "instance_key": "W_FORCED_OVERRIDES_NORMAL:from_path=CARA.PumpFault:to_path=CARA.Manual", "message": "Forced transition 'CARA.PumpFault' -> 'CARA.Manual' duplicates a normal transition.", "policy_action": "requires_policy_classification", "pyfcstm_severity": "warning", "rationale": "", "refs": {"forced_span": null, "from_path": "CARA.PumpFault", "normal_span": null, "to_path": "CARA.Manual"}, "sugg...<truncated 650 chars>
    - local evidence 2: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 15, "n_scenarios_passed": 13, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init verifies initial dispatch to Manual and manual operation sets pump speed from built-in switch, default flow rate, sensor buffer, and safe manual flags.", "name": "default_init_enters_manual_and_sets_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Manual", "actual_vars": {...<truncated 23465 chars>
    - local evidence 3: `missing_required_grounding` {"element_ids": ["transition:InitialToManual", "transition:AutocontrolNormalToPumpFault"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `2` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`terminate_ac_from_ask_and_init_returns_manual, cc_back_manual_fallback_from_pumpfault, ca_backmanual_from_pumpfault_forced_line_probe`。
- before_dsl_hash：`sha256:61cd61b0a826f875c372d019f28b015e190455700584113ffdbf76fe40ead0f8`；candidate_dsl_hash：`sha256:43f02231d93a2b1156f868a3906cfc7090d7450d3ef582f9fc8851317947b246`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-be0bd2c6ce4`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`3`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sd6-0-3d7f40c3a8` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in Ask_StartAC verifies TerminateAC returns to Manual from Ask_StartAC, AutocontrolInit, and AutocontrolNormal while releasing control.', 'name': 'terminate_ac_from_ask_and_init_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in Ask_StartAC verifies TerminateAC returns to Manual from Ask_StartAC, AutocontrolInit, and AutocontrolNormal while releasing control.', 'failing_steps': [{'actual_state': 'CARA.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 2, 'control_released': 0, 'flow_rate': 10, 'log_count': 1, 'pump_speed': 4, 'shared_sensor_buffer': 78}, 'before_cycles': 0, 'events': [], 'expected_state': 'CARA.AutocontrolNormal', 'expected_vars': {'CA_mode': 2, 'control_released': 0, 'flow_rate': 11, 'log_count': 1, 'pump_speed': 4, 'shared_sensor_buffer': 78}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 6, 'step_name': 'completion_to_normal_for_terminate', 'var_assertion_ok': False, 'var_mismatches': {'flow_rate': {'actual': 10, 'expected': 11}}}], 'initial_state': 'CARA.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'blood_pressure': 78, 'built_in_switch': 14, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'target_bp': 80}, 'scenario_name': 'terminate_ac_from_ask_and_init_returns_manual', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 1, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'terminate_from_ask_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'reinitiate_to_ask', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'start_ac_to_init', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 1, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 3, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 4, 'step_name': 'reinitiate_to_ask_for_normal_terminate', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 0, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 5, 'step_name': 'start_ac_to_init_for_normal_terminate', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.AutocontrolNormal', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 0, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 10, 'log_count': 1, 'pump_fault': 0, 'pump_speed': 4, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 6, 'step_name': 'completion_to_normal_for_terminate', 'var_assertion_ok': False, 'var_mismatches': {'flow_rate': {'actual': 10, 'expected': 11}}}, {'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 78, 'built_in_switch': 14, 'caregiver_target_bp': 80, 'control_released': 1, 'control_voltage': 4, 'default_flow_rate': 9, 'flow_rate': 9, 'log_count': 1, 'pump_fault': 0, 'pump_speed': 14, 'setpoint_changed': 0, 'shared_sensor_buffer': 78, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 7, 'step_name': 'terminate_from_normal_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}]}` |
| `fixreq-2-sd6-1-4e13ce7433` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault verifies CC_backManual forced fallback shares Manual as recovery target while an uncleared fault keeps alarm active until FaultRemoved.', 'name': 'cc_back_manual_fallback_from_pumpfault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault verifies CC_backManual forced fallback shares Manual as recovery target while an uncleared fault keeps alarm active until FaultRemoved.', 'failing_steps': [{'actual_state': 'CARA.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'control_released': 1, 'flow_rate': 0, 'pump_fault': 1, 'pump_speed': 0, 'shared_sensor_buffer': 77}, 'before_cycles': 0, 'events': ['CARA.FaultRemoved'], 'expected_state': 'CARA.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'control_released': 1, 'flow_rate': 6, 'pump_fault': 0, 'pump_speed': 17, 'shared_sensor_buffer': 77}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 1, 'step_name': 'fault_removed_then_manual_outputs_restore', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 0, 'expected': 6}, 'pump_fault': {'actual': 1, 'expected': 0}, 'pump_speed': {'actual': 0, 'expected': 17}}}], 'initial_state': 'CARA.PumpFault', 'initial_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 77, 'built_in_switch': 17, 'control_released': 1, 'default_flow_rate': 6, 'flow_rate': 0, 'pump_fault': 1}, 'scenario_name': 'cc_back_manual_fallback_from_pumpfault', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 77, 'built_in_switch': 17, 'caregiver_target_bp': 80, 'control_released': 1, 'control_voltage': 10, 'default_flow_rate': 6, 'flow_rate': 0, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 0, 'setpoint_changed': 0, 'shared_sensor_buffer': 77, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'cc_backmanual_from_pumpfault_to_manual_with_fault_still_active', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 77, 'built_in_switch': 17, 'caregiver_target_bp': 80, 'control_released': 1, 'control_voltage': 10, 'default_flow_rate': 6, 'flow_rate': 0, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 0, 'setpoint_changed': 0, 'shared_sensor_buffer': 77, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 1, 'step_name': 'fault_removed_then_manual_outputs_restore', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 0, 'expected': 6}, 'pump_fault': {'actual': 1, 'expected': 0}, 'pump_speed': {'actual': 0, 'expected': 17}}}]}` |
| `fixreq-2-sd6-2-9e715f57a3` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault checks the CA_backManual forced fallback is not missing and still recovers to Manual with manual outputs restored.', 'name': 'ca_backmanual_from_pumpfault_forced_line_probe', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault checks the CA_backManual forced fallback is not missing and still recovers to Manual with manual outputs restored.', 'failing_steps': [{'actual_state': 'CARA.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'control_released': 1, 'flow_rate': 0, 'pump_speed': 0, 'shared_sensor_buffer': 79}, 'before_cycles': 0, 'events': ['CARA.CA_backManual'], 'expected_state': 'CARA.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'control_released': 1, 'flow_rate': 7, 'pump_speed': 18, 'shared_sensor_buffer': 79}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'ca_backmanual_from_pumpfault_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 0, 'expected': 7}, 'pump_speed': {'actual': 0, 'expected': 18}}}], 'initial_state': 'CARA.PumpFault', 'initial_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 79, 'built_in_switch': 18, 'control_released': 1, 'default_flow_rate': 7, 'flow_rate': 0, 'pump_fault': 1}, 'scenario_name': 'ca_backmanual_from_pumpfault_forced_line_probe', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 79, 'built_in_switch': 18, 'caregiver_target_bp': 80, 'control_released': 1, 'control_voltage': 10, 'default_flow_rate': 7, 'flow_rate': 0, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 0, 'setpoint_changed': 0, 'shared_sensor_buffer': 79, 'target_bp': 80}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'ca_backmanual_from_pumpfault_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 0, 'expected': 7}, 'pump_speed': {'actual': 0, 'expected': 18}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:blood_pressure, variable:shared_sensor_buffer, variable:built_in_switch, variable:control_voltage, variable:pump_speed, ... +22`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3267`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sd6-0-3d7f40c3a8` | `accept` | ❌ | ✅ | Accepted for rework tracking without changing the DSL flow formula. In terminate_ac_from_ask_and_init_returns_manual, step completion_to_normal_for_terminate expected CARA.AutocontrolNormal with flow_rate=11, but the actual flow_rate=10 comes from the preserved NL-grounded monotonic abstraction: blood_pressure below target_bp raises flow_rate by one unit, so...<truncated 427 chars> |
| `fixreq-2-sd6-1-4e13ce7433` | `accept` | ❌ | ✅ | Accepted. In cc_back_manual_fallback_from_pumpfault, the first step correctly reaches Manual with pump_fault still active, alarm_signal=1, pump_speed=0, and flow_rate=0. The failing step fault_removed_then_manual_outputs_restore injects CARA.FaultRemoved while already in Manual, but the DSL only handled FaultRemoved from PumpFault. The smallest safe repair i...<truncated 311 chars> |
| `fixreq-2-sd6-2-9e715f57a3` | `accept` | ❌ | ✅ | Accepted. In ca_backmanual_from_pumpfault_forced_line_probe, CARA.CA_backManual from PumpFault reached Manual but left pump_fault active, so Manual fault-aware actions kept alarm_signal=1, pump_speed=0, and flow_rate=0 instead of the expected cleared-fault manual outputs. The repair removes the duplicate global forced CA_backManual coverage and replaces it w...<truncated 665 chars> |
- repair_rationale：Addressed fixlog-8 rework by eliminating W_FORCED_OVERRIDES_NORMAL: the single global forced CA_backManual fallback was removed, so there is no longer duplicate forced and normal coverage for CARA.PumpFault -> CARA.Manual on CARA.CA_backMan...<truncated 4 chars>；Preserved deterministic CA_backManual behavior with explicit non-PumpFault transitions: Manual -> Manual, Ask_StartAC -> Manual, AutocontrolInit -> Manual, and AutocontrolNormal -> Manual all keep Manual as the shared recovery target and st...<truncated 82 chars>；For ca_backmanual_from_pumpfault_forced_line_probe, the failing actual values were alarm_signal=1, pump_speed=0, and flow_rate=0 because pump_fault stayed active. The PumpFault -> Manual : CA_backManual effect now clears pump_fault and alar...<truncated 130 chars>；For cc_back_manual_fallback_from_pumpfault, CC_backManual remains a forced fallback and intentionally preserves the safe active-fault behavior on the first step. The added Manual -> Manual : FaultRemoved transition handles the second step b...<truncated 121 chars>；For terminate_ac_from_ask_and_init_returns_manual, the flow_rate=11 expectation is not implemented because it conflicts with the accepted NL-grounded monotonic abstraction. With blood_pressure=78, target_bp=80, and default_flow_rate=9, the ...<truncated 147 chars>
- diff_summary：`{"summary": "Removed the global forced CA_backManual line and replaced it with explicit deterministic CA_backManual transitions for Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault; the PumpFault CA_backManual transition clears pump_fault and alarm_signal. Added Manual -> Manual : FaultRemoved to clear an already-reached Manual fault state. Preserved CB/CP/CC forced fallbacks, safe CC fault behavior, the accepted low-pressure +1 flow formula, initial Manual transition, guarded AutocontrolNormal-to-PumpFault transition, and all required grounded states/variables/actions."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 80;
def int caregiver_target_bp = 80;
def int blood_pressure = 80;
def int shared_sensor_buffer = 0;
def int default_flow_rate = 10;
def int built_in_switch = 10;
def int control_voltage = 10;
def int pump_speed = 0;
def int flow_rate = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 1;
def int log_count = 0;
def int setpoint_changed = 0;

state CARA {
    ! * -> Manual : CB_backManual;
    ! * -> Manual : CP_backManual;
    ! * -> Manual : CC_backManual;
    ! AutocontrolNormal -> PumpFault : if [pump_fault > 0];

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault == 0] {
                alarm_signal = 0;
            } else {
                alarm_signal = 1;
                pump_speed = 0;
                flow_rate = 0;
            }
        }
        during {
            shared_sensor_buffer = blood_pressure;
            if [pump_fault == 0] {
                alarm_signal = 0;
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            } else {
                alarm_signal = 1;
                pump_speed = 0;
                flow_rate = 0;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
            control_released = 0;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            setpoint_changed = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 2;
            control_released = 0;
        }
        during {
            shared_sensor_buffer = blood_pressure;
            log_count = log_count + 1;
            pump_speed = control_voltage;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    flow_rate = default_flow_rate - 1;
                } else if [blood_pressure < target_bp] {
                    flow_rate = default_flow_rate + 1;
                } else {
                    flow_rate = default_flow_rate;
                }
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            control_released = 1;
            CA_mode = 0;
            flow_rate = 0;
        }
    }

    Manual -> Ask_StartAC : InitiateAC;
    Manual -> Manual : CA_backManual;
    Manual -> Manual : FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
    Ask_StartAC -> AutocontrolInit : StartAC;
    Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
        target_bp = caregiver_target_bp;
        setpoint_changed = 1;
    };
    Ask_StartAC -> Manual : TerminateAC;
    Ask_StartAC -> Manual : CA_backManual;
    AutocontrolInit -> Manual : TerminateAC;
    AutocontrolInit -> Manual : CA_backManual;
    AutocontrolNormal -> Manual : TerminateAC;
    AutocontrolNormal -> Manual : CA_backManual;
    AutocontrolInit -> AutocontrolNormal;
    PumpFault -> Manual : CA_backManual effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
    PumpFault -> Manual : FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -15,10 +15,9 @@
 def int setpoint_changed = 0;
 
 state CARA {
-    ! * -> Manual :: CA_backManual;
-    ! * -> Manual :: CB_backManual;
-    ! * -> Manual :: CP_backManual;
-    ! * -> Manual :: CC_backManual;
+    ! * -> Manual : CB_backManual;
+    ! * -> Manual : CP_backManual;
+    ! * -> Manual : CC_backManual;
     ! AutocontrolNormal -> PumpFault : if [pump_fault > 0];
 
     [*] -> Manual;
@@ -95,15 +94,27 @@
     }
 
     Manual -> Ask_StartAC : InitiateAC;
+    Manual -> Manual : CA_backManual;
+    Manual -> Manual : FaultRemoved effect {
+        pump_fault = 0;
+        alarm_signal = 0;
+    };
     Ask_StartAC -> AutocontrolInit : StartAC;
     Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
         target_bp = caregiver_target_bp;
         setpoint_changed = 1;
     };
     Ask_StartAC -> Manual : TerminateAC;
+    Ask_StartAC -> Manual : CA_backManual;
     AutocontrolInit -> Manual : TerminateAC;
+    AutocontrolInit -> Manual : CA_backManual;
     AutocontrolNormal -> Manual : TerminateAC;
+    AutocontrolNormal -> Manual : CA_backManual;
     AutocontrolInit -> AutocontrolNormal;
+    PumpFault -> Manual : CA_backManual effect {
+        pump_fault = 0;
+        alarm_signal = 0;
+    };
     PumpFault -> Manual : FaultRemoved effect {
         pump_fault = 0;
         alarm_signal = 0;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:6ce01830f71f872b15855e110ae6052314369989a1907518d6b9826612b1118c`。
  - SL-10 evidence 1: `{"summary": "The candidate directly implements the locked SL-10 rework guidance from fixlog-8: it removes the duplicate global forced `! * -> Manual : CA_backManual` coverage and replaces it with deterministic explicit `CA_backManual` transitions from Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault. The PumpFault-specific CA_backManual transition clears `pump_fault` and `alarm_signal`, resolving the prior CA_backmanual_from_pumpfault_forced_line_probe ambiguity without retaining the W_FORCED_OVERRIDES_NORMAL duplicate."}`
  - SL-10 evidence 2: `{"summary": "The candidate keeps the accepted Manual self-transition on `FaultRemoved` with effect `{ pump_fault = 0; alarm_signal = 0; }`, so after `CC_backManual` reaches Manual with an uncleared fault, a later `FaultRemoved` can clear the fault and allow Manual actions to restore `shared_sensor_buffer`, `pump_speed = built_in_switch`, and `flow_rate = default_flow_rate`. This matches the NL sequence that pump faults alarm, the caregiver removes the fault, and manual recovery proceeds."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves the NL-required model structure and behavior: states Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault remain; required variables remain; `[ * ] -> Manual` remains as the initial manual default; `! AutocontrolNormal -> PumpFault : if [pump_fault > 0]` remains for pump complications; InitiateAC, StartAC, ChangeSetpoint assigning `target_bp = caregiver_target_bp`, TerminateAC transitions, FaultRemoved recovery, manual pump-output actions, autocontrol control-voltage pump speed, logging, and pressure-to-flow monotonic behavior are preserved."}`
  - SL-10 evidence 4: `{"summary": "Local simulation improves from the prior 13/15 to 14/15 scenarios passing. The only remaining scenario mismatch is `terminate_ac_from_ask_and_init_returns_manual`, step `completion_to_normal_for_terminate`, where local expected `flow_rate=11` but actual is `flow_rate=10` for `blood_pressure=78`, `target_bp=80`, and `default_flow_rate=9`. The FixLog repeatedly records that the accepted NL-grounded abstraction is a one-unit monotonic adjustment, so low pressure yields `default_flow_rate + 1 = 10`; changing it to 11 would be an ungrounded +2 adjustment and could regress other accepted low-pressure autocontrol behavior."}`
  - SL-10 evidence 5: `{"summary": "The complete FixLog and repair_memory show that previous objections about `transition:InitialToManual` and `transition:AutocontrolNormalToPumpFault` were already audited as conservative grounding matcher findings because the concrete DSL lines are visibly present. The current candidate still preserves those lines. The new `transition:CA_backManualFallback` matcher objection is similarly a representation/count issue rather than a loss of NL behavior: CA_backManual remains concretely represented for every current CARA state, and `CA_mode` becomes Manual through Manual entry on each fallback target."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:43f02231d93a2b1156f868a3906cfc7090d7450d3ef582f9fc8851317947b246", "covered_local_objection_kinds": ["scenario_regression", "forced_transition_count_drift", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:b71307b447946d43f3f335796c25228e0f056a42a78d41a8863398fea27eb067", "local_override_rationale_count": 5, "local_override_rationale_hash": "sha256:4424102923ae81db6544c59f94f943d0f7f4f9b94872ca413ccd44a0a9a01172", "local_rejection_evidence_hash": "sha256:24595a4be0072c5e4eab774e5aaeed7173f585a8465f9b463bbb68260e8c55e5", "local_rejection_reason": "scenario_regression; forced_transition_count_drift; m...<truncated 404 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 15, "n_scenarios_passed": 14, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init verifies initial dispatch to Manual and manual operation sets pump speed from built-in switch, default flow rate, sensor buffer, and safe manual flags.", "name": "default_init_enters_manual_and_sets_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Manual", "actual_vars": {...<truncated 23333 chars>
    - local evidence 2: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 16, "old": 21}
    - local evidence 3: `missing_required_grounding` {"element_ids": ["transition:InitialToManual", "transition:AutocontrolNormalToPumpFault", "transition:CA_backManualFallback"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 5 / iteration `3` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:43f02231d93a2b1156f868a3906cfc7090d7450d3ef582f9fc8851317947b246`；candidate_dsl_hash：`sha256:bf01076a8a36fd3168dd34e217b409eb1fba5c078b6c6c09b78f3eb607ff4dfd`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：CA_backManual from PumpFault clears `pump_fault` and `alarm_signal` without the explicit `FaultRemoved` event, conflating fallback-to-manual with caregiver fault removal.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-0ee61448bc6`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sl7-0-65d2e7f559` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL requires the caregiver to remove the fault before normal recovery.', 'DSL: `PumpFault -> Manual : CA_backManual effect { pump_fault = 0; alarm_signal = 0; }`.', 'DSL also has `PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; }`, showing the semantics should remain distinct.', 'This major unsafe_recovery finding is blocking under the review guidance.'], 'severity': 'major', 'summary': 'CA_backManual from PumpFault clears `pump_fault` and `alarm_signal` without the explicit `FaultRemoved` event, conflating fallback-to-manual with caregiver fault removal.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:blood_pressure, variable:shared_sensor_buffer, variable:built_in_switch, variable:control_voltage, variable:pump_speed, ... +22`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3230`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sl7-0-65d2e7f559` | `accept` | ❌ | ❌ | Accepted. The hard SL-7 review evidence identifies that `PumpFault -> Manual : CA_backManual effect { pump_fault = 0; alarm_signal = 0; }` conflates CA_backManual fallback-to-manual with the NL-required separate caregiver fault removal. The smallest safe edit preserves the CA_backManual recovery target Manual but removes the fault-clearing effect from that t...<truncated 503 chars> |
- repair_rationale：Hard request `fixreq-3-sl7-0-65d2e7f559` is resolved by separating CA_backManual fallback from caregiver fault removal: `PumpFault -> Manual : CA_backManual;` now changes the state to Manual without clearing `pump_fault` or `alarm_signal`.；The explicit fault-removal semantics remain grounded and available through `PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; };` and `Manual -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; };...<truncated 2 chars>；Manual remains fault-aware: if `pump_fault > 0`, Manual keeps `alarm_signal = 1` and suppresses `pump_speed` and `flow_rate`; after `FaultRemoved`, Manual restores `pump_speed = built_in_switch` and `flow_rate = default_flow_rate`.；The latest waived local objections about the stale `flow_rate=11` scenario, forced-transition count drift, and conservative grounding matcher are audit-only per SL-10; this repair does not change the accepted one-unit low-pressure flow form...<truncated 70 chars>；Required preserved elements remain represented: `[ * ] -> Manual` is preserved as `[ * ] -> Manual;`, `AutocontrolNormalToPumpFault` is preserved as `! AutocontrolNormal -> PumpFault : if [pump_fault > 0];`, and CA/CB/CP/CC backManual recov...<truncated 30 chars>
- diff_summary：`{"summary": "Removed the fault-clearing effect from the PumpFault CA_backManual transition, preserving the Manual recovery target while requiring explicit FaultRemoved to clear pump_fault and alarm_signal. All required states, variables, fallback events, FaultRemoved transitions, initial Manual entry, autocontrol fault transition, setpoint update, and pressure-to-flow behavior are preserved."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 80;
def int caregiver_target_bp = 80;
def int blood_pressure = 80;
def int shared_sensor_buffer = 0;
def int default_flow_rate = 10;
def int built_in_switch = 10;
def int control_voltage = 10;
def int pump_speed = 0;
def int flow_rate = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 1;
def int log_count = 0;
def int setpoint_changed = 0;

state CARA {
    ! * -> Manual : CB_backManual;
    ! * -> Manual : CP_backManual;
    ! * -> Manual : CC_backManual;
    ! AutocontrolNormal -> PumpFault : if [pump_fault > 0];

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault == 0] {
                alarm_signal = 0;
            } else {
                alarm_signal = 1;
                pump_speed = 0;
                flow_rate = 0;
            }
        }
        during {
            shared_sensor_buffer = blood_pressure;
            if [pump_fault == 0] {
                alarm_signal = 0;
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            } else {
                alarm_signal = 1;
                pump_speed = 0;
                flow_rate = 0;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
            control_released = 0;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            setpoint_changed = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 2;
            control_released = 0;
        }
        during {
            shared_sensor_buffer = blood_pressure;
            log_count = log_count + 1;
            pump_speed = control_voltage;
            if [pump_fault == 0] {
                if [blood_pressure > target_bp] {
                    flow_rate = default_flow_rate - 1;
                } else if [blood_pressure < target_bp] {
                    flow_rate = default_flow_rate + 1;
                } else {
                    flow_rate = default_flow_rate;
                }
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            control_released = 1;
            CA_mode = 0;
            pump_speed = 0;
            flow_rate = 0;
        }
    }

    Manual -> Ask_StartAC : InitiateAC;
    Manual -> Manual : CA_backManual;
    Manual -> Manual : FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
    Ask_StartAC -> AutocontrolInit : StartAC;
    Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect {
        target_bp = caregiver_target_bp;
        setpoint_changed = 1;
    };
    Ask_StartAC -> Manual : TerminateAC;
    Ask_StartAC -> Manual : CA_backManual;
    AutocontrolInit -> Manual : TerminateAC;
    AutocontrolInit -> Manual : CA_backManual;
    AutocontrolNormal -> Manual : TerminateAC;
    AutocontrolNormal -> Manual : CA_backManual;
    AutocontrolInit -> AutocontrolNormal;
    PumpFault -> Manual : CA_backManual;
    PumpFault -> Manual : FaultRemoved effect {
        pump_fault = 0;
        alarm_signal = 0;
    };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -89,6 +89,7 @@
             alarm_signal = 1;
             control_released = 1;
             CA_mode = 0;
+            pump_speed = 0;
             flow_rate = 0;
         }
     }
@@ -111,10 +112,7 @@
     AutocontrolNormal -> Manual : TerminateAC;
     AutocontrolNormal -> Manual : CA_backManual;
     AutocontrolInit -> AutocontrolNormal;
-    PumpFault -> Manual : CA_backManual effect {
-        pump_fault = 0;
-        alarm_signal = 0;
-    };
+    PumpFault -> Manual : CA_backManual;
     PumpFault -> Manual : FaultRemoved effect {
         pump_fault = 0;
         alarm_signal = 0;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:5ff634b5a4c848f8d17c0a1aeb24ba910e6ee3aa4631416e37a4cdd587a8ffca`。
  - SL-10 evidence 1: `{"summary": "The hard SL-7 request is directly resolved. The request identified `PumpFault -> Manual : CA_backManual effect { pump_fault = 0; alarm_signal = 0; }` as unsafe because it conflated fallback-to-Manual with the NL-required caregiver fault-removal step. The candidate changes that transition to `PumpFault -> Manual : CA_backManual;`, preserving Manual as the recovery target while leaving `pump_fault` and `alarm_signal` unchanged until `FaultRemoved` occurs."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves the explicit caregiver fault-removal paths required by the NL: `PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; }` and `Manual -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; }`. Manual remains fault-aware, so while `pump_fault > 0` it keeps `alarm_signal = 1` and suppresses `pump_speed` and `flow_rate`; after `FaultRemoved`, Manual restores sensor buffering, built-in-switch pump speed, and default flow rate."}`
  - SL-10 evidence 3: `{"summary": "The required grounded structure is preserved in the DSL: states Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault remain; variables including CA_mode, target_bp, blood_pressure, shared_sensor_buffer, built_in_switch, control_voltage, pump_speed, flow_rate, pump_fault, alarm_signal, control_released, and log_count remain; `[ * ] -> Manual`, `! AutocontrolNormal -> PumpFault : if [pump_fault > 0]`, InitiateAC, StartAC, ChangeSetpoint with `target_bp = caregiver_target_bp`, TerminateAC transitions, and backManual recovery paths remain represented."}`
  - SL-10 evidence 4: `{"summary": "The complete FixLog shows earlier SL-10 passes overrode conservative local expectations and then a later hard SL-7 review reopened the CA_backManual-from-PumpFault behavior as unsafe. The current SL-9 decision correctly follows the new hard request rather than the older local probe that expected CA_backManual to clear the fault. This is a legitimate NL-fidelity correction, not an ungrounded regression."}`
  - SL-10 evidence 5: `{"summary": "The only substantive DSL behavior change is the removal of the fault-clearing effect from `PumpFault -> Manual : CA_backManual`; the added `pump_speed = 0` in PumpFault.enter is consistent with pump-fault safe output suppression and does not drop any NL-required behavior."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:bf01076a8a36fd3168dd34e217b409eb1fba5c078b6c6c09b78f3eb607ff4dfd", "covered_local_objection_kinds": ["scenario_regression", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:b8153797761ea452aa751da3a708bfe79313964c3931097e41912ed5ac5938ca", "local_override_rationale_count": 6, "local_override_rationale_hash": "sha256:670a29357bfa61b1f155a36e9dff1beaf8becdac310d18247aa07f00512b7959", "local_rejection_evidence_hash": "sha256:b3d6a9ab1fb6ca0e5cdb343a4343d001230f1b931940dc0f6df80e7d61ca18c8", "local_rejection_reason": "scenario_regression; missing_required_grounding", "missing_local_objection_kinds": [],...<truncated 340 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 15, "n_scenarios_passed": 14, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init verifies initial dispatch to Manual and manual operation sets pump speed from built-in switch, default flow rate, sensor buffer, and safe manual flags.", "name": "default_init_enters_manual_and_sets_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Manual", "actual_vars": {...<truncated 23428 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:InitialToManual", "transition:AutocontrolNormalToPumpFault", "transition:CA_backManualFallback"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-eef005362b4` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-eef005362b4` | accept=8, reject=0 | `sl10_review` | `sha256:b33b133cba821c111f054a2fa54395c557d5c8d02a4ad00fe6eb009fbebe8fb1` | Primary gap across the failing repair_briefs is unresolved event paths such as CARA.InitiateAC, CARA.StartAC, CARA.ChangeSetpoint, and CARA.FaultRemoved. The existing transitions used local :: events, which are source-state namespace events; the scenarios inject CARA-scope events. The smallest safe repair is changing those four caregiver/fault-removal transitions to parent/CARA-scope event syntax with : Event., For initiate_change_setpoint_start_ac_to_normal_high_pressure, step initiate_ac_enters_ask_startac expected CARA.Ask_StartAC with CA_mode=1 and control_released=0 but stayed in CARA.Manual due to unresolved CARA.InitiateAC. Manual -> Ask_StartAC : InitiateAC now resolves at CARA scope and preserves Ask_StartAC.enter actions., For direct_initiate_ac_wrong_target_probe, the same InitiateAC repair targets Ask_StartAC, not another autocontrol state, preserving the NL-grounded caregiver initiation behavior., ... +5 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-eef005362b4` | accept=8, reject=0 | `sc11_accept_then_sd2` | `sha256:b33b133cba821c111f054a2fa54395c557d5c8d02a4ad00fe6eb009fbebe8fb1` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-afcf071a815` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-afcf071a815` | accept=2, reject=0 | `sl10_review` | `sha256:61cd61b0a826f875c372d019f28b015e190455700584113ffdbf76fe40ead0f8` | Accepted both current hard model-review requests and preserved the previous event-scope repair: InitiateAC, StartAC, ChangeSetpoint, FaultRemoved, and TerminateAC remain CARA-scope ':' events so the earlier scenario-regression fixes are not undone., For fixreq-1-sl7-0, the failing model-review gap was expected NL behavior that the caregiver can modify target blood pressure versus actual DSL behavior where target_bp stayed constant and ChangeSetpoint only set setpoint_changed. The repair adds caregiver_target_bp as an external caregiver input and writes target_bp = caregiver_target_bp in the ChangeSetpoint effect., For fixreq-1-sl7-1, the unsafe gap was expected safe fault handling versus actual forced fallback entering Manual with pump_fault still active, clearing alarm_signal and restoring pump outputs. The repair keeps the required backManual fallbacks and Manual recovery target, but Manual.enter and Manual.during now keep alarm_signal = 1 and pump_speed/flow_rate = 0 while pump_fault > 0., ... +2 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-afcf071a815` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:61cd61b0a826f875c372d019f28b015e190455700584113ffdbf76fe40ead0f8` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |
| 7 | `2` | `request_batch` | `fixbatch-2-sha256-be0bd2c6ce4` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 8 | `2` | `sl9_decision` | `fixbatch-2-sha256-be0bd2c6ce4` | accept=2, reject=1 | `sl10_review` | `sha256:4e2c7794b7f3d7d4f0a53ce595461cb93e3e68723ba5bcd88b135ca5fea2ca90` | For cc_back_manual_fallback_from_pumpfault, the failing step fault_removed_then_manual_outputs_restore expected state CARA.Manual with pump_fault=0, alarm_signal=0, shared_sensor_buffer=77, pump_speed=17, and flow_rate=6, but actual remained pump_fault=1, alarm_signal=1, pump_speed=0, and flow_rate=0 because FaultRemoved was only available from PumpFault. Adding Manual -> Manual : FaultRemoved clears the fault after a prior backManual fallback has already entered Manual; Manual enter/during then restores the expected manual outputs., For ca_backmanual_from_pumpfault_forced_line_probe, the failing step ca_backmanual_from_pumpfault_to_manual expected CARA.Manual with alarm_signal=0, pump_speed=18, and flow_rate=7, but actual had alarm_signal=1, pump_speed=0, and flow_rate=0 because pump_fault stayed asserted. Adding the source-specific PumpFault -> Manual : CA_backManual clearing transition gives the CA fallback a completed recovery path while preserving the required root-level ! * -> Manual : CA_backManual fallback line., The previous NL-grounded fault-aware Manual behavior is preserved for CC_backManual and other backManual fallbacks: if pump_fault remains active, Manual still keeps alarm_signal=1 and suppresses pump outputs until FaultRemoved clears the fault., ... +2 |
| 9 | `2` | `sl10_review` | `fixbatch-2-sha256-be0bd2c6ce4` | accept=2, reject=1 | `sl9_rework` | `sha256:4e2c7794b7f3d7d4f0a53ce595461cb93e3e68723ba5bcd88b135ca5fea2ca90` | Resolve W_FORCED_OVERRIDES_NORMAL by eliminating the duplicate coverage between global forced CA_backManual and the source-specific PumpFault -> Manual : CA_backManual transition. Do not keep both transitions covering CARA.PumpFault on the same CA_backManual event., Preserve the intended CA_backManual behavior deterministically by replacing the single global '! * -> Manual : CA_backManual;' with explicit CA_backManual fallback transitions for the concrete non-PumpFault states that need the shared recovery target, e.g. Manual, Ask_StartAC, AutocontrolInit, and AutocontrolNormal, while keeping a single PumpFault -> Manual : CA_backManual transition with the intended fault-clearing effect if that is the chosen repair for the CA-specific probe., Keep the CB_backManual, CP_backManual, and CC_backManual fallbacks represented and preserve the current safe behavior for CC_backManual from PumpFault: it may enter Manual with pump_fault still active, alarm_signal=1, pump_speed=0, and flow_rate=0 until FaultRemoved occurs., ... +20 |
| 10 | `2` | `sl9_rework_decision` | `fixbatch-2-sha256-be0bd2c6ce4` | accept=3, reject=0 | `sl10_review` | `sha256:43f02231d93a2b1156f868a3906cfc7090d7450d3ef582f9fc8851317947b246` | Addressed fixlog-8 rework by eliminating W_FORCED_OVERRIDES_NORMAL: the single global forced CA_backManual fallback was removed, so there is no longer duplicate forced and normal coverage for CARA.PumpFault -> CARA.Manual on CARA.CA_backManual., Preserved deterministic CA_backManual behavior with explicit non-PumpFault transitions: Manual -> Manual, Ask_StartAC -> Manual, AutocontrolInit -> Manual, and AutocontrolNormal -> Manual all keep Manual as the shared recovery target and still re-enter/enter Manual so manual outputs are restored when pump_fault is clear., For ca_backmanual_from_pumpfault_forced_line_probe, the failing actual values were alarm_signal=1, pump_speed=0, and flow_rate=0 because pump_fault stayed active. The PumpFault -> Manual : CA_backManual effect now clears pump_fault and alarm_signal before Manual runs, so Manual restores shared_sensor_buffer, pump_speed=built_in_switch, and flow_rate=default_flow_rate., ... +4 |
| 11 | `2` | `sl10_rework_review` | `fixbatch-2-sha256-be0bd2c6ce4` | accept=3, reject=0 | `sc11_accept_then_sd2` | `sha256:43f02231d93a2b1156f868a3906cfc7090d7450d3ef582f9fc8851317947b246` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |
| 12 | `3` | `request_batch` | `fixbatch-3-sha256-0ee61448bc6` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 13 | `3` | `sl9_decision` | `fixbatch-3-sha256-0ee61448bc6` | accept=1, reject=0 | `sl10_review` | `sha256:bf01076a8a36fd3168dd34e217b409eb1fba5c078b6c6c09b78f3eb607ff4dfd` | Hard request `fixreq-3-sl7-0-65d2e7f559` is resolved by separating CA_backManual fallback from caregiver fault removal: `PumpFault -> Manual : CA_backManual;` now changes the state to Manual without clearing `pump_fault` or `alarm_signal`., The explicit fault-removal semantics remain grounded and available through `PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; };` and `Manual -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; };`., Manual remains fault-aware: if `pump_fault > 0`, Manual keeps `alarm_signal = 1` and suppresses `pump_speed` and `flow_rate`; after `FaultRemoved`, Manual restores `pump_speed = built_in_switch` and `flow_rate = default_flow_rate`., ... +2 |
| 14 | `3` | `sl10_review` | `fixbatch-3-sha256-0ee61448bc6` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:bf01076a8a36fd3168dd34e217b409eb1fba5c078b6c6c09b78f3eb607ff4dfd` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3935, 'completion_chars': 15332, 'completion_tokens': 5830, 'elapsed_seconds': 108.29030194401275, 'estimated_completion_tokens': 3833, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 10490, 'first_chunk_seconds': 37.73927063800511, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12280}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3539, 'completion_chars': 14275, 'completion_tokens': 5639, 'elapsed_seconds': 103.51769054000033, 'estimated_completion_tokens': 3569, 'estimated_prompt_tokens': 13414, 'estimated_total_tokens': 16983, 'first_chunk_seconds': 39.72807799500879, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 53655, 'prompt_tokens': 13190, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 18829}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4229, 'completion_chars': 17025, 'completion_tokens': 4945, 'elapsed_seconds': 91.67551251698751, 'estimated_completion_tokens': 4257, 'estimated_prompt_tokens': 17218, 'estimated_total_tokens': 21475, 'first_chunk_seconds': 16.133478578994982, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 68870, 'prompt_tokens': 16928, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21873}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4980, 'completion_chars': 20036, 'completion_tokens': 5669, 'elapsed_seconds': 103.9187387410202, 'estimated_completion_tokens': 5009, 'estimated_prompt_tokens': 17905, 'estimated_total_tokens': 22914, 'first_chunk_seconds': 14.581287641020026, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 71620, 'prompt_tokens': 17618, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23287}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2290, 'completion_chars': 9227, 'completion_tokens': 2809, 'elapsed_seconds': 55.66558548799367, 'estimated_completion_tokens': 2307, 'estimated_prompt_tokens': 57520, 'estimated_total_tokens': 59827, 'first_chunk_seconds': 14.002354152995395, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 230078, 'prompt_tokens': 49346, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 52155}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 779, 'completion_chars': 3672, 'completion_tokens': 1220, 'elapsed_seconds': 26.062881736987038, 'estimated_completion_tokens': 918, 'estimated_prompt_tokens': 71911, 'estimated_total_tokens': 72829, 'first_chunk_seconds': 11.39561515499372, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 287643, 'prompt_tokens': 59772, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 60992}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3712, 'completion_chars': 14950, 'completion_tokens': 4734, 'elapsed_seconds': 86.99605163000524, 'estimated_completion_tokens': 3738, 'estimated_prompt_tokens': 19150, 'estimated_total_tokens': 22888, 'first_chunk_seconds': 20.119237089005765, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 76597, 'prompt_tokens': 19092, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23826}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2152, 'completion_chars': 9886, 'completion_tokens': 3071, 'elapsed_seconds': 59.372915443993406, 'estimated_completion_tokens': 2472, 'estimated_prompt_tokens': 19753, 'estimated_total_tokens': 22225, 'first_chunk_seconds': 19.499723315995652, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 79012, 'prompt_tokens': 19741, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22812}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1549, 'completion_chars': 6633, 'completion_tokens': 2521, 'elapsed_seconds': 48.32334122402244, 'estimated_completion_tokens': 1659, 'estimated_prompt_tokens': 96879, 'estimated_total_tokens': 98538, 'first_chunk_seconds': 20.538234038016526, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 387514, 'prompt_tokens': 81397, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 83918}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1183, 'completion_chars': 5399, 'completion_tokens': 1496, 'elapsed_seconds': 30.4148563699855, 'estimated_completion_tokens': 1350, 'estimated_prompt_tokens': 109521, 'estimated_total_tokens': 110871, 'first_chunk_seconds': 9.312161409005057, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 438083, 'prompt_tokens': 89918, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 91414}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3872, 'completion_chars': 15597, 'completion_tokens': 4391, 'elapsed_seconds': 90.22851891300525, 'estimated_completion_tokens': 3900, 'estimated_prompt_tokens': 22569, 'estimated_total_tokens': 26469, 'first_chunk_seconds': 11.718997805000981, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 90273, 'prompt_tokens': 22551, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26942}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2017, 'completion_chars': 8483, 'completion_tokens': 4260, 'elapsed_seconds': 80.586271734006, 'estimated_completion_tokens': 2121, 'estimated_prompt_tokens': 61969, 'estimated_total_tokens': 64090, 'first_chunk_seconds': 46.171783500001766, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 247873, 'prompt_tokens': 49273, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 53533}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 908, 'completion_chars': 4161, 'completion_tokens': 3451, 'elapsed_seconds': 64.89759723600582, 'estimated_completion_tokens': 1041, 'estimated_prompt_tokens': 59771, 'estimated_total_tokens': 60812, 'first_chunk_seconds': 48.95148220000556, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 239083, 'prompt_tokens': 47079, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 50530}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2211, 'completion_chars': 9297, 'completion_tokens': 3750, 'elapsed_seconds': 71.851776393014, 'estimated_completion_tokens': 2325, 'estimated_prompt_tokens': 144829, 'estimated_total_tokens': 147154, 'first_chunk_seconds': 31.864895622013137, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 579314, 'prompt_tokens': 109596, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 113346}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1367, 'completion_chars': 6452, 'completion_tokens': 1703, 'elapsed_seconds': 34.32076867701835, 'estimated_completion_tokens': 1613, 'estimated_prompt_tokens': 86552, 'estimated_total_tokens': 88165, 'first_chunk_seconds': 9.653515695012175, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 346205, 'prompt_tokens': 67854, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 69557}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2514, 'completion_chars': 9684, 'completion_tokens': 3361, 'elapsed_seconds': 64.06337673598318, 'estimated_completion_tokens': 2421, 'estimated_prompt_tokens': 24675, 'estimated_total_tokens': 27096, 'first_chunk_seconds': 19.122314968000865, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 98699, 'prompt_tokens': 24790, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 28151}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1742, 'completion_chars': 8031, 'completion_tokens': 2725, 'elapsed_seconds': 52.52167426698725, 'estimated_completion_tokens': 2008, 'estimated_prompt_tokens': 25481, 'estimated_total_tokens': 27489, 'first_chunk_seconds': 21.48486125099589, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 101921, 'prompt_tokens': 25650, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 28375}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1579, 'completion_chars': 6233, 'completion_tokens': 1985, 'elapsed_seconds': 41.50014643598115, 'estimated_completion_tokens': 1559, 'estimated_prompt_tokens': 257702, 'estimated_total_tokens': 259261, 'first_chunk_seconds': 12.970453073008684, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 1030808, 'prompt_tokens': 183426, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 185411}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1229, 'completion_chars': 5640, 'completion_tokens': 1671, 'elapsed_seconds': 35.807675235992065, 'estimated_completion_tokens': 1410, 'estimated_prompt_tokens': 106591, 'estimated_total_tokens': 108001, 'first_chunk_seconds': 13.54326291300822, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 426362, 'prompt_tokens': 77279, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 78950}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2711, 'completion_chars': 10445, 'completion_tokens': 3619, 'elapsed_seconds': 69.1670355600072, 'estimated_completion_tokens': 2612, 'estimated_prompt_tokens': 26652, 'estimated_total_tokens': 29264, 'first_chunk_seconds': 20.672161804017378, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 106607, 'prompt_tokens': 26787, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 30406}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1647, 'completion_chars': 7917, 'completion_tokens': 2153, 'elapsed_seconds': 41.77465729700634, 'estimated_completion_tokens': 1980, 'estimated_prompt_tokens': 27456, 'estimated_total_tokens': 29436, 'first_chunk_seconds': 12.620760179008357, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 109821, 'prompt_tokens': 27636, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 29789}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`68/16`，missing=`<none>`。
- repairs：`4/5` accepted；scenario_history=`11`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
