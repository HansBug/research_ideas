# A finite-state machine-based control design for thermal and state-of-charge balancing of lithium iron phosphate battery using flyback converters - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把电池温度与 `SoC` 联合均衡控制写成 `3` 态 FSM，并给出 `SL,max / TL,max / Sav` 判定条件、状态驻留条件与 `80%` 充电前均衡目标，是一条细节很完整的电池管理样本。

## 条目 1: Three-state thermal/SoC balancing supervisor

- 控制对象：串联锂铁电池组的温度与荷电状态联合均衡控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个依据最大 `SoC` 偏差、最大温差和平均 `SoC` 在温度均衡与 `SoC` 均衡之间切换的电池管理状态机。
- 判断：算。对象是真实 BMS 里的离散模式管理器，不是单纯优化公式；原文给出了三态定义、阈值、状态持续条件和状态切换顺序。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Abstract
> To achieve the SoC and temperature balancing functions using the same balancing circuits, a finite-state machine control design decides on the operating mode, and a balancing strategy balances either temperature or SoC depending on the operating mode.

#### 摘录 B

- 出处：第 11 页，Section `4.2.1 Proposed finite-state machine-based control design`
> In the proposed finite-state machine-based control design, three states are defined.
>
> The operating state is decided based on the limiting criteria for the maximum SoC derivation (SL,max), the maximum temperature derivation (TL,max), and the average SoC (Sav) at each sampling instant.
>
> The Sllim, Tllim, and Thlim values are chosen as 0.1%, 0.5 °C, and 0.6 °C respectively.
>
> State 1 happens ... balancing circuits are off.
>
> State 2 ... the priority is to balance SoCs.
>
> State 3 ... the priority is to balance temperatures.

#### 摘录 C

- 出处：第 11-12 页，Section `4.2.1 / 4.2.2`
> State 2 stays until SoCL,max is less than or equal to the minimum allowed SoC imbalance (Sllim,) and Sav is greater than Sav,lim.
>
> State 3 happens when TL,max reaches its upper bound limit (Thlim,). State 3 stays until Sav is smaller than Sav,lim or TL,max is less than Tllim, meaning cell temperatures are balanced.
>
> the sampling time k happens every 1 s due to slower dynamic changes in thermal modeling compared to ones in electrical modeling.

#### 摘录 D

- 出处：第 14 页，Section `5.3 Proposed finite-state control design performance`
> In the beginning, the proposed controller operates on state 3 to balance temperature. After balancing temperatures, when Sav reaches Sav,lim, state 2 balances SoCs to ensure balanced SoCs before reaching the 80% charging limit.
>
> The proposed finite-state machine-based control improves the temperature balancing between cells during the charge without compromising the SoC balancing requirements which maximize the charging capacity.

### 2. 基于原文整理后的自然语言描述

The proposed battery-balancing controller is a three-state FSM that selects whether the balancing circuits should be off, should prioritize `SoC` equalization, or should prioritize temperature equalization. At every sampling instant, the supervisor evaluates three aggregate variables, namely the maximum `SoC` deviation `SL,max`, the maximum temperature deviation `TL,max`, and the average `SoC` `Sav`, and compares them against fixed limits `Sllim = 0.1%`, `Tllim = 0.5 °C`, and `Thlim = 0.6 °C`. `State 1` is the idle state in which both balancing factors are zero and the circuits are off once the cells are already within the required bounds or the pack has progressed beyond the average-SoC threshold. `State 2` enables only `SoC` balancing and remains active until `SL,max` is reduced to the allowed `0.1%` level while `Sav` stays above `Sav,lim`, whereas `State 3` enables only temperature balancing and remains active until either the pack average falls below `Sav,lim` or the temperature spread drops below the lower thermal bound. In the reported charging experiment, the controller starts from `State 3` to first reduce thermal imbalance, then switches to `State 2` once `Sav` reaches the prescribed threshold so that the cells arrive at the `80%` charging limit with balanced `SoC` and significantly improved temperature consistency.

### 3. 逐句溯源

1. 句子 1：The proposed battery-balancing controller is a three-state FSM that selects whether the balancing circuits should be off, should prioritize `SoC` equalization, or should prioritize temperature equalization.
   对应摘录：A, B
2. 句子 2：At every sampling instant, the supervisor evaluates three aggregate variables, namely the maximum `SoC` deviation `SL,max`, the maximum temperature deviation `TL,max`, and the average `SoC` `Sav`, and compares them against fixed limits `Sllim = 0.1%`, `Tllim = 0.5 °C`, and `Thlim = 0.6 °C`.
   对应摘录：B
3. 句子 3：`State 1` is the idle state in which both balancing factors are zero and the circuits are off once the cells are already within the required bounds or the pack has progressed beyond the average-SoC threshold.
   对应摘录：B
4. 句子 4：`State 2` enables only `SoC` balancing and remains active until `SL,max` is reduced to the allowed `0.1%` level while `Sav` stays above `Sav,lim`, whereas `State 3` enables only temperature balancing and remains active until either the pack average falls below `Sav,lim` or the temperature spread drops below the lower thermal bound.
   对应摘录：B, C
5. 句子 5：In the reported charging experiment, the controller starts from `State 3` to first reduce thermal imbalance, then switches to `State 2` once `Sav` reaches the prescribed threshold so that the cells arrive at the `80%` charging limit with balanced `SoC` and significantly improved temperature consistency.
   对应摘录：D
