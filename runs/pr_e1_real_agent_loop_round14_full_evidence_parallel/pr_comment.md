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
| token / elapsed | `{'completion_tokens': 6475, 'n_calls': 3, 'prompt_tokens': 28726, 'total_tokens': 35201}` / `162.149s` |
| full stage table | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/checks.json`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=8203 | 生成初始 DSL 与 grounding seeds | initial len=611 | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=17, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=12794 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=14204 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d.agent_loop.json.gz) |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_increase_then_hold_at_upper_boundary` | default-init dispatches to increase and, with slp exactly 0.01, the next cycle takes increase -> hold while checking bot...<truncated 24 chars> | ✅ |
| `increase_no_hold_above_upper_boundary` | explicit-hot-start in increase with slp just above 0.01 should not satisfy increase -> hold and should keep increase out...<truncated 12 chars> | ✅ |
| `hold_to_increase_above_upper_boundary` | explicit-hot-start in hold with slp greater than 0.01 should take hold -> increase and command inlet pressure increase. | ✅ |
| `hold_stays_at_upper_boundary` | explicit-hot-start in hold with slp exactly 0.01 should not take hold -> increase because that guard is strictly greater...<truncated 11 chars> | ✅ |
| `hold_to_decrease_below_lower_boundary` | explicit-hot-start in hold with slp less than -0.01 should take hold -> decrease and command pressure release. | ✅ |
| `hold_stays_at_lower_boundary` | explicit-hot-start in hold with slp exactly -0.01 should not take hold -> decrease because that guard is strictly less t...<truncated 10 chars> | ✅ |
| `decrease_to_hold_at_lower_boundary` | explicit-hot-start in decrease with slp exactly -0.01 should take decrease -> hold because the recovery guard is inclusi...<truncated 3 chars> | ✅ |
| `decrease_stays_below_lower_boundary` | explicit-hot-start in decrease with slp just below -0.01 should not satisfy decrease -> hold and should keep release-pre...<truncated 21 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SD-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2066, 'model': 'gpt-5.5', 'prompt_tokens': 6137, 'total_tokens': 8203}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2407, 'model': 'gpt-5.5', 'prompt_tokens': 10387, 'total_tokens': 12794}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2002, 'model': 'gpt-5.5', 'prompt_tokens': 12202, 'total_tokens': 14204}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/17`，missing=`SD-8, SL-9, SD-10, SL-10B, SC-11`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 SD-10/SL-10B 审查证据见 `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_abs-default-round14fullevidenceparallel-5bb9395d/report.md` §7。

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
| token / elapsed | `{'completion_tokens': 11769, 'n_calls': 3, 'prompt_tokens': 35065, 'total_tokens': 46834}` / `486.406s` |
| full stage table | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/checks.json`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=11802 | 生成初始 DSL 与 grounding seeds | initial len=2012 | [`record`](./pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=14, info=1 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=16755 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=18277 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc.agent_loop.json.gz) |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_enters_manual_with_manual_outputs` | default-init: first cycle should dispatch into Manual, release software control, and use manual switch/default flow sett...<truncated 5 chars> | ✅ |
| `manual_initiate_start_autocontrol_sequence` | explicit-hot-start: caregiver initiates algorithmic control, changes setpoint in Ask_StartAC, presses StartAC into Autoc...<truncated 44 chars> | ✅ |
| `autocontrol_normal_no_fault_stays_normal` | explicit-hot-start: with pump_fault at the no-fault boundary, normal autocontrol should continue computing flow and logg...<truncated 4 chars> | ✅ |
| `autocontrol_fault_enters_pumpfault_alarm` | explicit-hot-start: a pump-operation fault during normal autocontrol should enter PumpFault, activate alarm, and release...<truncated 18 chars> | ✅ |
| `fault_removed_returns_to_manual_and_clears_alarm` | explicit-hot-start: after caregiver removes the pump fault, FaultRemoved should return to Manual and clear fault/alarm i...<truncated 10 chars> | ✅ |
| `ca_backmanual_forces_manual_from_autocontrol_normal` | explicit-hot-start: cross-component CA_backManual fallback from AutocontrolNormal should force Manual as the shared reco...<truncated 12 chars> | ✅ |
| `cb_backmanual_forces_manual_from_pumpfault` | explicit-hot-start: cross-component CB_backManual fallback from PumpFault should force Manual as the shared recovery tar...<truncated 4 chars> | ✅ |
| `cp_backmanual_forces_manual_from_ask_startac` | explicit-hot-start: cross-component CP_backManual fallback from Ask_StartAC should force Manual instead of continuing to...<truncated 17 chars> | ✅ |
| `cc_backmanual_forces_manual_from_autocontrol_init` | explicit-hot-start: cross-component CC_backManual fallback from AutocontrolInit should force Manual before normal autoco...<truncated 17 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SD-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 5608, 'model': 'gpt-5.5', 'prompt_tokens': 6194, 'total_tokens': 11802}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3689, 'model': 'gpt-5.5', 'prompt_tokens': 13066, 'total_tokens': 16755}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2472, 'model': 'gpt-5.5', 'prompt_tokens': 15805, 'total_tokens': 18277}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/17`，missing=`SD-8, SL-9, SD-10, SL-10B, SC-11`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 SD-10/SL-10B 审查证据见 `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_cara-default-round14fullevidenceparallel-da86a4dc/report.md` §7。

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
| token / elapsed | `{'completion_tokens': 7265, 'n_calls': 3, 'prompt_tokens': 26372, 'total_tokens': 33637}` / `399.823s` |
| full stage table | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/checks.json`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=9182 | 生成初始 DSL 与 grounding seeds | initial len=669 | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=0, advisory=1, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SL-5` | 是 | 0 | ✅ | LLM calls=1, tokens=13753 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SD-5A` | 否 | 0 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SC-5F` | 否 | 0 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SD-6` | 否 | 0 | ✅ | ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SL-7` | 是 | 0 | ✅ | LLM calls=1, tokens=10702 | LLM model review | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SC-12` | 否 | - | ✅ | full_pass_all_required_feedback_ok | 写 final verdict | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f.agent_loop.json.gz) |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 1 |
|---|---|---|
| `default_init_to_floor1_stopped` | default-init verifies the initial transition dispatches to floor F1 with stopped hbrg output, then an empty cycle does n...<truncated 25 chars> | ✅ |
| `f1_request_f2_then_continue_to_f3` | default-init covers F1 PS2 upward motion to MU2, S2 arrival at F2, immediate PS3 check to continue upward to MU3, and S3...<truncated 15 chars> | ✅ |
| `f1_direct_request_f3` | default-init verifies PS3 from F1 targets direct upward motion MU3, then S3 stops at F3. | ✅ |
| `f3_request_f2_then_continue_to_f1` | explicit-hot-start at F3 covers PS2 downward motion to MD2, S2 arrival at F2, immediate PS1 check to continue downward t...<truncated 28 chars> | ✅ |
| `f3_direct_request_f1` | explicit-hot-start at F3 verifies PS1 targets direct downward motion MD1 and S1 stops at F1. | ✅ |
| `reset_forces_floor1_from_up_motion` | explicit-hot-start from upward motion MU3 verifies Reset forces floor F1 and stopped hbrg regardless of outstanding upwa...<truncated 19 chars> | ✅ |
| `reset_forces_floor1_from_down_motion` | explicit-hot-start from downward motion MD2 verifies Reset forces floor F1 and stopped hbrg regardless of outstanding do...<truncated 23 chars> | ✅ |
| `reset_forces_floor1_from_floor_state` | explicit-hot-start from floor state F2 verifies Reset forces floor F1 and stopped hbrg even when already stopped at a no...<truncated 11 chars> | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

- 本 run 未进入 `SD-8/SL-9/SD-10` repair block；通常表示流程在 repair 前已成功、被 provider/schema 错误中断，或在 pre-repair 阶段直接退出。

### 8. 尝试记录与成本

- `SL-1`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 3000, 'model': 'gpt-5.5', 'prompt_tokens': 6182, 'total_tokens': 9182}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-5`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 2561, 'model': 'gpt-5.5', 'prompt_tokens': 11192, 'total_tokens': 13753}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。
- `SL-7`：retry_count=`0`，schema_ok=`True`，usage=`{'completion_tokens': 1704, 'model': 'gpt-5.5', 'prompt_tokens': 8998, 'total_tokens': 10702}`，attempts=`1`。
  - attempt 0: error_kind=`None`，model=`gpt-5.5`。

