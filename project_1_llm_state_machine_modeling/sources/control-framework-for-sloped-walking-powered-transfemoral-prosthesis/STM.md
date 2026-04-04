# Control Framework for Sloped Walking With a Powered Transfemoral Prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把斜坡行走下的动力股骨假肢控制器明确写成“有限状态机 + 斜坡相关参数函数”，保住了相位划分、切换条件、状态内输出和跨坡度适配逻辑，可直接作为高质量 `EFSM + T0` 样本。

## 条目 1: Slope-adaptive gait-phase supervisor for a powered transfemoral prosthesis
- 控制对象：动力股骨假肢在上下坡行走中的 knee/ankle gait-phase controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向动力股骨假肢斜坡行走的 gait-phase supervisor，用有限状态机分割步态并按坡度角调度 knee/ankle 的 stiffness、damping、reference angle 与 swing trajectory。
- 判断：算。对象是真实动力假肢控制器，不是纯算法框架；原文明确给出状态划分、切换条件、状态内输出形式以及参数随坡度变化的映射。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 43-50
> human sloped walking data. The functions derived for each slope condition were
> simpliﬁed using principal component analysis. The weights of the resulting basis functions
> were found to obey monotonic trends within upslope and downslope walking, proving
> the existence of a relationship between the joint parameter functions and the slope
> angle. Using these trends, one can now design a controller for any given slope angle.
> Amputee and able-bodied walking trials with a powered transfemoral prosthesis revealed
> the controller to generate a healthy human gait.

#### 摘录 B
- 出处：第 2 页，Section `1.1. Background on Sloped Walking Control`，行 27-40
> limited to level and upslope walking ( Paredes et al., 2016 ). The
> former has been extensively used for level and sloped walking
> (both upslope and downslope). Almost all implementations
> of impedance control involves sectioning a gait cycle into 4– 6
> phases. These phases form the states in a ﬁnite state machine.
> A gait cycle is deﬁned to begin and end with a heel-strike on
> the same limb. We will refer to the progress in a gait cycle using
> t which is 0 at gait cycle initiation and 1 (equivalent to 100%)
> at completion. Important kinematic moments in the gait cycle
> like heel-oﬀ and maximum knee ﬂexion during swing phase are
> chosen as switching points between states.

#### 摘录 C
- 出处：第 3 页，Section `3. Proposed Control Framework`，行 63-76
> human trajectories. We thus propose a ﬁnite state machine with
> 4 states for the ankle and 5 for the knee. Both joints have three
> states during stance phase with the switches at φFF, φHO, and φTO.
> In other words, State 1 begins at heel-strike and ends with φFF,
> followed by State 2 which concludes at φHO. State 3, the last state
> in the stance phase, ends at φTO. During these three states, we
> adopted the same strategy as in Anil Kumar et al. (2020). That
> is, K and D vary as polynomial functions of t, while θref assumes
> constant values during each state.
> During swing phase, ankle angle does not vary much
> regardless of the slope angle – a motion achievable using constant
> K, D, and θref values.

#### 摘录 D
- 出处：第 11 页，Section `6. Conclusion`，行 28-55
> We propose a sloped walking control framework with fewer
> tuning parameters than the state-of-the-art controllers. The
> framework includes impedance control during stance phase
> and trajectory tracking during swing phase. The smooth
> transition between the two is facilitated by Bezier curves.
> The joint control parameters were determined through
> a data-driven optimization. Basis functions spanning the
> entire set of joint parameter functions were found through
> Principle Component Analysis. Given any slope angle, the
> stiﬀness and damping control parameters can be found as follows:
> ... The weights for these basis polynomials vary as functions of the
> slope angle ...
> Testing with an amputee and able-bodied subject proved the feasibility of the
> proposed scheme at varying slope angles.

### 2. 基于原文整理后的自然语言描述

The powered transfemoral prosthesis uses an extended gait-phase supervisor that partitions one stride into finite states, with four ankle states and five knee states. The stance submachine is delimited by heel-strike, flat-foot, heel-off, and toe-off, so the controller advances from `State 1` to `State 3` according to explicit biomechanical switching conditions before entering swing-specific behavior. Within each stance state, stiffness `K` and damping `D` are polynomial functions of normalized gait progress `t`, while the reference angle `θref` remains statewise constant; during swing, the controller switches to trajectory tracking, and Bezier curves smooth the stance-to-swing transition. The state outputs are not fixed globally, because the stiffness and damping basis-function weights are explicit functions of slope angle, which lets the same FSM skeleton retune push-off assistance and terrain adaptation continuously from downslope to upslope walking.

### 3. 逐句溯源

1. 句子 1：The powered transfemoral prosthesis uses an extended gait-phase supervisor that partitions one stride into finite states, with four ankle states and five knee states.
   对应摘录：B, C
2. 句子 2：The stance submachine is delimited by heel-strike, flat-foot, heel-off, and toe-off, so the controller advances from `State 1` to `State 3` according to explicit biomechanical switching conditions before entering swing-specific behavior.
   对应摘录：B, C
3. 句子 3：Within each stance state, stiffness `K` and damping `D` are polynomial functions of normalized gait progress `t`, while the reference angle `θref` remains statewise constant; during swing, the controller switches to trajectory tracking, and Bezier curves smooth the stance-to-swing transition.
   对应摘录：C, D
4. 句子 4：The state outputs are not fixed globally, because the stiffness and damping basis-function weights are explicit functions of slope angle, which lets the same FSM skeleton retune push-off assistance and terrain adaptation continuously from downslope to upslope walking.
   对应摘录：A, D
