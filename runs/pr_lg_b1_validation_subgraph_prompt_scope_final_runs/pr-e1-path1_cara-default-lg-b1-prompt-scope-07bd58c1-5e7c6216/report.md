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
| Git commit | `07bd58c155b512bef419dbaadb50f6e43c3ce544` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:d48663b271a8682c7ee1717bf559731df76d03215d4145494e6940c0c7416d7a", "iteration": 2, "matching_repair_history_indices": [2], "repair_history_index": 2, "selected_source_stage": "SL-7", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 450873, 'completion_tokens': 53042, 'total_tokens': 503915, 'estimated_prompt_tokens': 476642, 'estimated_completion_tokens': 42129, 'estimated_total_tokens': 518771, 'prompt_chars': 1906538, 'completion_chars': 168498, 'n_calls': 16, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`1020.578s` |
| run record | [`pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:da30a6c4b1a20de3548241767d6c27b40f011c2d6238c9cc64991eb8518cd99e` |
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
| `langgraph_node_trace_hash` | `sha256:059f8d273595b859e15b7cce0f2aff428bc9864b86b859ad2b67292ed3469c76` |
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
def int pump_fault = 0;
def int alarm_active = 0;
def int control_released = 1;
def int infusion_log_records = 0;
def float patient_bp = 0.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_sensor_buffer = 0.0;
def float manual_default_flow_rate = 1.0;
def float default_flow_rate = 1.0;
def float pressure_gain = 0.01;
def float flow_rate = 0.0;
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
        ! * -> Manual :: TerminateAC;

        >> during before { shared_sensor_buffer = patient_bp; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                if [pump_fault > 0] {
                    alarm_active = 1;
                } else {
                    alarm_active = 0;
                }
                control_released = 1;
            }
            during {
                pump_speed = manual_switch_speed;
                flow_rate = manual_default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 1;
                if [pump_fault > 0] {
                    alarm_active = 1;
                    control_released = 1;
                } else {
                    alarm_active = 0;
                }
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 2;
                if [pump_fault > 0] {
                    control_released = 1;
                    alarm_active = 1;
                } else {
                    control_released = 0;
                    alarm_active = 0;
                    flow_rate = default_flow_rate;
                }
            }
        }

        state Autocontrol {
            enter {
                CA_mode = 3;
                control_released = 0;
                alarm_active = 0;
            }
            during {
                if [pump_fault == 0] {
                    if [patient_bp > target_bp] {
                        flow_rate = default_flow_rate - ((patient_bp - target_bp) * pressure_gain);
                    } else {
                        flow_rate = default_flow_rate + ((target_bp - patient_bp) * pressure_gain);
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    infusion_log_records = infusion_log_records + 1;
                }
            }
        }

        state PumpFault {
            enter {
                CA_mode = 4;
                alarm_active = 1;
                control_released = 1;
            }
        }

        Manual -> Manual : /Mode_Control_Algorithm.PumpFault.FaultRemoved effect { pump_fault = 0; alarm_active = 0; };
        Manual -> Manual : if [pump_fault > 0] effect { alarm_active = 1; control_released = 1; };
        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> PumpFault : if [pump_fault > 0];
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> PumpFault : if [pump_fault > 0];
        AutocontrolInit -> Autocontrol;
        Autocontrol -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=13835 | 生成初始 DSL 与 grounding seeds | initial len=2821 | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=153860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=79170 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=133063 | LLM per-request accept/reject + repair | candidate len=2944,3064,3617 | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=123987 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=153860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=153860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=133063 | LLM per-request accept/reject + repair | candidate len=2944,3064,3617 | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=123987 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=153860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=79170 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=133063 | LLM per-request accept/reject + repair | candidate len=2944,3064,3617 | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=123987 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1; blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=153860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=153860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=79170 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-prompt-scope-07bd58c1-5e7c6216.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T14:38:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T14:38:49Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T14:38:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T14:38:49Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T14:41:05Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T14:41:05Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2821,hash=sha256:482015188fe1 |
| 7 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T14:41:05Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:482015188fe1f54616d4b49e12679f832c1bafb562ab1960150d6a29964e23ee |
| 10 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T14:41:05Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2821,hash=sha256:482015188fe1, current_hash=sha256:482015188fe1f54616d4b49e12679f832c1bafb562ab1960150d6a29964e23ee |
| 12 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T14:41:05Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T14:41:05Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T14:41:05Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T14:41:05Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T14:41:05Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T14:41:05Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T14:41:05Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T14:41:05Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T14:42:24Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T14:42:24Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T14:42:25Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T14:42:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T14:42:25Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T14:42:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T14:42:25Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T14:42:25Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-05T14:42:25Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T14:42:25Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 33 | `2026-06-05T14:43:21Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T14:43:21Z` | `SL-7` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-05T14:43:21Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 36 | `2026-06-05T14:43:21Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T14:43:21Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["DSL Manual.enter sets alarm_active=0", "DSL forced transitions from any state to Manual do not clear or guard pump_fault", "DSL only FaultRemoved effect clears pump_fault=0", "sim cp_backmanual_from_pumpfault: actual_state Manual, pump_fault=1, alarm_active=0", "NL requires pump fault al...<truncated 467 chars> | <none> |
| 38 | `2026-06-05T14:43:21Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 39 | `2026-06-05T14:43:21Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T14:43:21Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["DSL Manual.enter sets alarm_active=0", "DSL forced transitions from any state to Manual do not clear or guard pump_fault", "DSL only FaultRemoved effect clears pump_fault=0", "sim cp_backmanual_from_pumpfault: actual_state Manual, pump_fault=1, alarm_active=0", "NL requires pump fault alarm act...<truncated 460 chars> | current_dsl:len=2821,hash=sha256:482015188fe1 |
| 41 | `2026-06-05T14:43:21Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-05T14:43:21Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 43 | `2026-06-05T14:43:21Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2821,hash=sha256:482015188fe1 |
| 44 | `2026-06-05T14:43:52Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 45 | `2026-06-05T14:43:52Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2944,hash=sha256:54fcdf1734e5 |
| 46 | `2026-06-05T14:43:52Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 47 | `2026-06-05T14:43:52Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:54fcdf1734e5639aa745de3c8846c7e22b53507fb28768bc8d6a2d53846a301c |
| 48 | `2026-06-05T14:44:16Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 49 | `2026-06-05T14:44:16Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 50 | `2026-06-05T14:44:16Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 51 | `2026-06-05T14:44:16Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2944,hash=sha256:54fcdf1734e5 |
| 52 | `2026-06-05T14:44:16Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:54fcdf1734e5639aa745de3c8846c7e22b53507fb28768bc8d6a2d53846a301c |
| 53 | `2026-06-05T14:44:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 54 | `2026-06-05T14:44:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 55 | `2026-06-05T14:44:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 56 | `2026-06-05T14:44:16Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:54fcdf1734e5639aa745de3c8846c7e22b53507fb28768bc8d6a2d53846a301c |
| 57 | `2026-06-05T14:44:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 58 | `2026-06-05T14:44:16Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=2944,hash=sha256:54fcdf1734e5, current_hash=sha256:54fcdf1734e5639aa745de3c8846c7e22b53507fb28768bc8d6a2d53846a301c |
| 59 | `2026-06-05T14:44:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 60 | `2026-06-05T14:44:16Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 61 | `2026-06-05T14:44:16Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 62 | `2026-06-05T14:44:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 63 | `2026-06-05T14:44:16Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 64 | `2026-06-05T14:44:16Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 65 | `2026-06-05T14:44:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 66 | `2026-06-05T14:44:16Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 67 | `2026-06-05T14:44:16Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-5A", "ok": true, "status": "StageStatus.OK"} | <none> |
| 68 | `2026-06-05T14:44:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 69 | `2026-06-05T14:44:16Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 targeted_retry", "ok": false, "reason": "reuse_frozen_scenario_set"} | <none> |
| 70 | `2026-06-05T14:44:16Z` | `<control>` | `1` | `frozen_scenario_refresh_targeted_retry` | {} | <none> |
| 71 | `2026-06-05T14:44:16Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 72 | `2026-06-05T14:44:16Z` | `SL-5` | `1` | `stage_enter` | {"reason": "targeted_refresh_after_frozen_gap_or_dsl_change"} | <none> |
| 73 | `2026-06-05T14:45:18Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 74 | `2026-06-05T14:45:18Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 75 | `2026-06-05T14:45:19Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 76 | `2026-06-05T14:45:19Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 77 | `2026-06-05T14:45:19Z` | `SL-5` | `1` | `stage_enter` | {"reason": "targeted_refresh_after_frozen_gap_or_dsl_change"} | <none> |
| 78 | `2026-06-05T14:46:42Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 79 | `2026-06-05T14:46:42Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 80 | `2026-06-05T14:46:43Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
- ……另有 `120` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SL-7` | yes | fixbatch-0-sha256-f883b5485a5 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-6` | yes | fixbatch-1-sha256-5adbf9ad4d9 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SL-7` | yes | fixbatch-2-sha256-fdd92baad50 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 |
|---|---|---|---|---|---|
| `default_init_manual_operation_outputs` | default-init dispatches into Manual and verifies manual switch speed, manual default flow, and sensor buffering obligati...<truncated 4 chars> | ✅ | ✅ | ✅ | ✅ |
| `initiate_change_setpoint_start_autocontrol` | default-init reaches Manual, then caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, and reaches ...<truncated 19 chars> | ✅ | ✅ | ✅ | ✅ |
| `autocontrol_no_fault_low_pressure_stays_controlled` | explicit-hot-start in Autocontrol with no pump fault verifies no phantom fault transition and higher flow for below-targ...<truncated 12 chars> | ✅ | ✅ | ✅ | ✅ |
| `autocontrol_fault_enters_pumpfault` | explicit-hot-start in Autocontrol with pump_fault present verifies fault transition to PumpFault, alarm activation, and ...<truncated 25 chars> | ✅ | ✅ | ✅ | ✅ |
| `fault_removed_returns_manual` | explicit-hot-start in PumpFault verifies caregiver fault removal returns to Manual and clears the fault for manual recov...<truncated 4 chars> | ✅ | ✅ | ✅ | ✅ |
| `ca_and_cb_forced_back_manual` | explicit-hot-start probes two cross-component backManual forced fallbacks from Autocontrol and Ask_StartAC to the shared...<truncated 15 chars> | ✅ | ✅ | ✅ | ✅ |
| `cp_and_cc_forced_back_manual` | explicit-hot-start probes CP_backManual from PumpFault with a still-present fault and CC_backManual from AutocontrolInit...<truncated 49 chars> | ✅ | ❌ | ✅ | ✅ |
| `terminate_ac_forced_manual_recovery` | explicit-hot-start in Autocontrol verifies caregiver TerminateAC releases algorithmic control and returns to Manual. | ✅ | ✅ | ✅ | ✅ |
| `manual_self_forced_backmanual_reentry` | explicit-hot-start in Manual with stale mode/control flags verifies CA_backManual is still a forced fallback that re-ent...<truncated 88 chars> | ⚪ | ✅ | ✅ | ✅ |
| `manual_self_terminate_forced_reentry` | explicit-hot-start in Manual with stale mode/control flags verifies TerminateAC is a forced fallback to Manual, detectin...<truncated 79 chars> | ⚪ | ✅ | ✅ | ✅ |
| `ask_startac_fault_guard_targets_pumpfault` | explicit-hot-start in Ask_StartAC with unresolved pump fault verifies the fault guard targets PumpFault and applies alar...<truncated 26 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `changesetpoint_unique_effect_value` | explicit-hot-start in Ask_StartAC verifies ChangeSetpoint self-transition preserves Ask_StartAC and assigns target_bp fr...<truncated 64 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `pumpfault_faultremoved_unique_clear_effect` | explicit-hot-start in PumpFault verifies FaultRemoved targets Manual and clears a nonzero pump_fault value, catching wro...<truncated 45 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `startac_isolated_target_and_init_outputs` | explicit-hot-start in Ask_StartAC without a fault verifies StartAC targets AutocontrolInit and applies initialization ou...<truncated 29 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `initiateac_isolated_target_and_entry_outputs` | explicit-hot-start in Manual verifies caregiver InitiateAC targets Ask_StartAC exactly and applies the Ask_StartAC mode/...<truncated 20 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `autocontrolinit_to_autocontrol_unique_outputs` | explicit-hot-start in AutocontrolInit without a fault verifies the automatic transition targets Autocontrol and computes...<truncated 51 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `autocontrolinit_fault_guard_targets_pumpfault` | explicit-hot-start in AutocontrolInit with unresolved pump fault verifies the fault guard targets PumpFault rather than ...<truncated 61 chars> | ⚪ | ⚪ | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_operation_outputs` — default-init dispatches into Manual and verifies manual switch speed, manual default flow, and sensor buffering obligations.</summary>

| Field | Value |
|---|---|
| description | default-init dispatches into Manual and verifies manual switch speed, manual default flow, and sensor buffering obligations. |
| initial_state | `<default-init>` |
| initial_vars | `{"manual_default_flow_rate": 1.7, "manual_switch_speed": 2.5, "patient_bp": 85.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `default_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 1.7, "pump_speed": 2.5, "shared_sensor_buffer": 85.0}` |

</details>

<details><summary>`initiate_change_setpoint_start_autocontrol` — default-init reaches Manual, then caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, and reaches normal Autocontrol.</summary>

| Field | Value |
|---|---|
| description | default-init reaches Manual, then caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC, and reaches normal Autocontrol. |
| initial_state | `<default-init>` |
| initial_vars | `{"default_flow_rate": 1.0, "patient_bp": 120.0, "pressure_gain": 0.01, "requested_target_bp": 90.0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_after_default_init` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0}` |
| 1 `initiate_enters_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "alarm_active": 0}` |
| 2 `change_setpoint_updates_target` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "target_bp": 90.0}` |
| 3 `startac_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 2, "alarm_active": 0, "control_released": 0, "flow_rate": 1.0}` |
| 4 `autocontrol_computes_lower_flow_for_high_pressure` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Autocontrol` | `{"CA_mode": 3, "alarm_active": 0, "control_released": 0, "control_voltage": 0.7, "flow_rate": 0.7, "infusion_log_records": 1, "pump_speed": 0.7, "shared_sensor_buffer": 120.0}` |

</details>

<details><summary>`autocontrol_no_fault_low_pressure_stays_controlled` — explicit-hot-start in Autocontrol with no pump fault verifies no phantom fault transition and higher flow for below-target pressure.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Autocontrol with no pump fault verifies no phantom fault transition and higher flow for below-target pressure. |
| initial_state | `CARA.Mode_Control_Algorithm.Autocontrol` |
| initial_vars | `{"default_flow_rate": 1.0, "infusion_log_records": 3, "patient_bp": 80.0, "pressure_gain": 0.01, "pump_fault": 0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `stay_in_autocontrol_and_compute_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Autocontrol` | `{"control_voltage": 1.2, "flow_rate": 1.2, "infusion_log_records": 4, "pump_speed": 1.2, "shared_sensor_buffer": 80.0}` |

</details>

<details><summary>`autocontrol_fault_enters_pumpfault` — explicit-hot-start in Autocontrol with pump_fault present verifies fault transition to PumpFault, alarm activation, and software control release.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Autocontrol with pump_fault present verifies fault transition to PumpFault, alarm activation, and software control release. |
| initial_state | `CARA.Mode_Control_Algorithm.Autocontrol` |
| initial_vars | `{"alarm_active": 0, "control_released": 0, "patient_bp": 110.0, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_detected_pumpfault_entered` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 4, "alarm_active": 1, "control_released": 1, "shared_sensor_buffer": 110.0}` |

</details>

<details><summary>`fault_removed_returns_manual` — explicit-hot-start in PumpFault verifies caregiver fault removal returns to Manual and clears the fault for manual recovery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in PumpFault verifies caregiver fault removal returns to Manual and clears the fault for manual recovery. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"alarm_active": 1, "control_released": 1, "manual_default_flow_rate": 0.9, "manual_switch_speed": 1.4, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_removed_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 0.9, "pump_fault": 0, "pump_speed": 1.4}` |

