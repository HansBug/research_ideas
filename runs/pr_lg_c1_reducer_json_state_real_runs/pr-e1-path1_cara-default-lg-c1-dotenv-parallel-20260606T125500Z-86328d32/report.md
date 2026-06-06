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
| Git commit | `372f0e6d9dacfc53c5509e895fd4b38007b575d7` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:7ba3465db7f9cfad6e47d2197f8f36738faf616536ef2db0a58ff045387bd4b1", "iteration": 1, "matching_repair_history_indices": [1], "repair_history_index": 1, "selected_source_stage": "SD-6", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 295953, 'completion_tokens': 32189, 'total_tokens': 328142, 'estimated_prompt_tokens': 329707, 'estimated_completion_tokens': 26008, 'estimated_total_tokens': 355715, 'prompt_chars': 1318813, 'completion_chars': 104013, 'n_calls': 10, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`610.401s` |
| run record | [`pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:2eb71f932e5973e76ce9c7036d0167de4840fe2a086deb261eb7ca6cfc489635` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `57` |
| `langgraph_node_trace_hash` | `sha256:a933c1f1e8c23cdb3567ea93331d2fb98268127b7d9f33bdbbf6ebb3dfa3f66a` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `57` |

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
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float target_blood_pressure = 0.0;
def float requested_target_blood_pressure = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_message_displayed = 0;
def int software_control = 0;
def int log_entry_count = 0;
def int CA_mode = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! * -> Manual :: TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                pump_speed = built_in_switch_speed;
                flow_rate = default_flow_rate;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                    error_message_displayed = 1;
                } else {
                    alarm_signal = 0;
                    error_message_displayed = 0;
                }
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 1;
                software_control = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 2;
                software_control = 1;
                alarm_signal = 0;
                error_message_displayed = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state NormalAutocontrol {
            enter {
                CA_mode = 3;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure < target_blood_pressure] {
                    flow_rate = target_blood_pressure - blood_pressure;
                } else {
                    flow_rate = 0.0;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_entry_count = log_entry_count + 1;
            }
        }

        state PumpFault {
            enter {
                CA_mode = 4;
                software_control = 0;
                alarm_signal = 1;
                error_message_displayed = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_blood_pressure = requested_target_blood_pressure; };
        Ask_StartAC -> AutocontrolInit : StartAC;
        AutocontrolInit -> NormalAutocontrol;
        NormalAutocontrol -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12903 | 生成初始 DSL 与 grounding seeds | initial len=3174 | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=2, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=99663 | LLM per-request accept/reject + repair | candidate len=3227,3222 | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=103365 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=4, tokens=87975 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=4, tokens=87975 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=4, tokens=87975 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ⚠️ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=99663 | LLM per-request accept/reject + repair | candidate len=3227,3222 | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=103365 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=21, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=4, tokens=87975 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=1, tokens=24236 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-c1-dotenv-parallel-20260606T125500Z-86328d32.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T04:34:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T04:34:53Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T04:34:53Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T04:34:53Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T04:36:52Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T04:36:52Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=3174,hash=sha256:a4bfb2414c52 |
| 7 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T04:36:52Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:a4bfb2414c52c9d8ae8d62b1e0d11ad7cec3fe3824994940663a98a6b9f43bf9 |
| 10 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T04:36:52Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=3174,hash=sha256:a4bfb2414c52, current_hash=sha256:a4bfb2414c52c9d8ae8d62b1e0d11ad7cec3fe3824994940663a98a6b9f43bf9 |
| 12 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T04:36:52Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T04:36:52Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T04:36:52Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T04:36:52Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T04:36:52Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T04:36:52Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 21 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T04:36:52Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=pump_fault", "W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.NormalAutocontrol:to_path=CARA.Mode_Control_Algorithm.PumpFault"], "diagnostic_codes": ["W_UNWRITTEN_READ_VAR", "W_GUARD_VARS_NEVER_CHANGE", "W_HIGH_VAR_TO_LEAF_RATIO", "W_UNREFERENCED_VAR", "W_UNREFERENCED_VAR", "W_UNRE...<truncated 1024 chars> | <none> |
| 23 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 24 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 26 | `2026-06-06T04:36:52Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=pump_fault", "W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.NormalAutocontrol:to_path=CARA.Mode_Control_Algorithm.PumpFault"], "diagnostic_codes": ["W_UNWRITTEN_READ_VAR", "W_GUARD_VARS_NEVER_CHANGE", "W_HIGH_VAR_TO_LEAF_RATIO", "W_UNREFERENCED_VAR", "W_UNREFERENCED_VAR", "W_UNREFERENCE...<truncated 5443 chars> | current_dsl:len=3174,hash=sha256:a4bfb2414c52 |
| 27 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 28 | `2026-06-06T04:36:52Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-06T04:36:52Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 2} | <none> |
| 30 | `2026-06-06T04:36:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 31 | `2026-06-06T04:36:52Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=3174,hash=sha256:a4bfb2414c52 |
| 32 | `2026-06-06T04:37:28Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-06T04:37:28Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-6e7fd24414", "fixreq-0-sd4-1-b901baec1e"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=3227,hash=sha256:a8ac09db1c32 |
| 34 | `2026-06-06T04:37:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-06T04:37:28Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 36 | `2026-06-06T04:37:28Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564 |
| 37 | `2026-06-06T04:37:45Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 38 | `2026-06-06T04:37:45Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 39 | `2026-06-06T04:37:45Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 40 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-06T04:37:45Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=3227,hash=sha256:a8ac09db1c32 |
| 42 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-06T04:37:45Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564 |
| 44 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 47 | `2026-06-06T04:37:45Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564 |
| 48 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 49 | `2026-06-06T04:37:45Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=3227,hash=sha256:a8ac09db1c32, current_hash=sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564 |
| 50 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 51 | `2026-06-06T04:37:45Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 52 | `2026-06-06T04:37:45Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 53 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 54 | `2026-06-06T04:37:45Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 55 | `2026-06-06T04:37:45Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 56 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 57 | `2026-06-06T04:37:45Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 58 | `2026-06-06T04:37:45Z` | `SD-4` | `1` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 59 | `2026-06-06T04:37:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 60 | `2026-06-06T04:37:45Z` | `SL-5` | `1` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 61 | `2026-06-06T04:39:04Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 62 | `2026-06-06T04:39:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 63 | `2026-06-06T04:39:04Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 64 | `2026-06-06T04:39:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 65 | `2026-06-06T04:39:04Z` | `SL-5` | `1` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 66 | `2026-06-06T04:40:13Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 67 | `2026-06-06T04:40:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 68 | `2026-06-06T04:40:13Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 69 | `2026-06-06T04:40:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 70 | `2026-06-06T04:40:13Z` | `SL-5` | `1` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 71 | `2026-06-06T04:41:32Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 72 | `2026-06-06T04:41:32Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 73 | `2026-06-06T04:41:32Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 74 | `2026-06-06T04:41:32Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 75 | `2026-06-06T04:41:32Z` | `<control>` | `1` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 76 | `2026-06-06T04:41:32Z` | `SC-5F` | `1` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 77 | `2026-06-06T04:41:32Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 78 | `2026-06-06T04:41:32Z` | `SD-6` | `1` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 79 | `2026-06-06T04:41:32Z` | `SD-6` | `1` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 80 | `2026-06-06T04:41:32Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
- ……另有 `67` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-4` | yes | fixbatch-0-sha256-2c1837fbac1 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-6` | yes | fixbatch-1-sha256-00f2a6e9827 / n=7 | accept=7, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 2 | Iter 3 |
|---|---|---|---|
| `default_init_manual_outputs` | default-init: first cycle dispatches to Manual and verifies manual pump speed, default flow, and sensor-buffer behavior. | ✅ | ✅ |
| `initiate_change_start_to_normal_autocontrol` | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, then automatic init reaches Norm...<truncated 14 chars> | ⚪ | ✅ |
| `normal_pump_fault_and_fault_removed_recovery` | explicit-hot-start: PumpFaultDetected during NormalAutocontrol activates alarms and releases software control; FaultRemo...<truncated 22 chars> | ⚪ | ✅ |
| `terminate_ac_forces_manual_from_normal` | explicit-hot-start: TerminateAC from NormalAutocontrol forces the shared Manual recovery target and releases software co...<truncated 6 chars> | ✅ | ✅ |
| `ca_backmanual_forces_manual_from_ask` | explicit-hot-start: CA_backManual from Ask_StartAC forces Manual and makes CA_mode Manual. | ✅ | ✅ |
| `cb_backmanual_forces_manual_from_autocontrol_init` | explicit-hot-start: CB_backManual from AutocontrolInit forces the shared Manual recovery target. | ✅ | ✅ |
| `cp_backmanual_forces_manual_from_pump_fault` | explicit-hot-start: CP_backManual from PumpFault forces Manual while an unresolved pump fault still keeps alarms active. | ✅ | ✅ |
| `normal_autocontrol_high_pressure_then_cc_backmanual` | explicit-hot-start: NormalAutocontrol computes lower flow at higher pressure, logs data, then CC_backManual forces Manua...<truncated 2 chars> | ✅ | ✅ |
| `change_setpoint_effect_is_exact` | explicit-hot-start: ChangeSetpoint in Ask_StartAC must remain in Ask_StartAC and copy the requested setpoint exactly, ca...<truncated 55 chars> | ⚪ | ✅ |
| `pump_fault_detected_effect_is_exact` | explicit-hot-start: PumpFaultDetected from NormalAutocontrol must enter PumpFault and set pump_fault exactly to active w...<truncated 42 chars> | ⚪ | ✅ |
| `fault_removed_effect_is_exact_manual_recovery` | explicit-hot-start: FaultRemoved from PumpFault must target Manual and clear pump_fault exactly to zero while restoring ...<truncated 20 chars> | ⚪ | ✅ |
| `initiate_ac_target_and_entry_effects` | explicit-hot-start: InitiateAC from Manual must target Ask_StartAC exactly and apply Ask_StartAC entry obligations witho...<truncated 29 chars> | ⚪ | ✅ |
| `startac_target_and_autocontrolinit_entry_effects` | explicit-hot-start: StartAC from Ask_StartAC must target AutocontrolInit exactly and set software control while clearing...<truncated 18 chars> | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_outputs` — default-init: first cycle dispatches to Manual and verifies manual pump speed, default flow, and sensor-buffer behavior.</summary>

| Field | Value |
|---|---|
| description | default-init: first cycle dispatches to Manual and verifies manual pump speed, default flow, and sensor-buffer behavior. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 82.0, "built_in_switch_speed": 3.5, "default_flow_rate": 6.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_after_initial_dispatch` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "error_message_displayed": 0, "flow_rate": 6.0, "pump_speed": 3.5, "sensor_buffer_bp": 82.0, "software_control": 0}` |

</details>

<details><summary>`initiate_change_start_to_normal_autocontrol` — default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, then automatic init reaches NormalAutocontrol.</summary>

| Field | Value |
|---|---|
| description | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, then automatic init reaches NormalAutocontrol. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 90.0, "requested_target_blood_pressure": 110.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "sensor_buffer_bp": 90.0, "software_control": 0}` |
| 1 `initiate_enters_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "sensor_buffer_bp": 90.0, "software_control": 0}` |
| 2 `change_setpoint_stays_in_ask` | `0` | `["CARA.Mode_Control_Algorithm.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "sensor_buffer_bp": 90.0, "software_control": 0, "target_blood_pressure": 110.0}` |
| 3 `startac_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 2, "alarm_signal": 0, "error_message_displayed": 0, "sensor_buffer_bp": 90.0, "software_control": 1}` |
| 4 `autocontrol_init_advances_to_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.NormalAutocontrol` | `{"CA_mode": 3, "control_voltage": 20.0, "flow_rate": 20.0, "log_entry_count": 1, "pump_speed": 20.0, "sensor_buffer_bp": 90.0, "software_control": 1}` |

