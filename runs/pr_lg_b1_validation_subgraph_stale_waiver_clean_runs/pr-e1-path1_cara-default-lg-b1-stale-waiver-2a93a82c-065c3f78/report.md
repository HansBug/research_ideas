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
| Git commit | `2a93a82c8c55e520d2f5cca317d67f2d4ee1221d` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:e2cfdd7ab1fd43540a75a5216158706cc6809d0eb975e3731e90124b8a1ff158` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `false` |
| state_mode_decorative_detected | `false` |
| path2_ref_model_blueprint_eligible | `n/a`；not_applicable_to_path1 |
| final.fcstm 来源 | `{"final_dsl_hash": "sha256:691c0b28fabc7e9dbe3443abafac6dda253d354c480d9f1670e6257a5bf3e921", "source_kind": "initial_or_unrepaired"}` |
| FixLog next_action 序列 | `<none>` |
| iteration exit_reason 序列 | `full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 79209, 'completion_tokens': 20174, 'total_tokens': 99383, 'estimated_prompt_tokens': 81094, 'estimated_completion_tokens': 16018, 'estimated_total_tokens': 97112, 'prompt_chars': 324365, 'completion_chars': 64067, 'n_calls': 5, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`379.371s` |
| run record | [`pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
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
| `graph_config_hash` | `sha256:5c962c628cf4722c88349e5a920dd11465e76171f36e6b0e8a1b21b76fac8185` |
| `node_edge_schema_version` | `pr-langgraph.stage-nodes.v1` |
| `checkpoint_backend` | `memory` |
| `checkpoint_backend_type` | `InMemorySaver` |
| `checkpoint_serde` | `pickle` |
| `checkpoint_path_hash` | `sha256:memory` |
| `resumed_from_checkpoint` | `False` |
| `resume_checkpoint_id_hash` | `None` |
| `instrumentation_layer` | `langgraph` |
| `stage_semantics_module` | `method.staged_runtime` |
| `langgraph_node_trace_count` | `20` |
| `langgraph_node_trace_hash` | `sha256:0275a55617f1fbea9405e3ae8b4ef64da7b526ab57d2e353aebdb2200aa99d67` |
| `langgraph_compat_ok` | `True` |
| `checkpoint_resume_smoke_scope` | `toy_ledger_langgraph_api_smoke` |
| `real_agent_loop_resume_supported` | `False` |
| `resume_append_only` | `True` |
| `final_trace_delegated_monolithic_runtime` | `False` |
| `final_trace_node_trace_count` | `20` |

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
def int alarm_signal = 0;
def int software_control = 0;
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float target_bp = 100.0;
def float target_bp_command = 100.0;
def float flow_rate = 0.0;
def float default_manual_flow_rate = 0.0;
def float builtin_switch_speed = 0.0;
def float control_voltage = 0.0;
def float pump_speed = 0.0;
def float infusion_log_rate = 0.0;

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
                control_voltage = 0.0;
                flow_rate = default_manual_flow_rate;
                pump_speed = builtin_switch_speed;
            }
            during {
                sensor_buffer_bp = blood_pressure;
                flow_rate = default_manual_flow_rate;
                pump_speed = builtin_switch_speed;
            }
        }

        state Ask_StartAC {
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
            }
            during {
                sensor_buffer_bp = blood_pressure;
            }
        }

        state AutocontrolNormal {
            during {
                sensor_buffer_bp = blood_pressure;
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    infusion_log_rate = flow_rate;
                }
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
            }
        }

        Manual -> Ask_StartAC :: InitiateAlgorithmicControl;
        Ask_StartAC -> Ask_StartAC :: SetpointChanged effect {
            target_bp = target_bp_command;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC effect {
            software_control = 1;
            CA_mode = 1;
        };
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual :: TerminateAlgorithmicControl;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: CaregiverRemovesFault effect {
            pump_fault = 0;
            alarm_signal = 0;
        };
    }
}

```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12256 | 生成初始 DSL 与 grounding seeds | initial len=2843 | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=20, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=63595 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=63595 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=3, tokens=63595 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=23532 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-lg-b1-stale-waiver-2a93a82c-065c3f78.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-05T09:37:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 2 | `2026-06-05T09:37:30Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 3 | `2026-06-05T09:37:30Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 4 | `2026-06-05T09:37:30Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 5 | `2026-06-05T09:39:17Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 6 | `2026-06-05T09:39:17Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2843,hash=sha256:691c0b28fabc |
| 7 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 8 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 9 | `2026-06-05T09:39:17Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:691c0b28fabc7e9dbe3443abafac6dda253d354c480d9f1670e6257a5bf3e921 |
| 10 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 11 | `2026-06-05T09:39:17Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2843,hash=sha256:691c0b28fabc, current_hash=sha256:691c0b28fabc7e9dbe3443abafac6dda253d354c480d9f1670e6257a5bf3e921 |
| 12 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 13 | `2026-06-05T09:39:17Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 14 | `2026-06-05T09:39:17Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 16 | `2026-06-05T09:39:17Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 17 | `2026-06-05T09:39:17Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 18 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 19 | `2026-06-05T09:39:17Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 20 | `2026-06-05T09:39:17Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-05T09:39:17Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 22 | `2026-06-05T09:39:17Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 23 | `2026-06-05T09:40:37Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 24 | `2026-06-05T09:40:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 25 | `2026-06-05T09:40:37Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 26 | `2026-06-05T09:40:37Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 27 | `2026-06-05T09:40:37Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 28 | `2026-06-05T09:41:31Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-05T09:41:31Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 30 | `2026-06-05T09:41:32Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 31 | `2026-06-05T09:41:32Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 32 | `2026-06-05T09:41:32Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 33 | `2026-06-05T09:42:54Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 34 | `2026-06-05T09:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 35 | `2026-06-05T09:42:54Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 36 | `2026-06-05T09:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 37 | `2026-06-05T09:42:54Z` | `<control>` | `0` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 38 | `2026-06-05T09:42:54Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": null} | <none> |
| 39 | `2026-06-05T09:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 40 | `2026-06-05T09:42:54Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 41 | `2026-06-05T09:42:54Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 42 | `2026-06-05T09:42:54Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 43 | `2026-06-05T09:42:54Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 44 | `2026-06-05T09:43:48Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 45 | `2026-06-05T09:43:48Z` | `SL-7` | `0` | `stage_result` | {"jump": "SC-12 success", "ok": true, "status": "StageStatus.OK"} | <none> |
| 46 | `2026-06-05T09:43:48Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 47 | `2026-06-05T09:43:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 48 | `2026-06-05T09:43:48Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SC-12 success", "selected_feedback": null} | <none> |
| 49 | `2026-06-05T09:43:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 50 | `2026-06-05T09:43:48Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "full_pass_all_required_feedback_ok", "verdict": "success"} | final_dsl:len=2843,hash=sha256:691c0b28fabc |
| 51 | `2026-06-05T09:43:48Z` | `<control>` | `-` | `langgraph_node_event` | {} | <none> |
| 52 | `2026-06-05T09:43:48Z` | `SC-13` | `-` | `run_end` | {"verdict": "success"} | final_dsl:len=2843,hash=sha256:691c0b28fabc |
| 53 | `` | `<control>` | `-` | `langgraph_node_trace` | {} | <none> |
| 54 | `` | `<control>` | `-` | `lg_d1_operator_log_artifacts` | {} | <none> |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_manual_outputs` | default-init dispatches into Manual and checks manual pump speed/flow come from the built-in switch and default manual f...<truncated 9 chars> | ✅ |
| `initiate_and_change_setpoint_in_ask_startac` | default-init first reaches Manual, then caregiver initiates algorithmic control and changes the setpoint within Ask_Star...<truncated 4 chars> | ✅ |
| `start_ac_init_then_normal_control` | explicit-hot-start in Ask_StartAC checks StartAC enters AutocontrolInit, then automatic progression reaches normal autoc...<truncated 30 chars> | ✅ |
| `autocontrol_no_fault_boundary_stays_normal` | explicit-hot-start in AutocontrolNormal with pump_fault at the no-fault boundary verifies no fault transition fires and ...<truncated 24 chars> | ✅ |
| `pump_fault_boundary_enters_fault_and_alarms` | explicit-hot-start in AutocontrolNormal with pump_fault present verifies transition to PumpFault activates alarm and rel...<truncated 23 chars> | ✅ |
| `caregiver_removes_fault_returns_manual` | explicit-hot-start in PumpFault checks caregiver fault removal returns to Manual, clears the fault/alarm, and keeps soft...<truncated 22 chars> | ✅ |
| `terminate_autocontrol_returns_manual` | explicit-hot-start in AutocontrolNormal checks caregiver termination of algorithmic control returns to Manual and restor...<truncated 24 chars> | ✅ |
| `forced_back_manual_events_from_distinct_modes` | explicit-hot-start probes wildcard backManual recovery from several concrete leaves, each requiring Manual as the shared...<truncated 17 chars> | ✅ |
| `forced_cp_back_manual_from_pump_fault` | explicit-hot-start in PumpFault checks CP_backManual also forces Manual as the shared recovery target. | ✅ |
| `forced_cc_back_manual_from_autocontrol_init` | explicit-hot-start in AutocontrolInit checks CC_backManual overrides autocontrol initialization and forces Manual recove...<truncated 3 chars> | ✅ |
| `setpoint_effect_used_by_autocontrol_flow` | explicit-hot-start in Ask_StartAC strengthens the SetpointChanged effect probe by requiring the changed target setpoint ...<truncated 52 chars> | ✅ |
| `fault_removal_effect_clears_fault_and_alarm_values` | explicit-hot-start in PumpFault isolates the CaregiverRemovesFault transition effect so missing or wrong constant assign...<truncated 44 chars> | ✅ |
| `start_ac_effect_sets_autocontrol_flags_from_dirty_values` | explicit-hot-start in Ask_StartAC uses dirty Manual-like flag values so StartAC must produce autocontrol ownership value...<truncated 33 chars> | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_outputs` — default-init dispatches into Manual and checks manual pump speed/flow come from the built-in switch and default manual flow rate.</summary>

| Field | Value |
|---|---|
| description | default-init dispatches into Manual and checks manual pump speed/flow come from the built-in switch and default manual flow rate. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 80.0, "builtin_switch_speed": 7.0, "default_manual_flow_rate": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 5.0, "pump_speed": 7.0, "sensor_buffer_bp": 80.0, "software_control": 0}` |

</details>

<details><summary>`initiate_and_change_setpoint_in_ask_startac` — default-init first reaches Manual, then caregiver initiates algorithmic control and changes the setpoint within Ask_StartAC.</summary>

| Field | Value |
|---|---|
| description | default-init first reaches Manual, then caregiver initiates algorithmic control and changes the setpoint within Ask_StartAC. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 88.0, "target_bp": 100.0, "target_bp_command": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_after_default_dispatch` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"sensor_buffer_bp": 88.0}` |
| 1 `initiate_enters_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAlgorithmicControl"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"sensor_buffer_bp": 88.0}` |
| 2 `setpoint_changed_stays_in_ask_and_updates_target` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointChanged"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"sensor_buffer_bp": 88.0, "target_bp": 120.0}` |

</details>

<details><summary>`start_ac_init_then_normal_control` — explicit-hot-start in Ask_StartAC checks StartAC enters AutocontrolInit, then automatic progression reaches normal autocontrol and computes/logs flow.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Ask_StartAC checks StartAC enters AutocontrolInit, then automatic progression reaches normal autocontrol and computes/logs flow. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"blood_pressure": 90.0, "pump_fault": 0, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `start_ac_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "sensor_buffer_bp": 90.0, "software_control": 1}` |
| 1 `automatic_step_to_autocontrol_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 30.0, "flow_rate": 30.0, "infusion_log_rate": 30.0, "pump_speed": 30.0, "sensor_buffer_bp": 90.0}` |

</details>

<details><summary>`autocontrol_no_fault_boundary_stays_normal` — explicit-hot-start in AutocontrolNormal with pump_fault at the no-fault boundary verifies no fault transition fires and flow remains controlled.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal with pump_fault at the no-fault boundary verifies no fault transition fires and flow remains controlled. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"blood_pressure": 110.0, "pump_fault": 0, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_fault_no_fire_and_lower_high_pressure_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 10.0, "flow_rate": 10.0, "infusion_log_rate": 10.0, "pump_speed": 10.0, "sensor_buffer_bp": 110.0}` |

</details>

<details><summary>`pump_fault_boundary_enters_fault_and_alarms` — explicit-hot-start in AutocontrolNormal with pump_fault present verifies transition to PumpFault activates alarm and releases software control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal with pump_fault present verifies transition to PumpFault activates alarm and releases software control. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 95.0, "pump_fault": 1, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_guard_fires_to_pump_fault` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "sensor_buffer_bp": 95.0, "software_control": 0}` |

</details>

<details><summary>`caregiver_removes_fault_returns_manual` — explicit-hot-start in PumpFault checks caregiver fault removal returns to Manual, clears the fault/alarm, and keeps software control released.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in PumpFault checks caregiver fault removal returns to Manual, clears the fault/alarm, and keeps software control released. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"alarm_signal": 1, "blood_pressure": 75.0, "builtin_switch_speed": 6.0, "default_manual_flow_rate": 4.0, "pump_fault": 1, "software_control": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `caregiver_removal_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.CaregiverRemovesFault"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 4.0, "pump_fault": 0, "pump_speed": 6.0, "sensor_buffer_bp": 75.0, "software_control": 0}` |

