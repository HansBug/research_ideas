## path1 / cara-infusion-pump-formal-spec__01 / default 真实运行结果：Path1 CARA representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`not_converged`；record_status：`budget_exhausted`；result_status：`not_converged`。
- main_result_eligible：`false`。
- Path2 ref-model blueprint eligible：`n/a`；reason：not_applicable_to_path1。
- 一句话结论：`design_or_variable_dynamics`；停止原因：SD-4 design diagnostics: W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `cara-infusion-pump-formal-spec__01` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `min_sl10_rework_attempts=1`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `c3f9c93618624e5520dbe3aba4746a0140ae0d29` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9` |
| final verdict/status | verdict=`not_converged`, record=`budget_exhausted`, result=`not_converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a", "iteration": 4, "matching_repair_history_indices": [3, 4], "repair_history_index": 4, "selected_source_stage": "SD-4", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| SC-11 post-accept validation | attempted=`true`；attempts=`1`；success=`0`；failure=`1` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, ... +3` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, SD-4 design diagnostics: W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT` |
| token/cost/time | tokens=`{'prompt_tokens': 823330, 'completion_tokens': 59825, 'total_tokens': 883155, 'estimated_prompt_tokens': 1010729, 'estimated_completion_tokens': 46250, 'estimated_total_tokens': 1056979, 'prompt_chars': 4042892, 'completion_chars': 184971, 'n_calls': 17, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`1156.796s` |
| run record | [`pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:c9d98feb8828fa5819fb09d37a73af5453b4f5eeb9bf35089d977320a3639762` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `107` |
| `langgraph_node_trace_hash` | `sha256:c1668805e2d0a9b56ad9ee773ca94b2feef06b4d757cd59c57d5d514c2090338` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `107` |

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
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_display = 0;
def int error_sound = 0;
def int infusion_log_records = 0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_buffer_bp = 100.0;
def float patient_bp = 100.0;
def float default_flow_rate = 1.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Ask_StartAC -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! PumpFaultState -> Manual : CA_backManual;
        ! PumpFaultState -> Manual : CB_backManual;
        ! PumpFaultState -> Manual : CP_backManual;
        ! PumpFaultState -> Manual : CC_backManual;
        ! Ask_StartAC -> Manual :: CA_backManual;
        ! Ask_StartAC -> Manual :: CB_backManual;
        ! Ask_StartAC -> Manual :: CP_backManual;
        ! Ask_StartAC -> Manual :: CC_backManual;
        ! AutocontrolInit -> Manual :: CA_backManual;
        ! AutocontrolInit -> Manual :: CB_backManual;
        ! AutocontrolInit -> Manual :: CP_backManual;
        ! AutocontrolInit -> Manual :: CC_backManual;
        ! PumpFaultState -> Manual :: CA_backManual;
        ! PumpFaultState -> Manual :: CB_backManual;
        ! PumpFaultState -> Manual :: CP_backManual;
        ! PumpFaultState -> Manual :: CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_voltage = 0.0;
                if [pump_fault == 0] {
                    alarm_signal = 0;
                    error_display = 0;
                    error_sound = 0;
                } else {
                    alarm_signal = 1;
                    error_display = 1;
                    error_sound = 1;
                }
            }
            during {
                patient_bp = shared_buffer_bp;
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                patient_bp = shared_buffer_bp;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                patient_bp = shared_buffer_bp;
                if [pump_fault == 0] {
                    if [patient_bp > target_bp] {
                        infusion_rate = default_flow_rate - 1.0;
                    } else if [patient_bp < target_bp] {
                        infusion_rate = default_flow_rate + 1.0;
                    } else {
                        infusion_rate = default_flow_rate;
                    }
                    control_voltage = infusion_rate;
                    pump_speed = control_voltage;
                    infusion_log_records = infusion_log_records + 1;
                } else {
                    control_voltage = 0.0;
                    software_control = 0;
                }
            }
        }

        state PumpFaultState {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
                control_voltage = 0.0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> PumpFaultState :: PumpFault;
        PumpFaultState -> Manual :: RemoveFault effect { pump_fault = 0; };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14048 | 生成初始 DSL 与 grounding seeds | initial len=3048 | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=12,  | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=129624 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=21429 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=358488 | LLM per-request accept/reject + repair | candidate len=3256,3884,3712,4340,4340 | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=359566 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=12,  | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=129624 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=129624 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=358488 | LLM per-request accept/reject + repair | candidate len=3256,3884,3712,4340,4340 | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=359566 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=0, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=12,  | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=358488 | LLM per-request accept/reject + repair | candidate len=3256,3884,3712,4340,4340 | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=359566 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=12,  | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=129624 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=129624 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=358488 | LLM per-request accept/reject + repair | candidate len=3256,3884,3712,4340,4340 | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=359566 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=0, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=12,  | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=358488 | LLM per-request accept/reject + repair | candidate len=3256,3884,3712,4340,4340 | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=359566 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=0, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=0, advisory=23, info=0; blocking=12, advisory=23, info=0; blocking=12,  | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SD-4 design diagnostics: W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWE | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c2-dotenv-64f2f6b9.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T06:42:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T06:42:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T06:42:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T06:42:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T06:45:12Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T06:45:12Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=3048,hash=sha256:883949f7ca0b |
| 7 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T06:45:12Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:883949f7ca0bd9aedd641b53d3359d4932b07a40b67b826b6c401bfbb449e7ff |
| 10 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T06:45:12Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=3048,hash=sha256:883949f7ca0b, current_hash=sha256:883949f7ca0bd9aedd641b53d3359d4932b07a40b67b826b6c401bfbb449e7ff |
| 12 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T06:45:12Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T06:45:12Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T06:45:12Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T06:45:12Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T06:45:12Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T06:45:12Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-06T06:45:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T06:45:12Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-06T06:46:39Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-06T06:46:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T06:46:40Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-06T06:46:40Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-06T06:46:40Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-06T06:46:40Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-06T06:46:40Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-06T06:46:40Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-06T06:46:40Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-06T06:46:40Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-06T06:47:29Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-06T06:47:29Z` | `SL-7` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-06T06:47:29Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-06T06:47:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-06T06:47:29Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["DSL has forced transitions `! * -> Manual :: CA_backManual/CB_backManual/CP_backManual/CC_backManual` with no guard or fault-clearing effect.", "`Manual.enter` unconditionally sets `alarm_signal = 0`, `error_display = 0`, and `error_sound = 0`.", "`PumpFaultState -> Manual :: RemoveFault...<truncated 675 chars> | <none> |
| 38 | `2026-06-06T06:47:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-06T06:47:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-06T06:47:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-06T06:47:29Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["DSL has forced transitions `! * -> Manual :: CA_backManual/CB_backManual/CP_backManual/CC_backManual` with no guard or fault-clearing effect.", "`Manual.enter` unconditionally sets `alarm_signal = 0`, `error_display = 0`, and `error_sound = 0`.", "`PumpFaultState -> Manual :: RemoveFault effect...<truncated 668 chars> | current_dsl:len=3048,hash=sha256:883949f7ca0b |
| 42 | `2026-06-06T06:47:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-06T06:47:29Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 44 | `2026-06-06T06:47:29Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 45 | `2026-06-06T06:47:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-06T06:47:29Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=3048,hash=sha256:883949f7ca0b |
| 47 | `2026-06-06T06:48:01Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 48 | `2026-06-06T06:48:01Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=3256,hash=sha256:8a179db549bd |
| 49 | `2026-06-06T06:48:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 50 | `2026-06-06T06:48:01Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 51 | `2026-06-06T06:48:01Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:8a179db549bd24d3ce10980917b5585b4c678d10aaee17283990e155f5963af4 |
| 52 | `2026-06-06T06:48:26Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 53 | `2026-06-06T06:48:26Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 54 | `2026-06-06T06:48:26Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 55 | `2026-06-06T06:48:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 56 | `2026-06-06T06:48:26Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=3256,hash=sha256:8a179db549bd |
| 57 | `2026-06-06T06:48:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 58 | `2026-06-06T06:48:26Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:8a179db549bd24d3ce10980917b5585b4c678d10aaee17283990e155f5963af4 |
| 59 | `2026-06-06T06:48:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 60 | `2026-06-06T06:48:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 61 | `2026-06-06T06:48:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 62 | `2026-06-06T06:48:26Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:8a179db549bd24d3ce10980917b5585b4c678d10aaee17283990e155f5963af4 |
| 63 | `2026-06-06T06:48:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 64 | `2026-06-06T06:48:26Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=3256,hash=sha256:8a179db549bd, current_hash=sha256:8a179db549bd24d3ce10980917b5585b4c678d10aaee17283990e155f5963af4 |
| 65 | `2026-06-06T06:48:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 66 | `2026-06-06T06:48:26Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 67 | `2026-06-06T06:48:26Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 68 | `2026-06-06T06:48:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 69 | `2026-06-06T06:48:26Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 70 | `2026-06-06T06:48:26Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 71 | `2026-06-06T06:48:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 72 | `2026-06-06T06:48:26Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 73 | `2026-06-06T06:48:26Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-5A", "ok": true, "status": "StageStatus.OK"} | <none> |
| 74 | `2026-06-06T06:48:26Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 75 | `2026-06-06T06:48:27Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 targeted_retry", "ok": false, "reason": "reuse_frozen_scenario_set"} | <none> |
| 76 | `2026-06-06T06:48:27Z` | `<control>` | `1` | `frozen_scenario_refresh_targeted_retry` | {} | <none> |
| 77 | `2026-06-06T06:48:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 78 | `2026-06-06T06:48:27Z` | `SL-5` | `1` | `stage_enter` | {"reason": "targeted_refresh_after_frozen_gap_or_dsl_change"} | <none> |
| 79 | `2026-06-06T06:49:17Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 80 | `2026-06-06T06:49:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
- ……另有 `191` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SL-7` | yes | fixbatch-0-sha256-4201eb5f343 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-6` | yes | fixbatch-1-sha256-d61e73186fd / n=3 | accept=2, reject=1, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; scenario_regression; count_drift; forced_transition_count_drift; missing_required_ground...<truncated 3 char...<truncated 2 chars> | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SD-4` | yes | fixbatch-2-sha256-be748878c43 / n=12 | accept=12, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; count_drift; forced_transition_count_drift; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `SD-6` | yes | fixbatch-3-sha256-e09a65494c8 / n=3 | accept=3, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; count_drift; forced_transition_count_drift; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 4 | `SD-4` | yes | fixbatch-4-sha256-be748878c43 / n=12 | accept=12, reject=0, waiver=12 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=design_target_unresolved; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | SD-4 design diagnostics: W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT, W_SHADOWED_EVENT |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 4 |
|---|---|---|---|---|
| `default_init_manual_mode_outputs` | default-init probe: CARA dispatches into Manual mode and manual operation uses the built-in switch speed and caregiver d...<truncated 12 chars> | ✅ | ✅ | ✅ |
| `initiate_change_setpoint_start_autocontrol_high_bp` | default-init probe: caregiver initiates AC, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit where ...<truncated 20 chars> | ✅ | ✅ | ✅ |
| `autocontrol_low_bp_then_terminate_manual` | explicit-hot-start probe: normal autocontrol with low BP raises flow, then TerminateAC returns to Manual recovery operat...<truncated 4 chars> | ✅ | ✅ | ✅ |
| `pump_fault_alarm_release_then_remove_fault` | explicit-hot-start probe: a pump fault from autocontrol enters PumpFaultState with alarms and released control, then car...<truncated 39 chars> | ✅ | ✅ | ✅ |
| `autocontrol_existing_pump_fault_releases_control` | explicit-hot-start probe: while in AutocontrolInit with a pump-operation complication already present, CARA releases sof...<truncated 42 chars> | ✅ | ✅ | ✅ |
| `ca_backmanual_forced_from_ask_startac` | explicit-hot-start probe: CA_backManual is a cross-component fallback from Ask_StartAC to Manual with CA_mode becoming M...<truncated 6 chars> | ✅ | ✅ | ✅ |
| `cb_backmanual_forced_from_autocontrol` | explicit-hot-start probe: CB_backManual is a cross-component fallback from AutocontrolInit to the shared Manual recovery...<truncated 8 chars> | ✅ | ✅ | ✅ |
| `cp_backmanual_forced_from_pump_fault` | explicit-hot-start probe: CP_backManual is a cross-component fallback from PumpFaultState to Manual, but it is not careg...<truncated 59 chars> | ✅ | ❌ | ✅ |
| `cc_backmanual_forced_from_autocontrol` | explicit-hot-start probe: CC_backManual is another cross-component fallback from active autocontrol to Manual with manua...<truncated 26 chars> | ✅ | ✅ | ✅ |
| `local_ca_backmanual_forced_line_missing_probe` | explicit-hot-start probe: CA_backManual local fallback from AutocontrolInit must force Manual; if the forced declaration...<truncated 48 chars> | ⚪ | ⚪ | ⚪ |
| `local_cb_cp_cc_backmanual_forced_lines_missing_probe` | explicit-hot-start probe: local CB_backManual, CP_backManual, and CC_backManual events must each use their forced declar...<truncated 43 chars> | ⚪ | ⚪ | ⚪ |
| `normal_transition_wrong_target_matrix` | explicit-hot-start probe: local normal events must hit their exact NL targets across Manual, Ask_StartAC, AutocontrolIni...<truncated 38 chars> | ⚪ | ⚪ | ✅ |
| `additional_forced_missing_lines_from_distinct_leaves` | explicit-hot-start probe: additional local backManual forced declarations from Ask_StartAC, AutocontrolInit, and PumpFau...<truncated 58 chars> | ⚪ | ⚪ | ⚪ |
| `qualified_forced_transition_missing_line_matrix` | explicit-hot-start probe: fully-qualified backManual forced events from multiple non-Manual leaves must all reach the ex...<truncated 65 chars> | ⚪ | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_mode_outputs` — default-init probe: CARA dispatches into Manual mode and manual operation uses the built-in switch speed and caregiver default flow.</summary>

| Field | Value |
|---|---|
| description | default-init probe: CARA dispatches into Manual mode and manual operation uses the built-in switch speed and caregiver default flow. |
| initial_state | `<default-init>` |
| initial_vars | `{"default_flow_rate": 3.0, "manual_switch_speed": 2.5, "shared_buffer_bp": 110.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_voltage": 0.0, "error_display": 0, "error_sound": 0, "infusion_rate": 3.0, "patient_bp": 110.0, "pump_speed": 2.5, "software_control": 0}` |

</details>

<details><summary>`initiate_change_setpoint_start_autocontrol_high_bp` — default-init probe: caregiver initiates AC, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit where high BP lowers flow.</summary>

| Field | Value |
|---|---|
| description | default-init probe: caregiver initiates AC, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit where high BP lowers flow. |
| initial_state | `<default-init>` |
| initial_vars | `{"default_flow_rate": 5.0, "infusion_log_records": 0, "pump_fault": 0, "requested_target_bp": 105.0, "shared_buffer_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiate_enters_ask_startac` | `1` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"patient_bp": 120.0}` |
| 1 `change_setpoint_updates_target` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"patient_bp": 120.0, "target_bp": 105.0}` |
| 2 `startac_enters_autocontrol_and_lowers_flow` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "control_voltage": 4.0, "error_display": 0, "error_sound": 0, "infusion_log_records": 1, "infusion_rate": 4.0, "patient_bp": 120.0, "pump_speed": 4.0, "software_control": 1}` |

</details>

<details><summary>`autocontrol_low_bp_then_terminate_manual` — explicit-hot-start probe: normal autocontrol with low BP raises flow, then TerminateAC returns to Manual recovery operation.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: normal autocontrol with low BP raises flow, then TerminateAC returns to Manual recovery operation. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "default_flow_rate": 5.0, "infusion_log_records": 7, "manual_switch_speed": 1.7, "pump_fault": 0, "shared_buffer_bp": 80.0, "software_control": 1, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `low_bp_raises_flow_in_autocontrol` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"control_voltage": 6.0, "infusion_log_records": 8, "infusion_rate": 6.0, "patient_bp": 80.0, "pump_speed": 6.0, "software_control": 1}` |
| 1 `terminate_returns_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolInit.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 5.0, "patient_bp": 80.0, "pump_speed": 1.7, "software_control": 0}` |

