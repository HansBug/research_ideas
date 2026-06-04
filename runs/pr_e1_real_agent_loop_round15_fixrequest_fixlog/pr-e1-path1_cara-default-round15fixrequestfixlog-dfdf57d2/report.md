## path1 / cara-infusion-pump-formal-spec__01 / default 真实运行结果：Path1 CARA representative NL

### 0. 准确边界与结论

- 运行入口：`method.loop.run_agent_loop(nl, LoopConfig(...))`。
- 是否使用 fake / fixture / hot-start / replay：否；本次使用真实默认入口/显式 PR-E1 探索条件，没有 fake、fixture、hot-start 或 replay。
- final verdict：`not_converged`；record_status：`rejected`；result_status：`not_converged`。
- main_result_eligible：`false`。
- 一句话结论：`semantic_or_topology`；停止原因：Do not clear pump_complication in the automatic AutocontrolNormal -> Manual transition merely because pump_complication > 0. Remove pump_complication = 0 from that guarded recovery effect.; Preserve the explicit Manual -> Manual :: CaregiverRemovesFault transition as the NL-grounded caregiver fault-removal action, and keep its effect clearing pump_complication and keeping control_released = 1.; Preserve Manual.during safety behavior: while pump_complication > 0, suppress manual pump_speed and flow_rate and keep alarm/release active; after CaregiverRemovesFault clears pump_complication, Manual.during may restore pump_speed = manual_switch_speed and flow_rate = default_flow_rate.; Preserve the AutocontrolNormal -> Manual recovery target and its alarm_active = 1 and control_released = 1 effects, but make clear in the DSL semantics that this transition releases software control and alarms, not that it removes the physical fault.; Preserve all required NL-grounded states, variables, events, guards, actions, and fallback transitions, including PumpFault, CaregiverRemovesFault, the four backManual events, InitiateAC, ChangeSetpoint, StartAC, autocontrol logging/control actions, and manual switch/default-flow behavior after the fault has been explicitly removed.。

### 1. 基本信息

| 字段 | 值 |
|---|---|
| Path | `path1` |
| case_id | `cara-infusion-pump-formal-spec__01` |
| config_id | `default` |
| 运行入口 | `method.loop.run_agent_loop(nl, LoopConfig(...))` |
| LoopConfig 摘要 | `condition_id=full_staged_v1`, `max_iterations=5`, `llm_max_retries=2`, `scenario_max_retries=2`, `model_review_mode=blocking_major_only`, `repair_review_mode=blocking_major_only` |
| Git commit | `214e9a0b067a60e40f40fea8943cacc232fa6de6` |
| clean / diff / prompt snapshot | clean=`True`, dirty=`False`, diff_hash=`sha256:2a69ad5797ac568a81bddcef615104303a97261094685f4edd8d4484e889ea09`, prompt_hash=`sha256:ce499624790550d734a59fdd9b6b28f8194710e89c85f739538372d5d8133081` |
| provider/model 脱敏标识 | mode=`real_env`, model=`gpt-5.5`, real_api=`True` |
| source / paper | source=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec`, paper=`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/paper.pdf` |
| 样本筛选理由 | issue #14 / PR-D 代表性医疗 EFSM，覆盖人工/自动模式、故障回退和跨组件事件。 |
| 变量参与说明 | 变量和事件混合；`CA_mode` 与 setpoint/blood pressure 语义强，但容易触发 grounding / required-element 保留问题。 |
| run_id | `pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2` |
| final verdict/status | verdict=`not_converged`, record=`rejected`, result=`not_converged` |
| main_result_eligible | `false` |
| token/cost/time | tokens=`{'prompt_tokens': 1114874, 'completion_tokens': 76852, 'total_tokens': 1191726, 'n_calls': 22}`, elapsed=`2638.054s` |
| run record | [`pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
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
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float patient_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;
def float control_voltage = 0.0;
def int pump_complication = 0;
def int alarm_active = 0;
def int control_released = 0;
def int log_entries = 0;

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
                control_released = 1;
            }
            during {
                if [pump_complication == 0] {
                    pump_speed = manual_switch_speed;
                    flow_rate = default_flow_rate;
                } else {
                    pump_speed = 0.0;
                    flow_rate = 0.0;
                    alarm_active = 1;
                    control_released = 1;
                }
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                control_released = 0;
                pump_speed = control_voltage;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_complication == 0] {
                    flow_rate = target_bp - patient_bp;
                    pump_speed = control_voltage;
                    log_entries = log_entries + 1;
                } else {
                    alarm_active = 1;
                    control_released = 1;
                }
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Manual -> Manual :: CaregiverRemovesFault effect {
            pump_complication = 0;
            alarm_active = 0;
            control_released = 1;
        };
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
            target_bp = requested_target_bp;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC effect {
            control_released = 0;
        };
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> AutocontrolNormal :: PumpFault effect {
            pump_complication = 1;
            alarm_active = 1;
        };
        AutocontrolNormal -> Manual : if [pump_complication > 0] effect {
            alarm_active = 1;
            control_released = 1;
        };
    }
}
```

### 4. 全流程真实摘要表

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=13003 | 生成初始 DSL 与 grounding seeds | initial len=1970 | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=2, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=447914 | LLM per-request accept/reject + repair | candidate len=2115,2245,2368,2502,2571 | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=474960 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=9, tokens=209781 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=9, tokens=209781 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=9, tokens=209781 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=447914 | LLM per-request accept/reject + repair | candidate len=2115,2245,2368,2502,2571 | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=474960 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=9, tokens=209781 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=9, tokens=209781 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=2, tokens=46068 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=447914 | LLM per-request accept/reject + repair | candidate len=2115,2245,2368,2502,2571 | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=474960 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=9, tokens=209781 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=9, tokens=209781 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=2, tokens=46068 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=447914 | LLM per-request accept/reject + repair | candidate len=2115,2245,2368,2502,2571 | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=474960 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=2, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1; blocking=0, advisory=12, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=9, tokens=209781 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-5` | 是 | 1 | ✅ | LLM calls=9, tokens=209781 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-5A` | 否 | 1 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SC-5F` | 否 | 1 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-6` | 否 | 1 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0; ok=False, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=447914 | LLM per-request accept/reject + repair | candidate len=2115,2245,2368,2502,2571 | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=474960 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | Do not clear pump_complication in the automatic AutocontrolNormal -> Manual transition merely because pump_complication > 0. Remove pump_complication = 0 from t | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz) |

### 5. Iteration / repair / review 摘要

| Iter | selected feedback | repair? | FixRequestBatch | SL-9 | local checks | SL-10 | 回到 SD-2? | verdict/备注 |
|---:|---|---|---|---|---|---|---|---|
| 0 | `SD-4` | yes | fixbatch-0-sha256-582b5000c55 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 1 | `SD-6` | yes | fixbatch-1-sha256-96cbb2c7803 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 2 | `SL-7` | yes | fixbatch-2-sha256-1c602042228 / n=2 | accept=2, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 3 | `SL-7` | yes | fixbatch-3-sha256-31963f0acfb / n=1 | accept=1, reject=0, waiver=0 | ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none> | yes | candidate_accepted_for_next_full_pass |
| 4 | `SD-6` | yes | fixbatch-4-sha256-d5f6aeec59a / n=5 | accept=5, reject=0, waiver=0 | ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | decision=rework, ok=False, target=False, regression=True, drift=major, rework=Do not clear pump_complication in the automatic AutocontrolNormal -> Manual transition merely because pump_complication > 0. Remove pump_compl...<truncated 262 chars> | no | Do not clear pump_complication in the automatic AutocontrolNormal -> Manual transition merely because pump_complication > 0. Remove pump_complication = 0 from that guarded recovery effect.; Preserve the explicit Manual -> Manual :: CaregiverRemovesFault transition as the NL-grounded caregiver fault-removal action, and keep its effect clearing pump_complication and keeping control_released = 1.; Preserve Manual.during safety behavior: while pump_complication > 0, suppress manual pump_speed and flow_rate and keep alarm/release active; after CaregiverRemovesFault clears pump_complication, Manual.during may restore pump_speed = manual_switch_speed and flow_rate = default_flow_rate.; Preserve the AutocontrolNormal -> Manual recovery target and its alarm_active = 1 and control_released = 1 effects, but make clear in the DSL semantics that this transition releases software control and alarms, not that it removes the physical fault.; Preserve all required NL-grounded states, variables, events, guards, actions, and fallback transitions, including PumpFault, CaregiverRemovesFault, the four backManual events, InitiateAC, ChangeSetpoint, StartAC, autocontrol logging/control actions, and manual switch/default-flow behavior after the fault has been explicitly removed. |

### 6. Scenario 明细与逐轮通过情况

#### 6.1 Scenario pass/fail by iteration

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 2 | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|---|
| `default_initializes_to_manual_outputs` | default-init verifies CARA dispatches to Manual and manual mode sets pump speed from the built-in switch and flow from t...<truncated 21 chars> | ✅ | ✅ | ✅ | ✅ |
| `manual_initiate_setpoint_start_autocontrol` | explicit-hot-start exercises caregiver initiation, Ask_StartAC setpoint change, StartAC to AutocontrolInit, and progress...<truncated 28 chars> | ✅ | ✅ | ✅ | ✅ |
| `autocontrol_normal_higher_pressure_lower_flow` | explicit-hot-start probes normal autocontrol calculation: with no complication, pump speed follows control voltage and h...<truncated 39 chars> | ✅ | ✅ | ✅ | ✅ |
| `no_complication_stays_in_autocontrol_normal` | explicit-hot-start boundary/no-fire probe for pump_complication: value 0 means no pump-operation complication, so CARA r...<truncated 29 chars> | ✅ | ✅ | ✅ | ✅ |
| `pump_fault_event_alarms_then_releases_control` | explicit-hot-start injects a pump fault during normal autocontrol, expecting alarm activation and then recovery to Manua...<truncated 33 chars> | ✅ | ✅ | ✅ | ❌ |
| `pump_complication_guard_direct_to_manual` | explicit-hot-start boundary probe for pump_complication > 0: an existing complication forces recovery from normal autoco...<truncated 16 chars> | ❌ | ✅ | ✅ | ❌ |
| `all_backmanual_events_share_manual_target` | explicit-hot-start probes cross-component fallback events from several concrete modes; CA_backManual, CB_backManual, CP_...<truncated 48 chars> | ✅ | ✅ | ✅ | ✅ |
| `constant_effects_exact_values_on_start_and_recovery` | explicit-hot-start focuses M5/M6 probes on constant-valued effects: StartAC must set released control to exactly 0, Pump...<truncated 146 chars> | ⚪ | ✅ | ✅ | ❌ |
| `setpoint_effect_persists_into_flow_calculation` | explicit-hot-start adds an M5/M6 probe: ChangeSetpoint must copy the requested setpoint exactly, and the copied target m...<truncated 71 chars> | ⚪ | ✅ | ✅ | ✅ |
| `change_setpoint_exact_copy_overrides_old_target` | explicit-hot-start adds a focused M5/M6 probe: ChangeSetpoint must overwrite a nonzero old target with the requested tar...<truncated 70 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `manual_recovery_clears_complication_exactly` | explicit-hot-start adds a direct M5/M6 probe for the AutocontrolNormal-to-Manual recovery effect: a pre-existing pump co...<truncated 86 chars> | ⚪ | ⚪ | ✅ | ❌ |
| `forced_manual_recovery_effect_outputs_exact` | explicit-hot-start adds an M5/M6-style effect-output probe for fallback recovery: a backManual event from autocontrol mu...<truncated 104 chars> | ⚪ | ⚪ | ✅ | ✅ |
| `caregiver_removes_fault_restores_manual_operation` | explicit-hot-start adds M2/M5/M6 probes for CaregiverRemovesFault: from Manual with a fault present, the event must targ...<truncated 85 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `initiate_start_targets_do_not_skip_ask_or_init` | explicit-hot-start strengthens M2 wrong-target probes: InitiateAC must first enter Ask_StartAC, and StartAC must enter A...<truncated 67 chars> | ⚪ | ⚪ | ⚪ | ✅ |
| `pumpfault_target_and_effect_before_guard_recovery` | explicit-hot-start adds a focused M2/M5/M6 probe: PumpFault must first remain in AutocontrolNormal with exact fault effe...<truncated 56 chars> | ⚪ | ⚪ | ⚪ | ❌ |
| `effect_value_probe_setpoint_startac_and_pumpfault` |  | ✅ | ✅ | ✅ | ⚪ |
| `fault_effects_survive_recovery_to_manual` |  | ❌ | ✅ | ✅ | ⚪ |

#### 6.2 Scenario definitions

<details><summary>`default_initializes_to_manual_outputs` — default-init verifies CARA dispatches to Manual and manual mode sets pump speed from the built-in switch and flow from the default pump rate.</summary>

| Field | Value |
|---|---|
| description | default-init verifies CARA dispatches to Manual and manual mode sets pump speed from the built-in switch and flow from the default pump rate. |
| initial_state | `<default-init>` |
| initial_vars | `{"default_flow_rate": 7.5, "manual_switch_speed": 2.5}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `first_cycle_enters_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"alarm_active": 0, "control_released": 1, "flow_rate": 7.5, "pump_speed": 2.5}` |

