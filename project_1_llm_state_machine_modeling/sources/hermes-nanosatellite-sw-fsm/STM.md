# A finite state machine approach to nano-satellite SW design: the HERMES case study - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 HERMES 纳卫星的软件模式管理写成了 `LEOP / NOM / HSAFE` 三模监督器，并给出双 OBC 协同、time-tagged startup 和 safe fallback 逻辑。

## 条目 1: LEOP-NOM-HSAFE mission-software supervisor

- 控制对象：航空航天与飞行控制领域的 HERMES 纳卫星软件模式、计划调度与故障安全监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是航空航天与飞行控制领域的纳卫星 flight software supervisor，用于管理 LEOP 启动序列、schedule-driven nominal mission 和 failure-safe fallback。
- 判断：算。对象是实际 CubeSat 任务软件架构，原文明确给出三大模式、入退条件、time-tagged startup、dual-OBC 协同以及持续监测/故障回退逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 7-8 页，`4.2 HERMES software high-level design`，`paper_content.txt` 第 339-377 行
> As proposed in Sec. 3.3, the HERMES’ software high level structure is divided into three main modes, LEOP, NOM, and HSAFE ... The LEOP mode is the one aimed to boot the system, the ADCS system, and the main communication system, in order to rapidly obtain the first contact with ground ... NOM is the mode in which the platform performs attitude manoeuvres, commands the scientific payload, connects to ground with all the communication systems, and monitors the satellite critical parameters. On the other hand, the HSAFE mode is dedicated to avoid any waste of power, to fast communicate with ground, to control the ADCS to maximise the power generation or to handle non nominal situation ...
> the on-board software for the HERMES nano-satellites is executed by two different OBCs on the spacecraft, namely OBC-MAIN and OBC-ADCS ...
> The software running in each of the two OBCs, named SW-MAIN and SW-ADCS respectively, is structured according to its own FSM ... The two are interfaced by means of structured data commands and monitoring parameters, with a master-slave logical architecture ... both software’s FSM reflect the same architecture defined by the three main modes: LEOP, NOM and HSAFE. The only exception is the lack the LEOP mode for SW-ADCS ...
> HSAFE is used as the LEOP exit condition ... while the first schedule upload allows transition to NOM mode.
> ... the HERMES FDIR strategy is based on the concept of the SSAFE routines ... the SSAFE object is a continuous monitor, that runs during both the NOM and the HSAFE phase of the mission ... otherwise, request the entire system in HSAFE.

#### 摘录 B

- 出处：第 9 页，`4.3.1 HERMES SW-MAIN finite state machine / LEOP mode`，`paper_content.txt` 第 390-412 行
> As proposed in Sec 3.3 every operation in the SW-MAIN LEOP mode is time tagged. Nominally, the correct operational order is the one schematised in Fig. 4 ...
> At first, the OBC-MAIN board switches on and performs its automatic power-up and boot procedure.
> Once the OBC is operative, it waits until the end of the short slot 1, it boots the UHF board ... and then it deploys the two antennas. If the boot and deployment complete successfully, the UHF is commissioned and the board starts sending a beacon message to ground ...
> After the UHF operation, the LEOP mode boots the OBC-ADCS board.
> Then, if the boot is successful the software commands the ADCS to activate the detumbling mode ...
> When the time slot 2 is concluded, even if the ADCS has not managed to completely detumble the satellite, the SW commands the deployment of the spacecraft’s solar arrays ...
> Once this process is concluded, the OBC system automatically enters the HSAFE mode.

### 2. 基于原文整理后的自然语言描述

The HERMES flight software is organized around three macro-modes, `LEOP`, `NOM`, and `HSAFE`, which respectively handle one-shot launch-and-early-operation tasks, schedule-driven nominal activities, and power-positive survival with rapid ground-contact seeking. The spacecraft runs two coordinated FSMs, `SW-MAIN` and `SW-ADCS`, on two OBCs; they exchange structured commands and monitoring data in a master-slave architecture, and both follow the same mode logic except that `SW-ADCS` omits `LEOP`. `LEOP` is explicitly time tagged: the software boots OBC-MAIN, waits for the first slot, boots UHF, deploys antennas, starts beacons, boots OBC-ADCS, commands detumbling, and then deploys the solar arrays at the second slot even if detumbling is not yet complete. After this one-shot sequence the system automatically enters `HSAFE`, and transition to `NOM` is allowed only after ground uploads the first schedule during a communication opportunity. In parallel with the mode logic, the `SSAFE` monitors keep checking vital parameters during `NOM` and `HSAFE` and can attempt simple recovery or request a full transition back to `HSAFE`, so the case is a `T1` parallel EFSM rather than a flat mode list.

### 3. 逐句溯源

1. 句子 1：The HERMES flight software is organized around three macro-modes, `LEOP`, `NOM`, and `HSAFE`, which respectively handle one-shot launch-and-early-operation tasks, schedule-driven nominal activities, and power-positive survival with rapid ground-contact seeking.
   对应摘录：A
2. 句子 2：The spacecraft runs two coordinated FSMs, `SW-MAIN` and `SW-ADCS`, on two OBCs; they exchange structured commands and monitoring data in a master-slave architecture, and both follow the same mode logic except that `SW-ADCS` omits `LEOP`.
   对应摘录：A
3. 句子 3：`LEOP` is explicitly time tagged: the software boots OBC-MAIN, waits for the first slot, boots UHF, deploys antennas, starts beacons, boots OBC-ADCS, commands detumbling, and then deploys the solar arrays at the second slot even if detumbling is not yet complete.
   对应摘录：B
4. 句子 4：After this one-shot sequence the system automatically enters `HSAFE`, and transition to `NOM` is allowed only after ground uploads the first schedule during a communication opportunity.
   对应摘录：A, B
5. 句子 5：In parallel with the mode logic, the `SSAFE` monitors keep checking vital parameters during `NOM` and `HSAFE` and can attempt simple recovery or request a full transition back to `HSAFE`, so the case is a `T1` parallel EFSM rather than a flat mode list.
   对应摘录：A
