# Visual Servoing Architecture of Mobile Manipulators for Precise Industrial Operations on Moving Objects - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 显式时钟, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把面向运动工件的移动机械臂操作流程写成“高层稳定性管理 + `s1-s8` 子状态机”的分层监督链，并明确给出 timeout、gripper 激活时长和安全回撤阶段，原文与描述都足够支撑双 A。

## 条目 1: Timed mobile-manipulator screwing supervisor with target-search recovery

- 控制对象：工业自动化与离散制造领域的移动机械臂运动目标锁螺丝视觉伺服监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 显式时钟, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向运动工件精密工业操作的视觉伺服控制架构，顶层负责目标搜索、错误处理和成功终止，子层 `s1-s8` 负责平台接近、机械臂接近、gripper 激活、作业和双阶段回撤。
- 判断：算。对象是实际工业移动机械臂的监督控制器，不是纯视觉算法流程；原文明确给出了高层状态、子状态机、search timeout、operation time `t`、以及目标丢失和 gripper 失败场景。

### 1. 原文摘录

#### 摘录 A

- 出处：第 9 页，`Complete state machine`，`paper_content.txt` 第 405-420 行
> Initial target search: The process starts with the mobile manipulator waiting for the target object to be detected. If the target is detected, the process moves to the operate while moving sub-state machine. Otherwise, if the target detection timeout is reached, the process transits to the error state.
> Operate while moving ... states s1 to s8. In case the target is lost during the process, the process moves to the searching target state ... once the task is completed, the successful operation state is reached.
> Searching target ... If the target is found again within a time limit, the state machine returns to the previous state ... If the timeout is reached, the process transits to the error state.

#### 摘录 B

- 出处：第 10-11 页，`Operate While Moving`，`paper_content.txt` 第 431-489 行
> The complete task is divided into three different phases:
> s1—Initial platform approach ... If the errors are below the threshold, the state transits to state s2.
> s2—Initial arm approach ... enables a safe maneuver towards the operation point.
> s3—Arm destination approach ... the manipulator moves towards the operation point.
> s4—Gripper activation ... this activation can take some time ... the control loop continues in this state until the activation is finalized.
> s5—Operation ... controls the operation time where the tool is working on the industrial task for a defined time t.
> s6—Arm retract ... manages a safe retract maneuver.

#### 摘录 C

- 出处：第 11 页与第 17 页，`Final retract / validation failures`，`paper_content.txt` 第 503-523、757-763 行
> s7—Final arm retract ... moving the manipulator away from the part.
> s8—Final platform retract ... state s8 moves the mobile platform from the object area.
> The PID values of the mobile platform are boosted ... the manipulator values are set to zero to deactivate the arm’s movements.
> The main failure reasons are the inability to reach the gripper activation state caused by large tool positioning errors ... the state machine can manage this state transition to gripper activation state, it is not able to handle the coupling error.

### 2. 基于原文整理后的自然语言描述

The controller is organized as a timed HSM whose top level manages `Initial target search`, `Operate while moving`, `Searching target`, `Error`, and `Successful operation`, so target acquisition and recovery are supervised separately from the actual process sequence. Inside `Operate while moving`, the process runs through `s1-s8`: platform approach, safe arm approach above the task pose, compliant approach to the operation point, asynchronous gripper activation, timed operation for duration `t`, local arm retract, final arm retract, and final platform retract. The state machine also re-parameterizes the low-level control law and impedance settings in each phase, which is why the discrete states remain tightly coupled to continuous servo behavior rather than being a pure task checklist. If the target is lost the system detours into `Searching target` and returns on reacquisition, while timeout and gripper-coupling failures escalate the run to controlled termination paths.

### 3. 逐句溯源

1. 句子 1：The controller is organized as a timed HSM whose top level manages `Initial target search`, `Operate while moving`, `Searching target`, `Error`, and `Successful operation`, so target acquisition and recovery are supervised separately from the actual process sequence.
   对应摘录：A
2. 句子 2：Inside `Operate while moving`, the process runs through `s1-s8`: platform approach, safe arm approach above the task pose, compliant approach to the operation point, asynchronous gripper activation, timed operation for duration `t`, local arm retract, final arm retract, and final platform retract.
   对应摘录：B, C
3. 句子 3：The state machine also re-parameterizes the low-level control law and impedance settings in each phase, which is why the discrete states remain tightly coupled to continuous servo behavior rather than being a pure task checklist.
   对应摘录：B, C
4. 句子 4：If the target is lost the system detours into `Searching target` and returns on reacquisition, while timeout and gripper-coupling failures escalate the run to controlled termination paths.
   对应摘录：A, C
