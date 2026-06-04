## path1 / cara-infusion-pump-formal-spec__01 / default 真实运行结果：Path1 CARA representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`not_converged`；record_status：`rejected`；result_status：`not_converged`。
- main_result_eligible：`false`。
- 一句话结论：`model_review_or_quality`；停止原因：SL-7 model review blocked candidate。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `cara-infusion-pump-formal-spec__01` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `55507fdfe159d41fb3a5e96faa8423b914900b57` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:ce499624790550d734a59fdd9b6b28f8194710e89c85f739538372d5d8133081` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-round24deepghsstream-1afcc21e` |
| final verdict/status | verdict=`not_converged`, record=`rejected`, result=`not_converged` |
| main_result_eligible | `false` |
| final.fcstm 来源 | `{"final_dsl_hash": "sha256:ecb9bdac24ae47785ee8d47eeb8a8609d691ab33bf9e24653c21a3c50ce71850", "last_rejected_candidate": {"candidate_dsl_hash": "sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04", "iteration": 0, "repair_history_index": 4, "rework_instructions": ["SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale."], "sl10_decision": "rework"}, "source_kind": "initial_or_unrepaired"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, exit_rejected_rework_budget_exhausted` |
| iteration exit_reason 序列 | `SL-7 model review blocked candidate` |
| token/cost/time | tokens=`{'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0, 'prompt_chars': 791966, 'completion_chars': 81641, 'n_calls': 13}`, elapsed=`539.059s` |
| run record | [`pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`flow_log.json`](./flow_log.json), [`fix_log.json`](./fix_log.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

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
def float blood_pressure = 0.0;
def float shared_bp_buffer = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float manual_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int log_count = 0;

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
                software_control = 0;
                alarm_active = 0;
                pump_fault = 0;
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
                control_voltage = 0.0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                shared_bp_buffer = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                shared_bp_buffer = blood_pressure;
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    control_voltage = flow_rate;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                software_control = 0;
                control_voltage = 0.0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault :: PumpFault;
        PumpFault -> Manual :: FaultRemoved;
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=0 | 生成初始 DSL 与 grounding seeds | initial len=2418 | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=21, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=0 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=0 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=0 | LLM per-request accept/reject + repair | candidate len=2447,2675,2695,2675,2675 | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=0 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=0 | LLM per-request accept/reject + repair | candidate len=2447,2675,2695,2675,2675 | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=5, tokens=0 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=0 | LLM per-request accept/reject + repair | candidate len=2447,2675,2695,2675,2675 | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=5, tokens=0 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=0 | LLM per-request accept/reject + repair | candidate len=2447,2675,2695,2675,2675 | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=5, tokens=0 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=0 | LLM per-request accept/reject + repair | candidate len=2447,2675,2695,2675,2675 | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=5, tokens=0 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SL-7 model review blocked candidate | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-round24deepghsstream-1afcc21e.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T02:44:10Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 2 | `2026-06-04T02:44:10Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 3 | `2026-06-04T02:46:02Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 4 | `2026-06-04T02:46:02Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 5 | `2026-06-04T02:46:02Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:ecb9bdac24ae47785ee8d47eeb8a8609d691ab33bf9e24653c21a3c50ce71850 |
| 6 | `2026-06-04T02:46:02Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2418,hash=sha256:ecb9bdac24ae, current_hash=sha256:ecb9bdac24ae47785ee8d47eeb8a8609d691ab33bf9e24653c21a3c50ce71850 |
| 7 | `2026-06-04T02:46:02Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 8 | `2026-06-04T02:46:02Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 9 | `2026-06-04T02:46:02Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 10 | `2026-06-04T02:46:03Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 11 | `2026-06-04T02:46:03Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 12 | `2026-06-04T02:46:03Z` | `SD-4` | `0` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 13 | `2026-06-04T02:46:03Z` | `SL-5` | `0` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 14 | `2026-06-04T02:47:10Z` | `SL-5` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 15 | `2026-06-04T02:47:10Z` | `SD-5A` | `0` | `stage_result` | {"jump": "SC-5F", "ok": true, "status": "StageStatus.OK"} | <none> |
| 16 | `2026-06-04T02:47:10Z` | `SC-5F` | `0` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 17 | `2026-06-04T02:47:10Z` | `SD-6` | `0` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 18 | `2026-06-04T02:47:10Z` | `SD-6` | `0` | `stage_result` | {"jump": "SL-7", "ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T02:47:10Z` | `SL-7` | `0` | `stage_enter` | {"reason": "SD-6 ok"} | <none> |
| 20 | `2026-06-04T02:48:01Z` | `SL-7` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-04T02:48:01Z` | `SL-7` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.OK"} | <none> |
| 22 | `2026-06-04T02:48:01Z` | `SL-7` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 23 | `2026-06-04T02:48:01Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["NL: \"If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault...\"", "DSL: `! * -> Manual :: CP_backManual;` and other forced `*_backManual` transitions target `Manual` from any state.", "DSL: `Manual.enter` sets `alarm_act...<truncated 1338 chars> | <none> |
| 24 | `2026-06-04T02:48:01Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_findings": [{"category": "unsafe_recovery", "evidence": ["NL: \"If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault...\"", "DSL: `! * -> Manual :: CP_backManual;` and other forced `*_backManual` transitions target `Manual` from any state.", "DSL: `Manual.enter` sets `alarm_active = 0...<truncated 1331 chars> | current_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 25 | `2026-06-04T02:48:01Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 26 | `2026-06-04T02:48:01Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 2} | <none> |
| 27 | `2026-06-04T02:48:01Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 28 | `2026-06-04T02:48:29Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 29 | `2026-06-04T02:48:29Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7", "fixreq-0-sl7-1-23c6ba7ffb"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2447,hash=sha256:0ff4eb8e59c1 |
| 30 | `2026-06-04T02:48:29Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 31 | `2026-06-04T02:48:29Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:0ff4eb8e59c1879f13730e20b7a84f2fb44173c11e58725f0a10aa7c984190b2 |
| 32 | `2026-06-04T02:49:13Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-04T02:49:13Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 34 | `2026-06-04T02:49:13Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 35 | `2026-06-04T02:49:13Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 36 | `2026-06-04T02:49:45Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 37 | `2026-06-04T02:49:45Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7", "fixreq-0-sl7-1-23c6ba7ffb"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2675,hash=sha256:0cb3a6242da5 |
| 38 | `2026-06-04T02:49:45Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 39 | `2026-06-04T02:49:45Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04 |
| 40 | `2026-06-04T02:50:09Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 41 | `2026-06-04T02:50:09Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 42 | `2026-06-04T02:50:09Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 43 | `2026-06-04T02:50:09Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 44 | `2026-06-04T02:50:43Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 45 | `2026-06-04T02:50:43Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7", "fixreq-0-sl7-1-23c6ba7ffb"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2695,hash=sha256:99b0a326ebee |
| 46 | `2026-06-04T02:50:43Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 47 | `2026-06-04T02:50:43Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:99b0a326ebeea9465293f0e2db1a3b73061d351cb6e6d73b9fddc25f2ec1a5c7 |
| 48 | `2026-06-04T02:51:10Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 49 | `2026-06-04T02:51:10Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 50 | `2026-06-04T02:51:10Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 51 | `2026-06-04T02:51:43Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 52 | `2026-06-04T02:51:43Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7", "fixreq-0-sl7-1-23c6ba7ffb"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2675,hash=sha256:0cb3a6242da5 |
| 53 | `2026-06-04T02:51:43Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 54 | `2026-06-04T02:51:43Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04 |
| 55 | `2026-06-04T02:52:07Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 56 | `2026-06-04T02:52:07Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SL-9 rework", "ok": false} | <none> |
| 57 | `2026-06-04T02:52:07Z` | `SL-9` | `0` | `stage_enter` | {"reason": "sl10_rework_locked"} | old_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 58 | `2026-06-04T02:52:39Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 59 | `2026-06-04T02:52:39Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sl7-0-be1e03bda7", "fixreq-0-sl7-1-23c6ba7ffb"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2675,hash=sha256:0cb3a6242da5 |
| 60 | `2026-06-04T02:52:39Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 61 | `2026-06-04T02:52:39Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04 |
| 62 | `2026-06-04T02:53:09Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 63 | `2026-06-04T02:53:09Z` | `SL-10` | `0` | `stage_result` | {"decision": "rework", "jump": "SC-12 rejected", "ok": false} | <none> |
| 64 | `2026-06-04T02:53:09Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": false, "jump": "SC-12 or retry"} | current_hash=sha256:ecb9bdac24ae47785ee8d47eeb8a8609d691ab33bf9e24653c21a3c50ce71850 |
| 65 | `2026-06-04T02:53:09Z` | `SC-12` | `-` | `sc12_verdict` | {"reason": "SL-7 model review blocked candidate", "verdict": "not_converged"} | final_dsl:len=2418,hash=sha256:ecb9bdac24ae |
| 66 | `2026-06-04T02:53:09Z` | `SC-13` | `-` | `run_end` | {"verdict": "not_converged"} | final_dsl:len=2418,hash=sha256:ecb9bdac24ae |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SL-7` | yes | fixbatch-0-sha256-7607c16ecc0 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local re...<truncated 63 chars> | no | SL-7 model review blocked candidate |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_initial_manual_outputs` | default-init dispatches into Manual and applies manual operation outputs from the caregiver-set default flow and built-i...<truncated 15 chars> | ✅ |
| `initiate_change_start_to_normal_autocontrol` | explicit-hot-start from Manual probes InitiateAC, Ask_StartAC setpoint change, StartAC into AutocontrolInit, and automat...<truncated 37 chars> | ✅ |
| `pump_fault_alarm_release_then_fault_removed_manual` | explicit-hot-start from AutocontrolNormal probes pump fault handling, alarm activation, software-control release, and ca...<truncated 41 chars> | ✅ |
| `forced_ca_backmanual_from_ask_startac` | explicit-hot-start from Ask_StartAC probes CA_backManual as a cross-component fallback to Manual recovery. | ✅ |
| `forced_cb_backmanual_from_autocontrol_normal` | explicit-hot-start from AutocontrolNormal probes CB_backManual as a cross-component fallback to Manual recovery. | ✅ |
| `forced_cp_backmanual_from_pump_fault` | explicit-hot-start from PumpFault probes CP_backManual as a cross-component fallback that clears alarm/fault indicators ...<truncated 19 chars> | ✅ |
| `forced_cc_backmanual_from_autocontrol_init` | explicit-hot-start from AutocontrolInit probes CC_backManual as a cross-component fallback to Manual recovery before nor...<truncated 23 chars> | ✅ |
| `terminate_ac_from_autocontrol_normal` | explicit-hot-start from AutocontrolNormal probes caregiver termination of algorithmic pump control back to Manual. | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_initial_manual_outputs` — default-init dispatches into Manual and applies manual operation outputs from the caregiver-set default flow and built-in switch speed.</summary>

| Field | Value |
|---|---|
| description | default-init dispatches into Manual and applies manual operation outputs from the caregiver-set default flow and built-in switch speed. |
| initial_state | `<default-init>` |
| initial_vars | `{"alarm_active": 1, "control_voltage": 9.0, "default_flow_rate": 4.2, "manual_switch_speed": 3.3, "pump_fault": 1, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_voltage": 0.0, "flow_rate": 4.2, "pump_fault": 0, "pump_speed": 3.3, "software_control": 0}` |

</details>

<details><summary>`initiate_change_start_to_normal_autocontrol` — explicit-hot-start from Manual probes InitiateAC, Ask_StartAC setpoint change, StartAC into AutocontrolInit, and automatic progression to normal autocontrol.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from Manual probes InitiateAC, Ask_StartAC setpoint change, StartAC into AutocontrolInit, and automatic progression to normal autocontrol. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"CA_mode": 0, "blood_pressure": 60.0, "control_voltage": 0.0, "flow_rate": 0.0, "log_count": 0, "requested_target_bp": 100.0, "shared_bp_buffer": 0.0, "software_control": 0, "target_bp": 80.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiate_enters_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 1 `change_setpoint_stays_in_ask` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 100.0}` |
| 2 `startac_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "shared_bp_buffer": 60.0, "software_control": 1}` |
| 3 `init_completes_to_normal_and_computes_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"CA_mode": 1, "control_voltage": 40.0, "flow_rate": 40.0, "log_count": 1, "shared_bp_buffer": 60.0, "software_control": 1}` |
| 4 `no_fault_stays_normal_and_logs_again` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 40.0, "flow_rate": 40.0, "log_count": 2}` |

