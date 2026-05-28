# Path 1 候选样本选样报告（codex 自动评审）
> **产出位置**：`project_1_llm_state_machine_modeling/paper_v1/selection/SELECTION_REPORT.md`
> **数据来源**：`sources/` T0+🟢 子集 × codex (gpt-5.5) `--sandbox read-only` 全文阅读评分
> **scoring rubric**：H 层次 / G 守卫算术 / A 动作非平凡 / F 故障恢复，每维 0-3，对应 baseline 自报 F1 最低的 3 个组件 (actions=0.34 / guards=0.42 / hierarchical=~0.5)

## 评分图例

| 分数 | Emoji | 含义 |
|:-:|:-:|---|
| 0 | ⚪ | 缺失 / 无信号 |
| 1 | 🟡 | 浅 / 表面提及 |
| 2 | 🟢 | 明确存在 |
| 3 | 💎 | 强 / 定义性特征 |

Verdict：🟢 candidate / 🟡 backup / ❌ exclude；excl：❌ 命中硬排除（parallel / history / IO-only / too_thin）

**领域 emoji 图例**（与 [`sources/SUMMARY.md`](../../sources/SUMMARY.md) 一致）：

🚗 汽车与道路车辆 / 🚆 轨道交通 / ✈️ 航空航天 / 🩺 医疗设备 / 🏭 工业自动化 / 🏢 楼宇机电 / 🌡️ 过程与环境 / 🚦 道路交通信号 / 🅿️ 智慧停车 / ⚙️ 通用控制 / 🧩 建模工程 / 🔐 安全分析

**关注特性 tag 图例**（基于评分 + trap + primitive 派生）：

| tag | 含义 | 触发条件 |
|---|---|---|
| 层次💎 | hierarchy 强 | H==3 |
| 算术guard💎 | 多变量算术 guard | G==3 |
| 丰富动作💎 | 非平凡 action | A==3 |
| 故障恢复💎 | 显式故障恢复 | F==3 |
| 全局应急🌐 | 跨状态全局 escape | T6 trap=True |
| 复合内行为🧱 | 复合状态自身行为 | T5 trap=True |
| forced/aspect🔁 | pyfcstm C3 强 | C3 strength=2 |
| 深复合DFS🌀 | pyfcstm C1 强 | C1 strength=2 |

## 总览统计

- 已评审 sample 总数：**323**（T0+🟢 候选池 = 323）
- 通过硬排除 + base≥4 的合格样本：**305**
- 最终选定候选 (Top-15)：**15**
- 备选 (Backup-15)：**15**
- 排除 / 不合格：**18**

### STM 类型分布

| STM 类型 | 评审样本数 | 候选池 (15) | 目标 |
|---|---:|---:|---|
| HSM | 71 | 7 | 5-6 |
| EFSM | 172 | 5 | 4-5 |
| FSM | 68 | 3 | 2-3 |
| Other | 0 + 3 + 9 | 0 | ≤1 |

### 维度命中分布

| 维度 | ⚪ 0 | 🟡 1 | 🟢 2 | 💎 3 |
|---|---:|---:|---:|---:|
| H | 164 | 72 | 30 | 57 |
| G | 10 | 19 | 92 | 202 |
| A | 0 | 1 | 123 | 199 |
| F | 124 | 56 | 82 | 61 |

### bd / ft 分布（重设计 prompt 后）

| 维度 | ⚪ 0 | 🟡 1 | 🟢 2 | 💎 3 |
|---|---:|---:|---:|---:|
| bd | 38 | 127 | 69 | 89 |
| ft | 24 | 88 | 105 | 106 |

### bd 命中 trap 频率（来自 baseline 自报 failure 模式）

| Trap | 命中样本数 | 占比 |
|---|---:|---:|
| T1_cross_section_element | 253 | 78.3% |
| T2_implicit_domain_term | 166 | 51.4% |
| T3_implicit_action_from_prose | 239 | 74.0% |
| T4_multivar_arith_guard | 232 | 71.8% |
| T5_composite_internal_behavior | 36 | 11.1% |
| T6_global_cross_cutting_recovery | 78 | 24.1% |

（统计基数：含 trap_signals 字段的样本 = 323）

### ft pyfcstm primitive 优势强度分布

| Primitive | ⚪ 0 (none) | 🟡 1 (weak) | 🟢 2 (strong) |
|---|---:|---:|---:|
| C1_speculative_dfs | 246 | 70 | 7 |
| C2_expr_ir_smt | 80 | 126 | 117 |
| C3_forced_and_aspect | 150 | 32 | 141 |
| C4_abstract_action | 150 | 155 | 18 |

（统计基数：含 primitive_advantage 字段的样本 = 323）

## 候选池 — Top 15（推荐主用）

> 列说明：🌐 领域 / 系统简述 (来自 STM.md `控制对象`) / 关注特性 (基于 H/G/A/F + trap + primitive 派生的高信号 emoji 标签)

| # | 🌐 | sample_id | type | 系统简述 | 关注特性 | H | G | A | F | final | bd/ft | V | excl |
|---:|:-:|---|---|---|---|:-:|:-:|:-:|:-:|---:|:-:|:-:|:-:|
| 1 | ⚙️ | `amazing-race-robot-edition__01` | HSM | 室内寻人问路与寻门任务监督器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 2 | ✈️ | `autonomous-firefighting-inside-buildings-unmanned-aerial-vehicle__01` | HSM | 室内灭火无人机室外-室内任务监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 / 深复合DFS🌀 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 3 | ⚙️ | `autonomous-navigation-framework-holonomic-mobile-robots-agriculture__01` | HSM | 温室全向移动机器人的高层导航与巡检监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 4 | 🌡️ | `control-system-design-of-water-filter-test-bench__01` | HSM | 水滤测试台的主状态、阀门与泵监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 5 | 🏭 | `fault-handling-plc-industry4__02` | HSM | 包装机械模块在故障后的恢复控制过程 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 6 | ⚙️ | `finite-state-automaton-control-system-walking-machines__01` | HSM |  walking machine / hexapod 高层导航与步态监督控… | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 7 | 🩺 | `cara-infusion-pump-formal-spec__01` | EFSM | CARA 输液泵控制系统中的泵控制方式 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 8 | 🅿️ | `lift-control-automatic-car-parking-using-plc__01` | EFSM |  PLC 多层停车升降机定位与存取控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 9 | 🏭 | `plc-scada-liquid-filling-automation-ejosat__01` | EFSM | PLC/SCADA 液体灌装产线中的配方驱动灌装、封盖与贴标控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 10 | 🚆 | `railway-generic-electronic-interlocking-software-engineering-methods__01` | EFSM | 电子铁路联锁软件中 Route 3 的设路、呼叫、占用与故障安全控制链 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 11 | ✈️ | `reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation__01` | EFSM | Masat-1 CubeSat 飞控软件中的任务/故障管理逻辑 | 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 🟢 2 | 💎 3 | 💎 3 | **11.0** | 3/3 | 🟢 | · |
| 12 | ⚙️ | `finite-state-machine-accommodating-unexpected-large-ground-height-variations-bipedal-robot-walking__01` | FSM |  `MABEL` 双足机器人未知台阶/绊倒应对监督控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 13 | 🌡️ | `optimization-control-energy-management-system-microgrids__01` | FSM | 并网微电网 EMS 模式切换控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.3** | 2/2 | 🟢 | · |
| 14 | ✈️ | `automated-contingency-management-in-unmanned-aircraft-systems__01` | FSM | 无人机自动应急管理安全监视器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | 💎 3 | **10.9** | 3/3 | 🟢 | · |
| 15 | 🚗 | `full-automated-drive-urban-environments-gomentum-station__01` | HSM | 城市场景自动驾驶高层行为监督器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |

### 候选 #1: ⚙️ `amazing-race-robot-edition__01`

- **领域**：⚙️　|　**STM 类型**：HSM
- **控制对象**：通用机器人与移动服务机器人领域的室内寻人问路与寻门任务监督器
- **关注特性**：层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁
- **评分**：H=💎3 G=💎3 A=💎3 F=💎3，final=**12.9**，bd=3，ft=3
- **pitch**：This is a strong stress test because a high-level robot supervisor combines explicit hierarchy, compound guards, nontrivial actions, and cross-cutting failure recovery.
- **rationale**：The sample is fundamentally hierarchical, with two composite behavior states nested under a five-state supervisor. It also contains guard-heavy navigation and dialogue logic, meaningful variable updates and I/O actions, and repeated fallback-to-WANDER recovery paths. The background SLAM and navigation processes are supporting context rather than required parallel state regions, so no hard exclusion applies.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/amazing-race-robot-edition/STM.md`](../../sources/amazing-race-robot-edition/STM.md)

### 候选 #2: ✈️ `autonomous-firefighting-inside-buildings-unmanned-aerial-vehicle__01`

- **领域**：✈️　|　**STM 类型**：HSM
- **控制对象**：航空航天与飞行/空管控制领域的室内灭火无人机室外-室内任务监督控制器
- **关注特性**：层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 / 深复合DFS🌀
- **评分**：H=💎3 G=💎3 A=💎3 F=💎3，final=**12.9**，bd=3，ft=3
- **pitch**：This is a high-value stress test because it combines deep mission hierarchy, compound guarded recovery, rich UAV actions, and a global abort-to-landing rule.
- **rationale**：The sample is fundamentally a hierarchical UAV mission supervisor, not just a perception pipeline. Its behavior requires modeling nested phases, estimator-mode switches, retry loops, local escape from failed flythrough, fire-loss recovery, and any-state abort landing. These are exactly the kinds of actions, guards, hierarchy, and cross-cutting recovery patterns that weak Umple-style baselines are likely to drop or flatten.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/autonomous-firefighting-inside-buildings-unmanned-aerial-vehicle/STM.md`](../../sources/autonomous-firefighting-inside-buildings-unmanned-aerial-vehicle/STM.md)

### 候选 #3: ⚙️ `autonomous-navigation-framework-holonomic-mobile-robots-agriculture__01`

- **领域**：⚙️　|　**STM 类型**：HSM
- **控制对象**：温室全向移动机器人的高层导航与巡检监督控制器
- **关注特性**：层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁
- **评分**：H=💎3 G=💎3 A=💎3 F=💎3，final=**12.9**，bd=3，ft=3
- **pitch**：A hierarchical greenhouse navigation supervisor with arithmetic alignment guards, nontrivial navigation actions, and global failure recovery stresses exactly the guard/action/hierarchy weaknesses of U
- **rationale**：This sample is a strong stress test because the paper gives an explicit hierarchical FSM and then spreads the operational semantics across navigation, alignment, and rail-traversal sections. The controller includes multi-variable numeric guards for rail alignment, concrete action outputs through planners and velocity commands, and a global recovery path from any failure. These features directly target prior baseline weaknesses in hierarchy, guards, actions, and cross-cutting recovery.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/autonomous-navigation-framework-holonomic-mobile-robots-agriculture/STM.md`](../../sources/autonomous-navigation-framework-holonomic-mobile-robots-agriculture/STM.md)

### 候选 #4: 🌡️ `control-system-design-of-water-filter-test-bench__01`

- **领域**：🌡️　|　**STM 类型**：HSM
- **控制对象**：水滤测试台的主状态、阀门与泵监督控制器
- **关注特性**：层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁
- **评分**：H=💎3 G=💎3 A=💎3 F=💎3，final=**12.9**，bd=3，ft=3
- **pitch**：A strong industrial HSM stress test with nested operating modes, multi-variable guards, heavy transition actions, and global stop/recovery behavior spread across supervisor, valve, pump, and safety se
- **rationale**：This sample directly targets the weakest baseline areas: guarded transitions, actions, hierarchy, and fault recovery are all central rather than incidental. The paper gives enough concrete control detail to build a reference state machine, but the information is distributed across main-state, valve, pump, and inner-stop sections, which is exactly where single-prompt or syntax-repair baselines are likely to lose semantics.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/control-system-design-of-water-filter-test-bench/STM.md`](../../sources/control-system-design-of-water-filter-test-bench/STM.md)

### 候选 #5: 🏭 `fault-handling-plc-industry4__02`

- **领域**：🏭　|　**STM 类型**：HSM
- **控制对象**：包装机械模块在故障后的恢复控制过程
- **关注特性**：层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁
- **评分**：H=💎3 G=💎3 A=💎3 F=💎3，final=**12.9**，bd=3，ft=3
- **pitch**：A hierarchical PackML-style fault recovery path with boolean restart guards, centralized error reactions, and group-level shutdown is a strong stress test for guard, action, and cross-cutting recovery
- **rationale**：This sample directly targets baseline-weak elements: hierarchical module/mode structure, guarded restart eligibility, non-trivial error-management actions, and fault recovery. The paper gives enough concrete behavior to construct a reference state machine, while still distributing key semantics across prose and architectural descriptions. Cross-cutting group shutdown and centralized error reaction make it especially difficult for flat event-driven baselines.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/fault-handling-plc-industry4/STM.md`](../../sources/fault-handling-plc-industry4/STM.md)

### 候选 #6: ⚙️ `finite-state-automaton-control-system-walking-machines__01`

- **领域**：⚙️　|　**STM 类型**：HSM
- **控制对象**：通用控制领域的 walking machine / hexapod 高层导航与步态监督控制器
- **关注特性**：层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁
- **评分**：H=💎3 G=💎3 A=💎3 F=💎3，final=**12.9**，bd=3，ft=3
- **pitch**：A layered walking-machine supervisor stresses hierarchy, guard attribution, action placement, and cross-layer fault exits in one concrete robotic control case.
- **rationale**：The paper gives enough concrete structure to build a reference HSM: named global/local/gait states, guard predicates, action sections, and fault endpoints are all specified. It is a strong baseline trap because key action and guard facts are distributed across state descriptions, state-activity prose, implementation details, and simulation traces. No hard exclusion is triggered because the benchmarkable target is the hierarchical supervisor, with FSM execution serialized by a scheduler rather than requiring orthogonal statechart regions.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/finite-state-automaton-control-system-walking-machines/STM.md`](../../sources/finite-state-automaton-control-system-walking-machines/STM.md)

