## path1 / cara-infusion-pump-formal-spec__01 / default 真实运行结果：Path1 CARA representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`not_converged`；record_status：`rejected`；result_status：`not_converged`。
- main_result_eligible：`false`。
- Path2 ref-model blueprint eligible：`n/a`；reason：not_applicable_to_path1。
- 一句话结论：`scenario_or_sim_oracle`；停止原因：SD-6 sim failure: 13/15 scenarios passed。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `cara-infusion-pump-formal-spec__01` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `min_sl10_rework_attempts=1`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `587af294f48e3b174169d015f59c390061347841` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d` |
| final verdict/status | verdict=`not_converged`, record=`rejected`, result=`not_converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:ca64688a961882c80131f3555091a4127ad0655a7da625098e2baebf67ee5145", "iteration": 1, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "iteration": 2, "repair_history_index": 2, "rework_instructions": null, "same_as_final": false, "sl10_decision": null}, "matching_repair_history_indices": [1], "repair_history_index": 1, "selected_source_stage": "SL-7", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, reject_or_waiver, exit_rejected` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, SD-6 sim failure: 13/15 scenarios passed` |
| token/cost/time | tokens=`{'prompt_tokens': 297141, 'completion_tokens': 32970, 'total_tokens': 330111, 'estimated_prompt_tokens': 330783, 'estimated_completion_tokens': 26421, 'estimated_total_tokens': 357204, 'prompt_chars': 1323119, 'completion_chars': 105667, 'n_calls': 11, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`630.858s` |
| run record | [`pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:f77cdc40f2038a0f920e19963516ec29d8ceb538080157c0318616790fc25f67` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `66` |
| `langgraph_node_trace_hash` | `sha256:b8d5a7d5ae3859156f87d13d1275354c7e3a12372a6db898ef4e61160c826d28` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `66` |

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
def int blood_pressure = 0;
def int shared_bp_buffer = 0;
def int target_bp = 100;
def int setpoint_delta = 0;
def int default_flow_rate = 0;
def int flow_rate = 0;
def int built_in_switch = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! AutocontrolInit -> Fault :: PumpFault;
        ! AutocontrolNormal -> Fault :: PumpFault;

        >> during before { shared_bp_buffer = blood_pressure; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                pump_control = 0;
                alarm_signal = pump_fault;
            }
            during {
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                target_bp = target_bp + setpoint_delta;
                setpoint_delta = 0;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                pump_control = 1;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                pump_control = 1;
            }
            during {
                if [pump_fault == 0] {
                    if [blood_pressure > target_bp] {
                        flow_rate = default_flow_rate - (blood_pressure - target_bp);
                    } else {
                        flow_rate = default_flow_rate + (target_bp - blood_pressure);
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_count = log_count + 1;
                }
            }
        }

        state Fault {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                pump_control = 0;
                CA_mode = 0;
            }
            during {
                alarm_signal = 1;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual :: TerminateAC;
        Fault -> Manual :: FaultCleared effect {
            pump_fault = 0;
            alarm_signal = 0;
            pump_control = 0;
            CA_mode = 0;
        };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12714 | 生成初始 DSL 与 grounding seeds | initial len=2747 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=89439 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=146270 | LLM per-request accept/reject + repair | candidate len=2747,2756,0 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=58743 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=89439 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=1, tokens=22945 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=146270 | LLM per-request accept/reject + repair | candidate len=2747,2756,0 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=58743 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=89439 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=89439 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=146270 | LLM per-request accept/reject + repair | candidate len=2747,2756,0 | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SD-6 sim failure: 13/15 scenarios passed | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e3-toolnode-20260605T192811Z-3e86ba8d.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T19:28:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T19:28:12Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T19:28:12Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T19:28:12Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T19:30:08Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T19:30:08Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2747,hash=sha256:5a35b49645c8 |
| 7 | `2026-06-05T19:30:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T19:30:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T19:30:08Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:5a35b49645c80d4a32869513ed1d5e4077093cba593515fc233813beb5dafbb3 |
| 10 | `2026-06-05T19:30:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T19:30:08Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2747,hash=sha256:5a35b49645c8, current_hash=sha256:5a35b49645c80d4a32869513ed1d5e4077093cba593515fc233813beb5dafbb3 |
| 12 | `2026-06-05T19:30:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T19:30:08Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T19:30:09Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T19:30:09Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T19:30:09Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T19:30:09Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T19:30:09Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T19:30:09Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T19:30:09Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T19:30:09Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T19:30:09Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T19:30:56Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T19:30:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T19:30:56Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-05T19:30:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T19:30:56Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-05T19:30:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-05T19:30:56Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-05T19:30:56Z` | `SD-6` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 31 | `2026-06-05T19:30:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T19:30:56Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 9, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 33 | `2026-06-05T19:30:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 34 | `2026-06-05T19:30:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T19:30:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 36 | `2026-06-05T19:30:56Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 9, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2747,hash=sha256:5a35b49645c8 |
| 37 | `2026-06-05T19:30:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 38 | `2026-06-05T19:30:56Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 39 | `2026-06-05T19:30:56Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 40 | `2026-06-05T19:30:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-05T19:30:56Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2747,hash=sha256:5a35b49645c8 |
| 42 | `2026-06-05T19:31:27Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 43 | `2026-06-05T19:31:27Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd6-0-a0046eb538"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2747,hash=sha256:cc3368769b53 |
| 44 | `2026-06-05T19:31:27Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-05T19:31:27Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 46 | `2026-06-05T19:31:27Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:cc3368769b53194be765d34e1bc7f636ef59487970939701746e6bfcf790a33d |
| 47 | `2026-06-05T19:31:49Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 48 | `2026-06-05T19:31:49Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 49 | `2026-06-05T19:31:49Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 50 | `2026-06-05T19:31:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 51 | `2026-06-05T19:31:49Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2747,hash=sha256:cc3368769b53 |
| 52 | `2026-06-05T19:31:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 53 | `2026-06-05T19:31:49Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:cc3368769b53194be765d34e1bc7f636ef59487970939701746e6bfcf790a33d |
| 54 | `2026-06-05T19:31:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 55 | `2026-06-05T19:31:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 56 | `2026-06-05T19:31:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 57 | `2026-06-05T19:31:49Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:cc3368769b53194be765d34e1bc7f636ef59487970939701746e6bfcf790a33d |
| 58 | `2026-06-05T19:31:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 59 | `2026-06-05T19:31:49Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=2747,hash=sha256:cc3368769b53, current_hash=sha256:cc3368769b53194be765d34e1bc7f636ef59487970939701746e6bfcf790a33d |
| 60 | `2026-06-05T19:31:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 61 | `2026-06-05T19:31:49Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 62 | `2026-06-05T19:31:49Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 63 | `2026-06-05T19:31:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 64 | `2026-06-05T19:31:49Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 65 | `2026-06-05T19:31:49Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 66 | `2026-06-05T19:31:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 67 | `2026-06-05T19:31:49Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 68 | `2026-06-05T19:31:49Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-5A", "ok": true, "status": "StageStatus.OK"} | <none> |
| 69 | `2026-06-05T19:31:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 70 | `2026-06-05T19:31:50Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 targeted_retry", "ok": false, "reason": "reuse_frozen_scenario_set"} | <none> |
| 71 | `2026-06-05T19:31:50Z` | `<control>` | `1` | `frozen_scenario_refresh_targeted_retry` | {} | <none> |
| 72 | `2026-06-05T19:31:50Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 73 | `2026-06-05T19:31:50Z` | `SL-5` | `1` | `stage_enter` | {"reason": "targeted_refresh_after_frozen_gap_or_dsl_change"} | <none> |
| 74 | `2026-06-05T19:32:55Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 75 | `2026-06-05T19:32:55Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 76 | `2026-06-05T19:32:56Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 77 | `2026-06-05T19:32:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 78 | `2026-06-05T19:32:56Z` | `SC-5F` | `1` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": "refreshed_scenario_set"} | <none> |
| 79 | `2026-06-05T19:32:56Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 80 | `2026-06-05T19:32:56Z` | `SD-6` | `1` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
- ……另有 `84` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-6` | yes | fixbatch-0-sha256-d4aa49fcb84 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SL-7` | yes | fixbatch-1-sha256-2a073349d05 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SD-6` | yes | fixbatch-2-sha256-0cbbf437fe0 / n=2 | accept=0, reject=2, waiver=0 | <none> | decision=None, ok=False, target=False, regression=False, drift=major, rework=<none> | no | SD-6 sim failure: 13/15 scenarios passed |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| `default_init_manual_mode_outputs` | default-init dispatches into Manual and verifies manual pump-speed/flow plus shared BP buffer behavior. | ✅ | ✅ | ✅ |
| `manual_initiate_to_ask_startac_and_setpoint_change` | explicit-hot-start in Manual probes InitiateAC target and Ask_StartAC setpoint update before StartAC. | ✅ | ✅ | ✅ |
| `ask_startac_to_autocontrol_normal_high_pressure` | explicit-hot-start in Ask_StartAC verifies StartAC enters AutocontrolInit, then normal autocontrol lowers flow for high ...<truncated 3 chars> | ✅ | ✅ | ✅ |
| `autocontrol_normal_low_pressure_and_terminate` | explicit-hot-start in AutocontrolNormal verifies low BP raises flow, logging occurs, and TerminateAC returns to Manual. | ✅ | ✅ | ✅ |
| `autocontrol_normal_pump_fault_then_clear` | explicit-hot-start in AutocontrolNormal verifies PumpFault enters Fault with alarm/release, then FaultCleared returns Ma...<truncated 5 chars> | ✅ | ✅ | ✅ |
| `autocontrol_init_terminate_and_pump_fault_paths` | explicit-hot-start in AutocontrolInit covers local TerminateAC recovery to Manual before normal autocontrol is reached. | ❌ | ✅ | ✅ |
| `pump_fault_from_autocontrol_init` | explicit-hot-start in AutocontrolInit verifies PumpFault also forces Fault before normal autocontrol is reached. | ✅ | ✅ | ✅ |
| `back_manual_forced_recovery_from_ask_and_normal` | explicit-hot-start probes cross-component backManual fallback from Ask_StartAC and AutocontrolNormal to shared Manual ta...<truncated 5 chars> | ✅ | ✅ | ✅ |
| `back_manual_forced_recovery_from_fault_and_init` | explicit-hot-start probes CP/CC backManual fallback from Fault and from AutocontrolInit to Manual. | ✅ | ✅ | ❌ |
| `standalone_forced_backmanual_ca_and_cb_lines` | explicit-hot-start isolates CA_backManual and CB_backManual wildcard forced recovery lines from non-Manual leaves so a m...<truncated 57 chars> | ⚪ | ⚪ | ✅ |
| `standalone_forced_backmanual_cp_and_cc_lines` | explicit-hot-start isolates CP_backManual and CC_backManual wildcard forced recovery lines from Fault and AutocontrolIni...<truncated 68 chars> | ⚪ | ⚪ | ❌ |
| `forced_backmanual_ca_from_manual_reenters_and_recovers_outputs` | explicit-hot-start in Manual with poisoned control/alarm variables verifies CA_backManual is a real wildcard forced tran...<truncated 52 chars> | ⚪ | ⚪ | ✅ |
| `forced_backmanual_cb_from_manual_reenters_and_recovers_outputs` | explicit-hot-start in Manual with poisoned control/alarm variables verifies CB_backManual is not ignored when the source...<truncated 46 chars> | ⚪ | ⚪ | ✅ |
| `forced_backmanual_cp_from_manual_reenters_and_recovers_outputs` | explicit-hot-start in Manual with poisoned control/alarm variables verifies CP_backManual is a real forced fallback line...<truncated 30 chars> | ⚪ | ⚪ | ✅ |
| `forced_backmanual_cc_from_manual_reenters_and_recovers_outputs` | explicit-hot-start in Manual with poisoned control/alarm variables verifies CC_backManual is a real forced fallback line...<truncated 30 chars> | ⚪ | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_mode_outputs` — default-init dispatches into Manual and verifies manual pump-speed/flow plus shared BP buffer behavior.</summary>

| Field | Value |
|---|---|
| description | default-init dispatches into Manual and verifies manual pump-speed/flow plus shared BP buffer behavior. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 85, "built_in_switch": 7, "default_flow_rate": 12}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 12, "pump_control": 0, "pump_speed": 7, "shared_bp_buffer": 85}` |

