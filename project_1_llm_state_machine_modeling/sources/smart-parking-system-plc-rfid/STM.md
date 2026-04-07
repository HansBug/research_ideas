# Rancang Bangun Sistem Parkir Pintar Berbasis PLC (Programmable Logic Controller) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 RFID 身份校验、空车位选择、平台取车板、入口桥板和满位禁入链写得比较完整，是停车场方向可靠的双 A `EFSM + T0` 样本。

## 条目 1: RFID-Guided Slot Assignment and Plat-Shuttle Parking Controller

- 控制对象：智慧停车与车位管理领域的多层停车楼 PLC 存取车控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用于微型多层停车楼的 PLC 控制器，结合 RFID 身份识别、空车位检测、平台平移/升降/旋转以及入口闸桥控制来完成入库和出库。
- 判断：算。对象是实际停车系统控制器，原文给出了输入输出映射、模式切换、空位选择、具体 memory 位、平台与闸桥的顺序动作以及满位阻塞逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Abstrak / Pendahuluan`，`paper_content.txt` 第 22-29 行、第 81-94 行
> "RFID"
>
> "trial and error"
>
> "90%"

摘要和引言直接说明系统采用多层停车楼、RFID 身份识别和 PLC 主控，并已经在缩比装置上实现了自动停车与取车。

#### 摘录 B

- 出处：第 2-3 页，`Pengalamatan Input-Output PLC`，`paper_content.txt` 第 145-202 行
> "Mode Masuk"
>
> "Mode Keluar"
>
> "Indikator Penuh"

输入输出表把模式按钮、楼层按钮、各车位边界、平台左右边界、旋转角度、四个车位传感器和闸门边界都映射到了 PLC 地址，同时给出了 `13` 个输出用于升降、左右移动、旋转和状态指示。

#### 摘录 C

- 出处：第 3-4 页，`Perancangan Visual Studio 2010`，`paper_content.txt` 第 229-255 行
> "kamar yang kosong"
>
> "kamar sudah penuh"

这里把上层 HMI 与 PLC 的衔接写清楚了：RFID 匹配数据库后，软件会自动选择空车位并把空位信息写给 PLC；如果车位已满，系统会直接阻止入场模式。

#### 摘录 D

- 出处：第 6-7 页，`Pengujian Sistem Secara Keseluruhan`，`paper_content.txt` 第 382-445 行
> "220.02"
>
> "mode masuk"

系统级测试部分明确说明了某一目标车位对应的 memory 位、入场前先取目标车板到地面、随后闸桥落下作为通道，以及四个车位的成功入场与满位提示逻辑。

### 2. 基于原文整理后的自然语言描述

The parking controller begins by reading an RFID tag, matching it against a stored user record, and then deciding whether the vehicle is entering or leaving through separate `Mode Masuk` and `Mode Keluar` branches. Its PLC I/O map explicitly models room boundaries, room-occupancy photodiode sensors, left-right platform limits, rotation positions, and gate limits, so the storage process is not just a counter update but a structured electromechanical sequence. When the HMI finds an empty room, it writes the room-selection result to the PLC, which can then activate a dedicated memory such as `220.02` for the selected destination and verify that the target room sensor still reports vacancy. Before the car actually enters, the system first brings the target plate down to the ground floor and only then lowers the protective gate to form a bridge, while the `Indikator Penuh` and the HMI full message block any new entry request after all four rooms are occupied.

### 3. 逐句溯源

1. 句子 1：The parking controller begins by reading an RFID tag, matching it against a stored user record, and then deciding whether the vehicle is entering or leaving through separate `Mode Masuk` and `Mode Keluar` branches.
   对应摘录：A, B, C
2. 句子 2：Its PLC I/O map explicitly models room boundaries, room-occupancy photodiode sensors, left-right platform limits, rotation positions, and gate limits, so the storage process is not just a counter update but a structured electromechanical sequence.
   对应摘录：B
3. 句子 3：When the HMI finds an empty room, it writes the room-selection result to the PLC, which can then activate a dedicated memory such as `220.02` for the selected destination and verify that the target room sensor still reports vacancy.
   对应摘录：C, D
4. 句子 4：Before the car actually enters, the system first brings the target plate down to the ground floor and only then lowers the protective gate to form a bridge, while the `Indikator Penuh` and the HMI full message block any new entry request after all four rooms are occupied.
   对应摘录：B, C, D
