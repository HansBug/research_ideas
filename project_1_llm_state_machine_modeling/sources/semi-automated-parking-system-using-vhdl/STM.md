# Semi-Automated Parking System Using VHDL - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然篇幅不长，但明确写出了 `INACTIVE / IDLE / WAIT_PASSWORD / RIGHT_PASS / WRONG_PASS / STOP` 六态链，以及前后传感器、密码校验和 `4` 个周期等待语义，足以形成双 A 的停车门禁控制样本。

## 条目 1: Password-Gated Semi-Automated Parking Gate FSM

- 控制对象：智慧停车与车位管理领域的密码门禁与跟车阻塞停车控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向停车场入口门禁的 Moore 型停车控制器，用前后传感器、密码校验、红绿灯提示和等待周期来管理车辆放行、拦停与复位。
- 判断：算。对象是实际停车门禁控制系统，不是 GUI 或软件流程；原文直接给出命名状态、传感器触发条件、密码判定路径和 `4` 周期等待，因此能稳定整理成 FSM 样本。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 21-30 行
> The Semi-automated auto/bike parking system ... makes effects easier ... The proposed system uses a VHDL based system in an organized manner using FSM methodology.

#### 摘录 B

- 出处：第 3 页，Section 3.2 `Finite State Machine`，`paper_content.txt` 第 131-141 行
> Originally, the FSM is in INACTIVE state until the reset button is active. And also, it's in IDLE state. However, FSM is switched to WAIT_PASSWORD state and it stay for 4 cycles for a user to enter the password ... if the word is correct ... state machine turns to RIGHT_PASS state ... If not, FSM turns to WRONG_PASS state ... When the current motor vehicle gets into the parking area ... the FSM is switched to STOP state ... After the motor vehicle passes the entry ... the FSM comes to IDLE state.

#### 摘录 C

- 出处：第 4-6 页，Section 4 `Simulation Results` 与 Section 5 `Conclusions`，`paper_content.txt` 第 170-176、185-190、204-209 行
> When Reset_n is in off state; the entire system is in INACTIVE state.  
> When Reset_n is '1' and front_sensor is '1'; it changes it's state from IDLE to WAIT_PASSWORD and then it checks password if it is correct, it moves to RIGHT_PASS state ...  
> If both front_sensor and back_sensor are '1' and the password is also correct; the state moves from WAIT_PASSWORD to RIGHT_PASS and immediately moves to STOP state.  
> Moore machine is used to design automatic secured car parking system ... Different states of designed and implemented Moore FSM machine are discussed.

### 2. 基于原文整理后的自然语言描述

The proposed parking controller is an explicit Moore FSM for a semi-automated gate-access workflow rather than a generic parking-management application. It starts from `INACTIVE`, settles in `IDLE` after reset, and moves to `WAIT_PASSWORD` when the front sensor detects an arriving vehicle, where the user is given four cycles to enter the password. A correct password drives the machine to `RIGHT_PASS` and opens the gate with green indication, while an incorrect password drives it to `WRONG_PASS` with red indication until a valid password is entered. If the vehicle is already entering and both front and rear sensors are active, the controller moves into `STOP` to hold the following vehicle, and once the current vehicle clears the entry the FSM returns to `IDLE`.

### 3. 逐句溯源

1. 句子 1：The proposed parking controller is an explicit Moore FSM for a semi-automated gate-access workflow rather than a generic parking-management application.
   对应摘录：A, C
2. 句子 2：It starts from `INACTIVE`, settles in `IDLE` after reset, and moves to `WAIT_PASSWORD` when the front sensor detects an arriving vehicle, where the user is given four cycles to enter the password.
   对应摘录：B, C
3. 句子 3：A correct password drives the machine to `RIGHT_PASS` and opens the gate with green indication, while an incorrect password drives it to `WRONG_PASS` with red indication until a valid password is entered.
   对应摘录：B, C
4. 句子 4：If the vehicle is already entering and both front and rear sensors are active, the controller moves into `STOP` to hold the following vehicle, and once the current vehicle clears the entry the FSM returns to `IDLE`.
   对应摘录：B, C
