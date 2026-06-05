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
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `min_sl10_rework_attempts=1`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `7cc8559b58d7e3df3fc5819d45114d325d207120` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:7b8ce3144e97ba307c15ae5a3bb922da8b77f89d1c0c60869f90bf6ba05397d1", "iteration": 1, "matching_repair_history_indices": [1], "repair_history_index": 1, "selected_source_stage": "SL-7", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 337946, 'completion_tokens': 57791, 'total_tokens': 395737, 'estimated_prompt_tokens': 353691, 'estimated_completion_tokens': 47417, 'estimated_total_tokens': 401108, 'prompt_chars': 1414749, 'completion_chars': 189654, 'n_calls': 14, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`1090.605s` |
| run record | [`pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:001ce94b2862f9cadc7fb08038f5cbe6c14669b26fa9bf63a609f7fdd75aaeff` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `67` |
| `langgraph_node_trace_hash` | `sha256:83e71f0e0d6e2a3b9e06e905e23adb9fb5075d8b1e4d8f990af084ab9c97302d` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `67` |

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
def int log_entry_count = 0;
def float patient_bp = 0.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_buffer_bp = 0.0;
def float flow_rate = 0.0;
def float manual_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def float infusion_rate_log = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        >> during before {
            shared_buffer_bp = patient_bp;
        }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_signal = 0;
                pump_fault = 0;
            }
            during {
                pump_speed = built_in_switch_speed;
                flow_rate = manual_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                pump_fault = 0;
            }
        }

        state Autocontrol {
            during {
                if [pump_fault == 0] {
                    flow_rate = target_bp - patient_bp;
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    infusion_rate_log = flow_rate;
                    log_entry_count = log_entry_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
            target_bp = requested_target_bp;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> Manual : TerminateAC;
        AutocontrolInit -> Autocontrol;
        Autocontrol -> PumpFault : if [pump_fault != 0];
        Autocontrol -> Manual : TerminateAC;
        Autocontrol -> PumpFault :: PumpFaultOccurred effect {
            pump_fault = 1;
        };
        PumpFault -> Manual :: FaultRemoved;
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=14097 | 生成初始 DSL 与 grounding seeds | initial len=2633 | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=68955 | LLM per-request accept/reject + repair | candidate len=2633,2690 | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=70908 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=57428 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=68955 | LLM per-request accept/reject + repair | candidate len=2633,2690 | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=70908 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=7, tokens=184349 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=57428 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b2-clean-7cc8559-9142f20d.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T17:34:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T17:34:06Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T17:34:06Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T17:34:06Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T17:36:27Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T17:36:27Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2633,hash=sha256:e364b823420f |
| 7 | `2026-06-05T17:36:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T17:36:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T17:36:27Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:e364b823420f00d9965b304c24f127cbd463153e96248cd7351fc9e86f5949e9 |
| 10 | `2026-06-05T17:36:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T17:36:27Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2633,hash=sha256:e364b823420f, current_hash=sha256:e364b823420f00d9965b304c24f127cbd463153e96248cd7351fc9e86f5949e9 |
| 12 | `2026-06-05T17:36:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T17:36:27Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T17:36:27Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T17:36:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T17:36:27Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T17:36:28Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T17:36:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T17:36:28Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T17:36:28Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T17:36:28Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T17:36:28Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T17:37:59Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T17:37:59Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T17:38:00Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T17:38:00Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T17:38:00Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T17:39:24Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T17:39:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T17:39:24Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T17:39:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T17:39:24Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T17:41:03Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T17:41:03Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T17:41:04Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T17:41:04Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T17:41:04Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T17:41:04Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T17:41:04Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 42 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T17:41:04Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 12, "n_scenarios_passed": 11, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 44 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 47 | `2026-06-05T17:41:04Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 12, "n_scenarios_passed": 11, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2633,hash=sha256:e364b823420f |
| 48 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 49 | `2026-06-05T17:41:04Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 50 | `2026-06-05T17:41:04Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 51 | `2026-06-05T17:41:04Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 52 | `2026-06-05T17:41:04Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2633,hash=sha256:e364b823420f |
| 53 | `2026-06-05T17:41:34Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 54 | `2026-06-05T17:41:34Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-a6820d936f"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2633,hash=sha256:f04099ce732a |
| 55 | `2026-06-05T17:41:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 56 | `2026-06-05T17:41:35Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 57 | `2026-06-05T17:41:35Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:f04099ce732a370989d587eccf7681da3e383b00686d0aca51dab7365d5c8563 |
| 58 | `2026-06-05T17:41:54Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 59 | `2026-06-05T17:41:54Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 60 | `2026-06-05T17:41:54Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 61 | `2026-06-05T17:41:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 62 | `2026-06-05T17:41:54Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2633,hash=sha256:f04099ce732a |
| 63 | `2026-06-05T17:41:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 64 | `2026-06-05T17:41:55Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:f04099ce732a370989d587eccf7681da3e383b00686d0aca51dab7365d5c8563 |
| 65 | `2026-06-05T17:41:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 66 | `2026-06-05T17:41:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 67 | `2026-06-05T17:41:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 68 | `2026-06-05T17:41:55Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:f04099ce732a370989d587eccf7681da3e383b00686d0aca51dab7365d5c8563 |
| 69 | `2026-06-05T17:41:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 70 | `2026-06-05T17:41:55Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=2633,hash=sha256:f04099ce732a, current_hash=sha256:f04099ce732a370989d587eccf7681da3e383b00686d0aca51dab7365d5c8563 |
| 71 | `2026-06-05T17:41:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 72 | `2026-06-05T17:41:55Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 73 | `2026-06-05T17:41:55Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 74 | `2026-06-05T17:41:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 75 | `2026-06-05T17:41:55Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 76 | `2026-06-05T17:41:55Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 77 | `2026-06-05T17:41:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 78 | `2026-06-05T17:41:55Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 79 | `2026-06-05T17:41:55Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-5A", "ok": true, "status": "StageStatus.OK"} | <none> |
| 80 | `2026-06-05T17:41:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
- ……另有 `93` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-6` | yes | fixbatch-0-sha256-8bd9f01c6cc / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SL-7` | yes | fixbatch-1-sha256-02af10fd183 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| `default_init_enters_manual_and_uses_manual_inputs` | default-init: first empty cycle dispatches to Manual, stores BP in the shared buffer, and drives pump speed/flow from ma...<truncated 12 chars> | ✅ | ✅ | ✅ |
| `initiate_change_setpoint_start_and_enter_autocontrol` | default-init: caregiver initiates AC, changes the Ask_StartAC setpoint, presses StartAC, then the init state advances to...<truncated 20 chars> | ✅ | ✅ | ✅ |
| `terminate_from_ask_and_init_returns_manual` | explicit-hot-start: TerminateAC returns Ask_StartAC to Manual, and after re-entering AutocontrolInit it also returns to ...<truncated 7 chars> | ❌ | ✅ | ✅ |
| `autocontrol_fault_alarms_then_fault_removed_manual` | explicit-hot-start: normal Autocontrol computes/logs flow while fault-free, PumpFaultOccurred enters PumpFault with alar...<truncated 57 chars> | ✅ | ✅ | ✅ |
| `autocontrol_with_existing_complication_does_not_control_flow` | explicit-hot-start: when Autocontrol already has a pump-operation complication, a no-event cycle must take the safety re...<truncated 54 chars> | ✅ | ✅ | ✅ |
| `terminate_from_autocontrol_returns_manual` | explicit-hot-start: caregiver TerminateAC from normal Autocontrol releases algorithmic control and returns to Manual ope...<truncated 7 chars> | ✅ | ✅ | ✅ |
| `forced_ca_and_cb_back_manual_from_distinct_states` | explicit-hot-start: CA_backManual from Autocontrol and CB_backManual from Ask_StartAC both force the shared recovery tar...<truncated 11 chars> | ✅ | ✅ | ✅ |
| `forced_cp_and_cc_back_manual_from_fault_and_init` | explicit-hot-start: CP_backManual from PumpFault and CC_backManual from AutocontrolInit both force Manual as the recover...<truncated 9 chars> | ✅ | ✅ | ✅ |
| `change_setpoint_effect_value_direct_probe` | explicit-hot-start: ChangeSetpoint in Ask_StartAC must assign target_bp exactly from requested_target_bp, exposing missi...<truncated 37 chars> | ✅ | ✅ | ✅ |
| `changed_setpoint_drives_autocontrol_flow` | explicit-hot-start: after ChangeSetpoint then StartAC, Autocontrol must compute flow from the changed target, catching m...<truncated 67 chars> | ✅ | ✅ | ✅ |
| `startac_control_enable_effect_value_probe` | explicit-hot-start: StartAC entering AutocontrolInit must set algorithmic-control outputs exactly, exposing missing or w...<truncated 36 chars> | ✅ | ✅ | ✅ |
| `pump_fault_entry_effect_value_probe` | explicit-hot-start: PumpFaultOccurred from Autocontrol must assert the fault/alarm and release software control exactly,...<truncated 51 chars> | ✅ | ✅ | ✅ |
| `fault_removed_manual_recovery_exact_reset_probe` | explicit-hot-start: FaultRemoved from PumpFault must land in Manual with fault/alarm cleared and manual outputs restored...<truncated 56 chars> | ⚪ | ✅ | ✅ |
| `forced_backmanual_exact_reset_from_dirty_autocontrol` | explicit-hot-start: a backManual fallback from dirty Autocontrol must force Manual and assign the exact shared recovery ...<truncated 59 chars> | ⚪ | ✅ | ✅ |
| `change_setpoint_wrong_constant_sentinel_probe` | explicit-hot-start: ChangeSetpoint must copy a non-default requested target exactly, so missing effect or wrong constant...<truncated 58 chars> | ⚪ | ⚪ | ✅ |
| `pumpfault_existing_complication_guard_entry_effect_probe` | explicit-hot-start: an already-present pump fault in Autocontrol must enter PumpFault without an event and set alarm/rel...<truncated 54 chars> | ⚪ | ⚪ | ✅ |
| `initiateac_ask_entry_exact_reset_probe` | explicit-hot-start: InitiateAC from dirty Manual must enter Ask_StartAC with CA_mode/software_control exactly reset, exp...<truncated 46 chars> | ⚪ | ⚪ | ✅ |
| `terminate_from_dirty_init_manual_reset_probe` | explicit-hot-start: TerminateAC from dirty AutocontrolInit must enter Manual and clear fault/alarm/control outputs exact...<truncated 58 chars> | ⚪ | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_enters_manual_and_uses_manual_inputs` — default-init: first empty cycle dispatches to Manual, stores BP in the shared buffer, and drives pump speed/flow from manual inputs.</summary>

| Field | Value |
|---|---|
| description | default-init: first empty cycle dispatches to Manual, stores BP in the shared buffer, and drives pump speed/flow from manual inputs. |
| initial_state | `<default-init>` |
| initial_vars | `{"built_in_switch_speed": 3.5, "manual_flow_rate": 7.2, "patient_bp": 85.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_after_initial_dispatch` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 7.2, "pump_fault": 0, "pump_speed": 3.5, "shared_buffer_bp": 85.0, "software_control": 0}` |

</details>

<details><summary>`initiate_change_setpoint_start_and_enter_autocontrol` — default-init: caregiver initiates AC, changes the Ask_StartAC setpoint, presses StartAC, then the init state advances to normal Autocontrol.</summary>

| Field | Value |
|---|---|
| description | default-init: caregiver initiates AC, changes the Ask_StartAC setpoint, presses StartAC, then the init state advances to normal Autocontrol. |
| initial_state | `<default-init>` |
| initial_vars | `{"patient_bp": 90.0, "requested_target_bp": 110.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_manual_ready` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "software_control": 0}` |
| 1 `initiate_enters_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 0, "shared_buffer_bp": 90.0, "software_control": 0}` |
| 2 `change_setpoint_updates_target` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 110.0}` |
| 3 `startac_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "pump_fault": 0, "software_control": 1}` |
| 4 `autocontrol_init_advances_to_autocontrol` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Autocontrol` | `{"control_voltage": 20.0, "flow_rate": 20.0, "infusion_rate_log": 20.0, "log_entry_count": 1, "pump_speed": 20.0, "shared_buffer_bp": 90.0}` |

</details>

<details><summary>`terminate_from_ask_and_init_returns_manual` — explicit-hot-start: TerminateAC returns Ask_StartAC to Manual, and after re-entering AutocontrolInit it also returns to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: TerminateAC returns Ask_StartAC to Manual, and after re-entering AutocontrolInit it also returns to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"built_in_switch_speed": 2.0, "manual_flow_rate": 4.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_from_ask_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 4.0, "pump_speed": 2.0, "software_control": 0}` |
| 1 `initiate_again_to_ask` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 0, "software_control": 0}` |
| 2 `startac_to_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "software_control": 1}` |
| 3 `terminate_from_init_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 4.0, "pump_speed": 2.0, "software_control": 0}` |

</details>

<details><summary>`autocontrol_fault_alarms_then_fault_removed_manual` — explicit-hot-start: normal Autocontrol computes/logs flow while fault-free, PumpFaultOccurred enters PumpFault with alarm and released control, then FaultRemove...<truncated 17 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: normal Autocontrol computes/logs flow while fault-free, PumpFaultOccurred enters PumpFault with alarm and released control, then FaultRemoved returns Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.Autocontrol` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "built_in_switch_speed": 1.5, "log_entry_count": 0, "manual_flow_rate": 6.0, "patient_bp": 95.0, "pump_fault": 0, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `normal_autocontrol_computes_and_logs` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Autocontrol` | `{"control_voltage": 25.0, "flow_rate": 25.0, "infusion_rate_log": 25.0, "log_entry_count": 1, "pump_speed": 25.0, "shared_buffer_bp": 95.0}` |
| 1 `pump_fault_enters_fault_state` | `0` | `["CARA.Mode_Control_Algorithm.Autocontrol.PumpFaultOccurred"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "pump_fault": 1, "software_control": 0}` |
| 2 `fault_removed_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 6.0, "pump_fault": 0, "pump_speed": 1.5, "software_control": 0}` |

</details>

<details><summary>`autocontrol_with_existing_complication_does_not_control_flow` — explicit-hot-start: when Autocontrol already has a pump-operation complication, a no-event cycle must take the safety recovery path to PumpFault and release sof...<truncated 14 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: when Autocontrol already has a pump-operation complication, a no-event cycle must take the safety recovery path to PumpFault and release software control. |
| initial_state | `CARA.Mode_Control_Algorithm.Autocontrol` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "control_voltage": 5.0, "flow_rate": 5.0, "infusion_rate_log": 5.0, "log_entry_count": 2, "patient_bp": 70.0, "pump_fault": 1, "pump_speed": 5.0, "software_control": 1, "target_bp": 130.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `existing_fault_enters_pumpfault_without_control_update` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "control_voltage": 5.0, "flow_rate": 5.0, "infusion_rate_log": 5.0, "log_entry_count": 2, "pump_fault": 1, "pump_speed": 5.0, "shared_buffer_bp": 70.0, "software_control": 0}` |

