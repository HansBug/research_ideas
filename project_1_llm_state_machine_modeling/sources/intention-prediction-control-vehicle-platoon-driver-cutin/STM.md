# Intention Prediction-Based Control for Vehicle Platoon to Handle Driver Cut-In - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把混合交通环境中车队对人驾车辆 cut-in 的应对写成 `CF / cut-in prevention / cut-in yielding` 三态高层 FSM，并用意图预测、可防止区间与实验状态轨迹把转移链讲清楚。

## 条目 1: Cut-In Prevention and Yielding Supervisor

- 控制对象：混合交通场景中车辆编队应对人驾车辆 cut-in 的高层模式选择控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个车队高层监督器，用 `CF`、`cut-in prevention` 与 `cut-in yielding` 三种模式在保持 platoon 完整性和道路安全之间切换。
- 判断：算。对象是实际车辆编队控制器，原文明确写出状态集合、基于 cut-in 意图与可防止区间的转移条件，并用 mandatory / discretionary 两类实验展示状态切换结果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5 页，Section IV-A High-Level FSM，行 469-516
> The high-level FSM is built to select control strategy for the VP to handle the cut-ins. The FSM consists of three states: the `CF`, `cut-in prevention`, and `cut-in yielding` states. In the `CF` state, the followers of the VP perform car-following to maintain a defined distance from the preceding vehicle. In the `cut-in prevention` state, the VP shortens the platoon gap to prevent the cut-ins of the HDV. In the `cut-in yielding` state, the VP yields to the cut-in vehicle by creating a safe distance. The state transitions are managed according to the predicted cut-in intention, the surrounding information, and the predicted trajectory of the HDV with respect to the VP. If the nearby HDV has no cut-in intention, the FSM remains in `CF`. If it has discretionary cut-in intention and the cut-in vehicle is in the preventable range, the FSM switches to `cut-in prevention`. If it suggests mandatory cut-in intention, or discretionary intention in the unpreventable range, the FSM switches to `cut-in yielding`. In the `cut-in prevention` state, the FSM returns to `CF` when the vehicle leaves the detectable range without cutting in, and switches to `cut-in yielding` when the vehicle becomes unpreventable. In the `cut-in yielding` state, the FSM returns to `CF` when the cut-in vehicle reaches the target lane.

#### 摘录 B

- 出处：第 9-10 页，Section V-B/C Experiments，行 1079-1085, 1151-1185
> In the mandatory cut-in test, the FSM state is switched from the `CF` state to the `cut-in yielding` state at 2.4 s, when the proposed method detects the cut-in intention of the HDV. Next, the FSM state is switched to the `CF` state at 5.4 s, when the cut-in vehicle reaches the target lane. In the discretionary cut-in within the preventable range test, the FSM state is switched from the `CF` state to the `cut-in prevention` state at 2.2 s when the proposed method detects the cut-in intention of the HDV, and the FSM remains in the `cut-in prevention` state as the HDV is in the detectable range. In the discretionary cut-in beyond the preventable range test, the FSM state is switched from the `CF` state to the `cut-in yielding` state at 2.2 s, and then switched to the `CF` state at 3.8 s when the cut-in vehicle reaches the target lane.

### 2. 基于原文整理后的自然语言描述

The vehicle-platoon controller uses a three-state high-level FSM with `CF`, `cut-in prevention`, and `cut-in yielding` to decide whether the target follower should keep its nominal platoon gap, shorten the gap to block a discretionary cut-in, or enlarge the gap to yield safely. The controller leaves `CF` only after the intention-prediction module and trajectory analysis indicate that a nearby human-driven vehicle intends to cut in, and it distinguishes preventable and unpreventable situations according to cut-in motivation and predicted trajectory. When the predicted cut-in is discretionary and still preventable, the FSM enters `cut-in prevention`; when the maneuver is mandatory or already unpreventable, it enters `cut-in yielding`; and once the cut-in vehicle either abandons the maneuver or finishes entering the target lane, the FSM returns to `CF`. Driver-in-the-loop experiments then validate the same state chain by showing concrete mode switches for mandatory cut-ins, discretionary cut-ins within the preventable range, and discretionary cut-ins beyond the preventable range.

### 3. 逐句溯源

1. 句子 1：The vehicle-platoon controller uses a three-state high-level FSM with `CF`, `cut-in prevention`, and `cut-in yielding` to decide whether the target follower should keep its nominal platoon gap, shorten the gap to block a discretionary cut-in, or enlarge the gap to yield safely.
   对应摘录：A
2. 句子 2：The controller leaves `CF` only after the intention-prediction module and trajectory analysis indicate that a nearby human-driven vehicle intends to cut in, and it distinguishes preventable and unpreventable situations according to cut-in motivation and predicted trajectory.
   对应摘录：A
3. 句子 3：When the predicted cut-in is discretionary and still preventable, the FSM enters `cut-in prevention`; when the maneuver is mandatory or already unpreventable, it enters `cut-in yielding`; and once the cut-in vehicle either abandons the maneuver or finishes entering the target lane, the FSM returns to `CF`.
   对应摘录：A
4. 句子 4：Driver-in-the-loop experiments then validate the same state chain by showing concrete mode switches for mandatory cut-ins, discretionary cut-ins within the preventable range, and discretionary cut-ins beyond the preventable range.
   对应摘录：B
