# Control System Design of Water Filter Test Bench - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：公开版虽然省略了部分机密参数，但主状态、`Lobby1/Lobby2/Lobby3`、阀泵守卫和 stop 路径都写得清楚，足以形成高质量的测试台状态机样本。

## 条目 1: Water-filter test-bench main-state and valve supervisor

- 控制对象：水滤测试台的主状态、阀门与泵监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是通用控制与形式化建模领域的水滤测试台监督控制器，用主状态机约束测量模式和手动模式，再用组件状态机约束阀门、泵和 stop 条件。
- 判断：算。对象是真实测试台控制系统，原文不是泛泛讲 UML，而是给出主状态、`ΔP`/`multi-pass`/`manual control` 三类运行模式、自动 stop 路径和阀泵的具体 guard。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract，对主状态与 guard 的总体说明，`paper_content.txt` 第 46-63 行
> The control system was modelled in Unified Modelling Language’s state machine diagrams ...
>
> Main states of the control system were modelled first.
>
> These states defined which of the components could be actuated during each state and which sensor/state data would be shown to the user by the Human-machine interface.
>
> Components’ state machine diagrams were modelled after this.
>
> These diagrams defined every possible scenario where a certain component could be used.
>
> The actuations were possible only if the set conditions for the action were true. These guards were set for the state changes so that the system would be safe to use, and unwanted action wouldn’t occur.

#### 摘录 B

- 出处：第 34-37 页，`Main states`，`paper_content.txt` 第 1088-1160 行
> The system is divided into 4 main states.
>
> Options are two different measuring states ISO 16689 and ISO 3968 and a manual control state.
>
> Route E.1 is a stop feature ... E.1 can be entered from every state of the system.
>
> ΔP Measurement has only one state and it is called Lobby1 ...
>
> When one wants to start the multi-pass test, pumps A.PM.1, B.PM.1, B.PM.3 and A.PM.2 has to be on, sensor pumps must be off, valve A.V.2 must be right, valve B.V.12 must be left and bypass must be active.
>
> Working principle of the manual control system is simple ... lobby3 is also entered when automatic stop1 or safety stop2 state becomes active.

#### 摘录 C

- 出处：第 38-40 页，`Valves`，`paper_content.txt` 第 1188-1214 行
> A.V.1 valve is a 3-way valve. Its initial state is left.
>
> It can be turned to right in manual control lobby 3 if reservoir B.W.1 is not full and a button A.V.1 is pressed.
>
> It will be turned right when the multi-pass test is started ...
>
> Valve A.V.1 can be turned to left in manual control lobby3 by pressing the A.V.1 button.
>
> Control valve is turned back to left when multi-pass measurement or ΔP measurement is pressed in the normal state, multi-pass test (TEST2) is finished or if reservoir of B.W.1 sensor is full.

### 2. 基于原文整理后的自然语言描述

The water-filter test bench is organized as a hierarchical supervisor that starts from a normal state and can move into a `ΔP Measurement` lobby, a `Multi-pass Measurement` lobby, or a `Manual Control` lobby, while a global stop route can be entered from every state when limits are violated or emergency stop is pressed. Entering `Lobby1` prepares the valves for `ΔP` measurement and exposes only the pump, throttle-valve, cleaning, and bypass actions relevant to that test mode. Entering `Lobby2` prepares the multi-pass configuration, and the actual test can start only when a long guard over pumps, sensor pumps, valve directions, and bypass status is satisfied. If `automatic stop1` or `safety stop2` becomes active, the system moves into the manual-control side so the operator can diagnose the situation and recover by directly actuating valves while unsafe pump usage remains blocked. At the component level, valves such as `A.V.1` are given their own state machines with explicit initial states and guard-controlled left/right transitions, which makes the whole controller a genuine HSM rather than a flat list of operating procedures.

### 3. 逐句溯源

1. 句子 1：The water-filter test bench is organized as a hierarchical supervisor that starts from a normal state and can move into a `ΔP Measurement` lobby, a `Multi-pass Measurement` lobby, or a `Manual Control` lobby, while a global stop route can be entered from every state when limits are violated or emergency stop is pressed.
   对应摘录：A, B
2. 句子 2：Entering `Lobby1` prepares the valves for `ΔP` measurement and exposes only the pump, throttle-valve, cleaning, and bypass actions relevant to that test mode.
   对应摘录：B
3. 句子 3：Entering `Lobby2` prepares the multi-pass configuration, and the actual test can start only when a long guard over pumps, sensor pumps, valve directions, and bypass status is satisfied.
   对应摘录：B
4. 句子 4：If `automatic stop1` or `safety stop2` becomes active, the system moves into the manual-control side so the operator can diagnose the situation and recover by directly actuating valves while unsafe pump usage remains blocked.
   对应摘录：B
5. 句子 5：At the component level, valves such as `A.V.1` are given their own state machines with explicit initial states and guard-controlled left/right transitions, which makes the whole controller a genuine HSM rather than a flat list of operating procedures.
   对应摘录：A, C
