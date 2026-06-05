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
| Git commit | `ccade7dd690796405b376cac2c6728f4915be990` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:993dd2a89560dc22cd287bbf50c2cbe6faab9e99a63729d53f02e0d42085b247` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:ce72c8d44b302dadf9c88f390efa482afacd8764f5a6e38e3daea29e5bd8651d", "iteration": 0, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:99ae00ad0dfe4674b9646e0d8f36ebf13bd9c8c2d06a8d7a58e902ef3e2923af", "iteration": 0, "repair_history_index": 2, "rework_instructions": ["SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.", "For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling."], "same_as_final": false, "sl10_decision": "rework"}, "matching_repair_history_indices": [3], "repair_history_index": 3, "selected_source_stage": "SD-6", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 564485, 'completion_tokens': 57608, 'total_tokens': 622093, 'estimated_prompt_tokens': 612205, 'estimated_completion_tokens': 48731, 'estimated_total_tokens': 660936, 'prompt_chars': 2448793, 'completion_chars': 194897, 'n_calls': 15, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`1089.098s` |
| run record | [`pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:d7423720ad4a2ca8ba2e862ccbd11e8e1e86f81ecb7c0b82513e93fd0e750b46` |
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
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_message = 0;
def int log_records = 0;
def float bp_reading = 120.0;
def float target_bp = 120.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float built_in_switch_speed = 1.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def float sensor_buffer_bp = 120.0;

state CARA {
    [*] -> Mode_Control_Algorithm effect {
        sensor_buffer_bp = bp_reading;
    };

    state Mode_Control_Algorithm {
        [*] -> Manual effect {
            CA_mode = 0;
            software_control = 0;
            control_voltage = 0.0;
        };

        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_voltage = 0.0;
            }
            during {
                sensor_buffer_bp = bp_reading;
                flow_rate = default_flow_rate;
                pump_speed = built_in_switch_speed;
            }
        }

        state Ask_StartAC {
            during {
                sensor_buffer_bp = bp_reading;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = bp_reading;
            }
        }

        state AutocontrolNormal {
            during {
                sensor_buffer_bp = bp_reading;
                if [pump_fault == 0] {
                    if [bp_reading > target_bp] {
                        flow_rate = flow_rate - 1.0;
                    } else if [bp_reading < target_bp] {
                        flow_rate = flow_rate + 1.0;
                    } else {
                        flow_rate = flow_rate;
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_records = log_records + 1;
                }
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                error_message = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit : StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal : if [software_control > 0];
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12517 | 生成初始 DSL 与 grounding seeds | initial len=2800 | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=0; blocking=0, advisory=19, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=127630 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=127630 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=127630 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=234337 | LLM per-request accept/reject + repair | candidate len=2789,2789,2944,2956 | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=4, tokens=223258 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=234337 | LLM per-request accept/reject + repair | candidate len=2789,2789,2944,2956 | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=4, tokens=223258 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=234337 | LLM per-request accept/reject + repair | candidate len=2789,2789,2944,2956 | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=4, tokens=223258 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=234337 | LLM per-request accept/reject + repair | candidate len=2789,2789,2944,2956 | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=223258 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=0; blocking=0, advisory=19, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=127630 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=127630 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=1, tokens=24351 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-clean-20260605-121653-6519968d.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T04:16:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T04:16:54Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T04:16:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T04:16:54Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T04:18:47Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T04:18:47Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2800,hash=sha256:6856744fb026 |
| 7 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T04:18:47Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:6856744fb026d92edfa34dfb0a784ee639344b5f61d3895ce6fbee6217164637 |
| 10 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 12 | `2026-06-05T04:18:47Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2800,hash=sha256:6856744fb026, current_hash=sha256:6856744fb026d92edfa34dfb0a784ee639344b5f61d3895ce6fbee6217164637 |
| 13 | `2026-06-05T04:18:47Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T04:18:47Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T04:18:47Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T04:18:47Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T04:18:47Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T04:18:47Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T04:18:47Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T04:18:47Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T04:20:04Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T04:20:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T04:20:04Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T04:20:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T04:20:04Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T04:21:37Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T04:21:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T04:21:37Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T04:21:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T04:21:37Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T04:23:43Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T04:23:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T04:23:43Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T04:23:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T04:23:43Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T04:23:43Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T04:23:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T04:23:43Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T04:23:43Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 42 | `2026-06-05T04:23:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T04:23:43Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 21, "n_scenarios_passed": 12, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 44 | `2026-06-05T04:23:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T04:23:43Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-05T04:23:43Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 21, "n_scenarios_passed": 12, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2800,hash=sha256:6856744fb026 |
| 47 | `2026-06-05T04:23:43Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 48 | `2026-06-05T04:23:43Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 9} | <none> |
| 49 | `2026-06-05T04:23:43Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2800,hash=sha256:6856744fb026 |
| 50 | `2026-06-05T04:24:41Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 51 | `2026-06-05T04:24:41Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-d861f18d08", "fixreq-0-sd6-1-b89694a3d8", "fixreq-0-sd6-2-6c81985d39", "fixreq-0-sd6-3-1378209e1f", "fixreq-0-sd6-4-f6b978093f", "fixreq-0-sd6-5-0a776f9d52", "fixreq-0-sd6-6-f42b9b46c4", "fixreq-0-sd6-7-daa3842279", "fixreq-0-sd6-8-5b0d4084ef"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2789,hash=sha256:933d32f6f2b7 |
| 52 | `2026-06-05T04:24:41Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 53 | `2026-06-05T04:24:41Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:933d32f6f2b756fb04e951511407508e0121e37fcc9cd5bdb9814d0584b46108 |
| 54 | `2026-06-05T04:25:05Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 55 | `2026-06-05T04:25:05Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 56 | `2026-06-05T04:25:05Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 57 | `2026-06-05T04:25:05Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2800,hash=sha256:6856744fb026 |
| 58 | `2026-06-05T04:26:08Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 59 | `2026-06-05T04:26:08Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-d861f18d08", "fixreq-0-sd6-1-b89694a3d8", "fixreq-0-sd6-2-6c81985d39", "fixreq-0-sd6-3-1378209e1f", "fixreq-0-sd6-4-f6b978093f", "fixreq-0-sd6-5-0a776f9d52", "fixreq-0-sd6-6-f42b9b46c4", "fixreq-0-sd6-7-daa3842279", "fixreq-0-sd6-8-5b0d4084ef"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2789,hash=sha256:29cc18bfbd8a |
| 60 | `2026-06-05T04:26:08Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 61 | `2026-06-05T04:26:08Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:29cc18bfbd8a369371b45238eda558b9556ee0e0ca68d1fbcf09b26de497a206 |
| 62 | `2026-06-05T04:26:34Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 63 | `2026-06-05T04:26:34Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 64 | `2026-06-05T04:26:34Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 65 | `2026-06-05T04:26:34Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2800,hash=sha256:6856744fb026 |
| 66 | `2026-06-05T04:27:39Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 67 | `2026-06-05T04:27:39Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-d861f18d08", "fixreq-0-sd6-1-b89694a3d8", "fixreq-0-sd6-2-6c81985d39", "fixreq-0-sd6-3-1378209e1f", "fixreq-0-sd6-4-f6b978093f", "fixreq-0-sd6-5-0a776f9d52", "fixreq-0-sd6-6-f42b9b46c4", "fixreq-0-sd6-7-daa3842279", "fixreq-0-sd6-8-5b0d4084ef"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2944,hash=sha256:99ae00ad0dfe |
| 68 | `2026-06-05T04:27:39Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 69 | `2026-06-05T04:27:39Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:99ae00ad0dfe4674b9646e0d8f36ebf13bd9c8c2d06a8d7a58e902ef3e2923af |
| 70 | `2026-06-05T04:28:09Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 71 | `2026-06-05T04:28:09Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 72 | `2026-06-05T04:28:09Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 73 | `2026-06-05T04:28:09Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2800,hash=sha256:6856744fb026 |
| 74 | `2026-06-05T04:29:16Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 75 | `2026-06-05T04:29:16Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-d861f18d08", "fixreq-0-sd6-1-b89694a3d8", "fixreq-0-sd6-2-6c81985d39", "fixreq-0-sd6-3-1378209e1f", "fixreq-0-sd6-4-f6b978093f", "fixreq-0-sd6-5-0a776f9d52", "fixreq-0-sd6-6-f42b9b46c4", "fixreq-0-sd6-7-daa3842279", "fixreq-0-sd6-8-5b0d4084ef"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2956,hash=sha256:ce72c8d44b30 |
| 76 | `2026-06-05T04:29:16Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 77 | `2026-06-05T04:29:16Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:ce72c8d44b302dadf9c88f390efa482afacd8764f5a6e38e3daea29e5bd8651d |
| 78 | `2026-06-05T04:29:50Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 79 | `2026-06-05T04:29:50Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 80 | `2026-06-05T04:29:50Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
- ……另有 `48` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-6` | yes | fixbatch-0-sha256-968f96516bd / n=9 | accept=9, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 |
|---|---|---|---|
| `default_init_manual_outputs` | default-init verifies CARA dispatches into Manual and manual operation uses caregiver/default pump settings. | ✅ | ✅ |
| `initiate_change_setpoint_start_autocontrol` | default-init exercises InitiateAC, ChangeSetpoint in Ask_StartAC, and StartAC entering AutocontrolInit. | ⚪ | ✅ |
| `terminate_from_ask_returns_manual` | explicit-hot-start verifies caregiver TerminateAC from Ask_StartAC returns to the Manual recovery target. | ⚪ | ✅ |
| `autocontrol_high_pressure_lowers_flow` | explicit-hot-start verifies normal autocontrol lowers flow when patient blood pressure is above target. | ✅ | ✅ |
| `autocontrol_low_pressure_raises_flow` | explicit-hot-start verifies normal autocontrol raises flow when patient blood pressure is below target. | ✅ | ✅ |
| `autocontrol_pump_fault_and_removal` | explicit-hot-start verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved returns to Manual releasing ...<truncated 17 chars> | ⚪ | ✅ |
| `terminate_from_normal_returns_manual` | explicit-hot-start verifies caregiver TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-spee...<truncated 11 chars> | ⚪ | ✅ |
| `normal_autocontrol_no_control_when_fault_present` | explicit-hot-start no-fire probe verifies normal autocontrol does not adjust flow/log when pump-operation complications ...<truncated 6 chars> | ✅ | ✅ |
| `forced_back_manual_events_from_distinct_states` | explicit-hot-start probes cross-component fallback events from multiple non-manual leaves, all forcing Manual. | ✅ | ✅ |
| `forced_back_manual_ca_cp_cc_coverage` | explicit-hot-start probes remaining cross-component fallback events CA_backManual, CP_backManual, and CC_backManual to M...<truncated 6 chars> | ✅ | ✅ |
| `cp_back_manual_from_pump_fault_target_and_effects` | explicit-hot-start strengthens forced CP_backManual from PumpFault, asserting wrong-target mutations and Manual enter re...<truncated 15 chars> | ✅ | ✅ |
| `cc_back_manual_from_init_target_and_effects` | explicit-hot-start strengthens forced CC_backManual from AutocontrolInit, asserting Manual as exact target and software-...<truncated 16 chars> | ✅ | ✅ |
| `change_setpoint_effect_exact_value` | explicit-hot-start isolates ChangeSetpoint self-transition and checks the target_bp effect is exactly a one-unit increas...<truncated 2 chars> | ⚪ | ✅ |
| `pump_fault_detected_effect_exact_value` | explicit-hot-start isolates PumpFaultDetected and checks both the PumpFault target and the pump/alarm/software-control e...<truncated 7 chars> | ⚪ | ✅ |
| `fault_removed_effect_exact_reset_values` | explicit-hot-start isolates FaultRemoved and checks fault/alarm/error reset values plus Manual recovery target. | ⚪ | ✅ |
| `initiate_ac_exact_target_from_manual` | explicit-hot-start isolates caregiver InitiateAC from Manual and asserts the exact Ask_StartAC target rather than anothe...<truncated 20 chars> | ⚪ | ✅ |
| `start_ac_enter_effects_exact_values` | explicit-hot-start isolates StartAC from Ask_StartAC and checks the exact AutocontrolInit target plus software-control e...<truncated 14 chars> | ⚪ | ✅ |
| `autocontrol_init_guard_to_normal_target_and_outputs` | explicit-hot-start probes the software_control guard from AutocontrolInit to the exact AutocontrolNormal target and norm...<truncated 26 chars> | ✅ | ✅ |
| `autocontrol_init_no_guard_when_control_not_enabled` | explicit-hot-start no-fire probe verifies AutocontrolInit does not enter normal autocontrol when software_control is not...<truncated 9 chars> | ✅ | ✅ |
| `ca_back_manual_from_ask_exact_target_and_manual_effects` | explicit-hot-start isolates CA_backManual from Ask_StartAC and checks exact Manual target plus Manual recovery output ef...<truncated 6 chars> | ✅ | ✅ |
| `cb_back_manual_from_normal_exact_target_and_manual_effects` | explicit-hot-start isolates CB_backManual from AutocontrolNormal and checks exact Manual target plus Manual recovery out...<truncated 12 chars> | ✅ | ✅ |
| `change_setpoint_overwrites_with_exact_increment_from_low_setpoint` | explicit-hot-start adds an effect-mutation probe for ChangeSetpoint: missing or wrong +100-style effect must not pass th...<truncated 36 chars> | ⚪ | ✅ |
| `pump_fault_detected_overwrites_stale_fault_value` | explicit-hot-start adds an effect-mutation probe for PumpFaultDetected: the transition effect must set pump_fault exactl...<truncated 61 chars> | ⚪ | ✅ |
| `fault_removed_overwrites_nonbinary_fault_alarm_error_values` | explicit-hot-start adds an effect-mutation probe for FaultRemoved: fault, alarm, and error outputs must reset exactly to...<truncated 48 chars> | ⚪ | ✅ |
| `start_ac_overwrites_stale_control_flags_exactly` | explicit-hot-start adds an effect-value probe for StartAC/AutocontrolInit entry: stale nonbinary control flags must be o...<truncated 45 chars> | ⚪ | ✅ |
| `manual_entry_overwrites_stale_control_outputs_on_terminate` | explicit-hot-start adds a missing/wrong effect probe for Manual recovery on TerminateAC: stale autocontrol outputs must ...<truncated 37 chars> | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_outputs` — default-init verifies CARA dispatches into Manual and manual operation uses caregiver/default pump settings.</summary>

| Field | Value |
|---|---|
| description | default-init verifies CARA dispatches into Manual and manual operation uses caregiver/default pump settings. |
| initial_state | `<default-init>` |
| initial_vars | `{"bp_reading": 118.0, "built_in_switch_speed": 3.5, "default_flow_rate": 2.5}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "flow_rate": 2.5, "pump_speed": 3.5, "sensor_buffer_bp": 118.0, "software_control": 0}` |

</details>

<details><summary>`initiate_change_setpoint_start_autocontrol` — default-init exercises InitiateAC, ChangeSetpoint in Ask_StartAC, and StartAC entering AutocontrolInit.</summary>

| Field | Value |
|---|---|
| description | default-init exercises InitiateAC, ChangeSetpoint in Ask_StartAC, and StartAC entering AutocontrolInit. |
| initial_state | `<default-init>` |
| initial_vars | `{"bp_reading": 120.0, "flow_rate": 1.0, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `default_reaches_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"flow_rate": 1.0, "sensor_buffer_bp": 120.0}` |
| 1 `caregiver_initiates_ac` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"sensor_buffer_bp": 120.0}` |
| 2 `caregiver_changes_setpoint` | `0` | `["CARA.Mode_Control_Algorithm.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"sensor_buffer_bp": 120.0, "target_bp": 121.0}` |
| 3 `start_ac_enters_init` | `0` | `["CARA.Mode_Control_Algorithm.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "sensor_buffer_bp": 120.0, "software_control": 1}` |
| 4 `software_control_enables_normal_autocontrol` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 1, "control_voltage": 2.0, "flow_rate": 2.0, "log_records": 1, "pump_speed": 2.0, "software_control": 1}` |

</details>

<details><summary>`terminate_from_ask_returns_manual` — explicit-hot-start verifies caregiver TerminateAC from Ask_StartAC returns to the Manual recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start verifies caregiver TerminateAC from Ask_StartAC returns to the Manual recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "bp_reading": 122.0, "built_in_switch_speed": 2.25, "default_flow_rate": 1.75, "software_control": 1, "target_bp": 125.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_before_start` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "flow_rate": 1.75, "pump_speed": 2.25, "sensor_buffer_bp": 122.0, "software_control": 0}` |

</details>

<details><summary>`autocontrol_high_pressure_lowers_flow` — explicit-hot-start verifies normal autocontrol lowers flow when patient blood pressure is above target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start verifies normal autocontrol lowers flow when patient blood pressure is above target. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "bp_reading": 135.0, "control_voltage": 0.0, "flow_rate": 5.0, "log_records": 7, "pump_fault": 0, "pump_speed": 0.0, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `high_bp_reduces_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 4.0, "flow_rate": 4.0, "log_records": 8, "pump_speed": 4.0, "sensor_buffer_bp": 135.0}` |

</details>

<details><summary>`autocontrol_low_pressure_raises_flow` — explicit-hot-start verifies normal autocontrol raises flow when patient blood pressure is below target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start verifies normal autocontrol raises flow when patient blood pressure is below target. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "bp_reading": 105.0, "control_voltage": 0.0, "flow_rate": 5.0, "log_records": 3, "pump_fault": 0, "pump_speed": 0.0, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `low_bp_increases_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 6.0, "flow_rate": 6.0, "log_records": 4, "pump_speed": 6.0, "sensor_buffer_bp": 105.0}` |

</details>

<details><summary>`autocontrol_pump_fault_and_removal` — explicit-hot-start verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved returns to Manual releasing software control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved returns to Manual releasing software control. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "bp_reading": 130.0, "built_in_switch_speed": 2.5, "default_flow_rate": 1.5, "error_message": 0, "flow_rate": 4.0, "pump_fault": 0, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_detected_enters_pump_fault` | `0` | `["CARA.Mode_Control_Algorithm.PumpFaultDetected"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "error_message": 1, "pump_fault": 1, "software_control": 0}` |
| 1 `fault_removed_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "error_message": 0, "flow_rate": 1.5, "pump_fault": 0, "pump_speed": 2.5, "sensor_buffer_bp": 130.0, "software_control": 0}` |

