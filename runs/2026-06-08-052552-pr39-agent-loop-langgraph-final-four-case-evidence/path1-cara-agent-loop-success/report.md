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
| Git commit | `20f104e865c000bc039d379a4700df48a5d1adf9` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:f705ac69b45689b590ac83622b5e87c8e46943c1aaeb6c6b4d4c7294afb0558b", "iteration": 1, "matching_repair_history_indices": [1], "repair_history_index": 1, "selected_source_stage": "SL-7", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 240064, 'completion_tokens': 29709, 'total_tokens': 269773, 'estimated_prompt_tokens': 255105, 'estimated_completion_tokens': 23556, 'estimated_total_tokens': 278661, 'prompt_chars': 1020404, 'completion_chars': 94213, 'n_calls': 10, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`593.523s` |
| run record | [`pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:c0a5bc7f03814a273bd09483e877729634899eaded22e0068de8da394a1a25d0` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `59` |
| `langgraph_node_trace_hash` | `sha256:f4e1db64d62c813fae1a464fcd3d5f7feda381ec4c904765066c6ccfd6305c35` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `59` |

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
def int patient_bp = 120;
def int shared_buffer_bp = 120;
def int target_bp = 120;
def int requested_target_bp = 120;
def int flow_rate = 0;
def int default_flow_rate = 1;
def int built_in_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int display_error = 0;
def int sound_error = 0;
def int control_released = 1;
def int log_count = 0;

state CARA_Mode_Control_Algorithm {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    >> during before { shared_buffer_bp = patient_bp; }

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault > 0] {
                alarm_signal = 1;
                display_error = 1;
                sound_error = 1;
            } else {
                alarm_signal = 0;
                display_error = 0;
                sound_error = 0;
            }
        }
        during {
            if [pump_fault == 0] {
                pump_speed = built_in_switch_speed;
                flow_rate = default_flow_rate;
            } else {
                alarm_signal = 1;
                display_error = 1;
                sound_error = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }
    }

    state Ask_StartAC;

    state AutocontrolInit {
        enter {
            CA_mode = 1;
            control_released = 0;
            alarm_signal = 0;
            display_error = 0;
            sound_error = 0;
        }
    }

    state AutocontrolNormal {
        during {
            if [pump_fault == 0] {
                if [patient_bp > target_bp] {
                    flow_rate = 1;
                } else if [patient_bp == target_bp] {
                    flow_rate = 3;
                } else {
                    flow_rate = 5;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_count = log_count + 1;
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            display_error = 1;
            sound_error = 1;
            control_released = 1;
            CA_mode = 0;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    AutocontrolInit -> PumpFault : if [pump_fault > 0];
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    AutocontrolNormal -> Manual :: TerminateAC;
    Ask_StartAC -> Manual :: TerminateAC;
    PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12623 | 生成初始 DSL 与 grounding seeds | initial len=2490 | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=1; blocking=0, advisory=23, info=1; blocking=0, advisory=23, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=66958 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=72166 | LLM per-request accept/reject + repair | candidate len=2490,2920 | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=67194 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=1; blocking=0, advisory=23, info=1; blocking=0, advisory=23, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=66958 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=50832 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=72166 | LLM per-request accept/reject + repair | candidate len=2490,2920 | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=67194 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=1; blocking=0, advisory=23, info=1; blocking=0, advisory=23, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=66958 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=50832 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg_m1_g_signature_gate_20f104e8-caefa210.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-07T21:25:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-07T21:25:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-07T21:25:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-07T21:25:53Z` | `SL-1` | `-` | `lg_d2_envelope_enter` | {} | <none> |
| 5 | `2026-06-07T21:25:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 6 | `2026-06-07T21:27:52Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 7 | `2026-06-07T21:27:52Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2490,hash=sha256:4cfdceaa2ee8 |
| 8 | `2026-06-07T21:27:52Z` | `SL-1` | `-` | `lg_d2_envelope_exit` | {} | <none> |
| 9 | `2026-06-07T21:27:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 10 | `2026-06-07T21:27:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-07T21:27:52Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:4cfdceaa2ee83167bc51907548c39f086230e7dcdf3be195528645bb7e6b56e0 |
| 12 | `2026-06-07T21:27:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-07T21:27:52Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2490,hash=sha256:4cfdceaa2ee8, current_hash=sha256:4cfdceaa2ee83167bc51907548c39f086230e7dcdf3be195528645bb7e6b56e0 |
| 14 | `2026-06-07T21:27:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 15 | `2026-06-07T21:27:52Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 16 | `2026-06-07T21:27:52Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-07T21:27:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 18 | `2026-06-07T21:27:52Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 19 | `2026-06-07T21:27:53Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-07T21:27:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 21 | `2026-06-07T21:27:53Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 22 | `2026-06-07T21:27:53Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-07T21:27:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-07T21:27:53Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 25 | `2026-06-07T21:27:53Z` | `SL-5` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 26 | `2026-06-07T21:29:06Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 27 | `2026-06-07T21:29:06Z` | `SL-5` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 28 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-07T21:29:06Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 30 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-07T21:29:06Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 32 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 33 | `2026-06-07T21:29:06Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 34 | `2026-06-07T21:29:06Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 35 | `2026-06-07T21:29:06Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 36 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-07T21:29:06Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 10, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 38 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-07T21:29:06Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 10, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2490,hash=sha256:4cfdceaa2ee8 |
| 42 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-07T21:29:06Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 44 | `2026-06-07T21:29:06Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 2} | <none> |
| 45 | `2026-06-07T21:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-07T21:29:06Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2490,hash=sha256:4cfdceaa2ee8 |
| 47 | `2026-06-07T21:29:06Z` | `SL-9` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 48 | `2026-06-07T21:29:41Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 49 | `2026-06-07T21:29:41Z` | `SL-9` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 50 | `2026-06-07T21:29:41Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-92f946153f", "fixreq-0-sd6-1-2244c80013"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2490,hash=sha256:6448459b7345 |
| 51 | `2026-06-07T21:29:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 52 | `2026-06-07T21:29:41Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 53 | `2026-06-07T21:29:41Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:6448459b73453475d51ae3f572df1ea7482c6730750fa2b744a9cc498d5f0f4f |
| 54 | `2026-06-07T21:29:41Z` | `SL-10` | `0` | `lg_d2_envelope_enter` | {} | <none> |
| 55 | `2026-06-07T21:30:01Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 56 | `2026-06-07T21:30:01Z` | `SL-10` | `0` | `lg_d2_envelope_exit` | {} | <none> |
| 57 | `2026-06-07T21:30:01Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 58 | `2026-06-07T21:30:01Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 59 | `2026-06-07T21:30:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 60 | `2026-06-07T21:30:01Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2490,hash=sha256:6448459b7345 |
| 61 | `2026-06-07T21:30:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 62 | `2026-06-07T21:30:01Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:6448459b73453475d51ae3f572df1ea7482c6730750fa2b744a9cc498d5f0f4f |
| 63 | `2026-06-07T21:30:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 64 | `2026-06-07T21:30:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 65 | `2026-06-07T21:30:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 66 | `2026-06-07T21:30:01Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:6448459b73453475d51ae3f572df1ea7482c6730750fa2b744a9cc498d5f0f4f |
| 67 | `2026-06-07T21:30:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 68 | `2026-06-07T21:30:01Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=2490,hash=sha256:6448459b7345, current_hash=sha256:6448459b73453475d51ae3f572df1ea7482c6730750fa2b744a9cc498d5f0f4f |
| 69 | `2026-06-07T21:30:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 70 | `2026-06-07T21:30:01Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 71 | `2026-06-07T21:30:01Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 72 | `2026-06-07T21:30:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 73 | `2026-06-07T21:30:01Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 74 | `2026-06-07T21:30:01Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 75 | `2026-06-07T21:30:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 76 | `2026-06-07T21:30:01Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 77 | `2026-06-07T21:30:01Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-5A", "ok": true, "status": "StageStatus.OK"} | <none> |
| 78 | `2026-06-07T21:30:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 79 | `2026-06-07T21:30:01Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 targeted_retry", "ok": false, "reason": "reuse_frozen_scenario_set"} | <none> |
| 80 | `2026-06-07T21:30:01Z` | `<control>` | `1` | `frozen_scenario_refresh_targeted_retry` | {} | <none> |
- ……另有 `98` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-6` | yes | fixbatch-0-sha256-b756e942c71 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SL-7` | yes | fixbatch-1-sha256-e5b28575443 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| `default_init_manual_outputs` | default-init: first cycle dispatches to Manual and manual operation sets pump speed from the built-in switch and flow fr...<truncated 25 chars> | ✅ | ✅ | ✅ |
| `initiate_change_setpoint_and_start_ac` | default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters Autocontrol...<truncated 5 chars> | ✅ | ✅ | ✅ |
| `autocontrol_init_advances_to_normal_high_bp` | explicit-hot-start: AutocontrolInit without a pump fault advances to normal autocontrol, where high blood pressure produ...<truncated 24 chars> | ✅ | ✅ | ✅ |
| `normal_autocontrol_equal_and_low_bp_flow` | explicit-hot-start: normal autocontrol computes medium flow at target pressure and, in a separate low-pressure hot-start...<truncated 31 chars> | ✅ | ✅ | ✅ |
| `normal_autocontrol_low_bp_high_flow` | explicit-hot-start: normal autocontrol with blood pressure below target produces a higher flow rate than at or above tar...<truncated 4 chars> | ⚪ | ✅ | ✅ |
| `pump_fault_boundary_and_recovery` | explicit-hot-start: pump_fault=0 is the no-fire boundary in normal autocontrol; pump_fault>0 enters PumpFault, and Fault...<truncated 26 chars> | ⚪ | ⚪ | ✅ |
| `autocontrol_fault_paths_release_control` | explicit-hot-start: faults from AutocontrolNormal and AutocontrolInit enter PumpFault with alarm/display/sound active an...<truncated 28 chars> | ⚪ | ⚪ | ✅ |
| `autocontrol_init_fault_priority` | explicit-hot-start: if a pump fault is already present in AutocontrolInit, the fault path should win over normal-autocon...<truncated 17 chars> | ❌ | ✅ | ✅ |
| `terminate_ac_from_control_states` | explicit-hot-start: caregiver TerminateAC from Ask_StartAC returns to Manual as the recovery mode. | ✅ | ✅ | ✅ |
| `terminate_ac_from_init_and_normal` | explicit-hot-start: local TerminateAC from AutocontrolInit releases control and returns to Manual. | ❌ | ✅ | ✅ |
| `terminate_ac_from_normal` | explicit-hot-start: local TerminateAC from AutocontrolNormal releases control and returns to Manual without requiring a ...<truncated 11 chars> | ⚪ | ✅ | ✅ |
| `forced_backmanual_events_from_distinct_states` | explicit-hot-start: cross-component CA/CB/CP/CC backManual events force recovery to Manual with CA_mode Manual and relea...<truncated 12 chars> | ✅ | ✅ | ✅ |
| `forced_backmanual_during_unresolved_fault_preserves_alarm` | explicit-hot-start: a cross-component backManual fallback during an unresolved pump fault reaches Manual but should not ...<truncated 55 chars> | ⚪ | ⚪ | ✅ |
| `autocontrol_normal_pump_fault_boundary` |  | ✅ | ✅ | ✅ |
| `autocontrol_normal_fault_enters_pumpfault` |  | ✅ | ✅ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_outputs` — default-init: first cycle dispatches to Manual and manual operation sets pump speed from the built-in switch and flow from the default flow rate.</summary>

| Field | Value |
|---|---|
| description | default-init: first cycle dispatches to Manual and manual operation sets pump speed from the built-in switch and flow from the default flow rate. |
| initial_state | `<default-init>` |
| initial_vars | `{"built_in_switch_speed": 7, "default_flow_rate": 2, "patient_bp": 118, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_after_initial_dispatch` | `0` | `[]` | `CARA_Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "display_error": 0, "flow_rate": 2, "pump_speed": 7, "shared_buffer_bp": 118, "sound_error": 0}` |

</details>

<details><summary>`initiate_change_setpoint_and_start_ac` — default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit.</summary>

| Field | Value |
|---|---|
| description | default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit. |
| initial_state | `<default-init>` |
| initial_vars | `{"pump_fault": 0, "requested_target_bp": 110, "target_bp": 120}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_ready` | `0` | `[]` | `CARA_Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1}` |
| 1 `initiate_enters_ask_startac` | `0` | `["CARA_Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA_Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 2 `change_setpoint_stays_in_ask` | `0` | `["CARA_Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA_Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 110}` |
| 3 `startac_enters_autocontrol_init` | `0` | `["CARA_Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA_Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "control_released": 0, "display_error": 0, "sound_error": 0}` |

</details>

<details><summary>`autocontrol_init_advances_to_normal_high_bp` — explicit-hot-start: AutocontrolInit without a pump fault advances to normal autocontrol, where high blood pressure produces the lower flow rate.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: AutocontrolInit without a pump fault advances to normal autocontrol, where high blood pressure produces the lower flow rate. |
| initial_state | `CARA_Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"log_count": 0, "patient_bp": 130, "pump_fault": 0, "target_bp": 120}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `normal_autocontrol_high_bp_low_flow` | `0` | `[]` | `CARA_Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 1, "flow_rate": 1, "log_count": 1, "pump_speed": 1, "shared_buffer_bp": 130}` |

</details>

<details><summary>`normal_autocontrol_equal_and_low_bp_flow` — explicit-hot-start: normal autocontrol computes medium flow at target pressure and, in a separate low-pressure hot-start, should compute a higher flow.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: normal autocontrol computes medium flow at target pressure and, in a separate low-pressure hot-start, should compute a higher flow. |
| initial_state | `CARA_Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"log_count": 4, "patient_bp": 120, "pump_fault": 0, "target_bp": 120}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `equal_bp_medium_flow` | `0` | `[]` | `CARA_Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 3, "flow_rate": 3, "log_count": 5, "pump_speed": 3, "shared_buffer_bp": 120}` |
| 1 `equal_bp_continues_logging` | `0` | `[]` | `CARA_Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 3, "flow_rate": 3, "log_count": 6, "pump_speed": 3, "shared_buffer_bp": 120}` |

</details>

<details><summary>`normal_autocontrol_low_bp_high_flow` — explicit-hot-start: normal autocontrol with blood pressure below target produces a higher flow rate than at or above target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: normal autocontrol with blood pressure below target produces a higher flow rate than at or above target. |
| initial_state | `CARA_Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"log_count": 2, "patient_bp": 110, "pump_fault": 0, "target_bp": 120}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `low_bp_high_flow` | `0` | `[]` | `CARA_Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 5, "flow_rate": 5, "log_count": 3, "pump_speed": 5, "shared_buffer_bp": 110}` |

</details>

<details><summary>`pump_fault_boundary_and_recovery` — explicit-hot-start: pump_fault=0 is the no-fire boundary in normal autocontrol; pump_fault>0 enters PumpFault, and FaultRemoved returns to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: pump_fault=0 is the no-fire boundary in normal autocontrol; pump_fault>0 enters PumpFault, and FaultRemoved returns to Manual. |
| initial_state | `CARA_Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "control_released": 0, "display_error": 0, "log_count": 0, "patient_bp": 125, "pump_fault": 0, "sound_error": 0, "target_bp": 120}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_fault_stays_normal` | `0` | `[]` | `CARA_Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 1, "flow_rate": 1, "log_count": 1, "pump_speed": 1, "shared_buffer_bp": 125}` |

</details>

<details><summary>`autocontrol_fault_paths_release_control` — explicit-hot-start: faults from AutocontrolNormal and AutocontrolInit enter PumpFault with alarm/display/sound active and software control released.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: faults from AutocontrolNormal and AutocontrolInit enter PumpFault with alarm/display/sound active and software control released. |
| initial_state | `CARA_Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "control_released": 0, "display_error": 0, "pump_fault": 1, "sound_error": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `normal_fault_alarm_and_release` | `0` | `[]` | `CARA_Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1, "display_error": 1, "sound_error": 1}` |
| 1 `fault_removed_returns_manual` | `0` | `["CARA_Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA_Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "display_error": 0, "pump_fault": 0, "sound_error": 0}` |

