## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/`。

| Path | case | config | verdict | status | clean | eligible | failure class | tokens | report |
|---|---|---|---|---|---:|---:|---|---:|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | `success` | 45164 | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_abs-default-round21compact-0c1e940c/report.md` |
| path1 | `path1_cara` | `default` | `not_converged` | `budget_exhausted` | ✅ | ❌ | `scenario_or_sim_oracle` | 438879 | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_cara-default-round21compact-d7784c4f/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | `success` | 35350 | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_elevator-default-round21compact-44c5c0fd/report.md` |
| path2 | `path2_lng_ems` | `default` | `not_converged` | `budget_exhausted` | ✅ | ❌ | `budget` | 539212 | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path2_lng_ems-default-round21compact-92de717a/report.md` |

### 可复现性边界

- clean commit 绑定：4/4 run 的 `reproducibility.json` 记录 dirty=false。
- prompt snapshot hash 种类：1；用于确认同一轮 4 例是否共享同一 prompt/context 版本。
- 每个 run 的 `reproducibility.json` 保存 git commit、dirty flag、diff hash、prompt file hash、runner command/config 与 source/paper path。

### 初步观察

- `default`：2/4 success，rejected=0，budget_exhausted=2，total_tokens=1058605。
- 主结果候选：当前 2/4 run 可进入 main_result_eligible；其余只能作为 exploratory / infrastructure evidence。

### 主要失败模式

- `success`：2 run(s)。
- `budget`：1 run(s)。
- `scenario_or_sim_oracle`：1 run(s)。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=scenario_or_sim_oracle，最大 observed iteration_count=5。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=budget，最大 observed iteration_count=5。

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
def int k1 = 0;
def int k2 = 0;
def int n = 0;

state ABSHydraulicRegulator {
    [*] -> increase;

    state increase {
        enter {
            k1 = 1;
            k2 = 0;
            n = 0;
        }
    }

    state hold {
        enter {
            k1 = 0;
            k2 = 0;
            n = 0;
        }
    }

    state decrease {
        enter {
            k1 = 0;
            k2 = 1;
            n = 500;
        }
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
| token / elapsed | `{'prompt_tokens': 35597, 'completion_tokens': 9568, 'total_tokens': 45164, 'n_calls': 3}` / `137.394s` |
| full stage table | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_abs-default-round21compact-0c1e940c/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_abs-default-round21compact-0c1e940c/pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_abs-default-round21compact-0c1e940c/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_abs-default-round21compact-0c1e940c/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_abs-default-round21compact-0c1e940c/checks.json`, `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_abs-default-round21compact-0c1e940c/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=12964 | 生成初始 DSL 与 grounding seeds | initial len=623 | [`record`](./pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=8, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=19858 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=12342 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-round21compact-0c1e940c.agent_loop.json.gz) |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_increase_then_hold_at_default_slip` | default-init: first empty cycle dispatches to increase with inlet active, then default slp=0.0 satisfies increase->hold ...<truncated 23 chars> | ✅ |
| `increase_to_hold_at_positive_boundary` | explicit-hot-start: increase must transition to hold exactly at slp=0.01 because the guard is slp <= 0.01. | ✅ |
| `increase_no_fire_above_positive_boundary` | explicit-hot-start: increase must remain increase just above slp=0.01, catching an overly broad increase->hold guard. | ✅ |
| `hold_no_fire_at_positive_boundary` | explicit-hot-start: hold must not transition to increase at slp=0.01 because hold->increase requires slp > 0.01. | ✅ |
| `hold_to_increase_above_positive_boundary` | explicit-hot-start: hold must transition to increase when slp is just above 0.01 and set increase outputs. | ✅ |
| `hold_no_fire_at_negative_boundary` | explicit-hot-start: hold must not transition to decrease at slp=-0.01 because hold->decrease requires slp < -0.01. | ✅ |
| `hold_to_decrease_below_negative_boundary` | explicit-hot-start: hold must transition to decrease when slp is just below -0.01 and command pressure release. | ✅ |
| `decrease_to_hold_at_negative_boundary` | explicit-hot-start: decrease must transition to hold exactly at slp=-0.01 because decrease->hold is slp >= -0.01. | ✅ |
| `decrease_no_fire_below_negative_boundary` | explicit-hot-start: decrease must remain decrease just below -0.01, catching an overly broad decrease->hold guard. | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3320, 'model': 'gpt-5.5', 'prompt_tokens': 9645, 'total_tokens': 12964}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 4422, 'model': 'gpt-5.5', 'prompt_tokens': 15436, 'total_tokens': 19858}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1826, 'model': 'gpt-5.5', 'prompt_tokens': 10516, 'total_tokens': 12342}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_abs-default-round21compact-0c1e940c/report.md` §7。

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

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `budget_exhausted` |
| failure class | `scenario_or_sim_oracle` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `7` / `5` / `10` |
| token / elapsed | `{'prompt_tokens': 372500, 'completion_tokens': 66379, 'total_tokens': 438879, 'n_calls': 23}` / `1992.751s` |
| full stage table | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_cara-default-round21compact-d7784c4f/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_cara-default-round21compact-d7784c4f/pr-e1-path1_cara-default-round21compact-d7784c4f.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_cara-default-round21compact-d7784c4f/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_cara-default-round21compact-d7784c4f/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_cara-default-round21compact-d7784c4f/checks.json`, `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_cara-default-round21compact-d7784c4f/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

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

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

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
| `cc_backmanual_manual_reentry_missing_line_probe` | explicit-hot-start: CC_
... <truncated 1048 chars in PR comment; see report.md>

#### Repair / blocking feedback 概览（report §7 摘录）

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

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_cara-default-round21compact-d7784c4f/report.md` §7。

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
    ! * -> F1 :: reset;

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
| token / elapsed | `{'prompt_tokens': 26602, 'completion_tokens': 8748, 'total_tokens': 35350, 'n_calls': 3}` / `165.619s` |
| full stage table | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_elevator-default-round21compact-44c5c0fd/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_elevator-default-round21compact-44c5c0fd/pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_elevator-default-round21compact-44c5c0fd/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_elevator-default-round21compact-44c5c0fd/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_elevator-default-round21compact-44c5c0fd/checks.json`, `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_elevator-default-round21compact-44c5c0fd/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=10011 | 生成初始 DSL 与 grounding seeds | initial len=669 | [`record`](./pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=14694 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10645 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round21compact-44c5c0fd.agent_loop.json.gz) |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_f1_to_f2_then_continue_up` | default-init probe: initial dispatch must land on F1 stopped, PS2 must drive upward to MU2, S2 must stop at F2, then a n...<truncated 37 chars> | ✅ |
| `explicit_f1_request_f3_arrival` | explicit-hot-start probe: from F1, PS3 must choose direct upward motion MU3 and S3 must stop at F3. | ✅ |
| `explicit_f2_request_f1_arrival` | explicit-hot-start probe: from F2, PS1 must drive downward to MD1 and S1 must stop at F1. | ✅ |
| `explicit_f3_request_f1_arrival` | explicit-hot-start probe: from F3, PS1 must choose downward motion MD1 and S1 must return to stopped F1. | ✅ |
| `explicit_f3_request_f2_arrival` | explicit-hot-start probe: from F3, PS2 must choose downward motion MD2 and S2 must stop at F2. | ✅ |
| `reset_from_up_motion_to_f1` | explicit-hot-start forced-transition probe: reset from an upward motion state must force F1 and stop the drive. | ✅ |
| `reset_from_down_motion_to_f1` | explicit-hot-start forced-transition probe: reset from a downward motion state must force F1 and stop the drive regardle...<truncated 22 chars> | ✅ |
| `no_event_stability_floor_and_motion` | default-init no-fire probe: without request or arrival events, a floor state must remain stopped and a motion state must...<truncated 63 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SL-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3832, 'model': 'gpt-5.5', 'prompt_tokens': 6179, 'total_tokens': 10011}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3378, 'model': 'gpt-5.5', 'prompt_tokens': 11316, 'total_tokens': 14694}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1538, 'model': 'gpt-5.5', 'prompt_tokens': 9107, 'total_tokens': 10645}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/12`，missing=`<none>`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path1_elevator-default-round21compact-44c5c0fd/report.md` §7。

</details>

<details><summary>path2 / path2_lng_ems / default / not_converged</summary>

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
def float SoC = 0.0;
def float eng3_Pmax = 0.0;
def float Pgmax = 0.0;
def float Pd1max = 0.0;
def float LNG_Pmax = 0.0;
def float DG1_Pmax = 0.0;
def float DG2_Pmax = 0.0;
def float DG3_Pmax = 0.0;
def float total_thermal_Pmax = 0.0;
def float requested_generator_power = 0.0;
def float battery_discharge_power = 0.0;
def float battery_charge_power = 0.0;
def float spare_power = 0.0;
def int cut_in_command = 0;
def int cut_out_command = 0;

state LNGShipEMS {
    enter {
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    >> during before {
        total_thermal_Pmax = LNG_Pmax + eng3_Pmax + DG1_Pmax + DG2_Pmax;
    }

    ! * -> ZeroLoadCharge : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0.0 && Ppv + Pw > 0.0 && SoC >= 0.95];
    ! * -> RESCharge : if [PL > 0.0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESSpare : if [PL > 0.0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryDischarge : if [PL > 0.0 && Ppv + Pw < PL && SoC > 0.2 && PL - Ppv - Pw <= total_thermal_Pmax];
    ! * -> LNGChargeMargin : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw + Pgmax / 5.0 <= LNG_Pmax];
    ! * -> LNGNormal : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw <= LNG_Pmax];
    ! * -> DG3LNG : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax && PL - Ppv - Pw <= LNG_Pmax + eng3_Pmax];
    ! * -> DG1AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= LNG_Pmax + eng3_Pmax + DG1_Pmax];
    ! * -> DG2AssistCharge : if [PL > 0.0 && Ppv + Pw < PL && SoC <= 0.2 && PL - Ppv - Pw > LNG_Pmax + eng3_Pmax + DG1_Pmax && PL - Ppv - Pw + Pd1max / 10.0 <= total_thermal_Pmax];
    ! * -> AllThermalBattery : if [PL > 0.0 && Ppv + Pw < PL && PL - Ppv - Pw > total_thermal_Pmax];
    ! * -> IllegalOverloadCompletion : if [PL < 0.0 && PL >= 0.0];

    [*] -> ZeroLoadCharge;

    state ZeroLoadCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state ZeroLoadSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESCharge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Ppv + Pw - PL;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state RESSpare {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = Ppv + Pw - PL;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state BatteryDischarge {
        enter {
            requested_generator_power = 0.0;
            battery_discharge_power = PL - Ppv - Pw;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 0;
            cut_out_command = 1;
        }
    }

    state LNGChargeMargin {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pgmax / 5.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pgmax / 5.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state LNGNormal {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG3LNG {
        enter {
            requested_generator_power = PL - Ppv - Pw;
            battery_discharge_power = 0.0;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG1AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state DG2AssistCharge {
        enter {
            requested_generator_power = PL - Ppv - Pw + Pd1max / 10.0;
            battery_discharge_power = 0.0;
            battery_charge_power = Pd1max / 10.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state AllThermalBattery {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }

    state IllegalOverloadCompletion {
        enter {
            requested_generator_power = total_thermal_Pmax;
            battery_discharge_power = PL - Ppv - Pw - total_thermal_Pmax;
            battery_charge_power = 0.0;
            spare_power = 0.0;
            cut_in_command = 1;
            cut_out_command = 0;
        }
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `budget_exhausted` |
| failure class | `budget` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SL-10 -> SL-9 -> SL-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SC-11 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `6` / `4` / `6` |
| token / elapsed | `{'prompt_tokens': 477056, 'completion_tokens': 62158, 'total_tokens': 539212, 'n_calls': 18}` / `1566.399s` |
| full stage table | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path2_lng_ems-default-round21compact-92de717a/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path2_lng_ems-default-round21compact-92de717a/pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path2_lng_ems-default-round21compact-92de717a/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path2_lng_ems-default-round21compact-92de717a/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path2_lng_ems-default-round21compact-92de717a/checks.json`, `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path2_lng_ems-default-round21compact-92de717a/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=17622 | 生成初始 DSL 与 grounding seeds | initial len=5541 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=87, advisory=83, info=0; blocking=51, advisory=81, info=0; blocking=0, advisory=81, info=0; blocking=0, advisory=93, info=0; blocking=1, advisory=131, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=199774 | LLM per-request accept/reject + repair | candidate len=5736,6144,6075,5698,5695,0 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=122430 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=87, advisory=83, info=0; blocking=51, advisory=81, info=0; blocking=0, advisory=81, info=0; blocking=0, advisory=93, info=0; blocking=1, advisory=131, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=199774 | LLM per-request accept/reject + repair | candidate len=5736,6144,6075,5698,5695,0 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=122430 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=87, advisory=83, info=0; blocking=51, advisory=81, info=0; blocking=0, advisory=81, info=0; blocking=0, advisory=93, info=0; blocking=1, advisory=131, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=127118 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=127118 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=127118 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ⚠️ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=199774 | LLM per-request accept/reject + repair | candidate len=5736,6144,6075,5698,5695,0 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=122430 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=87, advisory=83, info=0; blocking=51, advisory=81, info=0; blocking=0, advisory=81, info=0; blocking=0, advisory=93, info=0; blocking=1, advisory=131, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=127118 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=5, tokens=127118 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ⚠️ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=False, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-7` | 是 | 3 | ✅ | LLM calls=1, tokens=72268 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=199774 | LLM per-request accept/reject + repair | candidate len=5736,6144,6075,5698,5695,0 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=122430 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=199774 | LLM per-request accept/reject + repair | candidate len=5736,6144,6075,5698,5695,0 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-10` | 是 | 0 | ✅ | LLM calls=5, tokens=122430 | LLM repair review（输入 NL/FixLog/local evidence） | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=87, advisory=83, info=0; blocking=51, advisory=81, info=0; blocking=0, advisory=81, info=0; blocking=0, advisory=93, info=0; blocking=1, advisory=131, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixRequestBatch | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=6, tokens=199774 | LLM per-request accept/reject + repair | candidate len=5736,6144,6075,5698,5695,0 | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ✅ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | SC-11 budget gate blocked SD-2 revalidation: iter+1=5 >= max_iterations=5 | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round21compact-92de717a.agent_loop.json.gz) |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 3 | Iter 4 |
|---|---|---|---|
| `default_init_zero_load_charges_battery` | default-init dispatches to the initial zero-load RES charging mode when PL=0, RES is available, and SoC is below 0.95. | ✅ | ✅ |
| `zero_load_soc_threshold_spare` | explicit-hot-start probes the zero-load SoC boundary: at SoC=0.95 RES production becomes spare power, not battery chargi...<truncated 3 chars> | ✅ | ✅ |
| `res_covers_load_soc_below_threshold` | explicit-hot-start verifies RES covers positive load and charges the battery while SoC is below 0.95. | ✅ | ✅ |
| `res_covers_load_soc_at_threshold_spare` | explicit-hot-start probes the RES-covered SoC boundary: at SoC=0.95 residual renewable power is spare. | ✅ | ✅ |
| `battery_discharge_priority_when_soc_suitable` | explicit-hot-start verifies that when RES is below load and SoC is suitable, the battery supplies the deficit before the...<truncated 11 chars> | ✅ | ✅ |
| `low_soc_lng_charge_margin` | explicit-hot-start verifies the low-SoC LNG-covered branch adds the Pgmax/5 charging margin. | ✅ | ✅ |
| `lng_and_dg_priority_branches` | explicit-hot-start scenarios from thermal modes probe LNG before diesel and DG3 before DG1/DG2 last-priority charging br...<truncated 7 chars> | ✅ | ✅ |
| `dg3_lng_capacity_branch` | explicit-hot-start verifies the next priority branch uses LNG plus engine-3 capacity before DG1/DG2. | ✅ | ✅ |
| `diesel_assist_charge_branches` | explicit-hot-start verifies low-SoC DG1 and DG2 last-priority branches add the Pd1max/10 charging margin. | ✅ | ✅ |
| `dg2_assist_charge_branch` | explicit-hot-start verifies DG2 assist is selected only after LNG, engine-3, and DG1 capacity are insufficient, with Pd1...<truncated 21 chars> | ✅ | ✅ |
| `extreme_demand_uses_all_thermal_and_battery` | explicit-hot-start verifies extreme demand beyond all RES and thermal resources activates all thermal units and covers r...<truncated 35 chars> | ✅ | ✅ |
| `illegal_overload_completion_never_selected` | explicit-hot-start probes the illegal overload-completion corner: even with extreme demand at empty SoC, NL says the ill...<truncated 41 chars> | ❌ | ✅ |
| `forced_reselection_from_zero_load_to_lng_normal` | explicit-hot-start targets the wildcard forced dispatch line: from a zero-load leaf, changed demand with suitable SoC an...<truncated 52 chars> | ✅ | ✅ |
| `forced_reselection_from_thermal_to_res_spare` | explicit-hot-start targets the wildcard forced dispatch line from a different concrete leaf: when RES now covers load an...<truncated 64 chars> | ✅ | ✅ |
| `default_init_forced_selection_to_res_charge` | default-init first dispatches to the initial leaf, then the wildcard forced dispatch guard must re-select RESCharge when...<truncated 55 chars> | ✅ | ✅ |
| `forced_exact_res_cover_boundary_to_res_charge` | explicit-hot-start strengthens the wildcard forced dispatch probe: when Ppv+Pw exactly equals positive PL and SoC is bel...<truncated 52 chars> | ⚪ | ✅ |
| `forced_zero_load_exact_soc_boundary_from_battery` | explicit-hot-start strengthens the wildcard forced dispatch probe: from a battery-discharge leaf, PL=0 with SoC exactly ...<truncated 30 chars> | ⚪ | ✅ |
| `forced_res_spare_exact_cover_and_soc_boundary` | explicit-hot-start targets unreachable-target mutations on the RES coverage and SoC>=0.95 forced guard: exact RES cover ...<truncated 39 chars> | ⚪ | ✅ |
| `forced_all_thermal_from_res_charge_extreme_demand` | explicit-hot-start targets a missing wildcard forced dispatch line from a RES leaf: extreme demand above all thermal res...<truncated 40 chars> | ⚪ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节记录 agent-loop 真实进入 repair block 后的证据链：FixRequestBatch、SL-9 per-request accept/reject、candidate diff、local-check evidence、SL-10(NL+FixLog) 审阅，以及完整 FixLog ledger 摘录。

| Repair | iteration | accepted | source | blocking diagnostics | SL-9 decisions | SL-10 / local checks | candidate hash |
|---:|---:|---:|---|---|---|---|---|
| 1 | `0` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=LNG_Pmax, W_UNWRITTEN_READ_VAR:var_name=DG1_Pmax, W_UNWRITTEN_READ_VAR:var_name=total_thermal_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGNormal, ... +87 | accept=4, reject=8, waiver=8 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=design_target_unresolved; new_blocking_design_diagnostic; missing_required_grounding | `sha256:69829f7850ab3861fd27c07e16b841ea694987f57aaf5930f68e7a8a7f892b2e` |
| 2 | `1` | ✅ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=LNG_Pmax, W_UNWRITTEN_READ_VAR:var_name=DG1_Pmax, W_UNWRITTEN_READ_VAR:var_name=DG2_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGChargeMargin, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.ZeroLoadCharge:to_path=LNGShipEMS.LNGNormal, ... +51 | accept=12, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:3a69e26a9639a55d35ca176ca3f86c259a1ba8364b6eacf68c65c280891258fd` |
| 3 | `2` | ✅ | `SD-6` | illegal_overload_completion_never_selected | accept=1, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=False, drift=major, local_stage=SD-10, reason=missing_required_grounding | `sha256:b9b293c5f1d54546ed6732d6f5f5fe3410841e17490ca551a584eb572de5aa37` |
| 4 | `3` | ❌ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=rework, ok=False, target=False, regression=True, drift=major, rework=Keep the removal of all negative-capacity clamping writes for LNG_Pmax, DG1_Pmax, and DG2_Pmax. Do not reintroduce clamping and do not add meaningless self-assignments to silen...<truncated 314 chars> | `sha256:3708738b7eb83639a2f4da79b0735b2fcc58e757e27910342469683c0aaf3cd2` |
| 5 | `3` | ✅ | `SL-7` | 0, 1 | accept=2, reject=0, waiver=0 | SL-10 decision=pass, ok=True, target=True, regression=False, drift=minor, rework=<none>; local ok=False, target=False, regression=True, drift=major, local_stage=SD-10, reason=new_blocking_design_diagnostic; scenario_regression; missing_required_grounding | `sha256:e81809b0ae1247aa985b29afeaa805e3220ba9027a7d9bfb28607cf1d7a00998` |
| 6 | `4` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=DG2_Pmax, W_UNWRITTEN_READ_VAR, W_UNREFERENCED_VAR, W_GUARD_VARS_NEVER_CHANGE, W_VARIABLE_DECLARED_NEVER_USED, ... +1 | accept=0, reject=1, waiver=1 | <none> | `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 local-check evidence 与 SL-10 审查证据见 `runs/pr_e1_real_agent_loop_round21_compact_context_current_head/pr-e1-path2_lng_ems-default-round21compact-92de717a/report.md` §7。

</details>