</details>

<details><summary>`manual_initiate_to_ask_startac_and_setpoint_change` — explicit-hot-start in Manual probes InitiateAC target and Ask_StartAC setpoint update before StartAC.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Manual probes InitiateAC target and Ask_StartAC setpoint update before StartAC. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"setpoint_delta": 5, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiate_enters_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"setpoint_delta": 0, "target_bp": 105}` |
| 1 `no_start_stays_in_ask_startac` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"setpoint_delta": 0, "target_bp": 105}` |

</details>

<details><summary>`ask_startac_to_autocontrol_normal_high_pressure` — explicit-hot-start in Ask_StartAC verifies StartAC enters AutocontrolInit, then normal autocontrol lowers flow for high BP.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Ask_StartAC verifies StartAC enters AutocontrolInit, then normal autocontrol lowers flow for high BP. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"blood_pressure": 120, "default_flow_rate": 50, "log_count": 0, "pump_fault": 0, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `start_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "pump_control": 1}` |
| 1 `init_progresses_to_normal_and_computes_lower_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 1, "control_voltage": 30, "flow_rate": 30, "log_count": 1, "pump_control": 1, "pump_speed": 30, "shared_bp_buffer": 120}` |

</details>

<details><summary>`autocontrol_normal_low_pressure_and_terminate` — explicit-hot-start in AutocontrolNormal verifies low BP raises flow, logging occurs, and TerminateAC returns to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal verifies low BP raises flow, logging occurs, and TerminateAC returns to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"blood_pressure": 80, "built_in_switch": 4, "default_flow_rate": 50, "log_count": 2, "pump_fault": 0, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `normal_controls_flow_for_low_pressure` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 70, "flow_rate": 70, "log_count": 3, "pump_speed": 70, "shared_bp_buffer": 80}` |
| 1 `terminate_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolNormal.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 50, "pump_control": 0, "pump_speed": 4}` |

</details>

<details><summary>`autocontrol_normal_pump_fault_then_clear` — explicit-hot-start in AutocontrolNormal verifies PumpFault enters Fault with alarm/release, then FaultCleared returns Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal verifies PumpFault enters Fault with alarm/release, then FaultCleared returns Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "built_in_switch": 3, "default_flow_rate": 10, "pump_control": 1, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `pump_fault_enters_fault` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolNormal.PumpFault"]` | `CARA.Mode_Control_Algorithm.Fault` | `{"CA_mode": 0, "alarm_signal": 1, "pump_control": 0, "pump_fault": 1}` |
| 1 `fault_cleared_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.Fault.FaultCleared"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 10, "pump_control": 0, "pump_fault": 0, "pump_speed": 3}` |

