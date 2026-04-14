# Configuring a Powered Knee and Ankle Prosthesis for Transfemoral Amputees within Five Specific Ambulation Modes - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 powered knee-ankle prosthesis 在五种步行模式下复用的四态阻抗状态机、角度/载荷函数和 mode-specific 参数化写得较全，可直接作为 multi-mode impedance FSM 样本。

## 条目 1: Four-state impedance FSM for the powered knee-ankle prosthesis across five ambulation modes
- 控制对象：主动膝踝一体假肢在五种 ambulation mode 下复用的四态阻抗控制状态机
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 powered knee-and-ankle prosthesis 的通用步态状态机，在 `level-ground / ramp ascent / ramp descent / stair ascent / stair descent` 五种模式下复用四个相位状态，并用角度与载荷函数在线调节阻抗参数。
- 判断：算。对象是真实主动假肢控制器，原文不仅给出状态划分和阈值触发，还明确给出了各状态下如何按 ankle angle、knee angle、axial force 等变量更新阻抗参数。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section `A. Powered Prosthesis Control`
> The device was controlled using an impedance-based model that generated torque commands ... The three impedance parameters of each joint were stiffness, k, equilibrium angle, he, and damping coefficient, b, which were modified using a finite state machine for each ambulation mode. The state machine architectures were similar to previous designs, but only included four states ... The stance phase was divided into two states: early to mid-stance and late stance, and the swing phase was divided into two states: swing flexion and swing extension. Four transitions ... were triggered based on mechanical sensor thresholds. Across 5 ambulation modes ... a total of 140 parameters ... could be modified.

#### 摘录 B
- 出处：第 2-3 页，Section `A. Powered Prosthesis Control`
> Across ambulation modes, 60% of the impedance parameters were set to constant values within each state. Five modified intrinsic control strategies were implemented to adjust the remaining impedance parameters ... basing impedance parameters on set values from the previous state; mimicking biological joint responses ... modifying joint impedance as a function of ankle angle; modifying joint impedance as a function of knee angle; or allowing users to control the rate of power generation or dissipation ... as a function of decreasing or increasing axial force in the prosthesis.

#### 摘录 C
- 出处：第 3 页，Section `Impedance as a Function of Knee Angle`
> Knee equilibrium angle, heknee, was modified as function of knee angle, hknee ... Knee equilibrium angle ‘‘followed’’ the current knee angle ... Eq. (3) modulated knee equilibrium angle during early to mid-stance of ramp descent and the entire stance phase during stair descent ... it did provide appropriate stance phase support during controlled knee flexion for ramp and stair descent.

#### 摘录 D
- 出处：第 3 页，Section `Impedance as a Function of Decreasing Prosthesis Load`
> Joint impedance, pi, was modulated as a linear function of axial force, F, within the prosthesis ... FInitial was set to the instantaneous force upon entering the state ... and FFinal was set to 10% body weight. This strategy was applied during level-ground walking, ramp ascent, and ramp descent during late stance; modulated kknee, heknee, and heankle for reduced knee stiffness, knee swing initiation, and powered plantarflexion as force decreased. Stair ascent during late stance modulated changes to heankle ... for powered plantarflexion as force decreased.

### 2. 基于原文整理后的自然语言描述

The powered knee-ankle prosthesis uses a common four-state gait machine in which `early-to-mid stance`, `late stance`, `swing flexion`, and `swing extension` are reused across five ambulation modes, while each mode carries its own impedance parameterization for knee and ankle joints. Instead of treating each state as a fixed stiffness-damping block only, the controller augments the FSM with mode-specific functions that update stiffness, equilibrium angle, and damping from ankle angle, knee angle, or axial load inside the prosthesis. This means the same gait-phase skeleton can support level walking, ramp ascent/descent, and stair ascent/descent by swapping parameter sets and variable-dependent laws rather than redesigning the state graph each time. In particular, late stance in walking and ramp modes uses decreasing axial load to reduce knee stiffness, initiate knee swing, and shift ankle equilibrium toward powered plantarflexion, while ramp and stair descent use knee-angle-following equilibrium control to support controlled stance flexion. The paper is therefore a strong EFSM-style sample in which the state graph is explicit, but the substantive control behavior is encoded in state-local parameter update functions tied to continuous sensor values.

### 3. 逐句溯源

1. 句子 1：The powered knee-ankle prosthesis uses a common four-state gait machine in which `early-to-mid stance`, `late stance`, `swing flexion`, and `swing extension` are reused across five ambulation modes, while each mode carries its own impedance parameterization for knee and ankle joints.
   对应摘录：A
2. 句子 2：Instead of treating each state as a fixed stiffness-damping block only, the controller augments the FSM with mode-specific functions that update stiffness, equilibrium angle, and damping from ankle angle, knee angle, or axial load inside the prosthesis.
   对应摘录：B, C, D
3. 句子 3：This means the same gait-phase skeleton can support level walking, ramp ascent/descent, and stair ascent/descent by swapping parameter sets and variable-dependent laws rather than redesigning the state graph each time.
   对应摘录：A, B
4. 句子 4：In particular, late stance in walking and ramp modes uses decreasing axial load to reduce knee stiffness, initiate knee swing, and shift ankle equilibrium toward powered plantarflexion, while ramp and stair descent use knee-angle-following equilibrium control to support controlled stance flexion.
   对应摘录：C, D
5. 句子 5：The paper is therefore a strong EFSM-style sample in which the state graph is explicit, but the substantive control behavior is encoded in state-local parameter update functions tied to continuous sensor values.
   对应摘录：A, B, C, D