</details>

<details><summary>`pump_fault_alarm_release_then_remove_fault` — explicit-hot-start probe: a pump fault from autocontrol enters PumpFaultState with alarms and released control, then caregiver fault removal returns to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: a pump fault from autocontrol enters PumpFaultState with alarms and released control, then caregiver fault removal returns to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "control_voltage": 3.0, "default_flow_rate": 4.0, "error_display": 0, "error_sound": 0, "manual_switch_speed": 2.0, "pump_fault": 0, "shared_buffer_bp": 100.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `pump_fault_enters_fault_state` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolInit.PumpFault"]` | `CARA.Mode_Control_Algorithm.PumpFaultState` | `{"CA_mode": 0, "alarm_signal": 1, "control_voltage": 0.0, "error_display": 1, "error_sound": 1, "pump_fault": 1, "software_control": 0}` |
| 1 `remove_fault_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFaultState.RemoveFault"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "error_display": 0, "error_sound": 0, "infusion_rate": 4.0, "pump_fault": 0, "pump_speed": 2.0, "software_control": 0}` |

</details>

<details><summary>`autocontrol_existing_pump_fault_releases_control` — explicit-hot-start probe: while in AutocontrolInit with a pump-operation complication already present, CARA releases software control instead of controlling flo...<truncated 2 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: while in AutocontrolInit with a pump-operation complication already present, CARA releases software control instead of controlling flow. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "control_voltage": 7.0, "default_flow_rate": 5.0, "pump_fault": 1, "shared_buffer_bp": 100.0, "software_control": 1, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `complication_releases_control` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"control_voltage": 0.0, "patient_bp": 100.0, "software_control": 0}` |

</details>

<details><summary>`ca_backmanual_forced_from_ask_startac` — explicit-hot-start probe: CA_backManual is a cross-component fallback from Ask_StartAC to Manual with CA_mode becoming Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: CA_backManual is a cross-component fallback from Ask_StartAC to Manual with CA_mode becoming Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "default_flow_rate": 2.2, "manual_switch_speed": 1.2, "shared_buffer_bp": 95.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 2.2, "patient_bp": 95.0, "pump_speed": 1.2, "software_control": 0}` |

</details>

<details><summary>`cb_backmanual_forced_from_autocontrol` — explicit-hot-start probe: CB_backManual is a cross-component fallback from AutocontrolInit to the shared Manual recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: CB_backManual is a cross-component fallback from AutocontrolInit to the shared Manual recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "control_voltage": 4.0, "default_flow_rate": 2.4, "manual_switch_speed": 1.4, "shared_buffer_bp": 102.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 2.4, "patient_bp": 102.0, "pump_speed": 1.4, "software_control": 0}` |

</details>

<details><summary>`cp_backmanual_forced_from_pump_fault` — explicit-hot-start probe: CP_backManual is a cross-component fallback from PumpFaultState to Manual, but it is not caregiver fault removal, so active fault alar...<truncated 19 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: CP_backManual is a cross-component fallback from PumpFaultState to Manual, but it is not caregiver fault removal, so active fault alarms remain asserted. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFaultState` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "default_flow_rate": 2.6, "error_display": 1, "error_sound": 1, "manual_switch_speed": 1.6, "pump_fault": 1, "shared_buffer_bp": 99.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_to_manual_with_fault_still_active` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 1, "error_display": 1, "error_sound": 1, "infusion_rate": 2.6, "patient_bp": 99.0, "pump_fault": 1, "pump_speed": 1.6, "software_control": 0}` |

</details>

<details><summary>`cc_backmanual_forced_from_autocontrol` — explicit-hot-start probe: CC_backManual is another cross-component fallback from active autocontrol to Manual with manual pump operation restored.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: CC_backManual is another cross-component fallback from active autocontrol to Manual with manual pump operation restored. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "control_voltage": 8.0, "default_flow_rate": 2.8, "manual_switch_speed": 1.8, "shared_buffer_bp": 101.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_backmanual_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 2.8, "patient_bp": 101.0, "pump_speed": 1.8, "software_control": 0}` |

</details>

<details><summary>`local_ca_backmanual_forced_line_missing_probe` — explicit-hot-start probe: CA_backManual local fallback from AutocontrolInit must force Manual; if the forced declaration is missing the event is ignored and thi...<truncated 8 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: CA_backManual local fallback from AutocontrolInit must force Manual; if the forced declaration is missing the event is ignored and this fails. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "control_voltage": 9.0, "default_flow_rate": 3.1, "manual_switch_speed": 2.1, "pump_fault": 0, "shared_buffer_bp": 104.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `local_ca_backmanual_forces_manual` | `0` | `["CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_voltage": 0.0, "error_display": 0, "error_sound": 0, "infusion_rate": 3.1, "patient_bp": 104.0, "pump_speed": 2.1, "software_control": 0}` |

</details>

<details><summary>`local_cb_cp_cc_backmanual_forced_lines_missing_probe` — explicit-hot-start probe: local CB_backManual, CP_backManual, and CC_backManual events must each use their forced declarations to return concrete leaves to Manu...<truncated 3 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: local CB_backManual, CP_backManual, and CC_backManual events must each use their forced declarations to return concrete leaves to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "control_voltage": 6.0, "default_flow_rate": 3.3, "manual_switch_speed": 2.3, "pump_fault": 0, "requested_target_bp": 100.0, "shared_buffer_bp": 103.0, "software_control": 1, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `local_cb_backmanual_forces_manual` | `0` | `["CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 3.3, "patient_bp": 103.0, "pump_speed": 2.3, "software_control": 0}` |
| 1 `navigate_manual_to_ask_for_cp_probe` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"patient_bp": 103.0}` |
| 2 `local_cp_backmanual_forces_manual` | `0` | `["CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 3.3, "patient_bp": 103.0, "pump_speed": 2.3, "software_control": 0}` |
| 3 `navigate_manual_to_ask_for_cc_probe` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"patient_bp": 103.0}` |
| 4 `start_autocontrol_for_cc_probe` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "control_voltage": 2.3, "error_display": 0, "error_sound": 0, "infusion_rate": 2.3, "patient_bp": 103.0, "pump_speed": 2.3, "software_control": 1}` |
| 5 `local_cc_backmanual_forces_manual` | `0` | `["CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 3.3, "patient_bp": 103.0, "pump_speed": 2.3, "software_control": 0}` |

</details>