</details>

<details><summary>`manual_initiate_setpoint_start_autocontrol` — explicit-hot-start exercises caregiver initiation, Ask_StartAC setpoint change, StartAC to AutocontrolInit, and progression into normal autocontrol.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start exercises caregiver initiation, Ask_StartAC setpoint change, StartAC to AutocontrolInit, and progression into normal autocontrol. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"control_voltage": 3.0, "log_entries": 0, "patient_bp": 70.0, "pump_complication": 0, "requested_target_bp": 110.0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiate_enters_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 1 `change_setpoint_updates_target` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 110.0}` |
| 2 `startac_enters_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"control_released": 0, "pump_speed": 3.0}` |
| 3 `init_completes_to_normal_autocontrol` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_released": 0, "flow_rate": 40.0, "log_entries": 1, "pump_speed": 3.0}` |

</details>

<details><summary>`autocontrol_normal_higher_pressure_lower_flow` — explicit-hot-start probes normal autocontrol calculation: with no complication, pump speed follows control voltage and high patient pressure yields lower flow.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes normal autocontrol calculation: with no complication, pump speed follows control voltage and high patient pressure yields lower flow. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"alarm_active": 0, "control_released": 0, "control_voltage": 2.0, "log_entries": 5, "patient_bp": 90.0, "pump_complication": 0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `normal_control_cycle_logs_and_controls` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"alarm_active": 0, "control_released": 0, "flow_rate": 10.0, "log_entries": 6, "pump_speed": 2.0}` |

</details>

<details><summary>`no_complication_stays_in_autocontrol_normal` — explicit-hot-start boundary/no-fire probe for pump_complication: value 0 means no pump-operation complication, so CARA remains in normal autocontrol.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start boundary/no-fire probe for pump_complication: value 0 means no pump-operation complication, so CARA remains in normal autocontrol. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"alarm_active": 0, "control_released": 0, "control_voltage": 4.0, "log_entries": 2, "patient_bp": 80.0, "pump_complication": 0, "target_bp": 120.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `no_fault_no_manual_recovery` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"alarm_active": 0, "control_released": 0, "flow_rate": 40.0, "log_entries": 3, "pump_speed": 4.0}` |

</details>

<details><summary>`pump_fault_event_alarms_then_releases_control` — explicit-hot-start injects a pump fault during normal autocontrol, expecting alarm activation and then recovery to Manual with software control released.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start injects a pump fault during normal autocontrol, expecting alarm activation and then recovery to Manual with software control released. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"alarm_active": 0, "control_released": 0, "control_voltage": 5.0, "default_flow_rate": 6.0, "log_entries": 0, "manual_switch_speed": 1.0, "patient_bp": 75.0, "pump_complication": 0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `pump_fault_activates_alarm` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolNormal.PumpFault"]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"alarm_active": 1, "control_released": 1, "pump_complication": 1}` |
| 1 `fault_condition_recovers_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"control_released": 1, "flow_rate": 6.0, "pump_complication": 0, "pump_speed": 1.0}` |

</details>

<details><summary>`pump_complication_guard_direct_to_manual` — explicit-hot-start boundary probe for pump_complication > 0: an existing complication forces recovery from normal autocontrol to Manual.</summary>

| Field | Value |
|---|---|
| description | explicit-hot-start boundary probe for pump_complication > 0: an existing complication forces recovery from normal autocontrol to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"alarm_active": 0, "control_released": 0, "default_flow_rate": 8.0, "manual_switch_speed": 1.5, "pump_complication": 1}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `complication_releases_to_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"alarm_active": 1, "control_released": 1, "flow_rate": 8.0, "pump_complication": 0, "pump_speed": 1.5}` |

</details>

<details><summary>`all_backmanual_events_share_manual_target` — explicit-hot-start probes cross-component fallback events from several concrete modes; CA_backManual, CB_backManual, CP_backManual, and CC_backManual all target...<truncated 8 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start probes cross-component fallback events from several concrete modes; CA_backManual, CB_backManual, CP_backManual, and CC_backManual all target Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"alarm_active": 0, "control_released": 0, "control_voltage": 3.5, "default_flow_rate": 9.0, "log_entries": 0, "manual_switch_speed": 2.0, "patient_bp": 60.0, "pump_complication": 0, "target_bp": 100.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_from_autocontrol_normal` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"control_released": 1, "flow_rate": 9.0, "pump_speed": 2.0}` |
| 1 `return_to_ask_for_cb_probe` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 2 `cb_backmanual_from_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.CB_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"control_released": 1, "flow_rate": 9.0, "pump_speed": 2.0}` |
| 3 `enter_autocontrol_init_for_cp_probe` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 4 `startac_to_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"control_released": 0, "pump_speed": 3.5}` |
| 5 `cp_backmanual_from_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.CP_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"control_released": 1, "flow_rate": 9.0, "pump_speed": 2.0}` |
| 6 `reenter_normal_for_cc_probe_ask` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 7 `reenter_normal_for_cc_probe_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"control_released": 0, "pump_speed": 3.5}` |
| 8 `reenter_normal_for_cc_probe_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_released": 0, "flow_rate": 40.0, "log_entries": 1, "pump_speed": 3.5}` |
| 9 `cc_backmanual_from_autocontrol_normal` | `0` | `["CARA.Mode_Control_Algorithm.CC_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"control_released": 1, "flow_rate": 9.0, "pump_speed": 2.0}` |

</details>

<details><summary>`constant_effects_exact_values_on_start_and_recovery` — explicit-hot-start focuses M5/M6 probes on constant-valued effects: StartAC must set released control to exactly 0, PumpFault must set complication and alarm to...<truncated 106 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start focuses M5/M6 probes on constant-valued effects: StartAC must set released control to exactly 0, PumpFault must set complication and alarm to exactly 1, and fault recovery must leave Manual with released control exactly 1 and complication cleared. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"alarm_active": 0, "control_released": 1, "control_voltage": 7.0, "default_flow_rate": 11.5, "log_entries": 10, "manual_switch_speed": 3.25, "patient_bp": 85.0, "pump_complication": 0, "requested_target_bp": 115.0, "target_bp": 115.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `startac_sets_control_released_exact_zero` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"control_released": 0, "pump_speed": 7.0}` |
| 1 `normal_keeps_autocontrol_before_fault` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_released": 0, "flow_rate": 30.0, "log_entries": 11, "pump_speed": 7.0}` |
| 2 `pumpfault_sets_exact_one_flags` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolNormal.PumpFault"]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"alarm_active": 1, "control_released": 1, "pump_complication": 1}` |
| 3 `fault_recovery_manual_exact_outputs` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"alarm_active": 1, "control_released": 1, "flow_rate": 11.5, "pump_complication": 0, "pump_speed": 3.25}` |

</details>

<details><summary>`setpoint_effect_persists_into_flow_calculation` — explicit-hot-start adds an M5/M6 probe: ChangeSetpoint must copy the requested setpoint exactly, and the copied target must be the value used for the next norma...<truncated 31 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start adds an M5/M6 probe: ChangeSetpoint must copy the requested setpoint exactly, and the copied target must be the value used for the next normal-autocontrol flow calculation. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"alarm_active": 0, "control_released": 1, "control_voltage": 8.0, "log_entries": 20, "patient_bp": 100.0, "pump_complication": 0, "requested_target_bp": 125.0, "target_bp": 60.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `setpoint_copy_not_missing_or_offset` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 125.0}` |
| 1 `start_after_exact_setpoint_copy` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"control_released": 0, "pump_speed": 8.0}` |
| 2 `normal_flow_uses_copied_target` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"alarm_active": 0, "control_released": 0, "flow_rate": 25.0, "log_entries": 21, "pump_speed": 8.0}` |

</details>

<details><summary>`change_setpoint_exact_copy_overrides_old_target` — explicit-hot-start adds a focused M5/M6 probe: ChangeSetpoint must overwrite a nonzero old target with the requested target exactly, not preserve the old target...<truncated 30 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start adds a focused M5/M6 probe: ChangeSetpoint must overwrite a nonzero old target with the requested target exactly, not preserve the old target or assign an offset constant. |
| initial_state | `CARA.Mode_Control_Algorithm.Ask_StartAC` |
| initial_vars | `{"alarm_active": 0, "control_released": 1, "control_voltage": 10.0, "log_entries": 40, "patient_bp": 104.0, "pump_complication": 0, "requested_target_bp": 144.0, "target_bp": 44.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `change_setpoint_exactly_overwrites_old_target` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.ChangeSetpoint"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{"target_bp": 144.0}` |
| 1 `start_after_exact_overwrite` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"control_released": 0, "pump_speed": 10.0}` |
| 2 `flow_uses_overwritten_target_exactly` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_released": 0, "flow_rate": 40.0, "log_entries": 41, "pump_speed": 10.0}` |

</details>