</details>

<details><summary>`ca_and_cb_forced_back_manual` — explicit-hot-start probes two cross-component backManual forced fallbacks from Autocontrol and Ask_StartAC to the shared Manual target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes two cross-component backManual forced fallbacks from Autocontrol and Ask_StartAC to the shared Manual target. |
| initial_state | `CARA.Mode_Control_Algorithm.Autocontrol` |
| initial_vars | `{"control_released": 0, "manual_default_flow_rate": 1.1, "manual_switch_speed": 3.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_from_autocontrol` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "flow_rate": 1.1, "pump_speed": 3.0}` |
| 1 `move_to_ask_startac_again` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1}` |
| 2 `cb_backmanual_from_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "flow_rate": 1.1, "pump_speed": 3.0}` |

</details>

<details><summary>`cp_and_cc_forced_back_manual` — explicit-hot-start probes CP_backManual from PumpFault with a still-present fault and CC_backManual from AutocontrolInit, both forcing the shared Manual recover...<truncated 9 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes CP_backManual from PumpFault with a still-present fault and CC_backManual from AutocontrolInit, both forcing the shared Manual recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"alarm_active": 1, "manual_default_flow_rate": 1.3, "manual_switch_speed": 2.2, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_from_pumpfault_fault_still_alarm` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 1, "control_released": 1, "flow_rate": 1.3, "pump_fault": 1, "pump_speed": 2.2}` |
| 1 `remove_fault_before_new_autocontrol_attempt` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 1.3, "pump_fault": 0, "pump_speed": 2.2}` |
| 2 `go_to_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1}` |
| 3 `go_to_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 2, "control_released": 0}` |
| 4 `cc_backmanual_from_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 1.3, "pump_speed": 2.2}` |

</details>

<details><summary>`terminate_ac_forced_manual_recovery` — explicit-hot-start in Autocontrol verifies caregiver TerminateAC releases algorithmic control and returns to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Autocontrol verifies caregiver TerminateAC releases algorithmic control and returns to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.Autocontrol` |
| initial_vars | `{"alarm_active": 0, "control_released": 0, "manual_default_flow_rate": 1.6, "manual_switch_speed": 1.8}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_ac_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 1.6, "pump_speed": 1.8}` |

