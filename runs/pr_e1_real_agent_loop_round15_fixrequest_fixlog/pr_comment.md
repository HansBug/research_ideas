## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/`。

| Path | case | config | verdict | status | clean | eligible | failure class | tokens | report |
|---|---|---|---|---|---:|---:|---|---:|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | `success` | 35812 | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233/report.md` |
| path1 | `path1_cara` | `default` | `not_converged` | `rejected` | ✅ | ❌ | `semantic_or_topology` | 1191726 | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | `success` | 33682 | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea/report.md` |
| path2 | `path2_lng_ems` | `default` | `success` | `success` | ✅ | ✅ | `success` | 261175 | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04/report.md` |

### 可复现性边界

- clean commit 绑定：4/4 run 的 `reproducibility.json` 记录 dirty=false。
- prompt snapshot hash 种类：1；用于确认同一轮 4 例是否共享同一 prompt/context 版本。
- 每个 run 的 `reproducibility.json` 保存 git commit、dirty flag、diff hash、prompt file hash、runner command/config 与 source/paper path。

### 初步观察

- `default`：3/4 success，rejected=1，budget_exhausted=0，total_tokens=1522395。
- 主结果候选：当前 3/4 run 可进入 main_result_eligible；其余只能作为 exploratory / infrastructure evidence。

### 主要失败模式

- `success`：3 run(s)。
- `semantic_or_topology`：1 run(s)。
- parse/semantic/topology 类问题说明 pyfcstm grammar 与层次路径约束仍需更强 prompt 约束或 repair context。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=semantic_or_topology，最大 observed iteration_count=5。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=success，最大 observed iteration_count=3。

### Reviewer 追加审查项：禁止样本特判 / benchmark overfit

- 后续三路 reviewer 需显式检查 agent-loop / prompt / deterministic policy 是否包含针对 ABS、CARA、Elevator、LNG EMS 或本 PR 4 个样本的 lexical special-case、case_id 分支、hard-coded hint、结果导向参数。
- 允许的优化必须是普适、可解释、可迁移的机制；例如通过 prompt 要求 LLM 区分外部输入与内部状态，而不是在代码中写样本专用词表。
- 若发现样本特判影响 blocking/advisory、repair target、scenario oracle 或主结论归类，应至少按 I 级处理；若污染 main_result_eligible 或论文结论则按 C 级处理。

### 4 例详细输入 / 输出 / artifact

<details><summary>path1 / path1_abs / default / success</summary>

#### NL 输入（原文）

```text
The paper implements the single-wheel ABS hydraulic regulator as a three-state FSM coupled with a PID-based slip controller. Wheel speed and vehicle speed are used to compute the slip ratio, and the PID output drives the Stateflow supervisor instead of sending commands directly to the hydraulic valves.

The FSM contains the states `increase`, `hold`, and `decrease`, where `increase` sets `k1=1, k2=0, n=0`, `hold` neutralizes both valves with `k1=0, k2=0, n=0`, and `decrease` sets `k1=0, k2=1, n=500` to release pressure.

The transition guards split the slip-error space into four bands: `increase -> hold` when `slp <= 0.01`, `hold -> increase` when `slp > 0.01`, `hold -> decrease` when `slp < -0.01`, and `decrease -> hold` when `slp >= -0.01`.

This gives a concrete discrete supervisor that maps slip-error thresholds to inlet-valve, return-valve, and pump actions while the continuous wheel-slip dynamics remain in the plant model.
```

#### NL 输入中文翻译

```text
论文把单轮 ABS 液压调节器实现为一个三状态 FSM，并与基于滑移率的 PID 控制器耦合。轮速与车速用于计算滑移率，PID 输出驱动 Stateflow 监督器，而不是直接发送液压阀命令。

FSM 包含 `increase`、`hold`、`decrease` 三个状态：`increase` 设置 `k1=1, k2=0, n=0`，`hold` 设置 `k1=0, k2=0, n=0`，`decrease` 设置 `k1=0, k2=1, n=500` 以释放压力。