</details>

<details><summary>`autocontrol_init_terminate_and_pump_fault_paths` — explicit-hot-start in AutocontrolInit covers local TerminateAC recovery to Manual before normal autocontrol is reached.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolInit covers local TerminateAC recovery to Manual before normal autocontrol is reached. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "built_in_switch": 6, "default_flow_rate": 20, "pump_control": 1, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_from_init_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolInit.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 20, "pump_control": 0, "pump_speed": 6}` |

</details>

<details><summary>`pump_fault_from_autocontrol_init` — explicit-hot-start in AutocontrolInit verifies PumpFault also forces Fault before normal autocontrol is reached.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolInit verifies PumpFault also forces Fault before normal autocontrol is reached. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "pump_control": 1, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `pump_fault_from_init_enters_fault` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolInit.PumpFault"]` | `CARA.Mode_Control_Algorithm.Fault` | `{"CA_mode": 0, "alarm_signal": 1, "pump_control": 0, "pump_fault": 1}` |

</details>

<details><summary>`back_manual_forced_recovery_from_ask_and_normal` — explicit-hot-start probes cross-component backManual fallback from Ask_StartAC and AutocontrolNormal to shared Manual target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes cross-component backManual fallback from Ask_StartAC and AutocontrolNormal to shared Manual target. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "blood_pressure": 100, "built_in_switch": 2, "default_flow_rate": 9, "pump_control": 1, "pump_fault": 0, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_from_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 9, "pump_control": 0, "pump_speed": 2}` |
| 1 `move_to_ask_for_normal_prefix` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 2 `start_to_init_for_normal_prefix` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "pump_control": 1}` |
| 3 `progress_to_normal_for_backmanual_probe` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 1, "pump_control": 1}` |
| 4 `cb_backmanual_from_autocontrol_normal` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 9, "pump_control": 0, "pump_speed": 2}` |

</details>

<details><summary>`back_manual_forced_recovery_from_fault_and_init` — explicit-hot-start probes CP/CC backManual fallback from Fault and from AutocontrolInit to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes CP/CC backManual fallback from Fault and from AutocontrolInit to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.Fault` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "built_in_switch": 8, "default_flow_rate": 15, "pump_control": 1, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_from_fault` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 15, "pump_control": 0, "pump_speed": 8}` |
| 1 `move_to_ask_for_init_prefix` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 2 `start_to_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "pump_control": 1}` |
| 3 `cc_backmanual_from_init` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 15, "pump_control": 0, "pump_speed": 8}` |

</details>

<details><summary>`standalone_forced_backmanual_ca_and_cb_lines` — explicit-hot-start isolates CA_backManual and CB_backManual wildcard forced recovery lines from non-Manual leaves so a missing forced line is observed as a stat...<truncated 17 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start isolates CA_backManual and CB_backManual wildcard forced recovery lines from non-Manual leaves so a missing forced line is observed as a state/output failure. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "blood_pressure": 100, "built_in_switch": 11, "default_flow_rate": 21, "pump_control": 1, "pump_fault": 0, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_forces_manual_from_ask` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 21, "pump_control": 0, "pump_speed": 11}` |
| 1 `return_to_ask_after_ca_probe` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 2 `enter_init_for_cb_probe` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "pump_control": 1}` |
| 3 `progress_to_normal_for_cb_probe` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 1, "pump_control": 1}` |
| 4 `cb_backmanual_forces_manual_from_normal` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 21, "pump_control": 0, "pump_speed": 11}` |

</details>

<details><summary>`standalone_forced_backmanual_cp_and_cc_lines` — explicit-hot-start isolates CP_backManual and CC_backManual wildcard forced recovery lines from Fault and AutocontrolInit so a missing forced line cannot be hid...<truncated 28 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start isolates CP_backManual and CC_backManual wildcard forced recovery lines from Fault and AutocontrolInit so a missing forced line cannot be hidden by other recovery paths. |
| initial_state | `CARA.Mode_Control_Algorithm.Fault` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "blood_pressure": 100, "built_in_switch": 12, "default_flow_rate": 22, "pump_control": 1, "pump_fault": 1, "target_bp": 100}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_forces_manual_from_fault` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 22, "pump_control": 0, "pump_speed": 12}` |
| 1 `return_to_ask_after_cp_probe` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 2 `enter_init_for_cc_probe` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "pump_control": 1}` |
| 3 `cc_backmanual_forces_manual_from_init` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 22, "pump_control": 0, "pump_speed": 12}` |

</details>

<details><summary>`forced_backmanual_ca_from_manual_reenters_and_recovers_outputs` — explicit-hot-start in Manual with poisoned control/alarm variables verifies CA_backManual is a real wildcard forced transition even when the target state is alr...<truncated 12 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Manual with poisoned control/alarm variables verifies CA_backManual is a real wildcard forced transition even when the target state is already Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "built_in_switch": 13, "default_flow_rate": 23, "pump_control": 1, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_reenters_manual_and_clears_control` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 23, "pump_control": 0, "pump_speed": 13}` |

</details>

<details><summary>`forced_backmanual_cb_from_manual_reenters_and_recovers_outputs` — explicit-hot-start in Manual with poisoned control/alarm variables verifies CB_backManual is not ignored when the source is already the shared Manual recovery t...<truncated 6 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Manual with poisoned control/alarm variables verifies CB_backManual is not ignored when the source is already the shared Manual recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "built_in_switch": 14, "default_flow_rate": 24, "pump_control": 1, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_reenters_manual_and_clears_control` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 24, "pump_control": 0, "pump_speed": 14}` |

</details>

<details><summary>`forced_backmanual_cp_from_manual_reenters_and_recovers_outputs` — explicit-hot-start in Manual with poisoned control/alarm variables verifies CP_backManual is a real forced fallback line from the Manual leaf as well.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Manual with poisoned control/alarm variables verifies CP_backManual is a real forced fallback line from the Manual leaf as well. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "built_in_switch": 15, "default_flow_rate": 25, "pump_control": 1, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_reenters_manual_and_clears_control` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 25, "pump_control": 0, "pump_speed": 15}` |

</details>

<details><summary>`forced_backmanual_cc_from_manual_reenters_and_recovers_outputs` — explicit-hot-start in Manual with poisoned control/alarm variables verifies CC_backManual is a real forced fallback line from the Manual leaf as well.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Manual with poisoned control/alarm variables verifies CC_backManual is a real forced fallback line from the Manual leaf as well. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "built_in_switch": 16, "default_flow_rate": 26, "pump_control": 1, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_backmanual_reenters_manual_and_clears_control` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 26, "pump_control": 0, "pump_speed": 16}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | autocontrol_init_terminate_and_pump_fault_paths | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:cc3368769b53194be765d34e1bc7f636ef59487970939701746e6bfcf790a33d` |
| 2 | `1` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:ca64688a961882c80131f3555091a4127ad0655a7da625098e2baebf67ee5145` |
| 3 | `2` | ❌ | `SD-6` | back_manual_forced_recovery_from_fault_and_init, standalone_forced_backmanual_cp_and_cc_lines | accept=0, reject=2, waiver=0 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

