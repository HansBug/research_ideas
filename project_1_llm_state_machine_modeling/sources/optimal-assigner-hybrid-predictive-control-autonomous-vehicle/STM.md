# Optimal Assigner Decisions in a Hybrid Predictive Control of an Autonomous Vehicle in Public Traffic - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 highway maneuver assigner 写成含多 FSM 的混合预测控制上层模块，离散机动集合、lane-specific maneuver states、强制机动 guard 和下层 PTG 的耦合都足够明确，是很稳定的 `EFSM + T0` 样本。

## 条目 1: Hybrid Predictive Assigner for Highway Maneuver Selection

- 控制对象：汽车与道路车辆控制领域的三车道自动驾驶正常跟踪、跟车、领车与强制换道 assigner
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个把离散机动 assigner 与混合预测轨迹引导器耦合的高速公路行为决策器，用三车道机动状态和权重变量来决定当前车道应保持正常跟踪、跟车、领车还是触发换道。
- 判断：算。对象是实际自动驾驶车辆的高层 maneuver planner，原文明确把机动集合组织成 FSM、列出 highway case 的状态表，并给出速度容差违反时的强制机动条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-3 页，控制框架与混合系统建模，`paper_content.txt` 第 67-78, 145-174, 182-210 行
> “finite state machines”
>
> “highway case”

#### 摘录 B

- 出处：第 3 页，机动定义，`paper_content.txt` 第 217-235 行
> “normal tracking”
>
> “following”
>
> “leading”

#### 摘录 C

- 出处：第 7 页，`TABLE I. DISCRETE MANEUVER STATES` 与强制机动条件，`paper_content.txt` 第 482-549 行
> “Lane 1”
>
> “forced maneuver”

### 2. 基于原文整理后的自然语言描述

The assigner is modeled as the discrete decision layer of a hierarchical hybrid predictive-control framework, where pre-defined FSMs provide maneuver candidates and the lower predictive-trajectory-guidance system optimizes among them. For the highway scenario, the paper defines three lane-local reference maneuvers, `normal tracking`, `following`, and `leading`, and treats lane change as a maneuver obtained by switching the reference lane from the current lane to another one. The top-level highway FSM can therefore jump among lane-specific maneuver states, and the paper makes those states explicit in a nine-entry table covering `normal/following/leading` on lanes 1, 2, and 3. The assigner does not simply apply fixed rules: if the chosen lane keeps the vehicle trapped in following or leading so that the target speed leaves the tolerated band around `vref`, a forced maneuver is inserted by driving the weight variable of a better lane candidate toward one. Priority rules then resolve which forced maneuver wins, with the default preference order lane 2, then lane 3, then lane 1, so the discrete machine remains tied to global driving policy instead of only local obstacle reaction.

### 3. 逐句溯源

1. 句子 1：The assigner is modeled as the discrete decision layer of a hierarchical hybrid predictive-control framework, where pre-defined FSMs provide maneuver candidates and the lower predictive-trajectory-guidance system optimizes among them.
   对应摘录：A；`paper_content.txt` 第 145-174 行。
2. 句子 2：For the highway scenario, the paper defines three lane-local reference maneuvers, `normal tracking`, `following`, and `leading`, and treats lane change as a maneuver obtained by switching the reference lane from the current lane to another one.
   对应摘录：B；`paper_content.txt` 第 217-235 行。
3. 句子 3：The top-level highway FSM can therefore jump among lane-specific maneuver states, and the paper makes those states explicit in a nine-entry table covering `normal/following/leading` on lanes 1, 2, and 3.
   对应摘录：A, C；`paper_content.txt` 第 196-205, 482-499 行。
4. 句子 4：The assigner does not simply apply fixed rules: if the chosen lane keeps the vehicle trapped in following or leading so that the target speed leaves the tolerated band around `vref`, a forced maneuver is inserted by driving the weight variable of a better lane candidate toward one.
   对应摘录：C；`paper_content.txt` 第 518-541 行。
5. 句子 5：Priority rules then resolve which forced maneuver wins, with the default preference order lane 2, then lane 3, then lane 1, so the discrete machine remains tied to global driving policy instead of only local obstacle reaction.
   对应摘录：C；`paper_content.txt` 第 542-549 行。
