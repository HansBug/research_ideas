# Application of Formal Verification to the Lane Change Module of an Autonomous Vehicle - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把换道模块中的 `Lateral State Manager` 直接写成七位置 EFSM，并把 update 周期、enter/during 方法和 timer 计数规则都讲清楚了。

## 条目 1: Seven-location lateral state manager for lane change

- 控制对象：自动驾驶车辆换道模块的横向状态管理器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个自动驾驶换道控制器里的 `Lateral State Manager (LSM)`，用七个离散位置跟踪当前换道进程，并在每次 planner 更新时执行一次状态推进。
- 判断：算。对象是实际道路车辆换道模块的主状态机，原文明确给出了初始态、请求态、完成态、单周期 update 机制以及三个 timer 变量的更新约束。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，`A. Planner / B. Lateral state manager`，`paper_content.txt` 第 323-353 行
> The lane change module is implemented with the use of several classes ... the class Planner is considered. Planner has the responsibility to decide and control how the lane change should be done. Planner is cyclically updated at a high frequency with the current status of the vehicle, surrounding traffic situation, and current reference signals.
>
> ... the Lateral State Manager (LSM) has to keep track of where in the process of lane change the car currently is, and thus it is implemented as a state machine ... This state machine consists of seven locations, two of which are NoRequest and Finished. ... When no lane change is requested LSM should be in NoRequest, which is also the initial state. Once a request comes, LSM moves to S1, and from there to either S2, S3 or back to NoRequest depending on the situation. Finally, when the lane change is done LSM will be in Finished and from there, on the next update, transit back to NoRequest.

#### 摘录 B

- 出处：第 5 页，`C. Implementation`，`paper_content.txt` 第 365-397 行
> LSM consists of three different types of methods. The first type ... is called updateState. This method is called from Planner every time that Planner is updated. The purpose of the updateState method is to call the current state's duringUpdate method ... Before the duringUpdate method terminates, it will either change the state or keep the current state. ... If the state is changed by the duringUpdate method, the new state's enterUpdate method is called ... In contrast to the duringUpdate methods which are executed repeatedly on each update while the state stays current, the enterUpdate methods are executed only once when the transition into the state occurs.
>
> Modeling LSM's 223 lines of MATLAB-code in Supremica was done manually ... This resulted in a single EFSM with 75 locations, 123 transitions, and 17 variables ... and a 7-valued variable holding the current location.

#### 摘录 C

- 出处：第 5-6 页，`V. Specifications`，`paper_content.txt` 第 409-448 行
> LSM receives requests from Planner to change lane to either left or right. ... the value of an internal variable, direction, and the incoming request parameter could be different from each other for two consecutive updates.
>
> In LSM there are three variables that are used as timers: timer1, timer2 and timer3. These “timers” are really counters that keep track of during how many consequtive updates certain Boolean variables have been true ... When the value is true, the timer should be incremented on each update.
>
> ... If two timer increments occur without an intermediate update the specification blocks.

### 2. 基于原文整理后的自然语言描述

The lane-change module is driven by a `Planner` that is updated cyclically with the vehicle state, surrounding traffic situation, and current lane-change request, and the part that preserves lane-change progress across updates is the `Lateral State Manager (LSM)`. LSM is a seven-location EFSM whose initial location is `NoRequest`; after a lane-change request arrives, it moves through intermediate locations such as `S1`, `S2`, and `S3`, eventually reaches `Finished` when the maneuver is complete, and then returns to `NoRequest` on the next planner update. Each planner cycle first calls `updateState`, which invokes the current state's `duringUpdate`; that method either keeps the current location for the next cycle or triggers a transition, in which case the destination state's `enterUpdate` runs once before the cycle terminates. The implementation is therefore not just a static diagram but a concrete update-driven machine with a 7-valued current-location variable inside an EFSM model with 75 locations, 123 transitions, and 17 variables. Around this cycle logic, the controller also tracks three timer counters, `timer1`, `timer2`, and `timer3`, which may be incremented only once per update and are checked together with the internal `direction` variable so the executed lane-change side must stay aligned with the current request.

### 3. 逐句溯源

1. 句子 1：The lane-change module is driven by a `Planner` that is updated cyclically with the vehicle state, surrounding traffic situation, and current lane-change request, and the part that preserves lane-change progress across updates is the `Lateral State Manager (LSM)`.
   对应摘录：A
2. 句子 2：LSM is a seven-location EFSM whose initial location is `NoRequest`; after a lane-change request arrives, it moves through intermediate locations such as `S1`, `S2`, and `S3`, eventually reaches `Finished` when the maneuver is complete, and then returns to `NoRequest` on the next planner update.
   对应摘录：A
3. 句子 3：Each planner cycle first calls `updateState`, which invokes the current state's `duringUpdate`; that method either keeps the current location for the next cycle or triggers a transition, in which case the destination state's `enterUpdate` runs once before the cycle terminates.
   对应摘录：B
4. 句子 4：The implementation is therefore not just a static diagram but a concrete update-driven machine with a 7-valued current-location variable inside an EFSM model with 75 locations, 123 transitions, and 17 variables.
   对应摘录：B
5. 句子 5：Around this cycle logic, the controller also tracks three timer counters, `timer1`, `timer2`, and `timer3`, which may be incremented only once per update and are checked together with the internal `direction` variable so the executed lane-change side must stay aligned with the current request.
   对应摘录：C