### 9. 最终停止状态与后续含义

- 停止状态：verdict=`success`，record_status=`success`。
- 主要原因分类：`success`。
- required stages executed：`12/17`，missing=`SD-8, SL-9, SD-10, SL-10B, SC-11`。
- repairs：`0/0` accepted；scenario_history=`1`。
- 配置含义：`recommended baseline candidate`；该结果可用于评估默认入口本身。
- 样本含义：若出现 `design_or_variable_dynamics`，应重点审查变量是否仅作为 guard/input 常量而没有事件/动作更新；若出现 pre-scenario parse/semantic 失败，则应先优化 pyfcstm grammar adherence。

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 SD-10/SL-10B 审查证据见 `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path1_elevator-default-round14fullevidenceparallel-0ebf931f/report.md` §7。

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
| token / elapsed | `{'completion_tokens': 47560, 'n_calls': 10, 'prompt_tokens': 586211, 'total_tokens': 633771}` / `2242.674s` |
| full stage table | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/report.md` §4 |
| run record | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz` |
| logs | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/run_logs/stdout.txt`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/run_logs/stderr.txt` |
| checks / repro | `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/checks.json`, `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/reproducibility.json` |

#### 全流程摘要表（report §4 摘录）

| Stage | 是否 LLM | iteration | 结果 | 获取的信息 / 反馈 | 本阶段做了什么 | DSL 修改 | artifact/log |
|---|---:|---:|---:|---|---|---|---|
| `SC-0` | 否 | - | ✅ | trace/control | 初始化 run state | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-1` | 是 | - | ✅ | LLM calls=1, tokens=15194 | 生成初始 DSL 与 grounding seeds | initial len=6902 | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=54, advisory=135, info=0; blocking=54, advisory=135, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixPlan | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=431547 | LLM repair candidate | candidate len=7059,6902,6873,7339,7041 | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-10` | 否 | 0 | ⚠️ | ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=maj | 本地 repair review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ⚠️ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ⚠️ | blocking=54, advisory=135, info=0; blocking=54, advisory=135, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixPlan | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=431547 | LLM repair candidate | candidate len=7059,6902,6873,7339,7041 | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-10` | 否 | 0 | ⚠️ | ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=maj | 本地 repair review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ⚠️ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=54, advisory=135, info=0; blocking=54, advisory=135, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-5` | 是 | 2 | ✅ | LLM calls=1, tokens=22396 | 生成模型测试 scenario | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=3, tokens=164634 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixPlan | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=431547 | LLM repair candidate | candidate len=7059,6902,6873,7339,7041 | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-10` | 否 | 0 | ⚠️ | ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=maj | 本地 repair review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ⚠️ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=54, advisory=135, info=0; blocking=54, advisory=135, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=3, tokens=164634 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixPlan | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=431547 | LLM repair candidate | candidate len=7059,6902,6873,7339,7041 | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-10` | 否 | 0 | ⚠️ | ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=maj | 本地 repair review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ⚠️ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-2` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 解析 pyfcstm DSL | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-3` | 否 | 0 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | AST→state-machine semantic check | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-4` | 否 | 0 | ✅ | blocking=54, advisory=135, info=0; blocking=54, advisory=135, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0; blocking=0, advisory=189, info=0 | 设计健康与变量/guard 检查 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-5A` | 否 | 2 | ✅ | trace/control | 检查 scenario coverage | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-5F` | 否 | 2 | ✅ | trace/control | 冻结 scenario oracle | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-6` | 否 | 2 | ✅ | ok=True, diag=0; ok=True, diag=0; ok=True, diag=0 | 执行 scenario simulation | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-7` | 是 | 2 | ✅ | LLM calls=3, tokens=164634 | LLM model review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-8` | 否 | 0 | ✅ | trace/control | 生成 FixPlan | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SL-9` | 是 | 0 | ✅ | LLM calls=5, tokens=431547 | LLM repair candidate | candidate len=7059,6902,6873,7339,7041 | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SD-10` | 否 | 0 | ⚠️ | ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=major; ok=False, target_resolved=False, drift=maj | 本地 repair review | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-11` | 否 | 0 | ⚠️ | trace/control | 接受/拒绝候选 | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-12` | 否 | - | ⚠️ | new_blocking_design_diagnostic; scenario_regression; forced_transition_count_drift; missing_required_grounding | 写 final verdict | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |
| `SC-13` | 否 | - | ✅ | trace/control | 写审计 run record | 无/见 record | [`record`](./pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0.agent_loop.json.gz) |

