## path1 / cara-infusion-pump-formal-spec__01 / default 真实运行结果：Path1 CARA representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`not_converged`；record_status：`budget_exhausted`；result_status：`not_converged`。
- main_result_eligible：`false`。
- Path2 ref-model blueprint eligible：`n/a`；reason：not_applicable_to_path1。
- 一句话结论：`scenario_or_sim_oracle`；停止原因：SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `cara-infusion-pump-formal-spec__01` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `4304eb65692c6576b81986b4f1208ed818c4be26` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:e2cfdd7ab1fd43540a75a5216158706cc6809d0eb975e3731e90124b8a1ff158` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e` |
| final verdict/status | verdict=`not_converged`, record=`budget_exhausted`, result=`not_converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c", "iteration": 4, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:4b7ddbbc35781ef3abb32c1b383b0c3781a16fd087b76b085b8a58b22fa99b7b", "iteration": 3, "repair_history_index": 5, "rework_instructions": ["Return a raw parseable pyfcstm DSL model only. Do not wrap it in JSON, do not include a `decisions` array, and do not put the DSL inside a quoted `candidate_dsl` string. The first token of the candidate should be a valid pyfcstm token such as `def` or `state`, not `{`.", "Restore the full prior parseable DSL structure rather than the truncated JSON/string candidate: all variable definitions, `state CARA`, nested `state Mode_Control_Algorithm`, states `Manual`, `Ask_StartAC`, `AutocontrolInit`, `AutocontrolNormal`, `PumpFault`, initial transitions, event transitions, guards, and actions must be present.", "Do not implement the proposed unconditional `alarm_signal = 0` in `Manual.enter` or `Manual.during`. Preserve the fixlog-12 safety behavior: in Manual, set `alarm_signal = 1` when `pump_fault > 0`, otherwise set `alarm_signal = 0`.", "Preserve the PumpFault fallback/termination transitions `PumpFault -> Manual : CA_backManual;`, `CB_backManual;`, `CP_backManual;`, `CC_backManual;`, and `TerminateAC;` without clearing `pump_fault`.", "Preserve `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };` as the only transition that clears `pump_fault`, matching the NL distinction between cross-component fallback to Manual and caregiver fault removal.", "Preserve Manual recovery outputs other than the pump-fault-sensitive alarm logic: `CA_mode = 0`, `software_control = 0`, `sensor_buffer_bp = blood_pressure`, `infusion_rate = default_flow_rate`, and `pump_speed = switch_speed`.", "Preserve `AutocontrolNormal -> PumpFault : if [pump_fault > 0];` so an unresolved fault persists across fallback and can re-enter PumpFault when autocontrol is restarted.", "In the SL-9 repair rationale, explicitly acknowledge that the current SD-6 scenarios expect `alarm_signal=0` after PumpFault fallback, but that this exact oracle was previously overridden in fixlog-12 because the NL requires alarms to remain active until `FaultRemoved` clears the fault. Do not chase that stale expected value by reintroducing the unsafe de-alarm behavior."], "same_as_final": false, "sl10_decision": "rework"}, "matching_repair_history_indices": [4, 6, 7], "repair_history_index": 7, "selected_source_stage": "SD-6", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, ... +9` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5` |
| token/cost/time | tokens=`{'prompt_tokens': None, 'completion_tokens': None, 'total_tokens': None, 'estimated_prompt_tokens': 1755858, 'estimated_completion_tokens': 56196, 'estimated_total_tokens': 1812054, 'prompt_chars': 7023391, 'completion_chars': 224755, 'n_calls': 24, 'token_usage_available': False, 'token_usage_unavailable_calls': 1}`, elapsed=`1444.281s` |
| run record | [`pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:6ecd52ebd944b26023390b892f680e22984f2a1905a99d8b254cc816e7ae86d8` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `78` |
| `langgraph_node_trace_hash` | `sha256:ef1dec353dd339195e8e39c649eb6c9d9b0f831a64f270ce9066c8169a76bbb3` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `78` |

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
def int target_bp = 100;
def int requested_target_bp = 100;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int infusion_rate = 0;
def int pump_speed = 0;
def int switch_speed = 0;
def int default_flow_rate = 0;
def int control_voltage = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_fault = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Manual -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolNormal -> Manual : CA_backManual;
        ! Manual -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolNormal -> Manual : CB_backManual;
        ! Manual -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolNormal -> Manual : CP_backManual;
        ! Manual -> Manual : CC_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! AutocontrolNormal -> Manual : CC_backManual;
        ! Manual -> Manual : TerminateAC;
        ! Ask_StartAC -> Manual : TerminateAC;
        ! AutocontrolInit -> Manual : TerminateAC;
        ! AutocontrolNormal -> Manual : TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
                }
            }
            during {
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
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
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 2;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure >= target_bp] {
                    infusion_rate = 0;
                } else {
                    infusion_rate = target_bp - blood_pressure;
                }
                control_voltage = infusion_rate;
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
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual : CA_backManual;
        PumpFault -> Manual : CB_backManual;
        PumpFault -> Manual : CP_backManual;
        PumpFault -> Manual : CC_backManual;
        PumpFault -> Manual : TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=13835 | 生成初始 DSL 与 grounding seeds | initial len=2826 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=141279 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=2, tokens=50271 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=141279 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=141279 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=141279 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=2, tokens=50271 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=141279 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=8, tokens=652736 | LLM per-request accept/reject + repair | candidate len=3645,3625,3983,3848,4128,2455,4128,4128 | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=8, tokens=458802 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5 | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-waiver-4304eb65-1e5b4c9e.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T10:34:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T10:34:52Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T10:34:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T10:34:52Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T10:37:07Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T10:37:07Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2826,hash=sha256:38a510f918f8 |
| 7 | `2026-06-05T10:37:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T10:37:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T10:37:07Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:38a510f918f8854457651897bbc3b319965d80e59a1f192d261c3cc8ceee5a72 |
| 10 | `2026-06-05T10:37:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T10:37:07Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2826,hash=sha256:38a510f918f8, current_hash=sha256:38a510f918f8854457651897bbc3b319965d80e59a1f192d261c3cc8ceee5a72 |
| 12 | `2026-06-05T10:37:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T10:37:07Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T10:37:07Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T10:37:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T10:37:07Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T10:37:08Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T10:37:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T10:37:08Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T10:37:08Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T10:37:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T10:37:08Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T10:38:51Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T10:38:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T10:38:51Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T10:38:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T10:38:51Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T10:38:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T10:38:51Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T10:38:51Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T10:38:51Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T10:38:51Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T10:39:41Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T10:39:41Z` | `SL-7` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T10:39:41Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T10:39:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T10:39:41Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["DSL: `! * -> Manual :: CA_backManual;`, `! * -> Manual :: CB_backManual;`, `! * -> Manual :: CP_backManual;`, `! * -> Manual :: CC_backManual;`, `! * -> Manual :: TerminateAC;`", "DSL: `Manual.enter` sets `alarm_signal = 0`", "DSL: `Manual.during` sets `pump_speed = switch_speed` and `in...<truncated 660 chars> | <none> |
| 38 | `2026-06-05T10:39:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T10:39:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T10:39:41Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["DSL: `! * -> Manual :: CA_backManual;`, `! * -> Manual :: CB_backManual;`, `! * -> Manual :: CP_backManual;`, `! * -> Manual :: CC_backManual;`, `! * -> Manual :: TerminateAC;`", "DSL: `Manual.enter` sets `alarm_signal = 0`", "DSL: `Manual.during` sets `pump_speed = switch_speed` and `infusion_...<truncated 653 chars> | current_dsl:len=2826,hash=sha256:38a510f918f8 |
| 41 | `2026-06-05T10:39:41Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-05T10:39:41Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 43 | `2026-06-05T10:39:41Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2826,hash=sha256:38a510f918f8 |
| 44 | `2026-06-05T10:40:48Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 45 | `2026-06-05T10:40:48Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=3645,hash=sha256:d13b720f6479 |
| 46 | `2026-06-05T10:40:48Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 47 | `2026-06-05T10:40:48Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:d13b720f647947765800eba3d078515a5fb42b1edd862d5496a2307469102258 |
| 48 | `2026-06-05T10:41:26Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 49 | `2026-06-05T10:41:26Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 50 | `2026-06-05T10:41:26Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 51 | `2026-06-05T10:41:26Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2826,hash=sha256:38a510f918f8 |
| 52 | `2026-06-05T10:42:12Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 53 | `2026-06-05T10:42:12Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=3625,hash=sha256:916de02edd77 |
| 54 | `2026-06-05T10:42:12Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 55 | `2026-06-05T10:42:12Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39 |
| 56 | `2026-06-05T10:42:41Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 57 | `2026-06-05T10:42:41Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 58 | `2026-06-05T10:42:41Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 59 | `2026-06-05T10:42:41Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=3625,hash=sha256:916de02edd77 |
| 60 | `2026-06-05T10:42:41Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39 |
| 61 | `2026-06-05T10:42:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 62 | `2026-06-05T10:42:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 63 | `2026-06-05T10:42:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 64 | `2026-06-05T10:42:41Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39 |
| 65 | `2026-06-05T10:42:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 66 | `2026-06-05T10:42:41Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=3625,hash=sha256:916de02edd77, current_hash=sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39 |
| 67 | `2026-06-05T10:42:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 68 | `2026-06-05T10:42:41Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 69 | `2026-06-05T10:42:41Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 70 | `2026-06-05T10:42:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 71 | `2026-06-05T10:42:41Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 72 | `2026-06-05T10:42:41Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 73 | `2026-06-05T10:42:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 74 | `2026-06-05T10:42:41Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 75 | `2026-06-05T10:42:41Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-5A", "ok": true, "status": "StageStatus.OK"} | <none> |
| 76 | `2026-06-05T10:42:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 77 | `2026-06-05T10:42:41Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 targeted_retry", "ok": false, "reason": "reuse_frozen_scenario_set"} | <none> |
| 78 | `2026-06-05T10:42:41Z` | `<control>` | `1` | `frozen_scenario_refresh_targeted_retry` | {} | <none> |
| 79 | `2026-06-05T10:42:41Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 80 | `2026-06-05T10:42:41Z` | `SL-5` | `1` | `stage_enter` | {"reason": "targeted_refresh_after_frozen_gap_or_dsl_change"} | <none> |
- ……另有 `185` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SL-7` | yes | fixbatch-0-sha256-23ece122ce8 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-6` | yes | fixbatch-1-sha256-8bd9f01c6cc / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SL-7` | yes | fixbatch-2-sha256-84bb8b508a9 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `SD-6` | yes | fixbatch-3-sha256-af0e33feb09 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 4 | `SD-6` | yes | fixbatch-4-sha256-af0e33feb09 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5 |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|---|
| `default_init_manual_sets_manual_outputs` | default-init verifies the Mode_Control_Algorithm initial leaf is Manual and manual operation uses switch speed/default f...<truncated 23 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `initiate_change_setpoint_start_autocontrol` | explicit-hot-start from Manual probes InitiateAC to Ask_StartAC, setpoint change there, StartAC to AutocontrolInit, then...<truncated 30 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `normal_autocontrol_low_pressure_positive_flow` | explicit-hot-start in AutocontrolNormal verifies BP below target produces a positive infusion rate, matching control vol...<truncated 28 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `normal_autocontrol_high_pressure_zero_flow` | explicit-hot-start in AutocontrolNormal verifies higher/equal BP produces lower flow, here zero rate and zero pump comma...<truncated 18 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_boundary_no_fire_at_zero` | explicit-hot-start in AutocontrolNormal probes pump_fault boundary: with no complication indicated, normal autocontrol m...<truncated 18 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_boundary_fire_and_fault_removed` | explicit-hot-start in AutocontrolNormal probes pump_fault boundary: a complication enters PumpFault, alarms/releases sof...<truncated 48 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_back_manual_from_ask_init_and_normal` | explicit-hot-start from Ask_StartAC probes CB_backManual, CP_backManual, CA_backManual, and CC_backManual as shared Manu...<truncated 42 chars> | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `forced_back_manual_from_pump_fault_preserves_active_alarm` | explicit-hot-start in PumpFault probes that shared backManual/TerminateAC recover to Manual while an unresolved pump fau...<truncated 41 chars> | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `forced_back_manual_from_ask_and_init` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `forced_ca_terminate_cc_back_manual_from_normal` |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| `isolated_wrong_target_mode_path_probes` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `forced_self_back_manual_from_manual_resets_outputs` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `isolated_wrong_target_fault_path_probes` |  | ⚪ | ✅ | ✅ | ✅ | ✅ |
| `forced_back_manual_from_pump_fault_leaf` |  | ⚪ | ❌ | ✅ | ❌ | ❌ |
| `forced_missing_line_matrix_from_manual` |  | ⚪ | ⚪ | ✅ | ✅ | ✅ |
| `forced_missing_line_matrix_from_ask` |  | ⚪ | ⚪ | ✅ | ✅ | ✅ |
| `forced_missing_line_matrix_from_init` |  | ⚪ | ⚪ | ✅ | ✅ | ✅ |
| `forced_and_fault_event_targets_from_pump_fault` |  | ⚪ | ⚪ | ✅ | ❌ | ❌ |
| `forced_missing_line_matrix_from_normal` |  | ⚪ | ⚪ | ✅ | ✅ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_sets_manual_outputs` — default-init verifies the Mode_Control_Algorithm initial leaf is Manual and manual operation uses switch speed/default flow while buffering BP.</summary>

| Field | Value |
|---|---|
| description | default-init verifies the Mode_Control_Algorithm initial leaf is Manual and manual operation uses switch speed/default flow while buffering BP. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 70, "default_flow_rate": 5, "switch_speed": 7}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "infusion_rate": 5, "pump_speed": 7, "sensor_buffer_bp": 70, "software_control": 0}` |

</details>

<details><summary>`initiate_change_setpoint_start_autocontrol` — explicit-hot-start from Manual probes InitiateAC to Ask_StartAC, setpoint change there, StartAC to AutocontrolInit, then normal autocontrol operation.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from Manual probes InitiateAC to Ask_StartAC, setpoint change there, StartAC to AutocontrolInit, then normal autocontrol operation. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"blood_pressure": 90, "log_count": 0, "requested_target_bp": 120, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiate_enters_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "sensor_buffer_bp": 90, "software_control": 0}` |
| 1 `change_setpoint_updates_target` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "sensor_buffer_bp": 90, "software_control": 0, "target_bp": 120}` |
| 2 `start_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 2, "alarm_signal": 0, "sensor_buffer_bp": 90, "software_control": 1}` |
| 3 `init_advances_to_normal_and_controls_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 2, "control_voltage": 30, "infusion_rate": 30, "log_count": 1, "pump_speed": 30, "sensor_buffer_bp": 90, "software_control": 1}` |

</details>

<details><summary>`normal_autocontrol_low_pressure_positive_flow` — explicit-hot-start in AutocontrolNormal verifies BP below target produces a positive infusion rate, matching control voltage/pump speed and logging.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal verifies BP below target produces a positive infusion rate, matching control voltage/pump speed and logging. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 2, "blood_pressure": 80, "log_count": 3, "software_control": 1, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `low_pressure_flow_computed` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 20, "infusion_rate": 20, "log_count": 4, "pump_speed": 20, "sensor_buffer_bp": 80}` |

</details>