</details>

<details><summary>`manual_self_forced_backmanual_reentry` — explicit-hot-start in Manual with stale mode/control flags verifies CA_backManual is still a forced fallback that re-enters Manual, detecting a missing forced l...<truncated 48 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Manual with stale mode/control flags verifies CA_backManual is still a forced fallback that re-enters Manual, detecting a missing forced line even when source and target are both Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"CA_mode": 9, "alarm_active": 1, "control_released": 0, "manual_default_flow_rate": 2.4, "manual_switch_speed": 4.4, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_reenters_manual_and_reapplies_enter` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 2.4, "pump_speed": 4.4}` |

</details>

<details><summary>`manual_self_terminate_forced_reentry` — explicit-hot-start in Manual with stale mode/control flags verifies TerminateAC is a forced fallback to Manual, detecting a missing forced transition declaratio...<truncated 39 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Manual with stale mode/control flags verifies TerminateAC is a forced fallback to Manual, detecting a missing forced transition declaration even from the shared recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"CA_mode": 7, "alarm_active": 1, "control_released": 0, "manual_default_flow_rate": 1.9, "manual_switch_speed": 3.6, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminateac_reenters_manual_and_releases_control` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 1.9, "pump_speed": 3.6}` |

</details>

<details><summary>`ask_startac_fault_guard_targets_pumpfault` — explicit-hot-start in Ask_StartAC with unresolved pump fault verifies the fault guard targets PumpFault and applies alarm/control-release outputs.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Ask_StartAC with unresolved pump fault verifies the fault guard targets PumpFault and applies alarm/control-release outputs. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"alarm_active": 0, "control_released": 0, "patient_bp": 123.0, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ask_startac_fault_goes_to_pumpfault` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 4, "alarm_active": 1, "control_released": 1, "shared_sensor_buffer": 123.0}` |

</details>

<details><summary>`changesetpoint_unique_effect_value` — explicit-hot-start in Ask_StartAC verifies ChangeSetpoint self-transition preserves Ask_StartAC and assigns target_bp from requested_target_bp, catching missing...<truncated 24 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Ask_StartAC verifies ChangeSetpoint self-transition preserves Ask_StartAC and assigns target_bp from requested_target_bp, catching missing or wrong effect values. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"alarm_active": 1, "control_released": 1, "pump_fault": 0, "requested_target_bp": 137.5, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `target_bp_updated_to_unique_requested_value` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "alarm_active": 0, "target_bp": 137.5}` |

</details>

<details><summary>`pumpfault_faultremoved_unique_clear_effect` — explicit-hot-start in PumpFault verifies FaultRemoved targets Manual and clears a nonzero pump_fault value, catching wrong target and missing or wrong clear eff...<truncated 5 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in PumpFault verifies FaultRemoved targets Manual and clears a nonzero pump_fault value, catching wrong target and missing or wrong clear effects. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"alarm_active": 1, "control_released": 1, "manual_default_flow_rate": 1.25, "manual_switch_speed": 2.7, "pump_fault": 42}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `faultremoved_clears_fault_and_enters_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 1.25, "pump_fault": 0, "pump_speed": 2.7}` |

</details>

<details><summary>`startac_isolated_target_and_init_outputs` — explicit-hot-start in Ask_StartAC without a fault verifies StartAC targets AutocontrolInit and applies initialization outputs including default flow.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Ask_StartAC without a fault verifies StartAC targets AutocontrolInit and applies initialization outputs including default flow. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"alarm_active": 1, "control_released": 1, "default_flow_rate": 2.35, "flow_rate": 0.0, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `startac_enters_autocontrolinit_with_default_flow` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 2, "alarm_active": 0, "control_released": 0, "flow_rate": 2.35}` |

</details>

<details><summary>`initiateac_isolated_target_and_entry_outputs` — explicit-hot-start in Manual verifies caregiver InitiateAC targets Ask_StartAC exactly and applies the Ask_StartAC mode/alarm entry outputs.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Manual verifies caregiver InitiateAC targets Ask_StartAC exactly and applies the Ask_StartAC mode/alarm entry outputs. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"CA_mode": 0, "alarm_active": 1, "control_released": 1, "manual_default_flow_rate": 1.05, "manual_switch_speed": 1.2, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiateac_targets_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 1, "alarm_active": 0}` |

</details>

<details><summary>`autocontrolinit_to_autocontrol_unique_outputs` — explicit-hot-start in AutocontrolInit without a fault verifies the automatic transition targets Autocontrol and computes unique flow, voltage, pump speed, and l...<truncated 11 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolInit without a fault verifies the automatic transition targets Autocontrol and computes unique flow, voltage, pump speed, and log outputs. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"alarm_active": 1, "control_released": 1, "control_voltage": 0.0, "default_flow_rate": 2.0, "flow_rate": 9.9, "infusion_log_records": 5, "patient_bp": 130.0, "pressure_gain": 0.02, "pump_fault": 0, "pump_speed": 0.0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `automatic_transition_to_autocontrol_computes_outputs` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Autocontrol` | `{"CA_mode": 3, "alarm_active": 0, "control_released": 0, "control_voltage": 1.4, "flow_rate": 1.4, "infusion_log_records": 6, "pump_speed": 1.4, "shared_sensor_buffer": 130.0}` |

</details>

