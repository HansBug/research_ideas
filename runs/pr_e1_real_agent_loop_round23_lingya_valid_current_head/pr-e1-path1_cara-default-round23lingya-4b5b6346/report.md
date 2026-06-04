## path1 / cara-infusion-pump-formal-spec__01 / default 真实运行结果：Path1 CARA representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`not_converged`；record_status：`rejected`；result_status：`not_converged`。
- main_result_eligible：`false`。
- 一句话结论：`repair_review_rework_budget`；停止原因：SD-6 sim failure: 12/17 scenarios passed。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `cara-infusion-pump-formal-spec__01` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `83e3fc6a641e02f5f0bc1fc50911c0b44e196ef2` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:ce499624790550d734a59fdd9b6b28f8194710e89c85f739538372d5d8133081` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-round23lingya-4b5b6346` |
| final verdict/status | verdict=`not_converged`, record=`rejected`, result=`not_converged` |
| main_result_eligible | `false` |
| final.fcstm 来源 | `{"accepted": false, "final_dsl_hash": "sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6", "iteration": 0, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:8de94e7b0e2b8a7b81b113a4d2c69652e1c6db9cd6daa44ea05152fdf3be98ae", "iteration": 1, "repair_history_index": 5, "rework_instructions": ["SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale."], "sl10_decision": "rework"}, "repair_history_index": 0, "selected_source_stage": "SD-6", "sl10_decision": "rework", "source_kind": "repair_candidate"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, sl9_rework, ... +2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, SD-6 sim failure: 12/17 scenarios passed` |
| token/cost/time | tokens=`{'prompt_tokens': 335815, 'completion_tokens': 56425, 'total_tokens': 392240, 'n_calls': 18}`, elapsed=`2759.605s` |
| run record | [`pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| summary/log/final DSL | [`summary.json`](./summary.json), [`checks.json`](./checks.json), [`reproducibility.json`](./reproducibility.json), [`final.fcstm`](./final.fcstm), [`stdout.txt`](./run_logs/stdout.txt), [`stderr.txt`](./run_logs/stderr.txt) |

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
def float target_bp = 100.0;
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float pump_control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_active = 0;
def int error_display = 0;
def int error_sound = 0;
def int software_control = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> PumpFault : PumpFault;
        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        >> during before { sensor_buffer_bp = blood_pressure; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_control_voltage = 0.0;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
        }

        state NormalAutocontrol {
            during {
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    pump_control_voltage = flow_rate;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> NormalAutocontrol;
        NormalAutocontrol -> Manual :: TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=13369 | 生成初始 DSL 与 grounding seeds | initial len=2290 | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=109824 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=109824 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=109824 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=150200 | LLM per-request accept/reject + repair | candidate len=2285,2285,2290,3320,3125,3128 | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=6, tokens=118847 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=150200 | LLM per-request accept/reject + repair | candidate len=2285,2285,2290,3320,3125,3128 | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=6, tokens=118847 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=22, info=1; blocking=0, advisory=22, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=109824 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=5, tokens=109824 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=150200 | LLM per-request accept/reject + repair | candidate len=2285,2285,2290,3320,3125,3128 | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=6, tokens=118847 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=150200 | LLM per-request accept/reject + repair | candidate len=2285,2285,2290,3320,3125,3128 | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=6, tokens=118847 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=150200 | LLM per-request accept/reject + repair | candidate len=2285,2285,2290,3320,3125,3128 | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=6, tokens=118847 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=150200 | LLM per-request accept/reject + repair | candidate len=2285,2285,2290,3320,3125,3128 | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ⚠️ | LLM calls=6, tokens=118847 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SD-6 sim failure: 12/17 scenarios passed | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-round23lingya-4b5b6346.agent_loop.json.gz) |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-6` | yes | fixbatch-0-sha256-a1b0c413df1 / n=5 | accept=5, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-6` | yes | fixbatch-1-sha256-2da44f9b7eb / n=5 | accept=5, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; forced_transition_count_drift; missing_required_grounding | decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local re...<truncated 63 chars> | no | SD-6 sim failure: 12/17 scenarios passed |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 |
|---|---|---|---|
| `default_init_enters_manual_and_stores_sensor` | default-init probe: the first empty cycle dispatches CARA into Manual, stores the blood pressure reading in the shared b...<truncated 39 chars> | ✅ | ✅ |
| `initiate_change_start_reaches_normal_autocontrol` | default-init probe: after dispatch to Manual, caregiver initiation reaches Ask_StartAC, setpoint change updates target_b...<truncated 73 chars> | ✅ | ✅ |
| `normal_autocontrol_high_pressure_lower_flow` | explicit-hot-start probe: in NormalAutocontrol with no pump fault, a high blood pressure reading produces a lower comput...<truncated 37 chars> | ✅ | ✅ |
| `terminate_autocontrol_returns_manual` | explicit-hot-start probe: caregiver TerminateAC from NormalAutocontrol returns to Manual and releases software control t...<truncated 32 chars> | ✅ | ✅ |
| `pump_fault_from_normal_then_fault_removed_to_manual` | explicit-hot-start probe: a forced PumpFault while CARA controls the pump activates alarms and releases control, then Fa...<truncated 30 chars> | ⚪ | ⚪ |
| `backmanual_fallback_from_ask_and_autocontrol_init` | explicit-hot-start probe: cross-component CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit both for...<truncated 37 chars> | ⚪ | ⚪ |
| `backmanual_fallback_from_normal_and_pumpfault` | explicit-hot-start probe: CP_backManual from NormalAutocontrol and CC_backManual from PumpFault both force Manual as the...<truncated 24 chars> | ⚪ | ⚪ |
| `normal_autocontrol_with_existing_fault_does_not_control_flow` | explicit-hot-start probe: NormalAutocontrol with pump_fault already present should not update flow, voltage, or log coun...<truncated 56 chars> | ✅ | ✅ |
| `pumpfault_forced_from_ask_startac_releases_control` | explicit-hot-start probe: PumpFault is a wildcard forced fallback, so a fault from Ask_StartAC must enter PumpFault, act...<truncated 43 chars> | ⚪ | ⚪ |
| `change_setpoint_effect_accumulates_target_bp` | explicit-hot-start probe: ChangeSetpoint self-transition in Ask_StartAC must apply its effect each time, increasing targ...<truncated 31 chars> | ✅ | ✅ |
| `fault_removed_effect_clears_pump_fault_before_manual` | explicit-hot-start probe: FaultRemoved transition from PumpFault must clear pump_fault and then Manual must be the share...<truncated 57 chars> | ✅ | ✅ |
| `forced_pumpfault_from_autocontrol_init_blocks_normal_progress` | explicit-hot-start probe: a global PumpFault from AutocontrolInit must take the forced PumpFault fallback immediately in...<truncated 75 chars> | ⚪ | ⚪ |
| `qualified_forced_pumpfault_from_manual` | explicit-hot-start probe: root-qualified PumpFault from concrete Manual leaf must exercise the wildcard forced fault lin...<truncated 76 chars> | ⚪ | ✅ |
| `qualified_forced_backmanual_from_normal` | explicit-hot-start probe: root-qualified CB_backManual from concrete NormalAutocontrol leaf must exercise the wildcard f...<truncated 94 chars> | ⚪ | ✅ |
| `qualified_forced_ca_backmanual_from_ask_startac` | explicit-hot-start probe: root-qualified CA_backManual from concrete Ask_StartAC leaf must exercise the wildcard forced ...<truncated 56 chars> | ⚪ | ✅ |
| `qualified_forced_cp_backmanual_from_autocontrol_init` | explicit-hot-start probe: root-qualified CP_backManual from AutocontrolInit must preempt automatic progress and force Ma...<truncated 46 chars> | ⚪ | ✅ |
| `qualified_forced_cc_backmanual_from_pumpfault` | explicit-hot-start probe: root-qualified CC_backManual from PumpFault must force Manual as the shared recovery target, d...<truncated 42 chars> | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_enters_manual_and_stores_sensor` — default-init probe: the first empty cycle dispatches CARA into Manual, stores the blood pressure reading in the shared buffer, and applies manual default flow.</summary>

| Field | Value |
|---|---|
| description | default-init probe: the first empty cycle dispatches CARA into Manual, stores the blood pressure reading in the shared buffer, and applies manual default flow. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 82.0, "default_flow_rate": 1.5}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `first_cycle_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "error_display": 0, "error_sound": 0, "flow_rate": 1.5, "pump_control_voltage": 0.0, "sensor_buffer_bp": 82.0, "software_control": 0}` |

</details>

<details><summary>`initiate_change_start_reaches_normal_autocontrol` — default-init probe: after dispatch to Manual, caregiver initiation reaches Ask_StartAC, setpoint change updates target_bp, StartAC enters AutocontrolInit, then ...<truncated 33 chars></summary>