<details><summary>`normal_autocontrol_high_pressure_zero_flow` — explicit-hot-start in AutocontrolNormal verifies higher/equal BP produces lower flow, here zero rate and zero pump command, while logging.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal verifies higher/equal BP produces lower flow, here zero rate and zero pump command, while logging. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 2, "blood_pressure": 120, "log_count": 0, "software_control": 1, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `high_pressure_flow_limited_to_zero` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 0, "infusion_rate": 0, "log_count": 1, "pump_speed": 0, "sensor_buffer_bp": 120}` |

</details>

<details><summary>`pump_fault_boundary_no_fire_at_zero` — explicit-hot-start in AutocontrolNormal probes pump_fault boundary: with no complication indicated, normal autocontrol must remain active.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal probes pump_fault boundary: with no complication indicated, normal autocontrol must remain active. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 2, "blood_pressure": 95, "log_count": 0, "pump_fault": 0, "software_control": 1, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_fault_stays_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 5, "infusion_rate": 5, "log_count": 1, "pump_speed": 5, "sensor_buffer_bp": 95}` |

</details>

<details><summary>`pump_fault_boundary_fire_and_fault_removed` — explicit-hot-start in AutocontrolNormal probes pump_fault boundary: a complication enters PumpFault, alarms/releases software control, then FaultRemoved returns...<truncated 8 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal probes pump_fault boundary: a complication enters PumpFault, alarms/releases software control, then FaultRemoved returns Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 2, "blood_pressure": 85, "default_flow_rate": 5, "pump_fault": 1, "software_control": 1, "switch_speed": 6}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_enters_pump_fault` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "infusion_rate": 5, "pump_speed": 6, "sensor_buffer_bp": 85, "software_control": 0}` |
| 1 `fault_removed_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "infusion_rate": 5, "pump_fault": 0, "pump_speed": 6, "sensor_buffer_bp": 85, "software_control": 0}` |

</details>

<details><summary>`forced_back_manual_from_ask_init_and_normal` — explicit-hot-start from Ask_StartAC probes CB_backManual, CP_backManual, CA_backManual, and CC_backManual as shared Manual recovery targets from non-fault leave...<truncated 2 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from Ask_StartAC probes CB_backManual, CP_backManual, CA_backManual, and CC_backManual as shared Manual recovery targets from non-fault leaves. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"blood_pressure": 75, "default_flow_rate": 4, "log_count": 0, "requested_target_bp": 110, "switch_speed": 8, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_back_manual_from_ask` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "infusion_rate": 4, "pump_speed": 8, "sensor_buffer_bp": 75, "software_control": 0}` |
| 1 `return_to_ask` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "sensor_buffer_bp": 75, "software_control": 0}` |
| 2 `start_enters_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 2, "alarm_signal": 0, "sensor_buffer_bp": 75, "software_control": 1}` |
| 3 `cp_back_manual_from_init` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "infusion_rate": 4, "pump_speed": 8, "sensor_buffer_bp": 75, "software_control": 0}` |
| 4 `reenter_normal_for_ca_and_cc` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "sensor_buffer_bp": 75, "software_control": 0}` |
| 5 `start_again_to_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 2, "alarm_signal": 0, "sensor_buffer_bp": 75, "software_control": 1}` |
| 6 `advance_to_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 2, "control_voltage": 25, "infusion_rate": 25, "log_count": 1, "pump_speed": 25, "sensor_buffer_bp": 75, "software_control": 1}` |
| 7 `ca_back_manual_from_normal` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "infusion_rate": 4, "pump_speed": 8, "sensor_buffer_bp": 75, "software_control": 0}` |
| 8 `manual_self_cc_back_manual` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "infusion_rate": 4, "pump_speed": 8, "sensor_buffer_bp": 75, "software_control": 0}` |

</details>

<details><summary>`forced_back_manual_from_pump_fault_preserves_active_alarm` — explicit-hot-start in PumpFault probes that shared backManual/TerminateAC recover to Manual while an unresolved pump fault keeps alarm active until FaultRemoved...<truncated 1 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in PumpFault probes that shared backManual/TerminateAC recover to Manual while an unresolved pump fault keeps alarm active until FaultRemoved. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 2, "alarm_signal": 1, "blood_pressure": 78, "default_flow_rate": 8, "pump_fault": 1, "software_control": 1, "switch_speed": 2, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_back_manual_from_pump_fault_keeps_alarm` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 1, "infusion_rate": 8, "pump_fault": 1, "pump_speed": 2, "sensor_buffer_bp": 78, "software_control": 0}` |
| 1 `reenter_fault_via_autocontrol_with_persistent_fault` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "sensor_buffer_bp": 78, "software_control": 0}` |
| 2 `start_to_init_with_persistent_fault` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 2, "alarm_signal": 0, "sensor_buffer_bp": 78, "software_control": 1}` |
| 3 `advance_to_normal_before_fault_guard` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 2, "control_voltage": 22, "infusion_rate": 22, "pump_speed": 22, "sensor_buffer_bp": 78, "software_control": 1}` |
| 4 `persistent_fault_reenters_pump_fault` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "infusion_rate": 8, "pump_fault": 1, "pump_speed": 2, "sensor_buffer_bp": 78, "software_control": 0}` |
| 5 `terminate_from_pump_fault_keeps_alarm_until_removed` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 1, "infusion_rate": 8, "pump_fault": 1, "pump_speed": 2, "sensor_buffer_bp": 78, "software_control": 0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Repair the fallback event representation so CARA.Mode_Control_Algorithm.CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC are again resolvable as pare...<truncated 758 chars> | `sha256:d13b720f647947765800eba3d078515a5fb42b1edd862d5496a2307469102258` |
| 2 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | `sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39` |
| 3 | `1` | ❌ | `SD-6` | forced_back_manual_from_pump_fault_leaf | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Keep the five parent-level PumpFault fallback/termination transitions so `CARA.Mode_Control_Algorithm.CA_backManual`, `CB_backManual`, `CP_backManual`, `CC_backManual`, and `Te...<truncated 477 chars> | `sha256:7210b3208097b368871ee1fd999eab559dfebd3caa802ea2c295d30441e0acf9` |
| 4 | `1` | ✅ | `SD-6` | forced_back_manual_from_pump_fault_leaf | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:0c453825a7e1638f62cf9c8f073d1dc0eaf11a6fcdec70b61dd74c72ce74073d` |
| 5 | `2` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c` |
| 6 | `3` | ❌ | `SD-6` | forced_back_manual_from_pump_fault_leaf, forced_and_fault_event_targets_from_pump_fault | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Return a raw parseable pyfcstm DSL model only. Do not wrap it in JSON, do not include a `decisions` array, and do not put the DSL inside a quoted `candidate_dsl` string. The fi...<truncated 550 chars> | `sha256:4b7ddbbc35781ef3abb32c1b383b0c3781a16fd087b76b085b8a58b22fa99b7b` |
| 7 | `3` | ✅ | `SD-6` | forced_back_manual_from_pump_fault_leaf, forced_and_fault_event_targets_from_pump_fault | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c` |
| 8 | `4` | ✅ | `SD-6` | forced_back_manual_from_pump_fault_leaf, forced_and_fault_event_targets_from_pump_fault | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c` |

<details><summary>Repair 1 / iteration `0` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:38a510f918f8854457651897bbc3b319965d80e59a1f192d261c3cc8ceee5a72`；candidate_dsl_hash：`sha256:d13b720f647947765800eba3d078515a5fb42b1edd862d5496a2307469102258`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Forced back-to-manual transitions can fire from PumpFault and return to Manual without requiring `FaultRemoved` or clearing `pump_fault`, causing alarm clearing and manual pump operation while the modeled pump fault remains active.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-23ece122ce8`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL: `! * -> Manual :: CA_backManual;`, `! * -> Manual :: CB_backManual;`, `! * -> Manual :: CP_backManual;`, `! * -> Manual :: CC_backManual;`, `! * -> Manual :: TerminateAC;`', 'DSL: `Manual.enter` sets `alarm_signal = 0`', 'DSL: `Manual.during` sets `pump_speed = switch_speed` and `infusion_rate = default_flow_rate`', 'DSL: forced transitions do not include guard `pump_fault == 0` or effect `pump_fault = 0`', 'NL requires the caregiver to remove the pump fault before recovery: "the caregiver removes the fault"'], 'severity': 'major', 'summary': 'Forced back-to-manual transitions can fire from PumpFault and return to Manual without requiring `FaultRemoved` or clearing `pump_fault`, causing alarm clearing and manual pump operation while the modeled pump fault remains active.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, ... +37`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3645`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ❌ | The review evidence is valid: a wildcard forced back-to-manual transition from `*` includes `PumpFault`, allowing recovery to `Manual` before `FaultRemoved` clears `pump_fault`. I repaired this by keeping all required back-manual and terminate events as forced transitions for the non-fault operational states only, while leaving `PumpFault -> Manual :: FaultR...<truncated 390 chars> |
- repair_rationale：Accepted the hard SL-7 model-review request because the original `! * -> Manual` transitions applied to `PumpFault` and could bypass the NL-required caregiver fault removal.；The repair preserves all required states, variables, events, initial transitions, normal autocontrol behavior, setpoint change behavior, logging abstraction, and the `pump_fault > 0` transition into `PumpFault`.；The back-to-manual and terminate fallback events remain modeled as forced transitions, but they are scoped to the non-fault operational states: `Manual`, `Ask_StartAC`, `AutocontrolInit`, and `AutocontrolNormal`.；No forced fallback transition is now declared from `PumpFault`; therefore once the model is in `PumpFault`, the only modeled recovery to `Manual` is `FaultRemoved`, which clears `pump_fault` as required by the diagnostic and NL evidence.
- diff_summary：`{"summary": "Replaced the five wildcard forced transitions `! * -> Manual :: ...` with source-specific forced transitions for Manual, Ask_StartAC, AutocontrolInit, and AutocontrolNormal, excluding PumpFault so fault recovery requires `FaultRemoved`."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 100;
def int requested_target_bp = 100;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int infusion_rate = 0;
def int pump_speed = 0;
def int switch_speed = 0;
def int default_flow_rate = 0;
def int control_voltage = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_fault = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Manual -> Manual :: CA_backManual;
        ! Ask_StartAC -> Manual :: CA_backManual;
        ! AutocontrolInit -> Manual :: CA_backManual;
        ! AutocontrolNormal -> Manual :: CA_backManual;
        ! Manual -> Manual :: CB_backManual;
        ! Ask_StartAC -> Manual :: CB_backManual;
        ! AutocontrolInit -> Manual :: CB_backManual;
        ! AutocontrolNormal -> Manual :: CB_backManual;
        ! Manual -> Manual :: CP_backManual;
        ! Ask_StartAC -> Manual :: CP_backManual;
        ! AutocontrolInit -> Manual :: CP_backManual;
        ! AutocontrolNormal -> Manual :: CP_backManual;
        ! Manual -> Manual :: CC_backManual;
        ! Ask_StartAC -> Manual :: CC_backManual;
        ! AutocontrolInit -> Manual :: CC_backManual;
        ! AutocontrolNormal -> Manual :: CC_backManual;
        ! Manual -> Manual :: TerminateAC;
        ! Ask_StartAC -> Manual :: TerminateAC;
        ! AutocontrolInit -> Manual :: TerminateAC;
        ! AutocontrolNormal -> Manual :: TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_signal = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
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
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 2;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure >= target_bp] {
                    infusion_rate = 0;
                } else {
                    infusion_rate = target_bp - blood_pressure;
                }
                control_voltage = infusion_rate;
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
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -17,11 +17,26 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
-        ! * -> Manual :: TerminateAC;
+        ! Manual -> Manual :: CA_backManual;
+        ! Ask_StartAC -> Manual :: CA_backManual;
+        ! AutocontrolInit -> Manual :: CA_backManual;
+        ! AutocontrolNormal -> Manual :: CA_backManual;
+        ! Manual -> Manual :: CB_backManual;
+        ! Ask_StartAC -> Manual :: CB_backManual;
+        ! AutocontrolInit -> Manual :: CB_backManual;
+        ! AutocontrolNormal -> Manual :: CB_backManual;
+        ! Manual -> Manual :: CP_backManual;
+        ! Ask_StartAC -> Manual :: CP_backManual;
+        ! AutocontrolInit -> Manual :: CP_backManual;
+        ! AutocontrolNormal -> Manual :: CP_backManual;
+        ! Manual -> Manual :: CC_backManual;
+        ! Ask_StartAC -> Manual :: CC_backManual;
+        ! AutocontrolInit -> Manual :: CC_backManual;
+        ! AutocontrolNormal -> Manual :: CC_backManual;
+        ! Manual -> Manual :: TerminateAC;
+        ! Ask_StartAC -> Manual :: TerminateAC;
+        ! AutocontrolInit -> Manual :: TerminateAC;
+        ! AutocontrolNormal -> Manual :: TerminateAC;
 
         [*] -> Manual;
 
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:335f0fe0b4e1fe3ab03c910919b195e398504f11aeddfab10b70ad1f74513e18`。
  - SL-10 evidence 1: `{"summary": "The NL requires CA_backManual and each of CB_backManual, CP_backManual, and CC_backManual to cause CA_mode to become Manual as a cross-component fallback, and TerminateAC is also required as caregiver termination of algorithmic pump control. The old DSL exposed these as parent-level forced wildcard transitions under Mode_Control_Algorithm. The candidate replaced them with source-specific forced transitions that exclude PumpFault, which addresses the unsafe-recovery intent in SL-9, but local simulation shows the required parent-level events are no longer resolvable from hot-started Ask_StartAC or AutocontrolNormal states."}`
  - SL-10 evidence 2: `{"summary": "Local scenario regression is concrete and NL-relevant: scenario forced_back_manual_from_ask_and_init fails at step cb_back_manual_from_ask when event CARA.Mode_Control_Algorithm.CB_backManual is injected from Ask_StartAC. Expected state was CARA.Mode_Control_Algorithm.Manual with CA_mode=0, software_control=0, alarm_signal=0, sensor_buffer_bp=75, infusion_rate=4, pump_speed=8. Actual state remained Ask_StartAC and runtime raised unresolved_event_path for CARA.Mode_Control_Algorithm.CB_backManual."}`
  - SL-10 evidence 3: `{"summary": "Local scenario forced_ca_terminate_cc_back_manual_from_normal also fails at step ca_back_manual_from_normal when event CARA.Mode_Control_Algorithm.CA_backManual is injected from AutocontrolNormal. Expected state was Manual with CA_mode=0, software_control=0, alarm_signal=0, sensor_buffer_bp=70, infusion_rate=9, pump_speed=4. Actual state remained AutocontrolNormal with CA_mode=2, software_control=1, sensor_buffer_bp=0, infusion_rate=0, pump_speed=0 and runtime raised unresolved_event_path for CARA.Mode_Control_Algorithm.CA_backManual."}`
  - SL-10 evidence 4: `{"summary": "The candidate preserves core states, variables, normal autocontrol flow, fault entry, and FaultRemoved recovery, and the passing fault scenario confirms PumpFault -> Manual :: FaultRemoved clears pump_fault. However, the diff introduces major behavioral drift by losing parent-visible fallback-event grounding and reducing forced transition coverage/count from the local checker perspective. Because the NL-required shared recovery events no longer execute, the repaired DSL is not ready for top-down revalidation."}`
- SL-10 rework_instructions：Repair the fallback event representation so CARA.Mode_Control_Algorithm.CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC are again resolvable as parent-level Mode_Control_Algorithm events from Manual, Ask_StartAC, AutocontrolInit, and AutocontrolNormal, and each sends the model to Manual so Manual.enter/during produce CA_mode=0, so...<truncated 128 chars>；Preserve the SL-7 unsafe-recovery fix: while pump_fault remains active in PumpFault, these fallback/terminate events must not bypass caregiver fault removal. PumpFault recovery to Manual must remain through PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; }.；Prefer the smallest DSL edit that restores event visibility without reintroducing unsafe recovery, such as replacing the 20 source-specific forced transitions with guarded parent-level wildcard forced transitions for the five events, e.g. wildcard forced transitions to Manual that fire only when pump_fault == 0, if this guard syntax is supported by the DSL. ...<truncated 228 chars>；After the edit, specifically verify the two failed local scenarios: from Ask_StartAC, CARA.Mode_Control_Algorithm.CB_backManual must enter Manual with sensor_buffer_bp=75, infusion_rate=4, pump_speed=8; from AutocontrolNormal, CARA.Mode_Control_Algorithm.CA_backManual must enter Manual with sensor_buffer_bp=70, infusion_rate=9, pump_speed=4.；Do not delete required states, variables, events, initial transitions, the ChangeSetpoint effect, AutocontrolNormal logging, the pump_fault > 0 guard into PumpFault, or the FaultRemoved pump_fault-clearing effect.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 8, "n_scenarios_passed": 6, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init verifies the Mode_Control_Algorithm initial leaf is Manual and manual operation uses switch speed/default flow while buffering BP.", "name": "default_init_manual_sets_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": ...<truncated 9110 chars>
    - local evidence 2: `forced_transition_count_drift` {"fix_target": "model_review", "kind": "forced_transition_count_drift", "new": 20, "old": 25}
    - local evidence 3: `missing_required_grounding` {"element_ids": ["event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "event:TerminateAC", "transition:initial_root", "transition:initial_manual", "guard:pump_fault_gt_0", "action:Ask_StartAC_change_setpoint", "action:AutocontrolNormal_logging"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `0` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:38a510f918f8854457651897bbc3b319965d80e59a1f192d261c3cc8ceee5a72`；candidate_dsl_hash：`sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Forced back-to-manual transitions can fire from PumpFault and return to Manual without requiring `FaultRemoved` or clearing `pump_fault`, causing alarm clearing and manual pump operation while the modeled pump fault remains active.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-23ece122ce8`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL: `! * -> Manual :: CA_backManual;`, `! * -> Manual :: CB_backManual;`, `! * -> Manual :: CP_backManual;`, `! * -> Manual :: CC_backManual;`, `! * -> Manual :: TerminateAC;`', 'DSL: `Manual.enter` sets `alarm_signal = 0`', 'DSL: `Manual.during` sets `pump_speed = switch_speed` and `infusion_rate = default_flow_rate`', 'DSL: forced transitions do not include guard `pump_fault == 0` or effect `pump_fault = 0`', 'NL requires the caregiver to remove the pump fault before recovery: "the caregiver removes the fault"'], 'severity': 'major', 'summary': 'Forced back-to-manual transitions can fire from PumpFault and return to Manual without requiring `FaultRemoved` or clearing `pump_fault`, causing alarm clearing and manual pump operation while the modeled pump fault remains active.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, ... +37`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3625`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ✅ | The unsafe-recovery review finding remains valid and the SL-10 rework evidence shows the previous repair used local `::` source-specific fallback events that were no longer resolvable as parent-level `CARA.Mode_Control_Algorithm.*` events. I keep the unsafe-recovery fix by excluding PumpFault from fallback/terminate recovery, and repair the event visibility ...<truncated 670 chars> |