</details>

<details><summary>`normal_pump_fault_and_fault_removed_recovery` — explicit-hot-start: PumpFaultDetected during NormalAutocontrol activates alarms and releases software control; FaultRemoved returns to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: PumpFaultDetected during NormalAutocontrol activates alarms and releases software control; FaultRemoved returns to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.NormalAutocontrol` |
| initial_vars | `{"blood_pressure": 100.0, "built_in_switch_speed": 2.0, "default_flow_rate": 5.0, "software_control": 1, "target_blood_pressure": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_detected_enters_pump_fault` | `0` | `["CARA.Mode_Control_Algorithm.PumpFaultDetected"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 4, "alarm_signal": 1, "error_message_displayed": 1, "pump_fault": 1, "sensor_buffer_bp": 100.0, "software_control": 0}` |
| 1 `fault_removed_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "error_message_displayed": 0, "flow_rate": 5.0, "pump_fault": 0, "pump_speed": 2.0, "sensor_buffer_bp": 100.0, "software_control": 0}` |

</details>

<details><summary>`terminate_ac_forces_manual_from_normal` — explicit-hot-start: TerminateAC from NormalAutocontrol forces the shared Manual recovery target and releases software control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: TerminateAC from NormalAutocontrol forces the shared Manual recovery target and releases software control. |
| initial_state | `CARA.Mode_Control_Algorithm.NormalAutocontrol` |
| initial_vars | `{"blood_pressure": 70.0, "built_in_switch_speed": 4.0, "default_flow_rate": 8.0, "software_control": 1, "target_blood_pressure": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 8.0, "pump_speed": 4.0, "sensor_buffer_bp": 70.0, "software_control": 0}` |

</details>

<details><summary>`ca_backmanual_forces_manual_from_ask` — explicit-hot-start: CA_backManual from Ask_StartAC forces Manual and makes CA_mode Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CA_backManual from Ask_StartAC forces Manual and makes CA_mode Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"blood_pressure": 75.0, "built_in_switch_speed": 1.5, "default_flow_rate": 4.5}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_manual_target` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 4.5, "pump_speed": 1.5, "sensor_buffer_bp": 75.0, "software_control": 0}` |

</details>

<details><summary>`cb_backmanual_forces_manual_from_autocontrol_init` — explicit-hot-start: CB_backManual from AutocontrolInit forces the shared Manual recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CB_backManual from AutocontrolInit forces the shared Manual recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"blood_pressure": 88.0, "built_in_switch_speed": 2.5, "default_flow_rate": 7.5, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_manual_target` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 7.5, "pump_speed": 2.5, "sensor_buffer_bp": 88.0, "software_control": 0}` |

</details>

<details><summary>`cp_backmanual_forces_manual_from_pump_fault` — explicit-hot-start: CP_backManual from PumpFault forces Manual while an unresolved pump fault still keeps alarms active.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CP_backManual from PumpFault forces Manual while an unresolved pump fault still keeps alarms active. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"alarm_signal": 1, "blood_pressure": 92.0, "built_in_switch_speed": 3.0, "default_flow_rate": 6.5, "error_message_displayed": 1, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_manual_target` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 1, "error_message_displayed": 1, "flow_rate": 6.5, "pump_speed": 3.0, "sensor_buffer_bp": 92.0, "software_control": 0}` |

</details>

<details><summary>`normal_autocontrol_high_pressure_then_cc_backmanual` — explicit-hot-start: NormalAutocontrol computes lower flow at higher pressure, logs data, then CC_backManual forces Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: NormalAutocontrol computes lower flow at higher pressure, logs data, then CC_backManual forces Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.NormalAutocontrol` |
| initial_vars | `{"blood_pressure": 95.0, "built_in_switch_speed": 5.0, "default_flow_rate": 9.0, "log_entry_count": 0, "software_control": 1, "target_blood_pressure": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `normal_high_pressure_low_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.NormalAutocontrol` | `{"control_voltage": 5.0, "flow_rate": 5.0, "log_entry_count": 1, "pump_speed": 5.0, "sensor_buffer_bp": 95.0}` |
| 1 `cc_backmanual_manual_target` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 9.0, "pump_speed": 5.0, "sensor_buffer_bp": 95.0, "software_control": 0}` |

