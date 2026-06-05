## path1 / cara-infusion-pump-formal-spec__01 / default 真实运行结果：Path1 CARA representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`not_converged`；record_status：`rejected`；result_status：`not_converged`。
- main_result_eligible：`false`。
- Path2 ref-model blueprint eligible：`n/a`；reason：not_applicable_to_path1。
- 一句话结论：`repair_review_rework_budget`；停止原因：SD-6 sim failure: 8/14 scenarios passed。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `cara-infusion-pump-formal-spec__01` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `min_sl10_rework_attempts=1`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `3794aa417982d9a1adb750ac0d2e0df7b3bdf2c9` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:e2cfdd7ab1fd43540a75a5216158706cc6809d0eb975e3731e90124b8a1ff158` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e` |
| final verdict/status | verdict=`not_converged`, record=`rejected`, result=`not_converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"final_dsl_hash": "sha256:3fbbdf9ad90a60957e2527a007b291fb9036bb1ac49e8bfbe004c84ca1f5854f", "last_rejected_candidate": {"candidate_dsl_hash": "sha256:e5e4732ddabeadd184806360d715999a302cfb465ecda022876f12fbe08a2d14", "iteration": 0, "repair_history_index": 4, "rework_instructions": ["Repair StartAC visibility from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart to CARA.Mode_Control_Algorithm.AutocontrolInit. The current line `! Ask_StartAC -> AutocontrolInit : StartAC;` did not resolve from the AwaitStart leaf, so do not return the same candidate unchanged.", "Do not reuse the previously rejected StartAC forms: do not use `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC`, do not use dotted source `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;`, do not use non-forced `Ask_StartAC -> AutocontrolInit : StartAC;`, and do not use `! Ask_StartAC -> AutocontrolInit :: StartAC;`.", "Try the narrowest syntactically valid DSL mechanism that the runtime resolves from nested leaves. If the DSL supports only wildcard forced parent-scope events for descendant visibility, try `! * -> AutocontrolInit : StartAC;` at Mode_Control_Algorithm scope and document in repair_rationale that this is an admitted abstraction of the NL-scoped StartAC obligation because all composite/leaf-specific StartAC forms failed parse, semantic, or runtime resolution. If a guard or priority mechanism exists to constrain it to Ask_StartAC, use that narrower form.", "Preserve AutocontrolInit as a sibling of Ask_StartAC under Mode_Control_Algorithm; do not move AutocontrolInit inside Ask_StartAC merely to satisfy name resolution.", "Preserve `AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; };` exactly so initiate_ac_change_setpoint_and_start step change_setpoint_updates_target_bp continues to pass with target_bp=requested_target_bp.", "Preserve `AutocontrolInit -> Manual :: TerminateAC;` before `AutocontrolInit -> AutocontrolNormal;` so terminate_ac_from_init_and_normal remains passing with Manual recovery variables restored.", "Fix the CP_backManual shadowing diagnostic. Avoid having both a broader `CP_backManual` chain event and a local `Manual.CP_backManual` with the same leaf name unless the repair_rationale explicitly proves this is required and unambiguous. Prefer consistent trigger scoping for all CP_backManual transitions, or remove the Manual self transition if it is not required by the scenarios.", "Ensure CP_backManual from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart reaches Manual with CA_mode=0, software_control=0, pump_control_voltage=0, alarms cleared, pump_speed=manual_switch_speed, and infusion_rate=default_flow_rate. The local brief previously showed this as a remaining failure, so verify it after any scoping changes.", "Preserve the already-passing backManual behavior for CA_backManual from AutocontrolNormal, CB_backManual from PumpFault, and CC_backManual from AutocontrolInit: each must enter Manual and run Manual recovery actions.", "Address count_drift and forced_transition_count_drift in the next SL-9 rationale. Either restore the necessary forced fallback coverage from the non-regressive frontier, or explicitly justify the smaller transition set as behaviorally equivalent using local scenario evidence.", "In the next repair_rationale, explicitly map concrete DSL lines to the grounding ids reported missing: `[ * ] -> Mode_Control_Algorithm`, `[ * ] -> Manual`, the ChangeSetpoint effect assigning `target_bp = requested_target_bp`, StartAC, CA_backManual, CB_backManual, CP_backManual, CC_backManual, `if [pump_fault == 0]`, and `infusion_log_count = infusion_log_count + 1`.", "Before returning, run local parse, semantic, design, and simulation checks. The repaired candidate must make initiate_ac_change_setpoint_and_start step start_ac_enters_autocontrol_init resolve StartAC from Ask_StartAC.AwaitStart and enter AutocontrolInit with CA_mode=1, software_control=1, alarm_active=0, display_error=0, and sound_alarm=0."], "same_as_final": false, "sl10_decision": "rework"}, "source_kind": "initial_or_unrepaired"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, exit_rejected_rework_budget_exhausted` |
| iteration exit_reason 序列 | `SD-6 sim failure: 8/14 scenarios passed` |
| token/cost/time | tokens=`{'prompt_tokens': 766602, 'completion_tokens': 45505, 'total_tokens': 812107, 'estimated_prompt_tokens': 865697, 'estimated_completion_tokens': 34171, 'estimated_total_tokens': 899868, 'prompt_chars': 3462765, 'completion_chars': 136662, 'n_calls': 14, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`886.309s` |
| run record | [`pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:d1a1b9c0eb2d38611770409d0f628779e01d52a37d53acab5680cb4debee5438` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `21` |
| `langgraph_node_trace_hash` | `sha256:2ee9ba0f28eb3bd6ceaa61221cefa25f97e04a01c3a29007325ca202f38f7a6a` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `21` |

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
def int target_bp = 120;
def int requested_target_bp = 120;
def int infusion_rate = 0;
def int default_flow_rate = 0;
def int manual_switch_speed = 0;
def int pump_speed = 0;
def int pump_control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int display_error = 0;
def int sound_alarm = 0;
def int software_control = 0;
def int infusion_log_count = 0;

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
                pump_control_voltage = 0;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
            during {
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            [*] -> AwaitStart;

            state AwaitStart;

            AwaitStart -> AwaitStart :: ChangeSetpoint effect {
                target_bp = requested_target_bp;
            };
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_fault == 0] {
                    infusion_rate = target_bp - patient_bp;
                    pump_control_voltage = infusion_rate;
                    infusion_log_count = infusion_log_count + 1;
                } else {
                    pump_control_voltage = 0;
                }
            }
        }

        state PumpFault {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 1;
                display_error = 1;
                sound_alarm = 1;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolNormal -> Manual :: TerminateAC;
        AutocontrolNormal -> PumpFault :: OcclusionFault effect {
            pump_fault = 1;
        };
        PumpFault -> Manual :: FaultRemoved effect {
            pump_fault = 0;
        };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14448 | 生成初始 DSL 与 grounding seeds | initial len=2702 | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=23, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=65221 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=65221 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=65221 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=444816 | LLM per-request accept/reject + repair | candidate len=2702,2709,2697,3560,2882 | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=287622 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=444816 | LLM per-request accept/reject + repair | candidate len=2702,2709,2697,3560,2882 | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=287622 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=444816 | LLM per-request accept/reject + repair | candidate len=2702,2709,2697,3560,2882 | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=287622 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=444816 | LLM per-request accept/reject + repair | candidate len=2702,2709,2697,3560,2882 | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=287622 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=444816 | LLM per-request accept/reject + repair | candidate len=2702,2709,2697,3560,2882 | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=287622 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SD-6 sim failure: 8/14 scenarios passed | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-final-3794aa41-05b66e9e.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T13:58:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T13:58:46Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T13:58:46Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T13:58:46Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T14:01:13Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T14:01:13Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2702,hash=sha256:3fbbdf9ad90a |
| 7 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T14:01:13Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:3fbbdf9ad90a60957e2527a007b291fb9036bb1ac49e8bfbe004c84ca1f5854f |
| 10 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T14:01:13Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2702,hash=sha256:3fbbdf9ad90a, current_hash=sha256:3fbbdf9ad90a60957e2527a007b291fb9036bb1ac49e8bfbe004c84ca1f5854f |
| 12 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T14:01:13Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T14:01:13Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T14:01:13Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T14:01:13Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T14:01:13Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T14:01:13Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T14:01:13Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T14:01:13Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T14:02:28Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T14:02:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T14:02:28Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T14:02:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T14:02:28Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T14:03:42Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T14:03:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T14:03:43Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T14:03:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T14:03:43Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T14:05:00Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T14:05:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T14:05:00Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T14:05:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T14:05:00Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T14:05:00Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T14:05:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T14:05:00Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T14:05:00Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 42 | `2026-06-05T14:05:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T14:05:00Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 14, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 44 | `2026-06-05T14:05:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T14:05:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-05T14:05:00Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 14, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2702,hash=sha256:3fbbdf9ad90a |
| 47 | `2026-06-05T14:05:00Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 48 | `2026-06-05T14:05:00Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 6} | <none> |
| 49 | `2026-06-05T14:05:00Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2702,hash=sha256:3fbbdf9ad90a |
| 50 | `2026-06-05T14:06:16Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 51 | `2026-06-05T14:06:16Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-09d3998124", "fixreq-0-sd6-1-2244c80013", "fixreq-0-sd6-2-0b7ad9e35b", "fixreq-0-sd6-3-989dda703e", "fixreq-0-sd6-4-775e5adc2d", "fixreq-0-sd6-5-1e8441f72f"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2702,hash=sha256:afd645ff2326 |
| 52 | `2026-06-05T14:06:16Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 53 | `2026-06-05T14:06:16Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:afd645ff2326b1f3d5efd929079528585f115dbbf4775fbf1b92e78188f2e18a |
| 54 | `2026-06-05T14:06:43Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 55 | `2026-06-05T14:06:43Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 56 | `2026-06-05T14:06:43Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2702,hash=sha256:3fbbdf9ad90a |
| 57 | `2026-06-05T14:07:29Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 58 | `2026-06-05T14:07:29Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-09d3998124", "fixreq-0-sd6-1-2244c80013", "fixreq-0-sd6-2-0b7ad9e35b", "fixreq-0-sd6-3-989dda703e", "fixreq-0-sd6-4-775e5adc2d", "fixreq-0-sd6-5-1e8441f72f"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2709,hash=sha256:dff1fe0e2a5e |
| 59 | `2026-06-05T14:07:29Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 60 | `2026-06-05T14:07:29Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:dff1fe0e2a5e437d0f7b3ee9c9a9ae74dcd6bd82233a8c90adf7bff3dec3a669 |
| 61 | `2026-06-05T14:07:57Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 62 | `2026-06-05T14:07:57Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 63 | `2026-06-05T14:07:57Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 64 | `2026-06-05T14:07:57Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2702,hash=sha256:3fbbdf9ad90a |
| 65 | `2026-06-05T14:08:44Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 66 | `2026-06-05T14:08:44Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-09d3998124", "fixreq-0-sd6-1-2244c80013", "fixreq-0-sd6-2-0b7ad9e35b", "fixreq-0-sd6-3-989dda703e", "fixreq-0-sd6-4-775e5adc2d", "fixreq-0-sd6-5-1e8441f72f"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2697,hash=sha256:cb98c02d15b6 |
| 67 | `2026-06-05T14:08:44Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 68 | `2026-06-05T14:08:44Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:cb98c02d15b6d76d55750a603a7ed90a8c109137c97a5acc7c2fb9b7db95e703 |
| 69 | `2026-06-05T14:09:18Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 70 | `2026-06-05T14:09:18Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 71 | `2026-06-05T14:09:18Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 72 | `2026-06-05T14:09:18Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2702,hash=sha256:3fbbdf9ad90a |
| 73 | `2026-06-05T14:10:35Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 74 | `2026-06-05T14:10:35Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-09d3998124", "fixreq-0-sd6-1-2244c80013", "fixreq-0-sd6-2-0b7ad9e35b", "fixreq-0-sd6-3-989dda703e", "fixreq-0-sd6-4-775e5adc2d", "fixreq-0-sd6-5-1e8441f72f"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=3560,hash=sha256:0ff7fe87ef63 |
| 75 | `2026-06-05T14:10:36Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 76 | `2026-06-05T14:10:36Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:0ff7fe87ef63a59441ab611029685acf2ad9c0b8636053998f540052bfce9b43 |
| 77 | `2026-06-05T14:11:25Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 78 | `2026-06-05T14:11:25Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 79 | `2026-06-05T14:11:25Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 80 | `2026-06-05T14:11:25Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2702,hash=sha256:3fbbdf9ad90a |
- ……另有 `14` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-6` | yes | fixbatch-0-sha256-1c5f60aebf5 / n=6 | accept=6, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; scenario_regression; count_drift; forced_transition_count_drift; missing_required_ground...<truncated 3 char...<truncated 2 chars> | decision=rework, ok=False, target=False, regression=True, drift=major, rework=Repair StartAC visibility from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart to CARA.Mode_Control_Algorithm.AutocontrolInit. The current ...<truncated 496 chars> | no | SD-6 sim failure: 8/14 scenarios passed |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_manual_operation_outputs` | default-init: first cycle dispatches to Manual, where manual switch speed and default flow rate drive pump_speed and inf...<truncated 11 chars> | ✅ |
| `initiate_ac_change_setpoint_and_start` | default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters Autocontrol...<truncated 5 chars> | ⚪ |
| `autocontrol_init_advances_to_normal_and_computes_flow` | explicit-hot-start: AutocontrolInit completes to AutocontrolNormal, which computes lower flow from higher patient pressu...<truncated 38 chars> | ✅ |
| `normal_autocontrol_high_pressure_lower_flow` | explicit-hot-start: AutocontrolNormal uses patient blood pressure to compute infusion rate, with higher pressure produci...<truncated 14 chars> | ✅ |
| `occlusion_fault_activates_alarm_and_releases_control` | explicit-hot-start: OcclusionFault during normal autocontrol enters PumpFault, activates alarms and error indications, a...<truncated 29 chars> | ✅ |
| `fault_removed_returns_to_manual_recovery` | explicit-hot-start: after caregiver removes the fault, CARA returns to Manual recovery with alarms cleared and manual pu...<truncated 19 chars> | ✅ |
| `terminate_ac_from_init_and_normal` | explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control. | ❌ |
| `terminate_ac_from_autocontrol_normal` | explicit-hot-start: caregiver TerminateAC from normal autocontrol returns to the shared Manual target and releases softw...<truncated 12 chars> | ✅ |
| `forced_back_manual_events_from_distinct_states` | explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mo...<truncated 10 chars> | ⚪ |
| `forced_back_manual_event_variants` | explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery tar...<truncated 24 chars> | ⚪ |
| `cp_back_manual_forces_from_ask_start` | explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, de...<truncated 52 chars> | ⚪ |
| `cc_back_manual_forces_from_autocontrol_init` | explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery tar...<truncated 33 chars> | ⚪ |
| `occlusion_fault_effect_sets_fault_flag` | explicit-hot-start: OcclusionFault must both target PumpFault and set pump_fault before PumpFault alarm/release actions,...<truncated 54 chars> | ✅ |
| `fault_removed_effect_clears_fault_flag` | explicit-hot-start: FaultRemoved must target Manual and clear pump_fault, detecting a missing transition effect even tho...<truncated 32 chars> | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_operation_outputs` — default-init: first cycle dispatches to Manual, where manual switch speed and default flow rate drive pump_speed and infusion_rate.</summary>

