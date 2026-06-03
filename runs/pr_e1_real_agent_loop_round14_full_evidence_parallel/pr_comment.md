## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/`。

| Path | case | config | verdict | status | clean | eligible | failure class | tokens | report |
|---|---|---|---|---|---:|---:|---|---:|---|
| path1 | `path1_abs` | `default` | `success` | `success` | ✅ | ✅ | `success` | 35201 | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/report.md` |
| path1 | `path1_cara` | `default` | `success` | `success` | ✅ | ✅ | `success` | 46834 | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/report.md` |
| path1 | `path1_elevator` | `default` | `success` | `success` | ✅ | ✅ | `success` | 33637 | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/report.md` |
| path2 | `path2_lng_ems` | `default` | `not_converged` | `rejected` | ✅ | ❌ | `semantic_or_topology` | 633771 | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/report.md` |

### 可复现性边界

- clean commit 绑定：4/4 run 的 `reproducibility.json` 记录 dirty=false。
- prompt snapshot hash 种类：1；用于确认同一轮 4 例是否共享同一 prompt/context 版本。
- 每个 run 的 `reproducibility.json` 保存 git commit、dirty flag、diff hash、prompt file hash、runner command/config 与 source/paper path。

### 初步观察

- `default`：3/4 success，rejected=1，budget_exhausted=0，total_tokens=749443。
- 主结果候选：当前 3/4 run 可进入 main_result_eligible；其余只能作为 exploratory / infrastructure evidence。

### 主要失败模式

- `success`：3 run(s)。
- `semantic_or_topology`：1 run(s)。
- parse/semantic/topology 类问题说明 pyfcstm grammar 与层次路径约束仍需更强 prompt 约束或 repair context。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=success，最大 observed iteration_count=1。
- `path1_elevator`：失败/成功类别=success，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=semantic_or_topology，最大 observed iteration_count=5。

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