</details>

<details><summary>`pump_fault_alarm_release_then_fault_removed_manual` — explicit-hot-start from AutocontrolNormal probes pump fault handling, alarm activation, software-control release, and caregiver fault-removal recovery to Manual...<truncated 1 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from AutocontrolNormal probes pump fault handling, alarm activation, software-control release, and caregiver fault-removal recovery to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 0, "control_voltage": 25.0, "default_flow_rate": 5.0, "flow_rate": 25.0, "manual_switch_speed": 2.0, "pump_fault": 0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `pump_fault_enters_fault_state` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolNormal.PumpFault"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"alarm_active": 1, "control_voltage": 0.0, "pump_fault": 1, "software_control": 0}` |
| 1 `fault_removed_recovers_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_voltage": 0.0, "flow_rate": 5.0, "pump_fault": 0, "pump_speed": 2.0, "software_control": 0}` |

</details>

<details><summary>`forced_ca_backmanual_from_ask_startac` — explicit-hot-start from Ask_StartAC probes CA_backManual as a cross-component fallback to Manual recovery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from Ask_StartAC probes CA_backManual as a cross-component fallback to Manual recovery. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 1, "control_voltage": 10.0, "default_flow_rate": 6.0, "flow_rate": 20.0, "manual_switch_speed": 1.5, "pump_fault": 0, "pump_speed": 0.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_voltage": 0.0, "flow_rate": 6.0, "pump_fault": 0, "pump_speed": 1.5, "software_control": 0}` |

</details>

<details><summary>`forced_cb_backmanual_from_autocontrol_normal` — explicit-hot-start from AutocontrolNormal probes CB_backManual as a cross-component fallback to Manual recovery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from AutocontrolNormal probes CB_backManual as a cross-component fallback to Manual recovery. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 0, "control_voltage": 30.0, "default_flow_rate": 7.0, "flow_rate": 30.0, "manual_switch_speed": 2.5, "pump_fault": 0, "pump_speed": 0.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_voltage": 0.0, "flow_rate": 7.0, "pump_fault": 0, "pump_speed": 2.5, "software_control": 0}` |

</details>

<details><summary>`forced_cp_backmanual_from_pump_fault` — explicit-hot-start from PumpFault probes CP_backManual as a cross-component fallback that clears alarm/fault indicators by entering Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from PumpFault probes CP_backManual as a cross-component fallback that clears alarm/fault indicators by entering Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 1, "control_voltage": 0.0, "default_flow_rate": 3.0, "flow_rate": 0.0, "manual_switch_speed": 4.0, "pump_fault": 1, "pump_speed": 0.0, "software_control": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_voltage": 0.0, "flow_rate": 3.0, "pump_fault": 0, "pump_speed": 4.0, "software_control": 0}` |

</details>

<details><summary>`forced_cc_backmanual_from_autocontrol_init` — explicit-hot-start from AutocontrolInit probes CC_backManual as a cross-component fallback to Manual recovery before normal autocontrol begins.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from AutocontrolInit probes CC_backManual as a cross-component fallback to Manual recovery before normal autocontrol begins. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 0, "control_voltage": 12.0, "default_flow_rate": 8.0, "flow_rate": 12.0, "manual_switch_speed": 1.0, "pump_fault": 0, "pump_speed": 0.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_backmanual_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_voltage": 0.0, "flow_rate": 8.0, "pump_fault": 0, "pump_speed": 1.0, "software_control": 0}` |

</details>

<details><summary>`terminate_ac_from_autocontrol_normal` — explicit-hot-start from AutocontrolNormal probes caregiver termination of algorithmic pump control back to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from AutocontrolNormal probes caregiver termination of algorithmic pump control back to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 0, "control_voltage": 35.0, "default_flow_rate": 9.0, "flow_rate": 35.0, "manual_switch_speed": 2.2, "pump_fault": 0, "pump_speed": 0.0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_ac_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_voltage": 0.0, "flow_rate": 9.0, "pump_fault": 0, "pump_speed": 2.2, "software_control": 0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Keep the accepted autocontrol repair: retain `pump_speed = control_voltage` in `AutocontrolNormal.during` after `control_voltage = flow_rate`., Do not restore unconditional `pu...<truncated 265 chars> | `sha256:0ff4eb8e59c1879f13730e20b7a84f2fb44173c11e58725f0a10aa7c984190b2` |
| 2 | `0` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 164 chars> | `sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04` |
| 3 | `0` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 164 chars> | `sha256:99b0a326ebeea9465293f0e2db1a3b73061d351cb6e6d73b9fddc25f2ec1a5c7` |
| 4 | `0` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 164 chars> | `sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04` |
| 5 | `0` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 164 chars> | `sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04` |

