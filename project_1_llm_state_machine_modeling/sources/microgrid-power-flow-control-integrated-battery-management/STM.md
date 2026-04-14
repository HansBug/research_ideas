# Microgrid Power Flow Control with Integrated Battery Management Functions - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把孤网微电网的 `Mode 1-4` 功率流控制、发电机投入/退出、负载切除和电池 `SOC` 滞回切换明确组织成一条四模式监督控制链。

## 条目 1: SOC-Hysteresis Four-Mode Microgrid Power-Flow Supervisor

- 控制对象：过程与环境控制领域的孤网微电网功率流与电池管理监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于孤网微电网的高层功率流监督器，用 `SOC`、发电机保护和关键/非关键负载切除条件在四种运行模式之间切换。
- 判断：算。对象是真实微电网控制器而不是单独的电池充电算法；原文明确给出 `Mode 1-4` 的状态语义、每种模式下 `BESS / PV / generator / loads` 的职责，以及由 `SOC` 滞回阈值和保护事件驱动的状态转移。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Table I `Microgrid operation modes`，行 164-192
> In Mode 1, the generator is turned off. The full load is supplied since the battery SOC is at a relatively high level. The BESS regulates voltage and frequency ... Mode 1 V/f regulation ... full. ... In Mode 2, the battery SOC is at a relatively low SOC level. The generator becomes the master unit to regulate voltage and frequency ... The BESS in Mode 2 acts as a grid-feeding unit ... The only difference between Mode 3 and Mode 2 is that all the non-critical loads are shed in Mode 3. Mode 4 represents the mode where all the units are shut down and disconnected.

#### 摘录 B

- 出处：第 4 页，Section `C. Smooth Mode Transitions`，行 1337-1359
> The state machine for the microgrid power flow controller is depicted in Fig. 6 and all the operation modes correspond to Table I. Battery SOC is the main trigger for state transitions. To ensure smooth state transition, SOC settings with hysteresis are applied to transitions between Mode 1 and Mode 2. ... The similar hysteresis settings LoadSOC lb and LoadSOC ub are applied to transitions between Mode 2 and Mode 3. ... Besides triggered by SOC, Mode 1 can be transitioned to from Mode 2 or Mode 3 whenever the generator is tripped by the overcurrent/undercurrent protection. ... Mode 4, in which the whole microgrid is shut down, can only be entered from Mode 3 when battery SOC is below SOC min.

### 2. 基于原文整理后的自然语言描述

The islanded microgrid is supervised by a four-mode EFSM whose states correspond to the operation modes in Table I. In `Mode 1`, the generator is offline while the battery energy storage system regulates voltage and frequency and the full load remains connected; in `Mode 2`, the generator becomes the grid-forming master and the battery switches to grid-feeding dispatch; in `Mode 3`, this generator-connected structure is preserved but non-critical loads are shed; and in `Mode 4`, all units are shut down and disconnected. The main guards for state transitions are battery `SOC` thresholds rather than ad hoc operator choices. The transition logic is explicit about hysteresis, using `GenSOC_lb / GenSOC_ub` between `Mode 1` and `Mode 2` and `LoadSOC_lb / LoadSOC_ub` between `Mode 2` and `Mode 3` to avoid chattering. The controller also includes exception transitions: a generator overcurrent or undercurrent trip pushes the system back toward `Mode 1`, while `Mode 4` is only reachable from `Mode 3` when the battery falls below `SOC_min`.

### 3. 逐句溯源

1. 句子 1：The islanded microgrid is supervised by a four-mode EFSM whose states correspond to the operation modes in Table I.
   对应摘录：A, B
2. 句子 2：In `Mode 1`, the generator is offline while the battery energy storage system regulates voltage and frequency and the full load remains connected; in `Mode 2`, the generator becomes the grid-forming master and the battery switches to grid-feeding dispatch; in `Mode 3`, this generator-connected structure is preserved but non-critical loads are shed; and in `Mode 4`, all units are shut down and disconnected.
   对应摘录：A
3. 句子 3：The main guards for state transitions are battery `SOC` thresholds rather than ad hoc operator choices.
   对应摘录：B
4. 句子 4：The transition logic is explicit about hysteresis, using `GenSOC_lb / GenSOC_ub` between `Mode 1` and `Mode 2` and `LoadSOC_lb / LoadSOC_ub` between `Mode 2` and `Mode 3` to avoid chattering.
   对应摘录：B
5. 句子 5：The controller also includes exception transitions: a generator overcurrent or undercurrent trip pushes the system back toward `Mode 1`, while `Mode 4` is only reachable from `Mode 3` when the battery falls below `SOC_min`.
   对应摘录：B