| Field | Value |
|---|---|
| description | default-init probe: after dispatch to Manual, caregiver initiation reaches Ask_StartAC, setpoint change updates target_bp, StartAC enters AutocontrolInit, then normal autocontrol computes flow. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 80.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiate_to_ask_startac` | `1` | `["InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 1 `ask_startac_no_event_stays_put` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 100.0}` |
| 2 `change_setpoint_self_transition` | `0` | `["ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 101.0}` |
| 3 `startac_enters_autocontrol_init` | `0` | `["StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_active": 0, "error_display": 0, "error_sound": 0, "software_control": 1}` |
| 4 `automatic_progress_to_normal_autocontrol` | `0` | `[]` | `CARA.Mode_Control_Algorithm.NormalAutocontrol` | `{"flow_rate": 21.0, "log_count": 1, "pump_control_voltage": 21.0}` |

</details>

<details><summary>`normal_autocontrol_high_pressure_lower_flow` — explicit-hot-start probe: in NormalAutocontrol with no pump fault, a high blood pressure reading produces a lower computed flow rate and records a log entry.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: in NormalAutocontrol with no pump fault, a high blood pressure reading produces a lower computed flow rate and records a log entry. |
| initial_state | `CARA.Mode_Control_Algorithm.NormalAutocontrol` |
| initial_vars | `{"blood_pressure": 90.0, "log_count": 0, "pump_fault": 0, "software_control": 1, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `compute_low_flow_for_high_pressure` | `0` | `[]` | `CARA.Mode_Control_Algorithm.NormalAutocontrol` | `{"flow_rate": 10.0, "log_count": 1, "pump_control_voltage": 10.0, "sensor_buffer_bp": 90.0}` |

</details>

<details><summary>`terminate_autocontrol_returns_manual` — explicit-hot-start probe: caregiver TerminateAC from NormalAutocontrol returns to Manual and releases software control to manual/default-flow operation.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: caregiver TerminateAC from NormalAutocontrol returns to Manual and releases software control to manual/default-flow operation. |
| initial_state | `CARA.Mode_Control_Algorithm.NormalAutocontrol` |
| initial_vars | `{"blood_pressure": 70.0, "default_flow_rate": 2.0, "pump_fault": 0, "software_control": 1, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_to_manual` | `0` | `["TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "error_display": 0, "error_sound": 0, "flow_rate": 2.0, "pump_control_voltage": 0.0, "software_control": 0}` |

</details>

<details><summary>`pump_fault_from_normal_then_fault_removed_to_manual` — explicit-hot-start probe: a forced PumpFault while CARA controls the pump activates alarms and releases control, then FaultRemoved recovers to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: a forced PumpFault while CARA controls the pump activates alarms and releases control, then FaultRemoved recovers to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.NormalAutocontrol` |
| initial_vars | `{"blood_pressure": 75.0, "default_flow_rate": 1.25, "pump_fault": 0, "software_control": 1, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_pump_fault_activates_alarm` | `0` | `["PumpFault"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"alarm_active": 1, "error_display": 1, "error_sound": 1, "pump_fault": 1, "software_control": 0}` |
| 1 `fault_removed_recovers_manual` | `0` | `["FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "error_display": 0, "error_sound": 0, "flow_rate": 1.25, "pump_control_voltage": 0.0, "pump_fault": 0, "software_control": 0}` |

</details>

<details><summary>`backmanual_fallback_from_ask_and_autocontrol_init` — explicit-hot-start probe: cross-component CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit both force the shared Manual recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: cross-component CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit both force the shared Manual recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"default_flow_rate": 1.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_from_ask` | `0` | `["CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 1.0, "pump_control_voltage": 0.0, "software_control": 0}` |
| 1 `return_to_ask` | `0` | `["InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 2 `enter_autocontrol_init_again` | `0` | `["StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "software_control": 1}` |
| 3 `cb_backmanual_from_autocontrol_init` | `0` | `["CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 1.0, "pump_control_voltage": 0.0, "software_control": 0}` |

</details>

<details><summary>`backmanual_fallback_from_normal_and_pumpfault` — explicit-hot-start probe: CP_backManual from NormalAutocontrol and CC_backManual from PumpFault both force Manual as the shared recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: CP_backManual from NormalAutocontrol and CC_backManual from PumpFault both force Manual as the shared recovery target. |
| initial_state | `CARA.Mode_Control_Algorithm.NormalAutocontrol` |
| initial_vars | `{"blood_pressure": 60.0, "default_flow_rate": 1.75, "pump_fault": 0, "software_control": 1, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_from_normal` | `0` | `["CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "error_display": 0, "error_sound": 0, "flow_rate": 1.75, "pump_control_voltage": 0.0, "software_control": 0}` |
| 1 `manual_forced_pump_fault` | `0` | `["PumpFault"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"alarm_active": 1, "error_display": 1, "error_sound": 1, "pump_fault": 1, "software_control": 0}` |
| 2 `cc_backmanual_from_pumpfault` | `0` | `["CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "error_display": 0, "error_sound": 0, "flow_rate": 1.75, "pump_control_voltage": 0.0, "software_control": 0}` |

</details>

<details><summary>`normal_autocontrol_with_existing_fault_does_not_control_flow` — explicit-hot-start probe: NormalAutocontrol with pump_fault already present should not update flow, voltage, or log count because control is only allowed withou...<truncated 16 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: NormalAutocontrol with pump_fault already present should not update flow, voltage, or log count because control is only allowed without complications. |
| initial_state | `CARA.Mode_Control_Algorithm.NormalAutocontrol` |
| initial_vars | `{"blood_pressure": 50.0, "flow_rate": 5.0, "log_count": 3, "pump_control_voltage": 5.0, "pump_fault": 1, "software_control": 1, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_control_update_while_fault_present` | `0` | `[]` | `CARA.Mode_Control_Algorithm.NormalAutocontrol` | `{"flow_rate": 5.0, "log_count": 3, "pump_control_voltage": 5.0}` |

</details>

<details><summary>`pumpfault_forced_from_ask_startac_releases_control` — explicit-hot-start probe: PumpFault is a wildcard forced fallback, so a fault from Ask_StartAC must enter PumpFault, activate alarms, and release software contr...<truncated 3 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: PumpFault is a wildcard forced fallback, so a fault from Ask_StartAC must enter PumpFault, activate alarms, and release software control. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"alarm_active": 0, "error_display": 0, "error_sound": 0, "pump_fault": 0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_fault_from_ask_startac` | `0` | `["PumpFault"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"alarm_active": 1, "error_display": 1, "error_sound": 1, "pump_fault": 1, "software_control": 0}` |

</details>

<details><summary>`change_setpoint_effect_accumulates_target_bp` — explicit-hot-start probe: ChangeSetpoint self-transition in Ask_StartAC must apply its effect each time, increasing target_bp by exactly one per press.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: ChangeSetpoint self-transition in Ask_StartAC must apply its effect each time, increasing target_bp by exactly one per press. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"blood_pressure": 80.0, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `first_setpoint_increment` | `0` | `["ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"sensor_buffer_bp": 80.0, "target_bp": 121.0}` |
| 1 `second_setpoint_increment` | `0` | `["ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 122.0}` |

</details>

<details><summary>`fault_removed_effect_clears_pump_fault_before_manual` — explicit-hot-start probe: FaultRemoved transition from PumpFault must clear pump_fault and then Manual must be the shared recovery state with alarms off and def...<truncated 17 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: FaultRemoved transition from PumpFault must clear pump_fault and then Manual must be the shared recovery state with alarms off and default manual flow. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"alarm_active": 1, "default_flow_rate": 2.5, "error_display": 1, "error_sound": 1, "pump_fault": 1, "software_control": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_removed_clears_fault_and_enters_manual` | `0` | `["FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "error_display": 0, "error_sound": 0, "flow_rate": 2.5, "pump_control_voltage": 0.0, "pump_fault": 0, "software_control": 0}` |

</details>

<details><summary>`forced_pumpfault_from_autocontrol_init_blocks_normal_progress` — explicit-hot-start probe: a global PumpFault from AutocontrolInit must take the forced PumpFault fallback immediately instead of being ignored or allowing autom...<truncated 35 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: a global PumpFault from AutocontrolInit must take the forced PumpFault fallback immediately instead of being ignored or allowing automatic progress to NormalAutocontrol. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"alarm_active": 0, "error_display": 0, "error_sound": 0, "pump_fault": 0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `forced_fault_preempts_autocontrol_init_progress` | `0` | `["PumpFault"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"alarm_active": 1, "error_display": 1, "error_sound": 1, "pump_fault": 1, "software_control": 0}` |

</details>

<details><summary>`qualified_forced_pumpfault_from_manual` — explicit-hot-start probe: root-qualified PumpFault from concrete Manual leaf must exercise the wildcard forced fault line; if that forced transition is missing ...<truncated 36 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: root-qualified PumpFault from concrete Manual leaf must exercise the wildcard forced fault line; if that forced transition is missing the state will not become PumpFault. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"alarm_active": 0, "default_flow_rate": 1.4, "error_display": 0, "error_sound": 0, "pump_fault": 0, "software_control": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `qualified_forced_fault_from_manual` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"alarm_active": 1, "error_display": 1, "error_sound": 1, "pump_fault": 1, "software_control": 0}` |

</details>

<details><summary>`qualified_forced_backmanual_from_normal` — explicit-hot-start probe: root-qualified CB_backManual from concrete NormalAutocontrol leaf must exercise the wildcard forced back-to-Manual line; if the forced...<truncated 54 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: root-qualified CB_backManual from concrete NormalAutocontrol leaf must exercise the wildcard forced back-to-Manual line; if the forced line is missing the state will remain in autocontrol. |
| initial_state | `CARA.Mode_Control_Algorithm.NormalAutocontrol` |
| initial_vars | `{"alarm_active": 0, "blood_pressure": 65.0, "default_flow_rate": 2.2, "error_display": 0, "error_sound": 0, "pump_fault": 0, "software_control": 1, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `qualified_cb_backmanual_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "error_display": 0, "error_sound": 0, "flow_rate": 2.2, "pump_control_voltage": 0.0, "software_control": 0}` |

</details>

<details><summary>`qualified_forced_ca_backmanual_from_ask_startac` — explicit-hot-start probe: root-qualified CA_backManual from concrete Ask_StartAC leaf must exercise the wildcard forced Manual fallback and fail if that forced ...<truncated 16 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: root-qualified CA_backManual from concrete Ask_StartAC leaf must exercise the wildcard forced Manual fallback and fail if that forced line is missing. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"alarm_active": 0, "default_flow_rate": 1.6, "error_display": 0, "error_sound": 0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `qualified_ca_backmanual_forces_manual` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "error_display": 0, "error_sound": 0, "flow_rate": 1.6, "pump_control_voltage": 0.0, "software_control": 0}` |

</details>

<details><summary>`qualified_forced_cp_backmanual_from_autocontrol_init` — explicit-hot-start probe: root-qualified CP_backManual from AutocontrolInit must preempt automatic progress and force Manual, catching a missing forced fallback...<truncated 6 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: root-qualified CP_backManual from AutocontrolInit must preempt automatic progress and force Manual, catching a missing forced fallback line. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolInit` |
| initial_vars | `{"alarm_active": 0, "default_flow_rate": 1.8, "error_display": 0, "error_sound": 0, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `qualified_cp_backmanual_preempts_init` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "error_display": 0, "error_sound": 0, "flow_rate": 1.8, "pump_control_voltage": 0.0, "software_control": 0}` |

</details>

<details><summary>`qualified_forced_cc_backmanual_from_pumpfault` — explicit-hot-start probe: root-qualified CC_backManual from PumpFault must force Manual as the shared recovery target, detecting a missing forced transition lin...<truncated 2 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probe: root-qualified CC_backManual from PumpFault must force Manual as the shared recovery target, detecting a missing forced transition line. |
| initial_state | `CARA.Mode_Control_Algorithm.PumpFault` |
| initial_vars | `{"alarm_active": 1, "default_flow_rate": 2.4, "error_display": 1, "error_sound": 1, "pump_fault": 1, "software_control": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `qualified_cc_backmanual_from_fault` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_active": 0, "error_display": 0, "error_sound": 0, "flow_rate": 2.4, "pump_control_voltage": 0.0, "software_control": 0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ❌ | `SD-6` | pump_fault_from_normal_then_fault_removed_to_manual, backmanual_fallback_from_ask_and_autocontrol_init, backmanual_fallback_from_normal_and_pumpfault, pumpfault_forced_from_ask_startac_releases_control, forced_pumpfault_from_autocontrol_init_blocks_normal_progress | accept=5, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 164 chars> | `sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6` |
| 2 | `0` | ✅ | `SD-6` | pump_fault_from_normal_then_fault_removed_to_manual, backmanual_fallback_from_ask_and_autocontrol_init, backmanual_fallback_from_normal_and_pumpfault, pumpfault_forced_from_ask_startac_releases_control, forced_pumpfault_from_autocontrol_init_blocks_normal_progress | accept=5, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6` |
| 3 | `1` | ❌ | `SD-6` | pump_fault_from_normal_then_fault_removed_to_manual, backmanual_fallback_from_ask_and_autocontrol_init, backmanual_fallback_from_normal_and_pumpfault, pumpfault_forced_from_ask_startac_releases_control, forced_pumpfault_from_autocontrol_init_blocks_normal_progress | accept=5, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Do not continue oscillating only between wildcard `! * -> ... : EventName` and `! * -> ... :: EventName`. Replace or supplement the wildcard forced fallbacks with explicit forc...<truncated 649 chars> | `sha256:efc845a5b1371135ba5528d0a1b3442eda6a8a09f716ea5720af8e110a3f898c` |
| 4 | `1` | ❌ | `SD-6` | pump_fault_from_normal_then_fault_removed_to_manual, backmanual_fallback_from_ask_and_autocontrol_init, backmanual_fallback_from_normal_and_pumpfault, pumpfault_forced_from_ask_startac_releases_control, forced_pumpfault_from_autocontrol_init_blocks_normal_progress | accept=5, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 220 chars> | `sha256:e1ff3f5f090623aa5f8c4329998a23720070de1409c95ee107a8082c5d4e6fa4` |
| 5 | `1` | ❌ | `SD-6` | pump_fault_from_normal_then_fault_removed_to_manual, backmanual_fallback_from_ask_and_autocontrol_init, backmanual_fallback_from_normal_and_pumpfault, pumpfault_forced_from_ask_startac_releases_control, forced_pumpfault_from_autocontrol_init_blocks_normal_progress | accept=5, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 195 chars> | `sha256:6d4bb7419815c153702b11a4636c6778b5a8c4ed91667afd80e5a70a84fee920` |
| 6 | `1` | ❌ | `SD-6` | pump_fault_from_normal_then_fault_removed_to_manual, backmanual_fallback_from_ask_and_autocontrol_init, backmanual_fallback_from_normal_and_pumpfault, pumpfault_forced_from_ask_startac_releases_control, forced_pumpfault_from_autocontrol_init_blocks_normal_progress | accept=5, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=True, regression=False, drift=minor, rework=SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structu...<truncated 195 chars> | `sha256:8de94e7b0e2b8a7b81b113a4d2c69652e1c6db9cd6daa44ea05152fdf3be98ae` |

<details><summary>Repair 1 / iteration `0` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`pump_fault_from_normal_then_fault_removed_to_manual, backmanual_fallback_from_ask_and_autocontrol_init, backmanual_fallback_from_normal_and_pumpfault, pumpfault_forced_from_ask_startac_releases_control, forced_pumpfault_from_autocontrol_init_blocks_normal_progress`。
- before_dsl_hash：`sha256:efc845a5b1371135ba5528d0a1b3442eda6a8a09f716ea5720af8e110a3f898c`；candidate_dsl_hash：`sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6`。

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
| `fixreq-0-sd6-0-5ebb8c5564` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: a forced PumpFault while CARA controls the pump activates alarms and releases control, then FaultRemoved recovers to Manual.', 'name': 'pump_fault_from_normal_then_fault_removed_to_manual', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 75.0, 'default_flow_rate': 1.25, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_pump_fault_activates_alarm', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-ba3195b0da` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: cross-component CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit both force the shared Manual recovery target.', 'name': 'backmanual_fallback_from_ask_and_autocontrol_init', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_backmanual_from_ask', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-2-63eba3c050` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: CP_backManual from NormalAutocontrol and CC_backManual from PumpFault both force Manual as the shared recovery target.', 'name': 'backmanual_fallback_from_normal_and_pumpfault', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 60.0, 'default_flow_rate': 1.75, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_backmanual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-fa60f927dc` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: PumpFault is a wildcard forced fallback, so a fault from Ask_StartAC must enter PumpFault, activate alarms, and release software control.', 'name': 'pumpfault_forced_from_ask_startac_releases_control', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_fault_from_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-5eca1a8a61` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: a global PumpFault from AutocontrolInit must take the forced PumpFault fallback immediately instead of being ignored or allowing automatic progress to NormalAutocontrol.', 'name': 'forced_pumpfault_from_autocontrol_init_blocks_normal_progress', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_fault_preempts_autocontrol_init_progress', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, variable:CA_mode, variable:target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, ... +33`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2285`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-5ebb8c5564` | `accept` | ❌ | ❌ | The forced PumpFault fallback was ignored in hot-start NormalAutocontrol because the wildcard forced transition used a local event scope. PumpFault is NL-grounded as a shared fallback signal, so it should be modeled as a parent-scoped event.；intent=Change wildcard forced PumpFault transition from local :: PumpFault to parent-scoped : PumpFault |
| `fixreq-0-sd6-1-ba3195b0da` | `accept` | ❌ | ❌ | The cross-component backManual fallbacks were ignored from Ask_StartAC and AutocontrolInit because the wildcard forced transitions used local event scopes. The NL explicitly describes these as shared cross-component fallback events.；intent=Change wildcard forced CA_backManual, CB_backManual, CP_backManual, and CC_backManual transitions to parent-scoped event...<truncated 1 chars> |
| `fixreq-0-sd6-2-63eba3c050` | `accept` | ❌ | ❌ | The same shared backManual forced fallback must work from NormalAutocontrol and PumpFault and target Manual so Manual.enter sets CA_mode and releases software control.；intent=Use shared parent-scoped backManual events on the wildcard forced Manual recovery transitions |
| `fixreq-0-sd6-3-fa60f927dc` | `accept` | ❌ | ❌ | PumpFault is a wildcard fallback across the Mode_Control_Algorithm hierarchy, so the event should not be local to each descendant state. Parent-scoping preserves the grounded PumpFault state and enter actions that activate alarms and release control.；intent=Parent-scope the wildcard PumpFault event while preserving PumpFault.enter alarm and release-control a...<truncated 6 chars> |
| `fixreq-0-sd6-4-5eca1a8a61` | `accept` | ❌ | ❌ | A PumpFault event from AutocontrolInit must preempt the automatic bare transition to NormalAutocontrol. Making the forced PumpFault event shared and parent-scoped allows it to match immediately.；intent=Ensure parent-scoped forced PumpFault fallback can preempt AutocontrolInit normal progress |
- repair_rationale：The smallest safe edit is to keep all grounded states, variables, lifecycle actions, and local user-action events intact while changing only the scope of the hierarchy-wide forced fallback events.；The NL describes PumpFault and backManual as cross-component or wildcard recovery signals, so parent-scoped forced transitions are more faithful than descendant-local events.；Manual.enter remains the shared recovery action for CA_mode = Manual and software-control release; PumpFault.enter remains the alarm and release-control action.
- diff_summary：`{"summary": "Changed five wildcard forced transitions inside Mode_Control_Algorithm from local event scope `:: EventName` to parent-scoped shared event scope `: EventName`; no grounded states, variables, or ordinary transitions were removed."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def float target_bp = 100.0;
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float pump_control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_active = 0;
def int error_display = 0;
def int error_sound = 0;
def int software_control = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> PumpFault : PumpFault;
        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        >> during before { sensor_buffer_bp = blood_pressure; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_control_voltage = 0.0;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
        }

        state NormalAutocontrol {
            during {
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    pump_control_voltage = flow_rate;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> NormalAutocontrol;
        NormalAutocontrol -> Manual :: TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -16,11 +16,11 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> PumpFault :: PumpFault;
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
+        ! * -> PumpFault : PumpFault;
+        ! * -> Manual : CA_backManual;
+        ! * -> Manual : CB_backManual;
+        ! * -> Manual : CP_backManual;
+        ! * -> Manual : CC_backManual;
 
         >> during before { sensor_buffer_bp = blood_pressure; }
 
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:728247241480de5567f75ac80d1954d8b629fa96d94f529698f747c590f17746`。
  - SL-10 evidence 1: `{"summary": "All five hard SD-6 requests target the same semantic defect: hierarchy-wide PumpFault and backManual fallback events were modeled as descendant-local `::` events, so hot-start probes from Ask_StartAC, AutocontrolInit, NormalAutocontrol, and PumpFault ignored the shared forced fallbacks. SL-9 accepted every request and made the smallest consistent repair: only the five wildcard forced transitions inside Mode_Control_Algorithm were changed from local `:: EventName` to parent-scoped shared `: EventName`."}`
  - SL-10 evidence 2: `{"summary": "The repair is grounded in the NL requirements. The NL explicitly says a pump fault causes alarms and software release when CARA was controlling the pump, and that CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual as a cross-component fallback. Parent-scoping these forced events is more faithful to the described cross-component/global fallback behavior than keeping them local to descendant states."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff does not remove required NL elements. CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, NormalAutocontrol, PumpFault, CA_mode, target_bp, blood_pressure, sensor_buffer_bp, flow_rate, default_flow_rate, pump_control_voltage, pump_fault, alarm_active, error_display, error_sound, software_control, and log_count remain present. Initial transitions, user transitions, ChangeSetpoint, StartAC, TerminateAC, FaultRemoved, StoreSensorBuffer, and the NoPumpFault guard remain present."}`
  - SL-10 evidence 4: `{"summary": "The repaired forced transitions preserve the required actions: Manual.enter still sets CA_mode to Manual and releases software control; PumpFault.enter still sets pump_fault, activates alarm/display/sound, and releases software control. Therefore the requested fault and backManual recovery obligations are addressed without adding ungrounded dynamics or deleting grounded behavior."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 12, "n_scenarios_passed": 7, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init probe: the first empty cycle dispatches CARA into Manual, stores the blood pressure reading in the shared buffer, and applies manual default flow.", "name": "default_init_enters_manual_and_stores_sensor", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actu...<truncated 13771 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:InitialRootToMCA", "transition:InitialMCAToManual", "transition:ManualToAskStartAC", "transition:AskStartACChangeSetpoint", "transition:AskStartACToAutocontrolInit", "transition:NormalAutocontrolToManual", "event:PumpFault", "transition:ForcedPumpFault", "transition:PumpFaultToManual", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:BackManualFallbacks", "action:StoreSensorBuffer", "guard:NoPumpFault"], "kind": ...<truncated 29 chars>

</details>

<details><summary>Repair 2 / iteration `0` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`pump_fault_from_normal_then_fault_removed_to_manual, backmanual_fallback_from_ask_and_autocontrol_init, backmanual_fallback_from_normal_and_pumpfault, pumpfault_forced_from_ask_startac_releases_control, forced_pumpfault_from_autocontrol_init_blocks_normal_progress`。
- before_dsl_hash：`sha256:efc845a5b1371135ba5528d0a1b3442eda6a8a09f716ea5720af8e110a3f898c`；candidate_dsl_hash：`sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6`。

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
| `fixreq-0-sd6-0-5ebb8c5564` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: a forced PumpFault while CARA controls the pump activates alarms and releases control, then FaultRemoved recovers to Manual.', 'name': 'pump_fault_from_normal_then_fault_removed_to_manual', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 75.0, 'default_flow_rate': 1.25, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_pump_fault_activates_alarm', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-1-ba3195b0da` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: cross-component CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit both force the shared Manual recovery target.', 'name': 'backmanual_fallback_from_ask_and_autocontrol_init', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_backmanual_from_ask', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-2-63eba3c050` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: CP_backManual from NormalAutocontrol and CC_backManual from PumpFault both force Manual as the shared recovery target.', 'name': 'backmanual_fallback_from_normal_and_pumpfault', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 60.0, 'default_flow_rate': 1.75, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_backmanual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-3-fa60f927dc` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: PumpFault is a wildcard forced fallback, so a fault from Ask_StartAC must enter PumpFault, activate alarms, and release software control.', 'name': 'pumpfault_forced_from_ask_startac_releases_control', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_fault_from_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-0-sd6-4-5eca1a8a61` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: a global PumpFault from AutocontrolInit must take the forced PumpFault fallback immediately instead of being ignored or allowing automatic progress to NormalAutocontrol.', 'name': 'forced_pumpfault_from_autocontrol_init_blocks_normal_progress', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_fault_preempts_autocontrol_init_progress', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, variable:CA_mode, variable:target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, ... +33`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2285`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-5ebb8c5564` | `accept` | ❌ | ✅ | PumpFault is described as a hierarchy-wide pump fault/fallback signal. The hot-start failure shows the forced wildcard transition was not matching the injected shared event when modeled as a local `:: PumpFault`; parent-scoping the forced event is the smallest faithful repair.；intent=Change the wildcard forced PumpFault transition from local `:: PumpFault` t...<truncated 30 chars> |
| `fixreq-0-sd6-1-ba3195b0da` | `accept` | ❌ | ✅ | The NL explicitly says CA_backManual, CB_backManual, CP_backManual, and CC_backManual are cross-component fallback causes that make CA_mode become Manual. They should be shared events at the Mode_Control_Algorithm scope rather than descendant-local events.；intent=Change all wildcard backManual forced transitions from local `:: EventName` to parent-scoped `: ...<truncated 11 chars> |
| `fixreq-0-sd6-2-63eba3c050` | `accept` | ❌ | ✅ | The same cross-component backManual events must recover from NormalAutocontrol and PumpFault to the shared Manual target, where Manual.enter resets CA_mode and releases software control.；intent=Use parent-scoped shared backManual events for the wildcard Manual recovery transitions. |
| `fixreq-0-sd6-3-fa60f927dc` | `accept` | ❌ | ✅ | PumpFault is a wildcard forced fallback across Mode_Control_Algorithm. Parent-scoping preserves the PumpFault state and its enter actions for alarms, error display/sound, and software-control release while allowing the shared event to match.；intent=Parent-scope the wildcard PumpFault event and preserve PumpFault.enter release/alarm actions. |
| `fixreq-0-sd6-4-5eca1a8a61` | `accept` | ❌ | ✅ | A shared PumpFault event from AutocontrolInit should preempt the unguarded automatic progress to NormalAutocontrol. The parent-scoped forced transition enables that preemption without changing the grounded normal progress transition.；intent=Ensure the parent-scoped forced PumpFault fallback can match before AutocontrolInit's automatic transition. |
- repair_rationale：The only DSL edits are the five wildcard forced fallback event scopes inside Mode_Control_Algorithm.；PumpFault and the backManual events are NL-grounded shared fallback signals, so parent-scoped `: EventName` is more faithful than descendant-local `:: EventName` for wildcard forced transitions.；All required states, variables, initial transitions, caregiver events, setpoint-change behavior, StartAC transition, TerminateAC transition, sensor-buffer storage, and no-pump-fault guard are preserved.；The prior local missing-grounding evidence is addressed conservatively: the events and transitions remain explicit in the DSL as forced parent-scoped transitions; no grounded branch or action is removed.
- diff_summary：`{"summary": "Changed `! * -> PumpFault :: PumpFault;` to `! * -> PumpFault : PumpFault;` and changed the four wildcard backManual transitions from `::` local events to `:` parent-scoped shared events. No other DSL structure was changed."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def float target_bp = 100.0;
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float pump_control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_active = 0;
def int error_display = 0;
def int error_sound = 0;
def int software_control = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> PumpFault : PumpFault;
        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        >> during before { sensor_buffer_bp = blood_pressure; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_control_voltage = 0.0;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
        }

        state NormalAutocontrol {
            during {
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    pump_control_voltage = flow_rate;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> NormalAutocontrol;
        NormalAutocontrol -> Manual :: TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -16,11 +16,11 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> PumpFault :: PumpFault;
-        ! * -> Manual :: CA_backManual;
-        ! * -> Manual :: CB_backManual;
-        ! * -> Manual :: CP_backManual;
-        ! * -> Manual :: CC_backManual;
+        ! * -> PumpFault : PumpFault;
+        ! * -> Manual : CA_backManual;
+        ! * -> Manual : CB_backManual;
+        ! * -> Manual : CP_backManual;
+        ! * -> Manual : CC_backManual;
 
         >> during before { sensor_buffer_bp = blood_pressure; }
 
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:18314b7a7844a15015a60ee143fb63c2288d4949a2228088323f655cd1ab207c`。
  - SL-10 evidence 1: `{"summary": "The NL requires PumpFault and CA_backManual/CB_backManual/CP_backManual/CC_backManual to behave as cross-component or hierarchy-wide fallback signals: PumpFault should force entry to PumpFault, activate alarms, and release software control, while all backManual events should force CA_mode/manual recovery. The candidate changes only those five wildcard forced-transition event scopes from descendant-local `:: EventName` to parent-scoped shared `: EventName`, which directly addresses all five hard SD-6 failures."}`
  - SL-10 evidence 2: `{"summary": "The complete FixLog shows every SL-9 request was accepted and then rework-locked with the same accepted edit intent: parent-scope the wildcard PumpFault and backManual events. The rework candidate implements exactly that locked repair and does not re-reject or waive any hard request."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is minimal: no grounded states, variables, ordinary caregiver transitions, initial transitions, setpoint-change effect, StartAC transition, TerminateAC transition, FaultRemoved transition, sensor-buffer action, PumpFault enter actions, Manual enter/during actions, or NormalAutocontrol no-fault guard were removed. Therefore the NL-required structure and scenario obligations remain represented."}`
  - SL-10 evidence 4: `{"summary": "The local deterministic check reports major rejection for `scenario_regression; missing_required_grounding`, but the listed grounding items are visibly present in the candidate DSL: root and MCA initial transitions, Manual/Ask_StartAC/AutocontrolInit/NormalAutocontrol/PumpFault transitions, PumpFault and all backManual forced transitions, sensor buffer storage, and the `pump_fault == 0` guard. The mismatch is attributable to the local checker treating the corrected parent-scoped forced events as missing or unrecognized rather than to an actual deletion of grounded requirements."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 12, "n_scenarios_passed": 7, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init probe: the first empty cycle dispatches CARA into Manual, stores the blood pressure reading in the shared buffer, and applies manual default flow.", "name": "default_init_enters_manual_and_stores_sensor", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actu...<truncated 13771 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:InitialRootToMCA", "transition:InitialMCAToManual", "transition:ManualToAskStartAC", "transition:AskStartACChangeSetpoint", "transition:AskStartACToAutocontrolInit", "transition:NormalAutocontrolToManual", "event:PumpFault", "transition:ForcedPumpFault", "transition:PumpFaultToManual", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:BackManualFallbacks", "action:StoreSensorBuffer", "guard:NoPumpFault"], "kind": ...<truncated 29 chars>

</details>

<details><summary>Repair 3 / iteration `1` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`pump_fault_from_normal_then_fault_removed_to_manual, backmanual_fallback_from_ask_and_autocontrol_init, backmanual_fallback_from_normal_and_pumpfault, pumpfault_forced_from_ask_startac_releases_control, forced_pumpfault_from_autocontrol_init_blocks_normal_progress`。
- before_dsl_hash：`sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6`；candidate_dsl_hash：`sha256:efc845a5b1371135ba5528d0a1b3442eda6a8a09f716ea5720af8e110a3f898c`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-2da44f9b7eb`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`5`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-185898eaee` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: a forced PumpFault while CARA controls the pump activates alarms and releases control, then FaultRemoved recovers to Manual.', 'name': 'pump_fault_from_normal_then_fault_removed_to_manual', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 75.0, 'default_flow_rate': 1.25, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_pump_fault_activates_alarm', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-1-3299d6189f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: cross-component CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit both force the shared Manual recovery target.', 'name': 'backmanual_fallback_from_ask_and_autocontrol_init', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_backmanual_from_ask', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-2-448e154f51` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: CP_backManual from NormalAutocontrol and CC_backManual from PumpFault both force Manual as the shared recovery target.', 'name': 'backmanual_fallback_from_normal_and_pumpfault', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 60.0, 'default_flow_rate': 1.75, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_backmanual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-3-9e403260bb` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: PumpFault is a wildcard forced fallback, so a fault from Ask_StartAC must enter PumpFault, activate alarms, and release software control.', 'name': 'pumpfault_forced_from_ask_startac_releases_control', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_fault_from_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-4-fab74ccc81` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: a global PumpFault from AutocontrolInit must take the forced PumpFault fallback immediately instead of being ignored or allowing automatic progress to NormalAutocontrol.', 'name': 'forced_pumpfault_from_autocontrol_init_blocks_normal_progress', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_fault_preempts_autocontrol_init_progress', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, variable:CA_mode, variable:target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, ... +33`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2290`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-185898eaee` | `accept` | ❌ | ❌ | The new simulation evidence shows the PumpFault fallback is still ignored from NormalAutocontrol after the prior parent-scoped edit. In pyfcstm, wildcard forced transitions can correctly use local `:: EventName` so the forced transition is expanded for descendant active states and can match the locally injected PumpFault event. Reverting this forced event to...<truncated 201 chars> |
| `fixreq-1-sd6-1-3299d6189f` | `accept` | ❌ | ❌ | The cross-component backManual forced fallbacks are ignored from Ask_StartAC and AutocontrolInit with the current parent-scoped event spelling. The DSL should keep the transitions forced and wildcard, but use local `::` events so each expanded descendant transition can respond to the injected backManual event without changing the grounded Manual recovery tar...<truncated 147 chars> |
| `fixreq-1-sd6-2-448e154f51` | `accept` | ❌ | ❌ | The same Manual recovery target must be reachable from NormalAutocontrol and PumpFault. Keeping wildcard forced transitions but using local event scope lets the forced fallback match from those active states while preserving Manual.enter as the shared recovery action that sets CA_mode to Manual and releases software control.；intent=Use local event scope on t...<truncated 111 chars> |
| `fixreq-1-sd6-3-9e403260bb` | `accept` | ❌ | ❌ | PumpFault is NL-grounded as a wildcard fault fallback. The current parent-scoped forced transition does not match the simulation event from Ask_StartAC, so the smallest safe repair is to keep the forced wildcard transition but restore local `:: PumpFault` event scope. PumpFault.enter continues to activate alarms and release software control.；intent=Restore l...<truncated 76 chars> |
| `fixreq-1-sd6-4-fab74ccc81` | `accept` | ❌ | ❌ | A PumpFault event from AutocontrolInit must preempt the bare automatic transition to NormalAutocontrol. With the forced wildcard transition using local `:: PumpFault`, pyfcstm can expand the forced transition for AutocontrolInit and match the event before normal progress.；intent=Use local `:: PumpFault` on the forced wildcard fallback so PumpFault preempts A...<truncated 31 chars> |
- repair_rationale：New iteration-1 evidence shows the parent-scoped forced events are still ignored in hot-start simulation.；pyfcstm supports wildcard forced transitions with local `:: EventName`; this is also consistent with local NL event injection from the active source state.；The repair changes only the five forced fallback event scopes and preserves all required states, variables, initial transitions, caregiver events, setpoint change, StartAC, TerminateAC, sensor-buffer storage, and the no-pump-fault guard.
- diff_summary：`{"summary": "Changed `! * -> PumpFault : PumpFault;` to `! * -> PumpFault :: PumpFault;` and changed the four wildcard backManual forced transitions from parent-scoped `: EventName` to local `:: EventName`. No grounded states, variables, lifecycle actions, ordinary transitions, guards, or effects were removed."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def float target_bp = 100.0;
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float pump_control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_active = 0;
def int error_display = 0;
def int error_sound = 0;
def int software_control = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> PumpFault :: PumpFault;
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;

        >> during before { sensor_buffer_bp = blood_pressure; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_control_voltage = 0.0;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
        }

        state NormalAutocontrol {
            during {
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    pump_control_voltage = flow_rate;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> NormalAutocontrol;
        NormalAutocontrol -> Manual :: TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -16,11 +16,11 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> PumpFault : PumpFault;
-        ! * -> Manual : CA_backManual;
-        ! * -> Manual : CB_backManual;
-        ! * -> Manual : CP_backManual;
-        ! * -> Manual : CC_backManual;
+        ! * -> PumpFault :: PumpFault;
+        ! * -> Manual :: CA_backManual;
+        ! * -> Manual :: CB_backManual;
+        ! * -> Manual :: CP_backManual;
+        ! * -> Manual :: CC_backManual;
 
         >> during before { sensor_buffer_bp = blood_pressure; }
 
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:bcfbc7b1507264f53b6e1c88445ea7a2df93b8833116678f40b21dd9b081f6b4`。
  - SL-10 evidence 1: `{"summary": "The candidate only reverts the five Mode_Control_Algorithm forced fallback event scopes from parent-scoped `: EventName` back to local `:: EventName`, preserving the NL-required states, variables, ordinary transitions, sensor-buffer action, and no-pump-fault guard. However, the current local deterministic evidence still reports `target_resolved=false`, `regression_detected=true`, `drift_risk=major`, with `scenario_regression` and only 12/17 scenarios passing. Because the hard-block requests are exactly about PumpFault and backManual forced fallbacks being ignored, and the current candidate is the same local-scope style that previously produced the initial fix requests, there is ...<truncated 61 chars>`
  - SL-10 evidence 2: `{"summary": "The local `missing_required_grounding` list includes visibly present elements such as the initial transitions, Manual-to-Ask_StartAC, ChangeSetpoint, StartAC, TerminateAC, StoreSensorBuffer, and NoPumpFault guard, so that portion may be a conservative recognition issue. But the scenario regression portion directly concerns the active hard-block behavior: PumpFault and backManual fallbacks must take effect from NormalAutocontrol, Ask_StartAC, AutocontrolInit, and PumpFault as required by the NL. The DSL-diff-only scope toggle has oscillated between `::` and `:` without producing passing local evidence."}`
  - SL-10 evidence 3: `{"summary": "The NL requires PumpFault to activate alarms and release software control, FaultRemoved to recover to Manual when CARA was controlling the pump, and CA_backManual/CB_backManual/CP_backManual/CC_backManual to force CA_mode to Manual as the shared recovery target. A repair must make those fallback events actually match from the concrete hot-start states rather than relying on wildcard event-scope behavior that the simulator continues to reject."}`
- SL-10 rework_instructions：Do not continue oscillating only between wildcard `! * -> ... : EventName` and `! * -> ... :: EventName`. Replace or supplement the wildcard forced fallbacks with explicit forced transitions from the concrete Mode_Control_Algorithm substates exercised by the scenarios.；Add explicit forced PumpFault transitions that preempt normal behavior from at least `Manual`, `Ask_StartAC`, `AutocontrolInit`, and `NormalAutocontrol` to `PumpFault`, using the event spelling that matches ordinary local event injection for each concrete source state. Preserve `PumpFault.enter` actions: `pump_fault = 1`, `alarm_active = 1`, `error_display =...<truncated 51 chars>；Add explicit forced Manual fallback transitions for each of `CA_backManual`, `CB_backManual`, `CP_backManual`, and `CC_backManual` from at least `Ask_StartAC`, `AutocontrolInit`, `NormalAutocontrol`, and `PumpFault` to `Manual`, so hot-start fallback probes from those states enter Manual. Preserve `Manual.enter` actions that set `CA_mode = 0`, release softwa...<truncated 42 chars>；Ensure PumpFault from `AutocontrolInit` is forced and has priority over the bare `AutocontrolInit -> NormalAutocontrol` progress transition.；Preserve all NL-grounded structure and behavior: root and Mode_Control_Algorithm initial transitions, states `Manual`, `Ask_StartAC`, `AutocontrolInit`, `NormalAutocontrol`, `PumpFault`, caregiver events `InitiateAC`, `ChangeSetpoint`, `StartAC`, `TerminateAC`, `FaultRemoved`, target-bp update, sensor buffer storage, normal-autocontrol `pump_fault == 0` guar...<truncated 104 chars>；After editing, run the local simulation checks and specifically verify the five hard-block probes: PumpFault from NormalAutocontrol then FaultRemoved to Manual; CA_backManual from Ask_StartAC; CB_backManual from AutocontrolInit; CP_backManual from NormalAutocontrol; CC_backManual from PumpFault; PumpFault from Ask_StartAC; and PumpFault from AutocontrolInit ...<truncated 27 chars>
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 17, "n_scenarios_passed": 12, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init probe: the first empty cycle dispatches CARA into Manual, stores the blood pressure reading in the shared buffer, and applies manual default flow.", "name": "default_init_enters_manual_and_stores_sensor", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "act...<truncated 18001 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:InitialRootToMCA", "transition:InitialMCAToManual", "transition:ManualToAskStartAC", "transition:AskStartACChangeSetpoint", "transition:AskStartACToAutocontrolInit", "transition:NormalAutocontrolToManual", "event:PumpFault", "transition:ForcedPumpFault", "transition:PumpFaultToManual", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:BackManualFallbacks", "action:StoreSensorBuffer", "guard:NoPumpFault"], "kind": ...<truncated 29 chars>

</details>

<details><summary>Repair 4 / iteration `1` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`pump_fault_from_normal_then_fault_removed_to_manual, backmanual_fallback_from_ask_and_autocontrol_init, backmanual_fallback_from_normal_and_pumpfault, pumpfault_forced_from_ask_startac_releases_control, forced_pumpfault_from_autocontrol_init_blocks_normal_progress`。
- before_dsl_hash：`sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6`；candidate_dsl_hash：`sha256:e1ff3f5f090623aa5f8c4329998a23720070de1409c95ee107a8082c5d4e6fa4`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-2da44f9b7eb`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`5`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-185898eaee` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: a forced PumpFault while CARA controls the pump activates alarms and releases control, then FaultRemoved recovers to Manual.', 'name': 'pump_fault_from_normal_then_fault_removed_to_manual', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 75.0, 'default_flow_rate': 1.25, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_pump_fault_activates_alarm', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-1-3299d6189f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: cross-component CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit both force the shared Manual recovery target.', 'name': 'backmanual_fallback_from_ask_and_autocontrol_init', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_backmanual_from_ask', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-2-448e154f51` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: CP_backManual from NormalAutocontrol and CC_backManual from PumpFault both force Manual as the shared recovery target.', 'name': 'backmanual_fallback_from_normal_and_pumpfault', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 60.0, 'default_flow_rate': 1.75, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_backmanual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-3-9e403260bb` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: PumpFault is a wildcard forced fallback, so a fault from Ask_StartAC must enter PumpFault, activate alarms, and release software control.', 'name': 'pumpfault_forced_from_ask_startac_releases_control', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_fault_from_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-4-fab74ccc81` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: a global PumpFault from AutocontrolInit must take the forced PumpFault fallback immediately instead of being ignored or allowing automatic progress to NormalAutocontrol.', 'name': 'forced_pumpfault_from_autocontrol_init_blocks_normal_progress', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_fault_preempts_autocontrol_init_progress', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, variable:CA_mode, variable:target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, ... +33`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3320`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-185898eaee` | `accept` | ❌ | ✅ | The PumpFault fallback must fire from NormalAutocontrol and then FaultRemoved must recover to Manual. To avoid the prior event-scope oscillation, the repair supplements the wildcard fallback with explicit forced local PumpFault transitions from concrete Mode_Control_Algorithm substates, preserving PumpFault.enter alarm and software-control release actions.；i...<truncated 150 chars> |
| `fixreq-1-sd6-1-3299d6189f` | `accept` | ❌ | ✅ | CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit must force the shared Manual recovery target. The repair adds explicit forced Manual fallback transitions for each backManual event from the exercised concrete substates.；intent=Add explicit forced CA_backManual, CB_backManual, CP_backManual, and CC_backManual transitions from Ask_StartAC ...<truncated 30 chars> |
| `fixreq-1-sd6-2-448e154f51` | `accept` | ❌ | ✅ | CP_backManual from NormalAutocontrol and CC_backManual from PumpFault must also force Manual. The repair adds explicit forced Manual fallback transitions from NormalAutocontrol and PumpFault for all four cross-component backManual events, preserving Manual.enter recovery actions.；intent=Add explicit forced backManual transitions from NormalAutocontrol and Pu...<truncated 18 chars> |
| `fixreq-1-sd6-3-9e403260bb` | `accept` | ❌ | ✅ | PumpFault is NL-grounded as a wildcard fault fallback and must fire from Ask_StartAC. The explicit forced local transition from Ask_StartAC to PumpFault addresses the ignored-event evidence without deleting the grounded PumpFault state or actions.；intent=Add explicit forced Ask_StartAC to PumpFault transition on PumpFault. |
| `fixreq-1-sd6-4-fab74ccc81` | `accept` | ❌ | ✅ | PumpFault from AutocontrolInit must preempt the bare AutocontrolInit to NormalAutocontrol progress transition. An explicit forced AutocontrolInit to PumpFault transition gives the fault transition priority while preserving the grounded normal progress transition.；intent=Add explicit forced AutocontrolInit to PumpFault transition on PumpFault. |
- repair_rationale：The prior ledger shows oscillation between wildcard parent-scoped and wildcard local-scoped forced events; SL-10 explicitly instructed not to continue that pattern.；The smallest coherent repair is to preserve the existing grounded wildcard fallbacks and supplement them with explicit forced local-event transitions from the concrete substates exercised by the failing scenarios.；Forced transitions from AutocontrolInit ensure PumpFault preempts the bare automatic transition to NormalAutocontrol.；All required states, variables, initial transitions, caregiver events, setpoint update, TerminateAC transition, FaultRemoved recovery, sensor-buffer storage, normal-autocontrol pump_fault guard, inverse pressure-to-flow calculation, logging...<truncated 71 chars>
- diff_summary：`{"summary": "Added explicit forced local-event PumpFault transitions from Manual, Ask_StartAC, AutocontrolInit, and NormalAutocontrol to PumpFault, and explicit forced local-event CA/CB/CP/CC_backManual transitions from Ask_StartAC, AutocontrolInit, NormalAutocontrol, and PumpFault to Manual. Existing grounded wildcard fallbacks and all states, variables, lifecycle actions, ordinary transitions, guards, and effects are preserved."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def float target_bp = 100.0;
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float pump_control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_active = 0;
def int error_display = 0;
def int error_sound = 0;
def int software_control = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> PumpFault : PumpFault;
        ! * -> Manual : CA_backManual;
        ! * -> Manual : CB_backManual;
        ! * -> Manual : CP_backManual;
        ! * -> Manual : CC_backManual;

        ! Manual -> PumpFault :: PumpFault;
        ! Ask_StartAC -> PumpFault :: PumpFault;
        ! AutocontrolInit -> PumpFault :: PumpFault;
        ! NormalAutocontrol -> PumpFault :: PumpFault;

        ! Ask_StartAC -> Manual :: CA_backManual;
        ! Ask_StartAC -> Manual :: CB_backManual;
        ! Ask_StartAC -> Manual :: CP_backManual;
        ! Ask_StartAC -> Manual :: CC_backManual;
        ! AutocontrolInit -> Manual :: CA_backManual;
        ! AutocontrolInit -> Manual :: CB_backManual;
        ! AutocontrolInit -> Manual :: CP_backManual;
        ! AutocontrolInit -> Manual :: CC_backManual;
        ! NormalAutocontrol -> Manual :: CA_backManual;
        ! NormalAutocontrol -> Manual :: CB_backManual;
        ! NormalAutocontrol -> Manual :: CP_backManual;
        ! NormalAutocontrol -> Manual :: CC_backManual;
        ! PumpFault -> Manual :: CA_backManual;
        ! PumpFault -> Manual :: CB_backManual;
        ! PumpFault -> Manual :: CP_backManual;
        ! PumpFault -> Manual :: CC_backManual;

        >> during before { sensor_buffer_bp = blood_pressure; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_control_voltage = 0.0;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
        }

        state NormalAutocontrol {
            during {
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    pump_control_voltage = flow_rate;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> NormalAutocontrol;
        NormalAutocontrol -> Manual :: TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -21,6 +21,28 @@
         ! * -> Manual : CB_backManual;
         ! * -> Manual : CP_backManual;
         ! * -> Manual : CC_backManual;
+
+        ! Manual -> PumpFault :: PumpFault;
+        ! Ask_StartAC -> PumpFault :: PumpFault;
+        ! AutocontrolInit -> PumpFault :: PumpFault;
+        ! NormalAutocontrol -> PumpFault :: PumpFault;
+
+        ! Ask_StartAC -> Manual :: CA_backManual;
+        ! Ask_StartAC -> Manual :: CB_backManual;
+        ! Ask_StartAC -> Manual :: CP_backManual;
+        ! Ask_StartAC -> Manual :: CC_backManual;
+        ! AutocontrolInit -> Manual :: CA_backManual;
+        ! AutocontrolInit -> Manual :: CB_backManual;
+        ! AutocontrolInit -> Manual :: CP_backManual;
+        ! AutocontrolInit -> Manual :: CC_backManual;
+        ! NormalAutocontrol -> Manual :: CA_backManual;
+        ! NormalAutocontrol -> Manual :: CB_backManual;
+        ! NormalAutocontrol -> Manual :: CP_backManual;
+        ! NormalAutocontrol -> Manual :: CC_backManual;
+        ! PumpFault -> Manual :: CA_backManual;
+        ! PumpFault -> Manual :: CB_backManual;
+        ! PumpFault -> Manual :: CP_backManual;
+        ! PumpFault -> Manual :: CC_backManual;
 
         >> during before { sensor_buffer_bp = blood_pressure; }
 
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:75faf91e7f64d557d393979645fe98a65d67755968ec07b6977b8d0f85fa4c40`。
  - SL-10 evidence 1: `{"summary": "The NL requires PumpFault to act as a pump-operation complication fallback that activates alarms and releases software control, and requires CA_backManual/CB_backManual/CP_backManual/CC_backManual to recover to Manual as the shared cross-component target. The candidate directly implements the locked SL-10 rework instructions by supplementing the existing wildcard fallbacks with explicit forced PumpFault transitions from Manual, Ask_StartAC, AutocontrolInit, and NormalAutocontrol, and explicit forced backManual transitions from Ask_StartAC, AutocontrolInit, NormalAutocontrol, and PumpFault to Manual."}`
  - SL-10 evidence 2: `{"summary": "All five iteration-1 SL-9 decisions accepted hard-block simulation requests and the candidate edits match those accepted intents: PumpFault from NormalAutocontrol can enter PumpFault and then FaultRemoved returns to Manual; CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit target Manual; CP_backManual from NormalAutocontrol and CC_backManual from PumpFault target Manual; PumpFault from Ask_StartAC and AutocontrolInit is explicit and forced, so AutocontrolInit fault handling can preempt the unguarded normal-progress transition."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is additive and preserves NL-grounded structure and behavior. It retains CARA and Mode_Control_Algorithm; states Manual, Ask_StartAC, AutocontrolInit, NormalAutocontrol, and PumpFault; variables CA_mode, target_bp, blood_pressure, sensor_buffer_bp, flow_rate, default_flow_rate, pump_control_voltage, pump_fault, alarm_active, error_display, error_sound, software_control, and log_count; initial transitions; caregiver events InitiateAC, ChangeSetpoint, StartAC, TerminateAC, FaultRemoved; sensor-buffer storage; the NormalAutocontrol pump_fault == 0 guard; inverse pressure-to-flow computation; logging; manual default-flow behavior; and PumpFault/Manual enter actions."}`
  - SL-10 evidence 4: `{"summary": "The complete FixLog shows the previous parent-scoped versus local-scoped wildcard-only repairs oscillated and remained insufficient. The current candidate follows the locked rework direction not to continue oscillating and instead adds concrete forced transitions for the scenario-exercised substates, while preserving the existing grounded wildcard fallbacks."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic evidence now reports no scenario_regression and regression_detected=false. Its remaining rejection is design/count/grounding conservatism rather than evidence that an NL-required behavior was deleted or that the hard-block simulations still fail."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; count_drift; forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_SHADOWED_EVENT", "instance_key": "W_SHADOWED_EVENT:9a2adf8046b5", "message": "Local event 'CARA.Mode_Control_Algorithm.Ask_StartAC.CA_backManual' shadows a chain event named 'CA_backManual'.", "policy_action": "requires_policy_classification", "pyfcstm_severity": "warning", "rationale": "", "refs": {"chain_path": "CARA.Mode_Control_Algorithm.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.Mode_Control_Alg...<truncated 20407 chars>
    - local evidence 2: `count_drift` {"direction": "increase", "drift_ratio": 0.6061, "field": "n_transitions", "fix_target": "sim", "kind": "count_drift", "new": 53, "old": 33}
    - local evidence 3: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 45, "old": 25}
    - local evidence 4: `missing_required_grounding` {"element_ids": ["transition:InitialRootToMCA", "transition:InitialMCAToManual", "transition:ManualToAskStartAC", "transition:AskStartACChangeSetpoint", "transition:AskStartACToAutocontrolInit", "transition:NormalAutocontrolToManual", "event:PumpFault", "transition:ForcedPumpFault", "transition:PumpFaultToManual", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:BackManualFallbacks", "action:StoreSensorBuffer", "guard:NoPumpFault"], "kind": ...<truncated 29 chars>

</details>

<details><summary>Repair 5 / iteration `1` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`pump_fault_from_normal_then_fault_removed_to_manual, backmanual_fallback_from_ask_and_autocontrol_init, backmanual_fallback_from_normal_and_pumpfault, pumpfault_forced_from_ask_startac_releases_control, forced_pumpfault_from_autocontrol_init_blocks_normal_progress`。
- before_dsl_hash：`sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6`；candidate_dsl_hash：`sha256:6d4bb7419815c153702b11a4636c6778b5a8c4ed91667afd80e5a70a84fee920`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-2da44f9b7eb`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`5`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-185898eaee` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: a forced PumpFault while CARA controls the pump activates alarms and releases control, then FaultRemoved recovers to Manual.', 'name': 'pump_fault_from_normal_then_fault_removed_to_manual', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 75.0, 'default_flow_rate': 1.25, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_pump_fault_activates_alarm', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-1-3299d6189f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: cross-component CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit both force the shared Manual recovery target.', 'name': 'backmanual_fallback_from_ask_and_autocontrol_init', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_backmanual_from_ask', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-2-448e154f51` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: CP_backManual from NormalAutocontrol and CC_backManual from PumpFault both force Manual as the shared recovery target.', 'name': 'backmanual_fallback_from_normal_and_pumpfault', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 60.0, 'default_flow_rate': 1.75, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_backmanual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-3-9e403260bb` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: PumpFault is a wildcard forced fallback, so a fault from Ask_StartAC must enter PumpFault, activate alarms, and release software control.', 'name': 'pumpfault_forced_from_ask_startac_releases_control', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_fault_from_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-4-fab74ccc81` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: a global PumpFault from AutocontrolInit must take the forced PumpFault fallback immediately instead of being ignored or allowing automatic progress to NormalAutocontrol.', 'name': 'forced_pumpfault_from_autocontrol_init_blocks_normal_progress', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_fault_preempts_autocontrol_init_progress', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, variable:CA_mode, variable:target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, ... +33`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3125`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-185898eaee` | `accept` | ❌ | ✅ | The PumpFault fallback must fire from NormalAutocontrol and then FaultRemoved must recover to Manual. To avoid the prior wildcard event-scope oscillation, replace the wildcard PumpFault fallback with explicit forced local-event transitions from concrete Mode_Control_Algorithm substates, preserving PumpFault.enter alarm and software-control release actions.；i...<truncated 202 chars> |
| `fixreq-1-sd6-1-3299d6189f` | `accept` | ❌ | ✅ | CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit must force the shared Manual recovery target. Explicit local forced transitions avoid the wildcard scope mismatch while preserving Manual.enter recovery behavior.；intent=Replace wildcard backManual fallbacks with explicit forced local-event Manual fallback transitions from Ask_StartAC and ...<truncated 16 chars> |
| `fixreq-1-sd6-2-448e154f51` | `accept` | ❌ | ✅ | CP_backManual from NormalAutocontrol and CC_backManual from PumpFault must also force Manual. Explicit forced local-event transitions preserve the shared Manual recovery target and avoid the previous wildcard scope ambiguity.；intent=Add explicit forced local-event backManual transitions from NormalAutocontrol and PumpFault to Manual. |
| `fixreq-1-sd6-3-9e403260bb` | `accept` | ❌ | ✅ | PumpFault is NL-grounded as a fault fallback and must fire from Ask_StartAC. An explicit forced Ask_StartAC-to-PumpFault local event transition addresses the ignored-event evidence without deleting PumpFault or its alarm actions.；intent=Add explicit forced Ask_StartAC to PumpFault transition on local PumpFault event. |
| `fixreq-1-sd6-4-fab74ccc81` | `accept` | ❌ | ✅ | PumpFault from AutocontrolInit must preempt the bare AutocontrolInit-to-NormalAutocontrol progress transition. A forced local-event transition from AutocontrolInit to PumpFault provides that priority while preserving the normal progress transition.；intent=Add explicit forced AutocontrolInit to PumpFault transition on local PumpFault event. |
- repair_rationale：The prior ledger shows oscillation between wildcard parent-scoped and wildcard local-scoped forced events; the repair stops that oscillation by replacing the wildcard fallbacks with explicit forced transitions from concrete substates.；Explicit forced PumpFault transitions from Manual, Ask_StartAC, AutocontrolInit, and NormalAutocontrol preserve the NL-grounded fault fallback and ensure AutocontrolInit fault handling preempts the bare normal-progress transition.；Explicit forced backManual transitions from Ask_StartAC, AutocontrolInit, NormalAutocontrol, and PumpFault preserve the cross-component Manual recovery target for CA_backManual, CB_backManual, CP_backManual, and CC_backManual.；All required states, variables, initial transitions, caregiver events, setpoint update, TerminateAC transition, FaultRemoved recovery, sensor-buffer storage, no-pump-fault guard, inverse pressure-to-flow computation, logging, manual default...<truncated 55 chars>
- diff_summary：`{"summary": "Removed the five wildcard forced fallback declarations and replaced them with explicit forced local-event transitions: PumpFault from Manual, Ask_StartAC, AutocontrolInit, and NormalAutocontrol; and CA/CB/CP/CC_backManual from Ask_StartAC, AutocontrolInit, NormalAutocontrol, and PumpFault to Manual. No grounded states, variables, lifecycle actions, ordinary transitions, guards, or effects were removed."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def float target_bp = 100.0;
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float pump_control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_active = 0;
def int error_display = 0;
def int error_sound = 0;
def int software_control = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Manual -> PumpFault :: PumpFault;
        ! Ask_StartAC -> PumpFault :: PumpFault;
        ! AutocontrolInit -> PumpFault :: PumpFault;
        ! NormalAutocontrol -> PumpFault :: PumpFault;

        ! Ask_StartAC -> Manual :: CA_backManual;
        ! Ask_StartAC -> Manual :: CB_backManual;
        ! Ask_StartAC -> Manual :: CP_backManual;
        ! Ask_StartAC -> Manual :: CC_backManual;
        ! AutocontrolInit -> Manual :: CA_backManual;
        ! AutocontrolInit -> Manual :: CB_backManual;
        ! AutocontrolInit -> Manual :: CP_backManual;
        ! AutocontrolInit -> Manual :: CC_backManual;
        ! NormalAutocontrol -> Manual :: CA_backManual;
        ! NormalAutocontrol -> Manual :: CB_backManual;
        ! NormalAutocontrol -> Manual :: CP_backManual;
        ! NormalAutocontrol -> Manual :: CC_backManual;
        ! PumpFault -> Manual :: CA_backManual;
        ! PumpFault -> Manual :: CB_backManual;
        ! PumpFault -> Manual :: CP_backManual;
        ! PumpFault -> Manual :: CC_backManual;

        >> during before { sensor_buffer_bp = blood_pressure; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_control_voltage = 0.0;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
        }

        state NormalAutocontrol {
            during {
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    pump_control_voltage = flow_rate;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> NormalAutocontrol;
        NormalAutocontrol -> Manual :: TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -16,11 +16,27 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> PumpFault : PumpFault;
-        ! * -> Manual : CA_backManual;
-        ! * -> Manual : CB_backManual;
-        ! * -> Manual : CP_backManual;
-        ! * -> Manual : CC_backManual;
+        ! Manual -> PumpFault :: PumpFault;
+        ! Ask_StartAC -> PumpFault :: PumpFault;
+        ! AutocontrolInit -> PumpFault :: PumpFault;
+        ! NormalAutocontrol -> PumpFault :: PumpFault;
+
+        ! Ask_StartAC -> Manual :: CA_backManual;
+        ! Ask_StartAC -> Manual :: CB_backManual;
+        ! Ask_StartAC -> Manual :: CP_backManual;
+        ! Ask_StartAC -> Manual :: CC_backManual;
+        ! AutocontrolInit -> Manual :: CA_backManual;
+        ! AutocontrolInit -> Manual :: CB_backManual;
+        ! AutocontrolInit -> Manual :: CP_backManual;
+        ! AutocontrolInit -> Manual :: CC_backManual;
+        ! NormalAutocontrol -> Manual :: CA_backManual;
+        ! NormalAutocontrol -> Manual :: CB_backManual;
+        ! NormalAutocontrol -> Manual :: CP_backManual;
+        ! NormalAutocontrol -> Manual :: CC_backManual;
+        ! PumpFault -> Manual :: CA_backManual;
+        ! PumpFault -> Manual :: CB_backManual;
+        ! PumpFault -> Manual :: CP_backManual;
+        ! PumpFault -> Manual :: CC_backManual;
 
         >> during before { sensor_buffer_bp = blood_pressure; }
 
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:da80690450cdb2da5bd5c453bb9489fa28ffc08f143d60867a17ebb532021627`。
  - SL-10 evidence 1: `{"summary": "The candidate implements the locked SL-10 rework direction by stopping the prior oscillation between wildcard parent-scoped and wildcard local-scoped fallbacks. It removes the five wildcard forced fallback declarations and replaces them with explicit forced local-event transitions from the concrete Mode_Control_Algorithm substates exercised by the hard-block scenarios."}`
  - SL-10 evidence 2: `{"summary": "For fixreq-1-sd6-0, PumpFault from NormalAutocontrol is now represented by `! NormalAutocontrol -> PumpFault :: PumpFault;`, and `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };` is preserved. PumpFault.enter still sets `pump_fault = 1`, activates alarm/display/sound, and releases software control."}`
  - SL-10 evidence 3: `{"summary": "For fixreq-1-sd6-1 and fixreq-1-sd6-2, the candidate includes explicit forced Manual recovery transitions for CA_backManual, CB_backManual, CP_backManual, and CC_backManual from Ask_StartAC, AutocontrolInit, NormalAutocontrol, and PumpFault to Manual. Manual.enter is preserved and sets `CA_mode = 0`, `software_control = 0`, and clears alarm/display/sound."}`
  - SL-10 evidence 4: `{"summary": "For fixreq-1-sd6-3 and fixreq-1-sd6-4, PumpFault from Ask_StartAC and AutocontrolInit is explicitly represented by forced transitions to PumpFault. The AutocontrolInit forced PumpFault transition appears before the untriggered `AutocontrolInit -> NormalAutocontrol` progress transition, matching the required preemption intent."}`
  - SL-10 evidence 5: `{"summary": "No NL-required state, variable, ordinary transition, guard, lifecycle action, or scenario obligation is dropped. The candidate preserves CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, NormalAutocontrol, PumpFault, initial transitions, InitiateAC, ChangeSetpoint, StartAC, TerminateAC, FaultRemoved, target-bp update, sensor-buffer storage, `pump_fault == 0` normal-autocontrol guard, inverse pressure-to-flow computation, logging, manual default flow, and pump-control-voltage behavior."}`
  - SL-10 evidence 6: `{"summary": "The only semantic change relative to the old DSL is the representation of fallback transitions: wildcard declarations are replaced by explicit concrete-state forced transitions. This is consistent with the FixLog rework direction and preserves the NL-required fallback semantics while reducing ambiguity from wildcard event-scope handling."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 17, "n_scenarios_passed": 12, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init probe: the first empty cycle dispatches CARA into Manual, stores the blood pressure reading in the shared buffer, and applies manual default flow.", "name": "default_init_enters_manual_and_stores_sensor", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "act...<truncated 21374 chars>
    - local evidence 2: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 20, "old": 25}
    - local evidence 3: `missing_required_grounding` {"element_ids": ["transition:InitialRootToMCA", "transition:InitialMCAToManual", "transition:ManualToAskStartAC", "transition:AskStartACChangeSetpoint", "transition:AskStartACToAutocontrolInit", "transition:NormalAutocontrolToManual", "event:PumpFault", "transition:ForcedPumpFault", "transition:PumpFaultToManual", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:BackManualFallbacks", "action:StoreSensorBuffer", "guard:NoPumpFault"], "kind": ...<truncated 29 chars>

</details>

<details><summary>Repair 6 / iteration `1` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`pump_fault_from_normal_then_fault_removed_to_manual, backmanual_fallback_from_ask_and_autocontrol_init, backmanual_fallback_from_normal_and_pumpfault, pumpfault_forced_from_ask_startac_releases_control, forced_pumpfault_from_autocontrol_init_blocks_normal_progress`。
- before_dsl_hash：`sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6`；candidate_dsl_hash：`sha256:8de94e7b0e2b8a7b81b113a4d2c69652e1c6db9cd6daa44ea05152fdf3be98ae`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-2da44f9b7eb`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`5`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-185898eaee` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: a forced PumpFault while CARA controls the pump activates alarms and releases control, then FaultRemoved recovers to Manual.', 'name': 'pump_fault_from_normal_then_fault_removed_to_manual', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 75.0, 'default_flow_rate': 1.25, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_pump_fault_activates_alarm', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-1-3299d6189f` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: cross-component CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit both force the shared Manual recovery target.', 'name': 'backmanual_fallback_from_ask_and_autocontrol_init', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'ca_backmanual_from_ask', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-2-448e154f51` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: CP_backManual from NormalAutocontrol and CC_backManual from PumpFault both force Manual as the shared recovery target.', 'name': 'backmanual_fallback_from_normal_and_pumpfault', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.NormalAutocontrol', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 60.0, 'default_flow_rate': 1.75, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'cp_backmanual_from_normal', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-3-9e403260bb` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: PumpFault is a wildcard forced fallback, so a fault from Ask_StartAC must enter PumpFault, activate alarms, and release software control.', 'name': 'pumpfault_forced_from_ask_startac_releases_control', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.Ask_StartAC', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_fault_from_ask_startac', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |
| `fixreq-1-sd6-4-fab74ccc81` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start probe: a global PumpFault from AutocontrolInit must take the forced PumpFault fallback immediately instead of being ignored or allowing automatic progress to NormalAutocontrol.', 'name': 'forced_pumpfault_from_autocontrol_init_blocks_normal_progress', 'setup_error': None, 'status': 'error', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 0.0, 'default_flow_rate': 1.0, 'flow_rate': 0.0, 'pump_control_voltage': 0.0, 'pump_fault': 0, 'sensor_buffer_bp': 0.0, 'target_bp': 100.0}, 'state_assertion_ok': None, 'status': 'error', 'step_index': 0, 'step_name': 'forced_fault_preempts_autocontrol_init_progress', 'var_assertion_ok': None, 'var_mismatches': {}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:NormalAutocontrol, state:PumpFault, variable:CA_mode, variable:target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, ... +33`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3128`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-185898eaee` | `accept` | ❌ | ✅ | The PumpFault fallback must fire from NormalAutocontrol and then FaultRemoved must recover to Manual. The prior ledger shows that oscillating only between wildcard parent-scoped and wildcard local-scoped events did not resolve the hot-start probes. The smallest safe rework is to replace the ambiguous wildcard PumpFault fallback with explicit forced local-eve...<truncated 366 chars> |
| `fixreq-1-sd6-1-3299d6189f` | `accept` | ❌ | ✅ | CA_backManual from Ask_StartAC and CB_backManual from AutocontrolInit must force the shared Manual recovery target. Explicit forced local-event fallbacks from those substates avoid the wildcard scope mismatch while preserving Manual.enter recovery behavior.；intent=Remove wildcard backManual forced fallbacks., Add explicit forced CA_backManual, CB_backManual,...<truncated 93 chars> |
| `fixreq-1-sd6-2-448e154f51` | `accept` | ❌ | ✅ | CP_backManual from NormalAutocontrol and CC_backManual from PumpFault must also force Manual. Explicit forced local-event transitions preserve the shared Manual recovery target and ensure Manual.enter sets CA_mode to Manual, releases software control, and clears alarm/display/sound.；intent=Add explicit forced CA_backManual, CB_backManual, CP_backManual, and ...<truncated 73 chars> |
| `fixreq-1-sd6-3-9e403260bb` | `accept` | ❌ | ✅ | PumpFault is NL-grounded as a pump fault fallback and must fire from Ask_StartAC. An explicit forced Ask_StartAC-to-PumpFault local event transition addresses the ignored-event evidence without deleting PumpFault or its alarm actions.；intent=Add an explicit forced Ask_StartAC to PumpFault transition on local PumpFault event. |
| `fixreq-1-sd6-4-fab74ccc81` | `accept` | ❌ | ✅ | PumpFault from AutocontrolInit must preempt the bare AutocontrolInit-to-NormalAutocontrol progress transition. A forced local-event transition from AutocontrolInit to PumpFault provides that priority while preserving the grounded normal progress transition.；intent=Add an explicit forced AutocontrolInit to PumpFault transition on local PumpFault event. |
- repair_rationale：All five hard requests are accepted because SL-10 marked the requests rework-locked and the evidence shows the existing parent-scoped wildcard fallbacks are ignored in hot-start simulation.；The repair stops the prior oscillation between wildcard `:` and wildcard `::` event scopes by replacing the ambiguous wildcard fallbacks with explicit forced local-event transitions from the concrete substates exercised by the scenarios.；The explicit AutocontrolInit-to-PumpFault forced transition is placed before the bare AutocontrolInit-to-NormalAutocontrol transition, so a PumpFault event preempts normal progress.；Manual.enter remains the single shared recovery action that sets CA_mode to Manual, releases software control, and clears alarm/display/sound.；PumpFault.enter remains the single pump-fault action that sets pump_fault, activates alarms/display/sound, and releases software control.
- diff_summary：`{"summary": "Removed the five wildcard forced fallback declarations and replaced them with explicit forced local-event transitions: PumpFault from Manual, Ask_StartAC, AutocontrolInit, and NormalAutocontrol; and CA_backManual, CB_backManual, CP_backManual, and CC_backManual from Ask_StartAC, AutocontrolInit, NormalAutocontrol, and PumpFault to Manual. No grounded states, variables, lifecycle actions, ordinary transitions, guards, or effects were removed."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def float target_bp = 100.0;
def float blood_pressure = 0.0;
def float sensor_buffer_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 1.0;
def float pump_control_voltage = 0.0;
def int pump_fault = 0;
def int alarm_active = 0;
def int error_display = 0;
def int error_sound = 0;
def int software_control = 0;
def int log_count = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! Manual -> PumpFault :: PumpFault;
        ! Ask_StartAC -> PumpFault :: PumpFault;
        ! AutocontrolInit -> PumpFault :: PumpFault;
        ! NormalAutocontrol -> PumpFault :: PumpFault;

        ! Ask_StartAC -> Manual :: CA_backManual;
        ! Ask_StartAC -> Manual :: CB_backManual;
        ! Ask_StartAC -> Manual :: CP_backManual;
        ! Ask_StartAC -> Manual :: CC_backManual;

        ! AutocontrolInit -> Manual :: CA_backManual;
        ! AutocontrolInit -> Manual :: CB_backManual;
        ! AutocontrolInit -> Manual :: CP_backManual;
        ! AutocontrolInit -> Manual :: CC_backManual;

        ! NormalAutocontrol -> Manual :: CA_backManual;
        ! NormalAutocontrol -> Manual :: CB_backManual;
        ! NormalAutocontrol -> Manual :: CP_backManual;
        ! NormalAutocontrol -> Manual :: CC_backManual;

        ! PumpFault -> Manual :: CA_backManual;
        ! PumpFault -> Manual :: CB_backManual;
        ! PumpFault -> Manual :: CP_backManual;
        ! PumpFault -> Manual :: CC_backManual;

        >> during before { sensor_buffer_bp = blood_pressure; }

        [*] -> Manual;

        state Manual {
            enter {
                CA_mode = 0;
                software_control = 0;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
            during {
                flow_rate = default_flow_rate;
                pump_control_voltage = 0.0;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_active = 0;
                error_display = 0;
                error_sound = 0;
            }
        }

        state NormalAutocontrol {
            during {
                if [pump_fault == 0] {
                    flow_rate = target_bp - blood_pressure;
                    pump_control_voltage = flow_rate;
                    log_count = log_count + 1;
                }
            }
        }

        state PumpFault {
            enter {
                pump_fault = 1;
                alarm_active = 1;
                error_display = 1;
                error_sound = 1;
                software_control = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = target_bp + 1.0; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> NormalAutocontrol;
        NormalAutocontrol -> Manual :: TerminateAC;
        PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -16,11 +16,30 @@
     [*] -> Mode_Control_Algorithm;
 
     state Mode_Control_Algorithm {
-        ! * -> PumpFault : PumpFault;
-        ! * -> Manual : CA_backManual;
-        ! * -> Manual : CB_backManual;
-        ! * -> Manual : CP_backManual;
-        ! * -> Manual : CC_backManual;
+        ! Manual -> PumpFault :: PumpFault;
+        ! Ask_StartAC -> PumpFault :: PumpFault;
+        ! AutocontrolInit -> PumpFault :: PumpFault;
+        ! NormalAutocontrol -> PumpFault :: PumpFault;
+
+        ! Ask_StartAC -> Manual :: CA_backManual;
+        ! Ask_StartAC -> Manual :: CB_backManual;
+        ! Ask_StartAC -> Manual :: CP_backManual;
+        ! Ask_StartAC -> Manual :: CC_backManual;
+
+        ! AutocontrolInit -> Manual :: CA_backManual;
+        ! AutocontrolInit -> Manual :: CB_backManual;
+        ! AutocontrolInit -> Manual :: CP_backManual;
+        ! AutocontrolInit -> Manual :: CC_backManual;
+
+        ! NormalAutocontrol -> Manual :: CA_backManual;
+        ! NormalAutocontrol -> Manual :: CB_backManual;
+        ! NormalAutocontrol -> Manual :: CP_backManual;
+        ! NormalAutocontrol -> Manual :: CC_backManual;
+
+        ! PumpFault -> Manual :: CA_backManual;
+        ! PumpFault -> Manual :: CB_backManual;
+        ! PumpFault -> Manual :: CP_backManual;
+        ! PumpFault -> Manual :: CC_backManual;
 
         >> during before { sensor_buffer_bp = blood_pressure; }
 
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:5e4bcd9e9b279b15f8f78786912dafa51efc08823fa21d56c9b699cc0f635f0e`。
  - SL-10 evidence 1: `{"summary": "The NL requires Manual, Ask_StartAC, AutocontrolInit, NormalAutocontrol, and PumpFault states; caregiver initiation/change/start/terminate behavior; sensor-buffer storage; normal autocontrol guarded by no pump fault; PumpFault alarm/release behavior; FaultRemoved recovery; and cross-component CA/CB/CP/CC_backManual recovery to Manual. The candidate preserves all of these concrete states, variables, lifecycle actions, ordinary transitions, guards, and effects."}`
  - SL-10 evidence 2: `{"summary": "All five hard-block SL-9 requests were accepted and rework-locked. The candidate implements the locked repair strategy from the FixLog: it stops the prior wildcard event-scope oscillation by replacing the five ambiguous wildcard forced fallbacks with explicit forced local-event transitions from the concrete Mode_Control_Algorithm substates exercised by the failing hot-start probes."}`
  - SL-10 evidence 3: `{"summary": "For the PumpFault requests, the candidate now has forced transitions from Manual, Ask_StartAC, AutocontrolInit, and NormalAutocontrol to PumpFault on PumpFault, preserving PumpFault.enter actions that set pump_fault, activate alarm/display/sound, and release software_control. This directly satisfies the NormalAutocontrol fault, Ask_StartAC fault, and AutocontrolInit fault-preemption obligations."}`
  - SL-10 evidence 4: `{"summary": "For the backManual requests, the candidate now has forced CA_backManual, CB_backManual, CP_backManual, and CC_backManual transitions from Ask_StartAC, AutocontrolInit, NormalAutocontrol, and PumpFault to Manual. Manual.enter remains the shared recovery action that sets CA_mode to Manual, releases software control, and clears alarm/display/sound, matching the NL shared Manual recovery target."}`
  - SL-10 evidence 5: `{"summary": "The DSL diff is narrowly scoped to forced fallback repair. It removes only the five ambiguous wildcard forced declarations and replaces them with explicit forced transitions; it does not remove the root initial transition, MCA initial transition, StartAC path, ChangeSetpoint effect, TerminateAC transition, FaultRemoved transition, sensor-buffer during-before action, no-pump-fault guard, inverse pressure-to-flow computation, logging, manual default flow, or pump-control-voltage behavior."}`
- SL-10 rework_instructions：SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 17, "n_scenarios_passed": 12, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init probe: the first empty cycle dispatches CARA into Manual, stores the blood pressure reading in the shared buffer, and applies manual default flow.", "name": "default_init_enters_manual_and_stores_sensor", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "act...<truncated 21374 chars>
    - local evidence 2: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 20, "old": 25}
    - local evidence 3: `missing_required_grounding` {"element_ids": ["transition:InitialRootToMCA", "transition:InitialMCAToManual", "transition:ManualToAskStartAC", "transition:AskStartACChangeSetpoint", "transition:AskStartACToAutocontrolInit", "transition:NormalAutocontrolToManual", "event:PumpFault", "transition:ForcedPumpFault", "transition:PumpFaultToManual", "event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:BackManualFallbacks", "action:StoreSensorBuffer", "guard:NoPumpFault"], "kind": ...<truncated 29 chars>

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-a1b0c413df1` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-a1b0c413df1` | accept=5, reject=0 | `sl10_review` | `sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6` | The smallest safe edit is to keep all grounded states, variables, lifecycle actions, and local user-action events intact while changing only the scope of the hierarchy-wide forced fallback events., The NL describes PumpFault and backManual as cross-component or wildcard recovery signals, so parent-scoped forced transitions are more faithful than descendant-local events., Manual.enter remains the shared recovery action for CA_mode = Manual and software-control release; PumpFault.enter remains the alarm and release-control action. |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-a1b0c413df1` | accept=5, reject=0 | `sl9_rework` | `sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale. |
| 4 | `0` | `sl9_rework_decision` | `fixbatch-0-sha256-a1b0c413df1` | accept=5, reject=0 | `sl10_review` | `sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6` | The only DSL edits are the five wildcard forced fallback event scopes inside Mode_Control_Algorithm., PumpFault and the backManual events are NL-grounded shared fallback signals, so parent-scoped `: EventName` is more faithful than descendant-local `:: EventName` for wildcard forced transitions., All required states, variables, initial transitions, caregiver events, setpoint-change behavior, StartAC transition, TerminateAC transition, sensor-buffer storage, and no-pump-fault guard are preserved., ... +2 |
| 5 | `0` | `sl10_rework_review` | `fixbatch-0-sha256-a1b0c413df1` | accept=5, reject=0 | `sc11_accept_then_sd2` | `sha256:cfccb494cc5d81479d0021d37c8760ab2e39c5b9a2c8fd55f566c2429592efe6` | grounding_update_hint:sha256:9e53cf77956bf9fee8d0e2b632c860dddb78fe35a4f8690ff57ea4107690eaac |
| 6 | `1` | `request_batch` | `fixbatch-1-sha256-2da44f9b7eb` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 7 | `1` | `sl9_decision` | `fixbatch-1-sha256-2da44f9b7eb` | accept=5, reject=0 | `sl10_review` | `sha256:efc845a5b1371135ba5528d0a1b3442eda6a8a09f716ea5720af8e110a3f898c` | New iteration-1 evidence shows the parent-scoped forced events are still ignored in hot-start simulation., pyfcstm supports wildcard forced transitions with local `:: EventName`; this is also consistent with local NL event injection from the active source state., The repair changes only the five forced fallback event scopes and preserves all required states, variables, initial transitions, caregiver events, setpoint change, StartAC, TerminateAC, sensor-buffer storage, and the no-pump-fault guard. |
| 8 | `1` | `sl10_review` | `fixbatch-1-sha256-2da44f9b7eb` | accept=5, reject=0 | `sl9_rework` | `sha256:efc845a5b1371135ba5528d0a1b3442eda6a8a09f716ea5720af8e110a3f898c` | Do not continue oscillating only between wildcard `! * -> ... : EventName` and `! * -> ... :: EventName`. Replace or supplement the wildcard forced fallbacks with explicit forced transitions from the concrete Mode_Control_Algorithm substates exercised by the scenarios., Add explicit forced PumpFault transitions that preempt normal behavior from at least `Manual`, `Ask_StartAC`, `AutocontrolInit`, and `NormalAutocontrol` to `PumpFault`, using the event spelling that matches ordinary local event injection for each concrete source state. Preserve `PumpFault.enter` actions: `pump_fault = 1`, `alarm_active = 1`, `error_display = 1`, `error_sound = 1`, and `software_control = 0`., Add explicit forced Manual fallback transitions for each of `CA_backManual`, `CB_backManual`, `CP_backManual`, and `CC_backManual` from at least `Ask_StartAC`, `AutocontrolInit`, `NormalAutocontrol`, and `PumpFault` to `Manual`, so hot-start fallback probes from those states enter Manual. Preserve `Manual.enter` actions that set `CA_mode = 0`, release software control, and clear alarm/display/sound., ... +5 |
| 9 | `1` | `sl9_rework_decision` | `fixbatch-1-sha256-2da44f9b7eb` | accept=5, reject=0 | `sl10_review` | `sha256:e1ff3f5f090623aa5f8c4329998a23720070de1409c95ee107a8082c5d4e6fa4` | The prior ledger shows oscillation between wildcard parent-scoped and wildcard local-scoped forced events; SL-10 explicitly instructed not to continue that pattern., The smallest coherent repair is to preserve the existing grounded wildcard fallbacks and supplement them with explicit forced local-event transitions from the concrete substates exercised by the failing scenarios., Forced transitions from AutocontrolInit ensure PumpFault preempts the bare automatic transition to NormalAutocontrol., ... +2 |
| 10 | `1` | `sl10_rework_review` | `fixbatch-1-sha256-2da44f9b7eb` | accept=5, reject=0 | `sl9_rework` | `sha256:e1ff3f5f090623aa5f8c4329998a23720070de1409c95ee107a8082c5d4e6fa4` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale., grounding_update_hint:sha256:95b28dd8a7f00b0f8a83c08e1d1648706367b905e2af0e6ec1661fdcf3bfea0e, grounding_update_hint:sha256:27d40d585e348a16d418cffe733ced2f0f2dd7640702eaa1b2c5621b1aebcc50 |
| 11 | `1` | `sl9_rework_decision` | `fixbatch-1-sha256-2da44f9b7eb` | accept=5, reject=0 | `sl10_review` | `sha256:6d4bb7419815c153702b11a4636c6778b5a8c4ed91667afd80e5a70a84fee920` | The prior ledger shows oscillation between wildcard parent-scoped and wildcard local-scoped forced events; the repair stops that oscillation by replacing the wildcard fallbacks with explicit forced transitions from concrete substates., Explicit forced PumpFault transitions from Manual, Ask_StartAC, AutocontrolInit, and NormalAutocontrol preserve the NL-grounded fault fallback and ensure AutocontrolInit fault handling preempts the bare normal-progress transition., Explicit forced backManual transitions from Ask_StartAC, AutocontrolInit, NormalAutocontrol, and PumpFault preserve the cross-component Manual recovery target for CA_backManual, CB_backManual, CP_backManual, and CC_backManual., ... +2 |
| 12 | `1` | `sl10_rework_review` | `fixbatch-1-sha256-2da44f9b7eb` | accept=5, reject=0 | `sl9_rework` | `sha256:6d4bb7419815c153702b11a4636c6778b5a8c4ed91667afd80e5a70a84fee920` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale. |
| 13 | `1` | `sl9_rework_decision` | `fixbatch-1-sha256-2da44f9b7eb` | accept=5, reject=0 | `sl10_review` | `sha256:8de94e7b0e2b8a7b81b113a4d2c69652e1c6db9cd6daa44ea05152fdf3be98ae` | All five hard requests are accepted because SL-10 marked the requests rework-locked and the evidence shows the existing parent-scoped wildcard fallbacks are ignored in hot-start simulation., The repair stops the prior oscillation between wildcard `:` and wildcard `::` event scopes by replacing the ambiguous wildcard fallbacks with explicit forced local-event transitions from the concrete substates exercised by the scenarios., The explicit AutocontrolInit-to-PumpFault forced transition is placed before the bare AutocontrolInit-to-NormalAutocontrol transition, so a PumpFault event preempts normal progress., ... +4 |
| 14 | `1` | `sl10_rework_review` | `fixbatch-1-sha256-2da44f9b7eb` | accept=5, reject=0 | `exit_rejected_rework_budget_exhausted` | `sha256:8de94e7b0e2b8a7b81b113a4d2c69652e1c6db9cd6daa44ea05152fdf3be98ae` | SL-10 pass was downgraded because local deterministic evidence reported major drift and SL-10 evidence did not explicitly address the local rejection reason/kind with a structured local_override_rationale. |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 7174, 'model': 'gpt-5.5', 'prompt_tokens': 6195, 'total_tokens': 13369}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4765, 'model': 'gpt-5.5', 'prompt_tokens': 14329, 'total_tokens': 19094}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3973, 'model': 'gpt-5.5', 'prompt_tokens': 17189, 'total_tokens': 21162}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4211, 'model': 'gpt-5.5', 'prompt_tokens': 17899, 'total_tokens': 22110}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2508, 'model': 'gpt-5.5', 'prompt_tokens': 21369, 'total_tokens': 23877}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1795, 'model': 'gpt-5.5', 'prompt_tokens': 10774, 'total_tokens': 12569}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1975, 'model': 'gpt-5.5', 'prompt_tokens': 16783, 'total_tokens': 18758}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1788, 'model': 'gpt-5.5', 'prompt_tokens': 13729, 'total_tokens': 15517}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4588, 'model': 'gpt-5.5', 'prompt_tokens': 18485, 'total_tokens': 23073}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 5358, 'model': 'gpt-5.5', 'prompt_tokens': 19027, 'total_tokens': 24385}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2267, 'model': 'gpt-5.5', 'prompt_tokens': 20049, 'total_tokens': 22316}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1983, 'model': 'gpt-5.5', 'prompt_tokens': 17204, 'total_tokens': 19187}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2318, 'model': 'gpt-5.5', 'prompt_tokens': 24122, 'total_tokens': 26440}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`1`，schema_ok=`True`，usage=`{'completion_tokens': 1383, 'model': 'gpt-5.5', 'prompt_tokens': 21379, 'total_tokens': 22762}`，attempts=`2`。
  - attempt 0: error_kind=`provider_error`，model=`gpt-5.5`。
  - attempt 1: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2865, 'model': 'gpt-5.5', 'prompt_tokens': 26227, 'total_tokens': 29092}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2578, 'model': 'gpt-5.5', 'prompt_tokens': 22056, 'total_tokens': 24634}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2954, 'model': 'gpt-5.5', 'prompt_tokens': 26763, 'total_tokens': 29717}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`1`，schema_ok=`True`，usage=`{'completion_tokens': 1942, 'model': 'gpt-5.5', 'prompt_tokens': 22236, 'total_tokens': 24178}`，attempts=`2`。
  - attempt 0: error_kind=`provider_error`，model=`gpt-5.5`。
  - attempt 1: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`not_converged`，record_status=`rejected`。
- 主要原因分类：`repair_review_rework_budget`。
- required stages executed：`40/16`，missing=`SL-7`。
- repairs：`1/6` accepted；scenario_history=`6`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