</details>

<details><summary>`terminate_from_normal_returns_manual` — explicit-hot-start verifies caregiver TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-speed behavior.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start verifies caregiver TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-speed behavior. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "bp_reading": 119.0, "built_in_switch_speed": 4.0, "control_voltage": 8.0, "default_flow_rate": 2.0, "flow_rate": 8.0, "pump_speed": 8.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_normal_control` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "flow_rate": 2.0, "pump_speed": 4.0, "sensor_buffer_bp": 119.0, "software_control": 0}` |

</details>

<details><summary>`normal_autocontrol_no_control_when_fault_present` — explicit-hot-start no-fire probe verifies normal autocontrol does not adjust flow/log when pump-operation complications exist.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start no-fire probe verifies normal autocontrol does not adjust flow/log when pump-operation complications exist. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "bp_reading": 140.0, "control_voltage": 5.0, "flow_rate": 5.0, "log_records": 10, "pump_fault": 1, "pump_speed": 5.0, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_blocks_control_adjustment` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 5.0, "flow_rate": 5.0, "log_records": 10, "pump_speed": 5.0, "sensor_buffer_bp": 140.0}` |

</details>

<details><summary>`forced_back_manual_events_from_distinct_states` — explicit-hot-start probes cross-component fallback events from multiple non-manual leaves, all forcing Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes cross-component fallback events from multiple non-manual leaves, all forcing Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "bp_reading": 121.0, "built_in_switch_speed": 2.25, "default_flow_rate": 1.25, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_back_manual_from_ask` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 1.25, "pump_speed": 2.25, "sensor_buffer_bp": 121.0, "software_control": 0}` |

</details>

<details><summary>`forced_back_manual_ca_cp_cc_coverage` — explicit-hot-start probes remaining cross-component fallback events CA_backManual, CP_backManual, and CC_backManual to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes remaining cross-component fallback events CA_backManual, CP_backManual, and CC_backManual to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "bp_reading": 128.0, "built_in_switch_speed": 2.8, "default_flow_rate": 1.8, "error_message": 1, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_back_manual_from_normal` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 1.8, "pump_speed": 2.8, "sensor_buffer_bp": 128.0, "software_control": 0}` |
| 1 `cp_back_manual_still_manual_target` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 1.8, "pump_speed": 2.8, "sensor_buffer_bp": 128.0, "software_control": 0}` |
| 2 `cc_back_manual_still_manual_target` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 1.8, "pump_speed": 2.8, "sensor_buffer_bp": 128.0, "software_control": 0}` |

</details>

<details><summary>`cp_back_manual_from_pump_fault_target_and_effects` — explicit-hot-start strengthens forced CP_backManual from PumpFault, asserting wrong-target mutations and Manual enter recovery effects.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start strengthens forced CP_backManual from PumpFault, asserting wrong-target mutations and Manual enter recovery effects. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "bp_reading": 126.0, "built_in_switch_speed": 2.6, "control_voltage": 9.0, "default_flow_rate": 1.6, "error_message": 1, "flow_rate": 9.0, "pump_fault": 1, "pump_speed": 9.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_forces_manual_from_fault` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "flow_rate": 1.6, "pump_speed": 2.6, "sensor_buffer_bp": 126.0, "software_control": 0}` |

</details>

<details><summary>`cc_back_manual_from_init_target_and_effects` — explicit-hot-start strengthens forced CC_backManual from AutocontrolInit, asserting Manual as exact target and software-control release.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start strengthens forced CC_backManual from AutocontrolInit, asserting Manual as exact target and software-control release. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "bp_reading": 127.0, "built_in_switch_speed": 2.7, "control_voltage": 8.0, "default_flow_rate": 1.7, "flow_rate": 8.0, "pump_speed": 8.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_forces_manual_from_init` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "flow_rate": 1.7, "pump_speed": 2.7, "sensor_buffer_bp": 127.0, "software_control": 0}` |

</details>

<details><summary>`change_setpoint_effect_exact_value` — explicit-hot-start isolates ChangeSetpoint self-transition and checks the target_bp effect is exactly a one-unit increase.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start isolates ChangeSetpoint self-transition and checks the target_bp effect is exactly a one-unit increase. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"bp_reading": 123.0, "target_bp": 130.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `setpoint_incremented_once` | `0` | `["CARA.Mode_Control_Algorithm.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"sensor_buffer_bp": 123.0, "target_bp": 131.0}` |

</details>

<details><summary>`pump_fault_detected_effect_exact_value` — explicit-hot-start isolates PumpFaultDetected and checks both the PumpFault target and the pump/alarm/software-control effects.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start isolates PumpFaultDetected and checks both the PumpFault target and the pump/alarm/software-control effects. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "bp_reading": 129.0, "error_message": 0, "flow_rate": 6.0, "pump_fault": 0, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_detected_sets_fault_and_alarms` | `0` | `["CARA.Mode_Control_Algorithm.PumpFaultDetected"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "error_message": 1, "pump_fault": 1, "software_control": 0}` |

</details>

<details><summary>`fault_removed_effect_exact_reset_values` — explicit-hot-start isolates FaultRemoved and checks fault/alarm/error reset values plus Manual recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start isolates FaultRemoved and checks fault/alarm/error reset values plus Manual recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "bp_reading": 131.0, "built_in_switch_speed": 2.9, "control_voltage": 7.0, "default_flow_rate": 1.9, "error_message": 1, "flow_rate": 7.0, "pump_fault": 1, "pump_speed": 7.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_removed_resets_and_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_voltage": 0.0, "error_message": 0, "flow_rate": 1.9, "pump_fault": 0, "pump_speed": 2.9, "sensor_buffer_bp": 131.0, "software_control": 0}` |

</details>

<details><summary>`initiate_ac_exact_target_from_manual` — explicit-hot-start isolates caregiver InitiateAC from Manual and asserts the exact Ask_StartAC target rather than another autocontrol state.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start isolates caregiver InitiateAC from Manual and asserts the exact Ask_StartAC target rather than another autocontrol state. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"CA_mode": 0, "bp_reading": 124.0, "built_in_switch_speed": 3.2, "default_flow_rate": 2.2, "flow_rate": 2.2, "pump_speed": 3.2, "software_control": 0, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiate_ac_enters_ask_start` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 0, "flow_rate": 2.2, "pump_speed": 3.2, "sensor_buffer_bp": 124.0, "software_control": 0}` |

</details>

<details><summary>`start_ac_enter_effects_exact_values` — explicit-hot-start isolates StartAC from Ask_StartAC and checks the exact AutocontrolInit target plus software-control enable effects.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start isolates StartAC from Ask_StartAC and checks the exact AutocontrolInit target plus software-control enable effects. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 0, "bp_reading": 125.0, "control_voltage": 0.0, "flow_rate": 3.0, "pump_speed": 0.0, "software_control": 0, "target_bp": 121.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `start_ac_sets_control_enabled` | `0` | `["CARA.Mode_Control_Algorithm.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "control_voltage": 0.0, "flow_rate": 3.0, "pump_speed": 0.0, "sensor_buffer_bp": 125.0, "software_control": 1}` |

</details>

<details><summary>`autocontrol_init_guard_to_normal_target_and_outputs` — explicit-hot-start probes the software_control guard from AutocontrolInit to the exact AutocontrolNormal target and normal-control output updates.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes the software_control guard from AutocontrolInit to the exact AutocontrolNormal target and normal-control output updates. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "bp_reading": 120.0, "control_voltage": 0.0, "flow_rate": 3.0, "log_records": 2, "pump_fault": 0, "pump_speed": 0.0, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `guard_enters_normal_and_updates_outputs` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 1, "control_voltage": 3.0, "flow_rate": 3.0, "log_records": 3, "pump_speed": 3.0, "sensor_buffer_bp": 120.0, "software_control": 1}` |

</details>

<details><summary>`autocontrol_init_no_guard_when_control_not_enabled` — explicit-hot-start no-fire probe verifies AutocontrolInit does not enter normal autocontrol when software_control is not enabled.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start no-fire probe verifies AutocontrolInit does not enter normal autocontrol when software_control is not enabled. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 0, "bp_reading": 132.0, "control_voltage": 0.0, "flow_rate": 4.0, "log_records": 5, "pump_speed": 0.0, "software_control": 0, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `control_disabled_stays_in_init` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 0, "control_voltage": 0.0, "flow_rate": 4.0, "log_records": 5, "pump_speed": 0.0, "sensor_buffer_bp": 132.0, "software_control": 0}` |

</details>

<details><summary>`ca_back_manual_from_ask_exact_target_and_manual_effects` — explicit-hot-start isolates CA_backManual from Ask_StartAC and checks exact Manual target plus Manual recovery output effects.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start isolates CA_backManual from Ask_StartAC and checks exact Manual target plus Manual recovery output effects. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "bp_reading": 133.0, "built_in_switch_speed": 4.3, "control_voltage": 9.0, "default_flow_rate": 2.3, "flow_rate": 9.0, "pump_speed": 9.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_forces_manual_from_ask` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "flow_rate": 2.3, "pump_speed": 4.3, "sensor_buffer_bp": 133.0, "software_control": 0}` |

</details>

<details><summary>`cb_back_manual_from_normal_exact_target_and_manual_effects` — explicit-hot-start isolates CB_backManual from AutocontrolNormal and checks exact Manual target plus Manual recovery output effects.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start isolates CB_backManual from AutocontrolNormal and checks exact Manual target plus Manual recovery output effects. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "bp_reading": 134.0, "built_in_switch_speed": 4.4, "control_voltage": 10.0, "default_flow_rate": 2.4, "flow_rate": 10.0, "log_records": 6, "pump_speed": 10.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_forces_manual_from_normal` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "flow_rate": 2.4, "pump_speed": 4.4, "sensor_buffer_bp": 134.0, "software_control": 0}` |

</details>

<details><summary>`change_setpoint_overwrites_with_exact_increment_from_low_setpoint` — explicit-hot-start adds an effect-mutation probe for ChangeSetpoint: missing or wrong +100-style effect must not pass the exact one-unit target_bp increase.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start adds an effect-mutation probe for ChangeSetpoint: missing or wrong +100-style effect must not pass the exact one-unit target_bp increase. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"bp_reading": 136.0, "target_bp": 80.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `change_setpoint_exact_increment_from_80` | `0` | `["CARA.Mode_Control_Algorithm.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"sensor_buffer_bp": 136.0, "target_bp": 81.0}` |

</details>

<details><summary>`pump_fault_detected_overwrites_stale_fault_value` — explicit-hot-start adds an effect-mutation probe for PumpFaultDetected: the transition effect must set pump_fault exactly to active value 1, not preserve or ass...<truncated 21 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start adds an effect-mutation probe for PumpFaultDetected: the transition effect must set pump_fault exactly to active value 1, not preserve or assign a wrong constant. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "bp_reading": 137.0, "error_message": 0, "flow_rate": 6.5, "pump_fault": 77, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_detected_sets_fault_exactly_one` | `0` | `["CARA.Mode_Control_Algorithm.PumpFaultDetected"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "error_message": 1, "pump_fault": 1, "software_control": 0}` |

</details>

<details><summary>`fault_removed_overwrites_nonbinary_fault_alarm_error_values` — explicit-hot-start adds an effect-mutation probe for FaultRemoved: fault, alarm, and error outputs must reset exactly to zero before Manual recovery during-acti...<truncated 8 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start adds an effect-mutation probe for FaultRemoved: fault, alarm, and error outputs must reset exactly to zero before Manual recovery during-actions run. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 88, "bp_reading": 138.0, "built_in_switch_speed": 4.6, "control_voltage": 11.0, "default_flow_rate": 2.6, "error_message": 99, "flow_rate": 11.0, "pump_fault": 77, "pump_speed": 11.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_removed_resets_exactly_zero` | `0` | `["CARA.Mode_Control_Algorithm.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_voltage": 0.0, "error_message": 0, "flow_rate": 2.6, "pump_fault": 0, "pump_speed": 4.6, "sensor_buffer_bp": 138.0, "software_control": 0}` |

</details>

<details><summary>`start_ac_overwrites_stale_control_flags_exactly` — explicit-hot-start adds an effect-value probe for StartAC/AutocontrolInit entry: stale nonbinary control flags must be overwritten exactly to enabled control va...<truncated 5 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start adds an effect-value probe for StartAC/AutocontrolInit entry: stale nonbinary control flags must be overwritten exactly to enabled control values. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 77, "bp_reading": 139.0, "control_voltage": 9.0, "flow_rate": 3.5, "pump_speed": 9.0, "software_control": 88, "target_bp": 122.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `start_ac_sets_control_flags_exactly_one` | `0` | `["CARA.Mode_Control_Algorithm.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "control_voltage": 9.0, "flow_rate": 3.5, "pump_speed": 9.0, "sensor_buffer_bp": 139.0, "software_control": 1}` |

</details>

