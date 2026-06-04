## path1 / cara-infusion-pump-formal-spec__01 / default 真实运行结果：Path1 CARA representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`not_converged`；record_status：`budget_exhausted`；result_status：`not_converged`。
- main_result_eligible：`false`。
- 一句话结论：`scenario_or_sim_oracle`；停止原因：SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `cara-infusion-pump-formal-spec__01` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `529e3096b4bb0f9c46cd21be461c2ec272e89c53` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:ce499624790550d734a59fdd9b6b28f8194710e89c85f739538372d5d8133081` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-round21compact-d7784c4f` |
| final verdict/status | verdict=`not_converged`, record=`budget_exhausted`, result=`not_converged` |
| main_result_eligible | `false` |
| final.fcstm 来源 | `{"accepted": true, "final_dsl_hash": "sha256:4e2c880451936159cd68420023899a192ce50745282c5d4b38ecc761e709b456", "iteration": 2, "last_rejected_candidate": {"candidate_dsl_hash": "sha256:755ad0fe1c1a1250313a82e8b039c5887f55a86bb21cfdf676de93081e486e84", "iteration": 2, "repair_history_index": 3, "rework_instructions": ["Do not reject this locked request. Continue repairing fixreq-2-sd6-0-01a4312604.", "Ensure BackManual from PumpFault executes an effect before Manual entry/during behavior so that pump_fault = 0 and alarm_active = 0, allowing Manual to set flow_rate = manual_flow_rate and pump_speed = builtin_switch_speed.", "Remove the semantic duplication where global forced '* -> Manual :: CA_backManual/CB_backManual/CP_backManual/CC_backManual' overrides the PumpFault-specific normal transitions. If the DSL supports scoped forced transitions or exclusions, restrict the forced BackManual fallbacks so they still cover all non-PumpFault active states while the PumpFault-specific effectful transitions handle PumpFault.", "Preserve the NL-required cross-component fallback behavior: CA_backManual, CB_backManual, CP_backManual, and CC_backManual must still cause CA_mode to become Manual from every relevant CARA mode, including PumpFault via the effectful PumpFault-specific path.", "Do not create source-local shadow BackManual events. PumpFault-specific transitions must reference the same CARA-scope/cross-component BackManual events used by the fallback mechanism.", "Keep all required states, variables, initial transition, InitiateAC/StartAC/TerminateAC transitions, pump_fault guards, FaultRemoved handling, Manual fault-safety behavior, and BackManual recovery coverage.", "After the edit, the hot-start PumpFault + CC_backManual scenario must reach CARA.Manual with CA_mode = 0, control_released = 1, pump_fault = 0, alarm_active = 0, flow_rate = manual_flow_rate, and pump_speed = builtin_switch_speed."], "sl10_decision": "rework"}, "repair_history_index": 4, "selected_source_stage": "SD-6", "sl10_decision": "pass", "source_kind": "repair_candidate"}` |
| FixLog next_action 序列 | `sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sc11_accept_then_sd2, sl9_decision_and_repair, sl10_review, sl9_rework, sl10_review, sl9_rework, sl10_review, ... +7` |
| iteration exit_reason 序列 | `candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, candidate_accepted_for_next_full_pass, SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5` |
| token/cost/time | tokens=`{'prompt_tokens': 372500, 'completion_tokens': 66379, 'total_tokens': 438879, 'n_calls': 23}`, elapsed=`1992.751s` |
| run record | [`pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
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
def int target_bp = 120;
def int requested_target_bp = 120;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int flow_rate = 0;
def int manual_flow_rate = 0;
def int builtin_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int control_released = 1;

state CARA {
    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault > 0] {
                alarm_active = 1;
            } else {
                alarm_active = 0;
            }
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault > 0] {
                alarm_active = 1;
                flow_rate = 0;
                pump_speed = 0;
            } else {
                alarm_active = 0;
                flow_rate = manual_flow_rate;
                pump_speed = builtin_switch_speed;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
        }
        during {
            target_bp = requested_target_bp;
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            alarm_active = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 3;
            control_released = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            flow_rate = target_bp - blood_pressure;
            pump_speed = control_voltage;
        }
    }

    state PumpFault {
        enter {
            CA_mode = 4;
            alarm_active = 1;
            control_released = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Manual -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> PumpFault : if [pump_fault > 0];
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
    };
    PumpFault -> Manual : CA_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual : CB_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual : CP_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual : CC_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };

    ! Manual -> Manual : CA_backManual;
    ! Ask_StartAC -> Manual : CA_backManual;
    ! AutocontrolInit -> Manual : CA_backManual;
    ! AutocontrolNormal -> Manual : CA_backManual;
    ! Manual -> Manual : CB_backManual;
    ! Ask_StartAC -> Manual : CB_backManual;
    ! AutocontrolInit -> Manual : CB_backManual;
    ! AutocontrolNormal -> Manual : CB_backManual;
    ! Manual -> Manual : CP_backManual;
    ! Ask_StartAC -> Manual : CP_backManual;
    ! AutocontrolInit -> Manual : CP_backManual;
    ! AutocontrolNormal -> Manual : CP_backManual;
    ! Manual -> Manual : CC_backManual;
    ! Ask_StartAC -> Manual : CC_backManual;
    ! AutocontrolInit -> Manual : CC_backManual;
    ! AutocontrolNormal -> Manual : CC_backManual;
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12742 | 生成初始 DSL 与 grounding seeds | initial len=2162 | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=143619 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=7, tokens=142020 | LLM per-request accept/reject + repair | candidate len=2162,2580,3008,3004,3600,3340,3600 | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=7, tokens=98294 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=143619 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=42204 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=7, tokens=142020 | LLM per-request accept/reject + repair | candidate len=2162,2580,3008,3004,3600,3340,3600 | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=7, tokens=98294 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=143619 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=7, tokens=142020 | LLM per-request accept/reject + repair | candidate len=2162,2580,3008,3004,3600,3340,3600 | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=7, tokens=98294 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=7, tokens=142020 | LLM per-request accept/reject + repair | candidate len=2162,2580,3008,3004,3600,3340,3600 | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=7, tokens=98294 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=7, tokens=142020 | LLM per-request accept/reject + repair | candidate len=2162,2580,3008,3004,3600,3340,3600 | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=7, tokens=98294 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=143619 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=143619 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=42204 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=7, tokens=142020 | LLM per-request accept/reject + repair | candidate len=2162,2580,3008,3004,3600,3340,3600 | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=7, tokens=98294 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1; blocking=0, advisory=19, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=6, tokens=143619 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=False, diag=0; ok=True, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=7, tokens=142020 | LLM per-request accept/reject + repair | candidate len=2162,2580,3008,3004,3600,3340,3600 | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=7, tokens=98294 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5 | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz) |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-6` | yes | fixbatch-0-sha256-a71f57456c3 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SL-7` | yes | fixbatch-1-sha256-a8d11e75057 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SD-6` | yes | fixbatch-2-sha256-6c78e328186 / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `SL-7` | yes | fixbatch-3-sha256-1d257c6524c / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 4 | `SD-6` | yes | fixbatch-4-sha256-b72cdbf75ec / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5 |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|---|
| `default_init_enters_manual_and_uses_manual_controls` | default-init: first cycle dispatches to Manual, where manual flow rate, built-in switch speed, and sensor buffer are app...<truncated 5 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `initiate_startac_reaches_normal_autocontrol` | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC into AutocontrolInit, then reache...<truncated 21 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `terminate_from_ask_returns_manual` | explicit-hot-start: TerminateAC from Ask_StartAC returns to Manual as caregiver termination of algorithmic control. | ✅ | ✅ | ✅ | ✅ | ✅ |
| `terminate_from_autocontrol_init_returns_manual` | explicit-hot-start: TerminateAC from AutocontrolInit should override continued autocontrol and return to Manual. | ❌ | ✅ | ✅ | ✅ | ✅ |
| `normal_autocontrol_no_fault_then_terminate` | explicit-hot-start: with pump_fault at the non-fault boundary, AutocontrolNormal stays active and computes flow before T...<truncated 26 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_from_normal_alarms_then_removed_to_manual` | explicit-hot-start: pump_fault positive in AutocontrolNormal enters PumpFault with alarm and released control, then Faul...<truncated 45 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_from_init_enters_pumpfault` | explicit-hot-start: pump_fault positive during AutocontrolInit should enter PumpFault rather than continuing into normal...<truncated 9 chars> | ❌ | ✅ | ✅ | ✅ | ✅ |
| `ca_backmanual_forces_manual_from_init` | explicit-hot-start: CA_backManual is a cross-component fallback that forces AutocontrolInit to the shared Manual recover...<truncated 9 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `cb_backmanual_forces_manual_from_ask` | explicit-hot-start: CB_backManual is a cross-component fallback that forces Ask_StartAC to the shared Manual recovery ta...<truncated 5 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `cp_backmanual_forces_manual_from_normal` | explicit-hot-start: CP_backManual is a cross-component fallback that forces AutocontrolNormal to the shared Manual recov...<truncated 11 chars> | ✅ | ✅ | ✅ | ✅ | ✅ |
| `cc_backmanual_forces_manual_from_pumpfault` | explicit-hot-start: CC_backManual is a cross-component fallback that forces PumpFault to the shared Manual recovery targ...<truncated 28 chars> | ✅ | ✅ | ❌ | ✅ | ❌ |
| `manual_fault_removed_self_transition_clears_fault` | explicit-hot-start: FaultRemoved in Manual is a self-transition that must remain in Manual and clear pump_fault before m...<truncated 22 chars> | ⚪ | ⚪ | ✅ | ✅ | ✅ |
| `pumpfault_fault_removed_strong_effect_probe` | explicit-hot-start: FaultRemoved from PumpFault must target Manual and set pump_fault exactly to 0, catching missing or ...<truncated 20 chars> | ⚪ | ⚪ | ✅ | ✅ | ✅ |
| `manual_ca_backmanual_forced_enter_effect_probe` | explicit-hot-start: CA_backManual from Manual must still run the forced recovery to Manual and restore CA_mode/control_r...<truncated 96 chars> | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `pumpfault_ca_backmanual_exact_fault_clear_probe` | explicit-hot-start: CA_backManual from PumpFault is a recovery-to-Manual transition whose effect must clear pump_fault e...<truncated 85 chars> | ⚪ | ⚪ | ⚪ | ✅ | ❌ |
| `ca_backmanual_forces_manual_from_normal_missing_line_probe` | explicit-hot-start: CA_backManual from AutocontrolNormal must force Manual; if that forced line is missing the event is ...<truncated 46 chars> | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `cb_backmanual_forces_manual_from_init_missing_line_probe` | explicit-hot-start: CB_backManual from AutocontrolInit must force Manual before the immediate normal-autocontrol transit...<truncated 14 chars> | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `cp_backmanual_forces_manual_from_ask_missing_line_probe` | explicit-hot-start: CP_backManual from Ask_StartAC must force the shared Manual recovery target rather than being ignore...<truncated 27 chars> | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `cp_backmanual_forces_manual_from_init_missing_line_probe` | explicit-hot-start: CP_backManual from AutocontrolInit must force Manual; missing the forced line would allow the immedi...<truncated 40 chars> | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `cc_backmanual_forces_manual_from_normal_missing_line_probe` | explicit-hot-start: CC_backManual from AutocontrolNormal must force Manual as the shared cross-component fallback. | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `cc_backmanual_forces_manual_from_init_missing_line_probe` | explicit-hot-start: CC_backManual from AutocontrolInit must force Manual, probing the forced transition line independent...<truncated 31 chars> | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `cb_backmanual_manual_reentry_missing_line_probe` | explicit-hot-start: CB_backManual from Manual must re-enter Manual and restore Manual-mode outputs, catching a missing f...<truncated 59 chars> | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `cc_backmanual_manual_reentry_missing_line_probe` | explicit-hot-start: CC_backManual from Manual must run the forced Manual recovery transition and restore Manual-mode eff...<truncated 5 chars> | ⚪ | ⚪ | ⚪ | ✅ | ✅ |
| `ca_backmanual_forces_manual_from_ask_missing_line_probe` | explicit-hot-start: CA_backManual from Ask_StartAC must force the shared Manual recovery target; if the Ask_StartAC forc...<truncated 54 chars> | ⚪ | ⚪ | ⚪ | ⚪ | ✅ |
| `cb_backmanual_forces_manual_from_normal_missing_line_probe` | explicit-hot-start: CB_backManual from AutocontrolNormal must force Manual; if that forced line is missing, normal autoc...<truncated 56 chars> | ⚪ | ⚪ | ⚪ | ⚪ | ✅ |
| `cp_backmanual_manual_reentry_missing_line_probe` | explicit-hot-start: CP_backManual from Manual must still execute the forced Manual recovery and restore Manual-mode outp...<truncated 52 chars> | ⚪ | ⚪ | ⚪ | ⚪ | ✅ |
| `cc_backmanual_forces_manual_from_ask_missing_line_probe` | explicit-hot-start: CC_backManual from Ask_StartAC must force Manual as the shared cross-component fallback; missing the...<truncated 55 chars> | ⚪ | ⚪ | ⚪ | ⚪ | ✅ |

#### 6.2 Scenario definitions

<details><summary>`default_init_enters_manual_and_uses_manual_controls` — default-init: first cycle dispatches to Manual, where manual flow rate, built-in switch speed, and sensor buffer are applied.</summary>

| Field | Value |
|---|---|
| description | default-init: first cycle dispatches to Manual, where manual flow rate, built-in switch speed, and sensor buffer are applied. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 110, "builtin_switch_speed": 7, "manual_flow_rate": 25}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_after_initial_dispatch` | `0` | `[]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 25, "pump_speed": 7, "sensor_buffer_bp": 110}` |

</details>

<details><summary>`initiate_startac_reaches_normal_autocontrol` — default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC into AutocontrolInit, then reaches normal autocontrol.</summary>

| Field | Value |
|---|---|
| description | default-init: caregiver initiates AC, changes setpoint in Ask_StartAC, presses StartAC into AutocontrolInit, then reaches normal autocontrol. |
| initial_state | `<default-init>` |
| initial_vars | `{"blood_pressure": 100, "control_voltage": 4, "requested_target_bp": 130}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `dispatch_to_manual` | `0` | `[]` | `CARA.Manual` | `{"CA_mode": 0}` |
| 1 `initiate_enters_ask_startac` | `0` | `["CARA.Manual.InitiateAC"]` | `CARA.Ask_StartAC` | `{"CA_mode": 1, "sensor_buffer_bp": 100, "target_bp": 130}` |
| 2 `startac_enters_autocontrol_init` | `0` | `["CARA.Ask_StartAC.StartAC"]` | `CARA.AutocontrolInit` | `{"CA_mode": 2, "alarm_active": 0, "control_released": 0}` |
| 3 `autocontrol_normal_controls_flow` | `0` | `[]` | `CARA.AutocontrolNormal` | `{"CA_mode": 3, "control_released": 0, "flow_rate": 30, "pump_speed": 4, "sensor_buffer_bp": 100}` |