| Field | Value |
|---|---|
| description | default-init: first cycle dispatches to Manual, where manual switch speed and default flow rate drive pump_speed and infusion_rate. |
| initial_state | `<default-init>` |
| initial_vars | `{"default_flow_rate": 3, "manual_switch_speed": 7}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "display_error": 0, "infusion_rate": 3, "pump_control_voltage": 0, "pump_speed": 7, "software_control": 0, "sound_alarm": 0}` |

</details>

<details><summary>`initiate_ac_change_setpoint_and_start` — default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit.</summary>

| Field | Value |
|---|---|
| description | default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit. |
| initial_state | `<default-init>` |
| initial_vars | `{"requested_target_bp": 130, "target_bp": 120}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0}` |
| 1 `initiate_enters_await_start` | `0` | `["InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart` | `{}` |
| 2 `change_setpoint_updates_target_bp` | `0` | `["ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart` | `{"target_bp": 130}` |
| 3 `start_ac_enters_autocontrol_init` | `0` | `["StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_active": 0, "display_error": 0, "software_control": 1, "sound_alarm": 0}` |

</details>

<details><summary>`autocontrol_init_advances_to_normal_and_computes_flow` — explicit-hot-start: AutocontrolInit completes to AutocontrolNormal, which computes lower flow from higher patient pressure and logs data when no fault exists.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: AutocontrolInit completes to AutocontrolNormal, which computes lower flow from higher patient pressure and logs data when no fault exists. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "infusion_log_count": 0, "patient_bp": 100, "pump_fault": 0, "software_control": 1, "target_bp": 120}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `normal_autocontrol_computes_and_logs` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"infusion_log_count": 1, "infusion_rate": 20, "pump_control_voltage": 20}` |

</details>

<details><summary>`normal_autocontrol_high_pressure_lower_flow` — explicit-hot-start: AutocontrolNormal uses patient blood pressure to compute infusion rate, with higher pressure producing lower flow.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: AutocontrolNormal uses patient blood pressure to compute infusion rate, with higher pressure producing lower flow. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"infusion_log_count": 4, "patient_bp": 130, "pump_fault": 0, "target_bp": 120}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `high_pressure_yields_lower_flow_and_log_increment` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"infusion_log_count": 5, "infusion_rate": -10, "pump_control_voltage": -10}` |

</details>