state System {
    [*] -> increase;

    state increase {
        during {
            k1 = 1;
            k2 = 0;
            n = 0;
        }
    }

    state hold {
        during {
            k1 = 0;
            k2 = 0;
            n = 0;
        }
    }

    state decrease {
        during {
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
| token / elapsed | `{'prompt_tokens': 28726, 'completion_tokens': 6475, 'total_tokens': 35201, 'n_calls': 3}` / `162.149s` |
| full stage table | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/checks.json`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/reproducibility.json` |

</details>

<details><summary>path1 / path1_cara / default / success</summary>

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
def int software_control = 0;
def int pump_alarm = 0;
def int pump_fault = 0;
def int log_count = 0;
def float target_bp = 0.0;
def float requested_target_bp = 0.0;
def float bp_buffer = 0.0;
def float patient_bp = 0.0;
def float flow_rate = 0.0;
def float default_flow_rate = 0.0;
def float manual_switch_speed = 0.0;
def float pump_speed = 0.0;
def float control_voltage = 0.0;

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
            }
            during {
                pump_speed = manual_switch_speed;
                flow_rate = default_flow_rate;
            }
        }

        state Ask_StartAC {
            during {
                target_bp = requested_target_bp;
            }
        }

        state AutocontrolInit {
            enter {
                CA_mode = 1;
                software_control = 1;
            }
        }

        state AutocontrolNormal {
            during {
                patient_bp = bp_buffer;
                flow_rate = target_bp - patient_bp;
                control_voltage = flow_rate;
                pump_speed = control_voltage;
                log_count = log_count + 1;
            }
        }

        state PumpFault {
            enter {
                pump_alarm = 1;
                software_control = 0;
                CA_mode = 0;
            }
        }

        Manual -> Ask_StartAC :: InitiateAC;
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> AutocontrolNormal;
        AutocontrolNormal -> PumpFault : if [pump_fault > 0];
        PumpFault -> Manual :: FaultRemoved effect {
            pump_fault = 0;
            pump_alarm = 0;
        };
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `success` / `success` |
| failure class | `success` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `0` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 35065, 'completion_tokens': 11769, 'total_tokens': 46834, 'n_calls': 3}` / `486.406s` |
| full stage table | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/checks.json`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/reproducibility.json` |

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
| token / elapsed | `{'prompt_tokens': 26372, 'completion_tokens': 7265, 'total_tokens': 33637, 'n_calls': 3}` / `399.823s` |
| full stage table | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/checks.json`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/reproducibility.json` |

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
def float Pd2max = 0.0;
def float Pbat_Pmax = 0.0;
def float Pgen_req = 0.0;
def float Pbat_discharge = 0.0;
def float Pbat_charge = 0.0;
def float Pspare = 0.0;
def int cut_in_LNG = 0;
def int cut_in_engine3 = 0;
def int cut_in_DG1 = 0;
def int cut_in_DG2 = 0;
def int cut_in_battery = 0;
def int cut_out_load = 0;

state LNGShipEMS {
    ! * -> IdleNoLoad : if [PL == 0 && Ppv + Pw == 0];
    ! * -> ZeroLoadCharge : if [PL == 0 && Ppv + Pw > 0 && SoC < 0.95];
    ! * -> ZeroLoadSpare : if [PL == 0 && Ppv + Pw > 0 && SoC >= 0.95];
    ! * -> RESCoversCharge : if [PL > 0 && Ppv + Pw >= PL && SoC < 0.95];
    ! * -> RESCoversSpare : if [PL > 0 && Ppv + Pw >= PL && SoC >= 0.95];
    ! * -> BatteryAssist : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw <= Pbat_Pmax];
    ! * -> LNGCoveredLowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGCoveredNormal : if [PL > 0 && Ppv + Pw < PL && SoC >= 0.2 && PL - Ppv - Pw > Pbat_Pmax && PL - Ppv - Pw <= Pgmax];
    ! * -> LNGAndEngine3Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax];
    ! * -> DG1LowSoCChargeMargin : if [PL > 0 && Ppv + Pw < PL && SoC < 0.2 && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw + Pd1max / 10 <= Pgmax + eng3_Pmax + Pd1max];
    ! * -> DG1CoveredNormal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max && (SoC >= 0.2 || PL - Ppv - Pw + Pd1max / 10 > Pgmax + eng3_Pmax + Pd1max)];
    ! * -> DG2Covered : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max && PL - Ppv - Pw <= Pgmax + eng3_Pmax + Pd1max + Pd2max];
    ! * -> OverloadCompletionIllegal : if [PL > 0 && Ppv + Pw < PL && PL - Ppv - Pw > Pgmax + eng3_Pmax + Pd1max + Pd2max];

    [*] -> IdleNoLoad;

    state IdleNoLoad {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state ZeroLoadCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state ZeroLoadSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state RESCoversCharge {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = Ppv + Pw - PL;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state RESCoversSpare {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = Ppv + Pw - PL;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state BatteryAssist {
        enter {
            Pgen_req = 0.0;
            Pbat_discharge = PL - Ppv - Pw;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 0;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredLowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pgmax / 5;
            Pbat_discharge = 0.0;
            Pbat_charge = Pgmax / 5;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state LNGCoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 0;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state LNGAndEngine3Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 0;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG1LowSoCChargeMargin {
        enter {
            Pgen_req = PL - Ppv - Pw + Pd1max / 10;
            Pbat_discharge = 0.0;
            Pbat_charge = Pd1max / 10;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 1;
            cut_out_load = 0;
        }
    }

    state DG1CoveredNormal {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 0;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state DG2Covered {
        enter {
            Pgen_req = PL - Ppv - Pw;
            Pbat_discharge = 0.0;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 0;
            cut_out_load = 0;
        }
    }

    state OverloadCompletionIllegal {
        enter {
            Pgen_req = Pgmax + eng3_Pmax + Pd1max + Pd2max;
            Pbat_discharge = PL - Ppv - Pw - Pgmax - eng3_Pmax - Pd1max - Pd2max;
            Pbat_charge = 0.0;
            Pspare = 0.0;
            cut_in_LNG = 1;
            cut_in_engine3 = 1;
            cut_in_DG1 = 1;
            cut_in_DG2 = 1;
            cut_in_battery = 1;
            cut_out_load = 1;
        }
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `rejected` |
| failure class | `semantic_or_topology` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SD-2 -> SD-3 -> SD-4 -> SD-5A -> SC-5F -> SD-6 -> SL-7 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `5` / `5` / `0` / `3` |
| token / elapsed | `{'prompt_tokens': 586211, 'completion_tokens': 47560, 'total_tokens': 633771, 'n_calls': 10}` / `2242.674s` |
| full stage table | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/checks.json`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/reproducibility.json` |

</details>