转移 guard 把滑移误差空间分成四个区间：`increase -> hold` 当 `slp <= 0.01`，`hold -> increase` 当 `slp > 0.01`，`hold -> decrease` 当 `slp < -0.01`，`decrease -> hold` 当 `slp >= -0.01`。

这给出了一个具体的离散监督器，把滑移误差阈值映射为进油阀、回油阀与泵动作，而连续轮胎滑移动力学仍留在被控对象模型中。
```

#### FCSTM 输出

```pyfcstm
def float slp = 0.0;
def float wheel_speed = 0.0;
def float vehicle_speed = 0.0;
def int k1 = 0;
def int k2 = 0;
def int n = 0;

state ABSHydraulicRegulator {
    [*] -> increase;

    state increase {
        enter { k1 = 1; k2 = 0; n = 0; }
    }

    state hold {
        enter { k1 = 0; k2 = 0; n = 0; }
    }

    state decrease {
        enter { k1 = 0; k2 = 1; n = 500; }
    }

    increase -> hold : if [slp <= 0.01];
    hold -> increase : if [slp > 0.01];
    hold -> decrease : if [slp < -0.01];
    decrease -> hold : if [slp >= -0.01];
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 28614, 'completion_tokens': 7198, 'total_tokens': 35812, 'n_calls': 3}` / `148.43s` |
| full stage table | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233/pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233/checks.json`, `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=8847 | 生成初始 DSL 与 grounding seeds | initial len=551 | [`record`](./pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=10, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=12860 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=14105 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233.agent_loop.json.gz) |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_enters_increase_outputs` | default-init: first cycle dispatches the initial transition to increase and applies its valve and pump outputs. | ✅ |
| `increase_to_hold_at_positive_boundary` | explicit-hot-start: increase transitions to hold exactly at the inclusive slp <= 0.01 boundary and hold neutralizes outp...<truncated 4 chars> | ✅ |
| `increase_stays_above_positive_boundary` | explicit-hot-start: increase must not transition to hold when slp is just above the slp <= 0.01 band. | ✅ |
| `hold_to_increase_strict_positive` | explicit-hot-start: hold transitions to increase only when slp is strictly greater than 0.01 and increase sets inlet-val...<truncated 11 chars> | ✅ |
| `hold_no_fire_at_positive_equality` | explicit-hot-start: hold must not transition to increase at slp = 0.01 because the increase guard is strict slp > 0.01. | ✅ |
| `hold_to_decrease_strict_negative` | explicit-hot-start: hold transitions to decrease only when slp is strictly less than -0.01 and decrease commands pressur...<truncated 18 chars> | ✅ |
| `hold_no_fire_at_negative_equality` | explicit-hot-start: hold must not transition to decrease at slp = -0.01 because the decrease guard is strict slp < -0.01...<truncated 1 chars> | ✅ |
| `decrease_to_hold_negative_boundary` | explicit-hot-start: decrease transitions to hold exactly at the inclusive slp >= -0.01 boundary and hold neutralizes out...<truncated 5 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2713, 'model': 'gpt-5.5', 'prompt_tokens': 6134, 'total_tokens': 8847}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2427, 'model': 'gpt-5.5', 'prompt_tokens': 10433, 'total_tokens': 12860}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2058, 'model': 'gpt-5.5', 'prompt_tokens': 12047, 'total_tokens': 14105}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/17`，missing=`SD-8, SL-9, SD-10, SL-10B, SC-11`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_abs-default-round15fixrequestfixlog-aa45a233/report.md` §7。

</details>

<details><summary>path1 / path1_cara / default / not_converged</summary>

#### NL 输入（原文）

