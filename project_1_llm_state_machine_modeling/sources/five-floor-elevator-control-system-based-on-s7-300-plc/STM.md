# The Five Floor Elevator Control System Design Based on S7-300 PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把五层电梯的速度切换、平层、呼梯方向过滤、反向响应和 `3` 秒门控延时写得比较完整，足以形成 `🏢` 方向的双 A 条目。

## 条目 1: Five-floor call-dispatch and 3-second door controller

- 控制对象：楼宇机电与电梯控制领域的五层 PLC 电梯呼梯、行驶与门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `S7-300 PLC` 的五层电梯控制系统，用磁隔离板和平层/减速传感器管理轿厢运行，并依据楼层呼梯与轿厢指令实现带方向约束的停层和门控。
- 判断：算。对象是实际电梯控制器，原文不仅给出平层/减速信号链，还明确写出 `3` 秒自动关门、反向呼梯不响应、最远反向响应与综合截停等离散控制规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`1.3 For speed change and leveling sensor device`，`paper_content.txt` 第 193-198 行
> Issued for speed change, floor and leveling signal sensor device are installed on the car ... When the car reaches the speed change position, speed change magnetic isolation plate inserted in the middle of speed change sensors and makes the motor slowdown. When car reaches parking floor, leveling magnetic isolation plate inserted in the middle of leveling sensors and car bottom is exactly flush with the floor.

#### 摘录 B

- 出处：第 3 页，`2. System control requirements analysis`，`paper_content.txt` 第 200-212 行
> This elevator model is total five floors ... each of floor hall were input (ascending and descending) button to call the elevator ... elevator stops at the floor, elevator stops running and door opens, and then closed automatically after three seconds delay ... During the elevator in the process of ascending (or descending), any descending in the opposite direction (or ascending) of hall call signal does not respond. Elevator should have the farthest reverse response function for hall call signals. The elevator has synthetic interception function.

#### 摘录 C

- 出处：第 6 页，`5. The elevator running status`，`paper_content.txt` 第 388-397 行
> The car door open can be divided into the following situations: a. Elevator on the first floor leveling, there is first floor hall call for ascending indication or car call indication ... Elevator on the fifth floor leveling, there is fifth floor hall call for descending indication or car call indication. f. When elevator on the leveling, pressing the door open button.

### 2. 基于原文整理后的自然语言描述

The five-floor elevator controller equips the car with speed-change, floor, and leveling sensors, and uses magnetic isolation plates in the shaft so the motor slows down at the deceleration position and the car aligns exactly with the landing at the parking floor. Across the five floors, each hall provides ascending or descending call inputs together with car-call signals inside the cabin. When a valid hall call or car call is served, the car stops at the requested floor, opens the door, and then closes it automatically after a `3` second delay. While the car is ascending or descending, hall calls in the opposite direction are ignored, but the controller still supports farthest reverse response and synthetic interception for pending requests. Once the car is leveled at a floor, door opening is enabled according to the floor-specific hall-call or car-call condition described for that floor.

### 3. 逐句溯源

1. 句子 1：The five-floor elevator controller equips the car with speed-change, floor, and leveling sensors, and uses magnetic isolation plates in the shaft so the motor slows down at the deceleration position and the car aligns exactly with the landing at the parking floor.
   对应摘录：A
2. 句子 2：Across the five floors, each hall provides ascending or descending call inputs together with car-call signals inside the cabin.
   对应摘录：B
3. 句子 3：When a valid hall call or car call is served, the car stops at the requested floor, opens the door, and then closes it automatically after a `3` second delay.
   对应摘录：B
4. 句子 4：While the car is ascending or descending, hall calls in the opposite direction are ignored, but the controller still supports farthest reverse response and synthetic interception for pending requests.
   对应摘录：B
5. 句子 5：Once the car is leveled at a floor, door opening is enabled according to the floor-specific hall-call or car-call condition described for that floor.
   对应摘录：C
