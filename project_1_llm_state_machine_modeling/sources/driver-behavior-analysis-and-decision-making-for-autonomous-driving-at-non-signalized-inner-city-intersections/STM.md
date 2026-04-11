# Driver Behavior Analysis and Decision-Making for Autonomous Driving at Non-Signalized Inner City Intersections - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文第 4 章把非信号 T 路口自动驾驶决策明确实现为 DES 状态机，给出相关车辆角色、事件表、11 个状态、分区阈值、死锁解析与目标速度，足以形成高质量交通决策控制样本。

## 条目 1: T-Intersection Discrete-Event Decision-Making Controller

- 控制对象：无信号 T 型城市路口的自动驾驶决策控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是汽车与道路车辆控制领域的交叉路口决策器，围绕 P-V、Y-V、B-V、L-V 四类相关车、六个距离分区和 11 个 DES 状态来控制自动车在无信号 T 路口的让行、通行与死锁解消。
- 判断：算。对象是实际自动驾驶决策控制器而不是单纯行为分析框架；正文明确给出了相关车辆分类、事件定义、状态图、速度参数和死锁处理策略。

### 1. 原文摘录

#### 摘录 A

- 出处：第 127-128 页，Section 4.2.1，`paper_content.txt` 第 4329-4395 行
> To model that concept, a traffic light is assigned to each of them and the A-V only drives if all lights are green. In total there are four relevant vehicles: The vehicle that has priority (P-V) ... The vehicle that has to yield (Y-V) ... The vehicle that potentially blocks the intersection (B-V) ... The vehicle that leads (L-V) ... the A-V is presumed to not know the turning direction of a C-V while it is further than 10m away from the start of the intersection.

#### 摘录 B

- 出处：第 139-145 页，Section 4.2.5-4.2.6，`paper_content.txt` 第 4750-4822 行，第 5001-5057 行
> Table 4.1 Base events ... Table 4.2 Events ... e1,p,I = eb1 or eb2 ... e1,y = not eb5 and (eb6 or eb7 or eb8 or eb9) ... e4 = eb15 deadlock possible ... The decision-making model itself consists of 11 states ... zones 2 to 5 each have at least an offensive and a defensive state ... States s21, s31, s41 and s51 are the states in which the A-V shows offensive behavior ... states s22, s32, s42 and s52 are the defensive states.

#### 摘录 C

- 出处：第 146-148 页，Section 4.2.6，`paper_content.txt` 第 5068-5139 行
> Target velocities vt in ms-1 for the states of the DES ... vt straight = 8.3, 6.0, 7.5, 6.0, 6.5 ... vt turning = 8.3, 6.0, 6.0, 6.0, 4.0 ... the model changes from offensive to defensive behavior ... if an emergency stop is still possible ... state s53 is reached from s52 either if no deadlock is possible and all four lights are green or if a deadlock occurred and can be solved by the A-V ... As soon as the A-V detects a deadlock, it attempts to solve it by starting to drive.

### 2. 基于原文整理后的自然语言描述

The controller models non-signalized T-intersection driving as a discrete-event state machine in which the autonomous vehicle evaluates four relevant traffic roles: a priority vehicle on the right (`P-V`), a yielding vehicle on the left (`Y-V`), a blocking vehicle on the exit lane (`B-V`), and a leading vehicle directly ahead (`L-V`). It assumes worst-case turning directions for other vehicles until they are within 10 m of the intersection and then derives base events and composite events that determine whether each relevant vehicle effectively gives a green light. The approach and crossing are divided into six distance-based zones, and the main controller uses 11 states: free driving in zones 1 and 6 plus offensive and defensive variants in zones 2 to 5, with `s53` representing offensive driving after waiting in zone 5. In zones 2 and 3 the decision is mainly driven by the priority vehicle, while in zone 4 all four lights are reevaluated every time step and the machine may switch between offensive and defensive behavior if emergency stopping is still possible. The paper also fixes target velocities for straight and turning cases, defines a two-second waiting threshold for yielding by the priority vehicle, and includes explicit deadlock detection and resolution so that the vehicle can decide to start driving when all three participants are stopped and the exit is clear.

### 3. 逐句溯源

1. 句子 1：The controller models non-signalized T-intersection driving as a discrete-event state machine in which the autonomous vehicle evaluates four relevant traffic roles: a priority vehicle on the right (`P-V`), a yielding vehicle on the left (`Y-V`), a blocking vehicle on the exit lane (`B-V`), and a leading vehicle directly ahead (`L-V`).
   对应摘录：A；`paper_content.txt` 第 4329-4369 行。
2. 句子 2：It assumes worst-case turning directions for other vehicles until they are within 10 m of the intersection and then derives base events and composite events that determine whether each relevant vehicle effectively gives a green light.
   对应摘录：A, B；`paper_content.txt` 第 4386-4395 行，4750-4822 行。
3. 句子 3：The approach and crossing are divided into six distance-based zones, and the main controller uses 11 states: free driving in zones 1 and 6 plus offensive and defensive variants in zones 2 to 5, with `s53` representing offensive driving after waiting in zone 5.
   对应摘录：B；`paper_content.txt` 第 5001-5057 行。
4. 句子 4：In zones 2 and 3 the decision is mainly driven by the priority vehicle, while in zone 4 all four lights are reevaluated every time step and the machine may switch between offensive and defensive behavior if emergency stopping is still possible.
   对应摘录：B, C；`paper_content.txt` 第 4811-4822 行，5080-5121 行。
5. 句子 5：The paper also fixes target velocities for straight and turning cases, defines a two-second waiting threshold for yielding by the priority vehicle, and includes explicit deadlock detection and resolution so that the vehicle can decide to start driving when all three participants are stopped and the exit is clear.
   对应摘录：B, C；`paper_content.txt` 第 4828-4850 行，5068-5074 行，5130-5139 行。
