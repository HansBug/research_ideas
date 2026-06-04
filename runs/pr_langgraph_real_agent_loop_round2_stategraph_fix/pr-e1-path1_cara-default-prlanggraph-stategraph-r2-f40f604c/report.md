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
| Git commit | `4f64caf598879346189afaac271a5722d526d936` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:993dd2a89560dc22cd287bbf50c2cbe6faab9e99a63729d53f02e0d42085b247` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:55db32db5a501930ea9caacc612bf09595ad3465ad588dfebdd27c8de7eeebea", "iteration": 2, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:c7b912815fce0736811c5a1361188b7cb22d932c2ba455ec05433adac293ffb1", "iteration": 2, "repair_history_index": 2, "rework_instructions": ["SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.", "For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling."], "same_as_final": false, "sl10_decision": "rework"}, "matching_repair_history_indices": [3], "repair_history_index": 3, "selected_source_stage": "SL-7", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'completion_chars': 134322, 'completion_tokens': 44509, 'estimated_completion_tokens': 33587, 'estimated_prompt_tokens': 544600, 'estimated_total_tokens': 578187, 'n_calls': 17, 'prompt_chars': 2178376, 'prompt_tokens': 520218, 'token_usage_available': True, 'token_usage_unavailable_calls': 0, 'total_tokens': 564727}`, elapsed=`865.721s` |
| run record | [`pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:dc5b944f171d8a7e812e83bf63456d149da939d74db976c3e43bb25d870df2fd` |
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
| `langgraph_node_trace_hash` | `sha256:882d0407c200131292f62fb6e94e6f801941edc6b71d41db564ee5d1275ea22f` |
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
def float blood_pressure = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 0;
def float buffer_bp = 0.0;
def float log_infusion_rate = 0.0;

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
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
                }
            }
            during {
                pump_speed = built_in_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                if [pump_fault > 0] {
                    CA_mode = 0;
                    control_released = 1;
                    alarm_signal = 1;
                } else {
                    CA_mode = 1;
                    control_released = 0;
                    alarm_signal = 0;
                }
            }
        }

        state AutocontrolNormal {
            during {
                buffer_bp = blood_pressure;
                if [blood_pressure > target_bp] {
                    flow_rate = flow_rate - 1.0;
                } else if [blood_pressure < target_bp] {
                    flow_rate = flow_rate + 1.0;
                } else {
                    flow_rate = flow_rate;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_infusion_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: SetpointChanged effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> PumpFault : if [pump_fault > 0];
        AutocontrolInit -> AutocontrolNormal : if [pump_fault == 0];
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12703 | 生成初始 DSL 与 grounding seeds | initial len=2318 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=93029 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=101283 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=184771 | LLM per-request accept/reject + repair | candidate len=2345,2468,2923,2757 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=172941 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=93029 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=101283 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=184771 | LLM per-request accept/reject + repair | candidate len=2345,2468,2923,2757 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=172941 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=93029 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=101283 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=184771 | LLM per-request accept/reject + repair | candidate len=2345,2468,2923,2757 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=4, tokens=172941 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=4, tokens=184771 | LLM per-request accept/reject + repair | candidate len=2345,2468,2923,2757 | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=4, tokens=172941 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=4, tokens=93029 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=4, tokens=101283 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-prlanggraph-stategraph-r2-f40f604c.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T16:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-04T16:42:54Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-04T16:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-04T16:42:54Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-04T16:44:49Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-04T16:44:49Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2318,hash=sha256:43713af1d56b |
| 7 | `2026-06-04T16:44:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-04T16:44:49Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-04T16:44:49Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:43713af1d56bda024bb0ebc14e14e97da1de77eb364dd7aad87eecf7bfa366db |
| 10 | `2026-06-04T16:44:49Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2318,hash=sha256:43713af1d56b, current_hash=sha256:43713af1d56bda024bb0ebc14e14e97da1de77eb364dd7aad87eecf7bfa366db |
| 11 | `2026-06-04T16:44:49Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 12 | `2026-06-04T16:44:49Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T16:44:49Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 14 | `2026-06-04T16:44:49Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T16:44:49Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 16 | `2026-06-04T16:44:49Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 17 | `2026-06-04T16:44:49Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 18 | `2026-06-04T16:45:58Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T16:45:58Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 20 | `2026-06-04T16:45:58Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 21 | `2026-06-04T16:45:58Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 22 | `2026-06-04T16:45:58Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-04T16:45:58Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 24 | `2026-06-04T16:46:52Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 25 | `2026-06-04T16:46:52Z` | `SL-7` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-04T16:46:52Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 27 | `2026-06-04T16:46:52Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["DSL: PumpFault -> Manual :: FaultRemoved; with no guard/effect on pump_fault.", "DSL: Manual.enter clears alarm_signal to 0.", "Simulation: after FaultRemoved, state is Manual with pump_fault = 1 and alarm_signal = 0."], "severity": "major", "summary": "Fault recovery can clear the alarm...<truncated 222 chars> | <none> |
| 28 | `2026-06-04T16:46:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-04T16:46:52Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-04T16:46:52Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["DSL: PumpFault -> Manual :: FaultRemoved; with no guard/effect on pump_fault.", "DSL: Manual.enter clears alarm_signal to 0.", "Simulation: after FaultRemoved, state is Manual with pump_fault = 1 and alarm_signal = 0."], "severity": "major", "summary": "Fault recovery can clear the alarm and en...<truncated 215 chars> | current_dsl:len=2318,hash=sha256:43713af1d56b |
| 31 | `2026-06-04T16:46:52Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 32 | `2026-06-04T16:46:52Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 33 | `2026-06-04T16:46:52Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2318,hash=sha256:43713af1d56b |
| 34 | `2026-06-04T16:47:16Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-04T16:47:16Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2345,hash=sha256:8d8bee3d93ca |
| 36 | `2026-06-04T16:47:16Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": true, "status": "StageStatus.OK"} | <none> |
| 37 | `2026-06-04T16:47:16Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:8d8bee3d93ca11a6f72e62f677cf8efec1d48133d8ee73ceeef315da4e74ef9a |
| 38 | `2026-06-04T16:47:30Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 39 | `2026-06-04T16:47:30Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 40 | `2026-06-04T16:47:30Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 41 | `2026-06-04T16:47:30Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2345,hash=sha256:8d8bee3d93ca |
| 42 | `2026-06-04T16:47:30Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:8d8bee3d93ca11a6f72e62f677cf8efec1d48133d8ee73ceeef315da4e74ef9a |
| 43 | `2026-06-04T16:47:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-04T16:47:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 45 | `2026-06-04T16:47:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 46 | `2026-06-04T16:47:30Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:8d8bee3d93ca11a6f72e62f677cf8efec1d48133d8ee73ceeef315da4e74ef9a |
| 47 | `2026-06-04T16:47:30Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=2345,hash=sha256:8d8bee3d93ca, current_hash=sha256:8d8bee3d93ca11a6f72e62f677cf8efec1d48133d8ee73ceeef315da4e74ef9a |
| 48 | `2026-06-04T16:47:30Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 49 | `2026-06-04T16:47:30Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 50 | `2026-06-04T16:47:30Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 51 | `2026-06-04T16:47:30Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 52 | `2026-06-04T16:47:30Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 53 | `2026-06-04T16:47:30Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-5A", "ok": true, "status": "StageStatus.OK"} | <none> |
| 54 | `2026-06-04T16:47:31Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 targeted_retry", "ok": false, "reason": "reuse_frozen_scenario_set"} | <none> |
| 55 | `2026-06-04T16:47:31Z` | `<control>` | `1` | `frozen_scenario_refresh_targeted_retry` | {} | <none> |
| 56 | `2026-06-04T16:47:31Z` | `SL-5` | `1` | `stage_enter` | {"reason": "targeted_refresh_after_frozen_gap_or_dsl_change"} | <none> |
| 57 | `2026-06-04T16:48:36Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 58 | `2026-06-04T16:48:36Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 59 | `2026-06-04T16:48:36Z` | `SC-5F` | `1` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": "refreshed_scenario_set"} | <none> |
| 60 | `2026-06-04T16:48:36Z` | `SD-6` | `1` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 61 | `2026-06-04T16:48:36Z` | `SD-6` | `1` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 62 | `2026-06-04T16:48:36Z` | `SL-7` | `1` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 63 | `2026-06-04T16:49:34Z` | `SL-7` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 64 | `2026-06-04T16:49:34Z` | `SL-7` | `1` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 65 | `2026-06-04T16:49:34Z` | `SL-7` | `1` | `grounding_update_hints_recorded` | {} | <none> |
| 66 | `2026-06-04T16:49:34Z` | `<control>` | `1` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["DSL: ! * -> Manual :: CA_backManual/CB_backManual/CP_backManual/CC_backManual/TerminateAC.", "DSL: Manual.enter sets alarm_signal = 0.", "DSL: these forced transitions have no guard pump_fault == 0 and no effect clearing pump_fault.", "NL requires pump faults to activate alarm signals an...<truncated 557 chars> | <none> |
| 67 | `2026-06-04T16:49:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 68 | `2026-06-04T16:49:34Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 69 | `2026-06-04T16:49:34Z` | `SD-8` | `1` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["DSL: ! * -> Manual :: CA_backManual/CB_backManual/CP_backManual/CC_backManual/TerminateAC.", "DSL: Manual.enter sets alarm_signal = 0.", "DSL: these forced transitions have no guard pump_fault == 0 and no effect clearing pump_fault.", "NL requires pump faults to activate alarm signals and descr...<truncated 550 chars> | current_dsl:len=2345,hash=sha256:8d8bee3d93ca |
| 70 | `2026-06-04T16:49:34Z` | `SD-8` | `1` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 71 | `2026-06-04T16:49:34Z` | `SD-8` | `1` | `fix_request_batch` | {"request_count": 1} | <none> |
| 72 | `2026-06-04T16:49:34Z` | `SL-9` | `1` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2345,hash=sha256:8d8bee3d93ca |
| 73 | `2026-06-04T16:50:04Z` | `SL-9` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 74 | `2026-06-04T16:50:04Z` | `SL-9` | `1` | `stage_result` | {"accepted_request_ids": ["fixreq-1-sl7-0-3096823055"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2468,hash=sha256:74b4333340ba |
| 75 | `2026-06-04T16:50:04Z` | `SD-10` | `1` | `stage_result` | {"jump": "SL-10", "ok": true, "status": "StageStatus.OK"} | <none> |
| 76 | `2026-06-04T16:50:04Z` | `SL-10` | `1` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:74b4333340ba8396c1696cf465c02e6614ac2b582ad47631a8bf8a7d47e26680 |
| 77 | `2026-06-04T16:50:24Z` | `SL-10` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 78 | `2026-06-04T16:50:24Z` | `SL-10` | `1` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 79 | `2026-06-04T16:50:24Z` | `SL-10` | `1` | `grounding_update_hints_recorded` | {} | <none> |
| 80 | `2026-06-04T16:50:24Z` | `SC-11` | `1` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2468,hash=sha256:74b4333340ba |
- ……另有 `77` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SL-7` | yes | fixbatch-0-sha256-b98dd6bcea8 / n=1 | accept=1, reject=0, waiver=0 | ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SL-7` | yes | fixbatch-1-sha256-6884b412ad6 / n=1 | accept=1, reject=0, waiver=0 | ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SL-7` | yes | fixbatch-2-sha256-4a913dec7ae / n=2 | accept=2, reject=0, waiver=0 | ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 |
|---|---|---|---|---|---|
| `default_init_enters_manual_and_sets_manual_outputs` | default-init: first empty cycle dispatches to Manual and manual operation uses the built-in switch speed and caregiver d...<truncated 17 chars> | ✅ | ✅ | ✅ | ✅ |
| `initiate_setpoint_start_ac_to_normal_high_pressure` | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC to enter AutocontrolInit, then no...<truncated 70 chars> | ✅ | ✅ | ✅ | ✅ |
| `autocontrol_normal_no_fault_low_pressure_increases_flow` | explicit-hot-start: from reachable AutocontrolNormal with no pump fault, CARA remains in normal autocontrol and raises f...<truncated 34 chars> | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_enters_alarm_state_then_fault_removed_returns_manual` | explicit-hot-start: pump fault during normal autocontrol enters PumpFault with alarm/control release, then FaultRemoved ...<truncated 56 chars> | ✅ | ✅ | ✅ | ✅ |
| `ca_and_cb_backmanual_force_manual_from_ask_and_init` | explicit-hot-start: cross-component CA_backManual and CB_backManual force Manual from distinct autocontrol-related leave...<truncated 28 chars> | ✅ | ✅ | ✅ | ✅ |
| `cp_backmanual_forces_manual_from_autocontrol_normal` | explicit-hot-start: CP_backManual forces Manual from AutocontrolNormal as the shared recovery target. | ✅ | ✅ | ✅ | ✅ |
| `cc_backmanual_forces_manual_from_pump_fault` | explicit-hot-start: CC_backManual forces Manual from PumpFault as the shared recovery target, but with an unresolved act...<truncated 40 chars> | ✅ | ✅ | ✅ | ✅ |
| `terminate_ac_forces_manual_from_autocontrol_init` | explicit-hot-start: caregiver TerminateAC during algorithmic control forces Manual and releases software control. | ✅ | ✅ | ✅ | ✅ |
| `fault_removed_clears_pump_fault_effect` | explicit-hot-start: directly probes the FaultRemoved transition effect so missing or wrong pump_fault clearing fails. | ⚪ | ✅ | ✅ | ✅ |
| `setpoint_changed_effect_uses_requested_target` | explicit-hot-start: directly probes the SetpointChanged effect so missing or wrong target_bp assignment fails. | ⚪ | ✅ | ✅ | ✅ |
| `start_ac_with_active_fault_routes_to_pump_fault` | explicit-hot-start: active pump fault while starting autocontrol should not proceed to normal control; AutocontrolInit r...<truncated 59 chars> | ⚪ | ⚪ | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_enters_manual_and_sets_manual_outputs` — default-init: first empty cycle dispatches to Manual and manual operation uses the built-in switch speed and caregiver default flow rate.</summary>

| Field | Value |
|---|---|
| description | default-init: first empty cycle dispatches to Manual and manual operation uses the built-in switch speed and caregiver default flow rate. |
| initial_state | `<default-init>` |
| initial_vars | `{"built_in_switch_speed": 2.5, "default_flow_rate": 4.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `default_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 4.0, "pump_speed": 2.5}` |

</details>

<details><summary>`initiate_setpoint_start_ac_to_normal_high_pressure` — default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC to enter AutocontrolInit, then normal autocontrol lowers flow for high pr...<truncated 30 chars></summary>

| Field | Value |
|---|---|
| description | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC to enter AutocontrolInit, then normal autocontrol lowers flow for high pressure when there is no fault. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 100.0, "built_in_switch_speed": 1.0, "default_flow_rate": 5.0, "flow_rate": 5.0, "pump_fault": 0, "requested_target_bp": 75.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `default_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 5.0, "pump_speed": 1.0}` |
| 1 `initiate_enters_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 2 `setpoint_changed_updates_target` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointChanged"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 75.0}` |
| 3 `start_ac_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "control_released": 0}` |
| 4 `no_fault_transition_to_normal_controls_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"buffer_bp": 100.0, "control_voltage": 4.0, "flow_rate": 4.0, "log_infusion_rate": 4.0, "pump_speed": 4.0}` |

</details>

<details><summary>`autocontrol_normal_no_fault_low_pressure_increases_flow` — explicit-hot-start: from reachable AutocontrolNormal with no pump fault, CARA remains in normal autocontrol and raises flow when pressure is below target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: from reachable AutocontrolNormal with no pump fault, CARA remains in normal autocontrol and raises flow when pressure is below target. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 70.0, "flow_rate": 5.0, "pump_fault": 0, "target_bp": 80.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_fault_stays_normal_and_increases_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 1, "buffer_bp": 70.0, "control_voltage": 6.0, "flow_rate": 6.0, "log_infusion_rate": 6.0, "pump_speed": 6.0}` |

</details>

<details><summary>`pump_fault_enters_alarm_state_then_fault_removed_returns_manual` — explicit-hot-start: pump fault during normal autocontrol enters PumpFault with alarm/control release, then FaultRemoved returns to Manual recovery and clears th...<truncated 16 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: pump fault during normal autocontrol enters PumpFault with alarm/control release, then FaultRemoved returns to Manual recovery and clears the modeled fault. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 90.0, "built_in_switch_speed": 3.0, "default_flow_rate": 7.0, "flow_rate": 6.0, "pump_fault": 1, "target_bp": 80.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_guard_enters_pump_fault` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1}` |
| 1 `fault_removed_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 7.0, "pump_fault": 0, "pump_speed": 3.0}` |

</details>

<details><summary>`ca_and_cb_backmanual_force_manual_from_ask_and_init` — explicit-hot-start: cross-component CA_backManual and CB_backManual force Manual from distinct autocontrol-related leaves and set CA_mode to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: cross-component CA_backManual and CB_backManual force Manual from distinct autocontrol-related leaves and set CA_mode to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "built_in_switch_speed": 2.0, "default_flow_rate": 8.0, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_from_ask` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 8.0, "pump_speed": 2.0}` |
| 1 `reenter_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 2 `start_ac_to_init_again` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "control_released": 0}` |
| 3 `cb_backmanual_from_init` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 8.0, "pump_speed": 2.0}` |

</details>

<details><summary>`cp_backmanual_forces_manual_from_autocontrol_normal` — explicit-hot-start: CP_backManual forces Manual from AutocontrolNormal as the shared recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CP_backManual forces Manual from AutocontrolNormal as the shared recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 80.0, "built_in_switch_speed": 4.0, "default_flow_rate": 6.0, "flow_rate": 9.0, "pump_fault": 0, "target_bp": 80.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_from_normal` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 6.0, "pump_speed": 4.0}` |

</details>

<details><summary>`cc_backmanual_forces_manual_from_pump_fault` — explicit-hot-start: CC_backManual forces Manual from PumpFault as the shared recovery target, but with an unresolved active pump fault the alarm remains active.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CC_backManual forces Manual from PumpFault as the shared recovery target, but with an unresolved active pump fault the alarm remains active. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 0, "alarm_signal": 1, "built_in_switch_speed": 1.5, "control_released": 1, "default_flow_rate": 3.5, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_backmanual_from_pump_fault` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1, "flow_rate": 3.5, "pump_fault": 1, "pump_speed": 1.5}` |

</details>

<details><summary>`terminate_ac_forces_manual_from_autocontrol_init` — explicit-hot-start: caregiver TerminateAC during algorithmic control forces Manual and releases software control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: caregiver TerminateAC during algorithmic control forces Manual and releases software control. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "built_in_switch_speed": 5.0, "control_released": 0, "default_flow_rate": 2.0, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_ac_from_init` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 2.0, "pump_speed": 5.0}` |

</details>

<details><summary>`fault_removed_clears_pump_fault_effect` — explicit-hot-start: directly probes the FaultRemoved transition effect so missing or wrong pump_fault clearing fails.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: directly probes the FaultRemoved transition effect so missing or wrong pump_fault clearing fails. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 0, "alarm_signal": 1, "built_in_switch_speed": 2.25, "control_released": 1, "default_flow_rate": 4.25, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_removed_clears_fault_and_enters_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "control_released": 1, "flow_rate": 4.25, "pump_fault": 0, "pump_speed": 2.25}` |

</details>

<details><summary>`setpoint_changed_effect_uses_requested_target` — explicit-hot-start: directly probes the SetpointChanged effect so missing or wrong target_bp assignment fails.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: directly probes the SetpointChanged effect so missing or wrong target_bp assignment fails. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"requested_target_bp": 85.0, "target_bp": 60.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `requested_setpoint_becomes_target` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointChanged"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 85.0}` |

</details>

<details><summary>`start_ac_with_active_fault_routes_to_pump_fault` — explicit-hot-start: active pump fault while starting autocontrol should not proceed to normal control; AutocontrolInit reports alarm/released control and then r...<truncated 19 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: active pump fault while starting autocontrol should not proceed to normal control; AutocontrolInit reports alarm/released control and then routes to PumpFault. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `start_ac_enters_init_with_fault_alarm` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1, "pump_fault": 1}` |
| 1 `active_fault_routes_to_pump_fault` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "control_released": 1, "pump_fault": 1}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:8d8bee3d93ca11a6f72e62f677cf8efec1d48133d8ee73ceeef315da4e74ef9a` |
| 2 | `1` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:74b4333340ba8396c1696cf465c02e6614ac2b582ad47631a8bf8a7d47e26680` |
| 3 | `2` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 689 chars> | `sha256:c7b912815fce0736811c5a1361188b7cb22d932c2ba455ec05433adac293ffb1` |
| 4 | `2` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:55db32db5a501930ea9caacc612bf09595ad3465ad588dfebdd27c8de7eeebea` |

<details><summary>Repair 1 / iteration `0` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:43713af1d56bda024bb0ebc14e14e97da1de77eb364dd7aad87eecf7bfa366db`；candidate_dsl_hash：`sha256:8d8bee3d93ca11a6f72e62f677cf8efec1d48133d8ee73ceeef315da4e74ef9a`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Fault recovery can clear the alarm and enter Manual while the modeled pump_fault remains active.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-b98dd6bcea8`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL: PumpFault -> Manual :: FaultRemoved; with no guard/effect on pump_fault.', 'DSL: Manual.enter clears alarm_signal to 0.', 'Simulation: after FaultRemoved, state is Manual with pump_fault = 1 and alarm_signal = 0.'], 'severity': 'major', 'summary': 'Fault recovery can clear the alarm and enter Manual while the modeled pump_fault remains active.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:blood_pressure, variable:target_bp, variable:requested_target_bp, variable:flow_rate, variable:default_flow_rate, ... +30`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2345`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ❌ | The review evidence shows that FaultRemoved can enter Manual while pump_fault remains active and Manual.enter clears alarm_signal. The smallest NL-grounded repair is to make the caregiver FaultRemoved event clear the modeled pump_fault before entering Manual, matching the requirement that the caregiver removes the fault.；intent=Add an effect to PumpFault -> ...<truncated 48 chars> |
- repair_rationale：Accepted the hard SL-7 model_review request because the evidence identifies a concrete unsafe recovery path.；Expected safe recovery: after the caregiver removes the fault, Manual recovery should not have pump_fault still active while alarm_signal is cleared. Actual current behavior: PumpFault -> Manual on FaultRemoved left pump_fault = 1, then Man...<truncated 31 chars>；The repair preserves the required FaultRemoved event and PumpFault_to_Manual transition while adding the grounded effect pump_fault = 0 to represent that the caregiver has removed the modeled fault.；No required states, variables, events, transitions, or Manual/AutocontrolNormal/PumpFault actions were deleted. The edit avoids inventing autonomous plant dynamics; pump_fault changes only on the explicit caregiver fault-removal event.
- diff_summary：`{"summary": "Changed only the PumpFault recovery transition from `PumpFault -> Manual :: FaultRemoved;` to `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };` so Manual is entered only after the modeled fault flag is cleared by the fault-removal event."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def float blood_pressure = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 0;
def float buffer_bp = 0.0;
def float log_infusion_rate = 0.0;

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
                alarm_signal = 0;
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
            }
        }

        state AutocontrolNormal {
            during {
                buffer_bp = blood_pressure;
                if [blood_pressure > target_bp] {
                    flow_rate = flow_rate - 1.0;
                } else if [blood_pressure < target_bp] {
                    flow_rate = flow_rate + 1.0;
                } else {
                    flow_rate = flow_rate;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_infusion_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: SetpointChanged effect { target_bp = requested_target_bp; };
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
@@ -76,6 +76,6 @@
         Ask_StartAC -> AutocontrolInit :: StartAC;
         AutocontrolInit -> AutocontrolNormal;
         AutocontrolNormal -> PumpFault : if [pump_fault > 0];
-        PumpFault -> Manual :: FaultRemoved;
+        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:176e65fb51cd8c22688e6879c68b8c6c10a35ef373b3bb97d45a87c78fc1a80d`。
  - SL-10 evidence 1: `{"summary": "The hard SL-7 request identified an unsafe recovery path: PumpFault -> Manual on FaultRemoved left pump_fault = 1 while Manual.enter cleared alarm_signal to 0. SL-9 accepted the request and made the smallest NL-grounded edit: the FaultRemoved transition now has effect { pump_fault = 0; }, directly representing the NL statement that the caregiver removes the fault before recovery to Manual."}`
  - SL-10 evidence 2: `{"summary": "The DSL diff changes only the PumpFault recovery transition from `PumpFault -> Manual :: FaultRemoved;` to `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };`. This resolves the remembered grounding risk that FaultRemoved was not tied to actual modeled fault absence, without adding unrelated behavior or autonomous plant dynamics."}`
  - SL-10 evidence 3: `{"summary": "Required NL elements are preserved: Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, all required variables, InitiateAC, SetpointChanged, StartAC, TerminateAC, CA/CB/CP/CC_backManual, FaultRemoved, and the required transitions/actions remain present. Manual operation, autocontrol initiation, setpoint change, autocontrol flow computation, alarm activation, release of control, and cross-component fallback behavior are not dropped."}`
  - SL-10 evidence 4: `{"summary": "Local deterministic repair review reports ok=true, target_resolved=true, regression_detected=false, drift_risk=none, and no local rejection. The scenario summary remains healthy, with no coverage gap or oracle weakness reported for the repair."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。

</details>

<details><summary>Repair 2 / iteration `1` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:8d8bee3d93ca11a6f72e62f677cf8efec1d48133d8ee73ceeef315da4e74ef9a`；candidate_dsl_hash：`sha256:74b4333340ba8396c1696cf465c02e6614ac2b582ad47631a8bf8a7d47e26680`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Forced back-to-manual and terminate transitions can enter Manual from PumpFault with pump_fault still active while Manual.enter clears alarm_signal, so unresolved pump faults can be hidden by recovery behavior.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-6884b412ad6`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sl7-0-3096823055` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL: ! * -> Manual :: CA_backManual/CB_backManual/CP_backManual/CC_backManual/TerminateAC.', 'DSL: Manual.enter sets alarm_signal = 0.', 'DSL: these forced transitions have no guard pump_fault == 0 and no effect clearing pump_fault.', 'NL requires pump faults to activate alarm signals and describes caregiver fault removal before recovery.', 'The simulation suite does not cover forced Manual recovery from PumpFault with pump_fault = 1.'], 'severity': 'major', 'summary': 'Forced back-to-manual and terminate transitions can enter Manual from PumpFault with pump_fault still active while Manual.enter clears alarm_signal, so unresolved pump faults can be hidden by recovery behavior.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:blood_pressure, variable:target_bp, variable:requested_target_bp, variable:flow_rate, variable:default_flow_rate, ... +30`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2468`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sl7-0-3096823055` | `accept` | ❌ | ❌ | The new SL-7 evidence is distinct from the previous FaultRemoved issue: the broad forced CA_backManual/CB_backManual/CP_backManual/CC_backManual/TerminateAC transitions can still enter Manual while pump_fault remains active, and Manual.enter unconditionally cleared alarm_signal. Forced transitions cannot carry guards or effects in pyfcstm, and the NL require...<truncated 392 chars> |
- repair_rationale：Accepted the hard model-review request because the current candidate fixed FaultRemoved but not the analogous forced-transition hazard from PumpFault to Manual.；Expected behavior: cross-component backManual/TerminateAC may make CA_mode Manual, but an unresolved pump_fault must not be hidden; alarm_signal should remain active until the caregiver removes the fault.；Actual behavior before this repair: the forced transitions entered Manual with pump_fault possibly still 1, and Manual.enter unconditionally set alarm_signal = 0.；Because pyfcstm forced transitions cannot have effect blocks or guards, adding effects to the forced fallback lines is not syntactically valid. Replacing the required forced fallbacks would risk deleting grounded recovery behavior.；The edit preserves all required states, variables, events, broad fallback transitions, FaultRemoved behavior, Manual_during, AutocontrolNormal_during, and PumpFault_enter. It does not invent autonomous plant dynamics; pump_fault is still cl...<truncated 49 chars>
- diff_summary：`{"summary": "Changed only Manual.enter: instead of always setting alarm_signal = 0, it now sets alarm_signal = 1 when pump_fault > 0 and clears it only when pump_fault == 0. This keeps unresolved pump faults visible during forced Manual fallback while preserving all fallback transitions."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def float blood_pressure = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 0;
def float buffer_bp = 0.0;
def float log_infusion_rate = 0.0;

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
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
                }
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
            }
        }

        state AutocontrolNormal {
            during {
                buffer_bp = blood_pressure;
                if [blood_pressure > target_bp] {
                    flow_rate = flow_rate - 1.0;
                } else if [blood_pressure < target_bp] {
                    flow_rate = flow_rate + 1.0;
                } else {
                    flow_rate = flow_rate;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_infusion_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: SetpointChanged effect { target_bp = requested_target_bp; };
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
@@ -29,7 +29,11 @@
             enter {
                 CA_mode = 0;
                 control_released = 1;
-                alarm_signal = 0;
+                if [pump_fault > 0] {
+                    alarm_signal = 1;
+                } else {
+                    alarm_signal = 0;
+                }
             }
             during {
                 pump_speed = built_in_switch_speed;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:a313cf8c0f8c7d4afc589ba673fa2f480850dd342b2a9664223ba81fc6b68035`。
  - SL-10 evidence 1: `{"summary": "The current hard SL-7 request concerns a distinct unsafe-recovery path left after the prior FaultRemoved repair: forced ! * -> Manual transitions for CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC could enter Manual from PumpFault while pump_fault remained 1, and the old Manual.enter unconditionally set alarm_signal = 0. That hid an unresolved pump fault despite the NL requirement that pump faults activate alarm signals until the caregiver removes the fault."}`
  - SL-10 evidence 2: `{"summary": "SL-9 accepted the hard request and made the smallest DSL edit compatible with the stated pyfcstm constraint that forced transitions cannot carry guards or effects: Manual.enter now sets alarm_signal = 1 when pump_fault > 0 and clears it only otherwise. This directly resolves the expected-vs-actual failure: forced fallback can still make CA_mode Manual as required, but an unresolved pump_fault is no longer hidden by Manual entry."}`
  - SL-10 evidence 3: `{"summary": "The previous FixLog memory objected that FaultRemoved was not tied to modeled fault absence; that was already resolved by PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; }. The current candidate preserves that repair, so caregiver FaultRemoved clears pump_fault before Manual entry, after which Manual.enter clears alarm_signal because pump_fault == 0. Thus both the remembered FaultRemoved recovery issue and the new forced-transition recovery issue are addressed together."}`
  - SL-10 evidence 4: `{"summary": "The DSL diff is narrowly scoped to Manual.enter. It does not remove or weaken required NL elements: Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, required variables, InitiateAC, SetpointChanged, StartAC, TerminateAC, CA/CB/CP/CC_backManual, FaultRemoved, normal autocontrol computation, manual pump-speed/default-flow behavior, PumpFault alarm/control-release behavior, and cross-component fallback transitions remain present."}`
  - SL-10 evidence 5: `{"summary": "The repair is NL-grounded and does not invent autonomous plant dynamics: pump_fault is still cleared only on the caregiver FaultRemoved event, while Manual entry merely reflects the current fault state in alarm_signal. This is consistent with the NL requirement that pump faults activate alarm signals and that manual operation is the shared fallback target."}`
  - SL-10 evidence 6: `{"summary": "Local deterministic repair review reports ok=true, target_resolved=true, regression_detected=false, drift_risk=none, and no local rejection. The scenario summary reports 10 scenarios with no coverage_gap and no oracle_weak finding, supporting acceptance for the next full top-down revalidation pass."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。

</details>

<details><summary>Repair 3 / iteration `2` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:74b4333340ba8396c1696cf465c02e6614ac2b582ad47631a8bf8a7d47e26680`；candidate_dsl_hash：`sha256:c7b912815fce0736811c5a1361188b7cb22d932c2ba455ec05433adac293ffb1`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Pump-fault handling is not faithful across the mode-control hierarchy: the DSL only enters PumpFault from AutocontrolNormal, while StartAC and AutocontrolInit can proceed with an active pump_fault and AutocontrolInit explicitly clears the alarm.
- 2. `<unknown>` `` policy=``：An active modeled pump fault can be present while software control is enabled and alarms are cleared during AutocontrolInit, before the model reaches the only guarded fault transition from AutocontrolNormal.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-4a913dec7ae`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sl7-0-e56a9044a1` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: "If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals".', 'NL: "During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications."', 'DSL: `Ask_StartAC -> AutocontrolInit :: StartAC;` has no guard excluding `pump_fault > 0`.', 'DSL: `state AutocontrolInit { enter { CA_mode = 1; control_released = 0; alarm_signal = 0; } }` clears the alarm unconditionally.', 'DSL: the only explicit fault transition is `AutocontrolNormal -> PumpFault : if [pump_fault > 0];`.'], 'severity': 'major', 'summary': 'Pump-fault handling is not faithful across the mode-control hierarchy: the DSL only enters PumpFault from AutocontrolNormal, while StartAC and AutocontrolInit can proceed with an active pump_fault and AutocontrolInit explicitly clears the alarm.'}` |
| `fixreq-2-sl7-1-ef61a52a60` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL: `AutocontrolInit.enter` sets `control_released = 0` and `alarm_signal = 0` regardless of `pump_fault`.', 'DSL: `StartAC` transition from Ask_StartAC to AutocontrolInit is unguarded.', 'DSL: `PumpFault.enter` releases control and sets alarm, but it is only reachable from AutocontrolNormal via `pump_fault > 0`.', 'Simulation scenarios include normal StartAC and normal fault-from-AutocontrolNormal cases, but no scenario with `pump_fault = 1` during Ask_StartAC or AutocontrolInit.'], 'severity': 'major', 'summary': 'An active modeled pump fault can be present while software control is enabled and alarms are cleared during AutocontrolInit, before the model reaches the only guarded fault transition from AutocontrolNormal.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:blood_pressure, variable:target_bp, variable:requested_target_bp, variable:flow_rate, variable:default_flow_rate, ... +30`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2923`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sl7-0-e56a9044a1` | `accept` | ❌ | ❌ | The evidence identifies a real NL-fidelity gap: pump faults must activate alarms and normal autocontrol should only proceed without pump-operation complications, but the previous DSL could route StartAC into AutocontrolInit while pump_fault was already active. Because pyfcstm does not allow event+guard on one transition, the smallest safe faithful repair is ...<truncated 619 chars> |
| `fixreq-2-sl7-1-ef61a52a60` | `accept` | ❌ | ❌ | The unsafe-recovery evidence is valid: an active pump_fault could coexist with AutocontrolInit enabling software control and clearing alarms before the only old fault guard in AutocontrolNormal. The repair prevents active-fault StartAC from entering AutocontrolInit, makes AutocontrolInit safe if reached/initialized with a fault, and adds a direct guard from ...<truncated 257 chars> |
- repair_rationale：Request fixreq-2-sl7-0 expected active pump faults to activate alarms and prevent normal autocontrol from proceeding with pump-operation complications. Actual prior behavior allowed Ask_StartAC -> AutocontrolInit on StartAC even when pump_f...<truncated 51 chars>；Request fixreq-2-sl7-1 expected no state where active pump_fault coexists with enabled software control and cleared alarms during AutocontrolInit. Actual prior behavior set control_released = 0 and alarm_signal = 0 unconditionally in Autoco...<truncated 16 chars>；pyfcstm forbids combining an event trigger and guard on one transition, so the StartAC path is repaired by a small NL-grounded pseudo state StartACDecision: the StartAC event is preserved, but routing now sends pump_fault > 0 to PumpFault a...<truncated 43 chars>；AutocontrolInit.enter is made conservative: if entered with pump_fault > 0, it keeps alarms active and control released; otherwise it preserves the original normal autocontrol initialization behavior.；AutocontrolInit now has an explicit pump_fault guard to PumpFault before the guarded normal transition to AutocontrolNormal, so PumpFault is reachable before normal autocontrol, not only from AutocontrolNormal.
- diff_summary：`{"summary": "Added a pseudo StartACDecision state and guarded StartAC routing so active pump_fault goes to PumpFault while fault-free StartAC enters AutocontrolInit; made AutocontrolInit.enter fault-aware; changed AutocontrolInit's outgoing flow to route pump_fault > 0 to PumpFault and only pump_fault == 0 to AutocontrolNormal. Preserved prior Manual alarm and FaultRemoved pump_fault-clearing repairs."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def float blood_pressure = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 0;
def float buffer_bp = 0.0;
def float log_infusion_rate = 0.0;

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
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
                }
            }
            during {
                pump_speed = built_in_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC;

        pseudo state StartACDecision;

        state AutocontrolInit {
            enter {
                if [pump_fault > 0] {
                    CA_mode = 0;
                    control_released = 1;
                    alarm_signal = 1;
                } else {
                    CA_mode = 1;
                    control_released = 0;
                    alarm_signal = 0;
                }
            }
        }

        state AutocontrolNormal {
            during {
                buffer_bp = blood_pressure;
                if [blood_pressure > target_bp] {
                    flow_rate = flow_rate - 1.0;
                } else if [blood_pressure < target_bp] {
                    flow_rate = flow_rate + 1.0;
                } else {
                    flow_rate = flow_rate;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_infusion_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: SetpointChanged effect { target_bp = requested_target_bp; };
        Ask_StartAC -> StartACDecision :: StartAC;
        StartACDecision -> PumpFault : if [pump_fault > 0];
        StartACDecision -> AutocontrolInit : if [pump_fault == 0];
        AutocontrolInit -> PumpFault : if [pump_fault > 0];
        AutocontrolInit -> AutocontrolNormal : if [pump_fault == 0];
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -43,11 +43,19 @@
 
         state Ask_StartAC;
 
+        pseudo state StartACDecision;
+
         state AutocontrolInit {
             enter {
-                CA_mode = 1;
-                control_released = 0;
-                alarm_signal = 0;
+                if [pump_fault > 0] {
+                    CA_mode = 0;
+                    control_released = 1;
+                    alarm_signal = 1;
+                } else {
+                    CA_mode = 1;
+                    control_released = 0;
+                    alarm_signal = 0;
+                }
             }
         }
 
@@ -77,8 +85,11 @@
 
         Manual -> Ask_StartAC :: InitiateAC;
         Ask_StartAC -> Ask_StartAC :: SetpointChanged effect { target_bp = requested_target_bp; };
-        Ask_StartAC -> AutocontrolInit :: StartAC;
-        AutocontrolInit -> AutocontrolNormal;
+        Ask_StartAC -> StartACDecision :: StartAC;
+        StartACDecision -> PumpFault : if [pump_fault > 0];
+        StartACDecision -> AutocontrolInit : if [pump_fault == 0];
+        AutocontrolInit -> PumpFault : if [pump_fault > 0];
+        AutocontrolInit -> AutocontrolNormal : if [pump_fault == 0];
         AutocontrolNormal -> PumpFault : if [pump_fault > 0];
         PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
     }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:04a24d8b689c2c40a3a9dfa1e0e729dc150651d34ea6f2872740717ef7add405`。
  - SL-10 evidence 1: `{"summary": "Both current hard SL-7 requests identify the same real gap: active pump_fault could pass through StartAC into AutocontrolInit, where the old DSL unconditionally set control_released = 0 and alarm_signal = 0, while PumpFault was only reached from AutocontrolNormal. This violated the NL requirement that pump faults activate alarms and that normal autocontrol operates only without pump-operation complications."}`
  - SL-10 evidence 2: `{"summary": "SL-9 accepted both requests and the candidate makes the requested fault-aware repair: Ask_StartAC now handles StartAC by entering StartACDecision, which routes pump_fault > 0 to PumpFault and pump_fault == 0 to AutocontrolInit; AutocontrolInit.enter no longer clears alarms/enables software control when pump_fault > 0; and AutocontrolInit has an explicit guarded path to PumpFault before normal autocontrol."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff preserves the earlier accepted repairs recorded in the FixLog: Manual.enter keeps alarm_signal = 1 when pump_fault > 0 during forced Manual fallback, and PumpFault -> Manual :: FaultRemoved still has effect { pump_fault = 0; }. Thus the previous unresolved-fault recovery objections remain resolved while the new StartAC/AutocontrolInit unsafe path is addressed."}`
  - SL-10 evidence 4: `{"summary": "Required NL elements are not dropped in substance: Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, the required variables, InitiateAC, SetpointChanged, StartAC, TerminateAC, CA/CB/CP/CC_backManual, FaultRemoved, manual pump behavior, setpoint update, normal autocontrol flow computation, PumpFault alarm/control-release behavior, and cross-component fallback behavior remain represented."}`
  - SL-10 evidence 5: `{"summary": "The candidate is NL-grounded and does not invent autonomous fault dynamics: pump_fault remains an external/modeled fault flag and is cleared only by the caregiver FaultRemoved event. The added routing only prevents algorithmic pump control from proceeding when a modeled pump fault is already active, which is consistent with the NL pump-fault and no-complications obligations."}`
  - SL-10 evidence 6: `{"summary": "Scenario evidence reports 10 scenarios with coverage_gap=false and oracle_weak=false. No regression is reported; the remaining issue is local deterministic conservatism about structural drift and exact grounding identity rather than an observed behavioral failure."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.；For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-ground...<truncated 152 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `forced_transition_count_drift` {"fix_target": "model_review", "kind": "forced_transition_count_drift", "new": 30, "old": 25}
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:Ask_StartAC_to_AutocontrolInit"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `2` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:74b4333340ba8396c1696cf465c02e6614ac2b582ad47631a8bf8a7d47e26680`；candidate_dsl_hash：`sha256:55db32db5a501930ea9caacc612bf09595ad3465ad588dfebdd27c8de7eeebea`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Pump-fault handling is not faithful across the mode-control hierarchy: the DSL only enters PumpFault from AutocontrolNormal, while StartAC and AutocontrolInit can proceed with an active pump_fault and AutocontrolInit explicitly clears the alarm.
- 2. `<unknown>` `` policy=``：An active modeled pump fault can be present while software control is enabled and alarms are cleared during AutocontrolInit, before the model reaches the only guarded fault transition from AutocontrolNormal.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-4a913dec7ae`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sl7-0-e56a9044a1` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: "If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals".', 'NL: "During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications."', 'DSL: `Ask_StartAC -> AutocontrolInit :: StartAC;` has no guard excluding `pump_fault > 0`.', 'DSL: `state AutocontrolInit { enter { CA_mode = 1; control_released = 0; alarm_signal = 0; } }` clears the alarm unconditionally.', 'DSL: the only explicit fault transition is `AutocontrolNormal -> PumpFault : if [pump_fault > 0];`.'], 'severity': 'major', 'summary': 'Pump-fault handling is not faithful across the mode-control hierarchy: the DSL only enters PumpFault from AutocontrolNormal, while StartAC and AutocontrolInit can proceed with an active pump_fault and AutocontrolInit explicitly clears the alarm.'}` |
| `fixreq-2-sl7-1-ef61a52a60` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL: `AutocontrolInit.enter` sets `control_released = 0` and `alarm_signal = 0` regardless of `pump_fault`.', 'DSL: `StartAC` transition from Ask_StartAC to AutocontrolInit is unguarded.', 'DSL: `PumpFault.enter` releases control and sets alarm, but it is only reachable from AutocontrolNormal via `pump_fault > 0`.', 'Simulation scenarios include normal StartAC and normal fault-from-AutocontrolNormal cases, but no scenario with `pump_fault = 1` during Ask_StartAC or AutocontrolInit.'], 'severity': 'major', 'summary': 'An active modeled pump fault can be present while software control is enabled and alarms are cleared during AutocontrolInit, before the model reaches the only guarded fault transition from AutocontrolNormal.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:blood_pressure, variable:target_bp, variable:requested_target_bp, variable:flow_rate, variable:default_flow_rate, ... +30`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2757`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sl7-0-e56a9044a1` | `accept` | ❌ | ✅ | The request is valid and rework-locked: the current DSL lets StartAC enter AutocontrolInit while pump_fault is active, and AutocontrolInit clears alarm_signal and enables software control before fault handling. The rework memory also requires preserving the concrete required grounding for transition:Ask_StartAC_to_AutocontrolInit and reducing structural drif...<truncated 504 chars> |
| `fixreq-2-sl7-1-ef61a52a60` | `accept` | ❌ | ✅ | The unsafe-recovery evidence is valid: an active pump_fault could coexist with software control enabled and alarms cleared during AutocontrolInit. The smallest safe repair is to prevent AutocontrolInit from enabling control or clearing alarms under an active fault, and to make PumpFault reachable directly from AutocontrolInit before normal autocontrol begins...<truncated 223 chars> |
- repair_rationale：Expected for fixreq-2-sl7-0: pump faults activate alarms, and normal autocontrol proceeds only without pump-operation complications. Actual prior state: StartAC could enter AutocontrolInit with pump_fault > 0, AutocontrolInit cleared alarm_...<truncated 169 chars>；Expected for fixreq-2-sl7-1: active pump_fault must not coexist with software control enabled and alarms cleared in AutocontrolInit. Actual prior state: AutocontrolInit.enter always set control_released = 0 and alarm_signal = 0. The candida...<truncated 74 chars>；Rework objection missing_required_grounding for transition:Ask_StartAC_to_AutocontrolInit is resolved by preserving the concrete direct line `Ask_StartAC -> AutocontrolInit :: StartAC;`. This maintains the NL-required behavior that pressing...<truncated 97 chars>；Rework objection forced_transition_count_drift is addressed by avoiding the previous pseudo StartACDecision expansion. No pseudo state is added and the required StartAC transition is not split. The only structural transition change is repla...<truncated 130 chars>；Previous accepted repairs are preserved: Manual.enter keeps alarm_signal active when pump_fault remains active during forced Manual fallback, and FaultRemoved still clears pump_fault before returning from PumpFault to Manual.
- diff_summary：`{"summary": "Kept `Ask_StartAC -> AutocontrolInit :: StartAC` to preserve required grounding; changed AutocontrolInit.enter to be fault-aware; replaced the bare AutocontrolInit -> AutocontrolNormal transition with guarded transitions to PumpFault when pump_fault > 0 and to AutocontrolNormal only when pump_fault == 0. Preserved prior Manual alarm and FaultRemoved repairs."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def float blood_pressure = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_signal = 0;
def int control_released = 0;
def float buffer_bp = 0.0;
def float log_infusion_rate = 0.0;

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
                if [pump_fault > 0] {
                    alarm_signal = 1;
                } else {
                    alarm_signal = 0;
                }
            }
            during {
                pump_speed = built_in_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                if [pump_fault > 0] {
                    CA_mode = 0;
                    control_released = 1;
                    alarm_signal = 1;
                } else {
                    CA_mode = 1;
                    control_released = 0;
                    alarm_signal = 0;
                }
            }
        }

        state AutocontrolNormal {
            during {
                buffer_bp = blood_pressure;
                if [blood_pressure > target_bp] {
                    flow_rate = flow_rate - 1.0;
                } else if [blood_pressure < target_bp] {
                    flow_rate = flow_rate + 1.0;
                } else {
                    flow_rate = flow_rate;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_infusion_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: SetpointChanged effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> PumpFault : if [pump_fault > 0];
        AutocontrolInit -> AutocontrolNormal : if [pump_fault == 0];
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -45,9 +45,15 @@
 
         state AutocontrolInit {
             enter {
-                CA_mode = 1;
-                control_released = 0;
-                alarm_signal = 0;
+                if [pump_fault > 0] {
+                    CA_mode = 0;
+                    control_released = 1;
+                    alarm_signal = 1;
+                } else {
+                    CA_mode = 1;
+                    control_released = 0;
+                    alarm_signal = 0;
+                }
             }
         }
 
@@ -78,7 +84,8 @@
         Manual -> Ask_StartAC :: InitiateAC;
         Ask_StartAC -> Ask_StartAC :: SetpointChanged effect { target_bp = requested_target_bp; };
         Ask_StartAC -> AutocontrolInit :: StartAC;
-        AutocontrolInit -> AutocontrolNormal;
+        AutocontrolInit -> PumpFault : if [pump_fault > 0];
+        AutocontrolInit -> AutocontrolNormal : if [pump_fault == 0];
         AutocontrolNormal -> PumpFault : if [pump_fault > 0];
         PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
     }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:f6b4ef8168a199634114454e443f3de0776b03ee744c15ddda1601b1a6b5b285`。
  - SL-10 evidence 1: `{"summary": "The current rework-locked SL-7 requests required fixing the path where an active pump_fault could enter AutocontrolInit, clear alarm_signal, enable software control, and only later reach PumpFault from AutocontrolNormal. The candidate directly addresses this: AutocontrolInit.enter is now fault-aware, setting CA_mode = 0, control_released = 1, and alarm_signal = 1 when pump_fault > 0; AutocontrolInit routes to PumpFault when pump_fault > 0; and it reaches AutocontrolNormal only when pump_fault == 0."}`
  - SL-10 evidence 2: `{"summary": "The repair is faithful to the NL obligations that pump faults activate alarm signals and that normal autocontrol controls flow only when there are no pump-operation complications. A fault-free StartAC still enters AutocontrolInit and then AutocontrolNormal, while an active fault cannot proceed into normal autocontrol with software control enabled and alarms cleared."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff also resolves the remembered local objections from fixlog-8. The previous rejected candidate split `Ask_StartAC -> AutocontrolInit :: StartAC` through a pseudo StartACDecision state and caused local missing_required_grounding plus forced_transition_count_drift. The current candidate preserves the concrete required line `Ask_StartAC -> AutocontrolInit :: StartAC`, removes the pseudo-state expansion, and limits structural change to replacing the bare AutocontrolInit-to-normal transition with two guarded outcomes."}`
  - SL-10 evidence 4: `{"summary": "Previously accepted repairs remain intact: Manual.enter keeps alarm_signal active when pump_fault remains active during forced CA/CB/CP/CC_backManual or TerminateAC fallback, and PumpFault -> Manual :: FaultRemoved still clears pump_fault to model caregiver fault removal before manual recovery."}`
  - SL-10 evidence 5: `{"summary": "Required NL elements are preserved: Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, all required variables, InitiateAC, SetpointChanged, StartAC, TerminateAC, CA/CB/CP/CC_backManual, FaultRemoved, manual-mode pump behavior, setpoint update, normal autocontrol flow computation, PumpFault alarm/control-release behavior, and cross-component fallback to Manual remain represented."}`
  - SL-10 evidence 6: `{"summary": "Local deterministic repair review now reports ok=true, target_resolved=true, regression_detected=false, drift_risk=none, and no local_rejection. Scenario evidence reports 10 scenarios with coverage_gap=false and oracle_weak=false, so there is no local unresolved target, regression, or major drift requiring override."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-b98dd6bcea8` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-b98dd6bcea8` | accept=1, reject=0 | `sl10_review` | `sha256:8d8bee3d93ca11a6f72e62f677cf8efec1d48133d8ee73ceeef315da4e74ef9a` | Accepted the hard SL-7 model_review request because the evidence identifies a concrete unsafe recovery path., Expected safe recovery: after the caregiver removes the fault, Manual recovery should not have pump_fault still active while alarm_signal is cleared. Actual current behavior: PumpFault -> Manual on FaultRemoved left pump_fault = 1, then Manual.enter set alarm_signal = 0., The repair preserves the required FaultRemoved event and PumpFault_to_Manual transition while adding the grounded effect pump_fault = 0 to represent that the caregiver has removed the modeled fault., ... +1 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-b98dd6bcea8` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:8d8bee3d93ca11a6f72e62f677cf8efec1d48133d8ee73ceeef315da4e74ef9a` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +4 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-6884b412ad6` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-6884b412ad6` | accept=1, reject=0 | `sl10_review` | `sha256:74b4333340ba8396c1696cf465c02e6614ac2b582ad47631a8bf8a7d47e26680` | Accepted the hard model-review request because the current candidate fixed FaultRemoved but not the analogous forced-transition hazard from PumpFault to Manual., Expected behavior: cross-component backManual/TerminateAC may make CA_mode Manual, but an unresolved pump_fault must not be hidden; alarm_signal should remain active until the caregiver removes the fault., Actual behavior before this repair: the forced transitions entered Manual with pump_fault possibly still 1, and Manual.enter unconditionally set alarm_signal = 0., ... +2 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-6884b412ad6` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:74b4333340ba8396c1696cf465c02e6614ac2b582ad47631a8bf8a7d47e26680` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |
| 7 | `2` | `request_batch` | `fixbatch-2-sha256-4a913dec7ae` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 8 | `2` | `sl9_decision` | `fixbatch-2-sha256-4a913dec7ae` | accept=2, reject=0 | `sl10_review` | `sha256:c7b912815fce0736811c5a1361188b7cb22d932c2ba455ec05433adac293ffb1` | Request fixreq-2-sl7-0 expected active pump faults to activate alarms and prevent normal autocontrol from proceeding with pump-operation complications. Actual prior behavior allowed Ask_StartAC -> AutocontrolInit on StartAC even when pump_fault > 0, and AutocontrolInit cleared alarm_signal., Request fixreq-2-sl7-1 expected no state where active pump_fault coexists with enabled software control and cleared alarms during AutocontrolInit. Actual prior behavior set control_released = 0 and alarm_signal = 0 unconditionally in AutocontrolInit.enter., pyfcstm forbids combining an event trigger and guard on one transition, so the StartAC path is repaired by a small NL-grounded pseudo state StartACDecision: the StartAC event is preserved, but routing now sends pump_fault > 0 to PumpFault and only pump_fault == 0 to AutocontrolInit., ... +4 |
| 9 | `2` | `sl10_review` | `fixbatch-2-sha256-4a913dec7ae` | accept=2, reject=0 | `sl9_rework` | `sha256:c7b912815fce0736811c5a1361188b7cb22d932c2ba455ec05433adac293ffb1` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., For the next SL-9 repair, do not blindly regenerate the same DSL. Either change the candidate so the local major-drift evidence is resolved, or keep the minimal DSL only with explicit repair_rationale mapping each local objection (for example missing_required_grounding, scenario_regression, count_drift, or forced_transition_count_drift) to concrete NL-grounded states/transitions/actions that remain in the candidate. This rationale is required so SL-10 can produce local_override_rationale instead of cycling., repair_memory:SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., ... +13 |
| 10 | `2` | `sl9_rework_decision` | `fixbatch-2-sha256-4a913dec7ae` | accept=2, reject=0 | `sl10_review` | `sha256:55db32db5a501930ea9caacc612bf09595ad3465ad588dfebdd27c8de7eeebea` | Expected for fixreq-2-sl7-0: pump faults activate alarms, and normal autocontrol proceeds only without pump-operation complications. Actual prior state: StartAC could enter AutocontrolInit with pump_fault > 0, AutocontrolInit cleared alarm_signal, and PumpFault was only reached later from AutocontrolNormal. The candidate makes AutocontrolInit fault-aware and blocks AutocontrolNormal unless pump_fault == 0., Expected for fixreq-2-sl7-1: active pump_fault must not coexist with software control enabled and alarms cleared in AutocontrolInit. Actual prior state: AutocontrolInit.enter always set control_released = 0 and alarm_signal = 0. The candidate sets control_released = 1 and alarm_signal = 1 whenever pump_fault > 0., Rework objection missing_required_grounding for transition:Ask_StartAC_to_AutocontrolInit is resolved by preserving the concrete direct line `Ask_StartAC -> AutocontrolInit :: StartAC;`. This maintains the NL-required behavior that pressing StartAC enters AutocontrolInit, while AutocontrolInit itself now safely handles an active fault., ... +4 |
| 11 | `2` | `sl10_rework_review` | `fixbatch-2-sha256-4a913dec7ae` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:55db32db5a501930ea9caacc612bf09595ad3465ad588dfebdd27c8de7eeebea` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4638, 'completion_chars': 18237, 'completion_tokens': 6253, 'elapsed_seconds': 114.89401185000315, 'estimated_completion_tokens': 4560, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11217, 'first_chunk_seconds': 31.321472467010608, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12703}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1786, 'completion_chars': 6952, 'completion_tokens': 3676, 'elapsed_seconds': 68.51483234099578, 'estimated_completion_tokens': 1738, 'estimated_prompt_tokens': 14582, 'estimated_total_tokens': 16320, 'first_chunk_seconds': 36.7770484520006, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 58327, 'prompt_tokens': 14270, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 17946}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1490, 'completion_chars': 6857, 'completion_tokens': 2788, 'elapsed_seconds': 54.33949597500032, 'estimated_completion_tokens': 1715, 'estimated_prompt_tokens': 18646, 'estimated_total_tokens': 20361, 'first_chunk_seconds': 43.316042110993294, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 74584, 'prompt_tokens': 18748, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21536}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1008, 'completion_chars': 4226, 'completion_tokens': 1137, 'elapsed_seconds': 23.891955551021965, 'estimated_completion_tokens': 1057, 'estimated_prompt_tokens': 19781, 'estimated_total_tokens': 20838, 'first_chunk_seconds': 5.41650395601755, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 79123, 'prompt_tokens': 19056, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20193}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 396, 'completion_chars': 1777, 'completion_tokens': 596, 'elapsed_seconds': 13.96384435199434, 'estimated_completion_tokens': 445, 'estimated_prompt_tokens': 16685, 'estimated_total_tokens': 17130, 'first_chunk_seconds': 6.782640485995216, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 66739, 'prompt_tokens': 15876, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 16472}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3035, 'completion_chars': 12159, 'completion_tokens': 3494, 'elapsed_seconds': 65.14494124997873, 'estimated_completion_tokens': 3040, 'estimated_prompt_tokens': 19063, 'estimated_total_tokens': 22103, 'first_chunk_seconds': 10.453892784978962, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 76250, 'prompt_tokens': 18776, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22270}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2024, 'completion_chars': 9465, 'completion_tokens': 3052, 'elapsed_seconds': 57.487792667001486, 'estimated_completion_tokens': 2367, 'estimated_prompt_tokens': 20925, 'estimated_total_tokens': 23292, 'first_chunk_seconds': 20.94465555998613, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 83699, 'prompt_tokens': 21074, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24126}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1150, 'completion_chars': 4961, 'completion_tokens': 1505, 'elapsed_seconds': 29.867027477972442, 'estimated_completion_tokens': 1241, 'estimated_prompt_tokens': 34157, 'estimated_total_tokens': 35398, 'first_chunk_seconds': 9.549773313978221, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 136626, 'prompt_tokens': 32664, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 34169}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 616, 'completion_chars': 2927, 'completion_tokens': 745, 'elapsed_seconds': 19.80755252399831, 'estimated_completion_tokens': 732, 'estimated_prompt_tokens': 31336, 'estimated_total_tokens': 32068, 'first_chunk_seconds': 5.022167435003212, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 125343, 'prompt_tokens': 29639, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 30384}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3060, 'completion_chars': 12264, 'completion_tokens': 3452, 'elapsed_seconds': 67.92718371399678, 'estimated_completion_tokens': 3066, 'estimated_prompt_tokens': 21590, 'estimated_total_tokens': 24656, 'first_chunk_seconds': 12.672956199006876, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 86360, 'prompt_tokens': 21336, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24788}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2329, 'completion_chars': 10187, 'completion_tokens': 3366, 'elapsed_seconds': 64.22863849101122, 'estimated_completion_tokens': 2547, 'estimated_prompt_tokens': 23156, 'estimated_total_tokens': 25703, 'first_chunk_seconds': 24.15763236201019, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 92622, 'prompt_tokens': 23254, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26620}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1690, 'completion_chars': 7288, 'completion_tokens': 3763, 'elapsed_seconds': 71.34507972700521, 'estimated_completion_tokens': 1822, 'estimated_prompt_tokens': 53649, 'estimated_total_tokens': 55471, 'first_chunk_seconds': 40.601030477002496, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 214594, 'prompt_tokens': 50859, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 54622}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 893, 'completion_chars': 4292, 'completion_tokens': 1412, 'elapsed_seconds': 29.672120589006227, 'estimated_completion_tokens': 1073, 'estimated_prompt_tokens': 53294, 'estimated_total_tokens': 54367, 'first_chunk_seconds': 12.772002640005667, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 213173, 'prompt_tokens': 49872, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 51284}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1641, 'completion_chars': 7022, 'completion_tokens': 2153, 'elapsed_seconds': 42.03151855399483, 'estimated_completion_tokens': 1756, 'estimated_prompt_tokens': 79477, 'estimated_total_tokens': 81233, 'first_chunk_seconds': 12.382090691011399, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 317906, 'prompt_tokens': 73634, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 75787}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 614, 'completion_chars': 2822, 'completion_tokens': 738, 'elapsed_seconds': 17.37181159600732, 'estimated_completion_tokens': 706, 'estimated_prompt_tokens': 80723, 'estimated_total_tokens': 81429, 'first_chunk_seconds': 6.1838604290096555, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 322891, 'prompt_tokens': 74063, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 74801}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3415, 'completion_chars': 13703, 'completion_tokens': 3905, 'elapsed_seconds': 72.96671925598639, 'estimated_completion_tokens': 3426, 'estimated_prompt_tokens': 24411, 'estimated_total_tokens': 27837, 'first_chunk_seconds': 11.40927734199795, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 97641, 'prompt_tokens': 24120, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 28025}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1955, 'completion_chars': 9183, 'completion_tokens': 2474, 'elapsed_seconds': 47.31587987000239, 'estimated_completion_tokens': 2296, 'estimated_prompt_tokens': 26468, 'estimated_total_tokens': 28764, 'first_chunk_seconds': 12.584504859987646, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 105872, 'prompt_tokens': 26527, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 29001}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`53/16`，missing=`<none>`。
- repairs：`3/4` accepted；scenario_history=`7`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
