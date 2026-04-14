# Automatic Door Control Using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `检测来人 -> 开门 -> 保持开启 -> 反转关门 -> 闭位停机` 链条、限位开关和正反转互锁一起写清楚了，足以形成双 A 门控样本。

## 条目 1: Presence-detected open-hold-close door controller

- 控制对象：楼宇机电领域的自动门开闭与方向联锁控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：资源互斥
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `PLC + IR/proximity sensor + motor + relay + limit switch` 的自动门控制系统，用传感触发门体开启、定时保持和反转关闭。
- 判断：算。对象是实际自动门控制器，原文不只给硬件清单，还明确写出输入触发、开启保持、关闭条件、限位停机和电机正反转互锁。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Introduction`，`paper_content.txt` 第 40-58 行
> In this system, sensors such as infrared (IR) or motion sensors are installed near the entrance to detect a person approaching the door. When a person is detected, the sensor sends a signal to the PLC. The PLC processes this input according to the programmed instructions and activates a motor to open the door. After a preset time delay or when no presence is detected, the PLC automatically sends a command to close the door. To ensure safe operation, interlocking logic is included in the PLC program. This prevents the motor from running in both forward and reverse directions simultaneously.

#### 摘录 B

- 出处：第 2-3 页，`Methodology / Result`，`paper_content.txt` 第 73-92、174-195 行
> The input section includes sensors such as IR or proximity sensors to detect human presence, while the control section consists of the PLC that processes input signals and executes the programmed logic. The output section includes the motor, relays, limit switches, and the mechanical door mechanism. ... Limit switches are fixed at fully open and closed positions to prevent over-travel. The PLC is programmed using ladder logic to open the door when motion is detected, hold it open for a preset time, and then close it automatically.
>
> Upon receiving this signal, the PLC energizes the motor to open the door. The door opens smoothly and stops precisely at the fully open ... the PLC starts a timer, keeping the door open for a preset duration to allow safe passage. Once the timer completes, the PLC reverses the motor to close the door. The door closes smoothly and stops at the fully closed position when the closed limit switch is activated. ... The interlock logic ensured that the motor never ran in both directions simultaneously.

### 2. 基于原文整理后的自然语言描述

The automatic door controller waits in a closed-and-monitoring condition until the IR or proximity sensor detects a person approaching the entrance. Once that input arrives, the PLC energizes the motor in the opening direction and keeps driving the door until the fully open position is reached. After the door reaches its open limit, the controller starts a preset hold timer so the doorway remains available for passage. When the timer expires, or when presence is no longer detected, the PLC reverses the motor, closes the door, and stops the motion at the closed limit switch. Throughout the cycle, interlocking logic prevents the forward and reverse drive paths from being active at the same time.

### 3. 逐句溯源

1. 句子 1：The automatic door controller waits in a closed-and-monitoring condition until the IR or proximity sensor detects a person approaching the entrance.
   对应摘录：A, B
2. 句子 2：Once that input arrives, the PLC energizes the motor in the opening direction and keeps driving the door until the fully open position is reached.
   对应摘录：A, B
3. 句子 3：After the door reaches its open limit, the controller starts a preset hold timer so the doorway remains available for passage.
   对应摘录：B
4. 句子 4：When the timer expires, or when presence is no longer detected, the PLC reverses the motor, closes the door, and stops the motion at the closed limit switch.
   对应摘录：A, B
5. 句子 5：Throughout the cycle, interlocking logic prevents the forward and reverse drive paths from being active at the same time.
   对应摘录：A, B