<details><summary>`normal_transition_wrong_target_matrix` — explicit-hot-start probe: local normal events must hit their exact NL targets across Manual, Ask_StartAC, AutocontrolInit, PumpFaultState, and back to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: local normal events must hit their exact NL targets across Manual, Ask_StartAC, AutocontrolInit, PumpFaultState, and back to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"default_flow_rate": 3.0, "infusion_log_records": 0, "manual_switch_speed": 2.0, "pump_fault": 0, "requested_target_bp": 110.0, "shared_buffer_bp": 90.0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiateac_exact_target_ask_startac` | `0` | `["InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"patient_bp": 90.0}` |
| 1 `changesetpoint_self_target_preserves_ask` | `0` | `["ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"patient_bp": 90.0, "target_bp": 110.0}` |
| 2 `startac_exact_target_autocontrolinit` | `0` | `["StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "control_voltage": 4.0, "infusion_log_records": 1, "infusion_rate": 4.0, "patient_bp": 90.0, "pump_speed": 4.0, "software_control": 1}` |
| 3 `terminateac_exact_target_manual` | `0` | `["TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 3.0, "patient_bp": 90.0, "pump_speed": 2.0, "software_control": 0}` |
| 4 `renavigate_to_autocontrol_for_fault_target` | `0` | `["InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"patient_bp": 90.0}` |
| 5 `restart_autocontrol_for_fault_target` | `0` | `["StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "infusion_log_records": 2, "software_control": 1}` |
| 6 `pumpfault_exact_target_fault_state` | `0` | `["PumpFault"]` | `CARA.Mode_Control_Algorithm.PumpFaultState` | `{"CA_mode": 0, "alarm_signal": 1, "control_voltage": 0.0, "error_display": 1, "error_sound": 1, "pump_fault": 1, "software_control": 0}` |
| 7 `removefault_exact_target_manual` | `0` | `["RemoveFault"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "error_display": 0, "error_sound": 0, "infusion_rate": 3.0, "patient_bp": 90.0, "pump_fault": 0, "pump_speed": 2.0, "software_control": 0}` |

</details>

<details><summary>`additional_forced_missing_lines_from_distinct_leaves` — explicit-hot-start probe: additional local backManual forced declarations from Ask_StartAC, AutocontrolInit, and PumpFaultState must not be ignored if any force...<truncated 18 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: additional local backManual forced declarations from Ask_StartAC, AutocontrolInit, and PumpFaultState must not be ignored if any forced line is missing. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "default_flow_rate": 3.4, "infusion_log_records": 0, "manual_switch_speed": 2.4, "pump_fault": 0, "requested_target_bp": 100.0, "shared_buffer_bp": 96.0, "software_control": 1, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_from_ask_startac_forces_manual` | `0` | `["CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 3.4, "patient_bp": 96.0, "pump_speed": 2.4, "software_control": 0}` |
| 1 `go_to_ask_for_cp_autocontrol_probe` | `0` | `["InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"patient_bp": 96.0}` |
| 2 `go_to_autocontrol_for_cp_probe` | `0` | `["StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "control_voltage": 4.4, "infusion_log_records": 1, "infusion_rate": 4.4, "pump_speed": 4.4, "software_control": 1}` |
| 3 `cp_backmanual_from_autocontrol_forces_manual` | `0` | `["CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 3.4, "patient_bp": 96.0, "pump_speed": 2.4, "software_control": 0}` |
| 4 `renavigate_to_autocontrol_for_fault_forced_probe` | `0` | `["InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"patient_bp": 96.0}` |
| 5 `restart_autocontrol_for_fault_forced_probe` | `0` | `["StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "infusion_log_records": 2, "software_control": 1}` |
| 6 `enter_pump_fault_for_cc_forced_probe` | `0` | `["PumpFault"]` | `CARA.Mode_Control_Algorithm.PumpFaultState` | `{"CA_mode": 0, "alarm_signal": 1, "error_display": 1, "error_sound": 1, "pump_fault": 1, "software_control": 0}` |
| 7 `cc_backmanual_from_pump_fault_forces_manual_with_fault_still_active` | `0` | `["CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 1, "error_display": 1, "error_sound": 1, "infusion_rate": 3.4, "patient_bp": 96.0, "pump_fault": 1, "pump_speed": 2.4, "software_control": 0}` |

</details>

<details><summary>`qualified_forced_transition_missing_line_matrix` — explicit-hot-start probe: fully-qualified backManual forced events from multiple non-Manual leaves must all reach the exact Manual recovery target, catching mis...<truncated 25 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: fully-qualified backManual forced events from multiple non-Manual leaves must all reach the exact Manual recovery target, catching missing forced declarations. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "default_flow_rate": 3.7, "infusion_log_records": 0, "manual_switch_speed": 2.7, "pump_fault": 0, "requested_target_bp": 100.0, "shared_buffer_bp": 98.0, "software_control": 1, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `qualified_ca_from_ask_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 3.7, "patient_bp": 98.0, "pump_speed": 2.7, "software_control": 0}` |
| 1 `renavigate_ask_for_qualified_cb` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"patient_bp": 98.0}` |
| 2 `qualified_cb_from_ask_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 3.7, "patient_bp": 98.0, "pump_speed": 2.7, "software_control": 0}` |
| 3 `renavigate_autocontrol_for_qualified_cp` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"patient_bp": 98.0}` |
| 4 `start_autocontrol_for_qualified_cp` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "control_voltage": 4.7, "infusion_log_records": 1, "infusion_rate": 4.7, "pump_speed": 4.7, "software_control": 1}` |
| 5 `qualified_cp_from_autocontrol_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "infusion_rate": 3.7, "patient_bp": 98.0, "pump_speed": 2.7, "software_control": 0}` |
| 6 `renavigate_fault_for_qualified_cc` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"patient_bp": 98.0}` |
| 7 `start_autocontrol_for_qualified_cc_fault` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "infusion_log_records": 2, "software_control": 1}` |
| 8 `enter_fault_for_qualified_cc` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolInit.PumpFault"]` | `CARA.Mode_Control_Algorithm.PumpFaultState` | `{"CA_mode": 0, "alarm_signal": 1, "error_display": 1, "error_sound": 1, "pump_fault": 1, "software_control": 0}` |
| 9 `qualified_cc_from_fault_forces_manual_with_fault_still_active` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 1, "error_display": 1, "error_sound": 1, "infusion_rate": 3.7, "patient_bp": 98.0, "pump_fault": 1, "pump_speed": 2.7, "software_control": 0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:8a179db549bd24d3ce10980917b5585b4c678d10aaee17283990e155f5963af4` |
| 2 | `1` | ✅ | `SD-6` | cp_backmanual_forced_from_pump_fault, local_ca_backmanual_forced_line_missing_probe, local_cb_cp_cc_backmanual_forced_lines_missing_probe | accept=2, reject=1, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; scenario_regression; count_drift; forced_transition_c...<truncated 57 chars> | `sha256:e6a8d18daf59578866d1755941aed2570242002296a7deb907b5b0a19fd2b974` |
| 3 | `2` | ✅ | `SD-4` | W_SHADOWED_EVENT:9a2adf8046b5, W_SHADOWED_EVENT:c3a3d83d124f, W_SHADOWED_EVENT:f4a31c8cdc03, W_SHADOWED_EVENT:cea5fb9348b6, W_SHADOWED_EVENT:30c3e7e6cb03, ... +11 | accept=12, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; count_drift; forced_transition_count_drift; missing_required_gro...<truncated 6 chars> | `sha256:b7a0368ce4e1d2c0819a8cdbfbe0de1f7d3708ffcdcb0e3e8a92ffd94faabbdd` |
| 4 | `3` | ✅ | `SD-6` | local_ca_backmanual_forced_line_missing_probe, local_cb_cp_cc_backmanual_forced_lines_missing_probe, additional_forced_missing_lines_from_distinct_leaves | accept=3, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; count_drift; forced_transition_count_drift; missing_...<truncated 18 chars> | `sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a` |
| 5 | `4` | ✅ | `SD-4` | W_SHADOWED_EVENT:9a2adf8046b5, W_SHADOWED_EVENT:c3a3d83d124f, W_SHADOWED_EVENT:f4a31c8cdc03, W_SHADOWED_EVENT:cea5fb9348b6, W_SHADOWED_EVENT:30c3e7e6cb03, ... +11 | accept=12, reject=0, waiver=12 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=design_target_unresolved; missing_required_grounding | `sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a` |

<details><summary>Repair 1 / iteration `0` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:883949f7ca0bd9aedd641b53d3359d4932b07a40b67b826b6c401bfbb449e7ff`；candidate_dsl_hash：`sha256:8a179db549bd24d3ce10980917b5585b4c678d10aaee17283990e155f5963af4`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Cross-component backManual recovery can suppress alarms and enter Manual while an active pump fault remains uncleared.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-4201eb5f343`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL has forced transitions `! * -> Manual :: CA_backManual/CB_backManual/CP_backManual/CC_backManual` with no guard or fault-clearing effect.', '`Manual.enter` unconditionally sets `alarm_signal = 0`, `error_display = 0`, and `error_sound = 0`.', '`PumpFaultState -> Manual :: RemoveFault effect { pump_fault = 0; }` clears the fault only on explicit RemoveFault, but forced backManual transitions do not.', 'Simulation scenario `cp_backmanual_forced_from_pump_fault` ends in `Manual` with `pump_fault: 1` and `alarm_signal/error_display/error_sound: 0`, despite the NL saying pump faults activate alarm signals and the caregiver removes the fault.'], 'severity': 'major', 'summary': 'Cross-component backManual recovery can suppress alarms and enter Manual while an active pump fault remains uncleared.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:PumpFaultState, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:error_display, variable:error_sound, variable:target_bp, ... +36`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3256`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ❌ | The hard blocking review evidence is valid: wildcard backManual transitions can enter Manual while pump_fault remains set, and Manual.enter previously cleared alarms unconditionally. The smallest safe NL-grounded repair is to make Manual entry clear alarms only when no pump fault remains; if pump_fault is still active, Manual preserves/reactivates alarm and ...<truncated 337 chars> |
- repair_rationale：Accepted the unsafe_recovery request because the evidence identifies a real NL-fidelity gap: backManual recovery should make CA_mode Manual, but it should not imply caregiver fault removal or suppress active pump-fault alarms.；Expected for cp_backmanual_forced_from_pump_fault: after CP_backManual from PumpFaultState, state may become Manual and software control is released, but pump_fault remains 1 until RemoveFault and alarm_signal/error_display/error_sound rema...<truncated 170 chars>；The explicit PumpFaultState -> Manual :: RemoveFault effect { pump_fault = 0; } remains the only modeled caregiver fault-removal path. Once RemoveFault clears pump_fault before Manual.enter runs, Manual.enter clears alarms/errors normally.；All required grounded elements are preserved: Mode_Control_Algorithm hierarchy, Manual, Ask_StartAC, AutocontrolInit, PumpFaultState, all variables, initial transitions, InitiateAC/ChangeSetpoint/StartAC/TerminateAC/PumpFault/RemoveFault tr...<truncated 182 chars>；No new plant/environment dynamics were invented; the edit only makes existing Manual entry side effects conditional on the already-modeled pump_fault state.
- diff_summary：`{"summary": "Changed Manual.enter from unconditional alarm/error clearing to conditional logic: clear alarm_signal/error_display/error_sound only when pump_fault == 0; otherwise set them to 1 while still setting CA_mode = 0, software_control = 0, and control_voltage = 0.0. No states, transitions, events, or variables were deleted."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_display = 0;
def int error_sound = 0;
def int infusion_log_records = 0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_buffer_bp = 100.0;
def float patient_bp = 100.0;
def float default_flow_rate = 1.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;

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
                control_voltage = 0.0;
                if [pump_fault == 0] {
                    alarm_signal = 0;
                    error_display = 0;
                    error_sound = 0;
                } else {
                    alarm_signal = 1;
                    error_display = 1;
                    error_sound = 1;
                }
            }
            during {
                patient_bp = shared_buffer_bp;
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                patient_bp = shared_buffer_bp;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                patient_bp = shared_buffer_bp;
                if [pump_fault == 0] {
                    if [patient_bp > target_bp] {
                        infusion_rate = default_flow_rate - 1.0;
                    } else if [patient_bp < target_bp] {
                        infusion_rate = default_flow_rate + 1.0;
                    } else {
                        infusion_rate = default_flow_rate;
                    }
                    control_voltage = infusion_rate;
                    pump_speed = control_voltage;
                    infusion_log_records = infusion_log_records + 1;
                } else {
                    control_voltage = 0.0;
                    software_control = 0;
                }
            }
        }

        state PumpFaultState {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
                control_voltage = 0.0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> PumpFaultState :: PumpFault;
        PumpFaultState -> Manual :: RemoveFault effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -31,9 +31,15 @@
                 CA_mode = 0;
                 software_control = 0;
                 control_voltage = 0.0;
-                alarm_signal = 0;
-                error_display = 0;
-                error_sound = 0;
+                if [pump_fault == 0] {
+                    alarm_signal = 0;
+                    error_display = 0;
+                    error_sound = 0;
+                } else {
+                    alarm_signal = 1;
+                    error_display = 1;
+                    error_sound = 1;
+                }
             }
             during {
                 patient_bp = shared_buffer_bp;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:4d12afaf460a6d792b02c0faedba595c43ef2886ec5a3219c1767d49c04c38f9`。
  - SL-10 evidence 1: `{"summary": "The hard SL-7 request was unsafe_recovery: wildcard backManual transitions could enter Manual with pump_fault still active while Manual.enter unconditionally cleared alarm_signal, error_display, and error_sound. The candidate directly changes only Manual.enter so alarms/errors are cleared when pump_fault == 0 and asserted when pump_fault != 0, while preserving CA_mode = 0, software_control = 0, and control_voltage = 0.0. This resolves the NL-fidelity problem because an uncleared pump fault continues to activate alarm/error indications until caregiver RemoveFault clears pump_fault."}`
  - SL-10 evidence 2: `{"summary": "The explicit caregiver fault-removal path is preserved: PumpFaultState -> Manual :: RemoveFault effect { pump_fault = 0; } remains the only transition that clears pump_fault. Because the effect clears pump_fault before Manual.enter, normal RemoveFault recovery still reaches Manual with alarms/errors cleared, matching the passing local scenario pump_fault_alarm_release_then_remove_fault."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves all NL-required states, variables, events, transitions, guards, and actions relevant to the request: Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, PumpFaultState, all four backManual events/transitions, ChangeSetpoint target_bp update, StartAC to AutocontrolInit, TerminateAC, PumpFault, RemoveFault, Manual pump-speed/default-flow behavior, and the AutocontrolInit pump_fault == 0 guarded BP-based infusion-rate computation."}`
  - SL-10 evidence 4: `{"summary": "Local simulation evidence supports no behavioral regression for the NL obligations: 8 of 9 scenarios pass, including default Manual operation, setpoint change and StartAC, BP high/low infusion-rate adjustment, TerminateAC recovery, PumpFault alarm/release, RemoveFault clearing, and backManual from non-fault states. The sole failing scenario is the previously identified weak oracle case expecting alarms off while pump_fault remains active after CP_backManual from PumpFaultState; that expectation contradicts the SL-7 blocking finding and NL fault-alarm requirement."}`
  - SL-10 evidence 5: `{"candidate_dsl_hash": "sha256:8a179db549bd24d3ce10980917b5585b4c678d10aaee17283990e155f5963af4", "covered_local_objection_kinds": ["scenario_regression", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:1cd090e8537fcf24ccda1ea4cd671490465a536808d96e27dc6ab4c0c8347e11", "local_override_rationale_count": 4, "local_override_rationale_hash": "sha256:a1e13fd0dd453652bf32c03822a4ddb3027a0fd39e6eade3ea7a5ffd98bdd818", "local_rejection_evidence_hash": "sha256:71fecb6ae4047639e6dcc7020e9c1232f3ccdf0f764c20fa4edf5a126d3b25b4", "local_rejection_reason": "scenario_regression; missing_required_grounding", "missing_local_objection_kinds": [],...<truncated 340 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 9, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init probe: CARA dispatches into Manual mode and manual operation uses the built-in switch speed and caregiver default flow.", "name": "default_init_manual_mode_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_signal":...<truncated 10187 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:InitialRoot", "transition:InitialModeControlManual", "action:SetTargetBP", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "guard:NoPumpFaultAutocontrol"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `1` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`cp_backmanual_forced_from_pump_fault, local_ca_backmanual_forced_line_missing_probe, local_cb_cp_cc_backmanual_forced_lines_missing_probe`。
- before_dsl_hash：`sha256:8a179db549bd24d3ce10980917b5585b4c678d10aaee17283990e155f5963af4`；candidate_dsl_hash：`sha256:e6a8d18daf59578866d1755941aed2570242002296a7deb907b5b0a19fd2b974`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-d61e73186fd`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`3`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-f99437c2d0` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: CP_backManual is a cross-component fallback from PumpFaultState to Manual, not a wildcard literal state.', 'name': 'cp_backmanual_forced_from_pump_fault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: CP_backManual is a cross-component fallback from PumpFaultState to Manual, not a wildcard literal state.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'error_display': 1, 'error_sound': 1, 'infusion_rate': 2.6, 'patient_bp': 99.0, 'pump_speed': 1.6, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'error_display': 0, 'error_sound': 0, 'infusion_rate': 2.6, 'patient_bp': 99.0, 'pump_speed': 1.6, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'cp_backmanual_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}, 'error_display': {'actual': 1, 'expected': 0}, 'error_sound': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFaultState', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 1, 'default_flow_rate': 2.6, 'error_display': 1, 'error_sound': 1, 'manual_switch_speed': 1.6, 'pump_fault': 1, 'shared_buffer_bp': 99.0, 'software_control': 1}, 'scenario_name': 'cp_backmanual_forced_from_pump_fault', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'control_voltage': 0.0, 'default_flow_rate': 2.6, 'error_display': 1, 'error_sound': 1, 'infusion_log_records': 0, 'infusion_rate': 2.6, 'manual_switch_speed': 1.6, 'patient_bp': 99.0, 'pump_fault': 1, 'pump_speed': 1.6, 'requested_target_bp': 100.0, 'shared_buffer_bp': 99.0, 'software_control': 0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'cp_backmanual_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}, 'error_display': {'actual': 1, 'expected': 0}, 'error_sound': {'actual': 1, 'expected': 0}}}]}` |
| `fixreq-1-sd6-1-98836cd10e` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: CA_backManual local fallback from AutocontrolInit must force Manual; if the forced declaration is missing the event is ignored and this fails.', 'name': 'local_ca_backmanual_forced_line_missing_probe', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: CA_backManual local fallback from AutocontrolInit must force Manual; if the forced declaration is missing the event is ignored and this fails.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'control_voltage': 9.0, 'error_display': 0, 'error_sound': 0, 'infusion_rate': 1.0, 'patient_bp': 100.0, 'pump_speed': 0.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'control_voltage': 0.0, 'error_display': 0, 'error_sound': 0, 'infusion_rate': 3.1, 'patient_bp': 104.0, 'pump_speed': 2.1, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CA_backManual'", 'runtime_error_hint': {'event_path': 'CA_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'local_ca_backmanual_forces_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'control_voltage': 9.0, 'default_flow_rate': 3.1, 'manual_switch_speed': 2.1, 'pump_fault': 0, 'shared_buffer_bp': 104.0, 'software_control': 1}, 'scenario_name': 'local_ca_backmanual_forced_line_missing_probe', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_voltage': 9.0, 'default_flow_rate': 3.1, 'error_display': 0, 'error_sound': 0, 'infusion_log_records': 0, 'infusion_rate': 1.0, 'manual_switch_speed': 2.1, 'patient_bp': 100.0, 'pump_fault': 0, 'pump_speed': 0.0, 'requested_target_bp': 100.0, 'shared_buffer_bp': 104.0, 'software_control': 1, 'target_bp': 100.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CA_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'local_ca_backmanual_forces_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-2-ae51f7e396` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: local CB_backManual, CP_backManual, and CC_backManual events must each use their forced wildcard declarations to return concrete leaves to Manual.', 'name': 'local_cb_cp_cc_backmanual_forced_lines_missing_probe', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: local CB_backManual, CP_backManual, and CC_backManual events must each use their forced wildcard declarations to return concrete leaves to Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'control_voltage': 6.0, 'infusion_rate': 1.0, 'patient_bp': 100.0, 'pump_speed': 0.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_voltage': 0.0, 'infusion_rate': 3.3, 'patient_bp': 103.0, 'pump_speed': 2.3, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CB_backManual'", 'runtime_error_hint': {'event_path': 'CB_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'local_cb_backmanual_forces_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'control_voltage': 6.0, 'default_flow_rate': 3.3, 'manual_switch_speed': 2.3, 'pump_fault': 0, 'requested_target_bp': 100.0, 'shared_buffer_bp': 103.0, 'software_control': 1, 'target_bp': 100.0}, 'scenario_name': 'local_cb_cp_cc_backmanual_forced_lines_missing_probe', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_voltage': 6.0, 'default_flow_rate': 3.3, 'error_display': 0, 'error_sound': 0, 'infusion_log_records': 0, 'infusion_rate': 1.0, 'manual_switch_speed': 2.3, 'patient_bp': 100.0, 'pump_fault': 0, 'pump_speed': 0.0, 'requested_target_bp': 100.0, 'shared_buffer_bp': 103.0, 'software_control': 1, 'target_bp': 100.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CB_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'local_cb_backmanual_forces_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:PumpFaultState, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:error_display, variable:error_sound, variable:target_bp, ... +36`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3884`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-f99437c2d0` | `reject` | ❌ | ❌ | Rejected as a stale/contradictory oracle target for cp_backmanual_forced_from_pump_fault. The failing step expects alarm_signal/error_display/error_sound to become 0 while pump_fault remains 1 after CP_backManual from PumpFaultState. The FixLog shows this exact local objection was already overridden by SL-10 because NL says pump faults activate alarms and th...<truncated 192 chars> |
| `fixreq-1-sd6-1-98836cd10e` | `accept` | ❌ | ❌ | Accepted. The local_ca_backmanual_forced_line_missing_probe shows a real runtime event-resolution gap: injecting local event CA_backManual from hot-start AutocontrolInit cannot resolve even though the NL requires CA_backManual to cause shared recovery to Manual. The smallest safe edit is to add source-leaf forced backManual declarations visible from Autocont...<truncated 304 chars> |
| `fixreq-1-sd6-2-ae51f7e396` | `accept` | ❌ | ❌ | Accepted. The local_cb_cp_cc_backmanual_forced_lines_missing_probe shows the same event-resolution gap for local CB_backManual/CP_backManual/CC_backManual injected from concrete active leaves. The edit adds explicit leaf-scope forced fallback declarations for the meaningful Mode_Control_Algorithm leaves so local event names resolve from active states while p...<truncated 305 chars> |
- repair_rationale：For local_ca_backmanual_forced_line_missing_probe, the expected state after local CA_backManual from AutocontrolInit is Manual with CA_mode = 0, software_control = 0, control_voltage = 0.0, and Manual.during restoring patient_bp, pump_speed...<truncated 255 chars>；For local_cb_cp_cc_backmanual_forced_lines_missing_probe, the expected state after local CB_backManual/CP_backManual/CC_backManual from concrete leaves is the shared Manual recovery target. The actual evidence showed unresolved local CB_bac...<truncated 252 chars>；For cp_backmanual_forced_from_pump_fault, the only mismatch is the stale expectation that alarms/errors clear even though pump_fault remains active. The FixLog and SL-10 override identify that expectation as contrary to the NL fault-alarm r...<truncated 179 chars>；All required grounded elements are preserved: Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, PumpFaultState, all variables, initial transitions, caregiver Start/Terminate/ChangeSetpoint events, PumpFault/RemoveFault handling,...<truncated 176 chars>
- diff_summary：`{"summary": "Kept the SL-10-accepted Manual.enter alarm conditional unchanged. Added explicit leaf-scope forced backManual declarations from Ask_StartAC, AutocontrolInit, and PumpFaultState for CA_backManual, CB_backManual, CP_backManual, and CC_backManual so local event injection from active concrete leaves resolves to Manual. Existing wildcard cross-component fallback declarations and all grounded states/actions/transitions are preserved."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_display = 0;
def int error_sound = 0;
def int infusion_log_records = 0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_buffer_bp = 100.0;
def float patient_bp = 100.0;
def float default_flow_rate = 1.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! Ask_StartAC -> Manual :: CA_backManual;
        ! Ask_StartAC -> Manual :: CB_backManual;
        ! Ask_StartAC -> Manual :: CP_backManual;
        ! Ask_StartAC -> Manual :: CC_backManual;
        ! AutocontrolInit -> Manual :: CA_backManual;
        ! AutocontrolInit -> Manual :: CB_backManual;
        ! AutocontrolInit -> Manual :: CP_backManual;
        ! AutocontrolInit -> Manual :: CC_backManual;
        ! PumpFaultState -> Manual :: CA_backManual;
        ! PumpFaultState -> Manual :: CB_backManual;
        ! PumpFaultState -> Manual :: CP_backManual;
        ! PumpFaultState -> Manual :: CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_voltage = 0.0;
                if [pump_fault == 0] {
                    alarm_signal = 0;
                    error_display = 0;
                    error_sound = 0;
                } else {
                    alarm_signal = 1;
                    error_display = 1;
                    error_sound = 1;
                }
            }
            during {
                patient_bp = shared_buffer_bp;
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                patient_bp = shared_buffer_bp;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                patient_bp = shared_buffer_bp;
                if [pump_fault == 0] {
                    if [patient_bp > target_bp] {
                        infusion_rate = default_flow_rate - 1.0;
                    } else if [patient_bp < target_bp] {
                        infusion_rate = default_flow_rate + 1.0;
                    } else {
                        infusion_rate = default_flow_rate;
                    }
                    control_voltage = infusion_rate;
                    pump_speed = control_voltage;
                    infusion_log_records = infusion_log_records + 1;
                } else {
                    control_voltage = 0.0;
                    software_control = 0;
                }
            }
        }

        state PumpFaultState {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
                control_voltage = 0.0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> PumpFaultState :: PumpFault;
        PumpFaultState -> Manual :: RemoveFault effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -23,6 +23,18 @@
         ! * -> Manual :: CB_backManual;
         ! * -> Manual :: CP_backManual;
         ! * -> Manual :: CC_backManual;
+        ! Ask_StartAC -> Manual :: CA_backManual;
+        ! Ask_StartAC -> Manual :: CB_backManual;
+        ! Ask_StartAC -> Manual :: CP_backManual;
+        ! Ask_StartAC -> Manual :: CC_backManual;
+        ! AutocontrolInit -> Manual :: CA_backManual;
+        ! AutocontrolInit -> Manual :: CB_backManual;
+        ! AutocontrolInit -> Manual :: CP_backManual;
+        ! AutocontrolInit -> Manual :: CC_backManual;
+        ! PumpFaultState -> Manual :: CA_backManual;
+        ! PumpFaultState -> Manual :: CB_backManual;
+        ! PumpFaultState -> Manual :: CP_backManual;
+        ! PumpFaultState -> Manual :: CC_backManual;
 
         [*] -> Manual;
 
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:d0c44f80bd963d39bdaddf64dda78875cceb57c523dd69df74d5cf779b397951`。
  - SL-10 evidence 1: `{"summary": "The current SL-9 candidate preserves the previously SL-10-accepted Manual.enter conditional alarm behavior: alarms and caregiver error indications clear only when pump_fault == 0 and remain asserted when pump_fault == 1. This continues to satisfy the NL requirement that pump faults activate alarm signals and that caregiver RemoveFault, not a backManual fallback, is the modeled fault-removal path."}`
  - SL-10 evidence 2: `{"summary": "The newly accepted repair requests were event-resolution failures for local CA_backManual, CB_backManual, CP_backManual, and CC_backManual injections from concrete leaves. The diff adds explicit forced leaf-scope transitions from Ask_StartAC, AutocontrolInit, and PumpFaultState to Manual for each of the four backManual events while preserving the original wildcard cross-component fallback declarations. Local simulation evidence confirms the two new probes now pass: local_ca_backmanual_forced_line_missing_probe reaches Manual with CA_mode = 0, software_control = 0, control_voltage = 0.0, patient_bp from shared_buffer_bp, pump_speed from manual_switch_speed, and infusion_rate from...<truncated 115 chars>`
  - SL-10 evidence 3: `{"summary": "SL-9 correctly rejected fixreq-1-sd6-0 as a stale contradictory oracle target. The cp_backmanual_forced_from_pump_fault scenario still expects alarm_signal/error_display/error_sound = 0 while pump_fault remains 1 after CP_backManual from PumpFaultState. The FixLog records that exact expectation was already overridden by SL-10 because it contradicts the NL fault-alarm requirement and the original unsafe_recovery repair objective."}`
  - SL-10 evidence 4: `{"summary": "The candidate does not drop NL-required structure or behavior. Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, PumpFaultState, all required variables, the initial transitions, InitiateAC, ChangeSetpoint with target_bp update, StartAC, TerminateAC, PumpFault, RemoveFault, all four backManual events, the pump_fault == 0 autocontrol guard, BP-based infusion computation, manual pump-speed/default-flow behavior, and fault alarm/release behavior remain represented."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic checks now show 10 of 11 scenarios passing. The only remaining scenario failure is the previously overridden stale CP_backManual alarm expectation. The prior local event-resolution errors that motivated the current repair are resolved, and the remaining local objections are design/count/matcher concerns caused by the deliberate explicit event-visibility repair rather than evidence of an NL-fidelity regression."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:e6a8d18daf59578866d1755941aed2570242002296a7deb907b5b0a19fd2b974", "covered_local_objection_kinds": ["new_blocking_design_diagnostic", "scenario_regression", "count_drift", "forced_transition_count_drift", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:7e85e4f6f597cd26d8decedafc3fdc784e34a8d5b030f8db28ecb7a7a470beeb", "local_override_rationale_count": 6, "local_override_rationale_hash": "sha256:c85403d57fe983c8a6a1810ee5f78b84e58264341c86dd37349c31e9ab56a110", "local_rejection_evidence_hash": "sha256:06ce53c0606c1ed49783c11f43bc974f5a373bb2e65ed33505ee8b962d0a6b3b", "local_rejection_reason": "new_...<truncated 498 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; scenario_regression; count_drift; forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_SHADOWED_EVENT", "instance_key": "W_SHADOWED_EVENT:9a2adf8046b5", "message": "Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.", "policy_action": "requires_policy_classification", "pyfcstm_severity": "warning", "rationale": "", "refs": {"chain_path": "CARA.Mode_Control_Algorithm.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.Mode_Control_Alg...<truncated 12125 chars>
    - local evidence 2: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 11, "n_scenarios_passed": 10, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init probe: CARA dispatches into Manual mode and manual operation uses the built-in switch speed and caregiver default flow.", "name": "default_init_manual_mode_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_signal...<truncated 15110 chars>
    - local evidence 3: `count_drift` {"direction": "increase", "drift_ratio": 0.5, "field": "n_transitions", "fix_target": "sim", "kind": "count_drift", "new": 36, "old": 24}
    - local evidence 4: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 28, "old": 16}
    - local evidence 5: `missing_required_grounding` {"element_ids": ["transition:InitialRoot", "transition:InitialModeControlManual", "action:SetTargetBP", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "guard:NoPumpFaultAutocontrol"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `2` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`False`。
- problem_summary：Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.PumpFaultState.CA_backManual' shadows a chain event named 'CA_backManual'.
- diagnostic ids：`W_SHADOWED_EVENT:9a2adf8046b5, W_SHADOWED_EVENT:c3a3d83d124f, W_SHADOWED_EVENT:f4a31c8cdc03, W_SHADOWED_EVENT:cea5fb9348b6, W_SHADOWED_EVENT:30c3e7e6cb03, W_SHADOWED_EVENT:71bb63ebf102, W_SHADOWED_EVENT:6c8ba1ef669e, W_SHADOWED_EVENT:9c2847ada744, W_SHADOWED_EVENT:51873bd93686, W_SHADOWED_EVENT:649a0af501b4, W_SHADOWED_EVENT:1f8ced956d1d, W_SHADOWED_EVENT:1e80b5845db8, ... +4`。
- before_dsl_hash：`sha256:e6a8d18daf59578866d1755941aed2570242002296a7deb907b5b0a19fd2b974`；candidate_dsl_hash：`sha256:b7a0368ce4e1d2c0819a8cdbfbe0de1f7d3708ffcdcb0e3e8a92ffd94faabbdd`。

#### 错误证据 / diagnostics

- 1. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:9a2adf8046b5` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual"}`
- 2. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:c3a3d83d124f` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual"}`
- 3. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:f4a31c8cdc03` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.PumpFaultState.CA_backManual' shadows a chain event named 'CA_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.Mode_Control_Algorithm.PumpFaultState.CA_backManual"}`
- 4. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:cea5fb9348b6` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CB_backManual' shadows a chain event named 'CB_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CB_backManual", "event_name": "CB_backManual", "local_path": "CARA.Mode_Control_Algorithm.Ask_StartAC.CB_backManual"}`
- 5. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:30c3e7e6cb03` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CB_backManual' shadows a chain event named 'CB_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CB_backManual", "event_name": "CB_backManual", "local_path": "CARA.Mode_Control_Algorithm.AutocontrolInit.CB_backManual"}`
- 6. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:71bb63ebf102` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.PumpFaultState.CB_backManual' shadows a chain event named 'CB_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CB_backManual", "event_name": "CB_backManual", "local_path": "CARA.Mode_Control_Algorithm.PumpFaultState.CB_backManual"}`
- 7. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:6c8ba1ef669e` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CC_backManual' shadows a chain event named 'CC_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CC_backManual", "event_name": "CC_backManual", "local_path": "CARA.Mode_Control_Algorithm.Ask_StartAC.CC_backManual"}`
- 8. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:9c2847ada744` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CC_backManual' shadows a chain event named 'CC_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CC_backManual", "event_name": "CC_backManual", "local_path": "CARA.Mode_Control_Algorithm.AutocontrolInit.CC_backManual"}`
- ……另有 `4` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `CA_mode` | `unknown` | ✅ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `alarm_signal` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `control_voltage` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `default_flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `error_display` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `error_sound` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `infusion_log_records` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `infusion_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `manual_switch_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `patient_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `pump_fault` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `pump_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `requested_target_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `shared_buffer_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `software_control` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `target_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-be748878c43`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sd4-0-95304766fc` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-2-sd4-1-efd1458b11` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-2-sd4-2-6ae2848916` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-2-sd4-3-83125227a5` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-2-sd4-4-cd6f6c8be0` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-2-sd4-5-3608c61314` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-2-sd4-6-f2bbd0ea7d` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-2-sd4-7-5ee7fcda61` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-2-sd4-8-6a083b52a5` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-2-sd4-9-1f255cdb47` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
- ……另有 `2` 个 request 见 run record。

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 2：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 3：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 4：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 5：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 6：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:PumpFaultState, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:error_display, variable:error_sound, variable:target_bp, ... +36`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3712`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sd4-0-95304766fc` | `accept` | ❌ | ❌ | Accepted. The CA_backManual warning is valid for Ask_StartAC because a local leaf-scoped CA_backManual event shadows the broader Mode_Control_Algorithm CA_backManual event. The smallest coherent repair is to make the backManual fallbacks consistently use the shared parent-scope event with chain `:` triggers on the concrete source leaves.；intent=Use shared ch...<truncated 113 chars> |
| `fixreq-2-sd4-1-efd1458b11` | `accept` | ❌ | ❌ | Accepted. The CA_backManual warning is valid for AutocontrolInit for the same shadowing reason. The repair uses the parent-scope CA_backManual event on the AutocontrolInit forced fallback instead of a separate local event.；intent=Use shared chain-scope CA_backManual event for AutocontrolInit fallback, Preserve software-control release through Manual.enter |
| `fixreq-2-sd4-2-6ae2848916` | `accept` | ❌ | ❌ | Accepted. The CA_backManual warning is valid for PumpFaultState. The repair keeps PumpFaultState recovery to Manual but binds it to the shared parent-scope CA_backManual event, avoiding a local shadow.；intent=Use shared chain-scope CA_backManual event for PumpFaultState fallback, Preserve active pump-fault alarm behavior until RemoveFault |
| `fixreq-2-sd4-3-83125227a5` | `accept` | ❌ | ❌ | Accepted. The CB_backManual warning is valid for Ask_StartAC. The repair uses one shared parent-scope CB_backManual event across the concrete source leaves rather than distinct local events.；intent=Use shared chain-scope CB_backManual event for Ask_StartAC fallback |
| `fixreq-2-sd4-4-cd6f6c8be0` | `accept` | ❌ | ❌ | Accepted. The CB_backManual warning is valid for AutocontrolInit. The repair keeps the fallback behavior but changes the trigger scope to the shared Mode_Control_Algorithm event.；intent=Use shared chain-scope CB_backManual event for AutocontrolInit fallback |
| `fixreq-2-sd4-5-3608c61314` | `accept` | ❌ | ❌ | Accepted. The CB_backManual warning is valid for PumpFaultState. The repair keeps the same recovery target and uses the shared parent-scope event to remove shadowing.；intent=Use shared chain-scope CB_backManual event for PumpFaultState fallback |
| `fixreq-2-sd4-6-f2bbd0ea7d` | `accept` | ❌ | ❌ | Accepted. The CC_backManual warning is valid for Ask_StartAC. The repair makes the fallback trigger consistently reference the parent-scope CC_backManual event.；intent=Use shared chain-scope CC_backManual event for Ask_StartAC fallback |
| `fixreq-2-sd4-7-5ee7fcda61` | `accept` | ❌ | ❌ | Accepted. The CC_backManual warning is valid for AutocontrolInit. The repair changes only the event scope, preserving the required Manual fallback behavior.；intent=Use shared chain-scope CC_backManual event for AutocontrolInit fallback |
| `fixreq-2-sd4-8-6a083b52a5` | `accept` | ❌ | ❌ | Accepted. The CC_backManual warning is valid for PumpFaultState. The repair keeps Manual as the recovery target and avoids local event shadowing by using the shared parent event.；intent=Use shared chain-scope CC_backManual event for PumpFaultState fallback |
| `fixreq-2-sd4-9-1f255cdb47` | `accept` | ❌ | ❌ | Accepted. The CP_backManual warning is valid for Ask_StartAC. The repair uses the shared parent-scope CP_backManual event on the concrete source fallback.；intent=Use shared chain-scope CP_backManual event for Ask_StartAC fallback |
| `fixreq-2-sd4-10-50ccde383c` | `accept` | ❌ | ❌ | Accepted. The CP_backManual warning is valid for AutocontrolInit. The repair preserves the required shared Manual recovery target while changing the trigger from local shadowing to parent-scope.；intent=Use shared chain-scope CP_backManual event for AutocontrolInit fallback |
| `fixreq-2-sd4-11-5b480d7d9c` | `accept` | ❌ | ❌ | Accepted. The CP_backManual warning is valid for PumpFaultState. The repair keeps the PumpFaultState-to-Manual fallback and binds it to the shared parent-scope CP_backManual event.；intent=Use shared chain-scope CP_backManual event for PumpFaultState fallback |
- repair_rationale：The selected SD-4 design target is W_SHADOWED_EVENT for CA_backManual, CB_backManual, CP_backManual, and CC_backManual. The current model had both broader Mode_Control_Algorithm backManual events and leaf-local events with the same names, p...<truncated 71 chars>；The repair makes the cross-component fallback events consistently parent-scope chain events: `! Ask_StartAC -> Manual : CA_backManual;` and analogous transitions for all required source leaves and all four backManual triggers. This matches ...<truncated 153 chars>；The earlier FixLog local objections about `cp_backmanual_forced_from_pump_fault` expecting alarms off while pump_fault remains active were already overridden by SL-10 and remain audit-only. This candidate preserves the accepted Manual.enter...<truncated 215 chars>；Required grounded elements are preserved: Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, PumpFaultState, all listed variables, root and mode initial transitions, InitiateAC, ChangeSetpoint with `target_bp = requested_target_b...<truncated 94 chars>；The edit also reduces the duplicated forced fallback representation from a wildcard-plus-local-alias pattern to concrete shared-event fallbacks, avoiding the count drift caused by duplicate aliases while retaining the same meaningful Manual...<truncated 57 chars>
- diff_summary：`{"summary": "Removed the shadowing wildcard/local backManual trigger pattern and represented all CA_backManual, CB_backManual, CP_backManual, and CC_backManual fallbacks as chain-scope forced transitions from Ask_StartAC, AutocontrolInit, and PumpFaultState to Manual. Preserved Manual alarm conditional, RemoveFault clearing path, all required states, variables, initial transitions, setpoint change, StartAC, TerminateAC, PumpFault, and autocontrol logic."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_display = 0;
def int error_sound = 0;
def int infusion_log_records = 0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_buffer_bp = 100.0;
def float patient_bp = 100.0;
def float default_flow_rate = 1.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Ask_StartAC -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! PumpFaultState -> Manual : CA_backManual;
        ! PumpFaultState -> Manual : CB_backManual;
        ! PumpFaultState -> Manual : CP_backManual;
        ! PumpFaultState -> Manual : CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_voltage = 0.0;
                if [pump_fault == 0] {
                    alarm_signal = 0;
                    error_display = 0;
                    error_sound = 0;
                } else {
                    alarm_signal = 1;
                    error_display = 1;
                    error_sound = 1;
                }
            }
            during {
                patient_bp = shared_buffer_bp;
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                patient_bp = shared_buffer_bp;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                patient_bp = shared_buffer_bp;
                if [pump_fault == 0] {
                    if [patient_bp > target_bp] {
                        infusion_rate = default_flow_rate - 1.0;
                    } else if [patient_bp < target_bp] {
                        infusion_rate = default_flow_rate + 1.0;
                    } else {
                        infusion_rate = default_flow_rate;
                    }
                    control_voltage = infusion_rate;
                    pump_speed = control_voltage;
                    infusion_log_records = infusion_log_records + 1;
                } else {
                    control_voltage = 0.0;
                    software_control = 0;
                }
            }
        }

        state PumpFaultState {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
                control_voltage = 0.0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> PumpFaultState :: PumpFault;
        PumpFaultState -> Manual :: RemoveFault effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -19,22 +19,18 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
-        ! Ask_StartAC -> Manual :: CA_backManual;
-        ! Ask_StartAC -> Manual :: CB_backManual;
-        ! Ask_StartAC -> Manual :: CP_backManual;
-        ! Ask_StartAC -> Manual :: CC_backManual;
-        ! AutocontrolInit -> Manual :: CA_backManual;
-        ! AutocontrolInit -> Manual :: CB_backManual;
-        ! AutocontrolInit -> Manual :: CP_backManual;
-        ! AutocontrolInit -> Manual :: CC_backManual;
-        ! PumpFaultState -> Manual :: CA_backManual;
-        ! PumpFaultState -> Manual :: CB_backManual;
-        ! PumpFaultState -> Manual :: CP_backManual;
-        ! PumpFaultState -> Manual :: CC_backManual;
+        ! Ask_StartAC -> Manual : CA_backManual;
+        ! Ask_StartAC -> Manual : CB_backManual;
+        ! Ask_StartAC -> Manual : CP_backManual;
+        ! Ask_StartAC -> Manual : CC_backManual;
+        ! AutocontrolInit -> Manual : CA_backManual;
+        ! AutocontrolInit -> Manual : CB_backManual;
+        ! AutocontrolInit -> Manual : CP_backManual;
+        ! AutocontrolInit -> Manual : CC_backManual;
+        ! PumpFaultState -> Manual : CA_backManual;
+        ! PumpFaultState -> Manual : CB_backManual;
+        ! PumpFaultState -> Manual : CP_backManual;
+        ! PumpFaultState -> Manual : CC_backManual;
 
         [*] -> Manual;
 
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:7ad7330e8b6f3f856343a074d1f20f4f0f8dfcb0cfe05653f2ecf8a8710e8095`。
  - SL-10 evidence 1: `{"summary": "The current SD-4 batch targets W_SHADOWED_EVENT diagnostics caused by having both parent-scope backManual events and leaf-local events named CA_backManual, CB_backManual, CP_backManual, and CC_backManual. SL-9 accepted all 12 requests and changed the backManual fallbacks to chain-scope forced transitions from Ask_StartAC, AutocontrolInit, and PumpFaultState to Manual using `:` triggers. This directly addresses the shadowing source while preserving the NL-required shared Manual recovery target."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves the required Mode_Control_Algorithm hierarchy and all NL-required mode states: Manual, Ask_StartAC, AutocontrolInit, and PumpFaultState. It also preserves CA_mode, software_control, pump_fault, alarm_signal, error_display, error_sound, target_bp, requested_target_bp, shared_buffer_bp, patient_bp, default_flow_rate, infusion_rate, control_voltage, pump_speed, manual_switch_speed, and infusion_log_records."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves the caregiver and control-flow obligations: initial root and mode dispatch still enter Manual; InitiateAC enters Ask_StartAC; ChangeSetpoint updates `target_bp = requested_target_bp`; StartAC enters AutocontrolInit; TerminateAC returns to Manual; PumpFault enters PumpFaultState; and RemoveFault clears pump_fault before returning to Manual."}`
  - SL-10 evidence 4: `{"summary": "The candidate preserves the prior SL-10 accepted active-fault behavior: Manual.enter clears alarm/error outputs only when `pump_fault == 0`, and keeps alarm_signal, error_display, and error_sound asserted when `pump_fault == 1`. This remains aligned with the NL statement that pump faults activate alarm signals and that caregiver fault removal is represented by RemoveFault, not by a backManual fallback."}`
  - SL-10 evidence 5: `{"summary": "The candidate preserves autocontrol behavior required by the NL: AutocontrolInit reads patient_bp from shared_buffer_bp, adjusts infusion_rate inversely to blood pressure relative to target_bp while `pump_fault == 0`, drives control_voltage and pump_speed from the computed infusion_rate, records infusion_log_records, and releases software_control when a pump fault is present."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:b7a0368ce4e1d2c0819a8cdbfbe0de1f7d3708ffcdcb0e3e8a92ffd94faabbdd", "covered_local_objection_kinds": ["scenario_regression", "count_drift", "forced_transition_count_drift", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:006b4e468c275b4a4acec0854c6be991c33803c35fde64fe2648187e56e26c5b", "local_override_rationale_count": 6, "local_override_rationale_hash": "sha256:b03f213848e4f42247e8ac2fde2f21e4f2a35ad98bda29f81a12e2f9c77745ba", "local_rejection_evidence_hash": "sha256:672affe8a9088aa33aeff3d55419f696fc0f52e34997b324b7198302d0d2442e", "local_rejection_reason": "scenario_regression; count_drift; forc...<truncated 432 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; count_drift; forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 11, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init probe: CARA dispatches into Manual mode and manual operation uses the built-in switch speed and caregiver default flow.", "name": "default_init_manual_mode_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_signal"...<truncated 12621 chars>
    - local evidence 2: `count_drift` {"direction": "decrease", "drift_ratio": -0.4444, "field": "n_transitions", "fix_target": "design", "kind": "count_drift", "new": 20, "old": 36, "reduction_ratio": 0.4444}
    - local evidence 3: `forced_transition_count_drift` {"fix_target": "design", "kind": "forced_transition_count_drift", "new": 12, "old": 28}
    - local evidence 4: `missing_required_grounding` {"element_ids": ["transition:InitialRoot", "transition:InitialModeControlManual", "action:SetTargetBP", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "guard:NoPumpFaultAutocontrol"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `3` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`local_ca_backmanual_forced_line_missing_probe, local_cb_cp_cc_backmanual_forced_lines_missing_probe, additional_forced_missing_lines_from_distinct_leaves`。
- before_dsl_hash：`sha256:b7a0368ce4e1d2c0819a8cdbfbe0de1f7d3708ffcdcb0e3e8a92ffd94faabbdd`；candidate_dsl_hash：`sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-e09a65494c8`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`3`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sd6-0-ce14b8b59b` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: CA_backManual local fallback from AutocontrolInit must force Manual; if the forced declaration is missing the event is ignored and this fails.', 'name': 'local_ca_backmanual_forced_line_missing_probe', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: CA_backManual local fallback from AutocontrolInit must force Manual; if the forced declaration is missing the event is ignored and this fails.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'control_voltage': 9.0, 'error_display': 0, 'error_sound': 0, 'infusion_rate': 1.0, 'patient_bp': 100.0, 'pump_speed': 0.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'control_voltage': 0.0, 'error_display': 0, 'error_sound': 0, 'infusion_rate': 3.1, 'patient_bp': 104.0, 'pump_speed': 2.1, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CA_backManual'", 'runtime_error_hint': {'event_path': 'CA_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'local_ca_backmanual_forces_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'control_voltage': 9.0, 'default_flow_rate': 3.1, 'manual_switch_speed': 2.1, 'pump_fault': 0, 'shared_buffer_bp': 104.0, 'software_control': 1}, 'scenario_name': 'local_ca_backmanual_forced_line_missing_probe', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_voltage': 9.0, 'default_flow_rate': 3.1, 'error_display': 0, 'error_sound': 0, 'infusion_log_records': 0, 'infusion_rate': 1.0, 'manual_switch_speed': 2.1, 'patient_bp': 100.0, 'pump_fault': 0, 'pump_speed': 0.0, 'requested_target_bp': 100.0, 'shared_buffer_bp': 104.0, 'software_control': 1, 'target_bp': 100.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CA_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'local_ca_backmanual_forces_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-3-sd6-1-7f4ab9c00c` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: local CB_backManual, CP_backManual, and CC_backManual events must each use their forced declarations to return concrete leaves to Manual.', 'name': 'local_cb_cp_cc_backmanual_forced_lines_missing_probe', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: local CB_backManual, CP_backManual, and CC_backManual events must each use their forced declarations to return concrete leaves to Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'control_voltage': 6.0, 'infusion_rate': 1.0, 'patient_bp': 100.0, 'pump_speed': 0.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_voltage': 0.0, 'infusion_rate': 3.3, 'patient_bp': 103.0, 'pump_speed': 2.3, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CB_backManual'", 'runtime_error_hint': {'event_path': 'CB_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'local_cb_backmanual_forces_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'control_voltage': 6.0, 'default_flow_rate': 3.3, 'manual_switch_speed': 2.3, 'pump_fault': 0, 'requested_target_bp': 100.0, 'shared_buffer_bp': 103.0, 'software_control': 1, 'target_bp': 100.0}, 'scenario_name': 'local_cb_cp_cc_backmanual_forced_lines_missing_probe', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_voltage': 6.0, 'default_flow_rate': 3.3, 'error_display': 0, 'error_sound': 0, 'infusion_log_records': 0, 'infusion_rate': 1.0, 'manual_switch_speed': 2.3, 'patient_bp': 100.0, 'pump_fault': 0, 'pump_speed': 0.0, 'requested_target_bp': 100.0, 'shared_buffer_bp': 103.0, 'software_control': 1, 'target_bp': 100.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CB_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'local_cb_backmanual_forces_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-3-sd6-2-142725b5f3` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: additional local backManual forced declarations from Ask_StartAC, AutocontrolInit, and PumpFaultState must not be ignored if any forced line is missing.', 'name': 'additional_forced_missing_lines_from_distinct_leaves', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probe: additional local backManual forced declarations from Ask_StartAC, AutocontrolInit, and PumpFaultState must not be ignored if any forced line is missing.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 1, 'control_voltage': 0.0, 'infusion_rate': 1.0, 'patient_bp': 100.0, 'pump_speed': 0.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_voltage': 0.0, 'infusion_rate': 3.4, 'patient_bp': 96.0, 'pump_speed': 2.4, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC' while resolving event reference 'CB_backManual'", 'runtime_error_hint': {'event_path': 'CB_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cb_backmanual_from_ask_startac_forces_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'default_flow_rate': 3.4, 'infusion_log_records': 0, 'manual_switch_speed': 2.4, 'pump_fault': 0, 'requested_target_bp': 100.0, 'shared_buffer_bp': 96.0, 'software_control': 1, 'target_bp': 100.0}, 'scenario_name': 'additional_forced_missing_lines_from_distinct_leaves', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_voltage': 0.0, 'default_flow_rate': 3.4, 'error_display': 0, 'error_sound': 0, 'infusion_log_records': 0, 'infusion_rate': 1.0, 'manual_switch_speed': 2.4, 'patient_bp': 100.0, 'pump_fault': 0, 'pump_speed': 0.0, 'requested_target_bp': 100.0, 'shared_buffer_bp': 96.0, 'software_control': 1, 'target_bp': 100.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC' while resolving event reference 'CB_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cb_backmanual_from_ask_startac_forces_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:PumpFaultState, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:error_display, variable:error_sound, variable:target_bp, ... +36`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`4340`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sd6-0-ce14b8b59b` | `accept` | ❌ | ❌ | Accepted. The scenario local_ca_backmanual_forced_line_missing_probe hot-starts in AutocontrolInit and injects unqualified local event CA_backManual. The current chain-scope-only fallback leaves that local event unresolved, so the smallest safe sim repair is to add the corresponding leaf-local forced CA_backManual fallback while preserving the existing paren...<truncated 209 chars> |
| `fixreq-3-sd6-1-7f4ab9c00c` | `accept` | ❌ | ❌ | Accepted. The scenario local_cb_cp_cc_backmanual_forced_lines_missing_probe shows unqualified CB_backManual from hot-start AutocontrolInit cannot resolve, while the NL requires CB/CP/CC backManual recovery to Manual. Add leaf-local forced backManual aliases for the concrete mode leaves without removing the already working shared parent-scope events.；intent=A...<truncated 164 chars> |
| `fixreq-3-sd6-2-142725b5f3` | `accept` | ❌ | ❌ | Accepted. The additional_forced_missing_lines_from_distinct_leaves scenario hot-starts in Ask_StartAC and injects unqualified CB_backManual; the current chain-scope-only representation does not create a local event visible from that leaf. Add the same leaf-local forced backManual fallbacks from Ask_StartAC, AutocontrolInit, and PumpFaultState so concrete-lea...<truncated 223 chars> |
- repair_rationale：For local_ca_backmanual_forced_line_missing_probe, expected state/vars after unqualified CA_backManual from AutocontrolInit are Manual with CA_mode = 0, software_control = 0, control_voltage = 0.0, and Manual.during restoring patient_bp, pu...<truncated 184 chars>；For local_cb_cp_cc_backmanual_forced_lines_missing_probe, expected unqualified CB_backManual from AutocontrolInit to reach Manual with manual pump variables restored; actual behavior was an unresolved local CB_backManual. The added local fo...<truncated 126 chars>；For additional_forced_missing_lines_from_distinct_leaves, expected unqualified CB_backManual from Ask_StartAC to force Manual; actual behavior was an unresolved local event in Ask_StartAC. The added local forced transitions from Ask_StartAC...<truncated 24 chars>；The existing chain-scope backManual transitions are retained so prior full root-qualified or parent-scope scenarios remain supported. This intentionally accepts local event aliases as the minimal sim repair because pyfcstm cannot resolve un...<truncated 66 chars>；The previously waived cp_backmanual_from_pump_fault alarm expectation is not changed: Manual.enter still clears alarms only when pump_fault == 0 and preserves alarm/error outputs while an active pump_fault remains, matching the NL fault-ala...<truncated 23 chars>
- diff_summary：`{"summary": "Added leaf-local forced backManual transitions using `::` from Ask_StartAC, AutocontrolInit, and PumpFaultState to Manual for CA_backManual, CB_backManual, CP_backManual, and CC_backManual. Kept the existing parent-scope chain backManual transitions, all required states/variables/transitions, setpoint update, StartAC path, autocontrol guard/logic, Manual recovery behavior, and active-fault alarm semantics."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_display = 0;
def int error_sound = 0;
def int infusion_log_records = 0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_buffer_bp = 100.0;
def float patient_bp = 100.0;
def float default_flow_rate = 1.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Ask_StartAC -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! PumpFaultState -> Manual : CA_backManual;
        ! PumpFaultState -> Manual : CB_backManual;
        ! PumpFaultState -> Manual : CP_backManual;
        ! PumpFaultState -> Manual : CC_backManual;
        ! Ask_StartAC -> Manual :: CA_backManual;
        ! Ask_StartAC -> Manual :: CB_backManual;
        ! Ask_StartAC -> Manual :: CP_backManual;
        ! Ask_StartAC -> Manual :: CC_backManual;
        ! AutocontrolInit -> Manual :: CA_backManual;
        ! AutocontrolInit -> Manual :: CB_backManual;
        ! AutocontrolInit -> Manual :: CP_backManual;
        ! AutocontrolInit -> Manual :: CC_backManual;
        ! PumpFaultState -> Manual :: CA_backManual;
        ! PumpFaultState -> Manual :: CB_backManual;
        ! PumpFaultState -> Manual :: CP_backManual;
        ! PumpFaultState -> Manual :: CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_voltage = 0.0;
                if [pump_fault == 0] {
                    alarm_signal = 0;
                    error_display = 0;
                    error_sound = 0;
                } else {
                    alarm_signal = 1;
                    error_display = 1;
                    error_sound = 1;
                }
            }
            during {
                patient_bp = shared_buffer_bp;
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                patient_bp = shared_buffer_bp;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                patient_bp = shared_buffer_bp;
                if [pump_fault == 0] {
                    if [patient_bp > target_bp] {
                        infusion_rate = default_flow_rate - 1.0;
                    } else if [patient_bp < target_bp] {
                        infusion_rate = default_flow_rate + 1.0;
                    } else {
                        infusion_rate = default_flow_rate;
                    }
                    control_voltage = infusion_rate;
                    pump_speed = control_voltage;
                    infusion_log_records = infusion_log_records + 1;
                } else {
                    control_voltage = 0.0;
                    software_control = 0;
                }
            }
        }

        state PumpFaultState {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
                control_voltage = 0.0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> PumpFaultState :: PumpFault;
        PumpFaultState -> Manual :: RemoveFault effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -31,6 +31,18 @@
         ! PumpFaultState -> Manual : CB_backManual;
         ! PumpFaultState -> Manual : CP_backManual;
         ! PumpFaultState -> Manual : CC_backManual;
+        ! Ask_StartAC -> Manual :: CA_backManual;
+        ! Ask_StartAC -> Manual :: CB_backManual;
+        ! Ask_StartAC -> Manual :: CP_backManual;
+        ! Ask_StartAC -> Manual :: CC_backManual;
+        ! AutocontrolInit -> Manual :: CA_backManual;
+        ! AutocontrolInit -> Manual :: CB_backManual;
+        ! AutocontrolInit -> Manual :: CP_backManual;
+        ! AutocontrolInit -> Manual :: CC_backManual;
+        ! PumpFaultState -> Manual :: CA_backManual;
+        ! PumpFaultState -> Manual :: CB_backManual;
+        ! PumpFaultState -> Manual :: CP_backManual;
+        ! PumpFaultState -> Manual :: CC_backManual;
 
         [*] -> Manual;
 
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:8cd6b32e6628e4bbd4931d0ddeb3719ed0b32da16f5304be11bcc43896168387`。
  - SL-10 evidence 1: `{"summary": "The NL requires CA_backManual and each of CB_backManual, CP_backManual, and CC_backManual to cause CA_mode to become Manual as the shared cross-component recovery target. The current requests are hard simulation failures where unqualified local CA_backManual/CB_backManual events from AutocontrolInit or Ask_StartAC were unresolved. SL-9 accepted all three requests and the DSL diff adds leaf-local forced `::` backManual transitions from Ask_StartAC, AutocontrolInit, and PumpFaultState to Manual for all four backManual events while preserving the existing parent-scope `:` fallbacks."}`
  - SL-10 evidence 2: `{"summary": "The candidate does not drop NL-required structure or behavior: Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, PumpFaultState, all required variables, initial transitions, InitiateAC, ChangeSetpoint with `target_bp = requested_target_bp`, StartAC, TerminateAC, PumpFault, RemoveFault, the no-pump-fault autocontrol branch, BP-based infusion-rate computation, manual pump-speed/default-flow behavior, software-control release, and active-fault alarms remain represented."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves the previously SL-10 accepted active-fault alarm semantics: Manual.enter clears alarm/error outputs only when `pump_fault == 0`; when a backManual recovery occurs while `pump_fault == 1`, alarms/errors remain asserted until the caregiver RemoveFault path clears the fault. This follows the NL requirement that pump faults activate alarm signals and that the caregiver removes the fault."}`
  - SL-10 evidence 4: `{"summary": "Current local_check_evidence reports no scenario_regression and regression_detected=false. The deterministic rejection is limited to W_SHADOWED_EVENT design warnings, transition-count drift, forced-transition-count drift, and matcher missing_required_grounding. Those are local design/matcher objections to the chosen event-visibility representation, not evidence that the current hard simulation targets remain unresolved or that NL behavior regressed."}`
  - SL-10 evidence 5: `{"candidate_dsl_hash": "sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a", "covered_local_objection_kinds": ["new_blocking_design_diagnostic", "count_drift", "forced_transition_count_drift", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:44395c8ad2983e6071ee6a337b9090163258cd24290017e0ca76391a27af13ee", "local_override_rationale_count": 6, "local_override_rationale_hash": "sha256:4098dab6f11d9e8e964f446057f4cdf208a7142ce7898c21f566e2cf9664bbe4", "local_rejection_evidence_hash": "sha256:13448725dd0f86c2ef068f7fae8bfb9a67e0ca0239675196be5e9f6e9927068d", "local_rejection_reason": "new_blocking_design_diagnos...<truncated 454 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; count_drift; forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 1, "code": "W_SHADOWED_EVENT", "instance_key": "W_SHADOWED_EVENT:9a2adf8046b5", "message": "Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.", "policy_action": "requires_policy_classification", "pyfcstm_severity": "warning", "rationale": "", "refs": {"chain_path": "CARA.Mode_Control_Algorithm.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.Mode_Control_Alg...<truncated 12125 chars>
    - local evidence 2: `count_drift` {"direction": "increase", "drift_ratio": 0.6, "field": "n_transitions", "fix_target": "sim", "kind": "count_drift", "new": 32, "old": 20}
    - local evidence 3: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 24, "old": 12}
    - local evidence 4: `missing_required_grounding` {"element_ids": ["transition:InitialRoot", "transition:InitialModeControlManual", "action:SetTargetBP", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "guard:NoPumpFaultAutocontrol"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 5 / iteration `4` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`False`。
- problem_summary：Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.PumpFaultState.CA_backManual' shadows a chain event named 'CA_backManual'.
- diagnostic ids：`W_SHADOWED_EVENT:9a2adf8046b5, W_SHADOWED_EVENT:c3a3d83d124f, W_SHADOWED_EVENT:f4a31c8cdc03, W_SHADOWED_EVENT:cea5fb9348b6, W_SHADOWED_EVENT:30c3e7e6cb03, W_SHADOWED_EVENT:71bb63ebf102, W_SHADOWED_EVENT:6c8ba1ef669e, W_SHADOWED_EVENT:9c2847ada744, W_SHADOWED_EVENT:51873bd93686, W_SHADOWED_EVENT:649a0af501b4, W_SHADOWED_EVENT:1f8ced956d1d, W_SHADOWED_EVENT:1e80b5845db8, ... +4`。
- before_dsl_hash：`sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a`；candidate_dsl_hash：`sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a`。

#### 错误证据 / diagnostics

- 1. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:9a2adf8046b5` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual"}`
- 2. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:c3a3d83d124f` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual"}`
- 3. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:f4a31c8cdc03` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.PumpFaultState.CA_backManual' shadows a chain event named 'CA_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.Mode_Control_Algorithm.PumpFaultState.CA_backManual"}`
- 4. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:cea5fb9348b6` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CB_backManual' shadows a chain event named 'CB_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CB_backManual", "event_name": "CB_backManual", "local_path": "CARA.Mode_Control_Algorithm.Ask_StartAC.CB_backManual"}`
- 5. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:30c3e7e6cb03` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CB_backManual' shadows a chain event named 'CB_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CB_backManual", "event_name": "CB_backManual", "local_path": "CARA.Mode_Control_Algorithm.AutocontrolInit.CB_backManual"}`
- 6. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:71bb63ebf102` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.PumpFaultState.CB_backManual' shadows a chain event named 'CB_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CB_backManual", "event_name": "CB_backManual", "local_path": "CARA.Mode_Control_Algorithm.PumpFaultState.CB_backManual"}`
- 7. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:6c8ba1ef669e` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CC_backManual' shadows a chain event named 'CC_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CC_backManual", "event_name": "CC_backManual", "local_path": "CARA.Mode_Control_Algorithm.Ask_StartAC.CC_backManual"}`
- 8. `W_SHADOWED_EVENT` `W_SHADOWED_EVENT:9c2847ada744` policy=`requires_policy_classification`：Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CC_backManual' shadows a chain event named 'CC_backManual'.；refs=`{"chain_path": "CARA.Mode_Control_Algorithm.CC_backManual", "event_name": "CC_backManual", "local_path": "CARA.Mode_Control_Algorithm.AutocontrolInit.CC_backManual"}`
- ……另有 `4` 条 evidence 见 run record。

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `CA_mode` | `unknown` | ✅ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `alarm_signal` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `control_voltage` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `default_flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `error_display` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `error_sound` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `infusion_log_records` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `infusion_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `manual_switch_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `patient_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `pump_fault` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `pump_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `requested_target_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `shared_buffer_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `software_control` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `target_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-4-sha256-be748878c43`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`12`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-4-sd4-0-534593cad6` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-4-sd4-1-eaedb0df30` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-4-sd4-2-ff15bc07c1` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-4-sd4-3-0359433d65` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-4-sd4-4-a624245b82` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-4-sd4-5-c4469ede74` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-4-sd4-6-75cbe21c21` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-4-sd4-7-0a1abd2acb` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-4-sd4-8-41300313c6` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
| `fixreq-4-sd4-9-920e9b028f` | `blocking_warning` | ❌ | ✅ | Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.; Local event 'CARA.Mode_Control_Algorithm.AutocontrolInit.CA_backManual' shadows a chain event named 'CA_ba...<truncated 127 chars> | `W_SHADOWED_EVENT` |
- ……另有 `2` 个 request 见 run record。

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 2：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 3：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 4：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 5：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- hint 6：The same event leaf name exists in local and broader scopes, which can make transition triggers easy to misread.；`actions=rename_event, adjust_scope；do_not=Do not rename only one trigger without checking all emitters.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:PumpFaultState, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:error_display, variable:error_sound, variable:target_bp, ... +36`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`4340`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-4-sd4-0-534593cad6` | `accept` | ✅ | ❌ | Accepted as a policy-classification repair rather than a structural DSL edit. The CA_backManual shadow warning for Ask_StartAC is real, but FixLog shows the chain-only structural fix was already tried and caused unresolved-event scenario regressions for unqualified local backManual injections. Keeping both the parent-scope and leaf-local NL-grounded CA_backM...<truncated 226 chars> |
| `fixreq-4-sd4-1-eaedb0df30` | `accept` | ✅ | ❌ | Accepted as a policy-classification repair. The AutocontrolInit CA_backManual local event shadows the parent-scope CA_backManual event, but removing it reopens the prior local_ca_backmanual_forced_line_missing_probe runtime error. The unchanged representation preserves both full parent-qualified and unqualified hot-start event behavior.；intent=Preserve Autoc...<truncated 85 chars> |
| `fixreq-4-sd4-2-ff15bc07c1` | `accept` | ✅ | ❌ | Accepted as a policy-classification repair. The PumpFaultState CA_backManual alias is intentionally retained alongside the parent-scope CA_backManual event so every concrete non-Manual leaf has the same Manual recovery visibility. This avoids oscillating back to the known chain-only candidate that regressed local event resolution.；intent=Preserve PumpFaultSt...<truncated 68 chars> |
| `fixreq-4-sd4-3-0359433d65` | `accept` | ✅ | ❌ | Accepted as a policy-classification repair. The Ask_StartAC CB_backManual warning is the same known local/parent event aliasing pattern. It is retained because the NL names CB_backManual as a cross-component back-to-manual event and prior evidence showed unqualified local injections need leaf-local event paths.；intent=Preserve Ask_StartAC local CB_backManual...<truncated 55 chars> |
| `fixreq-4-sd4-4-a624245b82` | `accept` | ✅ | ❌ | Accepted as a policy-classification repair. The AutocontrolInit CB_backManual shadow is intentional to satisfy both parent-scope cross-component fallback semantics and local hot-start event resolution. Removing either side would regress previously accepted behavior.；intent=Preserve AutocontrolInit local CB_backManual fallback, Preserve parent-scope CB_backMa...<truncated 13 chars> |
| `fixreq-4-sd4-5-c4469ede74` | `accept` | ✅ | ❌ | Accepted as a policy-classification repair. The PumpFaultState CB_backManual alias is retained as one of the concrete leaf fallbacks to Manual. This is consistent with the prior SL-10 accepted representation and avoids losing local event visibility.；intent=Preserve PumpFaultState local CB_backManual fallback, Keep shared Manual recovery behavior |
| `fixreq-4-sd4-6-75cbe21c21` | `accept` | ✅ | ❌ | Accepted as a policy-classification repair. The Ask_StartAC CC_backManual shadow warning is intentionally waived because the duplicated event name represents the same NL-grounded recovery trigger at both parent and leaf visibility scopes.；intent=Preserve Ask_StartAC local CC_backManual fallback, Preserve parent-scope CC_backManual fallback |
| `fixreq-4-sd4-7-0a1abd2acb` | `accept` | ✅ | ❌ | Accepted as a policy-classification repair. The AutocontrolInit CC_backManual local alias must remain to preserve unqualified event injection from the active leaf, while the parent-scope event must remain for full cross-component fallback paths.；intent=Preserve AutocontrolInit local CC_backManual fallback, Preserve parent-scope CC_backManual fallback |
| `fixreq-4-sd4-8-41300313c6` | `accept` | ✅ | ❌ | Accepted as a policy-classification repair. The PumpFaultState CC_backManual warning is the same intentionally retained shadow pattern. Removing it would not be the smallest safe edit because it would reduce local recovery coverage from a required fault-related leaf.；intent=Preserve PumpFaultState local CC_backManual fallback, Keep Manual as recovery target |
| `fixreq-4-sd4-9-920e9b028f` | `accept` | ✅ | ❌ | Accepted as a policy-classification repair. The Ask_StartAC CP_backManual local alias is retained because CP_backManual is explicitly named in the NL as a back-to-manual event and prior repair history shows local aliases are needed for unqualified hot-start scenarios.；intent=Preserve Ask_StartAC local CP_backManual fallback, Preserve parent-scope CP_backManu...<truncated 11 chars> |
| `fixreq-4-sd4-10-07b4e640b8` | `accept` | ✅ | ❌ | Accepted as a policy-classification repair. The AutocontrolInit CP_backManual warning is intentionally waived to preserve the non-regressive candidate that satisfies both local unqualified CP_backManual resolution and parent-scope cross-component fallback semantics.；intent=Preserve AutocontrolInit local CP_backManual fallback, Preserve parent-scope CP_backMa...<truncated 13 chars> |
| `fixreq-4-sd4-11-71abdc85d5` | `accept` | ✅ | ❌ | Accepted as a policy-classification repair. The PumpFaultState CP_backManual alias is retained because PumpFaultState is a required fault state and CP_backManual from this state must recover to Manual without clearing an active pump fault prematurely.；intent=Preserve PumpFaultState local CP_backManual fallback, Preserve active-fault alarm semantics until Rem...<truncated 8 chars> |
- repair_rationale：The current batch repeats the W_SHADOWED_EVENT design objections against the exact representation that iteration 3 added to resolve hard simulation failures. FixLog shows the chain-only candidate removed these warnings but regressed unquali...<truncated 103 chars>；No new evidence shows that the chain-only representation is now safe. The current selected diagnostics are design warnings with waiver_allowed=true, while the prior SL-10 review accepted the current dual-scope representation and reported re...<truncated 24 chars>；The unchanged DSL intentionally keeps parent-scope `:` backManual transitions for cross-component fully qualified events and leaf-local `::` backManual aliases for unqualified local injections from active leaves. This is grounded in the NL ...<truncated 115 chars>；All required preserve elements remain represented: Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, PumpFaultState, all listed variables, initial transitions, InitiateAC, ChangeSetpoint with `target_bp = requested_target_bp`, S...<truncated 49 chars>；Active pump-fault alarm behavior is preserved: Manual clears alarm/error outputs only when `pump_fault == 0`, while RemoveFault is the caregiver fault-removal path that clears the active fault before returning to Manual.
- diff_summary：`{"summary": "No DSL text edit. The W_SHADOWED_EVENT diagnostics are classified as intentional, NL-grounded dual-scope event aliases required to preserve both parent-scope cross-component backManual recovery and previously verified unqualified local event resolution. Returning the unchanged DSL avoids oscillating back to the known chain-only candidate that regressed local backManual scenarios."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_display = 0;
def int error_sound = 0;
def int infusion_log_records = 0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_buffer_bp = 100.0;
def float patient_bp = 100.0;
def float default_flow_rate = 1.0;
def float infusion_rate = 1.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Ask_StartAC -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! PumpFaultState -> Manual : CA_backManual;
        ! PumpFaultState -> Manual : CB_backManual;
        ! PumpFaultState -> Manual : CP_backManual;
        ! PumpFaultState -> Manual : CC_backManual;
        ! Ask_StartAC -> Manual :: CA_backManual;
        ! Ask_StartAC -> Manual :: CB_backManual;
        ! Ask_StartAC -> Manual :: CP_backManual;
        ! Ask_StartAC -> Manual :: CC_backManual;
        ! AutocontrolInit -> Manual :: CA_backManual;
        ! AutocontrolInit -> Manual :: CB_backManual;
        ! AutocontrolInit -> Manual :: CP_backManual;
        ! AutocontrolInit -> Manual :: CC_backManual;
        ! PumpFaultState -> Manual :: CA_backManual;
        ! PumpFaultState -> Manual :: CB_backManual;
        ! PumpFaultState -> Manual :: CP_backManual;
        ! PumpFaultState -> Manual :: CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_voltage = 0.0;
                if [pump_fault == 0] {
                    alarm_signal = 0;
                    error_display = 0;
                    error_sound = 0;
                } else {
                    alarm_signal = 1;
                    error_display = 1;
                    error_sound = 1;
                }
            }
            during {
                patient_bp = shared_buffer_bp;
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                patient_bp = shared_buffer_bp;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                patient_bp = shared_buffer_bp;
                if [pump_fault == 0] {
                    if [patient_bp > target_bp] {
                        infusion_rate = default_flow_rate - 1.0;
                    } else if [patient_bp < target_bp] {
                        infusion_rate = default_flow_rate + 1.0;
                    } else {
                        infusion_rate = default_flow_rate;
                    }
                    control_voltage = infusion_rate;
                    pump_speed = control_voltage;
                    infusion_log_records = infusion_log_records + 1;
                } else {
                    control_voltage = 0.0;
                    software_control = 0;
                }
            }
        }

        state PumpFaultState {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
                control_voltage = 0.0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> PumpFaultState :: PumpFault;
        PumpFaultState -> Manual :: RemoveFault effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

- before 与 candidate 文本完全一致；无 diff。

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:b498bd1babf65136a89f8814c992f1a4d26abe740712e13f7cb3f017d8aeca25`。
  - SL-10 evidence 1: `{"summary": "The current batch contains only waiver-allowed W_SHADOWED_EVENT design warnings for CA_backManual, CB_backManual, CP_backManual, and CC_backManual leaf-local events shadowing parent-scope events. SL-9 accepted all 12 as policy-classification repairs with waivers, not DSL edits, because the complete FixLog shows that removing the leaf-local aliases in iteration 2 resolved the design warning but caused unresolved-event simulation failures for unqualified local backManual injections."}`
  - SL-10 evidence 2: `{"summary": "The candidate DSL is unchanged from the iteration-3 candidate already accepted by SL-10. It preserves both parent-scope `:` backManual forced transitions and leaf-local `::` backManual forced transitions from Ask_StartAC, AutocontrolInit, and PumpFaultState to Manual. This directly supports the NL requirement that CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual as the shared recovery target."}`
  - SL-10 evidence 3: `{"summary": "No NL-required state, variable, event, guard, action, or scenario obligation is dropped. The DSL still contains Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, PumpFaultState, CA_mode, software_control, pump_fault, alarm/error outputs, target_bp/requested_target_bp, shared_buffer_bp/patient_bp, default_flow_rate/infusion_rate/control_voltage/pump_speed/manual_switch_speed, initial Manual dispatch, InitiateAC, ChangeSetpoint with `target_bp = requested_target_bp`, StartAC, TerminateAC, PumpFault, RemoveFault, and the no-pump-fault autocontrol guard."}`
  - SL-10 evidence 4: `{"summary": "The DSL continues to satisfy the fault-alarm NL semantics accepted in prior SL-10 reviews: PumpFaultState asserts pump_fault and alarm/error outputs, software control is released, and Manual only clears alarm/error outputs when pump_fault has been cleared by RemoveFault. This avoids the previously audited non-NL expectation that CP_backManual from PumpFaultState should silence alarms while pump_fault remains active."}`
  - SL-10 evidence 5: `{"summary": "Current local_check_evidence reports regression_detected=false and no scenario_regression. The rejection is limited to design_target_unresolved for the intentional shadow aliases plus matcher missing_required_grounding. Given the FixLog oscillation between chain-only and alias-complete candidates, the unchanged dual-scope candidate is the non-regressive local-only frontier and should proceed to full top-down revalidation."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a", "covered_local_objection_kinds": ["design_target_unresolved", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:520485b8413c7103f893824d94b80bcd89264fd7abb41055728845df7283b2a4", "local_override_rationale_count": 5, "local_override_rationale_hash": "sha256:c39f38bb7c32eb09b4e693f752aef2b8f8b3faff24450acb4fc5f45635f12eae", "local_rejection_evidence_hash": "sha256:19af86f598a724646d0682d64126646ce6028ec863c14c238e23f86a0652967d", "local_rejection_reason": "design_target_unresolved; missing_required_grounding", "missing_local_objection_k...<truncated 350 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`design_target_unresolved; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `design_target_unresolved` {"items": [{"budget_exhausted": true, "budget_remaining": 0, "code": "W_SHADOWED_EVENT", "instance_key": "W_SHADOWED_EVENT:9a2adf8046b5", "message": "Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.", "policy_action": "requires_policy_classification", "pyfcstm_severity": "warning", "rationale": "", "refs": {"chain_path": "CARA.Mode_Control_Algorithm.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.Mode_Control_Algo...<truncated 12107 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:InitialRoot", "transition:InitialModeControlManual", "action:SetTargetBP", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "guard:NoPumpFaultAutocontrol"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-4201eb5f343` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-4201eb5f343` | accept=1, reject=0 | `sl10_review` | `sha256:8a179db549bd24d3ce10980917b5585b4c678d10aaee17283990e155f5963af4` | Accepted the unsafe_recovery request because the evidence identifies a real NL-fidelity gap: backManual recovery should make CA_mode Manual, but it should not imply caregiver fault removal or suppress active pump-fault alarms., Expected for cp_backmanual_forced_from_pump_fault: after CP_backManual from PumpFaultState, state may become Manual and software control is released, but pump_fault remains 1 until RemoveFault and alarm_signal/error_display/error_sound remain 1. Actual previous behavior entered Manual with pump_fault 1 and alarms/errors 0. The repair changes only Manual.enter so active pump faults keep alarms/errors active., The explicit PumpFaultState -> Manual :: RemoveFault effect { pump_fault = 0; } remains the only modeled caregiver fault-removal path. Once RemoveFault clears pump_fault before Manual.enter runs, Manual.enter clears alarms/errors normally., ... +2 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-4201eb5f343` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:8a179db549bd24d3ce10980917b5585b4c678d10aaee17283990e155f5963af4` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +2 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-d61e73186fd` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-d61e73186fd` | accept=2, reject=1 | `sl10_review` | `sha256:e6a8d18daf59578866d1755941aed2570242002296a7deb907b5b0a19fd2b974` | For local_ca_backmanual_forced_line_missing_probe, the expected state after local CA_backManual from AutocontrolInit is Manual with CA_mode = 0, software_control = 0, control_voltage = 0.0, and Manual.during restoring patient_bp, pump_speed, and infusion_rate from shared/manual inputs. The actual result was a runtime unresolved-event error. Adding explicit `! AutocontrolInit -> Manual :: CA_backManual;` makes that local event visible from the hot-start leaf without changing Manual behavior., For local_cb_cp_cc_backmanual_forced_lines_missing_probe, the expected state after local CB_backManual/CP_backManual/CC_backManual from concrete leaves is the shared Manual recovery target. The actual evidence showed unresolved local CB_backManual from AutocontrolInit. The added explicit leaf-scope forced declarations for Ask_StartAC, AutocontrolInit, and PumpFaultState provide local event owners for all four backManual events while preserving the existing wildcard fallback declarations., For cp_backmanual_forced_from_pump_fault, the only mismatch is the stale expectation that alarms/errors clear even though pump_fault remains active. The FixLog and SL-10 override identify that expectation as contrary to the NL fault-alarm requirement, so the candidate intentionally preserves the existing conditional Manual.enter behavior: alarms clear only when pump_fault == 0 and remain active when pump_fault == 1., ... +1 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-d61e73186fd` | accept=2, reject=1 | `sc11_accept_then_sd2` | `sha256:e6a8d18daf59578866d1755941aed2570242002296a7deb907b5b0a19fd2b974` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 7 | `2` | `request_batch` | `fixbatch-2-sha256-be748878c43` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 8 | `2` | `sl9_decision` | `fixbatch-2-sha256-be748878c43` | accept=12, reject=0 | `sl10_review` | `sha256:b7a0368ce4e1d2c0819a8cdbfbe0de1f7d3708ffcdcb0e3e8a92ffd94faabbdd` | The selected SD-4 design target is W_SHADOWED_EVENT for CA_backManual, CB_backManual, CP_backManual, and CC_backManual. The current model had both broader Mode_Control_Algorithm backManual events and leaf-local events with the same names, producing shadowing at Ask_StartAC, AutocontrolInit, and PumpFaultState., The repair makes the cross-component fallback events consistently parent-scope chain events: `! Ask_StartAC -> Manual : CA_backManual;` and analogous transitions for all required source leaves and all four backManual triggers. This matches the NL statement that CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual as a shared recovery target., The earlier FixLog local objections about `cp_backmanual_forced_from_pump_fault` expecting alarms off while pump_fault remains active were already overridden by SL-10 and remain audit-only. This candidate preserves the accepted Manual.enter conditional: alarms and caregiver error indications clear only when `pump_fault == 0`; if a backManual fallback occurs while the pump fault is still active, the model keeps alarms/errors asserted until RemoveFault., ... +2 |
| 9 | `2` | `sl10_review` | `fixbatch-2-sha256-be748878c43` | accept=12, reject=0 | `sc11_accept_then_sd2` | `sha256:b7a0368ce4e1d2c0819a8cdbfbe0de1f7d3708ffcdcb0e3e8a92ffd94faabbdd` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 10 | `3` | `request_batch` | `fixbatch-3-sha256-e09a65494c8` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 11 | `3` | `sl9_decision` | `fixbatch-3-sha256-e09a65494c8` | accept=3, reject=0 | `sl10_review` | `sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a` | For local_ca_backmanual_forced_line_missing_probe, expected state/vars after unqualified CA_backManual from AutocontrolInit are Manual with CA_mode = 0, software_control = 0, control_voltage = 0.0, and Manual.during restoring patient_bp, pump_speed, and infusion_rate. Actual behavior was an unresolved local event in AutocontrolInit. The added `! AutocontrolInit -> Manual :: CA_backManual;` provides that local event path., For local_cb_cp_cc_backmanual_forced_lines_missing_probe, expected unqualified CB_backManual from AutocontrolInit to reach Manual with manual pump variables restored; actual behavior was an unresolved local CB_backManual. The added local forced CB/CP/CC transitions from AutocontrolInit and the other concrete non-Manual leaves provide the required event visibility., For additional_forced_missing_lines_from_distinct_leaves, expected unqualified CB_backManual from Ask_StartAC to force Manual; actual behavior was an unresolved local event in Ask_StartAC. The added local forced transitions from Ask_StartAC resolve this exact gap., ... +2 |
| 12 | `3` | `sl10_review` | `fixbatch-3-sha256-e09a65494c8` | accept=3, reject=0 | `sc11_accept_then_sd2` | `sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 13 | `4` | `request_batch` | `fixbatch-4-sha256-be748878c43` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 14 | `4` | `sl9_decision` | `fixbatch-4-sha256-be748878c43` | accept=12, reject=0 | `sl10_review` | `sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a` | The current batch repeats the W_SHADOWED_EVENT design objections against the exact representation that iteration 3 added to resolve hard simulation failures. FixLog shows the chain-only candidate removed these warnings but regressed unqualified local CA_backManual/CB_backManual event resolution from hot-start AutocontrolInit and Ask_StartAC., No new evidence shows that the chain-only representation is now safe. The current selected diagnostics are design warnings with waiver_allowed=true, while the prior SL-10 review accepted the current dual-scope representation and reported regression_detected=false., The unchanged DSL intentionally keeps parent-scope `:` backManual transitions for cross-component fully qualified events and leaf-local `::` backManual aliases for unqualified local injections from active leaves. This is grounded in the NL requirement that CA_backManual, CB_backManual, CP_backManual, and CC_backManual all cause CA_mode to become Manual., ... +2 |
| 15 | `4` | `sl10_review` | `fixbatch-4-sha256-be748878c43` | accept=12, reject=0 | `sc11_accept_then_sd2` | `sha256:0de838946b2c899d53576ddbba1b0b7d4dec28f63ee1ed649f303660cd0dfd6a` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5332, 'completion_chars': 21201, 'completion_tokens': 7598, 'elapsed_seconds': 139.12134379008785, 'estimated_completion_tokens': 5301, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11958, 'first_chunk_seconds': 42.932872587116435, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14048}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2864, 'completion_chars': 11282, 'completion_tokens': 4739, 'elapsed_seconds': 86.84816090716049, 'estimated_completion_tokens': 2821, 'estimated_prompt_tokens': 15346, 'estimated_total_tokens': 18167, 'first_chunk_seconds': 37.293803580105305, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 61382, 'prompt_tokens': 14964, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 19703}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1898, 'completion_chars': 8855, 'completion_tokens': 2417, 'elapsed_seconds': 49.10829253005795, 'estimated_completion_tokens': 2214, 'estimated_prompt_tokens': 19123, 'estimated_total_tokens': 21337, 'first_chunk_seconds': 15.049715487053618, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 76489, 'prompt_tokens': 19012, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21429}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1384, 'completion_chars': 6184, 'completion_tokens': 1607, 'elapsed_seconds': 31.827325955033302, 'estimated_completion_tokens': 1546, 'estimated_prompt_tokens': 22986, 'estimated_total_tokens': 24532, 'first_chunk_seconds': 6.8487369120121, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 91944, 'prompt_tokens': 21730, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23337}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 914, 'completion_chars': 4426, 'completion_tokens': 1199, 'elapsed_seconds': 24.984580578049645, 'estimated_completion_tokens': 1107, 'estimated_prompt_tokens': 26704, 'estimated_total_tokens': 27811, 'first_chunk_seconds': 8.42775660706684, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 106814, 'prompt_tokens': 23664, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24863}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2176, 'completion_chars': 8419, 'completion_tokens': 2695, 'elapsed_seconds': 50.40669681201689, 'estimated_completion_tokens': 2105, 'estimated_prompt_tokens': 20846, 'estimated_total_tokens': 22951, 'first_chunk_seconds': 12.09208114608191, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 83383, 'prompt_tokens': 20484, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23179}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4014, 'completion_chars': 15849, 'completion_tokens': 4533, 'elapsed_seconds': 84.40763870999217, 'estimated_completion_tokens': 3963, 'estimated_prompt_tokens': 21139, 'estimated_total_tokens': 25102, 'first_chunk_seconds': 12.519035252043977, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 84556, 'prompt_tokens': 20782, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25315}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1984, 'completion_chars': 8849, 'completion_tokens': 4056, 'elapsed_seconds': 76.89806754002348, 'estimated_completion_tokens': 2213, 'estimated_prompt_tokens': 81800, 'estimated_total_tokens': 84013, 'first_chunk_seconds': 41.63452313491143, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 327200, 'prompt_tokens': 67016, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 71072}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1287, 'completion_chars': 6370, 'completion_tokens': 1611, 'elapsed_seconds': 36.63477940694429, 'estimated_completion_tokens': 1593, 'estimated_prompt_tokens': 105138, 'estimated_total_tokens': 106731, 'first_chunk_seconds': 12.996197203872725, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 420551, 'prompt_tokens': 83698, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 85309}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2802, 'completion_chars': 11818, 'completion_tokens': 4356, 'elapsed_seconds': 81.7785921629984, 'estimated_completion_tokens': 2955, 'estimated_prompt_tokens': 112736, 'estimated_total_tokens': 115691, 'first_chunk_seconds': 35.61296288482845, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 450941, 'prompt_tokens': 87367, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 91723}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1154, 'completion_chars': 5568, 'completion_tokens': 1984, 'elapsed_seconds': 41.834560392890126, 'estimated_completion_tokens': 1392, 'estimated_prompt_tokens': 110514, 'estimated_total_tokens': 111906, 'first_chunk_seconds': 20.81472247489728, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 442056, 'prompt_tokens': 85022, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 87006}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6029, 'completion_chars': 23987, 'completion_tokens': 7450, 'elapsed_seconds': 137.1365205401089, 'estimated_completion_tokens': 5997, 'estimated_prompt_tokens': 22945, 'estimated_total_tokens': 28942, 'first_chunk_seconds': 33.030765098985285, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 91780, 'prompt_tokens': 22954, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 30404}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5017, 'completion_chars': 19106, 'completion_tokens': 6054, 'elapsed_seconds': 110.92686955491081, 'estimated_completion_tokens': 4777, 'estimated_prompt_tokens': 24980, 'estimated_total_tokens': 29757, 'first_chunk_seconds': 21.25348277995363, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 99918, 'prompt_tokens': 24969, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 31023}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2049, 'completion_chars': 8897, 'completion_tokens': 2817, 'elapsed_seconds': 53.8161923319567, 'estimated_completion_tokens': 2225, 'estimated_prompt_tokens': 107843, 'estimated_total_tokens': 110068, 'first_chunk_seconds': 17.249617937020957, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 431369, 'prompt_tokens': 82551, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 85368}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1116, 'completion_chars': 5473, 'completion_tokens': 1403, 'elapsed_seconds': 30.17074913904071, 'estimated_completion_tokens': 1369, 'estimated_prompt_tokens': 105033, 'estimated_total_tokens': 106402, 'first_chunk_seconds': 9.151518129045144, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 420129, 'prompt_tokens': 79688, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 81091}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3087, 'completion_chars': 13491, 'completion_tokens': 4121, 'elapsed_seconds': 77.09657124592923, 'estimated_completion_tokens': 3373, 'estimated_prompt_tokens': 104505, 'estimated_total_tokens': 107878, 'first_chunk_seconds': 25.02831034292467, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 418018, 'prompt_tokens': 82867, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 86988}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1076, 'completion_chars': 5196, 'completion_tokens': 1185, 'elapsed_seconds': 24.251766997156665, 'estimated_completion_tokens': 1299, 'estimated_prompt_tokens': 102434, 'estimated_total_tokens': 103733, 'first_chunk_seconds': 5.083896248135716, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 409736, 'prompt_tokens': 80112, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 81297}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`not_converged`，record_status=`budget_exhausted`。
- 主要原因分类：`design_or_variable_dynamics`。
- required stages executed：`61/16`，missing=`<none>`。
- repairs：`5/5` accepted；scenario_history=`7`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
