# Verilog-Based Solution for Multi-Vehicle Parking - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把停车场门禁认证、入口/出口检测、满位阻断和 `car_count` 更新写成了一个显式五态停车控制器，原文足以形成双 A 样本。

## 条目 1: Password-Gated Four-Slot Parking Controller

- 控制对象：智慧停车领域的多车位门禁与容量控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Verilog 的停车场控制器，用用户名/密码认证、入口/出口传感器和 `car_count` 变量共同管理四个停车位的放行、拒绝和离场更新。
- 判断：算。对象是实际停车基础设施控制器，原文明确给出 `IDLE / WAIT_PASSWORD / RIGHT_PASS / WRONG_PASS / STOP` 五个状态、认证变量、入口/出口传感器以及满位时的阻断规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，`3. IMPLEMENTATION OF PROPOSED ARCHITECTURE / Figure 4`，`paper_content.txt` 第 213-221、234-246 行
> The system to be designed is a very simple one and its purpose is to design an FSM using VHDL. The FSM has four states: A, B, C, and D.
>
> In the proposed multi-car parking system 5 states have been considered. They are IDLE, WAIT PASSWORD, RIGHT PASS, WRONG PASS, STOP. The main idea is that when a car enters the car parking arena, one has to give his username and password for the verification of entry.

#### 摘录 B

- 出处：第 4 页，`Figure 4: Proposed Parking System as FSM`，`paper_content.txt` 第 256-289 行
> uses two sensors known as sensor entrance and sensor exit. Initially when the car is in idle state, sensor_entrance is made to 1 and when right password is entered then sensor entrance is made to 0 ensuring that car is parked. When the car exits, the sensor_exit is made to 0 and the sensor_entrance is made to 1.
>
> a ‘car count’ is created which keeps tracks on how many cars can enter. So, in our project, the number of parking slots available is taken to be 4.
>
> As long as car parking count i.e., the car count, is less than 4, cars may be allowed to park. Once it reaches the limit of 4 the other entering cars are sent out at STOP point.

#### 摘录 C

- 出处：第 5-6 页，`4. RESULTS & DISCUSSION / 5. CONCLUSIONS`，`paper_content.txt` 第 359-367、414-424 行
> Figure 6 shows the block diagram of the parking system. In this PASS_1 and PASS_2 represents Password and User name. Back sensor and Front sensor represent the entry vehicle or exit vehicle. G_LED and R_LED represents the vehicle parking.
>
> This design aimed to solve the issue of car parking system by proposing a simulation-based approach with the feature of identifying the availability for multiple slots.
>
> Because the majority of the operation is hardware based, maintaining the network of incoming and outgoing cars is also relatively simple.

### 2. 基于原文整理后的自然语言描述

The proposed parking controller is a Verilog-based multi-slot gate system that combines password authentication with entry and exit sensing, so it does not merely count vehicles but explicitly decides whether an arriving car may enter the lot. Its main control chain is organized around five named states, `IDLE`, `WAIT_PASSWORD`, `RIGHT_PASS`, `WRONG_PASS`, and `STOP`, where valid credentials move the controller toward admission while invalid credentials keep the car in the rejection branch. The controller uses `sensor_entrance` and `sensor_exit` to distinguish arrival and departure, flipping the entrance-side status when a car is parked or leaves. On top of that state logic, the design introduces a `car_count` register for four parking slots, allows admission only while the count is below the slot limit, and diverts further incoming vehicles to the `STOP` point once the lot is full. The block-level implementation also ties authentication signals, front/back sensing, and red-green indicator outputs into the same parking controller, making the whole sample a concrete EFSM rather than a bare password checker.

### 3. 逐句溯源

1. 句子 1：The proposed parking controller is a Verilog-based multi-slot gate system that combines password authentication with entry and exit sensing, so it does not merely count vehicles but explicitly decides whether an arriving car may enter the lot.
   对应摘录：A, B, C
2. 句子 2：Its main control chain is organized around five named states, `IDLE`, `WAIT_PASSWORD`, `RIGHT_PASS`, `WRONG_PASS`, and `STOP`, where valid credentials move the controller toward admission while invalid credentials keep the car in the rejection branch.
   对应摘录：A
3. 句子 3：The controller uses `sensor_entrance` and `sensor_exit` to distinguish arrival and departure, flipping the entrance-side status when a car is parked or leaves.
   对应摘录：B
4. 句子 4：On top of that state logic, the design introduces a `car_count` register for four parking slots, allows admission only while the count is below the slot limit, and diverts further incoming vehicles to the `STOP` point once the lot is full.
   对应摘录：B
5. 句子 5：The block-level implementation also ties authentication signals, front/back sensing, and red-green indicator outputs into the same parking controller, making the whole sample a concrete EFSM rather than a bare password checker.
   对应摘录：C