</details>

<details><summary>`terminate_from_ask_returns_manual` — explicit-hot-start: TerminateAC from Ask_StartAC returns to Manual as caregiver termination of algorithmic control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: TerminateAC from Ask_StartAC returns to Manual as caregiver termination of algorithmic control. |
| initial_state | `CARA.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 90, "builtin_switch_speed": 3, "control_released": 0, "manual_flow_rate": 12}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_to_manual` | `0` | `["CARA.Ask_StartAC.TerminateAC"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 12, "pump_speed": 3, "sensor_buffer_bp": 90}` |

</details>

<details><summary>`terminate_from_autocontrol_init_returns_manual` — explicit-hot-start: TerminateAC from AutocontrolInit should override continued autocontrol and return to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: TerminateAC from AutocontrolInit should override continued autocontrol and return to Manual. |
| initial_state | `CARA.AutocontrolInit` |
| initial_vars | `{"CA_mode": 2, "blood_pressure": 101, "builtin_switch_speed": 2, "control_released": 0, "manual_flow_rate": 8, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `terminate_init_to_manual` | `0` | `["CARA.AutocontrolInit.TerminateAC"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 8, "pump_speed": 2, "sensor_buffer_bp": 101}` |

</details>

<details><summary>`normal_autocontrol_no_fault_then_terminate` — explicit-hot-start: with pump_fault at the non-fault boundary, AutocontrolNormal stays active and computes flow before TerminateAC returns Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: with pump_fault at the non-fault boundary, AutocontrolNormal stays active and computes flow before TerminateAC returns Manual. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 3, "blood_pressure": 80, "builtin_switch_speed": 1, "control_voltage": 5, "manual_flow_rate": 6, "pump_fault": 0, "target_bp": 120}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_fault_stays_normal` | `0` | `[]` | `CARA.AutocontrolNormal` | `{"flow_rate": 40, "pump_speed": 5, "sensor_buffer_bp": 80}` |
| 1 `terminate_normal_to_manual` | `0` | `["CARA.AutocontrolNormal.TerminateAC"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 6, "pump_speed": 1, "sensor_buffer_bp": 80}` |

</details>

<details><summary>`pump_fault_from_normal_alarms_then_removed_to_manual` — explicit-hot-start: pump_fault positive in AutocontrolNormal enters PumpFault with alarm and released control, then FaultRemoved returns Manual and clears the f...<truncated 5 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: pump_fault positive in AutocontrolNormal enters PumpFault with alarm and released control, then FaultRemoved returns Manual and clears the fault. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 3, "blood_pressure": 95, "builtin_switch_speed": 2, "control_released": 0, "manual_flow_rate": 10, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `positive_fault_enters_pumpfault` | `0` | `[]` | `CARA.PumpFault` | `{"CA_mode": 4, "alarm_active": 1, "control_released": 1, "sensor_buffer_bp": 95}` |
| 1 `fault_removed_returns_manual` | `0` | `["CARA.PumpFault.FaultRemoved"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 10, "pump_fault": 0, "pump_speed": 2, "sensor_buffer_bp": 95}` |

</details>