<details><summary>`occlusion_fault_activates_alarm_and_releases_control` — explicit-hot-start: OcclusionFault during normal autocontrol enters PumpFault, activates alarms and error indications, and releases software control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: OcclusionFault during normal autocontrol enters PumpFault, activates alarms and error indications, and releases software control. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 0, "display_error": 0, "pump_control_voltage": 15, "pump_fault": 0, "software_control": 1, "sound_alarm": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_enters_pump_fault` | `0` | `["OcclusionFault"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_active": 1, "display_error": 1, "pump_control_voltage": 0, "pump_fault": 1, "software_control": 0, "sound_alarm": 1}` |

</details>

<details><summary>`fault_removed_returns_to_manual_recovery` — explicit-hot-start: after caregiver removes the fault, CARA returns to Manual recovery with alarms cleared and manual pump settings active.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: after caregiver removes the fault, CARA returns to Manual recovery with alarms cleared and manual pump settings active. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"alarm_active": 1, "default_flow_rate": 2, "display_error": 1, "manual_switch_speed": 6, "pump_fault": 1, "software_control": 1, "sound_alarm": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_removed_manual_recovery` | `0` | `["FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "display_error": 0, "infusion_rate": 2, "pump_fault": 0, "pump_speed": 6, "software_control": 0, "sound_alarm": 0}` |

</details>

<details><summary>`terminate_ac_from_init_and_normal` — explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "default_flow_rate": 1, "manual_switch_speed": 4, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_from_init_to_manual` | `0` | `["TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "infusion_rate": 1, "pump_speed": 4, "software_control": 0}` |
| 1 `manual_recovery_remains_asserted` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0}` |

</details>

<details><summary>`terminate_ac_from_autocontrol_normal` — explicit-hot-start: caregiver TerminateAC from normal autocontrol returns to the shared Manual target and releases software control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: caregiver TerminateAC from normal autocontrol returns to the shared Manual target and releases software control. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "default_flow_rate": 5, "manual_switch_speed": 8, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_from_normal_to_manual` | `0` | `["TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "infusion_rate": 5, "pump_speed": 8, "software_control": 0}` |

</details>

<details><summary>`forced_back_manual_events_from_distinct_states` — explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mode Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mode Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "default_flow_rate": 2, "manual_switch_speed": 9, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_back_manual_from_normal` | `0` | `["CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "infusion_rate": 2, "pump_speed": 9, "software_control": 0}` |

</details>

<details><summary>`forced_back_manual_event_variants` — explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery target with CA_mode Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery target with CA_mode Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 1, "default_flow_rate": 4, "display_error": 1, "manual_switch_speed": 5, "software_control": 1, "sound_alarm": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_back_manual_from_pump_fault` | `0` | `["CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "display_error": 0, "infusion_rate": 4, "pump_speed": 5, "software_control": 0, "sound_alarm": 0}` |
| 1 `manual_remains_manual_after_cp_back_manual` | `0` | `["CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "software_control": 0}` |
| 2 `manual_remains_manual_after_cc_back_manual` | `0` | `["CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "software_control": 0}` |

</details>

<details><summary>`cp_back_manual_forces_from_ask_start` — explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, detecting a missing forced transition or w...<truncated 12 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, detecting a missing forced transition or wrong target. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 0, "default_flow_rate": 6, "display_error": 0, "manual_switch_speed": 10, "software_control": 1, "sound_alarm": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_back_manual_from_await_start` | `0` | `["CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "display_error": 0, "infusion_rate": 6, "pump_control_voltage": 0, "pump_speed": 10, "software_control": 0, "sound_alarm": 0}` |

</details>

<details><summary>`cc_back_manual_forces_from_autocontrol_init` — explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery target with manual outputs restored.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery target with manual outputs restored. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 0, "default_flow_rate": 7, "display_error": 0, "manual_switch_speed": 11, "pump_control_voltage": 22, "software_control": 1, "sound_alarm": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_back_manual_from_init` | `0` | `["CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "display_error": 0, "infusion_rate": 7, "pump_control_voltage": 0, "pump_speed": 11, "software_control": 0, "sound_alarm": 0}` |

</details>

<details><summary>`occlusion_fault_effect_sets_fault_flag` — explicit-hot-start: OcclusionFault must both target PumpFault and set pump_fault before PumpFault alarm/release actions, detecting missing transition effect and...<truncated 14 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: OcclusionFault must both target PumpFault and set pump_fault before PumpFault alarm/release actions, detecting missing transition effect and wrong target. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 0, "display_error": 0, "pump_control_voltage": 18, "pump_fault": 0, "software_control": 1, "sound_alarm": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `occlusion_sets_flag_and_enters_fault` | `0` | `["OcclusionFault"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_active": 1, "display_error": 1, "pump_control_voltage": 0, "pump_fault": 1, "software_control": 0, "sound_alarm": 1}` |

</details>

<details><summary>`fault_removed_effect_clears_fault_flag` — explicit-hot-start: FaultRemoved must target Manual and clear pump_fault, detecting a missing transition effect even though Manual recovery actions run.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: FaultRemoved must target Manual and clear pump_fault, detecting a missing transition effect even though Manual recovery actions run. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"alarm_active": 1, "default_flow_rate": 8, "display_error": 1, "manual_switch_speed": 12, "pump_fault": 1, "software_control": 1, "sound_alarm": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_removed_clears_flag_and_manual_outputs` | `0` | `["FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "display_error": 0, "infusion_rate": 8, "pump_fault": 0, "pump_speed": 12, "software_control": 0, "sound_alarm": 0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-6` | initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, ... +1 | accept=6, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=False, drift=major, rework=Repair the dangling StartAC transition while preserving the intended SL-9 behavior. Do not leave `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC` unless ...<truncated 580 chars> | `sha256:afd645ff2326b1f3d5efd929079528585f115dbbf4775fbf1b92e78188f2e18a` |
| 2 | `0` | ❌ | `SD-6` | initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, ... +1 | accept=6, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=False, drift=major, rework=Fix the parse error by removing the unsupported dotted source transition `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;`., Do not revert to the previously rejected nes...<truncated 299 chars> | `sha256:dff1fe0e2a5e437d0f7b3ee9c9a9ae74dcd6bd82233a8c90adf7bff3dec3a669` |
| 3 | `0` | ❌ | `SD-6` | initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, ... +1 | accept=6, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Repair StartAC visibility from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart while keeping AutocontrolInit as a sibling of Ask_StartAC under Mode_Control_Algorithm. Do not...<truncated 967 chars> | `sha256:cb98c02d15b6d76d55750a603a7ed90a8c109137c97a5acc7c2fb9b7db95e703` |
| 4 | `0` | ❌ | `SD-6` | initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, ... +1 | accept=6, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Repair only the remaining StartAC visibility failure unless the full local brief shows additional scenario failures. Preserve `AutocontrolInit` as `CARA.Mode_Control_Algorithm....<truncated 753 chars> | `sha256:0ff7fe87ef63a59441ab611029685acf2ad9c0b8636053998f540052bfce9b43` |
| 5 | `0` | ❌ | `SD-6` | initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, ... +1 | accept=6, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Repair StartAC visibility from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart to CARA.Mode_Control_Algorithm.AutocontrolInit. The current line `! Ask_StartAC -> Autocontrol...<truncated 692 chars> | `sha256:e5e4732ddabeadd184806360d715999a302cfb465ecda022876f12fbe08a2d14` |

<details><summary>Repair 1 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, cc_back_manual_forces_from_autocontrol_init`。
- before_dsl_hash：`sha256:3fbbdf9ad90a60957e2527a007b291fb9036bb1ac49e8bfbe004c84ca1f5854f`；candidate_dsl_hash：`sha256:afd645ff2326b1f3d5efd929079528585f115dbbf4775fbf1b92e78188f2e18a`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-1c5f60aebf5`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`6`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-09d3998124` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit.', 'name': 'initiate_ac_change_setpoint_and_start', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars_focus': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'software_control': 0, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'software_control': 1, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'StartAC' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'StartAC'", 'runtime_error_hint': {'event_path': 'StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 3, 'step_name': 'start_ac_enters_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'requested_target_bp': 130, 'target_bp': 120}, 'scenario_name': 'initiate_ac_change_setpoint_and_start', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'dispatch_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'initiate_enters_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 130}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'change_setpoint_updates_target_bp', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 130}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'StartAC' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 3, 'step_name': 'start_ac_enters_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-2244c80013` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control.', 'name': 'terminate_ac_from_init_and_normal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'infusion_rate': 1, 'pump_speed': 4, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'infusion_rate': {'actual': 0, 'expected': 1}, 'pump_speed': {'actual': 0, 'expected': 4}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1}, 'before_cycles': 0, 'events': None, 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 1, 'step_name': 'manual_recovery_remains_asserted', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'default_flow_rate': 1, 'manual_switch_speed': 4, 'software_control': 1}, 'scenario_name': 'terminate_ac_from_init_and_normal', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 1, 'display_error': 0, 'infusion_log_count': 1, 'infusion_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'infusion_rate': {'actual': 0, 'expected': 1}, 'pump_speed': {'actual': 0, 'expected': 4}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 1, 'display_error': 0, 'infusion_log_count': 1, 'infusion_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 1, 'step_name': 'manual_recovery_remains_asserted', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}}}]}` |
| `fixreq-0-sd6-2-0b7ad9e35b` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mode Manual.', 'name': 'forced_back_manual_events_from_distinct_states', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mode Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'infusion_rate': 2, 'pump_speed': 9, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CA_backManual'", 'runtime_error_hint': {'event_path': 'CA_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'ca_back_manual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'default_flow_rate': 2, 'manual_switch_speed': 9, 'software_control': 1}, 'scenario_name': 'forced_back_manual_events_from_distinct_states', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 2, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 9, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CA_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_back_manual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-989dda703e` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery target with CA_mode Manual.', 'name': 'forced_back_manual_event_variants', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery target with CA_mode Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 1, 'display_error': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 1}, 'before_cycles': 0, 'events': ['CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 4, 'pump_speed': 5, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CB_backManual'", 'runtime_error_hint': {'event_path': 'CB_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_active': 1, 'default_flow_rate': 4, 'display_error': 1, 'manual_switch_speed': 5, 'software_control': 1, 'sound_alarm': 1}, 'scenario_name': 'forced_back_manual_event_variants', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 1, 'alarm_active': 1, 'default_flow_rate': 4, 'display_error': 1, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 5, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 1, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CB_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-775e5adc2d` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, detecting a missing forced transition or wrong target.', 'name': 'cp_back_manual_forces_from_ask_start', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, detecting a missing forced transition or wrong target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 0, 'pump_control_voltage': 0, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 6, 'pump_control_voltage': 0, 'pump_speed': 10, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'CP_backManual'", 'runtime_error_hint': {'event_path': 'CP_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cp_back_manual_from_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'initial_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 6, 'display_error': 0, 'manual_switch_speed': 10, 'software_control': 1, 'sound_alarm': 0}, 'scenario_name': 'cp_back_manual_forces_from_ask_start', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 6, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 10, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'CP_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_back_manual_from_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-5-1e8441f72f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery target with manual outputs restored.', 'name': 'cc_back_manual_forces_from_autocontrol_init', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery target with manual outputs restored.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 0, 'pump_control_voltage': 22, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 7, 'pump_control_voltage': 0, 'pump_speed': 11, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CC_backManual'", 'runtime_error_hint': {'event_path': 'CC_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cc_back_manual_from_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 7, 'display_error': 0, 'manual_switch_speed': 11, 'pump_control_voltage': 22, 'software_control': 1, 'sound_alarm': 0}, 'scenario_name': 'cc_back_manual_forces_from_autocontrol_init', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 7, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 11, 'patient_bp': 120, 'pump_control_voltage': 22, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CC_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cc_back_manual_from_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, hierarchical_state:Ask_StartAC, state:AwaitStart, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:patient_bp, variable:target_bp, variable:requested_target_bp, ... +43`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2702`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-09d3998124` | `accept` | ❌ | ❌ | The failing StartAC step is caused by StartAC being declared on the composite Ask_StartAC source, while the active state is the leaf Ask_StartAC.AwaitStart. I accept the request and make StartAC visible from the active leaf by moving the StartAC transition to AwaitStart while preserving the Ask_StartAC hierarchy and AutocontrolInit target.；intent=Change Star...<truncated 57 chars> |
| `fixreq-0-sd6-1-2244c80013` | `accept` | ❌ | ❌ | The TerminateAC hot-start from AutocontrolInit was preempted by the unconditional AutocontrolInit -> AutocontrolNormal transition. I accept the request and place the TerminateAC transition before the automatic initialization-complete transition so the caregiver termination event can return to Manual and run Manual recovery actions in the same cycle.；intent=P...<truncated 94 chars> |
| `fixreq-0-sd6-2-0b7ad9e35b` | `accept` | ❌ | ❌ | The CA_backManual fallback event was not resolvable from an autocontrol leaf because the forced transition used a local event form. This cross-component fallback is NL-grounded as a shared recovery signal, so I accept the request and encode it as a parent-scope forced event visible across descendants.；intent=Change CA_backManual forced transition to parent-s...<truncated 15 chars> |
| `fixreq-0-sd6-3-989dda703e` | `accept` | ❌ | ❌ | The CB_backManual variant similarly failed event resolution from PumpFault. I accept the request and encode the shared CB_backManual fallback as a parent-scope forced event while preserving the Manual recovery target.；intent=Change CB_backManual forced transition to parent-scope event form |
| `fixreq-0-sd6-4-775e5adc2d` | `accept` | ❌ | ❌ | The CP_backManual fallback from Ask_StartAC.AwaitStart failed event resolution. I accept the request and encode the shared CP_backManual fallback as a parent-scope forced event targeting Manual.；intent=Change CP_backManual forced transition to parent-scope event form |
| `fixreq-0-sd6-5-1e8441f72f` | `accept` | ❌ | ❌ | The CC_backManual fallback from AutocontrolInit failed event resolution and must preempt autocontrol. I accept the request and encode CC_backManual as a parent-scope forced event targeting Manual, with Manual.enter and Manual.during restoring release-control and manual outputs.；intent=Change CC_backManual forced transition to parent-scope event form |
- repair_rationale：For initiate_ac_change_setpoint_and_start, step start_ac_enters_autocontrol_init expected CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1 and software_control=1, but actual remained in Ask_StartAC.AwaitStart with an unresolved St...<truncated 188 chars>；For terminate_ac_from_init_and_normal, step terminate_from_init_to_manual expected Manual with CA_mode=0, software_control=0, pump_speed from manual_switch_speed, and infusion_rate from default_flow_rate, but the automatic AutocontrolInit -...<truncated 247 chars>；For forced_back_manual_events_from_distinct_states, CA_backManual from AutocontrolNormal expected the shared Manual recovery target but the event was unresolved. The repair encodes CA_backManual as a parent-scope forced event, which matches...<truncated 131 chars>；For forced_back_manual_event_variants, CB_backManual from PumpFault expected Manual with alarms cleared and manual outputs restored, but the event was unresolved. The repair uses the same parent-scope forced fallback form for CB_backManual.；For cp_back_manual_forces_from_ask_start, CP_backManual from Ask_StartAC.AwaitStart expected Manual and release of software control. The repair uses a parent-scope forced fallback form so the event is visible from nested Ask_StartAC leaves.
- diff_summary：`{"summary": "Changed the four backManual forced transitions from local-event scope (::) to parent-scope event form (:) for shared fallback visibility; moved StartAC from the composite Ask_StartAC source to the active AwaitStart leaf; placed AutocontrolInit -> Manual :: TerminateAC before the unconditional AutocontrolInit -> AutocontrolNormal transition so termination preempts automatic progression."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int patient_bp = 120;
def int target_bp = 120;
def int requested_target_bp = 120;
def int infusion_rate = 0;
def int default_flow_rate = 0;
def int manual_switch_speed = 0;
def int pump_speed = 0;
def int pump_control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int display_error = 0;
def int sound_alarm = 0;
def int software_control = 0;
def int infusion_log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
            during {
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            [*] -> AwaitStart;

            state AwaitStart;

            AwaitStart -> AwaitStart :: ChangeSetpoint effect {
                target_bp = requested_target_bp;
            };

            AwaitStart -> AutocontrolInit :: StartAC;
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_fault == 0] {
                    infusion_rate = target_bp - patient_bp;
                    pump_control_voltage = infusion_rate;
                    infusion_log_count = infusion_log_count + 1;
                } else {
                    pump_control_voltage = 0;
                }
            }
        }

        state PumpFault {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 1;
                display_error = 1;
                sound_alarm = 1;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual :: TerminateAC;
        AutocontrolNormal -> PumpFault :: OcclusionFault effect {
            pump_fault = 1;
        };
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
@@ -18,10 +18,10 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
+        ! * -> Manual : CA_backManual;
+        ! * -> Manual : CB_backManual;
+        ! * -> Manual : CP_backManual;
+        ! * -> Manual : CC_backManual;
 
         [*] -> Manual;
 
@@ -48,6 +48,8 @@
             AwaitStart -> AwaitStart :: ChangeSetpoint effect {
                 target_bp = requested_target_bp;
             };
+
+            AwaitStart -> AutocontrolInit :: StartAC;
         }
 
         state AutocontrolInit {
@@ -84,9 +86,8 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> AutocontrolInit :: StartAC;
+        AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolInit -> AutocontrolNormal;
-        AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolNormal -> Manual :: TerminateAC;
         AutocontrolNormal -> PumpFault :: OcclusionFault effect {
             pump_fault = 1;
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:dc9d2c39e22cd3168cbd2739204fbd009dfa98107119426658c4a72d1ec1f85b`。
  - SL-10 evidence 1: `{"summary": "SL-9 accepted all six hard simulation requests and the candidate addresses the intended behavioral causes: StartAC should be visible from the active AwaitStart leaf, TerminateAC from AutocontrolInit should preempt the unconditional AutocontrolInit-to-AutocontrolNormal transition, and CA/CB/CP/CC_backManual should be parent-scope forced fallbacks to Manual."}`
  - SL-10 evidence 2: `{"summary": "However, the candidate DSL is not semantically valid. Local deterministic evidence reports E_DANGLING_TRANSITION on `AwaitStart -> AutocontrolInit :: StartAC;` because that transition is declared inside `state Ask_StartAC`, where `AutocontrolInit` is not a child of Ask_StartAC and therefore cannot be resolved as a target."}`
  - SL-10 evidence 3: `{"summary": "This unresolved semantic error directly prevents acceptance for the next top-down revalidation pass. It also means the original scenario obligation `initiate_ac_change_setpoint_and_start` is not yet safely resolved: step `start_ac_enters_autocontrol_init` expects event `StartAC` from `CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart` to enter `CARA.Mode_Control_Algorithm.AutocontrolInit` with `CA_mode=1` and `software_control=1`, but the repaired transition currently has an invalid target reference."}`
  - SL-10 evidence 4: `{"summary": "The NL requires AutocontrolInit as an autocontrol-related mode-control state in the Mode_Control_Algorithm hierarchy, not nested under Ask_StartAC. Therefore the fix should preserve AutocontrolInit as a sibling of Ask_StartAC and adjust the transition reference/scope, rather than moving AutocontrolInit under Ask_StartAC."}`
- SL-10 rework_instructions：Repair the dangling StartAC transition while preserving the intended SL-9 behavior. Do not leave `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC` unless the DSL supports an explicit parent/sibling target reference. Prefer moving the StartAC transition to the `Mode_Control_Algorithm` scope and make its source the active leaf, e.g. `Ask_S...<truncated 101 chars>；Keep `AutocontrolInit` as a sibling state of `Ask_StartAC` under `Mode_Control_Algorithm`; do not nest AutocontrolInit inside Ask_StartAC just to satisfy name resolution.；Preserve the passing ChangeSetpoint behavior: `AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; };` must remain active from `Ask_StartAC.AwaitStart`.；Preserve the TerminateAC repair order: `AutocontrolInit -> Manual :: TerminateAC;` must remain before the unconditional `AutocontrolInit -> AutocontrolNormal;` so the hot-start scenario `terminate_ac_from_init_and_normal` returns to Manual with `CA_mode=0`, `software_control=0`, `pump_speed=manual_switch_speed`, and `infusion_rate=default_flow_rate`.；Preserve the parent-scope forced backManual edits for `CA_backManual`, `CB_backManual`, `CP_backManual`, and `CC_backManual` if the single-colon form is the valid DSL mechanism for events visible from descendant states; these are required by the NL cross-component fallback to shared Manual recovery.；After the StartAC scoping fix, ensure the candidate parses and passes semantic checks before returning it for SL-10.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`candidate semantic failed`，rejected_by_stage=`SD-10`。
    - local evidence 1: `<unknown>` {"code": "E_DANGLING_TRANSITION", "message": "Unknown to state 'AutocontrolInit' of transition:\nAwaitStart -> AutocontrolInit :: StartAC;", "refs": {"reason": "tgt_not_found", "src": "AwaitStart", "tgt": "AutocontrolInit"}, "severity": "error", "span": {"column": 13, "end_column": 54, "end_line": 52, "line": 52}}

</details>

<details><summary>Repair 2 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, cc_back_manual_forces_from_autocontrol_init`。
- before_dsl_hash：`sha256:3fbbdf9ad90a60957e2527a007b291fb9036bb1ac49e8bfbe004c84ca1f5854f`；candidate_dsl_hash：`sha256:dff1fe0e2a5e437d0f7b3ee9c9a9ae74dcd6bd82233a8c90adf7bff3dec3a669`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-1c5f60aebf5`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`6`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-09d3998124` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit.', 'name': 'initiate_ac_change_setpoint_and_start', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars_focus': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'software_control': 0, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'software_control': 1, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'StartAC' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'StartAC'", 'runtime_error_hint': {'event_path': 'StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 3, 'step_name': 'start_ac_enters_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'requested_target_bp': 130, 'target_bp': 120}, 'scenario_name': 'initiate_ac_change_setpoint_and_start', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'dispatch_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'initiate_enters_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 130}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'change_setpoint_updates_target_bp', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 130}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'StartAC' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 3, 'step_name': 'start_ac_enters_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-2244c80013` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control.', 'name': 'terminate_ac_from_init_and_normal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'infusion_rate': 1, 'pump_speed': 4, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'infusion_rate': {'actual': 0, 'expected': 1}, 'pump_speed': {'actual': 0, 'expected': 4}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1}, 'before_cycles': 0, 'events': None, 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 1, 'step_name': 'manual_recovery_remains_asserted', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'default_flow_rate': 1, 'manual_switch_speed': 4, 'software_control': 1}, 'scenario_name': 'terminate_ac_from_init_and_normal', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 1, 'display_error': 0, 'infusion_log_count': 1, 'infusion_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'infusion_rate': {'actual': 0, 'expected': 1}, 'pump_speed': {'actual': 0, 'expected': 4}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 1, 'display_error': 0, 'infusion_log_count': 1, 'infusion_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 1, 'step_name': 'manual_recovery_remains_asserted', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}}}]}` |
| `fixreq-0-sd6-2-0b7ad9e35b` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mode Manual.', 'name': 'forced_back_manual_events_from_distinct_states', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mode Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'infusion_rate': 2, 'pump_speed': 9, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CA_backManual'", 'runtime_error_hint': {'event_path': 'CA_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'ca_back_manual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'default_flow_rate': 2, 'manual_switch_speed': 9, 'software_control': 1}, 'scenario_name': 'forced_back_manual_events_from_distinct_states', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 2, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 9, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CA_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_back_manual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-989dda703e` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery target with CA_mode Manual.', 'name': 'forced_back_manual_event_variants', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery target with CA_mode Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 1, 'display_error': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 1}, 'before_cycles': 0, 'events': ['CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 4, 'pump_speed': 5, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CB_backManual'", 'runtime_error_hint': {'event_path': 'CB_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_active': 1, 'default_flow_rate': 4, 'display_error': 1, 'manual_switch_speed': 5, 'software_control': 1, 'sound_alarm': 1}, 'scenario_name': 'forced_back_manual_event_variants', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 1, 'alarm_active': 1, 'default_flow_rate': 4, 'display_error': 1, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 5, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 1, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CB_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-775e5adc2d` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, detecting a missing forced transition or wrong target.', 'name': 'cp_back_manual_forces_from_ask_start', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, detecting a missing forced transition or wrong target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 0, 'pump_control_voltage': 0, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 6, 'pump_control_voltage': 0, 'pump_speed': 10, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'CP_backManual'", 'runtime_error_hint': {'event_path': 'CP_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cp_back_manual_from_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'initial_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 6, 'display_error': 0, 'manual_switch_speed': 10, 'software_control': 1, 'sound_alarm': 0}, 'scenario_name': 'cp_back_manual_forces_from_ask_start', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 6, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 10, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'CP_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_back_manual_from_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-5-1e8441f72f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery target with manual outputs restored.', 'name': 'cc_back_manual_forces_from_autocontrol_init', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery target with manual outputs restored.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 0, 'pump_control_voltage': 22, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 7, 'pump_control_voltage': 0, 'pump_speed': 11, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CC_backManual'", 'runtime_error_hint': {'event_path': 'CC_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cc_back_manual_from_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 7, 'display_error': 0, 'manual_switch_speed': 11, 'pump_control_voltage': 22, 'software_control': 1, 'sound_alarm': 0}, 'scenario_name': 'cc_back_manual_forces_from_autocontrol_init', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 7, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 11, 'patient_bp': 120, 'pump_control_voltage': 22, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CC_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cc_back_manual_from_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, hierarchical_state:Ask_StartAC, state:AwaitStart, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:patient_bp, variable:target_bp, variable:requested_target_bp, ... +43`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2709`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-09d3998124` | `accept` | ❌ | ✅ | The StartAC failure is still actionable and rework-locked by SL-10. The prior candidate made StartAC local to AwaitStart but placed the transition inside Ask_StartAC, where the sibling AutocontrolInit target was semantically dangling. I preserve the intended behavior and move the StartAC transition to the Mode_Control_Algorithm scope using the active leaf so...<truncated 182 chars> |
| `fixreq-0-sd6-1-2244c80013` | `accept` | ❌ | ✅ | The TerminateAC hot-start failure remains valid. I preserve the non-regressive frontier behavior by keeping AutocontrolInit -> Manual :: TerminateAC before the unconditional AutocontrolInit -> AutocontrolNormal transition so TerminateAC preempts automatic progression and Manual actions restore manual outputs.；intent=Keep TerminateAC from AutocontrolInit orde...<truncated 76 chars> |
| `fixreq-0-sd6-2-0b7ad9e35b` | `accept` | ❌ | ✅ | The CA_backManual fallback failure remains valid. I preserve the parent-scope forced fallback repair from the non-regressive frontier so CA_backManual is visible as a shared cross-component recovery event and targets Manual.；intent=Keep ! * -> Manual : CA_backManual |
| `fixreq-0-sd6-3-989dda703e` | `accept` | ❌ | ✅ | The CB_backManual fallback variant remains valid. I preserve the parent-scope forced fallback repair so CB_backManual from PumpFault reaches Manual and Manual recovery actions clear alarms and restore manual outputs.；intent=Keep ! * -> Manual : CB_backManual |
| `fixreq-0-sd6-4-775e5adc2d` | `accept` | ❌ | ✅ | The CP_backManual fallback from Ask_StartAC.AwaitStart remains valid. I preserve the parent-scope forced fallback repair so the nested AwaitStart leaf can recover to Manual without changing the passing ChangeSetpoint behavior.；intent=Keep ! * -> Manual : CP_backManual |
| `fixreq-0-sd6-5-1e8441f72f` | `accept` | ❌ | ✅ | The CC_backManual fallback from AutocontrolInit remains valid. I preserve the parent-scope forced fallback repair so CC_backManual preempts autocontrol and enters Manual, where software control and pump control voltage are released.；intent=Keep ! * -> Manual : CC_backManual |
- repair_rationale：For initiate_ac_change_setpoint_and_start, the failing step start_ac_enters_autocontrol_init expected CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1 and software_control=1, but the prior candidate had a dangling AwaitStart -> Au...<truncated 332 chars>；For terminate_ac_from_init_and_normal, I preserve the frontier behavior: AutocontrolInit -> Manual :: TerminateAC remains before AutocontrolInit -> AutocontrolNormal, so a hot-start TerminateAC reaches Manual and Manual.enter/during restore...<truncated 100 chars>；For forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, and cc_back_manual_forces_from_autocontrol_init, I preserve the frontier parent-scope forced transitions ! * -> Man...<truncated 188 chars>；The passing ChangeSetpoint behavior is preserved inside Ask_StartAC.AwaitStart: AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; } remains unchanged.；AutocontrolInit remains a sibling of Ask_StartAC under Mode_Control_Algorithm, as required by SL-10 and the NL Mode_Control_Algorithm hierarchy; it is not nested under Ask_StartAC merely to satisfy target resolution.
- diff_summary：`{"summary": "Preserved the non-regressive frontier repairs for backManual parent-scope forced fallbacks and TerminateAC ordering, but fixed the SL-10 semantic rejection by moving the StartAC transition out of Ask_StartAC to Mode_Control_Algorithm scope as Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int patient_bp = 120;
def int target_bp = 120;
def int requested_target_bp = 120;
def int infusion_rate = 0;
def int default_flow_rate = 0;
def int manual_switch_speed = 0;
def int pump_speed = 0;
def int pump_control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int display_error = 0;
def int sound_alarm = 0;
def int software_control = 0;
def int infusion_log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
            during {
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            [*] -> AwaitStart;

            state AwaitStart;

            AwaitStart -> AwaitStart :: ChangeSetpoint effect {
                target_bp = requested_target_bp;
            };
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_fault == 0] {
                    infusion_rate = target_bp - patient_bp;
                    pump_control_voltage = infusion_rate;
                    infusion_log_count = infusion_log_count + 1;
                } else {
                    pump_control_voltage = 0;
                }
            }
        }

        state PumpFault {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 1;
                display_error = 1;
                sound_alarm = 1;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual :: TerminateAC;
        AutocontrolNormal -> PumpFault :: OcclusionFault effect {
            pump_fault = 1;
        };
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
@@ -18,10 +18,10 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
+        ! * -> Manual : CA_backManual;
+        ! * -> Manual : CB_backManual;
+        ! * -> Manual : CP_backManual;
+        ! * -> Manual : CC_backManual;
 
         [*] -> Manual;
 
@@ -84,9 +84,9 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> AutocontrolInit :: StartAC;
+        Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;
+        AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolInit -> AutocontrolNormal;
-        AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolNormal -> Manual :: TerminateAC;
         AutocontrolNormal -> PumpFault :: OcclusionFault effect {
             pump_fault = 1;
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:e2a7db00f2d3c6fdf9c414c59fce31dcce286171713e2e0b55868754de06ebb2`。
  - SL-10 evidence 1: `{"summary": "The current candidate preserves the NL-required states, variables, Manual recovery actions, TerminateAC ordering, ChangeSetpoint behavior, and parent-scope CA/CB/CP/CC_backManual fallback intent from the non-regressive frontier, but it is not acceptable for the next top-down revalidation pass because the DSL does not parse."}`
  - SL-10 evidence 2: `{"summary": "Local deterministic evidence reports candidate parse failed with SyntaxFailError at line 87, column 19: got '.', no viable alternative at input 'Ask_StartAC.'. This directly identifies the new StartAC repair line `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;` as invalid DSL syntax."}`
  - SL-10 evidence 3: `{"summary": "The FixLog shows the previous rejected candidate had semantically invalid `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC` because `AutocontrolInit` is a sibling under `Mode_Control_Algorithm`, not a child of `Ask_StartAC`. The current candidate correctly tries to keep `AutocontrolInit` as a sibling and move the StartAC transition to `Mode_Control_Algorithm` scope, but the dotted source path is not supported by the parser."}`
  - SL-10 evidence 4: `{"summary": "The original hard scenario `initiate_ac_change_setpoint_and_start` remains unresolved until StartAC is represented by a syntactically valid transition visible from the active `Ask_StartAC.AwaitStart` leaf and targeting sibling `AutocontrolInit`, with `CA_mode=1` and `software_control=1` set by `AutocontrolInit.enter`."}`
  - SL-10 evidence 5: `{"summary": "There is no evidence of behavioral regression beyond the parse failure: SL-9 intentionally preserved the non-regressive frontier repairs for TerminateAC preemption and CA/CB/CP/CC_backManual shared Manual fallback, which are NL-grounded by the caregiver termination and cross-component fallback requirements."}`