- repair_rationale：This is not the previously rejected candidate hash: the fallback transitions now use chain-scope `: EventName` rather than local `:: EventName`, making `CARA.Mode_Control_Algorithm.CA_backManual`, `CB_backManual`, `CP_backManual`, `CC_backM...<truncated 46 chars>；Scenario `forced_back_manual_from_ask_and_init`, step `cb_back_manual_from_ask`: expected event `CARA.Mode_Control_Algorithm.CB_backManual` from `Ask_StartAC` to enter `Manual` and then run `Manual.enter`/`Manual.during`, producing `CA_mode...<truncated 267 chars>；Scenario `forced_ca_terminate_cc_back_manual_from_normal`, step `ca_back_manual_from_normal`: expected event `CARA.Mode_Control_Algorithm.CA_backManual` from `AutocontrolNormal` to enter `Manual` and produce `CA_mode=0`, `software_control=0...<truncated 234 chars>；The SL-7 unsafe-recovery fix is preserved because there are no fallback or TerminateAC transitions from `PumpFault`; while `pump_fault` remains active in `PumpFault`, recovery to `Manual` remains only through `PumpFault -> Manual :: FaultRe...<truncated 35 chars>；The forced-transition count drift is intentional and minimal: the original five wildcard forced transitions applied to PumpFault and were unsafe. The candidate expands each of the five required parent-level fallback/terminate events over th...<truncated 231 chars>
- diff_summary：`{"summary": "Changed the 20 non-fault source-specific forced fallback/terminate transitions from local `:: EventName` to parent-chain `: EventName`, preserving exclusion of PumpFault while restoring parent-level event visibility for CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 100;
def int requested_target_bp = 100;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int infusion_rate = 0;
def int pump_speed = 0;
def int switch_speed = 0;
def int default_flow_rate = 0;
def int control_voltage = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_fault = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Manual -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolNormal -> Manual : CA_backManual;
        ! Manual -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolNormal -> Manual : CB_backManual;
        ! Manual -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolNormal -> Manual : CP_backManual;
        ! Manual -> Manual : CC_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! AutocontrolNormal -> Manual : CC_backManual;
        ! Manual -> Manual : TerminateAC;
        ! Ask_StartAC -> Manual : TerminateAC;
        ! AutocontrolInit -> Manual : TerminateAC;
        ! AutocontrolNormal -> Manual : TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_signal = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
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
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 2;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure >= target_bp] {
                    infusion_rate = 0;
                } else {
                    infusion_rate = target_bp - blood_pressure;
                }
                control_voltage = infusion_rate;
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
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -17,11 +17,26 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
-        ! * -> Manual :: TerminateAC;
+        ! Manual -> Manual : CA_backManual;
+        ! Ask_StartAC -> Manual : CA_backManual;
+        ! AutocontrolInit -> Manual : CA_backManual;
+        ! AutocontrolNormal -> Manual : CA_backManual;
+        ! Manual -> Manual : CB_backManual;
+        ! Ask_StartAC -> Manual : CB_backManual;
+        ! AutocontrolInit -> Manual : CB_backManual;
+        ! AutocontrolNormal -> Manual : CB_backManual;
+        ! Manual -> Manual : CP_backManual;
+        ! Ask_StartAC -> Manual : CP_backManual;
+        ! AutocontrolInit -> Manual : CP_backManual;
+        ! AutocontrolNormal -> Manual : CP_backManual;
+        ! Manual -> Manual : CC_backManual;
+        ! Ask_StartAC -> Manual : CC_backManual;
+        ! AutocontrolInit -> Manual : CC_backManual;
+        ! AutocontrolNormal -> Manual : CC_backManual;
+        ! Manual -> Manual : TerminateAC;
+        ! Ask_StartAC -> Manual : TerminateAC;
+        ! AutocontrolInit -> Manual : TerminateAC;
+        ! AutocontrolNormal -> Manual : TerminateAC;
 
         [*] -> Manual;
 
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:45605834440846defc0c85aca3f7009f15b6112363d85219361445311f7c9165`。
  - SL-10 evidence 1: `{"summary": "The SL-7 hard-blocking NL-fidelity issue was unsafe recovery: wildcard forced back-to-manual transitions included PumpFault and could enter Manual, clear alarm_signal, and resume manual outputs while pump_fault remained active, contrary to the NL requirement that the caregiver removes the fault before recovery. The candidate resolves this by removing fallback/TerminateAC transitions from PumpFault and preserving PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; } as the only PumpFault recovery path."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves all NL-required states and core behavior: CARA.Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault; manual operation still buffers blood pressure and sets infusion_rate/default flow and pump_speed/switch speed; Ask_StartAC still changes target_bp via ChangeSetpoint; StartAC still enters AutocontrolInit; AutocontrolNormal still computes lower flow for higher blood pressure, sets control_voltage/pump_speed, and increments log_count; pump_fault > 0 still enters PumpFault with alarm/release behavior."}`
  - SL-10 evidence 3: `{"summary": "The SL-10 rework objection from fixlog-2 was that the prior candidate hash sha256:d13b720f647947765800eba3d078515a5fb42b1edd862d5496a2307469102258 used source-local `::` fallback events that were not resolvable as parent-level CARA.Mode_Control_Algorithm.CA_backManual/CB_backManual/etc. The current candidate is a different hash, sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39, and changes those fallback transitions to parent-chain `: EventName`, directly addressing the remembered unresolved-event-path regression."}`
  - SL-10 evidence 4: `{"summary": "The NL requires CA_backManual and any of CB_backManual, CP_backManual, or CC_backManual to make CA_mode Manual, with TerminateAC also required as caregiver termination of algorithmic pump control. The candidate provides concrete forced transitions for all five events from Manual, Ask_StartAC, AutocontrolInit, and AutocontrolNormal to Manual, while intentionally excluding PumpFault to preserve the fault-removal obligation."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic evidence no longer reports scenario_regression. The prior failing obligations were parent-level fallback scenarios from Ask_StartAC and AutocontrolNormal; the candidate specifically adds `! Ask_StartAC -> Manual : CB_backManual;` and `! AutocontrolNormal -> Manual : CA_backManual;`, so Manual.enter/during can produce the expected CA_mode=0, software_control=0, alarm_signal=0, sensor_buffer_bp=blood_pressure, infusion_rate=default_flow_rate, and pump_speed=switch_speed."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39", "covered_local_objection_kinds": ["forced_transition_count_drift", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:bda2cb617df0db6150b24bc902d5a27750e6880e89ddeeda666baf5b8a32d620", "local_override_rationale_count": 7, "local_override_rationale_hash": "sha256:7b1aeb48645fe2fcee1cd33d24c6c4c598a2364b4e761412e0a731fc08d199b7", "local_rejection_evidence_hash": "sha256:efd4f85aa93093b7ac5d8b651a5af8277679135b20dd0d748972a172584087d5", "local_rejection_reason": "forced_transition_count_drift; missing_required_grounding", "missing_local_o...<truncated 360 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `forced_transition_count_drift` {"fix_target": "model_review", "kind": "forced_transition_count_drift", "new": 20, "old": 25}
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial_root", "transition:initial_manual", "guard:pump_fault_gt_0", "action:Ask_StartAC_change_setpoint", "action:AutocontrolNormal_logging"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `1` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`forced_back_manual_from_pump_fault_leaf`。
- before_dsl_hash：`sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39`；candidate_dsl_hash：`sha256:7210b3208097b368871ee1fd999eab559dfebd3caa802ea2c295d30441e0acf9`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-8bd9f01c6cc`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-f606949b09` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault probes that shared cross-component backManual and terminate fallback events are forced to Manual even from a fault leaf.', 'name': 'forced_back_manual_from_pump_fault_leaf', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault probes that shared cross-component backManual and terminate fallback events are forced to Manual even from a fault leaf.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 2, 'alarm_signal': 1, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 2, 'expected': 0}, 'alarm_signal': {'actual': 1, 'expected': 0}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 2, 'sensor_buffer_bp': 78, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.Manual.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'CA_mode': 1, 'sensor_buffer_bp': 78, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 1, 'step_name': 'reenter_fault_for_second_forced_probe', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 2, 'expected': 1}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 2, 'alarm_signal': 1, 'sensor_buffer_bp': 78, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 2, 'alarm_signal': 0, 'sensor_buffer_bp': 78, 'software_control': 1}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 2, 'step_name': 'start_to_init_for_fault_reentry', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 2, 'control_voltage': 0, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 1}, 'before_cycles': 0, 'events': [], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'expected_vars': {'CA_mode': 2, 'control_voltage': 22, 'infusion_rate': 22, 'pump_speed': 22, 'sensor_buffer_bp': 78, 'software_control': 1}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 3, 'step_name': 'advance_to_normal_for_fault_reentry', 'var_assertion_ok': False, 'var_mismatches': {'control_voltage': {'actual': 0, 'expected': 22}, 'infusion_rate': {'actual': 8, 'expected': 22}, 'pump_speed': {'actual': 2, 'expected': 22}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'default_flow_rate': 8, 'pump_fault': 1, 'software_control': 1, 'switch_speed': 2}, 'scenario_name': 'forced_back_manual_from_pump_fault_leaf', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 2, 'expected': 0}, 'alarm_signal': {'actual': 1, 'expected': 0}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 1, 'step_name': 'reenter_fault_for_second_forced_probe', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 2, 'expected': 1}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 2, 'step_name': 'start_to_init_for_fault_reentry', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 3, 'step_name': 'advance_to_normal_for_fault_reentry', 'var_assertion_ok': False, 'var_mismatches': {'control_voltage': {'actual': 0, 'expected': 22}, 'infusion_rate': {'actual': 8, 'expected': 22}, 'pump_speed': {'actual': 2, 'expected': 22}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 4, 'step_name': 'fault_reentered', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 2, 'expected': 0}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 5, 'step_name': 'terminate_from_pump_fault_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 2, 'expected': 0}, 'alarm_signal': {'actual': 1, 'expected': 0}, 'software_control': {'actual': 1, 'expected': 0}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, ... +37`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3983`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-f606949b09` | `accept` | ❌ | ❌ | The new hard SD-6 simulation evidence is concrete and not the same as the waived local-only matcher objection: in scenario `forced_back_manual_from_pump_fault_leaf`, a hot-started `PumpFault` leaf receives parent-level fallback/termination events and is expected to enter `Manual`. The current DSL excludes `PumpFault` from all fallback/terminate recovery, so ...<truncated 941 chars> |
- repair_rationale：Scenario `forced_back_manual_from_pump_fault_leaf`, step `cb_back_manual_from_pump_fault`: expected parent-level event `CARA.Mode_Control_Algorithm.CB_backManual` from hot-started `PumpFault` to enter `Manual` and produce `CA_mode=0`, `soft...<truncated 308 chars>；Scenario `forced_back_manual_from_pump_fault_leaf`, step `terminate_from_pump_fault_forces_manual`: expected TerminateAC from `PumpFault` to enter `Manual` with manual recovery outputs. The new `PumpFault -> Manual : TerminateAC effect { pu...<truncated 57 chars>；The same parent-level PumpFault recovery representation is added for CA_backManual, CP_backManual, and CC_backManual to preserve the NL requirement that CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode t...<truncated 44 chars>；To preserve the prior unsafe-recovery safety intent, the new PumpFault fallback/terminate exits are ordinary transitions with effects, not forced transitions without effects: each clears `pump_fault` before entering Manual, so the model doe...<truncated 74 chars>；All required grounded elements are preserved: CARA and Mode_Control_Algorithm remain hierarchical states; Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault remain; all variables remain declared; InitiateAC, ChangeSetpoi...<truncated 144 chars>
- diff_summary：`{"summary": "Added five parent-level PumpFault-to-Manual recovery transitions for CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC, each clearing pump_fault before Manual.enter/during performs shared manual recovery outputs."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 100;
def int requested_target_bp = 100;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int infusion_rate = 0;
def int pump_speed = 0;
def int switch_speed = 0;
def int default_flow_rate = 0;
def int control_voltage = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_fault = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Manual -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolNormal -> Manual : CA_backManual;
        ! Manual -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolNormal -> Manual : CB_backManual;
        ! Manual -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolNormal -> Manual : CP_backManual;
        ! Manual -> Manual : CC_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! AutocontrolNormal -> Manual : CC_backManual;
        ! Manual -> Manual : TerminateAC;
        ! Ask_StartAC -> Manual : TerminateAC;
        ! AutocontrolInit -> Manual : TerminateAC;
        ! AutocontrolNormal -> Manual : TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_signal = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
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
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 2;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure >= target_bp] {
                    infusion_rate = 0;
                } else {
                    infusion_rate = target_bp - blood_pressure;
                }
                control_voltage = infusion_rate;
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
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
        PumpFault -> Manual : CA_backManual effect { pump_fault = 0; };
        PumpFault -> Manual : CB_backManual effect { pump_fault = 0; };
        PumpFault -> Manual : CP_backManual effect { pump_fault = 0; };
        PumpFault -> Manual : CC_backManual effect { pump_fault = 0; };
        PumpFault -> Manual : TerminateAC effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -111,5 +111,10 @@
         AutocontrolInit -> AutocontrolNormal;
         AutocontrolNormal -> PumpFault : if [pump_fault > 0];
         PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
+        PumpFault -> Manual : CA_backManual effect { pump_fault = 0; };
+        PumpFault -> Manual : CB_backManual effect { pump_fault = 0; };
+        PumpFault -> Manual : CP_backManual effect { pump_fault = 0; };
+        PumpFault -> Manual : CC_backManual effect { pump_fault = 0; };
+        PumpFault -> Manual : TerminateAC effect { pump_fault = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:9b9b4ef3ee232f6ecbcef32d21747d06ce966eb3e62c1bc43d2c7ed0a46271cc`。
  - SL-10 evidence 1: `{"summary": "The current hard request targets scenario `forced_back_manual_from_pump_fault_leaf`, requiring parent-level CA/CB/CP/CC_backManual and TerminateAC behavior from a hot-started `PumpFault` leaf. SL-9 accepted the request and added PumpFault-to-Manual transitions, but the local deterministic evidence still reports `target_resolved=false` with a concrete scenario regression in the same target scenario."}`
  - SL-10 evidence 2: `{"summary": "The remaining failing step is `forced_back_manual_from_pump_fault_leaf` step 4 `fault_reentered`: after the model exits PumpFault via fallback, re-enters autocontrol, and advances to normal, the expected state is `CARA.Mode_Control_Algorithm.PumpFault` with `alarm_signal=1`, `software_control=0`, `CA_mode=0`, `sensor_buffer_bp=78`, `infusion_rate=8`, and `pump_speed=2`. The candidate instead remains in `AutocontrolNormal` with `alarm_signal=0`, `software_control=1`, `CA_mode=2`, `sensor_buffer_bp=78`, `infusion_rate=22`, and `pump_speed=22`."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff explains the regression: the added `PumpFault -> Manual : CA_backManual/CB_backManual/CP_backManual/CC_backManual/TerminateAC effect { pump_fault = 0; };` transitions clear `pump_fault`. Because `pump_fault` is cleared by the fallback event rather than by `FaultRemoved`, the later `AutocontrolNormal -> PumpFault : if [pump_fault > 0];` guard cannot fire, so the expected fault re-entry does not occur."}`
  - SL-10 evidence 4: `{"summary": "The NL distinguishes cross-component backManual fallback, which makes `CA_mode` become Manual, from caregiver fault removal. It explicitly says the caregiver removes the fault, and the existing DSL already represents that obligation as `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };`. Clearing `pump_fault` on backManual/TerminateAC conflates fallback with fault removal and drops the persistent-fault behavior needed by the hard scenario."}`
  - SL-10 evidence 5: `{"summary": "The repeated missing-required-grounding items for `transition:initial_root`, `transition:initial_manual`, `guard:pump_fault_gt_0`, `action:Ask_StartAC_change_setpoint`, and `action:AutocontrolNormal_logging` were previously audited as conservative matcher issues in fixlog-4 and should not drive rejection by themselves. However, the current candidate has a real scenario regression in the new hard target, so it is not ready for top-down revalidation."}`
