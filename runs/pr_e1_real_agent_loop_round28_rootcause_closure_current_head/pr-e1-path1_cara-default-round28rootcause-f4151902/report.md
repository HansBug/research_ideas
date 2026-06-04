## path1 / cara-infusion-pump-formal-spec__01 / default 真实运行结果：Path1 CARA representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`success`；record_status：`success`；result_status：`converged`。
- main_result_eligible：`true`。
- 一句话结论：`success`；停止原因：full_pass_all_required_feedback_ok。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `cara-infusion-pump-formal-spec__01` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `132721b4da597071d7874597e3293f003cd8f890` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:993dd2a89560dc22cd287bbf50c2cbe6faab9e99a63729d53f02e0d42085b247` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-round28rootcause-f4151902` |
| final verdict/status | verdict=`success`, record=`success`, result=`converged` |
| main_result_eligible | `true` |
| final.fcstm 来源 | `{"accepted": true, "accepted_after_rework": false, "final_dsl_hash": "sha256:73e3d8d47f98f98c17918558f31366c1bbc17ff11223e44cef11c6bded7def51", "iteration": 2, "matching_repair_history_indices": [2], "repair_history_index": 2, "selected_source_stage": "SL-7", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, full_pass_all_required_feedback_ok` |
| token/cost/time | tokens=`{'prompt_tokens': 408024, 'completion_tokens': 52325, 'total_tokens': 460349, 'estimated_prompt_tokens': 442654, 'estimated_completion_tokens': 42931, 'estimated_total_tokens': 485585, 'prompt_chars': 1770596, 'completion_chars': 171705, 'n_calls': 15, 'token_usage_available': True, 'token_usage_unavailable_calls': 0}`, elapsed=`996.721s` |
| run record | [`pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
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
def int CA_mode = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_complication = 0;
def float blood_pressure = 0.0;
def float shared_bp_buffer = 0.0;
def float target_bp = 120.0;
def float requested_target_bp = 120.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float pump_speed = 0.0;
def float builtin_switch_speed = 0.0;
def float control_voltage = 0.0;
def float log_flow_rate = 0.0;

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
            }
            during {
                shared_bp_buffer = blood_pressure;
                pump_speed = builtin_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                shared_bp_buffer = blood_pressure;
                pump_speed = builtin_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
            }
            during {
                shared_bp_buffer = blood_pressure;
            }
        }

        state AutocontrolNormal {
            during {
                shared_bp_buffer = blood_pressure;
                if [blood_pressure > target_bp] {
                    flow_rate = default_flow_rate - 1.0;
                } else if [blood_pressure < target_bp] {
                    flow_rate = default_flow_rate + 1.0;
                } else {
                    flow_rate = default_flow_rate;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_flow_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_complication = 1; };
        AutocontrolNormal -> PumpFault : if [pump_complication > 0];
        PumpFault -> Manual :: FaultRemoved effect { alarm_signal = 0; pump_complication = 0; };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=13201 | 生成初始 DSL 与 grounding seeds | initial len=2798 | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=2, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=123067 | LLM per-request accept/reject + repair | candidate len=2966,2966,2911 | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=124028 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=6, tokens=151001 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=6, tokens=151001 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=6, tokens=151001 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=123067 | LLM per-request accept/reject + repair | candidate len=2966,2966,2911 | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=124028 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=6, tokens=151001 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=6, tokens=151001 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=2, tokens=49052 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=3, tokens=123067 | LLM per-request accept/reject + repair | candidate len=2966,2966,2911 | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=3, tokens=124028 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1; blocking=0, advisory=20, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=6, tokens=151001 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=2, tokens=49052 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-round28rootcause-f4151902.agent_loop.json.gz) |

### 4.1 完整流程日志（stage/control-flow replay ledger）

口径：本节来自 `AgentLoopRunRecord.logs`，与 [`flow_log.json`](./flow_log.json) 一致；用于复现每个 stage 如何进入、得到什么批示、跳转到哪里，以及每次 DSL 产物/候选如何变化。

| # | ts | stage | iter | event | result / jump | DSL evidence |
|---:|---|---|---:|---|---|---|
| 1 | `2026-06-04T06:58:43Z` | `SC-0` | `-` | `run_start` | {} | <none> |
| 2 | `2026-06-04T06:58:43Z` | `SL-1` | `-` | `stage_enter` | {"reason": "initial_modeling_adapter_available"} | <none> |
| 3 | `2026-06-04T07:00:47Z` | `SL-1` | `-` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 4 | `2026-06-04T07:00:47Z` | `SL-1` | `-` | `stage_result` | {"jump": "SD-2", "ok": true} | candidate_dsl:len=2798,hash=sha256:b0d86cbe73bc |
| 5 | `2026-06-04T07:00:47Z` | `<control>` | `0` | `iteration_enter` | {} | current_hash=sha256:b0d86cbe73bc1b1f5b33d844568a0a60e02152bdcf7edce4b55688391c7f820d |
| 6 | `2026-06-04T07:00:47Z` | `<control>` | `0` | `iteration_validation_enter` | {} | dsl:len=2798,hash=sha256:b0d86cbe73bc, current_hash=sha256:b0d86cbe73bc1b1f5b33d844568a0a60e02152bdcf7edce4b55688391c7f820d |
| 7 | `2026-06-04T07:00:47Z` | `SD-2` | `0` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 8 | `2026-06-04T07:00:47Z` | `SD-2` | `0` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 9 | `2026-06-04T07:00:47Z` | `SD-3` | `0` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 10 | `2026-06-04T07:00:47Z` | `SD-3` | `0` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 11 | `2026-06-04T07:00:47Z` | `SD-4` | `0` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 12 | `2026-06-04T07:00:47Z` | `SD-4` | `0` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 13 | `2026-06-04T07:00:47Z` | `<control>` | `0` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=pump_complication", "W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault"], "diagnostic_codes": ["W_UNWRITTEN_READ_VAR", "W_GUARD_VARS_NEVER_CHANGE", "W_HIGH_VAR_TO_LEAF_RATIO", "W_UNREFERENCED_VAR", "W_UNREFERENCED_VAR", ...<truncated 997 chars> | <none> |
| 14 | `2026-06-04T07:00:47Z` | `SD-8` | `0` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "blocking_instance_keys": ["W_UNWRITTEN_READ_VAR:var_name=pump_complication", "W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault"], "diagnostic_codes": ["W_UNWRITTEN_READ_VAR", "W_GUARD_VARS_NEVER_CHANGE", "W_HIGH_VAR_TO_LEAF_RATIO", "W_UNREFERENCED_VAR", "W_UNREFERENCED_VAR", "W_UNRE...<truncated 5139 chars> | current_dsl:len=2798,hash=sha256:b0d86cbe73bc |
| 15 | `2026-06-04T07:00:47Z` | `SD-8` | `0` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 16 | `2026-06-04T07:00:47Z` | `SD-8` | `0` | `fix_request_batch` | {"request_count": 2} | <none> |
| 17 | `2026-06-04T07:00:47Z` | `SL-9` | `0` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2798,hash=sha256:b0d86cbe73bc |
| 18 | `2026-06-04T07:01:20Z` | `SL-9` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 19 | `2026-06-04T07:01:20Z` | `SL-9` | `0` | `stage_result` | {"accepted_request_ids": ["fixreq-0-sd4-0-a6f1595e9f", "fixreq-0-sd4-1-8e1eb9dac6"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2966,hash=sha256:249d10e52de0 |
| 20 | `2026-06-04T07:01:20Z` | `SD-10` | `0` | `stage_result` | {"jump": "SL-10", "ok": true, "status": "StageStatus.OK"} | <none> |
| 21 | `2026-06-04T07:01:20Z` | `SL-10` | `0` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:249d10e52de0915268b7f3599a1abc4366220347d8e593644538348853f2bbe9 |
| 22 | `2026-06-04T07:01:35Z` | `SL-10` | `0` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 23 | `2026-06-04T07:01:35Z` | `SL-10` | `0` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 24 | `2026-06-04T07:01:35Z` | `SL-10` | `0` | `grounding_update_hints_recorded` | {} | <none> |
| 25 | `2026-06-04T07:01:35Z` | `SC-11` | `0` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2966,hash=sha256:249d10e52de0 |
| 26 | `2026-06-04T07:01:35Z` | `<control>` | `0` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:249d10e52de0915268b7f3599a1abc4366220347d8e593644538348853f2bbe9 |
| 27 | `2026-06-04T07:01:35Z` | `<control>` | `1` | `iteration_enter` | {} | current_hash=sha256:249d10e52de0915268b7f3599a1abc4366220347d8e593644538348853f2bbe9 |
| 28 | `2026-06-04T07:01:35Z` | `<control>` | `1` | `iteration_validation_enter` | {} | dsl:len=2966,hash=sha256:249d10e52de0, current_hash=sha256:249d10e52de0915268b7f3599a1abc4366220347d8e593644538348853f2bbe9 |
| 29 | `2026-06-04T07:01:35Z` | `SD-2` | `1` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 30 | `2026-06-04T07:01:35Z` | `SD-2` | `1` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 31 | `2026-06-04T07:01:35Z` | `SD-3` | `1` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 32 | `2026-06-04T07:01:35Z` | `SD-3` | `1` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 33 | `2026-06-04T07:01:35Z` | `SD-4` | `1` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 34 | `2026-06-04T07:01:35Z` | `SD-4` | `1` | `stage_result` | {"jump": "SL-5", "ok": true, "status": "StageStatus.OK"} | <none> |
| 35 | `2026-06-04T07:01:35Z` | `SL-5` | `1` | `stage_enter` | {"reason": "scenario_set_absent"} | <none> |
| 36 | `2026-06-04T07:03:20Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 37 | `2026-06-04T07:03:20Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 38 | `2026-06-04T07:03:20Z` | `SL-5` | `1` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 39 | `2026-06-04T07:04:53Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 40 | `2026-06-04T07:04:54Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 41 | `2026-06-04T07:04:54Z` | `SL-5` | `1` | `stage_enter` | {"reason": "scenario_coverage_gap_retry"} | <none> |
| 42 | `2026-06-04T07:06:34Z` | `SL-5` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 43 | `2026-06-04T07:06:35Z` | `SD-5A` | `1` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 44 | `2026-06-04T07:06:35Z` | `<control>` | `1` | `scenario_coverage_retry_exhausted` | {} | <none> |
| 45 | `2026-06-04T07:06:35Z` | `SC-5F` | `1` | `stage_result` | {"jump": "SD-6", "ok": true} | <none> |
| 46 | `2026-06-04T07:06:35Z` | `SD-6` | `1` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
| 47 | `2026-06-04T07:06:35Z` | `SD-6` | `1` | `stage_result` | {"jump": "SD-8", "ok": false, "status": "StageStatus.FAIL"} | <none> |
| 48 | `2026-06-04T07:06:35Z` | `<control>` | `1` | `iteration_validation_result` | {"jump": "SD-8 repair", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 15, "n_scenarios_passed": 14, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | <none> |
| 49 | `2026-06-04T07:06:35Z` | `SD-8` | `1` | `repair_path_enter` | {"jump": "SD-8", "selected_feedback": {"blocking": true, "is_pre_scenario": false, "n_scenarios": 15, "n_scenarios_passed": 14, "ok": false, "oracle_weak": false, "pre_scenario": false, "setup_error": null, "source": "sim", "source_stage": "SD-6", "weak_oracle_evidence": {}, "weak_oracle_reason": ""}} | current_dsl:len=2966,hash=sha256:249d10e52de0 |
| 50 | `2026-06-04T07:06:35Z` | `SD-8` | `1` | `stage_result` | {"jump": "SL-9", "ok": true, "status": "StageStatus.OK"} | <none> |
| 51 | `2026-06-04T07:06:35Z` | `SD-8` | `1` | `fix_request_batch` | {"request_count": 1} | <none> |
| 52 | `2026-06-04T07:06:35Z` | `SL-9` | `1` | `stage_enter` | {"reason": "fix_requests_ready"} | old_dsl:len=2966,hash=sha256:249d10e52de0 |
| 53 | `2026-06-04T07:07:08Z` | `SL-9` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 54 | `2026-06-04T07:07:08Z` | `SL-9` | `1` | `stage_result` | {"accepted_request_ids": ["fixreq-1-sd6-0-1ec8de9706"], "jump": "SL-10", "ok": true, "rejected_request_ids": []} | candidate_dsl:len=2966,hash=sha256:4b981b2ad909 |
| 55 | `2026-06-04T07:07:08Z` | `SD-10` | `1` | `stage_result` | {"jump": "SL-10", "ok": true, "status": "StageStatus.OK"} | <none> |
| 56 | `2026-06-04T07:07:08Z` | `SL-10` | `1` | `stage_enter` | {"reason": "candidate_dsl_and_local_evidence_ready"} | candidate_hash=sha256:4b981b2ad909079cd44b68d8f31b06f97458d7d3a1852b6952f103bb7be3b583 |
| 57 | `2026-06-04T07:07:22Z` | `SL-10` | `1` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 58 | `2026-06-04T07:07:22Z` | `SL-10` | `1` | `stage_result` | {"decision": "pass", "jump": "SC-11", "ok": true} | <none> |
| 59 | `2026-06-04T07:07:22Z` | `SL-10` | `1` | `grounding_update_hints_recorded` | {} | <none> |
| 60 | `2026-06-04T07:07:22Z` | `SC-11` | `1` | `stage_result` | {"jump": "SD-2 next iteration", "ok": true, "reason": "SL-10 accepted candidate; next iteration must restart at SD-2"} | candidate_dsl:len=2966,hash=sha256:4b981b2ad909 |
| 61 | `2026-06-04T07:07:22Z` | `<control>` | `1` | `iteration_repair_result` | {"accepted": true, "jump": "SD-2 next iteration"} | current_hash=sha256:4b981b2ad909079cd44b68d8f31b06f97458d7d3a1852b6952f103bb7be3b583 |
| 62 | `2026-06-04T07:07:22Z` | `<control>` | `2` | `iteration_enter` | {} | current_hash=sha256:4b981b2ad909079cd44b68d8f31b06f97458d7d3a1852b6952f103bb7be3b583 |
| 63 | `2026-06-04T07:07:22Z` | `<control>` | `2` | `iteration_validation_enter` | {} | dsl:len=2966,hash=sha256:4b981b2ad909, current_hash=sha256:4b981b2ad909079cd44b68d8f31b06f97458d7d3a1852b6952f103bb7be3b583 |
| 64 | `2026-06-04T07:07:22Z` | `SD-2` | `2` | `stage_enter` | {"reason": "full_validation_pass"} | <none> |
| 65 | `2026-06-04T07:07:22Z` | `SD-2` | `2` | `stage_result` | {"jump": "SD-3", "ok": true, "status": "StageStatus.OK"} | <none> |
| 66 | `2026-06-04T07:07:22Z` | `SD-3` | `2` | `stage_enter` | {"reason": "SD-2 ok"} | <none> |
| 67 | `2026-06-04T07:07:22Z` | `SD-3` | `2` | `stage_result` | {"jump": "SD-4", "ok": true, "status": "StageStatus.OK"} | <none> |
| 68 | `2026-06-04T07:07:22Z` | `SD-4` | `2` | `stage_enter` | {"reason": "SD-3 ok"} | <none> |
| 69 | `2026-06-04T07:07:22Z` | `SD-4` | `2` | `stage_result` | {"jump": "SD-5A", "ok": true, "status": "StageStatus.OK"} | <none> |
| 70 | `2026-06-04T07:07:22Z` | `SD-5A` | `2` | `stage_result` | {"jump": "SL-5 targeted_retry", "ok": false, "reason": "reuse_frozen_scenario_set"} | <none> |
| 71 | `2026-06-04T07:07:22Z` | `<control>` | `2` | `frozen_scenario_refresh_targeted_retry` | {} | <none> |
| 72 | `2026-06-04T07:07:22Z` | `SL-5` | `2` | `stage_enter` | {"reason": "targeted_refresh_after_frozen_gap_or_dsl_change"} | <none> |
| 73 | `2026-06-04T07:09:20Z` | `SL-5` | `2` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 74 | `2026-06-04T07:09:21Z` | `SD-5A` | `2` | `stage_result` | {"jump": "SL-5 retry", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 75 | `2026-06-04T07:09:21Z` | `SL-5` | `2` | `stage_enter` | {"reason": "targeted_refresh_after_frozen_gap_or_dsl_change"} | <none> |
| 76 | `2026-06-04T07:10:58Z` | `SL-5` | `2` | `llm_stage_result` | {"ok": true, "status": "StageStatus.OK"} | <none> |
| 77 | `2026-06-04T07:10:58Z` | `SD-5A` | `2` | `stage_result` | {"jump": "SC-5F weak_oracle", "ok": false, "status": "StageStatus.ADVISORY"} | <none> |
| 78 | `2026-06-04T07:10:58Z` | `<control>` | `2` | `scenario_refresh_retry_exhausted` | {} | <none> |
| 79 | `2026-06-04T07:10:58Z` | `SC-5F` | `2` | `stage_result` | {"jump": "SD-6", "ok": true, "reason": "refreshed_scenario_set"} | <none> |
| 80 | `2026-06-04T07:10:58Z` | `SD-6` | `2` | `stage_enter` | {"reason": "scenario_set_ready"} | <none> |
- ……另有 `42` 条流程日志见 [`flow_log.json`](./flow_log.json) / run record。

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-4` | yes | fixbatch-0-sha256-9c85cb95fd1 / n=2 | accept=2, reject=0, waiver=0 | ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-6` | yes | fixbatch-1-sha256-019672ca0f5 / n=1 | accept=1, reject=0, waiver=0 | ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SL-7` | yes | fixbatch-2-sha256-79bee9e51cb / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=minor, local_stage=SD-10, reason=scenario_regression | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `<none>` | no | <none> | <none> | <none> | <none> | no | full_pass_all_required_feedback_ok |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 2 | Iter 3 | Iter 4 |
|---|---|---|---|---|
| `default_init_manual_operation_outputs` | default-init dispatches to Manual and verifies manual-mode shared buffer, built-in-switch pump speed, and default flow-r...<truncated 13 chars> | ✅ | ✅ | ✅ |
| `manual_initiate_change_start_to_normal_low_pressure` | explicit-hot-start from Manual covers InitiateAC, ChangeSetpoint, StartAC, AutocontrolInit, and low-pressure normal auto...<truncated 24 chars> | ⚪ | ⚪ | ✅ |
| `autocontrol_high_pressure_lower_flow` | explicit-hot-start from AutocontrolNormal verifies higher blood pressure than target produces a lower flow rate and logs...<truncated 4 chars> | ⚪ | ⚪ | ✅ |
| `terminate_from_pre_normal_autocontrol_states` | explicit-hot-start from Ask_StartAC verifies TerminateAC returns to Manual, then re-enters AutocontrolInit and verifies ...<truncated 54 chars> | ⚪ | ⚪ | ✅ |
| `terminate_from_autocontrolnormal_to_manual` | explicit-hot-start from AutocontrolNormal verifies caregiver termination releases software control and restores Manual o...<truncated 9 chars> | ✅ | ✅ | ✅ |
| `pump_fault_event_alarm_release_and_removed` | explicit-hot-start from AutocontrolNormal verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved clear...<truncated 35 chars> | ✅ | ✅ | ✅ |
| `pump_complication_guard_boundary` | explicit-hot-start from AutocontrolNormal probes the complication guard boundary: zero complication stays normal, positi...<truncated 33 chars> | ⚪ | ⚪ | ✅ |
| `forced_backmanual_fallbacks_from_distinct_leaves` | explicit-hot-start from Ask_StartAC exercises CA/CB/CP/CC backManual forced fallbacks from distinct leaves, including pr...<truncated 40 chars> | ⚪ | ⚪ | ✅ |
| `manual_initiate_start_to_normal_low_pressure` |  | ✅ | ✅ | ⚪ |
| `ask_change_setpoint_then_high_pressure_flow` |  | ✅ | ✅ | ⚪ |
| `terminate_from_ask_startac_to_manual` |  | ✅ | ✅ | ⚪ |
| `terminate_from_autocontrolinit_to_manual` |  | ❌ | ✅ | ⚪ |
| `no_fault_no_complication_stays_normal` |  | ✅ | ✅ | ⚪ |
| `pump_complication_guard_enters_pumpfault` |  | ✅ | ✅ | ⚪ |
| `backmanual_fallback_from_ask_and_init` |  | ✅ | ✅ | ⚪ |
| `cp_backmanual_fallback_from_normal` |  | ✅ | ✅ | ⚪ |
| `cc_backmanual_fallback_from_pumpfault` |  | ✅ | ✅ | ⚪ |
| `change_setpoint_effect_value_probe` |  | ✅ | ✅ | ⚪ |
| `pump_fault_detected_effect_value_probe` |  | ✅ | ✅ | ⚪ |
| `fault_removed_effect_value_probe` |  | ✅ | ✅ | ⚪ |
| `start_ac_control_flags_value_probe` |  | ⚪ | ✅ | ⚪ |
| `forced_backmanual_dirty_flags_value_probe` |  | ⚪ | ✅ | ⚪ |
| `change_setpoint_effect_drives_later_flow_probe` |  | ⚪ | ✅ | ⚪ |
| `pump_fault_detected_exact_effect_from_dirty_value_probe` |  | ⚪ | ✅ | ⚪ |

#### 6.2 Scenario definitions

<details><summary>`default_init_manual_operation_outputs` — default-init dispatches to Manual and verifies manual-mode shared buffer, built-in-switch pump speed, and default flow-rate behavior.</summary>

| Field | Value |
|---|---|
| description | default-init dispatches to Manual and verifies manual-mode shared buffer, built-in-switch pump speed, and default flow-rate behavior. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 90.0, "builtin_switch_speed": 2.5, "default_flow_rate": 5.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initial_dispatch_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 5.0, "pump_speed": 2.5, "shared_bp_buffer": 90.0, "software_control": 0}` |

</details>

<details><summary>`manual_initiate_change_start_to_normal_low_pressure` — explicit-hot-start from Manual covers InitiateAC, ChangeSetpoint, StartAC, AutocontrolInit, and low-pressure normal autocontrol increasing flow.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from Manual covers InitiateAC, ChangeSetpoint, StartAC, AutocontrolInit, and low-pressure normal autocontrol increasing flow. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"blood_pressure": 100.0, "builtin_switch_speed": 1.5, "default_flow_rate": 5.0, "requested_target_bp": 120.0, "target_bp": 110.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiate_enters_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"flow_rate": 5.0, "pump_speed": 1.5, "shared_bp_buffer": 100.0}` |
| 1 `change_setpoint_self_transition` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"flow_rate": 5.0, "pump_speed": 1.5, "shared_bp_buffer": 100.0, "target_bp": 120.0}` |
| 2 `start_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "shared_bp_buffer": 100.0, "software_control": 1, "target_bp": 120.0}` |
| 3 `init_completes_to_normal_low_pressure_flow` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 6.0, "flow_rate": 6.0, "log_flow_rate": 6.0, "pump_speed": 6.0, "shared_bp_buffer": 100.0}` |

