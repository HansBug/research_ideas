# The effects of swing assistance in a microprocessor-controlled transfemoral prosthesis on walking at varying speeds and grades - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出 stance-controlled swing-assist 膝假肢的 `4` 态 walking `FSM`、角度/负载 guard、cadence 缩放参考轨迹，以及 steep-downslope 下的 pre-swing bypass 与不同 extension trajectory，可直接作为 `EFSM + T1` 样本。

## 条目 1: Four-state swing-assist supervisor for a stance-controlled transfemoral knee
- 控制对象：stance-controlled swing-assisted transfemoral knee prosthesis 的 walking supervisor
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 swing-assist 主动膝假肢的 gait-phase 监督控制器，用 `Stance / Pre-Swing / Swing Flexion / Swing Extension` 四态骨架调度液压阀阻尼、motor damping 和 assist-as-needed torque pulse，并在 steep downslope 时切换到特化行为。
- 判断：算。对象是真实 transfemoral prosthesis 的 walking controller；原文同时保住了显式状态集合、transition guards、cadence 驱动的 reference generation、state-specific actuator behavior 以及 steep-downslope fallback。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section `3. Swing-assist controller`，行 101-117
> The swing-assist controller is implemented within a finite-state machine (FSM). This FSM provides transitions between the different phases of gait and generates the splines and trajectories needed for the swing-assist controller, as well as the resistance levels commanded via the hydraulic valve. The FSM employs four states, as shown in Figure 3. The conditions governing transitions between states are described in Table 1.
>
> Figure 2 ... the reference angle and phase are generated within the external finite-state machine (FSM). An example plot of minimal acceptable trajectory (`θref`) is shown ... where the start angle and slope are a function of the user’s knee movement at toe off, and the peak angle is determined by cadence ... the torque command ... provides a unique and predictable zero crossing, and a known maximum amplitude.

#### 摘录 B
- 出处：第 5 页，Section `3. Swing-assist controller`，行 122-127
> Upon transition to state 1 (pre-swing), the valve is rotated into an open position to allow the user to begin flexing the knee ... As the leg is unloaded, the FSM transitions into state 2 (swing flexion), at which time the valve remains fully open, cadence information is calculated based on stance phase duration, and the reference knee trajectory and period scaling factor are computed. The motor torque is governed by the swing-assist controller during states 2 and 3. Once the leg has reached peak flexion, the FSM transitions into state 3 (swing extension) ... Once the knee nears full extension, the drive motor switches back into a passive damping mode ... As the leg is loaded, the FSM transitions back to state 0 (stance).

#### 摘录 C
- 出处：第 5 页，Figure `3` 与 Table `1`，行 132-144
> Figure 3. Finite-state machine used for walking. The finite-state machine consists of four states: Stance, Pre-Swing, Swing Flexion, and Swing Extension. When the device detects that the user is walking down a steep slope, the pre-swing state is bypassed to avoid knee buckling.
>
> Table 1. FSM transitions
> `0→1` Thigh sufficiently behind user (indicated by angle) and not steep-slope walking
> `0→2` Steep slope walking and leg unloaded
> `2→0` Leg loaded
> `1→0` Thigh not sufficiently behind user prior to toe off
> `1→2` Leg unloaded
> `2→3` Knee angle trajectory velocity negative
> `3→0` Leg loaded or knee reaches full extension

#### 摘录 D
- 出处：第 6 页，Section `3. Swing-assist controller`，行 149-153
> When this occurs, state 1 is bypassed, since flexion for steep downslope is achieved during stance-knee yielding, and thus further flexion is not needed. Instead, the controller simply transitions from state 0 to state 2 when the leg is unloaded. ... when steep downslope walking is detected, the state 0 hydraulic behavior is modified slightly to reduce stance knee resistance ... Additionally, a different extension trajectory and torque pulse are implemented, to better accommodate the different swing-phase patterns employed in steep-slope descent.

### 2. 基于原文整理后的自然语言描述

The swing-assist transfemoral knee is organized as a four-state extended state machine with `Stance`, `Pre-Swing`, `Swing Flexion`, and `Swing Extension`, and the same FSM also generates the reference splines and valve resistance settings used by the assist controller. In `Stance`, the valve is kept at high damping, `Pre-Swing` opens the valve and adds passive motor damping for controlled unloading, `Swing Flexion` computes cadence-dependent reference trajectories and period scaling from stance duration, and `Swing Extension` re-locks the valve in advance of heel strike before returning to passive damping near full extension. Transition guards are explicit and sensor-driven: thigh angle determines `0→1`, unloading enables `1→2` or `0→2`, negative knee-angle trajectory velocity triggers `2→3`, and leg loading or full extension closes the cycle back to `Stance`. The assist torque is not a generic tracking output but an assist-as-needed pulse with a unique zero crossing, whose sign and magnitude depend on the comparison between measured knee motion and the minimal acceptable trajectory defined from toe-off motion and cadence. For steep downslope gait, the controller detects stance-knee yielding, bypasses `Pre-Swing`, reduces stance resistance, and swaps in a different extension trajectory and torque pulse so the same supervisor can accommodate downslope-specific swing patterns without knee buckling.

### 3. 逐句溯源

1. 句子 1：The swing-assist transfemoral knee is organized as a four-state extended state machine with `Stance`, `Pre-Swing`, `Swing Flexion`, and `Swing Extension`, and the same FSM also generates the reference splines and valve resistance settings used by the assist controller.
   对应摘录：A, C
2. 句子 2：In `Stance`, the valve is kept at high damping, `Pre-Swing` opens the valve and adds passive motor damping for controlled unloading, `Swing Flexion` computes cadence-dependent reference trajectories and period scaling from stance duration, and `Swing Extension` re-locks the valve in advance of heel strike before returning to passive damping near full extension.
   对应摘录：B
3. 句子 3：Transition guards are explicit and sensor-driven: thigh angle determines `0→1`, unloading enables `1→2` or `0→2`, negative knee-angle trajectory velocity triggers `2→3`, and leg loading or full extension closes the cycle back to `Stance`.
   对应摘录：C
4. 句子 4：The assist torque is not a generic tracking output but an assist-as-needed pulse with a unique zero crossing, whose sign and magnitude depend on the comparison between measured knee motion and the minimal acceptable trajectory defined from toe-off motion and cadence.
   对应摘录：A
5. 句子 5：For steep downslope gait, the controller detects stance-knee yielding, bypasses `Pre-Swing`, reduces stance resistance, and swaps in a different extension trajectory and torque pulse so the same supervisor can accommodate downslope-specific swing patterns without knee buckling.
   对应摘录：C, D
