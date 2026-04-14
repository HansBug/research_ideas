# HANDSFREE VALET TECHNOLOGY (HFVT) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动泊车的搜索、判位、对齐、泊入和停车后修正链写成了明确的高层 FSM，并保留了并联泊车 / 头入泊车两条分支，足以构成 `🅿️` 方向的双 A 样本。

## 条目 1: Five-Stage Sensor-Driven Valet Parking FSM

- 控制对象：智慧停车与车位管理领域的自动代客泊车高层控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向停车场自动泊车的高层监督器，用右侧超声与前后触碰传感器完成 `Looking -> Detecting -> Alignment -> Park -> Stop` 的串行控制，并在 `Alignment/Park` 阶段按 `isParallel` 分成并联泊车和头入泊车两种动作链。
- 判断：算。对象是真实停车控制流程，不是单纯传感器介绍；原文明确写了命名状态、进入条件、回退条件、`isParallel` 分支和停车后的修正逻辑。需要如实说明的是，正文提到“six states”，但提取文本中被完整枚举并解释的命名状态是 `Looking / Detecting / Alignment / Park / Stop` 这五个，仍足以恢复主控制链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 18-52 行
> Therefore we propose Hands Free Valet Technology (HFVT): a technology that can identify a parking space and simultaneously perform a parallel or head-in park by itself ... The HFVT contains four primary components integrated neatly into a single package: a vehicle chassis, four sensors (two ultrasonic and two bumps), two motors, and a goal-based reflex algorithm. Firstly, a car is driven down a street searching for a parking space to its right using a distance sensor. When the car identifies a space, it checks to see whether it is large enough for the car to be parked in. If it determines that there is sufficient space, the car will begin parking into that space completely autonomously.

#### 摘录 B

- 出处：第 2 页，Parking Algorithm，`paper_content.txt` 第 134-173 行
> The Parking algorithm uses a high-level finite state machine which consists of six states that must be traversed for each successful park:
>
> Looking: The vehicle begins with the state Looking ... it will continue to be in that state until a desired transition condition (specific spike in sensor readings or a jump in distance for the depth between the right side of the car and a wall or open space) is met.
>
> The vehicle sets a flag isParallel based on the sensor reading, sets the distance to Drop, and transitions into the state Detecting.
>
> Detecting: HFVT looks to satisfy two conditions based on the type of spot for parking that isParallel denotes ... If either of these conditions is violated, the vehicle will go back into looking.

#### 摘录 C

- 出处：第 3 页，Alignment / Park / Corrective Steering，`paper_content.txt` 第 183-218 行
> Alignment ... Parallel Parking: The vehicle pulls forward to align its back wheels with the beginning of the parking spot ... and then proceeds to the state Park.
>
> Head-in Parking: The vehicle needs to align itself to the desired position which is to reverse back and away from the parking spot ... and then proceeds to the state Park.
>
> Park: If isParallel set for head-in parking, the vehicle drives forward ... If isParallel set for parallel parking, the car must travel in a similar manner except in reverse ... the vehicle successfully parked inside a spot, achieved its goal state, and transitioned into the state Stop.
>
> In the Stop state ... the vehicle now determines whether or not it is parallel to the surface on the right ... Using the information from the two touch sensors, the vehicle will slowly align itself for the parking spot’s defined width and depth.

### 2. 基于原文整理后的自然语言描述

The HFVT controller is a high-level parking FSM that uses two right-side ultrasonic sensors together with front and rear touch sensors to supervise autonomous spot search and parking execution. The vehicle starts in `Looking`, where it keeps driving straight while polling the sensors, captures the initial right-side baseline distance, and waits for a sensor spike that indicates open space; once such a condition is observed, it sets `isParallel`, stores the measured drop distance, and transitions to `Detecting`. In `Detecting`, the controller checks whether the candidate space preserves the required depth and whether the car has travelled the remembered width distance; if those conditions fail, the controller abandons the candidate and returns to `Looking`. If the spot is accepted, the machine enters `Alignment`, where `isParallel` decides whether the vehicle performs the forward alignment needed for a reverse S-turn or the backing-away alignment needed for head-in parking, and then moves into `Park`. In `Park`, the controller executes the actual parking trajectory and finally enters `Stop`, where it uses ultrasonic difference and touch-sensor feedback to correct misalignment and maintain the proper curb or neighboring-car distance.

### 3. 逐句溯源

1. 句子 1：The HFVT controller is a high-level parking FSM that uses two right-side ultrasonic sensors together with front and rear touch sensors to supervise autonomous spot search and parking execution.
   对应摘录：A
2. 句子 2：The vehicle starts in `Looking`, where it keeps driving straight while polling the sensors, captures the initial right-side baseline distance, and waits for a sensor spike that indicates open space; once such a condition is observed, it sets `isParallel`, stores the measured drop distance, and transitions to `Detecting`.
   对应摘录：B
3. 句子 3：In `Detecting`, the controller checks whether the candidate space preserves the required depth and whether the car has travelled the remembered width distance; if those conditions fail, the controller abandons the candidate and returns to `Looking`.
   对应摘录：B
4. 句子 4：If the spot is accepted, the machine enters `Alignment`, where `isParallel` decides whether the vehicle performs the forward alignment needed for a reverse S-turn or the backing-away alignment needed for head-in parking, and then moves into `Park`.
   对应摘录：C
5. 句子 5：In `Park`, the controller executes the actual parking trajectory and finally enters `Stop`, where it uses ultrasonic difference and touch-sensor feedback to correct misalignment and maintain the proper curb or neighboring-car distance.
   对应摘录：C