- SL-10 rework_instructions：Fix the parse error by removing the unsupported dotted source transition `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;`.；Do not revert to the previously rejected nested transition `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC`, because local semantic evidence already showed `AutocontrolInit` is dangling from that scope.；Use a syntactically valid DSL mechanism that makes StartAC visible from the active `Ask_StartAC.AwaitStart` leaf while targeting sibling `AutocontrolInit`. Given the DSL evidence that single-colon parent-scope events are valid for descendant visibility, prefer declaring at `Mode_Control_Algorithm` scope: `Ask_StartAC -> AutocontrolInit : StartAC;` if this pa...<truncated 50 chars>；Keep `AutocontrolInit` as a sibling of `Ask_StartAC` under `Mode_Control_Algorithm`; do not nest `AutocontrolInit` under `Ask_StartAC` merely to satisfy name resolution.；Preserve `AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; };` inside `Ask_StartAC` so the passing setpoint-change step remains active from `Ask_StartAC.AwaitStart`.；Preserve `AutocontrolInit -> Manual :: TerminateAC;` before the unconditional `AutocontrolInit -> AutocontrolNormal;` so `terminate_ac_from_init_and_normal` returns to Manual with `CA_mode=0`, `software_control=0`, `pump_speed=manual_switch_speed`, and `infusion_rate=default_flow_rate`.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`candidate parse failed`，rejected_by_stage=`SD-10`。
    - local evidence 1: `<unknown>` {"code": "SyntaxFailError", "col": 19, "got": ".", "line": 87, "message": "Invalid syntax - check for missing semicolons, braces, or operators", "raw_message": "no viable alternative at input 'Ask_StartAC.'"}

</details>

<details><summary>Repair 3 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, cc_back_manual_forces_from_autocontrol_init`。
- before_dsl_hash：`sha256:3fbbdf9ad90a60957e2527a007b291fb9036bb1ac49e8bfbe004c84ca1f5854f`；candidate_dsl_hash：`sha256:cb98c02d15b6d76d55750a603a7ed90a8c109137c97a5acc7c2fb9b7db95e703`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-1c5f60aebf5`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`6`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-09d3998124` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit.', 'name': 'initiate_ac_change_setpoint_and_start', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars_focus': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'software_control': 0, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'software_control': 1, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'StartAC' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'StartAC'", 'runtime_error_hint': {'event_path': 'StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 3, 'step_name': 'start_ac_enters_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'requested_target_bp': 130, 'target_bp': 120}, 'scenario_name': 'initiate_ac_change_setpoint_and_start', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'dispatch_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'initiate_enters_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 130}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'change_setpoint_updates_target_bp', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 130}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'StartAC' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 3, 'step_name': 'start_ac_enters_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-2244c80013` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control.', 'name': 'terminate_ac_from_init_and_normal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'infusion_rate': 1, 'pump_speed': 4, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'infusion_rate': {'actual': 0, 'expected': 1}, 'pump_speed': {'actual': 0, 'expected': 4}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1}, 'before_cycles': 0, 'events': None, 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 1, 'step_name': 'manual_recovery_remains_asserted', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'default_flow_rate': 1, 'manual_switch_speed': 4, 'software_control': 1}, 'scenario_name': 'terminate_ac_from_init_and_normal', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 1, 'display_error': 0, 'infusion_log_count': 1, 'infusion_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'infusion_rate': {'actual': 0, 'expected': 1}, 'pump_speed': {'actual': 0, 'expected': 4}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 1, 'display_error': 0, 'infusion_log_count': 1, 'infusion_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 1, 'step_name': 'manual_recovery_remains_asserted', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}}}]}` |
| `fixreq-0-sd6-2-0b7ad9e35b` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mode Manual.', 'name': 'forced_back_manual_events_from_distinct_states', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mode Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'infusion_rate': 2, 'pump_speed': 9, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CA_backManual'", 'runtime_error_hint': {'event_path': 'CA_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'ca_back_manual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'default_flow_rate': 2, 'manual_switch_speed': 9, 'software_control': 1}, 'scenario_name': 'forced_back_manual_events_from_distinct_states', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 2, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 9, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CA_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_back_manual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-989dda703e` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery target with CA_mode Manual.', 'name': 'forced_back_manual_event_variants', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery target with CA_mode Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 1, 'display_error': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 1}, 'before_cycles': 0, 'events': ['CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 4, 'pump_speed': 5, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CB_backManual'", 'runtime_error_hint': {'event_path': 'CB_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_active': 1, 'default_flow_rate': 4, 'display_error': 1, 'manual_switch_speed': 5, 'software_control': 1, 'sound_alarm': 1}, 'scenario_name': 'forced_back_manual_event_variants', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 1, 'alarm_active': 1, 'default_flow_rate': 4, 'display_error': 1, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 5, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 1, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CB_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-775e5adc2d` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, detecting a missing forced transition or wrong target.', 'name': 'cp_back_manual_forces_from_ask_start', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, detecting a missing forced transition or wrong target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 0, 'pump_control_voltage': 0, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 6, 'pump_control_voltage': 0, 'pump_speed': 10, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'CP_backManual'", 'runtime_error_hint': {'event_path': 'CP_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cp_back_manual_from_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'initial_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 6, 'display_error': 0, 'manual_switch_speed': 10, 'software_control': 1, 'sound_alarm': 0}, 'scenario_name': 'cp_back_manual_forces_from_ask_start', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 6, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 10, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'CP_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_back_manual_from_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-5-1e8441f72f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery target with manual outputs restored.', 'name': 'cc_back_manual_forces_from_autocontrol_init', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery target with manual outputs restored.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 0, 'pump_control_voltage': 22, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 7, 'pump_control_voltage': 0, 'pump_speed': 11, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CC_backManual'", 'runtime_error_hint': {'event_path': 'CC_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cc_back_manual_from_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 7, 'display_error': 0, 'manual_switch_speed': 11, 'pump_control_voltage': 22, 'software_control': 1, 'sound_alarm': 0}, 'scenario_name': 'cc_back_manual_forces_from_autocontrol_init', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 7, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 11, 'patient_bp': 120, 'pump_control_voltage': 22, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CC_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cc_back_manual_from_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, hierarchical_state:Ask_StartAC, state:AwaitStart, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:patient_bp, variable:target_bp, variable:requested_target_bp, ... +43`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2697`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-09d3998124` | `accept` | ❌ | ✅ | The request is rework-locked and the failing scenario initiate_ac_change_setpoint_and_start still needs StartAC to be visible while the active leaf is CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart and to target sibling AutocontrolInit. I accept it and use the SL-10-guided syntactically valid parent-scope transition Ask_StartAC -> AutocontrolInit : Start...<truncated 278 chars> |
| `fixreq-0-sd6-1-2244c80013` | `accept` | ❌ | ✅ | The request is rework-locked. The terminate_ac_from_init_and_normal scenario expected TerminateAC from AutocontrolInit to enter Manual and restore manual outputs, but the unconditional AutocontrolInit -> AutocontrolNormal transition preempted it. I accept it and preserve the non-regressive frontier ordering by placing AutocontrolInit -> Manual :: TerminateAC...<truncated 135 chars> |
| `fixreq-0-sd6-2-0b7ad9e35b` | `accept` | ❌ | ✅ | The request is rework-locked. The forced_back_manual_events_from_distinct_states scenario expected CA_backManual from AutocontrolNormal to resolve as a shared cross-component fallback to Manual. I accept it and preserve the parent-scope forced transition form required by the non-regressive frontier.；intent=Use ! * -> Manual : CA_backManual |
| `fixreq-0-sd6-3-989dda703e` | `accept` | ❌ | ✅ | The request is rework-locked. The forced_back_manual_event_variants scenario expected CB_backManual from PumpFault to resolve and enter Manual, clearing alarms through Manual.enter. I accept it and preserve the parent-scope forced transition form.；intent=Use ! * -> Manual : CB_backManual |
| `fixreq-0-sd6-4-775e5adc2d` | `accept` | ❌ | ✅ | The request is rework-locked. The cp_back_manual_forces_from_ask_start scenario expected CP_backManual from the nested Ask_StartAC.AwaitStart leaf to enter Manual. I accept it and preserve the parent-scope forced fallback so the event is visible from descendants without changing the passing ChangeSetpoint behavior.；intent=Use ! * -> Manual : CP_backManual |
| `fixreq-0-sd6-5-1e8441f72f` | `accept` | ❌ | ✅ | The request is rework-locked. The cc_back_manual_forces_from_autocontrol_init scenario expected CC_backManual from AutocontrolInit to preempt autocontrol and restore Manual outputs. I accept it and preserve the parent-scope forced transition form targeting Manual.；intent=Use ! * -> Manual : CC_backManual |
- repair_rationale：For initiate_ac_change_setpoint_and_start, step start_ac_enters_autocontrol_init expected StartAC from active Ask_StartAC.AwaitStart to reach CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1 and software_control=1. The prior rewor...<truncated 414 chars>；The passing ChangeSetpoint step is preserved exactly as AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; }; inside Ask_StartAC, so target_bp still updates from requested_target_bp while in AwaitStart.；For terminate_ac_from_init_and_normal, TerminateAC from AutocontrolInit must preempt the automatic transition to AutocontrolNormal. The repair preserves AutocontrolInit -> Manual :: TerminateAC before AutocontrolInit -> AutocontrolNormal, s...<truncated 140 chars>；For forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, and cc_back_manual_forces_from_autocontrol_init, the four NL-grounded cross-component fallback events are preserved...<truncated 110 chars>；This is a minimal syntax/scope repair from the latest non-regressive local-only frontier: it removes the unsupported dotted StartAC source, does not revert to the dangling nested AwaitStart transition, and preserves all required states, var...<truncated 134 chars>
- diff_summary：`{"summary": "Changed the StartAC repair to the parseable Mode_Control_Algorithm-scope transition Ask_StartAC -> AutocontrolInit : StartAC; preserved parent-scope forced backManual fallbacks; preserved ChangeSetpoint inside Ask_StartAC; and kept AutocontrolInit -> Manual :: TerminateAC before the unconditional AutocontrolInit -> AutocontrolNormal transition."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int patient_bp = 120;
def int target_bp = 120;
def int requested_target_bp = 120;
def int infusion_rate = 0;
def int default_flow_rate = 0;
def int manual_switch_speed = 0;
def int pump_speed = 0;
def int pump_control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int display_error = 0;
def int sound_alarm = 0;
def int software_control = 0;
def int infusion_log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
            during {
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            [*] -> AwaitStart;

            state AwaitStart;

            AwaitStart -> AwaitStart :: ChangeSetpoint effect {
                target_bp = requested_target_bp;
            };
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_fault == 0] {
                    infusion_rate = target_bp - patient_bp;
                    pump_control_voltage = infusion_rate;
                    infusion_log_count = infusion_log_count + 1;
                } else {
                    pump_control_voltage = 0;
                }
            }
        }

        state PumpFault {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 1;
                display_error = 1;
                sound_alarm = 1;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> AutocontrolInit : StartAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual :: TerminateAC;
        AutocontrolNormal -> PumpFault :: OcclusionFault effect {
            pump_fault = 1;
        };
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
@@ -18,10 +18,10 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
+        ! * -> Manual : CA_backManual;
+        ! * -> Manual : CB_backManual;
+        ! * -> Manual : CP_backManual;
+        ! * -> Manual : CC_backManual;
 
         [*] -> Manual;
 
@@ -84,9 +84,9 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> AutocontrolInit :: StartAC;
+        Ask_StartAC -> AutocontrolInit : StartAC;
+        AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolInit -> AutocontrolNormal;
-        AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolNormal -> Manual :: TerminateAC;
         AutocontrolNormal -> PumpFault :: OcclusionFault effect {
             pump_fault = 1;
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:a2cb36d2f0d5e9569e02184d7d7b8400e4219e552065ce9c17b9464da759523e`。
  - SL-10 evidence 1: `{"summary": "The candidate preserves the NL-required Mode_Control_Algorithm hierarchy, Manual/Ask_StartAC/AwaitStart/AutocontrolInit/AutocontrolNormal/PumpFault states, variables, ChangeSetpoint effect, TerminateAC ordering, and CA/CB/CP/CC_backManual shared Manual fallback intent from the FixLog frontier."}`
  - SL-10 evidence 2: `{"summary": "However, local deterministic evidence reports scenario_regression and target_resolved=false. The hard scenario initiate_ac_change_setpoint_and_start still fails at step start_ac_enters_autocontrol_init: event StartAC is injected from active state CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart, expected state CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1 and software_control=1, but actual remains CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart with CA_mode=0 and software_control=0, and runtime error says Event 'StartAC' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart'."}`
  - SL-10 evidence 3: `{"summary": "The current repair line Ask_StartAC -> AutocontrolInit : StartAC parses but does not make StartAC visible from the nested AwaitStart leaf under the simulator semantics. This does not resolve the original NL obligation that within Ask_StartAC pressing StartAC enters AutocontrolInit."}`
  - SL-10 evidence 4: `{"summary": "The FixLog repair_memory explicitly records two rejected StartAC forms: nested AwaitStart -> AutocontrolInit :: StartAC inside Ask_StartAC is semantically dangling because AutocontrolInit is a sibling, and dotted Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC is syntactically unsupported. The current candidate avoids those two forms but still fails the scenario, so further DSL repair is required rather than pass."}`
  - SL-10 evidence 5: `{"summary": "Local evidence also reports missing_required_grounding for transition:initial_root_to_mode_control, transition:initial_mode_control_to_manual, action:set_target_bp_from_requested, event:StartAC, event:CA_backManual, event:CB_backManual, event:CP_backManual, event:CC_backManual, guard:AutocontrolNormal_no_pump_fault, and action:AutocontrolNormal_log_data. Some of these appear concretely present in the DSL and may be matcher limitations, but event:StartAC is behaviorally confirmed unresolved and therefore cannot be overridden."}`
