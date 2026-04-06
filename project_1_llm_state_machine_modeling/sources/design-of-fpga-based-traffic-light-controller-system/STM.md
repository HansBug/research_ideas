# Design of FPGA-Based Traffic Light Controller System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把真实双路口六灯交通控制写成了带 `PEAK / SENSOR1 / SENSOR2` 条件分支的显式时序控制器，既给出 `32 / 16 / 8 / 4 / 2 s` 时长，也给出 off-peak 下的分支切换和窄路跳过逻辑，可稳定形成双 A 样本。

## 条目 1: Six-light peak/off-peak sensor-gated traffic controller

- 控制对象：道路交通信号控制领域的六灯峰/谷时交通信号控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向两处相连路口的 FPGA 交通灯控制器，用 `PEAK` 标志与 `Sensor1 / Sensor2` 条件决定 `T1-T6` 六个信号灯在 peak / off-peak 场景下的放行顺序、持续时长和跳过逻辑。
- 判断：算。对象是实际交通灯控制器，不是单纯硬件展示；原文直接给出了六灯结构、主路/窄路角色、固定时长、传感器触发的分支切换，以及峰谷时不同的完整相位链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Abstract，`paper_content.txt` 第 2-25 行
> This paper proposed a design of a modern FPGA-based Traffic Light Control (TLC) System to manage the road traffic ... during peak and off-peak hours.
>
> The implementation is based on real location in a city in Malaysia ... The proposed design is a more universal and intelligent approach ... Theoretically the waiting time for drivers during off-peak hours has been reduced further.

#### 摘录 B

- 出处：第 3 页，`II. ROAD STRUCTURE / A. TIMING Setting`，`paper_content.txt` 第 104-178 行
> six traffics, represented by T1, T2, T3, T4, T5 and T6 to be controlled. T1 and T2 have been identified as the main road for the first junction while T4 and T6 are for the second junction. The last two traffic lights, T3 and T5 are the smaller roads.
>
> For main roads T1, T2, T4 and T6 are 32s (peak) / 16s (off-peak) while for narrow road T3 and T5 are 16s (peak) / 8s (off-peak). Amber ... 4s. Red ... 2s.
>
> When both sensors (Sensor 1 and Sensor 2) are activated, the cycles are the same as Fig. 2 except that timing for green light will be less ...
>
> At a condition where only Sensor 1 is being set off ... T3 and T6 ... When only Sensor 2 is triggered ... T2 and T5 ... At a time when both sensors are not activated, the cycles for T3 and T5 will be skipped.

#### 摘录 C

- 出处：第 4-6 页，`III. RESULTS AND DISCUSSION`，`paper_content.txt` 第 215-255 行
> First cycle initiated with T1 and T6 are green ... After 32s, T1 and T6 will change to amber for 4s and then red for 2s ...
>
> Second cycle begins with both T2 and T4 turn to green for 32s, subsequently amber for 4s and lastly red for 2s ...
>
> Third cycle starts when traffic lights T3 and T5 (at narrow roads) turn green for just 16s, followed by amber for 4s and in the end red for another 2s ...
>
> when only Sensor 2 is activated, traffic light corresponding to this sensor, T5 will be green together with T2 for 8s ... The cycle will then continue with the first cycle where T1 and T6 turning green.

### 2. 基于原文整理后的自然语言描述

The controller manages a real two-junction road structure with six controlled signals `T1-T6`, where `T1/T2/T4/T6` are main-road phases and `T3/T5` are the narrow-road phases. In peak mode, the system executes a fixed three-cycle sequence: `T1+T6 green -> amber -> red`, then `T2+T4 green -> amber -> red`, and finally `T3+T5 green -> amber -> red`, with explicit durations of `32 s` green for the main-road cycles, `16 s` green for the narrow-road cycle, `4 s` amber, and `2 s` red. In off-peak mode, the same controller becomes input-conditioned: if both sensors are active, all green times shrink to `16 s` for the main roads and `8 s` for the narrow roads; if only `Sensor1` is active, the third cycle becomes `T3+T6`; if only `Sensor2` is active, the third cycle becomes `T2+T5`; and if neither sensor is active, the `T3/T5` narrow-road cycle is skipped. This makes the paper a timed EFSM-style traffic-control sample rather than a plain fixed-cycle FSM, because the active sensor and peak/off-peak flag directly alter which phase is entered and how long it is held.

### 3. 逐句溯源

1. 句子 1：The controller manages a real two-junction road structure with six controlled signals `T1-T6`, where `T1/T2/T4/T6` are main-road phases and `T3/T5` are the narrow-road phases.
   对应摘录：A, B
2. 句子 2：In peak mode, the system executes a fixed three-cycle sequence: `T1+T6 green -> amber -> red`, then `T2+T4 green -> amber -> red`, and finally `T3+T5 green -> amber -> red`, with explicit durations of `32 s` green for the main-road cycles, `16 s` green for the narrow-road cycle, `4 s` amber, and `2 s` red.
   对应摘录：B, C
3. 句子 3：In off-peak mode, the same controller becomes input-conditioned: if both sensors are active, all green times shrink to `16 s` for the main roads and `8 s` for the narrow roads; if only `Sensor1` is active, the third cycle becomes `T3+T6`; if only `Sensor2` is active, the third cycle becomes `T2+T5`; and if neither sensor is active, the `T3/T5` narrow-road cycle is skipped.
   对应摘录：B, C
4. 句子 4：This makes the paper a timed EFSM-style traffic-control sample rather than a plain fixed-cycle FSM, because the active sensor and peak/off-peak flag directly alter which phase is entered and how long it is held.
   对应摘录：A, B, C
