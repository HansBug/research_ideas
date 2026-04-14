# A Secure Automated Elevator Management System and Pressure Sensor based Floor Estimation for Indoor Mobile Robot Transportation - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把机器人乘梯任务写成了“呼梯/选层/测层/判门/异常恢复”的分层控制链，既有主流程也有外部与内部两套错误处理分支，足以稳定支撑 `HSM + T0` 双 A 样本。

## 条目 1: Robot Elevator Request, Floor-Estimation, and Recovery Supervisor
- 控制对象：面向室内移动机器人的自动电梯管理与乘梯恢复控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个让移动机器人安全使用楼宇电梯的高层监督控制器，负责呼叫电梯、根据任务状态选择目标楼层、在轿厢内估计当前楼层、识别门状态，并在失败时执行外部/内部恢复分支。
- 判断：算。对象是实际 elevator handling supervisor，不是纯传感算法或流程说明；原文把 `AEMS`、floor estimation、door-status checking 和 inside/outside error handling 串成了明确的控制链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 17-35 行
> In this paper, a secure elevator handl ing system is presented to enable a flexible movement of wheeled mobile robot s among laboratories distributed in different floor s. The automate d handling system consists mainly of an ADAM module which has the ability to call the elevator to the robot’s current floor and to request the destination floor. The LPS25HP pressure sensor attached to an STM32F411 microcontroller is utilized as a height measurement system to estimate the robot’s current floor i nside the elevator. The ultrasonic sensor is used to recognize the elevator’s door status ... An error handling management system is utilized to guarantee a stable automated elevator management system performance.

#### 摘录 B
- 出处：第 3-4 页，`Automated Elevator Management System`，`paper_content.txt` 第 302-340 行
> The AEMS calls the elevator to the robot’s current floor when the mobile robot needs the elevator to move to another floor during a transportation task ... Inside the elevator, the MFS needs a logical solution to specify the destination floor. At this level, the movement core depends on the transportation task status (Grasp Position Done, Place Position Done, and Charge Position Done) to determine the current destination ... The reconnection function is developed to handle the weakness of the Wi-Fi signal ... In case of missing data, the function closes the socket to AE and then initializes the connection again till a stable connection is realized.

#### 摘录 C
- 出处：第 5-6 页，`Floor estimation / Elevator Handling Error Management System`，`paper_content.txt` 第 450-515 行
> During a multi-floor transportation tasks, the ultrasonic sensor is used to recognize the elevator door’s status. When the destination floor matches the estimated robot’s current floor and the elevator’s door status is recognized as “open”, the robot leaves the elevator to complete the transportation task process.
>
> The EHS classifies the error according to its appearance space as either outside or inside elevator error handling ... If the mobile robot fails to reach the required elevator button pushing area accurately ... the position and orientation correction function checks the robot's position after movement and tries to correct it three times ... If previous attempts have failed, the EHS selects the AEMS over the Wi-Fi socket to open the door.
>
> The error handling system inside the elevator starts by monitoring whether or not the destination floor has been reached ... If it does not reach the destination floor after a specified number of attempts, the MFS sends a warning alarm ... another warning alarm is sent ... if the door is still closed ... if the floor reached matches the required destination floor ... the error handling system returns the robot back to the elevator and chooses the destination floor again.

### 2. 基于原文整理后的自然语言描述

The robot-elevator supervisor organizes multi-floor transportation as a layered control chain rather than as a single button-press action. At the mission layer, the `AEMS` first calls the elevator to the robot’s current floor and selects the internal destination button according to the task status, such as grasp, place, or charge completion. Inside the cabin, a pressure-sensor floor estimator and an ultrasonic door-status reader jointly decide when the robot has reached the correct floor and may leave, requiring both “destination floor matched” and “door open” before exit is allowed. Around that nominal path, the `EHS` adds two nested recovery branches: outside the elevator it retries pose correction and button pressing before falling back to Wi-Fi door opening, while inside the elevator it monitors repeated failure to reach the destination, repeated closed-door conditions, and wrong-floor landmark detections, then either reselects the destination or escalates the fault to the higher-level controller.

### 3. 逐句溯源

1. 句子 1：The robot-elevator supervisor organizes multi-floor transportation as a layered control chain rather than as a single button-press action.
   对应摘录：A, C
2. 句子 2：At the mission layer, the `AEMS` first calls the elevator to the robot’s current floor and selects the internal destination button according to the task status, such as grasp, place, or charge completion.
   对应摘录：A, B
3. 句子 3：Inside the cabin, a pressure-sensor floor estimator and an ultrasonic door-status reader jointly decide when the robot has reached the correct floor and may leave, requiring both “destination floor matched” and “door open” before exit is allowed.
   对应摘录：A, C
4. 句子 4：Around that nominal path, the `EHS` adds two nested recovery branches: outside the elevator it retries pose correction and button pressing before falling back to Wi-Fi door opening, while inside the elevator it monitors repeated failure to reach the destination, repeated closed-door conditions, and wrong-floor landmark detections, then either reselects the destination or escalates the fault to the higher-level controller.
   对应摘录：C