</details>

<details><summary>`change_setpoint_effect_is_exact` — explicit-hot-start: ChangeSetpoint in Ask_StartAC must remain in Ask_StartAC and copy the requested setpoint exactly, catching wrong-target and missing/wrong-ef...<truncated 15 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: ChangeSetpoint in Ask_StartAC must remain in Ask_StartAC and copy the requested setpoint exactly, catching wrong-target and missing/wrong-effect mutations. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"blood_pressure": 77.0, "requested_target_blood_pressure": 115.0, "target_blood_pressure": 80.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `change_setpoint_exact_copy` | `0` | `["CARA.Mode_Control_Algorithm.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "sensor_buffer_bp": 77.0, "software_control": 0, "target_blood_pressure": 115.0}` |

</details>

<details><summary>`pump_fault_detected_effect_is_exact` — explicit-hot-start: PumpFaultDetected from NormalAutocontrol must enter PumpFault and set pump_fault exactly to active while releasing control and raising alarm...<truncated 2 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: PumpFaultDetected from NormalAutocontrol must enter PumpFault and set pump_fault exactly to active while releasing control and raising alarms. |
| initial_state | `CARA.Mode_Control_Algorithm.NormalAutocontrol` |
| initial_vars | `{"alarm_signal": 0, "blood_pressure": 101.0, "error_message_displayed": 0, "pump_fault": 0, "software_control": 1, "target_blood_pressure": 130.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `pump_fault_detected_exact_effect` | `0` | `["CARA.Mode_Control_Algorithm.PumpFaultDetected"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 4, "alarm_signal": 1, "error_message_displayed": 1, "pump_fault": 1, "sensor_buffer_bp": 101.0, "software_control": 0}` |

</details>

<details><summary>`fault_removed_effect_is_exact_manual_recovery` — explicit-hot-start: FaultRemoved from PumpFault must target Manual and clear pump_fault exactly to zero while restoring manual pump outputs.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: FaultRemoved from PumpFault must target Manual and clear pump_fault exactly to zero while restoring manual pump outputs. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"alarm_signal": 1, "blood_pressure": 83.0, "built_in_switch_speed": 2.2, "default_flow_rate": 5.5, "error_message_displayed": 1, "pump_fault": 1, "software_control": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_removed_exact_clear_and_manual` | `0` | `["CARA.Mode_Control_Algorithm.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "error_message_displayed": 0, "flow_rate": 5.5, "pump_fault": 0, "pump_speed": 2.2, "sensor_buffer_bp": 83.0, "software_control": 0}` |

</details>

<details><summary>`initiate_ac_target_and_entry_effects` — explicit-hot-start: InitiateAC from Manual must target Ask_StartAC exactly and apply Ask_StartAC entry obligations without starting software control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: InitiateAC from Manual must target Ask_StartAC exactly and apply Ask_StartAC entry obligations without starting software control. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"CA_mode": 0, "blood_pressure": 86.0, "built_in_switch_speed": 2.8, "default_flow_rate": 6.8, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiate_ac_exact_ask_target` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "sensor_buffer_bp": 86.0, "software_control": 0}` |

</details>

