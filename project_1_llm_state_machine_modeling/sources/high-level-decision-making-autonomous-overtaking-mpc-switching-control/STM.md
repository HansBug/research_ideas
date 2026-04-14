# High-level decision-making for autonomous overtaking: An MPC-based switching control approach - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双向道路自动超车高层决策抽象成 switched system，离散模式 `following lane / slowdown / stop / overtaking`、状态约束、模式切换限制和 receding-horizon 决策过程都写得很完整，是正式期刊里的双 A 样本。

## 条目 1: Four-Mode MPC Switching Supervisor for Autonomous Overtaking

- 控制对象：汽车与道路车辆控制领域的双向道路自动超车跟车、减速、停车与超车切换监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是面向双向乡村道路自动超车的高层决策器，用四个离散决策模式和 MPC 预测优化持续决定当前应跟车、减速、停车等待还是发起超车。
- 判断：算。对象是实际自动驾驶车辆的 overtaking decision maker，原文明确给出离散模式集合、模式对应的 switched-system 语义、成本函数驱动的切换逻辑和模式转移约束，而不是只给出轨迹优化结果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract / Introduction，`paper_content.txt` 第 22-39, 60-66 行
> “switched system”
>
> “Following lane”
>
> “Overtaking”

#### 摘录 B

- 出处：第 5-6 页，`2.4 Autonomous overtaking process description`，`paper_content.txt` 第 413-498 行
> “q ∈ {1, −1, −2, 2}”
>
> “stop”

#### 摘录 C

- 出处：第 7 页，`3.1-3.2`，`paper_content.txt` 第 548-683 行
> “switching modes”
>
> “Algorithm 1”

### 2. 基于原文整理后的自然语言描述

The overtaking decision maker abstracts the autonomous vehicle as a switched system whose high-level mode directly determines the control inputs passed to the lower planning layer. The discrete decision variable is explicitly defined as `q ∈ {1, -1, -2, 2}`, corresponding to `following lane`, `slowdown`, `stop`, and `overtaking`, so the supervisor can initiate, hold, postpone, or resume an overtake instead of only choosing a path once. The paper then explains the decision logic in sequence: normal lane following remains optimal while the target-speed error is small, slowdown is selected when the leading vehicle closes in but the opposite lane is still unsafe, stop is chosen when oncoming traffic blocks the overtaking opportunity, and overtaking is reactivated once the opposite lane becomes available. When the overtake is in progress and the oncoming-traffic distance grows again, the optimal decision switches back to lane following so that the vehicle returns to the original lane after passing. This whole mode sequence is repeatedly recomputed by an MPC problem with state, input, and elliptical safety constraints, so the discrete supervisor is tightly coupled to continuous vehicle evolution without depending on hand-written one-shot rules.

### 3. 逐句溯源

1. 句子 1：The overtaking decision maker abstracts the autonomous vehicle as a switched system whose high-level mode directly determines the control inputs passed to the lower planning layer.
   对应摘录：A, C；`paper_content.txt` 第 22-35, 323-329, 512-518 行。
2. 句子 2：The discrete decision variable is explicitly defined as `q ∈ {1, -1, -2, 2}`, corresponding to `following lane`, `slowdown`, `stop`, and `overtaking`, so the supervisor can initiate, hold, postpone, or resume an overtake instead of only choosing a path once.
   对应摘录：B；`paper_content.txt` 第 413-428 行。
3. 句子 3：The paper then explains the decision logic in sequence: normal lane following remains optimal while the target-speed error is small, slowdown is selected when the leading vehicle closes in but the opposite lane is still unsafe, stop is chosen when oncoming traffic blocks the overtaking opportunity, and overtaking is reactivated once the opposite lane becomes available.
   对应摘录：B；`paper_content.txt` 第 452-483 行。
4. 句子 4：When the overtake is in progress and the oncoming-traffic distance grows again, the optimal decision switches back to lane following so that the vehicle returns to the original lane after passing.
   对应摘录：B；`paper_content.txt` 第 483-497 行。
5. 句子 5：This whole mode sequence is repeatedly recomputed by an MPC problem with state, input, and elliptical safety constraints, so the discrete supervisor is tightly coupled to continuous vehicle evolution without depending on hand-written one-shot rules.
   对应摘录：A, C；`paper_content.txt` 第 30-39, 548-683 行。