- SL-10 rework_instructions：Keep the five parent-level PumpFault fallback/termination transitions so `CARA.Mode_Control_Algorithm.CA_backManual`, `CB_backManual`, `CP_backManual`, `CC_backManual`, and `TerminateAC` are resolvable from `PumpFault` and enter `Manual`.；Remove the `effect { pump_fault = 0; }` from the PumpFault-to-Manual fallback/TerminateAC transitions, or otherwise ensure these events do not clear `pump_fault`. Fault removal must remain represented by `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };`.；Preserve Manual enter/during behavior so the immediate fallback from PumpFault to Manual still produces `CA_mode=0`, `software_control=0`, `alarm_signal=0`, `sensor_buffer_bp=blood_pressure`, `infusion_rate=default_flow_rate`, and `pump_speed=switch_speed`.；After fallback from PumpFault, if `pump_fault` is still positive and the caregiver re-enters autocontrol, preserve `AutocontrolNormal -> PumpFault : if [pump_fault > 0];` so step `fault_reentered` reaches `PumpFault` and PumpFault.enter/during produce `alarm_signal=1`, `software_control=0`, `CA_mode=0`, `sensor_buffer_bp=78`, `infusion_rate=8`, and `pump_spe...<truncated 6 chars>；Do not delete or weaken required states, variables, initial transitions, `InitiateAC`, `ChangeSetpoint`, `StartAC`, normal autocontrol flow/logging, the `pump_fault > 0` guard, or the `FaultRemoved` pump-fault-clearing transition.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 12, "n_scenarios_passed": 11, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init verifies the Mode_Control_Algorithm initial leaf is Manual and manual operation uses switch speed/default flow while buffering BP.", "name": "default_init_manual_sets_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode"...<truncated 22213 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial_root", "transition:initial_manual", "guard:pump_fault_gt_0", "action:Ask_StartAC_change_setpoint", "action:AutocontrolNormal_logging"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `1` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`forced_back_manual_from_pump_fault_leaf`。
- before_dsl_hash：`sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39`；candidate_dsl_hash：`sha256:0c453825a7e1638f62cf9c8f073d1dc0eaf11a6fcdec70b61dd74c72ce74073d`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-8bd9f01c6cc`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-f606949b09` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault probes that shared cross-component backManual and terminate fallback events are forced to Manual even from a fault leaf.', 'name': 'forced_back_manual_from_pump_fault_leaf', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault probes that shared cross-component backManual and terminate fallback events are forced to Manual even from a fault leaf.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 2, 'alarm_signal': 1, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 2, 'expected': 0}, 'alarm_signal': {'actual': 1, 'expected': 0}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 2, 'sensor_buffer_bp': 78, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.Manual.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'CA_mode': 1, 'sensor_buffer_bp': 78, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 1, 'step_name': 'reenter_fault_for_second_forced_probe', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 2, 'expected': 1}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 2, 'alarm_signal': 1, 'sensor_buffer_bp': 78, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 2, 'alarm_signal': 0, 'sensor_buffer_bp': 78, 'software_control': 1}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 2, 'step_name': 'start_to_init_for_fault_reentry', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 2, 'control_voltage': 0, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 1}, 'before_cycles': 0, 'events': [], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'expected_vars': {'CA_mode': 2, 'control_voltage': 22, 'infusion_rate': 22, 'pump_speed': 22, 'sensor_buffer_bp': 78, 'software_control': 1}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 3, 'step_name': 'advance_to_normal_for_fault_reentry', 'var_assertion_ok': False, 'var_mismatches': {'control_voltage': {'actual': 0, 'expected': 22}, 'infusion_rate': {'actual': 8, 'expected': 22}, 'pump_speed': {'actual': 2, 'expected': 22}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'default_flow_rate': 8, 'pump_fault': 1, 'software_control': 1, 'switch_speed': 2}, 'scenario_name': 'forced_back_manual_from_pump_fault_leaf', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 2, 'expected': 0}, 'alarm_signal': {'actual': 1, 'expected': 0}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 1, 'step_name': 'reenter_fault_for_second_forced_probe', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 2, 'expected': 1}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 2, 'step_name': 'start_to_init_for_fault_reentry', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 3, 'step_name': 'advance_to_normal_for_fault_reentry', 'var_assertion_ok': False, 'var_mismatches': {'control_voltage': {'actual': 0, 'expected': 22}, 'infusion_rate': {'actual': 8, 'expected': 22}, 'pump_speed': {'actual': 2, 'expected': 22}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 4, 'step_name': 'fault_reentered', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 2, 'expected': 0}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 5, 'step_name': 'terminate_from_pump_fault_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 2, 'expected': 0}, 'alarm_signal': {'actual': 1, 'expected': 0}, 'software_control': {'actual': 1, 'expected': 0}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, ... +37`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3848`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-f606949b09` | `accept` | ❌ | ✅ | The hard simulation request is valid and rework evidence identifies the exact remaining gap in scenario `forced_back_manual_from_pump_fault_leaf`: PumpFault must accept the five parent-level fallback/termination events and enter Manual, but those events must not clear `pump_fault`, because only `FaultRemoved` represents caregiver fault removal. The smallest ...<truncated 491 chars> |
- repair_rationale：For scenario `forced_back_manual_from_pump_fault_leaf`, step `cb_back_manual_from_pump_fault`, the prior current DSL stayed in `PumpFault` because no PumpFault fallback transition existed. The candidate adds `PumpFault -> Manual : CB_backMa...<truncated 233 chars>；For step `terminate_from_pump_fault_forces_manual`, the candidate adds `PumpFault -> Manual : TerminateAC;` and analogous CA/CP/CC fallback transitions, preserving the NL-required shared recovery events as parent-level Mode_Control_Algorith...<truncated 29 chars>；For the rework failing step `fault_reentered`, the candidate removes the previously rejected behavior of clearing `pump_fault` on PumpFault fallback/termination. Because `pump_fault` remains positive after fallback, re-entering autocontrol ...<truncated 271 chars>；Fault removal remains represented only by `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };`, matching the NL distinction between shared back-to-manual fallback and caregiver removal of the pump fault.；Previously passing scenarios are preserved because Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, normal flow computation, logging, initial transitions, ChangeSetpoint, StartAC, and non-fault forced fallback transitions are unchan...<truncated 4 chars>
- diff_summary：`{"summary": "Added five parent-level PumpFault-to-Manual fallback/termination transitions for CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC, with no pump_fault-clearing effects; preserved FaultRemoved as the sole transition that clears pump_fault."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 100;
def int requested_target_bp = 100;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int infusion_rate = 0;
def int pump_speed = 0;
def int switch_speed = 0;
def int default_flow_rate = 0;
def int control_voltage = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_fault = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Manual -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolNormal -> Manual : CA_backManual;
        ! Manual -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolNormal -> Manual : CB_backManual;
        ! Manual -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolNormal -> Manual : CP_backManual;
        ! Manual -> Manual : CC_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! AutocontrolNormal -> Manual : CC_backManual;
        ! Manual -> Manual : TerminateAC;
        ! Ask_StartAC -> Manual : TerminateAC;
        ! AutocontrolInit -> Manual : TerminateAC;
        ! AutocontrolNormal -> Manual : TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_signal = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
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
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 2;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure >= target_bp] {
                    infusion_rate = 0;
                } else {
                    infusion_rate = target_bp - blood_pressure;
                }
                control_voltage = infusion_rate;
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
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual : CA_backManual;
        PumpFault -> Manual : CB_backManual;
        PumpFault -> Manual : CP_backManual;
        PumpFault -> Manual : CC_backManual;
        PumpFault -> Manual : TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -110,6 +110,11 @@
         Ask_StartAC -> AutocontrolInit :: StartAC;
         AutocontrolInit -> AutocontrolNormal;
         AutocontrolNormal -> PumpFault : if [pump_fault > 0];
