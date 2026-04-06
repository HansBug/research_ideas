# Brain-machine interfacing control of whole-body humanoid motion - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 humanoid contact-transition low-level controller 直接写成含子状态的 FSM，并清楚交代了 `Shift CoM / Move contact link`、way-point 修正和人工脑机干预如何改变控制链，足以作为双 A 的层次控制样本。

## 条目 1: Contact-transition whole-body humanoid controller

- 控制对象：通用控制与机器人任务领域的人形机器人全身接触转换监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个把 humanoid 多接触 whole-body motion 执行过程组织成 `Shift CoM / Move contact link` 两层结构的控制器，并允许脑机接口在加接触阶段修正中间 way-point。
- 判断：算。对象是真实 humanoid motion controller，而不是 EEG 分类流程或纯连续优化器；原文给出了状态名、各状态的动作语义、子状态划分，以及人工指令如何改变状态内行为。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，Section `3`，`paper_content.txt` 第 103-115 行
> The second stage of the controller is an on-line real-time low-level controller ... These objectives are autonomously decided by a finite-state machine (FSM) that encodes the current type of transition among the following two types:
>
> ... The corresponding FSM state is labeled “Shift CoM.”
>
> ... The corresponding FSM state is labeled “Move contact link.”
>
> As an example, a cyclic walking FSM state transition sequence will look like: Move contact link (left foot) → Shift CoM (on the left foot) → Move contact link (right foot) → Shift CoM (on the right foot) → Move contact link → ...

#### 摘录 B

- 出处：第 4 页，Section `5. Component Integration`，`paper_content.txt` 第 171-185 行
> When the robot is executing a step that requires moving a link to a planned contact location ... we decompose the motion of the end-link ... into two phases:
>
> • Lift-off phase ...
> • Touch-down phase ...
>
> Each of these two phases correspond to a sub-state of the meta-state “Move contact link” of the FSM, namely:
> • State “Move contact link to way-point”
> • State “Move contact link to goal”
>
> ... the transition from the former to the latter sub-state [is] triggered when the contact link crosses a designated threshold plan along the way ...

#### 摘录 C

- 出处：第 5-8 页，Section `5` 与 Figure `9`，`paper_content.txt` 第 237-240、307-308、342-344 行
> Manual user intervention, here through the brain command, is then necessary to un-block the motion of the link by adequately moving the tracked way-point.
>
> ... 8 commands (“up”/“down”) were sent during this controlled transition phase ... We then externally (manually) triggered the FSM transition to the following step ...
>
> The autonomous collision-avoidance strategy combined with the proposed BMI-control approach helps reposition the way-point and overcome the local-minimum problem. The robot safely reaches the goal contact location and the motion along the sequence can be completed.

### 2. 基于原文整理后的自然语言描述

The low-level humanoid controller follows a planned sequence of contact transitions through a hierarchical FSM rather than through a single undifferentiated continuous controller. At the top level it distinguishes removing-contact transitions from adding-contact transitions, using `Shift CoM` when the robot must unload a contact and `Move contact link` when a foot or hand must be guided to the next contact location. Inside the contact-adding branch, `Move contact link` is decomposed into `Move contact link to way-point` and `Move contact link to goal`, and the handoff between these sub-states is triggered before the link fully reaches the intermediate way-point so the motion stays smooth. The BMI command does not replace the nominal planner; it perturbs the tracked way-point during this step to escape collision-avoidance local minima and let the foot continue toward the stair contact. In the stair-climbing experiment, the user sent eight up/down commands during one contact-adding transition and the remaining sequence was then resumed, so the paper provides both the state hierarchy and the human correction semantics needed for a reusable STM sample.

### 3. 逐句溯源

1. 句子 1：The low-level humanoid controller follows a planned sequence of contact transitions through a hierarchical FSM rather than through a single undifferentiated continuous controller.
   对应摘录：A, B
2. 句子 2：At the top level it distinguishes removing-contact transitions from adding-contact transitions, using `Shift CoM` when the robot must unload a contact and `Move contact link` when a foot or hand must be guided to the next contact location.
   对应摘录：A
3. 句子 3：Inside the contact-adding branch, `Move contact link` is decomposed into `Move contact link to way-point` and `Move contact link to goal`, and the handoff between these sub-states is triggered before the link fully reaches the intermediate way-point so the motion stays smooth.
   对应摘录：B
4. 句子 4：The BMI command does not replace the nominal planner; it perturbs the tracked way-point during this step to escape collision-avoidance local minima and let the foot continue toward the stair contact.
   对应摘录：C
5. 句子 5：In the stair-climbing experiment, the user sent eight up/down commands during one contact-adding transition and the remaining sequence was then resumed, so the paper provides both the state hierarchy and the human correction semantics needed for a reusable STM sample.
   对应摘录：C
