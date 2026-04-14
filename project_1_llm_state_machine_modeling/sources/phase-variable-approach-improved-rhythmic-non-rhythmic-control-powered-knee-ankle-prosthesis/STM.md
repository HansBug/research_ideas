# A Phase Variable Approach for Improved Rhythmic and Non-Rhythmic Control of a Powered Knee-Ankle Prosthesis - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把主动膝踝假肢的相位变量控制器写成 `S1-S5` 五态 FSM，用 `FC`、大腿角、速度符号和 backward-stance guard 覆盖前进、后退与非节律动作。

## 条目 1: Five-state phase-variable supervisor for rhythmic and non-rhythmic prosthesis control

- 控制对象：医疗设备与生命支持控制领域的主动膝踝假肢相位变量监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个通过 `S1 stance / S2 pushoff onset / S3 preswing / S4 swing / S5 backward stance` 切换相位变量定义和关节输出的主动膝踝假肢控制器。
- 判断：算。对象是真实动力假肢控制器；原文明确给出状态集合、`FC`、大腿角 `qh`、`qpo / q41_h / q51_h` 阈值、速度符号和反向步态处理，并在人体实验中覆盖快慢走、急停急启、倒走、跨障碍和踢球。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> We introduce a new piecewise holonomic phase variable, which, through a finite state machine, forms the basis of our controller. The phase variable is constructed by measuring the thigh angle, and the transitions in the finite state machine are formulated through sensing foot contact along with attributes of a nominal reference gait trajectory. The controller was implemented on a powered knee-ankle prosthesis and tested with a transfemoral amputee subject ...

#### 摘录 B

- 出处：第 4 页，Section `B. Constructing the Phase Variable`
> The result is depicted in Fig. 2(a) in the form of an FSM with four states, where S1 and S2 pertain to the descending part of the thigh trajectory, and S3 and S4 correspond to the ascending part. Note that S1, S2, and S3 are all parts of the stance phase, and thus for all of these states FC = 1 ... transitioning from S1 (stance) to S2 (pushoff onset) occurs at a specific thigh angle (qh = qpo), and transitioning from S2 to S3 (pre-swing) occurs when qdot_h = 0.

#### 摘录 C

- 出处：第 4-5 页，Section `B. Constructing the Phase Variable` / Figure `2`
> In order to avoid this, we added another state, S5, to the FSM (Fig. 2(b)). This new state keeps the leg in stance phase when walking backward, and it transitions to pushoff only if the subject resumes moving forward. ... Transition from S5 to S1 ... happens when the subject steps backward and then decides to move forward. The transition condition is given by qh < q51_h ... Transition from S4 to S1 or S5 ... When foot contact happens (FC = 1), the transition will be to S1 if qh >= q41_h, otherwise it will be to S5 ...

#### 摘录 D

- 出处：第 1 页，Abstract / 第 6-8 页，Experiments
> The controller was implemented on a powered knee-ankle prosthesis and tested with a transfemoral amputee subject, who successfully performed a wide range of rhythmic and non-rhythmic tasks, including slow and fast walking, quick start and stop, backward walking, walking over obstacles, and kicking a soccer ball.

### 2. 基于原文整理后的自然语言描述

The powered knee-ankle prosthesis uses a five-state EFSM to choose which piecewise holonomic phase-variable definition should drive the knee and ankle virtual constraints. In forward walking, `S1` is stance, `S2` is pushoff onset, `S3` is preswing, and `S4` is swing; `S1-S3` keep `FC = 1`, `S1 -> S2` occurs at the thigh-angle threshold `qh = qpo`, and `S2 -> S3` occurs when thigh angular velocity changes sign. `S3` and `S4` use the ascending thigh trajectory, and a unidirectional phase filter prevents the preswing phase variable from decreasing as load is removed from the prosthetic leg. To support non-rhythmic tasks, the controller adds `S5 backward stance`, enters it from `S4` when foot contact occurs with `qh < q41_h`, and leaves it for normal stance only when the user reverses forward past `q51_h`. This makes the controller more than a stance-swing detector: it is an extended gait-phase supervisor whose guards, state-specific phase definitions and backward-walking recovery branch support slow/fast walking, start-stop, backward walking, obstacle crossing and kicking.

### 3. 逐句溯源

1. 句子 1：The powered knee-ankle prosthesis uses a five-state EFSM to choose which piecewise holonomic phase-variable definition should drive the knee and ankle virtual constraints.
   对应摘录：A, B, C
2. 句子 2：In forward walking, `S1` is stance, `S2` is pushoff onset, `S3` is preswing, and `S4` is swing; `S1-S3` keep `FC = 1`, `S1 -> S2` occurs at the thigh-angle threshold `qh = qpo`, and `S2 -> S3` occurs when thigh angular velocity changes sign.
   对应摘录：B
3. 句子 3：`S3` and `S4` use the ascending thigh trajectory, and a unidirectional phase filter prevents the preswing phase variable from decreasing as load is removed from the prosthetic leg.
   对应摘录：B
4. 句子 4：To support non-rhythmic tasks, the controller adds `S5 backward stance`, enters it from `S4` when foot contact occurs with `qh < q41_h`, and leaves it for normal stance only when the user reverses forward past `q51_h`.
   对应摘录：C
5. 句子 5：This makes the controller more than a stance-swing detector: it is an extended gait-phase supervisor whose guards, state-specific phase definitions and backward-walking recovery branch support slow/fast walking, start-stop, backward walking, obstacle crossing and kicking.
   对应摘录：A, C, D