</details>

<details><summary>`terminate_from_autocontrol_returns_manual` — explicit-hot-start: caregiver TerminateAC from normal Autocontrol releases algorithmic control and returns to Manual operation.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: caregiver TerminateAC from normal Autocontrol releases algorithmic control and returns to Manual operation. |
| initial_state | `CARA.Mode_Control_Algorithm.Autocontrol` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "built_in_switch_speed": 2.5, "manual_flow_rate": 8.0, "pump_fault": 0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_from_autocontrol_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 8.0, "pump_fault": 0, "pump_speed": 2.5, "software_control": 0}` |

</details>

<details><summary>`forced_ca_and_cb_back_manual_from_distinct_states` — explicit-hot-start: CA_backManual from Autocontrol and CB_backManual from Ask_StartAC both force the shared recovery target Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CA_backManual from Autocontrol and CB_backManual from Ask_StartAC both force the shared recovery target Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.Autocontrol` |
| initial_vars | `{"CA_mode": 1, "built_in_switch_speed": 3.0, "manual_flow_rate": 9.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_from_autocontrol` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 9.0, "pump_speed": 3.0, "software_control": 0}` |
| 1 `initiate_to_ask_for_second_forced_probe` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 0, "software_control": 0}` |
| 2 `cb_backmanual_from_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 9.0, "pump_speed": 3.0, "software_control": 0}` |

