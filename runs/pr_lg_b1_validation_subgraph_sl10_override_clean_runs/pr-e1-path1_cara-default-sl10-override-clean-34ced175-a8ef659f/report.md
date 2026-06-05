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
| Git commit | `34ced175cd735eb52fba99c3e4238d5c31479eb2` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:993dd2a89560dc22cd287bbf50c2cbe6faab9e99a63729d53f02e0d42085b247` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:43958c2c35783741aaad6ed9cd4ea74838bd73029d1b20852b1458ce78872fa1", "iteration": 0, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:4e45221702cf0f2e4287194cb63691e7859e97cd53d7322b8d366a6812b90ec0", "iteration": 0, "repair_history_index": 1, "rework_instructions": ["Fix `cb_cp_cc_backmanual_forced_recovery` by ensuring `CB_backManual` from `AutocontrolInit` takes precedence over the unconditional `AutocontrolInit -> AutocontrolNormal` transition. In the DSL, place or otherwise define `AutocontrolInit -> Manual :: CB_backManual` so it is considered before the untriggered `AutocontrolInit -> AutocontrolNormal` transition, or change the transition structure so an injected CB_backManual cannot be bypassed by the untriggered advance.", "After the CB repair, the scenario `cb_cp_cc_backmanual_forced_recovery` step `cb_from_autocontrol_init` must reach `CARA.Mode_Control_Algorithm.Manual` and Manual enter/during behavior must yield CA_mode=0, control_released=1, control_voltage=0, pump_speed=manual_switch_speed=3, flow_rate=default_flow_rate=9, and shared_buffer_bp=patient_bp=81.", "Eliminate the `W_SHADOWED_EVENT` design problem by avoiding duplicate same-named local and chain events. Do not keep both the broad `! * -> Manual :: CA_backManual` / `CB_backManual` / `CP_backManual` / `CC_backManual` / `TerminateAC` declarations and same-named leaf-local `::` transitions unless the DSL syntax provides a non-shadowing way to reference the same event. Prefer one consistent representation that is resolvable from the hot-start leaves.", "If removing or replacing the broad forced declarations to avoid shadowing, provide concrete NL-grounded equivalents for the required fallback obligations: CA_backManual from Ask_StartAC to Manual, CB_backManual from AutocontrolInit to Manual, TerminateAC from AutocontrolNormal to Manual, CP_backManual from AutocontrolNormal to Manual, and CC_backManual from PumpFault to Manual, with Manual as the shared recovery target. State explicitly in the repair rationale how these concrete transitions implement event:CA_backManual, event:CB_backManual, event:CP_backManual, event:CC_backManual, and event:TerminateAC.", "Preserve all required NL-grounded structure and behavior: states CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault; variables including CA_mode, patient_bp, shared_buffer_bp, target_bp, requested_target_bp, flow_rate, default_flow_rate, manual_switch_speed, pump_speed, control_voltage, pump_fault, alarm_signal, error_display, error_sound, control_released, and log_flow_rate; initial transitions `[*] -> Mode_Control_Algorithm` and `[*] -> Manual`; InitiateAC, ChangeSetpoint, StartAC, FaultRemoved; BP-inverse AutocontrolNormal flow computation; PumpFault alarm/release behavior; and Manual pump-speed/default-flow/shared-buffer actions.", "In the next SL-9 rationale, explicitly address the remaining local objections: why `CB_backManual` no longer loses to `AutocontrolInit -> AutocontrolNormal`, how shadowed event names were removed or made unambiguous, and how the reported missing grounding IDs are concretely represented or intentionally mapped to equivalent DSL elements."], "same_as_final": false, "sl10_decision": "rework"}, "matching_repair_history_indices": [2], "repair_history_index": 2, "selected_source_stage": "SD-6", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 520279, 'completion_tokens': 42984, 'total_tokens': 563263, 'estimated_prompt_tokens': 608268, 'estimated_completion_tokens': 35394, 'estimated_total_tokens': 643662, 'prompt_chars': 2433056, 'completion_chars': 141564, 'n_calls': 13, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`823.684s` |
| run record | [`pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:168df14800e6544dbbae0be845c2d1dac218bd4cd4264c49c306b21fb874fe0a` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `37` |
| `langgraph_node_trace_hash` | `sha256:de41a0deafe958300dd558bb2c086d84a638ffcedbe5790ee6a259a86fbc1d9b` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `37` |

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
def int patient_bp = 0;
def int shared_buffer_bp = 0;
def int target_bp = 100;
def int requested_target_bp = 100;
def int flow_rate = 0;
def int default_flow_rate = 0;
def int manual_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_display = 0;
def int error_sound = 0;
def int control_released = 1;
def int log_flow_rate = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                control_released = 1;
                control_voltage = 0;
            }
            during {
                pump_speed = manual_switch_speed;
                flow_rate = default_flow_rate;
                shared_buffer_bp = patient_bp;
            }
        }

        state Ask_StartAC {
            during {
                shared_buffer_bp = patient_bp;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                control_released = 0;
                alarm_signal = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                shared_buffer_bp = patient_bp;
            }
        }

        state AutocontrolNormal {
            during {
                shared_buffer_bp = patient_bp;
                if [patient_bp >= target_bp] {
                    flow_rate = 0;
                } else {
                    flow_rate = target_bp - patient_bp;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_flow_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                error_display = 1;
                error_sound = 1;
                control_released = 1;
                CA_mode = 0;
                control_voltage = 0;
            }
            during {
                shared_buffer_bp = patient_bp;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Manual -> Manual :: CA_backManual;
        Manual -> Manual :: CB_backManual;
        Manual -> Manual :: CP_backManual;
        Manual -> Manual :: CC_backManual;

        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        Ask_StartAC -> Manual :: CA_backManual;
        Ask_StartAC -> Manual :: CB_backManual;
        Ask_StartAC -> Manual :: CP_backManual;
        Ask_StartAC -> Manual :: CC_backManual;

        AutocontrolInit -> Manual :: CA_backManual;
        AutocontrolInit -> Manual :: CB_backManual;
        AutocontrolInit -> Manual :: CP_backManual;
        AutocontrolInit -> Manual :: CC_backManual;
        AutocontrolInit -> AutocontrolNormal;

        AutocontrolNormal -> Manual :: TerminateAC;
        AutocontrolNormal -> Manual :: CA_backManual;
        AutocontrolNormal -> Manual :: CB_backManual;
        AutocontrolNormal -> Manual :: CP_backManual;
        AutocontrolNormal -> Manual :: CC_backManual;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];

        PumpFault -> Manual :: CA_backManual;
        PumpFault -> Manual :: CB_backManual;
        PumpFault -> Manual :: CP_backManual;
        PumpFault -> Manual :: CC_backManual;
        PumpFault -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            alarm_signal = 0;
            error_display = 0;
            error_sound = 0;
        };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12996 | 生成初始 DSL 与 grounding seeds | initial len=2834 | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=115545 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=115545 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=115545 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=247829 | LLM per-request accept/reject + repair | candidate len=2829,3086,3663 | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=161022 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=247829 | LLM per-request accept/reject + repair | candidate len=2829,3086,3663 | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=161022 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=247829 | LLM per-request accept/reject + repair | candidate len=2829,3086,3663 | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=161022 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=24, info=1; blocking=0, advisory=24, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=115545 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=115545 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=1, tokens=25871 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-sl10-override-clean-34ced175-a8ef659f.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T07:27:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T07:27:04Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T07:27:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T07:27:04Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T07:29:05Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T07:29:05Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2834,hash=sha256:f88d4617840d |
| 7 | `2026-06-05T07:29:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T07:29:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T07:29:05Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:f88d4617840d4d21aa52334cf7dcb6426a3a03f81299a2e688cc68cfe891374d |
| 10 | `2026-06-05T07:29:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T07:29:05Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2834,hash=sha256:f88d4617840d, current_hash=sha256:f88d4617840d4d21aa52334cf7dcb6426a3a03f81299a2e688cc68cfe891374d |
| 12 | `2026-06-05T07:29:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T07:29:05Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T07:29:05Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T07:29:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T07:29:05Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T07:29:06Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T07:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T07:29:06Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T07:29:06Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T07:29:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T07:29:06Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T07:30:24Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T07:30:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T07:30:24Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T07:30:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T07:30:24Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T07:31:13Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T07:31:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T07:31:14Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T07:31:14Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T07:31:14Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T07:32:25Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T07:32:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T07:32:25Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T07:32:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T07:32:25Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T07:32:25Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T07:32:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T07:32:25Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T07:32:25Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 42 | `2026-06-05T07:32:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T07:32:25Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 12, "n_scenarios_passed": 7, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 44 | `2026-06-05T07:32:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T07:32:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-05T07:32:25Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 12, "n_scenarios_passed": 7, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2834,hash=sha256:f88d4617840d |
| 47 | `2026-06-05T07:32:25Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 48 | `2026-06-05T07:32:25Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 5} | <none> |
| 49 | `2026-06-05T07:32:25Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2834,hash=sha256:f88d4617840d |
| 50 | `2026-06-05T07:33:13Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 51 | `2026-06-05T07:33:13Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-0cac400bb2", "fixreq-0-sd6-1-1090ceac6d", "fixreq-0-sd6-2-15b38cfc79", "fixreq-0-sd6-3-bd3fee27ff", "fixreq-0-sd6-4-c17c8c07ff"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2829,hash=sha256:e364c76c1243 |
| 52 | `2026-06-05T07:33:13Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 53 | `2026-06-05T07:33:13Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:e364c76c12431bc1cc447e1d140ecd4a15437c4501440c519594c8ab7a94695a |
| 54 | `2026-06-05T07:33:43Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 55 | `2026-06-05T07:33:43Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 56 | `2026-06-05T07:33:43Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 57 | `2026-06-05T07:33:43Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2834,hash=sha256:f88d4617840d |
| 58 | `2026-06-05T07:34:39Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 59 | `2026-06-05T07:34:39Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-0cac400bb2", "fixreq-0-sd6-1-1090ceac6d", "fixreq-0-sd6-2-15b38cfc79", "fixreq-0-sd6-3-bd3fee27ff", "fixreq-0-sd6-4-c17c8c07ff"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=3086,hash=sha256:4e45221702cf |
| 60 | `2026-06-05T07:34:39Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 61 | `2026-06-05T07:34:39Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:4e45221702cf0f2e4287194cb63691e7859e97cd53d7322b8d366a6812b90ec0 |
| 62 | `2026-06-05T07:35:23Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 63 | `2026-06-05T07:35:23Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 64 | `2026-06-05T07:35:23Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 65 | `2026-06-05T07:35:23Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2834,hash=sha256:f88d4617840d |
| 66 | `2026-06-05T07:36:26Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 67 | `2026-06-05T07:36:26Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-0cac400bb2", "fixreq-0-sd6-1-1090ceac6d", "fixreq-0-sd6-2-15b38cfc79", "fixreq-0-sd6-3-bd3fee27ff", "fixreq-0-sd6-4-c17c8c07ff"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=3663,hash=sha256:43958c2c3578 |
| 68 | `2026-06-05T07:36:26Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 69 | `2026-06-05T07:36:26Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:43958c2c35783741aaad6ed9cd4ea74838bd73029d1b20852b1458ce78872fa1 |
| 70 | `2026-06-05T07:37:01Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 71 | `2026-06-05T07:37:01Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 72 | `2026-06-05T07:37:01Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 73 | `2026-06-05T07:37:01Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=3663,hash=sha256:43958c2c3578 |
| 74 | `2026-06-05T07:37:01Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:43958c2c35783741aaad6ed9cd4ea74838bd73029d1b20852b1458ce78872fa1 |
| 75 | `2026-06-05T07:37:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 76 | `2026-06-05T07:37:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 77 | `2026-06-05T07:37:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 78 | `2026-06-05T07:37:01Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:43958c2c35783741aaad6ed9cd4ea74838bd73029d1b20852b1458ce78872fa1 |
| 79 | `2026-06-05T07:37:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 80 | `2026-06-05T07:37:01Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=3663,hash=sha256:43958c2c3578, current_hash=sha256:43958c2c35783741aaad6ed9cd4ea74838bd73029d1b20852b1458ce78872fa1 |
- ……另有 `40` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-6` | yes | fixbatch-0-sha256-a1b0c413df1 / n=5 | accept=5, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 |
|---|---|---|---|
| `default_init_manual_outputs` | default-init: first cycle dispatches to Manual and manual-mode outputs follow caregiver pump settings and sensor bufferi...<truncated 3 chars> | ✅ | ✅ |
| `initiate_change_start_to_normal_autocontrol` | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, then reaches normal autocontrol ...<truncated 27 chars> | ✅ | ✅ |
| `autocontrol_normal_lower_bp_positive_flow` | explicit-hot-start: in AutocontrolNormal, patient BP below target produces positive flow and matching voltage, pump spee...<truncated 11 chars> | ✅ | ✅ |
| `autocontrol_normal_high_bp_zero_flow` | explicit-hot-start: in AutocontrolNormal, patient BP at or above target gives zero flow rather than increasing infusion. | ✅ | ✅ |
| `pump_fault_guard_no_fire_at_zero` | explicit-hot-start: AutocontrolNormal with no pump-operation complication stays in normal control and does not enter Pum...<truncated 7 chars> | ✅ | ✅ |
| `pump_fault_guard_fires_at_positive_fault` | explicit-hot-start: AutocontrolNormal with pump_fault positive enters PumpFault and activates alarms while releasing sof...<truncated 14 chars> | ✅ | ✅ |
| `fault_removed_returns_manual` | explicit-hot-start: after caregiver removes the fault from PumpFault, CARA returns to Manual, clears fault/alarm indicat...<truncated 35 chars> | ✅ | ✅ |
| `ca_backmanual_forces_manual_from_ask_startac` | explicit-hot-start: CA_backManual is a cross-component fallback from Ask_StartAC to the shared Manual recovery target. | ⚪ | ✅ |
| `cb_cp_cc_backmanual_forced_recovery` | explicit-hot-start: CB_backManual, CP_backManual, and CC_backManual each force different autocontrol-related leaves back...<truncated 11 chars> | ⚪ | ✅ |
| `terminate_ac_forces_manual_from_normal` | explicit-hot-start: TerminateAC from normal autocontrol releases algorithmic pump control and returns to Manual recovery...<truncated 11 chars> | ⚪ | ✅ |
| `cp_backmanual_forces_manual_from_normal` | explicit-hot-start: CP_backManual must be a real forced fallback from AutocontrolNormal, so removing that forced line le...<truncated 39 chars> | ⚪ | ✅ |
| `cc_backmanual_forces_manual_from_pumpfault` | explicit-hot-start: CC_backManual must force recovery even from PumpFault; if the forced transition is missing, the mach...<truncated 25 chars> | ⚪ | ✅ |
| `autocontrol_init_untriggered_target_probe` | explicit-hot-start: the untriggered transition from AutocontrolInit must target AutocontrolNormal, not any other mode-co...<truncated 12 chars> | ⚪ | ✅ |
| `cb_backmanual_target_probe_from_ask_startac` | explicit-hot-start: CB_backManual from Ask_StartAC must target Manual as the shared recovery state, catching wrong-targe...<truncated 12 chars> | ⚪ | ✅ |
| `ca_backmanual_target_probe_from_pumpfault` | explicit-hot-start: CA_backManual from PumpFault must target Manual and clear software control to manual recovery, catch...<truncated 36 chars> | ⚪ | ✅ |
| `manual_backmanual_self_target_probe` | default-init: after dispatch to Manual, CA_backManual and CB_backManual from Manual must keep the shared recovery target...<truncated 65 chars> | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_outputs` — default-init: first cycle dispatches to Manual and manual-mode outputs follow caregiver pump settings and sensor buffering.</summary>

