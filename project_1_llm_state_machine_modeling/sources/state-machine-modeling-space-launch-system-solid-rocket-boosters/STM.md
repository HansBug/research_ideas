# State machine modeling of the Space Launch System Solid Rocket Boosters - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次、显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把左右 SRB 作为顶层状态、把 ignition 和 separation 作为关键 use case，并给出了 `t >= tHat` 与 `p <= pHat` 这类可直接建模的 transition condition。

## 条目 1: SRB ignition-and-separation hierarchical supervisor

- 控制对象：Space Launch System 固体火箭助推器的分层点火与分离监督逻辑
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次、显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是航天发射系统工程中的 booster supervisor，用于在左右助推器主状态下协调 avionics、FSS、SRM、TVC 和 separation 等子系统，并分析点火/分离的 nominal 与 off-nominal 序列。
- 判断：算。对象是真实火箭助推器控制与状态分析模型，不是抽象建模流程；原文清楚写出了顶层与子层状态关系、SRM 离散状态、点火异常情形，以及基于 mission time 和 pressure 的分离 guard。

### 1. 原文摘录

#### 摘录 A

- 出处：第 7 页，`Solid Rocket Booster state machine model`，`paper_content.txt` 第 227-240 行
> The left and right SRBs are modeled as states in the main model, with their subsystems modeled as substates. The SRB model includes the following systems: Avionics, Flight Safety System, Separation, Solid Rocket Motor, Thrust Vector Control ... Certain states are abstracted at a very high level into two states: nominal and off nominal.

#### 摘录 B

- 出处：第 9 页，`Solid Rocket Motor / Ignition`，`paper_content.txt` 第 269-273 行、第 287-291 行
> The SRM itself is abstracted into three states (off, ignited, and burnout) ... The ignition controllers and safe and arm devices are fully modeled in the state machine.
>
> Prior to launch the flight computers issue a command sequence to ignite the SRMs ... Aside from nominal ignition, there are two important off-nominal ignition cases: failure to ignite one or both SRMs, and the SRMs igniting with too much time separation between the ignition of each individual SRM.

#### 摘录 C

- 出处：第 10 页，`Separation`，`paper_content.txt` 第 296-307 行
> The Solid Rocket Boosters nominally separate from the Core Stage once two conditions have been met: t >= tHat ... p <= pHat ... The MET is represented using a clock object in Simulink ... In Stateflow, these conditions can be combined to form a transition condition as [(t >= tHat) && (p <= pHat)].

#### 摘录 D

- 出处：第 10 页，`Summary and Recommendations`，`paper_content.txt` 第 309-315 行
> Interesting separation cases include inadvertent separation and failure to separate after the boosters have burned out.
>
> The booster ignition and separation sequences were modeled and state analysis was run for both nominal and offnominal scenarios.

### 2. 基于原文整理后的自然语言描述

At the top level of the SLS model, the left and right solid rocket boosters are represented as main-model states, and each booster contains hierarchical substates for avionics, flight safety, separation, the solid rocket motor, and thrust-vector control. Inside this hierarchy, the solid rocket motor itself is abstracted into the three discrete states `off`, `ignited`, and `burnout`, and the ignition controllers together with the safe-and-arm devices are modeled explicitly rather than being hidden inside continuous dynamics. Before launch, the flight computers execute a booster ignition command sequence, and the paper highlights two off-nominal ignition situations that must be analyzed: failure to ignite one or both SRMs, and excessive temporal separation between left and right ignition. For nominal separation, the booster may separate only when mission elapsed time satisfies `t >= tHat` and motor pressure satisfies `p <= pHat`; these conditions are implemented as a Stateflow transition guard and then checked against inadvertent-separation and failure-to-separate scenarios.

### 3. 逐句溯源

1. 句子 1：At the top level of the SLS model, the left and right solid rocket boosters are represented as main-model states, and each booster contains hierarchical substates for avionics, flight safety, separation, the solid rocket motor, and thrust-vector control.
   对应摘录：A
2. 句子 2：Inside this hierarchy, the solid rocket motor itself is abstracted into the three discrete states `off`, `ignited`, and `burnout`, and the ignition controllers together with the safe-and-arm devices are modeled explicitly rather than being hidden inside continuous dynamics.
   对应摘录：B
3. 句子 3：Before launch, the flight computers execute a booster ignition command sequence, and the paper highlights two off-nominal ignition situations that must be analyzed: failure to ignite one or both SRMs, and excessive temporal separation between left and right ignition.
   对应摘录：B
4. 句子 4：For nominal separation, the booster may separate only when mission elapsed time satisfies `t >= tHat` and motor pressure satisfies `p <= pHat`; these conditions are implemented as a Stateflow transition guard and then checked against inadvertent-separation and failure-to-separate scenarios.
   对应摘录：C, D