<details><summary>`pump_fault_from_init_enters_pumpfault` — explicit-hot-start: pump_fault positive during AutocontrolInit should enter PumpFault rather than continuing into normal control.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: pump_fault positive during AutocontrolInit should enter PumpFault rather than continuing into normal control. |
| initial_state | `CARA.AutocontrolInit` |
| initial_vars | `{"CA_mode": 2, "blood_pressure": 105, "control_released": 0, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `init_fault_to_pumpfault` | `0` | `[]` | `CARA.PumpFault` | `{"CA_mode": 4, "alarm_active": 1, "control_released": 1, "sensor_buffer_bp": 105}` |

</details>

<details><summary>`ca_backmanual_forces_manual_from_init` — explicit-hot-start: CA_backManual is a cross-component fallback that forces AutocontrolInit to the shared Manual recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CA_backManual is a cross-component fallback that forces AutocontrolInit to the shared Manual recovery target. |
| initial_state | `CARA.AutocontrolInit` |
| initial_vars | `{"CA_mode": 2, "blood_pressure": 100, "builtin_switch_speed": 4, "control_released": 0, "manual_flow_rate": 11}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_to_manual` | `0` | `["CARA.CA_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 11, "pump_speed": 4, "sensor_buffer_bp": 100}` |

</details>

<details><summary>`cb_backmanual_forces_manual_from_ask` — explicit-hot-start: CB_backManual is a cross-component fallback that forces Ask_StartAC to the shared Manual recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CB_backManual is a cross-component fallback that forces Ask_StartAC to the shared Manual recovery target. |
| initial_state | `CARA.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 99, "builtin_switch_speed": 5, "manual_flow_rate": 9}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_to_manual` | `0` | `["CARA.CB_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 9, "pump_speed": 5, "sensor_buffer_bp": 99}` |

</details>

<details><summary>`cp_backmanual_forces_manual_from_normal` — explicit-hot-start: CP_backManual is a cross-component fallback that forces AutocontrolNormal to the shared Manual recovery target.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CP_backManual is a cross-component fallback that forces AutocontrolNormal to the shared Manual recovery target. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 3, "blood_pressure": 102, "builtin_switch_speed": 6, "control_released": 0, "manual_flow_rate": 14, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_to_manual` | `0` | `["CARA.CP_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 14, "pump_speed": 6, "sensor_buffer_bp": 102}` |

</details>

<details><summary>`cc_backmanual_forces_manual_from_pumpfault` — explicit-hot-start: CC_backManual is a cross-component fallback that forces PumpFault to the shared Manual recovery target and silences alarm state.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CC_backManual is a cross-component fallback that forces PumpFault to the shared Manual recovery target and silences alarm state. |
| initial_state | `CARA.PumpFault` |
| initial_vars | `{"CA_mode": 4, "alarm_active": 1, "blood_pressure": 88, "builtin_switch_speed": 3, "control_released": 1, "manual_flow_rate": 7, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_backmanual_to_manual` | `0` | `["CARA.CC_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 7, "pump_speed": 3, "sensor_buffer_bp": 88}` |

</details>

<details><summary>`manual_fault_removed_self_transition_clears_fault` — explicit-hot-start: FaultRemoved in Manual is a self-transition that must remain in Manual and clear pump_fault before manual controls resume.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: FaultRemoved in Manual is a self-transition that must remain in Manual and clear pump_fault before manual controls resume. |
| initial_state | `CARA.Manual` |
| initial_vars | `{"CA_mode": 0, "alarm_active": 1, "blood_pressure": 112, "builtin_switch_speed": 8, "control_released": 1, "manual_flow_rate": 16, "pump_fault": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_fault_removed_cleared` | `0` | `["CARA.Manual.FaultRemoved"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 16, "pump_fault": 0, "pump_speed": 8, "sensor_buffer_bp": 112}` |

</details>

<details><summary>`pumpfault_fault_removed_strong_effect_probe` — explicit-hot-start: FaultRemoved from PumpFault must target Manual and set pump_fault exactly to 0, catching missing or wrong effect values.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: FaultRemoved from PumpFault must target Manual and set pump_fault exactly to 0, catching missing or wrong effect values. |
| initial_state | `CARA.PumpFault` |
| initial_vars | `{"CA_mode": 4, "alarm_active": 1, "blood_pressure": 107, "builtin_switch_speed": 9, "control_released": 1, "manual_flow_rate": 18, "pump_fault": 5}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `pumpfault_fault_removed_exact_clear` | `0` | `["CARA.PumpFault.FaultRemoved"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 18, "pump_fault": 0, "pump_speed": 9, "sensor_buffer_bp": 107}` |

</details>

<details><summary>`manual_ca_backmanual_forced_enter_effect_probe` — explicit-hot-start: CA_backManual from Manual must still run the forced recovery to Manual and restore CA_mode/control_released, catching a missing forced trans...<truncated 56 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CA_backManual from Manual must still run the forced recovery to Manual and restore CA_mode/control_released, catching a missing forced transition line even when the target state name is unchanged. |
| initial_state | `CARA.Manual` |
| initial_vars | `{"CA_mode": 3, "alarm_active": 1, "blood_pressure": 115, "builtin_switch_speed": 10, "control_released": 0, "manual_flow_rate": 21, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `manual_ca_backmanual_reenters_manual` | `0` | `["CARA.CA_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 21, "pump_speed": 10, "sensor_buffer_bp": 115}` |

</details>

<details><summary>`pumpfault_ca_backmanual_exact_fault_clear_probe` — explicit-hot-start: CA_backManual from PumpFault is a recovery-to-Manual transition whose effect must clear pump_fault exactly to 0, catching missing or wrong e...<truncated 45 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CA_backManual from PumpFault is a recovery-to-Manual transition whose effect must clear pump_fault exactly to 0, catching missing or wrong effect values on the backManual recovery path. |
| initial_state | `CARA.PumpFault` |
| initial_vars | `{"CA_mode": 4, "alarm_active": 1, "blood_pressure": 109, "builtin_switch_speed": 11, "control_released": 1, "manual_flow_rate": 19, "pump_fault": 6}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `pumpfault_ca_backmanual_exact_clear` | `0` | `["CARA.CA_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 19, "pump_fault": 0, "pump_speed": 11, "sensor_buffer_bp": 109}` |

</details>

<details><summary>`ca_backmanual_forces_manual_from_normal_missing_line_probe` — explicit-hot-start: CA_backManual from AutocontrolNormal must force Manual; if that forced line is missing the event is ignored and normal autocontrol remains a...<truncated 6 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CA_backManual from AutocontrolNormal must force Manual; if that forced line is missing the event is ignored and normal autocontrol remains active. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 3, "blood_pressure": 90, "builtin_switch_speed": 4, "control_released": 0, "control_voltage": 6, "manual_flow_rate": 13, "pump_fault": 0, "target_bp": 125}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_normal_to_manual` | `0` | `["CARA.CA_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 13, "pump_speed": 4, "sensor_buffer_bp": 90}` |

</details>

<details><summary>`cb_backmanual_forces_manual_from_init_missing_line_probe` — explicit-hot-start: CB_backManual from AutocontrolInit must force Manual before the immediate normal-autocontrol transition can occur.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CB_backManual from AutocontrolInit must force Manual before the immediate normal-autocontrol transition can occur. |
| initial_state | `CARA.AutocontrolInit` |
| initial_vars | `{"CA_mode": 2, "blood_pressure": 96, "builtin_switch_speed": 5, "control_released": 0, "manual_flow_rate": 15, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_init_to_manual` | `0` | `["CARA.CB_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 15, "pump_speed": 5, "sensor_buffer_bp": 96}` |

</details>

<details><summary>`cp_backmanual_forces_manual_from_ask_missing_line_probe` — explicit-hot-start: CP_backManual from Ask_StartAC must force the shared Manual recovery target rather than being ignored while asking to start AC.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CP_backManual from Ask_StartAC must force the shared Manual recovery target rather than being ignored while asking to start AC. |
| initial_state | `CARA.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "blood_pressure": 97, "builtin_switch_speed": 6, "control_released": 0, "manual_flow_rate": 17, "requested_target_bp": 135}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_ask_to_manual` | `0` | `["CARA.CP_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 17, "pump_speed": 6, "sensor_buffer_bp": 97}` |

</details>

<details><summary>`cp_backmanual_forces_manual_from_init_missing_line_probe` — explicit-hot-start: CP_backManual from AutocontrolInit must force Manual; missing the forced line would allow the immediate transition toward AutocontrolNormal.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CP_backManual from AutocontrolInit must force Manual; missing the forced line would allow the immediate transition toward AutocontrolNormal. |
| initial_state | `CARA.AutocontrolInit` |
| initial_vars | `{"CA_mode": 2, "blood_pressure": 103, "builtin_switch_speed": 7, "control_released": 0, "manual_flow_rate": 20, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_init_to_manual` | `0` | `["CARA.CP_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 20, "pump_speed": 7, "sensor_buffer_bp": 103}` |

</details>

<details><summary>`cc_backmanual_forces_manual_from_normal_missing_line_probe` — explicit-hot-start: CC_backManual from AutocontrolNormal must force Manual as the shared cross-component fallback.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CC_backManual from AutocontrolNormal must force Manual as the shared cross-component fallback. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 3, "blood_pressure": 92, "builtin_switch_speed": 8, "control_released": 0, "control_voltage": 8, "manual_flow_rate": 22, "pump_fault": 0, "target_bp": 118}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_backmanual_normal_to_manual` | `0` | `["CARA.CC_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 22, "pump_speed": 8, "sensor_buffer_bp": 92}` |

</details>

<details><summary>`cc_backmanual_forces_manual_from_init_missing_line_probe` — explicit-hot-start: CC_backManual from AutocontrolInit must force Manual, probing the forced transition line independently of PumpFault-local recovery.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CC_backManual from AutocontrolInit must force Manual, probing the forced transition line independently of PumpFault-local recovery. |
| initial_state | `CARA.AutocontrolInit` |
| initial_vars | `{"CA_mode": 2, "blood_pressure": 104, "builtin_switch_speed": 9, "control_released": 0, "manual_flow_rate": 23, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_backmanual_init_to_manual` | `0` | `["CARA.CC_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 23, "pump_speed": 9, "sensor_buffer_bp": 104}` |

</details>

<details><summary>`cb_backmanual_manual_reentry_missing_line_probe` — explicit-hot-start: CB_backManual from Manual must re-enter Manual and restore Manual-mode outputs, catching a missing forced self-recovery line even when state...<truncated 19 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CB_backManual from Manual must re-enter Manual and restore Manual-mode outputs, catching a missing forced self-recovery line even when state name is unchanged. |
| initial_state | `CARA.Manual` |
| initial_vars | `{"CA_mode": 3, "alarm_active": 1, "blood_pressure": 116, "builtin_switch_speed": 12, "control_released": 0, "manual_flow_rate": 24, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_manual_reentry` | `0` | `["CARA.CB_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 24, "pump_speed": 12, "sensor_buffer_bp": 116}` |

</details>

<details><summary>`cc_backmanual_manual_reentry_missing_line_probe` — explicit-hot-start: CC_backManual from Manual must run the forced Manual recovery transition and restore Manual-mode effects.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CC_backManual from Manual must run the forced Manual recovery transition and restore Manual-mode effects. |
| initial_state | `CARA.Manual` |
| initial_vars | `{"CA_mode": 4, "alarm_active": 1, "blood_pressure": 117, "builtin_switch_speed": 13, "control_released": 0, "manual_flow_rate": 26, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_backmanual_manual_reentry` | `0` | `["CARA.CC_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 26, "pump_speed": 13, "sensor_buffer_bp": 117}` |

</details>

<details><summary>`ca_backmanual_forces_manual_from_ask_missing_line_probe` — explicit-hot-start: CA_backManual from Ask_StartAC must force the shared Manual recovery target; if the Ask_StartAC forced line is missing, the system remains i...<truncated 14 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CA_backManual from Ask_StartAC must force the shared Manual recovery target; if the Ask_StartAC forced line is missing, the system remains in Ask_StartAC. |
| initial_state | `CARA.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 1, "blood_pressure": 98, "builtin_switch_speed": 14, "control_released": 0, "manual_flow_rate": 27, "requested_target_bp": 140}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_ask_to_manual` | `0` | `["CARA.CA_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 27, "pump_speed": 14, "sensor_buffer_bp": 98}` |

</details>

<details><summary>`cb_backmanual_forces_manual_from_normal_missing_line_probe` — explicit-hot-start: CB_backManual from AutocontrolNormal must force Manual; if that forced line is missing, normal autocontrol continues and computes voltage-dr...<truncated 16 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CB_backManual from AutocontrolNormal must force Manual; if that forced line is missing, normal autocontrol continues and computes voltage-driven pump speed. |
| initial_state | `CARA.AutocontrolNormal` |
| initial_vars | `{"CA_mode": 3, "blood_pressure": 91, "builtin_switch_speed": 15, "control_released": 0, "control_voltage": 9, "manual_flow_rate": 28, "pump_fault": 0, "target_bp": 126}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cb_backmanual_normal_to_manual` | `0` | `["CARA.CB_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 28, "pump_speed": 15, "sensor_buffer_bp": 91}` |

</details>

<details><summary>`cp_backmanual_manual_reentry_missing_line_probe` — explicit-hot-start: CP_backManual from Manual must still execute the forced Manual recovery and restore Manual-mode outputs, catching a missing forced self-tran...<truncated 12 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CP_backManual from Manual must still execute the forced Manual recovery and restore Manual-mode outputs, catching a missing forced self-transition line. |
| initial_state | `CARA.Manual` |
| initial_vars | `{"CA_mode": 2, "alarm_active": 1, "blood_pressure": 118, "builtin_switch_speed": 16, "control_released": 0, "manual_flow_rate": 29, "pump_fault": 0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cp_backmanual_manual_reentry` | `0` | `["CARA.CP_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 29, "pump_speed": 16, "sensor_buffer_bp": 118}` |

</details>

<details><summary>`cc_backmanual_forces_manual_from_ask_missing_line_probe` — explicit-hot-start: CC_backManual from Ask_StartAC must force Manual as the shared cross-component fallback; missing the Ask_StartAC forced line leaves the ask ...<truncated 15 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start: CC_backManual from Ask_StartAC must force Manual as the shared cross-component fallback; missing the Ask_StartAC forced line leaves the ask submode active. |
| initial_state | `CARA.Ask_StartAC` |
| initial_vars | `{"CA_mode": 1, "alarm_active": 1, "blood_pressure": 119, "builtin_switch_speed": 17, "control_released": 0, "manual_flow_rate": 30, "requested_target_bp": 128}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `cc_backmanual_ask_to_manual` | `0` | `["CARA.CC_backManual"]` | `CARA.Manual` | `{"CA_mode": 0, "alarm_active": 0, "control_released": 1, "flow_rate": 30, "pump_speed": 17, "sensor_buffer_bp": 119}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | terminate_from_autocontrol_init_returns_manual, pump_fault_from_init_enters_pumpfault | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:f8f286722a1786991ddb5879a95dcacb1cddefe4a93f7e94ac4eb0a77b88d75f` |
| 2 | `1` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:fa931a7e3f291fba03a27d6a4972e5896113a336544bd45a3f50460ee52d2bd5` |
| 3 | `2` | ❌ | `SD-6` | cc_backmanual_forces_manual_from_pumpfault | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Keep all NL-required states, variables, events, guards, and existing required transitions, including the global forced CA_backManual, CB_backManual, CP_backManual, and CC_backM...<truncated 528 chars> | `sha256:fddc63ff4675e7e5e723a40bbc2155348192613831d43c2eaddf299acae4648d` |
| 4 | `2` | ❌ | `SD-6` | cc_backmanual_forces_manual_from_pumpfault | accept=1, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Do not reject this locked request. Continue repairing fixreq-2-sd6-0-01a4312604., Ensure BackManual from PumpFault executes an effect before Manual entry/during behavior so tha...<truncated 304 chars> | `sha256:755ad0fe1c1a1250313a82e8b039c5887f55a86bb21cfdf676de93081e486e84` |
| 5 | `2` | ✅ | `SD-6` | cc_backmanual_forces_manual_from_pumpfault | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=none, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=forced_transition_count_drift; missing_required_grounding | `sha256:4e2c880451936159cd68420023899a192ce50745282c5d4b38ecc761e709b456` |
| 6 | `3` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:94ad3dd3ec279dbf6be28e4a5ef9c715aa3a70019844dd7368a954eeebcbaedb` |
| 7 | `4` | ✅ | `SD-6` | cc_backmanual_forces_manual_from_pumpfault, pumpfault_ca_backmanual_exact_fault_clear_probe | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:4e2c880451936159cd68420023899a192ce50745282c5d4b38ecc761e709b456` |

<details><summary>Repair 1 / iteration `0` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`terminate_from_autocontrol_init_returns_manual, pump_fault_from_init_enters_pumpfault`。
- before_dsl_hash：`sha256:af4f21e14abe2bd34c7857ecddcc87506133613caeb2e4b69dd29c4ecb55d906`；candidate_dsl_hash：`sha256:f8f286722a1786991ddb5879a95dcacb1cddefe4a93f7e94ac4eb0a77b88d75f`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-a71f57456c3`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd6-0-6941aaba0a` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: TerminateAC from AutocontrolInit should override continued autocontrol and return to Manual.', 'name': 'terminate_from_autocontrol_init_returns_manual', 'setup_error': None, 'status': 'fail', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.AutocontrolNormal', 'actual_vars': {'CA_mode': 3, '_omitted_keys': 5, 'blood_pressure': 101, 'builtin_switch_speed': 2, 'flow_rate': 19, 'manual_flow_rate': 8, 'requested_target_bp': 120, 'sensor_buffer_bp': 101, 'target_bp': 120}, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'terminate_init_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': "{'expected': 0, 'actual': 3}", 'control_released': "{'expected': 1, 'actual': 0}", 'flow_rate': "{'expected': 8, 'actual': 19}", 'pump_speed': "{'expected': 2, 'actual': 0}"}}]}` |
| `fixreq-0-sd6-1-c6e52f5ee8` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: pump_fault positive during AutocontrolInit should enter PumpFault rather than continuing into normal control.', 'name': 'pump_fault_from_init_enters_pumpfault', 'setup_error': None, 'status': 'fail', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.AutocontrolNormal', 'actual_vars': {'CA_mode': 3, '_omitted_keys': 5, 'blood_pressure': 105, 'builtin_switch_speed': 0, 'flow_rate': 15, 'manual_flow_rate': 0, 'requested_target_bp': 120, 'sensor_buffer_bp': 105, 'target_bp': 120}, 'state_assertion_ok': False, 'status': 'fail', 'step_index': 0, 'step_name': 'init_fault_to_pumpfault', 'var_assertion_ok': False, 'var_mismatches': {'CA_mode': "{'expected': 4, 'actual': 3}", 'alarm_active': "{'expected': 1, 'actual': 0}", 'control_released': "{'expected': 1, 'actual': 0}"}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, variable:manual_flow_rate, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2162`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd6-0-6941aaba0a` | `accept` | ❌ | ❌ | The simulation evidence shows the unconditional AutocontrolInit -> AutocontrolNormal transition fires before the TerminateAC event transition when hot-started in AutocontrolInit. Reordering the AutocontrolInit outgoing transitions lets the explicit TerminateAC transition take precedence while preserving all required states, variables, events, and transitions...<truncated 128 chars> |
| `fixreq-0-sd6-1-c6e52f5ee8` | `accept` | ❌ | ❌ | The simulation evidence shows the unconditional AutocontrolInit -> AutocontrolNormal transition also masks the pump_fault guard. Reordering the guarded PumpFault transition before the unconditional normal-progress transition lets pump faults enter PumpFault as required.；intent=Move AutocontrolInit -> PumpFault : if [pump_fault > 0] before the unconditional A...<truncated 47 chars> |
- repair_rationale：The failure was caused by transition priority from AutocontrolInit: the unconditional transition to AutocontrolNormal was listed before the TerminateAC event and pump_fault guard transitions.；The smallest safe edit is to reorder only the AutocontrolInit outgoing transitions so explicit recovery/fault transitions are evaluated before the unconditional normal progression.；All required grounded states, variables, events, guards, and transitions are preserved.
- diff_summary：`{"summary": "Reordered AutocontrolInit outgoing transitions: TerminateAC and pump_fault guard now precede the unconditional transition to AutocontrolNormal."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 120;
def int requested_target_bp = 120;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int flow_rate = 0;
def int manual_flow_rate = 0;
def int builtin_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int control_released = 1;

state CARA {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            alarm_active = 0;
        }
        during {
            flow_rate = manual_flow_rate;
            pump_speed = builtin_switch_speed;
            sensor_buffer_bp = blood_pressure;
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
        }
        during {
            target_bp = requested_target_bp;
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            alarm_active = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 3;
            control_released = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            flow_rate = target_bp - blood_pressure;
            pump_speed = control_voltage;
        }
    }

    state PumpFault {
        enter {
            CA_mode = 4;
            alarm_active = 1;
            control_released = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> PumpFault : if [pump_fault > 0];
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
    };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -77,9 +77,9 @@
     Manual -> Ask_StartAC :: InitiateAC;
     Ask_StartAC -> AutocontrolInit :: StartAC;
     Ask_StartAC -> Manual :: TerminateAC;
-    AutocontrolInit -> AutocontrolNormal;
     AutocontrolInit -> Manual :: TerminateAC;
     AutocontrolInit -> PumpFault : if [pump_fault > 0];
+    AutocontrolInit -> AutocontrolNormal;
     AutocontrolNormal -> Manual :: TerminateAC;
     AutocontrolNormal -> PumpFault : if [pump_fault > 0];
     PumpFault -> Manual :: FaultRemoved effect {
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:c60c5eb91d5b72aaebe2116f574c3af8618065719e0d4dee6f5cebb06f64d730`。
  - SL-10 evidence 1: `{"summary": "Both hard-block SL-9 requests were accepted and repaired by the smallest edit: only the ordering of AutocontrolInit outgoing transitions changed. In the old DSL the unconditional AutocontrolInit -> AutocontrolNormal transition preceded TerminateAC and pump_fault, causing the two SD-6 hot-start simulation failures. In the candidate DSL, AutocontrolInit -> Manual :: TerminateAC and AutocontrolInit -> PumpFault : if [pump_fault > 0] now precede the unconditional AutocontrolInit -> AutocontrolNormal transition, so TerminateAC returns to Manual and pump_fault enters PumpFault before normal autocontrol progression."}`
  - SL-10 evidence 2: `{"summary": "The repair is consistent with the NL requirements: TerminateAC/algorithmic control termination must release software control and return to manual operation, and pump faults during control must activate alarm behavior and release control. The candidate preserves Manual enter behavior with CA_mode = 0, control_released = 1, manual flow, and switch-controlled pump speed; it preserves PumpFault enter behavior with CA_mode = 4, alarm_active = 1, and control_released = 1."}`
  - SL-10 evidence 3: `{"summary": "No NL-required states, variables, events, guards, or scenario obligations were dropped. The candidate still contains Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault; variables including CA_mode, target_bp, requested_target_bp, blood_pressure, sensor_buffer_bp, flow_rate, manual_flow_rate, builtin_switch_speed, pump_speed, control_voltage, pump_fault, alarm_active, and control_released; events InitiateAC, StartAC, TerminateAC, FaultRemoved, CA_backManual, CB_backManual, CP_backManual, and CC_backManual; the pump_fault > 0 guard; and all manual/autocontrol/fault/fallback transitions."}`
  - SL-10 evidence 4: `{"summary": "The local check reported major drift due to missing_required_grounding for required transitions, including initial_to_Manual, Manual_to_Ask_StartAC_InitiateAC, Ask_StartAC_to_AutocontrolInit_StartAC, Ask_StartAC_to_Manual_TerminateAC, AutocontrolInit_to_Manual_TerminateAC, AutocontrolNormal_to_Manual_TerminateAC, AutocontrolInit_to_PumpFault, AutocontrolNormal_to_PumpFault, PumpFault_to_Manual_FaultRemoved, and the four forced backManual transitions. This rejection is contradicted by direct inspection of the candidate DSL, where each listed transition is present with the same source, target, event/guard/effect semantics as required. The local finding is therefore treated as cons...<truncated 65 chars>`
  - SL-10 evidence 5: `{"summary": "The DSL diff is limited to reordering AutocontrolInit outgoing transitions. It does not change declarations, state bodies, effects, guard expressions, event names, or transition targets. Therefore there is no detected regression and no substantive model drift relative to the NL or FixLog ledger."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial_to_Manual", "transition:Manual_to_Ask_StartAC_InitiateAC", "transition:Ask_StartAC_to_AutocontrolInit_StartAC", "transition:Ask_StartAC_to_Manual_TerminateAC", "transition:AutocontrolInit_to_Manual_TerminateAC", "transition:AutocontrolNormal_to_Manual_TerminateAC", "transition:AutocontrolInit_to_PumpFault", "transition:AutocontrolNormal_to_PumpFault", "transition:PumpFault_to_Manual_FaultRemoved", "transition:forced_CA_backManual", "transition:forced_CB_backM...<truncated 116 chars>

</details>

<details><summary>Repair 2 / iteration `1` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:f8f286722a1786991ddb5879a95dcacb1cddefe4a93f7e94ac4eb0a77b88d75f`；candidate_dsl_hash：`sha256:fa931a7e3f291fba03a27d6a4972e5896113a336544bd45a3f50460ee52d2bd5`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Forced BackManual recovery can move from PumpFault to Manual with `pump_fault` still active and `alarm_active` cleared, allowing unsafe manual operation before fault removal.
- 2. `<unknown>` `` policy=``：The recovery behavior is not faithful to the NL because it permits alarm deactivation without fault removal.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-a8d11e75057`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sl7-0-3096823055` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['DSL: `! * -> Manual :: CC_backManual;` with Manual entry `alarm_active = 0`.', 'DSL: only `PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; }` clears the fault.', 'Simulation: `cc_backmanual_forces_manual_from_pumpfault` passes with `pump_fault: 1`, `alarm_active: 0`, and `actual_state: CARA.Manual`.', 'NL: pump fault activates alarm signals and the caregiver removes the fault.'], 'severity': 'major', 'summary': 'Forced BackManual recovery can move from PumpFault to Manual with `pump_fault` still active and `alarm_active` cleared, allowing unsafe manual operation before fault removal.'}` |
| `fixreq-1-sl7-1-f1f2c62158` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL requires pump fault alarm activation and caregiver fault removal.', 'DSL clears alarm on entering Manual through any BackManual event, independent of `FaultRemoved` and independent of `pump_fault`.'], 'severity': 'major', 'summary': 'The recovery behavior is not faithful to the NL because it permits alarm deactivation without fault removal.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, variable:manual_flow_rate, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2580`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sl7-0-3096823055` | `accept` | ❌ | ❌ | The evidence is valid: the global BackManual forced transitions can enter Manual while pump_fault remains active, and the old Manual entry unconditionally cleared alarm_active. The smallest safe repair is to make Manual preserve/raise the alarm when pump_fault is still active and prevent manual pump actuation until the fault is removed, while keeping BackMan...<truncated 256 chars> |
| `fixreq-1-sl7-1-f1f2c62158` | `accept` | ❌ | ❌ | The NL requires alarm activation on pump fault and caregiver fault removal. The old DSL allowed alarm deactivation simply by entering Manual through any BackManual event. The repair makes alarm deactivation conditional on pump_fault being cleared, preserving NL fidelity without deleting required states, events, guards, or recovery transitions.；intent=Keep al...<truncated 185 chars> |
- repair_rationale：Preserves all required states, variables, initial transition, InitiateAC/StartAC/TerminateAC transitions, pump_fault guards, and BackManual forced recovery behavior.；BackManual still causes CA_mode to become Manual, satisfying the cross-component fallback requirement.；Manual no longer clears the alarm while pump_fault is active, so alarm deactivation is tied to actual fault removal.；Manual pump actuation is inhibited while pump_fault is active, avoiding unsafe manual operation before caregiver removal of the fault.；A Manual FaultRemoved self-transition supports the case where software has already released control to Manual via BackManual and the caregiver then removes the fault.
- diff_summary：`{"summary": "Updated Manual entry/during logic to keep alarms active and inhibit pump output while pump_fault > 0, and added a Manual FaultRemoved self-transition to clear the fault/alarm after BackManual recovery."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 120;
def int requested_target_bp = 120;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int flow_rate = 0;
def int manual_flow_rate = 0;
def int builtin_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int control_released = 1;

state CARA {
    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;

    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault > 0] {
                alarm_active = 1;
            } else {
                alarm_active = 0;
            }
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault > 0] {
                alarm_active = 1;
                flow_rate = 0;
                pump_speed = 0;
            } else {
                alarm_active = 0;
                flow_rate = manual_flow_rate;
                pump_speed = builtin_switch_speed;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
        }
        during {
            target_bp = requested_target_bp;
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            alarm_active = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 3;
            control_released = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            flow_rate = target_bp - blood_pressure;
            pump_speed = control_voltage;
        }
    }

    state PumpFault {
        enter {
            CA_mode = 4;
            alarm_active = 1;
            control_released = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Manual -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> PumpFault : if [pump_fault > 0];
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
    };
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -24,12 +24,23 @@
         enter {
             CA_mode = 0;
             control_released = 1;
-            alarm_active = 0;
+            if [pump_fault > 0] {
+                alarm_active = 1;
+            } else {
+                alarm_active = 0;
+            }
         }
         during {
-            flow_rate = manual_flow_rate;
-            pump_speed = builtin_switch_speed;
             sensor_buffer_bp = blood_pressure;
+            if [pump_fault > 0] {
+                alarm_active = 1;
+                flow_rate = 0;
+                pump_speed = 0;
+            } else {
+                alarm_active = 0;
+                flow_rate = manual_flow_rate;
+                pump_speed = builtin_switch_speed;
+            }
         }
     }
 
@@ -75,6 +86,10 @@
     }
 
     Manual -> Ask_StartAC :: InitiateAC;
