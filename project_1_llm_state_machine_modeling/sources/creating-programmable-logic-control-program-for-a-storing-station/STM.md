# Creating Programmable Logic Control Program for a Storing Station - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动仓储站的 FIFO 入库/出库顺序、`C0/C1` 传送带检测、`M3/M4` 位置计数、抓取/放置功能块和 `2` 秒落料延时都写得很细，足以形成高质量制造控制样本。

## 条目 1: FIFO storing-and-leaving station supervisor

- 控制对象：自动仓储站的 FIFO 入库、出库与机械臂搬运控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是工业自动化与离散制造领域的仓储站顺序控制器，用传送带传感器、机械臂坐标传感器、计数内存和抓取/放置功能块实现 FIFO 入库与逆序出库。
- 判断：算。对象是真实自动仓储站控制系统，原文明确写出入库主链、出库主链、坐标/计数变量、机械臂运动状态和局部延时。

### 1. 原文摘录

#### 摘录 A

- 出处：第 26-27 页，`The programming controlling storing station / Flow chart of sequential program for storing operation`，`paper_content.txt` 第 115-124 行
> The storing process begins after the power of station and start conveyor buttons are on ...
>
> The sensor C0 at the initial conveyor position is activated, so the conveyor runs ... until sensor C1 is activated and the conveyor then is paused.
>
> the memory word is declared by 1 ... the arm is let down until the K0 is on ... the gripper closes ... the arm is lifted to position 1 ... the cylinder extends, then the gripper opens to leave the item onto rack.
>
> The similar process will run from item 3 to 20 to fill all racks of the storing station.
>
> The leaving item process will be launch after the storing station is full and the LEA button is turn on ... The leaving process will continue from item 20 to 1 sequentially until the station is empty.

#### 摘录 B

- 出处：第 34-37 页，`Sensors / Variables / PLC program`，`paper_content.txt` 第 156-166 行、第 174-188 行
> The arm can move by the operation of two motors moving along the x and y axis. The motors have three statuses of rotation, such as clockwise (CW), counterclockwise (CCW), and stop.
>
> M3 ... Position
>
> M4 ... Counting block
>
> C0 ... Initial point
>
> C1 ... preparing for lift
>
> C2 ... End of conveyor
>
> After the power and the STO turned on, the functions controlling conveyor (FC1) and arm motion (FC2) is called ... Because the value of M4 is 0, the function FC2 is called to move the arm to Position 1.

#### 摘录 C

- 出处：第 42-45 页，`counting / FC3 / FC5`，`paper_content.txt` 第 197-212 行
> After the item passes the C0, the conveyor will continue running until the item meets the sensor C1.
>
> The sensor C1 also takes on a role as the counter of items, so the counter will write the value 1 into M4. The data in M4 will be transferred to M3 to define the position of item on racks.
>
> The function FC3 ... At network 1, the motor Y goes down until the K0 is activated. The gripper will close ... to make the arm go up until B0 is activated again.
>
> After two seconds since Z is set, the variable G is reset to release the item on the rack, which will inactivate Z to retract the arm cylinder in the last step of the process.

### 2. 基于原文整理后的自然语言描述

The storing-station controller begins its storing cycle after power and conveyor start are enabled, then uses `C0` and `C1` to move an incoming pallet from the initial conveyor point to the pick-up point and pause the conveyor there. Each activation of `C1` increments the counting word `M4`, copies that value into `M3`, and thereby selects the target rack position for the current item. The arm subsystem is then driven by `FC3` and `FC5`: motor `Y` moves downward until `K0` is active, the gripper closes, the arm rises back to the upper line, and the cylinder extends so the pallet can be placed at the rack slot indexed by `M3`. After a `2` second delay with `Z` set, the gripper is released and the cylinder retracts, completing the placement cycle before the next item is processed. Once the station is full and `LEA` is enabled, the controller switches to the leaving sequence, starts from stored position `20`, and empties the rack back toward position `1`, so the overall controller behaves as a FIFO storing system with an explicitly modelled reverse retrieval routine.

### 3. 逐句溯源

1. 句子 1：The storing-station controller begins its storing cycle after power and conveyor start are enabled, then uses `C0` and `C1` to move an incoming pallet from the initial conveyor point to the pick-up point and pause the conveyor there.
   对应摘录：A, B
2. 句子 2：Each activation of `C1` increments the counting word `M4`, copies that value into `M3`, and thereby selects the target rack position for the current item.
   对应摘录：A, B, C
3. 句子 3：The arm subsystem is then driven by `FC3` and `FC5`: motor `Y` moves downward until `K0` is active, the gripper closes, the arm rises back to the upper line, and the cylinder extends so the pallet can be placed at the rack slot indexed by `M3`.
   对应摘录：A, C
4. 句子 4：After a `2` second delay with `Z` set, the gripper is released and the cylinder retracts, completing the placement cycle before the next item is processed.
   对应摘录：C
5. 句子 5：Once the station is full and `LEA` is enabled, the controller switches to the leaving sequence, starts from stored position `20`, and empties the rack back toward position `1`, so the overall controller behaves as a FIFO storing system with an explicitly modelled reverse retrieval routine.
   对应摘录：A