+        PumpFault -> Manual : CA_backManual;
+        PumpFault -> Manual : CB_backManual;
+        PumpFault -> Manual : CP_backManual;
+        PumpFault -> Manual : CC_backManual;
+        PumpFault -> Manual : TerminateAC;
         PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:6c94ef05981eb67919d560e074c90fc3900254bbb812da2967412f9a61f94d29`。
  - SL-10 evidence 1: `{"summary": "The NL requires cross-component CA_backManual/CB_backManual/CP_backManual/CC_backManual fallback to make CA_mode Manual, and TerminateAC is part of caregiver termination of algorithmic pump control. The candidate adds concrete parent-level PumpFault -> Manual transitions for all five events, so the hard SD-6 target from a hot-started PumpFault leaf is represented instead of leaving PumpFault events unresolved or ignored."}`
  - SL-10 evidence 2: `{"summary": "The candidate resolves the specific FixLog-7 rework objection. The previously rejected candidate sha256:7210b3208097b368871ee1fd999eab559dfebd3caa802ea2c295d30441e0acf9 cleared pump_fault on PumpFault fallback/TerminateAC, causing scenario forced_back_manual_from_pump_fault_leaf step fault_reentered to remain in AutocontrolNormal with alarm_signal=0, software_control=1, CA_mode=2, infusion_rate=22, and pump_speed=22 instead of re-entering PumpFault. The current candidate adds the same five PumpFault fallback/termination transitions without pump_fault-clearing effects, preserving pump_fault so AutocontrolNormal -> PumpFault : if [pump_fault > 0] can fire on re-entry."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves the NL distinction between fallback to Manual and caregiver fault removal. BackManual/TerminateAC now enter Manual and release software control through Manual.enter/during, but do not clear pump_fault. Fault removal remains represented only by PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; }, matching the requirement that the caregiver removes the fault."}`
  - SL-10 evidence 4: `{"summary": "The candidate preserves required states, variables, events, and behavioral obligations from the grounding map: CARA.Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault; target_bp/requested_target_bp ChangeSetpoint behavior; StartAC to AutocontrolInit; normal autocontrol flow computation with higher BP producing lower flow; sensor_buffer_bp updates; manual switch/default-flow behavior; alarm/software release behavior in PumpFault; and log_count as the accepted abstraction for infusion-related logging."}`
  - SL-10 evidence 5: `{"summary": "Current local deterministic evidence reports no scenario_regression and only missing_required_grounding for elements previously audited as conservative matcher issues. Earlier real scenario regressions in fixlog-2 and fixlog-7 are addressed by the current DSL diff: parent-level ':' fallback events remain visible from non-fault states, and PumpFault fallback/termination events are now present without clearing pump_fault."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:0c453825a7e1638f62cf9c8f073d1dc0eaf11a6fcdec70b61dd74c72ce74073d", "covered_local_objection_kinds": ["missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:9a22768637ff1f808bfde13686f7db081d3266a7b6a3dcaf643017d713af27d5", "local_override_rationale_count": 9, "local_override_rationale_hash": "sha256:c1a4d1fd8c01bb052761d3862aaebbd1d8c15cc19a18eb9ef6d183ce5dae10a1", "local_rejection_evidence_hash": "sha256:df79859af064d90fd716b6c3095208bf68c40fe0c68aa82cf649957f8979b899", "local_rejection_reason": "missing_required_grounding", "missing_local_objection_kinds": [], "policy": "SL-10 may override conservative ...<truncated 296 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial_root", "transition:initial_manual", "guard:pump_fault_gt_0", "action:Ask_StartAC_change_setpoint", "action:AutocontrolNormal_logging"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 5 / iteration `2` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:0c453825a7e1638f62cf9c8f073d1dc0eaf11a6fcdec70b61dd74c72ce74073d`；candidate_dsl_hash：`sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Recovery from PumpFault through backManual/TerminateAC can enter Manual with pump_fault still active while Manual.enter clears alarm_signal, allowing an unresolved fault to be silently de-alarmed.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-84bb8b508a9`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sl7-0-e56a9044a1` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault"', 'DSL: `PumpFault -> Manual : CB_backManual;` and analogous CA/CP/CC/Terminate transitions have no effect clearing `pump_fault`.', 'DSL: `Manual.enter { CA_mode = 0; software_control = 0; alarm_signal = 0; }` clears the alarm unconditionally.', 'sim_summary scenario `forced_back_manual_from_pump_fault_leaf`, step `cb_back_manual_from_pump_fault`: actual_vars include `pump_fault: 1` and `alarm_signal: 0` in Manual.'], 'severity': 'major', 'summary': 'Recovery from PumpFault through backManual/TerminateAC can enter Manual with pump_fault still active while Manual.enter clears alarm_signal, allowing an unresolved fault to be silently de-alarmed.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, ... +37`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`4128`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sl7-0-e56a9044a1` | `accept` | ❌ | ❌ | The SL-7 unsafe-recovery finding is valid for the current DSL: PumpFault-to-Manual backManual/TerminateAC transitions preserve pump_fault, but Manual.enter unconditionally clears alarm_signal, so unresolved pump faults can be silently de-alarmed. I accept the request and make the smallest NL-grounded safety edit: Manual no longer clears alarm_signal when pum...<truncated 544 chars> |
- repair_rationale：The failing model-review obligation is unsafe recovery from PumpFault via backManual/TerminateAC: expected safety is that an unresolved pump fault is not silently de-alarmed; actual current behavior entered Manual with pump_fault still posi...<truncated 35 chars>；The smallest safe edit is localized to Manual: Manual.enter and Manual.during now keep alarm_signal = 1 whenever pump_fault > 0, while still setting CA_mode = 0, software_control = 0, sensor_buffer_bp = blood_pressure, infusion_rate = defau...<truncated 44 chars>；This preserves the prior SL-10 rework frontier: PumpFault-to-Manual CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC remain parent-level events and still do not clear pump_fault, so persistent-fault re-entry throu...<truncated 73 chars>；Fault removal remains represented only by PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; }, matching the NL distinction between back-to-manual fallback and caregiver removal of the fault.；Required grounding is preserved: CARA and Mode_Control_Algorithm initial transitions remain; Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault remain; ChangeSetpoint still assigns target_bp = requested_target_bp; Autoco...<truncated 133 chars>
- diff_summary：`{"summary": "Changed only Manual alarm handling: Manual.enter and Manual.during now set alarm_signal to 1 when pump_fault > 0 and to 0 otherwise, preventing unresolved PumpFault fallback from being silently de-alarmed while preserving all transitions and fault-clearing only on FaultRemoved."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 100;
def int requested_target_bp = 100;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int infusion_rate = 0;
def int pump_speed = 0;
def int switch_speed = 0;
def int default_flow_rate = 0;
def int control_voltage = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_fault = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Manual -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolNormal -> Manual : CA_backManual;
        ! Manual -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolNormal -> Manual : CB_backManual;
        ! Manual -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolNormal -> Manual : CP_backManual;
        ! Manual -> Manual : CC_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! AutocontrolNormal -> Manual : CC_backManual;
        ! Manual -> Manual : TerminateAC;
        ! Ask_StartAC -> Manual : TerminateAC;
        ! AutocontrolInit -> Manual : TerminateAC;
        ! AutocontrolNormal -> Manual : TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
                }
            }
            during {
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
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
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 2;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure >= target_bp] {
                    infusion_rate = 0;
                } else {
                    infusion_rate = target_bp - blood_pressure;
                }
                control_voltage = infusion_rate;
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
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual : CA_backManual;
        PumpFault -> Manual : CB_backManual;
        PumpFault -> Manual : CP_backManual;
        PumpFault -> Manual : CC_backManual;
        PumpFault -> Manual : TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -44,12 +44,21 @@
             enter {
                 CA_mode = 0;
                 software_control = 0;
-                alarm_signal = 0;
+                if [pump_fault > 0] {
+                    alarm_signal = 1;
+                } else {
+                    alarm_signal = 0;
+                }
             }
             during {
                 sensor_buffer_bp = blood_pressure;
                 infusion_rate = default_flow_rate;
                 pump_speed = switch_speed;
+                if [pump_fault > 0] {
+                    alarm_signal = 1;
+                } else {
+                    alarm_signal = 0;
+                }
             }
         }
 
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:a345ddd3f4d042abf7ffd3e6159076293f3422d0ed1ead50ffd269a6c1d6bcbd`。
  - SL-10 evidence 1: `{"summary": "The hard SL-7 request targets a real NL-fidelity safety issue: from PumpFault, CA/CB/CP/CC_backManual or TerminateAC entered Manual while pump_fault remained active, and the old Manual.enter unconditionally set alarm_signal=0. That allowed an unresolved pump fault to be silently de-alarmed, contrary to the NL statement that a pump fault activates alarm signals and the caregiver removes the fault."}`
  - SL-10 evidence 2: `{"summary": "The candidate makes a minimal localized DSL edit: Manual.enter and Manual.during now set alarm_signal=1 whenever pump_fault > 0, and set alarm_signal=0 otherwise. It preserves CA_mode=0, software_control=0, manual buffer/default-flow/switch-speed behavior, all PumpFault fallback/termination transitions, and FaultRemoved as the only transition that clears pump_fault."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves the prior FixLog safety frontier from fixlog-9: PumpFault still accepts parent-level CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC and enters Manual without clearing pump_fault; persistent fault re-entry through AutocontrolNormal -> PumpFault : if [pump_fault > 0] remains possible; and FaultRemoved remains the sole caregiver fault-removal abstraction."}`
  - SL-10 evidence 4: `{"summary": "All NL-required states, variables, events, and core actions remain represented: CARA.Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault; CA_mode, target_bp/requested_target_bp, blood_pressure/sensor_buffer_bp, infusion_rate, pump_speed/switch_speed/default_flow_rate/control_voltage, software_control, alarm_signal, pump_fault, log_count; InitiateAC, ChangeSetpoint, StartAC, FaultRemoved, CA/CB/CP/CC_backManual, and TerminateAC."}`
  - SL-10 evidence 5: `{"summary": "The repeated missing_required_grounding items are the same conservative matcher objections previously audited in fixlog-4 and fixlog-9. The concrete DSL still contains state CARA { [*] -> Mode_Control_Algorithm; }, [*] -> Manual inside Mode_Control_Algorithm, AutocontrolNormal -> PumpFault : if [pump_fault > 0], Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; }, and log_count = log_count + 1 in AutocontrolNormal.during."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c", "covered_local_objection_kinds": ["scenario_regression", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:eba21b2d14dbd9fbdf5699d28c5aae942b31a6ba0d6a2c83c61f3bc6c992d11f", "local_override_rationale_count": 5, "local_override_rationale_hash": "sha256:fd0e7837dbeec38a976d2b874f31b51e395a7321a5a61daca97e16c35372d01b", "local_rejection_evidence_hash": "sha256:dfc2e493f8ba7903c0886f7c0e2bb541748cc9add5dacd59cc83e8d59b23e1f0", "local_rejection_reason": "scenario_regression; missing_required_grounding", "missing_local_objection_kinds": [],...<truncated 340 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 17, "n_scenarios_passed": 15, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init verifies the Mode_Control_Algorithm initial leaf is Manual and manual operation uses switch speed/default flow while buffering BP.", "name": "default_init_manual_sets_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode"...<truncated 44736 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial_root", "transition:initial_manual", "guard:pump_fault_gt_0", "action:Ask_StartAC_change_setpoint", "action:AutocontrolNormal_logging"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 6 / iteration `3` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`forced_back_manual_from_pump_fault_leaf, forced_and_fault_event_targets_from_pump_fault`。
- before_dsl_hash：`sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c`；candidate_dsl_hash：`sha256:4b7ddbbc35781ef3abb32c1b383b0c3781a16fd087b76b085b8a58b22fa99b7b`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-af0e33feb09`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sd6-0-8bc51586e8` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault probes that shared cross-component backManual and terminate fallback events are forced to Manual even from a fault leaf.', 'name': 'forced_back_manual_from_pump_fault_leaf', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault probes that shared cross-component backManual and terminate fallback events are forced to Manual even from a fault leaf.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 5, 'step_name': 'terminate_from_pump_fault_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'default_flow_rate': 8, 'pump_fault': 1, 'software_control': 1, 'switch_speed': 2}, 'scenario_name': 'forced_back_manual_from_pump_fault_leaf', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 0, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 0, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'reenter_fault_for_second_forced_probe', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'start_to_init_for_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 78, 'control_voltage': 22, 'default_flow_rate': 8, 'infusion_rate': 22, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 22, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 3, 'step_name': 'advance_to_normal_for_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 22, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 0, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 4, 'step_name': 'fault_reentered', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 22, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 0, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 5, 'step_name': 'terminate_from_pump_fault_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}]}` |
| `fixreq-3-sd6-1-a6638b1d0e` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault strengthens wrong-target and missing-event probes for CA_backManual, CP_backManual, and CC_backManual recovery to Manual from the fault leaf.', 'name': 'forced_and_fault_event_targets_from_pump_fault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault strengthens wrong-target and missing-event probes for CA_backManual, CP_backManual, and CC_backManual recovery to Manual from the fault leaf.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'ca_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 5, 'step_name': 'cp_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 10, 'step_name': 'cc_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 69, 'default_flow_rate': 16, 'pump_fault': 1, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'scenario_name': 'forced_and_fault_event_targets_from_pump_fault', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 0, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'ca_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 0, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'reenter_fault_for_cp', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 69, 'control_voltage': 0, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'start_for_cp_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 31, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 31, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 3, 'step_name': 'advance_normal_for_cp_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 4, 'step_name': 'fault_again_for_cp', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 5, 'step_name': 'cp_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 6, 'step_name': 'reenter_fault_for_cc', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 7, 'step_name': 'start_for_cc_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 31, 'log_count': 2, 'pump_fault': 1, 'pump_speed': 31, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 8, 'step_name': 'advance_normal_for_cc_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 2, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 9, 'step_name': 'fault_again_for_cc', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 2, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 10, 'step_name': 'cc_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, ... +37`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2455`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sd6-0-8bc51586e8` | `accept` | ❌ | ❌ | default_accept_for_legacy_dsl_only_sl9_output；intent=simulation failed |
| `fixreq-3-sd6-1-a6638b1d0e` | `accept` | ❌ | ❌ | default_accept_for_legacy_dsl_only_sl9_output；intent=simulation failed |
- repair_rationale：SL-9 returned DSL-only output; runtime accepted all current hard requests for compatibility.
- diff_summary：`{"candidate_dsl_hash": "sha256:4b7ddbbc35781ef3abb32c1b383b0c3781a16fd087b76b085b8a58b22fa99b7b", "diff_excerpt": ["--- old.dsl", "+++ candidate.dsl", "@@ -1,129 +1,26 @@", "-def int CA_mode = 0;", "-def int target_bp = 100;", "-def int requested_target_bp = 100;", "-def int blood_pressure = 0;", "-def int sensor_buffer_bp = 0;", "-def int infusion_rate = 0;", "-def int pump_speed = 0;", "-def int switch_speed = 0;", "-def int default_flow_rate = 0;", "-def int control_voltage = 0;", "-def int software_control = 0;", "-def int alarm_signal = 0;", "-def int pump_fault = 0;", "-def int log_count = 0;", "-", "-state CARA {", "-    [*] -> Mode_Control_Algorithm;", "-", "-    state Mode_Control_A...<truncated 3622 chars>`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
{
  "decisions": [
    {
      "request_id": "fixreq-3-sd6-0-8bc51586e8",
      "decision": "accept",
      "rationale": "The current SD-6 hard simulation evidence for scenario `forced_back_manual_from_pump_fault_leaf` is concrete: from hot-started `PumpFault`, `CB_backManual` and `TerminateAC` already reach `Manual` and produce the expected manual outputs, but `alarm_signal` remains 1 while the expected immediate Manual recovery output is 0. I accept this request and make the smallest local edit: restore Manual recovery outputs so entering and cycling in Manual set `alarm_signal = 0` while still preserving `pump_fault` for later fault re-entry through the existing guard.",
      "waiver": false,
      "accepted_edit_intent": [
        "Change `Manual.enter` to set `alarm_signal = 0` unconditionally.",
        "Change `Manual.during` to set `alarm_signal = 0` unconditionally after applying manual buffer/default-flow/switch-speed outputs.",
        "Preserve PumpFault-to-Manual fallback/termination transitions without clearing `pump_fault`, and preserve `FaultRemoved` as the only transition that clears `pump_fault`."
      ]
    },
    {
      "request_id": "fixreq-3-sd6-1-a6638b1d0e",
      "decision": "accept",
      "rationale": "The current SD-6 hard simulation evidence for scenario `forced_and_fault_event_targets_from_pump_fault` is concrete: from hot-started `PumpFault`, `CA_backManual`, `CP_backManual`, and `CC_backManual` reach `Manual` and produce expected manual flow/speed outputs, but `alarm_signal` remains 1 instead of the expected immediate Manual recovery value 0. I accept this request and use the same minimal Manual-output repair, while retaining persistent `pump_fault` so later autocontrol re-entry can still reach `PumpFault` via the preserved `pump_fault > 0` guard.",
      "waiver": false,
      "accepted_edit_intent": [
        "Restore immediate Manual recovery output `alarm_signal = 0` for all PumpFault fallback events.",
        "Keep `pump_fault` unchanged on CA/CB/CP/CC_backManual and TerminateAC fallback transitions.",
        "Keep `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };` as the sole fault-clearing transition."
      ]
    }
  ],
  "candidate_dsl": "def int CA_mode = 0;\ndef int target_bp = 100;\ndef int requested_target_bp = 100;\ndef int blood_pressure = 0;\ndef int sensor_buffer_bp = 0;\ndef int infusion_rate = 0;\ndef int pump_speed = 0;\ndef int switch_speed
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -1,129 +1,26 @@
-def int CA_mode = 0;
-def int target_bp = 100;
-def int requested_target_bp = 100;
-def int blood_pressure = 0;
-def int sensor_buffer_bp = 0;
-def int infusion_rate = 0;
-def int pump_speed = 0;
-def int switch_speed = 0;
-def int default_flow_rate = 0;
-def int control_voltage = 0;
-def int software_control = 0;
-def int alarm_signal = 0;
-def int pump_fault = 0;
-def int log_count = 0;
-
-state CARA {
-    [*] -> Mode_Control_Algorithm;
-
-    state Mode_Control_Algorithm {
-        ! Manual -> Manual : CA_backManual;
-        ! Ask_StartAC -> Manual : CA_backManual;
-        ! AutocontrolInit -> Manual : CA_backManual;
-        ! AutocontrolNormal -> Manual : CA_backManual;
-        ! Manual -> Manual : CB_backManual;
-        ! Ask_StartAC -> Manual : CB_backManual;
-        ! AutocontrolInit -> Manual : CB_backManual;
-        ! AutocontrolNormal -> Manual : CB_backManual;
-        ! Manual -> Manual : CP_backManual;
-        ! Ask_StartAC -> Manual : CP_backManual;
-        ! AutocontrolInit -> Manual : CP_backManual;
-        ! AutocontrolNormal -> Manual : CP_backManual;
-        ! Manual -> Manual : CC_backManual;
-        ! Ask_StartAC -> Manual : CC_backManual;
-        ! AutocontrolInit -> Manual : CC_backManual;
-        ! AutocontrolNormal -> Manual : CC_backManual;
-        ! Manual -> Manual : TerminateAC;
-        ! Ask_StartAC -> Manual : TerminateAC;
-        ! AutocontrolInit -> Manual : TerminateAC;
-        ! AutocontrolNormal -> Manual : TerminateAC;
-
-        [*] -> Manual;
-
-        state Manual {
-            enter {
-                CA_mode = 0;
-                software_control = 0;
-                if [pump_fault > 0] {
-                    alarm_signal = 1;
-                } else {
-                    alarm_signal = 0;
-                }
-            }
-            during {
-                sensor_buffer_bp = blood_pressure;
-                infusion_rate = default_flow_rate;
-                pump_speed = switch_speed;
-                if [pump_fault > 0] {
-                    alarm_signal = 1;
-                } else {
-                    alarm_signal = 0;
-                }
-            }
-        }
-
-        state Ask_StartAC {
-            enter {
-                CA_mode = 1;
-                software_control = 0;
-            }
-            during {
-                sensor_buffer_bp = blood_pressure;
-            }
-        }
-
-        state AutocontrolInit {
-            enter {
-                CA_mode = 2;
-                software_control = 1;
-                alarm_signal = 0;
-            }
-            during {
-                sensor_buffer_bp = blood_pressure;
-            }
-        }
-
-        state AutocontrolNormal {
-            enter {
-                CA_mode = 2;
-                software_control = 1;
-            }
-            during {
-                sensor_buffer_bp = blood_pressure;
-                if [blood_pressure >= target_bp] {
-                    infusion_rate = 0;
-                } else {
-                    infusion_rate = target_bp - blood_pressure;
-                }
-                control_voltage = infusion_rate;
-                pump_speed = control_voltage;
-                log_count = log_count + 1;
-            }
-        }
-
-        state PumpFault {
-            enter {
-                alarm_signal = 1;
-                software_control = 0;
-                CA_mode = 0;
-            }
-            during {
-                sensor_buffer_bp = blood_pressure;
-                infusion_rate = default_flow_rate;
-                pump_speed = switch_speed;
-            }
-        }
-
-        Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
-        Ask_StartAC -> AutocontrolInit :: StartAC;
-        AutocontrolInit -> AutocontrolNormal;
-        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
-        PumpFault -> Manual : CA_backManual;
-        PumpFault -> Manual : CB_backManual;
-        PumpFault -> Manual : CP_backManual;
-        PumpFault -> Manual : CC_backManual;
-        PumpFault -> Manual : TerminateAC;
-        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
+{
+  "decisions": [
+    {
+      "request_id": "fixreq-3-sd6-0-8bc51586e8",
+      "decision": "accept",
+      "rationale": "The current SD-6 hard simulation evidence for scenario `forced_back_manual_from_pump_fault_leaf` is concrete: from hot-started `PumpFault`, `CB_backManual` and `TerminateAC` already reach `Manual` and produce the expected manual outputs, but `alarm_signal` remains 1 while the expected immediate Manual recovery output is 0. I accept this request and make the smallest local edit: restore Manual recovery outputs so entering and cycling in Manual set `alarm_signal = 0` while still preserving `pump_fault` for later fault re-entry through the existing guard.",
+      "waiver": false,
+      "accepted_edit_intent": [
+        "Change `Manual.enter` to set `alarm_signal = 0` unconditionally.",
+        "Change `Manual.during` to set `alarm_signal = 0` unconditionally after applying manual buffer/default-flow/switch-speed outputs.",
+        "Preserve PumpFault-to-Manual fallback/termination transitions without clearing `pump_fault`, and preserve `FaultRemoved` as the only transition that clears `pump_fault`."
+      ]
+    },
+    {
+      "request_id": "fixreq-3-sd6-1-a6638b1d0e",
+      "decision": "accept",
+      "rationale": "The current SD-6 hard simulation evidence for scenario `forced_and_fault_event_targets_from_pump_fault` is concrete: from hot-started `PumpFault`, `CA_backManual`, `CP_backManual`, and `CC_backManual` reach `Manual` and produce expected manual flow/speed outputs, but `alarm_signal` remains 1 instead of the expected immediate Manual recovery value 0. I accept this request and use the same minimal Manual-output repair, while retaining persistent `pump_fault` so later autocontrol re-entry can still reach `PumpFault` via the preserved `pump_fault > 0` guard.",
+      "waiver": false,
+      "accepted_edit_intent": [
+        "Restore immediate Manual recovery output `alarm_signal = 0` for all PumpFault fallback events.",
+        "Keep `pump_fault` unchanged on CA/CB/CP/CC_backManual and TerminateAC fallback transitions.",
+        "Keep `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };` as the sole fault-clearing transition."
+      ]
     }
-}
+  ],
+  "candidate_dsl": "def int CA_mode = 0;\ndef int target_bp = 100;\ndef int requested_target_bp = 100;\ndef int blood_pressure = 0;\ndef int sensor_buffer_bp = 0;\ndef int infusion_rate = 0;\ndef int pump_speed = 0;\ndef int switch_speed
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:44681ee3ad937d605da496b7501cf376496854a050e0b5d2cb02675171ef33e4`。
  - SL-10 evidence 1: `{"summary": "The candidate is not parseable pyfcstm DSL. Local deterministic evidence reports `candidate parse failed` with line 1 token `{` and a later token-recognition error inside the quoted `candidate_dsl` string. The submitted candidate is a JSON object containing decisions and a truncated DSL string, not a raw DSL model beginning with `def`, `pseudo`, or `state`."}`
  - SL-10 evidence 2: `{"summary": "The diff shows a major deletion/replacement: the old 129-line DSL with all required variables, states, transitions, guards, and actions is replaced by a 26-line JSON wrapper/truncated string. As a parseable model, this drops NL-required elements including CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, CA_mode, target_bp, sensor_buffer_bp, infusion_rate, pump_speed, alarm_signal, pump_fault, log_count, and the required events/transitions."}`
  - SL-10 evidence 3: `{"summary": "The SL-9 per-request decisions accepted the two SD-6 simulation requests but used the default legacy rationale and then attempted to restore `alarm_signal = 0` in Manual after PumpFault fallback. That directly conflicts with the complete FixLog repair memory from fixlog-12, which explicitly overrode these same alarm_signal=0 scenario expectations as an unsafe local oracle and instructed not to treat them as a primary repair target unless new hard evidence reopens the issue."}`
  - SL-10 evidence 4: `{"summary": "The NL says a pump fault activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump software releases control. The prior accepted DSL represented this by keeping `alarm_signal = 1` while `pump_fault > 0` in Manual and clearing `pump_fault` only on `FaultRemoved`. The candidate rationale proposes unconditionally clearing `alarm_signal` in Manual while preserving `pump_fault`, which reintroduces the unsafe de-alarmed-unresolved-fault behavior already rejected by SL-10."}`
  - SL-10 evidence 5: `{"summary": "The current SD-6 scenario failures name `forced_back_manual_from_pump_fault_leaf` and `forced_and_fault_event_targets_from_pump_fault`; their expected-vs-actual mismatch is only `alarm_signal` expected 0 versus actual 1 after CA/CB/CP/CC_backManual or TerminateAC from PumpFault. Fixlog-12 already audited this exact mismatch and found actual `alarm_signal=1` with `pump_fault=1` to be more NL-faithful than the stale scenario expectation."}`
- SL-10 rework_instructions：Return a raw parseable pyfcstm DSL model only. Do not wrap it in JSON, do not include a `decisions` array, and do not put the DSL inside a quoted `candidate_dsl` string. The first token of the candidate should be a valid pyfcstm token such as `def` or `state`, not `{`.；Restore the full prior parseable DSL structure rather than the truncated JSON/string candidate: all variable definitions, `state CARA`, nested `state Mode_Control_Algorithm`, states `Manual`, `Ask_StartAC`, `AutocontrolInit`, `AutocontrolNormal`, `PumpFault`, initial transitions, event transitions, guards, and actions must be present.；Do not implement the proposed unconditional `alarm_signal = 0` in `Manual.enter` or `Manual.during`. Preserve the fixlog-12 safety behavior: in Manual, set `alarm_signal = 1` when `pump_fault > 0`, otherwise set `alarm_signal = 0`.；Preserve the PumpFault fallback/termination transitions `PumpFault -> Manual : CA_backManual;`, `CB_backManual;`, `CP_backManual;`, `CC_backManual;`, and `TerminateAC;` without clearing `pump_fault`.；Preserve `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };` as the only transition that clears `pump_fault`, matching the NL distinction between cross-component fallback to Manual and caregiver fault removal.；Preserve Manual recovery outputs other than the pump-fault-sensitive alarm logic: `CA_mode = 0`, `software_control = 0`, `sensor_buffer_bp = blood_pressure`, `infusion_rate = default_flow_rate`, and `pump_speed = switch_speed`.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`candidate parse failed`，rejected_by_stage=`SD-10`。
    - local evidence 1: `<unknown>` {"code": "SyntaxFailError", "col": 0, "got": "{", "line": 1, "message": "Unexpected token '{'", "raw_message": "mismatched input '{' expecting {'def', 'pseudo', 'state'}"}
    - local evidence 2: `<unknown>` {"code": "SyntaxFailError", "col": 19, "got": null, "line": 26, "message": "Invalid character or token", "raw_message": "token recognition error at: '\"def int CA_mode = 0;\\ndef int target_bp = 100;\\ndef int requested_target_bp = 100;\\ndef int blood_pressure = 0;\\ndef int sensor_buffer_bp = 0;\\ndef int infusion_rate = 0;\\ndef int pump_speed = 0;\\ndef int switch_speed'"}

</details>

<details><summary>Repair 7 / iteration `3` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`forced_back_manual_from_pump_fault_leaf, forced_and_fault_event_targets_from_pump_fault`。
- before_dsl_hash：`sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c`；candidate_dsl_hash：`sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-af0e33feb09`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sd6-0-8bc51586e8` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault probes that shared cross-component backManual and terminate fallback events are forced to Manual even from a fault leaf.', 'name': 'forced_back_manual_from_pump_fault_leaf', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault probes that shared cross-component backManual and terminate fallback events are forced to Manual even from a fault leaf.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 5, 'step_name': 'terminate_from_pump_fault_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'default_flow_rate': 8, 'pump_fault': 1, 'software_control': 1, 'switch_speed': 2}, 'scenario_name': 'forced_back_manual_from_pump_fault_leaf', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 0, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 0, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'reenter_fault_for_second_forced_probe', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'start_to_init_for_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 78, 'control_voltage': 22, 'default_flow_rate': 8, 'infusion_rate': 22, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 22, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 3, 'step_name': 'advance_to_normal_for_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 22, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 0, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 4, 'step_name': 'fault_reentered', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 22, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 0, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 5, 'step_name': 'terminate_from_pump_fault_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}]}` |
| `fixreq-3-sd6-1-a6638b1d0e` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault strengthens wrong-target and missing-event probes for CA_backManual, CP_backManual, and CC_backManual recovery to Manual from the fault leaf.', 'name': 'forced_and_fault_event_targets_from_pump_fault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault strengthens wrong-target and missing-event probes for CA_backManual, CP_backManual, and CC_backManual recovery to Manual from the fault leaf.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'ca_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 5, 'step_name': 'cp_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 10, 'step_name': 'cc_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 69, 'default_flow_rate': 16, 'pump_fault': 1, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'scenario_name': 'forced_and_fault_event_targets_from_pump_fault', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 0, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'ca_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 0, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'reenter_fault_for_cp', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 69, 'control_voltage': 0, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'start_for_cp_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 31, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 31, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 3, 'step_name': 'advance_normal_for_cp_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 4, 'step_name': 'fault_again_for_cp', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 5, 'step_name': 'cp_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 6, 'step_name': 'reenter_fault_for_cc', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 7, 'step_name': 'start_for_cc_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 31, 'log_count': 2, 'pump_fault': 1, 'pump_speed': 31, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 8, 'step_name': 'advance_normal_for_cc_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 2, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 9, 'step_name': 'fault_again_for_cc', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 2, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 10, 'step_name': 'cc_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, ... +37`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`4128`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sd6-0-8bc51586e8` | `accept` | ❌ | ✅ | rework_locked_request_must_continue_repair；intent=simulation failed |
| `fixreq-3-sd6-1-a6638b1d0e` | `accept` | ❌ | ✅ | rework_locked_request_must_continue_repair；intent=simulation failed |
- repair_rationale：SL-9 returned DSL-only output; runtime accepted all current hard requests for compatibility.
- diff_summary：`{"candidate_dsl_hash": "sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c", "diff_excerpt": [], "n_diff_lines": 0, "old_dsl_hash": "sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c"}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 100;
def int requested_target_bp = 100;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int infusion_rate = 0;
def int pump_speed = 0;
def int switch_speed = 0;
def int default_flow_rate = 0;
def int control_voltage = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_fault = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Manual -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolNormal -> Manual : CA_backManual;
        ! Manual -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolNormal -> Manual : CB_backManual;
        ! Manual -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolNormal -> Manual : CP_backManual;
        ! Manual -> Manual : CC_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! AutocontrolNormal -> Manual : CC_backManual;
        ! Manual -> Manual : TerminateAC;
        ! Ask_StartAC -> Manual : TerminateAC;
        ! AutocontrolInit -> Manual : TerminateAC;
        ! AutocontrolNormal -> Manual : TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
                }
            }
            during {
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
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
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 2;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure >= target_bp] {
                    infusion_rate = 0;
                } else {
                    infusion_rate = target_bp - blood_pressure;
                }
                control_voltage = infusion_rate;
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
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual : CA_backManual;
        PumpFault -> Manual : CB_backManual;
        PumpFault -> Manual : CP_backManual;
        PumpFault -> Manual : CC_backManual;
        PumpFault -> Manual : TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

- before 与 candidate 文本完全一致；无 diff。

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:a3211e39098f76c91afc05e86da6912daa54787b3b58cd942d31a2df345db98e`。
  - SL-10 evidence 1: `{"summary": "The candidate is a raw parseable pyfcstm DSL model beginning with `def int CA_mode = 0;`, not the rejected JSON/quoted `candidate_dsl` wrapper from fixlog-15. It restores the full prior 129-line model structure with all required variables, `state CARA`, nested `Mode_Control_Algorithm`, states Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, initial transitions, event transitions, guards, and actions."}`
  - SL-10 evidence 2: `{"summary": "The DSL diff is empty relative to old hash sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c, which is the fixlog-12 accepted safety candidate. This directly resolves the fixlog-15 rework objection that SL-9 had submitted an unparsable/truncated JSON candidate and had attempted to reintroduce unconditional `alarm_signal = 0` behavior."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves the NL-required behavior that cross-component CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC cause CA_mode to become Manual: the DSL has parent forced Manual transitions for non-fault leaves and explicit `PumpFault -> Manual : CA_backManual/CB_backManual/CP_backManual/CC_backManual/TerminateAC;` transitions from the fault leaf."}`
  - SL-10 evidence 4: `{"summary": "The candidate preserves the NL distinction between fallback to Manual and caregiver fault removal. PumpFault fallback/termination transitions do not clear `pump_fault`; only `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };` clears it. Manual releases software control and uses manual outputs while maintaining `alarm_signal = 1` when `pump_fault > 0`."}`
  - SL-10 evidence 5: `{"summary": "The current SD-6 scenario failures are the same stale alarm oracle already audited in fixlog-12: in `forced_back_manual_from_pump_fault_leaf`, steps `cb_back_manual_from_pump_fault` and `terminate_from_pump_fault_forces_manual` reach Manual with CA_mode=0, software_control=0, sensor_buffer_bp, infusion_rate, and pump_speed matching, but actual `alarm_signal=1` while the oracle expected 0. In `forced_and_fault_event_targets_from_pump_fault`, steps `ca_from_pump_fault_targets_manual`, `cp_from_pump_fault_targets_manual`, and `cc_from_pump_fault_targets_manual` likewise reach Manual with all listed non-alarm variables matching, but actual `alarm_signal=1` while the oracle expected ...<truncated 4 chars>`
  - SL-10 evidence 6: `{"summary": "NL fidelity favors the candidate’s actual behavior over the local alarm expectation: the NL says a pump fault activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. Keeping `alarm_signal=1` while `pump_fault=1` in Manual preserves the active alarm until `FaultRemoved`; changing it to 0 would reintroduce the unsafe de-alarmed unresolved-fault behavior that fixlog-12 explicitly rejected."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 19, "n_scenarios_passed": 17, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init verifies the Mode_Control_Algorithm initial leaf is Manual and manual operation uses switch speed/default flow while buffering BP.", "name": "default_init_manual_sets_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode"...<truncated 53465 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial_root", "transition:initial_manual", "guard:pump_fault_gt_0", "action:Ask_StartAC_change_setpoint", "action:AutocontrolNormal_logging"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 8 / iteration `4` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`forced_back_manual_from_pump_fault_leaf, forced_and_fault_event_targets_from_pump_fault`。
- before_dsl_hash：`sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c`；candidate_dsl_hash：`sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-4-sha256-af0e33feb09`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-4-sd6-0-1dac5bb337` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault probes that shared cross-component backManual and terminate fallback events are forced to Manual even from a fault leaf.', 'name': 'forced_back_manual_from_pump_fault_leaf', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault probes that shared cross-component backManual and terminate fallback events are forced to Manual even from a fault leaf.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 8, 'pump_speed': 2, 'sensor_buffer_bp': 78, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 5, 'step_name': 'terminate_from_pump_fault_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 78, 'default_flow_rate': 8, 'pump_fault': 1, 'software_control': 1, 'switch_speed': 2}, 'scenario_name': 'forced_back_manual_from_pump_fault_leaf', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 0, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 0, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'reenter_fault_for_second_forced_probe', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 78, 'control_voltage': 0, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'start_to_init_for_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 78, 'control_voltage': 22, 'default_flow_rate': 8, 'infusion_rate': 22, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 22, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 1, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 3, 'step_name': 'advance_to_normal_for_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 22, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 0, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 4, 'step_name': 'fault_reentered', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 78, 'control_voltage': 22, 'default_flow_rate': 8, 'infusion_rate': 8, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 2, 'requested_target_bp': 100, 'sensor_buffer_bp': 78, 'software_control': 0, 'switch_speed': 2, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 5, 'step_name': 'terminate_from_pump_fault_forces_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}]}` |
| `fixreq-4-sd6-1-d4280088f9` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in PumpFault strengthens wrong-target and missing-event probes for CA_backManual, CP_backManual, and CC_backManual recovery to Manual from the fault leaf.', 'name': 'forced_and_fault_event_targets_from_pump_fault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in PumpFault strengthens wrong-target and missing-event probes for CA_backManual, CP_backManual, and CC_backManual recovery to Manual from the fault leaf.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'ca_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 5, 'step_name': 'cp_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'infusion_rate': 16, 'pump_speed': 17, 'sensor_buffer_bp': 69, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 10, 'step_name': 'cc_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 2, 'alarm_signal': 1, 'blood_pressure': 69, 'default_flow_rate': 16, 'pump_fault': 1, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'scenario_name': 'forced_and_fault_event_targets_from_pump_fault', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 0, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'ca_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 0, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'reenter_fault_for_cp', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 69, 'control_voltage': 0, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 0, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'start_for_cp_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 31, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 31, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 3, 'step_name': 'advance_normal_for_cp_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 4, 'step_name': 'fault_again_for_cp', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 5, 'step_name': 'cp_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 6, 'step_name': 'reenter_fault_for_cc', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 1, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 7, 'step_name': 'start_for_cc_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 2, 'alarm_signal': 0, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 31, 'log_count': 2, 'pump_fault': 1, 'pump_speed': 31, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 1, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 8, 'step_name': 'advance_normal_for_cc_fault_reentry', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 2, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 9, 'step_name': 'fault_again_for_cc', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 69, 'control_voltage': 31, 'default_flow_rate': 16, 'infusion_rate': 16, 'log_count': 2, 'pump_fault': 1, 'pump_speed': 17, 'requested_target_bp': 100, 'sensor_buffer_bp': 69, 'software_control': 0, 'switch_speed': 17, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 10, 'step_name': 'cc_from_pump_fault_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, ... +37`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`4128`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-4-sd6-0-1dac5bb337` | `accept` | ❌ | ❌ | default_accept_for_legacy_dsl_only_sl9_output；intent=simulation failed |
| `fixreq-4-sd6-1-d4280088f9` | `accept` | ❌ | ❌ | default_accept_for_legacy_dsl_only_sl9_output；intent=simulation failed |
- repair_rationale：SL-9 returned DSL-only output; runtime accepted all current hard requests for compatibility.
- diff_summary：`{"candidate_dsl_hash": "sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c", "diff_excerpt": [], "n_diff_lines": 0, "old_dsl_hash": "sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c"}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 100;
def int requested_target_bp = 100;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int infusion_rate = 0;
def int pump_speed = 0;
def int switch_speed = 0;
def int default_flow_rate = 0;
def int control_voltage = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_fault = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Manual -> Manual : CA_backManual;
        ! Ask_StartAC -> Manual : CA_backManual;
        ! AutocontrolInit -> Manual : CA_backManual;
        ! AutocontrolNormal -> Manual : CA_backManual;
        ! Manual -> Manual : CB_backManual;
        ! Ask_StartAC -> Manual : CB_backManual;
        ! AutocontrolInit -> Manual : CB_backManual;
        ! AutocontrolNormal -> Manual : CB_backManual;
        ! Manual -> Manual : CP_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual : CP_backManual;
        ! AutocontrolNormal -> Manual : CP_backManual;
        ! Manual -> Manual : CC_backManual;
        ! Ask_StartAC -> Manual : CC_backManual;
        ! AutocontrolInit -> Manual : CC_backManual;
        ! AutocontrolNormal -> Manual : CC_backManual;
        ! Manual -> Manual : TerminateAC;
        ! Ask_StartAC -> Manual : TerminateAC;
        ! AutocontrolInit -> Manual : TerminateAC;
        ! AutocontrolNormal -> Manual : TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
                }
            }
            during {
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
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
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 2;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [blood_pressure >= target_bp] {
                    infusion_rate = 0;
                } else {
                    infusion_rate = target_bp - blood_pressure;
                }
                control_voltage = infusion_rate;
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
                sensor_buffer_bp = blood_pressure;
                infusion_rate = default_flow_rate;
                pump_speed = switch_speed;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual : CA_backManual;
        PumpFault -> Manual : CB_backManual;
        PumpFault -> Manual : CP_backManual;
        PumpFault -> Manual : CC_backManual;
        PumpFault -> Manual : TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

- before 与 candidate 文本完全一致；无 diff。

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:4b6f10aab8b7101b0a26c0696ab84c54be81fbc22e66ea6701f2ad541966d465`。
  - SL-10 evidence 1: `{"summary": "The candidate DSL is identical to the old DSL and to the previously accepted fixlog-12/fixlog-17 safety frontier, with zero diff lines and hash sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c. It is a raw parseable pyfcstm DSL, not the rejected JSON/quoted candidate from fixlog-15."}`
  - SL-10 evidence 2: `{"summary": "All NL-required structural elements are preserved: CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault; variables CA_mode, target_bp, requested_target_bp, blood_pressure, sensor_buffer_bp, infusion_rate, pump_speed, switch_speed, default_flow_rate, control_voltage, software_control, alarm_signal, pump_fault, log_count; and events InitiateAC, ChangeSetpoint, StartAC, FaultRemoved, CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC."}`
  - SL-10 evidence 3: `{"summary": "The DSL continues to satisfy the NL mode-control path: Manual -> Ask_StartAC on InitiateAC, target setpoint modification in Ask_StartAC via ChangeSetpoint, StartAC entering AutocontrolInit, and unguarded transition to AutocontrolNormal under the documented abstraction that the NL gives no concrete initialization-complete trigger."}`
  - SL-10 evidence 4: `{"summary": "The DSL preserves normal autocontrol obligations: AutocontrolNormal buffers blood_pressure, computes infusion_rate inversely to pressure with zero flow when blood_pressure >= target_bp, drives control_voltage and pump_speed from infusion_rate, and increments log_count as the accepted log-file abstraction."}`
  - SL-10 evidence 5: `{"summary": "The DSL preserves manual-mode obligations: Manual sets CA_mode=0, releases software_control, buffers blood_pressure, sets infusion_rate to default_flow_rate, and sets pump_speed to switch_speed."}`
  - SL-10 evidence 6: `{"summary": "The DSL preserves the cross-component fallback target required by the NL: CA_backManual and each of CB_backManual, CP_backManual, CC_backManual, plus TerminateAC, drive the mode-control hierarchy to Manual, including explicit PumpFault -> Manual transitions from the fault leaf."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 19, "n_scenarios_passed": 17, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init verifies the Mode_Control_Algorithm initial leaf is Manual and manual operation uses switch speed/default flow while buffering BP.", "name": "default_init_manual_sets_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode"...<truncated 53465 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial_root", "transition:initial_manual", "guard:pump_fault_gt_0", "action:Ask_StartAC_change_setpoint", "action:AutocontrolNormal_logging"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-23ece122ce8` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-23ece122ce8` | accept=1, reject=0 | `sl10_review` | `sha256:d13b720f647947765800eba3d078515a5fb42b1edd862d5496a2307469102258` | Accepted the hard SL-7 model-review request because the original `! * -> Manual` transitions applied to `PumpFault` and could bypass the NL-required caregiver fault removal., The repair preserves all required states, variables, events, initial transitions, normal autocontrol behavior, setpoint change behavior, logging abstraction, and the `pump_fault > 0` transition into `PumpFault`., The back-to-manual and terminate fallback events remain modeled as forced transitions, but they are scoped to the non-fault operational states: `Manual`, `Ask_StartAC`, `AutocontrolInit`, and `AutocontrolNormal`., ... +1 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-23ece122ce8` | accept=1, reject=0 | `sl9_rework` | `sha256:d13b720f647947765800eba3d078515a5fb42b1edd862d5496a2307469102258` | Repair the fallback event representation so CARA.Mode_Control_Algorithm.CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC are again resolvable as parent-level Mode_Control_Algorithm events from Manual, Ask_StartAC, AutocontrolInit, and AutocontrolNormal, and each sends the model to Manual so Manual.enter/during produce CA_mode=0, software_control=0, alarm_signal=0, sensor_buffer_bp=blood_pressure, infusion_rate=default_flow_rate, and pump_speed=switch_speed., Preserve the SL-7 unsafe-recovery fix: while pump_fault remains active in PumpFault, these fallback/terminate events must not bypass caregiver fault removal. PumpFault recovery to Manual must remain through PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; }., Prefer the smallest DSL edit that restores event visibility without reintroducing unsafe recovery, such as replacing the 20 source-specific forced transitions with guarded parent-level wildcard forced transitions for the five events, e.g. wildcard forced transitions to Manual that fire only when pump_fault == 0, if this guard syntax is supported by the DSL. If guarded wildcard forced transitions are not supported, use another parseable parent-visible representation that excludes active PumpFault recovery while preserving the five required event names at CARA.Mode_Control_Algorithm., ... +16 |
| 4 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-23ece122ce8` | accept=1, reject=0 | `sl10_review` | `sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39` | This is not the previously rejected candidate hash: the fallback transitions now use chain-scope `: EventName` rather than local `:: EventName`, making `CARA.Mode_Control_Algorithm.CA_backManual`, `CB_backManual`, `CP_backManual`, `CC_backManual`, and `TerminateAC` parent-level events., Scenario `forced_back_manual_from_ask_and_init`, step `cb_back_manual_from_ask`: expected event `CARA.Mode_Control_Algorithm.CB_backManual` from `Ask_StartAC` to enter `Manual` and then run `Manual.enter`/`Manual.during`, producing `CA_mode=0`, `software_control=0`, `alarm_signal=0`, `sensor_buffer_bp=75`, `infusion_rate=4`, and `pump_speed=8`. The `! Ask_StartAC -> Manual : CB_backManual;` transition directly addresses the unresolved event path and preserves the Manual actions that compute those vars., Scenario `forced_ca_terminate_cc_back_manual_from_normal`, step `ca_back_manual_from_normal`: expected event `CARA.Mode_Control_Algorithm.CA_backManual` from `AutocontrolNormal` to enter `Manual` and produce `CA_mode=0`, `software_control=0`, `alarm_signal=0`, `sensor_buffer_bp=70`, `infusion_rate=9`, and `pump_speed=4`. The `! AutocontrolNormal -> Manual : CA_backManual;` transition makes that parent event visible and uses existing Manual actions for the expected vars., ... +5 |
| 5 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-23ece122ce8` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:916de02edd77928ed485d3c9c60c237e33a0294d038d83936fd431bbc9267e39` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 6 | `1` | `request_batch` | `fixbatch-1-sha256-8bd9f01c6cc` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 7 | `1` | `sl9_decision` | `fixbatch-1-sha256-8bd9f01c6cc` | accept=1, reject=0 | `sl10_review` | `sha256:7210b3208097b368871ee1fd999eab559dfebd3caa802ea2c295d30441e0acf9` | Scenario `forced_back_manual_from_pump_fault_leaf`, step `cb_back_manual_from_pump_fault`: expected parent-level event `CARA.Mode_Control_Algorithm.CB_backManual` from hot-started `PumpFault` to enter `Manual` and produce `CA_mode=0`, `software_control=0`, `alarm_signal=0`, `sensor_buffer_bp=78`, `infusion_rate=8`, and `pump_speed=2`. The new `PumpFault -> Manual : CB_backManual effect { pump_fault = 0; };` transition makes that event visible at the Mode_Control_Algorithm parent scope and lets Manual.enter/during compute the expected outputs., Scenario `forced_back_manual_from_pump_fault_leaf`, step `terminate_from_pump_fault_forces_manual`: expected TerminateAC from `PumpFault` to enter `Manual` with manual recovery outputs. The new `PumpFault -> Manual : TerminateAC effect { pump_fault = 0; };` transition directly addresses that gap., The same parent-level PumpFault recovery representation is added for CA_backManual, CP_backManual, and CC_backManual to preserve the NL requirement that CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual as a shared recovery target., ... +3 |
| 8 | `1` | `sl10_review` | `fixbatch-1-sha256-8bd9f01c6cc` | accept=1, reject=0 | `sl9_rework` | `sha256:7210b3208097b368871ee1fd999eab559dfebd3caa802ea2c295d30441e0acf9` | Keep the five parent-level PumpFault fallback/termination transitions so `CARA.Mode_Control_Algorithm.CA_backManual`, `CB_backManual`, `CP_backManual`, `CC_backManual`, and `TerminateAC` are resolvable from `PumpFault` and enter `Manual`., Remove the `effect { pump_fault = 0; }` from the PumpFault-to-Manual fallback/TerminateAC transitions, or otherwise ensure these events do not clear `pump_fault`. Fault removal must remain represented by `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };`., Preserve Manual enter/during behavior so the immediate fallback from PumpFault to Manual still produces `CA_mode=0`, `software_control=0`, `alarm_signal=0`, `sensor_buffer_bp=blood_pressure`, `infusion_rate=default_flow_rate`, and `pump_speed=switch_speed`., ... +16 |
| 9 | `1` | `sl9_rework_decision` | `fixbatch-1-sha256-8bd9f01c6cc` | accept=1, reject=0 | `sl10_review` | `sha256:0c453825a7e1638f62cf9c8f073d1dc0eaf11a6fcdec70b61dd74c72ce74073d` | For scenario `forced_back_manual_from_pump_fault_leaf`, step `cb_back_manual_from_pump_fault`, the prior current DSL stayed in `PumpFault` because no PumpFault fallback transition existed. The candidate adds `PumpFault -> Manual : CB_backManual;`, so the parent-level event enters Manual and Manual.enter/during produce `CA_mode=0`, `software_control=0`, `alarm_signal=0`, `sensor_buffer_bp=blood_pressure`, `infusion_rate=default_flow_rate`, and `pump_speed=switch_speed`., For step `terminate_from_pump_fault_forces_manual`, the candidate adds `PumpFault -> Manual : TerminateAC;` and analogous CA/CP/CC fallback transitions, preserving the NL-required shared recovery events as parent-level Mode_Control_Algorithm events from the fault leaf., For the rework failing step `fault_reentered`, the candidate removes the previously rejected behavior of clearing `pump_fault` on PumpFault fallback/termination. Because `pump_fault` remains positive after fallback, re-entering autocontrol still reaches `AutocontrolNormal`, then the preserved `AutocontrolNormal -> PumpFault : if [pump_fault > 0];` guard fires and PumpFault.enter/during produce `alarm_signal=1`, `software_control=0`, `CA_mode=0`, `sensor_buffer_bp=78`, `infusion_rate=8`, and `pump_speed=2`., ... +4 |
| 10 | `1` | `sl10_rework_review` | `fixbatch-1-sha256-8bd9f01c6cc` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:0c453825a7e1638f62cf9c8f073d1dc0eaf11a6fcdec70b61dd74c72ce74073d` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |
| 11 | `2` | `request_batch` | `fixbatch-2-sha256-84bb8b508a9` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 12 | `2` | `sl9_decision` | `fixbatch-2-sha256-84bb8b508a9` | accept=1, reject=0 | `sl10_review` | `sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c` | The failing model-review obligation is unsafe recovery from PumpFault via backManual/TerminateAC: expected safety is that an unresolved pump fault is not silently de-alarmed; actual current behavior entered Manual with pump_fault still positive and alarm_signal cleared to 0., The smallest safe edit is localized to Manual: Manual.enter and Manual.during now keep alarm_signal = 1 whenever pump_fault > 0, while still setting CA_mode = 0, software_control = 0, sensor_buffer_bp = blood_pressure, infusion_rate = default_flow_rate, and pump_speed = switch_speed., This preserves the prior SL-10 rework frontier: PumpFault-to-Manual CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC remain parent-level events and still do not clear pump_fault, so persistent-fault re-entry through AutocontrolNormal -> PumpFault : if [pump_fault > 0] remains possible., ... +2 |
| 13 | `2` | `sl10_review` | `fixbatch-2-sha256-84bb8b508a9` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |
| 14 | `3` | `request_batch` | `fixbatch-3-sha256-af0e33feb09` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 15 | `3` | `sl9_decision` | `fixbatch-3-sha256-af0e33feb09` | accept=2, reject=0 | `sl10_review` | `sha256:4b7ddbbc35781ef3abb32c1b383b0c3781a16fd087b76b085b8a58b22fa99b7b` | SL-9 returned DSL-only output; runtime accepted all current hard requests for compatibility. |
| 16 | `3` | `sl10_review` | `fixbatch-3-sha256-af0e33feb09` | accept=2, reject=0 | `sl9_rework` | `sha256:4b7ddbbc35781ef3abb32c1b383b0c3781a16fd087b76b085b8a58b22fa99b7b` | Return a raw parseable pyfcstm DSL model only. Do not wrap it in JSON, do not include a `decisions` array, and do not put the DSL inside a quoted `candidate_dsl` string. The first token of the candidate should be a valid pyfcstm token such as `def` or `state`, not `{`., Restore the full prior parseable DSL structure rather than the truncated JSON/string candidate: all variable definitions, `state CARA`, nested `state Mode_Control_Algorithm`, states `Manual`, `Ask_StartAC`, `AutocontrolInit`, `AutocontrolNormal`, `PumpFault`, initial transitions, event transitions, guards, and actions must be present., Do not implement the proposed unconditional `alarm_signal = 0` in `Manual.enter` or `Manual.during`. Preserve the fixlog-12 safety behavior: in Manual, set `alarm_signal = 1` when `pump_fault > 0`, otherwise set `alarm_signal = 0`., ... +20 |
| 17 | `3` | `sl9_rework_decision` | `fixbatch-3-sha256-af0e33feb09` | accept=2, reject=0 | `sl10_review` | `sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c` | SL-9 returned DSL-only output; runtime accepted all current hard requests for compatibility., rework_locked=true |
| 18 | `3` | `sl10_rework_review` | `fixbatch-3-sha256-af0e33feb09` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |
| 19 | `4` | `request_batch` | `fixbatch-4-sha256-af0e33feb09` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 20 | `4` | `sl9_decision` | `fixbatch-4-sha256-af0e33feb09` | accept=2, reject=0 | `sl10_review` | `sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c` | SL-9 returned DSL-only output; runtime accepted all current hard requests for compatibility. |
| 21 | `4` | `sl10_review` | `fixbatch-4-sha256-af0e33feb09` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:0a5120107c33c8e653b64304dbdea896b74f34ee77f79f37ca4a6ca5f5679b0c` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +9 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5344, 'completion_chars': 20956, 'completion_tokens': 7385, 'elapsed_seconds': 135.48626775699086, 'estimated_completion_tokens': 5239, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11896, 'first_chunk_seconds': 39.039893253007904, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13835}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3420, 'completion_chars': 14212, 'completion_tokens': 5479, 'elapsed_seconds': 103.09283740702085, 'estimated_completion_tokens': 3553, 'estimated_prompt_tokens': 15319, 'estimated_total_tokens': 18872, 'first_chunk_seconds': 40.92805629700888, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 61273, 'prompt_tokens': 14983, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20462}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2163, 'completion_chars': 9764, 'completion_tokens': 2682, 'elapsed_seconds': 50.170440065005096, 'estimated_completion_tokens': 2441, 'estimated_prompt_tokens': 19686, 'estimated_total_tokens': 22127, 'first_chunk_seconds': 11.785140847001458, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 78743, 'prompt_tokens': 19333, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22015}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1386, 'completion_chars': 5926, 'completion_tokens': 3459, 'elapsed_seconds': 66.84481216399581, 'estimated_completion_tokens': 1482, 'estimated_prompt_tokens': 21929, 'estimated_total_tokens': 23411, 'first_chunk_seconds': 40.84736365900608, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 87714, 'prompt_tokens': 21006, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24465}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 965, 'completion_chars': 4452, 'completion_tokens': 1799, 'elapsed_seconds': 37.14095895198989, 'estimated_completion_tokens': 1113, 'estimated_prompt_tokens': 26019, 'estimated_total_tokens': 27132, 'first_chunk_seconds': 19.79872388599324, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 104075, 'prompt_tokens': 23147, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24946}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1945, 'completion_chars': 8250, 'completion_tokens': 2351, 'elapsed_seconds': 45.85533191499417, 'estimated_completion_tokens': 2063, 'estimated_prompt_tokens': 108931, 'estimated_total_tokens': 110994, 'first_chunk_seconds': 10.714066263986751, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 435723, 'prompt_tokens': 84753, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 87104}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1110, 'completion_chars': 5115, 'completion_tokens': 1443, 'elapsed_seconds': 29.008745803992497, 'estimated_completion_tokens': 1279, 'estimated_prompt_tokens': 95852, 'estimated_total_tokens': 97131, 'first_chunk_seconds': 10.520360827998957, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 383405, 'prompt_tokens': 73886, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 75329}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4117, 'completion_chars': 17114, 'completion_tokens': 4571, 'elapsed_seconds': 84.66309028799878, 'estimated_completion_tokens': 4279, 'estimated_prompt_tokens': 21216, 'estimated_total_tokens': 25495, 'first_chunk_seconds': 10.456435130996397, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 84861, 'prompt_tokens': 20786, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25357}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5266, 'completion_chars': 21885, 'completion_tokens': 5599, 'elapsed_seconds': 103.90277395397425, 'estimated_completion_tokens': 5472, 'estimated_prompt_tokens': 21941, 'estimated_total_tokens': 27413, 'first_chunk_seconds': 8.43299150999519, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 87763, 'prompt_tokens': 21483, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 27082}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1880, 'completion_chars': 8094, 'completion_tokens': 3435, 'elapsed_seconds': 65.18032579100691, 'estimated_completion_tokens': 2024, 'estimated_prompt_tokens': 73961, 'estimated_total_tokens': 75985, 'first_chunk_seconds': 31.452705125004286, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 295843, 'prompt_tokens': 59319, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 62754}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 982, 'completion_chars': 4034, 'completion_tokens': 2328, 'elapsed_seconds': 44.94434421998449, 'estimated_completion_tokens': 1009, 'estimated_prompt_tokens': 31162, 'estimated_total_tokens': 32171, 'first_chunk_seconds': 27.211864755983697, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 124646, 'prompt_tokens': 27384, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 29712}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1825, 'completion_chars': 7723, 'completion_tokens': 2344, 'elapsed_seconds': 47.7159191169776, 'estimated_completion_tokens': 1931, 'estimated_prompt_tokens': 117635, 'estimated_total_tokens': 119566, 'first_chunk_seconds': 14.698261588986497, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 470539, 'prompt_tokens': 91261, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 93605}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1162, 'completion_chars': 5509, 'completion_tokens': 1681, 'elapsed_seconds': 32.990268980007386, 'estimated_completion_tokens': 1378, 'estimated_prompt_tokens': 52838, 'estimated_total_tokens': 54216, 'first_chunk_seconds': 11.990436156018404, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 211349, 'prompt_tokens': 44151, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 45832}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6756, 'completion_chars': 27003, 'completion_tokens': 8123, 'elapsed_seconds': 148.74342422900372, 'estimated_completion_tokens': 6751, 'estimated_prompt_tokens': 24522, 'estimated_total_tokens': 31273, 'first_chunk_seconds': 27.04107917199144, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 98088, 'prompt_tokens': 24129, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 32252}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2042, 'completion_chars': 9028, 'completion_tokens': 2561, 'elapsed_seconds': 48.9511728999787, 'estimated_completion_tokens': 2257, 'estimated_prompt_tokens': 26073, 'estimated_total_tokens': 28330, 'first_chunk_seconds': 12.11794054499478, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 104291, 'prompt_tokens': 25695, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 28256}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1657, 'completion_chars': 7242, 'completion_tokens': 2642, 'elapsed_seconds': 52.012731573020574, 'estimated_completion_tokens': 1811, 'estimated_prompt_tokens': 102085, 'estimated_total_tokens': 103896, 'first_chunk_seconds': 22.043018656026106, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 408338, 'prompt_tokens': 78403, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 81045}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1158, 'completion_chars': 5171, 'completion_tokens': 1967, 'elapsed_seconds': 37.65972881001653, 'estimated_completion_tokens': 1293, 'estimated_prompt_tokens': 39655, 'estimated_total_tokens': 40948, 'first_chunk_seconds': 16.592817619995913, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 158619, 'prompt_tokens': 32876, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 34843}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3708, 'completion_chars': 15396, 'completion_tokens': 4211, 'elapsed_seconds': 77.90831347799394, 'estimated_completion_tokens': 3849, 'estimated_prompt_tokens': 32273, 'estimated_total_tokens': 36122, 'first_chunk_seconds': 11.499950091994833, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 129091, 'prompt_tokens': 31915, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 36126}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 597, 'completion_chars': 2455, 'completion_tokens': None, 'elapsed_seconds': 63.95224057600717, 'estimated_completion_tokens': 614, 'estimated_prompt_tokens': 163577, 'estimated_total_tokens': 164191, 'first_chunk_seconds': 26.944279381015804, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 654307, 'prompt_tokens': None, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': False, 'token_usage_estimation_method': 'ceil(chars/4)', 'total_tokens': None}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1093, 'completion_chars': 4729, 'completion_tokens': 1901, 'elapsed_seconds': 37.83706827601418, 'estimated_completion_tokens': 1183, 'estimated_prompt_tokens': 99740, 'estimated_total_tokens': 100923, 'first_chunk_seconds': 18.764373431011336, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 398957, 'prompt_tokens': 72864, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 74765}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 890, 'completion_chars': 4128, 'completion_tokens': 1075, 'elapsed_seconds': 22.793143873976078, 'estimated_completion_tokens': 1032, 'estimated_prompt_tokens': 105530, 'estimated_total_tokens': 106562, 'first_chunk_seconds': 6.6897003459744155, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 422117, 'prompt_tokens': 82213, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 83288}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1398, 'completion_chars': 5945, 'completion_tokens': 1666, 'elapsed_seconds': 36.66172083601123, 'estimated_completion_tokens': 1487, 'estimated_prompt_tokens': 91306, 'estimated_total_tokens': 92793, 'first_chunk_seconds': 12.570645316009177, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 365221, 'prompt_tokens': 69504, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 71170}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 890, 'completion_chars': 4128, 'completion_tokens': 1228, 'elapsed_seconds': 27.626538195007015, 'estimated_completion_tokens': 1032, 'estimated_prompt_tokens': 314803, 'estimated_total_tokens': 315835, 'first_chunk_seconds': 11.40244453199557, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 1259210, 'prompt_tokens': 219247, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 220475}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1437, 'completion_chars': 6496, 'completion_tokens': 1541, 'elapsed_seconds': 30.942522948986152, 'estimated_completion_tokens': 1624, 'estimated_prompt_tokens': 143148, 'estimated_total_tokens': 144772, 'first_chunk_seconds': 5.186143971979618, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 572592, 'prompt_tokens': 100664, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 102205}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`not_converged`，record_status=`budget_exhausted`。
- 主要原因分类：`scenario_or_sim_oracle`。
- required stages executed：`71/16`，missing=`<none>`。
- repairs：`5/8` accepted；scenario_history=`9`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