<details><summary>`startac_target_and_autocontrolinit_entry_effects` — explicit-hot-start: StartAC from Ask_StartAC must target AutocontrolInit exactly and set software control while clearing alarm indicators.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: StartAC from Ask_StartAC must target AutocontrolInit exactly and set software control while clearing alarm indicators. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"alarm_signal": 1, "blood_pressure": 91.0, "error_message_displayed": 1, "software_control": 0, "target_blood_pressure": 115.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `startac_exact_init_target_and_effects` | `0` | `["CARA.Mode_Control_Algorithm.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 2, "alarm_signal": 0, "error_message_displayed": 0, "sensor_buffer_bp": 91.0, "software_control": 1}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=pump_fault, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.NormalAutocontrol:to_path=CARA.Mode_Control_Algorithm.PumpFault, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, ... +3 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564` |
| 2 | `1` | ✅ | `SD-6` | initiate_change_start_to_normal_autocontrol, normal_pump_fault_and_fault_removed_recovery, change_setpoint_effect_is_exact, pump_fault_detected_effect_is_exact, fault_removed_effect_is_exact_manual_recovery, ... +2 | accept=7, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:7ba3465db7f9cfad6e47d2197f8f36738faf616536ef2db0a58ff045387bd4b1` |

<details><summary>Repair 1 / iteration `0` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'pump_fault' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=pump_fault, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.NormalAutocontrol:to_path=CARA.Mode_Control_Algorithm.PumpFault, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT, I_TRANSITION_NEVER_EVENT_TRIGGERED`。
- before_dsl_hash：`sha256:a4bfb2414c52c9d8ae8d62b1e0d11ad7cec3fe3824994940663a98a6b9f43bf9`；candidate_dsl_hash：`sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=pump_fault` policy=`budgeted_repair`：Variable 'pump_fault' is read but never written by any action or transition effect.；refs=`{"init_value": "0", "read_states": ["CARA.Mode_Control_Algorithm.Manual", "CARA.Mode_Control_Algorithm.NormalAutocontrol"], "var_name": "pump_fault"}`
- 2. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.NormalAutocontrol:to_path=CARA.Mode_Control_Algorithm.PumpFault` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "CARA.Mode_Control_Algorithm.NormalAutocontrol", "guard_vars": ["pump_fault"], "to_path": "CARA.Mode_Control_Algorithm.PumpFault"}`

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `CA_mode` | `unknown` | ✅ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `alarm_signal` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `blood_pressure` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `built_in_switch_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `control_voltage` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `default_flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `error_message_displayed` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `log_entry_count` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `pump_fault` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE` |
| `pump_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `requested_target_blood_pressure` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `sensor_buffer_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `software_control` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `target_blood_pressure` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-2c1837fbac1`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd4-0-6e7fd24414` | `blocking_warning` | ❌ | ✅ | Variable 'pump_fault' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects. | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-1-b901baec1e` | `blocking_warning` | ❌ | ✅ | Variable 'pump_fault' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects. | `W_GUARD_VARS_NEVER_CHANGE` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, variable:blood_pressure, variable:sensor_buffer_bp, variable:target_blood_pressure, variable:requested_target_blood_pressure, variable:flow_rate, variable:default_flow_rate, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3227`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd4-0-6e7fd24414` | `accept` | ❌ | ❌ | The NL explicitly describes a pump fault occurring and later being removed. I model that as an event-driven occurrence that writes pump_fault to 1, and the caregiver removal event writes it back to 0, avoiding a meaningless self-assignment or invented plant dynamics.；intent=Change the NormalAutocontrol-to-PumpFault transition to a pump-fault event with effec...<truncated 75 chars> |
| `fixreq-0-sd4-1-b901baec1e` | `accept` | ❌ | ❌ | The guard-only transition depended on pump_fault even though pump_fault never changed. Replacing the guard with the NL-grounded pump-fault occurrence event removes the stale guard while preserving the required NormalAutocontrol-to-PumpFault behavior.；intent=Replace the pump_fault guard on NormalAutocontrol -> PumpFault with a PumpFaultDetected event transiti...<truncated 25 chars> |
- repair_rationale：Accepted both design requests because the selected diagnostics identify the same root problem: pump_fault was treated as a runtime condition but had no NL-grounded update path.；The smallest safe edit is to encode the NL phrase 'If a pump fault such as fluid-tubing occlusion occurs' as a discrete PumpFaultDetected event from NormalAutocontrol to PumpFault, with effect pump_fault = 1.；The NL phrase 'the caregiver removes the fault' is preserved on FaultRemoved, now with effect pump_fault = 0 so the fault status is cleared on recovery to Manual.；All required states, variables, initial transitions, cross-component backManual forced transitions, manual pump-control actions, autocontrol flow computation, log update, and PumpFault alarm/software-release actions are preserved.；No external plant dynamics were invented; the pump fault is updated only by explicit NL-grounded occurrence/removal events.
- diff_summary：`{"summary": "Replaced NormalAutocontrol -> PumpFault guard on pump_fault with an NL-grounded PumpFaultDetected event that sets pump_fault = 1, and added pump_fault = 0 to the FaultRemoved recovery transition."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float target_blood_pressure = 0.0;
def float requested_target_blood_pressure = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_message_displayed = 0;
def int software_control = 0;
def int log_entry_count = 0;
def int CA_mode = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! * -> Manual :: TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                pump_speed = built_in_switch_speed;
                flow_rate = default_flow_rate;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                    error_message_displayed = 1;
                } else {
                    alarm_signal = 0;
                    error_message_displayed = 0;
                }
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 1;
                software_control = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 2;
                software_control = 1;
                alarm_signal = 0;
                error_message_displayed = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state NormalAutocontrol {
            enter {
                CA_mode = 3;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure < target_blood_pressure] {
                    flow_rate = target_blood_pressure - blood_pressure;
                } else {
                    flow_rate = 0.0;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_entry_count = log_entry_count + 1;
            }
        }

        state PumpFault {
            enter {
                CA_mode = 4;
                software_control = 0;
                alarm_signal = 1;
                error_message_displayed = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_blood_pressure = requested_target_blood_pressure; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> NormalAutocontrol;
        NormalAutocontrol -> PumpFault :: PumpFaultDetected effect { pump_fault = 1; };
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -101,7 +101,7 @@
         Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_blood_pressure = requested_target_blood_pressure; };
         Ask_StartAC -> AutocontrolInit :: StartAC;
         AutocontrolInit -> NormalAutocontrol;
-        NormalAutocontrol -> PumpFault : if [pump_fault > 0];
-        PumpFault -> Manual :: FaultRemoved;
+        NormalAutocontrol -> PumpFault :: PumpFaultDetected effect { pump_fault = 1; };
+        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:fcd45d0c5b13f30e58ef4d8e6f548182289810dbf73dfadbd8a9aebfd78e7c36`。
  - SL-10 evidence 1: `{"summary": "The two selected SD-4 design requests share the same root issue: pump_fault was read in the NormalAutocontrol -> PumpFault guard and in Manual.during but was never written. The candidate resolves this by replacing the stale guard transition with an event transition `NormalAutocontrol -> PumpFault :: PumpFaultDetected effect { pump_fault = 1; }`, so pump_fault now changes on the NL-described occurrence of a pump fault."}`
  - SL-10 evidence 2: `{"summary": "The candidate also adds `pump_fault = 0` to `PumpFault -> Manual :: FaultRemoved`, which is directly grounded in the NL statement that the caregiver removes the fault and CARA returns/releases to manual recovery. This avoids a meaningless self-assignment and does not invent autonomous plant dynamics; the variable changes only through explicit fault occurrence/removal events."}`
  - SL-10 evidence 3: `{"summary": "The required NL-grounded hierarchy, states, variables, forced backManual recovery transitions, TerminateAC transition, manual-mode actions, Ask_StartAC setpoint change, StartAC to AutocontrolInit, AutocontrolInit to NormalAutocontrol, normal autocontrol flow computation/logging, and PumpFault alarm/software-release actions are preserved in the candidate DSL."}`
  - SL-10 evidence 4: `{"summary": "The DSL diff is minimal and targeted: only the NormalAutocontrol-to-PumpFault transition mechanism and the FaultRemoved transition effect changed. No scenario regression is reported by local evidence, and the SL-9 decisions accepted both requests with NL-grounded rationale."}`
  - SL-10 evidence 5: `{"candidate_dsl_hash": "sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564", "covered_local_objection_kinds": ["missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:666be32c1ddb0d5105ffcf884456b6d8cf08914207fda5b7832d9b5248e73f7a", "local_override_rationale_count": 2, "local_override_rationale_hash": "sha256:462b576635c1c6b32f3c32d42a38db50fec7b8c0d3fa8abaa2c3f12e2aa71866", "local_rejection_evidence_hash": "sha256:351b2252f8fbf9e6601c992a5110ef94dfb03f83218d8efab0d556e31187bbac", "local_rejection_reason": "missing_required_grounding", "missing_local_objection_kinds": [], "policy": "SL-10 may override conservative ...<truncated 296 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial:CARA_to_Mode_Control_Algorithm", "transition:initial:Mode_Control_Algorithm_to_Manual"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `1` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_change_start_to_normal_autocontrol, normal_pump_fault_and_fault_removed_recovery, change_setpoint_effect_is_exact, pump_fault_detected_effect_is_exact, fault_removed_effect_is_exact_manual_recovery, initiate_ac_target_and_entry_effects, startac_target_and_autocontrolinit_entry_effects`。