<details><summary>`autocontrolinit_fault_guard_targets_pumpfault` — explicit-hot-start in AutocontrolInit with unresolved pump fault verifies the fault guard targets PumpFault rather than normal Autocontrol and applies alarm/con...<truncated 21 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolInit with unresolved pump fault verifies the fault guard targets PumpFault rather than normal Autocontrol and applies alarm/control-release outputs. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"alarm_active": 0, "control_released": 0, "patient_bp": 101.0, "pump_fault": 3}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `autocontrolinit_fault_goes_to_pumpfault` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 4, "alarm_active": 1, "control_released": 1, "shared_sensor_buffer": 101.0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:54fcdf1734e5639aa745de3c8846c7e22b53507fb28768bc8d6a2d53846a301c` |
| 2 | `1` | ✅ | `SD-6` | cp_and_cc_forced_back_manual | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:5ff9d43b7100f6a2a25bd3b281247b1d0f8978779233f97647f7342ab4639666` |
| 3 | `2` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:d48663b271a8682c7ee1717bf559731df76d03215d4145494e6940c0c7416d7a` |

<details><summary>Repair 1 / iteration `0` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:482015188fe1f54616d4b49e12679f832c1bafb562ab1960150d6a29964e23ee`；candidate_dsl_hash：`sha256:54fcdf1734e5639aa745de3c8846c7e22b53507fb28768bc8d6a2d53846a301c`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Forced backManual recovery can enter Manual with pump_fault still active while Manual.enter clears alarm_active, suppressing fault alarm indication before the caregiver removes the fault.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-f883b5485a5`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL Manual.enter sets alarm_active=0', 'DSL forced transitions from any state to Manual do not clear or guard pump_fault', 'DSL only FaultRemoved effect clears pump_fault=0', 'sim cp_backmanual_from_pumpfault: actual_state Manual, pump_fault=1, alarm_active=0', 'NL requires pump fault alarm activation and caregiver fault removal before recovery from the fault condition'], 'severity': 'major', 'summary': 'Forced backManual recovery can enter Manual with pump_fault still active while Manual.enter clears alarm_active, suppressing fault alarm indication before the caregiver removes the fault.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:Autocontrol, state:PumpFault, variable:CA_mode, variable:pump_fault, variable:alarm_active, variable:control_released, variable:patient_bp, ... +38`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2944`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ❌ | The evidence shows an unsafe recovery path: forced backManual events can enter Manual while pump_fault remains active, and Manual.enter currently clears alarm_active. This is a hard blocking safety finding and can be repaired with a minimal NL-grounded edit that preserves all required states, events, transitions, and actions.；intent=Preserve the alarm in Man...<truncated 112 chars> |
- repair_rationale：Accepted the unsafe_recovery repair request because the current Manual.enter unconditionally set alarm_active = 0 even when pump_fault remained 1 after a forced backManual transition.；The smallest safe edit is local to Manual.enter: CA_mode still becomes Manual and control_released remains 1, but alarm_active is set to 1 whenever pump_fault > 0.；This preserves the NL safety invariant that pump fault alarms remain active until the caregiver removes the fault.；The existing PumpFault -> Manual :: FaultRemoved effect still clears pump_fault = 0 before entering Manual, so Manual.enter then clears alarm_active only after fault removal.；All required preserve elements remain represented: the CARA and Mode_Control_Algorithm hierarchy, Manual, Ask_StartAC, AutocontrolInit, Autocontrol, PumpFault, all listed variables, all forced backManual events, TerminateAC, StartAC, Change...<truncated 159 chars>
- diff_summary：`{"summary": "Changed Manual.enter from unconditional alarm_active = 0 to a pump_fault-sensitive conditional that keeps alarm_active = 1 while pump_fault > 0 and clears it only when pump_fault == 0."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int control_released = 1;
def int infusion_log_records = 0;
def float patient_bp = 0.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_sensor_buffer = 0.0;
def float manual_default_flow_rate = 1.0;
def float default_flow_rate = 1.0;
def float pressure_gain = 0.01;
def float flow_rate = 0.0;
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
        ! * -> Manual :: TerminateAC;

        >> during before { shared_sensor_buffer = patient_bp; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                if [pump_fault > 0] {
                    alarm_active = 1;
                } else {
                    alarm_active = 0;
                }
                control_released = 1;
            }
            during {
                pump_speed = manual_switch_speed;
                flow_rate = manual_default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 1;
                alarm_active = 0;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 2;
                control_released = 0;
                alarm_active = 0;
                flow_rate = default_flow_rate;
            }
        }

        state Autocontrol {
            enter {
                CA_mode = 3;
                control_released = 0;
                alarm_active = 0;
            }
            during {
                if [pump_fault == 0] {
                    if [patient_bp > target_bp] {
                        flow_rate = default_flow_rate - ((patient_bp - target_bp) * pressure_gain);
                    } else {
                        flow_rate = default_flow_rate + ((target_bp - patient_bp) * pressure_gain);
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    infusion_log_records = infusion_log_records + 1;
                }
            }
        }

        state PumpFault {
            enter {
                CA_mode = 4;
                alarm_active = 1;
                control_released = 1;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Autocontrol;
        Autocontrol -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -32,7 +32,11 @@
         state Manual {
             enter {
                 CA_mode = 0;
-                alarm_active = 0;
+                if [pump_fault > 0] {
+                    alarm_active = 1;
+                } else {
+                    alarm_active = 0;
+                }
                 control_released = 1;
             }
             during {
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:c8330288f17870179e2cd4258a7af6b10616b98b2066eb96f598caf6d61d7e70`。
  - SL-10 evidence 1: `{"summary": "The hard SL-7 request was unsafe_recovery: forced backManual transitions could enter Manual while pump_fault remained active, and old Manual.enter unconditionally set alarm_active = 0. The candidate changes only Manual.enter so that when pump_fault > 0 it sets alarm_active = 1, otherwise it clears alarm_active = 0. This directly satisfies the NL obligation that pump fault alarms remain active until the caregiver removes the fault, while preserving the NL-required cross-component fallback that CA_backManual, CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves the required FaultRemoved path semantics: PumpFault -> Manual :: FaultRemoved still clears pump_fault = 0 before Manual.enter executes, so after caregiver fault removal Manual.enter takes the else branch and clears alarm_active. This matches the SL-9 accepted edit intent to preserve the alarm in Manual when pump_fault is active and allow FaultRemoved to clear the fault before Manual clears the alarm."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is minimal and local: no required states, variables, events, transitions, guards, or actions are deleted. CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, Autocontrol, PumpFault, InitiateAC, ChangeSetpoint, StartAC, FaultRemoved, forced backManual transitions, TerminateAC, sensor buffering, manual pump control, autocontrol flow computation, control release, alarm activation, and infusion logging remain represented."}`
  - SL-10 evidence 4: `{"summary": "Scenario evidence reports no regression and no coverage gap: 8 scenarios remain in the set, mutation coverage catches wrong transition targets, missing forced transitions, missing effects, and wrong effect values. The local check reports regression_detected=false; its failure is limited to required-grounding matching, not a behavioral scenario failure."}`
  - SL-10 evidence 5: `{"candidate_dsl_hash": "sha256:54fcdf1734e5639aa745de3c8846c7e22b53507fb28768bc8d6a2d53846a301c", "covered_local_objection_kinds": ["missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:692be568f04728d63d8c6dce685e3239bee2926e6575196a5d92c71b1bf7ddd6", "local_override_rationale_count": 3, "local_override_rationale_hash": "sha256:676d6818ea518831c115086e05c4e2b4940684d03549b608b0396b4c68d15e52", "local_rejection_evidence_hash": "sha256:e97c8cc2906c062efd7e8a3f29189bba88b834d5743232d51087cee1c7b8a110", "local_rejection_reason": "missing_required_grounding", "missing_local_objection_kinds": [], "policy": "SL-10 may override conservative ...<truncated 296 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:InitialRootToModeControl", "transition:InitialModeControlToManual", "action:SetTargetBloodPressure", "guard:PumpFaultDetected"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `1` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`cp_and_cc_forced_back_manual`。
- before_dsl_hash：`sha256:54fcdf1734e5639aa745de3c8846c7e22b53507fb28768bc8d6a2d53846a301c`；candidate_dsl_hash：`sha256:5ff9d43b7100f6a2a25bd3b281247b1d0f8978779233f97647f7342ab4639666`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-5adbf9ad4d9`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-74ed51a7b4` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probes CP_backManual from PumpFault with a still-present fault and CC_backManual from AutocontrolInit, both forcing the shared Manual recovery target.', 'name': 'cp_and_cc_forced_back_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probes CP_backManual from PumpFault with a still-present fault and CC_backManual from AutocontrolInit, both forcing the shared Manual recovery target.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_active': 1, 'control_released': 1, 'flow_rate': 1.3, 'pump_fault': 1, 'pump_speed': 2.2}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'control_released': 1, 'flow_rate': 1.3, 'pump_fault': 0, 'pump_speed': 2.2}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 1, 'step_name': 'remove_fault_before_new_autocontrol_attempt', 'var_assertion_ok': False, 'var_mismatches': {'alarm_active': {'actual': 1, 'expected': 0}, 'pump_fault': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_active': 1, 'control_released': 1, 'flow_rate': 1.3, 'pump_speed': 2.2}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_active': 0, 'control_released': 1, 'flow_rate': 1.3, 'pump_speed': 2.2}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 4, 'step_name': 'cc_backmanual_from_autocontrol_init', 'var_assertion_ok': False, 'var_mismatches': {'alarm_active': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.PumpFault', 'initial_vars': {'alarm_active': 1, 'manual_default_flow_rate': 1.3, 'manual_switch_speed': 2.2, 'pump_fault': 1}, 'scenario_name': 'cp_and_cc_forced_back_manual', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_active': 1, 'control_released': 1, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 1.3, 'infusion_log_records': 0, 'manual_default_flow_rate': 1.3, 'manual_switch_speed': 2.2, 'patient_bp': 0.0, 'pressure_gain': 0.01, 'pump_fault': 1, 'pump_speed': 2.2, 'requested_target_bp': 100.0, 'shared_sensor_buffer': 0.0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'cp_backmanual_from_pumpfault_fault_still_alarm', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_active': 1, 'control_released': 1, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 1.3, 'infusion_log_records': 0, 'manual_default_flow_rate': 1.3, 'manual_switch_speed': 2.2, 'patient_bp': 0.0, 'pressure_gain': 0.01, 'pump_fault': 1, 'pump_speed': 2.2, 'requested_target_bp': 100.0, 'shared_sensor_buffer': 0.0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 1, 'step_name': 'remove_fault_before_new_autocontrol_attempt', 'var_assertion_ok': False, 'var_mismatches': {'alarm_active': {'actual': 1, 'expected': 0}, 'pump_fault': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 1, 'alarm_active': 0, 'control_released': 1, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 1.3, 'infusion_log_records': 0, 'manual_default_flow_rate': 1.3, 'manual_switch_speed': 2.2, 'patient_bp': 0.0, 'pressure_gain': 0.01, 'pump_fault': 1, 'pump_speed': 2.2, 'requested_target_bp': 100.0, 'shared_sensor_buffer': 0.0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'go_to_ask_startac', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 2, 'alarm_active': 0, 'control_released': 0, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 1.0, 'infusion_log_records': 0, 'manual_default_flow_rate': 1.3, 'manual_switch_speed': 2.2, 'patient_bp': 0.0, 'pressure_gain': 0.01, 'pump_fault': 1, 'pump_speed': 2.2, 'requested_target_bp': 100.0, 'shared_sensor_buffer': 0.0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 3, 'step_name': 'go_to_autocontrol_init', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_active': 1, 'control_released': 1, 'control_voltage': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 1.3, 'infusion_log_records': 0, 'manual_default_flow_rate': 1.3, 'manual_switch_speed': 2.2, 'patient_bp': 0.0, 'pressure_gain': 0.01, 'pump_fault': 1, 'pump_speed': 2.2, 'requested_target_bp': 100.0, 'shared_sensor_buffer': 0.0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 4, 'step_name': 'cc_backmanual_from_autocontrol_init', 'var_assertion_ok': False, 'var_mismatches': {'alarm_active': {'actual': 1, 'expected': 0}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:Autocontrol, state:PumpFault, variable:CA_mode, variable:pump_fault, variable:alarm_active, variable:control_released, variable:patient_bp, ... +38`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3064`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-74ed51a7b4` | `accept` | ❌ | ❌ | The sim evidence for scenario cp_and_cc_forced_back_manual shows two local variable failures after the prior safety fix: after CP_backManual forces PumpFault to Manual with pump_fault still active, the scenario then injects the PumpFault.FaultRemoved event while already in Manual and expects pump_fault=0 and alarm_active=0. The existing PumpFault -> Manual :...<truncated 640 chars> |
- repair_rationale：Accepted scenario cp_and_cc_forced_back_manual as the primary sim repair target.；Failing step remove_fault_before_new_autocontrol_attempt expected state CARA.Mode_Control_Algorithm.Manual with pump_fault=0 and alarm_active=0 after event CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved, but actual state was already Man...<truncated 243 chars>；Failing step cc_backmanual_from_autocontrol_init expected Manual with alarm_active=0, but actual alarm_active remained 1 because the previous FaultRemoved event had not cleared pump_fault. Once the new Manual self-transition clears pump_fau...<truncated 106 chars>；This preserves the prior non-regressive safety repair: Manual.enter still keeps alarm_active=1 whenever pump_fault remains active, so cp_backmanual_from_pumpfault_fault_still_alarm continues to pass.；All required grounding elements remain represented, including CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, Autocontrol, PumpFault, the initial transitions, ChangeSetpoint target-blood-pressure action, PumpFaultDetecte...<truncated 154 chars>
- diff_summary：`{"summary": "Added one Manual self-transition, `Manual -> Manual : /Mode_Control_Algorithm.PumpFault.FaultRemoved effect { pump_fault = 0; alarm_active = 0; };`, so caregiver fault removal can clear the active fault/alarm after a forced backManual recovery has already moved the machine from PumpFault into Manual."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int control_released = 1;
def int infusion_log_records = 0;
def float patient_bp = 0.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_sensor_buffer = 0.0;
def float manual_default_flow_rate = 1.0;
def float default_flow_rate = 1.0;
def float pressure_gain = 0.01;
def float flow_rate = 0.0;
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
        ! * -> Manual :: TerminateAC;

        >> during before { shared_sensor_buffer = patient_bp; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                if [pump_fault > 0] {
                    alarm_active = 1;
                } else {
                    alarm_active = 0;
                }
                control_released = 1;
            }
            during {
                pump_speed = manual_switch_speed;
                flow_rate = manual_default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 1;
                alarm_active = 0;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 2;
                control_released = 0;
                alarm_active = 0;
                flow_rate = default_flow_rate;
            }
        }

        state Autocontrol {
            enter {
                CA_mode = 3;
                control_released = 0;
                alarm_active = 0;
            }
            during {
                if [pump_fault == 0] {
                    if [patient_bp > target_bp] {
                        flow_rate = default_flow_rate - ((patient_bp - target_bp) * pressure_gain);
                    } else {
                        flow_rate = default_flow_rate + ((target_bp - patient_bp) * pressure_gain);
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    infusion_log_records = infusion_log_records + 1;
                }
            }
        }

        state PumpFault {
            enter {
                CA_mode = 4;
                alarm_active = 1;
                control_released = 1;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Manual -> Manual : /Mode_Control_Algorithm.PumpFault.FaultRemoved effect { pump_fault = 0; alarm_active = 0; };
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Autocontrol;
        Autocontrol -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -90,6 +90,7 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
+        Manual -> Manual : /Mode_Control_Algorithm.PumpFault.FaultRemoved effect { pump_fault = 0; alarm_active = 0; };
         Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
         Ask_StartAC -> AutocontrolInit :: StartAC;
         AutocontrolInit -> Autocontrol;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:bae4bd341fc1e3c50e10f4ecb6b843b99f06ad0c5cef66a77ec8110f8bdca0d2`。
  - SL-10 evidence 1: `{"summary": "The current hard request is the SD-6 simulation failure in scenario cp_and_cc_forced_back_manual. Step 1, remove_fault_before_new_autocontrol_attempt, injects the existing FaultRemoved event after CP_backManual has already forced the active state from PumpFault to Manual; the old candidate had only PumpFault -> Manual :: FaultRemoved, so the event could not fire in Manual and actual pump_fault/alarm_active stayed 1/1 instead of expected 0/0. The candidate adds a Manual self-transition for the existing PumpFault.FaultRemoved event with effect { pump_fault = 0; alarm_active = 0; }, directly resolving that expected-vs-actual mismatch while keeping the state Manual and preserving co...<truncated 39 chars>`
  - SL-10 evidence 2: `{"summary": "The same edit also resolves the later failing step 4, cc_backmanual_from_autocontrol_init. In the failing trace, CC_backManual from AutocontrolInit reached Manual with alarm_active=1 because step 1 had not cleared pump_fault. With the new Manual self-transition, step 1 clears pump_fault to 0 and alarm_active to 0, so later CC_backManual re-enters Manual with pump_fault already clear and Manual.enter takes its else branch, leaving alarm_active=0 as expected."}`
  - SL-10 evidence 3: `{"summary": "The edit preserves the prior SL-7/SL-10 safety repair and repair_memory guidance. Manual.enter remains pump_fault-sensitive, setting alarm_active=1 whenever pump_fault > 0, so the previously fixed unsafe recovery case CP_backManual from PumpFault with a still-present fault continues to keep the alarm active. The new self-transition only clears the fault/alarm in response to the caregiver fault-removal event, which is grounded in the NL statement that the caregiver removes the fault."}`
  - SL-10 evidence 4: `{"summary": "The DSL diff is minimal and does not delete NL-required model structure. CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, Autocontrol, PumpFault, all required variables, the initial transitions, InitiateAC, ChangeSetpoint target-blood-pressure effect, StartAC, AutocontrolInit-to-Autocontrol, PumpFaultDetected guard, PumpFault FaultRemoved transition, forced CA/CB/CP/CC_backManual transitions, TerminateAC, sensor buffering, manual pump control, autocontrol flow computation, alarm activation, control release, and infusion logging all remain represented."}`
  - SL-10 evidence 5: `{"summary": "The scenario_summary still notes an oracle/coverage weakness for one missing-forced-transition mutation type, but that is a scenario-suite coverage limitation rather than evidence that this candidate regressed the DSL or failed the current hard repair target. It should be carried into the next full top-down revalidation pass, not used to reject this localized repair."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:5ff9d43b7100f6a2a25bd3b281247b1d0f8978779233f97647f7342ab4639666", "covered_local_objection_kinds": ["missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:692be568f04728d63d8c6dce685e3239bee2926e6575196a5d92c71b1bf7ddd6", "local_override_rationale_count": 3, "local_override_rationale_hash": "sha256:e55286ed06a5302b3657446e7d3c3b43010f2fc0ae877141da726d2faa8acb63", "local_rejection_evidence_hash": "sha256:e97c8cc2906c062efd7e8a3f29189bba88b834d5743232d51087cee1c7b8a110", "local_rejection_reason": "missing_required_grounding", "missing_local_objection_kinds": [], "policy": "SL-10 may override conservative ...<truncated 296 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:InitialRootToModeControl", "transition:InitialModeControlToManual", "action:SetTargetBloodPressure", "guard:PumpFaultDetected"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `2` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:5ff9d43b7100f6a2a25bd3b281247b1d0f8978779233f97647f7342ab4639666`；candidate_dsl_hash：`sha256:d48663b271a8682c7ee1717bf559731df76d03215d4145494e6940c0c7416d7a`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：The model can enter or progress through autocontrol initiation while a pump fault is already present, and some autocontrol-related entry actions clear the alarm despite the unresolved fault.
- 2. `<unknown>` `` policy=``：Fault/alarm behavior is not consistently faithful to the NL because active faults can be bypassed during autocontrol initiation and alarms can be cleared before fault removal.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-fdd92baad50`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sl7-0-e56a9044a1` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL: `Manual -> Ask_StartAC :: InitiateAC;` has no `pump_fault == 0` guard.', 'DSL: `Ask_StartAC.enter { ... alarm_active = 0; }` clears alarm unconditionally.', 'DSL: `Ask_StartAC -> AutocontrolInit :: StartAC;` has no `pump_fault == 0` guard.', 'DSL: `AutocontrolInit.enter { control_released = 0; alarm_active = 0; ... }` can assert control and suppress alarm with an unresolved fault.', 'NL requires alarm activation on pump fault and normal autocontrol only with no pump-operation complications.'], 'severity': 'major', 'summary': 'The model can enter or progress through autocontrol initiation while a pump fault is already present, and some autocontrol-related entry actions clear the alarm despite the unresolved fault.'}` |
| `fixreq-2-sl7-1-ef61a52a60` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: pump faults activate alarm signals and caregiver removes the fault.', 'NL: normal autocontrol controls flow rate only while there are no pump-operation complications.', 'DSL lacks guards or fail-safe transitions from Ask_StartAC/AutocontrolInit for `pump_fault > 0`.'], 'severity': 'major', 'summary': 'Fault/alarm behavior is not consistently faithful to the NL because active faults can be bypassed during autocontrol initiation and alarms can be cleared before fault removal.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:Autocontrol, state:PumpFault, variable:CA_mode, variable:pump_fault, variable:alarm_active, variable:control_released, variable:patient_bp, ... +38`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3617`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sl7-0-e56a9044a1` | `accept` | ❌ | ❌ | Accepted because the evidence identifies a hard unsafe_recovery issue: autocontrol initiation could be attempted while pump_fault remains active, and Ask_StartAC/AutocontrolInit could clear alarms or assert control before fault removal. This can be repaired with small NL-grounded fail-safe guards and fault-sensitive entry actions while preserving the require...<truncated 319 chars> |
| `fixreq-2-sl7-1-ef61a52a60` | `accept` | ❌ | ❌ | Accepted because the NL-fidelity finding is valid: pump faults should activate alarms, caregiver fault removal should precede clearing the fault/alarm, and normal autocontrol should only control flow when there are no pump-operation complications. The repair adds fail-safe fault guards from autocontrol-initiation states and avoids unconditional alarm clearin...<truncated 291 chars> |
- repair_rationale：Both current SL-7 requests are accepted because they provide new hard model-review evidence after the earlier scenario repair: active pump faults could still be bypassed during autocontrol initiation.；The previous non-regressive behavior is preserved: Manual.enter remains pump_fault-sensitive, so forced backManual recovery with pump_fault > 0 still keeps alarm_active = 1; the Manual FaultRemoved self-transition remains before the new gua...<truncated 81 chars>；Because pyfcstm cannot mix an event and a guard on the same transition, the required Manual -> Ask_StartAC :: InitiateAC and Ask_StartAC -> AutocontrolInit :: StartAC event transitions are preserved, and small ordered guard fail-safes are a...<truncated 13 chars>；For InitiateAC with pump_fault > 0, the added Manual guard self-transition keeps the machine in Manual and maintains alarm_active = 1/control_released = 1 before the unguarded InitiateAC transition can advance the mode.；For Ask_StartAC and AutocontrolInit, added pump_fault > 0 guard transitions route to PumpFault, preserving the NL requirement that pump faults activate alarm signals and that normal autocontrol proceeds only without pump-operation complicat...<truncated 5 chars>
- diff_summary：`{"summary": "Preserved the prior Manual fault-removal repair, added a Manual pump_fault guard self-transition before InitiateAC, added pump_fault fail-safe transitions from Ask_StartAC and AutocontrolInit to PumpFault, and made Ask_StartAC/AutocontrolInit entry actions fault-sensitive so active faults keep alarms active and software control released."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int control_released = 1;
def int infusion_log_records = 0;
def float patient_bp = 0.0;
def float target_bp = 100.0;
def float requested_target_bp = 100.0;
def float shared_sensor_buffer = 0.0;
def float manual_default_flow_rate = 1.0;
def float default_flow_rate = 1.0;
def float pressure_gain = 0.01;
def float flow_rate = 0.0;
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
        ! * -> Manual :: TerminateAC;

        >> during before { shared_sensor_buffer = patient_bp; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                if [pump_fault > 0] {
                    alarm_active = 1;
                } else {
                    alarm_active = 0;
                }
                control_released = 1;
            }
            during {
                pump_speed = manual_switch_speed;
                flow_rate = manual_default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 1;
                if [pump_fault > 0] {
                    alarm_active = 1;
                    control_released = 1;
                } else {
                    alarm_active = 0;
                }
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 2;
                if [pump_fault > 0] {
                    control_released = 1;
                    alarm_active = 1;
                } else {
                    control_released = 0;
                    alarm_active = 0;
                    flow_rate = default_flow_rate;
                }
            }
        }

        state Autocontrol {
            enter {
                CA_mode = 3;
                control_released = 0;
                alarm_active = 0;
            }
            during {
                if [pump_fault == 0] {
                    if [patient_bp > target_bp] {
                        flow_rate = default_flow_rate - ((patient_bp - target_bp) * pressure_gain);
                    } else {
                        flow_rate = default_flow_rate + ((target_bp - patient_bp) * pressure_gain);
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    infusion_log_records = infusion_log_records + 1;
                }
            }
        }

        state PumpFault {
            enter {
                CA_mode = 4;
                alarm_active = 1;
                control_released = 1;
            }
        }

        Manual -> Manual : /Mode_Control_Algorithm.PumpFault.FaultRemoved effect { pump_fault = 0; alarm_active = 0; };
        Manual -> Manual : if [pump_fault > 0] effect { alarm_active = 1; control_released = 1; };
        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> PumpFault : if [pump_fault > 0];
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> PumpFault : if [pump_fault > 0];
        AutocontrolInit -> Autocontrol;
        Autocontrol -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -48,16 +48,26 @@
         state Ask_StartAC {
             enter {
                 CA_mode = 1;
-                alarm_active = 0;
+                if [pump_fault > 0] {
+                    alarm_active = 1;
+                    control_released = 1;
+                } else {
+                    alarm_active = 0;
+                }
             }
         }
 
         state AutocontrolInit {
             enter {
                 CA_mode = 2;
-                control_released = 0;
-                alarm_active = 0;
-                flow_rate = default_flow_rate;
+                if [pump_fault > 0] {
+                    control_released = 1;
+                    alarm_active = 1;
+                } else {
+                    control_released = 0;
+                    alarm_active = 0;
+                    flow_rate = default_flow_rate;
+                }
             }
         }
 
@@ -89,10 +99,13 @@
             }
         }
 
+        Manual -> Manual : /Mode_Control_Algorithm.PumpFault.FaultRemoved effect { pump_fault = 0; alarm_active = 0; };
+        Manual -> Manual : if [pump_fault > 0] effect { alarm_active = 1; control_released = 1; };
         Manual -> Ask_StartAC :: InitiateAC;
-        Manual -> Manual : /Mode_Control_Algorithm.PumpFault.FaultRemoved effect { pump_fault = 0; alarm_active = 0; };
+        Ask_StartAC -> PumpFault : if [pump_fault > 0];
         Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
         Ask_StartAC -> AutocontrolInit :: StartAC;
+        AutocontrolInit -> PumpFault : if [pump_fault > 0];
         AutocontrolInit -> Autocontrol;
         Autocontrol -> PumpFault : if [pump_fault > 0];
         PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:6b5eb2b5ed8a4331621ef00e2ff89c6788aa5e0e13e934bd9f1ad846751a008b`。
  - SL-10 evidence 1: `{"summary": "Both current SL-7 hard-block requests are resolved. The unsafe_recovery and NL-fidelity findings identified that Manual->Ask_StartAC and Ask_StartAC->AutocontrolInit could proceed while pump_fault>0, and Ask_StartAC/AutocontrolInit entry actions could clear alarms or assert control before caregiver fault removal. The candidate preserves the required InitiateAC and StartAC transitions but adds ordered fail-safe behavior: a Manual self-transition when pump_fault>0 keeps the machine in Manual with alarm_active=1 and control_released=1; Ask_StartAC->PumpFault and AutocontrolInit->PumpFault guard transitions route active faults to PumpFault before normal autocontrol progression."}`
  - SL-10 evidence 2: `{"summary": "The candidate makes the autocontrol-initiation entry actions fault-sensitive. Ask_StartAC.enter now leaves alarm_active=1 and control_released=1 when pump_fault>0 instead of unconditionally clearing alarm_active. AutocontrolInit.enter now leaves control_released=1 and alarm_active=1 when pump_fault>0 instead of asserting software control and suppressing the alarm. This matches the NL obligations that pump faults activate alarm signals, caregiver removal precedes clearing the fault/alarm, and normal autocontrol controls flow only when there are no pump-operation complications."}`
  - SL-10 evidence 3: `{"summary": "The complete FixLog shows prior repairs were preserved. Manual.enter remains pump_fault-sensitive, so forced backManual recovery with an unresolved fault still keeps alarm_active=1. The Manual self-transition for /Mode_Control_Algorithm.PumpFault.FaultRemoved remains before the new pump_fault guard, so caregiver fault removal while already in Manual still clears pump_fault and alarm_active, preserving the previously repaired cp_and_cc_forced_back_manual scenario obligation."}`
  - SL-10 evidence 4: `{"summary": "The DSL diff is minimal and does not delete NL-required structure. CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, Autocontrol, PumpFault, all required variables, the root and Mode_Control initial transitions, InitiateAC, ChangeSetpoint with target_bp=requested_target_bp, StartAC, AutocontrolInit-to-Autocontrol, PumpFaultDetected guards, FaultRemoved, forced CA/CB/CP/CC_backManual transitions, TerminateAC, shared sensor buffering, manual pump control, autocontrol flow computation, control voltage/pump speed update, alarm activation, control release, and infusion logging all remain represented."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic evidence reports regression_detected=false and scenario_summary reports 10 scenarios with no coverage gap or weak oracle. The local failure is the same missing_required_grounding matcher objection for four elements that are visibly present in the DSL, not a reported behavioral regression against the current repair target."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:d48663b271a8682c7ee1717bf559731df76d03215d4145494e6940c0c7416d7a", "covered_local_objection_kinds": ["missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:692be568f04728d63d8c6dce685e3239bee2926e6575196a5d92c71b1bf7ddd6", "local_override_rationale_count": 3, "local_override_rationale_hash": "sha256:89cdd4abb728e89233bbd8fe61fc8dca5adfde28cb51d1780936bf1a6385940d", "local_rejection_evidence_hash": "sha256:e97c8cc2906c062efd7e8a3f29189bba88b834d5743232d51087cee1c7b8a110", "local_rejection_reason": "missing_required_grounding", "missing_local_objection_kinds": [], "policy": "SL-10 may override conservative ...<truncated 296 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:InitialRootToModeControl", "transition:InitialModeControlToManual", "action:SetTargetBloodPressure", "guard:PumpFaultDetected"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-f883b5485a5` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-f883b5485a5` | accept=1, reject=0 | `sl10_review` | `sha256:54fcdf1734e5639aa745de3c8846c7e22b53507fb28768bc8d6a2d53846a301c` | Accepted the unsafe_recovery repair request because the current Manual.enter unconditionally set alarm_active = 0 even when pump_fault remained 1 after a forced backManual transition., The smallest safe edit is local to Manual.enter: CA_mode still becomes Manual and control_released remains 1, but alarm_active is set to 1 whenever pump_fault > 0., This preserves the NL safety invariant that pump fault alarms remain active until the caregiver removes the fault., ... +2 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-f883b5485a5` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:54fcdf1734e5639aa745de3c8846c7e22b53507fb28768bc8d6a2d53846a301c` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-5adbf9ad4d9` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-5adbf9ad4d9` | accept=1, reject=0 | `sl10_review` | `sha256:5ff9d43b7100f6a2a25bd3b281247b1d0f8978779233f97647f7342ab4639666` | Accepted scenario cp_and_cc_forced_back_manual as the primary sim repair target., Failing step remove_fault_before_new_autocontrol_attempt expected state CARA.Mode_Control_Algorithm.Manual with pump_fault=0 and alarm_active=0 after event CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved, but actual state was already Manual with pump_fault=1 and alarm_active=1. The added Manual self-transition listens to the existing absolute PumpFault.FaultRemoved event and clears pump_fault and alarm_active, so Manual.enter then keeps alarm_active=0 because pump_fault is 0., Failing step cc_backmanual_from_autocontrol_init expected Manual with alarm_active=0, but actual alarm_active remained 1 because the previous FaultRemoved event had not cleared pump_fault. Once the new Manual self-transition clears pump_fault in step 1, later CC_backManual re-enters Manual with pump_fault=0 and Manual.enter sets alarm_active=0., ... +2 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-5adbf9ad4d9` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:5ff9d43b7100f6a2a25bd3b281247b1d0f8978779233f97647f7342ab4639666` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 7 | `2` | `request_batch` | `fixbatch-2-sha256-fdd92baad50` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 8 | `2` | `sl9_decision` | `fixbatch-2-sha256-fdd92baad50` | accept=2, reject=0 | `sl10_review` | `sha256:d48663b271a8682c7ee1717bf559731df76d03215d4145494e6940c0c7416d7a` | Both current SL-7 requests are accepted because they provide new hard model-review evidence after the earlier scenario repair: active pump faults could still be bypassed during autocontrol initiation., The previous non-regressive behavior is preserved: Manual.enter remains pump_fault-sensitive, so forced backManual recovery with pump_fault > 0 still keeps alarm_active = 1; the Manual FaultRemoved self-transition remains before the new guard so caregiver fault removal in Manual still clears pump_fault and alarm_active., Because pyfcstm cannot mix an event and a guard on the same transition, the required Manual -> Ask_StartAC :: InitiateAC and Ask_StartAC -> AutocontrolInit :: StartAC event transitions are preserved, and small ordered guard fail-safes are added instead., ... +4 |
| 9 | `2` | `sl10_review` | `fixbatch-2-sha256-fdd92baad50` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:d48663b271a8682c7ee1717bf559731df76d03215d4145494e6940c0c7416d7a` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +4 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5334, 'completion_chars': 20802, 'completion_tokens': 7385, 'elapsed_seconds': 135.88635911501478, 'estimated_completion_tokens': 5201, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11858, 'first_chunk_seconds': 39.621242968016304, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13835}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2636, 'completion_chars': 10612, 'completion_tokens': 4214, 'elapsed_seconds': 79.02822419302538, 'estimated_completion_tokens': 2653, 'estimated_prompt_tokens': 15366, 'estimated_total_tokens': 18019, 'first_chunk_seconds': 31.009873091010377, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 61464, 'prompt_tokens': 15079, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 19293}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1976, 'completion_chars': 9234, 'completion_tokens': 2951, 'elapsed_seconds': 56.21029340600944, 'estimated_completion_tokens': 2309, 'estimated_prompt_tokens': 19976, 'estimated_total_tokens': 22285, 'first_chunk_seconds': 19.820096709008794, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 79903, 'prompt_tokens': 20010, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22961}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1188, 'completion_chars': 5077, 'completion_tokens': 1521, 'elapsed_seconds': 31.171759482007474, 'estimated_completion_tokens': 1270, 'estimated_prompt_tokens': 22499, 'estimated_total_tokens': 23769, 'first_chunk_seconds': 9.97175784999854, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 89996, 'prompt_tokens': 21241, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22762}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 816, 'completion_chars': 3931, 'completion_tokens': 1063, 'elapsed_seconds': 23.160941743990406, 'estimated_completion_tokens': 983, 'estimated_prompt_tokens': 19512, 'estimated_total_tokens': 20495, 'first_chunk_seconds': 8.264520370983519, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 78046, 'prompt_tokens': 18114, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 19177}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2793, 'completion_chars': 11252, 'completion_tokens': 3287, 'elapsed_seconds': 62.36591252699145, 'estimated_completion_tokens': 2813, 'estimated_prompt_tokens': 20539, 'estimated_total_tokens': 23352, 'first_chunk_seconds': 12.07380106599885, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 82154, 'prompt_tokens': 20278, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23565}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3317, 'completion_chars': 13383, 'completion_tokens': 4511, 'elapsed_seconds': 83.52895889099455, 'estimated_completion_tokens': 3346, 'estimated_prompt_tokens': 20792, 'estimated_total_tokens': 24138, 'first_chunk_seconds': 24.261911684006918, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 83168, 'prompt_tokens': 20439, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24950}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1463, 'completion_chars': 6312, 'completion_tokens': 2258, 'elapsed_seconds': 43.81108304200461, 'estimated_completion_tokens': 1578, 'estimated_prompt_tokens': 45440, 'estimated_total_tokens': 47018, 'first_chunk_seconds': 17.352181124006165, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 181758, 'prompt_tokens': 41784, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 44042}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1085, 'completion_chars': 4979, 'completion_tokens': 1391, 'elapsed_seconds': 32.0355255479808, 'estimated_completion_tokens': 1245, 'estimated_prompt_tokens': 44255, 'estimated_total_tokens': 45500, 'first_chunk_seconds': 12.637688991002506, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 177018, 'prompt_tokens': 39787, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 41178}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3317, 'completion_chars': 13383, 'completion_tokens': 3836, 'elapsed_seconds': 72.67642809299286, 'estimated_completion_tokens': 3346, 'estimated_prompt_tokens': 21681, 'estimated_total_tokens': 25027, 'first_chunk_seconds': 12.888920278986916, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 86721, 'prompt_tokens': 21568, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25404}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2315, 'completion_chars': 10371, 'completion_tokens': 2834, 'elapsed_seconds': 54.37903536099475, 'estimated_completion_tokens': 2593, 'estimated_prompt_tokens': 23660, 'estimated_total_tokens': 26253, 'first_chunk_seconds': 12.664274943992496, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 94638, 'prompt_tokens': 23806, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26640}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1822, 'completion_chars': 8003, 'completion_tokens': 2859, 'elapsed_seconds': 56.42021573401871, 'estimated_completion_tokens': 2001, 'estimated_prompt_tokens': 69976, 'estimated_total_tokens': 71977, 'first_chunk_seconds': 23.4517609620234, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 279901, 'prompt_tokens': 63400, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 66259}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1050, 'completion_chars': 5124, 'completion_tokens': 1496, 'elapsed_seconds': 30.501378286018735, 'estimated_completion_tokens': 1281, 'estimated_prompt_tokens': 69386, 'estimated_total_tokens': 70667, 'first_chunk_seconds': 11.825923408003291, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 277541, 'prompt_tokens': 62136, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 63632}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4252, 'completion_chars': 17218, 'completion_tokens': 5170, 'elapsed_seconds': 97.14776286200504, 'estimated_completion_tokens': 4305, 'estimated_prompt_tokens': 24423, 'estimated_total_tokens': 28728, 'first_chunk_seconds': 19.685910711996257, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 97690, 'prompt_tokens': 24288, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 29458}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5025, 'completion_chars': 20278, 'completion_tokens': 5967, 'elapsed_seconds': 110.26516958401771, 'estimated_completion_tokens': 5070, 'estimated_prompt_tokens': 25382, 'estimated_total_tokens': 30452, 'first_chunk_seconds': 19.9135846850113, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 101525, 'prompt_tokens': 25223, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 31190}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1780, 'completion_chars': 8539, 'completion_tokens': 2299, 'elapsed_seconds': 44.89806745998794, 'estimated_completion_tokens': 2135, 'estimated_prompt_tokens': 27098, 'estimated_total_tokens': 29233, 'first_chunk_seconds': 12.815122174011776, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 108389, 'prompt_tokens': 27270, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 29569}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success_but_weak_oracle_ineligible`。
- required stages executed：`54/16`，missing=`<none>`。
- repairs：`3/3` accepted；scenario_history=`9`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