</details>

<details><summary>`forced_cp_and_cc_back_manual_from_fault_and_init` — explicit-hot-start: CP_backManual from PumpFault and CC_backManual from AutocontrolInit both force Manual as the recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CP_backManual from PumpFault and CC_backManual from AutocontrolInit both force Manual as the recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "built_in_switch_speed": 4.0, "manual_flow_rate": 10.0, "pump_fault": 1, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_from_pumpfault` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 10.0, "pump_fault": 0, "pump_speed": 4.0, "software_control": 0}` |
| 1 `initiate_to_ask` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 0, "software_control": 0}` |
| 2 `startac_to_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "pump_fault": 0, "software_control": 1}` |
| 3 `cc_backmanual_from_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 10.0, "pump_fault": 0, "pump_speed": 4.0, "software_control": 0}` |

</details>

<details><summary>`change_setpoint_effect_value_direct_probe` — explicit-hot-start: ChangeSetpoint in Ask_StartAC must assign target_bp exactly from requested_target_bp, exposing missing or wrong transition effect values.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: ChangeSetpoint in Ask_StartAC must assign target_bp exactly from requested_target_bp, exposing missing or wrong transition effect values. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"patient_bp": 100.0, "requested_target_bp": 125.0, "target_bp": 80.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `change_setpoint_assigns_requested_value` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 0, "shared_buffer_bp": 100.0, "software_control": 0, "target_bp": 125.0}` |

</details>

<details><summary>`changed_setpoint_drives_autocontrol_flow` — explicit-hot-start: after ChangeSetpoint then StartAC, Autocontrol must compute flow from the changed target, catching missing or wrong ChangeSetpoint effects t...<truncated 27 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: after ChangeSetpoint then StartAC, Autocontrol must compute flow from the changed target, catching missing or wrong ChangeSetpoint effects that only appear downstream. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"log_entry_count": 0, "patient_bp": 100.0, "requested_target_bp": 125.0, "target_bp": 80.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `setpoint_changed_before_start` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 125.0}` |
| 1 `start_preserves_changed_target` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "software_control": 1, "target_bp": 125.0}` |
| 2 `autocontrol_uses_changed_target_for_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Autocontrol` | `{"control_voltage": 25.0, "flow_rate": 25.0, "infusion_rate_log": 25.0, "log_entry_count": 1, "pump_speed": 25.0, "shared_buffer_bp": 100.0}` |

</details>

