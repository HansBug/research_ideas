# Hybrid Vehicle Supervisory Controller Development Process to Minimize Emissions and Fuel Consumption in EcoCAR 2 - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把插电式混合动力汽车的 `CD / CS / Performance / ICE Only` 高层模式和 `SOC / speed / component health / 2-second pedal hold` 触发条件写成了可追溯 supervisory controller。

## 条目 1: CD-CS-performance-ICE-only supervisory mode manager

- 控制对象：汽车与道路车辆控制领域的插电式混合动力汽车高层监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个 EcoCAR 2 插电式混合动力汽车的 supervisory controller，用 rule-based discrete modes 在 `Charge Depleting`、`Charge Sustaining`、`Performance`、`ICE Only` 和故障回退链之间切换前后桥动力系统。
- 判断：算。对象是真实车辆的高层 mode-selection controller，原文直接给出了模式集合、进入条件、分阶段 CS 流程和 fault fallback，而不是只谈 Simulink 开发流程。

### 1. 原文摘录

#### 摘录 A

- 出处：第 49-50 页，`Mode Selection Logic Structure`
> The UW team elected to use a set of discrete modes of operation in order to determine how to coordinate the torque requested from the two powertrain systems. Transitions between operation modes governed by a rule-based decision making process.

#### 摘录 B

- 出处：第 51 页，`3.3.1 Charge Depleting Mode`
> The vehicle operates in a Charge Depleting (CD) mode whenever the SOC is over a certain threshold. In this mode, the ICE is turned off and all torque requests are delivered by the eSystem.

#### 摘录 C

- 出处：第 52-53 页，`3.3.2 Charge Sustaining Mode`
> Once the vehicle drops below a lower limit to SOC, the HSC triggers a shift to Charge Sustaining (CS) mode.
>
> When the vehicle is at a stop, the ICE is turned off and the vehicle launches by using the eSystem to deliver the full driver torque request.
>
> Once a certain speed threshold is reached, the engine is started and torque from the iceSystem is slowly blended in as speed increases.
>
> Once the iceSystem is successfully blended in, the ICE Propulsion with Load Shifting phase begins.

#### 摘录 D

- 出处：第 54-55 页，`3.3.3 Additional Modes`
> Performance mode is used to enhance consumer acceptability ... To enter this mode the driver must press both the brake and accelerator pedal for two seconds, which causes the HSC to start the engine if it was off and begin evenly splitting torque between the two powertrains.
>
> The HSC has been programmed with an ICE Only mode, which is entered if the eSystem is ever evaluated to be offline.
>
> In a similar manner, if the iceSystem faults out and is evaluated to be Offline in the System Level diagnostics, the vehicle will switch to CD mode.

### 2. 基于原文整理后的自然语言描述

The EcoCAR 2 hybrid supervisory controller is organized around a discrete rule-based mode selector rather than a continuously optimized torque allocator. Its baseline branch starts in `Charge Depleting`, where the vehicle stays electric-only while battery `SOC` remains above a threshold, and then transitions to `Charge Sustaining` once the lower `SOC` limit is crossed. Inside `Charge Sustaining`, the controller itself contains a staged sub-sequence: at standstill the vehicle performs an electric launch, after a speed threshold the engine is started and blended in, and after the blend the controller enters an `ICE propulsion with load shifting` phase in which electric torque is used to move the engine toward preferred operating points. Beyond these main energy modes, the same supervisor adds `Performance mode`, entered only after the driver holds brake and accelerator together for `2 seconds`, and two limp-home branches: `ICE Only` when the electric system is offline and a fallback back to `CD` when the ICE system faults out. Because its transitions depend on `SOC`, vehicle speed, driver input timing, and component online/offline diagnostics, the case is a detailed automotive EFSM with local engineering timing.

### 3. 逐句溯源

1. 句子 1：The EcoCAR 2 hybrid supervisory controller is organized around a discrete rule-based mode selector rather than a continuously optimized torque allocator.
   对应摘录：A
2. 句子 2：Its baseline branch starts in `Charge Depleting`, where the vehicle stays electric-only while battery `SOC` remains above a threshold, and then transitions to `Charge Sustaining` once the lower `SOC` limit is crossed.
   对应摘录：B, C
3. 句子 3：Inside `Charge Sustaining`, the controller itself contains a staged sub-sequence: at standstill the vehicle performs an electric launch, after a speed threshold the engine is started and blended in, and after the blend the controller enters an `ICE propulsion with load shifting` phase in which electric torque is used to move the engine toward preferred operating points.
   对应摘录：C
4. 句子 4：Beyond these main energy modes, the same supervisor adds `Performance mode`, entered only after the driver holds brake and accelerator together for `2 seconds`, and two limp-home branches: `ICE Only` when the electric system is offline and a fallback back to `CD` when the ICE system faults out.
   对应摘录：D
5. 句子 5：Because its transitions depend on `SOC`, vehicle speed, driver input timing, and component online/offline diagnostics, the case is a detailed automotive EFSM with local engineering timing.
   对应摘录：A, B, C, D