- before_dsl_hash：`sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564`；candidate_dsl_hash：`sha256:7ba3465db7f9cfad6e47d2197f8f36738faf616536ef2db0a58ff045387bd4b1`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：
- 7. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-00f2a6e9827`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`7`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-91f3534105` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, then automatic init reaches NormalAutocontrol.', 'name': 'initiate_change_start_to_normal_autocontrol', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, then automatic init reaches NormalAutocontrol.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'sensor_buffer_bp': 90.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'CA_mode': 1, 'sensor_buffer_bp': 90.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'initiate_enters_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'blood_pressure': 90.0, 'requested_target_blood_pressure': 110.0}, 'scenario_name': 'initiate_change_start_to_normal_autocontrol', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 90.0, 'built_in_switch_speed': 0.0, 'control_voltage': 0.0, 'default_flow_rate': 0.0, 'error_message_displayed': 0, 'flow_rate': 0.0, 'log_entry_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'requested_target_blood_pressure': 110.0, 'sensor_buffer_bp': 90.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'dispatch_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 90.0, 'built_in_switch_speed': 0.0, 'control_voltage': 0.0, 'default_flow_rate': 0.0, 'error_message_displayed': 0, 'flow_rate': 0.0, 'log_entry_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'requested_target_blood_pressure': 110.0, 'sensor_buffer_bp': 90.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'initiate_enters_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-1-c0e512b80a` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: PumpFaultDetected during NormalAutocontrol activates alarms and releases software control; FaultRemoved returns to Manual.', 'name': 'normal_pump_fault_and_fault_removed_recovery', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: PumpFaultDetected during NormalAutocontrol activates alarms and releases software control; FaultRemoved returns to Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 0, 'error_message_displayed': 0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'expected_vars': {'CA_mode': 4, 'alarm_signal': 1, 'error_message_displayed': 1, 'pump_fault': 1, 'sensor_buffer_bp': 100.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.NormalAutocontrol.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_detected_enters_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'initial_vars': {'blood_pressure': 100.0, 'built_in_switch_speed': 2.0, 'default_flow_rate': 5.0, 'software_control': 1, 'target_blood_pressure': 120.0}, 'scenario_name': 'normal_pump_fault_and_fault_removed_recovery', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 100.0, 'built_in_switch_speed': 2.0, 'control_voltage': 0.0, 'default_flow_rate': 5.0, 'error_message_displayed': 0, 'flow_rate': 0.0, 'log_entry_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'requested_target_blood_pressure': 0.0, 'sensor_buffer_bp': 0.0, 'software_control': 1, 'target_blood_pressure': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.NormalAutocontrol.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_detected_enters_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-2-cce4a5f0d2` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: ChangeSetpoint in Ask_StartAC must remain in Ask_StartAC and copy the requested setpoint exactly, catching wrong-target and missing/wrong-effect mutations.', 'name': 'change_setpoint_effect_is_exact', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: ChangeSetpoint in Ask_StartAC must remain in Ask_StartAC and copy the requested setpoint exactly, catching wrong-target and missing/wrong-effect mutations.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 0, 'sensor_buffer_bp': 0.0, 'software_control': 0, 'target_blood_pressure': 80.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.ChangeSetpoint'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'CA_mode': 1, 'sensor_buffer_bp': 77.0, 'software_control': 0, 'target_blood_pressure': 115.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.ChangeSetpoint', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'change_setpoint_exact_copy', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'blood_pressure': 77.0, 'requested_target_blood_pressure': 115.0, 'target_blood_pressure': 80.0}, 'scenario_name': 'change_setpoint_effect_is_exact', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 77.0, 'built_in_switch_speed': 0.0, 'control_voltage': 0.0, 'default_flow_rate': 0.0, 'error_message_displayed': 0, 'flow_rate': 0.0, 'log_entry_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'requested_target_blood_pressure': 115.0, 'sensor_buffer_bp': 0.0, 'software_control': 0, 'target_blood_pressure': 80.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'change_setpoint_exact_copy', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-3-e1cca81955` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: PumpFaultDetected from NormalAutocontrol must enter PumpFault and set pump_fault exactly to active while releasing control and raising alarms.', 'name': 'pump_fault_detected_effect_is_exact', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: PumpFaultDetected from NormalAutocontrol must enter PumpFault and set pump_fault exactly to active while releasing control and raising alarms.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 0, 'error_message_displayed': 0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'expected_vars': {'CA_mode': 4, 'alarm_signal': 1, 'error_message_displayed': 1, 'pump_fault': 1, 'sensor_buffer_bp': 101.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.NormalAutocontrol.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'pump_fault_detected_exact_effect', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'initial_vars': {'alarm_signal': 0, 'blood_pressure': 101.0, 'error_message_displayed': 0, 'pump_fault': 0, 'software_control': 1, 'target_blood_pressure': 130.0}, 'scenario_name': 'pump_fault_detected_effect_is_exact', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 101.0, 'built_in_switch_speed': 0.0, 'control_voltage': 0.0, 'default_flow_rate': 0.0, 'error_message_displayed': 0, 'flow_rate': 0.0, 'log_entry_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'requested_target_blood_pressure': 0.0, 'sensor_buffer_bp': 0.0, 'software_control': 1, 'target_blood_pressure': 130.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.NormalAutocontrol.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'pump_fault_detected_exact_effect', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-4-6ec0f22a22` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: FaultRemoved from PumpFault must target Manual and clear pump_fault exactly to zero while restoring manual pump outputs.', 'name': 'fault_removed_effect_is_exact_manual_recovery', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: FaultRemoved from PumpFault must target Manual and clear pump_fault exactly to zero while restoring manual pump outputs.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'error_message_displayed': 1, 'flow_rate': 0.0, 'pump_fault': 1, 'pump_speed': 0.0, 'sensor_buffer_bp': 0.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.FaultRemoved'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'error_message_displayed': 0, 'flow_rate': 5.5, 'pump_fault': 0, 'pump_speed': 2.2, 'sensor_buffer_bp': 83.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.FaultRemoved', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_removed_exact_clear_and_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'alarm_signal': 1, 'blood_pressure': 83.0, 'built_in_switch_speed': 2.2, 'default_flow_rate': 5.5, 'error_message_displayed': 1, 'pump_fault': 1, 'software_control': 0}, 'scenario_name': 'fault_removed_effect_is_exact_manual_recovery', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 83.0, 'built_in_switch_speed': 2.2, 'control_voltage': 0.0, 'default_flow_rate': 5.5, 'error_message_displayed': 1, 'flow_rate': 0.0, 'log_entry_count': 0, 'pump_fault': 1, 'pump_speed': 0.0, 'requested_target_blood_pressure': 0.0, 'sensor_buffer_bp': 0.0, 'software_control': 0, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_removed_exact_clear_and_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-5-33fa7fbde0` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: InitiateAC from Manual must target Ask_StartAC exactly and apply Ask_StartAC entry obligations without starting software control.', 'name': 'initiate_ac_target_and_entry_effects', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: InitiateAC from Manual must target Ask_StartAC exactly and apply Ask_StartAC entry obligations without starting software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'sensor_buffer_bp': 0.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'CA_mode': 1, 'sensor_buffer_bp': 86.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'initiate_ac_exact_ask_target', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Manual', 'initial_vars': {'CA_mode': 0, 'blood_pressure': 86.0, 'built_in_switch_speed': 2.8, 'default_flow_rate': 6.8, 'software_control': 1}, 'scenario_name': 'initiate_ac_target_and_entry_effects', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'blood_pressure': 86.0, 'built_in_switch_speed': 2.8, 'control_voltage': 0.0, 'default_flow_rate': 6.8, 'error_message_displayed': 0, 'flow_rate': 0.0, 'log_entry_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'requested_target_blood_pressure': 0.0, 'sensor_buffer_bp': 0.0, 'software_control': 1, 'target_blood_pressure': 0.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'initiate_ac_exact_ask_target', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-6-6a7b373009` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: StartAC from Ask_StartAC must target AutocontrolInit exactly and set software control while clearing alarm indicators.', 'name': 'startac_target_and_autocontrolinit_entry_effects', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: StartAC from Ask_StartAC must target AutocontrolInit exactly and set software control while clearing alarm indicators.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'error_message_displayed': 1, 'sensor_buffer_bp': 0.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 2, 'alarm_signal': 0, 'error_message_displayed': 0, 'sensor_buffer_bp': 91.0, 'software_control': 1}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'startac_exact_init_target_and_effects', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'alarm_signal': 1, 'blood_pressure': 91.0, 'error_message_displayed': 1, 'software_control': 0, 'target_blood_pressure': 115.0}, 'scenario_name': 'startac_target_and_autocontrolinit_entry_effects', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 91.0, 'built_in_switch_speed': 0.0, 'control_voltage': 0.0, 'default_flow_rate': 0.0, 'error_message_displayed': 1, 'flow_rate': 0.0, 'log_entry_count': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'requested_target_blood_pressure': 0.0, 'sensor_buffer_bp': 0.0, 'software_control': 0, 'target_blood_pressure': 115.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'startac_exact_init_target_and_effects', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, variable:blood_pressure, variable:sensor_buffer_bp, variable:target_blood_pressure, variable:requested_target_blood_pressure, variable:flow_rate, variable:default_flow_rate, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3222`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-91f3534105` | `accept` | ❌ | ❌ | The scenario injects `CARA.Mode_Control_Algorithm.InitiateAC`, `ChangeSetpoint`, and `StartAC`, but the DSL represented these as source-local `::` events, so the parent-scoped event path could not resolve. Re-scoping these caregiver actions as Mode_Control_Algorithm parent-scope events fixes the path while preserving the same states, targets, and effects.；in...<truncated 113 chars> |
| `fixreq-1-sd6-1-c0e512b80a` | `accept` | ❌ | ❌ | The PumpFaultDetected event is injected as `CARA.Mode_Control_Algorithm.PumpFaultDetected`, but the current transition owns it under NormalAutocontrol. Re-scoping it to the Mode_Control_Algorithm scope makes the hot-start event resolvable and preserves the NL-grounded pump fault transition and effect.；intent=Change PumpFaultDetected from `:: PumpFaultDetecte...<truncated 27 chars> |
| `fixreq-1-sd6-2-cce4a5f0d2` | `accept` | ❌ | ❌ | ChangeSetpoint must remain in Ask_StartAC and copy requested_target_blood_pressure exactly. The self-transition and effect are already correct; only the event scope is wrong for the scenario's parent-scoped injected event.；intent=Preserve Ask_StartAC self-target and exact setpoint copy while changing ChangeSetpoint to parent-scope `: ChangeSetpoint` |
| `fixreq-1-sd6-3-e1cca81955` | `accept` | ❌ | ❌ | PumpFaultDetected must enter PumpFault and set pump_fault to 1 while PumpFault.entry releases software control and raises alarms. The transition target/effect are already correct from the prior accepted design repair; changing only event scope resolves the runtime event path.；intent=Preserve PumpFaultDetected target/effect and re-scope the event to Mode_Cont...<truncated 13 chars> |
| `fixreq-1-sd6-4-6ec0f22a22` | `accept` | ❌ | ❌ | FaultRemoved must return PumpFault to Manual and clear pump_fault. The transition target and effect are already correct; re-scoping FaultRemoved to the parent Mode_Control_Algorithm event path makes the scenario event resolvable and allows Manual.during to restore pump outputs.；intent=Change FaultRemoved from `:: FaultRemoved` to `: FaultRemoved` while prese...<truncated 25 chars> |
| `fixreq-1-sd6-5-33fa7fbde0` | `accept` | ❌ | ❌ | InitiateAC from Manual already targets Ask_StartAC and Ask_StartAC.entry sets CA_mode to 1 and software_control to 0. The only blocking mismatch is the unresolved parent-scoped event path, so the minimal fix is to re-scope InitiateAC.；intent=Change InitiateAC from `:: InitiateAC` to `: InitiateAC` |
| `fixreq-1-sd6-6-6a7b373009` | `accept` | ❌ | ❌ | StartAC from Ask_StartAC already targets AutocontrolInit, whose entry sets software_control and clears alarm indicators. The repair keeps that target and entry action and only makes StartAC visible at the injected Mode_Control_Algorithm event path.；intent=Change StartAC from `:: StartAC` to `: StartAC` |
- repair_rationale：For `initiate_change_start_to_normal_autocontrol`, step `initiate_enters_ask_startac` expected Ask_StartAC with CA_mode 1, software_control 0, and sensor_buffer_bp 90.0, but the runtime could not resolve `CARA.Mode_Control_Algorithm.Initiat...<truncated 163 chars>；For `change_setpoint_effect_is_exact`, the self-transition already copied `requested_target_blood_pressure` exactly, but `CARA.Mode_Control_Algorithm.ChangeSetpoint` could not resolve from Ask_StartAC. Re-scoping ChangeSetpoint to `: Change...<truncated 122 chars>；For `startac_target_and_autocontrolinit_entry_effects`, StartAC already targeted AutocontrolInit, whose entry sets CA_mode 2, software_control 1, and clears alarms; changing only the event scope to `: StartAC` resolves the injected parent e...<truncated 10 chars>；For `normal_pump_fault_and_fault_removed_recovery` and `pump_fault_detected_effect_is_exact`, PumpFaultDetected already targets PumpFault with effect `pump_fault = 1`; re-scoping it to `: PumpFaultDetected` resolves `CARA.Mode_Control_Algor...<truncated 89 chars>；For `fault_removed_effect_is_exact_manual_recovery`, FaultRemoved already returns to Manual with effect `pump_fault = 0`; re-scoping it to `: FaultRemoved` resolves the injected event and lets Manual.during restore sensor_buffer_bp, pump_sp...<truncated 37 chars>
- diff_summary：`{"summary": "Changed the scenario-injected Mode_Control_Algorithm event transitions InitiateAC, ChangeSetpoint, StartAC, PumpFaultDetected, and FaultRemoved from source-local `::` events to parent-scope `:` events, preserving all targets and effects."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float target_blood_pressure = 0.0;
def float requested_target_blood_pressure = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_message_displayed = 0;
def int software_control = 0;
def int log_entry_count = 0;
def int CA_mode = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! * -> Manual :: TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                pump_speed = built_in_switch_speed;
                flow_rate = default_flow_rate;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                    error_message_displayed = 1;
                } else {
                    alarm_signal = 0;
                    error_message_displayed = 0;
                }
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 1;
                software_control = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 2;
                software_control = 1;
                alarm_signal = 0;
                error_message_displayed = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state NormalAutocontrol {
            enter {
                CA_mode = 3;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure < target_blood_pressure] {
                    flow_rate = target_blood_pressure - blood_pressure;
                } else {
                    flow_rate = 0.0;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_entry_count = log_entry_count + 1;
            }
        }

        state PumpFault {
            enter {
                CA_mode = 4;
                software_control = 0;
                alarm_signal = 1;
                error_message_displayed = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_blood_pressure = requested_target_blood_pressure; };
        Ask_StartAC -> AutocontrolInit : StartAC;
        AutocontrolInit -> NormalAutocontrol;
        NormalAutocontrol -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -97,11 +97,11 @@
             }
         }
 