```text
At run time, CARA coordinates the Caregiver Interface, Blood Pressure Monitor, Algorithm, and Pump Monitors around an infusion pump that moves fluid into the patient, while sensor readings are stored in a shared buffer for software access. The pump has manual and autocontrol modes. In manual mode, pump speed is set with the built-in switch and the caregiver sets a default flow rate directly on the pump for manual operation, while in autocontrol mode pump speed is set by a control voltage from an external source. The Algorithm component controls infusion rate and records infusion-related data in log files; patient blood pressure is used to compute the infusion rate, with higher pressure producing a lower flow rate. The Caregiver Interface lets the caregiver modify target blood pressure and initiate or terminate algorithmic pump control, and it also displays and sounds error messages. In the Mode_Control_Algorithm hierarchy, CARA has manual and autocontrol-related mode-control states plus an Ask_StartAC submode; within Ask_StartAC, the setpoint can be changed and pressing StartAC enters AutocontrolInit. During normal autocontrol, CARA controls flow rate only while there are no pump-operation complications. If a pump fault such as fluid-tubing occlusion occurs, the pump activates alarm signals, the caregiver removes the fault, and when CARA was controlling the pump the software releases control. As a cross-component fallback, CA_backManual or any of CB_backManual, CP_backManual, or CC_backManual causes CA_mode to become Manual, making manual operation the shared recovery target.
```

#### NL 输入中文翻译

```text
运行时，CARA 围绕一台向患者输液的输液泵协调 Caregiver Interface、Blood Pressure Monitor、Algorithm 与 Pump Monitors，传感器读数会写入共享缓冲区供软件访问。泵具有手动和自动控制两种模式。手动模式下，泵速由内置开关设置，护理人员直接在泵上设置默认流量；自动控制模式下，泵速由外部控制电压设置。Algorithm 组件控制输液速率并记录输液相关日志；患者血压用于计算输液速率，血压越高流量越低。Caregiver Interface 允许护理人员修改目标血压，并启动或终止算法泵控制，同时显示和发出错误消息。在 Mode_Control_Algorithm 层次中，CARA 具有手动与自动控制相关的模式控制状态以及 Ask_StartAC 子模式；在 Ask_StartAC 中可以修改设定点，按下 StartAC 会进入 AutocontrolInit。正常自动控制期间，只有没有泵操作并发症时 CARA 才控制流量。如果出现输液管堵塞等泵故障，泵会激活报警信号，护理人员排除故障；当 CARA 正在控制泵时，软件会释放控制。作为跨组件回退，CA_backManual 或 CB_backManual、CP_backManual、CC_backManual 中任一事件都会使 CA_mode 变为 Manual，使手动操作成为共享恢复目标。
```

#### FCSTM 输出

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

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `rejected` |
| failure class | `semantic_or_topology` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `5` / `4` / `12` |
| token / elapsed | `{'prompt_tokens': 1114874, 'completion_tokens': 76852, 'total_tokens': 1191726, 'n_calls': 22}` / `2638.054s` |
| full stage table | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2/pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2/checks.json`, `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

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

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

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

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=pump_complication, W_GUARD_VARS_NEVER_CHANGE:from_path=CARA.Mode_Control_Algorithm.AutocontrolNormal:to_path=CARA.Mode_Control_Algorithm.Manual, W_UNWRITTEN_READ_VAR, W_GUARD_VARS_NEVER_CHANGE, W_HIGH_VAR_TO_LEAF_RATIO, ... +2 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:80e89626ea7f6fe4b1595dd499bde14d4b727623d5c42ad54814b3bed2d5c7c1` |
| 2 | `1` | ✅ | `SD-6` | pump_complication_guard_direct_to_manual, fault_effects_survive_recovery_to_manual | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:d80130b8e29f04e5c1f008e51d812660ed13135952eac183abb351b36c249f21` |
| 3 | `2` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:3af25448acb0aa8176a168b10a7f96d65459f40b7cac136e633cb01135a966c6` |
| 4 | `3` | ✅ | `SL-7` | 0 | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=scenario_regression; missing_required_grounding | `sha256:d5fc27ce2507b0b0d9533fba9817a55384364141ee57d7c0ad930290c88474ff` |
| 5 | `4` | ❌ | `SD-6` | pump_fault_event_alarms_then_releases_control, pump_complication_guard_direct_to_manual, constant_effects_exact_values_on_start_and_recovery, manual_recovery_clears_complication_exactly, pumpfault_target_and_effect_before_guard_recovery | accept=5, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Do not clear pump_complication in the automatic AutocontrolNormal -> Manual transition merely because pump_complication > 0. Remove pump_complication = 0 from that guarded reco...<truncated 343 chars> | `sha256:52e0a3e7ac653bfd0e3a9d7ad45dd7a82d65868b3b3379a438097cdb74a4ba61` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_cara-default-round15fixrequestfixlog-dfdf57d2/report.md` §7。