</details>

<details><summary>`autocontrol_init_fault_priority` — explicit-hot-start: if a pump fault is already present in AutocontrolInit, the fault path should win over normal-autocontrol progression.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: if a pump fault is already present in AutocontrolInit, the fault path should win over normal-autocontrol progression. |
| initial_state | `CARA_Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "control_released": 0, "display_error": 0, "pump_fault": 1, "sound_error": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `init_fault_enters_pumpfault` | `0` | `[]` | `CARA_Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1, "display_error": 1, "sound_error": 1}` |

</details>

<details><summary>`terminate_ac_from_control_states` — explicit-hot-start: caregiver TerminateAC from Ask_StartAC returns to Manual as the recovery mode.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: caregiver TerminateAC from Ask_StartAC returns to Manual as the recovery mode. |
| initial_state | `CARA_Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "built_in_switch_speed": 4, "control_released": 0, "default_flow_rate": 2, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_from_ask_returns_manual` | `0` | `["CARA_Mode_Control_Algorithm.Ask_StartAC.TerminateAC"]` | `CARA_Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "flow_rate": 2, "pump_speed": 4}` |

</details>

<details><summary>`terminate_ac_from_init_and_normal` — explicit-hot-start: local TerminateAC from AutocontrolInit releases control and returns to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: local TerminateAC from AutocontrolInit releases control and returns to Manual. |
| initial_state | `CARA_Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "built_in_switch_speed": 6, "control_released": 0, "default_flow_rate": 3, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_from_init_returns_manual` | `0` | `["CARA_Mode_Control_Algorithm.AutocontrolInit.TerminateAC"]` | `CARA_Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "flow_rate": 3, "pump_speed": 6}` |

</details>

<details><summary>`terminate_ac_from_normal` — explicit-hot-start: local TerminateAC from AutocontrolNormal releases control and returns to Manual without requiring a pump fault.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: local TerminateAC from AutocontrolNormal releases control and returns to Manual without requiring a pump fault. |
| initial_state | `CARA_Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "built_in_switch_speed": 8, "control_released": 0, "default_flow_rate": 4, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_from_normal_returns_manual` | `0` | `["CARA_Mode_Control_Algorithm.AutocontrolNormal.TerminateAC"]` | `CARA_Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "flow_rate": 4, "pump_speed": 8}` |

</details>

<details><summary>`forced_backmanual_events_from_distinct_states` — explicit-hot-start: cross-component CA/CB/CP/CC backManual events force recovery to Manual with CA_mode Manual and released control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: cross-component CA/CB/CP/CC backManual events force recovery to Manual with CA_mode Manual and released control. |
| initial_state | `CARA_Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "built_in_switch_speed": 5, "control_released": 0, "default_flow_rate": 2, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_from_normal` | `0` | `["CARA_Mode_Control_Algorithm.CA_backManual"]` | `CARA_Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "flow_rate": 2, "pump_speed": 5}` |
| 1 `cb_backmanual_from_manual_idempotent` | `0` | `["CARA_Mode_Control_Algorithm.CB_backManual"]` | `CARA_Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1}` |
| 2 `cp_backmanual_from_manual_idempotent` | `0` | `["CARA_Mode_Control_Algorithm.CP_backManual"]` | `CARA_Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1}` |
| 3 `cc_backmanual_from_manual_idempotent` | `0` | `["CARA_Mode_Control_Algorithm.CC_backManual"]` | `CARA_Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1}` |

</details>

<details><summary>`forced_backmanual_during_unresolved_fault_preserves_alarm` — explicit-hot-start: a cross-component backManual fallback during an unresolved pump fault reaches Manual but should not silence alarm/display/sound until the fa...<truncated 15 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: a cross-component backManual fallback during an unresolved pump fault reaches Manual but should not silence alarm/display/sound until the fault is removed. |
| initial_state | `CARA_Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "built_in_switch_speed": 5, "control_released": 0, "default_flow_rate": 2, "display_error": 0, "pump_fault": 1, "sound_error": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_with_fault_manual_alarm_active` | `0` | `["CARA_Mode_Control_Algorithm.CA_backManual"]` | `CARA_Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1, "display_error": 1, "sound_error": 1}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | autocontrol_init_fault_priority, terminate_ac_from_init_and_normal | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:6448459b73453475d51ae3f572df1ea7482c6730750fa2b744a9cc498d5f0f4f` |
| 2 | `1` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:f705ac69b45689b590ac83622b5e87c8e46943c1aaeb6c6b4d4c7294afb0558b` |

