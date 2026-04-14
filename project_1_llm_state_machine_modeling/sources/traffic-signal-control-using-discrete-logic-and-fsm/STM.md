# Traffic Signal Control Using Discrete Logic and FSM - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双向路口交通灯控制器明确写成 `S1-S4` 四状态 FSM，并给出 `timer expiration + vehicle presence` 触发条件和触发器/逻辑门实现口径，是一条清晰的 `FSM + T1` 交通信号样本。

## 条目 1: Four-state two-way traffic-light controller

- 控制对象：道路交通信号控制领域的双向路口交通灯相位控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向双向交叉口的交通灯控制器，用 `S1-S4` 四状态表示南北向/东西向红黄绿相位，并用 `T1` 与 `V_NS / V_EW` 决定状态转移。
- 判断：算。对象是实际 traffic signal controller，而不是泛化综述；原文直接写出状态集合、传感器条件、定时触发和数字逻辑实现方式。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 3 行
> This research paper presents a novel approach to traffic signal control using discrete logic and finite state machines (FSM). The proposed system employs a discrete logic-based controller, designed to transition between various states based on real-time traffic conditions, such as vehicle count and pedestrian presence. The finite state machine model is used to represent the traffic signal cycles, incorporating multiple states (e.g., red, yellow, and green) and transitions triggered by specific input signals.

#### 摘录 B

- 出处：第 10 页，`3.3 FSM State Diagram for Traffic Signal Controller`，`paper_content.txt` 第 1340-1397 行
> S1 (Green for North-South, Red for East-West)
>
> S2 (Yellow for North-South, Red for East-West)
>
> S3 (Red for North-South, Green for East-West)
>
> S4 (Red for North-South, Yellow for East-West)
>
> The transitions between these states will depend on conditions such as timers (for time-based transitions) or sensor inputs (e.g., vehicle detection sensors). ... The state transitions depend on input conditions like timer expiration (T1) and vehicle presence sensors (VNS for North-South, VEW for East-West).

#### 摘录 C

- 出处：第 10-11 页，`State Encoding and Transition Equations / Hardware or Simulation Environments`，`paper_content.txt` 第 1399-1430 行
> To implement this FSM using discrete logic, we will first encode the four states using two binary variables: Q1 and Q0.
>
> ... The states Q1 and Q0 are stored using D flip-flops. The flip-flops update their state on the clock signal, which is triggered either by a timer or external sensor inputs.

### 2. 基于原文整理后的自然语言描述

The traffic-signal controller is a four-state FSM for a two-way intersection. Its state set is `S1` for North-South green / East-West red, `S2` for North-South yellow / East-West red, `S3` for North-South red / East-West green, and `S4` for North-South red / East-West yellow. The controller does not rotate phases blindly: the paper states that transitions depend on timer-based triggers and sensor inputs, with `T1` representing timer expiration and `VNS / VEW` representing vehicle presence on the two road directions. The machine is implemented as a concrete digital controller by encoding the state in two bits `Q1 / Q0` and storing them in `D` flip-flops driven by the timer or sensor events. This means the source preserves both the phase-level traffic semantics and the low-level transition mechanism, making it a clean `FSM + T1` sample instead of a loose narrative about traffic lights.

### 3. 逐句溯源

1. 句子 1：The traffic-signal controller is a four-state FSM for a two-way intersection.
   对应摘录：A, B
2. 句子 2：Its state set is `S1` for North-South green / East-West red, `S2` for North-South yellow / East-West red, `S3` for North-South red / East-West green, and `S4` for North-South red / East-West yellow.
   对应摘录：B
3. 句子 3：The controller does not rotate phases blindly: the paper states that transitions depend on timer-based triggers and sensor inputs, with `T1` representing timer expiration and `VNS / VEW` representing vehicle presence on the two road directions.
   对应摘录：A, B
4. 句子 4：The machine is implemented as a concrete digital controller by encoding the state in two bits `Q1 / Q0` and storing them in `D` flip-flops driven by the timer or sensor events.
   对应摘录：C
5. 句子 5：This means the source preserves both the phase-level traffic semantics and the low-level transition mechanism, making it a clean `FSM + T1` sample instead of a loose narrative about traffic lights.
   对应摘录：A, B, C
