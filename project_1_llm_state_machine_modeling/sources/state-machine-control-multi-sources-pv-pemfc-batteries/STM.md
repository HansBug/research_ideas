# Advanced efficient energy management strategy based on state machine control for multi-sources PV-PEMFC-batteries system - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出 `SOC` 分段、`Pnet` 阈值、`15` 个状态与三种工况下的切换行为，是一条很完整的多源能量管理控制链。

## 条目 1: Fifteen-State SOC-Segmented PV-PEMFC-Battery EMS

- 控制对象：过程与环境控制领域的 PV-PEMFC-电池多源混合供能能量管理系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `SOC` 区间和净负载功率阈值进行状态切换的多源可再生能源管理控制器，用于在 PV、燃料电池和电池之间分配供能与充放电职责。
- 判断：算。对象是真实能源管理控制器，原文把状态数、状态分区、阈值区间和三类工况下的动作分配都写得非常具体。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，Introduction，`paper_content.txt` 第 142-151 行
> "15 states"

- 证据说明：该段直接说明 EMS 目标是 DC bus 稳压与负载跟随，并指出所提 SMC 方案采用 15 个状态。

#### 摘录 B

- 出处：第 8-9 页，`Suggested state machine energy management strategy`，`paper_content.txt` 第 347-360、390-408 行
> "three SOC intervals"

- 证据说明：原文把电池 `SOC` 划分为 `Low / Medium / High` 三个区间，并在每个区间内再按 `Pnet` 相对 `Pfcmin / Pfcopt / Pmid / Pfcmax` 的关系列出状态 1 到状态 15。

#### 摘录 C

- 出处：第 10-15 页，Cases 1-3，`paper_content.txt` 第 414-429、446-489、505-527 行
> "follows the reference load"

- 证据说明：三组工况分别说明当 `SOC` 低、中、高时，PEMFC 与电池怎样轮流承担“供负载 / 充电 / 放电 / 最小支撑”职责，并验证负载与 DC bus 跟踪效果。

### 2. 基于原文整理后的自然语言描述

The proposed energy-management controller is an extended state machine for a hybrid DC system that combines photovoltaic generation, a PEM fuel cell, and battery storage around two objectives: DC-bus stability and load following. Its state space is explicitly constructed from two groups of variables, namely the battery `SOC` interval (`Low`, `Medium`, `High`) and the net-power interval of `Pnet` relative to `Pfcmin`, `Pfcopt`, `Pmid`, and `Pfcmax`, which yields `15` discrete operating states. Each state assigns a reference fuel-cell power rather than leaving the coordination implicit, so the controller decides whether the PEMFC should only support the load, support the load while charging the battery, or stay near a lower support level while the battery discharges. In the low-SOC case, the PEMFC is biased toward both serving the demand and recharging the battery; in the medium-SOC case, battery charge and discharge alternate according to the current load interval; and in the high-SOC case, the battery is required to discharge while the PEMFC supplies only the needed support. The simulation section further shows that the total generated power tracks the reference load and the DC-bus voltage returns quickly to the `180 V` target after demand changes.

### 3. 逐句溯源

1. 句子 1：The proposed energy-management controller is an extended state machine for a hybrid DC system that combines photovoltaic generation, a PEM fuel cell, and battery storage around two objectives: DC-bus stability and load following.
   对应摘录：A
2. 句子 2：Its state space is explicitly constructed from two groups of variables, namely the battery `SOC` interval (`Low`, `Medium`, `High`) and the net-power interval of `Pnet` relative to `Pfcmin`, `Pfcopt`, `Pmid`, and `Pfcmax`, which yields `15` discrete operating states.
   对应摘录：A, B
3. 句子 3：Each state assigns a reference fuel-cell power rather than leaving the coordination implicit, so the controller decides whether the PEMFC should only support the load, support the load while charging the battery, or stay near a lower support level while the battery discharges.
   对应摘录：B
4. 句子 4：In the low-SOC case, the PEMFC is biased toward both serving the demand and recharging the battery; in the medium-SOC case, battery charge and discharge alternate according to the current load interval; and in the high-SOC case, the battery is required to discharge while the PEMFC supplies only the needed support.
   对应摘录：C
5. 句子 5：The simulation section further shows that the total generated power tracks the reference load and the DC-bus voltage returns quickly to the `180 V` target after demand changes.
   对应摘录：C