<details><summary>Repair 1 / iteration `0` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`autocontrol_init_fault_priority, terminate_ac_from_init_and_normal`。
- before_dsl_hash：`sha256:4cfdceaa2ee83167bc51907548c39f086230e7dcdf3be195528645bb7e6b56e0`；candidate_dsl_hash：`sha256:6448459b73453475d51ae3f572df1ea7482c6730750fa2b744a9cc498d5f0f4f`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-b756e942c71`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-92f946153f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: if a pump fault is already present in AutocontrolInit, the fault path should win over the normal-autocontrol progression.', 'name': 'autocontrol_init_fault_priority', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: if a pump fault is already present in AutocontrolInit, the fault path should win over the normal-autocontrol progression.', 'failing_steps': [{'actual_state': 'CARA_Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'display_error': 0, 'sound_error': 0}, 'before_cycles': 0, 'events': [], 'expected_state': 'CARA_Mode_Control_Algorithm.PumpFault', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 1, 'control_released': 1, 'display_error': 1, 'sound_error': 1}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'init_fault_enters_pumpfault', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'alarm_signal': {'actual': 0, 'expected': 1}, 'control_released': {'actual': 0, 'expected': 1}, 'display_error': {'actual': 0, 'expected': 1}, 'sound_error': {'actual': 0, 'expected': 1}}}], 'initial_state': 'CARA_Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'display_error': 0, 'pump_fault': 1, 'sound_error': 0}, 'scenario_name': 'autocontrol_init_fault_priority', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA_Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'built_in_switch_speed': 0, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 1, 'display_error': 0, 'flow_rate': 0, 'log_count': 0, 'patient_bp': 120, 'pump_fault': 1, 'pump_speed': 0, 'requested_target_bp': 120, 'shared_buffer_bp': 120, 'sound_error': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'init_fault_enters_pumpfault', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'alarm_signal': {'actual': 0, 'expected': 1}, 'control_released': {'actual': 0, 'expected': 1}, 'display_error': {'actual': 0, 'expected': 1}, 'sound_error': {'actual': 0, 'expected': 1}}}]}` |
| `fixreq-0-sd6-1-2244c80013` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: local TerminateAC from AutocontrolInit and AutocontrolNormal releases control and returns to Manual.', 'name': 'terminate_ac_from_init_and_normal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: local TerminateAC from AutocontrolInit and AutocontrolNormal releases control and returns to Manual.', 'failing_steps': [{'actual_state': 'CARA_Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'flow_rate': 3, 'pump_speed': 3}, 'before_cycles': 0, 'events': ['CARA_Mode_Control_Algorithm.AutocontrolInit.TerminateAC'], 'expected_state': 'CARA_Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'flow_rate': 3, 'pump_speed': 6}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'terminate_from_init_returns_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'control_released': {'actual': 0, 'expected': 1}, 'pump_speed': {'actual': 3, 'expected': 6}}}], 'initial_state': 'CARA_Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'built_in_switch_speed': 6, 'control_released': 0, 'default_flow_rate': 3}, 'scenario_name': 'terminate_ac_from_init_and_normal', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA_Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'built_in_switch_speed': 6, 'control_released': 0, 'control_voltage': 3, 'default_flow_rate': 3, 'display_error': 0, 'flow_rate': 3, 'log_count': 1, 'patient_bp': 120, 'pump_fault': 0, 'pump_speed': 3, 'requested_target_bp': 120, 'shared_buffer_bp': 120, 'sound_error': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'terminate_from_init_returns_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'control_released': {'actual': 0, 'expected': 1}, 'pump_speed': {'actual': 3, 'expected': 6}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, transition:initial:Manual, transition:Manual_to_Ask_StartAC, transition:Ask_StartAC_setpoint, transition:Ask_StartAC_to_AutocontrolInit, transition:AutocontrolInit_to_AutocontrolNormal, transition:AutocontrolNormal_to_PumpFault, transition:AutocontrolInit_to_PumpFault, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2490`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-92f946153f` | `accept` | ❌ | ❌ | The autocontrol_init_fault_priority scenario starts hot in AutocontrolInit with pump_fault = 1 and expects PumpFault with alarm_signal/display_error/sound_error/control_released set and CA_mode returned to Manual. The current unconditional AutocontrolInit -> AutocontrolNormal transition is listed before the pump-fault guard, so it wins first. Reordering the ...<truncated 288 chars> |
| `fixreq-0-sd6-1-2244c80013` | `accept` | ❌ | ❌ | The terminate_ac_from_init_and_normal scenario starts hot in AutocontrolInit and injects the local AutocontrolInit.TerminateAC event, expecting Manual with control released and manual pump-speed behavior. The current unconditional AutocontrolInit -> AutocontrolNormal transition precedes the TerminateAC transition, so the event is ignored. Reordering the Auto...<truncated 319 chars> |
- repair_rationale：For autocontrol_init_fault_priority, expected_state was CARA_Mode_Control_Algorithm.PumpFault with alarm_signal/display_error/sound_error/control_released = 1 and CA_mode = 0, but actual_state was AutocontrolNormal with those variables stil...<truncated 217 chars>；For terminate_ac_from_init_and_normal, expected_state was CARA_Mode_Control_Algorithm.Manual after the local AutocontrolInit.TerminateAC event, with CA_mode = 0, control_released = 1, pump_speed = built_in_switch_speed, and flow_rate = defa...<truncated 229 chars>；This is a minimal transition-priority edit only. It preserves all grounded states, variables, events, forced backManual transitions, Ask_StartAC behavior, normal autocontrol behavior, PumpFault behavior, shared-buffer update, and the requir...<truncated 100 chars>
- diff_summary：`{"summary": "Reordered AutocontrolInit outgoing transitions so pump_fault and TerminateAC are evaluated before the unconditional AutocontrolInit -> AutocontrolNormal progression; no states, variables, actions, or grounded transitions were deleted."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int patient_bp = 120;
def int shared_buffer_bp = 120;
def int target_bp = 120;
def int requested_target_bp = 120;
def int flow_rate = 0;
def int default_flow_rate = 1;
def int built_in_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int display_error = 0;
def int sound_error = 0;
def int control_released = 1;
def int log_count = 0;

state CARA_Mode_Control_Algorithm {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    >> during before { shared_buffer_bp = patient_bp; }

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            alarm_signal = 0;
            display_error = 0;
            sound_error = 0;
        }
        during {
            pump_speed = built_in_switch_speed;
            flow_rate = default_flow_rate;
        }
    }

    state Ask_StartAC;

    state AutocontrolInit {
        enter {
            CA_mode = 1;
            control_released = 0;
            alarm_signal = 0;
            display_error = 0;
            sound_error = 0;
        }
    }

    state AutocontrolNormal {
        during {
            if [pump_fault == 0] {
                if [patient_bp > target_bp] {
                    flow_rate = 1;
                } else if [patient_bp == target_bp] {
                    flow_rate = 3;
                } else {
                    flow_rate = 5;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_count = log_count + 1;
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            display_error = 1;
            sound_error = 1;
            control_released = 1;
            CA_mode = 0;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    AutocontrolInit -> PumpFault : if [pump_fault > 0];
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    AutocontrolNormal -> Manual :: TerminateAC;
    Ask_StartAC -> Manual :: TerminateAC;
    PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -81,10 +81,10 @@
     Manual -> Ask_StartAC :: InitiateAC;
     Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
     Ask_StartAC -> AutocontrolInit :: StartAC;
+    AutocontrolInit -> PumpFault : if [pump_fault > 0];
+    AutocontrolInit -> Manual :: TerminateAC;
     AutocontrolInit -> AutocontrolNormal;
-    AutocontrolInit -> PumpFault : if [pump_fault > 0];
     AutocontrolNormal -> PumpFault : if [pump_fault > 0];
-    AutocontrolInit -> Manual :: TerminateAC;
     AutocontrolNormal -> Manual :: TerminateAC;
     Ask_StartAC -> Manual :: TerminateAC;
     PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:90d000104a169f6aa32074c1db6ede7d44154124fc9c68500fc4120dfd79ee35`。
  - SL-10 evidence 1: `{"summary": "Both hard SD-6 simulation requests were accepted by SL-9 with a minimal transition-priority repair. In the old DSL, the unconditional `AutocontrolInit -> AutocontrolNormal` transition preceded both the `pump_fault > 0` transition and the `TerminateAC` transition, so hot-start scenarios in AutocontrolInit incorrectly advanced to AutocontrolNormal before fault or terminate handling. The candidate reorders only the three AutocontrolInit outgoing transitions so `AutocontrolInit -> PumpFault : if [pump_fault > 0]` and `AutocontrolInit -> Manual :: TerminateAC` are evaluated before the unconditional normal progression."}`
  - SL-10 evidence 2: `{"summary": "For `autocontrol_init_fault_priority`, the candidate now makes an already-present pump fault win from AutocontrolInit and enter PumpFault. PumpFault.enter sets `alarm_signal = 1`, `display_error = 1`, `sound_error = 1`, `control_released = 1`, and `CA_mode = 0`, matching the failing scenario's expected state and variables and the NL requirement that pump faults activate alarms and release software control when CARA was controlling the pump."}`
  - SL-10 evidence 3: `{"summary": "For `terminate_ac_from_init_and_normal`, the candidate now allows local `AutocontrolInit.TerminateAC` to return directly to Manual before unconditional progression. Manual.enter sets `CA_mode = 0` and `control_released = 1`, and Manual.during sets `pump_speed = built_in_switch_speed` and `flow_rate = default_flow_rate`, matching the scenario expectation and the NL requirement that the caregiver can terminate algorithmic pump control and return to manual operation."}`
  - SL-10 evidence 4: `{"summary": "The DSL diff is limited to reordering existing AutocontrolInit transitions. No required NL-grounded states, variables, events, actions, or transitions were deleted: Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, initial Manual, InitiateAC, ChangeSetpoint, StartAC, fault transitions, TerminateAC transitions, FaultRemoved, all backManual forced transitions, shared buffer update, manual during behavior, normal autocontrol flow computation/logging, and PumpFault alarm/release behavior remain represented."}`
  - SL-10 evidence 5: `{"candidate_dsl_hash": "sha256:6448459b73453475d51ae3f572df1ea7482c6730750fa2b744a9cc498d5f0f4f", "covered_local_objection_kinds": ["missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:065eb2766b18c8d54ec50d2b6e5128861486dde34aed271edb31614318aff3bd", "local_override_rationale_count": 2, "local_override_rationale_hash": "sha256:090680834e61300cb98a9b7ba8ddd1832fff2d3c144939ce2230bed0b2f3ff64", "local_rejection_evidence_hash": "sha256:dec143b31bea133be00c5192ec467b466b3badcccf1d4f82b76615e73d5a5e48", "local_rejection_reason": "missing_required_grounding", "missing_local_objection_kinds": [], "policy": "SL-10 may override conservative ...<truncated 296 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial:Manual"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `1` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:6448459b73453475d51ae3f572df1ea7482c6730750fa2b744a9cc498d5f0f4f`；candidate_dsl_hash：`sha256:f705ac69b45689b590ac83622b5e87c8e46943c1aaeb6c6b4d4c7294afb0558b`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Global backManual recovery can bypass the PumpFault fault-removal path and enter Manual while pump_fault remains active, clearing alarms and allowing manual pump outputs before the caregiver removes the fault.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-e5b28575443`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sl7-0-3096823055` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL has forced transitions from any state to Manual: `! * -> Manual :: CA_backManual;`, `CB_backManual`, `CP_backManual`, `CC_backManual`.', 'DSL PumpFault preserves active fault until `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; }`.', 'DSL Manual.enter clears `alarm_signal`, `display_error`, and `sound_error` to 0, and Manual.during sets `pump_speed = built_in_switch_speed` and `flow_rate = default_flow_rate`.', 'NL says: `If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control.`', 'The model therefore admits a path PumpFault --CA/CB/CP/CC_backManual--> Manual with `pump_fault` still > 0 but alarms cleared.'], 'severity': 'major', 'summary': 'Global backManual recovery can bypass the PumpFault fault-removal path and enter Manual while pump_fault remains active, clearing alarms and allowing manual pump outputs before the caregiver removes the fault.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, transition:initial:Manual, transition:Manual_to_Ask_StartAC, transition:Ask_StartAC_setpoint, transition:Ask_StartAC_to_AutocontrolInit, transition:AutocontrolInit_to_AutocontrolNormal, transition:AutocontrolNormal_to_PumpFault, transition:AutocontrolInit_to_PumpFault, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2920`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sl7-0-3096823055` | `accept` | ❌ | ❌ | The unsafe_recovery finding is supported: the preserved global backManual transitions can enter Manual while pump_fault remains active, and the current Manual.enter/during unconditionally clears alarms and applies manual pump outputs. The smallest safe repair preserves all required backManual-to-Manual transitions and the FaultRemoved path, but makes Manual ...<truncated 578 chars> |
