# PLC Based Washing Machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把液位定时、门锁联锁、三阶段洗涤序列和结束告警写成了完整 PLC 时序链，是工业自动化方向很标准的双 A `EFSM + T1` 样本。

## 条目 1: Timed soak-rinse-spin washing-machine controller

- 控制对象：工业自动化与离散制造领域的 PLC 洗衣机液位、门锁与三阶段洗涤顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 `PLC + inlet valve + outlet valve + DC motor + door lock switch + alarm` 实现的自动洗衣机顺序控制器。
- 判断：算。对象是实际洗衣机控制系统，原文给出了启动、液位设定、门锁校验、三阶段电机动作、排水和结束告警的完整时序逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`System Block Diagram`，`paper_content.txt` 第 48-67 行
> The three main components consists of inlet valve, motor control and the outlet valve which are controlled by the PLC ... PLC controls the different operations of the machine.(Soak, wash, rinse and spin).
>
> based on the water level set by the user, input valve remains ON for that particular time ... Door lock switch remains ON during machine operation ... if unexpectedly user opens the door ... whole operation of the machine stops.

#### 摘录 B

- 出处：第 1-2 页，`Algorithm`，`paper_content.txt` 第 71-95 行、第 102-107 行
> Start the washing machine by pressing the ‘START’ switch. Set the timer for the water level by pressing the ‘LEVEL SWITCH’. The inlet valve is on for that particular time set by the timer. Ensure that the ‘DOOR LOCK SWITCH’ is on.
>
> STAGE 1: Motor running -Forward direction for 5sec. -Reverse direction for 3sec. (This occurs for 2min.) -Forward direction for 60 sec. ... Outlet valve remains ‘ON’ for 60 sec.
>
> STAGE 2: ... Motor starts running -Forward direction for 60 sec ... Outlet valve remains ON for 60 sec. ... STAGE 3: ... -Forward direction for 120 sec ... Alarm starts ringing.

#### 摘录 C

- 出处：第 2 页，`Flow Chart`，`paper_content.txt` 第 113-135 行
> for level 1, timer is set for 15 sec and for level 4, timer is set for 60 sec ... PLC ensures that the door lock switch is ON ... motor starts rotating based on the algorithms set in stage 1 ... In this stage soaking and washing of clothes takes place. After completion of stage 1 drain valve opens ... In second stage again water is allowed ... In this stage rinsing of clothes takes place. In the third stage motor rotates in forward direction with no water in the drum ... After completion of all the three stages, motor stops and alarm goes ON.

### 2. 基于原文整理后的自然语言描述

The PLC washing-machine controller begins by waiting for a start command, a user-selected water-level timer, and a closed door-lock interlock before it enables any washing sequence. In Stage 1 it fills water to the selected level, runs the drum forward for 5 s and reverse for 3 s in repeated alternation for 2 minutes, then runs forward for 60 s and drains for 60 s. In Stage 2 it refills to the selected level, runs forward for 60 s, and drains again for 60 s to perform rinsing. In Stage 3 it runs the motor forward for 120 s with no water for spinning, then stops the motor and rings the alarm.

### 3. 逐句溯源

1. 句子 1：The PLC washing-machine controller begins by waiting for a start command, a user-selected water-level timer, and a closed door-lock interlock before it enables any washing sequence.
   对应摘录：A, B, C
2. 句子 2：In Stage 1 it fills water to the selected level, runs the drum forward for 5 s and reverse for 3 s in repeated alternation for 2 minutes, then runs forward for 60 s and drains for 60 s.
   对应摘录：B, C
3. 句子 3：In Stage 2 it refills to the selected level, runs forward for 60 s, and drains again for 60 s to perform rinsing.
   对应摘录：B, C
4. 句子 4：In Stage 3 it runs the motor forward for 120 s with no water for spinning, then stops the motor and rings the alarm.
   对应摘录：B, C
