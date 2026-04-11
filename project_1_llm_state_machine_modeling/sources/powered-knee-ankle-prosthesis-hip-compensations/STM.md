# Effects of a Powered Knee-Ankle Prosthesis on Amputee Hip Compensations: A Case Series - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把主动膝踝假肢控制器明确写成 `Early Stance / Mid-stance / Push-off / Swing / Touchdown` 五态 FSM，并给出 `FC`、关节角、相位变量与 `tpo / tfw` 定时 guard。

## 备注

- `paper_content.txt` 中含少量 `NUL` 噪声字节，但去噪后正文、图题和转移条件均可稳定核对，因此未重提取原文。

## 条目 1: Five-state gait-phase supervisor for a powered knee-ankle prosthesis

- 控制对象：医疗设备与生命支持控制领域的主动膝踝假肢步态相位监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用于主动膝踝假肢的五态步态监督器，用地面接触、关节角、相位变量和局部时间参数来切换站立、预推蹬、摆动和落地准备。
- 判断：算。对象是真实主动假肢控制器；原文不仅给出 Fig. 2 的显式五态 FSM，还把每个 transition 的 guard 写成 `FC / q_a / q_k / s_d / s_a / tpo / tfw` 组合，因此足以支撑高质量 `EFSM + T1` 条目。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Introduction / control scheme，`paper_content.txt` 第 15-19、123-133 行
> The powered prosthesis used impedance control during stance for compliant interaction with the ground, a time-based push-off controller to deliver high torque and power, and phase-based trajectory tracking during swing to provide user control over foot placement. ... Impedance control is utilized during the stance phase ... Time-based kinematic control is used during push-off ... Lastly, a time-invariant kinematic control method, based on a phase variable derived from thigh motion, is utilized to provide user synchronization across walking speeds ...

#### 摘录 B

- 出处：第 3 页，Figure 2
> Figure 2 shows the controller FSM with the states `Early Stance`, `Mid-stance`, `Push-off`, `Swing`, and `Touchdown`. The caption states that the yellow circles correspond to impedance-controlled states, the blue rectangles to time-based position-controlled states, and the green triangle to position control based on a holonomic phase variable.

#### 摘录 C

- 出处：第 4 页，Section `C. Control Method`，`paper_content.txt` 第 424-493 行
> Transitions in the FSM are based on foot contact (FC) for stance states, time in time-based states, ankle angle for impedance-controlled states, and two phase variables for phase-controlled states. ... 1) Transition between early and mid-stance: When the ankle angle becomes greater than qa,ms ... Conversely, if the foot contact is lost or the thigh angle rises above sd, the system goes back to early-stance ... 2) Transition from mid-stance to push-off: When the ankle angle becomes greater than qa,po ... time is set to zero. ... 3) Transition from push-off to swing ... determined by the preset push-off duration (tpo) ... 4) Transition from swing to touchdown ... a pre-specified forward thigh angle ... 5) Transition from touchdown to (early) stance ... preset duration (tfw) ... start when the foot touches the ground (FC = 1) ... 6) Transition from touchdown to swing ... 7) Direct transition from swing to early stance ...

### 2. 基于原文整理后的自然语言描述

The powered knee-ankle prosthesis is controlled by a five-state extended FSM with `Early Stance`, `Mid-stance`, `Push-off`, `Swing`, and `Touchdown`, where stance behavior, time-based push-off, and phase-based swing tracking are handled in different control modes. The two stance states are impedance-controlled, `Push-off` and `Touchdown` are time-based position-control states, and `Swing` is driven by a holonomic phase variable, so the discrete controller is tightly coupled to continuous gait variables rather than acting as a pure mode labeler. The transition from `Early Stance` to `Mid-stance` is guarded by ankle angle, while the return depends on foot-contact loss or the thigh-phase variable; the `Mid-stance -> Push-off` transition is another ankle-angle guard that also resets time. The controller leaves `Push-off` only after the preset push-off duration `tpo` and sufficient forward thigh progression, switches from `Swing` to `Touchdown` when a forward thigh-angle threshold is reached before ground contact, and leaves `Touchdown` through the preset timer `tfw` plus foot contact, or falls back to `Swing` if contact does not occur. A direct `Swing -> Early Stance` shortcut is also defined when the foot touches the ground during swing and the knee angle stays below the specified threshold, making the controller a concrete timed gait-phase supervisor with explicit sensor and state-variable guards.

### 3. 逐句溯源

1. 句子 1：The powered knee-ankle prosthesis is controlled by a five-state extended FSM with `Early Stance`, `Mid-stance`, `Push-off`, `Swing`, and `Touchdown`, where stance behavior, time-based push-off, and phase-based swing tracking are handled in different control modes.
   对应摘录：A, B
2. 句子 2：The two stance states are impedance-controlled, `Push-off` and `Touchdown` are time-based position-control states, and `Swing` is driven by a holonomic phase variable, so the discrete controller is tightly coupled to continuous gait variables rather than acting as a pure mode labeler.
   对应摘录：A, B
3. 句子 3：The transition from `Early Stance` to `Mid-stance` is guarded by ankle angle, while the return depends on foot-contact loss or the thigh-phase variable; the `Mid-stance -> Push-off` transition is another ankle-angle guard that also resets time.
   对应摘录：C
4. 句子 4：The controller leaves `Push-off` only after the preset push-off duration `tpo` and sufficient forward thigh progression, switches from `Swing` to `Touchdown` when a forward thigh-angle threshold is reached before ground contact, and leaves `Touchdown` through the preset timer `tfw` plus foot contact, or falls back to `Swing` if contact does not occur.
   对应摘录：C
5. 句子 5：A direct `Swing -> Early Stance` shortcut is also defined when the foot touches the ground during swing and the knee angle stays below the specified threshold, making the controller a concrete timed gait-phase supervisor with explicit sensor and state-variable guards.
   对应摘录：C