- repair_rationale：Accepted the current SL-7 model_review request because the evidence identifies a real unsafe path: PumpFault --CA/CB/CP/CC_backManual--> Manual could occur with pump_fault still active, and the old Manual state immediately cleared alarm_sig...<truncated 82 chars>；The repair preserves the previous non-regressive simulation frontier from FixLog: AutocontrolInit still prioritizes pump_fault and TerminateAC before the unconditional AutocontrolInit -> AutocontrolNormal transition, so the earlier autocont...<truncated 81 chars>；The backManual transitions remain present and still target Manual, preserving the NL-grounded cross-component recovery target and all required transition IDs. The change is local to Manual actions rather than deleting or retargeting grounde...<truncated 23 chars>；Manual normal behavior is unchanged when pump_fault == 0: CA_mode becomes Manual, control is released, alarms are cleared, and Manual.during sets pump_speed from built_in_switch_speed and flow_rate from default_flow_rate.；When pump_fault > 0, Manual now keeps alarm_signal, display_error, and sound_error asserted and keeps control_released = 1 while withholding manual pump_speed/flow_rate assignments until FaultRemoved clears pump_fault. This matches the NL o...<truncated 137 chars>
- diff_summary：`{"summary": "Changed only Manual.enter and Manual.during to be pump_fault-aware. Manual no longer clears alarms or applies manual pump outputs while pump_fault remains active; all states, variables, events, transitions, shared-buffer update, AutocontrolInit transition priority, PumpFault behavior, FaultRemoved behavior, and all four backManual forced transitions are preserved."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int patient_bp = 120;
def int shared_buffer_bp = 120;
def int target_bp = 120;
def int requested_target_bp = 120;
def int flow_rate = 0;
def int default_flow_rate = 1;
def int built_in_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int display_error = 0;
def int sound_error = 0;
def int control_released = 1;
def int log_count = 0;

state CARA_Mode_Control_Algorithm {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    >> during before { shared_buffer_bp = patient_bp; }

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault > 0] {
                alarm_signal = 1;
                display_error = 1;
                sound_error = 1;
            } else {
                alarm_signal = 0;
                display_error = 0;
                sound_error = 0;
            }
        }
        during {
            if [pump_fault == 0] {
                pump_speed = built_in_switch_speed;
                flow_rate = default_flow_rate;
            } else {
                alarm_signal = 1;
                display_error = 1;
                sound_error = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }
    }

    state Ask_StartAC;

    state AutocontrolInit {
        enter {
            CA_mode = 1;
            control_released = 0;
            alarm_signal = 0;
            display_error = 0;
            sound_error = 0;
        }
    }

    state AutocontrolNormal {
        during {
            if [pump_fault == 0] {
                if [patient_bp > target_bp] {
                    flow_rate = 1;
                } else if [patient_bp == target_bp] {
                    flow_rate = 3;
                } else {
                    flow_rate = 5;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_count = log_count + 1;
            }
        }
    }

    state PumpFault {
        enter {
            alarm_signal = 1;
            display_error = 1;
            sound_error = 1;
            control_released = 1;
            CA_mode = 0;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    AutocontrolInit -> PumpFault : if [pump_fault > 0];
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    AutocontrolNormal -> Manual :: TerminateAC;
    Ask_StartAC -> Manual :: TerminateAC;
    PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -29,13 +29,27 @@
         enter {
             CA_mode = 0;
             control_released = 1;
-            alarm_signal = 0;
-            display_error = 0;
-            sound_error = 0;
+            if [pump_fault > 0] {
+                alarm_signal = 1;
+                display_error = 1;
+                sound_error = 1;
+            } else {
+                alarm_signal = 0;
+                display_error = 0;
+                sound_error = 0;
+            }
         }
         during {
-            pump_speed = built_in_switch_speed;
-            flow_rate = default_flow_rate;
+            if [pump_fault == 0] {
+                pump_speed = built_in_switch_speed;
+                flow_rate = default_flow_rate;
+            } else {
+                alarm_signal = 1;
+                display_error = 1;
+                sound_error = 1;
+                control_released = 1;
+                CA_mode = 0;
+            }
         }
     }
 
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:2086f80ec2e3604e4dc37ade363a614bf60f11703d05051d3f451007ce3c343b`。
  - SL-10 evidence 1: `{"summary": "The current hard SL-7 request is the unsafe_recovery finding: global CA/CB/CP/CC_backManual transitions could enter Manual while pump_fault remained active, after which the old Manual.enter cleared alarm_signal/display_error/sound_error and Manual.during applied built_in_switch_speed/default_flow_rate. The candidate directly resolves that target by making Manual fault-aware: on Manual entry with pump_fault > 0 it asserts alarm_signal, display_error, and sound_error, and during Manual with pump_fault > 0 it keeps alarms asserted, keeps control_released = 1 and CA_mode = 0, and withholds manual pump_speed/flow_rate assignments until pump_fault == 0."}`
  - SL-10 evidence 2: `{"summary": "The repair is grounded in the NL. The NL says a pump fault activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. The candidate preserves global backManual as the shared Manual recovery target while preventing it from silently clearing alarms or enabling ordinary manual pump outputs before the active fault is removed."}`
  - SL-10 evidence 3: `{"summary": "The diff is narrowly scoped to Manual.enter and Manual.during. All required NL-grounded states, variables, events, and transitions remain represented: Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, initial [*] -> Manual, InitiateAC, ChangeSetpoint, StartAC, AutocontrolInit/AutocontrolNormal fault transitions, TerminateAC transitions, FaultRemoved, and all four global backManual transitions."}`
  - SL-10 evidence 4: `{"summary": "The prior FixLog simulation frontier is preserved. The earlier accepted AutocontrolInit transition-priority repair remains unchanged: AutocontrolInit -> PumpFault if pump_fault > 0 and AutocontrolInit -> Manual :: TerminateAC still precede the unconditional AutocontrolInit -> AutocontrolNormal transition. Thus the previous fixes for autocontrol_init_fault_priority and terminate_ac_from_init_and_normal are not regressed."}`
  - SL-10 evidence 5: `{"summary": "Normal Manual behavior remains intact when pump_fault == 0: Manual.enter sets CA_mode = 0 and control_released = 1 and clears error outputs, and Manual.during sets pump_speed = built_in_switch_speed and flow_rate = default_flow_rate, preserving the NL-required manual-mode pump operation after no fault is active or after FaultRemoved clears pump_fault."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:f705ac69b45689b590ac83622b5e87c8e46943c1aaeb6c6b4d4c7294afb0558b", "covered_local_objection_kinds": ["missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:065eb2766b18c8d54ec50d2b6e5128861486dde34aed271edb31614318aff3bd", "local_override_rationale_count": 2, "local_override_rationale_hash": "sha256:c8960b62ff533412e5883b8980be4bf16a117d1616e938bc9e6fc65e034cae13", "local_rejection_evidence_hash": "sha256:dec143b31bea133be00c5192ec467b466b3badcccf1d4f82b76615e73d5a5e48", "local_rejection_reason": "missing_required_grounding", "missing_local_objection_kinds": [], "policy": "SL-10 may override conservative ...<truncated 296 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial:Manual"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-b756e942c71` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-b756e942c71` | accept=2, reject=0 | `sl10_review` | `sha256:6448459b73453475d51ae3f572df1ea7482c6730750fa2b744a9cc498d5f0f4f` | For autocontrol_init_fault_priority, expected_state was CARA_Mode_Control_Algorithm.PumpFault with alarm_signal/display_error/sound_error/control_released = 1 and CA_mode = 0, but actual_state was AutocontrolNormal with those variables still in the AutocontrolInit values. Reordering the AutocontrolInit pump_fault guard before the bare transition makes an already-present pump fault win and enters PumpFault, whose enter action sets the expected variables., For terminate_ac_from_init_and_normal, expected_state was CARA_Mode_Control_Algorithm.Manual after the local AutocontrolInit.TerminateAC event, with CA_mode = 0, control_released = 1, pump_speed = built_in_switch_speed, and flow_rate = default_flow_rate. Reordering AutocontrolInit -> Manual :: TerminateAC before the bare transition lets the event fire before normal progression; Manual.enter and Manual.during already provide the expected manual-mode variable values., This is a minimal transition-priority edit only. It preserves all grounded states, variables, events, forced backManual transitions, Ask_StartAC behavior, normal autocontrol behavior, PumpFault behavior, shared-buffer update, and the required unconditional AutocontrolInit_to_AutocontrolNormal transition for the no-fault/no-terminate case. |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-b756e942c71` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:6448459b73453475d51ae3f572df1ea7482c6730750fa2b744a9cc498d5f0f4f` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-e5b28575443` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-e5b28575443` | accept=1, reject=0 | `sl10_review` | `sha256:f705ac69b45689b590ac83622b5e87c8e46943c1aaeb6c6b4d4c7294afb0558b` | Accepted the current SL-7 model_review request because the evidence identifies a real unsafe path: PumpFault --CA/CB/CP/CC_backManual--> Manual could occur with pump_fault still active, and the old Manual state immediately cleared alarm_signal/display_error/sound_error and applied built_in_switch_speed/default_flow_rate., The repair preserves the previous non-regressive simulation frontier from FixLog: AutocontrolInit still prioritizes pump_fault and TerminateAC before the unconditional AutocontrolInit -> AutocontrolNormal transition, so the earlier autocontrol_init_fault_priority and terminate_ac_from_init_and_normal fixes are retained., The backManual transitions remain present and still target Manual, preserving the NL-grounded cross-component recovery target and all required transition IDs. The change is local to Manual actions rather than deleting or retargeting grounded fallback transitions., ... +2 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-e5b28575443` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:f705ac69b45689b590ac83622b5e87c8e46943c1aaeb6c6b4d4c7294afb0558b` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +4 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4553, 'completion_chars': 17660, 'completion_tokens': 6169, 'elapsed_seconds': 119.14542422699742, 'estimated_completion_tokens': 4415, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11072, 'first_chunk_seconds': 34.97134239296429, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6454, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12623}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2810, 'completion_chars': 11562, 'completion_tokens': 3850, 'elapsed_seconds': 73.04962173296371, 'estimated_completion_tokens': 2891, 'estimated_prompt_tokens': 14395, 'estimated_total_tokens': 17286, 'first_chunk_seconds': 22.1931895709713, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 57578, 'prompt_tokens': 14145, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 17995}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1433, 'completion_chars': 5906, 'completion_tokens': 1665, 'elapsed_seconds': 34.397767935995944, 'estimated_completion_tokens': 1477, 'estimated_prompt_tokens': 26186, 'estimated_total_tokens': 27663, 'first_chunk_seconds': 8.283381017972715, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 104742, 'prompt_tokens': 23926, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25591}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 733, 'completion_chars': 3418, 'completion_tokens': 861, 'elapsed_seconds': 19.829657164984383, 'estimated_completion_tokens': 855, 'estimated_prompt_tokens': 26450, 'estimated_total_tokens': 27305, 'first_chunk_seconds': 6.340441465959884, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 105797, 'prompt_tokens': 23391, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24252}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3252, 'completion_chars': 13382, 'completion_tokens': 4810, 'elapsed_seconds': 92.0757111699786, 'estimated_completion_tokens': 3346, 'estimated_prompt_tokens': 18123, 'estimated_total_tokens': 21469, 'first_chunk_seconds': 33.28348606696818, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 72492, 'prompt_tokens': 17983, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22793}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1821, 'completion_chars': 8447, 'completion_tokens': 2861, 'elapsed_seconds': 56.67664292402333, 'estimated_completion_tokens': 2112, 'estimated_prompt_tokens': 20912, 'estimated_total_tokens': 23024, 'first_chunk_seconds': 23.44825940701412, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 83648, 'prompt_tokens': 20895, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23756}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1443, 'completion_chars': 6178, 'completion_tokens': 1962, 'elapsed_seconds': 42.241389798000455, 'estimated_completion_tokens': 1545, 'estimated_prompt_tokens': 49082, 'estimated_total_tokens': 50627, 'first_chunk_seconds': 16.045254482945893, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 196328, 'prompt_tokens': 44613, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 46575}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 768, 'completion_chars': 3628, 'completion_tokens': 941, 'elapsed_seconds': 21.671338205982465, 'estimated_completion_tokens': 907, 'estimated_prompt_tokens': 46579, 'estimated_total_tokens': 47486, 'first_chunk_seconds': 7.598300285986625, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 186313, 'prompt_tokens': 42001, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 42942}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3615, 'completion_chars': 14816, 'completion_tokens': 4137, 'elapsed_seconds': 78.63678401696961, 'estimated_completion_tokens': 3704, 'estimated_prompt_tokens': 22131, 'estimated_total_tokens': 25835, 'first_chunk_seconds': 13.21322869200958, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 88522, 'prompt_tokens': 22033, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26170}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1955, 'completion_chars': 9216, 'completion_tokens': 2453, 'elapsed_seconds': 49.68760341202142, 'estimated_completion_tokens': 2304, 'estimated_prompt_tokens': 24590, 'estimated_total_tokens': 26894, 'first_chunk_seconds': 14.347108233021572, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 98358, 'prompt_tokens': 24623, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 27076}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`37/16`，missing=`<none>`。
- repairs：`2/2` accepted；scenario_history=`5`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