<details><summary>`startac_control_enable_effect_value_probe` — explicit-hot-start: StartAC entering AutocontrolInit must set algorithmic-control outputs exactly, exposing missing or wrong assignment effects on AC entry.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: StartAC entering AutocontrolInit must set algorithmic-control outputs exactly, exposing missing or wrong assignment effects on AC entry. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 99, "alarm_signal": 99, "patient_bp": 88.0, "pump_fault": 99, "software_control": 99}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `startac_sets_control_enabled_exactly` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "pump_fault": 0, "shared_buffer_bp": 88.0, "software_control": 1}` |

</details>

<details><summary>`pump_fault_entry_effect_value_probe` — explicit-hot-start: PumpFaultOccurred from Autocontrol must assert the fault/alarm and release software control exactly, exposing missing or wrong fault-entry a...<truncated 11 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: PumpFaultOccurred from Autocontrol must assert the fault/alarm and release software control exactly, exposing missing or wrong fault-entry assignments. |
| initial_state | `CARA.Mode_Control_Algorithm.Autocontrol` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "patient_bp": 105.0, "pump_fault": 0, "software_control": 1, "target_bp": 130.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_entry_assigns_alarm_and_release_values` | `0` | `["CARA.Mode_Control_Algorithm.Autocontrol.PumpFaultOccurred"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "pump_fault": 1, "shared_buffer_bp": 105.0, "software_control": 0}` |

</details>

<details><summary>`fault_removed_manual_recovery_exact_reset_probe` — explicit-hot-start: FaultRemoved from PumpFault must land in Manual with fault/alarm cleared and manual outputs restored, exposing missing or wrong recovery ass...<truncated 16 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: FaultRemoved from PumpFault must land in Manual with fault/alarm cleared and manual outputs restored, exposing missing or wrong recovery assignment effects. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "built_in_switch_speed": 6.5, "flow_rate": 99.0, "manual_flow_rate": 11.5, "patient_bp": 77.0, "pump_fault": 1, "pump_speed": 99.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_removed_clears_fault_and_restores_manual_exactly` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 11.5, "pump_fault": 0, "pump_speed": 6.5, "shared_buffer_bp": 77.0, "software_control": 0}` |

</details>

<details><summary>`forced_backmanual_exact_reset_from_dirty_autocontrol` — explicit-hot-start: a backManual fallback from dirty Autocontrol must force Manual and assign the exact shared recovery outputs, exposing missing or wrong force...<truncated 19 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: a backManual fallback from dirty Autocontrol must force Manual and assign the exact shared recovery outputs, exposing missing or wrong forced-recovery effects. |
| initial_state | `CARA.Mode_Control_Algorithm.Autocontrol` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "built_in_switch_speed": 7.5, "flow_rate": 88.0, "manual_flow_rate": 12.5, "patient_bp": 66.0, "pump_fault": 1, "pump_speed": 88.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_clears_dirty_values_exactly` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 12.5, "pump_fault": 0, "pump_speed": 7.5, "shared_buffer_bp": 66.0, "software_control": 0}` |

</details>

<details><summary>`change_setpoint_wrong_constant_sentinel_probe` — explicit-hot-start: ChangeSetpoint must copy a non-default requested target exactly, so missing effect or wrong constant-plus-100 mutations leave target_bp inco...<truncated 18 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: ChangeSetpoint must copy a non-default requested target exactly, so missing effect or wrong constant-plus-100 mutations leave target_bp incorrect immediately. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"patient_bp": 91.0, "requested_target_bp": 135.0, "target_bp": 35.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `change_setpoint_copies_135_not_old_or_wrong_constant` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 0, "shared_buffer_bp": 91.0, "software_control": 0, "target_bp": 135.0}` |

</details>

<details><summary>`pumpfault_existing_complication_guard_entry_effect_probe` — explicit-hot-start: an already-present pump fault in Autocontrol must enter PumpFault without an event and set alarm/release values, exposing missing safety rec...<truncated 14 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: an already-present pump fault in Autocontrol must enter PumpFault without an event and set alarm/release values, exposing missing safety recovery effects. |
| initial_state | `CARA.Mode_Control_Algorithm.Autocontrol` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "control_voltage": 17.0, "flow_rate": 17.0, "infusion_rate_log": 17.0, "log_entry_count": 3, "patient_bp": 102.0, "pump_fault": 1, "pump_speed": 17.0, "software_control": 1, "target_bp": 140.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `existing_complication_forces_fault_alarm_and_release` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "control_voltage": 17.0, "flow_rate": 17.0, "infusion_rate_log": 17.0, "log_entry_count": 3, "pump_fault": 1, "pump_speed": 17.0, "shared_buffer_bp": 102.0, "software_control": 0}` |

</details>

