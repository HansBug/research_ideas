# Auto Railway Gate - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 RFID 认证、距离阈值、障碍重开和 2 秒复位写成了完整道口控制闭环，是铁路平交口方向质量很高的双 A `EFSM + T1` 样本。

## 条目 1: RFID-verified obstacle-safe railway gate supervisor

- 控制对象：轨道交通与铁路控制领域的 RFID 认证、距离阈值与障碍重开道口门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个由 `RFID + ultrasonic + IR sensor + servo gate + LED + buzzer` 构成的铁路道口自动门控监督器。
- 判断：算。对象是实际平交口门控控制系统，原文直接给出了空闲、列车确认、接近检测、关闸、障碍重开、列车离开和复位等控制步骤，并附了阈值与代码级动作。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 24-35 行
> The system utilizes an ultrasonic sensor to detect the distance of an approaching train, an RFID module to authenticate train presence, and an IR sensor to check for obstacles on the track. ... The gate only closes when both the ultrasonic and RFID confirmations are received ... An additional safety feature is implemented to slightly reopen the gate if an obstacle is detected during closure.

#### 摘录 B

- 出处：第 3 页，`Proposed System`，`paper_content.txt` 第 133-141 行
> The system uses an RFID module to verify the authenticity of approaching trains and an ultrasonic sensor to determine their proximity. Once both conditions are met, the gate begins its closure sequence. An IR sensor is used to detect any obstacle at the gate ... If an obstacle is detected during closure, the gate opens slightly ... The system is designed to operate autonomously and reset once the train has passed.

#### 摘录 C

- 出处：第 6-8 页，`Methodology / Sample Code`，`paper_content.txt` 第 256-294 行、第 384-402 行
> The gate remains open by default, with the green LED turned on. ... When a valid RFID tag is scanned ... If the train’s distance is within a predefined threshold (e.g., < 50 cm) ... Upon both RFID confirmation and proximity detection, the system activates a buzzer and switches the red LED on ... If detected, the gate opens slightly ... If no obstacle is present, the gate closes fully ...
>
> if (rfidDetected) { if (distance < 50) { ... digitalWrite(redLED, HIGH); digitalWrite(greenLED, LOW); if (digitalRead(irPin) == LOW) { ... gate.write(45); } else { ... gate.write(0); } } }

#### 摘录 D

- 出处：第 9 页，`Result`，`paper_content.txt` 第 430-449 行
> The system consistently responded only when a valid RFID tag was scanned and the train was detected within a specified distance. ... In situations where an obstacle was detected while the gate was closing, the system successfully reopened the gate slightly ... After the train moved away ... and remained away for a continuous period of two seconds, the system reopened the gate, turned off the red LED, and reactivated the green LED ...

### 2. 基于原文整理后的自然语言描述

The railway-gate controller begins in an idle-open state with the green LED on while it monitors RFID authentication, train distance, and gate obstacles. When a valid RFID tag is read and the ultrasonic distance falls below 50 cm, the system enters train-approach handling, activates the buzzer, turns on the red warning signal, and prepares the gate-closing sequence. If the IR sensor detects an obstacle during closure, the servo reopens the gate slightly and keeps the warning state active until the path is clear. Otherwise the servo closes the gate fully and the controller keeps monitoring train departure. After the train moves beyond the threshold for 2 continuous seconds, the controller reopens the gate, turns red off, restores green, and resets to idle.

### 3. 逐句溯源

1. 句子 1：The railway-gate controller begins in an idle-open state with the green LED on while it monitors RFID authentication, train distance, and gate obstacles.
   对应摘录：B, C
2. 句子 2：When a valid RFID tag is read and the ultrasonic distance falls below 50 cm, the system enters train-approach handling, activates the buzzer, turns on the red warning signal, and prepares the gate-closing sequence.
   对应摘录：A, B, C
3. 句子 3：If the IR sensor detects an obstacle during closure, the servo reopens the gate slightly and keeps the warning state active until the path is clear.
   对应摘录：A, B, C, D
4. 句子 4：Otherwise the servo closes the gate fully and the controller keeps monitoring train departure.
   对应摘录：B, C
5. 句子 5：After the train moves beyond the threshold for 2 continuous seconds, the controller reopens the gate, turns red off, restores green, and resets to idle.
   对应摘录：C, D