</details>

<details><summary>`autocontrol_high_pressure_lower_flow` — explicit-hot-start from AutocontrolNormal verifies higher blood pressure than target produces a lower flow rate and logs it.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from AutocontrolNormal verifies higher blood pressure than target produces a lower flow rate and logs it. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 140.0, "default_flow_rate": 5.0, "pump_complication": 0, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `high_pressure_selects_lower_flow_branch` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 4.0, "flow_rate": 4.0, "log_flow_rate": 4.0, "pump_complication": 0, "pump_speed": 4.0, "shared_bp_buffer": 140.0}` |

</details>

<details><summary>`terminate_from_pre_normal_autocontrol_states` — explicit-hot-start from Ask_StartAC verifies TerminateAC returns to Manual, then re-enters AutocontrolInit and verifies TerminateAC overrides the init-to-normal...<truncated 14 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from Ask_StartAC verifies TerminateAC returns to Manual, then re-enters AutocontrolInit and verifies TerminateAC overrides the init-to-normal continuation. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 118.0, "builtin_switch_speed": 3.0, "default_flow_rate": 4.5, "software_control": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_ask_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 4.5, "pump_speed": 3.0, "shared_bp_buffer": 118.0, "software_control": 0}` |
| 1 `reenter_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"flow_rate": 4.5, "pump_speed": 3.0, "shared_bp_buffer": 118.0}` |
| 2 `start_to_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "shared_bp_buffer": 118.0, "software_control": 1}` |
| 3 `terminate_init_to_manual_before_normal` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 4.5, "pump_speed": 3.0, "shared_bp_buffer": 118.0, "software_control": 0}` |

</details>

<details><summary>`terminate_from_autocontrolnormal_to_manual` — explicit-hot-start from AutocontrolNormal verifies caregiver termination releases software control and restores Manual operation.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from AutocontrolNormal verifies caregiver termination releases software control and restores Manual operation. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 120.0, "builtin_switch_speed": 3.5, "default_flow_rate": 5.0, "pump_complication": 0, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_normal_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.TerminateAC"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "flow_rate": 5.0, "pump_speed": 3.5, "shared_bp_buffer": 120.0, "software_control": 0}` |

