# Hybrid FES-Robot Cooperative Control of Ambulatory Gait Rehabilitation Exoskeleton - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `Kinesis` 混合外骨骼的 gait assistance 控制明确组织成 `t-FSM + c-FSM` 双层结构，并给出 `learning / monitoring` 周期、`5%` 收敛阈值、`19%` 疲劳检测与安全回退链，可直接作为高质量层次控制样本。

## 条目 1: Hierarchical cooperative gait controller for the Kinesis hybrid exoskeleton
- 控制对象：混合 `FES + robot` 步行康复外骨骼 `Kinesis` 的高层协同控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个通过时间域 gait FSM 协调双腿周期域学习/监测 FSM，并在 stance / swing 中分配机器人与电刺激贡献的混合外骨骼监督控制器。
- 判断：算。对象是真实步行康复外骨骼控制器，不是康复流程；原文明确给出双层状态机、分阶段控制职责、收敛条件、疲劳管理与安全回退。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section `Kinesis: a hybrid lower limb exoskeleton for SCI rehabilitation`
> The high-level control approach to achieve a cooperative behavior is shown in Figure 1. The controller comprises four main components: 1) a robotic or joint controller, 2) a FES controller, 3) a muscle fatigue estimator (MFE), and 4) a finite-state machine (FSM), that coordinates the FES and joint controllers.

#### 摘录 B
- 出处：第 4-6 页，Section `Knee joint control` / `Stimulator controller`
> Detection of gait events is performed by a finite state machine (t-FSMa) that gathers information from the sensors.
>
> The swing phase can be determined by joint trajectory and time. Conversely, the stance phase must be determined based on a stability criterion prior to the initiation of a new step.
>
> Thus, in our approach we have implemented a dual closed-loop FES controller, in which knee extensor muscles are controlled by a PID controller and the flexor muscles are controlled by an iterative error-based learning controller.

#### 摘录 C
- 出处：第 7 页，Section `Cooperative approach`
> We have designed a FSM that operates in the domain of the gait cycle (c-FSM, Figure 3, right), one for each leg, during swing phase, coordinated with the t-FSM that operates in the time domain.
>
> The t-FSM coordinates the left and right c-FSM by broadcasting cycle events: once a leg enters in swing state, a new step event is broadcasted to the respective cycle-domain FSM, either left or right.
>
> Each c-FSM has two states: learning state and monitoring state.

#### 摘录 D
- 出处：第 7 页，Section `Cooperative approach`
> Learning state is the default state when the user commands the first step.
>
> By calculating the gradient of the stimulation output time-integral ... the ILC convergence is assumed when this gradient is lower than 5%. Therefore the monitoring state is entered.
>
> Within this state, the last control vector output from ILC is stored in memory and repeated as stimulation pattern during the next steps, and the ILC algorithm is stopped. Then the MFE monitors the TTI ... Once muscle fatigue is estimated by the MFE, by an increase of 19% of TTI, a muscle fatigue management approach can be deployed.

#### 摘录 E
- 出处：第 7 页，Section `Safety`
> In case of exceeding these limits, the state machine executes the locking of the motor shaft, then moving back to a default safe knee position.
>
> An equivalent safe strategy was implemented in the stimulator controller to set safety limits for pulse width and amplitude modulation.

### 2. 基于原文整理后的自然语言描述

The Kinesis hybrid gait-rehabilitation exoskeleton uses a hierarchical cooperative controller that combines a robotic joint controller, an FES controller, a muscle fatigue estimator, and a supervisory FSM. At the top level, a time-domain `t-FSM` detects gait events from sensors and separates stance from swing behavior, so stance is handled by a stability-oriented loop while swing is handled as a trajectory-and-time-defined phase. Inside swing, the supervisor activates a separate cycle-domain `c-FSM` for each leg, and the `t-FSM` broadcasts a `new step` event whenever a leg enters swing, which starts a two-state `learning / monitoring` submachine. During `learning`, an iterative learning controller updates the stimulation pattern until the stimulation-output integral gradient falls below `5%`; during `monitoring`, the last learned pattern is replayed, the muscle fatigue estimator tracks `TTI`, and robotic assistance is reduced cycle by cycle while preserving at least the required knee-flexion objective. If muscle fatigue is detected from a `19%` change in `TTI`, or if joint safety limits are exceeded, the controller changes behavior by restarting the learning process or by locking the motor shaft and returning the knee to a default safe position.

### 3. 逐句溯源

1. 句子 1：The Kinesis hybrid gait-rehabilitation exoskeleton uses a hierarchical cooperative controller that combines a robotic joint controller, an FES controller, a muscle fatigue estimator, and a supervisory FSM.
   对应摘录：A
2. 句子 2：At the top level, a time-domain `t-FSM` detects gait events from sensors and separates stance from swing behavior, so stance is handled by a stability-oriented loop while swing is handled as a trajectory-and-time-defined phase.
   对应摘录：B
3. 句子 3：Inside swing, the supervisor activates a separate cycle-domain `c-FSM` for each leg, and the `t-FSM` broadcasts a `new step` event whenever a leg enters swing, which starts a two-state `learning / monitoring` submachine.
   对应摘录：C
4. 句子 4：During `learning`, an iterative learning controller updates the stimulation pattern until the stimulation-output integral gradient falls below `5%`; during `monitoring`, the last learned pattern is replayed, the muscle fatigue estimator tracks `TTI`, and robotic assistance is reduced cycle by cycle while preserving at least the required knee-flexion objective.
   对应摘录：D
5. 句子 5：If muscle fatigue is detected from a `19%` change in `TTI`, or if joint safety limits are exceeded, the controller changes behavior by restarting the learning process or by locking the motor shaft and returning the knee to a default safe position.
   对应摘录：D, E