#### Scenario 逐轮通过矩阵（report §6.1 摘录）

口径：`✅` = 该 scenario 在该轮 SD-6 simulation 通过；`❌` = 该轮失败；`⚪` = 该轮未执行或无该 scenario 结果。

| Scenario | Intent | Iter 3 | Iter 4 | Iter 5 |
|---|---|---|---|---|
| `default_init_then_zero_load_charge` | default-init probe: first cycle must dispatch to IdleNoLoad, then zero load with RES and SoC below 0.95 must transition ...<truncated 20 chars> | ✅ | ✅ | ✅ |
| `forced_idle_no_load_no_res` | explicit-hot-start probe: from a non-idle operating state, PL=0 with no RES must force IdleNoLoad with all dispatch outp...<truncated 8 chars> | ✅ | ✅ | ✅ |
| `zero_load_spare_soc_boundary` | explicit-hot-start probe: with PL=0 and RES present, SoC exactly 0.95 should route renewable power to spare, not chargin...<truncated 2 chars> | ✅ | ✅ | ✅ |
| `res_covers_charge_below_soc_boundary` | explicit-hot-start probe: when RES covers positive load and SoC is just below 0.95, residual RES must charge the battery...<truncated 1 chars> | ✅ | ✅ | ✅ |
| `res_covers_spare_at_soc_boundary` | explicit-hot-start probe: when RES covers positive load and SoC is exactly 0.95, residual RES must become spare power. | ✅ | ✅ | ✅ |
| `battery_assist_low_deficit_soc_boundary` | explicit-hot-start probe: with RES below load, SoC exactly 0.2 and deficit within battery power, battery assist should c...<truncated 17 chars> | ✅ | ✅ | ✅ |
| `lng_low_soc_charge_margin` | explicit-hot-start probe: low SoC with LNG-capable deficit should include the Pgmax/5 charging margin. | ✅ | ✅ | ✅ |
| `lng_normal_after_battery_limit` | explicit-hot-start probe: normal SoC with deficit above battery limit but within LNG capacity should request LNG only. | ✅ | ✅ | ✅ |
| `lng_and_engine3_capacity_boundary` | explicit-hot-start probe: deficit above LNG capacity but within LNG plus engine3 should cut in LNG and engine3 only. | ✅ | ✅ | ✅ |
| `dg1_low_soc_charge_margin` | explicit-hot-start probe: low SoC diesel-generator branch should add the Pd1max/10 charging margin and cut in DG1. | ✅ | ✅ | ✅ |
| `dg1_normal_and_dg2_last_priority` | explicit-hot-start probe: normal DG1 branch should cover an intermediate deficit, then a separate high deficit hot-start...<truncated 44 chars> | ✅ | ✅ | ✅ |
| `dg2_and_overload_extreme_cases` | explicit-hot-start probe: DG2 should cover demand beyond DG1 capacity, while extreme demand beyond all thermal resources...<truncated 49 chars> | ✅ | ✅ | ✅ |

