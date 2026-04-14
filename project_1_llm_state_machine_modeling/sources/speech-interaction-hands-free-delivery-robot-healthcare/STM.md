# Speech Interaction to Control a Hands-Free Delivery Robot for High-Risk Health Care Scenarios - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把语音触发、房间确认、UV-C 消杀、到房间播报、取件确认、返回 home 与 error reset 串成完整配送 supervisor，原文锚点非常集中，能稳定支持双 A 条目。

## 条目 1: Speech-guided delivery-and-return supervisor

- 控制对象：高风险护理场景中语音驱动配送机器人的任务监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个根据语音命令、房间号解析、yes/no 确认、UV-C 消杀、到房间播报与取件确认来推进配送闭环的移动机器人监督控制器。
- 判断：算。对象是真实配送机器人而不是语音识别工具；原文明确给出命令识别、确认、消杀、导航、投递确认、返回和 error reset 的完整状态链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，Section `0.5.2 Intent Parsing`，`paper_content.txt` 第 176-198 行
> The main type of intent parsing that occurred was detecting when a user intended to initiate a delivery, and then parsing out the location of the delivery. The first step ... was to ensure a recognized sentence started with the word “robot” ... all the delivery sentences contained the phrase “deliver this package to” ... The first confirmation happened after the selected room identifier was parsed ... If the sentence contained confirmation statements such as “yes” the robot then performed the delivery ... otherwise the system continued listening for a confirmation or rejection.

#### 摘录 B

- 出处：第 4 页，Section `0.6 State Machine for Human-Robot Interaction`，`paper_content.txt` 第 207-231 行
> All of the components demonstrated so far were connected together into a complete system using a state machine ... Once the robot has successfully parsed a delivery sentence the state machine advances to the confirmation state ... Once the robot received verbal confirmation ... the robot sanitized itself by navigating into the UV-c sanitization pod. Once the robot had waited for the correct amount of time in the pod it navigated to the coordinates for the target room ... After a time delay to account for the removal of the package the robot asked for confirmation that the package has been removed ... the state machine entered the final state, in which the robot navigated back to the home position.

#### 摘录 C

- 出处：第 5-6 页，Figure 1 与 Section `0.7 Experiment 1`，`paper_content.txt` 第 253-256, 285-289 行
> Delivery was triggered and confirmed by speech interaction between a visitor and the robot. The robot navigated to the delivery target waypoint, with a stop to clean the item with UV-C light. At the target waypoint the robot used speech to confirm delivery and then returned to its home position.
>
> The robot then navigated into the sanitization box, waited for the correct amount of time, and then autonomously navigated to lab T. Once the package was removed and the robot received verbal confirmation it returned to the initial starting point in lab C.

### 2. 基于原文整理后的自然语言描述

The delivery robot begins in a command-recognition stage where it only accepts speech addressed to `robot`, extracts the destination from the fixed phrase `deliver this package to ...`, and stores the selected room as the control variable for the mission. After a room identifier is parsed, the supervisor enters a confirmation stage, repeats the room number through TTS, and waits for either acceptance or rejection; if the command is unclear, the dedicated error state resets the interaction back to the initial command-recognition state. Once the room is confirmed, the controller sends the room id to the navigation stack, drives into the UV-C sanitization pod, waits there for the required dwell time, and then navigates to the target waypoint. At the destination, the robot announces that the package should be removed, waits long enough for removal, asks for explicit delivery confirmation, and only then transitions to the final return-home state. Taken together, the paper exposes a full EFSM-style mission chain whose guarded progress depends on parsed room data, yes/no confirmations, and two local timing segments: sanitization dwell and package-removal delay.

### 3. 逐句溯源

1. 句子 1：The delivery robot begins in a command-recognition stage where it only accepts speech addressed to `robot`, extracts the destination from the fixed phrase `deliver this package to ...`, and stores the selected room as the control variable for the mission.
   对应摘录：A
2. 句子 2：After a room identifier is parsed, the supervisor enters a confirmation stage, repeats the room number through TTS, and waits for either acceptance or rejection; if the command is unclear, the dedicated error state resets the interaction back to the initial command-recognition state.
   对应摘录：A, B
3. 句子 3：Once the room is confirmed, the controller sends the room id to the navigation stack, drives into the UV-C sanitization pod, waits there for the required dwell time, and then navigates to the target waypoint.
   对应摘录：B, C
4. 句子 4：At the destination, the robot announces that the package should be removed, waits long enough for removal, asks for explicit delivery confirmation, and only then transitions to the final return-home state.
   对应摘录：B, C
5. 句子 5：Taken together, the paper exposes a full EFSM-style mission chain whose guarded progress depends on parsed room data, yes/no confirmations, and two local timing segments: sanitization dwell and package-removal delay.
   对应摘录：A, B, C