-        Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_blood_pressure = requested_target_blood_pressure; };
-        Ask_StartAC -> AutocontrolInit :: StartAC;
+        Manual -> Ask_StartAC : InitiateAC;
+        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_blood_pressure = requested_target_blood_pressure; };
+        Ask_StartAC -> AutocontrolInit : StartAC;
         AutocontrolInit -> NormalAutocontrol;
-        NormalAutocontrol -> PumpFault :: PumpFaultDetected effect { pump_fault = 1; };
-        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
+        NormalAutocontrol -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
+        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:c83c5335580e7dabcca4aaf4b3bd25dcf63fecfda851b344ee02699110efca7d`。
  - SL-10 evidence 1: `{"summary": "All seven SD-6 simulation requests identify the same concrete mechanism: scenario events were injected at the `CARA.Mode_Control_Algorithm.<Event>` parent scope, while the old DSL used source-local `::` event ownership for `InitiateAC`, `ChangeSetpoint`, `StartAC`, `PumpFaultDetected`, and `FaultRemoved`. The candidate changes only those five event bindings from `::` to `:` and preserves each transition source, target, and effect."}`
  - SL-10 evidence 2: `{"summary": "For `initiate_change_start_to_normal_autocontrol` and `initiate_ac_target_and_entry_effects`, the failing event was `CARA.Mode_Control_Algorithm.InitiateAC`, expected to move from Manual to Ask_StartAC with `CA_mode = 1`, `software_control = 0`, and sensor buffering. The candidate keeps `Manual -> Ask_StartAC` and Ask_StartAC entry/during behavior, while making `InitiateAC` parent-scoped and therefore visible to the injected event path."}`
  - SL-10 evidence 3: `{"summary": "For `change_setpoint_effect_is_exact`, the failing event was `CARA.Mode_Control_Algorithm.ChangeSetpoint`, expected to remain in Ask_StartAC and copy `requested_target_blood_pressure` exactly to `target_blood_pressure`. The candidate preserves the self-transition and exact effect `target_blood_pressure = requested_target_blood_pressure;` and changes only the event scope."}`
  - SL-10 evidence 4: `{"summary": "For `startac_target_and_autocontrolinit_entry_effects`, the failing event was `CARA.Mode_Control_Algorithm.StartAC`, expected to enter AutocontrolInit with `CA_mode = 2`, `software_control = 1`, alarms cleared, and sensor buffering. The candidate preserves `Ask_StartAC -> AutocontrolInit` and AutocontrolInit entry/during actions, changing only `StartAC` to parent scope."}`
  - SL-10 evidence 5: `{"summary": "For `normal_pump_fault_and_fault_removed_recovery` and `pump_fault_detected_effect_is_exact`, the failing event was `CARA.Mode_Control_Algorithm.PumpFaultDetected`, expected to enter PumpFault, set `pump_fault = 1`, release software control, and raise alarm/display signals. The candidate preserves `NormalAutocontrol -> PumpFault` with effect `pump_fault = 1` and PumpFault entry actions, changing only the event scope."}`
  - SL-10 evidence 6: `{"summary": "For `fault_removed_effect_is_exact_manual_recovery`, the failing event was `CARA.Mode_Control_Algorithm.FaultRemoved`, expected to return to Manual, clear `pump_fault = 0`, clear alarms, and restore manual pump outputs through Manual.during. The candidate preserves `PumpFault -> Manual effect { pump_fault = 0; }` and Manual.during manual-output behavior, changing only the event scope."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial:CARA_to_Mode_Control_Algorithm", "transition:initial:Mode_Control_Algorithm_to_Manual"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-2c1837fbac1` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-2c1837fbac1` | accept=2, reject=0 | `sl10_review` | `sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564` | Accepted both design requests because the selected diagnostics identify the same root problem: pump_fault was treated as a runtime condition but had no NL-grounded update path., The smallest safe edit is to encode the NL phrase 'If a pump fault such as fluid-tubing occlusion occurs' as a discrete PumpFaultDetected event from NormalAutocontrol to PumpFault, with effect pump_fault = 1., The NL phrase 'the caregiver removes the fault' is preserved on FaultRemoved, now with effect pump_fault = 0 so the fault status is cleared on recovery to Manual., ... +2 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-2c1837fbac1` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:a8ac09db1c329cf5f1b89513fbb26424021598f023a924f190dade32dca38564` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +4 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-00f2a6e9827` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-00f2a6e9827` | accept=7, reject=0 | `sl10_review` | `sha256:7ba3465db7f9cfad6e47d2197f8f36738faf616536ef2db0a58ff045387bd4b1` | For `initiate_change_start_to_normal_autocontrol`, step `initiate_enters_ask_startac` expected Ask_StartAC with CA_mode 1, software_control 0, and sensor_buffer_bp 90.0, but the runtime could not resolve `CARA.Mode_Control_Algorithm.InitiateAC` while Manual was active. Re-scoping InitiateAC to `: InitiateAC` makes that parent-owned event resolvable without changing the target or entry/during actions., For `change_setpoint_effect_is_exact`, the self-transition already copied `requested_target_blood_pressure` exactly, but `CARA.Mode_Control_Algorithm.ChangeSetpoint` could not resolve from Ask_StartAC. Re-scoping ChangeSetpoint to `: ChangeSetpoint` preserves the exact self-target/effect and lets Ask_StartAC.entry/during establish CA_mode and sensor_buffer_bp., For `startac_target_and_autocontrolinit_entry_effects`, StartAC already targeted AutocontrolInit, whose entry sets CA_mode 2, software_control 1, and clears alarms; changing only the event scope to `: StartAC` resolves the injected parent event path., ... +4 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-00f2a6e9827` | accept=7, reject=0 | `sc11_accept_then_sd2` | `sha256:7ba3465db7f9cfad6e47d2197f8f36738faf616536ef2db0a58ff045387bd4b1` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +6 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4492, 'completion_chars': 18049, 'completion_tokens': 6453, 'elapsed_seconds': 118.52410193998367, 'estimated_completion_tokens': 4513, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11170, 'first_chunk_seconds': 37.60481163399527, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12903}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1340, 'completion_chars': 5772, 'completion_tokens': 1859, 'elapsed_seconds': 35.68085202097427, 'estimated_completion_tokens': 1443, 'estimated_prompt_tokens': 28315, 'estimated_total_tokens': 29758, 'first_chunk_seconds': 11.93684882298112, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 113258, 'prompt_tokens': 25563, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 27422}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 593, 'completion_chars': 2764, 'completion_tokens': 754, 'elapsed_seconds': 16.151911867025774, 'estimated_completion_tokens': 691, 'estimated_prompt_tokens': 26130, 'estimated_total_tokens': 26821, 'first_chunk_seconds': 5.421799495990854, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 104517, 'prompt_tokens': 22699, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23453}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2556, 'completion_chars': 10273, 'completion_tokens': 4289, 'elapsed_seconds': 79.20731173700187, 'estimated_completion_tokens': 2569, 'estimated_prompt_tokens': 15384, 'estimated_total_tokens': 17953, 'first_chunk_seconds': 33.12155182601418, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 61536, 'prompt_tokens': 15122, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 19411}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3331, 'completion_chars': 13462, 'completion_tokens': 3685, 'elapsed_seconds': 68.44356662599603, 'estimated_completion_tokens': 3366, 'estimated_prompt_tokens': 18163, 'estimated_total_tokens': 21529, 'first_chunk_seconds': 10.513800615037326, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 72650, 'prompt_tokens': 17853, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21538}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3803, 'completion_chars': 15390, 'completion_tokens': 4261, 'elapsed_seconds': 78.67873739800416, 'estimated_completion_tokens': 3848, 'estimated_prompt_tokens': 18960, 'estimated_total_tokens': 22808, 'first_chunk_seconds': 11.453653573989868, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 75839, 'prompt_tokens': 18628, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22889}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2315, 'completion_chars': 9694, 'completion_tokens': 2834, 'elapsed_seconds': 54.12041673401836, 'estimated_completion_tokens': 2424, 'estimated_prompt_tokens': 80694, 'estimated_total_tokens': 83118, 'first_chunk_seconds': 12.250332678027917, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 322776, 'prompt_tokens': 69407, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 72241}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1040, 'completion_chars': 4690, 'completion_tokens': 1370, 'elapsed_seconds': 28.49170827801572, 'estimated_completion_tokens': 1173, 'estimated_prompt_tokens': 93633, 'estimated_total_tokens': 94806, 'first_chunk_seconds': 9.79987412301125, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 374532, 'prompt_tokens': 78542, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 79912}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3803, 'completion_chars': 15390, 'completion_tokens': 4201, 'elapsed_seconds': 78.04618731798837, 'estimated_completion_tokens': 3848, 'estimated_prompt_tokens': 20068, 'estimated_total_tokens': 23916, 'first_chunk_seconds': 9.23945414298214, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 80269, 'prompt_tokens': 19936, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24137}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1777, 'completion_chars': 8529, 'completion_tokens': 2483, 'elapsed_seconds': 47.40482612000778, 'estimated_completion_tokens': 2133, 'estimated_prompt_tokens': 21703, 'estimated_total_tokens': 23836, 'first_chunk_seconds': 15.354213984974194, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 86810, 'prompt_tokens': 21753, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24236}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`35/16`，missing=`<none>`。
- repairs：`2/2` accepted；scenario_history=`5`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
