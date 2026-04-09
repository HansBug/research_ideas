# Autonomous Social Robot Navigation using a Behavioral Finite State Social Machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 并行, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把社交导览机器人的并行导航体系写成了以 BFSSM 速度管理器为核心、带 sequencer / APF / announcement lock 协同的定时监督控制链，原文与描述都足够支撑双 A。

## 条目 1: Timed social-tour navigation supervisor with parallel sequencer and regrouping BFSSM

- 控制对象：通用控制与服务机器人领域的社交导览机器人并行导航、访客 regrouping 与 announcement arbitration 监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 并行, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个社交导览机器人任务监督器，顶层把 `goal sequencer`、`speed manager`、`APF` 控制器与 `announcement lock` 共享资源组织在一起，其中速度管理器本身又是带 `tstop / tannounce` 的 BFSSM。
- 判断：算。对象是真实服务机器人导航控制链，不是方法流程；原文明确给出了并行模块边界、共享语音资源仲裁、`moving / stopped / wait for visitors` 等状态、以及由 `tstop / tannounce` 触发的恢复与继续游览逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 11 页，`Fig. 2. Goal sequencer / 4.2. Speed manager`，`paper_content.txt` 第 525-536 行
> The second module is the goal sequencer. Here, the different visit sites or goal of the environment (workspace map) are defined. The module sequences different mission sites. Reaching each mission site is further a motion to goal behavior, which is broken into multiple sub-goals. On reaching each mission site, the robot makes the announcements explaining about the site as a tour guide.
>
> An announcement lock system is also built in this scheme. Both the speed manager module and the sequencer module run in parallel and use the speaker as a resource for giving an audio feedback to the visitors for different reasons. It is possible for both audio messages to be invoked together.
>
> The APF is the third module which acts as a controller for the robot. Here, potential function and force are applied on the robot, which is used to calculate the control signal for the robot.

#### 摘录 B

- 出处：第 11 页，`4.2. Speed manager`，`paper_content.txt` 第 540-555 行
> The speed management module sets an allowable navigation speed for the robot, and the module is modeled as a BFSSM for the robot navigation.
>
> The module empowers the robot to make the decision of its speed based on the different states as shown in Fig. 3. The robot is initially at the moving stage, wherein it moves as per the sequencer and controller. In the BFSSM, a timer is assumed to available at every stage.
>
> However, if any visitors are not available for a certain time then the robot adjusts its speed as per the time when the visitors were not seen. Eventually, after `tstop` amount of time, if the visitors are still not seen, the robot will stop... after `tannounce` time, an audio feedback is provided to get the attention of the missing visitors.

#### 摘录 C

- 出处：第 13 页，`Algorithm 1 Velocity manager`，`paper_content.txt` 第 625-661 行
> 4) state = “Moving”
>
> If (state = “moving”) ... `vpref_R = vmax max((T - tlastSeenV) / tstop, 0)` ... If `vpref_R = 0`, `tstopped = T` and `state = "stopped"`.
>
> Else if (state = “Stopped” and `T - tstopped > tannounce`) State = “Wait for announcement lock”.
>
> Else if (state = “Wait for announcement lock” and not announcementLock) ... play(wait message) ... State = “wait for visitors”.
>
> Else if (State = “wait for visitors” and visitorsStatus) State = “Wait for announcement lock second” ... play(moving message) ... State = “moving”.

### 2. 基于原文整理后的自然语言描述

The robot-guide architecture combines a `goal sequencer`, a BFSSM-based `speed manager`, and an `APF` controller, with the speed manager and sequencer running in parallel and arbitrating access to a shared speaker through an `announcement lock`. Inside the speed manager, the robot normally stays in `moving`, but if visitors disappear the allowable speed is reduced as a function of `T - tlastSeenV` until `tstop` forces a transition to `stopped`. If the visitors remain missing longer than `tannounce`, the supervisor moves through `Wait for announcement lock` to issue a wait message and then enters `wait for visitors` until the group is detected again. Once all visitors are visible, the controller acquires the lock a second time, plays the moving message, and returns the system to `moving`. In parallel, the sequencer decomposes each visit site into ordered sub-goals and the APF tracks those goals under the speed limit published by the BFSSM, so the case is best read as a timed, parallel HSM rather than a flat speed-only FSM.

### 3. 逐句溯源

1. 句子 1：The robot-guide architecture combines a `goal sequencer`, a BFSSM-based `speed manager`, and an `APF` controller, with the speed manager and sequencer running in parallel and arbitrating access to a shared speaker through an `announcement lock`.
   对应摘录：A
2. 句子 2：Inside the speed manager, the robot normally stays in `moving`, but if visitors disappear the allowable speed is reduced as a function of `T - tlastSeenV` until `tstop` forces a transition to `stopped`.
   对应摘录：B, C
3. 句子 3：If the visitors remain missing longer than `tannounce`, the supervisor moves through `Wait for announcement lock` to issue a wait message and then enters `wait for visitors` until the group is detected again.
   对应摘录：B, C
4. 句子 4：Once all visitors are visible, the controller acquires the lock a second time, plays the moving message, and returns the system to `moving`.
   对应摘录：C
5. 句子 5：In parallel, the sequencer decomposes each visit site into ordered sub-goals and the APF tracks those goals under the speed limit published by the BFSSM, so the case is best read as a timed, parallel HSM rather than a flat speed-only FSM.
   对应摘录：A, B
