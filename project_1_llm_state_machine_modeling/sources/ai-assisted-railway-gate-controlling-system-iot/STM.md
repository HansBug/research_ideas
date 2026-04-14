# Design and development of artificial intelligence assisted railway gate controlling system using internet of things - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把铁路道口门控的到车检测、5 秒闭门/开门、障碍检测和 GSM 报警串成了一条完整的工程控制链。

## 条目 1: IR-Triggered Gate Close-Open and Obstacle Alert Controller

- 控制对象：轨道交通与铁路控制领域的道口自动门控与障碍预警控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于双侧红外传感器、超声传感器、LCD、蜂鸣器、直流电机和 GSM 的铁路平交道口自动门控系统。
- 判断：算。对象是真实道口控制器，原文明确给出了到车触发、关门动作、离车开门、障碍检测和短信告警的有序流程。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，`Launch of Train Service`，`paper_content.txt` 第 279-285 行
> "IR1 will alert"

- 证据说明：该段说明 IR1 检到来车后，微控制器会先鸣铃，再驱动门控执行机构闭门。

#### 摘录 B

- 出处：第 4 页，`Launch of Train Service / Securing the Rails`，`paper_content.txt` 第 286-297 行
> "for 5 seconds"

- 证据说明：原文分别给出关门时电机顺时针运行 5 秒、开门时反转 5 秒的局部定时动作，并配合 LCD 显示状态。

#### 摘录 C

- 出处：第 4-5 页，`Identifying Dangers ... / Safeguards against Collision`，`paper_content.txt` 第 304-321 行
> "text message"

- 证据说明：超声传感器仅在闸门关闭后启用，用于检测门间障碍；一旦发现阻塞，控制器通过 GSM 向火车司机发送告警短信。

### 2. 基于原文整理后的自然语言描述

The proposed level-crossing controller uses two infrared sensors placed on both sides of the track to detect train arrival and departure and drive a gate-control sequence automatically. When `IR1` detects an incoming train, the controller activates the warning bell, drives the DC motor clockwise for `5 seconds`, closes the gate, and reports the close event on the LCD. After the train leaves, `IR2` triggers the reverse branch, so the controller sounds the buzzer again, runs the motors in reverse for `5 seconds`, and reopens the gate. The obstacle-protection logic is not separate from the gate controller: once the gates are closed, an ultrasonic sensor checks whether a vehicle is trapped between them, and if an obstruction is detected, the GSM unit sends an alert message to the locomotive pilot.

### 3. 逐句溯源

1. 句子 1：The proposed level-crossing controller uses two infrared sensors placed on both sides of the track to detect train arrival and departure and drive a gate-control sequence automatically.
   对应摘录：A, B
2. 句子 2：When `IR1` detects an incoming train, the controller activates the warning bell, drives the DC motor clockwise for `5 seconds`, closes the gate, and reports the close event on the LCD.
   对应摘录：A, B
3. 句子 3：After the train leaves, `IR2` triggers the reverse branch, so the controller sounds the buzzer again, runs the motors in reverse for `5 seconds`, and reopens the gate.
   对应摘录：B
4. 句子 4：The obstacle-protection logic is not separate from the gate controller: once the gates are closed, an ultrasonic sensor checks whether a vehicle is trapped between them, and if an obstruction is detected, the GSM unit sends an alert message to the locomotive pilot.
   对应摘录：C
