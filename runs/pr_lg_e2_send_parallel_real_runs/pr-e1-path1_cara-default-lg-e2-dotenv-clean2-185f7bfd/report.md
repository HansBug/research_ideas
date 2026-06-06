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
| Git commit | `93e4aa88d1e85c708aab022ca299b8f4fc343ae5` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:29acd3d1171a37b465f2b9278c85877dcbc5703e2d154247154b0c8cb90d6c8e` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:8e233622c2e3e55e2f1f038be5b3f9660f43a30a451fe052399864155456cb81", "iteration": 1, "matching_repair_history_indices": [1], "repair_history_index": 1, "selected_source_stage": "SL-7", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| SC-11 post-accept validation | attempted=`false`；attempts=`0`；success=`0`；failure=`0` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 231241, 'completion_tokens': 32991, 'total_tokens': 264232, 'estimated_prompt_tokens': 243455, 'estimated_completion_tokens': 25440, 'estimated_total_tokens': 268895, 'prompt_chars': 973804, 'completion_chars': 101739, 'n_calls': 11, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`647.519s` |
| run record | [`pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`flow_log.json`](./flow_log.json), [`fix_log.json`](./fix_log.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

### 1.1 LangGraph runtime metadata / checkpoint 口径

| 字段 | 值 |
|---|---|
| `graph_runtime_backend` | `langgraph` |
| `graph_runtime_status` | `enabled` |
| `graph_runtime_backend_version` | `pr-langgraph.stategraph.v1` |
| `langgraph_version` | `1.1.6` |
| `langgraph_checkpoint_version` | `4.0.1` |
| `graph_runtime_id` | `langgraph:pr-langgraph.stategraph.v1` |
| `graph_config_hash` | `sha256:85759c160e384ecfc9d360a5d66c68038e93757600633cf92a0b46e61d2ba8b2` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `60` |
| `langgraph_node_trace_hash` | `sha256:cddc8e87fe685e25138f3324751edc492edd20944e8708f38dfa66f577694f53` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `60` |

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
def float sensor_buffer_bp = 0.0;
def float target_blood_pressure = 100.0;
def float caregiver_target_blood_pressure = 100.0;
def float infusion_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int pump_complication = 0;
def int alarm_display = 0;
def int alarm_sound = 0;
def int control_released = 1;
def int log_record_count = 0;

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
                if [pump_complication == 0] {
                    alarm_display = 0;
                    alarm_sound = 0;
                } else {
                    alarm_display = 1;
                    alarm_sound = 1;
                }
            }
            during {
                pump_speed = built_in_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                control_released = 1;
            }
            during {
                target_blood_pressure = caregiver_target_blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                if [pump_complication == 0] {
                    CA_mode = 1;
                    control_released = 0;
                    alarm_display = 0;
                    alarm_sound = 0;
                } else {
                    CA_mode = 0;
                    control_released = 1;
                    alarm_display = 1;
                    alarm_sound = 1;
                }
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                control_released = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [pump_complication == 0] {
                    infusion_rate = target_blood_pressure - sensor_buffer_bp;
                    control_voltage = infusion_rate;
                    pump_speed = control_voltage;
                    log_record_count = log_record_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                alarm_display = 1;
                alarm_sound = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> PumpFault : if [pump_complication > 0];
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> PumpFault : if [pump_complication > 0];
        AutocontrolInit -> AutocontrolNormal :: InitComplete;
        AutocontrolNormal -> PumpFault : if [pump_complication > 0];
        PumpFault -> Manual :: FaultRemoved effect {
            pump_complication = 0;
            alarm_display = 0;
            alarm_sound = 0;
        };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12741 | 生成初始 DSL 与 grounding seeds | initial len=2820 | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=20, info=0; blocking=0, advisory=20, info=0; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=65449 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=68846 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=61855 | LLM per-request accept/reject + repair | candidate len=2993,3379 | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=55341 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=20, info=0; blocking=0, advisory=20, info=0; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=65449 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=68846 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=61855 | LLM per-request accept/reject + repair | candidate len=2993,3379 | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=55341 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=20, info=0; blocking=0, advisory=20, info=0; blocking=0, advisory=20, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=65449 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=3, tokens=68846 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-e2-dotenv-clean2-185f7bfd.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-06T08:05:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-06T08:05:29Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-06T08:05:29Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-06T08:05:29Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-06T08:07:39Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-06T08:07:39Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2820,hash=sha256:f8fc7fc18409 |
| 7 | `2026-06-06T08:07:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-06T08:07:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-06T08:07:39Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:f8fc7fc18409497e332adb20735d5529f3adee54c81966345c7e22c1f4f258d9 |
| 10 | `2026-06-06T08:07:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-06T08:07:39Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2820,hash=sha256:f8fc7fc18409, current_hash=sha256:f8fc7fc18409497e332adb20735d5529f3adee54c81966345c7e22c1f4f258d9 |
| 12 | `2026-06-06T08:07:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-06T08:07:39Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-06T08:07:39Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-06T08:07:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-06T08:07:39Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-06T08:07:39Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-06T08:07:39Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-06T08:07:40Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-06T08:07:40Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-06T08:07:40Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-06T08:07:40Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-06T08:09:07Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-06T08:09:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-06T08:09:07Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-06T08:09:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-06T08:09:07Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 28 | `2026-06-06T08:09:07Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 29 | `2026-06-06T08:09:07Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 30 | `2026-06-06T08:09:08Z` | `SD-6` | `0` | `lg_e2_send_parallel_result` | {} | <none> |
| 31 | `2026-06-06T08:09:08Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 32 | `2026-06-06T08:09:08Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 33 | `2026-06-06T08:09:08Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 34 | `2026-06-06T08:10:01Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-06T08:10:01Z` | `SL-7` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 36 | `2026-06-06T08:10:01Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 37 | `2026-06-06T08:10:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 38 | `2026-06-06T08:10:01Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["`! * -> Manual` transitions are available for backManual and TerminateAC from any substate, including PumpFault.", "`Manual.enter` unconditionally sets `alarm_display = 0` and `alarm_sound = 0`.", "`pump_complication` is only cleared by the explicit `FaultRemoved` effect, so a forced tra...<truncated 514 chars> | <none> |
| 39 | `2026-06-06T08:10:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-06T08:10:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 41 | `2026-06-06T08:10:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 42 | `2026-06-06T08:10:01Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["`! * -> Manual` transitions are available for backManual and TerminateAC from any substate, including PumpFault.", "`Manual.enter` unconditionally sets `alarm_display = 0` and `alarm_sound = 0`.", "`pump_complication` is only cleared by the explicit `FaultRemoved` effect, so a forced transition...<truncated 507 chars> | current_dsl:len=2820,hash=sha256:f8fc7fc18409 |
| 43 | `2026-06-06T08:10:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 44 | `2026-06-06T08:10:01Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 45 | `2026-06-06T08:10:01Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 1} | <none> |
| 46 | `2026-06-06T08:10:01Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 47 | `2026-06-06T08:10:01Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2820,hash=sha256:f8fc7fc18409 |
| 48 | `2026-06-06T08:10:33Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 49 | `2026-06-06T08:10:33Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2993,hash=sha256:8e7a16c271d7 |
| 50 | `2026-06-06T08:10:33Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 51 | `2026-06-06T08:10:34Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": true, "status": "StageStatus.OK"} | <none> |
| 52 | `2026-06-06T08:10:34Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:8e7a16c271d73f0bcf56927fc93c4ce5920460dc3fe3058174c9c68c988b67e8 |
| 53 | `2026-06-06T08:10:44Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 54 | `2026-06-06T08:10:44Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 55 | `2026-06-06T08:10:44Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 56 | `2026-06-06T08:10:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 57 | `2026-06-06T08:10:44Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2993,hash=sha256:8e7a16c271d7 |
| 58 | `2026-06-06T08:10:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 59 | `2026-06-06T08:10:44Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:8e7a16c271d73f0bcf56927fc93c4ce5920460dc3fe3058174c9c68c988b67e8 |
| 60 | `2026-06-06T08:10:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 61 | `2026-06-06T08:10:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 62 | `2026-06-06T08:10:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 63 | `2026-06-06T08:10:44Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:8e7a16c271d73f0bcf56927fc93c4ce5920460dc3fe3058174c9c68c988b67e8 |
| 64 | `2026-06-06T08:10:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 65 | `2026-06-06T08:10:44Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=2993,hash=sha256:8e7a16c271d7, current_hash=sha256:8e7a16c271d73f0bcf56927fc93c4ce5920460dc3fe3058174c9c68c988b67e8 |
| 66 | `2026-06-06T08:10:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 67 | `2026-06-06T08:10:44Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 68 | `2026-06-06T08:10:44Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 69 | `2026-06-06T08:10:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 70 | `2026-06-06T08:10:44Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 71 | `2026-06-06T08:10:44Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 72 | `2026-06-06T08:10:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 73 | `2026-06-06T08:10:44Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 74 | `2026-06-06T08:10:44Z` | `SD-4` | `1` | `stage_result` | {"jump": "SD-5A", "ok": true, "status": "StageStatus.OK"} | <none> |
| 75 | `2026-06-06T08:10:44Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 76 | `2026-06-06T08:10:45Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 targeted_retry", "ok": false, "reason": "reuse_frozen_scenario_set"} | <none> |
| 77 | `2026-06-06T08:10:45Z` | `<control>` | `1` | `frozen_scenario_refresh_targeted_retry` | {} | <none> |
| 78 | `2026-06-06T08:10:45Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 79 | `2026-06-06T08:10:45Z` | `SL-5` | `1` | `stage_enter` | {"reason": "targeted_refresh_after_frozen_gap_or_dsl_change"} | <none> |
| 80 | `2026-06-06T08:11:56Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
- ……另有 `83` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SL-7` | yes | fixbatch-0-sha256-46d238967f4 / n=1 | accept=1, reject=0, waiver=0 | ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SL-7` | yes | fixbatch-1-sha256-a0e43d2150b / n=3 | accept=3, reject=0, waiver=0 | ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| `default_init_manual_then_ask_startac` | default-init dispatches to Manual, then caregiver InitiateAC enters Ask_StartAC where the caregiver setpoint is copied t...<truncated 24 chars> | ✅ | ✅ | ✅ |
| `start_ac_then_init_complete_normal_control` | explicit-hot-start in Ask_StartAC probes StartAC to AutocontrolInit, then InitComplete to AutocontrolNormal with control...<truncated 38 chars> | ✅ | ✅ | ✅ |
| `normal_autocontrol_no_fault_boundary` | explicit-hot-start in AutocontrolNormal with pump_complication at the no-fault boundary 0 should not enter PumpFault and...<truncated 32 chars> | ✅ | ✅ | ✅ |
| `normal_autocontrol_fault_boundary_and_removed` | explicit-hot-start in AutocontrolNormal with pump_complication positive should enter PumpFault, alarm/release control, t...<truncated 35 chars> | ✅ | ✅ | ✅ |
| `manual_mode_uses_switch_and_default_flow` | explicit-hot-start in Manual verifies manual operation uses the built-in switch for pump speed and default flow rate for...<truncated 10 chars> | ✅ | ✅ | ✅ |
| `forced_ca_and_cb_back_manual` | explicit-hot-start in AutocontrolInit verifies CA_backManual forces Manual, then CB_backManual also forces Manual from A...<truncated 11 chars> | ✅ | ✅ | ✅ |
| `forced_cp_cc_and_terminate_back_manual` | explicit-hot-start in PumpFault verifies CP_backManual, CC_backManual, and TerminateAC each force the shared Manual reco...<truncated 53 chars> | ✅ | ✅ | ✅ |
| `forced_back_manual_from_active_fault_preserves_alarms` | explicit-hot-start in PumpFault with an unresolved pump complication verifies forced Manual recovery releases software c...<truncated 65 chars> | ⚪ | ✅ | ✅ |
| `ask_startac_fault_wrong_target_probe` | explicit-hot-start in Ask_StartAC with an existing pump complication verifies the safety guard targets PumpFault rather ...<truncated 26 chars> | ⚪ | ⚪ | ✅ |
| `autocontrol_init_fault_wrong_target_probe` | explicit-hot-start in AutocontrolInit with a pump complication verifies the safety guard targets PumpFault before normal...<truncated 20 chars> | ⚪ | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_then_ask_startac` — default-init dispatches to Manual, then caregiver InitiateAC enters Ask_StartAC where the caregiver setpoint is copied to target blood pressure.</summary>

| Field | Value |
|---|---|
| description | default-init dispatches to Manual, then caregiver InitiateAC enters Ask_StartAC where the caregiver setpoint is copied to target blood pressure. |
| initial_state | `<default-init>` |
| initial_vars | `{"built_in_switch_speed": 2.5, "caregiver_target_blood_pressure": 115.0, "default_flow_rate": 7.5}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `default_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 0, "alarm_sound": 0, "control_released": 1, "infusion_rate": 7.5, "pump_speed": 2.5}` |
| 1 `initiate_ac_enters_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"CA_mode": 0, "control_released": 1, "target_blood_pressure": 115.0}` |

</details>

<details><summary>`start_ac_then_init_complete_normal_control` — explicit-hot-start in Ask_StartAC probes StartAC to AutocontrolInit, then InitComplete to AutocontrolNormal with control outputs computed from blood pressure.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Ask_StartAC probes StartAC to AutocontrolInit, then InitComplete to AutocontrolNormal with control outputs computed from blood pressure. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"blood_pressure": 90.0, "caregiver_target_blood_pressure": 110.0, "log_record_count": 0, "pump_complication": 0, "target_blood_pressure": 110.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `start_ac_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_display": 0, "alarm_sound": 0, "control_released": 0, "sensor_buffer_bp": 90.0}` |
| 1 `init_complete_enters_normal_control` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolInit.InitComplete"]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 1, "control_released": 0, "control_voltage": 20.0, "infusion_rate": 20.0, "log_record_count": 1, "pump_speed": 20.0, "sensor_buffer_bp": 90.0}` |

</details>

<details><summary>`normal_autocontrol_no_fault_boundary` — explicit-hot-start in AutocontrolNormal with pump_complication at the no-fault boundary 0 should not enter PumpFault and should continue computing flow.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal with pump_complication at the no-fault boundary 0 should not enter PumpFault and should continue computing flow. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 80.0, "control_released": 0, "log_record_count": 2, "pump_complication": 0, "target_blood_pressure": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_fault_stays_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 20.0, "infusion_rate": 20.0, "log_record_count": 3, "pump_speed": 20.0, "sensor_buffer_bp": 80.0}` |

</details>

<details><summary>`normal_autocontrol_fault_boundary_and_removed` — explicit-hot-start in AutocontrolNormal with pump_complication positive should enter PumpFault, alarm/release control, then FaultRemoved returns to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal with pump_complication positive should enter PumpFault, alarm/release control, then FaultRemoved returns to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 95.0, "built_in_switch_speed": 1.5, "control_released": 0, "default_flow_rate": 6.0, "pump_complication": 1, "target_blood_pressure": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `positive_complication_enters_pumpfault` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_display": 1, "alarm_sound": 1, "control_released": 1}` |
| 1 `fault_removed_returns_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 0, "alarm_sound": 0, "control_released": 1, "infusion_rate": 6.0, "pump_complication": 0, "pump_speed": 1.5}` |