</details>

<details><summary>`terminate_autocontrol_returns_manual` — explicit-hot-start in AutocontrolNormal checks caregiver termination of algorithmic control returns to Manual and restores manual pump settings.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolNormal checks caregiver termination of algorithmic control returns to Manual and restores manual pump settings. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 82.0, "builtin_switch_speed": 5.0, "default_manual_flow_rate": 3.0, "pump_fault": 0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolNormal.TerminateAlgorithmicControl"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 3.0, "pump_speed": 5.0, "sensor_buffer_bp": 82.0, "software_control": 0}` |

</details>

<details><summary>`forced_back_manual_events_from_distinct_modes` — explicit-hot-start probes wildcard backManual recovery from several concrete leaves, each requiring Manual as the shared recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes wildcard backManual recovery from several concrete leaves, each requiring Manual as the shared recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 70.0, "builtin_switch_speed": 4.0, "default_manual_flow_rate": 2.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_back_manual_from_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 2.0, "pump_speed": 4.0, "sensor_buffer_bp": 70.0, "software_control": 0}` |
| 1 `return_to_ask_for_additional_forced_probe` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAlgorithmicControl"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"sensor_buffer_bp": 70.0}` |
| 2 `cb_back_manual_from_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 2.0, "pump_speed": 4.0, "sensor_buffer_bp": 70.0, "software_control": 0}` |