### 候选 #7: 🩺 `cara-infusion-pump-formal-spec__01`

- **领域**：🩺　|　**STM 类型**：EFSM
- **控制对象**：CARA 输液泵控制系统中的泵控制方式
- **关注特性**：算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁
- **评分**：H=🟢2 G=💎3 A=💎3 F=💎3，final=**11.9**，bd=3，ft=3
- **pitch**：This is a compact but high-value stress test because mode hierarchy, multi-source manual fallback, fault-triggered alarm/control-release actions, and cross-cutting back-to-manual logic are scattered a
- **rationale**：The sample has a real EFSM mode controller with manual/autocontrol operational semantics, a shallow hierarchical submode, and a composed backManual guard over four modules. Its strongest stress-test value is the global recovery pattern: pump complications and any backManual request force control back to Manual while also involving alarms and release of CARA control. The information is distributed across overview, EFSM architecture, and Hermes model sections, making it a strong baseline-trap case rather than a single-table extraction.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/cara-infusion-pump-formal-spec/STM.md`](../../sources/cara-infusion-pump-formal-spec/STM.md)

### 候选 #8: 🅿️ `lift-control-automatic-car-parking-using-plc__01`

- **领域**：🅿️　|　**STM 类型**：EFSM
- **控制对象**：智慧停车领域的 PLC 多层停车升降机定位与存取控制器
- **关注特性**：算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁
- **评分**：H=🟢2 G=💎3 A=💎3 F=💎3，final=**11.9**，bd=3，ft=3
- **pitch**：This lift controller is a strong stress test because arithmetic level guards, mode-local actions, cross-section action attribution, and global emergency behavior all interact in one compact PLC case.
- **rationale**：The paper provides enough concrete operational detail to build an EFSM: manual and auto modes, level-difference direction logic, sensor-gated slow/stop behavior, VFD outputs, and confirmation/error branches. It directly targets baseline-weak regions because guards and actions are split across prose, figures, wiring, simulation, and conclusion sections. The global alarm-to-emergency rule and parent-mode lamp/speed behavior make it especially difficult for flat Umple-style extraction.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/lift-control-automatic-car-parking-using-plc/STM.md`](../../sources/lift-control-automatic-car-parking-using-plc/STM.md)

### 候选 #9: 🏭 `plc-scada-liquid-filling-automation-ejosat__01`

- **领域**：🏭　|　**STM 类型**：EFSM
- **控制对象**：PLC/SCADA 液体灌装产线中的配方驱动灌装、封盖与贴标控制器
- **关注特性**：算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁
- **评分**：H=🟢2 G=💎3 A=💎3 F=💎3，final=**11.9**，bd=3，ft=3
- **pitch**：This is a strong industrial EFSM stress test because recipe-driven guards, closed-loop sensor guards, multi-actuator actions, composite capping steps, and cross-cutting recovery are scattered across t
- **rationale**：The paper defines more than wiring: it gives HMI parameter guards, loadcell and encoder feedback, a five-step capping sub-sequence, labeling branches, and several alarm/restart/recovery paths. It directly targets known baseline weaknesses because guards and actions must be reconstructed from distributed industrial prose, not copied from a formal statechart. The main caveat is that the hierarchy is process decomposition rather than a fully formal nested state-machine notation.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/plc-scada-liquid-filling-automation-ejosat/STM.md`](../../sources/plc-scada-liquid-filling-automation-ejosat/STM.md)

### 候选 #10: 🚆 `railway-generic-electronic-interlocking-software-engineering-methods__01`

- **领域**：🚆　|　**STM 类型**：EFSM
- **控制对象**：电子铁路联锁软件中 Route 3 的设路、呼叫、占用与故障安全控制链
- **关注特性**：算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁
- **评分**：H=🟢2 G=💎3 A=💎3 F=💎3，final=**11.9**，bd=3，ft=3
- **pitch**：Route 3 is a strong stress test because it combines multi-element Boolean interlocking guards, staged actuator/state updates, and cross-cutting fail-safe cancellation across multiple operating phases.
- **rationale**：The sample has meaningful hierarchy through route-request sub-functions, strong multi-variable guards, non-trivial transition actions, and explicit fail-safe behavior. Its information is distributed across prose, tables, statechart sections, and test results, which creates documented baseline traps for guard/action attribution. The global safety-critical rule also maps naturally to forced transitions, giving pyfcstm a clear uniqueness advantage over flatter Umple or PlantUML encodings.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/railway-generic-electronic-interlocking-software-engineering-methods/STM.md`](../../sources/railway-generic-electronic-interlocking-software-engineering-methods/STM.md)

### 候选 #11: ✈️ `reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation__01`

- **领域**：✈️　|　**STM 类型**：EFSM
- **控制对象**：Masat-1 CubeSat 飞控软件中的任务/故障管理逻辑
- **关注特性**：丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁
- **评分**：H=🟢2 G=🟢2 A=💎3 F=💎3，final=**11.0**，bd=3，ft=3
- **pitch**：This is a strong spacecraft-mode stress test because the modeler must recover mode guards, rich per-mode actions, and a global hierarchical FDIR safe-mode escape from prose spread across CONOPS and im
- **rationale**：The STM extraction is consistent with the paper's CONOPS and application-layer architecture: Masat-1 is explicitly governed by a finite-state operational-mode controller with battery, sun-visibility, task-completion, telecommand, and anomaly-triggered transitions. Its strongest stress-test value is in action attribution and global recovery: each mode has concrete operational side effects, while hierarchical FDIR routes major anomalies to SAFE. The hierarchy is not a fully nested statechart, but the INIT pseudo-state sequence and FDIR layers add enough structure to stress baselines beyond a fla
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation/STM.md`](../../sources/reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation/STM.md)

### 候选 #12: ⚙️ `finite-state-machine-accommodating-unexpected-large-ground-height-variations-bipedal-robot-walking__01`

- **领域**：⚙️　|　**STM 类型**：FSM
- **控制对象**：通用控制与机器人任务领域的 `MABEL` 双足机器人未知台阶/绊倒应对监督控制器
- **关注特性**：算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁
- **评分**：H=🟢2 G=💎3 A=💎3 F=💎3，final=**11.9**，bd=3，ft=3
- **pitch**：A hard stress-test because the paper mixes a terrain-mode FSM, a nested tripping-reflex sub-FSM, arithmetic sensor guards, controller-switching actions, and cross-cutting recovery transitions.
- **rationale**：The sample is not a thin I/O description: the paper defines concrete FSM modes, sensor-derived transition guards, and controller actions for MABEL walking over unknown terrain. It directly stresses known weak baseline areas because guards are arithmetic and multi-variable, actions are distributed across control-design prose, and the tripping-reflex recovery path is both nested and cross-cutting.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/finite-state-machine-accommodating-unexpected-large-ground-height-variations-bipedal-robot-walking/STM.md`](../../sources/finite-state-machine-accommodating-unexpected-large-ground-height-variations-bipedal-robot-walking/STM.md)

### 候选 #13: 🌡️ `optimization-control-energy-management-system-microgrids__01`

- **领域**：🌡️　|　**STM 类型**：FSM
- **控制对象**：过程与环境控制领域的并网微电网 EMS 模式切换控制器
- **关注特性**：算术guard💎 / 丰富动作💎 / 故障恢复💎 / 复合内行为🧱 / forced/aspect🔁
- **评分**：H=🟢2 G=💎3 A=💎3 F=💎3，final=**11.3**，bd=2，ft=2
- **pitch**：A compact microgrid EMS supervisor stresses baselines with grouped operating modes, multi-variable synchronization guards, concrete actuator actions, and several fault-recovery paths.
- **rationale**：This is a strong stress-test because the paper gives a real FSM with five operating modes over encoded switch/breaker/grid states, while the important actions and recovery behavior are spread across controller and simulation sections. Guards are not merely event labels: synchronization depends on magnitude, frequency, phase, and thresholded waveform error, while outage and reclosure depend on combinations of power and switch status. The sample directly targets known weak spots in guards, actions, and hierarchical/grouped state recovery without triggering any hard exclusion.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/optimization-control-energy-management-system-microgrids/STM.md`](../../sources/optimization-control-energy-management-system-microgrids/STM.md)

### 候选 #14: ✈️ `automated-contingency-management-in-unmanned-aircraft-systems__01`

- **领域**：✈️　|　**STM 类型**：FSM
- **控制对象**：航空航天与飞行/空管控制领域的无人机自动应急管理安全监视器
- **关注特性**：算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁
- **评分**：H=🟡1 G=💎3 A=💎3 F=💎3，final=**10.9**，bd=3，ft=3
- **pitch**：A flat but safety-critical UAS monitor with global emergency escape, split prose-to-action semantics, and guarded policy logic makes a strong stress test for guard/action recall and cross-cutting tran
- **rationale**：The core Safety Monitor is not hierarchical beyond semantic grouping, but it has strong fault-handling structure: abnormal-state recovery, final unrecoverable emergency state, and a global emergency escape. The paper spreads the operational actions across architecture, formal model, implementation, and simulation sections, which is exactly the kind of context fragmentation that weak Umple-style baselines tend to lose. Its pyfcstm fit is high because forced cross-cutting transitions and structured guard expressions directly reduce encoding duplication and semantic drift.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/automated-contingency-management-in-unmanned-aircraft-systems/STM.md`](../../sources/automated-contingency-management-in-unmanned-aircraft-systems/STM.md)

### 候选 #15: 🚗 `full-automated-drive-urban-environments-gomentum-station__01`

- **领域**：🚗　|　**STM 类型**：HSM
- **控制对象**：汽车与道路车辆控制领域的城市场景自动驾驶高层行为监督器
- **关注特性**：层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁
- **评分**：H=💎3 G=💎3 A=💎3 F=💎3，final=**12.9**，bd=3，ft=3
- **pitch**：A strong stress-test case because the AD supervisor combines explicit hierarchy, event-disjunction guards, arithmetic TTC logic, distributed STOP behavior, and global error escape paths.
- **rationale**：The paper gives a real HSM with composite communication sub-states, nontrivial event and arithmetic guards, and rich inter-module actions rather than a flat toy FSM. STOP behavior is intentionally split across the state-machine, behavior-planning, and scenario sections, creating several documented baseline traps. Its global ERROR/disengagement path and heartbeat-based recovery make it especially useful for testing whether a method can encode cross-cutting safety behavior.
- **STM.md**：[`project_1_llm_state_machine_modeling/sources/full-automated-drive-urban-environments-gomentum-station/STM.md`](../../sources/full-automated-drive-urban-environments-gomentum-station/STM.md)

## 备选池 — Backup 15

| # | 🌐 | sample_id | type | 系统简述 | 关注特性 | H | G | A | F | final | bd/ft | V | excl |
|---:|:-:|---|---|---|---|:-:|:-:|:-:|:-:|---:|:-:|:-:|:-:|
| 1 | ✈️ | `long-duration-fully-autonomous-operation-of-rotorcraft-uas-for-remote-sensing-data-acquisition__01` | HSM | 长时自主旋翼无人机的数据采集与回充任务控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 2 | ✈️ | `methodology-to-develop-a-discrete-event-supervisory-controller-for-an-autonomous-helicopter-flight__01` | HSM | Bell 412 直升机自主飞行监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 3 | 🚗 | `odin-team-victortango-darpa-urban-challenge__01` | HSM | 城市自动驾驶分层 driving behaviors 控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 4 | ✈️ | `onboard-mission-management-vtol-uav-sequence-supervisory-control__01` | HSM | VTOL 无人机的机载任务执行与监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 5 | ✈️ | `robust-accurate-drone-landing-moving-targets__01` | HSM | 移动目标无人机视觉滑降监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 6 | 🏭 | `safety4-dynamic-fsm-multilayer-operation-modes__01` | HSM | 人机协作机床上下料单元安全 operation-mode 监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 7 | 🅿️ | `scale-model-parking-garage-integrating-automation-in-parking-facilities__01` | HSM | 环形车库自动/手动分层控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 8 | ✈️ | `sequence-supervisory-control-onboard-uav-mission-management__01` | HSM |  `Mission Mode / Command Mode` 无人直升机任… | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 9 | ⚙️ | `autonomous-robotic-manipulation-exploratory-interactions__01` | HSM | 自主机器人材料探索与舀取操作的任务监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **12.1** | 3/3 | 🟢 | · |
| 10 | 🏢 | `mechatronic-control-system-finite-state-machine__01` | HSM | 自动滑门运动与阻塞恢复控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **12.1** | 3/3 | 🟢 | · |
| 11 | 🏭 | `prefabricated-board-transfer-palletizer-s7-1500-plc__01` | HSM | 预制板转运码垛机模式与顺序控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **12.1** | 3/3 | 🟢 | · |
| 12 | ⚙️ | `state-machine-based-hybrid-position-force-control-waste-mobile-robot__01` | HSM | 垃圾分拣移动机器人 5DOF 机械臂的任务监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **12.1** | 3/3 | 🟢 | · |
| 13 | 🌡️ | `virtual-commissioning-wick-soilless-cultivations__01` | HSM | 营养液制备模块分层监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 / 深复合DFS🌀 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **12.1** | 3/3 | 🟢 | · |
| 14 | ✈️ | `autonomous-uav-multimodal-mapping-underground-mines__01` | HSM | 地下矿井测绘无人机的任务监督控制器 | 层次💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 🟢 2 | 💎 3 | 💎 3 | **12.0** | 3/3 | 🟢 | · |
| 15 | ✈️ | `hybrid-autonomy-future-mars-science-helicopter__01` | HSM | 火星科学直升机任务自治监督器 | 层次💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 🟢 2 | 💎 3 | 💎 3 | **12.0** | 3/3 | 🟢 | · |

