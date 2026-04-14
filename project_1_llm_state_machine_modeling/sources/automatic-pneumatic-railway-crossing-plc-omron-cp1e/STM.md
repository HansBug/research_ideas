# Palang Pintu Kereta Api Pneumatik Otomatis Berbasis PLC Omron CP1E-NA20DR-A - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把两端传感器触发的道口门控写成了显式四状态图，并给出 `T0-T6` 迁移与 `3` 秒执行窗口，是铁路道口方向很稳定的双 A `FSM + T1` 样本。

## 条目 1: Four-State Pneumatic Gate Controller with Sensor-Triggered Close/Open Delays

- 控制对象：轨道交通领域的铁路平交道口气动栏杆控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用两个 proximity 传感器监测列车来向，并驱动 sirene、lampu 与气动 solenoid 完成道口关闭和重新开放的 PLC 道口控制器。
- 判断：算。对象是实际平交道口安全子系统，原文明确给出了双传感器输入、四个离散状态、带 `3` 秒窗口的前进/后退执行动作以及双向测试结果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-3 页，`Abstract / Desain Sistem`，`paper_content.txt` 第 21-24 行、第 117-121 行
> "dua buah sensor proximity"
>
> "sirene , lampu"

摘要和系统设计段都说明系统使用分置在道口两端的两枚 proximity 传感器作为输入，并把 sirene、lampu 和 pneumatik palang 作为核心输出。

#### 摘录 B

- 出处：第 3 页，`Algoritme`，`paper_content.txt` 第 137-139 行
> "sensor mendeteksi"
>
> "palang pintu akan menutup"

流程描述非常直接：第一枚传感器检测到列车后，先告警再关闭；第二枚传感器确认列车离开后，系统才重新打开道口。

#### 摘录 C

- 出处：第 4 页，`Diagram state sistem`，`paper_content.txt` 第 148-156 行
> "STA"
>
> "STB"
>
> "STC"
>
> "STD"
>
> "3 detik"

状态图把系统精确写成 `OFF -> lampu&siren -> solenoid maju -> solenoid mundur` 四态，并给出了 `T0-T6` 的事件顺序和两个 `3` 秒动作窗口。

#### 摘录 D

- 出处：第 8 页，`Tabel pengujian keberhasilan alat / Kesimpulan`，`paper_content.txt` 第 313-345 行
> "S1"
>
> "S2"
>
> "100%"

测试表验证了两个方向都服从相同的控制链：起始方向上的第一枚传感器负责关闭，另一侧第二枚传感器负责打开，系统整体在五次测试里达到 `100%` 成功率。

### 2. 基于原文整理后的自然语言描述

The railway-crossing controller is an explicit four-state machine in which the resting `OFF` state is followed by an alarm state, then a closing-actuator state, and finally an opening-actuator state. Two proximity sensors are placed on opposite sides of the crossing, and whichever side detects the train first drives the machine out of `STA` into `STB`, where sirens and lamps are activated before the closing solenoid is commanded. After that, the controller energizes the forward solenoid for a `3 s` window to close the gate, holds the protected state until the train is detected by the opposite-side sensor, and then energizes the reverse solenoid for another `3 s` window to reopen the crossing. Because the same `S1 -> close -> S2 -> open` and `S2 -> close -> S1 -> open` pattern is tested for both arrival directions, the paper provides a clean bidirectional `FSM + T1` crossing-gate sample rather than only a one-way laboratory demo.

### 3. 逐句溯源

1. 句子 1：The railway-crossing controller is an explicit four-state machine in which the resting `OFF` state is followed by an alarm state, then a closing-actuator state, and finally an opening-actuator state.
   对应摘录：C
2. 句子 2：Two proximity sensors are placed on opposite sides of the crossing, and whichever side detects the train first drives the machine out of `STA` into `STB`, where sirens and lamps are activated before the closing solenoid is commanded.
   对应摘录：A, B, C
3. 句子 3：After that, the controller energizes the forward solenoid for a `3 s` window to close the gate, holds the protected state until the train is detected by the opposite-side sensor, and then energizes the reverse solenoid for another `3 s` window to reopen the crossing.
   对应摘录：B, C
4. 句子 4：Because the same `S1 -> close -> S2 -> open` and `S2 -> close -> S1 -> open` pattern is tested for both arrival directions, the paper provides a clean bidirectional `FSM + T1` crossing-gate sample rather than only a one-way laboratory demo.
   对应摘录：D
