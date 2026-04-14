# Enhanced Hierarchical Control Framework of Microgrids With Efficiency Improvement and Thermal Management - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把微电网次级控制器明确写成四状态有限状态机，并给出由温度、轻载和谐波阈值触发的系统级切换规则，能够稳定支持双 A 的过程控制样本。

## 条目 1: Inverter-count secondary supervisor for microgrid efficiency and thermal balance

- 控制对象：过程与环境控制领域的微电网次级控制器，用于按热负荷、效率与谐波风险调整并联逆变器投入数量
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是微电网层级控制框架里的二级监督器，把 `S1-S4` 四个逆变器投入状态、温度阈值、轻载阈值和谐波阈值组织成一个负责系统级切换的有限状态机。
- 判断：算。对象是实际微电网控制器而不是纯功率电子分析模型，原文明确给出了状态集合、布尔触发条件、逆变器启停真值表，以及由 `Tc`、`Px < 50% Prated`、`THD` 驱动的切换规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6-8 页，`finite state machine-based secondary control strategy`，行 385-399
> To implement dynamic shift of operating points, finite state machine model [37] is adopted to model secondary controller, where the control signals as Boolean variables can be transmitted by low bandwidth communication. The model defines a finite set of states as well as how the system is shifted from one state to another when certain conditions happen. Fig. 7 shows the finite state machine-based secondary control strategy in islanded microgrids ... With the assumption that the microgrid consists of 4 inverters, it thus can be controlled at 4 operation states. Sx (x=1,2,3,4) indicates operation status, where x is operation number of inverters under each state.

#### 摘录 B

- 出处：第 7-8 页，`Active thermal management` 与 `efficiency improvement`，行 407-449
> The trigger condition is defined by discrete logic variables ... Tc is defined as critical temperature to trigger state transition. In this work, Tc is defined as 120°C. Once Te is higher than Tc, thermal status of each inverter Tx will be switched to 1 ... point B where output power is lower than 50% of rated power. To improve system efficiency, the number of inverters is decreased ... if Px is lower than 50% Prated, then load status variable δx is switched to 1 ... TABLE II ... S1 1 1 1 1 / S2 1 1 1 0 / S3 1 1 0 0 / S4 1 0 0 0.

#### 摘录 C

- 出处：第 9 页，`The proposed secondary control strategy in grid-connected microgrids`，行 528-560
> Fig. 10 shows operation principle of the proposed secondary control strategy ... Once the measured THD value from resonance detection block is higher than critical value, system status can be shifted to other states ... where HM is measured THD value, Hc is threshold to trigger secondary controller and Hx is Boolean variable that indicates harmonic status of each inverter. Then, power reference command is updated to assign output power of each inverter ...

### 2. 基于原文整理后的自然语言描述

The paper models the microgrid secondary controller as a finite-state supervisor with four discrete operating states `S1-S4`, where each state encodes how many of the four parallel inverters are active. State transitions are driven by Boolean status variables rather than informal heuristics: thermal management is triggered when any inverter temperature exceeds the critical threshold `Tc = 120°C`, and efficiency-oriented downshifting is triggered when inverter output power falls below `50%` of rated power. The truth table makes the state semantics explicit, ranging from `S1 = 1111` with all four inverters on down to `S4 = 1000` with only one inverter operating. In grid-connected mode, the same secondary layer also reacts to harmonic resonance by monitoring `THD`; once the measured harmonic index crosses its threshold, the controller shifts system status and updates inverter power references accordingly.

### 3. 逐句溯源

1. 句子 1：The paper models the microgrid secondary controller as a finite-state supervisor with four discrete operating states `S1-S4`, where each state encodes how many of the four parallel inverters are active.
   对应摘录：A
2. 句子 2：State transitions are driven by Boolean status variables rather than informal heuristics: thermal management is triggered when any inverter temperature exceeds the critical threshold `Tc = 120°C`, and efficiency-oriented downshifting is triggered when inverter output power falls below `50%` of rated power.
   对应摘录：B
3. 句子 3：The truth table makes the state semantics explicit, ranging from `S1 = 1111` with all four inverters on down to `S4 = 1000` with only one inverter operating.
   对应摘录：B
4. 句子 4：In grid-connected mode, the same secondary layer also reacts to harmonic resonance by monitoring `THD`; once the measured harmonic index crosses its threshold, the controller shifts system status and updates inverter power references accordingly.
   对应摘录：C