#### Repair / blocking feedback 概览（report §7 摘录）

口径：本节只记录 agent-loop 真实进入 repair block 后已有证据；`diff` 基于 run record 中可恢复的 before/candidate DSL 文本生成，若 before DSL 未落盘则明确标注不可恢复。

| Repair | iteration | accepted | source | blocking diagnostics | SD-10 / SL-10B | candidate hash |
|---:|---:|---:|---|---|---|---|
| 1 | `0` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, ... +53 | SD-10 ok=False, target=False, regression=False, drift=major, reason=missing_required_grounding | `sha256:93caebf626f3e191c1aa3fa4e47d5767b9697dcd6806f3c540cd8eba6fa27c91` |
| 2 | `1` | ❌ | `SD-4` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, ... +53 | SD-10 ok=False, target=False, regression=False, drift=major, reason=missing_required_grounding | `sha256:180df4cf113445e8e8ed80c4a7699aec96a916a393847d1d19d37639fb3a5a13` |
| 3 | `2` | ❌ | `SL-7` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, ... +49 | SD-10 ok=False, target=False, regression=True, drift=major, reason=scenario_regression; missing_required_grounding | `sha256:302f510d4d02007c3eb00a902b754fdc37e3d30fe9e1d7e6711f423fe90c9f63` |
| 4 | `3` | ❌ | `SL-7` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, ... +49 | SD-10 ok=False, target=False, regression=False, drift=major, reason=missing_required_grounding | `sha256:fe8c613b70a699a7b91fc62e878399f1ffd7cd8e9882a089319e4c8115ce959f` |
| 5 | `4` | ❌ | `SL-7` | W_UNWRITTEN_READ_VAR:var_name=Pd2max, W_UNWRITTEN_READ_VAR:var_name=Pbat_Pmax, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.BatteryAssist, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.LNGCoveredNormal, W_GUARD_VARS_NEVER_CHANGE:from_path=LNGShipEMS.IdleNoLoad:to_path=LNGShipEMS.DG2Covered, ... +49 | SD-10 ok=False, target=False, regression=True, drift=major, reason=new_blocking_design_diagnostic; scenario_regression; forced_transition_count_drift; missing_required_grounding | `sha256:372f20d03a9f02ee8ffc77cc2d117143e9863993c6619dc4a7cecf3d4bd1110d` |

> 完整 repair 细节、进入修复原因、SD-8 修改建议、SL-9 candidate、before→candidate diff 与 SD-10/SL-10B 审查证据见 `runs/pr_e1_real_agent_loop_round14_full_evidence_parallel/pr-e1-path2_lng_ems-default-round14fullevidenceparallel-a78258a0/report.md` §7。

</details>
