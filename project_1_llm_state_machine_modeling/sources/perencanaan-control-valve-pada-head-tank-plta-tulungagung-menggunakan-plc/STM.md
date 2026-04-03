# Perencanaan Control Valve Pada Head Tank PLTA Tulungagung Menggunakan PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了头水箱液位阈值到阀门动作的明确 PLC 控制逻辑，并包含 auto/manual 与传感器改造信息。

## 条目 1: Head-Tank Elevation Valve Control
- 控制对象：过程控制领域的水电站头水箱 PLC 控制阀系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是 PLTA 头水箱液位控制器，用于根据超声波测得的水位高度自动驱动电动阀/电磁阀维持冷却水系统所需水位。
- 判断：算。对象是实际冷却系统控制子系统，原文明确给出了液位阈值和阀门开关条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract, 行 17-24
> Head Tank ... still has a manual control valve which consists of a gate valve and a pair of float valves. ... In this research, there would build a plan of the automatic control valve of the Tulungagung HEPP. PLC Siemens Simatic Step 7 was used as a control base on a SCADA software Wonderware Intouch version 10.0.0. In this modification plan, a pair of float valve changed over solenoid valve and manual gate valve change over motorized valve. For the water level that would be ultrasonic sensor SICK UM 30 ...

#### 摘录 B
- 出处：第 3 页，control logic summary, 行 140-146
> 1. Jika elevasi head tank ≤ 41.60 mdpl maka sinyal elevasi head tank low terkirim di ruang CCR, dan float valve 1 + float valve 2 = ON
>
> 2. Jika elevasi head tank ≤ 41.80 mdpl, maka float valve 1 + float valve 2 = ON hingga elevasi head tank mencapai 42.00 mdpl.
>
> 3. Jika 41.80 mdpl ≤ elevasi head tank ≤ 42.00 mdpl, maka float ...

#### 摘录 C
- 出处：第 5-6 页，`4.1 Konsep Modifikasi / flowchart setelah modifikasi`，行 195-216, 323-351
> Elevasi maksimal head tank ... 42.00 mdpl,
> Elevasi minimal untuk kondisi kerja 1 ... 41.80 mdpl,
> Elevasi minimal untuk kondisi kerja 2 ... 41.60 mdpl,
> “elevasi head tank low” yaitu 41.00 mdpl.
> ...
> Auto control valve 1 ... operasi berdasar elevasi minimal 41.80 mdpl hingga 42.00 mdpl,
> Auto control valve 2 ... operasi berdasar elevasi minimal 41.60 mdpl hingga 42.00 mdpl,
> Back up valve ... operasi berdasar elevasi dibawah 41.60 mdpl,
> ...
> 1. Awal pengisisan head tank adalah kondisi ≤ 41.00 mdpl dengan mengirim sinyal alarm head tank low di ruang CCR
> 2. Jika elevasi head tank ≤ 41.60 akan memerintahkan back up valve + solenoid valve 1 + solenoid valve 2 beroperasi hingga air mencapai elevasi 42.00 mdpl.
> 3. Jika 41.60 mdpl ≤ elevasi air head tank ≤ 41.80 mdpl, maka solenoid valve 1 + solenoid 2 ON hingga elevasi air mencapai 42.00 mdpl
> 4. Jika 41.80 mdpl ≤ elevasi air head tank ≤ 42.00 mdpl, maka solenoid valve 1 hingga elevasi air mencapai 42.00 mdpl
> 5. Jika elevasi air head tank ≥ 42.00 mdpl, maka back up valve + solenoid valve 1 + solenoid valve 2 = CLOSE

### 2. 基于原文整理后的自然语言描述

The modified head-tank controller replaces the original manual gate-valve and float-valve arrangement with a PLC-based automatic system that uses an ultrasonic level sensor, two solenoid inlet valves, and a motorized back-up valve while still supporting auto/manual operation through PLC and SCADA. The control ranges are explicitly layered: `41.00 mdpl` is the low-level alarm threshold, `41.60 mdpl` is the threshold for operating the back-up valve together with solenoid valves 1 and 2, `41.80 mdpl` is the threshold for operating only solenoid valves 1 and 2, and `42.00 mdpl` is the full level. When the head-tank elevation falls to `41.00 mdpl` or below, a low-level signal is sent to the control room, and when it falls to `41.60 mdpl` or below the controller opens the back-up valve plus both solenoid valves until the level returns to `42.00 mdpl`. If the elevation is between `41.60 mdpl` and `41.80 mdpl`, only solenoid valves 1 and 2 are opened, and if it is between `41.80 mdpl` and `42.00 mdpl`, only solenoid valve 1 remains active; once the level reaches or exceeds `42.00 mdpl`, all three valves are closed.

### 3. 逐句溯源

1. 句子 1：The modified head-tank controller replaces the original manual gate-valve and float-valve arrangement with a PLC-based automatic system that uses an ultrasonic level sensor, two solenoid inlet valves, and a motorized back-up valve while still supporting auto/manual operation through PLC and SCADA.
   对应摘录：A, C
2. 句子 2：The control ranges are explicitly layered: `41.00 mdpl` is the low-level alarm threshold, `41.60 mdpl` is the threshold for operating the back-up valve together with solenoid valves 1 and 2, `41.80 mdpl` is the threshold for operating only solenoid valves 1 and 2, and `42.00 mdpl` is the full level.
   对应摘录：B, C
3. 句子 3：When the head-tank elevation falls to `41.00 mdpl` or below, a low-level signal is sent to the control room, and when it falls to `41.60 mdpl` or below the controller opens the back-up valve plus both solenoid valves until the level returns to `42.00 mdpl`.
   对应摘录：B, C
4. 句子 4：If the elevation is between `41.60 mdpl` and `41.80 mdpl`, only solenoid valves 1 and 2 are opened, and if it is between `41.80 mdpl` and `42.00 mdpl`, only solenoid valve 1 remains active; once the level reaches or exceeds `42.00 mdpl`, all three valves are closed.
   对应摘录：B, C
