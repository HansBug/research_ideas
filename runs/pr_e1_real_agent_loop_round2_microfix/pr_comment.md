## PR-E1 real-run evidence update

身份：主 session / PR-E1 runner。

本 comment 汇总当前已产出的真实 `method.loop.run_agent_loop` 运行证据；详细报告见仓库内 `runs/pr_e1_real_agent_loop_round2_microfix/`。

| Path | case | config | verdict | status | clean | eligible | failure class | tokens | report |
|---|---|---|---|---|---:|---:|---|---:|---|
| path1 | `path1_abs` | `default` | `not_converged` | `rejected` | ✅ | ❌ | `grounding_or_required_element_loss` | 51671 | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_abs-default-round2microfix-386e71ad/report.md` |
| path1 | `path1_cara` | `default` | `not_converged` | `rejected` | ✅ | ❌ | `grounding_or_required_element_loss` | 31023 | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_cara-default-round2microfix-68290344/report.md` |
| path1 | `path1_elevator` | `default` | `not_converged` | `rejected` | ✅ | ❌ | `grounding_or_required_element_loss` | 61426 | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_elevator-default-round2microfix-b39fe7e0/report.md` |
| path2 | `path2_lng_ems` | `default` | `not_converged` | `rejected` | ✅ | ❌ | `model_quality_or_unclassified` | 27695 | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path2_lng_ems-default-round2microfix-1613a6e9/report.md` |

### 可复现性边界

- clean commit 绑定：4/4 run 的 `reproducibility.json` 记录 dirty=false。
- prompt snapshot hash 种类：1；用于确认同一轮 4 例是否共享同一 prompt/context 版本。
- 每个 run 的 `reproducibility.json` 保存 git commit、dirty flag、diff hash、prompt file hash、runner command/config 与 source/paper path。

### 初步观察

- `default`：0/4 success，rejected=4，budget_exhausted=0，total_tokens=171815。
- Q1/max_iterations：当前证据未产生 success；若 run 早停于 `rejected`，瓶颈更可能是 prompt/repair candidate quality 或样本变量语义，而不是单纯迭代预算。
- 主结果候选：当前 0/4 run 可进入 main_result_eligible；其余只能作为 exploratory / infrastructure evidence。

### 主要失败模式

- `grounding_or_required_element_loss`：3 run(s)。
- `model_quality_or_unclassified`：1 run(s)。
- `grounding_or_required_element_loss` 表示 repair 虽可能通过局部语法/语义检查，但丢失 NL-grounded required elements；这类结果不能因更高预算而算作改善。

### 样本筛选观察

- 样本覆盖：4 个 case，Path1=3，Path2=1。
- `path1_abs`：失败/成功类别=grounding_or_required_element_loss，最大 observed iteration_count=1。
- `path1_cara`：失败/成功类别=grounding_or_required_element_loss，最大 observed iteration_count=1。
- `path1_elevator`：失败/成功类别=grounding_or_required_element_loss，最大 observed iteration_count=1。
- `path2_lng_ems`：失败/成功类别=model_quality_or_unclassified，最大 observed iteration_count=1。
- 实证筛选更新：repair 能通过局部语法/语义但丢失 required grounded elements 的样本，应标为高风险，不应因为预算增大而视为质量提升。

### 4 例详细输入 / 输出 / artifact

<details><summary>path1 / path1_abs / default / not_converged</summary>

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
def int k1 = 0;
def int k2 = 0;
def int n = 0;
def float slp = 0.0;

