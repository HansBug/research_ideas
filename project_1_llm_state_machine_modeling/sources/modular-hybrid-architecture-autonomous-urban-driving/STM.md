# A Modular, Hybrid System Architecture for Autonomous, Urban Driving - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 Sting Racing 的城市自动驾驶控制架构明确定义成 `Nested Hybrid Automata`，顶层和子层状态集合、交叉口子机、绕障子机以及 `Blocked` 的时间触发切换都直接写在正文里，是标准的 `HSM + T1` 双 A 样本。

## 条目 1: Nested Hybrid Automaton for Urban-Driving Situation Awareness

- 控制对象：汽车与道路车辆控制领域的 Sting Racing 城市自动驾驶模式、交叉口与绕障层次监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是 DARPA Urban Challenge 车辆的层次监督控制架构，用顶层城市驾驶模式和更深层的交叉口、绕障、停车子机共同驱动行为仲裁器与底层车辆控制。
- 判断：算。对象是实际自动驾驶车的 situational-awareness 与行为监督系统，原文不仅给出顶层模式，还给出 follow-lanes 子机、intersection 子机和 NHA 的形式化定义，并明确存在基于时间的转移。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-5 页，模式总览，`paper_content.txt` 第 98-110, 136-181 行
> “modes of operation”
>
> “Follow Lanes”
>
> “Handle Intersection”

#### 摘录 B

- 出处：第 4 页，`Follow Lanes` 细节，`paper_content.txt` 第 147-150 行
> “based primarily on time”

#### 摘录 C

- 出处：第 7-10 页，`Nested Hybrid Automata`，`paper_content.txt` 第 242-255, 333-360 行
> “nested hybrid automaton”
>
> “follow-lanes”
>
> “traverse-intersection”

### 2. 基于原文整理后的自然语言描述

The Sting Racing urban-driving supervisor is modeled as a nested hybrid automaton whose highest mission layer switches among the six major modes `Follow Lanes`, `Overtake Static Obstacle`, `U-Turn`, `Handle Intersection`, `Park`, and `Unpark`. Inside `Follow Lanes`, the controller further refines behavior into `Follow Lane`, `Overtake`, `Blocked`, and `Blind`, and the `Blocked` state does not merely describe a condition: it explicitly transitions to `Overtake` after a parameterized dwell time if the obstruction persists. The hierarchy continues at intersection level, where the machine cycles through `Approach`, `Find Queue Position`, `Wait For Turn`, `Go`, and `Done`, and the formal NHA section later rewrites the same logic as nested automata with states such as `approach-intersection`, `establish-precedence`, `wait-for-precedence`, `wait-for-oncoming-traffic`, and `traverse-intersection`. The `traverse-intersection` node itself contains a deeper submachine including `go`, `follow-points`, and `follow-lanes-in-intersection`, so the design is not a flat FSM but a true layered HSM. Each discrete state is mapped onward to action selections for the behavior-arbitration block, which means the hierarchy is directly tied to continuous steering and velocity commands rather than being a stand-alone planner sketch.

### 3. 逐句溯源

1. 句子 1：The Sting Racing urban-driving supervisor is modeled as a nested hybrid automaton whose highest mission layer switches among the six major modes `Follow Lanes`, `Overtake Static Obstacle`, `U-Turn`, `Handle Intersection`, `Park`, and `Unpark`.
   对应摘录：A, C；`paper_content.txt` 第 98-110, 242-255, 333-340 行。
2. 句子 2：Inside `Follow Lanes`, the controller further refines behavior into `Follow Lane`, `Overtake`, `Blocked`, and `Blind`, and the `Blocked` state does not merely describe a condition: it explicitly transitions to `Overtake` after a parameterized dwell time if the obstruction persists.
   对应摘录：A, B；`paper_content.txt` 第 136-153 行。
3. 句子 3：The hierarchy continues at intersection level, where the machine cycles through `Approach`, `Find Queue Position`, `Wait For Turn`, `Go`, and `Done`, and the formal NHA section later rewrites the same logic as nested automata with states such as `approach-intersection`, `establish-precedence`, `wait-for-precedence`, `wait-for-oncoming-traffic`, and `traverse-intersection`.
   对应摘录：A, C；`paper_content.txt` 第 169-176, 347-354 行。
4. 句子 4：The `traverse-intersection` node itself contains a deeper submachine including `go`, `follow-points`, and `follow-lanes-in-intersection`, so the design is not a flat FSM but a true layered HSM.
   对应摘录：C；`paper_content.txt` 第 354-360 行。
5. 句子 5：Each discrete state is mapped onward to action selections for the behavior-arbitration block, which means the hierarchy is directly tied to continuous steering and velocity commands rather than being a stand-alone planner sketch.
   对应摘录：C；`paper_content.txt` 第 242-255 行。