## 全量评审表（按 final 降序，含被排除样本）

| # | 🌐 | sample_id | type | 系统简述 | 关注特性 | H | G | A | F | final | bd/ft | V | excl |
|---:|:-:|---|---|---|---|:-:|:-:|:-:|:-:|---:|:-:|:-:|:-:|
| 1 | ⚙️ | `amazing-race-robot-edition__01` | HSM | 室内寻人问路与寻门任务监督器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 2 | ✈️ | `autonomous-firefighting-inside-buildings-unmanned-aerial-vehicle__01` | HSM | 室内灭火无人机室外-室内任务监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 / 深复合DFS🌀 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 3 | ⚙️ | `autonomous-navigation-framework-holonomic-mobile-robots-agriculture__01` | HSM | 温室全向移动机器人的高层导航与巡检监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 4 | 🌡️ | `control-system-design-of-water-filter-test-bench__01` | HSM | 水滤测试台的主状态、阀门与泵监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 5 | 🏭 | `fault-handling-plc-industry4__02` | HSM | 包装机械模块在故障后的恢复控制过程 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 6 | ⚙️ | `finite-state-automaton-control-system-walking-machines__01` | HSM |  walking machine / hexapod 高层导航与步态监督控… | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 7 | 🚗 | `full-automated-drive-urban-environments-gomentum-station__01` | HSM | 城市场景自动驾驶高层行为监督器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 8 | ✈️ | `long-duration-fully-autonomous-operation-of-rotorcraft-uas-for-remote-sensing-data-acquisition__01` | HSM | 长时自主旋翼无人机的数据采集与回充任务控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 9 | ✈️ | `methodology-to-develop-a-discrete-event-supervisory-controller-for-an-autonomous-helicopter-flight__01` | HSM | Bell 412 直升机自主飞行监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 10 | 🚗 | `odin-team-victortango-darpa-urban-challenge__01` | HSM | 城市自动驾驶分层 driving behaviors 控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 11 | ✈️ | `onboard-mission-management-vtol-uav-sequence-supervisory-control__01` | HSM | VTOL 无人机的机载任务执行与监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 12 | ✈️ | `robust-accurate-drone-landing-moving-targets__01` | HSM | 移动目标无人机视觉滑降监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 13 | 🏭 | `safety4-dynamic-fsm-multilayer-operation-modes__01` | HSM | 人机协作机床上下料单元安全 operation-mode 监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 14 | 🅿️ | `scale-model-parking-garage-integrating-automation-in-parking-facilities__01` | HSM | 环形车库自动/手动分层控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 15 | ✈️ | `sequence-supervisory-control-onboard-uav-mission-management__01` | HSM |  `Mission Mode / Command Mode` 无人直升机任… | 层次💎 / 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 💎 3 | **12.9** | 3/3 | 🟢 | · |
| 16 | ⚙️ | `autonomous-robotic-manipulation-exploratory-interactions__01` | HSM | 自主机器人材料探索与舀取操作的任务监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **12.1** | 3/3 | 🟢 | · |
| 17 | 🏢 | `mechatronic-control-system-finite-state-machine__01` | HSM | 自动滑门运动与阻塞恢复控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **12.1** | 3/3 | 🟢 | · |
| 18 | 🏭 | `prefabricated-board-transfer-palletizer-s7-1500-plc__01` | HSM | 预制板转运码垛机模式与顺序控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **12.1** | 3/3 | 🟢 | · |
| 19 | ⚙️ | `state-machine-based-hybrid-position-force-control-waste-mobile-robot__01` | HSM | 垃圾分拣移动机器人 5DOF 机械臂的任务监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **12.1** | 3/3 | 🟢 | · |
| 20 | 🌡️ | `virtual-commissioning-wick-soilless-cultivations__01` | HSM | 营养液制备模块分层监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 / 深复合DFS🌀 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **12.1** | 3/3 | 🟢 | · |
| 21 | ✈️ | `autonomous-uav-multimodal-mapping-underground-mines__01` | HSM | 地下矿井测绘无人机的任务监督控制器 | 层次💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 🟢 2 | 💎 3 | 💎 3 | **12.0** | 3/3 | 🟢 | · |
| 22 | ✈️ | `hybrid-autonomy-future-mars-science-helicopter__01` | HSM | 火星科学直升机任务自治监督器 | 层次💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 🟢 2 | 💎 3 | 💎 3 | **12.0** | 3/3 | 🟢 | · |
| 23 | ⚙️ | `pirate-precision-imaging-real-time-autonomous-tracker-explorer__01` | HSM | 任务监督控制器 | 层次💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 🟢 2 | 💎 3 | 💎 3 | **12.0** | 3/3 | 🟢 | · |
| 24 | ⚙️ | `self-evolution-mobile-robot-high-voltage-transmission-line__01` | HSM | 高压输电线路多任务维护行为监督器 | 层次💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 🟢 2 | 💎 3 | 💎 3 | **12.0** | 3/3 | ❌ | ❌ |
| 25 | 🚗 | `a-hierarchical-control-system-for-autonomous-driving-towards-urban-challenges__01` | HSM | 城市道路自动驾驶车辆的高层决策控制器 | 层次💎 / 算术guard💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 🟢 2 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 26 | 🅿️ | `a-novel-approach-of-lift-control-in-automatic-car-parking-using-plc__01` | HSM | 立体车库升降机控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 27 | 🅿️ | `autonomous-parking-system-urban-mobility__01` | HSM | 自动驾驶泊车全流程监督控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 28 | 🩺 | `cara-infusion-pump-formal-spec__01` | EFSM | CARA 输液泵控制系统中的泵控制方式 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 29 | ⚙️ | `finite-state-machine-accommodating-unexpected-large-ground-height-variations-bipedal-robot-walking__01` | FSM |  `MABEL` 双足机器人未知台阶/绊倒应对监督控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 30 | 🚗 | `junior-stanford-entry-urban-challenge__01` | HSM | 城市自动驾驶高层行为监督器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 31 | 🅿️ | `lift-control-automatic-car-parking-using-plc__01` | EFSM |  PLC 多层停车升降机定位与存取控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 32 | 🏭 | `plc-course-fsm__02` | HSM | PLC 子过程外层的 auto/standby 控制 | 层次💎 / 算术guard💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 💎 3 | 🟢 2 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 33 | 🏭 | `plc-scada-liquid-filling-automation-ejosat__01` | EFSM | PLC/SCADA 液体灌装产线中的配方驱动灌装、封盖与贴标控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 34 | 🏢 | `priority-rank-elevator-control-plc__01` | HSM | 四级权限电梯调度监督器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 35 | 🚆 | `railway-generic-electronic-interlocking-software-engineering-methods__01` | EFSM | 电子铁路联锁软件中 Route 3 的设路、呼叫、占用与故障安全控制链 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 36 | 🏢 | `secure-automated-elevator-management-pressure-sensor-floor-estimation__01` | HSM | 面向室内移动机器人的自动电梯管理与乘梯恢复控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | 🟢 | · |
| 37 | 🚆 | `some-experiences-on-formal-specification-of-railway-interlocking-systems-using-statecharts__01` | Resource | 铁路联锁系统 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.9** | 3/3 | ❌ | ❌ |
| 38 | ⚙️ | `pallet-manipulation-hierarchical-state-machine-experiment__01` | HSM | 托盘搬运移动机器人分层监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **11.8** | 2/3 | 🟢 | · |
| 39 | 🌡️ | `power-dispatching-fsm-standalone-photovoltaic-hybrid-energy-storage__01` | HSM | 独立光伏混合储能系统的分层功率调度控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **11.8** | 2/3 | 🟢 | · |
| 40 | ⚙️ | `communication-within-multi-fsm-based-robotic-systems__01` | HSM | 乒乓球收集移动机器人控制子系统 | 层次💎 / 算术guard💎 / 丰富动作💎 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **11.5** | 2/2 | 🟢 | · |
| 41 | ⚙️ | `pm-fsm-robust-quadrupedal-locomotion__01` | HSM | 四足机器人在平地、扰动和上下楼场景下的接触感知步态与反射控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **11.5** | 1/3 | 🟢 | · |
| 42 | ✈️ | `autonomous-autopilot-control-system-small-scale-uavs__01` | HSM | 小型无人机 flight management system 与 auto… | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 / 深复合DFS🌀 | 💎 3 | 💎 3 | 💎 3 | 🟡 1 | **11.3** | 3/3 | 🟢 | · |
| 43 | 🏭 | `autonomous-mobile-manipulation-wall-building-mbzirc-2020__01` | HSM | 砖块抓取、运输与放置移动操作监督器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 / 深复合DFS🌀 | 💎 3 | 💎 3 | 💎 3 | 🟡 1 | **11.3** | 3/3 | 🟢 | · |
| 44 | 🌡️ | `control-strategies-low-voltage-dc-microgrids__01` | HSM | 低压直流微电网接口变换器协调控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟡 1 | **11.3** | 3/3 | 🟢 | · |
| 45 | 🌡️ | `optimization-control-energy-management-system-microgrids__01` | FSM | 并网微电网 EMS 模式切换控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 💎 3 | **11.3** | 2/2 | 🟢 | · |
| 46 | ⚙️ | `robot-soccer-strategy-hfsm-centralized-architectures__01` | HSM | 机器人足球战术-角色分层协调器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟡 1 | **11.3** | 3/3 | 🟢 | · |
| 47 | ✈️ | `beatle-self-reconfigurable-aerial-robot__01` | HSM | BEATLE 空中模块化机器人在飞行中执行对接/分离的重构运动规划器 | 层次💎 / 算术guard💎 / 丰富动作💎 | 💎 3 | 💎 3 | 💎 3 | 🟢 2 | **11.2** | 1/2 | 🟢 | · |
| 48 | ✈️ | `software-architecture-autonomous-uav-mission-management-control__01` | HSM | 自主 UAV 的任务规划与动作执行监督器 | 层次💎 / 丰富动作💎 / 全局应急🌐 / forced/aspect🔁 / 深复合DFS🌀 | 💎 3 | 🟢 2 | 💎 3 | 🟢 2 | **11.2** | 3/3 | 🟢 | · |
| 49 | ⚙️ | `brain-machine-interface-humanoid-motion__01` | HSM | 人形机器人全身接触转换监督控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | 🟡 1 | **11.0** | 2/3 | 🟢 | · |
| 50 | ⚙️ | `hirosco-high-level-robotic-spacecraft-controller__01` | HSM | 航天器子系统生命周期与错误恢复监督器 | 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 🟢 2 | 💎 3 | 💎 3 | **11.0** | 3/3 | 🟢 | · |
| 51 | ✈️ | `mode-confusion-analysis-of-a-flight-guidance-system-using-formal-methods__01` | HSM | 飞机飞行引导系统（FGS）模式逻辑 | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 / 深复合DFS🌀 | 💎 3 | 💎 3 | 💎 3 | 🟡 1 | **11.0** | 2/3 | ❌ | ❌ |
| 52 | ✈️ | `reusable-and-reliable-flight-control-software-for-a-fail-safe-and-cost-efficient-cubesat-mission-design-and-implementation__01` | EFSM | Masat-1 CubeSat 飞控软件中的任务/故障管理逻辑 | 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 🟢 2 | 💎 3 | 💎 3 | **11.0** | 3/3 | 🟢 | · |
| 53 | ✈️ | `automated-contingency-management-in-unmanned-aircraft-systems__01` | FSM | 无人机自动应急管理安全监视器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | 💎 3 | **10.9** | 3/3 | 🟢 | · |
| 54 | 🌡️ | `design-development-and-testing-of-flexible-combined-heat-and-power-fchp-system__01` | EFSM |  F-CHP 能源系统中央控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | 💎 3 | **10.9** | 3/3 | 🟢 | · |
| 55 | 🅿️ | `five-parking-lifting-stereo-garage-s7-200__01` | EFSM | 两层五车位升降横移立体车库存取控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | 💎 3 | **10.9** | 3/3 | 🟢 | · |
| 56 | ✈️ | `safe-mission-manager-unmanned-aircraft-systems__01` | EFSM |  soft/hard contingency 安全任务监督器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | 💎 3 | **10.9** | 3/3 | 🟢 | · |
| 57 | 🏭 | `sensor-guided-assembly-segmented-structures-industrial-robots__01` | FSM | 分段复合板装配流程监督控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | 💎 3 | **10.9** | 3/3 | ❌ | ❌ |
| 58 | 🌡️ | `smart-charging-architecture-power-quality-distribution__01` | EFSM | 电动汽车 Smart Charger 充电功率监督控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | 💎 3 | **10.9** | 3/3 | 🟢 | · |
| 59 | ⚙️ | `development-of-360-degrees-autonomus-and-manual-fire-fighting-robot__01` | HSM | 自主/手动探火、避障与灭火监督控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 🟢 2 | **10.8** | 2/3 | 🟢 | · |
| 60 | 🏭 | `fault-handling-plc-industry4__01` | HSM | PLC 机器部件的标准化 operation modes | 层次💎 / 算术guard💎 / forced/aspect🔁 | 💎 3 | 💎 3 | 🟢 2 | 🟢 2 | **10.8** | 2/3 | 🟢 | · |
| 61 | 🚗 | `intelligent-decision-making-vehicle-emergency-fsm__01` | HSM | 紧急工况自动驾驶行为决策控制器 | 层次💎 / 算术guard💎 | 💎 3 | 💎 3 | 🟢 2 | 🟢 2 | **10.8** | 2/3 | 🟢 | · |
| 62 | 🌡️ | `microgrid-power-flow-control-integrated-battery-management__01` | EFSM | 孤网微电网功率流与电池管理监督控制器 | 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 🟢 2 | **10.8** | 3/2 | 🟢 | · |
| 63 | ⚙️ | `safety-critical-autonomous-inspection-distillation-columns__01` | FSM | 在蒸馏塔多层托盘环境中执行自主巡检的四足机器人任务监督控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 🟢 2 | **10.8** | 2/3 | 🟢 | · |
| 64 | ⚙️ | `terrestrial-unmanned-roving-vertical-take-off-and-landing-turvtol__01` | HSM | TURVTOL 多模态自主载具的任务监督控制器 | 层次💎 / 算术guard💎 / forced/aspect🔁 | 💎 3 | 💎 3 | 🟢 2 | 🟢 2 | **10.8** | 2/3 | 🟢 | · |
| 65 | 🌡️ | `water-distribution-control-system-using-plc__01` | EFSM | 多水库配水系统的液位、阀门和泵组监督控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 🟢 2 | **10.8** | 2/3 | 🟢 | · |
| 66 | ⚙️ | `autonomous-control-miniaturized-mobile-robots-unknown-pipe-networks__01` | EFSM |  Joey 微型管网巡检机器人自主探索控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | 💎 3 | **10.6** | 3/2 | 🟢 | · |
| 67 | 🌡️ | `enhanced-intelligent-energy-management-ac-microgrid__01` | HSM |  AC 微电网混合储能能量管理监督器 | 层次💎 / 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | ⚪ 0 | **10.5** | 3/3 | 🟢 | · |
| 68 | 🚗 | `intelligent-decision-making-vehicles-emergency-conditions-apf-fsm__01` | HSM | 紧急工况自动驾驶行为决策控制器 | 层次💎 / 算术guard💎 | 💎 3 | 💎 3 | 🟢 2 | 🟢 2 | **10.5** | 1/3 | 🟢 | · |
| 69 | 🚗 | `extending-fsm-model-critical-decision-making-safety-control-autonomous-vehicles__01` | HSM | 自动驾驶高层行为决策控制器 | 层次💎 / 算术guard💎 / 丰富动作💎 | 💎 3 | 💎 3 | 💎 3 | 🟡 1 | **10.4** | 1/2 | 🟢 | · |
| 70 | 🚗 | `predictive-maneuver-planning-autonomous-vehicle-public-highway__01` | EFSM | 高速公路自动驾驶巡航、跟车、领车与换道预测机动监督器 | 算术guard💎 / 丰富动作💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | 🟡 1 | **10.3** | 3/3 | 🟢 | · |
| 71 | 🩺 | `assistive-control-active-knee-orthosis-walker-post-stroke__01` | HSM | `ALLOR` 主动膝关节矫形器加助行器的步态康复监督控制器 | 丰富动作💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 🟢 2 | 💎 3 | 🟢 2 | **10.2** | 3/3 | 🟢 | · |
| 72 | 🚗 | `topsis-gra-autonomous-driving-decision-making-5g-v2x__01` | HSM | 5G-V2X 智能网联车的分层驾驶行为决策系统 | 层次💎 / 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 💎 3 | 💎 3 | 💎 3 | ⚪ 0 | **10.2** | 2/3 | 🟢 | · |
| 73 | ✈️ | `behavior-trees-for-uav-mission-management__01` | HSM | 无人机任务管理模块 | 层次💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 / 深复合DFS🌀 | 💎 3 | 🟢 2 | 💎 3 | 🟡 1 | **10.1** | 2/3 | 🟢 | · |
| 74 | 🏭 | `stereoscopic-warehouse-control-system-based-on-plc__01` | EFSM | 立体仓库堆垛机三轴存取控制系统 | 算术guard💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 💎 3 | 🟢 2 | 🟢 2 | **10.1** | 3/3 | 🟢 | · |
| 75 | 🅿️ | `automated-valet-parking-decision-planning-finite-state-machine__01` | HSM | 自动代客泊车与定点召回分层决策控制器 | 层次💎 / 算术guard💎 / forced/aspect🔁 | 💎 3 | 💎 3 | 🟢 2 | 🟡 1 | **10.0** | 2/3 | 🟢 | · |
| 76 | 🅿️ | `controller-development-multi-layer-parking-equipment-stm32__01` | EFSM | 三层六车位立体停车设备控制器 | 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 🟢 2 | 🟢 2 | 💎 3 | **10.0** | 3/3 | 🟢 | · |
| 77 | 🏭 | `packaging-filling-machine-control-plc-logicon__01` | HSM | 散料包装/灌装机主控程序 | 故障恢复💎 / 全局应急🌐 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 🟢 2 | 🟢 2 | 💎 3 | **10.0** | 3/3 | 🟢 | · |
| 78 | 🚆 | `automated-railway-crossing-system-using-multi-sensor-integration__01` | EFSM | 多传感器道口门控与告警控制系统 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | 💎 3 | **9.9** | 3/3 | 🟢 | · |
| 79 | 🅿️ | `hierarchical-driver-aid-for-parallel-parking__02` | HSM | 并联泊车辅助系统中的 Stage 1 / Stage 2 分阶段控制逻辑 | 层次💎 / 算术guard💎 / 丰富动作💎 | 💎 3 | 💎 3 | 💎 3 | ⚪ 0 | **9.9** | 1/3 | 🟢 | · |
| 80 | 🚗 | `hybrid-verification-technique-decision-making-self-driving-vehicles__01` | FSM | 停车场自动驾驶行为监督器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | 💎 3 | **9.9** | 3/3 | 🟢 | · |
| 81 | 🌡️ | `automation-of-water-drainage-systems-using-a-programmable-logic-controller-in-mining__01` | EFSM | 矿井排水泵站 PLC 监督控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | 🟢 2 | **9.8** | 2/3 | 🟢 | · |
| 82 | 🏭 | `bumblebee-autonomous-robotic-vine-pruning__01` | HSM | 葡萄藤自主修剪高层监督控制器 | 层次💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 💎 3 | 🟡 1 | 🟢 2 | 💎 3 | **9.8** | 3/2 | 🟢 | · |
| 83 | ⚙️ | `fuel-cell-electric-robot-energy-management__01` | EFSM | 燃料电池电动机器人的燃料电池-电池混合供能能量管理控制器 | 算术guard💎 / 丰富动作💎 / 全局应急🌐 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | 🟢 2 | **9.8** | 3/2 | 🟢 | · |
| 84 | 🅿️ | `handsfree-valet-technology-hfvt__01` | FSM | 自动代客泊车高层控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | 🟢 2 | **9.8** | 2/3 | 🟢 | · |
| 85 | ✈️ | `autonomous-control-framework-unmanned-helicopter-low-altitude-flight__01` | FSM | 无人直升机低空飞行任务的高层决策控制器 | 算术guard💎 / 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | 💎 3 | **9.6** | 3/2 | 🟢 | · |
| 86 | 🅿️ | `plc-based-automatic-intelligent-car-parking-system__01` | EFSM | 停车场入口/出口门禁与车位占用监督控制器 | 算术guard💎 / 故障恢复💎 / 全局应急🌐 | 🟡 1 | 💎 3 | 🟢 2 | 💎 3 | **9.6** | 3/2 | 🟡 | · |
| 87 | 🚗 | `automated-driving-control-highway-hierarchical-architecture__01` | HSM | 高速公路自动驾驶机动选择与轨迹规划监督器 | 算术guard💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | ⚪ 0 | **9.5** | 3/3 | 🟢 | · |
| 88 | 🌡️ | `automatic-dosing-system-based-on-reclaimed-water-treatment__01` | EFSM | 再生水处理流量/水质反馈加药控制器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | 🟢 2 | **9.5** | 2/2 | 🟢 | · |
| 89 | 🚗 | `formal-verification-of-autonomous-vehicle-platooning__01` | Protocol | 车队控制中的 follower joining procedure | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | 🟢 2 | **9.5** | 2/2 | 🟢 | · |
| 90 | 🌡️ | `liquid-level-monitoring-flow-liquid-distribution-plc-scada__01` | EFSM | 液位/流量联锁的液体转运阀泵监督控制器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | 🟢 2 | **9.5** | 2/2 | 🟢 | · |
| 91 | 🚗 | `modular-verification-of-vehicle-platooning-with-respect-to-decisions-spa__01` | Protocol | 车队控制架构中的 joining procedure | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | 🟢 2 | **9.5** | 2/2 | 🟢 | · |
| 92 | 🩺 | `open-source-bionic-leg-clinical-implementation__01` | HSM | open-source powered knee-ankle prosth… | 层次💎 / 丰富动作💎 / forced/aspect🔁 | 💎 3 | 🟢 2 | 💎 3 | 🟡 1 | **9.5** | 1/2 | 🟢 | · |
| 93 | 🅿️ | `automatic-system-for-garage-control__01` | HSM | 优先级缓冲式自动泊入与取车监督器 | 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 | 🟢 2 | 🟢 2 | 💎 3 | 🟡 1 | **9.4** | 3/3 | 🟢 | · |
| 94 | 🚆 | `french-railway-interlocking-hcpn__01` | Resource | 法国铁路联锁系统中的进路建立控制逻辑 | 算术guard💎 / 丰富动作💎 | 🟢 2 | 💎 3 | 💎 3 | 🟡 1 | **9.4** | 2/1 | 🟢 | · |
| 95 | ⚙️ | `underground-multi-robot-systems-at-work-a-revolution-in-mining__01` | HSM | 地下矿井 `Deployer-Stinger` 协同部署与钻孔任务监督器 | 层次💎 | 💎 3 | 🟢 2 | 🟢 2 | 🟢 2 | **9.3** | 1/2 | 🟢 | · |
| 96 | 🩺 | `affordable-insole-sensor-based-transfemoral-prosthesis__01` | HSM | 基于 plantar insole 的 transfemoral pros… | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | ⚪ 0 | **9.2** | 2/3 | 🟢 | · |
| 97 | 🏭 | `automatic-intelligent-car-washing-machine-plc__01` | EFSM | 基于双 PLC 与三维喷头机构的智能洗车机控制系统 | 全局应急🌐 / forced/aspect🔁 | 🟢 2 | 🟢 2 | 🟢 2 | 🟢 2 | **9.2** | 3/3 | 🟢 | · |
| 98 | 🌡️ | `energy-management-system-residential-dc-microgrid__01` | EFSM | 住宅直流微电网全局能量管理控制器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | 🟢 2 | **9.2** | 1/2 | 🟢 | · |
| 99 | ⚙️ | `using-perception-cues-for-context-aware-navigation-in-dynamic-outdoor-environments__01` | FSM | 小型 UGV 上下文感知导航监督器 | 算术guard💎 / 丰富动作💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | 🟢 2 | **9.1** | 3/3 | 🟢 | · |
| 100 | 🚆 | `development-of-a-network-level-crossing-system__01` | EFSM | 网络化道口四模式监督控制器 | 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 🟢 2 | 💎 3 | 💎 3 | **9.0** | 3/3 | 🟢 | · |
| 101 | 🚗 | `driving-behavior-planning-trajectory-generation-autonomous-electric-bus__01` | HSM | 自动驾驶电动公交双层行为规划监督器 | 层次💎 / 丰富动作💎 / 复合内行为🧱 | 💎 3 | 🟢 2 | 💎 3 | ⚪ 0 | **9.0** | 1/3 | 🟢 | · |
| 102 | 🚆 | `french-railway-interlocking-hcpn__02` | Resource | 法国铁路联锁系统中的运行模式选择与模式约束逻辑 | 算术guard💎 / forced/aspect🔁 | 🟢 2 | 💎 3 | 🟢 2 | 🟡 1 | **9.0** | 2/3 | 🟢 | · |
| 103 | 🚗 | `hierarchical-hybrid-predictive-control-autonomous-road-vehicle__01` | EFSM | 高速公路场景下自动驾驶车辆的高层 maneuver assigner 与轨… | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | 🟡 1 | **9.0** | 2/3 | 🟢 | · |
| 104 | ⚙️ | `modular-autonomous-driving-system-electric-boats-fuzzy-q-learning__01` | FSM | 电动船自主驾驶监督控制器 | 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟡 1 | 🟢 2 | 🟢 2 | 💎 3 | **9.0** | 3/3 | 🟢 | · |
| 105 | ✈️ | `preliminary-design-of-robotic-control-software-for-mars-sample-return-capture-containment-and-return-system__01` | EFSM | 火星样本返回 `CCRS` 机器人传送系统的 Robot Software… | 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 🟢 2 | 💎 3 | 💎 3 | **9.0** | 3/3 | 🟢 | · |
| 106 | 🚗 | `autonomous-vehicle-driving-behavior-hierarchical-state-machine__01` | HSM | 直道自动驾驶行为决策控制器 | 层次💎 / 算术guard💎 / forced/aspect🔁 | 💎 3 | 💎 3 | 🟢 2 | ⚪ 0 | **8.9** | 1/3 | 🟢 | · |
| 107 | 🏭 | `human-robot-collaborative-assembly-eye-hand-fsm__01` | HSM | 眼手协同装配人机协作监督控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟢 2 | 💎 3 | 💎 3 | ⚪ 0 | **8.9** | 1/3 | 🟢 | · |
| 108 | 🏭 | `modular-supervisory-control-coordination-manufacturing-cell-observable-faults__01` | FSM | 制造单元旋转工作台故障容错控制器 | 算术guard💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 🟢 2 | 💎 3 | **8.9** | 3/3 | 🟢 | · |
| 109 | 🏭 | `modular-supervisory-control-multi-floor-manufacturing__01` | FSM | 多楼层制造物料转运监督控制器 | 算术guard💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 🟢 2 | 💎 3 | **8.9** | 3/3 | 🟢 | · |
| 110 | 🏭 | `no-code-robotic-programming-agile-production__01` | HSM | 多模态无代码机器人编程监督控制器 | 层次💎 / 丰富动作💎 / 复合内行为🧱 / forced/aspect🔁 | 💎 3 | 🟡 1 | 💎 3 | 🟡 1 | **8.9** | 1/3 | 🟢 | · |
| 111 | ⚙️ | `robot-excavation-geometrically-cohesive-granular-media__01` | FSM | 几何黏聚颗粒物挖掘机器人的循环任务监督器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | 🟢 2 | **8.9** | 1/1 | 🟢 | · |
| 112 | 🏢 | `asm-robot-cyber-physical-home-automation-controller__01` | EFSM | 水位、温控、烟雾、照明与门禁一体化过程控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | 🟢 2 | **8.8** | 2/3 | 🟢 | · |
| 113 | 🩺 | `design-and-control-of-the-mindwalker-exoskeleton__01` | EFSM | `MINDWALKER` 下肢外骨骼的 gait assistance 监… | 算术guard💎 / 丰富动作💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | 🟢 2 | **8.8** | 3/2 | 🟢 | · |
| 114 | 🚗 | `high-level-decision-making-autonomous-overtaking-mpc-switching-control__01` | EFSM | 双向道路自动超车跟车、减速、停车与超车切换监督器 | 算术guard💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 🟢 2 | 🟢 2 | **8.8** | 2/3 | 🟢 | · |
| 115 | 🚗 | `planning-for-safe-abortable-overtaking-maneuvers-in-autonomous-driving__01` | FSM | 双向道路场景中的自动驾驶车辆超车行为与轨迹规划器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | 🟢 2 | **8.8** | 2/3 | 🟢 | · |
| 116 | 🏭 | `control-system-automatic-bamboo-splitting-equipment-plc__01` | EFSM | 自动破竹机的 PLC 送料、选刀、对中与切割控制系统 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | 🟡 1 | **8.7** | 2/2 | 🟢 | · |
| 117 | 🅿️ | `hanging-rotary-parking-system-plc-hmi__01` | EFSM | 旋转式多车位停车控制器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | 🟡 1 | **8.7** | 2/2 | 🟢 | · |
| 118 | 🩺 | `modular-neuroprosthesis-hybrid-fes-robot-assistance__01` | EFSM | 面向 hybrid `FES-robot` gait assistance… | 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | 🟡 1 | 🟢 2 | 🟢 2 | 💎 3 | **8.7** | 3/2 | 🟢 | · |
| 119 | 🌡️ | `semi-automatic-dam-gate-plc-mini-hoist__01` | EFSM | 半自动水闸门 PLC 监督控制系统 | 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 🟢 2 | 💎 3 | 💎 3 | **8.7** | 3/2 | 🟡 | · |
| 120 | 🚗 | `decision-making-framework-autonomous-vehicles-hierarchical-state-machine__01` | HSM | 复杂直线路段场景下自动驾驶车辆的三级行为决策控制器 | 层次💎 / 算术guard💎 | 💎 3 | 💎 3 | 🟢 2 | ⚪ 0 | **8.6** | 1/2 | 🟢 | · |
| 121 | 🩺 | `pediatric-knee-exoskeleton-adaptive-control-overground-walking__01` | EFSM | `P.REX` 儿童膝关节外骨骼的高层 gait-phase 监督控制器 | 丰富动作💎 / 全局应急🌐 / forced/aspect🔁 | 🟡 1 | 🟢 2 | 💎 3 | 🟢 2 | **8.6** | 3/1 | 🟡 | · |
| 122 | 🏭 | `plc-course-fsm__01` | FSM | PLC 控制的 box fill 子过程 | 算术guard💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 🟢 2 | 💎 3 | **8.6** | 3/2 | 🟡 | · |
| 123 | 🏢 | `design-of-automatic-control-system-of-intelligent-garage-door-based-on-plc__01` | EFSM | 智能车库门自动/手动与防夹控制器 | 算术guard💎 | 🟡 1 | 💎 3 | 🟢 2 | 🟢 2 | **8.5** | 2/2 | 🟡 | · |
| 124 | 🚆 | `door-design-control-system-high-speed-train-kcmp__01` | EFSM | 高速列车滑动塞拉门开闭与防夹控制器 | 算术guard💎 | 🟡 1 | 💎 3 | 🟢 2 | 🟢 2 | **8.5** | 2/2 | 🟢 | · |
| 125 | 🚗 | `hybrid-state-system-development-autonomous-vehicle-control-urban-scenarios__01` | HSM | 城市自动驾驶 `HSS` 高层元状态与道路障碍绕行监督器 | 层次💎 | 💎 3 | 🟢 2 | 🟢 2 | 🟡 1 | **8.5** | 1/2 | 🟢 | · |
| 126 | ✈️ | `proactive-guidance-uav-landing-dynamic-platform__01` | EFSM | 四旋翼 UAV 面向动态平台回收的高层自主降落监督控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟢 2 | **8.5** | 2/2 | 🟢 | · |
| 127 | ⚙️ | `reflexive-evasion-robot-instantaneous-dynamic-obstacle-avoidance__01` | FSM | 四足机器人面对高速动态障碍时的瞬时避障与恢复控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟢 2 | **8.5** | 2/2 | 🟢 | · |
| 128 | ✈️ | `modelling-and-analysing-the-landing-gear-system-a-solution-with-event-b-rodin__01` | EFSM | 飞机起落架控制系统 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | 🟡 1 | **8.4** | 1/2 | 🟡 | · |
| 129 | 🅿️ | `plc-based-tower-type-elevator-model-for-automatic-car-parking-system__01` | Resource | 塔式自动停车系统的 PLC 电梯与车位分配控制器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | 🟡 1 | **8.4** | 1/2 | 🟡 | · |
| 130 | 🌡️ | `ozone-desulfurization-and-denitration-control-system-based-on-plc-and-kingview__01` | EFSM | 锅炉烟气臭氧脱硫脱硝 `PLC` 监督控制器 | 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 🟢 2 | 💎 3 | 🟢 2 | **8.3** | 1/2 | 🟢 | · |
| 131 | 🅿️ | `vertical-rotary-car-parking-plc-outseal__01` | EFSM | 立体旋转式停车库的车位选择、旋转取放与出车放行 PLC 控制器 | 丰富动作💎 | 🟡 1 | 🟢 2 | 💎 3 | 🟢 2 | **8.3** | 2/1 | 🟡 | · |
| 132 | 🚗 | `autonomous-longitudinal-speed-controller-urban-stop-and-go-traffic__01` | FSM | 城市 stop-and-go 自主跟驰纵向监督控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟢 2 | **8.2** | 1/2 | 🟢 | · |
| 133 | 🌡️ | `energy-management-strategy-hybrid-micro-grid-renewable-energy__01` | EFSM | 混合微电网的能量管理控制器 | 算术guard💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 🟢 2 | 🟢 2 | **8.2** | 1/2 | 🟢 | · |
| 134 | 🏭 | `exoskeleton-workflow-finite-state-machine-adaptivity__01` | HSM | 面向板件拆装工序的工业手腕外骨骼工作流自适应支持监督器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **8.2** | 2/3 | 🟡 | · |
| 135 | 🚗 | `infrastructure-assisted-automated-driving-functions__01` | EFSM | 基础设施辅助自动驾驶轨迹规划控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **8.2** | 2/3 | 🟢 | · |
| 136 | ✈️ | `multiple-ground-target-finding-inspection-multirotor-uas__01` | EFSM | 多旋翼 UAS 多目标搜索与近距检查任务控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟢 2 | **8.2** | 1/2 | 🟢 | · |
| 137 | 🌡️ | `novel-supervisory-ev-charging-microgrid__01` | EFSM | 光伏-储能-电网混合 `EV` 快充站监督器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **8.2** | 2/3 | 🟢 | · |
| 138 | 🚗 | `optimal-assigner-hybrid-predictive-control-autonomous-vehicle__01` | EFSM | 三车道自动驾驶正常跟踪、跟车、领车与强制换道 assigner | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **8.2** | 2/3 | 🟢 | · |
| 139 | 🚆 | `system-modeling-in-the-cosma-environment__01` | EFSM | 分布式列车制动控制器 | 算术guard💎 | 🟡 1 | 💎 3 | 🟢 2 | 🟢 2 | **8.2** | 1/2 | 🟢 | · |
| 140 | ✈️ | `uav-delivery-unknown-heterogeneous-energy-storage__01` | EFSM | 按需配送 UAV 任务竞价与返航控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟢 2 | **8.2** | 1/2 | 🟢 | · |
| 141 | 🌡️ | `wind-energy-conversion-system-supervisor-deterministic-finite-state-machine__01` | FSM | 变速变桨 DFIG 风能转换系统运行状态监督器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟢 2 | **8.2** | 1/2 | 🟢 | · |
| 142 | 🩺 | `data-driven-phase-based-control-powered-knee-ankle-prosthesis-variable-incline-stair-ascent-descent__01` | EFSM | 主动膝踝假肢楼梯上下行 HKIC 相位监督控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **7.9** | 2/2 | 🟢 | · |
| 143 | 🩺 | `error-recovery-wearable-robotic-co-grasping__01` | FSM |  wearable robotic co-grasping gripper… | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟢 2 | **7.9** | 1/1 | 🟢 | · |
| 144 | 🚆 | `microcontroller-railway-crossing-track-obstacle-monitoring__01` | EFSM | 铁路平交口闸门与障碍告警控制器 | 丰富动作💎 / 全局应急🌐 | ⚪ 0 | 🟢 2 | 💎 3 | 🟢 2 | **7.9** | 3/2 | 🟡 | · |
| 145 | 🅿️ | `versatile-mode-parking-system-fpga__01` | EFSM | 四模式停车位识别与路径生成控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **7.9** | 1/3 | 🟢 | · |
| 146 | ⚙️ | `vision-driven-trailer-loading-autonomous-surface-vehicles__01` | EFSM | 自主水面艇 `ASV` 的拖车装载高层监督控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟢 2 | **7.9** | 1/1 | 🟡 | · |
| 147 | 🌡️ | `boiler-wastewater-treatment-control-monitoring-plc-hmi__01` | EFSM | 锅炉废水处理与监控控制系统 | 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 🟢 2 | 💎 3 | 🟡 1 | **7.8** | 1/3 | 🟢 | · |
| 148 | ✈️ | `feasibility-of-onboard-processing-of-heuristic-path-planning-and-navigation-algorithms-within-suas-autopilot-computational-constraints__01` | FSM |  SUAS 移动目标启发式跟踪控制器 | 算术guard💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 🟢 2 | 🟢 2 | **7.8** | 3/2 | 🟢 | · |
| 149 | 🏢 | `home-automation-system-hardware-descriptive-tools__01` | EFSM | 楼宇与家居自动化场景下的门禁、安全告警与环境调节控制器 | 算术guard💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 🟢 2 | 🟢 2 | **7.8** | 3/2 | 🟡 | · |
| 150 | 🩺 | `preliminary-evaluations-of-a-self-contained-anthropomorphic-transfemoral-prosthesis__01` | HSM | 自供能膝踝一体主动股骨假肢的高层活动模式与相位监督控制器 | 层次💎 / 丰富动作💎 / forced/aspect🔁 | 💎 3 | 🟡 1 | 💎 3 | ⚪ 0 | **7.8** | 1/2 | 🟢 | · |
| 151 | 🚗 | `real-time-decision-making-for-autonomous-city-vehicles__01` | FSM | 城市自动驾驶高层 maneuver 决策控制器 | 丰富动作💎 / 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 🟡 1 | 💎 3 | 💎 3 | **7.8** | 3/2 | 🟡 | · |
| 152 | 🅿️ | `verilog-multi-car-parking-fsm-urban-management__01` | EFSM | 多车位门禁与容量控制器 | 丰富动作💎 | 🟡 1 | 🟢 2 | 💎 3 | 🟡 1 | **7.8** | 2/2 | 🟡 | · |
| 153 | 🏢 | `siemens-simatic-s7-200-plc-controlled-elevator__01` | EFSM | 三层电梯原型呼梯、停靠与电机方向控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | 🟡 1 | **7.7** | 2/2 | 🟡 | · |
| 154 | 🩺 | `size-adjustable-pediatric-lower-limb-exoskeleton-weight-shift__01` | EFSM | 儿童下肢外骨骼的 gait assistance 监督控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | 🟡 1 | **7.7** | 1/3 | 🟢 | · |
| 155 | 🚆 | `standardization-of-logic-for-a-constant-warning-time-control-at-automatic-level-crossings__01` | EFSM | 自动道口恒定预警时间控制的 level crossing controll… | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟡 1 | **7.7** | 2/2 | 🟢 | · |
| 156 | 🌡️ | `state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship__01` | EFSM | LNG 船混合供能系统的能量管理控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟡 1 | **7.7** | 2/2 | 🟢 | · |
| 157 | 🧩 | `sysml-safety-analysis-integration__01` | EFSM | 飞机轮刹系统的容错供压逻辑 | 算术guard💎 / 故障恢复💎 | ⚪ 0 | 💎 3 | 🟢 2 | 💎 3 | **7.7** | 1/1 | 🟡 | · |
| 158 | 🏭 | `collective-transport-robot-swarms__01` | FSM | 仓储群体机器人集体搬运控制器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **7.6** | 1/2 | 🟢 | · |
| 159 | 🩺 | `control-of-multigrasp-myoelectric-prosthetic-hands__01` | EFSM | 多指假手的 multigrasp myoelectric coordina… | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **7.6** | 1/2 | 🟢 | · |
| 160 | 🚗 | `deterministic-operating-strategy-multi-objective-nmpc-safe-autonomous-driving-urban-traffic__01` | EFSM | 城市自动驾驶 NMPC 模式监督器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **7.6** | 1/2 | 🟢 | · |
| 161 | 🩺 | `phase-variable-approach-improved-rhythmic-non-rhythmic-control-powered-knee-ankle-prosthesis__01` | EFSM | 主动膝踝假肢相位变量监督控制器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **7.6** | 1/2 | 🟢 | · |
| 162 | 🅿️ | `smart-parking-system-plc-rfid__01` | EFSM | 多层停车楼 PLC 存取车控制器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **7.6** | 1/2 | 🟡 | · |
| 163 | 🚗 | `trajectory-optimization-and-state-selection-for-urban-automated-driving__01` | EFSM | 城市场景自动驾驶车辆的轨迹规划模式选择器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **7.6** | 1/2 | 🟢 | · |
| 164 | ✈️ | `aircraft-electrical-distribution-fsm-control__01` | EFSM | 飞机电气分配系统重构与 shedding 监督控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | 🟢 2 | **7.5** | 2/2 | 🟡 | · |
| 165 | 🚗 | `autonomous-driving-benefit-evaluation-fsm__01` | FSM | 自动驾驶车辆的高层驾驶行为决策系统 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | 🟢 2 | **7.5** | 2/2 | 🟢 | · |
| 166 | 🚗 | `hierarchical-framework-decision-making-trajectory-tracking-autonomous-vehicles__01` | FSM | 高速公路自动驾驶高层行为决策控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | 🟢 2 | **7.5** | 2/2 | 🟢 | · |
| 167 | ⚙️ | `automatic-bridge-control-for-ships-using-plc__01` | EFSM | 船舶触发开桥、栏杆联动与信号切换控制器 | 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 🟢 2 | 🟢 2 | 💎 3 | **7.4** | 3/1 | 🟡 | · |
| 168 | 🏢 | `automatic-elevator-controller__01` | FSM | 三层自动电梯的楼层与升降方向控制器 | 故障恢复💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 🟢 2 | 🟢 2 | 💎 3 | **7.4** | 3/1 | 🟡 | · |
| 169 | 🏭 | `development-of-automatic-packaging-system-using-plc-and-scada-for-industries__02` | EFSM | 包装产线后端的装箱、封箱与称重放行/剔除控制段 | 丰富动作💎 | 🟡 1 | 🟢 2 | 💎 3 | 🟢 2 | **7.4** | 0/0 | 🟡 | · |
| 170 | 🚗 | `intention-prediction-control-vehicle-platoon-driver-cutin__01` | FSM | 混合交通场景中车辆编队应对人驾车辆 cut-in 的高层模式选择控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟡 1 | **7.4** | 1/2 | 🟢 | · |
| 171 | ⚙️ | `optimized-autonomous-navigation-field-robots__01` | FSM |  FarmBeast 田间机器人行间导航监督控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟡 1 | **7.4** | 2/1 | 🟢 | · |
| 172 | 🚆 | `verifying-accuracy-interlocking-tables-railway-signalling-asm__01` | EFSM | 车站联锁进路请求、道岔布置与列车移动监督控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | 🟡 1 | **7.4** | 2/1 | 🟢 | · |
| 173 | ✈️ | `development-of-a-finite-state-machine-for-a-small-unmanned-aircraft-system-using-experimental-design__01` | FSM |  SUAS 地面车辆跟踪参数切换控制器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **7.3** | 1/1 | 🟢 | · |
| 174 | 🏢 | `enhanced-smart-home-control-monitoring-system__01` | EFSM | 智能家居场景下的水位、温控、烟雾、照明与密码门禁一体化控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | 🟢 2 | **7.3** | 1/2 | 🟢 | · |
| 175 | 🚆 | `implementation-of-automatic-gate-control-for-railroad-switch-and-anti-collision__01` | EFSM | 道口门控与障碍广播保护控制器 | 丰富动作💎 / forced/aspect🔁 | ⚪ 0 | 🟢 2 | 💎 3 | 🟢 2 | **7.3** | 1/2 | 🟡 | · |
| 176 | 🅿️ | `sistem-parkir-pintar-berbasis-plc-rfid__01` | EFSM |  RFID 导向型多层停车入库控制器 | 算术guard💎 / 丰富动作💎 | 🟡 1 | 💎 3 | 💎 3 | ⚪ 0 | **7.3** | 1/1 | 🟡 | · |
| 177 | 🚆 | `dependable-state-machine-hardware-architecture-railway-interlocking__01` | FSM | 铁路道口联锁与栏杆告警控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | 🟢 2 | **7.2** | 2/1 | 🟡 | · |
| 178 | 🏢 | `distributed-elevator-control-system-can__01` | EFSM | 基于 `CAN` 广播的分布式电梯调度与运动控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **7.2** | 2/3 | 🟢 | · |
| 179 | 🏭 | `industrial-agv-supervisory-control__01` | FSM |  AGV 运行模式监督器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | 🟢 2 | **7.2** | 1/2 | 🟢 | · |
| 180 | 🅿️ | `plc-control-system-for-translation-motion-stereo-garage__01` | EFSM | 平移式立体车库存取控制器 | 丰富动作💎 | 🟡 1 | 🟢 2 | 💎 3 | 🟡 1 | **7.2** | 1/1 | 🟡 | · |
| 181 | ⚙️ | `a-robot-with-decoupled-mechanical-structure-and-adapted-state-machine-control-for-both-ground-and-staircase-situations__01` | FSM | 解耦机械结构送货机器人的楼梯切换与攀爬控制器 | 算术guard💎 | 🟡 1 | 💎 3 | 🟢 2 | 🟡 1 | **7.1** | 1/1 | 🟢 | · |
| 182 | ✈️ | `autonomous-aerial-robot-high-speed-search-intercept__01` | FSM | 高速搜索与拦截任务中的无人机 mission-control 控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | 🟢 2 | **7.0** | 0/2 | 🟡 | · |
| 183 | ⚙️ | `autonomous-interactive-robot-guide-industrial-museum__01` | EFSM | 工业博物馆导览机器人任务编排器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | 🟢 2 | **7.0** | 0/2 | 🟡 | · |
| 184 | ⚙️ | `design-of-mobile-robot-for-air-ducts-exploration__01` | FSM | 通风管道巡检机器人的高层导航与恢复控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | 🟢 2 | **7.0** | 1/1 | 🟢 | · |
| 185 | 🏭 | `automatic-wall-painting-machine-plc-cp1e-na20dr-a__01` | EFSM | 自动墙面喷涂机升降横移顺序控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | 🟢 2 | **6.9** | 1/1 | 🟡 | · |
| 186 | 🌡️ | `enhanced-hierarchical-microgrids-thermal-management__01` | EFSM | 微电网次级控制器，用于按热负荷、效率与谐波风险调整并联逆变器投入数量 | 算术guard💎 | 🟡 1 | 💎 3 | 🟢 2 | ⚪ 0 | **6.9** | 2/2 | 🟡 | · |
| 187 | ✈️ | `mini-uav-altitude-energy-management__01` | EFSM | 小型 VTOL UAV 混合动力能量管理控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.9** | 2/2 | 🟢 | · |
| 188 | ⚙️ | `protection-of-induction-motor-using-plc__01` | EFSM | 三相感应电机 PLC 保护控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | 🟢 2 | **6.9** | 1/1 | 🟡 | · |
| 189 | 🌡️ | `ship-water-supply-automatic-control-plc__01` | EFSM | 船舶集中供水系统的 PLC 温度调节与启停控制器 | 全局应急🌐 | ⚪ 0 | 🟢 2 | 🟢 2 | 🟢 2 | **6.9** | 3/2 | 🟡 | · |
| 190 | 🚗 | `formal-verification-of-autonomous-vehicle-platooning__02` | Protocol | 车队控制中的 follower leaving procedure | — | 🟡 1 | 🟢 2 | 🟢 2 | 🟡 1 | **6.8** | 2/2 | 🟡 | · |
| 191 | 🚗 | `localization-perception-control-decision-making-low-speed-autonomous-shuttle__01` | FSM | 低速 autonomous shuttle 决策与跟驰/信号处理监督器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | 🟡 1 | **6.8** | 2/2 | 🟡 | · |
| 192 | 🩺 | `design-and-control-of-a-powered-transfemoral-prosthesis__01` | EFSM | 动力股骨假肢膝踝一体 gait-phase 监督控制器 | 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 🟢 2 | 💎 3 | ⚪ 0 | **6.7** | 1/2 | 🟡 | · |
| 193 | 🩺 | `enhanced-gastrocnemius-mimicking-powered-exoskeleton__01` | EFSM | `EGME` 下肢动力外骨骼的相位识别监督控制器 | 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 🟢 2 | 💎 3 | ⚪ 0 | **6.7** | 1/2 | 🟡 | · |
| 194 | 🚗 | `local-motion-planning-rural-road-overtaking__01` | FSM | 乡村道路环境中的自动驾驶超车行为与局部轨迹规划器 | 丰富动作💎 | 🟡 1 | 🟢 2 | 💎 3 | ⚪ 0 | **6.7** | 2/1 | 🟡 | · |
| 195 | 🏢 | `plc-based-multi-floor-elevator-control-system__01` | EFSM | 四层 PLC 电梯的上行/下行遍历控制 | 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 🟢 2 | 💎 3 | ⚪ 0 | **6.7** | 1/2 | 🟡 | · |
| 196 | 🅿️ | `arduino-multi-tiered-car-parking-unilag__01` | EFSM | 多层停车场的入口/出口门禁与车位占用监控控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟡 | · |
| 197 | 🅿️ | `automatic-car-parking-using-plc__01` | EFSM | 多层自动停车 PLC 控制系统 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟡 | · |
| 198 | 🌡️ | `automatic-fluid-level-control-using-programmable-logic-controller__01` | EFSM | 混合罐、操作罐与用户罐组成的三罐液位泵阀控制器 | 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 🟢 2 | 🟢 2 | 🟢 2 | **6.6** | 3/1 | 🟡 | · |
| 199 | 🌡️ | `battery-balancing-fsm-flyback-converters__01` | EFSM | 串联锂铁电池组的温度与荷电状态联合均衡控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟡 | · |
| 200 | 🅿️ | `behavioral-planner-car-sharing-fleet-relocation__01` | FSM | 智慧停车与车共享重定位场景中的自动驾驶 follower 行为规划器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟢 | · |
| 201 | 🏭 | `development-of-plc-based-automated-packaging-control-system-via-grafcet__01` | EFSM | 罐装包装顺序控制器 | 算术guard💎 | 🟡 1 | 💎 3 | 🟢 2 | ⚪ 0 | **6.6** | 2/1 | 🟡 | · |
| 202 | 🏢 | `electro-hydraulic-telescopic-elevator-plc-control__01` | EFSM | 四层伸缩式液压电梯 PLC 控制器 | 算术guard💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 🟢 2 | ⚪ 0 | **6.6** | 1/2 | 🟡 | · |
| 203 | 🏢 | `electro-pneumatic-prototype-elevator-controlled-by-plc__01` | EFSM | 三层电-气动 PLC 电梯呼梯、行驶与门控控制器 | 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 🟢 2 | 🟢 2 | 🟢 2 | **6.6** | 3/1 | 🟡 | · |
| 204 | ✈️ | `flight-control-hybrid-drones-parcel-relay-manoeuvres__01` | EFSM | 速度阈值驱动混合无人机飞行模式切换控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟢 | · |
| 205 | ✈️ | `formal-specification-and-analysis-of-take-off-procedure-using-vdm-sl__01` | Resource | 机场地面空管中的起飞流程控制 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟢 | · |
| 206 | ✈️ | `fuzzy-state-machine-energy-management-hybrid-electric-uavs__01` | EFSM | 混合电动无人机的光伏-燃料电池-电池能量管理控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟢 | · |
| 207 | 🚗 | `low-speed-autonomous-vehicles-park-fsm__01` | FSM | 园区低速自动驾驶决策控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟢 | · |
| 208 | 🚆 | `modelling-railway-interlocking-tables-using-coloured-petri-nets__01` | Resource | 铁路联锁表中的 route locking / release logic | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 2/1 | 🟡 | · |
| 209 | ✈️ | `multi-uavs-formation-autonomous-control-rqpso-fsm-dmpc__01` | FSM | 多无人机编队重构任务中的 formation management unit | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟢 | · |
| 210 | 🅿️ | `scada-multi-area-parking-system-plc-m221__01` | EFSM | 双区域停车系统的入口/出口闸杆、满位指示与计数联锁控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟡 | · |
| 211 | 🅿️ | `smart-car-parking-system-rfid-iot__01` | EFSM |  RFID 门禁、车位占用同步与出场计费控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟡 | · |
| 212 | 🅿️ | `smart-parking-spot-allocation-priority-verilog-hdl__01` | EFSM | 类别优先停车位分配与道闸控制器 | 算术guard💎 / 丰富动作💎 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟢 | · |
| 213 | 🌡️ | `state-machine-control-multi-sources-pv-pemfc-batteries__01` | EFSM |  PV-PEMFC-电池多源混合供能能量管理系统 | 算术guard💎 / forced/aspect🔁 | 🟡 1 | 💎 3 | 🟢 2 | ⚪ 0 | **6.6** | 1/2 | 🟢 | · |
| 214 | 🚆 | `using-z-specification-for-railway-interlocking-safety__01` | Resource | 铁路联锁系统的组件级状态描述 | 算术guard💎 | 🟡 1 | 💎 3 | 🟢 2 | ⚪ 0 | **6.6** | 2/1 | 🟡 | · |
| 215 | 🚆 | `verification-of-railway-interlocking-systems__01` | Resource | SSI 联锁系统中的 route lifecycle 控制逻辑 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 2/1 | 🟡 | · |
| 216 | 🅿️ | `verilog-design-for-multi-car-parking-management-system__01` | EFSM | 口令校验、车位计数与进出传感控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟡 | · |
| 217 | 🅿️ | `vision-based-parking-assistance-system-for-leaving-perpendicular-angle-parking-lots__01` | EFSM | 离位倒车辅助检测与告警控制模块 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.6** | 1/2 | 🟢 | · |
| 218 | ✈️ | `flight-demonstrations-unmanned-aerial-vehicle-swarming-concepts__01` | FSM | 双无人机协同搜索与目标确认任务的高层任务控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | 🟡 1 | **6.5** | 1/2 | 🟡 | · |
| 219 | 🌡️ | `perencanaan-control-valve-pada-head-tank-plta-tulungagung-menggunakan-plc__01` | EFSM | 水电站头水箱 PLC 控制阀系统 | — | 🟡 1 | 🟢 2 | 🟢 2 | 🟡 1 | **6.5** | 1/2 | 🟡 | · |
| 220 | 🏭 | `product-filling-packaging-hmi-omron-plc__01` | EFSM | 可配置计数式产品灌装/包装控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | 🟡 1 | **6.5** | 1/2 | 🟡 | · |
| 221 | 🩺 | `control-framework-for-sloped-walking-powered-transfemoral-prosthesis__01` | EFSM | 动力股骨假肢在上下坡行走中的 knee/ankle gait-phase … | 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 🟢 2 | 💎 3 | ⚪ 0 | **6.4** | 0/2 | 🟡 | · |
| 222 | 🩺 | `controlling-knee-swing-initiation-and-ankle-plantarflexion-active-prosthesis__01` | EFSM | active knee and ankle prosthesis 的四态 … | 丰富动作💎 | 🟡 1 | 🟢 2 | 💎 3 | ⚪ 0 | **6.4** | 1/1 | 🟡 | · |
| 223 | 🚆 | `formal-verification-dependable-state-machine-hardware-architecture-safety-critical-cps__01` | EFSM | 双传感道口门控与告警铁路联锁控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | 🟡 1 | **6.4** | 2/1 | 🟡 | · |
| 224 | 🚆 | `railway-interlocking-nusmv-hardware-architecture__01` | FSM | 五态联锁闸门、警灯与汽笛控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | 🟡 1 | **6.4** | 2/1 | 🟡 | · |
| 225 | ✈️ | `simultaneous-obstacles-avoidance-robust-autonomous-landing-uav-moving-vehicle__01` | FSM | 无人机移动载具避障着陆监督控制器 | 丰富动作💎 | 🟡 1 | 🟢 2 | 💎 3 | ⚪ 0 | **6.4** | 1/1 | 🟡 | · |
| 226 | 🩺 | `adaptive-stair-climbing-powered-knee-ankle-prosthesis__01` | EFSM | powered knee and ankle prosthesis 的 a… | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.3** | 1/1 | 🟢 | · |
| 227 | 🩺 | `biomechanical-comparison-emg-biological-torque-hip-exoskeleton__01` | EFSM | 气动 hip exoskeleton 的 biological torqu… | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.3** | 1/1 | 🟡 | · |
| 228 | 🩺 | `design-and-control-of-a-pneumatically-actuated-transtibial-prosthesis__01` | EFSM | 气动驱动经胫截肢踝关节假肢的实时步态相位控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.3** | 1/1 | 🟡 | · |
| 229 | ⚙️ | `design-and-implementation-of-an-asynchronous-finite-state-controller-for-wheeled-mobile-robots__01` | EFSM | 轮式移动机器人在三车道环境中的避障换道控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.3** | 1/1 | 🟡 | · |
| 230 | 🌡️ | `intelligent-water-tank-automation-system-using-fpga-for-efficient-water-management__01` | EFSM | 水箱液位自动控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟢 2 | **6.3** | 1/2 | 🟡 | · |
| 231 | 🏢 | `motion-based-automatic-door-opener-metal-detector__01` | EFSM | 基于 `PIR` 与金属检测的自动门控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.3** | 1/1 | 🟡 | · |
| 232 | 🅿️ | `multisensor-based-environment-modelling-and-control-applications-for-mobile-robots__01` | FSM | 视觉引导移动机器人停车控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.3** | 1/1 | 🟡 | · |
| 233 | 🚆 | `radio-based-intelligent-railway-grade-crossing-system__01` | EFSM | 多轨铁路道口的无线报文驱动门控与信号控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.3** | 1/1 | 🟡 | · |
| 234 | 🩺 | `robotic-knee-ankle-prosthesis-shared-neural-control__01` | EFSM | 机器人膝踝假肢的 shared neural high-level con… | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.3** | 1/1 | 🟡 | · |
| 235 | 🩺 | `semi-powered-stance-control-swing-assist-transfemoral-prosthesis__01` | EFSM | semi-powered stance-control swing-ass… | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.3** | 1/1 | 🟡 | · |
| 236 | ⚙️ | `supervisory-control-systems-state-machines-outputs__01` | FSM | 三设备双缓存制造系统 Mealy 监督控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.3** | 1/1 | 🟢 | · |
| 237 | 🅿️ | `verilog-based-solution-for-multi-vehicle-parking__01` | EFSM | 多车位门禁与容量控制器 | 算术guard💎 / 丰富动作💎 | ⚪ 0 | 💎 3 | 💎 3 | ⚪ 0 | **6.3** | 1/1 | 🟡 | · |
| 238 | ⚙️ | `center-articulated-hydrostatic-cotton-harvesting-rover__01` | EFSM | 中心铰接式棉花采摘车的视觉伺服任务监督控制器 | 算术guard💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **6.2** | 3/2 | 🟡 | · |
| 239 | 🅿️ | `plc-based-automatic-multistoried-car-parking-system__01` | EFSM | 半圆形多层停车系统中的升降机与托盘联合控制器 | — | 🟡 1 | 🟢 2 | 🟢 2 | 🟡 1 | **6.2** | 1/1 | 🟡 | · |
| 240 | 🅿️ | `sistem-otomasi-mesin-tempat-parkir-mobil-bawah-tanah__01` | EFSM | 地下立体停车升降-旋转-推送控制器 | — | 🟡 1 | 🟢 2 | 🟢 2 | 🟡 1 | **6.2** | 1/1 | 🟡 | · |
| 241 | 🏢 | `automatic-door-controller-smart-building__01` | EFSM | 基于 PIR 与超声波传感器的智能楼宇自动滑门控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | 🟡 1 | **6.1** | 1/1 | 🟡 | · |
| 242 | 🏢 | `vlsi-elevator-control-finite-state-machine__01` | FSM | 三层电梯 Mealy 状态机控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | 🟡 1 | **6.1** | 1/1 | 🟡 | · |
| 243 | 🏭 | `automatic-sorting-conveyor-belt-plc__01` | EFSM | 基于 PLC 的按高度分拣输送带与气缸剔除控制系统 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | ⚪ 0 | **6.0** | 2/2 | 🟡 | · |
| 244 | 🩺 | `combining-neural-stimulation-powered-exoskeletal-knee-stroke-walking__01` | EFSM | 卒中步行辅助混合外骨骼四相位控制器 | 丰富动作💎 / forced/aspect🔁 | ⚪ 0 | 🟢 2 | 💎 3 | ⚪ 0 | **6.0** | 2/2 | 🟡 | · |
| 245 | 🏢 | `electro-pneumatic-prototype-elevator-plc__01` | EFSM | 三层电气动电梯呼梯、升降与门控监督器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟢 2 | **6.0** | 1/1 | 🟡 | · |
| 246 | 🌡️ | `intelligent-water-tank-automation-fpga__01` | FSM | 水位阈值驱动补水与手动复位控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟢 2 | **6.0** | 1/1 | 🟡 | · |
| 247 | 🅿️ | `parking-gate-spike-barrier-microcontroller__01` | EFSM | 停车闸门与强闯防逃逸 `spike barrier` 控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟢 2 | **6.0** | 1/1 | 🟡 | · |
| 248 | 🚆 | `pressure-sensed-fast-response-anti-collision-system-railway-gate-control__01` | EFSM | 带防碰撞检测的铁路道口门控控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟢 2 | **6.0** | 0/2 | 🟡 | · |
| 249 | ✈️ | `unmanned-aerial-carrier-anchoring-companion-uavs__01` | FSM | 空中载机运输与锚定监督控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟢 2 | **6.0** | 1/1 | 🟡 | · |
| 250 | 🚗 | `improved-mpc-self-driving-cars__01` | EFSM | 障碍避让与超车监督控制器 | 算术guard💎 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.9** | 1/3 | 🟢 | · |
| 251 | 🚗 | `lane-change-decision-planning-multilane-expressway-autonomous-vehicles__01` | EFSM | 多车道高速场景自动驾驶换道决策与轨迹规划控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.9** | 1/3 | 🟡 | · |
| 252 | 🚗 | `maneuver-planner-for-automated-vehicles-on-urban-scenarios__01` | FSM | 城市自动驾驶机动规划器中的监管信号处理模块 | 算术guard💎 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.9** | 1/3 | 🟡 | · |
| 253 | 🌡️ | `embedded-dam-gate-control-system-c-visual-basic__01` | EFSM | 水坝闸门液位阈值控制器 | — | 🟡 1 | 🟢 2 | 🟢 2 | ⚪ 0 | **5.7** | 1/2 | 🟡 | · |
| 254 | 🩺 | `stair-ascent-phase-variable-control-powered-knee-ankle-prosthesis__01` | EFSM | 主动膝踝假肢 stair-ascent 相位变量监督控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | ⚪ 0 | **5.7** | 1/2 | 🟡 | · |
| 255 | 🚆 | `automatic-generation-and-verification-of-railway-interlocking-control-ta__01` | Resource | 铁路联锁控制表中的进路设定逻辑 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.6** | 2/1 | 🟡 | · |
| 256 | 🏢 | `designing-an-elevator-controller-using-vhdl__01` | FSM | 四层电梯请求服务控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.6** | 2/1 | 🟡 | · |
| 257 | 🚗 | `integrated-decision-and-control-at-multi-lane-intersections-with-mixed-traffic-flow__01` | EFSM | 多车道路口信号感知式预期车速切换控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.6** | 1/2 | 🟡 | · |
| 258 | 🚦 | `intelligent-traffic-congestion-control-using-machine-learning-wireless-network__01` | EFSM | 摄像头车流计数、救护车优先与相邻路口联动控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.6** | 1/2 | 🟡 | · |
| 259 | 🏢 | `three-floor-elevator-state-diagram__01` | EFSM | 三层电梯呼梯、选层与上下行驱动控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.6** | 2/1 | 🟡 | · |
| 260 | 🚆 | `alterability-states-single-track-railway-line-control-system__01` | FSM | 单线铁路低流量线路 routing/update 状态机 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟡 1 | **5.5** | 2/1 | 🟡 | · |
| 261 | 🅿️ | `automated-parking-system-using-plc-technology__01` | EFSM | 双门禁停车场可用车位监督控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟡 1 | **5.5** | 1/2 | 🟡 | · |
| 262 | 🅿️ | `automatic-car-parking-system-verilog-hdl__01` | EFSM | 密码门禁与车位引导控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟡 1 | **5.5** | 1/2 | 🟡 | · |
| 263 | 🩺 | `bio-inspired-control-robotic-foot-ankle-prosthesis-level-walking-stair-ascent__01` | EFSM | 机器人 foot-ankle prosthesis 的 BiOM gait… | 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 🟡 1 | 💎 3 | ⚪ 0 | **5.5** | 1/1 | 🟡 | · |
| 264 | 🩺 | `configuring-powered-knee-ankle-prosthesis-five-ambulation-modes__01` | EFSM | 主动膝踝一体假肢在五种 ambulation mode 下复用的四态阻抗控… | 丰富动作💎 / forced/aspect🔁 | 🟡 1 | 🟡 1 | 💎 3 | ⚪ 0 | **5.5** | 1/1 | 🟡 | · |
| 265 | 🏭 | `automated-liquid-filling-system-interactive-design-approach__01` | EFSM | 激光定位、视觉液位匹配与输送放行灌装控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | ⚪ 0 | **5.4** | 1/1 | 🟡 | · |
| 266 | 🏭 | `autonomous-forklift-navigation-cluttered-logistics-factory__01` | FSM | 工厂物流叉车走廊导航与避障控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟢 2 | **5.4** | 0/0 | 🟡 | · |
| 267 | 🅿️ | `design-and-implementation-of-car-parking-system-on-fpga__01` | EFSM | 停车场入口门禁与车位分配控制器 | — | 🟡 1 | 🟢 2 | 🟢 2 | ⚪ 0 | **5.4** | 1/1 | 🟡 | · |
| 268 | 🚆 | `prevention-of-accidents-using-automated-railway-crossing-system__01` | EFSM | 自动铁路道口门控与障碍检查控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟢 2 | **5.4** | 0/0 | 🟡 | · |
| 269 | 🚆 | `smart-railway-gate-level-crossing-system__01` | EFSM | 列车到达关闸与道路信号恢复控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | ⚪ 0 | **5.4** | 1/1 | 🟡 | · |
| 270 | 🚗 | `abs-fsm-brake-control__01` | FSM | 单轮 ABS 液压压力调节控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.3** | 1/1 | 🟡 | · |
| 271 | 🚦 | `conceptual-design-intelligent-traffic-light-controller__01` | FSM | 主干道/支路路口的智能交通灯相位控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.3** | 1/1 | 🟡 | · |
| 272 | 🏢 | `development-of-an-automatic-door-controller-for-a-smart-building__01` | EFSM | 滑动自动门控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.3** | 1/1 | 🟡 | · |
| 273 | 🏢 | `elevator-controller-based-on-ram-fpga__01` | EFSM | 两层电梯 LUT/RAM 门控与行驶控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.3** | 1/1 | 🟡 | · |
| 274 | ✈️ | `fuzzy-state-machine-spraying-uav-hybrid-power-system__01` | EFSM | 喷洒无人机燃料电池-电池混合供能能量管理控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.3** | 1/1 | 🟡 | · |
| 275 | 🏭 | `human-robot-collaborative-manufacturing-cell-learning-based-interaction__01` | FSM | 人机协作制造单元机械臂监督控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.3** | 1/1 | 🟡 | · |
| 276 | 🌡️ | `plc-based-automated-irrigation-system__01` | EFSM | 分区灌溉阀门与水泵控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.3** | 1/1 | 🟡 | · |
| 277 | 🌡️ | `plc-based-automatic-dam-shutter-control__01` | EFSM | 双浮球双闸门水位控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.3** | 1/1 | 🟡 | · |
| 278 | 🅿️ | `rule-based-controller-simulation-autonomous-parallel-parking-car-like-robot__01` | EFSM | 并联停车辅助控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.3** | 1/1 | 🟡 | · |
| 279 | 🅿️ | `seva3d-autonomous-vehicles-parking-simulator-three-dimensional-environment__01` | FSM | 并联泊车监督控制器 | 算术guard💎 | ⚪ 0 | 💎 3 | 🟢 2 | ⚪ 0 | **5.3** | 1/1 | 🟡 | · |
| 280 | 🚗 | `mlca-minimizing-lane-changes-autonomous-vehicles__01` | FSM | 自动驾驶车辆的 MLCA 换道决策控制器 | 算术guard💎 / 全局应急🌐 / forced/aspect🔁 | ⚪ 0 | 💎 3 | 🟡 1 | ⚪ 0 | **5.2** | 3/2 | 🟡 | · |
| 281 | ⚙️ | `plc-based-automatic-drawbridge-model__01` | EFSM | 船舶触发道闸与开桥顺序控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟡 1 | **5.2** | 1/1 | 🟡 | · |
| 282 | 🅿️ | `plc-based-multilevel-automatic-car-parking-system__01` | EFSM | 多层自动停车装置的旋转、升降与投放顺序控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟡 1 | **5.2** | 1/1 | 🟡 | · |
| 283 | 🩺 | `adaptive-ambulation-powered-knee-ankle-prosthesis__01` | EFSM | powered knee and ankle prosthesis 的 a… | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | ⚪ 0 | **5.1** | 0/1 | 🟡 | · |
| 284 | 🅿️ | `automated-multi-storied-car-parking-system-using-rfid__01` | EFSM | 多层立体停车场门禁与升降机调度控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | ⚪ 0 | **5.1** | 0/1 | 🟡 | · |
| 285 | 🏢 | `automated-secure-garage-system-license-plate-recognition__01` | EFSM | 授权车库门禁与滑门控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | ⚪ 0 | **5.1** | 0/1 | 🟡 | · |
| 286 | 🏢 | `floor-tiling-robotic-system__01` | FSM | 地砖铺设机器人中负责抓取、对位、放置与异常停机的机械臂控制器 | — | ⚪ 0 | 🟡 1 | 🟢 2 | 🟢 2 | **5.1** | 1/1 | 🟡 | · |
| 287 | 🅿️ | `intelligent-car-parking-management-system-on-fpga__01` | EFSM | 停车场引导入场、安全出场与车位计数控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | ⚪ 0 | **5.1** | 0/1 | 🟡 | · |
| 288 | 🚆 | `involuntary-railway-crossing-controller__01` | EFSM | 双红外道口栏杆门控控制器 | — | ⚪ 0 | 🟡 1 | 🟢 2 | 🟢 2 | **5.1** | 1/1 | 🟡 | · |
| 289 | 🌡️ | `self-regulating-water-management-system-using-programmable-logic-controller__01` | EFSM | 水库闸门 PLC 控制系统 | — | ⚪ 0 | 🟢 2 | 🟢 2 | ⚪ 0 | **5.0** | 2/2 | 🟡 | · |
| 290 | 🏭 | `automatic-control-three-dimensional-warehouse-based-on-plc__01` | EFSM | 三维自动仓库存取控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟡 1 | **4.9** | 1/0 | 🟡 | · |
| 291 | 🅿️ | `low-vertical-car-parking-automatic-control-system-using-programmable-logic-control__01` | EFSM | 六槽位立体停车原型的槽位定位与呼叫控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟡 1 | **4.9** | 1/0 | 🟡 | · |
| 292 | 🌡️ | `simulation-of-automatic-water-level-control-system-using-plc__01` | EFSM | 基于 S7-1200 的八级水位传感与泵启停控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟡 1 | **4.9** | 1/0 | 🟡 | · |
| 293 | 🅿️ | `design-of-automated-parking-system-using-plc__01` | EFSM | 起重机梳齿式立体停车存取车顺序控制器 | — | 🟡 1 | 🟢 2 | 🟢 2 | ⚪ 0 | **4.8** | 0/0 | 🟡 | · |
| 294 | 🅿️ | `fpga-based-smart-parking-management-system-with-real-time-slot-monitoring-and-entry-exit-detection__01` | EFSM | 停车场出入场与车位占用监测控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | ⚪ 0 | **4.8** | 0/0 | 🟡 | · |
| 295 | 🅿️ | `parking-monitoring-system-security-system-features__01` | EFSM | 私有停车位的空位检测、密码门禁与闸门开闭控制器 | 丰富动作💎 | ⚪ 0 | 🟢 2 | 💎 3 | ⚪ 0 | **4.8** | 0/0 | 🟡 | · |
| 296 | 🏢 | `application-of-plc-for-elevator-control-system__01` | EFSM |  PLC 电梯控制系统 | — | ⚪ 0 | 🟢 2 | 🟢 2 | ⚪ 0 | **4.7** | 1/2 | 🟡 | · |
| 297 | 🌡️ | `enhancing-sustainable-farming-practices-through-fpga-technology__01` | EFSM | 基于 FPGA 的土壤湿度灌溉泵控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | 🟡 1 | **4.6** | 0/0 | 🟡 | · |
| 298 | 🚆 | `automation-of-railway-gate-control-using-microcontroller__01` | FSM | 铁路平交道口自动栏杆控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | ⚪ 0 | **4.4** | 1/1 | 🟡 | · |
| 299 | 🚆 | `design-and-simulation-of-plc-iot-railway-level-crossing-gate-control-track-monitoring-system__01` | EFSM |  PLC 道口门控与轨道监测联动控制器 | — | ⚪ 0 | 🟡 1 | 🟢 2 | 🟡 1 | **4.3** | 1/1 | 🟡 | · |
| 300 | 🏢 | `sliding-garage-door-vfd-outseal-plc-remote__01` | EFSM |  PLC 车库滑门开闭控制器 | — | ⚪ 0 | 🟡 1 | 🟢 2 | 🟡 1 | **4.3** | 1/1 | 🟡 | · |
| 301 | 🚆 | `next-gen-railway-crossings-iot-safety-control__01` | FSM |  IoT 铁路平交口闸门控制器 | 丰富动作💎 | ⚪ 0 | 🟡 1 | 💎 3 | ⚪ 0 | **4.2** | 0/1 | 🟡 | · |
| 302 | 🚆 | `automatic-railway-gate-crossing-control-sensors-microcontroller__01` | EFSM | 双传感器铁路道口门控控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | ⚪ 0 | **4.1** | 0/1 | 🟡 | · |
| 303 | 🚆 | `plc-based-traffic-light-control-with-automatic-railway-gate-crossing__01` | EFSM |  PLC 道口栏杆与道路信号联动控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | ⚪ 0 | **4.1** | 0/1 | 🟡 | · |
| 304 | 🚆 | `fabrication-of-automatic-railway-gate-controller__01` | EFSM |  PIC 道口自动门控控制器 | 丰富动作💎 | ⚪ 0 | 🟡 1 | 💎 3 | ⚪ 0 | **3.9** | 0/0 | 🟡 | · |
| 305 | 🏢 | `fpga-application-of-home-security-code-using-verilog__01` | FSM | 四状态门禁密码锁控制器 | — | ⚪ 0 | ⚪ 0 | 🟢 2 | 🟢 2 | **3.9** | 0/1 | 🟡 | · |
| 306 | 🏢 | `finite-state-machine-untuk-pengendali-elevator-berbasis-fpga__01` | FSM | 基于 FPGA 的电梯运动状态控制器 | — | ⚪ 0 | 🟢 2 | 🟢 2 | ⚪ 0 | **3.8** | 0/0 | 🟡 | · |
| 307 | 🌡️ | `water-tank-level-controller-by-using-plc__01` | EFSM | PLC 水箱液位控制系统 | — | ⚪ 0 | 🟢 2 | 🟢 2 | ⚪ 0 | **3.8** | 0/0 | 🟡 | · |
| 308 | 🚆 | `automatic-railway-gate-crossing-control-using-plc__01` | FSM | 铁路平交口自动栏杆门控系统 | — | ⚪ 0 | 🟡 1 | 🟢 2 | 🟡 1 | **3.7** | 0/0 | 🟡 | · |
| 309 | 🚆 | `controlling-railway-gates-using-automata-based-intelligent-controller__01` | FSM | 铁路平交口自动栏杆门控控制器 | — | ⚪ 0 | 🟡 1 | 🟢 2 | 🟡 1 | **3.7** | 0/0 | 🟡 | · |
| 310 | 🚆 | `fpga-based-soc-for-railway-level-crossing-management-system__01` | FSM |  RF 驱动平交口预警与栏杆控制器 | 丰富动作💎 | ⚪ 0 | ⚪ 0 | 💎 3 | ⚪ 0 | **3.3** | 0/1 | ❌ | · |
| 311 | 🌡️ | `plc-based-water-level-control-system__01` | EFSM |  PLC 水位控制系统 | — | ⚪ 0 | 🟡 1 | 🟢 2 | ⚪ 0 | **3.2** | 0/1 | ❌ | · |
| 312 | 🏭 | `prototype-car-washing-automation-outseal-plc-modbus-hmi__01` | EFSM |  Outseal PLC 洗车线顺序控制器 | — | ⚪ 0 | 🟡 1 | 🟢 2 | ⚪ 0 | **3.2** | 0/1 | ❌ | · |
| 313 | 🌡️ | `automatic-water-level-and-pressure-control-system-prototype__01` | EFSM | PLC 水箱液位控制子系统中的泵启停逻辑 | — | ⚪ 0 | 🟡 1 | 🟢 2 | ⚪ 0 | **2.9** | 0/0 | ❌ | · |
| 314 | ⚙️ | `automation-of-drawbridge-model-using-plc__01` | EFSM | 船舶检测、路障封闭与桥体升降控制器 | — | ⚪ 0 | 🟡 1 | 🟢 2 | ⚪ 0 | **2.9** | 0/0 | ❌ | · |
| 315 | 🩺 | `reaching-and-grasping-glass-of-water-bci-controlled-humanoid-robot__01` | FSM |  BCI 人形机器人抓取与递送自主控制器 | — | ⚪ 0 | 🟡 1 | 🟢 2 | ⚪ 0 | **2.9** | 0/0 | ❌ | · |
| 316 | 🚆 | `automatic-railway-gate-control-system-using-plc__01` | EFSM | 铁路道口的栏杆门控与道路信号联动控制器 | — | ⚪ 0 | ⚪ 0 | 🟢 2 | ⚪ 0 | **2.3** | 0/1 | ❌ | · |
| 317 | 🚆 | `plc-based-railway-level-crossing-gate-control__01` | FSM | 铁路平交口的 PLC 道口栏杆控制器 | — | ⚪ 0 | ⚪ 0 | 🟢 2 | ⚪ 0 | **2.3** | 0/1 | ❌ | · |
| 318 | 🚆 | `design-and-construction-of-automatic-railway-crossing-gate-control-omron-cp1e-e30-sdra-plc__01` | EFSM | 基于 Omron PLC 的铁路道口栏杆门控控制器 | — | ⚪ 0 | ⚪ 0 | 🟢 2 | ⚪ 0 | **2.0** | 0/0 | ❌ | · |
| 319 | 🏢 | `design-and-implementation-of-efficient-elevator-control-system-using-fpga__01` | FSM | 三层电梯 FPGA 状态机控制器 | — | ⚪ 0 | ⚪ 0 | 🟢 2 | ⚪ 0 | **2.0** | 0/0 | ❌ | · |
| 320 | 🏭 | `development-of-automatic-packaging-system-using-plc-and-scada-for-industries__01` | EFSM | 包装产线前端的瓶清洗、灌装与封盖控制段 | — | ⚪ 0 | ⚪ 0 | 🟢 2 | ⚪ 0 | **2.0** | 0/0 | ❌ | · |
| 321 | 🏭 | `implementation-of-finite-state-automata-for-6-axis-robot-in-the-screwing-process__01` | FSM |  6 轴 EPSON 锁螺丝机器人顺序控制器 | — | ⚪ 0 | ⚪ 0 | 🟢 2 | ⚪ 0 | **2.0** | 0/0 | ❌ | · |
| 322 | 🏭 | `six-axis-robot-screwing-finite-state-automata__01` | FSM | 六轴机器人取刀、取螺钉与拧紧作业顺序控制器 | — | ⚪ 0 | ⚪ 0 | 🟢 2 | ⚪ 0 | **2.0** | 0/0 | ❌ | · |
| 323 | 🅿️ | `smart-car-parking-system-using-plc__01` | EFSM | 入口闸杆、车位占用显示与出口门禁控制器 | — | ⚪ 0 | ⚪ 0 | 🟢 2 | ⚪ 0 | **2.0** | 0/0 | ❌ | · |