</details>

<details><summary>`manual_mode_uses_switch_and_default_flow` — explicit-hot-start in Manual verifies manual operation uses the built-in switch for pump speed and default flow rate for infusion.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Manual verifies manual operation uses the built-in switch for pump speed and default flow rate for infusion. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"built_in_switch_speed": 4.0, "default_flow_rate": 12.0, "infusion_rate": 0.0, "pump_speed": 0.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_during_sets_outputs` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"infusion_rate": 12.0, "pump_speed": 4.0}` |

</details>

<details><summary>`forced_ca_and_cb_back_manual` — explicit-hot-start in AutocontrolInit verifies CA_backManual forces Manual, then CB_backManual also forces Manual from Ask_StartAC.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolInit verifies CA_backManual forces Manual, then CB_backManual also forces Manual from Ask_StartAC. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "built_in_switch_speed": 2.0, "caregiver_target_blood_pressure": 118.0, "control_released": 0, "default_flow_rate": 8.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_back_manual_from_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 0, "alarm_sound": 0, "control_released": 1, "infusion_rate": 8.0, "pump_speed": 2.0}` |
| 1 `reenter_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"control_released": 1, "target_blood_pressure": 118.0}` |
| 2 `cb_back_manual_from_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "infusion_rate": 8.0, "pump_speed": 2.0}` |

</details>

<details><summary>`forced_cp_cc_and_terminate_back_manual` — explicit-hot-start in PumpFault verifies CP_backManual, CC_backManual, and TerminateAC each force the shared Manual recovery target from distinct autocontrol-re...<truncated 13 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in PumpFault verifies CP_backManual, CC_backManual, and TerminateAC each force the shared Manual recovery target from distinct autocontrol-related states. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_display": 1, "alarm_sound": 1, "blood_pressure": 85.0, "built_in_switch_speed": 3.0, "caregiver_target_blood_pressure": 105.0, "control_released": 0, "default_flow_rate": 9.0, "pump_complication": 0, "target_blood_pressure": 105.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_back_manual_from_pumpfault` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 0, "alarm_sound": 0, "control_released": 1, "infusion_rate": 9.0, "pump_speed": 3.0}` |
| 1 `go_to_ask_again` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_blood_pressure": 105.0}` |
| 2 `start_ac_to_autocontrol_init_again` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "control_released": 0, "sensor_buffer_bp": 85.0}` |
| 3 `cc_back_manual_from_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "control_released": 1, "infusion_rate": 9.0, "pump_speed": 3.0}` |
| 4 `go_to_normal_for_terminate_probe` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_blood_pressure": 105.0}` |
| 5 `start_ac_for_terminate_probe` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "control_released": 0}` |
| 6 `init_complete_for_terminate_probe` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolInit.InitComplete"]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 1, "control_released": 0, "control_voltage": 20.0, "infusion_rate": 20.0, "pump_speed": 20.0, "sensor_buffer_bp": 85.0}` |
| 7 `terminate_ac_from_autocontrol_normal` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 0, "alarm_sound": 0, "control_released": 1, "infusion_rate": 9.0, "pump_speed": 3.0}` |

</details>

<details><summary>`forced_back_manual_from_active_fault_preserves_alarms` — explicit-hot-start in PumpFault with an unresolved pump complication verifies forced Manual recovery releases software control but keeps alarm outputs active un...<truncated 25 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in PumpFault with an unresolved pump complication verifies forced Manual recovery releases software control but keeps alarm outputs active until the fault is removed. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_display": 1, "alarm_sound": 1, "built_in_switch_speed": 2.25, "control_released": 0, "default_flow_rate": 5.5, "pump_complication": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_back_manual_unresolved_fault_keeps_alarms` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_display": 1, "alarm_sound": 1, "control_released": 1, "infusion_rate": 5.5, "pump_complication": 1, "pump_speed": 2.25}` |

