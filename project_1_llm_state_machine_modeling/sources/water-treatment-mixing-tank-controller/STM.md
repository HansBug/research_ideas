# Modelling and Verification of an Automatic Controller for a Water Treatment Mixing Tank - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把混合槽控制器写成 `S0-S10` 与 `T0-T9` 的完整顺序链，并明确保留 `LS1/LS2`、`V1/V2/V3`、搅拌泵、指示灯和 on-delay timer，满足双 A 样本要求。

## 条目 1: Timed Fill-Mix-Drain Controller for Water Treatment Tank

- 控制对象：过程与环境控制领域的双化学品水处理混合槽顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个 PLC 控制的水处理混合槽循环控制器，用液位开关、进液阀、搅拌泵、延时器和排液阀驱动进液-搅拌-排液循环。
- 判断：算。对象是论文主控制系统，原文明确给出设备、状态、迁移、guard 和定时条件，不是单纯 Petri net 教学例子。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，Section 2.2
> When the start button is pressed, the PLC and lamp 1 are in the ON state. LS1 and LS2 are responsible for sending information about the level of water treatment inside the tank to the PLC.
>
> If the level of the mixed chemicals inside the tank is at the lower limit (L), LS1 is OFF and LS2 is ON, and electromagnetic valves (V1) and (V2) are OPEN to let the two chemicals flow into the tank.

#### 摘录 B

- 出处：第 4 页，Section 2.2
> When the level of the chemicals inside the tank reaches one-third of the capacity of the tank (N) the mixer motor is turned ON ... If the level of the chemical reaches the high level (H), LS2 is turned OFF and LS1 is turned ON, valves (V1) and (V2) are turned OFF ... an on-delay timer is turned ON.
>
> When the time has elapse, the mixer motor is turned OFF ... electromagnetic valve (V3) is OPEN.

#### 摘录 C

- 出处：第 5 页，Section 2.3
> When the push button switch is press to the ON state, T0 is enabled ... the state moves to S0. In that state lamp 1 is ON and T1 is enabled only if LS1 is OFF ...
>
> If T2 is enabled it changes the state from S1 to S2, in which case electromagnetic valves (V1) and (V2) are opened.
>
> T7 can only be enabled if the on-delay timer is OFF. When T7 is enabled another state, S8, is entered ... electromagnetic valve (V3) is OPEN.
>
> T9 can be enabled only when LS2 is ON. If T9 is enabled, another state, S10, is entered where the electromagnetic valve (V3) is OFF.

### 2. 基于原文整理后的自然语言描述

The water-treatment mixing-tank controller runs a timed sequential cycle over explicit Petri-net/PLC states `S0-S10`. After the start push button fires `T0`, the controller enters the lamp-1 operating state and waits for the low-level condition reported by `LS1` and `LS2`. When the tank is at the lower limit, the PLC opens `V1` and `V2` so two chemicals flow into the tank and turns on the corresponding filling indication. As the liquid reaches the intermediate and high-level thresholds, the controller starts the mixer motor, then closes `V1` and `V2`, turns off the filling lamp, and starts an on-delay timer to hold the mixing phase. Once the timer expires, the mixer is stopped and `V3` opens so the mixed chemical drains until `LS2` reports the lower-level condition again; then `V3` is closed and the cycle can repeat until the PLC push button is turned off.

### 3. 逐句溯源

1. 句子 1：The water-treatment mixing-tank controller runs a timed sequential cycle over explicit Petri-net/PLC states `S0-S10`.
   对应摘录：C
2. 句子 2：After the start push button fires `T0`, the controller enters the lamp-1 operating state and waits for the low-level condition reported by `LS1` and `LS2`.
   对应摘录：A, C
3. 句子 3：When the tank is at the lower limit, the PLC opens `V1` and `V2` so two chemicals flow into the tank and turns on the corresponding filling indication.
   对应摘录：A, C
4. 句子 4：As the liquid reaches the intermediate and high-level thresholds, the controller starts the mixer motor, then closes `V1` and `V2`, turns off the filling lamp, and starts an on-delay timer to hold the mixing phase.
   对应摘录：B, C
5. 句子 5：Once the timer expires, the mixer is stopped and `V3` opens so the mixed chemical drains until `LS2` reports the lower-level condition again; then `V3` is closed and the cycle can repeat until the PLC push button is turned off.
   对应摘录：B, C