</details>

<details><summary>path1 / path1_elevator / default / success</summary>

#### NL 输入（原文）

```text
The automatic elevator controller is built as a finite-state machine whose state space combines floor states `F1`, `F2`, and `F3` with motion states `MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel.

In the normal workflow, the system starts from an ideal state on floor 1, chooses either the up or down branch according to floor requests, stops at the requested floor, and then immediately checks the next destination before deciding whether to continue moving.

The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as sensing inputs for arrival. From `F1`, `PS2` triggers `MU2` and `PS3` triggers `MU3`. From `F2`, `PS3` triggers `MU3` and `PS1` triggers `MD1`. From `F3`, `PS1` triggers `MD1` and `PS2` triggers `MD2`. Arrival sensors complete motion transitions: `MU2 + S2 -> F2`, `MU3 + S3 -> F3`, `MD1 + S1 -> F1`, and `MD2 + S2 -> F2`.

The `hbrg` output distinguishes upward drive, downward drive, and stop conditions. A reset signal forces the controller back to floor 1 regardless of the outstanding request context.
```

#### NL 输入中文翻译

```text
自动电梯控制器被构建为有限状态机，其状态空间由楼层状态 `F1`、`F2`、`F3` 与上/下行运动状态 `MU2`、`MU3`、`MD1`、`MD2` 组合而成。

正常流程中，系统从 1 楼理想状态开始，根据楼层请求选择上行或下行分支，在请求楼层停止，然后立即检查下一目的地以决定是否继续移动。

控制器使用 `PS1/PS2/PS3` 作为楼层请求输入，使用 `S1/S2/S3` 作为到位传感输入。从 `F1`，`PS2` 触发 `MU2`，`PS3` 触发 `MU3`；从 `F2`，`PS3` 触发 `MU3`，`PS1` 触发 `MD1`；从 `F3`，`PS1` 触发 `MD1`，`PS2` 触发 `MD2`。到位传感器完成运动转移：`MU2 + S2 -> F2`，`MU3 + S3 -> F3`，`MD1 + S1 -> F1`，`MD2 + S2 -> F2`。

`hbrg` 输出区分上行驱动、下行驱动和停止状态。复位信号会无视当前请求上下文，强制控制器回到 1 楼。
```

#### FCSTM 输出

```pyfcstm
def int hbrg = 0;