+    Manual -> Manual :: FaultRemoved effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
     Ask_StartAC -> AutocontrolInit :: StartAC;
     Ask_StartAC -> Manual :: TerminateAC;
     AutocontrolInit -> Manual :: TerminateAC;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:7e669d8db16d60a839217644bc157a173ceb0ed9ec6c679d5e0cd888a0d23c52`。
  - SL-10 evidence 1: `{"summary": "The accepted SL-9 repair directly addresses both hard-blocking SL-7 findings. In the candidate DSL, entering Manual via any BackManual event while pump_fault > 0 no longer clears alarm_active; Manual enter and during logic set alarm_active = 1 while the fault remains active. Manual during logic also inhibits pump output by setting flow_rate = 0 and pump_speed = 0 while pump_fault > 0, preventing unsafe manual operation before caregiver fault removal."}`
  - SL-10 evidence 2: `{"summary": "The NL requires pump fault alarm activation, caregiver removal of the fault, and release of software control when CARA was controlling the pump. The candidate preserves BackManual as the shared recovery target by keeping all four forced transitions to Manual, preserves control_released = 1 in Manual, and adds a Manual FaultRemoved self-transition so that if BackManual has already returned the system to Manual, the caregiver can still remove the active fault and clear pump_fault/alarm_active."}`
  - SL-10 evidence 3: `{"summary": "Required grounded states, variables, events, guards, and scenario obligations are preserved in the candidate DSL: Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, CA_mode, target/setpoint variables, blood pressure buffer, flow/pump variables, pump_fault, alarm_active, control_released, InitiateAC, StartAC, TerminateAC, FaultRemoved, pump_fault guards, and forced BackManual transitions remain present."}`
  - SL-10 evidence 4: `{"summary": "The local deterministic check reports major drift with scenario_regression and missing_required_grounding. The missing_required_grounding class is the same conservative local issue already overridden in the prior SL-10 pass, where the required transitions were visibly present in the DSL; the current candidate likewise visibly preserves those transitions and adds only a fault-removal self-transition in Manual. The reported scenario regression is not treated as an NL regression because the behavioral change is the requested safety repair: after BackManual with pump_fault still active, alarm and pump inhibition must persist until FaultRemoved rather than allowing alarm deactivation...<truncated 84 chars>`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 11, "n_scenarios_passed": 10, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: first cycle dispatches to Manual, where manual flow rate, built-in switch speed, and sensor buffer are applied.", "name": "default_init_enters_manual_and_uses_manual_controls", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Manual", "actual_vars": {"CA_mode": 0, "alarm_active": 0, "bloo...<truncated 10782 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial_to_Manual", "transition:Manual_to_Ask_StartAC_InitiateAC", "transition:Ask_StartAC_to_AutocontrolInit_StartAC", "transition:Ask_StartAC_to_Manual_TerminateAC", "transition:AutocontrolInit_to_Manual_TerminateAC", "transition:AutocontrolNormal_to_Manual_TerminateAC", "transition:AutocontrolInit_to_PumpFault", "transition:AutocontrolNormal_to_PumpFault", "transition:PumpFault_to_Manual_FaultRemoved", "transition:forced_CA_backManual", "transition:forced_CB_backM...<truncated 116 chars>

</details>

<details><summary>Repair 3 / iteration `2` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`cc_backmanual_forces_manual_from_pumpfault`。
- before_dsl_hash：`sha256:fa931a7e3f291fba03a27d6a4972e5896113a336544bd45a3f50460ee52d2bd5`；candidate_dsl_hash：`sha256:fddc63ff4675e7e5e723a40bbc2155348192613831d43c2eaddf299acae4648d`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-6c78e328186`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sd6-0-01a4312604` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual is a cross-component fallback that forces PumpFault to the shared Manual recovery target and silences alarm state.', 'name': 'cc_backmanual_forces_manual_from_pumpfault', 'setup_error': None, 'status': 'fail', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 88, 'builtin_switch_speed': 3, 'flow_rate': 0, 'manual_flow_rate': 7, 'requested_target_bp': 120, 'sensor_buffer_bp': 88, 'target_bp': 120}, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'cc_backmanual_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_active': "{'expected': 0, 'actual': 1}", 'flow_rate': "{'expected': 7, 'actual': 0}", 'pump_speed': "{'expected': 3, 'actual': 0}"}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, variable:manual_flow_rate, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3008`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sd6-0-01a4312604` | `accept` | ❌ | ❌ | The simulation evidence is valid: when hot-started in PumpFault, CC_backManual reaches Manual, but the current Manual entry/during logic still sees pump_fault active and therefore keeps the alarm asserted while inhibiting manual flow and switch speed. Forced transitions cannot carry effects, so the smallest safe repair is to add PumpFault-local BackManual re...<truncated 641 chars> |
- repair_rationale：The failing scenario reaches Manual through CC_backManual from PumpFault, but Manual still observes pump_fault > 0 and therefore asserts alarm_active and suppresses manual pump output.；Forced transitions cannot have effects, so adding ordinary PumpFault-local BackManual transitions provides the needed recovery effect before Manual entry/during executes.；The existing global forced BackManual transitions remain present as cross-component fallback coverage for all other active states.
- diff_summary：`{"summary": "Added PumpFault-local BackManual recovery transitions that clear pump_fault/alarm_active before entering Manual, and moved global forced BackManual fallbacks after ordinary transitions so these local effects take precedence from PumpFault."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 120;
def int requested_target_bp = 120;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int flow_rate = 0;
def int manual_flow_rate = 0;
def int builtin_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int control_released = 1;

state CARA {
    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault > 0] {
                alarm_active = 1;
            } else {
                alarm_active = 0;
            }
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault > 0] {
                alarm_active = 1;
                flow_rate = 0;
                pump_speed = 0;
            } else {
                alarm_active = 0;
                flow_rate = manual_flow_rate;
                pump_speed = builtin_switch_speed;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
        }
        during {
            target_bp = requested_target_bp;
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            alarm_active = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 3;
            control_released = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            flow_rate = target_bp - blood_pressure;
            pump_speed = control_voltage;
        }
    }

    state PumpFault {
        enter {
            CA_mode = 4;
            alarm_active = 1;
            control_released = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Manual -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> PumpFault : if [pump_fault > 0];
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: CA_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual :: CB_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual :: CP_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual :: CC_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
    };

    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -13,11 +13,6 @@
 def int control_released = 1;
 
 state CARA {
-    ! * -> Manual :: CA_backManual;
-    ! * -> Manual :: CB_backManual;
-    ! * -> Manual :: CP_backManual;
-    ! * -> Manual :: CC_backManual;
-
     [*] -> Manual;
 
     state Manual {
@@ -97,7 +92,28 @@
     AutocontrolInit -> AutocontrolNormal;
     AutocontrolNormal -> Manual :: TerminateAC;
     AutocontrolNormal -> PumpFault : if [pump_fault > 0];
+    PumpFault -> Manual :: CA_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+    PumpFault -> Manual :: CB_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+    PumpFault -> Manual :: CP_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+    PumpFault -> Manual :: CC_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
     PumpFault -> Manual :: FaultRemoved effect {
         pump_fault = 0;
     };
+
+    ! * -> Manual :: CA_backManual;
+    ! * -> Manual :: CB_backManual;
+    ! * -> Manual :: CP_backManual;
+    ! * -> Manual :: CC_backManual;
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:4773799a27f85810743e743720b39d1657e314cc8d8522130d6418c21471da66`。
  - SL-10 evidence 1: `{"summary": "The SL-9 edit intent is aligned with the NL and the request: from PumpFault, a BackManual fallback should recover to Manual and permit Manual operation after the fault/alarm has been cleared. However, the candidate implements PumpFault-local transitions using the same leaf event names as the existing global forced BackManual events, and the local check reports W_SHADOWED_EVENT diagnostics for this exact pattern. This is not merely cosmetic: it means the effectful PumpFault transition may be listening to a different source-local event than the cross-component fallback event required by the NL, leaving the original forced fallback to fire without clearing pump_fault/alarm_active."...<truncated 1 chars>`
  - SL-10 evidence 2: `{"summary": "The local deterministic evidence reports target_resolved=false, scenario_regression=true, and drift_risk=major for the current candidate. Unlike the repeated missing_required_grounding finding seen in prior iterations, which appears conservative because the named transitions are visibly present in the DSL, the new shadowed-event diagnostic is directly caused by the candidate diff and directly threatens the requested CC_backManual-from-PumpFault behavior."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves the NL-required states, variables, and global forced fallback transitions textually, but the new PumpFault-local BackManual transitions must be repaired so they are triggered by the same cross-component BackManual events as the global fallbacks. As written, the candidate cannot be accepted for the next full pass because the repair may not actually resolve the hot-start PumpFault CC_backManual scenario and has introduced a new blocking design ambiguity."}`
- SL-10 rework_instructions：Keep all NL-required states, variables, events, guards, and existing required transitions, including the global forced CA_backManual, CB_backManual, CP_backManual, and CC_backManual fallbacks to Manual.；Repair the PumpFault BackManual recovery transitions so they do not define or trigger source-local shadow events such as CARA.PumpFault.CC_backManual. They must listen to the same CARA-scope/cross-component BackManual events used by the global forced fallbacks, while still taking priority when the active state is PumpFault.；Use the correct pyfcstm event qualification/scope syntax for referencing the existing chain/root BackManual events from the PumpFault-specific transitions. Do not create duplicate local events with the same leaf names.；After the fix, a hot-start in PumpFault with CC_backManual must enter CARA.Manual with CA_mode = 0, control_released = 1, pump_fault = 0, alarm_active = 0, flow_rate = manual_flow_rate, and pump_speed = builtin_switch_speed after Manual entry/during behavior.；Keep the global forced BackManual fallbacks ordered after the ordinary PumpFault-specific recovery transitions if that ordering is required for PumpFault-specific effects to take precedence.；Do not undo the prior Manual safety behavior: Manual must still keep alarm_active asserted and inhibit flow_rate/pump_speed while pump_fault > 0, except when the validated BackManual/FaultRemoved recovery path has actually cleared the fault.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_SHADOWED_EVENT", "instance_key": "W_SHADOWED_EVENT:c60af7e5d001", "message": "Local event 'CARA.PumpFault.CA_backManual' shadows a chain event named 'CA_backManual'.", "policy_action": "requires_policy_classification", "pyfcstm_severity": "warning", "rationale": "", "refs": {"chain_path": "CARA.CA_backManual", "event_name": "CA_backManual", "local_path": "CARA.PumpFault.CA_backManual"}, "suggested_fix_hints": [{"do_not": ["...<truncated 3433 chars>
    - local evidence 2: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 13, "n_scenarios_passed": 12, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: first cycle dispatches to Manual, where manual flow rate, built-in switch speed, and sensor buffer are applied.", "name": "default_init_enters_manual_and_uses_manual_controls", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Manual", "actual_vars": {"CA_mode": 0, "alarm_active": 0, "bloo...<truncated 12349 chars>
    - local evidence 3: `missing_required_grounding` {"element_ids": ["transition:initial_to_Manual", "transition:Manual_to_Ask_StartAC_InitiateAC", "transition:Ask_StartAC_to_AutocontrolInit_StartAC", "transition:Ask_StartAC_to_Manual_TerminateAC", "transition:AutocontrolInit_to_Manual_TerminateAC", "transition:AutocontrolNormal_to_Manual_TerminateAC", "transition:AutocontrolInit_to_PumpFault", "transition:AutocontrolNormal_to_PumpFault", "transition:PumpFault_to_Manual_FaultRemoved", "transition:forced_CA_backManual", "transition:forced_CB_backM...<truncated 116 chars>

</details>

<details><summary>Repair 4 / iteration `2` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`cc_backmanual_forces_manual_from_pumpfault`。
- before_dsl_hash：`sha256:fa931a7e3f291fba03a27d6a4972e5896113a336544bd45a3f50460ee52d2bd5`；candidate_dsl_hash：`sha256:755ad0fe1c1a1250313a82e8b039c5887f55a86bb21cfdf676de93081e486e84`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-6c78e328186`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sd6-0-01a4312604` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual is a cross-component fallback that forces PumpFault to the shared Manual recovery target and silences alarm state.', 'name': 'cc_backmanual_forces_manual_from_pumpfault', 'setup_error': None, 'status': 'fail', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 88, 'builtin_switch_speed': 3, 'flow_rate': 0, 'manual_flow_rate': 7, 'requested_target_bp': 120, 'sensor_buffer_bp': 88, 'target_bp': 120}, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'cc_backmanual_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_active': "{'expected': 0, 'actual': 1}", 'flow_rate': "{'expected': 7, 'actual': 0}", 'pump_speed': "{'expected': 3, 'actual': 0}"}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, variable:manual_flow_rate, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3004`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sd6-0-01a4312604` | `accept` | ❌ | ✅ | The rework evidence is valid. PumpFault-specific BackManual recovery needs an effect to clear pump_fault before Manual entry/during logic runs, but using source-local :: BackManual events created shadowed events. The smallest safe repair is to add PumpFault-specific transitions that listen to the existing CARA-scope BackManual events with chain-scope ': Even...<truncated 441 chars> |
- repair_rationale：The failed scenario hot-starts in PumpFault and injects CC_backManual. Manual correctly inhibits pump output while pump_fault remains active, so the BackManual recovery path must clear the fault before Manual during behavior applies manual ...<truncated 22 chars>；Forced transitions cannot carry effects, so PumpFault-specific ordinary transitions are needed for the recovery effect.；The PumpFault-specific transitions use ': BackManualEvent' chain-scope syntax, so they listen to the same CARA-scope events as the global cross-component fallbacks and do not create source-local shadow events.；All required states, variables, required StartAC/TerminateAC/InitiateAC transitions, pump_fault guards, FaultRemoved handling, and global forced BackManual fallbacks are preserved.
- diff_summary：`{"summary": "Added PumpFault-specific chain-scope BackManual transitions to Manual with effects clearing pump_fault and alarm_active, and kept the global forced BackManual fallbacks after ordinary transitions while preserving Manual fault-safety behavior."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 120;
def int requested_target_bp = 120;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int flow_rate = 0;
def int manual_flow_rate = 0;
def int builtin_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int control_released = 1;

state CARA {
    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault > 0] {
                alarm_active = 1;
            } else {
                alarm_active = 0;
            }
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault > 0] {
                alarm_active = 1;
                flow_rate = 0;
                pump_speed = 0;
            } else {
                alarm_active = 0;
                flow_rate = manual_flow_rate;
                pump_speed = builtin_switch_speed;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
        }
        during {
            target_bp = requested_target_bp;
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            alarm_active = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 3;
            control_released = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            flow_rate = target_bp - blood_pressure;
            pump_speed = control_voltage;
        }
    }

    state PumpFault {
        enter {
            CA_mode = 4;
            alarm_active = 1;
            control_released = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Manual -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> PumpFault : if [pump_fault > 0];
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
    };
    PumpFault -> Manual : CA_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual : CB_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual : CP_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual : CC_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };

    ! * -> Manual :: CA_backManual;
    ! * -> Manual :: CB_backManual;
    ! * -> Manual :: CP_backManual;
    ! * -> Manual :: CC_backManual;
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -13,11 +13,6 @@
 def int control_released = 1;
 
 state CARA {
-    ! * -> Manual :: CA_backManual;
-    ! * -> Manual :: CB_backManual;
-    ! * -> Manual :: CP_backManual;
-    ! * -> Manual :: CC_backManual;
-
     [*] -> Manual;
 
     state Manual {
@@ -100,4 +95,25 @@
     PumpFault -> Manual :: FaultRemoved effect {
         pump_fault = 0;
     };
+    PumpFault -> Manual : CA_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+    PumpFault -> Manual : CB_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+    PumpFault -> Manual : CP_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+    PumpFault -> Manual : CC_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+
+    ! * -> Manual :: CA_backManual;
+    ! * -> Manual :: CB_backManual;
+    ! * -> Manual :: CP_backManual;
+    ! * -> Manual :: CC_backManual;
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:1de03fdbd2e07538e63cd3704aadd602829f7e026cc2059a03a0c3beb95ca17a`。
  - SL-10 evidence 1: `{"summary": "The NL requires BackManual events to recover to Manual, and the specific hard request requires hot-starting in PumpFault with CC_backManual to enter Manual with the fault/alarm cleared and manual flow/speed restored. The candidate adds PumpFault-specific BackManual transitions with clearing effects, but local deterministic evidence still reports target_resolved=false with scenario_regression: 12/13 scenarios pass and the same BackManual-from-PumpFault behavior remains unresolved."}`
  - SL-10 evidence 2: `{"summary": "The local new blocking design diagnostic W_FORCED_OVERRIDES_NORMAL is directly relevant, not merely conservative drift: the candidate keeps global forced '* -> Manual :: BackManual' transitions that duplicate the new PumpFault normal BackManual transitions. If forced transitions override normal transitions, the PumpFault-specific effect that clears pump_fault and alarm_active is bypassed, so Manual still inhibits flow_rate and pump_speed while alarm_active remains asserted. This matches the original failing scenario mechanism."}`
  - SL-10 evidence 3: `{"summary": "The candidate preserves the required states, variables, StartAC/TerminateAC/InitiateAC transitions, pump_fault guards, FaultRemoved path, and BackManual fallback declarations, so there is no evidence of NL element deletion. However, preserving the forced fallbacks as '*'-scoped transitions while also adding normal PumpFault transitions creates semantic conflict and fails the accepted SL-9 rework intent that PumpFault-specific recovery effects take priority."}`
  - SL-10 evidence 4: `{"summary": "The repeated missing_required_grounding report has appeared in prior accepted iterations and appears conservative because the listed transitions are visibly present in the DSL. It is not the primary rejection basis here. The rework is required because of the new forced-overrides-normal diagnostic and scenario regression tied to the hard simulation request."}`
- SL-10 rework_instructions：Do not reject this locked request. Continue repairing fixreq-2-sd6-0-01a4312604.；Ensure BackManual from PumpFault executes an effect before Manual entry/during behavior so that pump_fault = 0 and alarm_active = 0, allowing Manual to set flow_rate = manual_flow_rate and pump_speed = builtin_switch_speed.；Remove the semantic duplication where global forced '* -> Manual :: CA_backManual/CB_backManual/CP_backManual/CC_backManual' overrides the PumpFault-specific normal transitions. If the DSL supports scoped forced transitions or exclusions, restrict the forced BackManual fallbacks so they still cover all non-PumpFault active states while the PumpFault-specific...<truncated 40 chars>；Preserve the NL-required cross-component fallback behavior: CA_backManual, CB_backManual, CP_backManual, and CC_backManual must still cause CA_mode to become Manual from every relevant CARA mode, including PumpFault via the effectful PumpFault-specific path.；Do not create source-local shadow BackManual events. PumpFault-specific transitions must reference the same CARA-scope/cross-component BackManual events used by the fallback mechanism.；Keep all required states, variables, initial transition, InitiateAC/StartAC/TerminateAC transitions, pump_fault guards, FaultRemoved handling, Manual fault-safety behavior, and BackManual recovery coverage.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`new_blocking_design_diagnostic; scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `new_blocking_design_diagnostic` {"items": [{"budget_exhausted": false, "budget_remaining": 2, "code": "W_FORCED_OVERRIDES_NORMAL", "instance_key": "W_FORCED_OVERRIDES_NORMAL:from_path=CARA.PumpFault:to_path=CARA.Manual", "message": "Forced transition 'CARA.PumpFault' -> 'CARA.Manual' duplicates a normal transition.", "policy_action": "requires_policy_classification", "pyfcstm_severity": "warning", "rationale": "", "refs": {"forced_span": null, "from_path": "CARA.PumpFault", "normal_span": null, "to_path": "CARA.Manual"}, "sugg...<truncated 3941 chars>
    - local evidence 2: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 13, "n_scenarios_passed": 12, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: first cycle dispatches to Manual, where manual flow rate, built-in switch speed, and sensor buffer are applied.", "name": "default_init_enters_manual_and_uses_manual_controls", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Manual", "actual_vars": {"CA_mode": 0, "alarm_active": 0, "bloo...<truncated 12349 chars>
    - local evidence 3: `missing_required_grounding` {"element_ids": ["transition:initial_to_Manual", "transition:Manual_to_Ask_StartAC_InitiateAC", "transition:Ask_StartAC_to_AutocontrolInit_StartAC", "transition:Ask_StartAC_to_Manual_TerminateAC", "transition:AutocontrolInit_to_Manual_TerminateAC", "transition:AutocontrolNormal_to_Manual_TerminateAC", "transition:AutocontrolInit_to_PumpFault", "transition:AutocontrolNormal_to_PumpFault", "transition:PumpFault_to_Manual_FaultRemoved", "transition:forced_CA_backManual", "transition:forced_CB_backM...<truncated 116 chars>

</details>

<details><summary>Repair 5 / iteration `2` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`cc_backmanual_forces_manual_from_pumpfault`。
- before_dsl_hash：`sha256:fa931a7e3f291fba03a27d6a4972e5896113a336544bd45a3f50460ee52d2bd5`；candidate_dsl_hash：`sha256:4e2c880451936159cd68420023899a192ce50745282c5d4b38ecc761e709b456`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-6c78e328186`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sd6-0-01a4312604` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual is a cross-component fallback that forces PumpFault to the shared Manual recovery target and silences alarm state.', 'name': 'cc_backmanual_forces_manual_from_pumpfault', 'setup_error': None, 'status': 'fail', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 88, 'builtin_switch_speed': 3, 'flow_rate': 0, 'manual_flow_rate': 7, 'requested_target_bp': 120, 'sensor_buffer_bp': 88, 'target_bp': 120}, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'cc_backmanual_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_active': "{'expected': 0, 'actual': 1}", 'flow_rate': "{'expected': 7, 'actual': 0}", 'pump_speed': "{'expected': 3, 'actual': 0}"}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, variable:manual_flow_rate, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3600`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sd6-0-01a4312604` | `accept` | ❌ | ✅ | Accepted because the request is rework_locked and the evidence identifies a real PumpFault BackManual recovery failure. The smallest safe repair is to keep the PumpFault-specific effectful BackManual transitions, make them listen to the CARA-scope BackManual events using chain-scope ': Event' syntax, and restrict the forced BackManual fallbacks to the non-Pu...<truncated 777 chars> |
- repair_rationale：PumpFault-specific recovery must run an effect before Manual during behavior; otherwise pump_fault remains active and Manual correctly keeps the alarm asserted while inhibiting flow and pump speed.；The PumpFault-specific BackManual transitions use chain-scope ': Event' triggers, so they reference the shared CARA-scope BackManual events rather than creating source-local shadow events.；The former root-wide forced '* -> Manual' transitions are narrowed to non-PumpFault states to avoid forced/normal duplication for PumpFault while preserving cross-component fallback behavior for Manual, Ask_StartAC, AutocontrolInit, and Aut...<truncated 15 chars>；Manual fault-safety behavior is preserved: if pump_fault is still active, alarm_active remains asserted and manual pump actuation is inhibited until a validated recovery path clears the fault.
- diff_summary：`{"summary": "Added effectful PumpFault BackManual transitions using chain-scope shared events, and replaced root-wide forced BackManual fallbacks with scoped forced fallbacks for non-PumpFault modes to avoid overriding the PumpFault recovery effect."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 120;
def int requested_target_bp = 120;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int flow_rate = 0;
def int manual_flow_rate = 0;
def int builtin_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int control_released = 1;

state CARA {
    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault > 0] {
                alarm_active = 1;
            } else {
                alarm_active = 0;
            }
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault > 0] {
                alarm_active = 1;
                flow_rate = 0;
                pump_speed = 0;
            } else {
                alarm_active = 0;
                flow_rate = manual_flow_rate;
                pump_speed = builtin_switch_speed;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
        }
        during {
            target_bp = requested_target_bp;
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            alarm_active = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 3;
            control_released = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            flow_rate = target_bp - blood_pressure;
            pump_speed = control_voltage;
        }
    }

    state PumpFault {
        enter {
            CA_mode = 4;
            alarm_active = 1;
            control_released = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Manual -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> PumpFault : if [pump_fault > 0];
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
    };
    PumpFault -> Manual : CA_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual : CB_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual : CP_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual : CC_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };

    ! Manual -> Manual : CA_backManual;
    ! Ask_StartAC -> Manual : CA_backManual;
    ! AutocontrolInit -> Manual : CA_backManual;
    ! AutocontrolNormal -> Manual : CA_backManual;
    ! Manual -> Manual : CB_backManual;
    ! Ask_StartAC -> Manual : CB_backManual;
    ! AutocontrolInit -> Manual : CB_backManual;
    ! AutocontrolNormal -> Manual : CB_backManual;
    ! Manual -> Manual : CP_backManual;
    ! Ask_StartAC -> Manual : CP_backManual;
    ! AutocontrolInit -> Manual : CP_backManual;
    ! AutocontrolNormal -> Manual : CP_backManual;
    ! Manual -> Manual : CC_backManual;
    ! Ask_StartAC -> Manual : CC_backManual;
    ! AutocontrolInit -> Manual : CC_backManual;
    ! AutocontrolNormal -> Manual : CC_backManual;
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -13,11 +13,6 @@
 def int control_released = 1;
 
 state CARA {
-    ! * -> Manual :: CA_backManual;
-    ! * -> Manual :: CB_backManual;
-    ! * -> Manual :: CP_backManual;
-    ! * -> Manual :: CC_backManual;
-
     [*] -> Manual;
 
     state Manual {
@@ -100,4 +95,37 @@
     PumpFault -> Manual :: FaultRemoved effect {
         pump_fault = 0;
     };
+    PumpFault -> Manual : CA_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+    PumpFault -> Manual : CB_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+    PumpFault -> Manual : CP_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+    PumpFault -> Manual : CC_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+
+    ! Manual -> Manual : CA_backManual;
+    ! Ask_StartAC -> Manual : CA_backManual;
+    ! AutocontrolInit -> Manual : CA_backManual;
+    ! AutocontrolNormal -> Manual : CA_backManual;
+    ! Manual -> Manual : CB_backManual;
+    ! Ask_StartAC -> Manual : CB_backManual;
+    ! AutocontrolInit -> Manual : CB_backManual;
+    ! AutocontrolNormal -> Manual : CB_backManual;
+    ! Manual -> Manual : CP_backManual;
+    ! Ask_StartAC -> Manual : CP_backManual;
+    ! AutocontrolInit -> Manual : CP_backManual;
+    ! AutocontrolNormal -> Manual : CP_backManual;
+    ! Manual -> Manual : CC_backManual;
+    ! Ask_StartAC -> Manual : CC_backManual;
+    ! AutocontrolInit -> Manual : CC_backManual;
+    ! AutocontrolNormal -> Manual : CC_backManual;
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`none`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:c017922a080ed04c2315365798aae15a24209c3af702a9904f0dd76235fbdd18`。
  - SL-10 evidence 1: `{"summary": "The candidate directly implements the locked SL-9 rework intent for fixreq-2-sd6-0-01a4312604: PumpFault now has effectful BackManual transitions for CA_backManual, CB_backManual, CP_backManual, and CC_backManual using chain-scope ':' triggers, and those effects clear pump_fault and alarm_active before entering Manual. After Manual entry/during behavior, this yields the requested recovery target with CA_mode = 0, control_released = 1, alarm_active = 0, flow_rate = manual_flow_rate, and pump_speed = builtin_switch_speed when the BackManual recovery path has cleared the fault."}`
  - SL-10 evidence 2: `{"summary": "The NL-required states and variables are preserved: Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, CA_mode, target_bp, requested_target_bp, blood_pressure, sensor_buffer_bp, flow_rate, manual_flow_rate, builtin_switch_speed, pump_speed, control_voltage, pump_fault, alarm_active, and control_released all remain concretely represented. Required InitiateAC, StartAC, TerminateAC, pump_fault guarded transitions, initial Manual entry, and FaultRemoved handling are also still present."}`
  - SL-10 evidence 3: `{"summary": "The local rejection reason 'forced_transition_count_drift' is an expected consequence of the prior SL-10 rework instruction, not an NL regression: the former root-wide '* -> Manual' forced fallbacks expanded over PumpFault and overrode the new effectful PumpFault recovery transitions. The candidate intentionally narrows forced fallbacks to Manual, Ask_StartAC, AutocontrolInit, and AutocontrolNormal while adding ordinary effectful PumpFault BackManual transitions. This preserves the NL cross-component fallback obligation that CA_backManual, CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual from every relevant mode, including PumpFault via the effectfu...<truncated 9 chars>`
  - SL-10 evidence 4: `{"summary": "The local 'missing_required_grounding' evidence appears to be a conservative grounding detector artifact: the candidate text still contains the required grounded transitions and events, including [*] -> Manual, Manual -> Ask_StartAC on InitiateAC, Ask_StartAC -> AutocontrolInit on StartAC, TerminateAC returns to Manual, guarded AutocontrolInit/AutocontrolNormal transitions to PumpFault, PumpFault/Manual FaultRemoved recovery, and BackManual recovery coverage. The DSL diff does not delete NL-required behavior; it changes only the scoping/coverage of forced BackManual declarations to avoid PumpFault override while preserving shared recovery semantics."}`
  - SL-10 evidence 5: `{"summary": "No scenario regression is reported in the current local evidence, and the earlier shadow-event and forced-overrides-normal diagnostics have been addressed by using chain-scope BackManual triggers and excluding PumpFault from the forced fallback declarations. Manual fault-safety behavior from earlier accepted fixes is preserved: Manual continues to keep alarm_active asserted and inhibit flow_rate/pump_speed while pump_fault > 0, except when a validated recovery path such as BackManual from PumpFault or FaultRemoved clears the fault."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`forced_transition_count_drift; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `forced_transition_count_drift` {"fix_target": "sim", "kind": "forced_transition_count_drift", "new": 16, "old": 20}
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial_to_Manual", "transition:Manual_to_Ask_StartAC_InitiateAC", "transition:Ask_StartAC_to_AutocontrolInit_StartAC", "transition:Ask_StartAC_to_Manual_TerminateAC", "transition:AutocontrolInit_to_Manual_TerminateAC", "transition:AutocontrolNormal_to_Manual_TerminateAC", "transition:AutocontrolInit_to_PumpFault", "transition:AutocontrolNormal_to_PumpFault", "transition:PumpFault_to_Manual_FaultRemoved", "transition:forced_CA_backManual", "transition:forced_CB_backM...<truncated 116 chars>

</details>

<details><summary>Repair 6 / iteration `3` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:4e2c880451936159cd68420023899a192ce50745282c5d4b38ecc761e709b456`；candidate_dsl_hash：`sha256:94ad3dd3ec279dbf6be28e4a5ef9c715aa3a70019844dd7368a954eeebcbaedb`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：BackManual recovery from PumpFault clears the physical/software fault and alarm state without requiring the NL-described caregiver fault-removal event.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-1d257c6524c`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sl7-0-65d2e7f559` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL requires caregiver removal after pump fault: "the caregiver removes the fault".', 'DSL backManual transitions from PumpFault clear `pump_fault = 0` and `alarm_active = 0`.', 'This can represent recovery by mode fallback alone rather than by fault removal, which is unsafe for a pump-fault scenario.'], 'severity': 'major', 'summary': 'BackManual recovery from PumpFault clears the physical/software fault and alarm state without requiring the NL-described caregiver fault-removal event.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, variable:manual_flow_rate, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3340`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sl7-0-65d2e7f559` | `accept` | ❌ | ❌ | The review evidence is valid. The PumpFault BackManual transitions should provide cross-component fallback to Manual and release software control, but they should not themselves clear the physical/software pump fault or alarm; the NL requires caregiver fault removal. The smallest safe edit is to keep the PumpFault-to-Manual BackManual recovery paths using th...<truncated 570 chars> |
- repair_rationale：BackManual remains a shared recovery event that moves CA_mode to Manual from PumpFault and other relevant modes.；BackManual from PumpFault no longer clears pump_fault or alarm_active; therefore fallback alone cannot represent caregiver removal of a physical pump fault.；Manual entry/during behavior is preserved so an uncleared pump_fault keeps alarm_active asserted and inhibits flow_rate and pump_speed.；FaultRemoved remains the explicit caregiver fault-removal path that clears pump_fault before Manual behavior resumes normal manual pump operation.
- diff_summary：`{"summary": "Removed pump_fault/alarm clearing effects from the PumpFault CA_backManual, CB_backManual, CP_backManual, and CC_backManual transitions while preserving shared BackManual fallback to Manual and FaultRemoved clearing behavior."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 120;
def int requested_target_bp = 120;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int flow_rate = 0;
def int manual_flow_rate = 0;
def int builtin_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int control_released = 1;

state CARA {
    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault > 0] {
                alarm_active = 1;
            } else {
                alarm_active = 0;
            }
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault > 0] {
                alarm_active = 1;
                flow_rate = 0;
                pump_speed = 0;
            } else {
                alarm_active = 0;
                flow_rate = manual_flow_rate;
                pump_speed = builtin_switch_speed;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
        }
        during {
            target_bp = requested_target_bp;
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            alarm_active = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 3;
            control_released = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            flow_rate = target_bp - blood_pressure;
            pump_speed = control_voltage;
        }
    }

    state PumpFault {
        enter {
            CA_mode = 4;
            alarm_active = 1;
            control_released = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Manual -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> PumpFault : if [pump_fault > 0];
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
    };
    PumpFault -> Manual : CA_backManual;
    PumpFault -> Manual : CB_backManual;
    PumpFault -> Manual : CP_backManual;
    PumpFault -> Manual : CC_backManual;

    ! Manual -> Manual : CA_backManual;
    ! Ask_StartAC -> Manual : CA_backManual;
    ! AutocontrolInit -> Manual : CA_backManual;
    ! AutocontrolNormal -> Manual : CA_backManual;
    ! Manual -> Manual : CB_backManual;
    ! Ask_StartAC -> Manual : CB_backManual;
    ! AutocontrolInit -> Manual : CB_backManual;
    ! AutocontrolNormal -> Manual : CB_backManual;
    ! Manual -> Manual : CP_backManual;
    ! Ask_StartAC -> Manual : CP_backManual;
    ! AutocontrolInit -> Manual : CP_backManual;
    ! AutocontrolNormal -> Manual : CP_backManual;
    ! Manual -> Manual : CC_backManual;
    ! Ask_StartAC -> Manual : CC_backManual;
    ! AutocontrolInit -> Manual : CC_backManual;
    ! AutocontrolNormal -> Manual : CC_backManual;
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -95,22 +95,10 @@
     PumpFault -> Manual :: FaultRemoved effect {
         pump_fault = 0;
     };
-    PumpFault -> Manual : CA_backManual effect {
-        pump_fault = 0;
-        alarm_active = 0;
-    };
-    PumpFault -> Manual : CB_backManual effect {
-        pump_fault = 0;
-        alarm_active = 0;
-    };
-    PumpFault -> Manual : CP_backManual effect {
-        pump_fault = 0;
-        alarm_active = 0;
-    };
-    PumpFault -> Manual : CC_backManual effect {
-        pump_fault = 0;
-        alarm_active = 0;
-    };
+    PumpFault -> Manual : CA_backManual;
+    PumpFault -> Manual : CB_backManual;
+    PumpFault -> Manual : CP_backManual;
+    PumpFault -> Manual : CC_backManual;
 
     ! Manual -> Manual : CA_backManual;
     ! Ask_StartAC -> Manual : CA_backManual;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:2dda6739997f9a7fbe693377634f0c18755b913690f6418666d98327eb2c22ab`。
  - SL-10 evidence 1: `{"summary": "The hard SL-7 request is resolved: the candidate removes the pump_fault = 0 and alarm_active = 0 effects from the PumpFault CA_backManual, CB_backManual, CP_backManual, and CC_backManual transitions. BackManual from PumpFault still moves CARA to Manual and releases software control through Manual entry/control_released behavior, but it no longer represents caregiver removal of a physical pump fault. This matches the NL requirement that after a pump fault the caregiver removes the fault, and avoids the unsafe recovery identified by SL-7."}`
  - SL-10 evidence 2: `{"summary": "The NL-required caregiver fault-removal path is preserved through PumpFault -> Manual :: FaultRemoved effect { pump_fault = 0; }. After FaultRemoved, Manual entry/during behavior sees pump_fault = 0 and clears alarm_active while restoring manual flow and switch-speed behavior. Thus fault clearing remains tied to the explicit caregiver-removal event rather than to cross-component BackManual fallback."}`
  - SL-10 evidence 3: `{"summary": "All grounded required states and variables remain present in the candidate DSL, including Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, PumpFault, CA_mode, target_bp, requested_target_bp, blood_pressure, sensor_buffer_bp, flow_rate, manual_flow_rate, builtin_switch_speed, pump_speed, control_voltage, pump_fault, alarm_active, and control_released."}`
  - SL-10 evidence 4: `{"summary": "All required mode-control and fault transitions remain concretely represented in the candidate DSL: initial_to_Manual, Manual_to_Ask_StartAC_InitiateAC, Ask_StartAC_to_AutocontrolInit_StartAC, Ask_StartAC_to_Manual_TerminateAC, AutocontrolInit_to_Manual_TerminateAC, AutocontrolNormal_to_Manual_TerminateAC, AutocontrolInit_to_PumpFault and AutocontrolNormal_to_PumpFault guarded by pump_fault > 0, PumpFault_to_Manual_FaultRemoved, and the BackManual recovery coverage."}`
  - SL-10 evidence 5: `{"summary": "The local deterministic check reports scenario_regression and drift_risk = major because previous scenarios expected PumpFault BackManual to clear pump_fault/alarm_active and restore manual pump output. That expectation directly conflicts with the current hard SL-7 model-review finding and the NL phrase that the caregiver removes the fault. The failed local scenarios are therefore treated as stale-oracle evidence from the earlier, now-rejected recovery interpretation, not as an NL regression."}`
  - SL-10 evidence 6: `{"summary": "The local missing_required_grounding finding is not supported by the visible DSL: the listed transitions are present textually in the candidate. This same grounding diagnostic appeared in prior iterations and was previously overridden as conservative/local evidence; no candidate edit deletes those NL-required elements."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 23, "n_scenarios_passed": 21, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init: first cycle dispatches to Manual, where manual flow rate, built-in switch speed, and sensor buffer are applied.", "name": "default_init_enters_manual_and_uses_manual_controls", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Manual", "actual_vars": {"CA_mode": 0, "alarm_active": 0, "bloo...<truncated 20596 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["transition:initial_to_Manual", "transition:Manual_to_Ask_StartAC_InitiateAC", "transition:Ask_StartAC_to_AutocontrolInit_StartAC", "transition:Ask_StartAC_to_Manual_TerminateAC", "transition:AutocontrolInit_to_Manual_TerminateAC", "transition:AutocontrolNormal_to_Manual_TerminateAC", "transition:AutocontrolInit_to_PumpFault", "transition:AutocontrolNormal_to_PumpFault", "transition:PumpFault_to_Manual_FaultRemoved", "transition:forced_CA_backManual", "transition:forced_CB_backM...<truncated 116 chars>

</details>

<details><summary>Repair 7 / iteration `4` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`cc_backmanual_forces_manual_from_pumpfault, pumpfault_ca_backmanual_exact_fault_clear_probe`。
- before_dsl_hash：`sha256:94ad3dd3ec279dbf6be28e4a5ef9c715aa3a70019844dd7368a954eeebcbaedb`；candidate_dsl_hash：`sha256:4e2c880451936159cd68420023899a192ce50745282c5d4b38ecc761e709b456`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-4-sha256-b72cdbf75ec`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-4-sd6-0-49d1dc9562` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CC_backManual is a cross-component fallback that forces PumpFault to the shared Manual recovery target and silences alarm state.', 'name': 'cc_backmanual_forces_manual_from_pumpfault', 'setup_error': None, 'status': 'fail', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 88, 'builtin_switch_speed': 3, 'flow_rate': 0, 'manual_flow_rate': 7, 'requested_target_bp': 120, 'sensor_buffer_bp': 88, 'target_bp': 120}, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'cc_backmanual_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_active': "{'expected': 0, 'actual': 1}", 'flow_rate': "{'expected': 7, 'actual': 0}", 'pump_speed': "{'expected': 3, 'actual': 0}"}}]}` |
| `fixreq-4-sd6-1-86269f603c` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start: CA_backManual from PumpFault is a recovery-to-Manual transition whose effect must clear pump_fault exactly to 0, catching missing or wrong effect values on the backManual recovery path.', 'name': 'pumpfault_ca_backmanual_exact_fault_clear_probe', 'setup_error': None, 'status': 'fail', 'step_results': [{'_omitted_keys': 1, 'actual_state': 'CARA.Manual', 'actual_vars': {'CA_mode': 0, '_omitted_keys': 5, 'blood_pressure': 109, 'builtin_switch_speed': 11, 'flow_rate': 0, 'manual_flow_rate': 19, 'requested_target_bp': 120, 'sensor_buffer_bp': 109, 'target_bp': 120}, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'pumpfault_ca_backmanual_exact_clear', 'var_assertion_ok': False, 'var_mismatches': {'alarm_active': "{'expected': 0, 'actual': 1}", 'flow_rate': "{'expected': 19, 'actual': 0}", 'pump_fault': "{'expected': 0, 'actual': 6}", 'pump_speed': "{'expected': 11, 'actual': 0}"}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, state:PumpFault, variable:CA_mode, variable:target_bp, variable:requested_target_bp, variable:blood_pressure, variable:sensor_buffer_bp, variable:flow_rate, variable:manual_flow_rate, ... +29`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`3600`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-4-sd6-0-49d1dc9562` | `accept` | ❌ | ❌ | The simulation evidence is valid: CC_backManual from PumpFault reaches Manual, but because pump_fault is not cleared before Manual entry/during logic, Manual correctly keeps the alarm asserted and inhibits manual flow and switch speed. The smallest safe edit is to add a PumpFault-specific effect on the shared CC_backManual recovery transition that clears pum...<truncated 475 chars> |
| `fixreq-4-sd6-1-86269f603c` | `accept` | ❌ | ❌ | The simulation evidence is valid: CA_backManual from PumpFault must be an effectful recovery path that clears pump_fault exactly to 0 before Manual behavior runs. Forced transitions cannot carry effects, and the current scoped forced transitions already avoid duplicating PumpFault, so the minimal repair is to add the clearing effect to the PumpFault-specific...<truncated 480 chars> |
- repair_rationale：Accepted both hard simulation requests because the current PumpFault BackManual paths reach Manual but do not clear pump_fault before Manual entry/during behavior.；Added effect blocks only to the PumpFault-specific BackManual transitions, because forced transitions cannot carry effects and the existing forced fallbacks are already scoped to non-PumpFault modes.；Kept BackManual events chain-scoped with ': Event' so the PumpFault-specific transitions listen to the shared CARA-scope fallback events rather than creating source-local shadow events.；Preserved Manual fault-safety behavior for cases where pump_fault remains active through other paths, and preserved FaultRemoved, required states, variables, initial transition, InitiateAC, StartAC, TerminateAC, and pump_fault guard transit...<truncated 5 chars>
- diff_summary：`{"summary": "Added pump_fault = 0 and alarm_active = 0 effects to the PumpFault-to-Manual CA_backManual, CB_backManual, CP_backManual, and CC_backManual transitions; preserved all other structure and scoped forced BackManual fallbacks."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def int CA_mode = 0;
def int target_bp = 120;
def int requested_target_bp = 120;
def int blood_pressure = 0;
def int sensor_buffer_bp = 0;
def int flow_rate = 0;
def int manual_flow_rate = 0;
def int builtin_switch_speed = 0;
def int pump_speed = 0;
def int control_voltage = 0;
def int pump_fault = 0;
def int alarm_active = 0;
def int control_released = 1;

state CARA {
    [*] -> Manual;

    state Manual {
        enter {
            CA_mode = 0;
            control_released = 1;
            if [pump_fault > 0] {
                alarm_active = 1;
            } else {
                alarm_active = 0;
            }
        }
        during {
            sensor_buffer_bp = blood_pressure;
            if [pump_fault > 0] {
                alarm_active = 1;
                flow_rate = 0;
                pump_speed = 0;
            } else {
                alarm_active = 0;
                flow_rate = manual_flow_rate;
                pump_speed = builtin_switch_speed;
            }
        }
    }

    state Ask_StartAC {
        enter {
            CA_mode = 1;
        }
        during {
            target_bp = requested_target_bp;
            sensor_buffer_bp = blood_pressure;
        }
    }

    state AutocontrolInit {
        enter {
            CA_mode = 2;
            control_released = 0;
            alarm_active = 0;
        }
    }

    state AutocontrolNormal {
        enter {
            CA_mode = 3;
            control_released = 0;
        }
        during {
            sensor_buffer_bp = blood_pressure;
            flow_rate = target_bp - blood_pressure;
            pump_speed = control_voltage;
        }
    }

    state PumpFault {
        enter {
            CA_mode = 4;
            alarm_active = 1;
            control_released = 1;
        }
        during {
            sensor_buffer_bp = blood_pressure;
        }
    }

    Manual -> Ask_StartAC :: InitiateAC;
    Manual -> Manual :: FaultRemoved effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    Ask_StartAC -> AutocontrolInit :: StartAC;
    Ask_StartAC -> Manual :: TerminateAC;
    AutocontrolInit -> Manual :: TerminateAC;
    AutocontrolInit -> PumpFault : if [pump_fault > 0];
    AutocontrolInit -> AutocontrolNormal;
    AutocontrolNormal -> Manual :: TerminateAC;
    AutocontrolNormal -> PumpFault : if [pump_fault > 0];
    PumpFault -> Manual :: FaultRemoved effect {
        pump_fault = 0;
    };
    PumpFault -> Manual : CA_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual : CB_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual : CP_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };
    PumpFault -> Manual : CC_backManual effect {
        pump_fault = 0;
        alarm_active = 0;
    };

    ! Manual -> Manual : CA_backManual;
    ! Ask_StartAC -> Manual : CA_backManual;
    ! AutocontrolInit -> Manual : CA_backManual;
    ! AutocontrolNormal -> Manual : CA_backManual;
    ! Manual -> Manual : CB_backManual;
    ! Ask_StartAC -> Manual : CB_backManual;
    ! AutocontrolInit -> Manual : CB_backManual;
    ! AutocontrolNormal -> Manual : CB_backManual;
    ! Manual -> Manual : CP_backManual;
    ! Ask_StartAC -> Manual : CP_backManual;
    ! AutocontrolInit -> Manual : CP_backManual;
    ! AutocontrolNormal -> Manual : CP_backManual;
    ! Manual -> Manual : CC_backManual;
    ! Ask_StartAC -> Manual : CC_backManual;
    ! AutocontrolInit -> Manual : CC_backManual;
    ! AutocontrolNormal -> Manual : CC_backManual;
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -95,10 +95,22 @@
     PumpFault -> Manual :: FaultRemoved effect {
         pump_fault = 0;
     };
-    PumpFault -> Manual : CA_backManual;
-    PumpFault -> Manual : CB_backManual;
-    PumpFault -> Manual : CP_backManual;
-    PumpFault -> Manual : CC_backManual;
+    PumpFault -> Manual : CA_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+    PumpFault -> Manual : CB_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+    PumpFault -> Manual : CP_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
+    PumpFault -> Manual : CC_backManual effect {
+        pump_fault = 0;
+        alarm_active = 0;
+    };
 
     ! Manual -> Manual : CA_backManual;
     ! Ask_StartAC -> Manual : CA_backManual;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:561931028a6b115dd9c17ec02f8a7ac3d171dc76849a581a7a4fa43b0a0fc975`。
  - SL-10 evidence 1: `{"summary": "Both current hard SD-6 simulation requests are addressed by the candidate diff: PumpFault -> Manual on CA_backManual, CB_backManual, CP_backManual, and CC_backManual now has effects setting pump_fault = 0 and alarm_active = 0 before Manual entry/during behavior, so Manual can set flow_rate = manual_flow_rate and pump_speed = builtin_switch_speed. This directly resolves the reported CA_backManual and CC_backManual mismatches for pump_fault, alarm_active, flow_rate, and pump_speed."}`
  - SL-10 evidence 2: `{"summary": "The candidate preserves the NL-required CARA structure and behavior: Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, and PumpFault states remain; CA_mode, blood-pressure/setpoint, sensor buffer, flow, manual pump controls, control voltage, pump_fault, alarm_active, and control_released variables remain; InitiateAC, StartAC, TerminateAC, pump_fault-guarded transitions, FaultRemoved handling, and cross-component BackManual recovery coverage remain."}`
  - SL-10 evidence 3: `{"summary": "The BackManual repair is consistent enough for the next full top-down revalidation pass because the NL requires cross-component fallback events, including CA_backManual and CC_backManual, to make CA_mode become Manual as the shared recovery target after pump complications. In this candidate, PumpFault-specific BackManual transitions use the shared chain-scope events and perform the required recovery cleanup before Manual behavior runs, while scoped forced BackManual fallbacks remain for non-PumpFault modes."}`
  - SL-10 evidence 4: `{"summary": "Local SD-10 rejected only for missing_required_grounding with drift_risk='major', but the cited required elements are visibly present in the candidate DSL: the initial transition, InitiateAC/StartAC/TerminateAC transitions, pump_fault transitions, FaultRemoved transition, and forced CA/CB/CP/CC BackManual transitions are all still represented. There is no local scenario_regression in the current evidence, and the reported missing grounding appears to be a conservative traceability/matcher issue rather than an actual DSL deletion."}`
  - SL-10 evidence 5: `{"summary": "The FixLog ledger shows this area has oscillated between two interpretations: preserving fault until FaultRemoved versus clearing it on PumpFault BackManual. The current hard sim batch specifically tests the latter and SL-9 accepted both hard requests with a minimal, localized edit. Because no required NL element is dropped and the current local failure is limited to apparent grounding recognition rather than behavioral regression, the candidate should proceed to full revalidation rather than be sent back for the same edit again."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["transition:initial_to_Manual", "transition:Manual_to_Ask_StartAC_InitiateAC", "transition:Ask_StartAC_to_AutocontrolInit_StartAC", "transition:Ask_StartAC_to_Manual_TerminateAC", "transition:AutocontrolInit_to_Manual_TerminateAC", "transition:AutocontrolNormal_to_Manual_TerminateAC", "transition:AutocontrolInit_to_PumpFault", "transition:AutocontrolNormal_to_PumpFault", "transition:PumpFault_to_Manual_FaultRemoved", "transition:forced_CA_backManual", "transition:forced_CB_backM...<truncated 116 chars>

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-a71f57456c3` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-a71f57456c3` | accept=2, reject=0 | `sl10_review` | `sha256:f8f286722a1786991ddb5879a95dcacb1cddefe4a93f7e94ac4eb0a77b88d75f` | The failure was caused by transition priority from AutocontrolInit: the unconditional transition to AutocontrolNormal was listed before the TerminateAC event and pump_fault guard transitions., The smallest safe edit is to reorder only the AutocontrolInit outgoing transitions so explicit recovery/fault transitions are evaluated before the unconditional normal progression., All required grounded states, variables, events, guards, and transitions are preserved. |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-a71f57456c3` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:f8f286722a1786991ddb5879a95dcacb1cddefe4a93f7e94ac4eb0a77b88d75f` | <none> |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-a8d11e75057` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-a8d11e75057` | accept=2, reject=0 | `sl10_review` | `sha256:fa931a7e3f291fba03a27d6a4972e5896113a336544bd45a3f50460ee52d2bd5` | Preserves all required states, variables, initial transition, InitiateAC/StartAC/TerminateAC transitions, pump_fault guards, and BackManual forced recovery behavior., BackManual still causes CA_mode to become Manual, satisfying the cross-component fallback requirement., Manual no longer clears the alarm while pump_fault is active, so alarm deactivation is tied to actual fault removal., ... +2 |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-a8d11e75057` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:fa931a7e3f291fba03a27d6a4972e5896113a336544bd45a3f50460ee52d2bd5` | <none> |
| 7 | `2` | `request_batch` | `fixbatch-2-sha256-6c78e328186` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 8 | `2` | `sl9_decision` | `fixbatch-2-sha256-6c78e328186` | accept=1, reject=0 | `sl10_review` | `sha256:fddc63ff4675e7e5e723a40bbc2155348192613831d43c2eaddf299acae4648d` | The failing scenario reaches Manual through CC_backManual from PumpFault, but Manual still observes pump_fault > 0 and therefore asserts alarm_active and suppresses manual pump output., Forced transitions cannot have effects, so adding ordinary PumpFault-local BackManual transitions provides the needed recovery effect before Manual entry/during executes., The existing global forced BackManual transitions remain present as cross-component fallback coverage for all other active states. |
| 9 | `2` | `sl10_review` | `fixbatch-2-sha256-6c78e328186` | accept=1, reject=0 | `sl9_rework` | `sha256:fddc63ff4675e7e5e723a40bbc2155348192613831d43c2eaddf299acae4648d` | Keep all NL-required states, variables, events, guards, and existing required transitions, including the global forced CA_backManual, CB_backManual, CP_backManual, and CC_backManual fallbacks to Manual., Repair the PumpFault BackManual recovery transitions so they do not define or trigger source-local shadow events such as CARA.PumpFault.CC_backManual. They must listen to the same CARA-scope/cross-component BackManual events used by the global forced fallbacks, while still taking priority when the active state is PumpFault., Use the correct pyfcstm event qualification/scope syntax for referencing the existing chain/root BackManual events from the PumpFault-specific transitions. Do not create duplicate local events with the same leaf names., ... +3 |
| 10 | `2` | `sl9_rework_decision` | `fixbatch-2-sha256-6c78e328186` | accept=1, reject=0 | `sl10_review` | `sha256:755ad0fe1c1a1250313a82e8b039c5887f55a86bb21cfdf676de93081e486e84` | The failed scenario hot-starts in PumpFault and injects CC_backManual. Manual correctly inhibits pump output while pump_fault remains active, so the BackManual recovery path must clear the fault before Manual during behavior applies manual flow and switch speed., Forced transitions cannot carry effects, so PumpFault-specific ordinary transitions are needed for the recovery effect., The PumpFault-specific transitions use ': BackManualEvent' chain-scope syntax, so they listen to the same CARA-scope events as the global cross-component fallbacks and do not create source-local shadow events., ... +2 |
| 11 | `2` | `sl10_rework_review` | `fixbatch-2-sha256-6c78e328186` | accept=1, reject=0 | `sl9_rework` | `sha256:755ad0fe1c1a1250313a82e8b039c5887f55a86bb21cfdf676de93081e486e84` | Do not reject this locked request. Continue repairing fixreq-2-sd6-0-01a4312604., Ensure BackManual from PumpFault executes an effect before Manual entry/during behavior so that pump_fault = 0 and alarm_active = 0, allowing Manual to set flow_rate = manual_flow_rate and pump_speed = builtin_switch_speed., Remove the semantic duplication where global forced '* -> Manual :: CA_backManual/CB_backManual/CP_backManual/CC_backManual' overrides the PumpFault-specific normal transitions. If the DSL supports scoped forced transitions or exclusions, restrict the forced BackManual fallbacks so they still cover all non-PumpFault active states while the PumpFault-specific effectful transitions handle PumpFault., ... +4 |
| 12 | `2` | `sl9_rework_decision` | `fixbatch-2-sha256-6c78e328186` | accept=1, reject=0 | `sl10_review` | `sha256:4e2c880451936159cd68420023899a192ce50745282c5d4b38ecc761e709b456` | PumpFault-specific recovery must run an effect before Manual during behavior; otherwise pump_fault remains active and Manual correctly keeps the alarm asserted while inhibiting flow and pump speed., The PumpFault-specific BackManual transitions use chain-scope ': Event' triggers, so they reference the shared CARA-scope BackManual events rather than creating source-local shadow events., The former root-wide forced '* -> Manual' transitions are narrowed to non-PumpFault states to avoid forced/normal duplication for PumpFault while preserving cross-component fallback behavior for Manual, Ask_StartAC, AutocontrolInit, and AutocontrolNormal., ... +2 |
| 13 | `2` | `sl10_rework_review` | `fixbatch-2-sha256-6c78e328186` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:4e2c880451936159cd68420023899a192ce50745282c5d4b38ecc761e709b456` | <none> |
| 14 | `3` | `request_batch` | `fixbatch-3-sha256-1d257c6524c` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 15 | `3` | `sl9_decision` | `fixbatch-3-sha256-1d257c6524c` | accept=1, reject=0 | `sl10_review` | `sha256:94ad3dd3ec279dbf6be28e4a5ef9c715aa3a70019844dd7368a954eeebcbaedb` | BackManual remains a shared recovery event that moves CA_mode to Manual from PumpFault and other relevant modes., BackManual from PumpFault no longer clears pump_fault or alarm_active; therefore fallback alone cannot represent caregiver removal of a physical pump fault., Manual entry/during behavior is preserved so an uncleared pump_fault keeps alarm_active asserted and inhibits flow_rate and pump_speed., ... +1 |
| 16 | `3` | `sl10_review` | `fixbatch-3-sha256-1d257c6524c` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:94ad3dd3ec279dbf6be28e4a5ef9c715aa3a70019844dd7368a954eeebcbaedb` | <none> |
| 17 | `4` | `request_batch` | `fixbatch-4-sha256-b72cdbf75ec` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 18 | `4` | `sl9_decision` | `fixbatch-4-sha256-b72cdbf75ec` | accept=2, reject=0 | `sl10_review` | `sha256:4e2c880451936159cd68420023899a192ce50745282c5d4b38ecc761e709b456` | Accepted both hard simulation requests because the current PumpFault BackManual paths reach Manual but do not clear pump_fault before Manual entry/during behavior., Added effect blocks only to the PumpFault-specific BackManual transitions, because forced transitions cannot carry effects and the existing forced fallbacks are already scoped to non-PumpFault modes., Kept BackManual events chain-scoped with ': Event' so the PumpFault-specific transitions listen to the shared CARA-scope fallback events rather than creating source-local shadow events., ... +1 |
| 19 | `4` | `sl10_review` | `fixbatch-4-sha256-b72cdbf75ec` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:4e2c880451936159cd68420023899a192ce50745282c5d4b38ecc761e709b456` | <none> |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 6255, 'model': 'gpt-5.5', 'prompt_tokens': 6487, 'total_tokens': 12742}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4935, 'model': 'gpt-5.5', 'prompt_tokens': 13712, 'total_tokens': 18647}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1389, 'model': 'gpt-5.5', 'prompt_tokens': 11859, 'total_tokens': 13248}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 860, 'model': 'gpt-5.5', 'prompt_tokens': 7836, 'total_tokens': 8696}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3315, 'model': 'gpt-5.5', 'prompt_tokens': 16710, 'total_tokens': 20025}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2786, 'model': 'gpt-5.5', 'prompt_tokens': 17901, 'total_tokens': 20687}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2097, 'model': 'gpt-5.5', 'prompt_tokens': 13865, 'total_tokens': 15962}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1023, 'model': 'gpt-5.5', 'prompt_tokens': 9933, 'total_tokens': 10956}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3888, 'model': 'gpt-5.5', 'prompt_tokens': 16871, 'total_tokens': 20759}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2796, 'model': 'gpt-5.5', 'prompt_tokens': 15643, 'total_tokens': 18439}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1660, 'model': 'gpt-5.5', 'prompt_tokens': 12135, 'total_tokens': 13795}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1815, 'model': 'gpt-5.5', 'prompt_tokens': 18061, 'total_tokens': 19876}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1294, 'model': 'gpt-5.5', 'prompt_tokens': 14219, 'total_tokens': 15513}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2381, 'model': 'gpt-5.5', 'prompt_tokens': 19278, 'total_tokens': 21659}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1226, 'model': 'gpt-5.5', 'prompt_tokens': 15265, 'total_tokens': 16491}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4338, 'model': 'gpt-5.5', 'prompt_tokens': 26898, 'total_tokens': 31236}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 6681, 'model': 'gpt-5.5', 'prompt_tokens': 18113, 'total_tokens': 24794}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2586, 'model': 'gpt-5.5', 'prompt_tokens': 18931, 'total_tokens': 21517}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1693, 'model': 'gpt-5.5', 'prompt_tokens': 19331, 'total_tokens': 21024}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1247, 'model': 'gpt-5.5', 'prompt_tokens': 15676, 'total_tokens': 16923}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 8134, 'model': 'gpt-5.5', 'prompt_tokens': 20024, 'total_tokens': 28158}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2865, 'model': 'gpt-5.5', 'prompt_tokens': 28947, 'total_tokens': 31812}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1115, 'model': 'gpt-5.5', 'prompt_tokens': 14805, 'total_tokens': 15920}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`not_converged`，record_status=`budget_exhausted`。
- 主要原因分类：`scenario_or_sim_oracle`。
- required stages executed：`71/16`，missing=`<none>`。
- repairs：`5/7` accepted；scenario_history=`10`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
