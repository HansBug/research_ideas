# SMART TRAFFIC CONTROL - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟 / 协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把常规配时、密度优先、应急/安保远程放行和行人过街阈值触发整合进同一个 PLC 控制器，能形成一条完整的多模式交通灯控制链。

## 条目 1: Density-Priority Signal and Emergency Override Controller
- 控制对象：道路交通信号领域的密度优先与应急放行控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟、协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个基于 PLC 的四车道路口交通控制器，用常规定时相位、密度优先触发、Wi-Fi 应急放行和 FSR 行人阈值触发来管理车流与人流。
- 判断：算。对象是实际交通信号控制系统，原文明确给出了定时周期、密度触发条件、应急覆盖流程和行人分支，不是泛化的优化框架。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 14-23 行
> This paper depicts the idea of a modern traffic management system for life emergency and national security service vehicles. There are three main features in this project. First Density based traffic control management. Second to provide traffic-free path for life emergency vehicles (ambulance, fire brigade, and VVIP escorts). Third provides automation for Pedestrian cross over. All the above three features are controlled by PLC (Programmable Logic Controller). It is the main controller, which controls all the actions of the traffic system using ladder programming.

#### 摘录 B
- 出处：第 1-3 页，`Density based traffic control management / Table-1`，`paper_content.txt` 第 69-76 行、第 166-176 行、第 194-196 行
> Here, the sensors have been placed at a certain distance away from each signal. When the number of vehicles at the path exceeds a certain limit, and if the sensor receives signals continuously from the vehicles for more than 5 seconds, which here is a dense lane then the sensor inturn triggers the PLC from which the traffic signal controlling takes place. Therefore, the signal turns green at such dense lane.
>
> As in normal traffic conditions, a sequence of timer-based operation is being operated. ... the RED signal is being operated for 57 seconds. YELLOW is being operated for 3 seconds and the signal turns GREEN for 17 seconds and the sequence will be repeated for all the four lanes. It starts from lane 1,2,3,4 and keeps on repeating the sequence until the system is turned on.
>
> The signal turns GREEN at its respective lane. The GREEN signal is turned on for 17 seconds after this operation is completed, it jumps back to normal sequence.

#### 摘录 C
- 出处：第 1-3 页，`Provide a traffic-free path for emergency vehicles / national security vehicle`，`paper_content.txt` 第 80-89 行、第 199-217 行
> When an emergency vehicle is stuck in a traffic signal and is unable to reach its destiny in such cases the ambulance driver can access an android application authorized to him through this application the driver can switch the traffic signal to green and clear that particular lane. After which the signal is back to normal sequence. All the changes in the traffic signals are done via PLC.
>
> The signal changes to green for 17 seconds, allowing the emergency vehicle to pass the lane. Here an android application is used to send the signal to PLC with the help of the Wi-Fi module, which is only controlled by the authorized person (Driver). Once the operation is completed the signal gets back to the normal sequence.
>
> The authorized person will be sending the signal to the PLC with the help of the Wi-Fi module to clear particular lanes this is done prior by blocking all the other lanes so that the escorts service can clear the traffic and pass safely after the operation is being completed conventional traffic takes over.

#### 摘录 D
- 出处：第 1-3 页，`Automation for pedestrian cross over`，`paper_content.txt` 第 91-104 行、第 220-229 行
> Usually, to cross over the path huge number of pedestrian will have to wait for very long time. To overcome this problem FSR is being placed as a weight measuring equipment in this project. A platform is provided for the pedestrian to stand, a predetermined value of weight is programmed using Arduino Uno, whenever the value reaches beyond the predetermined weight, the Arduino controller activates the signal helping pedestrian cross-over instantaneously.
>
> A predetermined value is being set in the program using the Arduino Uno and measurement of weight is done with the help of FSR. Here in this project, FSR acts as a weight measuring equipment. Whenever the pedestrians occupies the platform their respective weight is measured by FSR and when it exceeds the predetermined value the PLC gets triggered and the signal turns to GREEN ... For the vehicles, the signal turns RED so that the pedestrian can cross over the path safely.

### 2. 基于原文整理后的自然语言描述

The PLC-controlled intersection runs a normal four-lane timing cycle in which each lane is served in order with `57 s` red, `3 s` yellow, and `17 s` green. When the IR sensor of a lane keeps detecting vehicles for more than `5 s`, the controller treats that lane as dense traffic, leaves the static sequence, gives that lane a dynamic `17 s` green phase, and then returns to the normal cycle. Authorized users can override the sequence through a Wi-Fi-linked Android application so an emergency lane receives green for `17 s`, and a security-service command can additionally block all other lanes to clear one selected lane before conventional traffic resumes. In parallel, an `FSR` pedestrian platform compares the measured weight against a predefined threshold, and once that threshold is exceeded the PLC turns vehicle signals red and enables the pedestrian crossing green.

### 3. 逐句溯源

1. 句子 1：The PLC-controlled intersection runs a normal four-lane timing cycle in which each lane is served in order with `57 s` red, `3 s` yellow, and `17 s` green.
   对应摘录：A, B
2. 句子 2：When the IR sensor of a lane keeps detecting vehicles for more than `5 s`, the controller treats that lane as dense traffic, leaves the static sequence, gives that lane a dynamic `17 s` green phase, and then returns to the normal cycle.
   对应摘录：B
3. 句子 3：Authorized users can override the sequence through a Wi-Fi-linked Android application so an emergency lane receives green for `17 s`, and a security-service command can additionally block all other lanes to clear one selected lane before conventional traffic resumes.
   对应摘录：C
4. 句子 4：In parallel, an `FSR` pedestrian platform compares the measured weight against a predefined threshold, and once that threshold is exceeded the PLC turns vehicle signals red and enables the pedestrian crossing green.
   对应摘录：D
