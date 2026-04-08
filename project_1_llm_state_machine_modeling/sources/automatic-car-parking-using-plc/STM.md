# AUTOMATIC CAR PARKING USING PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多层停车系统的入口检测、空托盘分配、车位记录、取车匹配与满位闭门逻辑写成一条完整的 PLC 控制链。

## 条目 1: Entry-Storage-Retrieval parking controller

- 控制对象：智慧停车与车位管理领域的多层自动停车 PLC 控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个自动立体停车控制器，负责在车辆入场时检测空托盘并搬运存车，在取车时依据 HMI 输入的车号检索并把对应托盘送回出口。
- 判断：算。对象是实际多层停车系统的 PLC 主控制链，不是单纯机械结构说明；原文明确给出了入口检测、车位分配、存储记录、取车匹配、占用计数和满位闭门逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，摘要与引言，`paper_content.txt` 第 13-20、34-40 行
> The automation process of an automatic car parking system is designed using a fully functional ladder logic, which is a small programmable logic controller (PLC). Infrared sensor (IR) are placed at every parking to detect the pallet and presence of car. It is also use to check whether parking is empty or full. In this parking system concept of lift and pulley is used. PLC operates stepper motors which is use for horizontal and vertical motion of the lift. HMI displays the parking full or empty as well as it also displays whether the sensor is active or in active.
>
> ... the driver leaves the car inside an entrance area and technology parks the vehicle at a designated area. Mechanical car lifters, with the help of PLC raise the vehicle to another level for proper storing. The vehicle can be transported vertically (up and down) and horizontally (left and right) to a vacant parking space until the car is need again. When the vehicle is needed, the process is reversed and the car lifts transport the vehicle back to the same area where the driver left it.

#### 摘录 B

- 出处：第 2-3 页，`III. METHODOLOGY / Working Principle`，`paper_content.txt` 第 93-101 行
> The car comes at entry point, the sensor sends signal to the control system, then system check the empty pallets and move that pallets at entry point. After car moved on pallets IR sensor send signal to PLC. Then PLC store the information related to that car and pallets using inputs from HMI and IR sensor. At the time of exit, user will enter the car number on HMI. Then HMI send signal to PLC. PLC compare the information with stored data. After matching information, the related pallets move to exit point. The number of cars available in the park will be calculated by the differencing the number of vehicles entering and the number of vehicles leaving the park. PLC will decide whether any space is available or not. If no space is available, the PLC will send acknowledge signal to the gate to keep the gate closed and turn on the indication “Car Park Full”.

#### 摘录 C

- 出处：第 3-4 页，`Components / IR Sensor`，`paper_content.txt` 第 148-152 行
> The IR sensor can detect obstacles from 1mm to 10cm. ... The IR sensors are used for detecting vehicle present in parking system. IR sensor is also used as gate sensor to check if the vehicle is present on the parking gate. In this sensor IR couple is used to detect the obstacle, but in this case it is used to detect the car as well as the pallet.

### 2. 基于原文整理后的自然语言描述

The parking controller uses IR sensors, HMI inputs, stepper-motor drives, and a lift-and-pallet mechanism to manage the full storage and retrieval cycle of a multi-storey parking system. When a vehicle arrives at the entry point, the gate sensor triggers the PLC to check for an empty pallet and move that pallet to the entrance so the car can be loaded. After the IR sensor confirms that the car is on the pallet, the PLC stores the mapping between the vehicle and the pallet using HMI and sensor inputs, and then commands vertical and horizontal pallet motion to move the car into a vacant slot. When the user later enters the car number on the HMI, the PLC compares that identifier with the stored data, retrieves the matching pallet, and brings it back to the exit point. In parallel, the controller keeps an occupancy count from entering and leaving cars and, if no space is available, it keeps the gate closed and raises the `Car Park Full` indication instead of starting another storage cycle.

### 3. 逐句溯源

1. 句子 1：The parking controller uses IR sensors, HMI inputs, stepper-motor drives, and a lift-and-pallet mechanism to manage the full storage and retrieval cycle of a multi-storey parking system.
   对应摘录：A, C
2. 句子 2：When a vehicle arrives at the entry point, the gate sensor triggers the PLC to check for an empty pallet and move that pallet to the entrance so the car can be loaded.
   对应摘录：B, C
3. 句子 3：After the IR sensor confirms that the car is on the pallet, the PLC stores the mapping between the vehicle and the pallet using HMI and sensor inputs, and then commands vertical and horizontal pallet motion to move the car into a vacant slot.
   对应摘录：A, B
4. 句子 4：When the user later enters the car number on the HMI, the PLC compares that identifier with the stored data, retrieves the matching pallet, and brings it back to the exit point.
   对应摘录：A, B
5. 句子 5：In parallel, the controller keeps an occupancy count from entering and leaving cars and, if no space is available, it keeps the gate closed and raises the `Car Park Full` indication instead of starting another storage cycle.
   对应摘录：B