<details><summary>`initiateac_ask_entry_exact_reset_probe` — explicit-hot-start: InitiateAC from dirty Manual must enter Ask_StartAC with CA_mode/software_control exactly reset, exposing missing or wrong entry-effect cons...<truncated 6 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: InitiateAC from dirty Manual must enter Ask_StartAC with CA_mode/software_control exactly reset, exposing missing or wrong entry-effect constants. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"CA_mode": 55, "alarm_signal": 0, "built_in_switch_speed": 4.5, "manual_flow_rate": 8.5, "patient_bp": 89.0, "pump_fault": 0, "software_control": 66}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiateac_resets_ask_control_flags_exactly` | `0` | `["CARA.Mode_Control_Algorithm.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 0, "shared_buffer_bp": 89.0, "software_control": 0}` |

</details>

<details><summary>`terminate_from_dirty_init_manual_reset_probe` — explicit-hot-start: TerminateAC from dirty AutocontrolInit must enter Manual and clear fault/alarm/control outputs exactly, exposing missing or wrong recovery a...<truncated 18 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: TerminateAC from dirty AutocontrolInit must enter Manual and clear fault/alarm/control outputs exactly, exposing missing or wrong recovery assignment effects. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 88, "built_in_switch_speed": 5.5, "flow_rate": 99.0, "manual_flow_rate": 13.5, "patient_bp": 92.0, "pump_fault": 77, "pump_speed": 99.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_from_dirty_init_clears_and_restores_manual` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 13.5, "pump_fault": 0, "pump_speed": 5.5, "shared_buffer_bp": 92.0, "software_control": 0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | terminate_from_ask_and_init_returns_manual | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:f04099ce732a370989d587eccf7681da3e383b00686d0aca51dab7365d5c8563` |
| 2 | `1` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:7b8ce3144e97ba307c15ae5a3bb922da8b77f89d1c0c60869f90bf6ba05397d1` |

<details><summary>Repair 1 / iteration `0` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`terminate_from_ask_and_init_returns_manual`。
- before_dsl_hash：`sha256:e364b823420f00d9965b304c24f127cbd463153e96248cd7351fc9e86f5949e9`；candidate_dsl_hash：`sha256:f04099ce732a370989d587eccf7681da3e383b00686d0aca51dab7365d5c8563`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-8bd9f01c6cc`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-a6820d936f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: TerminateAC returns Ask_StartAC to Manual, and after re-entering AutocontrolInit it also returns to Manual.', 'name': 'terminate_from_ask_and_init_returns_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start: TerminateAC returns Ask_StartAC to Manual, and after re-entering AutocontrolInit it also returns to Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Autocontrol', 'actual_vars_focus': {'CA_mode': 1, 'flow_rate': 100.0, 'pump_speed': 100.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'flow_rate': 4.0, 'pump_speed': 2.0, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 3, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 100.0, 'expected': 4.0}, 'pump_speed': {'actual': 100.0, 'expected': 2.0}, 'software_control': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'initial_vars': {'built_in_switch_speed': 2.0, 'manual_flow_rate': 4.0}, 'scenario_name': 'terminate_from_ask_and_init_returns_manual', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'built_in_switch_speed': 2.0, 'control_voltage': 0.0, 'flow_rate': 4.0, 'infusion_rate_log': 0.0, 'log_entry_count': 0, 'manual_flow_rate': 4.0, 'patient_bp': 0.0, 'pump_fault': 0, 'pump_speed': 2.0, 'requested_target_bp': 100.0, 'shared_buffer_bp': 0.0, 'software_control': 0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'terminate_from_ask_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 0, 'built_in_switch_speed': 2.0, 'control_voltage': 0.0, 'flow_rate': 4.0, 'infusion_rate_log': 0.0, 'log_entry_count': 0, 'manual_flow_rate': 4.0, 'patient_bp': 0.0, 'pump_fault': 0, 'pump_speed': 2.0, 'requested_target_bp': 100.0, 'shared_buffer_bp': 0.0, 'software_control': 0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'initiate_again_to_ask', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'built_in_switch_speed': 2.0, 'control_voltage': 0.0, 'flow_rate': 4.0, 'infusion_rate_log': 0.0, 'log_entry_count': 0, 'manual_flow_rate': 4.0, 'patient_bp': 0.0, 'pump_fault': 0, 'pump_speed': 2.0, 'requested_target_bp': 100.0, 'shared_buffer_bp': 0.0, 'software_control': 1, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'startac_to_init', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Autocontrol', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'built_in_switch_speed': 2.0, 'control_voltage': 100.0, 'flow_rate': 100.0, 'infusion_rate_log': 100.0, 'log_entry_count': 1, 'manual_flow_rate': 4.0, 'patient_bp': 0.0, 'pump_fault': 0, 'pump_speed': 100.0, 'requested_target_bp': 100.0, 'shared_buffer_bp': 0.0, 'software_control': 1, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 3, 'step_name': 'terminate_from_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 100.0, 'expected': 4.0}, 'pump_speed': {'actual': 100.0, 'expected': 2.0}, 'software_control': {'actual': 1, 'expected': 0}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:CARA, state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:Autocontrol, state:PumpFault, variable:CA_mode, variable:patient_bp, variable:target_bp, variable:requested_target_bp, variable:shared_buffer_bp, ... +44`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2633`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-a6820d936f` | `accept` | ❌ | ❌ | The failing scenario terminate_from_ask_and_init_returns_manual shows that when TerminateAC is injected while AutocontrolInit is active, the unconditional AutocontrolInit -> Autocontrol transition fires instead of the TerminateAC transition to Manual. This is a local transition-priority/order issue, so the smallest safe edit is to place AutocontrolInit -> Ma...<truncated 211 chars> |
- repair_rationale：Accepted the hard SD-6 simulation request because the evidence provides a precise failing step and a minimal local repair.；For scenario terminate_from_ask_and_init_returns_manual, failing step terminate_from_init_to_manual expected state CARA.Mode_Control_Algorithm.Manual with CA_mode=0, software_control=0, pump_speed=2.0, and flow_rate=4.0, but the actual stat...<truncated 92 chars>；The cause is that AutocontrolInit had an unconditional transition to Autocontrol declared before the TerminateAC transition. Reordering lets the TerminateAC event be considered before the fallback progression to Autocontrol.；Entering Manual preserves the existing Manual enter/during actions, so CA_mode and software_control are cleared and pump_speed/flow_rate return to built_in_switch_speed/manual_flow_rate, matching the failing step expectations.；Previously passing scenario steps are preserved: Ask_StartAC still terminates to Manual, InitiateAC still reaches Ask_StartAC, StartAC still reaches AutocontrolInit, and the unconditional AutocontrolInit -> Autocontrol transition remains fo...<truncated 65 chars>
- diff_summary：`{"summary": "Moved `AutocontrolInit -> Manual : TerminateAC;` before `AutocontrolInit -> Autocontrol;` so TerminateAC from AutocontrolInit wins over the unconditional progression to Autocontrol."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int log_entry_count = 0;
def float patient_bp = 0.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_buffer_bp = 0.0;
def float flow_rate = 0.0;
def float manual_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def float infusion_rate_log = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        >> during before {
            shared_buffer_bp = patient_bp;
        }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_signal = 0;
                pump_fault = 0;
            }
            during {
                pump_speed = built_in_switch_speed;
                flow_rate = manual_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                pump_fault = 0;
            }
        }

        state Autocontrol {
            during {
                if [pump_fault == 0] {
                    flow_rate = target_bp - patient_bp;
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    infusion_rate_log = flow_rate;
                    log_entry_count = log_entry_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
            target_bp = requested_target_bp;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> Manual : TerminateAC;
        AutocontrolInit -> Autocontrol;
        Autocontrol -> Manual : TerminateAC;
        Autocontrol -> PumpFault :: PumpFaultOccurred effect {
            pump_fault = 1;
        };
        PumpFault -> Manual :: FaultRemoved;
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -84,9 +84,9 @@
             target_bp = requested_target_bp;
         };
         Ask_StartAC -> AutocontrolInit :: StartAC;
-        AutocontrolInit -> Autocontrol;
         Ask_StartAC -> Manual : TerminateAC;
         AutocontrolInit -> Manual : TerminateAC;
+        AutocontrolInit -> Autocontrol;
         Autocontrol -> Manual : TerminateAC;
         Autocontrol -> PumpFault :: PumpFaultOccurred effect {
             pump_fault = 1;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:fe9f76733a1fe47f8a8f392874764962de5e8e4af232d1b873b0dd1db0aff3f8`。
  - SL-10 evidence 1: `{"summary": "The hard SD-6 simulation request was for scenario terminate_from_ask_and_init_returns_manual, failing at step terminate_from_init_to_manual: TerminateAC from AutocontrolInit was expected to enter Manual with CA_mode=0, software_control=0, pump_speed=2.0, and flow_rate=4.0, but the old DSL advanced via the unconditional AutocontrolInit -> Autocontrol transition and produced CA_mode=1, software_control=1, pump_speed=100.0, and flow_rate=100.0. The candidate moves AutocontrolInit -> Manual : TerminateAC before AutocontrolInit -> Autocontrol, so the event-specific termination transition has priority over the unconditional progression. Entering Manual preserves the existing Manual en...<truncated 129 chars>`
  - SL-10 evidence 2: `{"summary": "The SL-9 decision accepted the request with the same minimal transition-order rationale, and the FixLog records no prior repair_memory objections or repeated-candidate warnings. The diff is limited to reordering the AutocontrolInit TerminateAC transition before the unconditional AutocontrolInit-to-Autocontrol transition; no grounded states, variables, events, guards, or actions are deleted."}`
  - SL-10 evidence 3: `{"summary": "The candidate continues to satisfy the NL-required structure and obligations: CARA and Mode_Control_Algorithm remain, Manual/Ask_StartAC/AutocontrolInit/Autocontrol/PumpFault remain, StartAC still enters AutocontrolInit, ChangeSetpoint still updates target_bp from requested_target_bp, TerminateAC remains available from Ask_StartAC, AutocontrolInit, and Autocontrol, pump fault handling and FaultRemoved recovery remain, and CA/CB/CP/CC_backManual forced transitions still target Manual."}`
  - SL-10 evidence 4: `{"summary": "The candidate also preserves the NL-required data/control actions: shared_buffer_bp is updated from patient_bp in the hierarchy-wide during-before block, Manual during sets pump_speed from built_in_switch_speed and flow_rate from manual_flow_rate, Autocontrol during is guarded by pump_fault == 0 and computes flow_rate inversely from patient_bp, then sets control_voltage, pump_speed, infusion_rate_log, and log_entry_count, and PumpFault enter activates alarm_signal and releases software_control."}`
  - SL-10 evidence 5: `{"candidate_dsl_hash": "sha256:f04099ce732a370989d587eccf7681da3e383b00686d0aca51dab7365d5c8563", "covered_local_objection_kinds": ["missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:dd1cf30db27c1d4d44b9688970a90e89ae2f1cac2e177ca963688a4cac22788c", "local_override_rationale_count": 3, "local_override_rationale_hash": "sha256:f5ab6231be5ab114a2e1c6971658440e6688bc6b1b75be939c3683d0e1abc45d", "local_rejection_evidence_hash": "sha256:66947cbf3693be9200213b4f6123269e2b050e1311fdeb4e56c76931f15522b6", "local_rejection_reason": "missing_required_grounding", "missing_local_objection_kinds": [], "policy": "SL-10 may override conservative ...<truncated 296 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial_root", "transition:initial_mode_control", "guard:Autocontrol_no_pump_fault", "action:buffer_bp"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `1` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:f04099ce732a370989d587eccf7681da3e383b00686d0aca51dab7365d5c8563`；candidate_dsl_hash：`sha256:7b8ce3144e97ba307c15ae5a3bb922da8b77f89d1c0c60869f90bf6ba05397d1`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Autocontrol can remain active with pump_fault=1 without alarm activation, control release, or transition to a safe/diagnostic fault state.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-02af10fd183`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sl7-0-3096823055` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL Autocontrol.during has if [pump_fault == 0] for normal control but no else branch for pump_fault != 0.', 'Fault response is only on event PumpFaultOccurred; there is no guarded transition from Autocontrol when pump_fault == 1.', 'sim_summary passing scenario "autocontrol_with_existing_complication_does_not_control_flow" shows Autocontrol with pump_fault=1, alarm_signal=0, software_control=1, and stale pump/control outputs.', 'NL requires pump fault alarm behavior and software control release when CARA was controlling the pump.'], 'severity': 'major', 'summary': 'Autocontrol can remain active with pump_fault=1 without alarm activation, control release, or transition to a safe/diagnostic fault state.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:CARA, state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:Autocontrol, state:PumpFault, variable:CA_mode, variable:patient_bp, variable:target_bp, variable:requested_target_bp, variable:shared_buffer_bp, ... +44`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2690`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sl7-0-3096823055` | `accept` | ❌ | ❌ | The SL-7 unsafe_recovery evidence is valid: if Autocontrol is active with pump_fault=1 and no PumpFaultOccurred event is injected, the current model skips normal control but leaves CARA in Autocontrol with alarm_signal=0 and software_control=1. The smallest NL-grounded repair is to add a guard-only transition from Autocontrol to PumpFault when pump_fault != ...<truncated 478 chars> |
- repair_rationale：Accepted the hard SL-7 model_review request because the current Autocontrol state can remain active with pump_fault=1, alarm_signal=0, and software_control=1 unless the PumpFaultOccurred event is explicitly injected.；The new `Autocontrol -> PumpFault : if [pump_fault != 0];` transition closes that exact gap for the cited `autocontrol_with_existing_complication_does_not_control_flow` condition: on the next cycle from Autocontrol with pump_fault=1, the mo...<truncated 105 chars>；The existing `if [pump_fault == 0]` guard inside Autocontrol.during is preserved, so normal autocontrol still computes flow_rate, control_voltage, pump_speed, infusion_rate_log, and log_entry_count only when there are no pump-operation comp...<truncated 10 chars>；The prior simulation repair is preserved: `AutocontrolInit -> Manual : TerminateAC;` remains before the unconditional `AutocontrolInit -> Autocontrol;`, so the earlier `terminate_from_ask_and_init_returns_manual` scenario remains addressed.；All required grounded states, variables, events, initial transitions, manual actions, buffer action, PumpFault alarm/release actions, PumpFaultOccurred event transition, FaultRemoved recovery transition, and CA/CB/CP/CC_backManual forced tr...<truncated 23 chars>
- diff_summary：`{"summary": "Added one guarded transition, `Autocontrol -> PumpFault : if [pump_fault != 0];`, before the Autocontrol TerminateAC/event fault transitions so an already-present pump fault in Autocontrol reaches the diagnostic PumpFault state and triggers the existing alarm/control-release enter actions."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int log_entry_count = 0;
def float patient_bp = 0.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_buffer_bp = 0.0;
def float flow_rate = 0.0;
def float manual_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def float infusion_rate_log = 0.0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        >> during before {
            shared_buffer_bp = patient_bp;
        }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_signal = 0;
                pump_fault = 0;
            }
            during {
                pump_speed = built_in_switch_speed;
                flow_rate = manual_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                software_control = 0;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
                pump_fault = 0;
            }
        }

        state Autocontrol {
            during {
                if [pump_fault == 0] {
                    flow_rate = target_bp - patient_bp;
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    infusion_rate_log = flow_rate;
                    log_entry_count = log_entry_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC : InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
            target_bp = requested_target_bp;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> Manual : TerminateAC;
        AutocontrolInit -> Autocontrol;
        Autocontrol -> PumpFault : if [pump_fault != 0];
        Autocontrol -> Manual : TerminateAC;
        Autocontrol -> PumpFault :: PumpFaultOccurred effect {
            pump_fault = 1;
        };
        PumpFault -> Manual :: FaultRemoved;
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -87,6 +87,7 @@
         Ask_StartAC -> Manual : TerminateAC;
         AutocontrolInit -> Manual : TerminateAC;
         AutocontrolInit -> Autocontrol;
+        Autocontrol -> PumpFault : if [pump_fault != 0];
         Autocontrol -> Manual : TerminateAC;
         Autocontrol -> PumpFault :: PumpFaultOccurred effect {
             pump_fault = 1;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:5457a3a79c481f65745243aa36d98d16da1ba99718da4e1a2ae499a4fdd480bc`。
  - SL-10 evidence 1: `{"summary": "The hard SL-7 request was a major unsafe_recovery finding: Autocontrol could remain active with pump_fault=1, alarm_signal=0, and software_control=1 when no PumpFaultOccurred event was injected. The candidate adds exactly one NL-grounded repair, `Autocontrol -> PumpFault : if [pump_fault != 0];`, so an already-present pump-operation complication in Autocontrol reaches PumpFault and triggers the existing PumpFault.enter actions that set alarm_signal=1, software_control=0, and CA_mode=0."}`
  - SL-10 evidence 2: `{"summary": "The SL-9 decision accepted this request with a minimal-edit rationale matching the DSL diff: add a guard-only Autocontrol-to-PumpFault transition for existing pump_fault != 0, preserve PumpFault alarm/release actions, and preserve the prior AutocontrolInit TerminateAC transition-order repair. The candidate implements that intent and does not delete required states, variables, events, existing fault-event transition, FaultRemoved recovery, or forced backManual transitions."}`
  - SL-10 evidence 3: `{"summary": "The NL requires CARA to control flow only while there are no pump-operation complications, and when a pump fault such as occlusion occurs the pump activates alarm signals and, when CARA was controlling the pump, the software releases control. The new guarded transition directly enforces that requirement for the previously uncovered existing-fault case, while the existing Autocontrol.during `if [pump_fault == 0]` continues to restrict normal flow/log/control-voltage updates to fault-free operation."}`
  - SL-10 evidence 4: `{"summary": "The prior SD-6 simulation repair remains preserved: `AutocontrolInit -> Manual : TerminateAC;` still appears before the unconditional `AutocontrolInit -> Autocontrol;`, and the local simulation evidence now shows the previously failing `terminate_from_ask_and_init_returns_manual` scenario passes, including the `terminate_from_init_to_manual` step entering Manual with CA_mode=0, software_control=0, pump_speed=2.0, and flow_rate=4.0."}`
  - SL-10 evidence 5: `{"summary": "The candidate preserves the required NL structure and actions: CARA and Mode_Control_Algorithm remain; Manual, Ask_StartAC, AutocontrolInit, Autocontrol, and PumpFault remain; StartAC still enters AutocontrolInit; ChangeSetpoint still assigns target_bp from requested_target_bp; TerminateAC remains from Ask_StartAC, AutocontrolInit, and Autocontrol; PumpFaultOccurred still enters PumpFault; FaultRemoved still returns Manual; CA/CB/CP/CC_backManual still force Manual; shared_buffer_bp is still updated from patient_bp; Manual still uses built_in_switch_speed and manual_flow_rate; and Autocontrol still computes flow_rate inversely from patient_bp when fault-free."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:7b8ce3144e97ba307c15ae5a3bb922da8b77f89d1c0c60869f90bf6ba05397d1", "covered_local_objection_kinds": ["scenario_regression", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:fb1f2af1876d5f626e300bbab9031169735ca994aa5c6c909b81111f083600be", "local_override_rationale_count": 4, "local_override_rationale_hash": "sha256:f0af4761198267643286b7a3cabfb3ec2567a1808c5251ba8a0bda8f939210ae", "local_rejection_evidence_hash": "sha256:8e38d0cafc15a0c5769d11d50aa6982ba37052558ad8660b0dce12d28e7c7145", "local_rejection_reason": "scenario_regression; missing_required_grounding", "missing_local_objection_kinds": [],...<truncated 340 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 14, "n_scenarios_passed": 13, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: first empty cycle dispatches to Manual, stores BP in the shared buffer, and drives pump speed/flow from manual inputs.", "name": "default_init_enters_manual_and_uses_manual_inputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode":...<truncated 21560 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial_root", "transition:initial_mode_control", "guard:Autocontrol_no_pump_fault", "action:buffer_bp"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-8bd9f01c6cc` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-8bd9f01c6cc` | accept=1, reject=0 | `sl10_review` | `sha256:f04099ce732a370989d587eccf7681da3e383b00686d0aca51dab7365d5c8563` | Accepted the hard SD-6 simulation request because the evidence provides a precise failing step and a minimal local repair., For scenario terminate_from_ask_and_init_returns_manual, failing step terminate_from_init_to_manual expected state CARA.Mode_Control_Algorithm.Manual with CA_mode=0, software_control=0, pump_speed=2.0, and flow_rate=4.0, but the actual state was Autocontrol with CA_mode=1, software_control=1, pump_speed=100.0, and flow_rate=100.0., The cause is that AutocontrolInit had an unconditional transition to Autocontrol declared before the TerminateAC transition. Reordering lets the TerminateAC event be considered before the fallback progression to Autocontrol., ... +3 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-8bd9f01c6cc` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:f04099ce732a370989d587eccf7681da3e383b00686d0aca51dab7365d5c8563` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +2 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-02af10fd183` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-02af10fd183` | accept=1, reject=0 | `sl10_review` | `sha256:7b8ce3144e97ba307c15ae5a3bb922da8b77f89d1c0c60869f90bf6ba05397d1` | Accepted the hard SL-7 model_review request because the current Autocontrol state can remain active with pump_fault=1, alarm_signal=0, and software_control=1 unless the PumpFaultOccurred event is explicitly injected., The new `Autocontrol -> PumpFault : if [pump_fault != 0];` transition closes that exact gap for the cited `autocontrol_with_existing_complication_does_not_control_flow` condition: on the next cycle from Autocontrol with pump_fault=1, the model enters PumpFault, whose existing enter action sets alarm_signal=1, software_control=0, and CA_mode=0., The existing `if [pump_fault == 0]` guard inside Autocontrol.during is preserved, so normal autocontrol still computes flow_rate, control_voltage, pump_speed, infusion_rate_log, and log_entry_count only when there are no pump-operation complications., ... +2 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-02af10fd183` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:7b8ce3144e97ba307c15ae5a3bb922da8b77f89d1c0c60869f90bf6ba05397d1` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +4 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5888, 'completion_chars': 23045, 'completion_tokens': 7647, 'elapsed_seconds': 141.51122696397942, 'estimated_completion_tokens': 5762, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 12419, 'first_chunk_seconds': 39.114279120985884, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 14097}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3335, 'completion_chars': 13356, 'completion_tokens': 4780, 'elapsed_seconds': 91.79486792100943, 'estimated_completion_tokens': 3339, 'estimated_prompt_tokens': 16012, 'estimated_total_tokens': 19351, 'first_chunk_seconds': 31.663114193012007, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 64046, 'prompt_tokens': 15704, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20484}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3986, 'completion_chars': 16031, 'completion_tokens': 4505, 'elapsed_seconds': 84.07212891799281, 'estimated_completion_tokens': 4008, 'estimated_prompt_tokens': 19537, 'estimated_total_tokens': 23545, 'first_chunk_seconds': 13.131111134018283, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 78147, 'prompt_tokens': 19186, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23691}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4477, 'completion_chars': 18062, 'completion_tokens': 5337, 'elapsed_seconds': 99.12170467298711, 'estimated_completion_tokens': 4516, 'estimated_prompt_tokens': 20206, 'estimated_total_tokens': 24722, 'first_chunk_seconds': 17.70524942598422, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 80822, 'prompt_tokens': 19837, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25174}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1241, 'completion_chars': 5247, 'completion_tokens': 1496, 'elapsed_seconds': 30.582326704025036, 'estimated_completion_tokens': 1312, 'estimated_prompt_tokens': 25622, 'estimated_total_tokens': 26934, 'first_chunk_seconds': 8.189589385001455, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 102488, 'prompt_tokens': 24048, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25544}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 858, 'completion_chars': 4015, 'completion_tokens': 984, 'elapsed_seconds': 19.90516325799399, 'estimated_completion_tokens': 1004, 'estimated_prompt_tokens': 23271, 'estimated_total_tokens': 24275, 'first_chunk_seconds': 4.401664311008062, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 93081, 'prompt_tokens': 21177, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22161}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5093, 'completion_chars': 20476, 'completion_tokens': 5612, 'elapsed_seconds': 103.24892420999822, 'estimated_completion_tokens': 5119, 'estimated_prompt_tokens': 21149, 'estimated_total_tokens': 26268, 'first_chunk_seconds': 11.465378005988896, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 84596, 'prompt_tokens': 20913, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26525}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5093, 'completion_chars': 20476, 'completion_tokens': 5595, 'elapsed_seconds': 102.80125429999316, 'estimated_completion_tokens': 5119, 'estimated_prompt_tokens': 21753, 'estimated_total_tokens': 26872, 'first_chunk_seconds': 11.538576041988563, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 87010, 'prompt_tokens': 21529, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 27124}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1854, 'completion_chars': 8875, 'completion_tokens': 3861, 'elapsed_seconds': 72.13534241801244, 'estimated_completion_tokens': 2219, 'estimated_prompt_tokens': 23893, 'estimated_total_tokens': 26112, 'first_chunk_seconds': 39.439853910007514, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 95572, 'prompt_tokens': 24077, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 27938}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1328, 'completion_chars': 5584, 'completion_tokens': 1844, 'elapsed_seconds': 36.82688523901743, 'estimated_completion_tokens': 1396, 'estimated_prompt_tokens': 45336, 'estimated_total_tokens': 46732, 'first_chunk_seconds': 12.356496832013363, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 181344, 'prompt_tokens': 41567, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 43411}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1201, 'completion_chars': 5539, 'completion_tokens': 1576, 'elapsed_seconds': 32.77388508600416, 'estimated_completion_tokens': 1385, 'estimated_prompt_tokens': 53665, 'estimated_total_tokens': 55050, 'first_chunk_seconds': 11.07655635100673, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 214660, 'prompt_tokens': 47171, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 48747}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3928, 'completion_chars': 15470, 'completion_tokens': 4858, 'elapsed_seconds': 90.09133652300807, 'estimated_completion_tokens': 3868, 'estimated_prompt_tokens': 24606, 'estimated_total_tokens': 28474, 'first_chunk_seconds': 20.7880561890197, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 98424, 'prompt_tokens': 24368, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 29226}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 6268, 'completion_chars': 25142, 'completion_tokens': 7139, 'elapsed_seconds': 131.34747005000827, 'estimated_completion_tokens': 6286, 'estimated_prompt_tokens': 25222, 'estimated_total_tokens': 31508, 'first_chunk_seconds': 20.38874032901367, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 100886, 'prompt_tokens': 24986, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 32125}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1747, 'completion_chars': 8336, 'completion_tokens': 2557, 'elapsed_seconds': 48.356181891984306, 'estimated_completion_tokens': 2084, 'estimated_prompt_tokens': 26762, 'estimated_total_tokens': 28846, 'first_chunk_seconds': 16.807112157985102, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 107047, 'prompt_tokens': 26933, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 29490}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success_but_weak_oracle_ineligible`。
- required stages executed：`45/16`，missing=`<none>`。
- repairs：`2/2` accepted；scenario_history=`9`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