<details><summary>`manual_entry_overwrites_stale_control_outputs_on_terminate` — explicit-hot-start adds a missing/wrong effect probe for Manual recovery on TerminateAC: stale autocontrol outputs must be overwritten to manual-mode values.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start adds a missing/wrong effect probe for Manual recovery on TerminateAC: stale autocontrol outputs must be overwritten to manual-mode values. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 77, "bp_reading": 141.0, "built_in_switch_speed": 4.7, "control_voltage": 12.0, "default_flow_rate": 2.7, "flow_rate": 12.0, "pump_speed": 12.0, "software_control": 88}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_overwrites_to_manual_values` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_voltage": 0.0, "flow_rate": 2.7, "pump_speed": 4.7, "sensor_buffer_bp": 141.0, "software_control": 0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-6` | initiate_change_setpoint_start_autocontrol, terminate_from_ask_returns_manual, autocontrol_pump_fault_and_removal, terminate_from_normal_returns_manual, change_setpoint_effect_exact_value, ... +4 | accept=9, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 658 chars> | `sha256:933d32f6f2b756fb04e951511407508e0121e37fcc9cd5bdb9814d0584b46108` |
| 2 | `0` | ❌ | `SD-6` | initiate_change_setpoint_start_autocontrol, terminate_from_ask_returns_manual, autocontrol_pump_fault_and_removal, terminate_from_normal_returns_manual, change_setpoint_effect_exact_value, ... +4 | accept=9, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 658 chars> | `sha256:29cc18bfbd8a369371b45238eda558b9556ee0e0ca68d1fbcf09b26de497a206` |
| 3 | `0` | ❌ | `SD-6` | initiate_change_setpoint_start_autocontrol, terminate_from_ask_returns_manual, autocontrol_pump_fault_and_removal, terminate_from_normal_returns_manual, change_setpoint_effect_exact_value, ... +4 | accept=9, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 658 chars> | `sha256:99ae00ad0dfe4674b9646e0d8f36ebf13bd9c8c2d06a8d7a58e902ef3e2923af` |
| 4 | `0` | ✅ | `SD-6` | initiate_change_setpoint_start_autocontrol, terminate_from_ask_returns_manual, autocontrol_pump_fault_and_removal, terminate_from_normal_returns_manual, change_setpoint_effect_exact_value, ... +4 | accept=9, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:ce72c8d44b302dadf9c88f390efa482afacd8764f5a6e38e3daea29e5bd8651d` |

<details><summary>Repair 1 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_change_setpoint_start_autocontrol, terminate_from_ask_returns_manual, autocontrol_pump_fault_and_removal, terminate_from_normal_returns_manual, change_setpoint_effect_exact_value, pump_fault_detected_effect_exact_value, fault_removed_effect_exact_reset_values, initiate_ac_exact_target_from_manual, start_ac_enter_effects_exact_values`。
- before_dsl_hash：`sha256:6856744fb026d92edfa34dfb0a784ee639344b5f61d3895ce6fbee6217164637`；candidate_dsl_hash：`sha256:933d32f6f2b756fb04e951511407508e0121e37fcc9cd5bdb9814d0584b46108`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：
- 7. `<unknown>` `` policy=``：
- 8. `<unknown>` `` policy=``：
- ……另有 `1` 条 evidence 见 run record。

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-968f96516bd`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`9`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-d861f18d08` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init exercises InitiateAC, ChangeSetpoint in Ask_StartAC, and StartAC entering AutocontrolInit.', 'name': 'initiate_change_setpoint_start_autocontrol', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init exercises InitiateAC, ChangeSetpoint in Ask_StartAC, and StartAC entering AutocontrolInit.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'sensor_buffer_bp': 120.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'sensor_buffer_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'caregiver_initiates_ac', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'bp_reading': 120.0, 'flow_rate': 1.0, 'target_bp': 120.0}, 'scenario_name': 'initiate_change_setpoint_start_autocontrol', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 120.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 1.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 1.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 120.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'default_reaches_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 120.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 1.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 1.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'caregiver_initiates_ac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-b89694a3d8` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start verifies caregiver TerminateAC from Ask_StartAC returns to the Manual recovery target.', 'name': 'terminate_from_ask_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start verifies caregiver TerminateAC from Ask_StartAC returns to the Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 1, 'control_voltage': 0.0, 'flow_rate': 0.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_voltage': 0.0, 'flow_rate': 1.75, 'pump_speed': 2.25, 'sensor_buffer_bp': 122.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.TerminateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_before_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'bp_reading': 122.0, 'built_in_switch_speed': 2.25, 'default_flow_rate': 1.75, 'software_control': 1, 'target_bp': 125.0}, 'scenario_name': 'terminate_from_ask_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 122.0, 'built_in_switch_speed': 2.25, 'control_voltage': 0.0, 'default_flow_rate': 1.75, 'error_message': 0, 'flow_rate': 0.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 125.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.TerminateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_before_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-2-6c81985d39` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved returns to Manual releasing software control.', 'name': 'autocontrol_pump_fault_and_removal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved returns to Manual releasing software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'error_message': 0, 'pump_fault': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 1, 'error_message': 1, 'pump_fault': 1, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_detected_enters_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 130.0, 'built_in_switch_speed': 2.5, 'default_flow_rate': 1.5, 'error_message': 0, 'flow_rate': 4.0, 'pump_fault': 0, 'software_control': 1, 'target_bp': 120.0}, 'scenario_name': 'autocontrol_pump_fault_and_removal', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 130.0, 'built_in_switch_speed': 2.5, 'control_voltage': 0.0, 'default_flow_rate': 1.5, 'error_message': 0, 'flow_rate': 4.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_detected_enters_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-1378209e1f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start verifies caregiver TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-speed behavior.', 'name': 'terminate_from_normal_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start verifies caregiver TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-speed behavior.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'control_voltage': 8.0, 'flow_rate': 8.0, 'pump_speed': 8.0, 'sensor_buffer_bp': 120.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_voltage': 0.0, 'flow_rate': 2.0, 'pump_speed': 4.0, 'sensor_buffer_bp': 119.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Termina", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_normal_control', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'bp_reading': 119.0, 'built_in_switch_speed': 4.0, 'control_voltage': 8.0, 'default_flow_rate': 2.0, 'flow_rate': 8.0, 'pump_speed': 8.0, 'software_control': 1}, 'scenario_name': 'terminate_from_normal_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 119.0, 'built_in_switch_speed': 4.0, 'control_voltage': 8.0, 'default_flow_rate': 2.0, 'error_message': 0, 'flow_rate': 8.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 8.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Termina", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_normal_control', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-f6b978093f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates ChangeSetpoint self-transition and checks the target_bp effect is exactly a one-unit increase.', 'name': 'change_setpoint_effect_exact_value', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates ChangeSetpoint self-transition and checks the target_bp effect is exactly a one-unit increase.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'sensor_buffer_bp': 120.0, 'target_bp': 130.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.ChangeSetpoint'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'sensor_buffer_bp': 123.0, 'target_bp': 131.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.ChangeSetpoint', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'setpoint_incremented_once', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'bp_reading': 123.0, 'target_bp': 130.0}, 'scenario_name': 'change_setpoint_effect_exact_value', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 123.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 0.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 130.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'setpoint_incremented_once', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-5-0a776f9d52` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates PumpFaultDetected and checks both the PumpFault target and the pump/alarm/software-control effects.', 'name': 'pump_fault_detected_effect_exact_value', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates PumpFaultDetected and checks both the PumpFault target and the pump/alarm/software-control effects.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'error_message': 0, 'pump_fault': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 1, 'error_message': 1, 'pump_fault': 1, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_detected_sets_fault_and_alarms', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 129.0, 'error_message': 0, 'flow_rate': 6.0, 'pump_fault': 0, 'software_control': 1, 'target_bp': 120.0}, 'scenario_name': 'pump_fault_detected_effect_exact_value', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 129.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 6.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_detected_sets_fault_and_alarms', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-6-f42b9b46c4` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates FaultRemoved and checks fault/alarm/error reset values plus Manual recovery target.', 'name': 'fault_removed_effect_exact_reset_values', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates FaultRemoved and checks fault/alarm/error reset values plus Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 1, 'control_voltage': 7.0, 'error_message': 1, 'flow_rate': 7.0, 'pump_fault': 1, 'pump_speed': 7.0, 'sensor_buffer_bp': 120.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.FaultRemoved'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'control_voltage': 0.0, 'error_message': 0, 'flow_rate': 1.9, 'pump_fault': 0, 'pump_speed': 2.9, 'sensor_buffer_bp': 131.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.FaultRemoved', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_removed_resets_and_returns_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 1, 'bp_reading': 131.0, 'built_in_switch_speed': 2.9, 'control_voltage': 7.0, 'default_flow_rate': 1.9, 'error_message': 1, 'flow_rate': 7.0, 'pump_fault': 1, 'pump_speed': 7.0, 'software_control': 1}, 'scenario_name': 'fault_removed_effect_exact_reset_values', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'bp_reading': 131.0, 'built_in_switch_speed': 2.9, 'control_voltage': 7.0, 'default_flow_rate': 1.9, 'error_message': 1, 'flow_rate': 7.0, 'log_records': 0, 'pump_fault': 1, 'pump_speed': 7.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_removed_resets_and_returns_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-7-daa3842279` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates caregiver InitiateAC from Manual and asserts the exact Ask_StartAC target rather than another autocontrol state.', 'name': 'initiate_ac_exact_target_from_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates caregiver InitiateAC from Manual and asserts the exact Ask_StartAC target rather than another autocontrol state.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'flow_rate': 2.2, 'pump_speed': 3.2, 'sensor_buffer_bp': 120.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'CA_mode': 0, 'flow_rate': 2.2, 'pump_speed': 3.2, 'sensor_buffer_bp': 124.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'initiate_ac_enters_ask_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Manual', 'initial_vars': {'CA_mode': 0, 'bp_reading': 124.0, 'built_in_switch_speed': 3.2, 'default_flow_rate': 2.2, 'flow_rate': 2.2, 'pump_speed': 3.2, 'software_control': 0, 'target_bp': 120.0}, 'scenario_name': 'initiate_ac_exact_target_from_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 124.0, 'built_in_switch_speed': 3.2, 'control_voltage': 0.0, 'default_flow_rate': 2.2, 'error_message': 0, 'flow_rate': 2.2, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 3.2, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'initiate_ac_enters_ask_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-8-5b0d4084ef` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates StartAC from Ask_StartAC and checks the exact AutocontrolInit target plus software-control enable effects.', 'name': 'start_ac_enter_effects_exact_values', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates StartAC from Ask_StartAC and checks the exact AutocontrolInit target plus software-control enable effects.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 0, 'control_voltage': 0.0, 'flow_rate': 3.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'control_voltage': 0.0, 'flow_rate': 3.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 125.0, 'software_control': 1}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'start_ac_sets_control_enabled', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 0, 'bp_reading': 125.0, 'control_voltage': 0.0, 'flow_rate': 3.0, 'pump_speed': 0.0, 'software_control': 0, 'target_bp': 121.0}, 'scenario_name': 'start_ac_enter_effects_exact_values', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 125.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 3.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 121.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'start_ac_sets_control_enabled', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:error_message, variable:bp_reading, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2789`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-d861f18d08` | `accept` | ❌ | ❌ | Scenario initiate_change_setpoint_start_autocontrol fails because CARA.Mode_Control_Algorithm.InitiateAC cannot resolve while Manual is active. The caregiver control events are shared Mode_Control_Algorithm-level events, so the transition is made parent-scoped and visible to the injected path.；intent=Change caregiver/pump events from source-local scope to Mo...<truncated 40 chars> |
| `fixreq-0-sd6-1-b89694a3d8` | `accept` | ❌ | ❌ | Scenario terminate_from_ask_returns_manual fails because CARA.Mode_Control_Algorithm.TerminateAC cannot resolve from Ask_StartAC. TerminateAC is a shared caregiver termination event and should be parent-scoped.；intent=Make Ask_StartAC TerminateAC transition use parent event scope. |
| `fixreq-0-sd6-2-6c81985d39` | `accept` | ❌ | ❌ | Scenario autocontrol_pump_fault_and_removal fails because CARA.Mode_Control_Algorithm.PumpFaultDetected cannot resolve from AutocontrolNormal. Pump fault detection is modeled as a Mode_Control_Algorithm-level event visible from normal autocontrol.；intent=Make PumpFaultDetected transition use parent event scope. |
| `fixreq-0-sd6-3-1378209e1f` | `accept` | ❌ | ❌ | Scenario terminate_from_normal_returns_manual fails because CARA.Mode_Control_Algorithm.TerminateAC cannot resolve from AutocontrolNormal. The existing Manual enter/during actions already restore CA_mode, software_control, control_voltage, flow_rate, pump_speed, and sensor_buffer_bp once the event resolves.；intent=Make AutocontrolNormal TerminateAC transitio...<truncated 25 chars> |
| `fixreq-0-sd6-4-f6b978093f` | `accept` | ❌ | ❌ | Scenario change_setpoint_effect_exact_value fails because CARA.Mode_Control_Algorithm.ChangeSetpoint cannot resolve from Ask_StartAC. The existing effect already increments target_bp by exactly 1.0; only event visibility needs repair.；intent=Make ChangeSetpoint self-transition use parent event scope. |
| `fixreq-0-sd6-5-0a776f9d52` | `accept` | ❌ | ❌ | Scenario pump_fault_detected_effect_exact_value fails because CARA.Mode_Control_Algorithm.PumpFaultDetected cannot resolve. The existing transition effect and PumpFault enter action already set pump_fault, alarm_signal, error_message, software_control, and CA_mode to the expected values.；intent=Make PumpFaultDetected transition use parent event scope while p...<truncated 48 chars> |
| `fixreq-0-sd6-6-f42b9b46c4` | `accept` | ❌ | ❌ | Scenario fault_removed_effect_exact_reset_values fails because CARA.Mode_Control_Algorithm.FaultRemoved cannot resolve from PumpFault. FaultRemoved is made parent-scoped; the existing effect plus Manual enter/during actions produce the expected reset and manual recovery values.；intent=Make FaultRemoved transition use parent event scope. |
| `fixreq-0-sd6-7-daa3842279` | `accept` | ❌ | ❌ | Scenario initiate_ac_exact_target_from_manual fails because CARA.Mode_Control_Algorithm.InitiateAC cannot resolve from Manual. The target Ask_StartAC is already correct; only the event scope is repaired.；intent=Make InitiateAC transition use parent event scope. |
| `fixreq-0-sd6-8-5b0d4084ef` | `accept` | ❌ | ❌ | Scenario start_ac_enter_effects_exact_values fails because CARA.Mode_Control_Algorithm.StartAC cannot resolve from Ask_StartAC. The AutocontrolInit enter action already enables CA_mode and software_control; only event visibility needs repair.；intent=Make StartAC transition use parent event scope. |
- repair_rationale：All nine failing scenarios report unresolved event paths of the form CARA.Mode_Control_Algorithm.<EventName> while the current DSL declares those events with source-local :: scope. In pyfcstm, :: makes events owned by the source state, e.g....<truncated 85 chars>；The smallest safe repair is to change the NL-grounded caregiver, pump-fault, and cross-component fallback events to parent-relative : Event scope inside Mode_Control_Algorithm. This preserves all states, variables, transitions, guards, and ...<truncated 73 chars>；For initiate_change_setpoint_start_autocontrol and initiate_ac_exact_target_from_manual, Manual -> Ask_StartAC remains the target and Manual/Ask_StartAC during actions preserve sensor_buffer_bp behavior.；For change_setpoint_effect_exact_value, the existing target_bp = target_bp + 1.0 effect is preserved; after the self-transition, Ask_StartAC during updates sensor_buffer_bp to the current bp_reading.；For start_ac_enter_effects_exact_values, Ask_StartAC -> AutocontrolInit remains the target, and AutocontrolInit.enter preserves CA_mode = 1 and software_control = 1.
- diff_summary：`{"summary": "Changed event scope from source-local ':: EventName' to parent-relative ': EventName' for Mode_Control_Algorithm caregiver, pump-fault, fault-removal, and backManual events so scenario paths CARA.Mode_Control_Algorithm.<EventName> resolve. Preserved all states, variables, actions, effects, guards, and transition targets."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_message = 0;
def int log_records = 0;
def float bp_reading = 120.0;
def float target_bp = 120.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float built_in_switch_speed = 1.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def float sensor_buffer_bp = 120.0;

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
                control_voltage = 0.0;
            }
            during {
                sensor_buffer_bp = bp_reading;
                flow_rate = default_flow_rate;
                pump_speed = built_in_switch_speed;
            }
        }

        state Ask_StartAC {
            during {
                sensor_buffer_bp = bp_reading;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = bp_reading;
            }
        }

        state AutocontrolNormal {
            during {
                sensor_buffer_bp = bp_reading;
                if [pump_fault == 0] {
                    if [bp_reading > target_bp] {
                        flow_rate = flow_rate - 1.0;
                    } else if [bp_reading < target_bp] {
                        flow_rate = flow_rate + 1.0;
                    } else {
                        flow_rate = flow_rate;
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_records = log_records + 1;
                }
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                error_message = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit : StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal : if [software_control > 0];
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -17,10 +17,10 @@
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
 
@@ -80,13 +80,13 @@
             }
         }
 
-        Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = target_bp + 1.0; };
-        Ask_StartAC -> AutocontrolInit :: StartAC;
-        Ask_StartAC -> Manual :: TerminateAC;
+        Manual -> Ask_StartAC : InitiateAC;
+        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_bp = target_bp + 1.0; };
+        Ask_StartAC -> AutocontrolInit : StartAC;
+        Ask_StartAC -> Manual : TerminateAC;
         AutocontrolInit -> AutocontrolNormal : if [software_control > 0];