state AutomaticElevatorController {
    ! * -> F1 :: Reset;

    [*] -> F1;

    state F1 {
        enter { hbrg = 0; }
    }

    state F2 {
        enter { hbrg = 0; }
    }

    state F3 {
        enter { hbrg = 0; }
    }

    state MU2 {
        enter { hbrg = 1; }
    }

    state MU3 {
        enter { hbrg = 1; }
    }

    state MD1 {
        enter { hbrg = -1; }
    }

    state MD2 {
        enter { hbrg = -1; }
    }

    F1 -> MU2 :: PS2;
    F1 -> MU3 :: PS3;
    F2 -> MU3 :: PS3;
    F2 -> MD1 :: PS1;
    F3 -> MD1 :: PS1;
    F3 -> MD2 :: PS2;
    MU2 -> F2 :: S2;
    MU3 -> F3 :: S3;
    MD1 -> F1 :: S1;
    MD2 -> F2 :: S2;
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 25940, 'completion_tokens': 7742, 'total_tokens': 33682, 'n_calls': 3}` / `227.516s` |
| full stage table | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea/pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea/checks.json`, `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9607 | 生成初始 DSL 与 grounding seeds | initial len=669 | [`record`](./pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13312 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10763 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea.agent_loop.json.gz) |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_initial_dispatch_to_f1_idle_stop` | default-init probe: first empty cycle must dispatch initial transition to F1 with stopped hbrg, and another no-event cyc...<truncated 31 chars> | ✅ |
| `f1_to_f2_then_f2_to_f3_up_sequence` | explicit-hot-start probe: from F1, PS2 should drive upward to MU2, S2 should stop at F2, then PS3 should drive upward to...<truncated 23 chars> | ✅ |
| `f1_direct_request_floor3_arrives_f3` | explicit-hot-start probe: from F1, PS3 must target MU3 rather than MU2, and S3 must complete arrival at F3 with stop out...<truncated 4 chars> | ✅ |
| `f2_request_floor1_down_to_f1` | explicit-hot-start probe: from F2, PS1 must enter downward motion MD1 and S1 must arrive at F1 with stopped hbrg. | ✅ |
| `f3_request_floor2_down_to_f2` | explicit-hot-start probe: from F3, PS2 must target MD2 downward motion and S2 must complete arrival at F2 with stop outp...<truncated 3 chars> | ✅ |
| `f3_request_floor1_down_to_f1` | explicit-hot-start probe: from F3, PS1 must target MD1 rather than MD2, and S1 must complete arrival at F1 with stop out...<truncated 4 chars> | ✅ |
| `reset_from_up_motion_forces_f1` | explicit-hot-start forced-transition probe: Reset during upward MU3 motion must force F1 regardless of outstanding reque...<truncated 25 chars> | ✅ |
| `reset_from_down_motion_and_floor_forces_f1` | explicit-hot-start forced-transition probe: Reset must force F1 both from downward motion and from a floor context, with...<truncated 14 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3428, 'model': 'gpt-5.5', 'prompt_tokens': 6179, 'total_tokens': 9607}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2384, 'model': 'gpt-5.5', 'prompt_tokens': 10928, 'total_tokens': 13312}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1930, 'model': 'gpt-5.5', 'prompt_tokens': 8833, 'total_tokens': 10763}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/17`，missing=`SD-8, SL-9, SD-10, SL-10B, SC-11`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path1_elevator-default-round15fixrequestfixlog-17b490ea/report.md` §7。

</details>

<details><summary>path2 / path2_lng_ems / default / success</summary>

#### NL 输入（原文）

```text
The LNG-ship EMS manages a ship energy system with PVs, WECs, DGs, LNG, batteries, and time-varying ship loads, issuing cut-in and cut-out commands for generating units and loads. It controls power dispatch between generating units and load demand during changing time periods and operating conditions, dynamically switching states to maintain power balance as resources and demands vary. The FSM reads load demand PL, renewable contributions Ppv and Pw, battery state of charge SoC, and engine capacity bounds such as eng3_Pmax, then returns requested generator power, battery discharge or charging power, and spare power. The twelve finite states are selected by logical transition conditions over demand, generation, capacity, and SoC. When Ppv + Pw covers PL, the EMS serves all ship demand from RES and charges batteries while SoC is below 0.95, or treats residual renewable power as spare once SoC is at least 0.95. When Ppv + Pw is below PL, dispatch follows the stated priority: RES first, batteries when SoC is suitable, LNG before diesel units, and DG1/DG2 only as the last priority. Low-SoC branches add explicit charging margins, including Pgmax/5 in an LNG-covered case and Pd1max/10 in later diesel-generator cases. When PL = 0, RES production is sent to battery charging or to spare power according to SoC thresholds. The overload completion state is illegal: if extreme demand exceeds all RES and thermal resources, EMS activates all thermal generating units, covers the lack by battery discharge, and the state shall never occur in practice.
```

#### NL 输入中文翻译

```text
LNG 船 EMS 管理一个包含光伏、波浪能、柴油机、LNG、电池和随时间变化船舶负载的船舶能源系统，并向发电单元与负载发出切入/切出命令。它在变化的时段和运行条件下控制发电单元与负载需求之间的功率调度，随着资源和需求变化动态切换状态以保持功率平衡。FSM 读取负载需求 PL、可再生贡献 Ppv 和 Pw、电池荷电状态 SoC，以及 eng3_Pmax 等发动机容量边界，然后返回请求的发电机功率、电池放电或充电功率以及备用功率。十二个有限状态由需求、发电、容量和 SoC 上的逻辑转移条件选择。当 Ppv + Pw 覆盖 PL 时，EMS 用 RES 满足全部船舶需求，并在 SoC 低于 0.95 时给电池充电，或在 SoC 至少为 0.95 时把剩余可再生功率视为备用功率。当 Ppv + Pw 低于 PL 时，调度遵循优先级：RES 优先，SoC 合适时使用电池，LNG 先于柴油机，DG1/DG2 只作为最后优先级。低 SoC 分支加入明确充电裕量，包括 LNG 覆盖场景中的 Pgmax/5，以及后续柴油发电机场景中的 Pd1max/10。当 PL = 0 时，RES 产出根据 SoC 阈值送往电池充电或备用功率。过载完成状态是非法状态：若极端需求超过全部 RES 与热力资源，EMS 会激活全部热发电单元并用电池放电弥补缺口，该状态实践中不应发生。
```

