# Real Time Automation and Ratio Control Using PLC & SCADA in Industry 4.0 - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把化工 mixer 的配比/液位/定时排料与后段分拣-灌装-封盖-贴标输送线接成一条长控制链，时间和分支条件都很具体。

## 条目 1: Mixer Ratio Selection and Timed Assembly-Line Supervisor

- 控制对象：化工厂中 PLC/SCADA 配比混合与后段灌装装配线的综合控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个化工过程与装配线一体化控制器，先根据 HMI 配方控制两路原料混合，再把成品送入按容器类型分支的输送、灌装、封盖和贴标流程。
- 判断：算。对象是实际工业控制系统，原文明确给出了 `LOW / MEDIUM / HIGH` 与 `3:4 / 2:1 / 2:5` 配方选择、`0.3 / 0.6 / 0.8 sec` 开阀时间、`20 / 40 / 55 sec` 混合驻留时间，以及 `S2-S6` 停带与恢复逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-3 页，`Abstract / Prototype of Simulated Chemical Process Plant`，`paper_content.txt` 第 7-21 行、第 88-90 行
> this paper proposes a SCADA and PLC system to control the ratio control division and the assembly line division inside the chemical plant ... the assembly line division is further divided into sorting stage, filling stage and the auxiliary stage, which includes the capping unit, labelling unit and then the storage ... we have taken the predefined levels (low, medium, high) and ratios (3:4, 2:1, 2:5).
>
> The plant has two stages: the first stage depicts the formation of products with raw materials and the second stage depicts the assembly line operation in supervisory control and data acquisition (SCADA) system.

#### 摘录 B

- 出处：第 8-9 页，`3 Operation`，`paper_content.txt` 第 227-252 行
> The first step is to check whether the safety sensor is ON or OFF ... The level to be decided from LOW, MEDIUM, HIGH. The predefined ratios (CH1:CH2) are 3:4, 2:1, 2:5 ... After selection of level and ratio the pumps and blender motor ON and the CH1 & CH2 start filling into the MIXER through control valves CV1 & CV2.
>
> LOW & 3:4 = [(CV1 × 30) + (CV2 × 40)] × 0.3 sec ... MEDIUM & 2:1 = [(CV1 × 70) + (CV2 × 35)] × 0.6 sec ... HIGH & 2:5 = [(CV1 × 20) + (CV2 × 50)] × 0.8 sec ... LS3 turns ON to indicate LOW level and remains ON for 20 sec ... LS3 & LS2 turn ON to indicate MEDIUM level and remain ON for 40 sec ... LS3, LS2 & LS1 turn ON to indicate HIGH level and remain ON for 55 sec ... There is a safety sensor ... to prevent the overflowing of the composition.

#### 摘录 C

- 出处：第 9-14 页，`3 Operation / 4.2 Assembly Line Division`，`paper_content.txt` 第 253-305 行、第 328-355 行
> when any of the other sensors (S2, S3, S4, S5, S6) get HIGH ... the motor stops. The stopping time depends upon the timer ... After the timer gets OFF, normal running process of conveyor system is resumed.
>
> When a big metallic container is moving on the belt, both capacitive PR sensors SS1 & SS2 are HIGH ... the inductive PR sensor gets HIGH ... But when the small non-metallic container is moving on the conveyor belt, SS1 turns HIGH and SS2 remains LOW ... S2 ... valve (V1) open and both containers got filled with tank1 composition up to one-third level ... S3 ... valve (V2) open ... up to two-third level ... S4 ... big size metallic type ... valve (V3) open ... up to the brim or 99% level ... small size non-metallic type ... the solenoid valve doesn’t open ... S5 ... capping unit places caps ... S6 ... labelling unit places labels ... after all the processes, here comes the storage.

### 2. 基于原文整理后的自然语言描述

The chemical-plant supervisor starts by checking the mixer safety sensor and then lets the HMI choose a production level of `LOW`, `MEDIUM`, or `HIGH` together with a ratio of `3:4`, `2:1`, or `2:5` for streams `CH1` and `CH2`. According to that selection, the PLC opens `CV1` and `CV2` for recipe-specific durations such as `0.3 sec`, `0.6 sec`, or `0.8 sec`, drives the blender, and keeps the level-sensor pattern active for `20 sec`, `40 sec`, or `55 sec` before routing the finished mixture into `tank2`, `tank1`, or `tank3`. Downstream, the conveyor normally runs until sensors `S2-S6` detect a container, at which point the motor stops for the timer associated with filling, capping, or labelling and restarts after the timer expires. The container path then branches by size and material: both container types receive the first two fills, only large metallic containers open `V3` for the final brim fill, and afterward both types pass through `S5` capping, `S6` labelling, and storage.

### 3. 逐句溯源

1. 句子 1：The chemical-plant supervisor starts by checking the mixer safety sensor and then lets the HMI choose a production level of `LOW`, `MEDIUM`, or `HIGH` together with a ratio of `3:4`, `2:1`, or `2:5` for streams `CH1` and `CH2`.
   对应摘录：A, B
2. 句子 2：According to that selection, the PLC opens `CV1` and `CV2` for recipe-specific durations such as `0.3 sec`, `0.6 sec`, or `0.8 sec`, drives the blender, and keeps the level-sensor pattern active for `20 sec`, `40 sec`, or `55 sec` before routing the finished mixture into `tank2`, `tank1`, or `tank3`.
   对应摘录：B
3. 句子 3：Downstream, the conveyor normally runs until sensors `S2-S6` detect a container, at which point the motor stops for the timer associated with filling, capping, or labelling and restarts after the timer expires.
   对应摘录：C
4. 句子 4：The container path then branches by size and material: both container types receive the first two fills, only large metallic containers open `V3` for the final brim fill, and afterward both types pass through `S5` capping, `S6` labelling, and storage.
   对应摘录：C