-        AutocontrolNormal -> Manual :: TerminateAC;
-        AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_fault = 1; };
-        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
+        AutocontrolNormal -> Manual : TerminateAC;
+        AutocontrolNormal -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
+        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:d88983ab56cb9fd05da451a3d3649f35d1bd5f12c5266fc848ca4fd84df5340f`。
  - SL-10 evidence 1: `{"summary": "The NL requires CARA.Mode_Control_Algorithm with Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, all listed variables, caregiver InitiateAC/StartAC/TerminateAC/ChangeSetpoint behavior, PumpFaultDetected/FaultRemoved behavior, and cross-component backManual recovery. The candidate preserves all states, variables, initial transitions, state actions, transition targets, guards, and effects from the old DSL; the only substantive DSL change is replacing source-local event declarations using ':: EventName' with parent-relative event declarations using ': EventName' for the Mode_Control_Algorithm events."}`
  - SL-10 evidence 2: `{"summary": "All nine hard simulation requests failed with unresolved event paths of the form CARA.Mode_Control_Algorithm.<EventName>: InitiateAC, TerminateAC, PumpFaultDetected, ChangeSetpoint, StartAC, and FaultRemoved. SL-9 accepted each request with the same minimal repair rationale: these are NL-grounded Mode_Control_Algorithm-level events, and the runtime errors show the old source-local '::' events were not visible to scenario injections at the parent path. The candidate directly repairs that mechanism by making those events parent-scoped while preserving the scenario-relevant targets and effects."}`
  - SL-10 evidence 3: `{"summary": "For initiate_change_setpoint_start_autocontrol and initiate_ac_exact_target_from_manual, Manual -> Ask_StartAC remains intact and Manual/Ask_StartAC actions still update sensor_buffer_bp and preserve manual flow/pump speed. For change_setpoint_effect_exact_value, the self-transition still increments target_bp by exactly 1.0. For start_ac_enter_effects_exact_values, Ask_StartAC -> AutocontrolInit remains intact and AutocontrolInit.enter still sets CA_mode = 1 and software_control = 1."}`
  - SL-10 evidence 4: `{"summary": "For terminate_from_ask_returns_manual and terminate_from_normal_returns_manual, the TerminateAC transitions still target Manual, whose enter/during actions restore CA_mode = 0, software_control = 0, control_voltage = 0.0, sensor_buffer_bp = bp_reading, flow_rate = default_flow_rate, and pump_speed = built_in_switch_speed. For pump-fault scenarios, AutocontrolNormal -> PumpFault still sets pump_fault = 1 and PumpFault.enter still activates alarm_signal/error_message and releases software control; FaultRemoved still resets fault/alarm/error and returns to Manual."}`
  - SL-10 evidence 5: `{"summary": "The DSL diff does not delete NL-required obligations. The initial CARA -> Mode_Control_Algorithm transition and Mode_Control_Algorithm -> Manual transition remain textually present as '[*] -> Mode_Control_Algorithm;' and '[*] -> Manual;'. All cross-component fallback transitions CA_backManual, CB_backManual, CP_backManual, and CC_backManual remain forced transitions to Manual and are made parent-visible consistently with the event-path repair."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.；For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-ground...<truncated 152 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial:CARA_to_Mode_Control_Algorithm", "transition:initial:Mode_Control_Algorithm_to_Manual"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_change_setpoint_start_autocontrol, terminate_from_ask_returns_manual, autocontrol_pump_fault_and_removal, terminate_from_normal_returns_manual, change_setpoint_effect_exact_value, pump_fault_detected_effect_exact_value, fault_removed_effect_exact_reset_values, initiate_ac_exact_target_from_manual, start_ac_enter_effects_exact_values`。
- before_dsl_hash：`sha256:6856744fb026d92edfa34dfb0a784ee639344b5f61d3895ce6fbee6217164637`；candidate_dsl_hash：`sha256:29cc18bfbd8a369371b45238eda558b9556ee0e0ca68d1fbcf09b26de497a206`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：
- 7. `<unknown>` `` policy=``：
- 8. `<unknown>` `` policy=``：
- ……另有 `1` 条 evidence 见 run record。

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-968f96516bd`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`9`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-d861f18d08` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init exercises InitiateAC, ChangeSetpoint in Ask_StartAC, and StartAC entering AutocontrolInit.', 'name': 'initiate_change_setpoint_start_autocontrol', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init exercises InitiateAC, ChangeSetpoint in Ask_StartAC, and StartAC entering AutocontrolInit.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'sensor_buffer_bp': 120.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'sensor_buffer_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'caregiver_initiates_ac', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'bp_reading': 120.0, 'flow_rate': 1.0, 'target_bp': 120.0}, 'scenario_name': 'initiate_change_setpoint_start_autocontrol', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 120.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 1.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 1.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 120.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'default_reaches_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 120.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 1.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 1.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'caregiver_initiates_ac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-b89694a3d8` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start verifies caregiver TerminateAC from Ask_StartAC returns to the Manual recovery target.', 'name': 'terminate_from_ask_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start verifies caregiver TerminateAC from Ask_StartAC returns to the Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 1, 'control_voltage': 0.0, 'flow_rate': 0.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_voltage': 0.0, 'flow_rate': 1.75, 'pump_speed': 2.25, 'sensor_buffer_bp': 122.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.TerminateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_before_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'bp_reading': 122.0, 'built_in_switch_speed': 2.25, 'default_flow_rate': 1.75, 'software_control': 1, 'target_bp': 125.0}, 'scenario_name': 'terminate_from_ask_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 122.0, 'built_in_switch_speed': 2.25, 'control_voltage': 0.0, 'default_flow_rate': 1.75, 'error_message': 0, 'flow_rate': 0.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 125.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.TerminateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_before_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-2-6c81985d39` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved returns to Manual releasing software control.', 'name': 'autocontrol_pump_fault_and_removal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved returns to Manual releasing software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'error_message': 0, 'pump_fault': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 1, 'error_message': 1, 'pump_fault': 1, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_detected_enters_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 130.0, 'built_in_switch_speed': 2.5, 'default_flow_rate': 1.5, 'error_message': 0, 'flow_rate': 4.0, 'pump_fault': 0, 'software_control': 1, 'target_bp': 120.0}, 'scenario_name': 'autocontrol_pump_fault_and_removal', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 130.0, 'built_in_switch_speed': 2.5, 'control_voltage': 0.0, 'default_flow_rate': 1.5, 'error_message': 0, 'flow_rate': 4.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_detected_enters_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-1378209e1f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start verifies caregiver TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-speed behavior.', 'name': 'terminate_from_normal_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start verifies caregiver TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-speed behavior.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'control_voltage': 8.0, 'flow_rate': 8.0, 'pump_speed': 8.0, 'sensor_buffer_bp': 120.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_voltage': 0.0, 'flow_rate': 2.0, 'pump_speed': 4.0, 'sensor_buffer_bp': 119.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Termina", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_normal_control', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'bp_reading': 119.0, 'built_in_switch_speed': 4.0, 'control_voltage': 8.0, 'default_flow_rate': 2.0, 'flow_rate': 8.0, 'pump_speed': 8.0, 'software_control': 1}, 'scenario_name': 'terminate_from_normal_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 119.0, 'built_in_switch_speed': 4.0, 'control_voltage': 8.0, 'default_flow_rate': 2.0, 'error_message': 0, 'flow_rate': 8.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 8.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Termina", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_normal_control', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-f6b978093f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates ChangeSetpoint self-transition and checks the target_bp effect is exactly a one-unit increase.', 'name': 'change_setpoint_effect_exact_value', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates ChangeSetpoint self-transition and checks the target_bp effect is exactly a one-unit increase.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'sensor_buffer_bp': 120.0, 'target_bp': 130.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.ChangeSetpoint'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'sensor_buffer_bp': 123.0, 'target_bp': 131.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.ChangeSetpoint', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'setpoint_incremented_once', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'bp_reading': 123.0, 'target_bp': 130.0}, 'scenario_name': 'change_setpoint_effect_exact_value', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 123.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 0.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 130.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'setpoint_incremented_once', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-5-0a776f9d52` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates PumpFaultDetected and checks both the PumpFault target and the pump/alarm/software-control effects.', 'name': 'pump_fault_detected_effect_exact_value', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates PumpFaultDetected and checks both the PumpFault target and the pump/alarm/software-control effects.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'error_message': 0, 'pump_fault': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 1, 'error_message': 1, 'pump_fault': 1, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_detected_sets_fault_and_alarms', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 129.0, 'error_message': 0, 'flow_rate': 6.0, 'pump_fault': 0, 'software_control': 1, 'target_bp': 120.0}, 'scenario_name': 'pump_fault_detected_effect_exact_value', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 129.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 6.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_detected_sets_fault_and_alarms', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-6-f42b9b46c4` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates FaultRemoved and checks fault/alarm/error reset values plus Manual recovery target.', 'name': 'fault_removed_effect_exact_reset_values', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates FaultRemoved and checks fault/alarm/error reset values plus Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 1, 'control_voltage': 7.0, 'error_message': 1, 'flow_rate': 7.0, 'pump_fault': 1, 'pump_speed': 7.0, 'sensor_buffer_bp': 120.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.FaultRemoved'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'control_voltage': 0.0, 'error_message': 0, 'flow_rate': 1.9, 'pump_fault': 0, 'pump_speed': 2.9, 'sensor_buffer_bp': 131.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.FaultRemoved', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_removed_resets_and_returns_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 1, 'bp_reading': 131.0, 'built_in_switch_speed': 2.9, 'control_voltage': 7.0, 'default_flow_rate': 1.9, 'error_message': 1, 'flow_rate': 7.0, 'pump_fault': 1, 'pump_speed': 7.0, 'software_control': 1}, 'scenario_name': 'fault_removed_effect_exact_reset_values', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'bp_reading': 131.0, 'built_in_switch_speed': 2.9, 'control_voltage': 7.0, 'default_flow_rate': 1.9, 'error_message': 1, 'flow_rate': 7.0, 'log_records': 0, 'pump_fault': 1, 'pump_speed': 7.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_removed_resets_and_returns_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-7-daa3842279` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates caregiver InitiateAC from Manual and asserts the exact Ask_StartAC target rather than another autocontrol state.', 'name': 'initiate_ac_exact_target_from_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates caregiver InitiateAC from Manual and asserts the exact Ask_StartAC target rather than another autocontrol state.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'flow_rate': 2.2, 'pump_speed': 3.2, 'sensor_buffer_bp': 120.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'CA_mode': 0, 'flow_rate': 2.2, 'pump_speed': 3.2, 'sensor_buffer_bp': 124.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'initiate_ac_enters_ask_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Manual', 'initial_vars': {'CA_mode': 0, 'bp_reading': 124.0, 'built_in_switch_speed': 3.2, 'default_flow_rate': 2.2, 'flow_rate': 2.2, 'pump_speed': 3.2, 'software_control': 0, 'target_bp': 120.0}, 'scenario_name': 'initiate_ac_exact_target_from_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 124.0, 'built_in_switch_speed': 3.2, 'control_voltage': 0.0, 'default_flow_rate': 2.2, 'error_message': 0, 'flow_rate': 2.2, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 3.2, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'initiate_ac_enters_ask_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-8-5b0d4084ef` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates StartAC from Ask_StartAC and checks the exact AutocontrolInit target plus software-control enable effects.', 'name': 'start_ac_enter_effects_exact_values', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates StartAC from Ask_StartAC and checks the exact AutocontrolInit target plus software-control enable effects.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 0, 'control_voltage': 0.0, 'flow_rate': 3.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'control_voltage': 0.0, 'flow_rate': 3.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 125.0, 'software_control': 1}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'start_ac_sets_control_enabled', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 0, 'bp_reading': 125.0, 'control_voltage': 0.0, 'flow_rate': 3.0, 'pump_speed': 0.0, 'software_control': 0, 'target_bp': 121.0}, 'scenario_name': 'start_ac_enter_effects_exact_values', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 125.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 3.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 121.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'start_ac_sets_control_enabled', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:error_message, variable:bp_reading, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2789`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-d861f18d08` | `accept` | ❌ | ✅ | Accepted because initiate_change_setpoint_start_autocontrol fails at caregiver_initiates_ac with unresolved event path CARA.Mode_Control_Algorithm.InitiateAC while Manual remains active. The expected target is Ask_StartAC with sensor_buffer_bp refreshed; the existing target/action logic is correct, so the minimal repair is to make InitiateAC a Mode_Control_A...<truncated 117 chars> |
| `fixreq-0-sd6-1-b89694a3d8` | `accept` | ❌ | ✅ | Accepted because terminate_from_ask_returns_manual fails with unresolved CARA.Mode_Control_Algorithm.TerminateAC from Ask_StartAC. The expected Manual recovery values are already produced by Manual enter/during once the event resolves, so only event visibility is repaired.；intent=Change Ask_StartAC -> Manual TerminateAC from source-local :: to parent-scoped ...<truncated 2 chars> |
| `fixreq-0-sd6-2-6c81985d39` | `accept` | ❌ | ✅ | Accepted because autocontrol_pump_fault_and_removal fails with unresolved CARA.Mode_Control_Algorithm.PumpFaultDetected from AutocontrolNormal. The expected PumpFault target and fault/alarm/software-control values are already represented by the transition effect and PumpFault.enter, so only event scope is changed.；intent=Change AutocontrolNormal -> PumpFault...<truncated 59 chars> |
| `fixreq-0-sd6-3-1378209e1f` | `accept` | ❌ | ✅ | Accepted because terminate_from_normal_returns_manual fails with unresolved CARA.Mode_Control_Algorithm.TerminateAC from AutocontrolNormal. The existing Manual recovery target and manual pump-speed behavior are preserved; making TerminateAC parent-scoped resolves the exact scenario gap.；intent=Change AutocontrolNormal -> Manual TerminateAC from source-local ...<truncated 22 chars> |
| `fixreq-0-sd6-4-f6b978093f` | `accept` | ❌ | ✅ | Accepted because change_setpoint_effect_exact_value fails with unresolved CARA.Mode_Control_Algorithm.ChangeSetpoint from Ask_StartAC. The existing self-transition effect target_bp = target_bp + 1.0 exactly matches the expected value; parent-scoping the event makes it visible to the scenario path.；intent=Change Ask_StartAC self-transition ChangeSetpoint from...<truncated 69 chars> |
| `fixreq-0-sd6-5-0a776f9d52` | `accept` | ❌ | ✅ | Accepted because pump_fault_detected_effect_exact_value fails with unresolved CARA.Mode_Control_Algorithm.PumpFaultDetected. The transition effect still sets pump_fault = 1 and PumpFault.enter still sets alarm_signal = 1, error_message = 1, software_control = 0, and CA_mode = 0.；intent=Change PumpFaultDetected event scope to parent-scoped : without changing ...<truncated 18 chars> |
| `fixreq-0-sd6-6-f42b9b46c4` | `accept` | ❌ | ✅ | Accepted because fault_removed_effect_exact_reset_values fails with unresolved CARA.Mode_Control_Algorithm.FaultRemoved from PumpFault. The existing effect resets pump_fault/alarm_signal/error_message and Manual enter/during releases software control and restores manual flow/pump speed; parent-scoping FaultRemoved resolves the runtime error.；intent=Change Pu...<truncated 102 chars> |
| `fixreq-0-sd6-7-daa3842279` | `accept` | ❌ | ✅ | Accepted because initiate_ac_exact_target_from_manual fails with unresolved CARA.Mode_Control_Algorithm.InitiateAC from Manual. The target Ask_StartAC is already correct and the Manual/Ask_StartAC actions preserve the expected variables; only event visibility is repaired.；intent=Make InitiateAC visible as a Mode_Control_Algorithm-level event. |
| `fixreq-0-sd6-8-5b0d4084ef` | `accept` | ❌ | ✅ | Accepted because start_ac_enter_effects_exact_values fails with unresolved CARA.Mode_Control_Algorithm.StartAC from Ask_StartAC. The target AutocontrolInit and its enter effects CA_mode = 1 and software_control = 1 are preserved; parent-scoping StartAC fixes the scenario.；intent=Change Ask_StartAC -> AutocontrolInit StartAC from source-local :: to parent-sco...<truncated 6 chars> |
- repair_rationale：All nine failing scenarios share the same expected-vs-actual gap: scenario events are injected as CARA.Mode_Control_Algorithm.<EventName>, but the current DSL declares those events with source-local :: scope, creating events such as Manual....<truncated 113 chars>；The smallest safe repair is to change the NL-grounded caregiver, pump fault, fault removal, and cross-component fallback events inside Mode_Control_Algorithm from :: EventName to parent-relative : EventName. This preserves all state targets...<truncated 52 chars>；initiate_change_setpoint_start_autocontrol and initiate_ac_exact_target_from_manual are repaired because InitiateAC now resolves at CARA.Mode_Control_Algorithm.InitiateAC and still targets Ask_StartAC; Ask_StartAC.during refreshes sensor_bu...<truncated 8 chars>；change_setpoint_effect_exact_value is repaired because ChangeSetpoint now resolves at CARA.Mode_Control_Algorithm.ChangeSetpoint while the self-transition still increments target_bp by exactly 1.0 and Ask_StartAC.during refreshes sensor_buf...<truncated 7 chars>；start_ac_enter_effects_exact_values is repaired because StartAC now resolves at CARA.Mode_Control_Algorithm.StartAC and still enters AutocontrolInit, whose enter action sets CA_mode = 1 and software_control = 1.
- diff_summary：`{"summary": "Changed Mode_Control_Algorithm event transitions and forced backManual fallbacks from source-local :: EventName to parent-relative : EventName so CARA.Mode_Control_Algorithm.<EventName> scenario injections resolve. Preserved all variables, states, effects, guards, and targets. Moved the Mode_Control_Algorithm initial transition [*] -> Manual; before forced fallback lines to make the required initial grounding explicit while preserving semantics."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_message = 0;
def int log_records = 0;
def float bp_reading = 120.0;
def float target_bp = 120.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float built_in_switch_speed = 1.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def float sensor_buffer_bp = 120.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        [*] -> Manual;

        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_voltage = 0.0;
            }
            during {
                sensor_buffer_bp = bp_reading;
                flow_rate = default_flow_rate;
                pump_speed = built_in_switch_speed;
            }
        }

        state Ask_StartAC {
            during {
                sensor_buffer_bp = bp_reading;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = bp_reading;
            }
        }

        state AutocontrolNormal {
            during {
                sensor_buffer_bp = bp_reading;
                if [pump_fault == 0] {
                    if [bp_reading > target_bp] {
                        flow_rate = flow_rate - 1.0;
                    } else if [bp_reading < target_bp] {
                        flow_rate = flow_rate + 1.0;
                    } else {
                        flow_rate = flow_rate;
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_records = log_records + 1;
                }
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                error_message = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit : StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal : if [software_control > 0];
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -17,12 +17,12 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
+        [*] -> Manual;
 
-        [*] -> Manual;
+        ! * -> Manual : CA_backManual;
+        ! * -> Manual : CB_backManual;
+        ! * -> Manual : CP_backManual;
+        ! * -> Manual : CC_backManual;
 
         state Manual {
             enter {
@@ -80,13 +80,13 @@
             }
         }
 
-        Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = target_bp + 1.0; };
-        Ask_StartAC -> AutocontrolInit :: StartAC;
-        Ask_StartAC -> Manual :: TerminateAC;
+        Manual -> Ask_StartAC : InitiateAC;
+        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_bp = target_bp + 1.0; };
+        Ask_StartAC -> AutocontrolInit : StartAC;
+        Ask_StartAC -> Manual : TerminateAC;
         AutocontrolInit -> AutocontrolNormal : if [software_control > 0];
-        AutocontrolNormal -> Manual :: TerminateAC;
-        AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_fault = 1; };
-        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
+        AutocontrolNormal -> Manual : TerminateAC;
+        AutocontrolNormal -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
+        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:3933da2f007422d0cd79c9f071f66f8d0974e12f4e96d52438dcd40d08aaa203`。
  - SL-10 evidence 1: `{"summary": "The NL requires CARA.Mode_Control_Algorithm with Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, variables for CA_mode/software_control/pump_fault/alarm/error/BP/target/flow/pump speed/control voltage/sensor buffer/logs, caregiver InitiateAC/ChangeSetpoint/StartAC/TerminateAC behavior, pump-fault detection/removal behavior, and cross-component backManual recovery to Manual. The candidate preserves all these states, variables, state actions, transition targets, guards, and effects."}`
  - SL-10 evidence 2: `{"summary": "All nine SL-9 decisions accept the same concrete repair: scenario injections use CARA.Mode_Control_Algorithm.<EventName>, while the old DSL declared source-local events using '::'. The candidate changes InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, FaultRemoved, and CA/CB/CP/CC_backManual transitions to parent-relative ':' events, directly addressing the unresolved_event_path failures without changing the intended targets or effects."}`
  - SL-10 evidence 3: `{"summary": "Scenario obligations are preserved at target/effect level: Manual -> Ask_StartAC on InitiateAC; Ask_StartAC self-transition increments target_bp by exactly 1.0 on ChangeSetpoint; Ask_StartAC -> AutocontrolInit on StartAC with AutocontrolInit.enter setting CA_mode = 1 and software_control = 1; TerminateAC from Ask_StartAC and AutocontrolNormal returns to Manual; PumpFaultDetected from AutocontrolNormal enters PumpFault and sets pump_fault/alarm/error/release-control values; FaultRemoved resets fault/alarm/error and returns to Manual."}`
  - SL-10 evidence 4: `{"summary": "Manual recovery remains consistent with the NL: Manual.enter clears CA_mode, software_control, and control_voltage, while Manual.during refreshes sensor_buffer_bp from bp_reading and restores flow_rate and pump_speed from default_flow_rate and built_in_switch_speed. The forced fallback transitions CA_backManual, CB_backManual, CP_backManual, and CC_backManual all still target Manual."}`
  - SL-10 evidence 5: `{"summary": "The rework candidate is not a blind repeat of the previously rejected candidate: its hash changed from sha256:933d32f6f2b756fb04e951511407508e0121e37fcc9cd5bdb9814d0584b46108 to sha256:29cc18bfbd8a369371b45238eda558b9556ee0e0ca68d1fbcf09b26de497a206, and it moved the nested Mode_Control_Algorithm initial transition before the forced fallback lines to make the required initial grounding explicit."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.；For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-ground...<truncated 152 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial:CARA_to_Mode_Control_Algorithm", "transition:initial:Mode_Control_Algorithm_to_Manual"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_change_setpoint_start_autocontrol, terminate_from_ask_returns_manual, autocontrol_pump_fault_and_removal, terminate_from_normal_returns_manual, change_setpoint_effect_exact_value, pump_fault_detected_effect_exact_value, fault_removed_effect_exact_reset_values, initiate_ac_exact_target_from_manual, start_ac_enter_effects_exact_values`。
- before_dsl_hash：`sha256:6856744fb026d92edfa34dfb0a784ee639344b5f61d3895ce6fbee6217164637`；candidate_dsl_hash：`sha256:99ae00ad0dfe4674b9646e0d8f36ebf13bd9c8c2d06a8d7a58e902ef3e2923af`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：
- 7. `<unknown>` `` policy=``：
- 8. `<unknown>` `` policy=``：
- ……另有 `1` 条 evidence 见 run record。

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-968f96516bd`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`9`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-d861f18d08` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init exercises InitiateAC, ChangeSetpoint in Ask_StartAC, and StartAC entering AutocontrolInit.', 'name': 'initiate_change_setpoint_start_autocontrol', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init exercises InitiateAC, ChangeSetpoint in Ask_StartAC, and StartAC entering AutocontrolInit.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'sensor_buffer_bp': 120.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'sensor_buffer_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'caregiver_initiates_ac', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'bp_reading': 120.0, 'flow_rate': 1.0, 'target_bp': 120.0}, 'scenario_name': 'initiate_change_setpoint_start_autocontrol', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 120.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 1.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 1.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 120.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'default_reaches_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 120.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 1.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 1.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'caregiver_initiates_ac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-b89694a3d8` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start verifies caregiver TerminateAC from Ask_StartAC returns to the Manual recovery target.', 'name': 'terminate_from_ask_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start verifies caregiver TerminateAC from Ask_StartAC returns to the Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 1, 'control_voltage': 0.0, 'flow_rate': 0.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_voltage': 0.0, 'flow_rate': 1.75, 'pump_speed': 2.25, 'sensor_buffer_bp': 122.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.TerminateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_before_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'bp_reading': 122.0, 'built_in_switch_speed': 2.25, 'default_flow_rate': 1.75, 'software_control': 1, 'target_bp': 125.0}, 'scenario_name': 'terminate_from_ask_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 122.0, 'built_in_switch_speed': 2.25, 'control_voltage': 0.0, 'default_flow_rate': 1.75, 'error_message': 0, 'flow_rate': 0.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 125.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.TerminateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_before_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-2-6c81985d39` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved returns to Manual releasing software control.', 'name': 'autocontrol_pump_fault_and_removal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved returns to Manual releasing software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'error_message': 0, 'pump_fault': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 1, 'error_message': 1, 'pump_fault': 1, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_detected_enters_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 130.0, 'built_in_switch_speed': 2.5, 'default_flow_rate': 1.5, 'error_message': 0, 'flow_rate': 4.0, 'pump_fault': 0, 'software_control': 1, 'target_bp': 120.0}, 'scenario_name': 'autocontrol_pump_fault_and_removal', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 130.0, 'built_in_switch_speed': 2.5, 'control_voltage': 0.0, 'default_flow_rate': 1.5, 'error_message': 0, 'flow_rate': 4.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_detected_enters_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-1378209e1f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start verifies caregiver TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-speed behavior.', 'name': 'terminate_from_normal_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start verifies caregiver TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-speed behavior.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'control_voltage': 8.0, 'flow_rate': 8.0, 'pump_speed': 8.0, 'sensor_buffer_bp': 120.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_voltage': 0.0, 'flow_rate': 2.0, 'pump_speed': 4.0, 'sensor_buffer_bp': 119.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Termina", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_normal_control', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'bp_reading': 119.0, 'built_in_switch_speed': 4.0, 'control_voltage': 8.0, 'default_flow_rate': 2.0, 'flow_rate': 8.0, 'pump_speed': 8.0, 'software_control': 1}, 'scenario_name': 'terminate_from_normal_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 119.0, 'built_in_switch_speed': 4.0, 'control_voltage': 8.0, 'default_flow_rate': 2.0, 'error_message': 0, 'flow_rate': 8.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 8.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Termina", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_normal_control', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-f6b978093f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates ChangeSetpoint self-transition and checks the target_bp effect is exactly a one-unit increase.', 'name': 'change_setpoint_effect_exact_value', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates ChangeSetpoint self-transition and checks the target_bp effect is exactly a one-unit increase.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'sensor_buffer_bp': 120.0, 'target_bp': 130.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.ChangeSetpoint'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'sensor_buffer_bp': 123.0, 'target_bp': 131.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.ChangeSetpoint', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'setpoint_incremented_once', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'bp_reading': 123.0, 'target_bp': 130.0}, 'scenario_name': 'change_setpoint_effect_exact_value', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 123.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 0.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 130.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'setpoint_incremented_once', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-5-0a776f9d52` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates PumpFaultDetected and checks both the PumpFault target and the pump/alarm/software-control effects.', 'name': 'pump_fault_detected_effect_exact_value', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates PumpFaultDetected and checks both the PumpFault target and the pump/alarm/software-control effects.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'error_message': 0, 'pump_fault': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 1, 'error_message': 1, 'pump_fault': 1, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_detected_sets_fault_and_alarms', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 129.0, 'error_message': 0, 'flow_rate': 6.0, 'pump_fault': 0, 'software_control': 1, 'target_bp': 120.0}, 'scenario_name': 'pump_fault_detected_effect_exact_value', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 129.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 6.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_detected_sets_fault_and_alarms', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-6-f42b9b46c4` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates FaultRemoved and checks fault/alarm/error reset values plus Manual recovery target.', 'name': 'fault_removed_effect_exact_reset_values', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates FaultRemoved and checks fault/alarm/error reset values plus Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 1, 'control_voltage': 7.0, 'error_message': 1, 'flow_rate': 7.0, 'pump_fault': 1, 'pump_speed': 7.0, 'sensor_buffer_bp': 120.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.FaultRemoved'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'control_voltage': 0.0, 'error_message': 0, 'flow_rate': 1.9, 'pump_fault': 0, 'pump_speed': 2.9, 'sensor_buffer_bp': 131.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.FaultRemoved', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_removed_resets_and_returns_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 1, 'bp_reading': 131.0, 'built_in_switch_speed': 2.9, 'control_voltage': 7.0, 'default_flow_rate': 1.9, 'error_message': 1, 'flow_rate': 7.0, 'pump_fault': 1, 'pump_speed': 7.0, 'software_control': 1}, 'scenario_name': 'fault_removed_effect_exact_reset_values', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'bp_reading': 131.0, 'built_in_switch_speed': 2.9, 'control_voltage': 7.0, 'default_flow_rate': 1.9, 'error_message': 1, 'flow_rate': 7.0, 'log_records': 0, 'pump_fault': 1, 'pump_speed': 7.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_removed_resets_and_returns_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-7-daa3842279` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates caregiver InitiateAC from Manual and asserts the exact Ask_StartAC target rather than another autocontrol state.', 'name': 'initiate_ac_exact_target_from_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates caregiver InitiateAC from Manual and asserts the exact Ask_StartAC target rather than another autocontrol state.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'flow_rate': 2.2, 'pump_speed': 3.2, 'sensor_buffer_bp': 120.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'CA_mode': 0, 'flow_rate': 2.2, 'pump_speed': 3.2, 'sensor_buffer_bp': 124.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'initiate_ac_enters_ask_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Manual', 'initial_vars': {'CA_mode': 0, 'bp_reading': 124.0, 'built_in_switch_speed': 3.2, 'default_flow_rate': 2.2, 'flow_rate': 2.2, 'pump_speed': 3.2, 'software_control': 0, 'target_bp': 120.0}, 'scenario_name': 'initiate_ac_exact_target_from_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 124.0, 'built_in_switch_speed': 3.2, 'control_voltage': 0.0, 'default_flow_rate': 2.2, 'error_message': 0, 'flow_rate': 2.2, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 3.2, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'initiate_ac_enters_ask_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-8-5b0d4084ef` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates StartAC from Ask_StartAC and checks the exact AutocontrolInit target plus software-control enable effects.', 'name': 'start_ac_enter_effects_exact_values', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates StartAC from Ask_StartAC and checks the exact AutocontrolInit target plus software-control enable effects.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 0, 'control_voltage': 0.0, 'flow_rate': 3.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'control_voltage': 0.0, 'flow_rate': 3.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 125.0, 'software_control': 1}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'start_ac_sets_control_enabled', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 0, 'bp_reading': 125.0, 'control_voltage': 0.0, 'flow_rate': 3.0, 'pump_speed': 0.0, 'software_control': 0, 'target_bp': 121.0}, 'scenario_name': 'start_ac_enter_effects_exact_values', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 125.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 3.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 121.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'start_ac_sets_control_enabled', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:error_message, variable:bp_reading, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2944`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-d861f18d08` | `accept` | ❌ | ✅ | initiate_change_setpoint_start_autocontrol fails because CARA.Mode_Control_Algorithm.InitiateAC is injected as a Mode_Control_Algorithm-level event, while the current DSL declares it as source-local Manual.InitiateAC. Change InitiateAC to parent-relative event scope and preserve the Manual -> Ask_StartAC target and sensor-buffer behavior.；intent=Change Manua...<truncated 57 chars> |
| `fixreq-0-sd6-1-b89694a3d8` | `accept` | ❌ | ✅ | terminate_from_ask_returns_manual fails because CARA.Mode_Control_Algorithm.TerminateAC cannot resolve from Ask_StartAC. TerminateAC is a caregiver command at the Mode_Control_Algorithm level; parent-relative scope preserves the Manual recovery target and actions.；intent=Change Ask_StartAC -> Manual TerminateAC from :: to parent-relative :. |
| `fixreq-0-sd6-2-6c81985d39` | `accept` | ❌ | ✅ | autocontrol_pump_fault_and_removal fails because CARA.Mode_Control_Algorithm.PumpFaultDetected cannot resolve from AutocontrolNormal. Parent-relative scope makes the pump-fault event visible while preserving the PumpFault target and fault/alarm/release-control effects.；intent=Change AutocontrolNormal -> PumpFault PumpFaultDetected from :: to parent-relative ...<truncated 2 chars> |
| `fixreq-0-sd6-3-1378209e1f` | `accept` | ❌ | ✅ | terminate_from_normal_returns_manual fails because CARA.Mode_Control_Algorithm.TerminateAC cannot resolve from AutocontrolNormal. Parent-relative scope fixes the event path and preserves Manual.enter/during restoration of manual operation.；intent=Change AutocontrolNormal -> Manual TerminateAC from :: to parent-relative :. |
| `fixreq-0-sd6-4-f6b978093f` | `accept` | ❌ | ✅ | change_setpoint_effect_exact_value fails because CARA.Mode_Control_Algorithm.ChangeSetpoint cannot resolve from Ask_StartAC. The existing target_bp = target_bp + 1.0 effect is already exact; only event visibility is changed.；intent=Change Ask_StartAC self-transition ChangeSetpoint from :: to parent-relative : while preserving target_bp increment. |
| `fixreq-0-sd6-5-0a776f9d52` | `accept` | ❌ | ✅ | pump_fault_detected_effect_exact_value fails because CARA.Mode_Control_Algorithm.PumpFaultDetected cannot resolve. Parent-relative scope preserves the transition effect pump_fault = 1 and PumpFault.enter alarm/error/software-control values.；intent=Make PumpFaultDetected a parent-relative Mode_Control_Algorithm event. |
| `fixreq-0-sd6-6-f42b9b46c4` | `accept` | ❌ | ✅ | fault_removed_effect_exact_reset_values fails because CARA.Mode_Control_Algorithm.FaultRemoved cannot resolve from PumpFault. Parent-relative scope preserves the reset effect and Manual recovery actions.；intent=Change PumpFault -> Manual FaultRemoved from :: to parent-relative :. |
| `fixreq-0-sd6-7-daa3842279` | `accept` | ❌ | ✅ | initiate_ac_exact_target_from_manual fails because CARA.Mode_Control_Algorithm.InitiateAC cannot resolve from Manual. The target Ask_StartAC is already correct; parent-relative event scope fixes only the runtime event-resolution gap.；intent=Make InitiateAC visible at the Mode_Control_Algorithm event path. |
| `fixreq-0-sd6-8-5b0d4084ef` | `accept` | ❌ | ✅ | start_ac_enter_effects_exact_values fails because CARA.Mode_Control_Algorithm.StartAC cannot resolve from Ask_StartAC. The AutocontrolInit target and its CA_mode/software_control enter effects are preserved; only event scope is repaired.；intent=Change Ask_StartAC -> AutocontrolInit StartAC from :: to parent-relative :. |
- repair_rationale：All nine hard simulation failures have the same concrete mechanism: the scenarios inject CARA.Mode_Control_Algorithm.<EventName>, but the original DSL used source-local :: events such as Manual.InitiateAC, Ask_StartAC.StartAC, and Autocontr...<truncated 126 chars>；The smallest functional edit is to change the NL-grounded caregiver, pump-fault, fault-removal, and cross-component backManual events inside Mode_Control_Algorithm from source-local :: EventName to parent-relative : EventName. This keeps th...<truncated 141 chars>；Scenario initiate_change_setpoint_start_autocontrol and initiate_ac_exact_target_from_manual now resolve InitiateAC at CARA.Mode_Control_Algorithm.InitiateAC and still enter Ask_StartAC. Ask_StartAC.during refreshes sensor_buffer_bp from bp...<truncated 9 chars>；Scenario change_setpoint_effect_exact_value now resolves ChangeSetpoint at CARA.Mode_Control_Algorithm.ChangeSetpoint; the self-transition still increments target_bp by exactly 1.0 and remains in Ask_StartAC.；Scenario start_ac_enter_effects_exact_values now resolves StartAC at CARA.Mode_Control_Algorithm.StartAC; Ask_StartAC -> AutocontrolInit is preserved and AutocontrolInit.enter still sets CA_mode = 1 and software_control = 1.
- diff_summary：`{"summary": "Changed Mode_Control_Algorithm events InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, FaultRemoved, CA_backManual, CB_backManual, CP_backManual, and CC_backManual from source-local :: scope to parent-relative : scope so CARA.Mode_Control_Algorithm.<EventName> scenario injections resolve. Preserved all required states, variables, transition targets, effects, and guards. Kept and made explicit the required initial transitions CARA -> Mode_Control_Algorithm and Mode_Control_Algorithm -> Manual with NL-consistent initialization effects to address the repeated missing_required_grounding objection."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_message = 0;
def int log_records = 0;
def float bp_reading = 120.0;
def float target_bp = 120.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float built_in_switch_speed = 1.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def float sensor_buffer_bp = 120.0;

state CARA {
    [*] -> Mode_Control_Algorithm effect { sensor_buffer_bp = bp_reading; };

    state Mode_Control_Algorithm {
        [*] -> Manual effect {
            CA_mode = 0;
            software_control = 0;
            control_voltage = 0.0;
        };

        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_voltage = 0.0;
            }
            during {
                sensor_buffer_bp = bp_reading;
                flow_rate = default_flow_rate;
                pump_speed = built_in_switch_speed;
            }
        }

        state Ask_StartAC {
            during {
                sensor_buffer_bp = bp_reading;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = bp_reading;
            }
        }

        state AutocontrolNormal {
            during {
                sensor_buffer_bp = bp_reading;
                if [pump_fault == 0] {
                    if [bp_reading > target_bp] {
                        flow_rate = flow_rate - 1.0;
                    } else if [bp_reading < target_bp] {
                        flow_rate = flow_rate + 1.0;
                    } else {
                        flow_rate = flow_rate;
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_records = log_records + 1;
                }
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                error_message = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit : StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal : if [software_control > 0];
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -14,15 +14,19 @@
 def float sensor_buffer_bp = 120.0;
 
 state CARA {
-    [*] -> Mode_Control_Algorithm;
+    [*] -> Mode_Control_Algorithm effect { sensor_buffer_bp = bp_reading; };
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
+        [*] -> Manual effect {
+            CA_mode = 0;
+            software_control = 0;
+            control_voltage = 0.0;
+        };
 
-        [*] -> Manual;
+        ! * -> Manual : CA_backManual;
+        ! * -> Manual : CB_backManual;
+        ! * -> Manual : CP_backManual;
+        ! * -> Manual : CC_backManual;
 
         state Manual {
             enter {
@@ -80,13 +84,13 @@
             }
         }
 
-        Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = target_bp + 1.0; };
-        Ask_StartAC -> AutocontrolInit :: StartAC;
-        Ask_StartAC -> Manual :: TerminateAC;
+        Manual -> Ask_StartAC : InitiateAC;
+        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_bp = target_bp + 1.0; };
+        Ask_StartAC -> AutocontrolInit : StartAC;
+        Ask_StartAC -> Manual : TerminateAC;
         AutocontrolInit -> AutocontrolNormal : if [software_control > 0];
-        AutocontrolNormal -> Manual :: TerminateAC;
-        AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_fault = 1; };
-        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
+        AutocontrolNormal -> Manual : TerminateAC;
+        AutocontrolNormal -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
+        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:7d0076e36ffa0403313565865b53452f1548da35f10352a7d8e138d6be60825a`。
  - SL-10 evidence 1: `{"summary": "The NL requires CARA.Mode_Control_Algorithm with Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, caregiver InitiateAC/ChangeSetpoint/StartAC/TerminateAC behavior, pump-fault detection/removal behavior, and cross-component backManual recovery to Manual. The candidate preserves all required states and variables and does not drop any NL-required targets, guards, or effects."}`
  - SL-10 evidence 2: `{"summary": "All nine hard simulation requests failed for the same mechanism: scenario injections used CARA.Mode_Control_Algorithm.<EventName>, but the old DSL declared the relevant events with source-local '::' scope, producing unresolved_event_path errors for InitiateAC, TerminateAC, PumpFaultDetected, ChangeSetpoint, StartAC, and FaultRemoved. SL-9 accepted each request with the same NL-grounded repair: make those events visible at Mode_Control_Algorithm scope. The candidate implements that by changing InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, FaultRemoved, and CA/CB/CP/CC_backManual from '::' to parent-relative ':' while preserving transition targets and effect...<truncated 4 chars>`
  - SL-10 evidence 3: `{"summary": "The target/effect obligations from the failing scenarios remain represented: Manual -> Ask_StartAC on InitiateAC; Ask_StartAC self-transition on ChangeSetpoint increments target_bp by exactly 1.0; Ask_StartAC -> AutocontrolInit on StartAC, with AutocontrolInit.enter setting CA_mode = 1 and software_control = 1; TerminateAC from Ask_StartAC and AutocontrolNormal returns to Manual; AutocontrolNormal -> PumpFault on PumpFaultDetected sets pump_fault = 1 and PumpFault.enter sets alarm_signal = 1, error_message = 1, software_control = 0, CA_mode = 0; PumpFault -> Manual on FaultRemoved resets pump_fault, alarm_signal, and error_message."}`
  - SL-10 evidence 4: `{"summary": "Manual recovery remains consistent with the NL fallback requirement: Manual.enter clears CA_mode, software_control, and control_voltage, and Manual.during refreshes sensor_buffer_bp from bp_reading while restoring flow_rate and pump_speed from default_flow_rate and built_in_switch_speed. The forced CA_backManual, CB_backManual, CP_backManual, and CC_backManual transitions still all target Manual."}`
  - SL-10 evidence 5: `{"summary": "The candidate specifically addresses the repeated FixLog repair_memory objection about initial grounding. Unlike prior rejected hashes sha256:933d32f6f2b756fb04e951511407508e0121e37fcc9cd5bdb9814d0584b46108 and sha256:29cc18bfbd8a369371b45238eda558b9556ee0e0ca68d1fbcf09b26de497a206, the current candidate hash sha256:99ae00ad0dfe4674b9646e0d8f36ebf13bd9c8c2d06a8d7a58e902ef3e2923af keeps and makes explicit both initial transitions with NL-consistent initialization effects."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.；For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-ground...<truncated 152 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial:CARA_to_Mode_Control_Algorithm", "transition:initial:Mode_Control_Algorithm_to_Manual"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `0` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`initiate_change_setpoint_start_autocontrol, terminate_from_ask_returns_manual, autocontrol_pump_fault_and_removal, terminate_from_normal_returns_manual, change_setpoint_effect_exact_value, pump_fault_detected_effect_exact_value, fault_removed_effect_exact_reset_values, initiate_ac_exact_target_from_manual, start_ac_enter_effects_exact_values`。
- before_dsl_hash：`sha256:6856744fb026d92edfa34dfb0a784ee639344b5f61d3895ce6fbee6217164637`；candidate_dsl_hash：`sha256:ce72c8d44b302dadf9c88f390efa482afacd8764f5a6e38e3daea29e5bd8651d`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：
- 6. `<unknown>` `` policy=``：
- 7. `<unknown>` `` policy=``：
- 8. `<unknown>` `` policy=``：
- ……另有 `1` 条 evidence 见 run record。

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-968f96516bd`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`9`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-d861f18d08` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'default-init exercises InitiateAC, ChangeSetpoint in Ask_StartAC, and StartAC entering AutocontrolInit.', 'name': 'initiate_change_setpoint_start_autocontrol', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'default-init exercises InitiateAC, ChangeSetpoint in Ask_StartAC, and StartAC entering AutocontrolInit.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'sensor_buffer_bp': 120.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'sensor_buffer_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 1, 'step_name': 'caregiver_initiates_ac', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': None, 'initial_vars': {'bp_reading': 120.0, 'flow_rate': 1.0, 'target_bp': 120.0}, 'scenario_name': 'initiate_change_setpoint_start_autocontrol', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 120.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 1.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 1.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 120.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'default_reaches_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 120.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 1.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 1.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 1, 'step_name': 'caregiver_initiates_ac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-b89694a3d8` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start verifies caregiver TerminateAC from Ask_StartAC returns to the Manual recovery target.', 'name': 'terminate_from_ask_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start verifies caregiver TerminateAC from Ask_StartAC returns to the Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 1, 'control_voltage': 0.0, 'flow_rate': 0.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_voltage': 0.0, 'flow_rate': 1.75, 'pump_speed': 2.25, 'sensor_buffer_bp': 122.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.TerminateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_before_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 1, 'bp_reading': 122.0, 'built_in_switch_speed': 2.25, 'default_flow_rate': 1.75, 'software_control': 1, 'target_bp': 125.0}, 'scenario_name': 'terminate_from_ask_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 122.0, 'built_in_switch_speed': 2.25, 'control_voltage': 0.0, 'default_flow_rate': 1.75, 'error_message': 0, 'flow_rate': 0.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 125.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.TerminateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_before_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-2-6c81985d39` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved returns to Manual releasing software control.', 'name': 'autocontrol_pump_fault_and_removal', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved returns to Manual releasing software control.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'error_message': 0, 'pump_fault': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 1, 'error_message': 1, 'pump_fault': 1, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_detected_enters_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 130.0, 'built_in_switch_speed': 2.5, 'default_flow_rate': 1.5, 'error_message': 0, 'flow_rate': 4.0, 'pump_fault': 0, 'software_control': 1, 'target_bp': 120.0}, 'scenario_name': 'autocontrol_pump_fault_and_removal', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 130.0, 'built_in_switch_speed': 2.5, 'control_voltage': 0.0, 'default_flow_rate': 1.5, 'error_message': 0, 'flow_rate': 4.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_detected_enters_pump_fault', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-1378209e1f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start verifies caregiver TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-speed behavior.', 'name': 'terminate_from_normal_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start verifies caregiver TerminateAC from AutocontrolNormal returns to Manual and restores manual pump-speed behavior.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'control_voltage': 8.0, 'flow_rate': 8.0, 'pump_speed': 8.0, 'sensor_buffer_bp': 120.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'control_voltage': 0.0, 'flow_rate': 2.0, 'pump_speed': 4.0, 'sensor_buffer_bp': 119.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Termina", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.TerminateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'terminate_normal_control', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'bp_reading': 119.0, 'built_in_switch_speed': 4.0, 'control_voltage': 8.0, 'default_flow_rate': 2.0, 'flow_rate': 8.0, 'pump_speed': 8.0, 'software_control': 1}, 'scenario_name': 'terminate_from_normal_returns_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 119.0, 'built_in_switch_speed': 4.0, 'control_voltage': 8.0, 'default_flow_rate': 2.0, 'error_message': 0, 'flow_rate': 8.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 8.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.TerminateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.Termina", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'terminate_normal_control', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-f6b978093f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates ChangeSetpoint self-transition and checks the target_bp effect is exactly a one-unit increase.', 'name': 'change_setpoint_effect_exact_value', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates ChangeSetpoint self-transition and checks the target_bp effect is exactly a one-unit increase.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'sensor_buffer_bp': 120.0, 'target_bp': 130.0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.ChangeSetpoint'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'sensor_buffer_bp': 123.0, 'target_bp': 131.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.ChangeSetpoint', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'setpoint_incremented_once', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'bp_reading': 123.0, 'target_bp': 130.0}, 'scenario_name': 'change_setpoint_effect_exact_value', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 123.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 0.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 130.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.ChangeSetpoint': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.ChangeSetp", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'setpoint_incremented_once', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-5-0a776f9d52` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates PumpFaultDetected and checks both the PumpFault target and the pump/alarm/software-control effects.', 'name': 'pump_fault_detected_effect_exact_value', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates PumpFaultDetected and checks both the PumpFault target and the pump/alarm/software-control effects.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'error_message': 0, 'pump_fault': 0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFaultDetected'], 'expected_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 1, 'error_message': 1, 'pump_fault': 1, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.PumpFaultDetected', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_detected_sets_fault_and_alarms', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 129.0, 'error_message': 0, 'flow_rate': 6.0, 'pump_fault': 0, 'software_control': 1, 'target_bp': 120.0}, 'scenario_name': 'pump_fault_detected_effect_exact_value', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'bp_reading': 129.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 6.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.PumpFaultDetected': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.AutocontrolNormal.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.P", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_detected_sets_fault_and_alarms', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-6-f42b9b46c4` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates FaultRemoved and checks fault/alarm/error reset values plus Manual recovery target.', 'name': 'fault_removed_effect_exact_reset_values', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates FaultRemoved and checks fault/alarm/error reset values plus Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 1, 'control_voltage': 7.0, 'error_message': 1, 'flow_rate': 7.0, 'pump_fault': 1, 'pump_speed': 7.0, 'sensor_buffer_bp': 120.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.FaultRemoved'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'control_voltage': 0.0, 'error_message': 0, 'flow_rate': 1.9, 'pump_fault': 0, 'pump_speed': 2.9, 'sensor_buffer_bp': 131.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.FaultRemoved', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'fault_removed_resets_and_returns_manual', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 1, 'bp_reading': 131.0, 'built_in_switch_speed': 2.9, 'control_voltage': 7.0, 'default_flow_rate': 1.9, 'error_message': 1, 'flow_rate': 7.0, 'pump_fault': 1, 'pump_speed': 7.0, 'software_control': 1}, 'scenario_name': 'fault_removed_effect_exact_reset_values', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'bp_reading': 131.0, 'built_in_switch_speed': 2.9, 'control_voltage': 7.0, 'default_flow_rate': 1.9, 'error_message': 1, 'flow_rate': 7.0, 'log_records': 0, 'pump_fault': 1, 'pump_speed': 7.0, 'sensor_buffer_bp': 120.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.FaultRemoved': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.PumpFault.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.FaultRemoved'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'fault_removed_resets_and_returns_manual', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-7-daa3842279` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates caregiver InitiateAC from Manual and asserts the exact Ask_StartAC target rather than another autocontrol state.', 'name': 'initiate_ac_exact_target_from_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates caregiver InitiateAC from Manual and asserts the exact Ask_StartAC target rather than another autocontrol state.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'flow_rate': 2.2, 'pump_speed': 3.2, 'sensor_buffer_bp': 120.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.InitiateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'expected_vars': {'CA_mode': 0, 'flow_rate': 2.2, 'pump_speed': 3.2, 'sensor_buffer_bp': 124.0, 'software_control': 0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.InitiateAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'initiate_ac_enters_ask_start', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Manual', 'initial_vars': {'CA_mode': 0, 'bp_reading': 124.0, 'built_in_switch_speed': 3.2, 'default_flow_rate': 2.2, 'flow_rate': 2.2, 'pump_speed': 3.2, 'software_control': 0, 'target_bp': 120.0}, 'scenario_name': 'initiate_ac_exact_target_from_manual', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 124.0, 'built_in_switch_speed': 3.2, 'control_voltage': 0.0, 'default_flow_rate': 2.2, 'error_message': 0, 'flow_rate': 2.2, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 3.2, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 120.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.InitiateAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Manual.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.InitiateAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'initiate_ac_enters_ask_start', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-8-5b0d4084ef` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates StartAC from Ask_StartAC and checks the exact AutocontrolInit target plus software-control enable effects.', 'name': 'start_ac_enter_effects_exact_values', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates StartAC from Ask_StartAC and checks the exact AutocontrolInit target plus software-control enable effects.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars_focus': {'CA_mode': 0, 'control_voltage': 0.0, 'flow_rate': 3.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 0}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.StartAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'expected_vars': {'CA_mode': 1, 'control_voltage': 0.0, 'flow_rate': 3.0, 'pump_speed': 0.0, 'sensor_buffer_bp': 125.0, 'software_control': 1}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'runtime_error_hint': {'event_path': 'CARA.Mode_Control_Algorithm.StartAC', 'instruction': 'The failing scenario injects this event but the runtime cannot resolve it from the active/hot-start state. Repair the DSL by adding or preserving an NL-grounded event/transition representation that is visible from the scenario source state; do not only change unrelated state/action code.', 'kind': 'unresolved_event_path'}, 'state_assertion_ok': None, 'step_index': 0, 'step_name': 'start_ac_sets_control_enabled', 'var_assertion_ok': None, 'var_mismatches': {}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'CA_mode': 0, 'bp_reading': 125.0, 'control_voltage': 0.0, 'flow_rate': 3.0, 'pump_speed': 0.0, 'software_control': 0, 'target_bp': 121.0}, 'scenario_name': 'start_ac_enter_effects_exact_values', 'status': 'error'}, 'setup_error': None, 'status': 'error', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'bp_reading': 125.0, 'built_in_switch_speed': 1.0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'error_message': 0, 'flow_rate': 3.0, 'log_records': 0, 'pump_fault': 0, 'pump_speed': 0.0, 'sensor_buffer_bp': 120.0, 'software_control': 0, 'target_bp': 121.0}, 'runtime_error': "SimulationRuntimeEventError: Cannot resolve event path 'CARA.Mode_Control_Algorithm.StartAC': failed with both StateMachine.resolve_event and State.resolve_event. Last error: State 'CARA.Mode_Control_Algorithm.Ask_StartAC.CARA' not found in hierarchy while resolving event reference 'CARA.Mode_Control_Algorithm.StartAC'", 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'start_ac_sets_control_enabled', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:software_control, variable:pump_fault, variable:alarm_signal, variable:error_message, variable:bp_reading, ... +25`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2956`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-d861f18d08` | `accept` | ❌ | ✅ | Accepted because initiate_change_setpoint_start_autocontrol fails at caregiver_initiates_ac: expected Ask_StartAC after CARA.Mode_Control_Algorithm.InitiateAC, but actual remained Manual due to unresolved parent event path. InitiateAC is NL-grounded as a Mode_Control_Algorithm caregiver command, so the transition is made parent-scoped while preserving the As...<truncated 134 chars> |
| `fixreq-0-sd6-1-b89694a3d8` | `accept` | ❌ | ✅ | Accepted because terminate_from_ask_returns_manual expects Ask_StartAC plus CARA.Mode_Control_Algorithm.TerminateAC to return to Manual with manual recovery variables, but the event path was unresolved. TerminateAC is a shared caregiver termination command at Mode_Control_Algorithm scope.；intent=Change Ask_StartAC -> Manual TerminateAC from source-local :: t...<truncated 20 chars> |
| `fixreq-0-sd6-2-6c81985d39` | `accept` | ❌ | ✅ | Accepted because autocontrol_pump_fault_and_removal expects PumpFaultDetected from AutocontrolNormal to enter PumpFault and set fault/alarm/release-control variables, but the parent event path was unresolved. The target and effects are already correct, so only event scope is repaired.；intent=Change AutocontrolNormal -> PumpFault PumpFaultDetected from source...<truncated 31 chars> |
| `fixreq-0-sd6-3-1378209e1f` | `accept` | ❌ | ✅ | Accepted because terminate_from_normal_returns_manual expects TerminateAC from AutocontrolNormal to return to Manual and restore manual pump-speed behavior, but CARA.Mode_Control_Algorithm.TerminateAC was unresolved. Parent-scoping the event preserves the existing Manual recovery actions.；intent=Change AutocontrolNormal -> Manual TerminateAC from source-loca...<truncated 26 chars> |
| `fixreq-0-sd6-4-f6b978093f` | `accept` | ❌ | ✅ | Accepted because change_setpoint_effect_exact_value expects ChangeSetpoint in Ask_StartAC to leave the state active, increment target_bp from 130.0 to 131.0, and refresh sensor_buffer_bp, but the parent event path was unresolved. The existing +1.0 effect is preserved.；intent=Change Ask_StartAC self-transition ChangeSetpoint from source-local :: to parent-rel...<truncated 53 chars> |
| `fixreq-0-sd6-5-0a776f9d52` | `accept` | ❌ | ✅ | Accepted because pump_fault_detected_effect_exact_value expects PumpFaultDetected to enter PumpFault with pump_fault, alarm_signal, error_message, software_control, and CA_mode set to exact values, but the event path was unresolved. The transition effect and PumpFault.enter actions are preserved.；intent=Make PumpFaultDetected a Mode_Control_Algorithm parent-...<truncated 48 chars> |
| `fixreq-0-sd6-6-f42b9b46c4` | `accept` | ❌ | ✅ | Accepted because fault_removed_effect_exact_reset_values expects FaultRemoved from PumpFault to reset fault/alarm/error values and return to Manual recovery, but CARA.Mode_Control_Algorithm.FaultRemoved was unresolved. Parent-scoping the event preserves the reset effect and Manual recovery actions.；intent=Change PumpFault -> Manual FaultRemoved from source-l...<truncated 60 chars> |
| `fixreq-0-sd6-7-daa3842279` | `accept` | ❌ | ✅ | Accepted because initiate_ac_exact_target_from_manual expects InitiateAC from Manual to enter Ask_StartAC exactly, but CARA.Mode_Control_Algorithm.InitiateAC was unresolved. The existing target is correct; event visibility is repaired.；intent=Make InitiateAC visible at the CARA.Mode_Control_Algorithm.InitiateAC event path. |
| `fixreq-0-sd6-8-5b0d4084ef` | `accept` | ❌ | ✅ | Accepted because start_ac_enter_effects_exact_values expects StartAC from Ask_StartAC to enter AutocontrolInit and set CA_mode/software_control to 1, but the parent event path was unresolved. The AutocontrolInit target and enter actions are preserved.；intent=Change Ask_StartAC -> AutocontrolInit StartAC from source-local :: to parent-relative :. |
- repair_rationale：All nine accepted requests share the same expected-vs-actual gap: scenario events are injected as CARA.Mode_Control_Algorithm.<EventName>, but the current DSL declared those caregiver/pump events as source-local events such as Manual.Initia...<truncated 190 chars>；The smallest functional edit is to change the NL-grounded Mode_Control_Algorithm caregiver, pump-fault, fault-removal, and cross-component fallback events from source-local :: to parent-relative : within the Mode_Control_Algorithm scope. Th...<truncated 266 chars>；initiate_change_setpoint_start_autocontrol and initiate_ac_exact_target_from_manual are repaired because InitiateAC now resolves at CARA.Mode_Control_Algorithm.InitiateAC and still targets Ask_StartAC. Ask_StartAC.during still refreshes sen...<truncated 30 chars>；change_setpoint_effect_exact_value is repaired because ChangeSetpoint now resolves at CARA.Mode_Control_Algorithm.ChangeSetpoint while preserving the exact target_bp = target_bp + 1.0 effect and the Ask_StartAC self-transition.；start_ac_enter_effects_exact_values is repaired because StartAC now resolves at CARA.Mode_Control_Algorithm.StartAC, still targets AutocontrolInit, and AutocontrolInit.enter still sets CA_mode = 1 and software_control = 1.
- diff_summary：`{"summary": "Changed Mode_Control_Algorithm events InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, FaultRemoved, CA_backManual, CB_backManual, CP_backManual, and CC_backManual from source-local :: scope to parent-relative : scope so CARA.Mode_Control_Algorithm.<EventName> scenario injections resolve. Preserved all required states, variables, targets, guards, and effects. Kept the concrete initial transitions [*] -> Mode_Control_Algorithm and [*] -> Manual and added NL-consistent initialization effects to make the missing_required_grounding objection explicit without changing recovery semantics."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int error_message = 0;
def int log_records = 0;
def float bp_reading = 120.0;
def float target_bp = 120.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float built_in_switch_speed = 1.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def float sensor_buffer_bp = 120.0;

state CARA {
    [*] -> Mode_Control_Algorithm effect {
        sensor_buffer_bp = bp_reading;
    };

    state Mode_Control_Algorithm {
        [*] -> Manual effect {
            CA_mode = 0;
            software_control = 0;
            control_voltage = 0.0;
        };

        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                control_voltage = 0.0;
            }
            during {
                sensor_buffer_bp = bp_reading;
                flow_rate = default_flow_rate;
                pump_speed = built_in_switch_speed;
            }
        }

        state Ask_StartAC {
            during {
                sensor_buffer_bp = bp_reading;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                sensor_buffer_bp = bp_reading;
            }
        }

        state AutocontrolNormal {
            during {
                sensor_buffer_bp = bp_reading;
                if [pump_fault == 0] {
                    if [bp_reading > target_bp] {
                        flow_rate = flow_rate - 1.0;
                    } else if [bp_reading < target_bp] {
                        flow_rate = flow_rate + 1.0;
                    } else {
                        flow_rate = flow_rate;
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_records = log_records + 1;
                }
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                error_message = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit : StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal : if [software_control > 0];
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -14,15 +14,21 @@
 def float sensor_buffer_bp = 120.0;
 
 state CARA {
-    [*] -> Mode_Control_Algorithm;
+    [*] -> Mode_Control_Algorithm effect {
+        sensor_buffer_bp = bp_reading;
+    };
 
     state Mode_Control_Algorithm {
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
+        [*] -> Manual effect {
+            CA_mode = 0;
+            software_control = 0;
+            control_voltage = 0.0;
+        };
 
-        [*] -> Manual;
+        ! * -> Manual : CA_backManual;
+        ! * -> Manual : CB_backManual;
+        ! * -> Manual : CP_backManual;
+        ! * -> Manual : CC_backManual;
 
         state Manual {
             enter {
@@ -80,13 +86,13 @@
             }
         }
 
-        Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = target_bp + 1.0; };
-        Ask_StartAC -> AutocontrolInit :: StartAC;
-        Ask_StartAC -> Manual :: TerminateAC;
+        Manual -> Ask_StartAC : InitiateAC;
+        Ask_StartAC -> Ask_StartAC : ChangeSetpoint effect { target_bp = target_bp + 1.0; };
+        Ask_StartAC -> AutocontrolInit : StartAC;
+        Ask_StartAC -> Manual : TerminateAC;
         AutocontrolInit -> AutocontrolNormal : if [software_control > 0];
-        AutocontrolNormal -> Manual :: TerminateAC;
-        AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_fault = 1; };
-        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
+        AutocontrolNormal -> Manual : TerminateAC;
+        AutocontrolNormal -> PumpFault : PumpFaultDetected effect { pump_fault = 1; };
+        PumpFault -> Manual : FaultRemoved effect { pump_fault = 0; alarm_signal = 0; error_message = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:8b4bbba0d4d1a1a590018f0ebab9d81565390fb7d436015c6158e63c08074c82`。
  - SL-10 evidence 1: `{"summary": "The NL requires a CARA Mode_Control_Algorithm hierarchy with Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault states; variables for CA_mode, software_control, pump_fault, alarm_signal, error_message, bp_reading, target_bp, flow_rate, pump_speed, built_in_switch_speed, default_flow_rate, control_voltage, sensor_buffer_bp, and log_records; caregiver InitiateAC, ChangeSetpoint, StartAC, and TerminateAC behavior; pump fault detection/removal behavior; and shared manual recovery through CA_backManual, CB_backManual, CP_backManual, and CC_backManual. The candidate preserves these required states, variables, targets, guards, and effects."}`
  - SL-10 evidence 2: `{"summary": "All nine hard SL-9 requests were accepted for the same concrete mechanism: scenarios injected CARA.Mode_Control_Algorithm.<EventName>, but the old DSL used source-local '::' events such as Manual.InitiateAC, Ask_StartAC.StartAC, AutocontrolNormal.PumpFaultDetected, and PumpFault.FaultRemoved, causing unresolved_event_path runtime errors. The candidate changes InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, FaultRemoved, CA_backManual, CB_backManual, CP_backManual, and CC_backManual to parent-relative ':' scope, directly repairing event visibility at Mode_Control_Algorithm scope."}`
  - SL-10 evidence 3: `{"summary": "Target-level scenario obligations remain represented: Manual -> Ask_StartAC on InitiateAC; Ask_StartAC self-transition on ChangeSetpoint with target_bp = target_bp + 1.0; Ask_StartAC -> AutocontrolInit on StartAC with AutocontrolInit.enter setting CA_mode = 1 and software_control = 1; TerminateAC from Ask_StartAC and AutocontrolNormal returning to Manual; AutocontrolNormal -> PumpFault on PumpFaultDetected with pump_fault = 1 and PumpFault.enter setting alarm_signal = 1, error_message = 1, software_control = 0, and CA_mode = 0; and PumpFault -> Manual on FaultRemoved resetting pump_fault, alarm_signal, and error_message."}`
  - SL-10 evidence 4: `{"summary": "Manual recovery remains consistent with the NL fallback requirement: Manual.enter clears CA_mode, software_control, and control_voltage, while Manual.during refreshes sensor_buffer_bp from bp_reading and restores flow_rate and pump_speed from default_flow_rate and built_in_switch_speed. The forced fallback transitions for CA_backManual, CB_backManual, CP_backManual, and CC_backManual still all target Manual."}`
  - SL-10 evidence 5: `{"summary": "The current candidate is not a blind repeat of the previously rejected hashes. Its hash is sha256:ce72c8d44b302dadf9c88f390efa482afacd8764f5a6e38e3daea29e5bd8651d, distinct from the previously rejected sha256:933d32f6f2b756fb04e951511407508e0121e37fcc9cd5bdb9814d0584b46108, sha256:29cc18bfbd8a369371b45238eda558b9556ee0e0ca68d1fbcf09b26de497a206, and sha256:99ae00ad0dfe4674b9646e0d8f36ebf13bd9c8c2d06a8d7a58e902ef3e2923af candidates. It specifically responds to the repeated repair_memory objection by keeping concrete initial transitions and adding explicit NL-consistent initialization effects."}`
  - SL-10 evidence 6: `{"summary": "Local deterministic evidence still reports missing_required_grounding for transition:initial:CARA_to_Mode_Control_Algorithm and transition:initial:Mode_Control_Algorithm_to_Manual with drift_risk='major', but the candidate DSL text contains concrete representations of both: 'state CARA { [*] -> Mode_Control_Algorithm effect { sensor_buffer_bp = bp_reading; }; ... }' and 'state Mode_Control_Algorithm { [*] -> Manual effect { CA_mode = 0; software_control = 0; control_voltage = 0.0; }; ... }'. These are the exact abstract grounding-map obligations identified by the local objection."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial:CARA_to_Mode_Control_Algorithm", "transition:initial:Mode_Control_Algorithm_to_Manual"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-968f96516bd` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-968f96516bd` | accept=9, reject=0 | `sl10_review` | `sha256:933d32f6f2b756fb04e951511407508e0121e37fcc9cd5bdb9814d0584b46108` | All nine failing scenarios report unresolved event paths of the form CARA.Mode_Control_Algorithm.<EventName> while the current DSL declares those events with source-local :: scope. In pyfcstm, :: makes events owned by the source state, e.g. Manual.InitiateAC, which is not the same event as Mode_Control_Algorithm.InitiateAC., The smallest safe repair is to change the NL-grounded caregiver, pump-fault, and cross-component fallback events to parent-relative : Event scope inside Mode_Control_Algorithm. This preserves all states, variables, transitions, guards, and actions while making the scenario-injected parent event paths resolvable., For initiate_change_setpoint_start_autocontrol and initiate_ac_exact_target_from_manual, Manual -> Ask_StartAC remains the target and Manual/Ask_StartAC during actions preserve sensor_buffer_bp behavior., ... +5 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-968f96516bd` | accept=9, reject=0 | `sl9_rework` | `sha256:933d32f6f2b756fb04e951511407508e0121e37fcc9cd5bdb9814d0584b46108` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling., repair_memory:SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., ... +10 |
| 4 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-968f96516bd` | accept=9, reject=0 | `sl10_review` | `sha256:29cc18bfbd8a369371b45238eda558b9556ee0e0ca68d1fbcf09b26de497a206` | All nine failing scenarios share the same expected-vs-actual gap: scenario events are injected as CARA.Mode_Control_Algorithm.<EventName>, but the current DSL declares those events with source-local :: scope, creating events such as Manual.InitiateAC or Ask_StartAC.StartAC instead of Mode_Control_Algorithm.InitiateAC or Mode_Control_Algorithm.StartAC., The smallest safe repair is to change the NL-grounded caregiver, pump fault, fault removal, and cross-component fallback events inside Mode_Control_Algorithm from :: EventName to parent-relative : EventName. This preserves all state targets, effects, guards, lifecycle actions, and variables., initiate_change_setpoint_start_autocontrol and initiate_ac_exact_target_from_manual are repaired because InitiateAC now resolves at CARA.Mode_Control_Algorithm.InitiateAC and still targets Ask_StartAC; Ask_StartAC.during refreshes sensor_buffer_bp., ... +9 |
| 5 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-968f96516bd` | accept=9, reject=0 | `sl9_rework` | `sha256:29cc18bfbd8a369371b45238eda558b9556ee0e0ca68d1fbcf09b26de497a206` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling., repair_memory:SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., ... +10 |
| 6 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-968f96516bd` | accept=9, reject=0 | `sl10_review` | `sha256:99ae00ad0dfe4674b9646e0d8f36ebf13bd9c8c2d06a8d7a58e902ef3e2923af` | All nine hard simulation failures have the same concrete mechanism: the scenarios inject CARA.Mode_Control_Algorithm.<EventName>, but the original DSL used source-local :: events such as Manual.InitiateAC, Ask_StartAC.StartAC, and AutocontrolNormal.PumpFaultDetected. In pyfcstm those are different event namespaces, causing the unresolved_event_path runtime errors., The smallest functional edit is to change the NL-grounded caregiver, pump-fault, fault-removal, and cross-component backManual events inside Mode_Control_Algorithm from source-local :: EventName to parent-relative : EventName. This keeps the events within the Mode_Control_Algorithm hierarchy without rewriting them into unrelated guards or chain-scope outside the local composite., Scenario initiate_change_setpoint_start_autocontrol and initiate_ac_exact_target_from_manual now resolve InitiateAC at CARA.Mode_Control_Algorithm.InitiateAC and still enter Ask_StartAC. Ask_StartAC.during refreshes sensor_buffer_bp from bp_reading., ... +8 |
| 7 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-968f96516bd` | accept=9, reject=0 | `sl9_rework` | `sha256:99ae00ad0dfe4674b9646e0d8f36ebf13bd9c8c2d06a8d7a58e902ef3e2923af` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling., repair_memory:SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., ... +11 |
| 8 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-968f96516bd` | accept=9, reject=0 | `sl10_review` | `sha256:ce72c8d44b302dadf9c88f390efa482afacd8764f5a6e38e3daea29e5bd8651d` | All nine accepted requests share the same expected-vs-actual gap: scenario events are injected as CARA.Mode_Control_Algorithm.<EventName>, but the current DSL declared those caregiver/pump events as source-local events such as Manual.InitiateAC, Ask_StartAC.StartAC, AutocontrolNormal.PumpFaultDetected, and PumpFault.FaultRemoved. In pyfcstm those are not the same event paths, producing the unresolved_event_path runtime errors., The smallest functional edit is to change the NL-grounded Mode_Control_Algorithm caregiver, pump-fault, fault-removal, and cross-component fallback events from source-local :: to parent-relative : within the Mode_Control_Algorithm scope. This makes InitiateAC, ChangeSetpoint, StartAC, TerminateAC, PumpFaultDetected, FaultRemoved, CA_backManual, CB_backManual, CP_backManual, and CC_backManual visible at CARA.Mode_Control_Algorithm.<EventName> without converting them to guards or inventing new dynamics., initiate_change_setpoint_start_autocontrol and initiate_ac_exact_target_from_manual are repaired because InitiateAC now resolves at CARA.Mode_Control_Algorithm.InitiateAC and still targets Ask_StartAC. Ask_StartAC.during still refreshes sensor_buffer_bp from bp_reading., ... +8 |
| 9 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-968f96516bd` | accept=9, reject=0 | `sc11_accept_then_sd2` | `sha256:ce72c8d44b302dadf9c88f390efa482afacd8764f5a6e38e3daea29e5bd8651d` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +7 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4424, 'completion_chars': 17518, 'completion_tokens': 6067, 'elapsed_seconds': 112.96310117302346, 'estimated_completion_tokens': 4380, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11037, 'first_chunk_seconds': 33.207701092003845, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12517}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3203, 'completion_chars': 12601, 'completion_tokens': 4071, 'elapsed_seconds': 76.8076419539866, 'estimated_completion_tokens': 3151, 'estimated_prompt_tokens': 14095, 'estimated_total_tokens': 17246, 'first_chunk_seconds': 18.309277563996147, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 56379, 'prompt_tokens': 13774, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 17845}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4560, 'completion_chars': 17903, 'completion_tokens': 4947, 'elapsed_seconds': 92.14610269002151, 'estimated_completion_tokens': 4476, 'estimated_prompt_tokens': 17456, 'estimated_total_tokens': 21932, 'first_chunk_seconds': 10.650972944014939, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 69821, 'prompt_tokens': 17152, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22099}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6245, 'completion_chars': 24372, 'completion_tokens': 6849, 'elapsed_seconds': 125.77952948899474, 'estimated_completion_tokens': 6093, 'estimated_prompt_tokens': 18781, 'estimated_total_tokens': 24874, 'first_chunk_seconds': 13.079571464011678, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 75123, 'prompt_tokens': 18509, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25358}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2300, 'completion_chars': 9827, 'completion_tokens': 3047, 'elapsed_seconds': 57.951781703013694, 'estimated_completion_tokens': 2457, 'estimated_prompt_tokens': 62940, 'estimated_total_tokens': 65397, 'first_chunk_seconds': 17.481913739000447, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 251759, 'prompt_tokens': 54272, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 57319}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 941, 'completion_chars': 4547, 'completion_tokens': 1150, 'elapsed_seconds': 23.860909320006613, 'estimated_completion_tokens': 1137, 'estimated_prompt_tokens': 80783, 'estimated_total_tokens': 81920, 'first_chunk_seconds': 6.807653355004732, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 323131, 'prompt_tokens': 67359, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 68509}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2753, 'completion_chars': 12015, 'completion_tokens': 3272, 'elapsed_seconds': 62.66846118698595, 'estimated_completion_tokens': 3004, 'estimated_prompt_tokens': 50787, 'estimated_total_tokens': 53791, 'first_chunk_seconds': 12.880176203005249, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 203145, 'prompt_tokens': 46165, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 49437}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 982, 'completion_chars': 4606, 'completion_tokens': 1276, 'elapsed_seconds': 25.63632884598337, 'estimated_completion_tokens': 1152, 'estimated_prompt_tokens': 45608, 'estimated_total_tokens': 46760, 'first_chunk_seconds': 8.624116561986739, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 182429, 'prompt_tokens': 41326, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 42602}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2728, 'completion_chars': 11798, 'completion_tokens': 3415, 'elapsed_seconds': 65.1552163180022, 'estimated_completion_tokens': 2950, 'estimated_prompt_tokens': 60428, 'estimated_total_tokens': 63378, 'first_chunk_seconds': 17.75253632699605, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 241709, 'prompt_tokens': 56162, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 59577}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1107, 'completion_chars': 4921, 'completion_tokens': 1490, 'elapsed_seconds': 29.58668685500743, 'estimated_completion_tokens': 1231, 'estimated_prompt_tokens': 54383, 'estimated_total_tokens': 55614, 'first_chunk_seconds': 9.550779699988198, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 217532, 'prompt_tokens': 50386, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 51876}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2993, 'completion_chars': 12961, 'completion_tokens': 3512, 'elapsed_seconds': 66.86945113399997, 'estimated_completion_tokens': 3241, 'estimated_prompt_tokens': 68354, 'estimated_total_tokens': 71595, 'first_chunk_seconds': 12.388989627012052, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 273415, 'prompt_tokens': 64492, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 68004}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1350, 'completion_chars': 5917, 'completion_tokens': 1680, 'elapsed_seconds': 33.53568747098325, 'estimated_completion_tokens': 1480, 'estimated_prompt_tokens': 62436, 'estimated_total_tokens': 63916, 'first_chunk_seconds': 9.146342734980863, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 249743, 'prompt_tokens': 58591, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 60271}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 7062, 'completion_chars': 27628, 'completion_tokens': 8099, 'elapsed_seconds': 148.3700636520225, 'estimated_completion_tokens': 6907, 'estimated_prompt_tokens': 23505, 'estimated_total_tokens': 30412, 'first_chunk_seconds': 23.063106556015555, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 94017, 'prompt_tokens': 23562, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 31661}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5251, 'completion_chars': 20298, 'completion_tokens': 6288, 'elapsed_seconds': 115.75599529600004, 'estimated_completion_tokens': 5075, 'estimated_prompt_tokens': 24319, 'estimated_total_tokens': 29394, 'first_chunk_seconds': 22.900888637988828, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 97273, 'prompt_tokens': 24379, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 30667}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1692, 'completion_chars': 7985, 'completion_tokens': 2445, 'elapsed_seconds': 46.23420785900089, 'estimated_completion_tokens': 1997, 'estimated_prompt_tokens': 21673, 'estimated_total_tokens': 23670, 'first_chunk_seconds': 15.526182955974946, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 86691, 'prompt_tokens': 21906, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24351}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success_but_weak_oracle_ineligible`。
- required stages executed：`36/16`，missing=`<none>`。
- repairs：`1/4` accepted；scenario_history=`6`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