state ABS_Supervisor {
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
| verdict / status | `not_converged` / `rejected` |
| failure class | `grounding_or_required_element_loss` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `1` / `0` / `3` |
| token / elapsed | `{'prompt_tokens': 47238, 'completion_tokens': 4433, 'total_tokens': 51671, 'n_calls': 5}` / `230.315s` |
| full stage table | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_abs-default-round2microfix-386e71ad/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_abs-default-round2microfix-386e71ad/pr-e1-path1_abs-default-round2microfix-386e71ad.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_abs-default-round2microfix-386e71ad/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_abs-default-round2microfix-386e71ad/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_abs-default-round2microfix-386e71ad/checks.json`, `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_abs-default-round2microfix-386e71ad/reproducibility.json` |

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
def int target_bp = 0;

def int complication_flag = 0;

state CARA {
    [*] -> Mode_Control_Algorithm;

    state Mode_Control_Algorithm {
        ! * -> Manual :: CA_backManual;
        ! * -> Manual :: CB_backManual;
        ! * -> Manual :: CP_backManual;
        ! * -> Manual :: CC_backManual;

        [*] -> Manual;

        state Manual;

        state Ask_StartAC;

        state AutocontrolInit;

        state Autocontrol;

        Manual -> Ask_StartAC :: InitiateAlgorithmicControl;
        Ask_StartAC -> AutocontrolInit :: StartAC;
        AutocontrolInit -> Autocontrol :: InitComplete;
        Autocontrol -> Manual :: TerminateAlgorithmicControl;
        Autocontrol -> Manual :: PumpFault;
    }
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `rejected` |
| failure class | `grounding_or_required_element_loss` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `1` / `0` / `1` |
| token / elapsed | `{'prompt_tokens': 28820, 'completion_tokens': 2203, 'total_tokens': 31023, 'n_calls': 3}` / `464.119s` |
| full stage table | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_cara-default-round2microfix-68290344/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_cara-default-round2microfix-68290344/pr-e1-path1_cara-default-round2microfix-68290344.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_cara-default-round2microfix-68290344/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_cara-default-round2microfix-68290344/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_cara-default-round2microfix-68290344/checks.json`, `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_cara-default-round2microfix-68290344/reproducibility.json` |

</details>

<details><summary>path1 / path1_elevator / default / not_converged</summary>

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
state ElevatorController {
    ! * -> F1 :: Reset;

    [*] -> F1;

    state F1;
    state F2;
    state F3;
    state MU2;
    state MU3;
    state MD1;
    state MD2;

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
| verdict / status | `not_converged` / `rejected` |
| failure class | `grounding_or_required_element_loss` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SL-5 -> SD-5A -> SC-5F -> SD-6 -> SD-8 -> SL-9 -> SD-10 -> SC-11 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `1` / `0` / `3` |
| token / elapsed | `{'prompt_tokens': 56386, 'completion_tokens': 5040, 'total_tokens': 61426, 'n_calls': 5}` / `264.761s` |
| full stage table | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_elevator-default-round2microfix-b39fe7e0/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_elevator-default-round2microfix-b39fe7e0/pr-e1-path1_elevator-default-round2microfix-b39fe7e0.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_elevator-default-round2microfix-b39fe7e0/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_elevator-default-round2microfix-b39fe7e0/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_elevator-default-round2microfix-b39fe7e0/checks.json`, `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path1_elevator-default-round2microfix-b39fe7e0/reproducibility.json` |

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
def float requested_generator_power = 0.0;
def float battery_power = 0.0;
def float spare_power = 0.0;

state LNGShipEMS {
    [*] -> RESCharge;

    state RESCharge {
        during {
            requested_generator_power = 0.0;
        }
    }

    state RESSpare;
    state RESBatterySupport;
    state LNGCover;
    state LNGCoverLowSoC;
    state DG1Assist;
    state DG1AssistLowSoC;
    state DG2Assist;
    state DG2AssistLowSoC;
    state ThermalBatterySupport;
    state ZeroLoadCharge;
    state ZeroLoadSpare;

    RESCharge -> RESSpare : if [Ppv + Pw >= PL && SoC >= 0.95];
    RESSpare -> RESCharge : if [Ppv + Pw >= PL && SoC < 0.95];

    RESCharge -> ZeroLoadCharge : if [PL == 0.0 && SoC < 0.95];
    RESSpare -> ZeroLoadSpare : if [PL == 0.0 && SoC >= 0.95];

    ZeroLoadCharge -> RESCharge : if [PL > 0.0];
    ZeroLoadSpare -> RESSpare : if [PL > 0.0];

    RESCharge -> RESBatterySupport : if [Ppv + Pw < PL && SoC > 0.0];
    RESSpare -> RESBatterySupport : if [Ppv + Pw < PL && SoC > 0.0];

    RESBatterySupport -> LNGCover : if [Ppv + Pw < PL && SoC >= 0.20];
    LNGCover -> LNGCoverLowSoC : if [SoC < 0.20];

    LNGCover -> DG1Assist : if [PL > Ppv + Pw + eng3_Pmax];
    DG1Assist -> DG1AssistLowSoC : if [SoC < 0.20];

    DG1Assist -> DG2Assist : if [PL > Ppv + Pw + eng3_Pmax + Pd1max];
    DG2Assist -> DG2AssistLowSoC : if [SoC < 0.20];

    DG2Assist -> ThermalBatterySupport : if [PL > Ppv + Pw + eng3_Pmax + Pd1max + Pgmax];

    LNGCoverLowSoC -> LNGCover : if [SoC >= 0.20];
    DG1AssistLowSoC -> DG1Assist : if [SoC >= 0.20];
    DG2AssistLowSoC -> DG2Assist : if [SoC >= 0.20];

    ThermalBatterySupport -> RESCharge : if [Ppv + Pw >= PL && SoC < 0.95];
    ThermalBatterySupport -> RESSpare : if [Ppv + Pw >= PL && SoC >= 0.95];
}
```

#### agent-loop 过程与日志路径

| 项 | 值 |
|---|---|
| verdict / status | `not_converged` / `rejected` |
| failure class | `model_quality_or_unclassified` |
| executed stages | `SC-0 -> SL-1 -> SD-2 -> SD-3 -> SD-4 -> SD-8 -> SL-9 -> SD-10 -> SL-10B -> SC-11 -> SC-12 -> SC-13` |
| iter / repairs / accepted / scenarios | `1` / `1` / `0` / `0` |
| token / elapsed | `{'prompt_tokens': 24768, 'completion_tokens': 2927, 'total_tokens': 27695, 'n_calls': 3}` / `433.811s` |
| full stage table | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path2_lng_ems-default-round2microfix-1613a6e9/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path2_lng_ems-default-round2microfix-1613a6e9/pr-e1-path2_lng_ems-default-round2microfix-1613a6e9.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path2_lng_ems-default-round2microfix-1613a6e9/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path2_lng_ems-default-round2microfix-1613a6e9/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path2_lng_ems-default-round2microfix-1613a6e9/checks.json`, `runs/pr_e1_real_agent_loop_round2_microfix/pr-e1-path2_lng_ems-default-round2microfix-1613a6e9/reproducibility.json` |

</details>