</details>

<details><summary>`ask_startac_fault_wrong_target_probe` — explicit-hot-start in Ask_StartAC with an existing pump complication verifies the safety guard targets PumpFault rather than starting autocontrol.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Ask_StartAC with an existing pump complication verifies the safety guard targets PumpFault rather than starting autocontrol. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 0, "alarm_display": 0, "alarm_sound": 0, "caregiver_target_blood_pressure": 112.0, "control_released": 1, "pump_complication": 1, "target_blood_pressure": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ask_startac_complication_enters_pumpfault` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_display": 1, "alarm_sound": 1, "control_released": 1}` |

</details>

<details><summary>`autocontrol_init_fault_wrong_target_probe` — explicit-hot-start in AutocontrolInit with a pump complication verifies the safety guard targets PumpFault before normal-control completion.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolInit with a pump complication verifies the safety guard targets PumpFault before normal-control completion. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "alarm_display": 0, "alarm_sound": 0, "blood_pressure": 92.0, "control_released": 0, "pump_complication": 1, "target_blood_pressure": 110.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `autocontrol_init_complication_enters_pumpfault` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_display": 1, "alarm_sound": 1, "control_released": 1}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:8e7a16c271d73f0bcf56927fc93c4ce5920460dc3fe3058174c9c68c988b67e8` |
| 2 | `1` | ✅ | `SL-7` | 0, 1, 2 | accept=3, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:8e233622c2e3e55e2f1f038be5b3f9660f43a30a451fe052399864155456cb81` |

<details><summary>Repair 1 / iteration `0` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:f8fc7fc18409497e332adb20735d5529f3adee54c81966345c7e22c1f4f258d9`；candidate_dsl_hash：`sha256:8e7a16c271d73f0bcf56927fc93c4ce5920460dc3fe3058174c9c68c988b67e8`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Forced fallback to Manual can clear pump-fault alarms without the caregiver fault-removal event, violating the intended safe fault handling sequence.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-46d238967f4`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['`! * -> Manual` transitions are available for backManual and TerminateAC from any substate, including PumpFault.', '`Manual.enter` unconditionally sets `alarm_display = 0` and `alarm_sound = 0`.', '`pump_complication` is only cleared by the explicit `FaultRemoved` effect, so a forced transition can leave the complication active while alarms are cleared.', 'NL requires pump faults to activate alarms and describes caregiver fault removal before recovery.'], 'severity': 'major', 'summary': 'Forced fallback to Manual can clear pump-fault alarms without the caregiver fault-removal event, violating the intended safe fault handling sequence.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:blood_pressure, variable:sensor_buffer_bp, variable:target_blood_pressure, variable:infusion_rate, variable:default_flow_rate, ... +24`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2993`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ❌ | The unsafe recovery finding is valid: forced backManual/TerminateAC transitions must remain NL-grounded, but Manual.enter should not unconditionally clear pump-fault alarms while pump_complication is still active. Repair keeps all required forced fallback events and makes alarm clearing conditional on the fault having been removed.；intent=Preserve forced Man...<truncated 185 chars> |
- repair_rationale：Accepted the hard model-review request because the current Manual.enter could clear alarm_display and alarm_sound after a forced fallback from PumpFault even though pump_complication remained active.；The smallest safe edit is localized to Manual.enter: CA_mode still becomes Manual and control_released remains asserted for shared recovery, but alarms are cleared only when pump_complication == 0.；If a forced CA_backManual, CB_backManual, CP_backManual, CC_backManual, or TerminateAC occurs while the fault flag is still active, Manual preserves/reasserts alarm_display = 1 and alarm_sound = 1 until the explicit FaultRemoved transition ...<truncated 35 chars>；All required states, variables, event transitions, guard transition to PumpFault, PumpFault.enter alarm behavior, and forced fallback transitions are preserved.
- diff_summary：`{"summary": "Modified only Manual.enter: replaced unconditional alarm_display/alarm_sound clearing with an if/else on pump_complication so active pump faults keep alarms on during forced Manual fallback, while normal Manual entry and FaultRemoved recovery still clear alarms."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float target_blood_pressure = 100.0;
def float caregiver_target_blood_pressure = 100.0;
def float infusion_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int pump_complication = 0;
def int alarm_display = 0;
def int alarm_sound = 0;
def int control_released = 1;
def int log_record_count = 0;

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
                if [pump_complication == 0] {
                    alarm_display = 0;
                    alarm_sound = 0;
                } else {
                    alarm_display = 1;
                    alarm_sound = 1;
                }
            }
            during {
                pump_speed = built_in_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                control_released = 1;
            }
            during {
                target_blood_pressure = caregiver_target_blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                control_released = 0;
                alarm_display = 0;
                alarm_sound = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                control_released = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [pump_complication == 0] {
                    infusion_rate = target_blood_pressure - sensor_buffer_bp;
                    control_voltage = infusion_rate;
                    pump_speed = control_voltage;
                    log_record_count = log_record_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                alarm_display = 1;
                alarm_sound = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal :: InitComplete;
        AutocontrolNormal -> PumpFault : if [pump_complication > 0];
        PumpFault -> Manual :: FaultRemoved effect {
            pump_complication = 0;
            alarm_display = 0;
            alarm_sound = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -30,8 +30,13 @@
             enter {
                 CA_mode = 0;
                 control_released = 1;
-                alarm_display = 0;
-                alarm_sound = 0;
+                if [pump_complication == 0] {
+                    alarm_display = 0;
+                    alarm_sound = 0;
+                } else {
+                    alarm_display = 1;
+                    alarm_sound = 1;
+                }
             }
             during {
                 pump_speed = built_in_switch_speed;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:016f8e943f226eca75a2f9fe4854b81ef86e671ffc23d9a4f3aef89d3e5ce96c`。
  - SL-10 evidence 1: `{"summary": "The hard SL-7 request identified an unsafe recovery path: global fallback events could force PumpFault to Manual and Manual.enter would clear alarm_display/alarm_sound even though pump_complication remained active, contrary to the NL sequence where pump faults activate alarms and the caregiver removes the fault before recovery."}`
  - SL-10 evidence 2: `{"summary": "SL-9 accepted the request and implemented the smallest NL-grounded repair: all required forced fallback transitions remain present, but Manual.enter now clears alarms only when pump_complication == 0 and otherwise reasserts alarm_display = 1 and alarm_sound = 1."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is localized to Manual.enter. It preserves the required states, variables, events, transitions, guard pump_complication > 0, PumpFault.enter alarm/control-release behavior, and FaultRemoved effect that clears pump_complication and alarms."}`
  - SL-10 evidence 4: `{"summary": "The repaired behavior matches the NL: CA_backManual/CB_backManual/CP_backManual/CC_backManual/TerminateAC still make CA_mode Manual and release software control for shared recovery, while an uncleared pump fault continues to produce visible and audible alarms until FaultRemoved clears the fault."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic repair review reports ok=true, target_resolved=true, regression_detected=false, and drift_risk=none; scenario coverage reports no coverage gap or weak oracle."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。

</details>

<details><summary>Repair 2 / iteration `1` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1, 2`。
- before_dsl_hash：`sha256:8e7a16c271d73f0bcf56927fc93c4ce5920460dc3fe3058174c9c68c988b67e8`；candidate_dsl_hash：`sha256:8e233622c2e3e55e2f1f038be5b3f9660f43a30a451fe052399864155456cb81`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Autocontrol initialization can clear alarms and keep software control active despite an unresolved pump complication.
- 2. `<unknown>` `` policy=``：The DSL does not preserve the NL's pump-fault alarm/release behavior across all CARA-controlled autocontrol behavior.
- 3. `<unknown>` `` policy=``：Estimated NFRR tier is capped at T1 diagnostic_only due to missing required safety-relevant pump-fault handling in autocontrol initialization.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-a0e43d2150b`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`3`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sl7-0-3096823055` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['`Ask_StartAC -> AutocontrolInit :: StartAC` is unguarded.', '`AutocontrolInit.enter` sets `control_released = 0`, `alarm_display = 0`, and `alarm_sound = 0` unconditionally.', 'Only `AutocontrolNormal` has `pump_complication > 0` routing to `PumpFault`.', 'NL requires pump faults to activate alarms and, when CARA was controlling the pump, release software control.'], 'severity': 'major', 'summary': 'Autocontrol initialization can clear alarms and keep software control active despite an unresolved pump complication.'}` |
| `fixreq-1-sl7-1-f1f2c62158` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL states broad fault semantics for pump faults, not only faults detected during `AutocontrolNormal`.', 'DSL marks `AutocontrolInit` as CARA control with `CA_mode = 1` and `control_released = 0`.', 'A positive `pump_complication` during or before `AutocontrolInit` is not forced to `PumpFault` or a diagnostic/fail-safe branch.'], 'severity': 'major', 'summary': "The DSL does not preserve the NL's pump-fault alarm/release behavior across all CARA-controlled autocontrol behavior."}` |
| `fixreq-1-sl7-2-2d6f65a397` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nfrr_quality_cap', 'evidence': ['The required states and many required transitions are present.', 'However, a required fault-handling behavior is incomplete for a CARA-controlled state.', 'This missing guard/transition/action family is safety-relevant and blocks within-scope candidate status.'], 'severity': 'major', 'summary': 'Estimated NFRR tier is capped at T1 diagnostic_only due to missing required safety-relevant pump-fault handling in autocontrol initialization.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:blood_pressure, variable:sensor_buffer_bp, variable:target_blood_pressure, variable:infusion_rate, variable:default_flow_rate, ... +24`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3379`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sl7-0-3096823055` | `accept` | ❌ | ❌ | The unsafe recovery finding is valid. AutocontrolInit was entered by an unguarded StartAC transition and then unconditionally cleared alarms and asserted active software control even if pump_complication was already positive. The repair adds NL-grounded fault routing before and during autocontrol initialization and makes AutocontrolInit.enter fail safe when ...<truncated 319 chars> |
| `fixreq-1-sl7-1-f1f2c62158` | `accept` | ❌ | ❌ | The NL-fidelity finding is valid. The NL describes broad pump-fault alarm and release behavior, not only fault handling in AutocontrolNormal. The repair extends the same pump_complication-positive fail-safe behavior to the Ask_StartAC/AutocontrolInit portion of the autocontrol path while preserving all required states, events, and fallback transitions.；inten...<truncated 216 chars> |
| `fixreq-1-sl7-2-2d6f65a397` | `accept` | ❌ | ❌ | The NFRR quality-cap finding is valid because the missing safety-relevant fault-handling family for AutocontrolInit prevented a within-scope candidate despite broad element coverage. The repair adds the missing guard/action family without deleting required NL-grounded elements or inventing unrelated plant dynamics.；intent=Add safety-relevant pump-fault guard...<truncated 156 chars> |
- repair_rationale：The current batch introduces new evidence beyond the prior accepted Manual.enter repair: the remaining unsafe gap is before and during AutocontrolInit, where unresolved pump_complication could be masked by unconditional alarm clearing and a...<truncated 14 chars>；For fixreq-1-sl7-0, expected behavior is that pump faults activate alarms and release software control; actual behavior was StartAC entering AutocontrolInit unconditionally and AutocontrolInit.enter setting control_released = 0, alarm_displ...<truncated 182 chars>；For fixreq-1-sl7-1, expected NL fidelity is broad pump-fault handling across CARA-controlled autocontrol behavior; actual behavior only routed AutocontrolNormal to PumpFault. The candidate preserves AutocontrolNormal -> PumpFault and extend...<truncated 56 chars>；For fixreq-1-sl7-2, the safety-relevant missing guard/action family is repaired without broad rewrite: PumpFault remains the alarm/release branch, StartAC remains represented for the no-fault path, and all required states, variables, events...<truncated 105 chars>；The previous non-regressive repair to Manual.enter is preserved: forced backManual/TerminateAC events still make CA_mode Manual and release control, while alarms remain asserted when pump_complication is still active.
- diff_summary：`{"summary": "Preserved the prior Manual.enter alarm-preservation repair. Added Ask_StartAC -> PumpFault : if [pump_complication > 0] before the StartAC transition, added AutocontrolInit -> PumpFault : if [pump_complication > 0], and changed AutocontrolInit.enter from unconditional active-control/alarm-clear assignments to an if/else that activates control only when there is no complication and otherwise keeps alarms on with control released."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float target_blood_pressure = 100.0;
def float caregiver_target_blood_pressure = 100.0;
def float infusion_rate = 0.0;
def float default_flow_rate = 0.0;
def float built_in_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int pump_complication = 0;
def int alarm_display = 0;
def int alarm_sound = 0;
def int control_released = 1;
def int log_record_count = 0;

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
                if [pump_complication == 0] {
                    alarm_display = 0;
                    alarm_sound = 0;
                } else {
                    alarm_display = 1;
                    alarm_sound = 1;
                }
            }
            during {
                pump_speed = built_in_switch_speed;
                infusion_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            enter {
                CA_mode = 0;
                control_released = 1;
            }
            during {
                target_blood_pressure = caregiver_target_blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                if [pump_complication == 0] {
                    CA_mode = 1;
                    control_released = 0;
                    alarm_display = 0;
                    alarm_sound = 0;
                } else {
                    CA_mode = 0;
                    control_released = 1;
                    alarm_display = 1;
                    alarm_sound = 1;
                }
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                control_released = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                if [pump_complication == 0] {
                    infusion_rate = target_blood_pressure - sensor_buffer_bp;
                    control_voltage = infusion_rate;
                    pump_speed = control_voltage;
                    log_record_count = log_record_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                alarm_display = 1;
                alarm_sound = 1;
                control_released = 1;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> PumpFault : if [pump_complication > 0];
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> PumpFault : if [pump_complication > 0];
        AutocontrolInit -> AutocontrolNormal :: InitComplete;
        AutocontrolNormal -> PumpFault : if [pump_complication > 0];
        PumpFault -> Manual :: FaultRemoved effect {
            pump_complication = 0;
            alarm_display = 0;
            alarm_sound = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -56,10 +56,17 @@
 
         state AutocontrolInit {
             enter {
-                CA_mode = 1;
-                control_released = 0;
-                alarm_display = 0;
-                alarm_sound = 0;
+                if [pump_complication == 0] {
+                    CA_mode = 1;
+                    control_released = 0;
+                    alarm_display = 0;
+                    alarm_sound = 0;
+                } else {
+                    CA_mode = 0;
+                    control_released = 1;
+                    alarm_display = 1;
+                    alarm_sound = 1;
+                }
             }
             during {
                 sensor_buffer_bp = blood_pressure;
@@ -92,7 +99,9 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
+        Ask_StartAC -> PumpFault : if [pump_complication > 0];
         Ask_StartAC -> AutocontrolInit :: StartAC;
+        AutocontrolInit -> PumpFault : if [pump_complication > 0];
         AutocontrolInit -> AutocontrolNormal :: InitComplete;
         AutocontrolNormal -> PumpFault : if [pump_complication > 0];
         PumpFault -> Manual :: FaultRemoved effect {
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:d7f5dda50c323f7cdaac9f8894af00a1a56786f1794eb1c13369fba661dea53a`。
  - SL-10 evidence 1: `{"summary": "The current hard SL-7 requests target the remaining pump-fault gap after the prior accepted Manual.enter repair: an unresolved or newly occurring pump_complication could pass through Ask_StartAC/AutocontrolInit, where AutocontrolInit.enter previously cleared alarm_display/alarm_sound and set control_released = 0 despite the NL requiring pump faults to activate alarms and release software control when CARA was controlling the pump."}`
  - SL-10 evidence 2: `{"summary": "SL-9 accepted all three hard requests and implemented the requested NL-grounded safety extension: Ask_StartAC now has a pump_complication > 0 route to PumpFault before the normal StartAC path, AutocontrolInit now has a pump_complication > 0 route to PumpFault, and AutocontrolInit.enter is conditional so active complications keep CA_mode = 0, control_released = 1, alarm_display = 1, and alarm_sound = 1 instead of asserting active control and clearing alarms."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff preserves all required NL elements and previous repairs: Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, StartAC, InitiateAC, InitComplete, AutocontrolNormal -> PumpFault, FaultRemoved, the forced CA/CB/CP/CC/TerminateAC Manual fallbacks, Manual's manual pump behavior, AutocontrolNormal's blood-pressure-based flow computation/logging abstraction, and the prior Manual.enter alarm-preservation behavior remain present."}`
  - SL-10 evidence 4: `{"summary": "The repaired behavior is aligned with the NL sequence. Normal no-fault StartAC still enters AutocontrolInit and can proceed to AutocontrolNormal; if pump_complication is positive before or during initialization, the model now reaches or emulates the PumpFault alarm/release semantics rather than clearing alarms and keeping software control active. FaultRemoved remains the explicit recovery effect that clears pump_complication and alarms."}`
  - SL-10 evidence 5: `{"summary": "The complete FixLog shows the previous iteration's objection about forced fallback clearing alarms was resolved and preserved in this candidate. The current candidate adds only the missing initialization-phase fault guard/action family identified in the iteration-1 repair_memory and SL-7 findings, without repeating the earlier unsafe behavior or introducing external plant dynamics."}`
  - SL-10 evidence 6: `{"summary": "Local deterministic repair review reports ok=true, target_resolved=true, regression_detected=false, drift_risk=none, and no local_rejection. Scenario coverage reports no coverage_gap and no oracle_weak finding, with applicable mutation classes caught."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-46d238967f4` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-46d238967f4` | accept=1, reject=0 | `sl10_review` | `sha256:8e7a16c271d73f0bcf56927fc93c4ce5920460dc3fe3058174c9c68c988b67e8` | Accepted the hard model-review request because the current Manual.enter could clear alarm_display and alarm_sound after a forced fallback from PumpFault even though pump_complication remained active., The smallest safe edit is localized to Manual.enter: CA_mode still becomes Manual and control_released remains asserted for shared recovery, but alarms are cleared only when pump_complication == 0., If a forced CA_backManual, CB_backManual, CP_backManual, CC_backManual, or TerminateAC occurs while the fault flag is still active, Manual preserves/reasserts alarm_display = 1 and alarm_sound = 1 until the explicit FaultRemoved transition clears the complication and alarms., ... +1 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-46d238967f4` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:8e7a16c271d73f0bcf56927fc93c4ce5920460dc3fe3058174c9c68c988b67e8` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +4 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-a0e43d2150b` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-a0e43d2150b` | accept=3, reject=0 | `sl10_review` | `sha256:8e233622c2e3e55e2f1f038be5b3f9660f43a30a451fe052399864155456cb81` | The current batch introduces new evidence beyond the prior accepted Manual.enter repair: the remaining unsafe gap is before and during AutocontrolInit, where unresolved pump_complication could be masked by unconditional alarm clearing and active control., For fixreq-1-sl7-0, expected behavior is that pump faults activate alarms and release software control; actual behavior was StartAC entering AutocontrolInit unconditionally and AutocontrolInit.enter setting control_released = 0, alarm_display = 0, and alarm_sound = 0. The candidate adds Ask_StartAC -> PumpFault and AutocontrolInit -> PumpFault guards on pump_complication > 0 and makes AutocontrolInit.enter conditional., For fixreq-1-sl7-1, expected NL fidelity is broad pump-fault handling across CARA-controlled autocontrol behavior; actual behavior only routed AutocontrolNormal to PumpFault. The candidate preserves AutocontrolNormal -> PumpFault and extends equivalent guard coverage to the initialization phase., ... +3 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-a0e43d2150b` | accept=3, reject=0 | `sc11_accept_then_sd2` | `sha256:8e233622c2e3e55e2f1f038be5b3f9660f43a30a451fe052399864155456cb81` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +6 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4247, 'completion_chars': 16905, 'completion_tokens': 6291, 'elapsed_seconds': 129.5469801449217, 'estimated_completion_tokens': 4227, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 10884, 'first_chunk_seconds': 52.47430834895931, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12741}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3017, 'completion_chars': 12120, 'completion_tokens': 4742, 'elapsed_seconds': 87.12586419191211, 'estimated_completion_tokens': 3030, 'estimated_prompt_tokens': 14044, 'estimated_total_tokens': 17074, 'first_chunk_seconds': 34.15095630986616, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 56174, 'prompt_tokens': 13688, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 18430}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1809, 'completion_chars': 8381, 'completion_tokens': 2830, 'elapsed_seconds': 53.00022087106481, 'estimated_completion_tokens': 2096, 'estimated_prompt_tokens': 17987, 'estimated_total_tokens': 20083, 'first_chunk_seconds': 21.926839540014043, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 71948, 'prompt_tokens': 17915, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20745}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1154, 'completion_chars': 5082, 'completion_tokens': 1609, 'elapsed_seconds': 32.71672792499885, 'estimated_completion_tokens': 1271, 'estimated_prompt_tokens': 20441, 'estimated_total_tokens': 21712, 'first_chunk_seconds': 12.134127245983109, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 81763, 'prompt_tokens': 19203, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20812}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 362, 'completion_chars': 1671, 'completion_tokens': 423, 'elapsed_seconds': 10.373102640034631, 'estimated_completion_tokens': 418, 'estimated_prompt_tokens': 17552, 'estimated_total_tokens': 17970, 'first_chunk_seconds': 3.9012496459763497, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 70205, 'prompt_tokens': 16141, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 16564}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3303, 'completion_chars': 13285, 'completion_tokens': 3822, 'elapsed_seconds': 71.04674465605058, 'estimated_completion_tokens': 3322, 'estimated_prompt_tokens': 18557, 'estimated_total_tokens': 21879, 'first_chunk_seconds': 11.63916655885987, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 74226, 'prompt_tokens': 18177, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 21999}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1968, 'completion_chars': 8948, 'completion_tokens': 3254, 'elapsed_seconds': 62.82959364098497, 'estimated_completion_tokens': 2237, 'estimated_prompt_tokens': 19783, 'estimated_total_tokens': 22020, 'first_chunk_seconds': 28.234486172907054, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 79131, 'prompt_tokens': 19614, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22868}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1841, 'completion_chars': 8202, 'completion_tokens': 2868, 'elapsed_seconds': 54.343815966974944, 'estimated_completion_tokens': 2051, 'estimated_prompt_tokens': 41470, 'estimated_total_tokens': 43521, 'first_chunk_seconds': 21.20249719102867, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 165878, 'prompt_tokens': 38175, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 41043}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 603, 'completion_chars': 2834, 'completion_tokens': 696, 'elapsed_seconds': 15.800899172900245, 'estimated_completion_tokens': 709, 'estimated_prompt_tokens': 42296, 'estimated_total_tokens': 43005, 'first_chunk_seconds': 4.961230638902634, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 169182, 'prompt_tokens': 38081, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 38777}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3774, 'completion_chars': 15193, 'completion_tokens': 4057, 'elapsed_seconds': 76.79686408583075, 'estimated_completion_tokens': 3799, 'estimated_prompt_tokens': 21532, 'estimated_total_tokens': 25331, 'first_chunk_seconds': 9.109900390030816, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 86127, 'prompt_tokens': 20963, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25020}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1880, 'completion_chars': 9118, 'completion_tokens': 2399, 'elapsed_seconds': 45.46583379688673, 'estimated_completion_tokens': 2280, 'estimated_prompt_tokens': 23136, 'estimated_total_tokens': 25416, 'first_chunk_seconds': 13.57120311097242, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 92544, 'prompt_tokens': 22834, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25233}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`38/16`，missing=`<none>`。
- repairs：`2/2` accepted；scenario_history=`5`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