- SL-10 rework_instructions：Repair StartAC visibility from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart while keeping AutocontrolInit as a sibling of Ask_StartAC under Mode_Control_Algorithm. Do not use the previously rejected nested `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC`, and do not use the unsupported dotted source `Ask_StartAC.AwaitStart -> Auto...<truncated 25 chars>；The current line `Ask_StartAC -> AutocontrolInit : StartAC;` is insufficient because the simulator still reports StartAC not found from the AwaitStart leaf. Replace it with a syntactically valid DSL mechanism that is visible from descendants. A likely minimal next edit is to try a forced parent-scope transition constrained to the Ask_StartAC composite, e.g. ...<truncated 253 chars>；Preserve `AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; };` inside Ask_StartAC so the already-passing setpoint-change step continues to update target_bp from requested_target_bp while in AwaitStart.；Preserve `AutocontrolInit -> Manual :: TerminateAC;` before the unconditional `AutocontrolInit -> AutocontrolNormal;` so terminate_ac_from_init_and_normal continues to return to Manual with CA_mode=0, software_control=0, pump_speed=manual_switch_speed, and infusion_rate=default_flow_rate.；Preserve the four parent-scope forced Manual fallbacks `! * -> Manual : CA_backManual;`, `! * -> Manual : CB_backManual;`, `! * -> Manual : CP_backManual;`, and `! * -> Manual : CC_backManual;` because the NL requires all four cross-component backManual events to drive CA_mode to Manual as the shared recovery target.；Before returning the next candidate, run local parse/semantic/sim checks. The repaired candidate must make the initiate_ac_change_setpoint_and_start step start_ac_enters_autocontrol_init resolve StartAC from Ask_StartAC.AwaitStart and enter AutocontrolInit with CA_mode=1, software_control=1, alarm_active=0, display_error=0, and sound_alarm=0.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 14, "n_scenarios_passed": 9, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: first cycle dispatches to Manual, where manual switch speed and default flow rate drive pump_speed and infusion_rate.", "name": "default_init_manual_operation_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_act...<truncated 15360 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial_root_to_mode_control", "transition:initial_mode_control_to_manual", "action:set_target_bp_from_requested", "event:StartAC", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "guard:AutocontrolNormal_no_pump_fault", "action:AutocontrolNormal_log_data"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, cc_back_manual_forces_from_autocontrol_init`。
- before_dsl_hash：`sha256:3fbbdf9ad90a60957e2527a007b291fb9036bb1ac49e8bfbe004c84ca1f5854f`；candidate_dsl_hash：`sha256:0ff7fe87ef63a59441ab611029685acf2ad9c0b8636053998f540052bfce9b43`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-1c5f60aebf5`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`6`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-09d3998124` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit.', 'name': 'initiate_ac_change_setpoint_and_start', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars_focus': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'software_control': 0, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'software_control': 1, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'StartAC' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'StartAC'", 'runtime_error_hint': {'event_path': 'StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 3, 'step_name': 'start_ac_enters_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'requested_target_bp': 130, 'target_bp': 120}, 'scenario_name': 'initiate_ac_change_setpoint_and_start', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'dispatch_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'initiate_enters_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 130}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'change_setpoint_updates_target_bp', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 130}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'StartAC' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 3, 'step_name': 'start_ac_enters_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-2244c80013` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control.', 'name': 'terminate_ac_from_init_and_normal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'infusion_rate': 1, 'pump_speed': 4, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'infusion_rate': {'actual': 0, 'expected': 1}, 'pump_speed': {'actual': 0, 'expected': 4}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1}, 'before_cycles': 0, 'events': None, 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 1, 'step_name': 'manual_recovery_remains_asserted', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'default_flow_rate': 1, 'manual_switch_speed': 4, 'software_control': 1}, 'scenario_name': 'terminate_ac_from_init_and_normal', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 1, 'display_error': 0, 'infusion_log_count': 1, 'infusion_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'infusion_rate': {'actual': 0, 'expected': 1}, 'pump_speed': {'actual': 0, 'expected': 4}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 1, 'display_error': 0, 'infusion_log_count': 1, 'infusion_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 1, 'step_name': 'manual_recovery_remains_asserted', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}}}]}` |
| `fixreq-0-sd6-2-0b7ad9e35b` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mode Manual.', 'name': 'forced_back_manual_events_from_distinct_states', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mode Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'infusion_rate': 2, 'pump_speed': 9, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CA_backManual'", 'runtime_error_hint': {'event_path': 'CA_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'ca_back_manual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'default_flow_rate': 2, 'manual_switch_speed': 9, 'software_control': 1}, 'scenario_name': 'forced_back_manual_events_from_distinct_states', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 2, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 9, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CA_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_back_manual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-989dda703e` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery target with CA_mode Manual.', 'name': 'forced_back_manual_event_variants', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery target with CA_mode Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 1, 'display_error': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 1}, 'before_cycles': 0, 'events': ['CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 4, 'pump_speed': 5, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CB_backManual'", 'runtime_error_hint': {'event_path': 'CB_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_active': 1, 'default_flow_rate': 4, 'display_error': 1, 'manual_switch_speed': 5, 'software_control': 1, 'sound_alarm': 1}, 'scenario_name': 'forced_back_manual_event_variants', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 1, 'alarm_active': 1, 'default_flow_rate': 4, 'display_error': 1, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 5, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 1, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CB_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-775e5adc2d` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, detecting a missing forced transition or wrong target.', 'name': 'cp_back_manual_forces_from_ask_start', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, detecting a missing forced transition or wrong target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 0, 'pump_control_voltage': 0, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 6, 'pump_control_voltage': 0, 'pump_speed': 10, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'CP_backManual'", 'runtime_error_hint': {'event_path': 'CP_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cp_back_manual_from_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'initial_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 6, 'display_error': 0, 'manual_switch_speed': 10, 'software_control': 1, 'sound_alarm': 0}, 'scenario_name': 'cp_back_manual_forces_from_ask_start', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 6, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 10, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'CP_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_back_manual_from_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-5-1e8441f72f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery target with manual outputs restored.', 'name': 'cc_back_manual_forces_from_autocontrol_init', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery target with manual outputs restored.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 0, 'pump_control_voltage': 22, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 7, 'pump_control_voltage': 0, 'pump_speed': 11, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CC_backManual'", 'runtime_error_hint': {'event_path': 'CC_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cc_back_manual_from_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 7, 'display_error': 0, 'manual_switch_speed': 11, 'pump_control_voltage': 22, 'software_control': 1, 'sound_alarm': 0}, 'scenario_name': 'cc_back_manual_forces_from_autocontrol_init', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 7, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 11, 'patient_bp': 120, 'pump_control_voltage': 22, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CC_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cc_back_manual_from_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, hierarchical_state:Ask_StartAC, state:AwaitStart, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:patient_bp, variable:target_bp, variable:requested_target_bp, ... +43`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3560`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-09d3998124` | `accept` | ❌ | ✅ | The rework-locked initiate_ac_change_setpoint_and_start scenario still fails because StartAC is unresolved from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart. I avoid the previously rejected nested sibling-target transition and unsupported dotted source, and add a non-wildcard forced transition at Mode_Control_Algorithm scope from Ask_StartAC to sibling...<truncated 245 chars> |
| `fixreq-0-sd6-1-2244c80013` | `accept` | ❌ | ✅ | The terminate_ac_from_init_and_normal scenario is rework-locked and already passed in the frontier when AutocontrolInit -> Manual :: TerminateAC was ordered before the unconditional AutocontrolInit -> AutocontrolNormal transition. I preserve that ordering so TerminateAC preempts automatic progression and Manual recovery actions restore CA_mode, software_cont...<truncated 132 chars> |
| `fixreq-0-sd6-2-0b7ad9e35b` | `accept` | ❌ | ✅ | The forced_back_manual_events_from_distinct_states scenario still reports CA_backManual unresolved from AutocontrolNormal. The wildcard and parent-scope forms have been rejected by simulation evidence, so I encode NL-grounded local forced fallback coverage for each Mode_Control_Algorithm child, including AutocontrolNormal, targeting Manual.；intent=Add explic...<truncated 133 chars> |
| `fixreq-0-sd6-3-989dda703e` | `accept` | ❌ | ✅ | The forced_back_manual_event_variants scenario still reports CB_backManual unresolved from PumpFault. I add the same explicit local forced fallback coverage for CB_backManual across the mode-control children so PumpFault and other active modes can reach Manual and run Manual recovery actions.；intent=Add explicit non-wildcard forced CB_backManual transitions ...<truncated 84 chars> |
| `fixreq-0-sd6-4-775e5adc2d` | `accept` | ❌ | ✅ | The cp_back_manual_forces_from_ask_start scenario still reports CP_backManual unresolved from the nested Ask_StartAC.AwaitStart leaf. A non-wildcard forced transition from Ask_StartAC to Manual is used so descendants of Ask_StartAC can resolve the local CP_backManual event while preserving ChangeSetpoint in AwaitStart.；intent=Add explicit non-wildcard forced...<truncated 88 chars> |
| `fixreq-0-sd6-5-1e8441f72f` | `accept` | ❌ | ✅ | The cc_back_manual_forces_from_autocontrol_init scenario still reports CC_backManual unresolved from AutocontrolInit. I add explicit local forced fallback coverage for CC_backManual, including AutocontrolInit to Manual, so Manual.enter/during clears software control and restores manual outputs.；intent=Add explicit non-wildcard forced CC_backManual transition...<truncated 86 chars> |
- repair_rationale：For initiate_ac_change_setpoint_and_start, the failing step start_ac_enters_autocontrol_init expected StartAC from Ask_StartAC.AwaitStart to enter CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1 and software_control=1, but the pr...<truncated 270 chars>；For forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, and cc_back_manual_forces_from_autocontrol_init, the runtime errors showed local event names CA_backManual, CB_back...<truncated 309 chars>；Manual.enter and Manual.during remain the shared recovery actions: CA_mode=0, software_control=0, pump_control_voltage=0, alarms cleared, pump_speed=manual_switch_speed, and infusion_rate=default_flow_rate. This preserves passing manual rec...<truncated 75 chars>；The passing ChangeSetpoint behavior is preserved exactly as AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; }; inside Ask_StartAC.；The passing TerminateAC repair is preserved by keeping AutocontrolInit -> Manual :: TerminateAC before the unconditional AutocontrolInit -> AutocontrolNormal transition.
- diff_summary：`{"summary": "Replaced the insufficient composite StartAC transition with a non-wildcard forced Ask_StartAC-to-AutocontrolInit local StartAC transition; replaced wildcard/parent-scope backManual fallback with explicit non-wildcard forced local fallback transitions from each Mode_Control_Algorithm child to Manual; preserved ChangeSetpoint, TerminateAC ordering, manual recovery actions, autocontrol computation/logging, and pump-fault transitions."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int patient_bp = 120;
def int target_bp = 120;
def int requested_target_bp = 120;
def int infusion_rate = 0;
def int default_flow_rate = 0;
def int manual_switch_speed = 0;
def int pump_speed = 0;
def int pump_control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int display_error = 0;
def int sound_alarm = 0;
def int software_control = 0;
def int infusion_log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Manual -> Manual :: CA_backManual;
        ! Ask_StartAC -> Manual :: CA_backManual;
        ! AutocontrolInit -> Manual :: CA_backManual;
        ! AutocontrolNormal -> Manual :: CA_backManual;
        ! PumpFault -> Manual :: CA_backManual;

        ! Manual -> Manual :: CB_backManual;
        ! Ask_StartAC -> Manual :: CB_backManual;
        ! AutocontrolInit -> Manual :: CB_backManual;
        ! AutocontrolNormal -> Manual :: CB_backManual;
        ! PumpFault -> Manual :: CB_backManual;

        ! Manual -> Manual :: CP_backManual;
        ! Ask_StartAC -> Manual :: CP_backManual;
        ! AutocontrolInit -> Manual :: CP_backManual;
        ! AutocontrolNormal -> Manual :: CP_backManual;
        ! PumpFault -> Manual :: CP_backManual;

        ! Manual -> Manual :: CC_backManual;
        ! Ask_StartAC -> Manual :: CC_backManual;
        ! AutocontrolInit -> Manual :: CC_backManual;
        ! AutocontrolNormal -> Manual :: CC_backManual;
        ! PumpFault -> Manual :: CC_backManual;

        ! Ask_StartAC -> AutocontrolInit :: StartAC;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
            during {
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            [*] -> AwaitStart;

            state AwaitStart;

            AwaitStart -> AwaitStart :: ChangeSetpoint effect {
                target_bp = requested_target_bp;
            };
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_fault == 0] {
                    infusion_rate = target_bp - patient_bp;
                    pump_control_voltage = infusion_rate;
                    infusion_log_count = infusion_log_count + 1;
                } else {
                    pump_control_voltage = 0;
                }
            }
        }

        state PumpFault {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 1;
                display_error = 1;
                sound_alarm = 1;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual :: TerminateAC;
        AutocontrolNormal -> PumpFault :: OcclusionFault effect {
            pump_fault = 1;
        };
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
@@ -18,10 +18,31 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
+        ! Manual -> Manual :: CA_backManual;
+        ! Ask_StartAC -> Manual :: CA_backManual;
+        ! AutocontrolInit -> Manual :: CA_backManual;
+        ! AutocontrolNormal -> Manual :: CA_backManual;
+        ! PumpFault -> Manual :: CA_backManual;
+
+        ! Manual -> Manual :: CB_backManual;
+        ! Ask_StartAC -> Manual :: CB_backManual;
+        ! AutocontrolInit -> Manual :: CB_backManual;
+        ! AutocontrolNormal -> Manual :: CB_backManual;
+        ! PumpFault -> Manual :: CB_backManual;
+
+        ! Manual -> Manual :: CP_backManual;
+        ! Ask_StartAC -> Manual :: CP_backManual;
+        ! AutocontrolInit -> Manual :: CP_backManual;
+        ! AutocontrolNormal -> Manual :: CP_backManual;
+        ! PumpFault -> Manual :: CP_backManual;
+
+        ! Manual -> Manual :: CC_backManual;
+        ! Ask_StartAC -> Manual :: CC_backManual;
+        ! AutocontrolInit -> Manual :: CC_backManual;
+        ! AutocontrolNormal -> Manual :: CC_backManual;
+        ! PumpFault -> Manual :: CC_backManual;
+
+        ! Ask_StartAC -> AutocontrolInit :: StartAC;
 
         [*] -> Manual;
 
@@ -84,9 +105,8 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> AutocontrolInit :: StartAC;
+        AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolInit -> AutocontrolNormal;
-        AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolNormal -> Manual :: TerminateAC;
         AutocontrolNormal -> PumpFault :: OcclusionFault effect {
             pump_fault = 1;
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:d10fbec1b567b1b86b13eb1bd8154dbe765aee94e2b884956550a44f1eb74a74`。
  - SL-10 evidence 1: `{"summary": "The candidate cannot be accepted because local deterministic evidence still reports target_resolved=false, regression_detected=true, drift_risk=major, with rejection reason `scenario_regression; forced_transition_count_drift; missing_required_grounding`. This is not merely a conservative grounding/count objection: the hard scenario `initiate_ac_change_setpoint_and_start` still fails behaviorally."}`
  - SL-10 evidence 2: `{"summary": "For `initiate_ac_change_setpoint_and_start`, steps 0-2 still pass: default dispatch reaches Manual, InitiateAC reaches `CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart`, and ChangeSetpoint updates `target_bp` from 120 to 130. Step 3 `start_ac_enters_autocontrol_init` injects `StartAC` from active state `CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart`; expected state is `CARA.Mode_Control_Algorithm.AutocontrolInit` with `CA_mode=1`, `software_control=1`, `alarm_active=0`, `display_error=0`, and `sound_alarm=0`. Actual remains `CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart` with `CA_mode=0`, `software_control=0`, and runtime error says `Event 'StartAC' not found in sta...<truncated 59 chars>`
  - SL-10 evidence 3: `{"summary": "The FixLog shows multiple previous StartAC repairs were rejected: nested `AwaitStart -> AutocontrolInit :: StartAC` inside `Ask_StartAC` was semantically dangling because `AutocontrolInit` is a sibling under `Mode_Control_Algorithm`; dotted source `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC` did not parse; non-forced `Ask_StartAC -> AutocontrolInit : StartAC` parsed but was not visible from `AwaitStart`; the current `! Ask_StartAC -> AutocontrolInit :: StartAC` still is not visible from `AwaitStart`. Therefore the current SL-9 rationale does not resolve the remembered objection."}`
  - SL-10 evidence 4: `{"summary": "The NL explicitly requires that within Ask_StartAC, pressing StartAC enters AutocontrolInit, and the grounding map requires `CARA.Mode_Control_Algorithm.AutocontrolInit`. Since the candidate still cannot resolve StartAC from the Ask_StartAC leaf, a required event/transition obligation remains unmet."}`
  - SL-10 evidence 5: `{"summary": "The candidate improves prior backManual behavior by replacing the previously ineffective wildcard/parent-scope forms with explicit forced local fallback coverage, and the SL-9 notes map grounding elements such as initial transitions, ChangeSetpoint effect, backManual events, the AutocontrolNormal no-fault branch, and log increment. However, local evidence still reports forced_transition_count_drift and missing_required_grounding; these might be partly matcher/count objections, but they cannot be overridden while a hard StartAC scenario regression remains."}`
- SL-10 rework_instructions：Repair only the remaining StartAC visibility failure unless the full local brief shows additional scenario failures. Preserve `AutocontrolInit` as `CARA.Mode_Control_Algorithm.AutocontrolInit`, a sibling of `Ask_StartAC` under `Mode_Control_Algorithm`; do not move it inside `Ask_StartAC`.；Replace the current ineffective line `! Ask_StartAC -> AutocontrolInit :: StartAC;`. The next minimal DSL experiment should use the forced non-wildcard parent-scope event form at `Mode_Control_Algorithm` scope: `! Ask_StartAC -> AutocontrolInit : StartAC;` if this parses. This is the untried combination suggested by the prior SL-10 guidance: forced transitio...<truncated 104 chars>；Do not reuse the previously rejected StartAC forms: do not use `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC`, do not use dotted source `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;`, do not revert to non-forced `Ask_StartAC -> AutocontrolInit : StartAC;`, and do not keep the current `! Ask_StartAC -> AutocontrolInit :: Start...<truncated 93 chars>；After the StartAC edit, locally verify that `initiate_ac_change_setpoint_and_start` step `start_ac_enters_autocontrol_init` resolves event `StartAC` from `CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart` and enters `CARA.Mode_Control_Algorithm.AutocontrolInit` with `CA_mode=1`, `software_control=1`, `alarm_active=0`, `display_error=0`, and `sound_alarm=0`...<truncated 1 chars>；Preserve the already-passing setpoint behavior exactly: inside `Ask_StartAC`, keep `AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; };` so step `change_setpoint_updates_target_bp` continues to pass.；Preserve `AutocontrolInit -> Manual :: TerminateAC;` before the unconditional `AutocontrolInit -> AutocontrolNormal;` so `terminate_ac_from_init_and_normal` remains passing with Manual recovery variables restored.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 14, "n_scenarios_passed": 12, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: first cycle dispatches to Manual, where manual switch speed and default flow rate drive pump_speed and infusion_rate.", "name": "default_init_manual_operation_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_ac...<truncated 15643 chars>
    - local evidence 2: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 26, "old": 24}
    - local evidence 3: `missing_required_grounding` {"element_ids": ["transition:initial_root_to_mode_control", "transition:initial_mode_control_to_manual", "action:set_target_bp_from_requested", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "guard:AutocontrolNormal_no_pump_fault", "action:AutocontrolNormal_log_data"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 5 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_ac_change_setpoint_and_start, terminate_ac_from_init_and_normal, forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, cc_back_manual_forces_from_autocontrol_init`。
- before_dsl_hash：`sha256:3fbbdf9ad90a60957e2527a007b291fb9036bb1ac49e8bfbe004c84ca1f5854f`；candidate_dsl_hash：`sha256:e5e4732ddabeadd184806360d715999a302cfb465ecda022876f12fbe08a2d14`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-1c5f60aebf5`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`6`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-09d3998124` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit.', 'name': 'initiate_ac_change_setpoint_and_start', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init: caregiver initiates algorithmic control, changes the Ask_StartAC setpoint, then StartAC enters AutocontrolInit.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars_focus': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'software_control': 0, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'software_control': 1, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'StartAC' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'StartAC'", 'runtime_error_hint': {'event_path': 'StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 3, 'step_name': 'start_ac_enters_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'requested_target_bp': 130, 'target_bp': 120}, 'scenario_name': 'initiate_ac_change_setpoint_and_start', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'dispatch_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'initiate_enters_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 130}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'change_setpoint_updates_target_bp', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 0, 'alarm_active': 0, 'default_flow_rate': 0, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 0, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 130, 'software_control': 0, 'sound_alarm': 0, 'target_bp': 130}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'StartAC' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 3, 'step_name': 'start_ac_enters_autocontrol_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-2244c80013` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control.', 'name': 'terminate_ac_from_init_and_normal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: caregiver TerminateAC returns AutocontrolInit to Manual and releases software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'infusion_rate': 1, 'pump_speed': 4, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'infusion_rate': {'actual': 0, 'expected': 1}, 'pump_speed': {'actual': 0, 'expected': 4}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1}, 'before_cycles': 0, 'events': None, 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 1, 'step_name': 'manual_recovery_remains_asserted', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'default_flow_rate': 1, 'manual_switch_speed': 4, 'software_control': 1}, 'scenario_name': 'terminate_ac_from_init_and_normal', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 1, 'display_error': 0, 'infusion_log_count': 1, 'infusion_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'infusion_rate': {'actual': 0, 'expected': 1}, 'pump_speed': {'actual': 0, 'expected': 4}, 'software_control': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 1, 'display_error': 0, 'infusion_log_count': 1, 'infusion_rate': 0, 'manual_switch_speed': 4, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 1, 'step_name': 'manual_recovery_remains_asserted', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}}}]}` |
| `fixreq-0-sd6-2-0b7ad9e35b` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mode Manual.', 'name': 'forced_back_manual_events_from_distinct_states', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CA_backManual from a non-manual autocontrol leaf forces the shared Manual recovery target with CA_mode Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CA_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'infusion_rate': 2, 'pump_speed': 9, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CA_backManual'", 'runtime_error_hint': {'event_path': 'CA_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'ca_back_manual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'default_flow_rate': 2, 'manual_switch_speed': 9, 'software_control': 1}, 'scenario_name': 'forced_back_manual_events_from_distinct_states', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 2, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 9, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CA_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CA_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolNormal' while resolving event reference 'CA_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_back_manual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-989dda703e` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery target with CA_mode Manual.', 'name': 'forced_back_manual_event_variants', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CB, CP, and CC backManual fallback variants each force Manual or keep the shared Manual recovery target with CA_mode Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 1, 'display_error': 1, 'infusion_rate': 0, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 1}, 'before_cycles': 0, 'events': ['CB_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 4, 'pump_speed': 5, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CB_backManual'", 'runtime_error_hint': {'event_path': 'CB_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_active': 1, 'default_flow_rate': 4, 'display_error': 1, 'manual_switch_speed': 5, 'software_control': 1, 'sound_alarm': 1}, 'scenario_name': 'forced_back_manual_event_variants', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 1, 'alarm_active': 1, 'default_flow_rate': 4, 'display_error': 1, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 5, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 1, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CB_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CB_backManual' not found in state 'CARA.Mode_Control_Algorithm.PumpFault' while resolving event reference 'CB_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cb_back_manual_from_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-775e5adc2d` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, detecting a missing forced transition or wrong target.', 'name': 'cp_back_manual_forces_from_ask_start', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CP_backManual from the Ask_StartAC AwaitStart leaf must use the global forced fallback to Manual, detecting a missing forced transition or wrong target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 0, 'pump_control_voltage': 0, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 6, 'pump_control_voltage': 0, 'pump_speed': 10, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'CP_backManual'", 'runtime_error_hint': {'event_path': 'CP_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cp_back_manual_from_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'initial_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 6, 'display_error': 0, 'manual_switch_speed': 10, 'software_control': 1, 'sound_alarm': 0}, 'scenario_name': 'cp_back_manual_forces_from_ask_start', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 6, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 10, 'patient_bp': 120, 'pump_control_voltage': 0, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CP_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CP_backManual' not found in state 'CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart' while resolving event reference 'CP_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_back_manual_from_await_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-5-1e8441f72f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery target with manual outputs restored.', 'name': 'cc_back_manual_forces_from_autocontrol_init', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: CC_backManual from AutocontrolInit must preempt autocontrol and force the shared Manual recovery target with manual outputs restored.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars_focus': {'CA_mode': 1, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 0, 'pump_control_voltage': 22, 'pump_speed': 0, 'software_control': 1, 'sound_alarm': 0}, 'before_cycles': 0, 'events': ['CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'display_error': 0, 'infusion_rate': 7, 'pump_control_voltage': 0, 'pump_speed': 11, 'software_control': 0, 'sound_alarm': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CC_backManual'", 'runtime_error_hint': {'event_path': 'CC_backManual', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'cc_back_manual_from_init', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 7, 'display_error': 0, 'manual_switch_speed': 11, 'pump_control_voltage': 22, 'software_control': 1, 'sound_alarm': 0}, 'scenario_name': 'cc_back_manual_forces_from_autocontrol_init', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'default_flow_rate': 7, 'display_error': 0, 'infusion_log_count': 0, 'infusion_rate': 0, 'manual_switch_speed': 11, 'patient_bp': 120, 'pump_control_voltage': 22, 'pump_fault': 0, 'pump_speed': 0, 'requested_target_bp': 120, 'software_control': 1, 'sound_alarm': 0, 'target_bp': 120}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CC_backManual': failed with both StateMachine.resolve_event and State.resolve_event. Last error: Event 'CC_backManual' not found in state 'CARA.Mode_Control_Algorithm.AutocontrolInit' while resolving event reference 'CC_backManual'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cc_back_manual_from_init', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, hierarchical_state:Ask_StartAC, state:AwaitStart, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:patient_bp, variable:target_bp, variable:requested_target_bp, ... +43`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2882`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-09d3998124` | `accept` | ❌ | ✅ | Rework-locked. The failing initiate_ac_change_setpoint_and_start step start_ac_enters_autocontrol_init still reports StartAC unresolved from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart. I accept and replace the ineffective StartAC forms with the untried forced non-wildcard parent-scope event transition at Mode_Control_Algorithm scope: ! Ask_StartAC ->...<truncated 170 chars> |
| `fixreq-0-sd6-1-2244c80013` | `accept` | ❌ | ✅ | Rework-locked. The terminate_ac_from_init_and_normal scenario requires TerminateAC from AutocontrolInit to preempt automatic progression to AutocontrolNormal and enter Manual with manual recovery outputs. I preserve AutocontrolInit -> Manual :: TerminateAC before AutocontrolInit -> AutocontrolNormal.；intent=Keep AutocontrolInit -> Manual :: TerminateAC befor...<truncated 56 chars> |
| `fixreq-0-sd6-2-0b7ad9e35b` | `accept` | ❌ | ✅ | Rework-locked. The forced_back_manual_events_from_distinct_states scenario expects CA_backManual from AutocontrolNormal to resolve and enter Manual. I keep the successful explicit local forced fallback from AutocontrolNormal to Manual.；intent=Represent CA_backManual as ! AutocontrolNormal -> Manual :: CA_backManual; |
| `fixreq-0-sd6-3-989dda703e` | `accept` | ❌ | ✅ | Rework-locked. The forced_back_manual_event_variants scenario expects CB_backManual from PumpFault to enter Manual and clear alarms through Manual recovery actions. I keep an explicit local forced fallback from PumpFault to Manual.；intent=Represent CB_backManual as ! PumpFault -> Manual :: CB_backManual; |
| `fixreq-0-sd6-4-775e5adc2d` | `accept` | ❌ | ✅ | Rework-locked. The cp_back_manual_forces_from_ask_start scenario still failed because CP_backManual was unresolved from Ask_StartAC.AwaitStart. I use the same descendant-visible parent-scope forced pattern for the Ask_StartAC composite: ! Ask_StartAC -> Manual : CP_backManual;, while preserving ChangeSetpoint inside AwaitStart.；intent=Use ! Ask_StartAC -> Ma...<truncated 55 chars> |
| `fixreq-0-sd6-5-1e8441f72f` | `accept` | ❌ | ✅ | Rework-locked. The cc_back_manual_forces_from_autocontrol_init scenario expects CC_backManual from AutocontrolInit to preempt autocontrol and enter Manual. I keep an explicit local forced fallback from AutocontrolInit to Manual.；intent=Represent CC_backManual as ! AutocontrolInit -> Manual :: CC_backManual; |
- repair_rationale：For initiate_ac_change_setpoint_and_start, steps 0-2 were already passing: [*] -> Mode_Control_Algorithm, [*] -> Manual, Manual -> Ask_StartAC :: InitiateAC, and AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_targ...<truncated 356 chars>；For terminate_ac_from_init_and_normal, AutocontrolInit -> Manual :: TerminateAC remains before AutocontrolInit -> AutocontrolNormal, so TerminateAC from AutocontrolInit reaches Manual and Manual.enter/during restore CA_mode=0, software_cont...<truncated 99 chars>；For forced_back_manual_events_from_distinct_states, CA_backManual is concretely represented by ! AutocontrolNormal -> Manual :: CA_backManual;, matching the scenario source AutocontrolNormal and the NL shared Manual recovery target.；For forced_back_manual_event_variants, CB_backManual is concretely represented by ! PumpFault -> Manual :: CB_backManual;, and Manual self transitions for CP_backManual and CC_backManual keep the shared Manual target resolvable after recove...<truncated 50 chars>；For cp_back_manual_forces_from_ask_start, CP_backManual from the nested AwaitStart leaf is represented by ! Ask_StartAC -> Manual : CP_backManual;, using the same parent-scope forced composite pattern selected for StartAC descendant visibil...<truncated 4 chars>
- diff_summary：`{"summary": "Added forced non-wildcard parent-scope StartAC from Ask_StartAC to sibling AutocontrolInit; replaced broad/ineffective backManual fallbacks with narrow explicit source fallbacks for CA, CB, CP, and CC plus Manual self handling for CP/CC variants; preserved ChangeSetpoint, initial transitions, TerminateAC ordering, autocontrol no-fault computation/logging, and pump-fault recovery."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int patient_bp = 120;
def int target_bp = 120;
def int requested_target_bp = 120;
def int infusion_rate = 0;
def int default_flow_rate = 0;
def int manual_switch_speed = 0;
def int pump_speed = 0;
def int pump_control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int display_error = 0;
def int sound_alarm = 0;
def int software_control = 0;
def int infusion_log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Ask_StartAC -> AutocontrolInit : StartAC;
        ! AutocontrolNormal -> Manual :: CA_backManual;
        ! PumpFault -> Manual :: CB_backManual;
        ! Ask_StartAC -> Manual : CP_backManual;
        ! AutocontrolInit -> Manual :: CC_backManual;

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
            during {
                pump_speed = manual_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            [*] -> AwaitStart;

            state AwaitStart;

            AwaitStart -> AwaitStart :: ChangeSetpoint effect {
                target_bp = requested_target_bp;
            };
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                display_error = 0;
                sound_alarm = 0;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_fault == 0] {
                    infusion_rate = target_bp - patient_bp;
                    pump_control_voltage = infusion_rate;
                    infusion_log_count = infusion_log_count + 1;
                } else {
                    pump_control_voltage = 0;
                }
            }
        }

        state PumpFault {
            enter {
                CA_mode = 0;
                software_control = 0;
                pump_control_voltage = 0;
                alarm_active = 1;
                display_error = 1;
                sound_alarm = 1;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Manual -> Manual :: CP_backManual;
        Manual -> Manual :: CC_backManual;
        Ask_StartAC -> Manual :: TerminateAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual :: TerminateAC;
        AutocontrolNormal -> PumpFault :: OcclusionFault effect {
            pump_fault = 1;
        };
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
@@ -18,10 +18,11 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
+        ! Ask_StartAC -> AutocontrolInit : StartAC;
+        ! AutocontrolNormal -> Manual :: CA_backManual;
+        ! PumpFault -> Manual :: CB_backManual;
+        ! Ask_StartAC -> Manual : CP_backManual;
+        ! AutocontrolInit -> Manual :: CC_backManual;
 
         [*] -> Manual;
 
@@ -84,9 +85,11 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> AutocontrolInit :: StartAC;
+        Manual -> Manual :: CP_backManual;
+        Manual -> Manual :: CC_backManual;
+        Ask_StartAC -> Manual :: TerminateAC;
+        AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolInit -> AutocontrolNormal;
-        AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolNormal -> Manual :: TerminateAC;
         AutocontrolNormal -> PumpFault :: OcclusionFault effect {
             pump_fault = 1;
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:61f1fa02208b61261aa7237b7525b7dbbb9cf54183868ab53000cdbe2dc98bda`。
  - SL-10 evidence 1: `{"summary": "The NL requires that within Ask_StartAC the setpoint can be changed and pressing StartAC enters CARA.Mode_Control_Algorithm.AutocontrolInit. The candidate preserves ChangeSetpoint, but local deterministic evidence still reports the hard scenario initiate_ac_change_setpoint_and_start failing at step start_ac_enters_autocontrol_init: event StartAC is injected from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart, expected CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1, software_control=1, alarm_active=0, display_error=0, and sound_alarm=0, but actual remains Ask_StartAC.AwaitStart with CA_mode=0 and software_control=0 and runtime error says Event 'StartAC' not found....<truncated 2 chars>`
  - SL-10 evidence 2: `{"summary": "The complete FixLog shows prior rejected StartAC forms: nested AwaitStart -> AutocontrolInit :: StartAC was semantically dangling because AutocontrolInit is a sibling of Ask_StartAC; dotted Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC did not parse; non-forced Ask_StartAC -> AutocontrolInit : StartAC parsed but was not visible from AwaitStart; forced local ! Ask_StartAC -> AutocontrolInit :: StartAC was also not visible from AwaitStart. The current SL-9 candidate uses the previously requested untried form ! Ask_StartAC -> AutocontrolInit : StartAC, but local evidence shows this still does not resolve StartAC from the AwaitStart leaf, so the remembered objection is not re...<truncated 9 chars>`
  - SL-10 evidence 3: `{"summary": "The candidate diff narrows the backManual repairs to ! AutocontrolNormal -> Manual :: CA_backManual, ! PumpFault -> Manual :: CB_backManual, ! Ask_StartAC -> Manual : CP_backManual, ! AutocontrolInit -> Manual :: CC_backManual, plus Manual self transitions for CP/CC. Local evidence still reports scenario_regression with 12/14 scenarios passed and includes a blocking W_SHADOWED_EVENT diagnostic for CP_backManual because a local Manual.CP_backManual shadows a broader Mode_Control_Algorithm.CP_backManual chain event."}`
  - SL-10 evidence 4: `{"summary": "Local count drift is major: n_transitions decreased from 35 to 20 and forced transitions from 24 to 7. Some missing_required_grounding items such as [*] -> Mode_Control_Algorithm, [*] -> Manual, ChangeSetpoint effect, AutocontrolNormal no-fault guard, and infusion_log_count increment appear textually present in the candidate and may be matcher limitations, but event:StartAC is behaviorally confirmed unresolved, and event:CP_backManual has a new shadowing diagnostic, so this cannot be accepted as an audited override."}`
  - SL-10 evidence 5: `{"summary": "The candidate preserves many NL-required elements, including the CARA/Mode_Control_Algorithm hierarchy, Manual, Ask_StartAC/AwaitStart, AutocontrolInit, AutocontrolNormal, PumpFault, manual recovery actions, TerminateAC ordering, OcclusionFault/FaultRemoved effects, no-fault infusion computation, and logging. However, hard scenario obligations remain unmet, so the repaired DSL is not ready for the next full top-down revalidation pass."}`
