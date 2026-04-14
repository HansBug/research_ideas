# Smart Car Parking System using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把入口放行、车位占用更新、LED 空位显示和出口放行写成了一条完整的停车场门禁与车位监督链，足以支撑双 A `EFSM + T0` 样本。

## 条目 1: Entry-gated slot occupancy parking controller

- 控制对象：智慧停车与车位管理领域的入口闸杆、车位占用显示与出口门禁控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个以 `PLC + IR sensor + servo motor + LED indicator` 实现的停车场入口放行、车位占用更新和出口放行控制器。
- 判断：算。对象是实际停车场控制系统，原文直接给出了入口检测、闸杆开闭、车位占用标记、LED 显示和出口放行的连续控制链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract / Description of System`，`paper_content.txt` 第 103-112 行、第 170-205 行
> The system aims to streamline the parking process by providing real-time information to drivers upon entry. Outside the parking area, a LED indicator is used which displays the available parking spots along with their corresponding numbers.
>
> PLC: selec TWIX-2 ... Used to keep the record of the number of cars and to indicate the available parking slots on LED. ... Sensor: IR Sensor ... Used to check the condition of the parking slot ... Arduino Board ... Used to control the movement of barricades at the entry and exit point. ... Servo Motor ... used to lift the barricade up and down at entry and exit point.

#### 摘录 B

- 出处：第 2-3 页，`How it works`，`paper_content.txt` 第 303-325 行
> IR sensors are installed at every parking slot and entry and exit point to detect the presence of vehicles, transmitting signals to the PLC. Upon receiving these signals, the PLC accurately tallies the number of parked cars and gives the status to an LED indicator ...
>
> The car will arrive at the entry gate ... the IR sensor will detect the car, and the barricade will open with the help of a servo motor. As the car enters inside, the barricade will close automatically. The driver will park his/her car at the decided slot.

#### 摘录 C

- 出处：第 3-4 页，`How it works / Results and Discussion`，`paper_content.txt` 第 399-403 行、第 598-625 行
> the LED indicator for slot 1 will glow, indicating that slot 1 is occupied. When the car leaves slot 1, the LED at the LED indicator will turn off. When the car leaves the slot to exit the parking area, it will reach the exit point where the IR sensor will detect the car, and the barricade will open with the help of a servo motor.
>
> Upon detecting a vehicle approaching the entry gate, the barricade opens automatically ... Similarly, when a vehicle approaches the exit point, the IR sensor triggers the opening of the barricade ... When a car occupies a slot, the corresponding LED indicator illuminates.

### 2. 基于原文整理后的自然语言描述

The parking controller stays in an entry-monitoring state where the PLC counts vehicles and exposes current slot availability on the LED panel. When a car reaches the entry gate, the entry IR sensor triggers the servo barricade to open, the car enters, and the barricade closes automatically behind it. Once the vehicle occupies a chosen slot, the matching slot IR sensor marks that slot as occupied and lights the corresponding LED until the car leaves. When the vehicle reaches the exit sensor, the controller opens the exit barricade and then returns to slot-availability monitoring.

### 3. 逐句溯源

1. 句子 1：The parking controller stays in an entry-monitoring state where the PLC counts vehicles and exposes current slot availability on the LED panel.
   对应摘录：A, B
2. 句子 2：When a car reaches the entry gate, the entry IR sensor triggers the servo barricade to open, the car enters, and the barricade closes automatically behind it.
   对应摘录：A, B
3. 句子 3：Once the vehicle occupies a chosen slot, the matching slot IR sensor marks that slot as occupied and lights the corresponding LED until the car leaves.
   对应摘录：B, C
4. 句子 4：When the vehicle reaches the exit sensor, the controller opens the exit barricade and then returns to slot-availability monitoring.
   对应摘录：C