#### FCSTM 输出

```pyfcstm
def float PL = 0.0;
def float Ppv = 0.0;
def float Pw = 0.0;
def float SoC = 0.5;
def float Pgmax = 0.0;
def float eng3_Pmax = 0.0;
def float Pd1max = 0.0;
def float Pd2max = 0.0;
def float Pbatmax = 0.0;
def float Pg_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cut_in_LNG = 0;
def int cut_in_eng3 = 0;
def int cut_in_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_out_loads = 0;

state LNGShipEMS {
    ! * -> ZeroLoad_Charge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoad_Spare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> ZeroLoad_Idle : if [PL == 0 && Ppv + Pw == 0];
    ! * -> RES_Charge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RES_Spare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> Battery_Assist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbatmax];
    ! * -> LNG_Covered : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbatmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNG_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNG_Eng3_Covered : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1_LowSoC_ChargeMargin : if [PL > 0 && Ppv + Pw < PL && ((SoC < 0.2 && PL - Ppv - Pw + Pd1max / 10 > Pgmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max) || (SoC >= 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max))];
    ! * -> DG2_LastPriority : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> IllegalOverloadCompletion : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> RES_Charge;

    state ZeroLoad_Charge {
        enter {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_eng3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_loads = 0;
        }
    }

    state ZeroLoad_Spare {
        enter {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            cut_in_LNG = 0;
            cut_in_eng3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_loads = 0;
        }
    }

    state ZeroLoad_Idle {
        enter {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_eng3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_loads = 0;
        }
    }

    state RES_Charge {
        enter {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_eng3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_loads = 0;
        }
    }

    state RES_Spare {
        enter {
            Pg_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_in_eng3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_loads = 0;
        }
    }

    state Battery_Assist {
        enter {
            Pg_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_eng3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_loads = 0;
        }
    }

    state LNG_Covered {
        enter {
            Pg_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_eng3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_loads = 0;
        }
    }

    state LNG_LowSoC_ChargeMargin {
        enter {
            Pg_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_eng3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_loads = 0;
        }
    }

    state LNG_Eng3_Covered {
        enter {
            Pg_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_eng3 = 1;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_out_loads = 0;
        }
    }

    state DG1_LowSoC_ChargeMargin {
        enter {
            if [SoC < 0.2] {
                Pg_req = PL - Ppv - Pw + Pd1max / 10;
                Pbat_charge = Pd1max / 10;
            } else {
                Pg_req = PL - Ppv - Pw;
                Pbat_charge = 0.0;
            }
            Pbat_discharge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_eng3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_out_loads = 0;
        }
    }

    state DG2_LastPriority {
        enter {
            Pg_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_eng3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_out_loads = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            Pg_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_eng3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_out_loads = 0;
        }
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `3` / `2` / `2` / `4` |
| token / elapsed | `{'prompt_tokens': 230300, 'completion_tokens': 30875, 'total_tokens': 261175, 'n_calls': 9}` / `1148.884s` |
| full stage table | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04/pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04/checks.json`, `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12959 | 生成初始 DSL 与 grounding seeds | initial len=5851 | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=162, info=0; blocking=0, advisory=162, info=0; blocking=0, advisory=162, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=2, tokens=43651 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=2, tokens=43651 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ⚠️ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=57767 | LLM per-request accept/reject + repair | candidate len=5839,6090 | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=51508 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=162, info=0; blocking=0, advisory=162, info=0; blocking=0, advisory=162, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=95290 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=2, tokens=57767 | LLM per-request accept/reject + repair | candidate len=5839,6090 | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=2, tokens=51508 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=162, info=0; blocking=0, advisory=162, info=0; blocking=0, advisory=162, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=False, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SL-7` | 是 | 1 | ✅ | LLM calls=2, tokens=95290 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04.agent_loop.json.gz) |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 | Iter 2 | Iter 3 |
|---|---|---|---|---|
| `default_init_dispatches_initial_leaf` | default-init probe: after the first empty cycle the model should dispatch to its declared initial EMS leaf and initializ...<truncated 15 chars> | ✅ | ✅ | ✅ |
| `zero_load_charge_spare_idle_selection` | explicit-hot-start probe: zero-load RES production is routed to charging below SoC 0.95, checking the zero-load charging...<truncated 8 chars> | ✅ | ✅ | ✅ |
| `zero_load_spare_at_soc_boundary` | explicit-hot-start probe: at PL=0 with renewable production and SoC exactly 0.95, RES should be treated as spare power. | ✅ | ✅ | ✅ |
| `zero_load_idle_no_res` | explicit-hot-start probe: when PL is zero and there is no renewable production, the EMS should idle with all outputs zer...<truncated 2 chars> | ✅ | ✅ | ✅ |
| `renewables_cover_load_soc_boundary` | explicit-hot-start probe: when RES covers positive load, surplus charges below SoC 0.95. | ✅ | ✅ | ✅ |
| `renewables_cover_load_spare_at_soc_boundary` | explicit-hot-start probe: when RES covers positive load and SoC is exactly 0.95, surplus should become spare power. | ✅ | ✅ | ✅ |
| `battery_assist_at_low_soc_boundary` | explicit-hot-start probe: with RES below demand and suitable SoC exactly at 0.2, batteries cover the deficit before LNG ...<truncated 17 chars> | ✅ | ✅ | ✅ |
| `lng_priority_and_low_soc_margin` | explicit-hot-start probe: LNG covers deficits before diesel when SoC is suitable. | ✅ | ✅ | ✅ |
| `lng_low_soc_charge_margin` | explicit-hot-start probe: low SoC in an LNG-covered case adds the Pgmax/5 charging margin. | ❌ | ✅ | ✅ |
| `lng_plus_eng3_covers_before_dg_units` | explicit-hot-start probe: when LNG alone is insufficient but LNG plus eng3 capacity covers the deficit, cut in LNG and e...<truncated 20 chars> | ✅ | ✅ | ✅ |
| `dg1_low_soc_margin_before_dg2` | explicit-hot-start probe: low-SoC later diesel branch cuts in DG1 and adds the Pd1max/10 battery charging margin before ...<truncated 10 chars> | ✅ | ✅ | ✅ |
| `dg2_last_priority_and_extreme_overload` | explicit-hot-start probe: DG2 is only used after LNG, eng3, and DG1 capacity are insufficient. | ✅ | ✅ | ✅ |
| `extreme_overload_uses_all_resources` | explicit-hot-start probe: beyond all thermal resources, the illegal overload completion dispatches all units and battery...<truncated 37 chars> | ✅ | ✅ | ✅ |
| `forced_transition_reselects_res_spare_from_idle` | explicit-hot-start forced-transition probe: from a concrete non-RES leaf, the global guarded forced selector must move t...<truncated 37 chars> | ✅ | ✅ | ✅ |
| `forced_transition_reselects_battery_from_thermal_leaf` | explicit-hot-start forced-transition probe: from a concrete thermal leaf, the global guarded forced selector must move t...<truncated 74 chars> | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-6` | lng_low_soc_charge_margin | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:8750a29c4aa89f25f5051842ff47a3b37629bc1d09559fda4ae45a5366f02114` |
| 2 | `1` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:bac9d466ccf524798ec7a6fa39d84a0c73c9c01604a1d01a96f91e82c93d94b6` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_e1_real_agent_loop_round15_fixrequest_fixlog/pr-e1-path2_lng_ems-default-round15fixrequestfixlog-60382b04/report.md` §7。

</details>