| Field | Value |
|---|---|
| description | default-init: first cycle dispatches to Manual and manual-mode outputs follow caregiver pump settings and sensor buffering. |
| initial_state | `<default-init>` |
| initial_vars | `{"default_flow_rate": 12, "manual_switch_speed": 7, "patient_bp": 93}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_after_default_dispatch` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 12, "pump_speed": 7, "shared_buffer_bp": 93}` |

</details>

<details><summary>`initiate_change_start_to_normal_autocontrol` — default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, then reaches normal autocontrol with inverse BP-based flow.</summary>

| Field | Value |
|---|---|
| description | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, then reaches normal autocontrol with inverse BP-based flow. |
| initial_state | `<default-init>` |
| initial_vars | `{"patient_bp": 85, "requested_target_bp": 110, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_ready` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0}` |
| 1 `initiate_enters_ask_startac` | `0` | `["InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"shared_buffer_bp": 85}` |
| 2 `change_setpoint_applies_request` | `0` | `["ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"shared_buffer_bp": 85, "target_bp": 110}` |
| 3 `startac_enters_autocontrol_init` | `0` | `["StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "control_released": 0, "error_display": 0, "error_sound": 0, "shared_buffer_bp": 85}` |
| 4 `untriggered_init_advances_to_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 25, "flow_rate": 25, "log_flow_rate": 25, "pump_speed": 25, "shared_buffer_bp": 85}` |

</details>

<details><summary>`autocontrol_normal_lower_bp_positive_flow` — explicit-hot-start: in AutocontrolNormal, patient BP below target produces positive flow and matching voltage, pump speed, and log.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: in AutocontrolNormal, patient BP below target produces positive flow and matching voltage, pump speed, and log. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"patient_bp": 70, "pump_fault": 0, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `positive_flow_computed` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 30, "flow_rate": 30, "log_flow_rate": 30, "pump_speed": 30, "shared_buffer_bp": 70}` |

</details>

<details><summary>`autocontrol_normal_high_bp_zero_flow` — explicit-hot-start: in AutocontrolNormal, patient BP at or above target gives zero flow rather than increasing infusion.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: in AutocontrolNormal, patient BP at or above target gives zero flow rather than increasing infusion. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"patient_bp": 120, "pump_fault": 0, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_flow_for_high_pressure` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 0, "flow_rate": 0, "log_flow_rate": 0, "pump_speed": 0, "shared_buffer_bp": 120}` |

</details>

<details><summary>`pump_fault_guard_no_fire_at_zero` — explicit-hot-start: AutocontrolNormal with no pump-operation complication stays in normal control and does not enter PumpFault.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: AutocontrolNormal with no pump-operation complication stays in normal control and does not enter PumpFault. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"patient_bp": 90, "pump_fault": 0, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_fault_stays_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 10, "flow_rate": 10, "log_flow_rate": 10, "pump_speed": 10, "shared_buffer_bp": 90}` |

</details>

<details><summary>`pump_fault_guard_fires_at_positive_fault` — explicit-hot-start: AutocontrolNormal with pump_fault positive enters PumpFault and activates alarms while releasing software control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: AutocontrolNormal with pump_fault positive enters PumpFault and activates alarms while releasing software control. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "control_released": 0, "patient_bp": 90, "pump_fault": 1, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_enters_pumpfault` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1, "control_voltage": 0, "error_display": 1, "error_sound": 1, "shared_buffer_bp": 90}` |

</details>