</details>

<details><summary>`forced_cp_back_manual_from_pump_fault` — explicit-hot-start in PumpFault checks CP_backManual also forces Manual as the shared recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in PumpFault checks CP_backManual also forces Manual as the shared recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 1, "blood_pressure": 65.0, "builtin_switch_speed": 9.0, "default_manual_flow_rate": 8.0, "pump_fault": 1, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_back_manual_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 8.0, "pump_speed": 9.0, "sensor_buffer_bp": 65.0, "software_control": 0}` |

</details>

<details><summary>`forced_cc_back_manual_from_autocontrol_init` — explicit-hot-start in AutocontrolInit checks CC_backManual overrides autocontrol initialization and forces Manual recovery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in AutocontrolInit checks CC_backManual overrides autocontrol initialization and forces Manual recovery. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 78.0, "builtin_switch_speed": 11.0, "default_manual_flow_rate": 6.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_back_manual_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 6.0, "pump_speed": 11.0, "sensor_buffer_bp": 78.0, "software_control": 0}` |

</details>

<details><summary>`setpoint_effect_used_by_autocontrol_flow` — explicit-hot-start in Ask_StartAC strengthens the SetpointChanged effect probe by requiring the changed target setpoint to drive the later autocontrol flow/log ...<truncated 12 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Ask_StartAC strengthens the SetpointChanged effect probe by requiring the changed target setpoint to drive the later autocontrol flow/log calculation. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"blood_pressure": 92.0, "pump_fault": 0, "target_bp": 100.0, "target_bp_command": 132.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `setpoint_effect_assigns_command_value` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.SetpointChanged"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"sensor_buffer_bp": 92.0, "target_bp": 132.0}` |
| 1 `start_after_changed_setpoint` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "sensor_buffer_bp": 92.0, "software_control": 1}` |
| 2 `normal_flow_uses_changed_target` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 40.0, "flow_rate": 40.0, "infusion_log_rate": 40.0, "pump_speed": 40.0, "sensor_buffer_bp": 92.0}` |