- SL-10 rework_instructions：Repair StartAC visibility from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart to CARA.Mode_Control_Algorithm.AutocontrolInit. The current line `! Ask_StartAC -> AutocontrolInit : StartAC;` did not resolve from the AwaitStart leaf, so do not return the same candidate unchanged.；Do not reuse the previously rejected StartAC forms: do not use `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC`, do not use dotted source `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;`, do not use non-forced `Ask_StartAC -> AutocontrolInit : StartAC;`, and do not use `! Ask_StartAC -> AutocontrolInit :: StartAC;`.；Try the narrowest syntactically valid DSL mechanism that the runtime resolves from nested leaves. If the DSL supports only wildcard forced parent-scope events for descendant visibility, try `! * -> AutocontrolInit : StartAC;` at Mode_Control_Algorithm scope and document in repair_rationale that this is an admitted abstraction of the NL-scoped StartAC obligat...<truncated 196 chars>；Preserve AutocontrolInit as a sibling of Ask_StartAC under Mode_Control_Algorithm; do not move AutocontrolInit inside Ask_StartAC merely to satisfy name resolution.；Preserve `AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; };` exactly so initiate_ac_change_setpoint_and_start step change_setpoint_updates_target_bp continues to pass with target_bp=requested_target_bp.；Preserve `AutocontrolInit -> Manual :: TerminateAC;` before `AutocontrolInit -> AutocontrolNormal;` so terminate_ac_from_init_and_normal remains passing with Manual recovery variables restored.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; scenario_regression; count_drift; forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_SHADOWED_EVENT", "instance_key": "W_SHADOWED_EVENT:32b0150153e4", "message": "Local event 'CARA.Mode_Control_Algorithm.Manual.CP_backManual' shadows a chain event named 'CP_backManual'.", "policy_action": "requires_policy_classification", "pyfcstm_severity": "warning", "rationale": "", "refs": {"chain_path": "CARA.Mode_Control_Algorithm.CP_backManual", "event_name": "CP_backManual", "local_path": "CARA.Mode_Control_Algorith...<truncated 586 chars>
    - local evidence 2: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 14, "n_scenarios_passed": 12, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: first cycle dispatches to Manual, where manual switch speed and default flow rate drive pump_speed and infusion_rate.", "name": "default_init_manual_operation_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_ac...<truncated 15643 chars>
    - local evidence 3: `count_drift` {"direction": "decrease", "drift_ratio": -0.4286, "field": "n_transitions", "fix_target": "sim", "kind": "count_drift", "new": 20, "old": 35, "reduction_ratio": 0.4286}
    - local evidence 4: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 7, "old": 24}
    - local evidence 5: `missing_required_grounding` {"element_ids": ["transition:initial_root_to_mode_control", "transition:initial_mode_control_to_manual", "action:set_target_bp_from_requested", "event:StartAC", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "guard:AutocontrolNormal_no_pump_fault", "action:AutocontrolNormal_log_data"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-1c5f60aebf5` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-1c5f60aebf5` | accept=6, reject=0 | `sl10_review` | `sha256:afd645ff2326b1f3d5efd929079528585f115dbbf4775fbf1b92e78188f2e18a` | For initiate_ac_change_setpoint_and_start, step start_ac_enters_autocontrol_init expected CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1 and software_control=1, but actual remained in Ask_StartAC.AwaitStart with an unresolved StartAC event. The repair makes StartAC a local event on AwaitStart, the active source leaf, while still targeting AutocontrolInit and preserving ChangeSetpoint behavior that already passed., For terminate_ac_from_init_and_normal, step terminate_from_init_to_manual expected Manual with CA_mode=0, software_control=0, pump_speed from manual_switch_speed, and infusion_rate from default_flow_rate, but the automatic AutocontrolInit -> AutocontrolNormal transition fired first. The repair orders AutocontrolInit -> Manual :: TerminateAC before the unconditional initialization-complete transition, so TerminateAC can preempt and Manual.enter/during restores the expected variables., For forced_back_manual_events_from_distinct_states, CA_backManual from AutocontrolNormal expected the shared Manual recovery target but the event was unresolved. The repair encodes CA_backManual as a parent-scope forced event, which matches the NL cross-component fallback and lets Manual recovery actions restore CA_mode, software_control, pump_speed, and infusion_rate., ... +4 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-1c5f60aebf5` | accept=6, reject=0 | `sl9_rework` | `sha256:afd645ff2326b1f3d5efd929079528585f115dbbf4775fbf1b92e78188f2e18a` | Repair the dangling StartAC transition while preserving the intended SL-9 behavior. Do not leave `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC` unless the DSL supports an explicit parent/sibling target reference. Prefer moving the StartAC transition to the `Mode_Control_Algorithm` scope and make its source the active leaf, e.g. `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;` if qualified leaf sources are supported by the DSL., Keep `AutocontrolInit` as a sibling state of `Ask_StartAC` under `Mode_Control_Algorithm`; do not nest AutocontrolInit inside Ask_StartAC just to satisfy name resolution., Preserve the passing ChangeSetpoint behavior: `AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; };` must remain active from `Ask_StartAC.AwaitStart`., ... +16 |
| 4 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-1c5f60aebf5` | accept=6, reject=0 | `sl10_review` | `sha256:dff1fe0e2a5e437d0f7b3ee9c9a9ae74dcd6bd82233a8c90adf7bff3dec3a669` | For initiate_ac_change_setpoint_and_start, the failing step start_ac_enters_autocontrol_init expected CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1 and software_control=1, but the prior candidate had a dangling AwaitStart -> AutocontrolInit transition inside Ask_StartAC. The smallest local-only rework is to remove that nested dangling transition and declare Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC at Mode_Control_Algorithm scope, where the sibling AutocontrolInit target is resolvable while StartAC remains local to the active AwaitStart leaf., For terminate_ac_from_init_and_normal, I preserve the frontier behavior: AutocontrolInit -> Manual :: TerminateAC remains before AutocontrolInit -> AutocontrolNormal, so a hot-start TerminateAC reaches Manual and Manual.enter/during restore CA_mode=0, software_control=0, pump_speed=manual_switch_speed, and infusion_rate=default_flow_rate., For forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, and cc_back_manual_forces_from_autocontrol_init, I preserve the frontier parent-scope forced transitions ! * -> Manual : CA_backManual, CB_backManual, CP_backManual, and CC_backManual. These are NL-grounded cross-component fallbacks to shared Manual recovery and avoid reintroducing scenario regression., ... +4 |
| 5 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-1c5f60aebf5` | accept=6, reject=0 | `sl9_rework` | `sha256:dff1fe0e2a5e437d0f7b3ee9c9a9ae74dcd6bd82233a8c90adf7bff3dec3a669` | Fix the parse error by removing the unsupported dotted source transition `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;`., Do not revert to the previously rejected nested transition `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC`, because local semantic evidence already showed `AutocontrolInit` is dangling from that scope., Use a syntactically valid DSL mechanism that makes StartAC visible from the active `Ask_StartAC.AwaitStart` leaf while targeting sibling `AutocontrolInit`. Given the DSL evidence that single-colon parent-scope events are valid for descendant visibility, prefer declaring at `Mode_Control_Algorithm` scope: `Ask_StartAC -> AutocontrolInit : StartAC;` if this parses and resolves from the nested AwaitStart leaf., ... +22 |
| 6 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-1c5f60aebf5` | accept=6, reject=0 | `sl10_review` | `sha256:cb98c02d15b6d76d55750a603a7ed90a8c109137c97a5acc7c2fb9b7db95e703` | For initiate_ac_change_setpoint_and_start, step start_ac_enters_autocontrol_init expected StartAC from active Ask_StartAC.AwaitStart to reach CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1 and software_control=1. The prior rework candidate failed parse because dotted source Ask_StartAC.AwaitStart is unsupported; the earlier candidate failed semantics because AwaitStart could not target sibling AutocontrolInit from inside Ask_StartAC. This repair uses Ask_StartAC -> AutocontrolInit : StartAC at Mode_Control_Algorithm scope, keeping AutocontrolInit as a sibling and making StartAC a parent-scope event visible while Ask_StartAC is active., The passing ChangeSetpoint step is preserved exactly as AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; }; inside Ask_StartAC, so target_bp still updates from requested_target_bp while in AwaitStart., For terminate_ac_from_init_and_normal, TerminateAC from AutocontrolInit must preempt the automatic transition to AutocontrolNormal. The repair preserves AutocontrolInit -> Manual :: TerminateAC before AutocontrolInit -> AutocontrolNormal, so Manual.enter and Manual.during restore CA_mode=0, software_control=0, pump_speed=manual_switch_speed, and infusion_rate=default_flow_rate., ... +3 |
| 7 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-1c5f60aebf5` | accept=6, reject=0 | `sl9_rework` | `sha256:cb98c02d15b6d76d55750a603a7ed90a8c109137c97a5acc7c2fb9b7db95e703` | Repair StartAC visibility from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart while keeping AutocontrolInit as a sibling of Ask_StartAC under Mode_Control_Algorithm. Do not use the previously rejected nested `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC`, and do not use the unsupported dotted source `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;`., The current line `Ask_StartAC -> AutocontrolInit : StartAC;` is insufficient because the simulator still reports StartAC not found from the AwaitStart leaf. Replace it with a syntactically valid DSL mechanism that is visible from descendants. A likely minimal next edit is to try a forced parent-scope transition constrained to the Ask_StartAC composite, e.g. `! Ask_StartAC -> AutocontrolInit : StartAC;` if the DSL supports forced transitions with a non-wildcard source. If only wildcard forced transitions resolve from descendants, use the narrowest valid form available and document the abstraction rationale., Preserve `AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; };` inside Ask_StartAC so the already-passing setpoint-change step continues to update target_bp from requested_target_bp while in AwaitStart., ... +19 |
| 8 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-1c5f60aebf5` | accept=6, reject=0 | `sl10_review` | `sha256:0ff7fe87ef63a59441ab611029685acf2ad9c0b8636053998f540052bfce9b43` | For initiate_ac_change_setpoint_and_start, the failing step start_ac_enters_autocontrol_init expected StartAC from Ask_StartAC.AwaitStart to enter CARA.Mode_Control_Algorithm.AutocontrolInit with CA_mode=1 and software_control=1, but the prior parseable composite transition did not make StartAC visible from the nested leaf. The candidate uses ! Ask_StartAC -> AutocontrolInit :: StartAC at Mode_Control_Algorithm scope, preserving AutocontrolInit as a sibling of Ask_StartAC and avoiding both rejected forms., For forced_back_manual_events_from_distinct_states, forced_back_manual_event_variants, cp_back_manual_forces_from_ask_start, and cc_back_manual_forces_from_autocontrol_init, the runtime errors showed local event names CA_backManual, CB_backManual, CP_backManual, and CC_backManual were unresolved from the active leaves. Because wildcard and parent-scope fallback forms were insufficient under the scenario semantics, this candidate enumerates explicit non-wildcard forced local fallback transitions from each Mode_Control_Algorithm child to Manual., Manual.enter and Manual.during remain the shared recovery actions: CA_mode=0, software_control=0, pump_control_voltage=0, alarms cleared, pump_speed=manual_switch_speed, and infusion_rate=default_flow_rate. This preserves passing manual recovery, TerminateAC, FaultRemoved, and default-init manual-output scenarios., ... +5 |
| 9 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-1c5f60aebf5` | accept=6, reject=0 | `sl9_rework` | `sha256:0ff7fe87ef63a59441ab611029685acf2ad9c0b8636053998f540052bfce9b43` | Repair only the remaining StartAC visibility failure unless the full local brief shows additional scenario failures. Preserve `AutocontrolInit` as `CARA.Mode_Control_Algorithm.AutocontrolInit`, a sibling of `Ask_StartAC` under `Mode_Control_Algorithm`; do not move it inside `Ask_StartAC`., Replace the current ineffective line `! Ask_StartAC -> AutocontrolInit :: StartAC;`. The next minimal DSL experiment should use the forced non-wildcard parent-scope event form at `Mode_Control_Algorithm` scope: `! Ask_StartAC -> AutocontrolInit : StartAC;` if this parses. This is the untried combination suggested by the prior SL-10 guidance: forced transition constrained to the Ask_StartAC composite, but with single-colon event scope for descendant visibility., Do not reuse the previously rejected StartAC forms: do not use `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC`, do not use dotted source `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;`, do not revert to non-forced `Ask_StartAC -> AutocontrolInit : StartAC;`, and do not keep the current `! Ask_StartAC -> AutocontrolInit :: StartAC;` because local simulation still reports StartAC unresolved from `Ask_StartAC.AwaitStart`., ... +28 |
| 10 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-1c5f60aebf5` | accept=6, reject=0 | `sl10_review` | `sha256:e5e4732ddabeadd184806360d715999a302cfb465ecda022876f12fbe08a2d14` | For initiate_ac_change_setpoint_and_start, steps 0-2 were already passing: [*] -> Mode_Control_Algorithm, [*] -> Manual, Manual -> Ask_StartAC :: InitiateAC, and AwaitStart -> AwaitStart :: ChangeSetpoint effect { target_bp = requested_target_bp; } are preserved. The failing step start_ac_enters_autocontrol_init expected AutocontrolInit with CA_mode=1 and software_control=1 but actual remained AwaitStart because StartAC was unresolved. The repair uses ! Ask_StartAC -> AutocontrolInit : StartAC; to make StartAC visible from descendants of Ask_StartAC while targeting sibling AutocontrolInit., For terminate_ac_from_init_and_normal, AutocontrolInit -> Manual :: TerminateAC remains before AutocontrolInit -> AutocontrolNormal, so TerminateAC from AutocontrolInit reaches Manual and Manual.enter/during restore CA_mode=0, software_control=0, pump_control_voltage=0, pump_speed=manual_switch_speed, and infusion_rate=default_flow_rate., For forced_back_manual_events_from_distinct_states, CA_backManual is concretely represented by ! AutocontrolNormal -> Manual :: CA_backManual;, matching the scenario source AutocontrolNormal and the NL shared Manual recovery target., ... +6 |
| 11 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-1c5f60aebf5` | accept=6, reject=0 | `exit_rejected_rework_budget_exhausted` | `sha256:e5e4732ddabeadd184806360d715999a302cfb465ecda022876f12fbe08a2d14` | Repair StartAC visibility from CARA.Mode_Control_Algorithm.Ask_StartAC.AwaitStart to CARA.Mode_Control_Algorithm.AutocontrolInit. The current line `! Ask_StartAC -> AutocontrolInit : StartAC;` did not resolve from the AwaitStart leaf, so do not return the same candidate unchanged., Do not reuse the previously rejected StartAC forms: do not use `AwaitStart -> AutocontrolInit :: StartAC;` inside `state Ask_StartAC`, do not use dotted source `Ask_StartAC.AwaitStart -> AutocontrolInit :: StartAC;`, do not use non-forced `Ask_StartAC -> AutocontrolInit : StartAC;`, and do not use `! Ask_StartAC -> AutocontrolInit :: StartAC;`., Try the narrowest syntactically valid DSL mechanism that the runtime resolves from nested leaves. If the DSL supports only wildcard forced parent-scope events for descendant visibility, try `! * -> AutocontrolInit : StartAC;` at Mode_Control_Algorithm scope and document in repair_rationale that this is an admitted abstraction of the NL-scoped StartAC obligation because all composite/leaf-specific StartAC forms failed parse, semantic, or runtime resolution. If a guard or priority mechanism exists to constrain it to Ask_StartAC, use that narrower form., ... +34 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5994, 'completion_chars': 23858, 'completion_tokens': 7998, 'elapsed_seconds': 147.22417497300194, 'estimated_completion_tokens': 5965, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 12622, 'first_chunk_seconds': 38.57138537400169, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14448}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2625, 'completion_chars': 11006, 'completion_tokens': 3501, 'elapsed_seconds': 74.79289329098538, 'estimated_completion_tokens': 2752, 'estimated_prompt_tokens': 16201, 'estimated_total_tokens': 18953, 'first_chunk_seconds': 19.030739768990315, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 64801, 'prompt_tokens': 15780, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 19281}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3443, 'completion_chars': 14363, 'completion_tokens': 3861, 'elapsed_seconds': 73.73564311300288, 'estimated_completion_tokens': 3591, 'estimated_prompt_tokens': 19165, 'estimated_total_tokens': 22756, 'first_chunk_seconds': 11.40828387401416, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 76659, 'prompt_tokens': 18576, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22437}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3707, 'completion_chars': 15439, 'completion_tokens': 4109, 'elapsed_seconds': 77.55510398201295, 'estimated_completion_tokens': 3860, 'estimated_prompt_tokens': 20004, 'estimated_total_tokens': 23864, 'first_chunk_seconds': 10.498926310014213, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 80016, 'prompt_tokens': 19394, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23503}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2024, 'completion_chars': 8855, 'completion_tokens': 3968, 'elapsed_seconds': 75.54902318600216, 'estimated_completion_tokens': 2214, 'estimated_prompt_tokens': 52453, 'estimated_total_tokens': 54667, 'first_chunk_seconds': 39.90319265599828, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 209811, 'prompt_tokens': 45164, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 49132}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 801, 'completion_chars': 3469, 'completion_tokens': 1215, 'elapsed_seconds': 26.815017065004213, 'estimated_completion_tokens': 868, 'estimated_prompt_tokens': 62460, 'estimated_total_tokens': 63328, 'first_chunk_seconds': 12.058725918992423, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 249837, 'prompt_tokens': 51542, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 52757}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1966, 'completion_chars': 8361, 'completion_tokens': 2335, 'elapsed_seconds': 45.76691528302035, 'estimated_completion_tokens': 2091, 'estimated_prompt_tokens': 118070, 'estimated_total_tokens': 120161, 'first_chunk_seconds': 10.174089766020188, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 472277, 'prompt_tokens': 101853, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 104188}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 936, 'completion_chars': 4050, 'completion_tokens': 1397, 'elapsed_seconds': 28.47026540598017, 'estimated_completion_tokens': 1013, 'estimated_prompt_tokens': 36679, 'estimated_total_tokens': 37692, 'first_chunk_seconds': 11.79069683898706, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 146716, 'prompt_tokens': 35181, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 36578}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2070, 'completion_chars': 8791, 'completion_tokens': 2424, 'elapsed_seconds': 46.46154766198015, 'estimated_completion_tokens': 2198, 'estimated_prompt_tokens': 52680, 'estimated_total_tokens': 54878, 'first_chunk_seconds': 9.077064727985999, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 210719, 'prompt_tokens': 51187, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 53611}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1078, 'completion_chars': 4739, 'completion_tokens': 1730, 'elapsed_seconds': 33.57455100398511, 'estimated_completion_tokens': 1185, 'estimated_prompt_tokens': 44613, 'estimated_total_tokens': 45798, 'first_chunk_seconds': 14.373490092984866, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 178451, 'prompt_tokens': 43363, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 45093}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2497, 'completion_chars': 10775, 'completion_tokens': 4052, 'elapsed_seconds': 77.50110893198871, 'estimated_completion_tokens': 2694, 'estimated_prompt_tokens': 110587, 'estimated_total_tokens': 113281, 'first_chunk_seconds': 31.68995632600854, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 442346, 'prompt_tokens': 95055, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 99107}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1475, 'completion_chars': 6344, 'completion_tokens': 2512, 'elapsed_seconds': 49.20484350100742, 'estimated_completion_tokens': 1586, 'estimated_prompt_tokens': 71372, 'estimated_total_tokens': 72958, 'first_chunk_seconds': 22.19816451202496, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 285486, 'prompt_tokens': 65403, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 67915}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2264, 'completion_chars': 9589, 'completion_tokens': 3794, 'elapsed_seconds': 72.36644339800114, 'estimated_completion_tokens': 2398, 'estimated_prompt_tokens': 163346, 'estimated_total_tokens': 165744, 'first_chunk_seconds': 31.30218069400871, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 653382, 'prompt_tokens': 134984, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 138778}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1584, 'completion_chars': 7023, 'completion_tokens': 2609, 'elapsed_seconds': 51.97448835000978, 'estimated_completion_tokens': 1756, 'estimated_prompt_tokens': 91410, 'estimated_total_tokens': 93166, 'first_chunk_seconds': 23.357814918999793, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 365638, 'prompt_tokens': 82670, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 85279}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`not_converged`，record_status=`rejected`。
- 主要原因分类：`repair_review_rework_budget`。
- required stages executed：`26/16`，missing=`SL-7, SC-11`。
- repairs：`0/5` accepted；scenario_history=`3`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