<details><summary>`fault_removed_returns_manual` — explicit-hot-start: after caregiver removes the fault from PumpFault, CARA returns to Manual, clears fault/alarm indicators, and uses manual pump settings.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: after caregiver removes the fault from PumpFault, CARA returns to Manual, clears fault/alarm indicators, and uses manual pump settings. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"alarm_signal": 1, "default_flow_rate": 8, "error_display": 1, "error_sound": 1, "manual_switch_speed": 5, "patient_bp": 88, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_removed_manual_recovery` | `0` | `["FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "control_voltage": 0, "error_display": 0, "error_sound": 0, "flow_rate": 8, "pump_fault": 0, "pump_speed": 5, "shared_buffer_bp": 88}` |

</details>

<details><summary>`ca_backmanual_forces_manual_from_ask_startac` — explicit-hot-start: CA_backManual is a cross-component fallback from Ask_StartAC to the shared Manual recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CA_backManual is a cross-component fallback from Ask_StartAC to the shared Manual recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "control_released": 0, "default_flow_rate": 6, "manual_switch_speed": 4, "patient_bp": 82}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_fallback_manual` | `0` | `["CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 6, "pump_speed": 4, "shared_buffer_bp": 82}` |

</details>

<details><summary>`cb_cp_cc_backmanual_forced_recovery` — explicit-hot-start: CB_backManual, CP_backManual, and CC_backManual each force different autocontrol-related leaves back to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CB_backManual, CP_backManual, and CC_backManual each force different autocontrol-related leaves back to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "control_released": 0, "default_flow_rate": 9, "manual_switch_speed": 3, "patient_bp": 81}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_from_autocontrol_init` | `0` | `["CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 9, "pump_speed": 3, "shared_buffer_bp": 81}` |
| 1 `cp_from_manual_still_manual` | `0` | `["CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 9, "pump_speed": 3, "shared_buffer_bp": 81}` |
| 2 `cc_from_manual_still_manual` | `0` | `["CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 9, "pump_speed": 3, "shared_buffer_bp": 81}` |

</details>

<details><summary>`terminate_ac_forces_manual_from_normal` — explicit-hot-start: TerminateAC from normal autocontrol releases algorithmic pump control and returns to Manual recovery operation.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: TerminateAC from normal autocontrol releases algorithmic pump control and returns to Manual recovery operation. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "control_released": 0, "control_voltage": 22, "default_flow_rate": 11, "manual_switch_speed": 2, "patient_bp": 77, "pump_fault": 0, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_lands_manual` | `0` | `["TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 11, "pump_speed": 2, "shared_buffer_bp": 77}` |

</details>

<details><summary>`cp_backmanual_forces_manual_from_normal` — explicit-hot-start: CP_backManual must be a real forced fallback from AutocontrolNormal, so removing that forced line leaves the system wrongly in autocontrol.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CP_backManual must be a real forced fallback from AutocontrolNormal, so removing that forced line leaves the system wrongly in autocontrol. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "control_released": 0, "default_flow_rate": 13, "manual_switch_speed": 6, "patient_bp": 84, "pump_fault": 0, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_forced_from_normal_to_manual` | `0` | `["CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 13, "pump_speed": 6, "shared_buffer_bp": 84}` |

</details>

<details><summary>`cc_backmanual_forces_manual_from_pumpfault` — explicit-hot-start: CC_backManual must force recovery even from PumpFault; if the forced transition is missing, the machine remains in PumpFault.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CC_backManual must force recovery even from PumpFault; if the forced transition is missing, the machine remains in PumpFault. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "control_released": 0, "default_flow_rate": 10, "error_display": 1, "error_sound": 1, "manual_switch_speed": 8, "patient_bp": 86, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_forced_from_fault_to_manual` | `0` | `["CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 10, "pump_speed": 8, "shared_buffer_bp": 86}` |

</details>

<details><summary>`autocontrol_init_untriggered_target_probe` — explicit-hot-start: the untriggered transition from AutocontrolInit must target AutocontrolNormal, not any other mode-control state.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: the untriggered transition from AutocontrolInit must target AutocontrolNormal, not any other mode-control state. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "control_released": 0, "patient_bp": 76, "pump_fault": 0, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `init_targets_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 24, "flow_rate": 24, "log_flow_rate": 24, "pump_speed": 24, "shared_buffer_bp": 76}` |

</details>

<details><summary>`cb_backmanual_target_probe_from_ask_startac` — explicit-hot-start: CB_backManual from Ask_StartAC must target Manual as the shared recovery state, catching wrong-target mutations.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CB_backManual from Ask_StartAC must target Manual as the shared recovery state, catching wrong-target mutations. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "control_released": 0, "default_flow_rate": 14, "manual_switch_speed": 9, "patient_bp": 79}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_ask_targets_manual` | `0` | `["CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 14, "pump_speed": 9, "shared_buffer_bp": 79}` |

</details>

<details><summary>`ca_backmanual_target_probe_from_pumpfault` — explicit-hot-start: CA_backManual from PumpFault must target Manual and clear software control to manual recovery, catching wrong-target fallback mutations.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CA_backManual from PumpFault must target Manual and clear software control to manual recovery, catching wrong-target fallback mutations. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "control_released": 0, "default_flow_rate": 15, "error_display": 1, "error_sound": 1, "manual_switch_speed": 10, "patient_bp": 87, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_fault_targets_manual` | `0` | `["CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 15, "pump_speed": 10, "shared_buffer_bp": 87}` |

</details>

<details><summary>`manual_backmanual_self_target_probe` — default-init: after dispatch to Manual, CA_backManual and CB_backManual from Manual must keep the shared recovery target exactly Manual, catching wrong-target s...<truncated 25 chars></summary>

| Field | Value |
|---|---|
| description | default-init: after dispatch to Manual, CA_backManual and CB_backManual from Manual must keep the shared recovery target exactly Manual, catching wrong-target self-transition mutations. |
| initial_state | `<default-init>` |
| initial_vars | `{"CA_mode": 0, "control_released": 1, "default_flow_rate": 16, "manual_switch_speed": 12, "patient_bp": 91}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_dispatched` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 16, "pump_speed": 12, "shared_buffer_bp": 91}` |
| 1 `ca_manual_self_targets_manual` | `0` | `["CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 16, "pump_speed": 12, "shared_buffer_bp": 91}` |
| 2 `cb_manual_self_targets_manual` | `0` | `["CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "control_voltage": 0, "flow_rate": 16, "pump_speed": 12, "shared_buffer_bp": 91}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-6` | ca_backmanual_forces_manual_from_ask_startac, cb_cp_cc_backmanual_forced_recovery, terminate_ac_forces_manual_from_normal, cp_backmanual_forces_manual_from_normal, cc_backmanual_forces_manual_from_pumpfault | accept=5, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Do not keep the current `! * -> Manual : CA_backManual` / `: CB_backManual` / `: CP_backManual` / `: CC_backManual` / `: TerminateAC` form as the sole representation, because l...<truncated 728 chars> | `sha256:e364c76c12431bc1cc447e1d140ecd4a15437c4501440c519594c8ab7a94695a` |
| 2 | `0` | ❌ | `SD-6` | ca_backmanual_forces_manual_from_ask_startac, cb_cp_cc_backmanual_forced_recovery, terminate_ac_forces_manual_from_normal, cp_backmanual_forces_manual_from_normal, cc_backmanual_forces_manual_from_pumpfault | accept=5, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Fix `cb_cp_cc_backmanual_forced_recovery` by ensuring `CB_backManual` from `AutocontrolInit` takes precedence over the unconditional `AutocontrolInit -> AutocontrolNormal` tran...<truncated 818 chars> | `sha256:4e45221702cf0f2e4287194cb63691e7859e97cd53d7322b8d366a6812b90ec0` |
| 3 | `0` | ✅ | `SD-6` | ca_backmanual_forces_manual_from_ask_startac, cb_cp_cc_backmanual_forced_recovery, terminate_ac_forces_manual_from_normal, cp_backmanual_forces_manual_from_normal, cc_backmanual_forces_manual_from_pumpfault | accept=5, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | `sha256:43958c2c35783741aaad6ed9cd4ea74838bd73029d1b20852b1458ce78872fa1` |

<details><summary>Repair 1 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`ca_backmanual_forces_manual_from_ask_startac, cb_cp_cc_backmanual_forced_recovery, terminate_ac_forces_manual_from_normal, cp_backmanual_forces_manual_from_normal, cc_backmanual_forces_manual_from_pumpfault`。
- before_dsl_hash：`sha256:f88d4617840d4d21aa52334cf7dcb6426a3a03f81299a2e688cc68cfe891374d`；candidate_dsl_hash：`sha256:e364c76c12431bc1cc447e1d140ecd4a15437c4501440c519594c8ab7a94695a`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-a1b0c413df1`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`5`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-0cac400bb2` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CA_backManual is a cross-component fallback from Ask_StartAC to the shared Manual recovery target.', 'name': 'ca_backmanual_forces_manual_from_ask_startac', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CA_backManual is a cross-component fallback from Ask_StartAC to the shared Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 0, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 6, 'pump_speed': 4, 'shared_buffer_bp': 82}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC' while resolving event reference 'CA_backManual'", 'runtime_error_hint': {'event_path': 'CA_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'ca_fallback_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'default_flow_rate': 6, 'manual_switch_speed': 4, 'patient_bp': 82}, 'scenario_name': 'ca_backmanual_forces_manual_from_ask_startac', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 6, 'error_display': 0, 'error_sound': 0, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 82, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC' while resolving event reference 'CA_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_fallback_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-1090ceac6d` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CB_backManual, CP_backManual, and CC_backManual each force different autocontrol-related leaves back to Manual.', 'name': 'cb_cp_cc_backmanual_forced_recovery', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CB_backManual, CP_backManual, and CC_backManual each force different autocontrol-related leaves back to Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 0, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 9, 'pump_speed': 3, 'shared_buffer_bp': 81}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CB_backManual'", 'runtime_error_hint': {'event_path': 'CB_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cb_from_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'default_flow_rate': 9, 'manual_switch_speed': 3, 'patient_bp': 81}, 'scenario_name': 'cb_cp_cc_backmanual_forced_recovery', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 9, 'error_display': 0, 'error_sound': 0, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 3, 'patient_bp': 81, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CB_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cb_from_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-2-15b38cfc79` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: TerminateAC from normal autocontrol releases algorithmic pump control and returns to Manual recovery operation.', 'name': 'terminate_ac_forces_manual_from_normal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: TerminateAC from normal autocontrol releases algorithmic pump control and returns to Manual recovery operation.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 22, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 11, 'pump_speed': 2, 'shared_buffer_bp': 77}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'TerminateAC' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'TerminateAC'", 'runtime_error_hint': {'event_path': 'TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_lands_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 22, 'default_flow_rate': 11, 'manual_switch_speed': 2, 'patient_bp': 77, 'pump_fault': 0, 'target_bp': 100}, 'scenario_name': 'terminate_ac_forces_manual_from_normal', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'control_voltage': 22, 'default_flow_rate': 11, 'error_display': 0, 'error_sound': 0, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 2, 'patient_bp': 77, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'TerminateAC' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'TerminateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_lands_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-bd3fee27ff` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CP_backManual must be a real forced fallback from AutocontrolNormal, so removing that forced line leaves the system wrongly in autocontrol.', 'name': 'cp_backmanual_forces_manual_from_normal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CP_backManual must be a real forced fallback from AutocontrolNormal, so removing that forced line leaves the system wrongly in autocontrol.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 0, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 13, 'pump_speed': 6, 'shared_buffer_bp': 84}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CP_backManual'", 'runtime_error_hint': {'event_path': 'CP_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cp_forced_from_normal_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'default_flow_rate': 13, 'manual_switch_speed': 6, 'patient_bp': 84, 'pump_fault': 0, 'target_bp': 100}, 'scenario_name': 'cp_backmanual_forces_manual_from_normal', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 13, 'error_display': 0, 'error_sound': 0, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 6, 'patient_bp': 84, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CP_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_forced_from_normal_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-c17c8c07ff` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual must force recovery even from PumpFault; if the forced transition is missing, the machine remains in PumpFault.', 'name': 'cc_backmanual_forces_manual_from_pumpfault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CC_backManual must force recovery even from PumpFault; if the forced transition is missing, the machine remains in PumpFault.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 0, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 10, 'pump_speed': 8, 'shared_buffer_bp': 86}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CC_backManual'", 'runtime_error_hint': {'event_path': 'CC_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cc_forced_from_fault_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 1, 'control_released': 0, 'default_flow_rate': 10, 'error_display': 1, 'error_sound': 1, 'manual_switch_speed': 8, 'patient_bp': 86, 'pump_fault': 1}, 'scenario_name': 'cc_backmanual_forces_manual_from_pumpfault', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 10, 'error_display': 1, 'error_sound': 1, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 8, 'patient_bp': 86, 'pump_fault': 1, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CC_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cc_forced_from_fault_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:CARA, state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:patient_bp, variable:shared_buffer_bp, variable:target_bp, variable:requested_target_bp, ... +37`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2829`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-0cac400bb2` | `accept` | ❌ | ❌ | The ca_backmanual_forces_manual_from_ask_startac scenario injects CA_backManual from hot-start state Ask_StartAC and expects Manual with Manual entry/during effects. The existing forced fallback is NL-grounded but used local forced-event scope, which was not resolvable from the hot-start leaf. Changing this cross-component fallback event to parent-chain scop...<truncated 194 chars> |
| `fixreq-0-sd6-1-1090ceac6d` | `accept` | ❌ | ❌ | The cb_cp_cc_backmanual_forced_recovery scenario injects CB_backManual from AutocontrolInit and expects Manual with CA_mode reset, control released, control voltage cleared, and Manual during values applied. Changing the cross-component forced fallback to parent-chain scope repairs the unresolved event without deleting required states, variables, or actions....<truncated 101 chars> |
| `fixreq-0-sd6-2-15b38cfc79` | `accept` | ❌ | ❌ | The terminate_ac_forces_manual_from_normal scenario injects TerminateAC from AutocontrolNormal and expects release to Manual. TerminateAC is a caregiver termination event applying across the Mode_Control_Algorithm region, so parent-chain event scope is the smallest faithful repair for visibility from autocontrol leaves.；intent=Change forced TerminateAC fallb...<truncated 60 chars> |
| `fixreq-0-sd6-3-bd3fee27ff` | `accept` | ❌ | ❌ | The cp_backmanual_forces_manual_from_normal scenario injects CP_backManual from AutocontrolNormal and expects forced recovery to Manual. The NL explicitly names CP_backManual as a cross-component fallback to shared Manual recovery, so parent-chain event scope preserves the required forced transition while making the event resolvable.；intent=Change forced CP_...<truncated 76 chars> |
| `fixreq-0-sd6-4-c17c8c07ff` | `accept` | ❌ | ❌ | The cc_backmanual_forces_manual_from_pumpfault scenario injects CC_backManual from PumpFault and expects Manual recovery. The required forced CC_backManual transition remains present, but its event scope is changed to the enclosing Mode_Control_Algorithm event namespace so it can resolve from PumpFault.；intent=Change forced CC_backManual fallback from local ...<truncated 45 chars> |
- repair_rationale：Addressed ca_backmanual_forces_manual_from_ask_startac: expected Manual with CA_mode = 0, control_released = 1, control_voltage = 0, pump_speed = manual_switch_speed, flow_rate = default_flow_rate, and shared_buffer_bp = patient_bp; actual ...<truncated 143 chars>；Addressed cb_cp_cc_backmanual_forced_recovery: expected CB_backManual from AutocontrolInit to force Manual and run Manual entry/during actions; actual failed because CB_backManual was unresolved. Parent-chain scope makes the shared fallback...<truncated 15 chars>；Addressed terminate_ac_forces_manual_from_normal: expected TerminateAC from AutocontrolNormal to release algorithmic control and return to Manual; actual failed because TerminateAC was unresolved. Parent-chain scope is appropriate for this ...<truncated 71 chars>；Addressed cp_backmanual_forces_manual_from_normal: expected CP_backManual from AutocontrolNormal to force Manual; actual failed because CP_backManual was unresolved. The required forced transition is preserved with corrected event visibilit...<truncated 2 chars>；Addressed cc_backmanual_forces_manual_from_pumpfault: expected CC_backManual from PumpFault to force Manual; actual failed because CC_backManual was unresolved. The required forced transition remains in the Mode_Control_Algorithm scope.
- diff_summary：`{"summary": "Changed the five forced cross-component recovery transitions in Mode_Control_Algorithm from local event scope `::` to parent-chain event scope `:`: CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC. No states, variables, guards, effects, or lifecycle actions were otherwise changed."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int patient_bp = 0;
def int shared_buffer_bp = 0;
def int target_bp = 100;
def int requested_target_bp = 100;
def int flow_rate = 0;
def int default_flow_rate = 0;
def int manual_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_display = 0;
def int error_sound = 0;
def int control_released = 1;
def int log_flow_rate = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;
        ! * -> Manual : TerminateAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                control_released = 1;
                control_voltage = 0;
            }
            during {
                pump_speed = manual_switch_speed;
                flow_rate = default_flow_rate;
                shared_buffer_bp = patient_bp;
            }
        }

        state Ask_StartAC {
            during {
                shared_buffer_bp = patient_bp;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                control_released = 0;
                alarm_signal = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                shared_buffer_bp = patient_bp;
            }
        }

        state AutocontrolNormal {
            during {
                shared_buffer_bp = patient_bp;
                if [patient_bp >= target_bp] {
                    flow_rate = 0;
                } else {
                    flow_rate = target_bp - patient_bp;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_flow_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                error_display = 1;
                error_sound = 1;
                control_released = 1;
                CA_mode = 0;
                control_voltage = 0;
            }
            during {
                shared_buffer_bp = patient_bp;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            alarm_signal = 0;
            error_display = 0;
            error_sound = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -19,11 +19,11 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
-        ! * -> Manual :: TerminateAC;
+        ! * -> Manual : CA_backManual;
+        ! * -> Manual : CB_backManual;
+        ! * -> Manual : CP_backManual;
+        ! * -> Manual : CC_backManual;
+        ! * -> Manual : TerminateAC;
 
         [*] -> Manual;
 
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:7a3e70848454a53ef33eeaf8afa0e870a8ff43a29b34a603b7b7a92d5364c7c1`。
  - SL-10 evidence 1: `{"summary": "The NL explicitly requires CA_backManual and any of CB_backManual, CP_backManual, or CC_backManual to cause CA_mode to become Manual as a cross-component fallback, and requires TerminateAC to terminate algorithmic pump control. The FixLog shows SL-9 attempted to repair the five unresolved fallback/termination events by changing the forced transitions from `::` to `:`. However, local deterministic simulation still reports the same five unresolved event-path errors: CA_backManual from Ask_StartAC, CB_backManual from AutocontrolInit, TerminateAC from AutocontrolNormal, CP_backManual from AutocontrolNormal, and CC_backManual from PumpFault. Therefore the target requests are not reso...<truncated 7 chars>`
  - SL-10 evidence 2: `{"summary": "The candidate DSL preserves the required states, variables, normal transitions, and actions, but the only diff changes event syntax on the five forced transitions. Local evidence indicates this syntax change did not make the events resolvable and additionally caused missing_required_grounding for event:TerminateAC, event:CA_backManual, event:CB_backManual, event:CP_backManual, event:CC_backManual, and initial transitions. Because the hard-block sim requests remain failing, this cannot be accepted for the next full revalidation pass."}`
  - SL-10 evidence 3: `{"summary": "For ca_backmanual_forces_manual_from_ask_startac, step ca_fallback_manual still expects state CARA.Mode_Control_Algorithm.Manual with CA_mode=0, control_released=1, control_voltage=0, pump_speed=4, flow_rate=6, shared_buffer_bp=82, but actual remains Ask_StartAC with CA_mode=1, control_released=0, pump_speed=0, flow_rate=0, shared_buffer_bp=0 due to unresolved CA_backManual. Equivalent unresolved-event failures remain for CB_backManual from AutocontrolInit, TerminateAC and CP_backManual from AutocontrolNormal, and CC_backManual from PumpFault."}`
- SL-10 rework_instructions：Do not keep the current `! * -> Manual : CA_backManual` / `: CB_backManual` / `: CP_backManual` / `: CC_backManual` / `: TerminateAC` form as the sole representation, because local simulation still cannot resolve those events and the local grounding check no longer recognizes them as required events.；Repair the fallback events with DSL-visible event transitions from the hot-start/source leaves used by the failing scenarios. At minimum, add or restore resolvable `::` event transitions so that `CA_backManual` is visible from Ask_StartAC, `CB_backManual` is visible from AutocontrolInit, `TerminateAC` is visible from AutocontrolNormal, `CP_backManual` is vis...<truncated 98 chars>；Prefer an NL-faithful representation of the cross-component fallback by adding explicit source-owned transitions for the autocontrol-related leaves, e.g. from Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault to Manual for CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC as appropriate, using the event syntax that loca...<truncated 76 chars>；Ensure the transition to Manual runs Manual enter/during behavior so the failing scenarios reach the expected variables: CA_mode=0, control_released=1, control_voltage=0, pump_speed=manual_switch_speed, flow_rate=default_flow_rate, and shared_buffer_bp=patient_bp. Do not add unrelated benchmark-specific assignments if Manual entry/during actions already prov...<truncated 17 chars>；Preserve all required NL-grounded states, variables, guards, actions, and ordinary transitions: CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault; the initial transitions `[ * ] -> Mode_Control_Algorithm` and `[ * ] -> Manual`; InitiateAC, ChangeSetpoint, StartAC, FaultRemoved; AutocontrolNormal BP-based flow co...<truncated 102 chars>；After editing, rerun or reason against the five named failing scenarios explicitly: ca_backmanual_forces_manual_from_ask_startac, cb_cp_cc_backmanual_forced_recovery, terminate_ac_forces_manual_from_normal, cp_backmanual_forces_manual_from_normal, and cc_backmanual_forces_manual_from_pumpfault. The repair rationale must state how the DSL makes each injected ...<truncated 93 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 12, "n_scenarios_passed": 7, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: first cycle dispatches to Manual and manual-mode outputs follow caregiver pump settings and sensor buffering.", "name": "default_init_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_signal": 0, "control_...<truncated 13593 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["event:TerminateAC", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:initial:CARA.Mode_Control_Algorithm", "transition:initial:Manual"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`ca_backmanual_forces_manual_from_ask_startac, cb_cp_cc_backmanual_forced_recovery, terminate_ac_forces_manual_from_normal, cp_backmanual_forces_manual_from_normal, cc_backmanual_forces_manual_from_pumpfault`。
- before_dsl_hash：`sha256:f88d4617840d4d21aa52334cf7dcb6426a3a03f81299a2e688cc68cfe891374d`；candidate_dsl_hash：`sha256:4e45221702cf0f2e4287194cb63691e7859e97cd53d7322b8d366a6812b90ec0`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-a1b0c413df1`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`5`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-0cac400bb2` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CA_backManual is a cross-component fallback from Ask_StartAC to the shared Manual recovery target.', 'name': 'ca_backmanual_forces_manual_from_ask_startac', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CA_backManual is a cross-component fallback from Ask_StartAC to the shared Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 0, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 6, 'pump_speed': 4, 'shared_buffer_bp': 82}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC' while resolving event reference 'CA_backManual'", 'runtime_error_hint': {'event_path': 'CA_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'ca_fallback_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'default_flow_rate': 6, 'manual_switch_speed': 4, 'patient_bp': 82}, 'scenario_name': 'ca_backmanual_forces_manual_from_ask_startac', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 6, 'error_display': 0, 'error_sound': 0, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 82, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC' while resolving event reference 'CA_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_fallback_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-1090ceac6d` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CB_backManual, CP_backManual, and CC_backManual each force different autocontrol-related leaves back to Manual.', 'name': 'cb_cp_cc_backmanual_forced_recovery', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CB_backManual, CP_backManual, and CC_backManual each force different autocontrol-related leaves back to Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 0, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 9, 'pump_speed': 3, 'shared_buffer_bp': 81}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CB_backManual'", 'runtime_error_hint': {'event_path': 'CB_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cb_from_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'default_flow_rate': 9, 'manual_switch_speed': 3, 'patient_bp': 81}, 'scenario_name': 'cb_cp_cc_backmanual_forced_recovery', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 9, 'error_display': 0, 'error_sound': 0, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 3, 'patient_bp': 81, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CB_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cb_from_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-2-15b38cfc79` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: TerminateAC from normal autocontrol releases algorithmic pump control and returns to Manual recovery operation.', 'name': 'terminate_ac_forces_manual_from_normal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: TerminateAC from normal autocontrol releases algorithmic pump control and returns to Manual recovery operation.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 22, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 11, 'pump_speed': 2, 'shared_buffer_bp': 77}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'TerminateAC' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'TerminateAC'", 'runtime_error_hint': {'event_path': 'TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_lands_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 22, 'default_flow_rate': 11, 'manual_switch_speed': 2, 'patient_bp': 77, 'pump_fault': 0, 'target_bp': 100}, 'scenario_name': 'terminate_ac_forces_manual_from_normal', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'control_voltage': 22, 'default_flow_rate': 11, 'error_display': 0, 'error_sound': 0, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 2, 'patient_bp': 77, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'TerminateAC' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'TerminateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_lands_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-bd3fee27ff` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CP_backManual must be a real forced fallback from AutocontrolNormal, so removing that forced line leaves the system wrongly in autocontrol.', 'name': 'cp_backmanual_forces_manual_from_normal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CP_backManual must be a real forced fallback from AutocontrolNormal, so removing that forced line leaves the system wrongly in autocontrol.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 0, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 13, 'pump_speed': 6, 'shared_buffer_bp': 84}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CP_backManual'", 'runtime_error_hint': {'event_path': 'CP_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cp_forced_from_normal_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'default_flow_rate': 13, 'manual_switch_speed': 6, 'patient_bp': 84, 'pump_fault': 0, 'target_bp': 100}, 'scenario_name': 'cp_backmanual_forces_manual_from_normal', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 13, 'error_display': 0, 'error_sound': 0, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 6, 'patient_bp': 84, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CP_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_forced_from_normal_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-c17c8c07ff` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual must force recovery even from PumpFault; if the forced transition is missing, the machine remains in PumpFault.', 'name': 'cc_backmanual_forces_manual_from_pumpfault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CC_backManual must force recovery even from PumpFault; if the forced transition is missing, the machine remains in PumpFault.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 0, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 10, 'pump_speed': 8, 'shared_buffer_bp': 86}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CC_backManual'", 'runtime_error_hint': {'event_path': 'CC_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cc_forced_from_fault_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 1, 'control_released': 0, 'default_flow_rate': 10, 'error_display': 1, 'error_sound': 1, 'manual_switch_speed': 8, 'patient_bp': 86, 'pump_fault': 1}, 'scenario_name': 'cc_backmanual_forces_manual_from_pumpfault', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 10, 'error_display': 1, 'error_sound': 1, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 8, 'patient_bp': 86, 'pump_fault': 1, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CC_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cc_forced_from_fault_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:CARA, state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:patient_bp, variable:shared_buffer_bp, variable:target_bp, variable:requested_target_bp, ... +37`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3086`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-0cac400bb2` | `accept` | ❌ | ✅ | The ca_backmanual_forces_manual_from_ask_startac failure is an unresolved CA_backManual event from hot-start state Ask_StartAC. I accept the request and add a concrete source-owned Ask_StartAC -> Manual :: CA_backManual transition so the scenario event is resolvable from that leaf and Manual entry/during behavior produces CA_mode=0, control_released=1, contr...<truncated 187 chars> |
| `fixreq-0-sd6-1-1090ceac6d` | `accept` | ❌ | ✅ | The cb_cp_cc_backmanual_forced_recovery failure is an unresolved CB_backManual event from hot-start state AutocontrolInit. I accept the request and add a concrete source-owned AutocontrolInit -> Manual :: CB_backManual transition while preserving the NL-grounded shared Manual recovery target.；intent=Add explicit AutocontrolInit -> Manual :: CB_backManual fal...<truncated 17 chars> |
| `fixreq-0-sd6-2-15b38cfc79` | `accept` | ❌ | ✅ | The terminate_ac_forces_manual_from_normal failure is an unresolved TerminateAC event from AutocontrolNormal. I accept the request and add a concrete source-owned AutocontrolNormal -> Manual :: TerminateAC transition so caregiver termination of algorithmic control releases to Manual.；intent=Add explicit AutocontrolNormal -> Manual :: TerminateAC transition. |
| `fixreq-0-sd6-3-bd3fee27ff` | `accept` | ❌ | ✅ | The cp_backmanual_forces_manual_from_normal failure is an unresolved CP_backManual event from AutocontrolNormal. I accept the request and add a concrete source-owned AutocontrolNormal -> Manual :: CP_backManual transition, preserving Manual as the shared recovery target.；intent=Add explicit AutocontrolNormal -> Manual :: CP_backManual fallback transition. |
| `fixreq-0-sd6-4-c17c8c07ff` | `accept` | ❌ | ✅ | The cc_backmanual_forces_manual_from_pumpfault failure is an unresolved CC_backManual event from PumpFault. I accept the request and add a concrete source-owned PumpFault -> Manual :: CC_backManual transition so recovery is resolvable even from the fault state.；intent=Add explicit PumpFault -> Manual :: CC_backManual fallback transition. |
- repair_rationale：This is not the previously rejected hash: the prior rejected candidate only changed forced fallback event syntax to parent-chain `:`. This candidate preserves the original NL-grounded forced `::` fallback declarations and adds concrete leaf...<truncated 77 chars>；ca_backmanual_forces_manual_from_ask_startac: expected CA_backManual from Ask_StartAC to reach CARA.Mode_Control_Algorithm.Manual with Manual outputs; actual remained Ask_StartAC because CA_backManual was unresolved. The added Ask_StartAC -...<truncated 67 chars>；cb_cp_cc_backmanual_forced_recovery: expected CB_backManual from AutocontrolInit to reach Manual with CA_mode reset and manual pump outputs; actual remained AutocontrolInit because CB_backManual was unresolved. The added AutocontrolInit -> ...<truncated 69 chars>；terminate_ac_forces_manual_from_normal: expected TerminateAC from AutocontrolNormal to release algorithmic control and reach Manual; actual remained AutocontrolNormal because TerminateAC was unresolved. The added AutocontrolNormal -> Manual...<truncated 85 chars>；cp_backmanual_forces_manual_from_normal: expected CP_backManual from AutocontrolNormal to force Manual; actual remained AutocontrolNormal because CP_backManual was unresolved. The added AutocontrolNormal -> Manual :: CP_backManual makes the...<truncated 38 chars>
- diff_summary：`{"summary": "Preserved all existing states, variables, initial transitions, forced fallback declarations, normal mode transitions, guards, effects, and lifecycle actions. Added five explicit leaf-local `::` recovery transitions to Manual: Ask_StartAC -> Manual on CA_backManual, AutocontrolInit -> Manual on CB_backManual, AutocontrolNormal -> Manual on TerminateAC, AutocontrolNormal -> Manual on CP_backManual, and PumpFault -> Manual on CC_backManual."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int patient_bp = 0;
def int shared_buffer_bp = 0;
def int target_bp = 100;
def int requested_target_bp = 100;
def int flow_rate = 0;
def int default_flow_rate = 0;
def int manual_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_display = 0;
def int error_sound = 0;
def int control_released = 1;
def int log_flow_rate = 0;

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
                control_released = 1;
                control_voltage = 0;
            }
            during {
                pump_speed = manual_switch_speed;
                flow_rate = default_flow_rate;
                shared_buffer_bp = patient_bp;
            }
        }

        state Ask_StartAC {
            during {
                shared_buffer_bp = patient_bp;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                control_released = 0;
                alarm_signal = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                shared_buffer_bp = patient_bp;
            }
        }

        state AutocontrolNormal {
            during {
                shared_buffer_bp = patient_bp;
                if [patient_bp >= target_bp] {
                    flow_rate = 0;
                } else {
                    flow_rate = target_bp - patient_bp;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_flow_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                error_display = 1;
                error_sound = 1;
                control_released = 1;
                CA_mode = 0;
                control_voltage = 0;
            }
            during {
                shared_buffer_bp = patient_bp;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            alarm_signal = 0;
            error_display = 0;
            error_sound = 0;
        };
        Ask_StartAC -> Manual :: CA_backManual;
        AutocontrolInit -> Manual :: CB_backManual;
        AutocontrolNormal -> Manual :: TerminateAC;
        AutocontrolNormal -> Manual :: CP_backManual;
        PumpFault -> Manual :: CC_backManual;
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -98,5 +98,10 @@
             error_display = 0;
             error_sound = 0;
         };
+        Ask_StartAC -> Manual :: CA_backManual;
+        AutocontrolInit -> Manual :: CB_backManual;
+        AutocontrolNormal -> Manual :: TerminateAC;
+        AutocontrolNormal -> Manual :: CP_backManual;
+        PumpFault -> Manual :: CC_backManual;
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:d23a4e404f38566acccfb488a90e5052ab8d5f216cbdcc5fdf23633ddede5b41`。
  - SL-10 evidence 1: `{"summary": "The NL requires CA_backManual and any of CB_backManual, CP_backManual, or CC_backManual to cause CA_mode to become Manual as the shared cross-component recovery target, and TerminateAC to terminate algorithmic pump control. The previous SL-10 rework specifically required resolvable fallback/termination transitions from the failing hot-start leaves while preserving Manual recovery behavior."}`
  - SL-10 evidence 2: `{"summary": "The current SL-9 rework is not the previously rejected hash and follows the requested direction by adding explicit leaf-local `::` transitions: Ask_StartAC -> Manual on CA_backManual, AutocontrolInit -> Manual on CB_backManual, AutocontrolNormal -> Manual on TerminateAC and CP_backManual, and PumpFault -> Manual on CC_backManual. This partially resolves the earlier unresolved-event problem: local simulation now passes 11 of 12 scenarios instead of 7 of 12."}`
  - SL-10 evidence 3: `{"summary": "However, local deterministic evidence still reports a hard-block scenario regression. In scenario `cb_cp_cc_backmanual_forced_recovery`, step `cb_from_autocontrol_init` injects `CB_backManual` from `CARA.Mode_Control_Algorithm.AutocontrolInit` and expects `CARA.Mode_Control_Algorithm.Manual` with CA_mode=0, control_released=1, control_voltage=0, pump_speed=3, flow_rate=9, shared_buffer_bp=81. Actual state is `CARA.Mode_Control_Algorithm.AutocontrolNormal` with CA_mode=1, control_released=0, control_voltage=19, pump_speed=19, flow_rate=19, shared_buffer_bp=81. This indicates the unconditional `AutocontrolInit -> AutocontrolNormal` transition is taking priority over the added `Aut...<truncated 60 chars>`
  - SL-10 evidence 4: `{"summary": "Local evidence also reports new blocking design diagnostics for `W_SHADOWED_EVENT`: the added leaf-local events such as `CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual` shadow broader chain events such as `CARA.Mode_Control_Algorithm.CA_backManual` from the preserved forced declarations. Because the candidate keeps both the broad forced `! * -> Manual :: ...` declarations and same-named leaf-local event transitions, event scope is ambiguous and requires repair rather than override."}`
  - SL-10 evidence 5: `{"summary": "The local checker still reports missing_required_grounding for event:TerminateAC, event:CA_backManual, event:CB_backManual, event:CP_backManual, event:CC_backManual, transition:initial:CARA.Mode_Control_Algorithm, and transition:initial:Manual. Although the DSL text appears to preserve the initial transitions and represent the events, this cannot be overridden because the CB_backManual hard-block scenario still fails and the new shadowed-event diagnostics show the event representation is not yet locally clean."}`
- SL-10 rework_instructions：Fix `cb_cp_cc_backmanual_forced_recovery` by ensuring `CB_backManual` from `AutocontrolInit` takes precedence over the unconditional `AutocontrolInit -> AutocontrolNormal` transition. In the DSL, place or otherwise define `AutocontrolInit -> Manual :: CB_backManual` so it is considered before the untriggered `AutocontrolInit -> AutocontrolNormal` transition,...<truncated 111 chars>；After the CB repair, the scenario `cb_cp_cc_backmanual_forced_recovery` step `cb_from_autocontrol_init` must reach `CARA.Mode_Control_Algorithm.Manual` and Manual enter/during behavior must yield CA_mode=0, control_released=1, control_voltage=0, pump_speed=manual_switch_speed=3, flow_rate=default_flow_rate=9, and shared_buffer_bp=patient_bp=81.；Eliminate the `W_SHADOWED_EVENT` design problem by avoiding duplicate same-named local and chain events. Do not keep both the broad `! * -> Manual :: CA_backManual` / `CB_backManual` / `CP_backManual` / `CC_backManual` / `TerminateAC` declarations and same-named leaf-local `::` transitions unless the DSL syntax provides a non-shadowing way to reference the s...<truncated 93 chars>；If removing or replacing the broad forced declarations to avoid shadowing, provide concrete NL-grounded equivalents for the required fallback obligations: CA_backManual from Ask_StartAC to Manual, CB_backManual from AutocontrolInit to Manual, TerminateAC from AutocontrolNormal to Manual, CP_backManual from AutocontrolNormal to Manual, and CC_backManual from ...<truncated 252 chars>；Preserve all required NL-grounded structure and behavior: states CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault; variables including CA_mode, patient_bp, shared_buffer_bp, target_bp, requested_target_bp, flow_rate, default_flow_rate, manual_switch_speed, pump_speed, control_voltage, pump_fault, alarm_signal, ...<truncated 327 chars>；In the next SL-9 rationale, explicitly address the remaining local objections: why `CB_backManual` no longer loses to `AutocontrolInit -> AutocontrolNormal`, how shadowed event names were removed or made unambiguous, and how the reported missing grounding IDs are concretely represented or intentionally mapped to equivalent DSL elements.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_SHADOWED_EVENT", "instance_key": "W_SHADOWED_EVENT:9a2adf8046b5", "message": "Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.", "policy_action": "requires_policy_classification", "pyfcstm_severity": "warning", "rationale": "", "refs": {"chain_path": "CARA.Mode_Control_Algorithm.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.Mode_Control_Alg...<truncated 4786 chars>
    - local evidence 2: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 12, "n_scenarios_passed": 11, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: first cycle dispatches to Manual and manual-mode outputs follow caregiver pump settings and sensor buffering.", "name": "default_init_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_signal": 0, "control...<truncated 13814 chars>
    - local evidence 3: `missing_required_grounding` {"element_ids": ["event:TerminateAC", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:initial:CARA.Mode_Control_Algorithm", "transition:initial:Manual"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `0` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`ca_backmanual_forces_manual_from_ask_startac, cb_cp_cc_backmanual_forced_recovery, terminate_ac_forces_manual_from_normal, cp_backmanual_forces_manual_from_normal, cc_backmanual_forces_manual_from_pumpfault`。
- before_dsl_hash：`sha256:f88d4617840d4d21aa52334cf7dcb6426a3a03f81299a2e688cc68cfe891374d`；candidate_dsl_hash：`sha256:43958c2c35783741aaad6ed9cd4ea74838bd73029d1b20852b1458ce78872fa1`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-a1b0c413df1`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`5`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-0cac400bb2` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CA_backManual is a cross-component fallback from Ask_StartAC to the shared Manual recovery target.', 'name': 'ca_backmanual_forces_manual_from_ask_startac', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CA_backManual is a cross-component fallback from Ask_StartAC to the shared Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 0, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 6, 'pump_speed': 4, 'shared_buffer_bp': 82}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC' while resolving event reference 'CA_backManual'", 'runtime_error_hint': {'event_path': 'CA_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'ca_fallback_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'default_flow_rate': 6, 'manual_switch_speed': 4, 'patient_bp': 82}, 'scenario_name': 'ca_backmanual_forces_manual_from_ask_startac', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 6, 'error_display': 0, 'error_sound': 0, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 82, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC' while resolving event reference 'CA_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_fallback_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-1090ceac6d` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CB_backManual, CP_backManual, and CC_backManual each force different autocontrol-related leaves back to Manual.', 'name': 'cb_cp_cc_backmanual_forced_recovery', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CB_backManual, CP_backManual, and CC_backManual each force different autocontrol-related leaves back to Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 0, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 9, 'pump_speed': 3, 'shared_buffer_bp': 81}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CB_backManual'", 'runtime_error_hint': {'event_path': 'CB_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cb_from_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'default_flow_rate': 9, 'manual_switch_speed': 3, 'patient_bp': 81}, 'scenario_name': 'cb_cp_cc_backmanual_forced_recovery', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 9, 'error_display': 0, 'error_sound': 0, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 3, 'patient_bp': 81, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CB_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cb_from_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-2-15b38cfc79` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: TerminateAC from normal autocontrol releases algorithmic pump control and returns to Manual recovery operation.', 'name': 'terminate_ac_forces_manual_from_normal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: TerminateAC from normal autocontrol releases algorithmic pump control and returns to Manual recovery operation.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 22, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 11, 'pump_speed': 2, 'shared_buffer_bp': 77}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'TerminateAC' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'TerminateAC'", 'runtime_error_hint': {'event_path': 'TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_lands_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 22, 'default_flow_rate': 11, 'manual_switch_speed': 2, 'patient_bp': 77, 'pump_fault': 0, 'target_bp': 100}, 'scenario_name': 'terminate_ac_forces_manual_from_normal', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'control_voltage': 22, 'default_flow_rate': 11, 'error_display': 0, 'error_sound': 0, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 2, 'patient_bp': 77, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'TerminateAC' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'TerminateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_lands_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-bd3fee27ff` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CP_backManual must be a real forced fallback from AutocontrolNormal, so removing that forced line leaves the system wrongly in autocontrol.', 'name': 'cp_backmanual_forces_manual_from_normal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CP_backManual must be a real forced fallback from AutocontrolNormal, so removing that forced line leaves the system wrongly in autocontrol.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 0, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 13, 'pump_speed': 6, 'shared_buffer_bp': 84}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CP_backManual'", 'runtime_error_hint': {'event_path': 'CP_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cp_forced_from_normal_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'control_released': 0, 'default_flow_rate': 13, 'manual_switch_speed': 6, 'patient_bp': 84, 'pump_fault': 0, 'target_bp': 100}, 'scenario_name': 'cp_backmanual_forces_manual_from_normal', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 13, 'error_display': 0, 'error_sound': 0, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 6, 'patient_bp': 84, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CP_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_forced_from_normal_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-c17c8c07ff` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual must force recovery even from PumpFault; if the forced transition is missing, the machine remains in PumpFault.', 'name': 'cc_backmanual_forces_manual_from_pumpfault', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CC_backManual must force recovery even from PumpFault; if the forced transition is missing, the machine remains in PumpFault.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 1, 'control_released': 0, 'control_voltage': 0, 'flow_rate': 0, 'pump_speed': 0, 'shared_buffer_bp': 0}, 'before_cycles': 0, 'events': ['CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_released': 1, 'control_voltage': 0, 'flow_rate': 10, 'pump_speed': 8, 'shared_buffer_bp': 86}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CC_backManual'", 'runtime_error_hint': {'event_path': 'CC_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cc_forced_from_fault_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 1, 'control_released': 0, 'default_flow_rate': 10, 'error_display': 1, 'error_sound': 1, 'manual_switch_speed': 8, 'patient_bp': 86, 'pump_fault': 1}, 'scenario_name': 'cc_backmanual_forces_manual_from_pumpfault', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'control_released': 0, 'control_voltage': 0, 'default_flow_rate': 10, 'error_display': 1, 'error_sound': 1, 'flow_rate': 0, 'log_flow_rate': 0, 'manual_switch_speed': 8, 'patient_bp': 86, 'pump_fault': 1, 'pump_speed': 0, 'requested_target_bp': 100, 'shared_buffer_bp': 0, 'target_bp': 100}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CC_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cc_forced_from_fault_to_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:CARA, state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:patient_bp, variable:shared_buffer_bp, variable:target_bp, variable:requested_target_bp, ... +37`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3663`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-0cac400bb2` | `accept` | ❌ | ✅ | Accepted because the rework-locked scenario ca_backmanual_forces_manual_from_ask_startac requires CA_backManual injected from Ask_StartAC to resolve and reach Manual. The repair keeps Manual recovery and makes CA_backManual a concrete source-owned local event transition without retaining the shadowing broad forced declaration.；intent=Remove shadowing broad f...<truncated 98 chars> |
| `fixreq-0-sd6-1-1090ceac6d` | `accept` | ❌ | ✅ | Accepted because cb_cp_cc_backmanual_forced_recovery is rework-locked and still failed when CB_backManual from AutocontrolInit lost to the unconditional AutocontrolInit -> AutocontrolNormal transition. The repair places AutocontrolInit -> Manual :: CB_backManual before the unconditional advance and also makes CB/CP/CC fallback events resolvable from Manual f...<truncated 245 chars> |
| `fixreq-0-sd6-2-15b38cfc79` | `accept` | ❌ | ✅ | Accepted because TerminateAC from AutocontrolNormal must release algorithmic control to Manual. The repair keeps a concrete AutocontrolNormal -> Manual :: TerminateAC event transition and removes the broader shadowing declaration.；intent=Represent TerminateAC as an explicit AutocontrolNormal -> Manual :: TerminateAC transition. |
| `fixreq-0-sd6-3-bd3fee27ff` | `accept` | ❌ | ✅ | Accepted because CP_backManual from AutocontrolNormal must reach Manual with Manual entry/during outputs. The repair adds explicit source-owned CP_backManual transitions to Manual and avoids duplicate local/chain event shadowing.；intent=Represent CP_backManual as explicit local fallback transitions to Manual. |
| `fixreq-0-sd6-4-c17c8c07ff` | `accept` | ❌ | ✅ | Accepted because CC_backManual from PumpFault must reach Manual and the multi-step recovery scenario also injects CC_backManual while already in Manual. The repair adds explicit PumpFault -> Manual and Manual -> Manual local CC_backManual transitions.；intent=Represent CC_backManual as explicit local fallback transitions to Manual, including Manual self-recov...<truncated 4 chars> |
- repair_rationale：Addressed ca_backmanual_forces_manual_from_ask_startac: expected CA_backManual from Ask_StartAC to reach CARA.Mode_Control_Algorithm.Manual with CA_mode=0, control_released=1, control_voltage=0, pump_speed=4, flow_rate=6, shared_buffer_bp=8...<truncated 196 chars>；Addressed cb_cp_cc_backmanual_forced_recovery: expected CB_backManual from AutocontrolInit to reach Manual, but previous actual advanced to AutocontrolNormal because the untriggered transition was considered first. AutocontrolInit -> Manual...<truncated 118 chars>；Addressed the same cb_cp_cc_backmanual_forced_recovery multi-step recovery behavior by adding Manual self-transitions for CA_backManual, CB_backManual, CP_backManual, and CC_backManual. Thus CP/CC events injected while already in Manual are...<truncated 48 chars>；Addressed terminate_ac_forces_manual_from_normal with AutocontrolNormal -> Manual :: TerminateAC, preserving caregiver termination of algorithmic pump control and allowing Manual entry/during to clear control_voltage and use manual pump set...<truncated 6 chars>；Addressed cp_backmanual_forces_manual_from_normal with AutocontrolNormal -> Manual :: CP_backManual, preserving the shared Manual recovery target.
- diff_summary：`{"summary": "Removed the five broad forced fallback declarations that caused shadowed event diagnostics. Added explicit local :: fallback transitions to Manual for CA_backManual, CB_backManual, CP_backManual, and CC_backManual from Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault as appropriate; added/kept AutocontrolNormal -> Manual :: TerminateAC. Placed AutocontrolInit fallback transitions before the unconditional AutocontrolInit -> AutocontrolNormal transition so CB_backManual cannot be bypassed. Preserved all states, variables, initial transitions, manual/autocontrol/fault actions, normal flow computation, and existing InitiateAC/ChangeSetpoint/StartAC/FaultRemoved...<truncated 12 chars>`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int patient_bp = 0;
def int shared_buffer_bp = 0;
def int target_bp = 100;
def int requested_target_bp = 100;
def int flow_rate = 0;
def int default_flow_rate = 0;
def int manual_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_display = 0;
def int error_sound = 0;
def int control_released = 1;
def int log_flow_rate = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                control_released = 1;
                control_voltage = 0;
            }
            during {
                pump_speed = manual_switch_speed;
                flow_rate = default_flow_rate;
                shared_buffer_bp = patient_bp;
            }
        }

        state Ask_StartAC {
            during {
                shared_buffer_bp = patient_bp;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                control_released = 0;
                alarm_signal = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                shared_buffer_bp = patient_bp;
            }
        }

        state AutocontrolNormal {
            during {
                shared_buffer_bp = patient_bp;
                if [patient_bp >= target_bp] {
                    flow_rate = 0;
                } else {
                    flow_rate = target_bp - patient_bp;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_flow_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                error_display = 1;
                error_sound = 1;
                control_released = 1;
                CA_mode = 0;
                control_voltage = 0;
            }
            during {
                shared_buffer_bp = patient_bp;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Manual -> Manual :: CA_backManual;
        Manual -> Manual :: CB_backManual;
        Manual -> Manual :: CP_backManual;
        Manual -> Manual :: CC_backManual;

        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        Ask_StartAC -> Manual :: CA_backManual;
        Ask_StartAC -> Manual :: CB_backManual;
        Ask_StartAC -> Manual :: CP_backManual;
        Ask_StartAC -> Manual :: CC_backManual;

        AutocontrolInit -> Manual :: CA_backManual;
        AutocontrolInit -> Manual :: CB_backManual;
        AutocontrolInit -> Manual :: CP_backManual;
        AutocontrolInit -> Manual :: CC_backManual;
        AutocontrolInit -> AutocontrolNormal;

        AutocontrolNormal -> Manual :: TerminateAC;
        AutocontrolNormal -> Manual :: CA_backManual;
        AutocontrolNormal -> Manual :: CB_backManual;
        AutocontrolNormal -> Manual :: CP_backManual;
        AutocontrolNormal -> Manual :: CC_backManual;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];

        PumpFault -> Manual :: CA_backManual;
        PumpFault -> Manual :: CB_backManual;
        PumpFault -> Manual :: CP_backManual;
        PumpFault -> Manual :: CC_backManual;
        PumpFault -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            alarm_signal = 0;
            error_display = 0;
            error_sound = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -19,12 +19,6 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
-        ! * -> Manual :: TerminateAC;
-
         [*] -> Manual;
 
         state Manual {
@@ -88,10 +82,35 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
+        Manual -> Manual :: CA_backManual;
+        Manual -> Manual :: CB_backManual;
+        Manual -> Manual :: CP_backManual;
+        Manual -> Manual :: CC_backManual;
+
         Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
         Ask_StartAC -> AutocontrolInit :: StartAC;
+        Ask_StartAC -> Manual :: CA_backManual;
+        Ask_StartAC -> Manual :: CB_backManual;
+        Ask_StartAC -> Manual :: CP_backManual;
+        Ask_StartAC -> Manual :: CC_backManual;
+
+        AutocontrolInit -> Manual :: CA_backManual;
+        AutocontrolInit -> Manual :: CB_backManual;
+        AutocontrolInit -> Manual :: CP_backManual;
+        AutocontrolInit -> Manual :: CC_backManual;
         AutocontrolInit -> AutocontrolNormal;
+
+        AutocontrolNormal -> Manual :: TerminateAC;
+        AutocontrolNormal -> Manual :: CA_backManual;
+        AutocontrolNormal -> Manual :: CB_backManual;
+        AutocontrolNormal -> Manual :: CP_backManual;
+        AutocontrolNormal -> Manual :: CC_backManual;
         AutocontrolNormal -> PumpFault : if [pump_fault > 0];
+
+        PumpFault -> Manual :: CA_backManual;
+        PumpFault -> Manual :: CB_backManual;
+        PumpFault -> Manual :: CP_backManual;
+        PumpFault -> Manual :: CC_backManual;
         PumpFault -> Manual :: FaultRemoved effect {
             pump_fault = 0;
             alarm_signal = 0;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:65e1de11c9f5b1256314ad00c44a64c3f6d901e8dfc1fdafec1c53660d9e9831`。
  - SL-10 evidence 1: `{"summary": "The NL requires Manual and autocontrol-related mode-control states, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, BP-based inverse flow computation, fault alarm/release behavior, and shared Manual recovery for CA_backManual and any of CB_backManual, CP_backManual, or CC_backManual. The candidate preserves all required states, variables, initial transitions, Manual actions, Ask_StartAC ChangeSetpoint/StartAC behavior, AutocontrolNormal flow computation, PumpFault behavior, and FaultRemoved behavior."}`
  - SL-10 evidence 2: `{"summary": "The complete FixLog shows two prior rejected repairs: first, changing broad forced transitions from `::` to `:` left all five injected events unresolved; second, adding leaf-local transitions while keeping broad forced declarations fixed most scenarios but introduced W_SHADOWED_EVENT diagnostics and allowed CB_backManual from AutocontrolInit to lose to the unconditional AutocontrolInit -> AutocontrolNormal transition. The current candidate is a new hash and directly follows the latest rework guidance: it removes the broad shadowing declarations, represents fallback events with explicit local `::` transitions, places AutocontrolInit fallback transitions before the unconditional A...<truncated 129 chars>`
  - SL-10 evidence 3: `{"summary": "For `ca_backmanual_forces_manual_from_ask_startac`, the candidate provides `Ask_StartAC -> Manual :: CA_backManual`; Manual enter/during then yields CA_mode=0, control_released=1, control_voltage=0, pump_speed=manual_switch_speed, flow_rate=default_flow_rate, and shared_buffer_bp=patient_bp. For `cb_cp_cc_backmanual_forced_recovery`, the candidate provides `AutocontrolInit -> Manual :: CB_backManual` before the untriggered advance and provides Manual self-transitions for CB_backManual, CP_backManual, and CC_backManual. For `terminate_ac_forces_manual_from_normal`, `cp_backmanual_forces_manual_from_normal`, and `cc_backmanual_forces_manual_from_pumpfault`, the candidate provides ...<truncated 153 chars>`
  - SL-10 evidence 4: `{"summary": "The latest local check reports no scenario regression, unlike the previous 7/12 and 11/12 simulation failures. Its remaining objections are structural matcher objections: forced transition count drift and missing_required_grounding for event/forced-transition IDs and initial transitions. The candidate text still contains the required initial transitions `[ * ] -> Mode_Control_Algorithm` and `[ * ] -> Manual` and concrete event-triggered transitions for TerminateAC, CA_backManual, CB_backManual, CP_backManual, and CC_backManual. Thus the hard simulation obligations that motivated the batch are resolved for purposes of the next full top-down revalidation pass."}`
  - SL-10 evidence 5: `{"candidate_dsl_hash": "sha256:43958c2c35783741aaad6ed9cd4ea74838bd73029d1b20852b1458ce78872fa1", "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:84c46f9497f12f0c44ce9d260e92d227047cddfdb2393d1d6289bfa2b3b92e7a", "local_override_rationale_count": 5, "local_override_rationale_hash": "sha256:4110118520a456fd79e412f1a5f6b6fb3529e766bab6924cc9726d27ac1b045a", "local_rejection_evidence_hash": "sha256:a672808686f89ad4e46e5025e06533286498993f314113d8a1dc0e3d0ea2f8b9", "local_rejection_reason": "forced_transition_count_drift; missing_required_grounding", "policy": "SL-10 may override conservative local major-drift evidence only when local_override_rationale explicitl...<truncated 225 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 0, "old": 25}
    - local evidence 2: `missing_required_grounding` {"element_ids": ["event:TerminateAC", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:initial:CARA.Mode_Control_Algorithm", "transition:initial:Manual", "transition:forced_CA_backManual", "transition:forced_CB_backManual", "transition:forced_CP_backManual", "transition:forced_CC_backManual", "transition:forced_TerminateAC"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-a1b0c413df1` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-a1b0c413df1` | accept=5, reject=0 | `sl10_review` | `sha256:e364c76c12431bc1cc447e1d140ecd4a15437c4501440c519594c8ab7a94695a` | Addressed ca_backmanual_forces_manual_from_ask_startac: expected Manual with CA_mode = 0, control_released = 1, control_voltage = 0, pump_speed = manual_switch_speed, flow_rate = default_flow_rate, and shared_buffer_bp = patient_bp; actual failed before transition because CA_backManual was unresolved. The forced transition remains NL-grounded and now uses parent-chain event scope., Addressed cb_cp_cc_backmanual_forced_recovery: expected CB_backManual from AutocontrolInit to force Manual and run Manual entry/during actions; actual failed because CB_backManual was unresolved. Parent-chain scope makes the shared fallback event visible., Addressed terminate_ac_forces_manual_from_normal: expected TerminateAC from AutocontrolNormal to release algorithmic control and return to Manual; actual failed because TerminateAC was unresolved. Parent-chain scope is appropriate for this caregiver termination event applying across the mode-control hierarchy., ... +4 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-a1b0c413df1` | accept=5, reject=0 | `sl9_rework` | `sha256:e364c76c12431bc1cc447e1d140ecd4a15437c4501440c519594c8ab7a94695a` | Do not keep the current `! * -> Manual : CA_backManual` / `: CB_backManual` / `: CP_backManual` / `: CC_backManual` / `: TerminateAC` form as the sole representation, because local simulation still cannot resolve those events and the local grounding check no longer recognizes them as required events., Repair the fallback events with DSL-visible event transitions from the hot-start/source leaves used by the failing scenarios. At minimum, add or restore resolvable `::` event transitions so that `CA_backManual` is visible from Ask_StartAC, `CB_backManual` is visible from AutocontrolInit, `TerminateAC` is visible from AutocontrolNormal, `CP_backManual` is visible from AutocontrolNormal, and `CC_backManual` is visible from PumpFault, each targeting Manual., Prefer an NL-faithful representation of the cross-component fallback by adding explicit source-owned transitions for the autocontrol-related leaves, e.g. from Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault to Manual for CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC as appropriate, using the event syntax that local simulation resolves (`::`). Preserve Manual as the shared recovery target., ... +18 |
| 4 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-a1b0c413df1` | accept=5, reject=0 | `sl10_review` | `sha256:4e45221702cf0f2e4287194cb63691e7859e97cd53d7322b8d366a6812b90ec0` | This is not the previously rejected hash: the prior rejected candidate only changed forced fallback event syntax to parent-chain `:`. This candidate preserves the original NL-grounded forced `::` fallback declarations and adds concrete leaf-local `::` event transitions from the exact hot-start states named by SL-10., ca_backmanual_forces_manual_from_ask_startac: expected CA_backManual from Ask_StartAC to reach CARA.Mode_Control_Algorithm.Manual with Manual outputs; actual remained Ask_StartAC because CA_backManual was unresolved. The added Ask_StartAC -> Manual :: CA_backManual makes the event visible from Ask_StartAC., cb_cp_cc_backmanual_forced_recovery: expected CB_backManual from AutocontrolInit to reach Manual with CA_mode reset and manual pump outputs; actual remained AutocontrolInit because CB_backManual was unresolved. The added AutocontrolInit -> Manual :: CB_backManual makes the event visible from AutocontrolInit., ... +7 |
| 5 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-a1b0c413df1` | accept=5, reject=0 | `sl9_rework` | `sha256:4e45221702cf0f2e4287194cb63691e7859e97cd53d7322b8d366a6812b90ec0` | Fix `cb_cp_cc_backmanual_forced_recovery` by ensuring `CB_backManual` from `AutocontrolInit` takes precedence over the unconditional `AutocontrolInit -> AutocontrolNormal` transition. In the DSL, place or otherwise define `AutocontrolInit -> Manual :: CB_backManual` so it is considered before the untriggered `AutocontrolInit -> AutocontrolNormal` transition, or change the transition structure so an injected CB_backManual cannot be bypassed by the untriggered advance., After the CB repair, the scenario `cb_cp_cc_backmanual_forced_recovery` step `cb_from_autocontrol_init` must reach `CARA.Mode_Control_Algorithm.Manual` and Manual enter/during behavior must yield CA_mode=0, control_released=1, control_voltage=0, pump_speed=manual_switch_speed=3, flow_rate=default_flow_rate=9, and shared_buffer_bp=patient_bp=81., Eliminate the `W_SHADOWED_EVENT` design problem by avoiding duplicate same-named local and chain events. Do not keep both the broad `! * -> Manual :: CA_backManual` / `CB_backManual` / `CP_backManual` / `CC_backManual` / `TerminateAC` declarations and same-named leaf-local `::` transitions unless the DSL syntax provides a non-shadowing way to reference the same event. Prefer one consistent representation that is resolvable from the hot-start leaves., ... +21 |
| 6 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-a1b0c413df1` | accept=5, reject=0 | `sl10_review` | `sha256:43958c2c35783741aaad6ed9cd4ea74838bd73029d1b20852b1458ce78872fa1` | Addressed ca_backmanual_forces_manual_from_ask_startac: expected CA_backManual from Ask_StartAC to reach CARA.Mode_Control_Algorithm.Manual with CA_mode=0, control_released=1, control_voltage=0, pump_speed=4, flow_rate=6, shared_buffer_bp=82; previous actual was unresolved or remained Ask_StartAC. Ask_StartAC -> Manual :: CA_backManual is now a concrete local event transition, and Manual enter/during supplies the expected variables., Addressed cb_cp_cc_backmanual_forced_recovery: expected CB_backManual from AutocontrolInit to reach Manual, but previous actual advanced to AutocontrolNormal because the untriggered transition was considered first. AutocontrolInit -> Manual :: CB_backManual is now listed before AutocontrolInit -> AutocontrolNormal, so the event transition takes precedence., Addressed the same cb_cp_cc_backmanual_forced_recovery multi-step recovery behavior by adding Manual self-transitions for CA_backManual, CB_backManual, CP_backManual, and CC_backManual. Thus CP/CC events injected while already in Manual are resolvable and keep the shared recovery target., ... +7 |
| 7 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-a1b0c413df1` | accept=5, reject=0 | `sc11_accept_then_sd2` | `sha256:43958c2c35783741aaad6ed9cd4ea74838bd73029d1b20852b1458ce78872fa1` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +4 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5225, 'completion_chars': 20475, 'completion_tokens': 6546, 'elapsed_seconds': 121.02293585398002, 'estimated_completion_tokens': 5119, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11776, 'first_chunk_seconds': 29.48569661899819, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12996}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2765, 'completion_chars': 11390, 'completion_tokens': 4128, 'elapsed_seconds': 77.99719166901195, 'estimated_completion_tokens': 2848, 'estimated_prompt_tokens': 15228, 'estimated_total_tokens': 18076, 'first_chunk_seconds': 31.769156302994816, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 60912, 'prompt_tokens': 14906, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 19034}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2178, 'completion_chars': 8925, 'completion_tokens': 2619, 'elapsed_seconds': 49.2371416479873, 'estimated_completion_tokens': 2232, 'estimated_prompt_tokens': 18241, 'estimated_total_tokens': 20473, 'first_chunk_seconds': 11.178569082985632, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 72961, 'prompt_tokens': 17790, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20409}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3293, 'completion_chars': 13507, 'completion_tokens': 3812, 'elapsed_seconds': 71.04251246099011, 'estimated_completion_tokens': 3377, 'estimated_prompt_tokens': 18770, 'estimated_total_tokens': 22147, 'first_chunk_seconds': 12.465862476004986, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 75078, 'prompt_tokens': 18318, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22130}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1923, 'completion_chars': 8527, 'completion_tokens': 2442, 'elapsed_seconds': 48.13491266898927, 'estimated_completion_tokens': 2132, 'estimated_prompt_tokens': 41660, 'estimated_total_tokens': 43792, 'first_chunk_seconds': 13.573650976002682, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 166640, 'prompt_tokens': 36576, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 39018}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1030, 'completion_chars': 4608, 'completion_tokens': 1441, 'elapsed_seconds': 29.57259243700537, 'estimated_completion_tokens': 1152, 'estimated_prompt_tokens': 59897, 'estimated_total_tokens': 61049, 'first_chunk_seconds': 12.21897546100081, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 239588, 'prompt_tokens': 49305, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 50746}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2169, 'completion_chars': 9364, 'completion_tokens': 2888, 'elapsed_seconds': 55.50141757901292, 'estimated_completion_tokens': 2341, 'estimated_prompt_tokens': 93851, 'estimated_total_tokens': 96192, 'first_chunk_seconds': 21.41056588399806, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 375403, 'prompt_tokens': 75068, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 77956}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1339, 'completion_chars': 5920, 'completion_tokens': 2268, 'elapsed_seconds': 44.287547960993834, 'estimated_completion_tokens': 1480, 'estimated_prompt_tokens': 47760, 'estimated_total_tokens': 49240, 'first_chunk_seconds': 22.664606998005183, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 191040, 'prompt_tokens': 41930, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 44198}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2388, 'completion_chars': 10544, 'completion_tokens': 3219, 'elapsed_seconds': 62.953218705020845, 'estimated_completion_tokens': 2636, 'estimated_prompt_tokens': 162562, 'estimated_total_tokens': 165198, 'first_chunk_seconds': 23.885242245014524, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 650245, 'prompt_tokens': 127636, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 130855}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1168, 'completion_chars': 5595, 'completion_tokens': 1687, 'elapsed_seconds': 33.89629552999395, 'estimated_completion_tokens': 1399, 'estimated_prompt_tokens': 74753, 'estimated_total_tokens': 76152, 'first_chunk_seconds': 12.927652042999398, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 299011, 'prompt_tokens': 64391, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 66078}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4010, 'completion_chars': 16420, 'completion_tokens': 4445, 'elapsed_seconds': 82.04867926801671, 'estimated_completion_tokens': 4105, 'estimated_prompt_tokens': 22137, 'estimated_total_tokens': 26242, 'first_chunk_seconds': 10.709625793009764, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 88546, 'prompt_tokens': 21759, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26204}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4446, 'completion_chars': 18260, 'completion_tokens': 5292, 'elapsed_seconds': 99.64357181699597, 'estimated_completion_tokens': 4565, 'estimated_prompt_tokens': 22865, 'estimated_total_tokens': 27430, 'first_chunk_seconds': 20.323356918001082, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 91459, 'prompt_tokens': 22476, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 27768}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1678, 'completion_chars': 8029, 'completion_tokens': 2197, 'elapsed_seconds': 42.53768568998203, 'estimated_completion_tokens': 2008, 'estimated_prompt_tokens': 23887, 'estimated_total_tokens': 25895, 'first_chunk_seconds': 14.250796773994807, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 95547, 'prompt_tokens': 23674, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25871}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`34/16`，missing=`<none>`。
- repairs：`1/3` accepted；scenario_history=`6`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
