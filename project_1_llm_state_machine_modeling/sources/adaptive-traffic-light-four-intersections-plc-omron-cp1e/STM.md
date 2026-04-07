# Desain Sistem Kontrol Traffic Light Adaptif pada Empat Persimpangan Berbasis PLC Omron CP1E - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四路口交通灯的正常模式、三档拥堵延长和总堵塞全红模式写得很完整，并明确给出传感器阈值、配时表和等待时间范围，可直接作为双 A `EFSM + T1` 样本。

## 条目 1: Four-Approach Adaptive Signal Controller with Queue-Level and Gridlock Overrides

- 控制对象：道路交通信号控制领域的四路口 PLC 自适应交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个以 PLC Omron CP1E 为核心的四路口交通灯控制器，用每条车道上的三枚排队传感器和路口中央的两枚总堵塞传感器来决定绿灯延长、正常轮转或全红封锁。
- 判断：算。对象是实际交通灯控制系统，原文同时给出了控制对象、三种运行层级、每级时间分配、传感器激活条件以及总堵塞恢复条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 3 行
> "tiga sensor"
>
> "45 detik" / "81 detik"

摘要直接说明每条路口使用三枚排队传感器来判断拥堵程度，并把最短等待时间与最坏等待时间都给了出来。

#### 摘录 B

- 出处：第 4-5 页，`Perancangan Sistem Kerja`，`paper_content.txt` 第 14-20 行
> "sistem normal"
>
> "sistem kepadatan"
>
> "kemacetan total"

这里把控制器分成正常、分级拥堵和总堵塞三层，并补充了整套硬件规模：`12` 个车道传感器、`2` 个路口中部堵塞传感器和 `12` 盏信号灯。

#### 摘录 C

- 出处：第 7 页，`Tabel 1 rancangan waktu pengaturan traffic light`，`paper_content.txt` 第 29 行
> "7 Detik"
>
> "12 Detik 17 Detik 22 Detik"

配时表明确给出正常模式与三档拥堵模式的红黄绿时长映射，是这条 STM 的核心时间证据。

#### 摘录 D

- 出处：第 11-12 页，`Perkiraan Waktu Tunggu Sistem Kepadatan`，`paper_content.txt` 第 59-62 行
> "1 menit"
>
> "30 detik"

原文进一步写清了单个排队传感器需要持续遮挡 `5` 秒才算激活，而中央堵塞传感器需要持续遮挡 `1` 分钟才触发全红，并在持续 `30` 秒无遮挡后恢复。

### 2. 基于原文整理后的自然语言描述

The adaptive traffic-light controller organizes a four-approach intersection into three operating layers: a normal rotation mode, a density-aware extension mode, and a total-gridlock override mode. Each approach is instrumented with three queue sensors, and the PLC interprets those sensors as three congestion levels that extend the green interval from the normal `7 s` to `12 s`, `17 s`, or `22 s` while keeping the red-yellow-green cycle structure intact. In parallel, two sensors placed in the middle of the intersection supervise a total-gridlock condition, and if both remain blocked long enough the controller forces all directions to red instead of serving any approach. The same paper also quantifies the operational consequence of this logic by showing a normal waiting time of `45 s` and a worst-case waiting time of `81 s`, which means the controller exposes both explicit local timers and a bounded queue-delay effect at the intersection level.

### 3. 逐句溯源

1. 句子 1：The adaptive traffic-light controller organizes a four-approach intersection into three operating layers: a normal rotation mode, a density-aware extension mode, and a total-gridlock override mode.
   对应摘录：B
2. 句子 2：Each approach is instrumented with three queue sensors, and the PLC interprets those sensors as three congestion levels that extend the green interval from the normal `7 s` to `12 s`, `17 s`, or `22 s` while keeping the red-yellow-green cycle structure intact.
   对应摘录：A, C, D
3. 句子 3：In parallel, two sensors placed in the middle of the intersection supervise a total-gridlock condition, and if both remain blocked long enough the controller forces all directions to red instead of serving any approach.
   对应摘录：A, B, D
4. 句子 4：The same paper also quantifies the operational consequence of this logic by showing a normal waiting time of `45 s` and a worst-case waiting time of `81 s`, which means the controller exposes both explicit local timers and a bounded queue-delay effect at the intersection level.
   对应摘录：A, D