</details>

<details><summary>`pump_fault_event_alarm_release_and_removed` — explicit-hot-start from AutocontrolNormal verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved clears the fault before Manual recovery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from AutocontrolNormal verifies PumpFaultDetected enters PumpFault with alarms and FaultRemoved clears the fault before Manual recovery. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "blood_pressure": 125.0, "builtin_switch_speed": 2.8, "default_flow_rate": 5.0, "pump_complication": 0, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `fault_detected_enters_pumpfault` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolNormal.PumpFaultDetected"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "pump_complication": 1, "software_control": 0}` |
| 1 `fault_remains_observable_before_removal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "pump_complication": 1, "software_control": 0}` |
| 2 `fault_removed_returns_manual_and_clears_fault` | `0` | `["CARA.Mode_Control_Algorithm.PumpFault.FaultRemoved"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 5.0, "pump_complication": 0, "pump_speed": 2.8, "shared_bp_buffer": 125.0, "software_control": 0}` |

</details>

<details><summary>`pump_complication_guard_boundary` — explicit-hot-start from AutocontrolNormal probes the complication guard boundary: zero complication stays normal, positive complication enters PumpFault.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from AutocontrolNormal probes the complication guard boundary: zero complication stays normal, positive complication enters PumpFault. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "blood_pressure": 120.0, "default_flow_rate": 5.0, "pump_complication": 0, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `zero_complication_no_fault_transition` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 5.0, "flow_rate": 5.0, "log_flow_rate": 5.0, "pump_complication": 0, "pump_speed": 5.0, "shared_bp_buffer": 120.0}` |

</details>

<details><summary>`forced_backmanual_fallbacks_from_distinct_leaves` — explicit-hot-start from Ask_StartAC exercises CA/CB/CP/CC backManual forced fallbacks from distinct leaves, including preserving fault flags until FaultRemoved.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start from Ask_StartAC exercises CA/CB/CP/CC backManual forced fallbacks from distinct leaves, including preserving fault flags until FaultRemoved. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "alarm_signal": 0, "blood_pressure": 116.0, "builtin_switch_speed": 2.1, "default_flow_rate": 4.0, "pump_complication": 0, "software_control": 1, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_from_ask` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 4.0, "pump_complication": 0, "pump_speed": 2.1, "shared_bp_buffer": 116.0, "software_control": 0}` |
| 1 `reenter_ask` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"flow_rate": 4.0, "pump_speed": 2.1, "shared_bp_buffer": 116.0}` |
| 2 `start_to_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "shared_bp_buffer": 116.0, "software_control": 1}` |
| 3 `ca_backmanual_from_init` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 4.0, "pump_complication": 0, "pump_speed": 2.1, "shared_bp_buffer": 116.0, "software_control": 0}` |
| 4 `reenter_normal` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"shared_bp_buffer": 116.0}` |
| 5 `start_again_to_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "software_control": 1}` |
| 6 `init_completes_to_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_voltage": 5.0, "flow_rate": 5.0, "log_flow_rate": 5.0, "pump_speed": 5.0, "shared_bp_buffer": 116.0}` |
| 7 `cp_backmanual_from_normal` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 0, "flow_rate": 4.0, "pump_complication": 0, "pump_speed": 2.1, "shared_bp_buffer": 116.0, "software_control": 0}` |
| 8 `reach_pumpfault_for_cc_probe` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"shared_bp_buffer": 116.0}` |
| 9 `start_for_fault_probe` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"CA_mode": 1, "alarm_signal": 0, "software_control": 1}` |
| 10 `normal_before_fault_probe` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"shared_bp_buffer": 116.0}` |
| 11 `fault_detected_before_cc_backmanual` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolNormal.PumpFaultDetected"]` | `CARA.Mode_Control_Algorithm.PumpFault` | `{"CA_mode": 0, "alarm_signal": 1, "pump_complication": 1, "software_control": 0}` |
| 12 `cc_backmanual_from_pumpfault_preserves_fault_until_removed` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"CA_mode": 0, "alarm_signal": 1, "flow_rate": 4.0, "pump_complication": 1, "pump_speed": 2.1, "shared_bp_buffer": 116.0, "software_control": 0}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=pump_complication, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, ... +3 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:249d10e52de0915268b7f3599a1abc4366220347d8e593644538348853f2bbe9` |
| 2 | `1` | ✅ | `SD-6` | terminate_from_autocontrolinit_to_manual | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=True, target=True, regression=False, drift=none, local_stage=SD-10, reason= | `sha256:4b981b2ad909079cd44b68d8f31b06f97458d7d3a1852b6952f103bb7be3b583` |
| 3 | `2` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=minor, local_stage=SD-10, reason=scenario_regression | `sha256:73e3d8d47f98f98c17918558f31366c1bbc17ff11223e44cef11c6bded7def51` |

<details><summary>Repair 1 / iteration `0` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'pump_complication' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=pump_complication, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT, I_TRANSITION_NEVER_EVENT_TRIGGERED`。
- before_dsl_hash：`sha256:b0d86cbe73bc1b1f5b33d844568a0a60e02152bdcf7edce4b55688391c7f820d`；candidate_dsl_hash：`sha256:249d10e52de0915268b7f3599a1abc4366220347d8e593644538348853f2bbe9`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=pump_complication` policy=`budgeted_repair`：Variable 'pump_complication' is read but never written by any action or transition effect.；refs=`{"init_value": "0", "read_states": ["CARA.Mode_Control_Algorithm.AutocontrolNormal"], "var_name": "pump_complication"}`
- 2. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.PumpFault` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "CARA.Mode_Control_Algorithm.AutocontrolNormal", "guard_vars": ["pump_complication"], "to_path": "CARA.Mode_Control_Algorithm.PumpFault"}`

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `CA_mode` | `unknown` | ✅ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `alarm_signal` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `blood_pressure` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `builtin_switch_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `control_voltage` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `default_flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `log_flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `pump_complication` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE` |
| `pump_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `requested_target_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `shared_bp_buffer` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `software_control` | `unknown` | ❌ | `W_UNREFERENCED_VAR, W_VARIABLE_WRITTEN_NEVER_READ_AND_NOT_NL_OUTPUT` |
| `target_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-9c85cb95fd1`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd4-0-a6f1595e9f` | `blocking_warning` | ❌ | ✅ | Variable 'pump_complication' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects. | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-1-8e1eb9dac6` | `blocking_warning` | ❌ | ✅ | Variable 'pump_complication' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects. | `W_GUARD_VARS_NEVER_CHANGE` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:software_control, variable:alarm_signal, variable:pump_complication, variable:blood_pressure, variable:shared_bp_buffer, ... +30`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2966`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd4-0-a6f1595e9f` | `accept` | ❌ | ❌ | The warning is valid: pump_complication is read by the AutocontrolNormal guard but was never written. A pump-operation complication is NL-grounded as a fault/occlusion occurrence, so the repair adds an event-triggered PumpFaultDetected transition that sets pump_complication to 1, and clears it when returning to Manual/fault removed.；intent=Add an NL-grounded...<truncated 118 chars> |
| `fixreq-0-sd4-1-8e1eb9dac6` | `accept` | ❌ | ❌ | The guard AutocontrolNormal -> PumpFault : if [pump_complication > 0] is preserved as required, but pump_complication now has meaningful NL-grounded writes so the guard is no longer controlled only by its initial value.；intent=Preserve the no-pump-operation-complications guard, Add meaningful state updates for the guard variable |
- repair_rationale：Addressed W_UNWRITTEN_READ_VAR by adding meaningful writes to pump_complication rather than a self-assignment.；Addressed W_GUARD_VARS_NEVER_CHANGE while preserving the required guard AutocontrolNormal -> PumpFault : if [pump_complication > 0].；The added PumpFaultDetected event is grounded in the NL pump fault/occlusion occurrence and does not invent continuous plant dynamics.；Manual recovery and FaultRemoved clear pump_complication, matching the NL caregiver removes the fault and manual operation is the shared recovery target.；All required states, variables, events, fallback transitions, and actions are preserved.
- diff_summary：`{"summary": "Added pump_complication = 0 to Manual.enter, added an AutocontrolNormal -> PumpFault :: PumpFaultDetected transition that sets pump_complication = 1, and added pump_complication = 0 effect on PumpFault -> Manual :: FaultRemoved while leaving the existing guard transition intact."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_complication = 0;
def float blood_pressure = 0.0;
def float shared_bp_buffer = 0.0;
def float target_bp = 120.0;
def float requested_target_bp = 120.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float pump_speed = 0.0;
def float builtin_switch_speed = 0.0;
def float control_voltage = 0.0;
def float log_flow_rate = 0.0;

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
                alarm_signal = 0;
                pump_complication = 0;
            }
            during {
                shared_bp_buffer = blood_pressure;
                pump_speed = builtin_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                shared_bp_buffer = blood_pressure;
                pump_speed = builtin_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
            }
            during {
                shared_bp_buffer = blood_pressure;
            }
        }

        state AutocontrolNormal {
            during {
                shared_bp_buffer = blood_pressure;
                if [blood_pressure > target_bp] {
                    flow_rate = default_flow_rate - 1.0;
                } else if [blood_pressure < target_bp] {
                    flow_rate = default_flow_rate + 1.0;
                } else {
                    flow_rate = default_flow_rate;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_flow_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolInit -> Manual : TerminateAC;
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_complication = 1; };
        AutocontrolNormal -> PumpFault : if [pump_complication > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_complication = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -29,6 +29,7 @@
                 CA_mode = 0;
                 software_control = 0;
                 alarm_signal = 0;
+                pump_complication = 0;
             }
             during {
                 shared_bp_buffer = blood_pressure;
@@ -87,7 +88,8 @@
         AutocontrolInit -> AutocontrolNormal;
         AutocontrolInit -> Manual : TerminateAC;
         AutocontrolNormal -> Manual : TerminateAC;
+        AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_complication = 1; };
         AutocontrolNormal -> PumpFault : if [pump_complication > 0];
-        PumpFault -> Manual :: FaultRemoved;
+        PumpFault -> Manual :: FaultRemoved effect { pump_complication = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:8a893901fcb5b7ed5cdb2a1cd8151afd74c0a5632f3f35d97a1a5a293ec43356`。
  - SL-10 evidence 1: `{"summary": "Both SL-9 accepted requests are addressed by the candidate: pump_complication is no longer only an initialized/read variable because Manual.enter clears it to 0, the added AutocontrolNormal -> PumpFault :: PumpFaultDetected transition sets it to 1, and PumpFault -> Manual :: FaultRemoved clears it to 0."}`
  - SL-10 evidence 2: `{"summary": "The repair is grounded in the NL requirement that pump faults such as fluid-tubing occlusion can occur, alarm signals activate, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. The new PumpFaultDetected event is a discrete representation of that fault occurrence, and FaultRemoved already appears as a required caregiver recovery event."}`
  - SL-10 evidence 3: `{"summary": "The required AutocontrolNormal -> PumpFault guard on pump_complication > 0 is preserved, satisfying the grounding that CARA controls flow rate only while there are no pump-operation complications. The guard variable now has meaningful writes, resolving the W_GUARD_VARS_NEVER_CHANGE and W_UNWRITTEN_READ_VAR requests without replacing the guard with a constant or deleting grounded behavior."}`
  - SL-10 evidence 4: `{"summary": "The diff is narrowly scoped: it only adds pump_complication reset/set effects and one NL-grounded fault-detection transition. Required states, variables, events, fallback transitions, manual/autocontrol behavior, Ask_StartAC behavior, flow-rate computation, logging, shared buffer updates, and alarm/release behavior are preserved."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic repair review reports ok=true, target_resolved=true, regression_detected=false, drift_risk=none, and no local rejection. This supports accepting the candidate for the next full top-down revalidation pass."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。

</details>

<details><summary>Repair 2 / iteration `1` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`terminate_from_autocontrolinit_to_manual`。
- before_dsl_hash：`sha256:249d10e52de0915268b7f3599a1abc4366220347d8e593644538348853f2bbe9`；candidate_dsl_hash：`sha256:4b981b2ad909079cd44b68d8f31b06f97458d7d3a1852b6952f103bb7be3b583`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-019672ca0f5`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-1ec8de9706` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start from AutocontrolInit verifies TerminateAC overrides continuing autocontrol and returns to Manual.', 'name': 'terminate_from_autocontrolinit_to_manual', 'repair_brief': {'actionable_rule': 'For each failing step, repair against expected_state/expected_vars versus actual_state/actual_vars_focus/runtime_error, and mention the scenario name in repair_rationale.', 'description': 'explicit-hot-start from AutocontrolInit verifies TerminateAC overrides continuing autocontrol and returns to Manual.', 'failing_steps': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars_focus': {'CA_mode': 1, 'alarm_signal': 0, 'flow_rate': 5.0, 'pump_complication': 0, 'pump_speed': 5.0, 'shared_bp_buffer': 119.0, 'software_control': 1}, 'before_cycles': 0, 'events': ['CARA.Mode_Control_Algorithm.TerminateAC'], 'expected_state': 'CARA.Mode_Control_Algorithm.Manual', 'expected_vars': {'CA_mode': 0, 'alarm_signal': 0, 'flow_rate': 4.0, 'pump_complication': 0, 'pump_speed': 2.2, 'shared_bp_buffer': 119.0, 'software_control': 0}, 'runtime_error': '', 'state_assertion_ok': False, 'step_index': 0, 'step_name': 'terminate_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 5.0, 'expected': 4.0}, 'pump_speed': {'actual': 5.0, 'expected': 2.2}, 'software_control': {'actual': 1, 'expected': 0}}}], 'initial_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'initial_vars': {'CA_mode': 1, 'blood_pressure': 119.0, 'builtin_switch_speed': 2.2, 'default_flow_rate': 4.0, 'software_control': 1}, 'scenario_name': 'terminate_from_autocontrolinit_to_manual', 'status': 'fail'}, 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'CA_mode': 1, 'alarm_signal': 0, 'blood_pressure': 119.0, 'builtin_switch_speed': 2.2, 'control_voltage': 5.0, 'default_flow_rate': 4.0, 'flow_rate': 5.0, 'log_flow_rate': 5.0, 'pump_complication': 0, 'pump_speed': 5.0, 'requested_target_bp': 120.0, 'shared_bp_buffer': 119.0, 'software_control': 1, 'target_bp': 120.0}, 'runtime_error': None, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'terminate_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': {'actual': 1, 'expected': 0}, 'flow_rate': {'actual': 5.0, 'expected': 4.0}, 'pump_speed': {'actual': 5.0, 'expected': 2.2}, 'software_control': {'actual': 1, 'expected': 0}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:software_control, variable:alarm_signal, variable:pump_complication, variable:blood_pressure, variable:shared_bp_buffer, ... +30`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2966`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-1ec8de9706` | `accept` | ❌ | ❌ | The failing scenario terminate_from_autocontrolinit_to_manual is valid. From explicit hot-start in AutocontrolInit with event CARA.Mode_Control_Algorithm.TerminateAC, expected_state is Manual with manual-mode variables, but actual_state was AutocontrolNormal because the unconditional AutocontrolInit -> AutocontrolNormal transition was listed before the Termi...<truncated 315 chars> |
- repair_rationale：For scenario terminate_from_autocontrolinit_to_manual, failing step terminate_init_to_manual starts in CARA.Mode_Control_Algorithm.AutocontrolInit and injects CARA.Mode_Control_Algorithm.TerminateAC. Expected_state is CARA.Mode_Control_Algo...<truncated 77 chars>；The expected_vars CA_mode=0, software_control=0, pump_speed=2.2, and flow_rate=4.0 are produced by entering Manual and running Manual.during. The actual_vars CA_mode=1, software_control=1, pump_speed=5.0, and flow_rate=5.0 came from falling...<truncated 71 chars>；The root cause is transition priority, not missing Manual behavior: the unconditional AutocontrolInit -> AutocontrolNormal transition preceded AutocontrolInit -> Manual : TerminateAC. Reordering those two transitions lets TerminateAC overri...<truncated 52 chars>；This preserves the prior accepted pump_complication repair, including PumpFaultDetected, the guarded PumpFault transition, and fault clearing on Manual/FaultRemoved.；The edit is narrowly scoped and should not regress the 14 passing scenarios because normal StartAC progression still enters AutocontrolInit and then proceeds unconditionally to AutocontrolNormal when TerminateAC is absent.
- diff_summary：`{"summary": "Moved AutocontrolInit -> Manual : TerminateAC before the unconditional AutocontrolInit -> AutocontrolNormal transition so TerminateAC has priority during AutocontrolInit."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_complication = 0;
def float blood_pressure = 0.0;
def float shared_bp_buffer = 0.0;
def float target_bp = 120.0;
def float requested_target_bp = 120.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float pump_speed = 0.0;
def float builtin_switch_speed = 0.0;
def float control_voltage = 0.0;
def float log_flow_rate = 0.0;

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
                alarm_signal = 0;
                pump_complication = 0;
            }
            during {
                shared_bp_buffer = blood_pressure;
                pump_speed = builtin_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                shared_bp_buffer = blood_pressure;
                pump_speed = builtin_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
            }
            during {
                shared_bp_buffer = blood_pressure;
            }
        }

        state AutocontrolNormal {
            during {
                shared_bp_buffer = blood_pressure;
                if [blood_pressure > target_bp] {
                    flow_rate = default_flow_rate - 1.0;
                } else if [blood_pressure < target_bp] {
                    flow_rate = default_flow_rate + 1.0;
                } else {
                    flow_rate = default_flow_rate;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_flow_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_complication = 1; };
        AutocontrolNormal -> PumpFault : if [pump_complication > 0];
        PumpFault -> Manual :: FaultRemoved effect { pump_complication = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -85,8 +85,8 @@
         Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
         Ask_StartAC -> AutocontrolInit :: StartAC;
         Ask_StartAC -> Manual : TerminateAC;
+        AutocontrolInit -> Manual : TerminateAC;
         AutocontrolInit -> AutocontrolNormal;
-        AutocontrolInit -> Manual : TerminateAC;
         AutocontrolNormal -> Manual : TerminateAC;
         AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_complication = 1; };
         AutocontrolNormal -> PumpFault : if [pump_complication > 0];
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:8a4ec08ca747929a627ebb7e2c96f170f74afce08f80b25685e36bdfa1dd36ec`。
  - SL-10 evidence 1: `{"summary": "The SL-9 accepted repair directly addresses the hard simulation failure terminate_from_autocontrolinit_to_manual. The failing step hot-started in CARA.Mode_Control_Algorithm.AutocontrolInit with event CARA.Mode_Control_Algorithm.TerminateAC and expected CARA.Mode_Control_Algorithm.Manual with CA_mode=0, software_control=0, pump_speed=2.2, and flow_rate=4.0; the old DSL instead took the earlier unconditional AutocontrolInit -> AutocontrolNormal transition, leaving CA_mode=1, software_control=1, pump_speed=5.0, and flow_rate=5.0. The candidate moves AutocontrolInit -> Manual : TerminateAC before AutocontrolInit -> AutocontrolNormal, giving TerminateAC priority when present."}`
  - SL-10 evidence 2: `{"summary": "The edit is consistent with the NL requirement that the Caregiver Interface can terminate algorithmic pump control and that manual operation is the shared recovery target. When TerminateAC is raised during AutocontrolInit, returning to Manual releases software control through Manual.enter and restores manual pump behavior through Manual.during."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves the normal autocontrol path: Ask_StartAC -> AutocontrolInit :: StartAC is unchanged, and AutocontrolInit still proceeds unconditionally to AutocontrolNormal when TerminateAC is absent. Thus the repair targets event priority without removing required AutocontrolInit or AutocontrolNormal behavior."}`
  - SL-10 evidence 4: `{"summary": "The prior accepted pump_complication repair is preserved: Manual.enter clears pump_complication, PumpFaultDetected sets pump_complication=1 on AutocontrolNormal -> PumpFault, the required guarded AutocontrolNormal -> PumpFault : if [pump_complication > 0] remains, and FaultRemoved clears pump_complication on recovery to Manual."}`
  - SL-10 evidence 5: `{"summary": "Required NL-grounded states, variables, events, fallback transitions, Ask_StartAC setpoint behavior, manual-mode pump behavior, autocontrol flow computation, shared blood-pressure buffer updates, logging, alarm activation, and software-control release behavior remain represented in the candidate DSL."}`
  - SL-10 evidence 6: `{"summary": "Local deterministic repair review reports ok=true, target_resolved=true, regression_detected=false, drift_risk=none, and no local rejection. This supports accepting the candidate for the next full top-down revalidation pass."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。

</details>

<details><summary>Repair 3 / iteration `2` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:4b981b2ad909079cd44b68d8f31b06f97458d7d3a1852b6952f103bb7be3b583`；candidate_dsl_hash：`sha256:73e3d8d47f98f98c17918558f31366c1bbc17ff11223e44cef11c6bded7def51`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Manual recovery clears alarm_signal and pump_complication on all backManual fallbacks, including from PumpFault, allowing unresolved pump faults to be masked before FaultRemoved/caregiver removal.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-79bee9e51cb`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sl7-0-e56a9044a1` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL: ! * -> Manual : CA_backManual / CB_backManual / CP_backManual / CC_backManual.', 'DSL: Manual.enter sets alarm_signal = 0 and pump_complication = 0.', 'DSL: PumpFault.enter sets alarm_signal = 1 and software_control = 0.', 'NL: pump fault activates alarm signals; caregiver removes the fault; manual operation is shared recovery target, but the NL does not justify clearing fault/alarm merely because backManual occurs.'], 'severity': 'major', 'summary': 'Manual recovery clears alarm_signal and pump_complication on all backManual fallbacks, including from PumpFault, allowing unresolved pump faults to be masked before FaultRemoved/caregiver removal.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:software_control, variable:alarm_signal, variable:pump_complication, variable:blood_pressure, variable:shared_bp_buffer, ... +30`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2911`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sl7-0-e56a9044a1` | `accept` | ❌ | ❌ | The model-review finding is valid: routing any backManual fallback into Manual caused Manual.enter to clear alarm_signal and pump_complication even when entering Manual from PumpFault before the caregiver FaultRemoved event. The smallest safe repair is to stop clearing fault/alarm state in Manual.enter, while clearing both alarm_signal and pump_complication ...<truncated 372 chars> |
- repair_rationale：For fixreq-2-sl7-0-e56a9044a1, the unsafe recovery gap was that Manual.enter cleared alarm_signal=0 and pump_complication=0 for every entry into Manual, including forced CA_backManual, CB_backManual, CP_backManual, or CC_backManual from Pum...<truncated 7 chars>；The repaired Manual.enter still represents the required shared manual recovery target by setting CA_mode=0 and software_control=0, but it no longer masks unresolved pump faults or alarms.；Fault clearing is moved to the NL-grounded caregiver-removal point: PumpFault -> Manual :: FaultRemoved now clears both alarm_signal and pump_complication.；Prior accepted repairs are preserved: PumpFaultDetected still writes pump_complication=1, the guarded AutocontrolNormal -> PumpFault transition remains, and AutocontrolInit still prioritizes TerminateAC before the unconditional transition t...<truncated 20 chars>；Previously passing TerminateAC-to-Manual behavior should not regress because normal termination paths already have alarm_signal=0 and pump_complication=0 unless an unresolved fault was present; Manual.during still sets shared_bp_buffer, pum...<truncated 72 chars>
- diff_summary：`{"summary": "Removed alarm_signal=0 and pump_complication=0 from Manual.enter, preserving only CA_mode/software_control manual recovery there; added alarm_signal=0 to the existing PumpFault -> Manual :: FaultRemoved effect so fault/alarm clearing happens only after caregiver fault removal."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int software_control = 0;
def int alarm_signal = 0;
def int pump_complication = 0;
def float blood_pressure = 0.0;
def float shared_bp_buffer = 0.0;
def float target_bp = 120.0;
def float requested_target_bp = 120.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float pump_speed = 0.0;
def float builtin_switch_speed = 0.0;
def float control_voltage = 0.0;
def float log_flow_rate = 0.0;

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
            }
            during {
                shared_bp_buffer = blood_pressure;
                pump_speed = builtin_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                shared_bp_buffer = blood_pressure;
                pump_speed = builtin_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
                alarm_signal = 0;
            }
            during {
                shared_bp_buffer = blood_pressure;
            }
        }

        state AutocontrolNormal {
            during {
                shared_bp_buffer = blood_pressure;
                if [blood_pressure > target_bp] {
                    flow_rate = default_flow_rate - 1.0;
                } else if [blood_pressure < target_bp] {
                    flow_rate = default_flow_rate + 1.0;
                } else {
                    flow_rate = default_flow_rate;
                }
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_flow_rate = flow_rate;
            }
        }

        state PumpFault {
            enter {
                alarm_signal = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect { target_bp = requested_target_bp; };
        Ask_StartAC -> AutocontrolInit :: StartAC;
        Ask_StartAC -> Manual : TerminateAC;
        AutocontrolInit -> Manual : TerminateAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> Manual : TerminateAC;
        AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_complication = 1; };
        AutocontrolNormal -> PumpFault : if [pump_complication > 0];
        PumpFault -> Manual :: FaultRemoved effect { alarm_signal = 0; pump_complication = 0; };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -28,8 +28,6 @@
             enter {
                 CA_mode = 0;
                 software_control = 0;
-                alarm_signal = 0;
-                pump_complication = 0;
             }
             during {
                 shared_bp_buffer = blood_pressure;
@@ -90,6 +88,6 @@
         AutocontrolNormal -> Manual : TerminateAC;
         AutocontrolNormal -> PumpFault :: PumpFaultDetected effect { pump_complication = 1; };
         AutocontrolNormal -> PumpFault : if [pump_complication > 0];
-        PumpFault -> Manual :: FaultRemoved effect { pump_complication = 0; };
+        PumpFault -> Manual :: FaultRemoved effect { alarm_signal = 0; pump_complication = 0; };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:f30bb08ad3fc32683470dbbb6ec6f88b53e890e2cfdda8657e2413e68e59ea57`。
  - SL-10 evidence 1: `{"summary": "The current hard SL-7 model-review request is resolved by the candidate DSL. The request objected that Manual.enter cleared alarm_signal=0 and pump_complication=0 on every forced backManual fallback, including from PumpFault, thereby masking unresolved pump faults before caregiver FaultRemoved. The candidate removes both clears from Manual.enter and keeps only CA_mode=0 and software_control=0 there, so CA_backManual/CB_backManual/CP_backManual/CC_backManual still reach the required shared Manual recovery target without erasing fault/alarm state."}`
  - SL-10 evidence 2: `{"summary": "The candidate moves fault/alarm clearing to the NL-grounded recovery point: PumpFault -> Manual :: FaultRemoved effect { alarm_signal = 0; pump_complication = 0; }. This matches the NL sequence that a pump fault activates alarm signals, the caregiver removes the fault, and then the system may recover to manual operation; it avoids clearing a fault merely because a backManual fallback was received."}`
  - SL-10 evidence 3: `{"summary": "Required NL-grounded behavior from prior repairs is preserved: PumpFaultDetected still sets pump_complication=1, the required AutocontrolNormal -> PumpFault guard if [pump_complication > 0] remains, PumpFault.enter still sets alarm_signal=1/software_control=0/CA_mode=0, and AutocontrolInit still prioritizes TerminateAC before the unconditional transition to AutocontrolNormal."}`
  - SL-10 evidence 4: `{"summary": "The diff is narrowly scoped to Manual.enter and the FaultRemoved transition effect. Required states Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault; required variables including alarm_signal, pump_complication, CA_mode, software_control, blood_pressure, shared_bp_buffer, target_bp, flow_rate, pump_speed, and log_flow_rate; required events including all backManual events, TerminateAC, FaultRemoved, StartAC, InitiateAC, and ChangeSetpoint; and required manual/autocontrol flow, setpoint, shared-buffer, logging, and alarm/release behavior remain represented."}`
  - SL-10 evidence 5: `{"summary": "Local deterministic evidence reports scenario_regression with 17/19 scenarios passing, but the two failed expectations conflict with the SL-7 hard review finding and the NL fault-removal sequence. In cc_backmanual_fallback_from_pumpfault, local expected CC_backManual from PumpFault to Manual to clear alarm_signal and pump_complication to 0; actual retained both as 1. In forced_backmanual_dirty_flags_value_probe, local expected CA_backManual from Ask_StartAC with dirty alarm/complication flags to clear both to 0; actual retained both as 1. Retaining these flags is the intended repair because backManual is only a shared manual recovery target, not the NL-grounded caregiver fault-r...<truncated 15 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`minor`。
  - local_rejection：reason=`scenario_regression`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 19, "n_scenarios_passed": 17, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init dispatches to Manual and verifies manual-mode shared buffer, built-in-switch pump speed, and default flow-rate behavior.", "name": "default_init_manual_operation_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"CA_mode": 0, "alarm_...<truncated 25522 chars>

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-9c85cb95fd1` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-9c85cb95fd1` | accept=2, reject=0 | `sl10_review` | `sha256:249d10e52de0915268b7f3599a1abc4366220347d8e593644538348853f2bbe9` | Addressed W_UNWRITTEN_READ_VAR by adding meaningful writes to pump_complication rather than a self-assignment., Addressed W_GUARD_VARS_NEVER_CHANGE while preserving the required guard AutocontrolNormal -> PumpFault : if [pump_complication > 0]., The added PumpFaultDetected event is grounded in the NL pump fault/occlusion occurrence and does not invent continuous plant dynamics., ... +2 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-9c85cb95fd1` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:249d10e52de0915268b7f3599a1abc4366220347d8e593644538348853f2bbe9` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-019672ca0f5` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-019672ca0f5` | accept=1, reject=0 | `sl10_review` | `sha256:4b981b2ad909079cd44b68d8f31b06f97458d7d3a1852b6952f103bb7be3b583` | For scenario terminate_from_autocontrolinit_to_manual, failing step terminate_init_to_manual starts in CARA.Mode_Control_Algorithm.AutocontrolInit and injects CARA.Mode_Control_Algorithm.TerminateAC. Expected_state is CARA.Mode_Control_Algorithm.Manual; actual_state was CARA.Mode_Control_Algorithm.AutocontrolNormal., The expected_vars CA_mode=0, software_control=0, pump_speed=2.2, and flow_rate=4.0 are produced by entering Manual and running Manual.during. The actual_vars CA_mode=1, software_control=1, pump_speed=5.0, and flow_rate=5.0 came from falling through to AutocontrolNormal and running autocontrol flow computation., The root cause is transition priority, not missing Manual behavior: the unconditional AutocontrolInit -> AutocontrolNormal transition preceded AutocontrolInit -> Manual : TerminateAC. Reordering those two transitions lets TerminateAC override continuing autocontrol when the event is present., ... +2 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-019672ca0f5` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:4b981b2ad909079cd44b68d8f31b06f97458d7d3a1852b6952f103bb7be3b583` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +5 |
| 7 | `2` | `request_batch` | `fixbatch-2-sha256-79bee9e51cb` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 8 | `2` | `sl9_decision` | `fixbatch-2-sha256-79bee9e51cb` | accept=1, reject=0 | `sl10_review` | `sha256:73e3d8d47f98f98c17918558f31366c1bbc17ff11223e44cef11c6bded7def51` | For fixreq-2-sl7-0-e56a9044a1, the unsafe recovery gap was that Manual.enter cleared alarm_signal=0 and pump_complication=0 for every entry into Manual, including forced CA_backManual, CB_backManual, CP_backManual, or CC_backManual from PumpFault., The repaired Manual.enter still represents the required shared manual recovery target by setting CA_mode=0 and software_control=0, but it no longer masks unresolved pump faults or alarms., Fault clearing is moved to the NL-grounded caregiver-removal point: PumpFault -> Manual :: FaultRemoved now clears both alarm_signal and pump_complication., ... +2 |
| 9 | `2` | `sl10_review` | `fixbatch-2-sha256-79bee9e51cb` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:73e3d8d47f98f98c17918558f31366c1bbc17ff11223e44cef11c6bded7def51` | repair_memory:sl10_evidence, repair_memory:sl10_evidence, repair_memory:sl10_evidence, ... +7 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4678, 'completion_chars': 18651, 'completion_tokens': 6751, 'elapsed_seconds': 123.94259498199972, 'estimated_completion_tokens': 4663, 'estimated_prompt_tokens': 6657, 'estimated_total_tokens': 11320, 'first_chunk_seconds': 39.68812413100386, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 26626, 'prompt_tokens': 6450, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 13201}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1261, 'completion_chars': 5299, 'completion_tokens': 1707, 'elapsed_seconds': 33.41360813900246, 'estimated_completion_tokens': 1325, 'estimated_prompt_tokens': 27277, 'estimated_total_tokens': 28602, 'first_chunk_seconds': 11.073566949999076, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 109106, 'prompt_tokens': 24815, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26522}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 432, 'completion_chars': 1995, 'completion_tokens': 679, 'elapsed_seconds': 14.867839819999062, 'estimated_completion_tokens': 499, 'estimated_prompt_tokens': 25014, 'estimated_total_tokens': 25513, 'first_chunk_seconds': 7.051558981998824, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 100055, 'prompt_tokens': 21906, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 22585}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 3861, 'completion_chars': 15462, 'completion_tokens': 5650, 'elapsed_seconds': 104.45138686100836, 'estimated_completion_tokens': 3866, 'estimated_prompt_tokens': 15168, 'estimated_total_tokens': 19034, 'first_chunk_seconds': 37.992066313003306, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 60671, 'prompt_tokens': 14765, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 20415}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4514, 'completion_chars': 18166, 'completion_tokens': 5033, 'elapsed_seconds': 93.005948866994, 'estimated_completion_tokens': 4542, 'estimated_prompt_tokens': 19220, 'estimated_total_tokens': 23762, 'first_chunk_seconds': 12.211957469000481, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 76878, 'prompt_tokens': 18773, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23806}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4879, 'completion_chars': 19659, 'completion_tokens': 5398, 'elapsed_seconds': 100.29676370600646, 'estimated_completion_tokens': 4915, 'estimated_prompt_tokens': 19896, 'estimated_total_tokens': 24811, 'first_chunk_seconds': 13.283414367004298, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 79582, 'prompt_tokens': 19426, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 24824}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1284, 'completion_chars': 5548, 'completion_tokens': 1577, 'elapsed_seconds': 32.9055371620052, 'estimated_completion_tokens': 1387, 'estimated_prompt_tokens': 43634, 'estimated_total_tokens': 45021, 'first_chunk_seconds': 7.756729814005666, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 174534, 'prompt_tokens': 39069, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 40646}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 569, 'completion_chars': 2588, 'completion_tokens': 649, 'elapsed_seconds': 14.354254439997021, 'estimated_completion_tokens': 647, 'estimated_prompt_tokens': 42027, 'estimated_total_tokens': 42674, 'first_chunk_seconds': 4.041117863991531, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 168107, 'prompt_tokens': 36909, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 37558}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 5597, 'completion_chars': 22602, 'completion_tokens': 6367, 'elapsed_seconds': 117.75935991200095, 'estimated_completion_tokens': 5651, 'estimated_prompt_tokens': 20493, 'estimated_total_tokens': 26144, 'first_chunk_seconds': 18.851518292998662, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 81972, 'prompt_tokens': 20011, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26378}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4415, 'completion_chars': 17660, 'completion_tokens': 5295, 'elapsed_seconds': 97.41748427100538, 'estimated_completion_tokens': 4415, 'estimated_prompt_tokens': 21229, 'estimated_total_tokens': 25644, 'first_chunk_seconds': 19.011056950010243, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 84915, 'prompt_tokens': 20729, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 26024}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1957, 'completion_chars': 9279, 'completion_tokens': 2931, 'elapsed_seconds': 55.49600708800426, 'estimated_completion_tokens': 2320, 'estimated_prompt_tokens': 21027, 'estimated_total_tokens': 23347, 'first_chunk_seconds': 20.193509687000187, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 84107, 'prompt_tokens': 20852, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 23783}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1258, 'completion_chars': 5519, 'completion_tokens': 1717, 'elapsed_seconds': 35.667978049008525, 'estimated_completion_tokens': 1380, 'estimated_prompt_tokens': 60231, 'estimated_total_tokens': 61611, 'first_chunk_seconds': 13.002512075006962, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 240924, 'prompt_tokens': 54182, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 55899}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1093, 'completion_chars': 5211, 'completion_tokens': 1538, 'elapsed_seconds': 31.465785011998378, 'estimated_completion_tokens': 1303, 'estimated_prompt_tokens': 72284, 'estimated_total_tokens': 73587, 'first_chunk_seconds': 12.58912361098919, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 289136, 'prompt_tokens': 62347, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 63885}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 4125, 'completion_chars': 16669, 'completion_tokens': 5079, 'elapsed_seconds': 96.38833918300224, 'estimated_completion_tokens': 4168, 'estimated_prompt_tokens': 24979, 'estimated_total_tokens': 29147, 'first_chunk_seconds': 24.084093451005174, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 99913, 'prompt_tokens': 24475, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 29554}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'chunk_count': 1559, 'completion_chars': 7397, 'completion_tokens': 1954, 'elapsed_seconds': 40.18931912900007, 'estimated_completion_tokens': 1850, 'estimated_prompt_tokens': 23518, 'estimated_total_tokens': 25368, 'first_chunk_seconds': 12.196571923996089, 'message_count': 2, 'model': 'gpt-5.5', 'prompt_chars': 94070, 'prompt_tokens': 23315, 'stream': True, 'stream_include_usage_requested': True, 'stream_usage_zero_reported': False, 'token_usage_available': True, 'token_usage_estimation_method': None, 'total_tokens': 25269}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`50/16`，missing=`<none>`。
- repairs：`3/3` accepted；scenario_history=`8`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