<details><summary>`manual_recovery_clears_complication_exactly` — explicit-hot-start adds a direct M5/M6 probe for the AutocontrolNormal-to-Manual recovery effect: a pre-existing pump complication must be removed exactly while...<truncated 46 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start adds a direct M5/M6 probe for the AutocontrolNormal-to-Manual recovery effect: a pre-existing pump complication must be removed exactly while Manual resumes switch/default-rate operation. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"alarm_active": 0, "control_released": 0, "default_flow_rate": 12.5, "flow_rate": 99.0, "manual_switch_speed": 4.5, "pump_complication": 1, "pump_speed": 99.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `recovery_effect_clears_fault_and_restores_manual_outputs` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"alarm_active": 1, "control_released": 1, "flow_rate": 12.5, "pump_complication": 0, "pump_speed": 4.5}` |

</details>

<details><summary>`forced_manual_recovery_effect_outputs_exact` — explicit-hot-start adds an M5/M6-style effect-output probe for fallback recovery: a backManual event from autocontrol must enter Manual with released control ex...<truncated 64 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start adds an M5/M6-style effect-output probe for fallback recovery: a backManual event from autocontrol must enter Manual with released control exactly 1 and manual switch/default-rate outputs exactly restored. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"alarm_active": 0, "control_released": 0, "control_voltage": 9.0, "default_flow_rate": 13.5, "flow_rate": 99.0, "log_entries": 30, "manual_switch_speed": 5.5, "patient_bp": 95.0, "pump_complication": 0, "pump_speed": 99.0, "target_bp": 130.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `ca_backmanual_restores_manual_outputs_exactly` | `0` | `["CARA.Mode_Control_Algorithm.CA_backManual"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"alarm_active": 0, "control_released": 1, "flow_rate": 13.5, "pump_speed": 5.5}` |

</details>

<details><summary>`caregiver_removes_fault_restores_manual_operation` — explicit-hot-start adds M2/M5/M6 probes for CaregiverRemovesFault: from Manual with a fault present, the event must target Manual and exactly clear complication...<truncated 45 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start adds M2/M5/M6 probes for CaregiverRemovesFault: from Manual with a fault present, the event must target Manual and exactly clear complication and alarm while preserving released control. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"alarm_active": 1, "control_released": 0, "default_flow_rate": 14.5, "flow_rate": 0.0, "manual_switch_speed": 6.5, "pump_complication": 1, "pump_speed": 0.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `remove_fault_clears_flags_and_stays_manual` | `0` | `["CARA.Mode_Control_Algorithm.Manual.CaregiverRemovesFault"]` | `CARA.Mode_Control_Algorithm.Manual` | `{"alarm_active": 0, "control_released": 1, "flow_rate": 14.5, "pump_complication": 0, "pump_speed": 6.5}` |

</details>

<details><summary>`initiate_start_targets_do_not_skip_ask_or_init` — explicit-hot-start strengthens M2 wrong-target probes: InitiateAC must first enter Ask_StartAC, and StartAC must enter AutocontrolInit rather than skipping dire...<truncated 27 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start strengthens M2 wrong-target probes: InitiateAC must first enter Ask_StartAC, and StartAC must enter AutocontrolInit rather than skipping directly to normal autocontrol. |
| initial_state | `CARA.Mode_Control_Algorithm.Manual` |
| initial_vars | `{"alarm_active": 0, "control_released": 1, "control_voltage": 6.75, "log_entries": 50, "patient_bp": 65.0, "pump_complication": 0, "requested_target_bp": 90.0, "target_bp": 90.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `initiate_must_target_ask_startac` | `0` | `["CARA.Mode_Control_Algorithm.Manual.InitiateAC"]` | `CARA.Mode_Control_Algorithm.Ask_StartAC` | `{}` |
| 1 `startac_must_target_autocontrol_init` | `0` | `["CARA.Mode_Control_Algorithm.Ask_StartAC.StartAC"]` | `CARA.Mode_Control_Algorithm.AutocontrolInit` | `{"control_released": 0, "pump_speed": 6.75}` |
| 2 `only_next_cycle_reaches_normal` | `0` | `[]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"control_released": 0, "flow_rate": 25.0, "log_entries": 51, "pump_speed": 6.75}` |

</details>

<details><summary>`pumpfault_target_and_effect_before_guard_recovery` — explicit-hot-start adds a focused M2/M5/M6 probe: PumpFault must first remain in AutocontrolNormal with exact fault effects before the following guard cycle rec...<truncated 16 chars></summary>

| Field | Value |
|---|---|
| description | explicit-hot-start adds a focused M2/M5/M6 probe: PumpFault must first remain in AutocontrolNormal with exact fault effects before the following guard cycle recovers to Manual. |
| initial_state | `CARA.Mode_Control_Algorithm.AutocontrolNormal` |
| initial_vars | `{"alarm_active": 0, "control_released": 0, "control_voltage": 4.25, "default_flow_rate": 15.5, "log_entries": 60, "manual_switch_speed": 7.5, "patient_bp": 90.0, "pump_complication": 0, "target_bp": 140.0}` |

| Step | before_cycles | events | expected_state | expected_vars |
|---:|---:|---|---|---|
| 0 `pumpfault_must_not_jump_directly_to_manual` | `0` | `["CARA.Mode_Control_Algorithm.AutocontrolNormal.PumpFault"]` | `CARA.Mode_Control_Algorithm.AutocontrolNormal` | `{"alarm_active": 1, "control_released": 1, "pump_complication": 1}` |
| 1 `next_cycle_fault_guard_targets_manual` | `0` | `[]` | `CARA.Mode_Control_Algorithm.Manual` | `{"alarm_active": 1, "control_released": 1, "flow_rate": 15.5, "pump_complication": 0, "pump_speed": 7.5}` |

</details>


### 7. Repair / blocking feedback 明细

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=pump_complication, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.Manual, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, ... +2 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:80e89626ea7f6fe4b1595dd499bde14d4b727623d5c42ad54814b3bed2d5c7c1` |
| 2 | `1` | ✅ | `SD-6` | pump_complication_guard_direct_to_manual, fault_effects_survive_recovery_to_manual | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:d80130b8e29f04e5c1f008e51d812660ed13135952eac183abb351b36c249f21` |
| 3 | `2` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:3af25448acb0aa8176a168b10a7f96d65459f40b7cac136e633cb01135a966c6` |
| 4 | `3` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:d5fc27ce2507b0b0d9533fba9817a55384364141ee57d7c0ad930290c88474ff` |
| 5 | `4` | ❌ | `SD-6` | pump_fault_event_alarms_then_releases_control, pump_complication_guard_direct_to_manual, constant_effects_exact_values_on_start_and_recovery, manual_recovery_clears_complication_exactly, pumpfault_target_and_effect_before_guard_recovery | accept=5, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Do not clear pump_complication in the automatic AutocontrolNormal -> Manual transition merely because pump_complication > 0. Remove pump_complication = 0 from that guarded reco...<truncated 343 chars> | `sha256:52e0a3e7ac653bfd0e3a9d7ad45dd7a82d65868b3b3379a438097cdb74a4ba61` |

<details><summary>Repair 1 / iteration `0` / source `SD-4` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-4`；blocking=`True`；pre_scenario=`True`。
- problem_summary：Variable 'pump_complication' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects.
- diagnostic ids：`W_UNWRITTEN_READ_VAR:var_name=pump_complication, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.Manual, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, W_UNREFERENCED_VAR, I_TRANSITION_NEVER_EVENT_TRIGGERED`。
- before_dsl_hash：`sha256:47fdd04da9854acfbf32a588bf445a3f066779d5c92996368dacbae23884d071`；candidate_dsl_hash：`sha256:80e89626ea7f6fe4b1595dd499bde14d4b727623d5c42ad54814b3bed2d5c7c1`。

#### 错误证据 / diagnostics

- 1. `W_UNWRITTEN_READ_VAR` `W_UNWRITTEN_READ_VAR:var_name=pump_complication` policy=`budgeted_repair`：Variable 'pump_complication' is read but never written by any action or transition effect.；refs=`{"init_value": "0", "read_states": ["CARA.Mode_Control_Algorithm.AutocontrolNormal"], "var_name": "pump_complication"}`
- 2. `W_GUARD_VARS_NEVER_CHANGE` `W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.Manual` policy=`budgeted_repair`：Transition guard reads only variables that are never changed by actions or effects.；refs=`{"from_path": "CARA.Mode_Control_Algorithm.AutocontrolNormal", "guard_vars": ["pump_complication"], "to_path": "CARA.Mode_Control_Algorithm.Manual"}`

#### 变量角色与上下文提示

- policy：Advisory only. Do not invent writes for external_input_candidate variables unless NL explicitly gives update semantics; add meaningful NL-grounded writes only for internal state variables.
- source：SD-4 diagnostic refs and generic NL external-input rationale

| Variable | role_hint | nl_token_present | diagnostics |
|---|---|---:|---|
| `alarm_active` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `control_released` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `control_voltage` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `default_flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `flow_rate` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `log_entries` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `manual_switch_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `patient_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `pump_complication` | `unknown` | ❌ | `W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE` |
| `pump_speed` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `requested_target_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |
| `target_bp` | `unknown` | ❌ | `W_UNREFERENCED_VAR` |

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-0-sha256-582b5000c55`；source_stage=`SD-4`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-0-sd4-0-a6f1595e9f` | `blocking_warning` | ❌ | ✅ | Variable 'pump_complication' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects. | `W_UNWRITTEN_READ_VAR` |
| `fixreq-0-sd4-1-00547968c2` | `blocking_warning` | ❌ | ✅ | Variable 'pump_complication' is read but never written by any action or transition effect.; Transition guard reads only variables that are never changed by actions or effects. | `W_GUARD_VARS_NEVER_CHANGE` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- hint 1：The variable is used as input but never updated after its initial definition, so model behavior may be accidentally constant.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment.`
- hint 2：This guard is controlled only by initial variable values. If those values never change, the transition condition is effectively fixed.；`actions=add_write, simplify_guard；do_not=Do not add a meaningless self-assignment; it does not model a real change., Do not rewrite the guard to a meaningless constant only to silence this diagnostic.`
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, variable:target_bp, variable:requested_target_bp, variable:patient_bp, variable:flow_rate, variable:default_flow_rate, variable:pump_speed, ... +28`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2115`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-0-sd4-0-a6f1595e9f` | `accept` | ❌ | ❌ | The NL explicitly describes pump faults such as fluid-tubing occlusion occurring during pump operation. Adding a fault-occurrence event that writes the internal pump_complication indicator is a meaningful NL-grounded update, not a self-assignment or invented plant dynamics.；intent=Add an AutocontrolNormal local PumpFault event transition that sets pump_compl...<truncated 37 chars> |
| `fixreq-0-sd4-1-00547968c2` | `accept` | ❌ | ❌ | The existing AutocontrolNormal-to-Manual guard on pump_complication is required by the grounding map. Writing pump_complication on a grounded pump-fault event makes the guard depend on a variable that can change at runtime while preserving the required guard and fallback behavior.；intent=Preserve the pump_complication guard and make it reachable by writing p...<truncated 42 chars> |
- repair_rationale：The repair preserves all required states, variables, events, transitions, guards, and grounded actions.；The new PumpFault event is grounded in the NL statement that pump faults such as occlusion can occur.；The pump_complication variable is now meaningfully written before being read by the no-complication action guard and the transition-to-Manual guard.；The required AutocontrolNormal -> Manual transition on pump_complication is preserved unchanged.
- diff_summary：`{"summary": "Added a local AutocontrolNormal self-transition on PumpFault that sets pump_complication = 1 and alarm_active = 1, enabling the existing complication guard to change at runtime without deleting grounded behavior."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float patient_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;
def float control_voltage = 0.0;
def int pump_complication = 0;
def int alarm_active = 0;
def int control_released = 0;
def int log_entries = 0;

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
                control_released = 1;
                alarm_active = 0;
            }
            during {
                pump_speed = manual_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                control_released = 0;
                pump_speed = control_voltage;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_complication == 0] {
                    flow_rate = target_bp - patient_bp;
                    pump_speed = control_voltage;
                    log_entries = log_entries + 1;
                } else {
                    alarm_active = 1;
                    control_released = 1;
                }
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
            target_bp = requested_target_bp;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC effect {
            control_released = 0;
        };
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> AutocontrolNormal :: PumpFault effect {
            pump_complication = 1;
            alarm_active = 1;
        };
        AutocontrolNormal -> Manual : if [pump_complication > 0] effect {
            alarm_active = 1;
            control_released = 1;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -63,6 +63,10 @@
             control_released = 0;
         };
         AutocontrolInit -> AutocontrolNormal;
+        AutocontrolNormal -> AutocontrolNormal :: PumpFault effect {
+            pump_complication = 1;
+            alarm_active = 1;
+        };
         AutocontrolNormal -> Manual : if [pump_complication > 0] effect {
             alarm_active = 1;
             control_released = 1;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:e9e2067fac4c63f40001cec6e2425f963ce46e77f5b7bb82859fd04a7abdaf7c`。
  - SL-10 evidence 1: `{"summary": "Both SL-9 requests were accepted with the same repair intent: preserve the required pump_complication guard and add a meaningful runtime write for pump_complication. The candidate implements this by adding AutocontrolNormal -> AutocontrolNormal :: PumpFault with effects pump_complication = 1 and alarm_active = 1."}`
  - SL-10 evidence 2: `{"summary": "The repair is grounded in the NL requirement that pump faults such as fluid-tubing occlusion can occur and activate alarm signals. The added PumpFault event models that occurrence without deleting the required AutocontrolNormal -> Manual guarded transition or replacing the required pump_complication guard with a constant."}`
  - SL-10 evidence 3: `{"summary": "The target diagnostics are resolved in the candidate DSL: pump_complication is no longer only read; it is written by the PumpFault transition effect, so the AutocontrolNormal -> Manual guard if [pump_complication > 0] can depend on a variable that changes at runtime."}`
  - SL-10 evidence 4: `{"summary": "The required NL-grounded states, variables, events, transitions, guards, and actions are preserved textually in the candidate DSL, including CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, the four backManual fallback transitions, InitiateAC, ChangeSetpoint, StartAC, manual pump-speed behavior, autocontrol guarded flow-rate/logging behavior, alarm activation, and release-control effects."}`
  - SL-10 evidence 5: `{"summary": "Local SD-10 evidence rejected the candidate for missing required grounding, but the listed missing elements are visibly present in both old and candidate DSL and were not removed by the diff. This appears to be conservative grounding/matching evidence rather than an actual NL regression. The only substantive diff is the added PumpFault self-transition."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:fallback_CA_backManual_to_Manual", "transition:fallback_CB_backManual_to_Manual", "transition:fallback_CP_backManual_to_Manual", "transition:fallback_CC_backManual_to_Manual", "transition:Manual_to_Ask_StartAC", "transition:Ask_StartAC_change_setpoint", "transition:Ask_StartAC_to_AutocontrolInit", "transition:AutocontrolNormal_to_Manual_on_complication", "guard:no_pump_complic...<truncated 135 chars>

</details>

<details><summary>Repair 2 / iteration `1` / source `SD-6` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`pump_complication_guard_direct_to_manual, fault_effects_survive_recovery_to_manual`。
- before_dsl_hash：`sha256:80e89626ea7f6fe4b1595dd499bde14d4b727623d5c42ad54814b3bed2d5c7c1`；candidate_dsl_hash：`sha256:d80130b8e29f04e5c1f008e51d812660ed13135952eac183abb351b36c249f21`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-1-sha256-96cbb2c7803`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-1-sd6-0-0ebc01e11a` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start boundary probe for pump_complication > 0: an existing complication forces recovery from normal autocontrol to Manual.', 'name': 'pump_complication_guard_direct_to_manual', 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'alarm_active': 0, 'control_released': 1, 'control_voltage': 0.0, 'default_flow_rate': 8.0, 'flow_rate': 8.0, 'log_entries': 0, 'manual_switch_speed': 1.5, 'patient_bp': 0.0, 'pump_complication': 1, 'pump_speed': 1.5, 'requested_target_bp': 0.0, 'target_bp': 0.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'complication_releases_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'alarm_active': {'actual': 0, 'expected': 1}}}]}` |
| `fixreq-1-sd6-1-af40444cbf` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start strengthens missing/wrong-effect probes: PumpFault must set exact fault flags, and the subsequent complication recovery to Manual must leave alarm active and software control released.', 'name': 'fault_effects_survive_recovery_to_manual', 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'alarm_active': 1, 'control_released': 1, 'control_voltage': 6.0, 'default_flow_rate': 7.25, 'flow_rate': 0.0, 'log_entries': 4, 'manual_switch_speed': 2.25, 'patient_bp': 80.0, 'pump_complication': 1, 'pump_speed': 0.0, 'requested_target_bp': 0.0, 'target_bp': 105.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'pumpfault_exact_effect_values', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'alarm_active': 0, 'control_released': 1, 'control_voltage': 6.0, 'default_flow_rate': 7.25, 'flow_rate': 7.25, 'log_entries': 4, 'manual_switch_speed': 2.25, 'patient_bp': 80.0, 'pump_complication': 1, 'pump_speed': 2.25, 'requested_target_bp': 0.0, 'target_bp': 105.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 1, 'step_name': 'guard_recovery_keeps_alarm_and_release', 'var_assertion_ok': False, 'var_mismatches': {'alarm_active': {'actual': 0, 'expected': 1}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, variable:target_bp, variable:requested_target_bp, variable:patient_bp, variable:flow_rate, variable:default_flow_rate, variable:pump_speed, ... +28`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2245`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-1-sd6-0-0ebc01e11a` | `accept` | ❌ | ❌ | The simulation evidence shows the guarded recovery from AutocontrolNormal to Manual reaches the correct Manual state and releases control, but Manual.enter immediately clears alarm_active to 0 after the transition effect sets it to 1. The smallest safe repair is to make Manual entry preserve/activate the alarm when pump_complication is already present, while...<truncated 163 chars> |
| `fixreq-1-sd6-1-af40444cbf` | `accept` | ❌ | ❌ | PumpFault already sets the exact fault flags in the first failing scenario step. The subsequent failure is caused by the same Manual.enter alarm reset, so the same conditional Manual entry repair preserves PumpFault behavior and lets alarm_active survive the complication recovery to Manual.；intent=Preserve PumpFault effects and prevent Manual.enter from clea...<truncated 40 chars> |
- repair_rationale：The failing variable is overwritten after the AutocontrolNormal -> Manual transition: transition effect sets alarm_active = 1, then Manual.enter sets alarm_active = 0.；Making Manual.enter conditional on pump_complication preserves normal manual initialization with alarm inactive while keeping alarms active during fault/complication recovery.；All required grounded states, variables, events, fallback transitions, Ask_StartAC transitions, pump-complication guards, logging action, alarm activation, and release-control behavior are preserved.
- diff_summary：`{"summary": "Replaced the unconditional alarm_active = 0 assignment in Manual.enter with a conditional assignment: alarm_active = 1 when pump_complication > 0, otherwise alarm_active = 0. No other structure or grounded behavior was changed."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float patient_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;
def float control_voltage = 0.0;
def int pump_complication = 0;
def int alarm_active = 0;
def int control_released = 0;
def int log_entries = 0;

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
                control_released = 1;
                if [pump_complication > 0] {
                    alarm_active = 1;
                } else {
                    alarm_active = 0;
                }
            }
            during {
                pump_speed = manual_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                control_released = 0;
                pump_speed = control_voltage;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_complication == 0] {
                    flow_rate = target_bp - patient_bp;
                    pump_speed = control_voltage;
                    log_entries = log_entries + 1;
                } else {
                    alarm_active = 1;
                    control_released = 1;
                }
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
            target_bp = requested_target_bp;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC effect {
            control_released = 0;
        };
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> AutocontrolNormal :: PumpFault effect {
            pump_complication = 1;
            alarm_active = 1;
        };
        AutocontrolNormal -> Manual : if [pump_complication > 0] effect {
            alarm_active = 1;
            control_released = 1;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -25,7 +25,11 @@
         state Manual {
             enter {
                 control_released = 1;
-                alarm_active = 0;
+                if [pump_complication > 0] {
+                    alarm_active = 1;
+                } else {
+                    alarm_active = 0;
+                }
             }
             during {
                 pump_speed = manual_switch_speed;
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:62390c35de9a4a1c3facba49abb8e4c3c839f88df974d7eb2eaad78a78da0be5`。
  - SL-10 evidence 1: `{"summary": "Both current SL-9 decisions accepted the same hard-blocking simulation repair: prevent Manual.enter from clearing alarm_active during pump-complication recovery while preserving normal Manual entry with no alarm. The candidate implements exactly that intent by replacing unconditional alarm_active = 0 in Manual.enter with if [pump_complication > 0] { alarm_active = 1; } else { alarm_active = 0; }."}`
  - SL-10 evidence 2: `{"summary": "The SD-6 failing scenarios showed recovery from AutocontrolNormal to Manual reached the correct Manual state and set control_released = 1, but alarm_active was overwritten to 0 by Manual.enter. In the candidate, a hot-start or PumpFault path with pump_complication = 1 will enter Manual and leave alarm_active = 1, resolving both pump_complication_guard_direct_to_manual and fault_effects_survive_recovery_to_manual."}`
  - SL-10 evidence 3: `{"summary": "The repair is consistent with the NL: pump faults such as fluid-tubing occlusion activate alarm signals, and when CARA was controlling the pump the software releases control. The candidate preserves the AutocontrolNormal -> Manual guard on pump_complication > 0 and preserves the transition effect setting alarm_active = 1 and control_released = 1."}`
  - SL-10 evidence 4: `{"summary": "The DSL diff is minimal and does not delete NL-required structure. CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, all required variables, the four backManual fallback events/transitions, InitiateAC, ChangeSetpoint, StartAC, PumpFault, the pump_complication guards, manual pump-speed/default-flow behavior, autocontrol flow-rate/logging behavior, alarm activation, and release-control behavior remain present."}`
  - SL-10 evidence 5: `{"summary": "The prior FixLog accepted the PumpFault addition as NL-grounded and previously waived the same local SD-10 missing-grounding rejection as conservative because the listed elements were visibly present. The current local check again reports missing_required_grounding for elements that are still textually present and were not touched by this diff, so it is evidence of matching conservatism rather than a new regression."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:fallback_CA_backManual_to_Manual", "transition:fallback_CB_backManual_to_Manual", "transition:fallback_CP_backManual_to_Manual", "transition:fallback_CC_backManual_to_Manual", "transition:Manual_to_Ask_StartAC", "transition:Ask_StartAC_change_setpoint", "transition:Ask_StartAC_to_AutocontrolInit", "transition:AutocontrolNormal_to_Manual_on_complication", "guard:no_pump_complic...<truncated 135 chars>

</details>

<details><summary>Repair 3 / iteration `2` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0, 1`。
- before_dsl_hash：`sha256:d80130b8e29f04e5c1f008e51d812660ed13135952eac183abb351b36c249f21`；candidate_dsl_hash：`sha256:3af25448acb0aa8176a168b10a7f96d65459f40b7cac136e633cb01135a966c6`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Fault recovery does not faithfully implement the NL sequence requiring caregiver fault removal; the DSL reaches Manual solely because `pump_complication > 0` and leaves the fault active.
- 2. `<unknown>` `` policy=``：The recovery model can resume manual pump speed/flow while an active pump complication remains present.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-2-sha256-1c602042228`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`2`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-2-sl7-0-e56a9044a1` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'nl_fidelity', 'evidence': ['NL says the caregiver removes the pump fault.', 'DSL has no event/action clearing `pump_complication`.', 'Simulation reaches Manual with `pump_complication: 1`.'], 'severity': 'major', 'summary': 'Fault recovery does not faithfully implement the NL sequence requiring caregiver fault removal; the DSL reaches Manual solely because `pump_complication > 0` and leaves the fault active.'}` |
| `fixreq-2-sl7-1-ef61a52a60` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['Manual.during unconditionally sets `pump_speed` and `flow_rate`.', 'Recovery transition to Manual is triggered by active `pump_complication > 0`.', 'Sim evidence shows Manual with active complication and nonzero manual outputs.'], 'severity': 'major', 'summary': 'The recovery model can resume manual pump speed/flow while an active pump complication remains present.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, variable:target_bp, variable:requested_target_bp, variable:patient_bp, variable:flow_rate, variable:default_flow_rate, variable:pump_speed, ... +28`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2368`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-2-sl7-0-e56a9044a1` | `accept` | ❌ | ❌ | The NL explicitly requires caregiver fault removal before safe recovery. The smallest coherent repair is to clear the internal pump_complication flag as part of the grounded AutocontrolNormal-to-Manual fault-recovery effect, while preserving alarm activation and software-control release.；intent=Add pump_complication = 0 to the AutocontrolNormal -> Manual rec...<truncated 91 chars> |
| `fixreq-2-sl7-1-ef61a52a60` | `accept` | ❌ | ❌ | Manual mode should not resume pump speed and flow while an active pump complication remains present. The repair guards Manual.during so manual outputs are set only when pump_complication has been cleared; otherwise outputs are driven to safe zero values and alarm/release remain active.；intent=Guard Manual.during manual speed/flow assignment with pump_complic...<truncated 68 chars> |
- repair_rationale：Preserves all required CARA and Mode_Control_Algorithm states, variables, fallback events, Ask_StartAC transitions, autocontrol behavior, logging, alarm activation, and release-control actions.；Models the NL-required caregiver fault removal by clearing pump_complication during grounded recovery from autocontrol to Manual.；Prevents unsafe manual pump speed/flow assignment if Manual is entered or hot-started while a pump complication is still active.
- diff_summary：`{"summary": "Manual.enter no longer clears alarm based on complication status; Manual.during only sets manual pump outputs when pump_complication == 0 and otherwise suppresses outputs with alarm/release active. The AutocontrolNormal -> Manual pump-complication recovery effect now clears pump_complication to represent caregiver fault removal before manual operation resumes."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float patient_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;
def float control_voltage = 0.0;
def int pump_complication = 0;
def int alarm_active = 0;
def int control_released = 0;
def int log_entries = 0;

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
                control_released = 1;
            }
            during {
                if [pump_complication == 0] {
                    pump_speed = manual_switch_speed;
                    flow_rate = default_flow_rate;
                } else {
                    pump_speed = 0.0;
                    flow_rate = 0.0;
                    alarm_active = 1;
                    control_released = 1;
                }
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                control_released = 0;
                pump_speed = control_voltage;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_complication == 0] {
                    flow_rate = target_bp - patient_bp;
                    pump_speed = control_voltage;
                    log_entries = log_entries + 1;
                } else {
                    alarm_active = 1;
                    control_released = 1;
                }
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
            target_bp = requested_target_bp;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC effect {
            control_released = 0;
        };
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> AutocontrolNormal :: PumpFault effect {
            pump_complication = 1;
            alarm_active = 1;
        };
        AutocontrolNormal -> Manual : if [pump_complication > 0] effect {
            alarm_active = 1;
            control_released = 1;
            pump_complication = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -25,15 +25,17 @@
         state Manual {
             enter {
                 control_released = 1;
-                if [pump_complication > 0] {
-                    alarm_active = 1;
-                } else {
-                    alarm_active = 0;
-                }
             }
             during {
-                pump_speed = manual_switch_speed;
-                flow_rate = default_flow_rate;
+                if [pump_complication == 0] {
+                    pump_speed = manual_switch_speed;
+                    flow_rate = default_flow_rate;
+                } else {
+                    pump_speed = 0.0;
+                    flow_rate = 0.0;
+                    alarm_active = 1;
+                    control_released = 1;
+                }
             }
         }
 
@@ -74,6 +76,7 @@
         AutocontrolNormal -> Manual : if [pump_complication > 0] effect {
             alarm_active = 1;
             control_released = 1;
+            pump_complication = 0;
         };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:0a1d4d02f98b0fb3ffdc65ecbdf7526bf9cce27267745b07a3bfb3fe21c9468a`。
  - SL-10 evidence 1: `{"summary": "Both current hard-blocking SL-9 requests were accepted and implemented: the AutocontrolNormal -> Manual pump-complication recovery effect now clears pump_complication to model the NL-required caregiver removal of the pump fault, and Manual.during is guarded so manual pump_speed/flow_rate assignments occur only when pump_complication == 0."}`
  - SL-10 evidence 2: `{"summary": "The candidate addresses the SL-7 NL-fidelity finding: the previous DSL reached Manual with pump_complication still active, while the candidate reaches Manual after alarm_active = 1, control_released = 1, and pump_complication = 0, representing fault removal before manual operation resumes."}`
  - SL-10 evidence 3: `{"summary": "The candidate addresses the unsafe-recovery finding without dropping required manual behavior: if Manual is entered or hot-started while pump_complication remains active, it suppresses pump_speed and flow_rate to 0 and keeps alarm/release active; when the recovery transition has cleared the complication, Manual resumes the NL-required built-in-switch/default-flow behavior."}`
  - SL-10 evidence 4: `{"summary": "Required NL-grounded structure is preserved in the DSL diff: CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, all required variables, backManual fallback events/transitions, InitiateAC, ChangeSetpoint, StartAC, PumpFault, the pump_complication guards, autocontrol calculation/logging, alarm activation, and release-control effects remain present."}`
  - SL-10 evidence 5: `{"summary": "Local SD-10 reports scenario_regression because two older scenarios still expected pump_complication to remain 1 after fault recovery, but that expectation conflicts with the current hard-blocking SL-7 requirement that the caregiver removes the pump fault and with SL-9's accepted edit intent to clear pump_complication. The missing_required_grounding portion repeats a previously judged conservative matcher issue for elements still textually present."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 11, "n_scenarios_passed": 9, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init verifies CARA dispatches to Manual and manual mode sets pump speed from the built-in switch and flow from the default pump rate.", "name": "default_initializes_to_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"alarm_active"...<truncated 20778 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:fallback_CA_backManual_to_Manual", "transition:fallback_CB_backManual_to_Manual", "transition:fallback_CP_backManual_to_Manual", "transition:fallback_CC_backManual_to_Manual", "transition:Manual_to_Ask_StartAC", "transition:Ask_StartAC_change_setpoint", "transition:Ask_StartAC_to_AutocontrolInit", "transition:AutocontrolNormal_to_Manual_on_complication", "guard:no_pump_complic...<truncated 135 chars>

</details>

<details><summary>Repair 4 / iteration `3` / source `SL-7` / accepted=✅</summary>

#### 为什么进入修复

- selected feedback source：`SL-7`；blocking=`True`；pre_scenario=`False`。
- problem_summary：model review failed
- diagnostic ids：`0`。
- before_dsl_hash：`sha256:3af25448acb0aa8176a168b10a7f96d65459f40b7cac136e633cb01135a966c6`；candidate_dsl_hash：`sha256:d5fc27ce2507b0b0d9533fba9817a55384364141ee57d7c0ad930290c88474ff`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：Fault recovery is modeled as an automatic transition that clears the pump complication without an explicit caregiver fault-removal action, which is unsafe relative to the NL sequence.

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-3-sha256-31963f0acfb`；source_stage=`SL-7`；legacy_plan_kind=`FixPlan`；requests=`1`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-3-sl7-0-65d2e7f559` | `review_fail` | ✅ | ❌ | model review failed | `{'category': 'unsafe_recovery', 'evidence': ['NL: "If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control."', 'DSL: AutocontrolNormal -> Manual : if [pump_complication > 0] effect { alarm_active = 1; control_released = 1; pump_complication = 0; }.', 'The transition clears pump_complication automatically on guard satisfaction; no caregiver-removes-fault event or confirmation guard is modeled before clearing the fault.'], 'severity': 'major', 'summary': 'Fault recovery is modeled as an automatic transition that clears the pump complication without an explicit caregiver fault-removal action, which is unsafe relative to the NL sequence.'}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, variable:target_bp, variable:requested_target_bp, variable:patient_bp, variable:flow_rate, variable:default_flow_rate, variable:pump_speed, ... +28`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2502`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-3-sl7-0-65d2e7f559` | `accept` | ❌ | ❌ | The review evidence is valid: the current guarded AutocontrolNormal-to-Manual recovery clears pump_complication automatically, without an explicit caregiver fault-removal action. The smallest safe repair is to preserve the required pump_complication guard and Manual recovery target, but stop clearing the fault on that automatic guard transition. Instead, add...<truncated 349 chars> |
- repair_rationale：The automatic pump-complication guard still releases software control and activates the alarm, preserving required fault recovery behavior.；The pump complication is no longer cleared by the automatic guard transition; it is cleared only by the explicit CaregiverRemovesFault event grounded in the NL caregiver-removal step.；Manual.during remains safe while a complication is active by suppressing pump speed and flow until the explicit removal event clears the fault.；All required states, variables, fallback events/transitions, Ask_StartAC behavior, autocontrol behavior, logging, alarm activation, and release-control actions are preserved.
- diff_summary：`{"summary": "Removed automatic pump_complication clearing from AutocontrolNormal -> Manual and added an explicit Manual :: CaregiverRemovesFault self-transition that clears the complication after caregiver fault removal."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float patient_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;
def float control_voltage = 0.0;
def int pump_complication = 0;
def int alarm_active = 0;
def int control_released = 0;
def int log_entries = 0;

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
                control_released = 1;
            }
            during {
                if [pump_complication == 0] {
                    pump_speed = manual_switch_speed;
                    flow_rate = default_flow_rate;
                } else {
                    pump_speed = 0.0;
                    flow_rate = 0.0;
                    alarm_active = 1;
                    control_released = 1;
                }
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                control_released = 0;
                pump_speed = control_voltage;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_complication == 0] {
                    flow_rate = target_bp - patient_bp;
                    pump_speed = control_voltage;
                    log_entries = log_entries + 1;
                } else {
                    alarm_active = 1;
                    control_released = 1;
                }
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Manual -> Manual :: CaregiverRemovesFault effect {
            pump_complication = 0;
            alarm_active = 0;
            control_released = 1;
        };
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
            target_bp = requested_target_bp;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC effect {
            control_released = 0;
        };
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> AutocontrolNormal :: PumpFault effect {
            pump_complication = 1;
            alarm_active = 1;
        };
        AutocontrolNormal -> Manual : if [pump_complication > 0] effect {
            alarm_active = 1;
            control_released = 1;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -62,6 +62,11 @@
         }
 
         Manual -> Ask_StartAC :: InitiateAC;