<details><summary>Repair 1 / iteration `0` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:ecb9bdac24ae47785ee8d47eeb8a8609d691ab33bf9e24653c21a3c50ce71850`；candidate_dsl_hash：`sha256:0ff4eb8e59c1879f13730e20b7a84f2fb44173c11e58725f0a10aa7c984190b2`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Forced back-to-Manual recovery can clear pump fault and alarm state without the caregiver fault-removal event, losing the NL-required distinction between a fault occurring, alarm activation, caregiver removal, and software release/control fallback.
- 2. `<unknown>` `` policy=``：Autocontrol pump-speed semantics are not faithfully represented: the NL says pump speed is set by a control voltage in autocontrol mode, but the DSL only writes `control_voltage` and does not update `pump_speed` during autocontrol.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-7607c16ecc0`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault..."', 'DSL: `! * -> Manual :: CP_backManual;` and other forced `*_backManual` transitions target `Manual` from any state.', 'DSL: `Manual.enter` sets `alarm_active = 0; pump_fault = 0; software_control = 0;`.', 'Simulation scenario `forced_cp_backmanual_from_pump_fault` expects CP_backManual from PumpFault to enter Manual with `pump_fault: 0` and `alarm_active: 0`, without `FaultRemoved`.'], 'severity': 'major', 'summary': 'Forced back-to-Manual recovery can clear pump fault and alarm state without the caregiver fault-removal event, losing the NL-required distinction between a fault occurring, alarm activation, caregiver removal, and software release/control fallback.'}` |
| `fixreq-0-sl7-1-23c6ba7ffb` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: "in autocontrol mode pump speed is set by a control voltage from an external source."', 'DSL `AutocontrolNormal.during`: `control_voltage = flow_rate;` but no `pump_speed = ...` assignment.', 'Manual mode explicitly updates `pump_speed = manual_switch_speed`, showing pump speed is modeled but not connected to control voltage in autocontrol.'], 'severity': 'major', 'summary': 'Autocontrol pump-speed semantics are not faithfully represented: the NL says pump speed is set by a control voltage in autocontrol mode, but the DSL only writes `control_voltage` and does not update `pump_speed` during autocontrol.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:blood_pressure, variable:shared_bp_buffer, variable:target_bp, variable:requested_target_bp, variable:flow_rate, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2447`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ❌ | The evidence is valid: forced back-to-Manual events should make CA_mode Manual and release software control, but should not erase the pump-fault/alarm condition before the caregiver FaultRemoved event. Preserve Manual as the recovery target while moving fault/alarm clearing to the FaultRemoved transition.；intent=Remove pump_fault and alarm_active clearing fr...<truncated 94 chars> |
| `fixreq-0-sl7-1-23c6ba7ffb` | `accept` | ❌ | ❌ | The evidence is valid: autocontrol updates control_voltage but does not connect it to pump_speed. Add a direct autocontrol assignment so pump speed is set from control voltage during normal complication-free autocontrol.；intent=Assign pump_speed = control_voltage in AutocontrolNormal.during after computing control_voltage |
- repair_rationale：Manual remains the shared recovery target for CA_backManual, CB_backManual, CP_backManual, and CC_backManual, preserving the cross-component fallback requirement.；Forced back-to-Manual now releases software control through Manual.enter but preserves pump_fault and alarm_active until the explicit caregiver FaultRemoved event.；Normal autocontrol now explicitly connects control_voltage to pump_speed, matching the NL statement that pump speed is set by control voltage in autocontrol mode.；All required states, variables, and events are preserved.
- diff_summary：`{"summary": "Removed pump_fault/alarm_active resets from Manual.enter; added pump_fault/alarm_active clearing effect to FaultRemoved; added pump_speed = control_voltage during normal autocontrol."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float blood_pressure = 0.0;
def float shared_bp_buffer = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float manual_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int log_count = 0;

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
                software_control = 0;
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
                control_voltage = 0.0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                shared_bp_buffer = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                shared_bp_buffer = blood_pressure;
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                software_control = 0;
                control_voltage = 0.0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault :: PumpFault;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_active = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -29,8 +29,6 @@
             enter {
                 CA_mode = 0;
                 software_control = 0;
-                alarm_active = 0;
-                pump_fault = 0;
                 flow_rate = default_flow_rate;
                 pump_speed = manual_switch_speed;
                 control_voltage = 0.0;
@@ -61,6 +59,7 @@
                 if [pump_fault == 0] {
                     flow_rate = target_bp - blood_pressure;
                     control_voltage = flow_rate;
+                    pump_speed = control_voltage;
                     log_count = log_count + 1;
                 }
             }
@@ -80,6 +79,6 @@
         Ask_StartAC -> AutocontrolInit :: StartAC;
         AutocontrolInit -> AutocontrolNormal;
         AutocontrolNormal -> PumpFault :: PumpFault;
-        PumpFault -> Manual :: FaultRemoved;
+        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_active = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:159089b8e8da915800c8936271b07836772eb2a32e91e69e744f4f3047eda006`。
  - SL-10 evidence 1: `{"summary": "The candidate correctly implements the accepted SL-9 intent for fixreq-0-sl7-1-23c6ba7ffb by adding `pump_speed = control_voltage` in `AutocontrolNormal.during`, satisfying the NL requirement that autocontrol pump speed is set by control voltage."}`
  - SL-10 evidence 2: `{"summary": "The candidate partially implements fixreq-0-sl7-0-be1e03bda7 by removing `pump_fault` and `alarm_active` clearing from `Manual.enter` and moving clearing onto `PumpFault -> Manual :: FaultRemoved`, preserving the NL-required distinction between fault/alarm occurrence and caregiver fault removal."}`
  - SL-10 evidence 3: `{"summary": "However, the repair leaves a semantic gap after forced back-to-Manual recovery from `PumpFault`: `CA_backManual`, `CB_backManual`, `CP_backManual`, or `CC_backManual` can move the machine to `Manual` while preserving `pump_fault = 1` and `alarm_active = 1`, but once in `Manual` there is no `FaultRemoved` transition/effect to clear the fault/alarm after caregiver removal. This does not fully satisfy the NL sequence requiring caregiver removal of the fault after a pump fault and weakens the SL-9 rationale that fault/alarm remain until the explicit `FaultRemoved` event."}`
  - SL-10 evidence 4: `{"summary": "Local deterministic evidence also reports major rejection with scenario regression and missing-required-grounding. The missing-grounding report appears conservative because the candidate still contains the named required transitions, but the scenario regression is directionally consistent with the unresolved fault/alarm lifecycle: removing clearing from `Manual.enter` requires an explicit alternative path for clearing after manual fallback, which is currently absent."}`
  - SL-10 evidence 5: `{"summary": "All required states, variables, and events appear preserved in the candidate DSL, so this should be reworked rather than failed; the accepted SL-9 requests remain valid and locked."}`
- SL-10 rework_instructions：Keep the accepted autocontrol repair: retain `pump_speed = control_voltage` in `AutocontrolNormal.during` after `control_voltage = flow_rate`.；Do not restore unconditional `pump_fault = 0` or `alarm_active = 0` clearing in `Manual.enter`, because that would reintroduce the unsafe recovery defect.；Add explicit caregiver fault-removal handling that remains reachable after forced fallback to Manual, for example add `Manual -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_active = 0; };` or an equivalent transition/state structure that clears fault/alarm only on the `FaultRemoved` event.；Preserve `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_active = 0; };` so direct caregiver removal from `PumpFault` remains represented.；If needed to satisfy initial startup scenarios without weakening fault recovery, clear `pump_fault` and `alarm_active` only on the initial transition into Manual, not in `Manual.enter` and not on forced back-to-Manual transitions.；Ensure the required grounded transitions remain concrete and parseable: `Manual -> Ask_StartAC :: InitiateAC`, `Ask_StartAC -> Ask_StartAC :: ChangeSetpoint`, `Ask_StartAC -> AutocontrolInit :: StartAC`, `AutocontrolNormal -> PumpFault :: PumpFault`, `PumpFault -> Manual :: FaultRemoved`, and all four forced `*_backManual` transitions.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 8, "n_scenarios_passed": 5, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init dispatches into Manual and applies manual operation outputs from the caregiver-set default flow and built-in switch speed.", "name": "default_initial_manual_outputs", "setup_error": null, "status": "fail", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_active"...<truncated 9301 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:Manual_to_Ask_StartAC_on_InitiateAC", "transition:Ask_StartAC_self_on_ChangeSetpoint", "transition:Ask_StartAC_to_AutocontrolInit_on_StartAC", "transition:AutocontrolNormal_to_PumpFault_on_PumpFault", "transition:PumpFault_to_Manual_on_FaultRemoved", "transition:forced_CA_backManual_to_Manual", "transition:forced_CB_backManual_to_Manual", "transition:forced_CP_backManual_to_Manual", "transition:forced_CC_backManual_to_Manual"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 2 / iteration `0` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:ecb9bdac24ae47785ee8d47eeb8a8609d691ab33bf9e24653c21a3c50ce71850`；candidate_dsl_hash：`sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Forced back-to-Manual recovery can clear pump fault and alarm state without the caregiver fault-removal event, losing the NL-required distinction between a fault occurring, alarm activation, caregiver removal, and software release/control fallback.
- 2. `<unknown>` `` policy=``：Autocontrol pump-speed semantics are not faithfully represented: the NL says pump speed is set by a control voltage in autocontrol mode, but the DSL only writes `control_voltage` and does not update `pump_speed` during autocontrol.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-7607c16ecc0`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault..."', 'DSL: `! * -> Manual :: CP_backManual;` and other forced `*_backManual` transitions target `Manual` from any state.', 'DSL: `Manual.enter` sets `alarm_active = 0; pump_fault = 0; software_control = 0;`.', 'Simulation scenario `forced_cp_backmanual_from_pump_fault` expects CP_backManual from PumpFault to enter Manual with `pump_fault: 0` and `alarm_active: 0`, without `FaultRemoved`.'], 'severity': 'major', 'summary': 'Forced back-to-Manual recovery can clear pump fault and alarm state without the caregiver fault-removal event, losing the NL-required distinction between a fault occurring, alarm activation, caregiver removal, and software release/control fallback.'}` |
| `fixreq-0-sl7-1-23c6ba7ffb` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: "in autocontrol mode pump speed is set by a control voltage from an external source."', 'DSL `AutocontrolNormal.during`: `control_voltage = flow_rate;` but no `pump_speed = ...` assignment.', 'Manual mode explicitly updates `pump_speed = manual_switch_speed`, showing pump speed is modeled but not connected to control voltage in autocontrol.'], 'severity': 'major', 'summary': 'Autocontrol pump-speed semantics are not faithfully represented: the NL says pump speed is set by a control voltage in autocontrol mode, but the DSL only writes `control_voltage` and does not update `pump_speed` during autocontrol.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:blood_pressure, variable:shared_bp_buffer, variable:target_bp, variable:requested_target_bp, variable:flow_rate, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2675`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ✅ | The unsafe recovery evidence is valid and SL-10 rework evidence showed the first repair needed an explicit FaultRemoved path after forced fallback. The repair keeps Manual as the shared recovery target and releases software control there, but no longer clears pump_fault or alarm_active on every Manual entry. Fault/alarm clearing is now tied to the caregiver ...<truncated 361 chars> |
| `fixreq-0-sl7-1-23c6ba7ffb` | `accept` | ❌ | ✅ | The autocontrol pump-speed fidelity evidence is valid. Normal autocontrol now explicitly maps the computed control voltage to pump_speed, preserving the NL distinction that manual mode uses the built-in switch while autocontrol uses control voltage.；intent=Assign pump_speed = control_voltage in AutocontrolNormal.during after control_voltage = flow_rate |
- repair_rationale：Manual remains the shared recovery target for CA_backManual, CB_backManual, CP_backManual, and CC_backManual.；Forced back-to-Manual releases software control by entering Manual but preserves pump_fault and alarm_active until an explicit FaultRemoved event.；Initial startup into Manual still initializes pump_fault and alarm_active to clear values without weakening forced recovery from PumpFault.；A Manual self-transition on FaultRemoved handles caregiver fault removal after a forced fallback has already returned the system to Manual.；Normal autocontrol now sets pump_speed from control_voltage after computing the control voltage.
- diff_summary：`{"summary": "Removed unconditional pump_fault/alarm_active clearing from Manual.enter; added initial-transition clearing for startup; added Manual self FaultRemoved clearing and PumpFault FaultRemoved clearing effects; retained all grounded states/events/transitions; added pump_speed = control_voltage in AutocontrolNormal.during."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float blood_pressure = 0.0;
def float shared_bp_buffer = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float manual_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! * -> Manual :: TerminateAC;

        [*] -> Manual effect {
            pump_fault = 0;
            alarm_active = 0;
        };

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
                control_voltage = 0.0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                shared_bp_buffer = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                shared_bp_buffer = blood_pressure;
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                software_control = 0;
                control_voltage = 0.0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Manual -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            alarm_active = 0;
        };
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault :: PumpFault;
        PumpFault -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            alarm_active = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -23,14 +23,15 @@
         ! * -> Manual :: CC_backManual;
         ! * -> Manual :: TerminateAC;
 