</details>

<details><summary>`fault_removal_effect_clears_fault_and_alarm_values` — explicit-hot-start in PumpFault isolates the CaregiverRemovesFault transition effect so missing or wrong constant assignments to pump_fault/alarm_signal are cau...<truncated 4 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in PumpFault isolates the CaregiverRemovesFault transition effect so missing or wrong constant assignments to pump_fault/alarm_signal are caught. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 0, "alarm_signal": 1, "blood_pressure": 68.0, "builtin_switch_speed": 13.0, "default_manual_flow_rate": 12.0, "pump_fault": 1, "software_control": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `caregiver_remove_fault_effect_values_are_zero` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.CaregiverRemovesFault"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 12.0, "pump_fault": 0, "pump_speed": 13.0, "sensor_buffer_bp": 68.0, "software_control": 0}` |

</details>

<details><summary>`start_ac_effect_sets_autocontrol_flags_from_dirty_values` — explicit-hot-start in Ask_StartAC uses dirty Manual-like flag values so StartAC must produce autocontrol ownership values before normal control proceeds.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start in Ask_StartAC uses dirty Manual-like flag values so StartAC must produce autocontrol ownership values before normal control proceeds. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 0, "alarm_signal": 1, "blood_pressure": 85.0, "pump_fault": 0, "software_control": 0, "target_bp": 125.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `start_ac_effect_and_entry_set_control_flags` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "sensor_buffer_bp": 85.0, "software_control": 1}` |
| 1 `normal_control_retains_autocontrol_flags_and_computes_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 1, "control_voltage": 40.0, "flow_rate": 40.0, "infusion_log_rate": 40.0, "pump_speed": 40.0, "sensor_buffer_bp": 85.0, "software_control": 1}` |

</details>


### 7. Repair / blocking feedback 明细

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4264, 'completion_chars': 18751, 'completion_tokens': 5806, 'elapsed_seconds': 107.3992232879973, 'estimated_completion_tokens': 4688, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11345, 'first_chunk_seconds': 30.585581863997504, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 12256}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2777, 'completion_chars': 11243, 'completion_tokens': 4332, 'elapsed_seconds': 79.70446880901, 'estimated_completion_tokens': 2811, 'estimated_prompt_tokens': 15612, 'estimated_total_tokens': 18423, 'first_chunk_seconds': 31.698067143006483, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 62446, 'prompt_tokens': 15182, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 19514}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2413, 'completion_chars': 9719, 'completion_tokens': 2772, 'elapsed_seconds': 53.86932339100167, 'estimated_completion_tokens': 2430, 'estimated_prompt_tokens': 18609, 'estimated_total_tokens': 21039, 'first_chunk_seconds': 11.638113139022607, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 74434, 'prompt_tokens': 18106, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20878}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3865, 'completion_chars': 15666, 'completion_tokens': 4384, 'elapsed_seconds': 82.14176354301162, 'estimated_completion_tokens': 3917, 'estimated_prompt_tokens': 19335, 'estimated_total_tokens': 23252, 'first_chunk_seconds': 14.96689268501359, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 77337, 'prompt_tokens': 18819, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23203}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1843, 'completion_chars': 8688, 'completion_tokens': 2880, 'elapsed_seconds': 53.949247070006095, 'estimated_completion_tokens': 2172, 'estimated_prompt_tokens': 20881, 'estimated_total_tokens': 23053, 'first_chunk_seconds': 21.561357510014204, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 83522, 'prompt_tokens': 20652, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23532}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success_but_weak_oracle_ineligible`。
- required stages executed：`16/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`3`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 主结果/蓝本边界：`main_result_eligible` 只表示该 run 非 provider-invalid 且 trace/schema/secret/final-verdict 口径可进入主结果候选；`path2_ref_model_blueprint_eligible=false` 时，模型仍可作为 FE/BVS 或 dispatch-classifier 压力测试证据，但不得称为 Path2 ref-model 主蓝本。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
