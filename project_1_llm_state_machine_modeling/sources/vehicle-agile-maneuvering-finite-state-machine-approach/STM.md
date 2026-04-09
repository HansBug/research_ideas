# Vehicle Agile Maneuvering: From Rally Drivers to a Finite State Machine Approach - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把激烈横摆机动控制器明确压成 `3` 状态 `FSM`，不仅写了状态含义，还给出了 `Mz1` 阈值判定、`alpha_r_ref` 侧滑建立条件、`delta1 / delta2` 转向输入和 `t_end` 返回条件，是很扎实的 `FSM + T1` 车辆运动控制样本。

## 条目 1: Three-state agile-yaw maneuver controller

- 控制对象：汽车与道路车辆控制领域的高横摆机动三状态 yaw-moment 控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个嵌入二轨车辆模型中的机动控制器，用有限状态机决定何时保持直行、何时先建立后轮侧滑、何时施加目标横摆力矩并在设定时长后回到初始状态。
- 判断：算。对象是车辆高机动控制器本身，不是仿真流程；原文直接给出 `3` 个状态、每个状态的输入输出、基于 `Mz_ref` 与 `alpha_r_hat` 的 guard，以及 `t_end` 定时返回条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Abstract / Introduction，`paper_content.txt` 第 67-71, 94-100 行
> Finally, a finite state machine is modelled in a two track vehicle model to evaluate the proposed methodology.
>
> Then, a finite state machine is implemented in a two track vehicle model (Matlab / Simulink) to drive the vehicle from straight line to cornering for different target yaw accelerations.
>
> metrics to characterize the vehicle agility are proposed (attitude change time, min sideslip and max yaw Acceleration).

#### 摘录 B

- 出处：第 7 页，`V. Finite State Machine / A. Description of the Finite State Machine`，`paper_content.txt` 第 503-517 行
> The Finite State Machine proposed in this paper consists of three states.
>
> State 1 corresponds to the vehicle driving in straight line at constant speed, prior to start the maneuver.
>
> When a target yaw moment is given to the machine, the State can change to State 2 or State 3.
>
> If Mzref is higher than the threshold Mz1, the machine switchs to State 2. If not, the machine goes directly to State 3.
>
> In State 2, the machine applies the steering and braking actions required to reach the sideslip condition necessary to achieve Mzref. Finally, when the sideslip condition is satisfactory, the machine switches to State 3, and the steering input is applied to generate Mzref.

#### 摘录 C

- 出处：第 7-8 页，`State 1 / State 2`，`paper_content.txt` 第 526-530, 571-579 行
> If {abs(Mzref) < Mz1}: ar = 0, delta = SR(afref), lambdaf = 0, lambdar = 0, State = State 3
>
> Else {}: ar = arref, delta = -delta1 sign(Mzref), lambdaf = 0, lambdar = -1, State = State 2
>
> If {abs(arhat) < abs(arref)}: delta = delta1, lambdaf = 0, lambdar = -1, State = State 2
>
> Else {}: delta = delta2 sign(Mzref), lambdaf = 0, lambdar = 0, State = State 3

#### 摘录 D

- 出处：第 8 页，`D. State 3 (Return to straight line)`，`paper_content.txt` 第 590-600 行
> Finally, the Machine returns to State 1 when the time condition tend is surpassed.
>
> If {t < tend}: hold delta, lambdaf = 0, lambdar = 0, State = State 3
>
> Else {}: delta = 0, lambdaf = 0, lambdar = 0, State = State 1

### 2. 基于原文整理后的自然语言描述

The retained controller is a three-state finite-state machine that drives the vehicle from straight-line driving into an agile cornering maneuver and then returns it to nominal motion. In `State 1`, the car remains in straight-line constant-speed driving until a target yaw moment `Mzref` is requested. The first guard is the threshold `Mz1`: if `abs(Mzref) < Mz1`, the controller skips the intermediate buildup phase and moves directly to `State 3`; otherwise it enters `State 2`, applies steering `delta1`, keeps the front longitudinal slip at zero, and fully locks the rear wheels with `lambdar = -1` to build the desired rear sideslip `arref`. The machine stays in `State 2` while `abs(arhat) < abs(arref)` and only transfers to `State 3` once the estimated rear-wheel slip is high enough, at which point it releases the braking lock and applies `delta2` to generate the requested yaw moment. `State 3` is explicitly timed: while `t < tend` the controller holds the steering command, and when `tend` is exceeded it resets `delta` to zero and returns to `State 1`. Because every transition is driven by vehicle-dynamics variables and actuator commands, the FSM is tightly coupled to the continuous vehicle model rather than being a purely symbolic phase chart.

### 3. 逐句溯源

1. 句子 1：The retained controller is a three-state finite-state machine that drives the vehicle from straight-line driving into an agile cornering maneuver and then returns it to nominal motion.
   对应摘录：A, B, D
2. 句子 2：In `State 1`, the car remains in straight-line constant-speed driving until a target yaw moment `Mzref` is requested.
   对应摘录：B
3. 句子 3：The first guard is the threshold `Mz1`: if `abs(Mzref) < Mz1`, the controller skips the intermediate buildup phase and moves directly to `State 3`; otherwise it enters `State 2`, applies steering `delta1`, keeps the front longitudinal slip at zero, and fully locks the rear wheels with `lambdar = -1` to build the desired rear sideslip `arref`.
   对应摘录：B, C
4. 句子 4：The machine stays in `State 2` while `abs(arhat) < abs(arref)` and only transfers to `State 3` once the estimated rear-wheel slip is high enough, at which point it releases the braking lock and applies `delta2` to generate the requested yaw moment.
   对应摘录：B, C
5. 句子 5：`State 3` is explicitly timed: while `t < tend` the controller holds the steering command, and when `tend` is exceeded it resets `delta` to zero and returns to `State 1`.
   对应摘录：D
6. 句子 6：Because every transition is driven by vehicle-dynamics variables and actuator commands, the FSM is tightly coupled to the continuous vehicle model rather than being a purely symbolic phase chart.
   对应摘录：A, C, D