+        Manual -> Manual :: CaregiverRemovesFault effect {
+            pump_complication = 0;
+            alarm_active = 0;
+            control_released = 1;
+        };
         Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
             target_bp = requested_target_bp;
         };
@@ -76,7 +81,6 @@
         AutocontrolNormal -> Manual : if [pump_complication > 0] effect {
             alarm_active = 1;
             control_released = 1;
-            pump_complication = 0;
         };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`pass`，ok=`True`，target_resolved=`True`，regression_detected=`False`，drift_risk=`minor`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:83d30a0cb26340719b4e01d19f90f550dccb77821d08286a2b5a51fd0cd8b216`。
  - SL-10 evidence 1: `{"summary": "The current hard-blocking SL-7 request objected that AutocontrolNormal -> Manual automatically cleared pump_complication without an explicit caregiver fault-removal action. SL-9 accepted that request with a locked edit intent to remove pump_complication = 0 from the automatic guarded recovery and add an explicit CaregiverRemovesFault event in Manual. The candidate implements exactly that diff."}`
  - SL-10 evidence 2: `{"summary": "The candidate is better aligned with the NL sequence: a pump fault can set pump_complication via PumpFault, the guarded AutocontrolNormal -> Manual recovery activates alarm_active and releases control without clearing the fault, Manual suppresses pump outputs while pump_complication remains active, and only the explicit Manual :: CaregiverRemovesFault transition clears pump_complication after the caregiver action."}`
  - SL-10 evidence 3: `{"summary": "Required NL-grounded structure is preserved: CARA, Mode_Control_Algorithm, Manual, Ask_StartAC, AutocontrolInit, AutocontrolNormal, all required variables, the four backManual fallback events/transitions, InitiateAC, ChangeSetpoint, StartAC, the AutocontrolNormal pump_complication guard, no-complication guarded autocontrol behavior, manual switch/default-flow behavior when no complication is active, logging, alarm activation, and release-control behavior remain represented."}`
  - SL-10 evidence 4: `{"summary": "Local SD-10 reports scenario regressions because several older scenarios still expect the automatic recovery transition to clear pump_complication and immediately restore manual outputs. Those expectations conflict with the current hard-blocking review request and SL-9 accepted edit intent requiring an explicit caregiver fault-removal action before clearing the fault. The local missing_required_grounding list also repeats the previously observed conservative matcher issue for elements that remain textually present."}`
  - SL-10 evidence 5: `{"summary": "No NL-required state, event, guard, action, or scenario obligation is dropped by the candidate. The only substantive additions/removals are the removal of automatic fault clearing from AutocontrolNormal -> Manual and addition of the explicit CaregiverRemovesFault self-transition."}`
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
  - local_rejection：reason=`scenario_regression; missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `scenario_regression` {"kind": "scenario_regression", "sim_feedback": {"n_scenarios": 14, "n_scenarios_passed": 9, "ok": false, "oracle_weak": false, "scenario_results": [{"description": "default-init verifies CARA dispatches to Manual and manual mode sets pump speed from the built-in switch and flow from the default pump rate.", "name": "default_initializes_to_manual_outputs", "setup_error": null, "status": "pass", "step_results": [{"actual_state": "CARA.Mode_Control_Algorithm.Manual", "actual_vars": {"alarm_active"...<truncated 25192 chars>
    - local evidence 2: `missing_required_grounding` {"element_ids": ["event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:fallback_CA_backManual_to_Manual", "transition:fallback_CB_backManual_to_Manual", "transition:fallback_CP_backManual_to_Manual", "transition:fallback_CC_backManual_to_Manual", "transition:Manual_to_Ask_StartAC", "transition:Ask_StartAC_change_setpoint", "transition:Ask_StartAC_to_AutocontrolInit", "transition:AutocontrolNormal_to_Manual_on_complication", "guard:no_pump_complic...<truncated 135 chars>

</details>

<details><summary>Repair 5 / iteration `4` / source `SD-6` / accepted=❌</summary>

#### 为什么进入修复

- selected feedback source：`SD-6`；blocking=`True`；pre_scenario=`False`。
- problem_summary：simulation failed
- diagnostic ids：`pump_fault_event_alarms_then_releases_control, pump_complication_guard_direct_to_manual, constant_effects_exact_values_on_start_and_recovery, manual_recovery_clears_complication_exactly, pumpfault_target_and_effect_before_guard_recovery`。
- before_dsl_hash：`sha256:d5fc27ce2507b0b0d9533fba9817a55384364141ee57d7c0ad930290c88474ff`；candidate_dsl_hash：`sha256:52e0a3e7ac653bfd0e3a9d7ad45dd7a82d65868b3b3379a438097cdb74a4ba61`。

#### 错误证据 / diagnostics

- 1. `<unknown>` `` policy=``：
- 2. `<unknown>` `` policy=``：
- 3. `<unknown>` `` policy=``：
- 4. `<unknown>` `` policy=``：
- 5. `<unknown>` `` policy=``：

#### SD-8 FixRequestBatch / 修改请求

- batch_id：`fixbatch-4-sha256-d5f6aeec59a`；source_stage=`SD-6`；legacy_plan_kind=`FixPlan`；requests=`5`。

| request_id | severity | hard | waiver | problem | evidence |
|---|---|---:|---:|---|---|
| `fixreq-4-sd6-0-250e33b7f5` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start injects a pump fault during normal autocontrol, expecting alarm activation and then recovery to Manual with software control released.', 'name': 'pump_fault_event_alarms_then_releases_control', 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'alarm_active': 1, 'control_released': 1, 'control_voltage': 5.0, 'default_flow_rate': 6.0, 'flow_rate': 0.0, 'log_entries': 0, 'manual_switch_speed': 1.0, 'patient_bp': 75.0, 'pump_complication': 1, 'pump_speed': 0.0, 'requested_target_bp': 0.0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'pump_fault_activates_alarm', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'alarm_active': 1, 'control_released': 1, 'control_voltage': 5.0, 'default_flow_rate': 6.0, 'flow_rate': 0.0, 'log_entries': 0, 'manual_switch_speed': 1.0, 'patient_bp': 75.0, 'pump_complication': 1, 'pump_speed': 0.0, 'requested_target_bp': 0.0, 'target_bp': 100.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 1, 'step_name': 'fault_condition_recovers_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'flow_rate': {'actual': 0.0, 'expected': 6.0}, 'pump_complication': {'actual': 1, 'expected': 0}, 'pump_speed': {'actual': 0.0, 'expected': 1.0}}}]}` |
| `fixreq-4-sd6-1-43b1533e88` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start boundary probe for pump_complication > 0: an existing complication forces recovery from normal autocontrol to Manual.', 'name': 'pump_complication_guard_direct_to_manual', 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'alarm_active': 1, 'control_released': 1, 'control_voltage': 0.0, 'default_flow_rate': 8.0, 'flow_rate': 0.0, 'log_entries': 0, 'manual_switch_speed': 1.5, 'patient_bp': 0.0, 'pump_complication': 1, 'pump_speed': 0.0, 'requested_target_bp': 0.0, 'target_bp': 0.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'complication_releases_to_manual', 'var_assertion_ok': False, 'var_mismatches': {'flow_rate': {'actual': 0.0, 'expected': 8.0}, 'pump_complication': {'actual': 1, 'expected': 0}, 'pump_speed': {'actual': 0.0, 'expected': 1.5}}}]}` |
| `fixreq-4-sd6-2-4b83acece0` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start focuses M5/M6 probes on constant-valued effects: StartAC must set released control to exactly 0, PumpFault must set complication and alarm to exactly 1, and fault recovery must leave Manual with released control exactly 1 and complication cleared.', 'name': 'constant_effects_exact_values_on_start_and_recovery', 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolInit', 'actual_vars': {'alarm_active': 0, 'control_released': 0, 'control_voltage': 7.0, 'default_flow_rate': 11.5, 'flow_rate': 0.0, 'log_entries': 10, 'manual_switch_speed': 3.25, 'patient_bp': 85.0, 'pump_complication': 0, 'pump_speed': 7.0, 'requested_target_bp': 115.0, 'target_bp': 115.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'startac_sets_control_released_exact_zero', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'alarm_active': 0, 'control_released': 0, 'control_voltage': 7.0, 'default_flow_rate': 11.5, 'flow_rate': 30.0, 'log_entries': 11, 'manual_switch_speed': 3.25, 'patient_bp': 85.0, 'pump_complication': 0, 'pump_speed': 7.0, 'requested_target_bp': 115.0, 'target_bp': 115.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 1, 'step_name': 'normal_keeps_autocontrol_before_fault', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'alarm_active': 1, 'control_released': 1, 'control_voltage': 7.0, 'default_flow_rate': 11.5, 'flow_rate': 30.0, 'log_entries': 11, 'manual_switch_speed': 3.25, 'patient_bp': 85.0, 'pump_complication': 1, 'pump_speed': 7.0, 'requested_target_bp': 115.0, 'target_bp': 115.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 2, 'step_name': 'pumpfault_sets_exact_one_flags', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'alarm_active': 1, 'control_released': 1, 'control_voltage': 7.0, 'default_flow_rate': 11.5, 'flow_rate': 0.0, 'log_entries': 11, 'manual_switch_speed': 3.25, 'patient_bp': 85.0, 'pump_complication': 1, 'pump_speed': 0.0, 'requested_target_bp': 115.0, 'target_bp': 115.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 3, 'step_name': 'fault_recovery_manual_exact_outputs', 'var_assertion_ok': False, 'var_mismatches': {'flow_rate': {'actual': 0.0, 'expected': 11.5}, 'pump_complication': {'actual': 1, 'expected': 0}, 'pump_speed': {'actual': 0.0, 'expected': 3.25}}}]}` |
| `fixreq-4-sd6-3-4727e62452` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start adds a direct M5/M6 probe for the AutocontrolNormal-to-Manual recovery effect: a pre-existing pump complication must be removed exactly while Manual resumes switch/default-rate operation.', 'name': 'manual_recovery_clears_complication_exactly', 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'alarm_active': 1, 'control_released': 1, 'control_voltage': 0.0, 'default_flow_rate': 12.5, 'flow_rate': 0.0, 'log_entries': 0, 'manual_switch_speed': 4.5, 'patient_bp': 0.0, 'pump_complication': 1, 'pump_speed': 0.0, 'requested_target_bp': 0.0, 'target_bp': 0.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 0, 'step_name': 'recovery_effect_clears_fault_and_restores_manual_outputs', 'var_assertion_ok': False, 'var_mismatches': {'flow_rate': {'actual': 0.0, 'expected': 12.5}, 'pump_complication': {'actual': 1, 'expected': 0}, 'pump_speed': {'actual': 0.0, 'expected': 4.5}}}]}` |
| `fixreq-4-sd6-4-dcc9377d49` | `sim_fail` | ✅ | ❌ | simulation failed | `{'description': 'explicit-hot-start adds a focused M2/M5/M6 probe: PumpFault must first remain in AutocontrolNormal with exact fault effects before the following guard cycle recovers to Manual.', 'name': 'pumpfault_target_and_effect_before_guard_recovery', 'setup_error': None, 'status': 'fail', 'step_results': [{'actual_state': 'CARA.Mode_Control_Algorithm.AutocontrolNormal', 'actual_vars': {'alarm_active': 1, 'control_released': 1, 'control_voltage': 4.25, 'default_flow_rate': 15.5, 'flow_rate': 0.0, 'log_entries': 60, 'manual_switch_speed': 7.5, 'patient_bp': 90.0, 'pump_complication': 1, 'pump_speed': 0.0, 'requested_target_bp': 0.0, 'target_bp': 140.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'pass', 'step_index': 0, 'step_name': 'pumpfault_must_not_jump_directly_to_manual', 'var_assertion_ok': True, 'var_mismatches': {}}, {'actual_state': 'CARA.Mode_Control_Algorithm.Manual', 'actual_vars': {'alarm_active': 1, 'control_released': 1, 'control_voltage': 4.25, 'default_flow_rate': 15.5, 'flow_rate': 0.0, 'log_entries': 60, 'manual_switch_speed': 7.5, 'patient_bp': 90.0, 'pump_complication': 1, 'pump_speed': 0.0, 'requested_target_bp': 0.0, 'target_bp': 140.0}, 'runtime_error': None, 'state_assertion_ok': True, 'status': 'fail', 'step_index': 1, 'step_name': 'next_cycle_fault_guard_targets_manual', 'var_assertion_ok': False, 'var_mismatches': {'flow_rate': {'actual': 0.0, 'expected': 15.5}, 'pump_complication': {'actual': 1, 'expected': 0}, 'pump_speed': {'actual': 0.0, 'expected': 7.5}}}]}` |

#### SD-8 legacy fix plan / 修改建议

- recommended_strategy：Use diagnostics as hints; choose the smallest globally consistent repair.；Before returning a candidate, verify every required_preserve_element_id still has a concrete DSL representation.
- forbidden_edits：`Do not delete grounded required elements merely to silence diagnostics., Do not invent internal plant/environment dynamics merely to make external input variables appear written.`。
- required_preserve_element_ids：`hierarchical_state:CARA, hierarchical_state:Mode_Control_Algorithm, state:Manual, state:Ask_StartAC, state:AutocontrolInit, state:AutocontrolNormal, variable:target_bp, variable:requested_target_bp, variable:patient_bp, variable:flow_rate, variable:default_flow_rate, variable:pump_speed, ... +28`。

#### SL-9 per-request 决策

- accepted_request_ids：`<derived-from-table>`；candidate_len=`2571`。

| request_id | decision | waiver | rework_locked | rationale / intent |
|---|---|---:|---:|---|
| `fixreq-4-sd6-0-250e33b7f5` | `accept` | ❌ | ❌ | The simulation evidence shows PumpFault correctly activates the alarm and release flag, but the following guarded recovery reaches Manual with pump_complication still set, so Manual suppresses pump_speed and flow_rate. The smallest simulation repair is to clear pump_complication in the existing AutocontrolNormal -> Manual recovery effect so Manual resumes no...<truncated 138 chars> |
| `fixreq-4-sd6-1-43b1533e88` | `accept` | ❌ | ❌ | The direct pump_complication > 0 boundary probe already reaches Manual and releases control, but because the complication remains active Manual.during drives outputs to zero. Clearing pump_complication in the recovery effect restores the expected manual outputs.；intent=Clear pump_complication during guarded recovery to Manual. |
| `fixreq-4-sd6-2-4b83acece0` | `accept` | ❌ | ❌ | StartAC and PumpFault exact effects already pass; only the recovery step fails because pump_complication is not cleared and manual outputs remain suppressed. Adding the clear to the existing recovery effect preserves the passing exact effects while resolving the recovery mismatch.；intent=Preserve StartAC and PumpFault effects; clear pump_complication on the ...<truncated 20 chars> |
| `fixreq-4-sd6-3-4727e62452` | `accept` | ❌ | ❌ | The failing probe specifically targets the AutocontrolNormal-to-Manual recovery effect. Adding pump_complication = 0 to that effect makes the fault-removal state explicit at recovery completion and allows Manual.during to restore pump_speed and flow_rate from the switch/default rate.；intent=Update the AutocontrolNormal -> Manual recovery effect to clear the ...<truncated 46 chars> |
| `fixreq-4-sd6-4-dcc9377d49` | `accept` | ❌ | ❌ | The PumpFault event correctly remains in AutocontrolNormal with exact fault effects before the next guard cycle. The following guard cycle fails only because the recovery effect leaves pump_complication active. Clearing it in that effect preserves the required PumpFault staging and fixes the Manual recovery outputs.；intent=Keep PumpFault as a self-transition...<truncated 66 chars> |
- repair_rationale：The current failures all share one cause: guarded recovery reaches Manual while pump_complication remains 1, so Manual.during suppresses pump_speed and flow_rate.；Adding pump_complication = 0 to the existing AutocontrolNormal -> Manual effect is the smallest edit that restores expected manual outputs and keeps alarm_active and control_released set.；All required states, variables, fallback events, Ask_StartAC transitions, PumpFault staging, no-complication autocontrol behavior, logging, alarm activation, and release-control behavior are preserved.
- diff_summary：`{"summary": "Added pump_complication = 0 to the AutocontrolNormal -> Manual guarded recovery effect; no structural changes or grounded transitions were removed."}`。

#### SL-9 candidate / 最终修改执行方案

```pyfcstm
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float patient_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float pump_speed = 0.0;
def float manual_switch_speed = 0.0;
def float control_voltage = 0.0;
def int pump_complication = 0;
def int alarm_active = 0;
def int control_released = 0;
def int log_entries = 0;

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
                control_released = 1;
            }
            during {
                if [pump_complication == 0] {
                    pump_speed = manual_switch_speed;
                    flow_rate = default_flow_rate;
                } else {
                    pump_speed = 0.0;
                    flow_rate = 0.0;
                    alarm_active = 1;
                    control_released = 1;
                }
            }
        }

        state Ask_StartAC;

        state AutocontrolInit {
            enter {
                control_released = 0;
                pump_speed = control_voltage;
            }
        }

        state AutocontrolNormal {
            during {
                if [pump_complication == 0] {
                    flow_rate = target_bp - patient_bp;
                    pump_speed = control_voltage;
                    log_entries = log_entries + 1;
                } else {
                    alarm_active = 1;
                    control_released = 1;
                }
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Manual -> Manual :: CaregiverRemovesFault effect {
            pump_complication = 0;
            alarm_active = 0;
            control_released = 1;
        };
        Ask_StartAC -> Ask_StartAC :: ChangeSetpoint effect {
            target_bp = requested_target_bp;
        };
        Ask_StartAC -> AutocontrolInit :: StartAC effect {
            control_released = 0;
        };
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> AutocontrolNormal :: PumpFault effect {
            pump_complication = 1;
            alarm_active = 1;
            control_released = 1;
        };
        AutocontrolNormal -> Manual : if [pump_complication > 0] effect {
            alarm_active = 1;
            control_released = 1;
            pump_complication = 0;
        };
    }
}
```

#### Candidate diff（before -> candidate）

```diff
--- before.fcstm
+++ candidate.fcstm
@@ -77,10 +77,12 @@
         AutocontrolNormal -> AutocontrolNormal :: PumpFault effect {
             pump_complication = 1;
             alarm_active = 1;
+            control_released = 1;
         };
         AutocontrolNormal -> Manual : if [pump_complication > 0] effect {
             alarm_active = 1;
             control_released = 1;
+            pump_complication = 0;
         };
     }
 }
```

#### SL-10 审查结果

- SL-10 decision=`rework`，ok=`False`，target_resolved=`False`，regression_detected=`True`，drift_risk=`major`。
- SL-10 review_meta：schema=`SL10RepairReviewOutput.v1`，failure_policy=`fail_closed`，replay_key=`SL-10:sha256:caa32374751d92257aa4ad7e001c9512c615fb378016f9768f4f2e3ab31f3ddc`。
  - SL-10 evidence 1: `{"summary": "The current candidate resolves the immediate SD-6 simulation mismatch by adding pump_complication = 0 to the automatic AutocontrolNormal -> Manual guarded recovery effect, which would allow Manual.during to restore pump_speed and flow_rate. However, this directly regresses the hard SL-7 model-review issue from iteration 3: the NL says the caregiver removes the pump fault, and SL-9/SL-10 previously accepted an explicit Manual::CaregiverRemovesFault event precisely to avoid automatic fault clearing on guard satisfaction."}`
  - SL-10 evidence 2: `{"summary": "The complete FixLog shows iteration 3 accepted and passed a repair that removed automatic pump_complication clearing and added CaregiverRemovesFault as the explicit NL-grounded removal action. The candidate reintroduces the automatic clearing while leaving CaregiverRemovesFault redundant for the autocontrol fault-recovery path, so it drops the NL scenario obligation that caregiver removal precedes clearing the complication."}`
  - SL-10 evidence 3: `{"summary": "The DSL diff is not limited to harmless simulation cleanup: it changes the semantics of AutocontrolNormal -> Manual so the software clears the pump fault without an explicit caregiver event. This conflicts with the NL sequence: pump fault occurs, alarm signals activate, caregiver removes the fault, and when CARA was controlling the pump the software releases control."}`
  - SL-10 evidence 4: `{"summary": "The local SD-10 evidence reports missing_required_grounding for elements that have repeatedly been judged as conservative matcher misses and remain textually present. That local evidence is not the primary blocker. The blocker is the NL/FixLog regression caused by automatic clearing of pump_complication."}`
  - SL-10 evidence 5: `{"summary": "Required states, variables, fallback events/transitions, Ask_StartAC behavior, PumpFault staging, alarm activation, and release-control behavior are mostly preserved structurally, but the required caregiver-fault-removal scenario obligation is not preserved in the candidate semantics."}`
- SL-10 rework_instructions：Do not clear pump_complication in the automatic AutocontrolNormal -> Manual transition merely because pump_complication > 0. Remove pump_complication = 0 from that guarded recovery effect.；Preserve the explicit Manual -> Manual :: CaregiverRemovesFault transition as the NL-grounded caregiver fault-removal action, and keep its effect clearing pump_complication and keeping control_released = 1.；Preserve Manual.during safety behavior: while pump_complication > 0, suppress manual pump_speed and flow_rate and keep alarm/release active; after CaregiverRemovesFault clears pump_complication, Manual.during may restore pump_speed = manual_switch_speed and flow_rate = default_flow_rate.；Preserve the AutocontrolNormal -> Manual recovery target and its alarm_active = 1 and control_released = 1 effects, but make clear in the DSL semantics that this transition releases software control and alarms, not that it removes the physical fault.；Preserve all required NL-grounded states, variables, events, guards, actions, and fallback transitions, including PumpFault, CaregiverRemovesFault, the four backManual events, InitiateAC, ChangeSetpoint, StartAC, autocontrol logging/control actions, and manual switch/default-flow behavior after the fault has been explicitly removed.
- local checks evidence：stage=`SD-10`；note=PR-E1 uses local parse/semantic/design/sim checks as SL-10 evidence, not as the final deterministic judge.。
  - local ok=`False`，target_resolved=`False`，regression_detected=`False`，drift_risk=`major`。
  - local_rejection：reason=`missing_required_grounding`，rejected_by_stage=`SD-10`。
    - local evidence 1: `missing_required_grounding` {"element_ids": ["event:CA_backManual", "event:CB_backManual", "event:CP_backManual", "event:CC_backManual", "transition:fallback_CA_backManual_to_Manual", "transition:fallback_CB_backManual_to_Manual", "transition:fallback_CP_backManual_to_Manual", "transition:fallback_CC_backManual_to_Manual", "transition:Manual_to_Ask_StartAC", "transition:Ask_StartAC_change_setpoint", "transition:Ask_StartAC_to_AutocontrolInit", "transition:AutocontrolNormal_to_Manual_on_complication", "guard:no_pump_complic...<truncated 135 chars>

</details>


#### FixLog ledger

口径：FixLog 是跨 iteration 的 append-only repair 台账，记录 request batch、SL-9 accept/reject、diff/local evidence、SL-10 批示和下一步动作。

| # | iteration | phase | batch | decisions | next_action | candidate | notes |
|---:|---:|---|---|---|---|---|---|
| 1 | `0` | `request_batch` | `fixbatch-0-sha256-582b5000c55` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 2 | `0` | `sl9_decision` | `fixbatch-0-sha256-582b5000c55` | accept=2, reject=0 | `sl10_review` | `sha256:80e89626ea7f6fe4b1595dd499bde14d4b727623d5c42ad54814b3bed2d5c7c1` | The repair preserves all required states, variables, events, transitions, guards, and grounded actions., The new PumpFault event is grounded in the NL statement that pump faults such as occlusion can occur., The pump_complication variable is now meaningfully written before being read by the no-complication action guard and the transition-to-Manual guard., ... +1 |
| 3 | `0` | `sl10_review` | `fixbatch-0-sha256-582b5000c55` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:80e89626ea7f6fe4b1595dd499bde14d4b727623d5c42ad54814b3bed2d5c7c1` | <none> |
| 4 | `1` | `request_batch` | `fixbatch-1-sha256-96cbb2c7803` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 5 | `1` | `sl9_decision` | `fixbatch-1-sha256-96cbb2c7803` | accept=2, reject=0 | `sl10_review` | `sha256:d80130b8e29f04e5c1f008e51d812660ed13135952eac183abb351b36c249f21` | The failing variable is overwritten after the AutocontrolNormal -> Manual transition: transition effect sets alarm_active = 1, then Manual.enter sets alarm_active = 0., Making Manual.enter conditional on pump_complication preserves normal manual initialization with alarm inactive while keeping alarms active during fault/complication recovery., All required grounded states, variables, events, fallback transitions, Ask_StartAC transitions, pump-complication guards, logging action, alarm activation, and release-control behavior are preserved. |
| 6 | `1` | `sl10_review` | `fixbatch-1-sha256-96cbb2c7803` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:d80130b8e29f04e5c1f008e51d812660ed13135952eac183abb351b36c249f21` | <none> |
| 7 | `2` | `request_batch` | `fixbatch-2-sha256-1c602042228` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 8 | `2` | `sl9_decision` | `fixbatch-2-sha256-1c602042228` | accept=2, reject=0 | `sl10_review` | `sha256:3af25448acb0aa8176a168b10a7f96d65459f40b7cac136e633cb01135a966c6` | Preserves all required CARA and Mode_Control_Algorithm states, variables, fallback events, Ask_StartAC transitions, autocontrol behavior, logging, alarm activation, and release-control actions., Models the NL-required caregiver fault removal by clearing pump_complication during grounded recovery from autocontrol to Manual., Prevents unsafe manual pump speed/flow assignment if Manual is entered or hot-started while a pump complication is still active. |
| 9 | `2` | `sl10_review` | `fixbatch-2-sha256-1c602042228` | accept=2, reject=0 | `sc11_accept_then_sd2` | `sha256:3af25448acb0aa8176a168b10a7f96d65459f40b7cac136e633cb01135a966c6` | <none> |
| 10 | `3` | `request_batch` | `fixbatch-3-sha256-31963f0acfb` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 11 | `3` | `sl9_decision` | `fixbatch-3-sha256-31963f0acfb` | accept=1, reject=0 | `sl10_review` | `sha256:d5fc27ce2507b0b0d9533fba9817a55384364141ee57d7c0ad930290c88474ff` | The automatic pump-complication guard still releases software control and activates the alarm, preserving required fault recovery behavior., The pump complication is no longer cleared by the automatic guard transition; it is cleared only by the explicit CaregiverRemovesFault event grounded in the NL caregiver-removal step., Manual.during remains safe while a complication is active by suppressing pump speed and flow until the explicit removal event clears the fault., ... +1 |
| 12 | `3` | `sl10_review` | `fixbatch-3-sha256-31963f0acfb` | accept=1, reject=0 | `sc11_accept_then_sd2` | `sha256:d5fc27ce2507b0b0d9533fba9817a55384364141ee57d7c0ad930290c88474ff` | <none> |
| 13 | `4` | `request_batch` | `fixbatch-4-sha256-d5f6aeec59a` | accept=0, reject=0 | `sl9_decision_and_repair` | `<none>` | SD-8 produced FixRequestBatch; deterministic stage does not decide final repair. |
| 14 | `4` | `sl9_decision` | `fixbatch-4-sha256-d5f6aeec59a` | accept=5, reject=0 | `sl10_review` | `sha256:52e0a3e7ac653bfd0e3a9d7ad45dd7a82d65868b3b3379a438097cdb74a4ba61` | The current failures all share one cause: guarded recovery reaches Manual while pump_complication remains 1, so Manual.during suppresses pump_speed and flow_rate., Adding pump_complication = 0 to the existing AutocontrolNormal -> Manual effect is the smallest edit that restores expected manual outputs and keeps alarm_active and control_released set., All required states, variables, fallback events, Ask_StartAC transitions, PumpFault staging, no-complication autocontrol behavior, logging, alarm activation, and release-control behavior are preserved. |
| 15 | `4` | `sl10_review` | `fixbatch-4-sha256-d5f6aeec59a` | accept=5, reject=0 | `exit_rejected_rework_budget_exhausted` | `sha256:52e0a3e7ac653bfd0e3a9d7ad45dd7a82d65868b3b3379a438097cdb74a4ba61` | Do not clear pump_complication in the automatic AutocontrolNormal -> Manual transition merely because pump_complication > 0. Remove pump_complication = 0 from that guarded recovery effect., Preserve the explicit Manual -> Manual :: CaregiverRemovesFault transition as the NL-grounded caregiver fault-removal action, and keep its effect clearing pump_complication and keeping control_released = 1., Preserve Manual.during safety behavior: while pump_complication > 0, suppress manual pump_speed and flow_rate and keep alarm/release active; after CaregiverRemovesFault clears pump_complication, Manual.during may restore pump_speed = manual_switch_speed and flow_rate = default_flow_rate., ... +2 |

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 6812, 'model': 'gpt-5.5', 'prompt_tokens': 6191, 'total_tokens': 13003}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1802, 'model': 'gpt-5.5', 'prompt_tokens': 32135, 'total_tokens': 33937}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 723, 'model': 'gpt-5.5', 'prompt_tokens': 32583, 'total_tokens': 33306}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 5683, 'model': 'gpt-5.5', 'prompt_tokens': 13677, 'total_tokens': 19360}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4328, 'model': 'gpt-5.5', 'prompt_tokens': 16608, 'total_tokens': 20936}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4816, 'model': 'gpt-5.5', 'prompt_tokens': 17154, 'total_tokens': 21970}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1431, 'model': 'gpt-5.5', 'prompt_tokens': 54453, 'total_tokens': 55884}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 598, 'model': 'gpt-5.5', 'prompt_tokens': 54457, 'total_tokens': 55055}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4778, 'model': 'gpt-5.5', 'prompt_tokens': 17561, 'total_tokens': 22339}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 5680, 'model': 'gpt-5.5', 'prompt_tokens': 18147, 'total_tokens': 23827}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3003, 'model': 'gpt-5.5', 'prompt_tokens': 20060, 'total_tokens': 23063}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2626, 'model': 'gpt-5.5', 'prompt_tokens': 72239, 'total_tokens': 74865}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 927, 'model': 'gpt-5.5', 'prompt_tokens': 78585, 'total_tokens': 79512}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 6031, 'model': 'gpt-5.5', 'prompt_tokens': 18620, 'total_tokens': 24651}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 6298, 'model': 'gpt-5.5', 'prompt_tokens': 18914, 'total_tokens': 25212}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2570, 'model': 'gpt-5.5', 'prompt_tokens': 20435, 'total_tokens': 23005}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2053, 'model': 'gpt-5.5', 'prompt_tokens': 100101, 'total_tokens': 102154}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1007, 'model': 'gpt-5.5', 'prompt_tokens': 106397, 'total_tokens': 107404}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 6464, 'model': 'gpt-5.5', 'prompt_tokens': 19728, 'total_tokens': 26192}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 5132, 'model': 'gpt-5.5', 'prompt_tokens': 20162, 'total_tokens': 25294}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-9`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2009, 'model': 'gpt-5.5', 'prompt_tokens': 179065, 'total_tokens': 181074}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-10`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2081, 'model': 'gpt-5.5', 'prompt_tokens': 197602, 'total_tokens': 199683}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`not_converged`，record_status=`rejected`。
- 主要原因分类：`semantic_or_topology`。
- required stages executed：`69/17`，missing=`SD-10, SL-10B`。
- repairs：`4/5` accepted；scenario_history=`12`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。