<details><summary>Repair 1 / iteration `0` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`autocontrol_init_terminate_and_pump_fault_paths`。
- before_dsl_hash：`sha256:5a35b49645c80d4a32869513ed1d5e4077093cba593515fc233813beb5dafbb3`；candidate_dsl_hash：`sha256:cc3368769b53194be765d34e1bc7f636ef59487970939701746e6bfcf790a33d`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-d4aa49fcb84`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-a0046eb538` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start in AutocontrolInit covers local TerminateAC to Manual and PumpFault forced transition to Fault from init.', 'name': 'autocontrol_init_terminate_and_pump_fault_paths', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start in AutocontrolInit covers local TerminateAC to Manual and PumpFault forced transition to Fault from init.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'flow_rate': 120, 'pump_control': 1, 'pump_speed': 120}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.AutocontrolInit.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'flow_rate': 20, 'pump_control': 0, 'pump_speed': 6}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'terminate_from_init_returns_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 120, 'expected': 20}, 'pump_control': {'actual': 1, 'expected': 0}, 'pump_speed': {'actual': 120, 'expected': 6}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 0, 'built_in_switch': 6, 'default_flow_rate': 20, 'pump_control': 1, 'pump_fault': 0}, 'scenario_name': 'autocontrol_init_terminate_and_pump_fault_paths', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 0, 'built_in_switch': 6, 'control_voltage': 120, 'default_flow_rate': 20, 'flow_rate': 120, 'log_count': 1, 'pump_control': 1, 'pump_fault': 0, 'pump_speed': 120, 'setpoint_delta': 0, 'shared_bp_buffer': 0, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'terminate_from_init_returns_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 120, 'expected': 20}, 'pump_control': {'actual': 1, 'expected': 0}, 'pump_speed': {'actual': 120, 'expected': 6}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:Fault, event:InitiateAC, event:StartAC, event:TerminateAC, event:PumpFault, event:FaultCleared, event:CA_backManual, ... +26`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2747`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-a0046eb538` | `accept` | ❌ | ❌ | The failing scenario autocontrol_init_terminate_and_pump_fault_paths hot-starts in AutocontrolInit and injects the local AutocontrolInit.TerminateAC event. The current DSL has an unconditional AutocontrolInit -> AutocontrolNormal transition listed before the TerminateAC transition, so the unconditional transition fires first and prevents return to Manual. Th...<truncated 272 chars> |
- repair_rationale：For scenario autocontrol_init_terminate_and_pump_fault_paths, failing step terminate_from_init_returns_manual expected state CARA.Mode_Control_Algorithm.Manual with CA_mode=0, pump_control=0, alarm_signal=0, pump_speed=6, and flow_rate=20, ...<truncated 109 chars>；The root cause is transition priority/order in AutocontrolInit: the unconditional AutocontrolInit -> AutocontrolNormal transition was considered before the local TerminateAC event transition, so the event was effectively bypassed.；The smallest safe edit is to place AutocontrolInit -> Manual :: TerminateAC before the unconditional AutocontrolInit -> AutocontrolNormal transition. When TerminateAC is injected while AutocontrolInit is active, Manual is entered and its du...<truncated 113 chars>；This preserves the grounded AutocontrolInit-to-AutocontrolNormal progression for cycles without TerminateAC, preserves the existing PumpFault forced transition from AutocontrolInit to Fault, and keeps all required states, events, variables,...<truncated 33 chars>
- diff_summary：`{"summary": "Reordered AutocontrolInit outgoing transitions so the local TerminateAC transition to Manual is listed before the unconditional transition to AutocontrolNormal; no grounded elements were deleted."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int blood_pressure = 0;
def int shared_bp_buffer = 0;
def int target_bp = 100;
def int setpoint_delta = 0;
def int default_flow_rate = 0;
def int flow_rate = 0;
def int built_in_switch = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! AutocontrolInit -> Fault :: PumpFault;
        ! AutocontrolNormal -> Fault :: PumpFault;

        >> during before { shared_bp_buffer = blood_pressure; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                pump_control = 0;
                alarm_signal = 0;
            }
            during {
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                target_bp = target_bp + setpoint_delta;
                setpoint_delta = 0;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                pump_control = 1;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                pump_control = 1;
            }
            during {
                if [pump_fault == 0] {
                    if [blood_pressure > target_bp] {
                        flow_rate = default_flow_rate - (blood_pressure - target_bp);
                    } else {
                        flow_rate = default_flow_rate + (target_bp - blood_pressure);
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_count = log_count + 1;
                }
            }
        }

        state Fault {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                pump_control = 0;
                CA_mode = 0;
            }
            during {
                alarm_signal = 1;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual :: TerminateAC;
        Fault -> Manual :: FaultCleared effect {
            pump_fault = 0;
            alarm_signal = 0;
            pump_control = 0;
            CA_mode = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -87,8 +87,8 @@
 
         Manual -> Ask_StartAC :: InitiateAC;
         Ask_StartAC -> AutocontrolInit :: StartAC;
+        AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolInit -> AutocontrolNormal;
-        AutocontrolInit -> Manual :: TerminateAC;
         AutocontrolNormal -> Manual :: TerminateAC;
         Fault -> Manual :: FaultCleared effect {
             pump_fault = 0;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:8c63222164482a57c456c5b0fd02d75e1ec49c35320ad1d51c5ed5b96075a4ce`。
  - SL-10 evidence 1: `{"summary": "The hard SD-6 simulation request was for scenario autocontrol_init_terminate_and_pump_fault_paths, step terminate_from_init_returns_manual: from hot-start AutocontrolInit with TerminateAC, expected Manual with CA_mode=0, pump_control=0, alarm_signal=0, pump_speed=6, and flow_rate=20, but old DSL took the unconditional AutocontrolInit -> AutocontrolNormal first and produced CA_mode=1, pump_control=1, pump_speed=120, flow_rate=120. SL-9 accepted this as a transition-priority defect and made the minimal edit: AutocontrolInit -> Manual :: TerminateAC is now ordered before AutocontrolInit -> AutocontrolNormal. This directly addresses the scenario mechanism without deleting any requir...<truncated 46 chars>`
  - SL-10 evidence 2: `{"summary": "The NL supports this behavior: the Caregiver Interface can terminate algorithmic pump control, and manual operation is the recovery target with CA_mode Manual, pump_control released, pump speed from built_in_switch, and flow_rate from default_flow_rate. The candidate preserves Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, Fault, InitiateAC, StartAC, TerminateAC, PumpFault, FaultCleared, the four backManual events, CA_mode and pump variables, shared BP buffer, target setpoint modification, normal autocontrol flow computation, no-pump-fault guard, alarm/release behavior, and fault/backManual recovery transitions."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is limited to reordering two AutocontrolInit outgoing transitions. It preserves the unconditional AutocontrolInit -> AutocontrolNormal progression when no TerminateAC is present, preserves forced PumpFault transitions from AutocontrolInit and AutocontrolNormal to Fault, and preserves all four forced backManual transitions to Manual."}`
  - SL-10 evidence 4: `{"summary": "Local deterministic evidence reports no scenario regression, but rejects on missing_required_grounding for transition:Autocontrol_to_Fault_PumpFault, transition:Forced_backManual_to_Manual, and guard:no_pump_fault. Manual inspection of the candidate DSL shows these elements are concretely present: ! AutocontrolNormal -> Fault :: PumpFault represents the required autocontrol fault transition; ! * -> Manual :: CA_backManual, CB_backManual, CP_backManual, and CC_backManual represent the forced shared recovery target; and AutocontrolNormal.during contains if [pump_fault == 0], the required no-pump-operation-complication guard."}`
  - SL-10 evidence 5: `{"candidate_dsl_hash": "sha256:cc3368769b53194be765d34e1bc7f636ef59487970939701746e6bfcf790a33d", "covered_local_objection_kinds": ["missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:003676388679c5aa21775dfe6778f0a300a3040b95f2f6e79683f416c6977e5b", "local_override_rationale_count": 2, "local_override_rationale_hash": "sha256:0405180f7c1d4c3288acb5be464a59e793cc43570b5a5327aa6f1c3110df91cd", "local_rejection_evidence_hash": "sha256:c92cb0a4d16181d695112b13f885cab33bbf84e09ce69904243d76700277c9b9", "local_rejection_reason": "missing_required_grounding", "missing_local_objection_kinds": [], "policy": "SL-10 may override conservative ...<truncated 296 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:Autocontrol_to_Fault_PumpFault", "transition:Forced_backManual_to_Manual", "guard:no_pump_fault"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `1` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:cc3368769b53194be765d34e1bc7f636ef59487970939701746e6bfcf790a33d`；candidate_dsl_hash：`sha256:ca64688a961882c80131f3555091a4127ad0655a7da625098e2baebf67ee5145`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Forced backManual recovery can silence fault alarm signaling while the fault remains uncleared.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-2a073349d05`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sl7-0-3096823055` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL: ! * -> Manual :: CP_backManual can transition from Fault to Manual.', 'DSL: Manual.enter sets alarm_signal = 0.', 'DSL forced backManual transitions do not clear pump_fault.', 'sim_summary: cp_backmanual_from_fault results in Manual with pump_fault = 1 and alarm_signal = 0.', 'NL requires pump fault alarm signaling until caregiver removes the fault.'], 'severity': 'major', 'summary': 'Forced backManual recovery can silence fault alarm signaling while the fault remains uncleared.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:Fault, event:InitiateAC, event:StartAC, event:TerminateAC, event:PumpFault, event:FaultCleared, event:CA_backManual, ... +26`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2756`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sl7-0-3096823055` | `accept` | ❌ | ❌ | The request is accepted because the evidence identifies a real unsafe recovery path: a forced backManual event can move from Fault to Manual while pump_fault remains set, and the current Manual.enter unconditionally clears alarm_signal. That contradicts the NL obligation that pump fault alarm signaling persists until the caregiver removes the fault. The smal...<truncated 502 chars> |
- repair_rationale：The selected model-review failure is unsafe_recovery: cp_backmanual_from_fault could reach Manual with pump_fault = 1 but alarm_signal = 0 because Manual.enter cleared the alarm unconditionally.；The repair changes only Manual.enter so alarm_signal = pump_fault. If a backManual event is taken from Fault, Fault.enter has already set pump_fault = 1, so entering Manual keeps alarm_signal = 1 while preserving the required shared recover...<truncated 47 chars>；When there is no fault, pump_fault = 0, so ordinary entry to Manual and TerminateAC recovery still produce alarm_signal = 0. This preserves the prior repaired scenario autocontrol_init_terminate_and_pump_fault_paths because AutocontrolInit ...<truncated 114 chars>；The caregiver fault-removal path remains Fault -> Manual :: FaultCleared with pump_fault = 0 and alarm_signal = 0, preserving the NL requirement that alarms clear when the caregiver removes the fault.；All required grounded elements are preserved, including the Mode_Control_Algorithm hierarchy, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, Fault, InitiateAC, StartAC, TerminateAC, PumpFault, FaultCleared, all four backManual eve...<truncated 115 chars>
- diff_summary：`{"summary": "Changed Manual.enter from unconditionally clearing alarm_signal to assigning alarm_signal = pump_fault, so forced backManual recovery from Fault keeps the alarm active until the fault is cleared. No states, events, variables, transitions, or grounded actions were removed; the previous AutocontrolInit transition-order fix is preserved."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int blood_pressure = 0;
def int shared_bp_buffer = 0;
def int target_bp = 100;
def int setpoint_delta = 0;
def int default_flow_rate = 0;
def int flow_rate = 0;
def int built_in_switch = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_control = 0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! AutocontrolInit -> Fault :: PumpFault;
        ! AutocontrolNormal -> Fault :: PumpFault;

        >> during before { shared_bp_buffer = blood_pressure; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                pump_control = 0;
                alarm_signal = pump_fault;
            }
            during {
                pump_speed = built_in_switch;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                target_bp = target_bp + setpoint_delta;
                setpoint_delta = 0;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                pump_control = 1;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                pump_control = 1;
            }
            during {
                if [pump_fault == 0] {
                    if [blood_pressure > target_bp] {
                        flow_rate = default_flow_rate - (blood_pressure - target_bp);
                    } else {
                        flow_rate = default_flow_rate + (target_bp - blood_pressure);
                    }
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_count = log_count + 1;
                }
            }
        }

        state Fault {
            enter {
                pump_fault = 1;
                alarm_signal = 1;
                pump_control = 0;
                CA_mode = 0;
            }
            during {
                alarm_signal = 1;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Manual :: TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual :: TerminateAC;
        Fault -> Manual :: FaultCleared effect {
            pump_fault = 0;
            alarm_signal = 0;
            pump_control = 0;
            CA_mode = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -32,7 +32,7 @@
             enter {
                 CA_mode = 0;
                 pump_control = 0;
-                alarm_signal = 0;
+                alarm_signal = pump_fault;
             }
             during {
                 pump_speed = built_in_switch;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:ae49eb5f8ff07511818f8460dc4a13d773d4459a77e260fa86ae6198a3bc9627`。
  - SL-10 evidence 1: `{"summary": "SL-9 accepted the hard SL-7 model-review request because the prior DSL allowed forced backManual recovery from Fault to enter Manual while pump_fault remained 1 and Manual.enter unconditionally set alarm_signal = 0. That contradicted the NL requirement that, when a pump fault occurs, alarm signaling remains active until the caregiver removes the fault. The candidate makes the smallest targeted edit: Manual.enter now assigns alarm_signal = pump_fault, so Manual still sets CA_mode = 0 and pump_control = 0, but an uncleared pump fault keeps the alarm active."}`
  - SL-10 evidence 2: `{"summary": "The DSL diff is limited to Manual.enter changing alarm_signal = 0 to alarm_signal = pump_fault. It preserves the previous AutocontrolInit transition-order fix, all required states, events, variables, transitions, the no-pump-fault guard in AutocontrolNormal, the PumpFault transitions to Fault, the FaultCleared transition clearing pump_fault and alarm_signal, and all four forced backManual transitions to Manual."}`
  - SL-10 evidence 3: `{"summary": "The candidate satisfies the NL recovery semantics better than the old DSL: forced backManual remains the shared recovery target for CA_backManual, CB_backManual, CP_backManual, and CC_backManual by entering Manual and setting CA_mode to Manual, while pump_control is released. Separately, only the caregiver fault-removal path FaultCleared clears pump_fault and alarm_signal, matching the NL phrase that the caregiver removes the fault before alarm release."}`
  - SL-10 evidence 4: `{"summary": "Local deterministic evidence reports one scenario failure in back_manual_forced_recovery_from_fault_and_init: cp_backmanual_from_fault and cc_backmanual_from_init expected Manual with alarm_signal = 0 but actual Manual with alarm_signal = 1 while pump_fault = 1. This is not an NL-fidelity regression; it is the intended correction of the unsafe behavior identified by SL-7. The local expected value preserves the prior bug by requiring the alarm to be silenced while the fault remains uncleared."}`
  - SL-10 evidence 5: `{"summary": "The local missing_required_grounding objections for transition:Autocontrol_to_Fault_PumpFault, transition:Forced_backManual_to_Manual, and guard:no_pump_fault are the same matcher-level objections previously overridden in FixLog repair_memory. Manual inspection again shows those elements are present: ! AutocontrolNormal -> Fault :: PumpFault, four ! * -> Manual backManual transitions, and if [pump_fault == 0] in AutocontrolNormal.during."}`
  - SL-10 evidence 6: `{"candidate_dsl_hash": "sha256:ca64688a961882c80131f3555091a4127ad0655a7da625098e2baebf67ee5145", "covered_local_objection_kinds": ["scenario_regression", "missing_required_grounding"], "kind": "local_major_drift_override_audit", "local_check_evidence_hash": "sha256:b22806afc3367af277d2549631523733b8cdf5080fdcf814654cd0ee7b7ac6d1", "local_override_rationale_count": 4, "local_override_rationale_hash": "sha256:7c5558b92d878ee50f751e9272429db8dfc184dce698f95cbc68e6e7e931c944", "local_rejection_evidence_hash": "sha256:fba8634ec9350d9c5f7f55eb378a69da50e474b58380d056b349ba42bcf7380c", "local_rejection_reason": "scenario_regression; missing_required_grounding", "missing_local_objection_kinds": [],...<truncated 340 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 9, "n_scenarios_passed": 8, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init dispatches into Manual and verifies manual pump-speed/flow plus shared BP buffer behavior.", "name": "default_init_manual_mode_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_signal": 0, "blood_pressure": 85, "bu...<truncated 12627 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:Autocontrol_to_Fault_PumpFault", "transition:Forced_backManual_to_Manual", "guard:no_pump_fault"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `2` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`back_manual_forced_recovery_from_fault_and_init, standalone_forced_backmanual_cp_and_cc_lines`。
- before_dsl_hash：`sha256:ca64688a961882c80131f3555091a4127ad0655a7da625098e2baebf67ee5145`；candidate_dsl_hash：`sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-0cbbf437fe0`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sd6-0-e179d5b71b` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probes CP/CC backManual fallback from Fault and from AutocontrolInit to Manual.', 'name': 'back_manual_forced_recovery_from_fault_and_init', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start probes CP/CC backManual fallback from Fault and from AutocontrolInit to Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'flow_rate': 15, 'pump_control': 0, 'pump_speed': 8}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'flow_rate': 15, 'pump_control': 0, 'pump_speed': 8}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'cp_backmanual_from_fault', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'flow_rate': 15, 'pump_control': 0, 'pump_speed': 8}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'flow_rate': 15, 'pump_control': 0, 'pump_speed': 8}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 3, 'step_name': 'cc_backmanual_from_init', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Fault', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 1, 'built_in_switch': 8, 'default_flow_rate': 15, 'pump_control': 1, 'pump_fault': 1}, 'scenario_name': 'back_manual_forced_recovery_from_fault_and_init', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 0, 'built_in_switch': 8, 'control_voltage': 0, 'default_flow_rate': 15, 'flow_rate': 15, 'log_count': 0, 'pump_control': 0, 'pump_fault': 1, 'pump_speed': 8, 'setpoint_delta': 0, 'shared_bp_buffer': 0, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'cp_backmanual_from_fault', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 0, 'built_in_switch': 8, 'control_voltage': 0, 'default_flow_rate': 15, 'flow_rate': 15, 'log_count': 0, 'pump_control': 0, 'pump_fault': 1, 'pump_speed': 8, 'setpoint_delta': 0, 'shared_bp_buffer': 0, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'move_to_ask_for_init_prefix', 'var_assertion_ok': None, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'blood_pressure': 0, 'built_in_switch': 8, 'control_voltage': 0, 'default_flow_rate': 15, 'flow_rate': 15, 'log_count': 0, 'pump_control': 1, 'pump_fault': 1, 'pump_speed': 8, 'setpoint_delta': 0, 'shared_bp_buffer': 0, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'start_to_init', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 0, 'built_in_switch': 8, 'control_voltage': 0, 'default_flow_rate': 15, 'flow_rate': 15, 'log_count': 0, 'pump_control': 0, 'pump_fault': 1, 'pump_speed': 8, 'setpoint_delta': 0, 'shared_bp_buffer': 0, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 3, 'step_name': 'cc_backmanual_from_init', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}]}` |
| `fixreq-2-sd6-1-b221f3f998` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start isolates CP_backManual and CC_backManual wildcard forced recovery lines from Fault and AutocontrolInit so a missing forced line cannot be hidden by other recovery paths.', 'name': 'standalone_forced_backmanual_cp_and_cc_lines', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start isolates CP_backManual and CC_backManual wildcard forced recovery lines from Fault and AutocontrolInit so a missing forced line cannot be hidden by other recovery paths.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'flow_rate': 22, 'pump_control': 0, 'pump_speed': 12}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CP_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'flow_rate': 22, 'pump_control': 0, 'pump_speed': 12}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 0, 'step_name': 'cp_backmanual_forces_manual_from_fault', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars_focus': {'CA_mode': 0, 'alarm_signal': 1, 'flow_rate': 22, 'pump_control': 0, 'pump_speed': 12}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.CC_backManual'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'flow_rate': 22, 'pump_control': 0, 'pump_speed': 12}, 'runtime_error': '', 'state_assertion_ok': True, 'step_index': 3, 'step_name': 'cc_backmanual_forces_manual_from_init', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.Fault', 'initial_vars': {'CA_mode': 1, 'alarm_signal': 1, 'blood_pressure': 100, 'built_in_switch': 12, 'default_flow_rate': 22, 'pump_control': 1, 'pump_fault': 1, 'target_bp': 100}, 'scenario_name': 'standalone_forced_backmanual_cp_and_cc_lines', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 100, 'built_in_switch': 12, 'control_voltage': 0, 'default_flow_rate': 22, 'flow_rate': 22, 'log_count': 0, 'pump_control': 0, 'pump_fault': 1, 'pump_speed': 12, 'setpoint_delta': 0, 'shared_bp_buffer': 100, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'cp_backmanual_forces_manual_from_fault', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 100, 'built_in_switch': 12, 'control_voltage': 0, 'default_flow_rate': 22, 'flow_rate': 22, 'log_count': 0, 'pump_control': 0, 'pump_fault': 1, 'pump_speed': 12, 'setpoint_delta': 0, 'shared_bp_buffer': 100, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'return_to_ask_after_cp_probe', 'var_assertion_ok': None, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 1, 'blood_pressure': 100, 'built_in_switch': 12, 'control_voltage': 0, 'default_flow_rate': 22, 'flow_rate': 22, 'log_count': 0, 'pump_control': 1, 'pump_fault': 1, 'pump_speed': 12, 'setpoint_delta': 0, 'shared_bp_buffer': 100, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'enter_init_for_cc_probe', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'CA_mode': 0, 'alarm_signal': 1, 'blood_pressure': 100, 'built_in_switch': 12, 'control_voltage': 0, 'default_flow_rate': 22, 'flow_rate': 22, 'log_count': 0, 'pump_control': 0, 'pump_fault': 1, 'pump_speed': 12, 'setpoint_delta': 0, 'shared_bp_buffer': 100, 'target_bp': 100}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 3, 'step_name': 'cc_backmanual_forces_manual_from_init', 'var_assertion_ok': False, 'var_mismatches': {'alarm_signal': {'actual': 1, 'expected': 0}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:Fault, event:InitiateAC, event:StartAC, event:TerminateAC, event:PumpFault, event:FaultCleared, event:CA_backManual, ... +26`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`0`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sd6-0-e179d5b71b` | `reject` | ❌ | ❌ | Rejected because this request reopens the same back_manual_forced_recovery_from_fault_and_init alarm_signal expectation that SL-10 already treated as a stale/local oracle conflict after the SL-7 unsafe_recovery repair. The failing steps cp_backmanual_from_fault and cc_backmanual_from_init expect Manual with alarm_signal = 0 while pump_fault remains 1. That c...<truncated 289 chars> |
| `fixreq-2-sd6-1-b221f3f998` | `reject` | ❌ | ❌ | Rejected because standalone_forced_backmanual_cp_and_cc_lines is the same substantive alarm expectation as the previously overridden local scenario regression: CP_backManual and CC_backManual correctly force Manual and release pump_control, but the scenario expects alarm_signal = 0 despite pump_fault = 1. The current behavior preserves the NL safety invarian...<truncated 194 chars> |
- repair_rationale：All current hard requests were rejected because they require reverting the prior NL-grounded safety repair from Manual.enter alarm_signal = 0 to alarm_signal = pump_fault.；FixLog shows SL-7 found that clearing alarm_signal on backManual while pump_fault remained uncleared was unsafe, and SL-10 explicitly overrode the same scenario_regression as a local oracle mismatch.；The current DSL already preserves the required forced backManual transitions to Manual, CA_mode = 0, pump_control = 0, manual pump_speed/flow behavior, PumpFault transitions to Fault, FaultCleared clearing pump_fault/alarm_signal, and the n...<truncated 40 chars>；No candidate DSL is emitted because accepting either request would require reintroducing a known unsafe recovery path or inventing ungrounded fault-clearing behavior for backManual.
- diff_summary：`{"summary": "No edit applied; current requests conflict with prior accepted NL-grounded fault-alarm safety repair."}`。

#### SL-9 candidate / 最终修改执行方案

- 本 repair 未记录 candidate_dsl。

#### Candidate diff（before -> candidate）

- 无 candidate DSL，因此无法生成 diff。

#### SL-10 审查结果

- SL-10：`<none>`（旧 record 或本 run 未进入 LLM repair review）。
- legacy repair_review：ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-d4aa49fcb84` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-d4aa49fcb84` | accept=1, reject=0 | `sl10_review` | `sha256:cc3368769b53194be765d34e1bc7f636ef59487970939701746e6bfcf790a33d` | For scenario autocontrol_init_terminate_and_pump_fault_paths, failing step terminate_from_init_returns_manual expected state CARA.Mode_Control_Algorithm.Manual with CA_mode=0, pump_control=0, alarm_signal=0, pump_speed=6, and flow_rate=20, but the actual state was AutocontrolNormal with CA_mode=1, pump_control=1, pump_speed=120, and flow_rate=120., The root cause is transition priority/order in AutocontrolInit: the unconditional AutocontrolInit -> AutocontrolNormal transition was considered before the local TerminateAC event transition, so the event was effectively bypassed., The smallest safe edit is to place AutocontrolInit -> Manual :: TerminateAC before the unconditional AutocontrolInit -> AutocontrolNormal transition. When TerminateAC is injected while AutocontrolInit is active, Manual is entered and its during action restores pump_speed from built_in_switch and flow_rate from default_flow_rate, matching the scenario., ... +1 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-d4aa49fcb84` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:cc3368769b53194be765d34e1bc7f636ef59487970939701746e6bfcf790a33d` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +3 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-2a073349d05` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-2a073349d05` | accept=1, reject=0 | `sl10_review` | `sha256:ca64688a961882c80131f3555091a4127ad0655a7da625098e2baebf67ee5145` | The selected model-review failure is unsafe_recovery: cp_backmanual_from_fault could reach Manual with pump_fault = 1 but alarm_signal = 0 because Manual.enter cleared the alarm unconditionally., The repair changes only Manual.enter so alarm_signal = pump_fault. If a backManual event is taken from Fault, Fault.enter has already set pump_fault = 1, so entering Manual keeps alarm_signal = 1 while preserving the required shared recovery target CA_mode = Manual and pump_control = 0., When there is no fault, pump_fault = 0, so ordinary entry to Manual and TerminateAC recovery still produce alarm_signal = 0. This preserves the prior repaired scenario autocontrol_init_terminate_and_pump_fault_paths because AutocontrolInit -> Manual :: TerminateAC remains ordered before the unconditional AutocontrolInit -> AutocontrolNormal transition., ... +2 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-2a073349d05` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:ca64688a961882c80131f3555091a4127ad0655a7da625098e2baebf67ee5145` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +4 |
| 7 | `2` | `request_batch` | `fixbatch-2-sha256-0cbbf437fe0` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 8 | `2` | `sl9_decision` | `fixbatch-2-sha256-0cbbf437fe0` | accept=0, reject=2 | `reject_or_waiver` | `<none>` | All current hard requests were rejected because they require reverting the prior NL-grounded safety repair from Manual.enter alarm_signal = 0 to alarm_signal = pump_fault., FixLog shows SL-7 found that clearing alarm_signal on backManual while pump_fault remained uncleared was unsafe, and SL-10 explicitly overrode the same scenario_regression as a local oracle mismatch., The current DSL already preserves the required forced backManual transitions to Manual, CA_mode = 0, pump_control = 0, manual pump_speed/flow behavior, PumpFault transitions to Fault, FaultCleared clearing pump_fault/alarm_signal, and the no-pump-fault guard in AutocontrolNormal., ... +1 |
| 9 | `2` | `sl9_all_rejected` | `fixbatch-2-sha256-0cbbf437fe0` | accept=0, reject=2 | `exit_rejected` | `<none>` | sl9_rejected_all_fix_requests:hard_block |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4458, 'completion_chars': 17636, 'completion_tokens': 6264, 'elapsed_seconds': 116.18475021302584, 'estimated_completion_tokens': 4409, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11066, 'first_chunk_seconds': 35.6385362240253, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12714}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1851, 'completion_chars': 7412, 'completion_tokens': 2370, 'elapsed_seconds': 46.88805456800037, 'estimated_completion_tokens': 1853, 'estimated_prompt_tokens': 14415, 'estimated_total_tokens': 16268, 'first_chunk_seconds': 14.50160922500072, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 57660, 'prompt_tokens': 14080, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 16450}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1213, 'completion_chars': 5206, 'completion_tokens': 1590, 'elapsed_seconds': 30.765960555989295, 'estimated_completion_tokens': 1302, 'estimated_prompt_tokens': 21034, 'estimated_total_tokens': 22336, 'first_chunk_seconds': 8.832719165977323, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 84135, 'prompt_tokens': 19611, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21201}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 835, 'completion_chars': 3921, 'completion_tokens': 1085, 'elapsed_seconds': 22.166631484986283, 'estimated_completion_tokens': 981, 'estimated_prompt_tokens': 19112, 'estimated_total_tokens': 20093, 'first_chunk_seconds': 7.060123825009214, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 76447, 'prompt_tokens': 17217, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 18302}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3004, 'completion_chars': 12276, 'completion_tokens': 3523, 'elapsed_seconds': 65.67996206899988, 'estimated_completion_tokens': 3069, 'estimated_prompt_tokens': 18110, 'estimated_total_tokens': 21179, 'first_chunk_seconds': 11.538304683024762, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 72440, 'prompt_tokens': 17886, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21409}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1614, 'completion_chars': 7722, 'completion_tokens': 2773, 'elapsed_seconds': 54.69006998799159, 'estimated_completion_tokens': 1931, 'estimated_prompt_tokens': 20283, 'estimated_total_tokens': 22214, 'first_chunk_seconds': 24.11250797100365, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 81130, 'prompt_tokens': 20172, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22945}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1318, 'completion_chars': 5789, 'completion_tokens': 2473, 'elapsed_seconds': 46.799334377021296, 'estimated_completion_tokens': 1448, 'estimated_prompt_tokens': 39692, 'estimated_total_tokens': 41140, 'first_chunk_seconds': 22.977334512019297, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 158767, 'prompt_tokens': 36401, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 38874}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 992, 'completion_chars': 4738, 'completion_tokens': 1262, 'elapsed_seconds': 25.177608669007896, 'estimated_completion_tokens': 1185, 'estimated_prompt_tokens': 44864, 'estimated_total_tokens': 46049, 'first_chunk_seconds': 7.17186662601307, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 179453, 'prompt_tokens': 39179, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 40441}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4135, 'completion_chars': 16967, 'completion_tokens': 4654, 'elapsed_seconds': 86.23869195202133, 'estimated_completion_tokens': 4242, 'estimated_prompt_tokens': 20298, 'estimated_total_tokens': 24540, 'first_chunk_seconds': 11.705904330010526, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 81192, 'prompt_tokens': 20071, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24725}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5134, 'completion_chars': 21065, 'completion_tokens': 5653, 'elapsed_seconds': 104.36637569899904, 'estimated_completion_tokens': 5267, 'estimated_prompt_tokens': 21471, 'estimated_total_tokens': 26738, 'first_chunk_seconds': 11.869430212012958, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 85883, 'prompt_tokens': 21202, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26855}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 641, 'completion_chars': 2935, 'completion_tokens': 1323, 'elapsed_seconds': 26.99967025400838, 'estimated_completion_tokens': 734, 'estimated_prompt_tokens': 104847, 'estimated_total_tokens': 105581, 'first_chunk_seconds': 15.331030678004026, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 419386, 'prompt_tokens': 84872, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 86195}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`not_converged`，record_status=`rejected`。
- 主要原因分类：`scenario_or_sim_oracle`。
- required stages executed：`40/16`，missing=`<none>`。
- repairs：`2/3` accepted；scenario_history=`6`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
