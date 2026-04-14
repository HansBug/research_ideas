# Automation of Tank Level Using Plc and Establishment of Hmi by Scada - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把液位上下阈值、地下水箱干转保护、`10` 分钟超时报警、手动覆盖和 HMI 上的空/充满/满/排空状态都写得很直接，满足 `🌡️` 方向双 A 要求。

## 条目 1: Low-level refill and dry-run alarm tank supervisor

- 控制对象：过程与环境控制领域的多水箱液位监控与泵阀监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个 `S7-300 PLC` 液位控制系统，负责依据地下/高位水箱液位和 HMI 输入控制泵、排液阀、手动覆盖和报警。
- 判断：算。对象是实际液位控制器，原文既给出自动启停和干转保护，也给出 `10` 分钟运行超时、手动启停覆盖和 `empty / filling / full / draining` 四类可观察运行状态。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 13-19 行
> Three level sensors were used to provide the level data to the PLC. PLC used this data to take the required decisions and thereby turning ON and OFF a pump. A manual switch was also provided to override the automatic system. The SIMATIC S7-300 universal controller was used as the main decision making module.

#### 摘录 B

- 出处：第 3 页，`III. Design And Implementation`，`paper_content.txt` 第 106-112 行
> The pump will automatically start when the water level of Over Head Tank reaches below Low Level and stop when the level reaches High Level. Dry run is checked by the Low Level sensor of the Under Ground Tank. In that case Pump will not run. Run time monitoring of the pump in Second and minute is recorded and Reset Switch is also provided. Provision of Manual Start/Stop switch is incorporated which will totally override the automatic system. Provisions are also made for various alarms, such as “Underground Tank Empty Alarm” and “Pump run time exceeded 10 Minutes”.

#### 摘录 C

- 出处：第 3 页，`3.1 Sensor Positioning`，`paper_content.txt` 第 120-124 行
> Four inductive Proximity sensors were used to sense presence of water at required levels. The sensors are UG_LL – Low Level Sensor Underground tank (I 0.2), OH_LL – Low Level Sensor Overhead tank (I 0.0), OH_HL – High Level Sensor Overhead tank (I 0.1) ... They give open contact when they are inside water and they give close contact when they are outside water.

#### 摘录 D

- 出处：第 6-7 页，`IV. Results`，`paper_content.txt` 第 263-330 行
> The Figure 9 shows the status of the various parameters when the tank is empty ... The drain valve is true ... pump is switched OFF.
>
> The Figure 10 shows the status of the various parameters when the tank is being filled. Pump is ON and Drain valve is OFF.
>
> The Figure 11 Shows TRUE value for all the level indicators ... tank is full. The pump is automatically turned OFF.
>
> During draining the drain valve shows TRUE value. The pump and the manual switch is kept OFF. The level indicators (Q5.0-Q5.7) show decreasing level.

### 2. 基于原文整理后的自然语言描述

The tank-level controller uses the underground and overhead tank sensors `UG_LL`, `OH_LL`, and `OH_HL` to supervise pump and valve actions through a Siemens `S7-300 PLC`. In automatic mode, the pump starts when the overhead tank falls below the low level and stops when the overhead tank reaches the high level, but dry-run protection prevents the pump from operating when the underground low-level sensor indicates an empty source tank. The controller also records pump runtime, provides a reset switch, raises an underground-tank-empty alarm, and triggers a runtime alarm if the pump runs continuously for `10` minutes. A manual start/stop switch can fully override the automatic logic from the HMI layer. On the monitored process side, the paper exposes explicit empty, filling, full, and draining situations: empty and draining keep the drain valve true with the pump off, filling turns the pump on with the drain valve off, and full forces all level indicators true while the pump is automatically turned off.

### 3. 逐句溯源

1. 句子 1：The tank-level controller uses the underground and overhead tank sensors `UG_LL`, `OH_LL`, and `OH_HL` to supervise pump and valve actions through a Siemens `S7-300 PLC`.
   对应摘录：A, C
2. 句子 2：In automatic mode, the pump starts when the overhead tank falls below the low level and stops when the overhead tank reaches the high level, but dry-run protection prevents the pump from operating when the underground low-level sensor indicates an empty source tank.
   对应摘录：B
3. 句子 3：The controller also records pump runtime, provides a reset switch, raises an underground-tank-empty alarm, and triggers a runtime alarm if the pump runs continuously for `10` minutes.
   对应摘录：B
4. 句子 4：A manual start/stop switch can fully override the automatic logic from the HMI layer.
   对应摘录：A, B
5. 句子 5：On the monitored process side, the paper exposes explicit empty, filling, full, and draining situations: empty and draining keep the drain valve true with the pump off, filling turns the pump on with the drain valve off, and full forces all level indicators true while the pump is automatically turned off.
   对应摘录：D
