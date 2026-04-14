# Design and application of the control system of mine damper and window - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把矿井双风门通行、`3 s` 延迟开门、`15 s` 超时关门、夹人回开、双门互锁和百叶风窗角度调节写成一条完整的现场控制链，足以支撑双 A 样本。

## 条目 1: Timed dual-damper passage and louver-angle controller

- 控制对象：过程与环境控制领域的矿井双风门通行与风窗角度调节控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个矿井通风联络巷的风门/风窗控制器，用双侧红外、气缸、互锁与声光报警把“通行开门-超时关门-防夹回开-对向门抑制-风量调节”组织成实际运行逻辑。
- 判断：算。对象是真实矿井通风设施控制系统，不是设备简介；原文明确给出了八步通行流程、`3 s` 与 `15 s` 时序、互锁与报警逻辑，以及风窗 `0-90°` 角度调节。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract / Design of control system`，`paper_content.txt` 第 10-20、43-48 行
> In view of this problem, the relevant theories and applications of the damper window control system are studied ... the flow of personnel or vehicles passing through the damper and the control system of the damper window are designed by using micro-control technology ... Under the movement of the cylinder and the air motor, the control of two air doors and wind Windows is realized.

#### 摘录 B

- 出处：第 2 页，`2.2 Software Design`，`paper_content.txt` 第 76-100 行
> Step 1: Pedestrians or vehicles first trigger the infrared sensor on the outside of the damper;
>
> Step 2: Wait 3 seconds, the cylinder extends the driving rod, open the damper;
>
> Step 3: After the damper is opened in place, wait for pedestrians or vehicles to pass;
>
> Step 4: If the pedestrian or vehicle triggers the inside infrared ... close the damper ... Otherwise, after 15 seconds, execute the throttle closing procedure. At the same time, if any infrared is triggered during the throttle closing, stop closing the door immediately and return to the second step;
>
> ... Step 6: Wait 3 seconds, the cylinder extends the driving rod, open another damper;
>
> ... Step 8: If the pedestrian or vehicle triggers the outside infrared ... close the damper ... Otherwise, after 15 seconds, perform the damper closing procedure.

#### 摘录 C

- 出处：第 2 页，`2.2 Software Design`，`paper_content.txt` 第 93-100 行
> If the two air doors are opened at the same time, it will lead to abnormal air flow in the connecting lane. Therefore, under the original mechanical lock device, an electrical lock is added, accompanied by sound and light alarm prompts, to prevent workers from misoperating, to avoid the occurrence of airflow disorder, resulting in the failure of the ventilation system.
>
> Compared with the damper, the control of the wind window is relatively simple, and only the opening Angle of the shutter can be adjusted ... When the air motor is turning, the opening Angle of the shutter is increased, and the opening Angle of the shutter is reduced when it is reversed.

#### 摘录 D

- 出处：第 3 页，`3. Application effect analysis`，`paper_content.txt` 第 112-131、143-148 行
> when A pedestrian or vehicle is near the damper A, the infrared sensor outside the damper detects the traffic signal ... the damper automatically opens ... If the damper is fully opened, change to the "Damper is open, please pass safely" prompt ... At the same time, close the damper B ...
>
> When pedestrians or vehicles safely pass through the damper and trigger the infrared sensor on the inside side of the damper, the damper automatically closes ...
>
> At the same time, if it is necessary to pass through the damper B ... the damper automatically opens ... and the damper A is closed.
>
> ... the opening Angle of the louver can be adjusted directly through the button, and remote adjustment can be realized through the underground ring network.

### 2. 基于原文整理后的自然语言描述

The mine ventilation controller manages a paired-damper passage and a louver window in the liaison lane by combining infrared sensing, pneumatic actuation, electrical interlocking, and networked monitoring. When a pedestrian or vehicle reaches the outside of damper `A`, the outer infrared sensor triggers the controller, which waits `3 s` and then extends the cylinder to open the door while the opposite damper is forced closed. If the user clears the inner infrared zone, the controller retracts the cylinder and closes damper `A`; otherwise it starts a `15 s` timeout close sequence, and any infrared retrigger during closing immediately aborts the close and returns the logic to the reopen step. The same timed sequence is mirrored for damper `B`, so the full passage is a bidirectional two-door cycle with mutual exclusion and sound-light prompts that prevent both dampers from being open simultaneously. In parallel, the controller drives the louver window motor forward or reverse to change the shutter angle between `0` and `90` degrees, which provides both local and remote air-volume regulation alongside the timed passage logic.

### 3. 逐句溯源

1. 句子 1：The mine ventilation controller manages a paired-damper passage and a louver window in the liaison lane by combining infrared sensing, pneumatic actuation, electrical interlocking, and networked monitoring.
   对应摘录：A, C, D
2. 句子 2：When a pedestrian or vehicle reaches the outside of damper `A`, the outer infrared sensor triggers the controller, which waits `3 s` and then extends the cylinder to open the door while the opposite damper is forced closed.
   对应摘录：B, D
3. 句子 3：If the user clears the inner infrared zone, the controller retracts the cylinder and closes damper `A`; otherwise it starts a `15 s` timeout close sequence, and any infrared retrigger during closing immediately aborts the close and returns the logic to the reopen step.
   对应摘录：B
4. 句子 4：The same timed sequence is mirrored for damper `B`, so the full passage is a bidirectional two-door cycle with mutual exclusion and sound-light prompts that prevent both dampers from being open simultaneously.
   对应摘录：B, C, D
5. 句子 5：In parallel, the controller drives the louver window motor forward or reverse to change the shutter angle between `0` and `90` degrees, which provides both local and remote air-volume regulation alongside the timed passage logic.
   对应摘录：A, C, D