-        [*] -> Manual;
+        [*] -> Manual effect {
+            pump_fault = 0;
+            alarm_active = 0;
+        };
 
         state Manual {
             enter {
                 CA_mode = 0;
                 software_control = 0;
-                alarm_active = 0;
-                pump_fault = 0;
                 flow_rate = default_flow_rate;
                 pump_speed = manual_switch_speed;
                 control_voltage = 0.0;
@@ -61,6 +62,7 @@
                 if [pump_fault == 0] {
                     flow_rate = target_bp - blood_pressure;
                     control_voltage = flow_rate;
+                    pump_speed = control_voltage;
                     log_count = log_count + 1;
                 }
             }
@@ -76,10 +78,17 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
+        Manual -> Manual :: FaultRemoved effect {
+            pump_fault = 0;
+            alarm_active = 0;
+        };
         Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
         Ask_StartAC -> AutocontrolInit :: StartAC;
         AutocontrolInit -> AutocontrolNormal;
         AutocontrolNormal -> PumpFault :: PumpFault;
-        PumpFault -> Manual :: FaultRemoved;
+        PumpFault -> Manual :: FaultRemoved effect {
+            pump_fault = 0;
+            alarm_active = 0;
+        };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:00bd88b6baa707f4f4b6135b66c15d3d1cf1a54c952b85de6b2276110ffc1e37`。
  - SL-10 evidence 1: `{"summary": "The unsafe-recovery request is resolved against the NL and FixLog. The candidate removes unconditional `pump_fault = 0` and `alarm_active = 0` from `Manual.enter`, so forced CA/CB/CP/CC back-to-Manual recovery still makes `CA_mode` Manual and releases software control, but no longer erases the fault/alarm condition before the caregiver `FaultRemoved` event. Fault/alarm clearing is now tied to `PumpFault -> Manual :: FaultRemoved` and to `Manual -> Manual :: FaultRemoved`, preserving caregiver fault-removal semantics even after forced fallback."}`
  - SL-10 evidence 2: `{"summary": "The autocontrol pump-speed request is resolved. In `AutocontrolNormal.during`, the candidate computes `flow_rate = target_bp - blood_pressure`, assigns `control_voltage = flow_rate`, and then assigns `pump_speed = control_voltage`, matching the NL distinction that manual mode uses the built-in switch while autocontrol sets pump speed by control voltage."}`
  - SL-10 evidence 3: `{"summary": "Required NL-grounded states, variables, events, and transitions are preserved in the candidate: `Manual`, `Ask_StartAC`, `AutocontrolInit`, `AutocontrolNormal`, `PumpFault`; the blood-pressure, buffer, setpoint, flow-rate, pump-speed, fault/alarm, software-control, and logging variables; and the required events `InitiateAC`, `ChangeSetpoint`, `StartAC`, `PumpFault`, `FaultRemoved`, `CA_backManual`, `CB_backManual`, `CP_backManual`, and `CC_backManual`."}`
  - SL-10 evidence 4: `{"summary": "The previous SL-10 rework instructions are satisfied: startup clearing is moved to the initial transition into `Manual`; `Manual.enter` no longer clears fault/alarm; `Manual -> Manual :: FaultRemoved` was added; `PumpFault -> Manual :: FaultRemoved` has explicit clearing effects; and the autocontrol `pump_speed = control_voltage` assignment is retained."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 8, "n_scenarios_passed": 6, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init dispatches into Manual and applies manual operation outputs from the caregiver-set default flow and built-in switch speed.", "name": "default_initial_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_active"...<truncated 9212 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:Manual_to_Ask_StartAC_on_InitiateAC", "transition:Ask_StartAC_self_on_ChangeSetpoint", "transition:Ask_StartAC_to_AutocontrolInit_on_StartAC", "transition:AutocontrolNormal_to_PumpFault_on_PumpFault", "transition:PumpFault_to_Manual_on_FaultRemoved", "transition:forced_CA_backManual_to_Manual", "transition:forced_CB_backManual_to_Manual", "transition:forced_CP_backManual_to_Manual", "transition:forced_CC_backManual_to_Manual"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 3 / iteration `0` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:ecb9bdac24ae47785ee8d47eeb8a8609d691ab33bf9e24653c21a3c50ce71850`；candidate_dsl_hash：`sha256:99b0a326ebeea9465293f0e2db1a3b73061d351cb6e6d73b9fddc25f2ec1a5c7`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Forced back-to-Manual recovery can clear pump fault and alarm state without the caregiver fault-removal event, losing the NL-required distinction between a fault occurring, alarm activation, caregiver removal, and software release/control fallback.
- 2. `<unknown>` `` policy=``：Autocontrol pump-speed semantics are not faithfully represented: the NL says pump speed is set by a control voltage in autocontrol mode, but the DSL only writes `control_voltage` and does not update `pump_speed` during autocontrol.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-7607c16ecc0`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault..."', 'DSL: `! * -> Manual :: CP_backManual;` and other forced `*_backManual` transitions target `Manual` from any state.', 'DSL: `Manual.enter` sets `alarm_active = 0; pump_fault = 0; software_control = 0;`.', 'Simulation scenario `forced_cp_backmanual_from_pump_fault` expects CP_backManual from PumpFault to enter Manual with `pump_fault: 0` and `alarm_active: 0`, without `FaultRemoved`.'], 'severity': 'major', 'summary': 'Forced back-to-Manual recovery can clear pump fault and alarm state without the caregiver fault-removal event, losing the NL-required distinction between a fault occurring, alarm activation, caregiver removal, and software release/control fallback.'}` |
| `fixreq-0-sl7-1-23c6ba7ffb` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: "in autocontrol mode pump speed is set by a control voltage from an external source."', 'DSL `AutocontrolNormal.during`: `control_voltage = flow_rate;` but no `pump_speed = ...` assignment.', 'Manual mode explicitly updates `pump_speed = manual_switch_speed`, showing pump speed is modeled but not connected to control voltage in autocontrol.'], 'severity': 'major', 'summary': 'Autocontrol pump-speed semantics are not faithfully represented: the NL says pump speed is set by a control voltage in autocontrol mode, but the DSL only writes `control_voltage` and does not update `pump_speed` during autocontrol.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:blood_pressure, variable:shared_bp_buffer, variable:target_bp, variable:requested_target_bp, variable:flow_rate, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2695`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ✅ | The request remains accepted and is rework-locked. Forced back-to-Manual recovery must release software control and set CA_mode to Manual without erasing the pump fault/alarm before the caregiver FaultRemoved event. The repair keeps Manual as the shared recovery target, removes unconditional fault/alarm clearing from Manual.enter, initializes clear fault/ala...<truncated 360 chars> |
| `fixreq-0-sl7-1-23c6ba7ffb` | `accept` | ❌ | ✅ | The request remains accepted and is rework-locked. Autocontrol must explicitly set pump_speed from the control voltage, preserving the NL distinction that manual mode uses the built-in switch while autocontrol uses control voltage.；intent=Assign pump_speed = control_voltage in AutocontrolNormal.during after control_voltage = flow_rate |
- repair_rationale：Manual remains the shared recovery target for CA_backManual, CB_backManual, CP_backManual, and CC_backManual.；Forced back-to-Manual recovery now releases software control through Manual.enter but preserves pump_fault and alarm_active until the explicit caregiver FaultRemoved event.；Initial default startup still initializes pump_fault and alarm_active to clear values without weakening fault recovery semantics.；FaultRemoved remains represented from PumpFault and is also reachable as a Manual self-transition after forced fallback has already moved the machine to Manual.；AutocontrolNormal now explicitly maps computed control_voltage to pump_speed during complication-free autocontrol.
- diff_summary：`{"summary": "Removed unconditional pump_fault/alarm_active resets from Manual.enter; added startup-only clearing on the initial transition to Manual; added Manual self FaultRemoved clearing; added FaultRemoved clearing effect on PumpFault -> Manual; retained all grounded states/events/transitions; added pump_speed = control_voltage in AutocontrolNormal.during."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float blood_pressure = 0.0;
def float shared_bp_buffer = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float manual_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! * -> Manual :: TerminateAC;

        [*] -> Manual effect {
            pump_fault = 0;
            alarm_active = 0;
        };

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
                control_voltage = 0.0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                shared_bp_buffer = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                shared_bp_buffer = blood_pressure;
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                software_control = 0;
                control_voltage = 0.0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Manual -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            alarm_active = 0;
        };
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
            target_bp = requested_target_bp;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault :: PumpFault;
        PumpFault -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            alarm_active = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -23,14 +23,15 @@
         ! * -> Manual :: CC_backManual;
         ! * -> Manual :: TerminateAC;
 
-        [*] -> Manual;
+        [*] -> Manual effect {
+            pump_fault = 0;
+            alarm_active = 0;
+        };
 
         state Manual {
             enter {
                 CA_mode = 0;
                 software_control = 0;
-                alarm_active = 0;
-                pump_fault = 0;
                 flow_rate = default_flow_rate;
                 pump_speed = manual_switch_speed;
                 control_voltage = 0.0;
@@ -61,6 +62,7 @@
                 if [pump_fault == 0] {
                     flow_rate = target_bp - blood_pressure;
                     control_voltage = flow_rate;
+                    pump_speed = control_voltage;
                     log_count = log_count + 1;
                 }
             }
@@ -76,10 +78,19 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
-        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
+        Manual -> Manual :: FaultRemoved effect {
+            pump_fault = 0;
+            alarm_active = 0;
+        };
+        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
+            target_bp = requested_target_bp;
+        };
         Ask_StartAC -> AutocontrolInit :: StartAC;
         AutocontrolInit -> AutocontrolNormal;
         AutocontrolNormal -> PumpFault :: PumpFault;
-        PumpFault -> Manual :: FaultRemoved;
+        PumpFault -> Manual :: FaultRemoved effect {
+            pump_fault = 0;
+            alarm_active = 0;
+        };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:c129f2db7d18c2b876bfba7d059c21e19c992171d04523e5d96b616867d275a4`。
  - SL-10 evidence 1: `{"summary": "Both hard SL-7 requests were accepted by SL-9 and remain rework-locked in the FixLog. The candidate implements the unsafe-recovery repair by removing unconditional `pump_fault = 0` and `alarm_active = 0` from `Manual.enter`, adding startup-only clearing on the initial transition to Manual, preserving `PumpFault -> Manual :: FaultRemoved` with fault/alarm clearing, and adding `Manual -> Manual :: FaultRemoved` so caregiver removal remains reachable after forced fallback. This matches the NL sequence: pump fault activates alarm, caregiver removes the fault, and when CARA was controlling the pump the software releases control."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves the NL-required shared recovery target: `CA_backManual`, `CB_backManual`, `CP_backManual`, and `CC_backManual` all still force transition to `Manual`; `Manual.enter` still sets `CA_mode = 0` and `software_control = 0`, so fallback releases software control and makes manual operation the recovery target without prematurely erasing fault/alarm state."}`
  - SL-10 evidence 3: `{"summary": "The autocontrol pump-speed fidelity request is resolved: `AutocontrolNormal.during` computes `control_voltage = flow_rate` and then assigns `pump_speed = control_voltage`, while `Manual` continues to set `pump_speed = manual_switch_speed`. This preserves the NL distinction between manual built-in switch speed control and autocontrol speed set by control voltage."}`
  - SL-10 evidence 4: `{"summary": "The candidate does not drop required grounded elements. The required states `Manual`, `Ask_StartAC`, `AutocontrolInit`, `AutocontrolNormal`, and `PumpFault` remain present; required variables including blood-pressure, flow-rate, pump-speed, control-voltage, fault/alarm, and software-control variables remain present; required events and transitions for InitiateAC, ChangeSetpoint, StartAC, PumpFault, FaultRemoved, and the four backManual events remain concrete in the DSL."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 8, "n_scenarios_passed": 6, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init dispatches into Manual and applies manual operation outputs from the caregiver-set default flow and built-in switch speed.", "name": "default_initial_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_active"...<truncated 9212 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:Manual_to_Ask_StartAC_on_InitiateAC", "transition:Ask_StartAC_self_on_ChangeSetpoint", "transition:Ask_StartAC_to_AutocontrolInit_on_StartAC", "transition:AutocontrolNormal_to_PumpFault_on_PumpFault", "transition:PumpFault_to_Manual_on_FaultRemoved", "transition:forced_CA_backManual_to_Manual", "transition:forced_CB_backManual_to_Manual", "transition:forced_CP_backManual_to_Manual", "transition:forced_CC_backManual_to_Manual"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 4 / iteration `0` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:ecb9bdac24ae47785ee8d47eeb8a8609d691ab33bf9e24653c21a3c50ce71850`；candidate_dsl_hash：`sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Forced back-to-Manual recovery can clear pump fault and alarm state without the caregiver fault-removal event, losing the NL-required distinction between a fault occurring, alarm activation, caregiver removal, and software release/control fallback.
- 2. `<unknown>` `` policy=``：Autocontrol pump-speed semantics are not faithfully represented: the NL says pump speed is set by a control voltage in autocontrol mode, but the DSL only writes `control_voltage` and does not update `pump_speed` during autocontrol.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-7607c16ecc0`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault..."', 'DSL: `! * -> Manual :: CP_backManual;` and other forced `*_backManual` transitions target `Manual` from any state.', 'DSL: `Manual.enter` sets `alarm_active = 0; pump_fault = 0; software_control = 0;`.', 'Simulation scenario `forced_cp_backmanual_from_pump_fault` expects CP_backManual from PumpFault to enter Manual with `pump_fault: 0` and `alarm_active: 0`, without `FaultRemoved`.'], 'severity': 'major', 'summary': 'Forced back-to-Manual recovery can clear pump fault and alarm state without the caregiver fault-removal event, losing the NL-required distinction between a fault occurring, alarm activation, caregiver removal, and software release/control fallback.'}` |
| `fixreq-0-sl7-1-23c6ba7ffb` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: "in autocontrol mode pump speed is set by a control voltage from an external source."', 'DSL `AutocontrolNormal.during`: `control_voltage = flow_rate;` but no `pump_speed = ...` assignment.', 'Manual mode explicitly updates `pump_speed = manual_switch_speed`, showing pump speed is modeled but not connected to control voltage in autocontrol.'], 'severity': 'major', 'summary': 'Autocontrol pump-speed semantics are not faithfully represented: the NL says pump speed is set by a control voltage in autocontrol mode, but the DSL only writes `control_voltage` and does not update `pump_speed` during autocontrol.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:blood_pressure, variable:shared_bp_buffer, variable:target_bp, variable:requested_target_bp, variable:flow_rate, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2675`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ✅ | The request is rework-locked and the evidence remains valid. The repair preserves Manual as the shared recovery target and keeps software release on entry to Manual, but prevents forced back-to-Manual recovery from clearing pump_fault or alarm_active before the explicit caregiver FaultRemoved event. Startup still initializes the model with no active fault/al...<truncated 332 chars> |
| `fixreq-0-sl7-1-23c6ba7ffb` | `accept` | ❌ | ✅ | The request is rework-locked and the evidence remains valid. Normal autocontrol now explicitly sets pump_speed from control_voltage after computing the control voltage, preserving the NL distinction between manual switch-driven speed and autocontrol voltage-driven speed.；intent=Assign pump_speed = control_voltage in AutocontrolNormal.during after control_vol...<truncated 16 chars> |
- repair_rationale：Manual remains the shared recovery target for CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC.；Forced fallback to Manual now releases software control through Manual.enter but preserves the pump fault and alarm until the caregiver FaultRemoved event.；Initial default startup still begins in Manual with pump_fault and alarm_active cleared via the initial transition effect, avoiding unsafe clearing on later forced recovery.；FaultRemoved is represented both from PumpFault and as a Manual self-transition so caregiver removal is still reachable after a forced fallback has already moved the system to Manual.；AutocontrolNormal explicitly maps the computed control_voltage to pump_speed during complication-free autocontrol.
- diff_summary：`{"summary": "Removed unconditional pump_fault/alarm_active resets from Manual.enter; added startup-only clearing on the initial transition to Manual; added Manual self FaultRemoved clearing; added FaultRemoved clearing effect on PumpFault -> Manual; retained all grounded required states/events/transitions; added pump_speed = control_voltage in AutocontrolNormal.during."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float blood_pressure = 0.0;
def float shared_bp_buffer = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float manual_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! * -> Manual :: TerminateAC;

        [*] -> Manual effect {
            pump_fault = 0;
            alarm_active = 0;
        };

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
                control_voltage = 0.0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                shared_bp_buffer = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                shared_bp_buffer = blood_pressure;
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                software_control = 0;
                control_voltage = 0.0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Manual -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            alarm_active = 0;
        };
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault :: PumpFault;
        PumpFault -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            alarm_active = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -23,14 +23,15 @@
         ! * -> Manual :: CC_backManual;
         ! * -> Manual :: TerminateAC;
 
-        [*] -> Manual;
+        [*] -> Manual effect {
+            pump_fault = 0;
+            alarm_active = 0;
+        };
 
         state Manual {
             enter {
                 CA_mode = 0;
                 software_control = 0;
-                alarm_active = 0;
-                pump_fault = 0;
                 flow_rate = default_flow_rate;
                 pump_speed = manual_switch_speed;
                 control_voltage = 0.0;
@@ -61,6 +62,7 @@
                 if [pump_fault == 0] {
                     flow_rate = target_bp - blood_pressure;
                     control_voltage = flow_rate;
+                    pump_speed = control_voltage;
                     log_count = log_count + 1;
                 }
             }
@@ -76,10 +78,17 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
+        Manual -> Manual :: FaultRemoved effect {
+            pump_fault = 0;
+            alarm_active = 0;
+        };
         Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
         Ask_StartAC -> AutocontrolInit :: StartAC;
         AutocontrolInit -> AutocontrolNormal;
         AutocontrolNormal -> PumpFault :: PumpFault;
-        PumpFault -> Manual :: FaultRemoved;
+        PumpFault -> Manual :: FaultRemoved effect {
+            pump_fault = 0;
+            alarm_active = 0;
+        };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:274267a5ad9ab0296aa3da154ce4375a6bb54a9ba9b101ba690b37e4c162037f`。
  - SL-10 evidence 1: `{"summary": "The candidate resolves fixreq-0-sl7-0-be1e03bda7 against the NL unsafe-recovery requirement. The NL requires pump fault/alarm activation, caregiver fault removal, and software release/control fallback to remain distinct. The old DSL cleared pump_fault and alarm_active on every Manual entry, so forced CA/CB/CP/CC_backManual transitions could erase a fault without FaultRemoved. The candidate removes those unconditional clears from Manual.enter, keeps Manual as the shared recovery target, releases software_control on Manual entry, initializes clear startup values only on the initial transition, and clears pump_fault/alarm_active only on FaultRemoved paths from PumpFault or Manual a...<truncated 23 chars>`
  - SL-10 evidence 2: `{"summary": "The candidate resolves fixreq-0-sl7-1-23c6ba7ffb against the NL autocontrol pump-speed requirement. The NL states that in autocontrol mode pump speed is set by a control voltage. The candidate keeps the existing flow_rate and control_voltage computation in AutocontrolNormal.during and adds pump_speed = control_voltage, while Manual continues to set pump_speed from manual_switch_speed. This preserves the NL distinction between manual switch-driven speed and autocontrol voltage-driven speed."}`
  - SL-10 evidence 3: `{"summary": "The required grounded states, variables, events, and scenario obligations are preserved in the candidate: CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault; variables including blood_pressure, shared_bp_buffer, target_bp, requested_target_bp, flow_rate, default_flow_rate, manual_switch_speed, pump_speed, control_voltage, CA_mode, software_control, pump_fault, alarm_active, and log_count; and events including InitiateAC, ChangeSetpoint, StartAC, PumpFault, FaultRemoved, CA_backManual, CB_backManual, CP_backManual, and CC_backManual."}`
  - SL-10 evidence 4: `{"summary": "The DSL diff is minimal and aligned with the complete FixLog ledger: it retains all previously accepted SL-9 edits, implements the SL-10 rework instruction to add startup-only clearing and Manual self FaultRemoved clearing, preserves PumpFault -> Manual on FaultRemoved, and retains pump_speed = control_voltage in normal autocontrol."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 8, "n_scenarios_passed": 6, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init dispatches into Manual and applies manual operation outputs from the caregiver-set default flow and built-in switch speed.", "name": "default_initial_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_active"...<truncated 9212 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:Manual_to_Ask_StartAC_on_InitiateAC", "transition:Ask_StartAC_self_on_ChangeSetpoint", "transition:Ask_StartAC_to_AutocontrolInit_on_StartAC", "transition:AutocontrolNormal_to_PumpFault_on_PumpFault", "transition:PumpFault_to_Manual_on_FaultRemoved", "transition:forced_CA_backManual_to_Manual", "transition:forced_CB_backManual_to_Manual", "transition:forced_CP_backManual_to_Manual", "transition:forced_CC_backManual_to_Manual"], "kind": "missing_required_grounding"}

</details>

<details><summary>Repair 5 / iteration `0` / source `SL-7` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:ecb9bdac24ae47785ee8d47eeb8a8609d691ab33bf9e24653c21a3c50ce71850`；candidate_dsl_hash：`sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Forced back-to-Manual recovery can clear pump fault and alarm state without the caregiver fault-removal event, losing the NL-required distinction between a fault occurring, alarm activation, caregiver removal, and software release/control fallback.
- 2. `<unknown>` `` policy=``：Autocontrol pump-speed semantics are not faithfully represented: the NL says pump speed is set by a control voltage in autocontrol mode, but the DSL only writes `control_voltage` and does not update `pump_speed` during autocontrol.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-7607c16ecc0`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sl7-0-be1e03bda7` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault..."', 'DSL: `! * -> Manual :: CP_backManual;` and other forced `*_backManual` transitions target `Manual` from any state.', 'DSL: `Manual.enter` sets `alarm_active = 0; pump_fault = 0; software_control = 0;`.', 'Simulation scenario `forced_cp_backmanual_from_pump_fault` expects CP_backManual from PumpFault to enter Manual with `pump_fault: 0` and `alarm_active: 0`, without `FaultRemoved`.'], 'severity': 'major', 'summary': 'Forced back-to-Manual recovery can clear pump fault and alarm state without the caregiver fault-removal event, losing the NL-required distinction between a fault occurring, alarm activation, caregiver removal, and software release/control fallback.'}` |
| `fixreq-0-sl7-1-23c6ba7ffb` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL: "in autocontrol mode pump speed is set by a control voltage from an external source."', 'DSL `AutocontrolNormal.during`: `control_voltage = flow_rate;` but no `pump_speed = ...` assignment.', 'Manual mode explicitly updates `pump_speed = manual_switch_speed`, showing pump speed is modeled but not connected to control voltage in autocontrol.'], 'severity': 'major', 'summary': 'Autocontrol pump-speed semantics are not faithfully represented: the NL says pump speed is set by a control voltage in autocontrol mode, but the DSL only writes `control_voltage` and does not update `pump_speed` during autocontrol.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:blood_pressure, variable:shared_bp_buffer, variable:target_bp, variable:requested_target_bp, variable:flow_rate, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2675`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sl7-0-be1e03bda7` | `accept` | ❌ | ✅ | The request is rework-locked and the evidence remains valid. Forced back-to-Manual recovery should release software control and set CA_mode to Manual, but must not clear pump_fault or alarm_active before the explicit caregiver FaultRemoved event. The repair keeps Manual as the shared recovery target, initializes startup with no active fault/alarm through the...<truncated 365 chars> |
| `fixreq-0-sl7-1-23c6ba7ffb` | `accept` | ❌ | ✅ | The request is rework-locked and the evidence remains valid. Normal autocontrol must explicitly set pump_speed from the computed control_voltage to preserve the NL distinction between manual switch-driven speed and autocontrol voltage-driven speed.；intent=Assign pump_speed = control_voltage in AutocontrolNormal.during after control_voltage = flow_rate |
- repair_rationale：Manual remains the shared recovery target for CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC.；Forced fallback to Manual releases software control through Manual.enter but preserves pump_fault and alarm_active until the caregiver FaultRemoved event.；Initial default startup still begins with pump_fault and alarm_active cleared via the initial transition effect, avoiding unsafe clearing on later forced recovery.；FaultRemoved is represented both from PumpFault and as a Manual self-transition so caregiver removal remains reachable after a forced fallback has already moved the machine to Manual.；AutocontrolNormal explicitly maps computed control_voltage to pump_speed during complication-free autocontrol.
- diff_summary：`{"summary": "Removed unconditional pump_fault/alarm_active resets from Manual.enter; added startup-only clearing on the initial transition to Manual; added Manual self FaultRemoved clearing; added FaultRemoved clearing effect on PumpFault -> Manual; retained all grounded required states/events/transitions; added pump_speed = control_voltage in AutocontrolNormal.during."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float blood_pressure = 0.0;
def float shared_bp_buffer = 0.0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float manual_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;
def int CA_mode = 0;
def int software_control = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;
        ! * -> Manual :: TerminateAC;

        [*] -> Manual effect {
            pump_fault = 0;
            alarm_active = 0;
        };

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
                control_voltage = 0.0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_speed = manual_switch_speed;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                shared_bp_buffer = blood_pressure;
            }
        }

        state AutocontrolNormal {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
            during {
                shared_bp_buffer = blood_pressure;
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    control_voltage = flow_rate;
                    pump_speed = control_voltage;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                software_control = 0;
                control_voltage = 0.0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Manual -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            alarm_active = 0;
        };
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault :: PumpFault;
        PumpFault -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            alarm_active = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -23,14 +23,15 @@
         ! * -> Manual :: CC_backManual;
         ! * -> Manual :: TerminateAC;
 
-        [*] -> Manual;
+        [*] -> Manual effect {
+            pump_fault = 0;
+            alarm_active = 0;
+        };
 
         state Manual {
             enter {
                 CA_mode = 0;
                 software_control = 0;
-                alarm_active = 0;
-                pump_fault = 0;
                 flow_rate = default_flow_rate;
                 pump_speed = manual_switch_speed;
                 control_voltage = 0.0;
@@ -61,6 +62,7 @@
                 if [pump_fault == 0] {
                     flow_rate = target_bp - blood_pressure;
                     control_voltage = flow_rate;
+                    pump_speed = control_voltage;
                     log_count = log_count + 1;
                 }
             }
@@ -76,10 +78,17 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
+        Manual -> Manual :: FaultRemoved effect {
+            pump_fault = 0;
+            alarm_active = 0;
+        };
         Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
         Ask_StartAC -> AutocontrolInit :: StartAC;
         AutocontrolInit -> AutocontrolNormal;
         AutocontrolNormal -> PumpFault :: PumpFault;
-        PumpFault -> Manual :: FaultRemoved;
+        PumpFault -> Manual :: FaultRemoved effect {
+            pump_fault = 0;
+            alarm_active = 0;
+        };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:35805363bc05687d124b8351d79142585e10507f0fa14667c2d1d8874b105952`。
  - SL-10 evidence 1: `{"summary": "Request fixreq-0-sl7-0-be1e03bda7 is resolved against the NL and FixLog: the candidate removes unconditional `pump_fault = 0` and `alarm_active = 0` from `Manual.enter`, so forced `CA_backManual`, `CB_backManual`, `CP_backManual`, and `CC_backManual` still make `CA_mode` Manual and release software control through Manual entry without erasing the fault/alarm before the caregiver `FaultRemoved` event. This preserves the NL-required sequence: pump fault occurs, alarm activates, caregiver removes the fault, and when CARA was controlling the pump the software releases control."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves startup semantics without weakening fault recovery: `[ * ] -> Manual effect { pump_fault = 0; alarm_active = 0; }` initializes the default no-fault/no-alarm condition only on initial entry, while later forced fallback to Manual does not clear fault/alarm. This directly follows the SL-10 rework instructions and the accepted SL-9 rework decisions."}`
  - SL-10 evidence 3: `{"summary": "The candidate adds explicit caregiver removal paths required by the accepted repair: `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_active = 0; }` handles direct removal from PumpFault, and `Manual -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_active = 0; }` keeps fault removal reachable after a forced fallback has already returned the mode to Manual."}`
  - SL-10 evidence 4: `{"summary": "Request fixreq-0-sl7-1-23c6ba7ffb is resolved: `AutocontrolNormal.during` computes `flow_rate = target_bp - blood_pressure`, assigns `control_voltage = flow_rate`, and then assigns `pump_speed = control_voltage`, preserving the NL distinction that manual mode uses the built-in switch while autocontrol sets pump speed by control voltage."}`
  - SL-10 evidence 5: `{"summary": "No NL-required grounded states, variables, or events are dropped. The candidate retains `CARA`, `Mode_Control_Algorithm`, `Manual`, `Ask_StartAC`, `AutocontrolInit`, `AutocontrolNormal`, `PumpFault`, all required variables, all required events, and the required transitions for InitiateAC, ChangeSetpoint, StartAC, PumpFault, FaultRemoved, and the four back-to-Manual fallback events."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 8, "n_scenarios_passed": 6, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init dispatches into Manual and applies manual operation outputs from the caregiver-set default flow and built-in switch speed.", "name": "default_initial_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_active"...<truncated 9212 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:Manual_to_Ask_StartAC_on_InitiateAC", "transition:Ask_StartAC_self_on_ChangeSetpoint", "transition:Ask_StartAC_to_AutocontrolInit_on_StartAC", "transition:AutocontrolNormal_to_PumpFault_on_PumpFault", "transition:PumpFault_to_Manual_on_FaultRemoved", "transition:forced_CA_backManual_to_Manual", "transition:forced_CB_backManual_to_Manual", "transition:forced_CP_backManual_to_Manual", "transition:forced_CC_backManual_to_Manual"], "kind": "missing_required_grounding"}

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-7607c16ecc0` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-7607c16ecc0` | accept=2, reject=0 | `sl10_review` | `sha256:0ff4eb8e59c1879f13730e20b7a84f2fb44173c11e58725f0a10aa7c984190b2` | Manual remains the shared recovery target for CA_backManual, CB_backManual, CP_backManual, and CC_backManual, preserving the cross-component fallback requirement., Forced back-to-Manual now releases software control through Manual.enter but preserves pump_fault and alarm_active until the explicit caregiver FaultRemoved event., Normal autocontrol now explicitly connects control_voltage to pump_speed, matching the NL statement that pump speed is set by control voltage in autocontrol mode., ... +1 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-7607c16ecc0` | accept=2, reject=0 | `sl9_rework` | `sha256:0ff4eb8e59c1879f13730e20b7a84f2fb44173c11e58725f0a10aa7c984190b2` | Keep the accepted autocontrol repair: retain `pump_speed = control_voltage` in `AutocontrolNormal.during` after `control_voltage = flow_rate`., Do not restore unconditional `pump_fault = 0` or `alarm_active = 0` clearing in `Manual.enter`, because that would reintroduce the unsafe recovery defect., Add explicit caregiver fault-removal handling that remains reachable after forced fallback to Manual, for example add `Manual -> Manual :: FaultRemoved effect { pump_fault = 0; alarm_active = 0; };` or an equivalent transition/state structure that clears fault/alarm only on the `FaultRemoved` event., ... +4 |
| 4 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-7607c16ecc0` | accept=2, reject=0 | `sl10_review` | `sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04` | Manual remains the shared recovery target for CA_backManual, CB_backManual, CP_backManual, and CC_backManual., Forced back-to-Manual releases software control by entering Manual but preserves pump_fault and alarm_active until an explicit FaultRemoved event., Initial startup into Manual still initializes pump_fault and alarm_active to clear values without weakening forced recovery from PumpFault., ... +3 |
| 5 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-7607c16ecc0` | accept=2, reject=0 | `sl9_rework` | `sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., grounding_update_hint:sha256:604304c842429ae4862c378835afe089e6a88fc12edf7d58f552dbf0242e752f |
| 6 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-7607c16ecc0` | accept=2, reject=0 | `sl10_review` | `sha256:99b0a326ebeea9465293f0e2db1a3b73061d351cb6e6d73b9fddc25f2ec1a5c7` | Manual remains the shared recovery target for CA_backManual, CB_backManual, CP_backManual, and CC_backManual., Forced back-to-Manual recovery now releases software control through Manual.enter but preserves pump_fault and alarm_active until the explicit caregiver FaultRemoved event., Initial default startup still initializes pump_fault and alarm_active to clear values without weakening fault recovery semantics., ... +3 |
| 7 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-7607c16ecc0` | accept=2, reject=0 | `sl9_rework` | `sha256:99b0a326ebeea9465293f0e2db1a3b73061d351cb6e6d73b9fddc25f2ec1a5c7` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale. |
| 8 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-7607c16ecc0` | accept=2, reject=0 | `sl10_review` | `sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04` | Manual remains the shared recovery target for CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC., Forced fallback to Manual now releases software control through Manual.enter but preserves the pump fault and alarm until the caregiver FaultRemoved event., Initial default startup still begins in Manual with pump_fault and alarm_active cleared via the initial transition effect, avoiding unsafe clearing on later forced recovery., ... +3 |
| 9 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-7607c16ecc0` | accept=2, reject=0 | `sl9_rework` | `sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale. |
| 10 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-7607c16ecc0` | accept=2, reject=0 | `sl10_review` | `sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04` | Manual remains the shared recovery target for CA_backManual, CB_backManual, CP_backManual, CC_backManual, and TerminateAC., Forced fallback to Manual releases software control through Manual.enter but preserves pump_fault and alarm_active until the caregiver FaultRemoved event., Initial default startup still begins with pump_fault and alarm_active cleared via the initial transition effect, avoiding unsafe clearing on later forced recovery., ... +4 |
| 11 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-7607c16ecc0` | accept=2, reject=0 | `exit_rejected_rework_budget_exhausted` | `sha256:0cb3a6242da518a08dc9d589109a92d71820925223a1771083859adff4b74c04` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale. |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4557, 'completion_chars': 17842, 'completion_tokens': 0, 'elapsed_seconds': 112.55379108099442, 'first_chunk_seconds': 30.92089325899724, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 25387, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1857, 'completion_chars': 7144, 'completion_tokens': 0, 'elapsed_seconds': 67.301063728999, 'first_chunk_seconds': 34.421792863999144, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 56838, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 2178, 'completion_chars': 9915, 'completion_tokens': 0, 'elapsed_seconds': 50.26042780300486, 'first_chunk_seconds': 10.991440162004437, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 70475, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1065, 'completion_chars': 4552, 'completion_tokens': 0, 'elapsed_seconds': 28.43334351599333, 'first_chunk_seconds': 9.15609403999406, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 52145, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 781, 'completion_chars': 3495, 'completion_tokens': 0, 'elapsed_seconds': 43.465362895003636, 'first_chunk_seconds': 29.530284991997178, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 35030, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1231, 'completion_chars': 5437, 'completion_tokens': 0, 'elapsed_seconds': 32.119295832992066, 'first_chunk_seconds': 9.86438839600305, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 62795, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 803, 'completion_chars': 3609, 'completion_tokens': 0, 'elapsed_seconds': 24.138108241997543, 'first_chunk_seconds': 10.709239609990618, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 47161, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1248, 'completion_chars': 5530, 'completion_tokens': 0, 'elapsed_seconds': 33.62361478499952, 'first_chunk_seconds': 11.063879831999657, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 72412, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 910, 'completion_chars': 4119, 'completion_tokens': 0, 'elapsed_seconds': 27.325520500002312, 'first_chunk_seconds': 10.777280395996058, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 56885, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1253, 'completion_chars': 5571, 'completion_tokens': 0, 'elapsed_seconds': 32.507470964003005, 'first_chunk_seconds': 10.406346075993497, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 82011, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 851, 'completion_chars': 4125, 'completion_tokens': 0, 'elapsed_seconds': 24.388304972992046, 'first_chunk_seconds': 9.00273109599948, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 66527, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1270, 'completion_chars': 5661, 'completion_tokens': 0, 'elapsed_seconds': 31.606397230003495, 'first_chunk_seconds': 8.58442598900001, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 91165, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1038, 'completion_chars': 4641, 'completion_tokens': 0, 'elapsed_seconds': 29.350105036995956, 'first_chunk_seconds': 11.015333677001763, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 73135, 'prompt_tokens': 0, 'stream': True, 'total_tokens': 0}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`not_converged`，record_status=`rejected`。
- 主要原因分类：`model_review_or_quality`。
- required stages executed：`23/16`，missing=`SC-11`。
- repairs：`0/5` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
