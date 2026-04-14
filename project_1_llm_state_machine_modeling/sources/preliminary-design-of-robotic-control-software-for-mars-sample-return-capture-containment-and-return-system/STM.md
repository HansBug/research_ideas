# A Preliminary Design of the Robotic Control Software for Mars Sample Return - Capture, Containment, and Return System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展有限状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：-
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 CCRS 机器人软件 `RSW` 的完整 motion-primitive 执行 FSM，包括状态表、`StateExit / StateEntry / StateRun / Step` 调用链、命令触发迁移、停机回退和全局 `FAULT` 入口，是很强的航天机器人控制样本。

## 条目 1: RSW Motion-Primitive Execution FSM for CCRS RTAS
- 控制对象：火星样本返回 `CCRS` 机器人传送系统的 Robot Software 主控流程
- 状态机类型：EFSM（扩展有限状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：-
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 `CCRS` 机器人软件在接收 motion primitive 命令后，对 `RSCE` 进行配置、预检、执行、后检并处理故障的主状态机。
- 判断：算。对象是 NASA/ESA 火星样本返回任务里的真实机器人控制软件，不是纯架构论文；原文给出了状态名、状态语义、状态调度函数、顺序迁移、停机回退和 fault 处理，足以直接抽成 source 数据。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页 Abstract
> Robot Software (RSW) is a set of software processes for commanding and monitoring the avionics that controls robotic mechanisms designed to sterilize and install OS into Earth Entry System.
>
> This paper describes a preliminary design of RSW including motion modes, architecture, and finite state machine.

#### 摘录 B
- 出处：第 14 页 Table 1 `RSW FSM States`
> UNKNOWN Initial state on startup.
>
> INITIALIZED After start up procedures and before valid telemetry from RSCE.
>
> RSCE_ON Initial configuration of RSCE.
>
> READY_ON Systems are initially configured. Ready to receive motion primitive commands.
>
> CONFIGURE Configure RSCE for motion primitive.
>
> PRE_MOTION_CHECK Perform pre-motion check using Worker Task for motion primitive.
>
> IN_MOTION Execute motion. Monitor telemetry.
>
> POST_MOTION_CHECK Perform post motion anomaly checks.
>
> FAULT A fault has occurred. Pending external intervention.

#### 摘录 C
- 出处：第 14-15 页 Section IV `RSW Design and Implementation`
> Step begins by checking if current state and requested state are the same. If current state and requested state are not the same, RSW calls StateExit and then StateEntry ... current state is then set to requested state ... Step method ends by calling StateRun.
>
> Transitioning to FAULT is valid for all states.
>
> When a motion primitive command is received while RSW is in READY_ON, RSW enters CONFIGURE.
>
> Once RSCE is configured, RSW enters PRE_MOTION_CHECK ... If a nominal work result is received from Worker Task, RSW enters IN_MOTION.
>
> When motion is complete, RSW performs a post-motion check for anomalies before re-entering READY_ON.
>
> If RSW receives a stop command during CONFIGURE, PRE_MOTION, IN_MOTION, and POST_MOTION_CHECK, RSW transitions directly back to READY_ON.

### 2. 基于原文整理后的自然语言描述

The Mars Sample Return CCRS robot software manages motion primitives through an extended finite state machine driven by both command inputs and execution feedback. On startup, `RSW` initializes in `UNKNOWN`, requests transition to `INITIALIZED`, waits for valid telemetry, performs the initial `RSCE_ON` configuration, and then enters `READY_ON` where it can accept motion primitive commands. Once a motion primitive is requested, the controller advances through `CONFIGURE`, `PRE_MOTION_CHECK`, `IN_MOTION`, and `POST_MOTION_CHECK`, with the `Step` routine explicitly sequencing `StateExit`, `StateEntry`, and `StateRun` according to the pair `(current_state, requested_state)`. During `CONFIGURE`, the software sends register-write commands that prepare the avionics; during `PRE_MOTION_CHECK`, it requests a Worker Task validation; during `IN_MOTION`, it starts the motion and monitors telemetry; and after completion it performs anomaly checks before returning to `READY_ON`. A stop command received in any execution stage immediately returns the controller to `READY_ON`, while transition to `FAULT` is globally allowed from every state, making the abnormal path as explicit as the nominal chain.

### 3. 逐句溯源

1. 句子 1：The Mars Sample Return CCRS robot software manages motion primitives through an extended finite state machine driven by both command inputs and execution feedback.
   对应摘录：A, B, C
2. 句子 2：On startup, `RSW` initializes in `UNKNOWN`, requests transition to `INITIALIZED`, waits for valid telemetry, performs the initial `RSCE_ON` configuration, and then enters `READY_ON` where it can accept motion primitive commands.
   对应摘录：B, C
3. 句子 3：Once a motion primitive is requested, the controller advances through `CONFIGURE`, `PRE_MOTION_CHECK`, `IN_MOTION`, and `POST_MOTION_CHECK`, with the `Step` routine explicitly sequencing `StateExit`, `StateEntry`, and `StateRun` according to the pair `(current_state, requested_state)`.
   对应摘录：B, C
4. 句子 4：During `CONFIGURE`, the software sends register-write commands that prepare the avionics; during `PRE_MOTION_CHECK`, it requests a Worker Task validation; during `IN_MOTION`, it starts the motion and monitors telemetry; and after completion it performs anomaly checks before returning to `READY_ON`.
   对应摘录：B, C
5. 句子 5：A stop command received in any execution stage immediately returns the controller to `READY_ON`, while transition to `FAULT` is globally allowed from every state, making the abnormal path as explicit as the nominal chain.
   对应摘录：C
