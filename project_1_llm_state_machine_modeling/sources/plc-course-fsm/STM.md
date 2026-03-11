# Teaching Finite State Machines (FSMs) as Part of a PLC Course - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：2
- 简要判断：给出了非常干净的 box-fill 三态 FSM 和 auto/standby 二态 FSM。

## 条目 1: Three-state box fill FSM
- 控制对象：PLC 控制的 box fill 子过程
- 整理后的英文描述：The box fill process is modeled as a three-state FSM. In state 10 the conveyor looks for an empty box, in state 20 the box is filled until the level switch is made, and in state 30 the conveyor runs until the full box clears the proximity switch. The sequence cycles 10 -> 20 -> 30 -> 10 while auto is active.
- 要素 1：显式状态：`state 10`, `state 20`, `state 30`。
- 要素 2：`state 10` 查找空箱；`state 20` 执行灌装；`state 30` 移走满箱。
- 要素 3：`state 10` 从 `state 30` 进入并向 `state 20` 退出。
- 要素 4：`state 20` 在 level switch 激活后进入 `state 30`。
- 要素 5：`state 30` 的 exit condition 是 `state 20`，完成后循环回到装箱阶段。
- 定位 1：`paper_content.txt` 第 5 页，Figure 3 前的过程描述，行 149-156。
- 定位 2：`paper_content.txt` 第 8-9 页，对 state 10/20/30 的逐段解释，行 219-239。
- 证据 1：`In state 10 the conveyor is running and we are looking for an empty box`
- 证据 2：`In state 20 the box is filled until the level switch is made`
- 证据 3：`In state 30 the conveyor runs until the proximity switch clears`
- 证据 4：`When in state 20 and the level switch activates ... the FSM moves to state 30`

## 条目 2: Auto/standby two-state FSM with estop permissive
- 控制对象：PLC 序列控制的自动/待机切换逻辑
- 整理后的英文描述：The system can be in `auto` or `standby`; the auto/standby circuit is implemented as a two-state FSM, with an estop permissive included in the logic. This outer FSM enables or disables the three-state box-fill sequence.
- 要素 1：显式状态：`auto` 与 `standby`。
- 要素 2：切换由 auto start pushbutton、stop pushbutton 和 estop permissive 共同约束。
- 要素 3：该二态 FSM 与后续 box-fill 三态 FSM 分层组合。
- 定位 1：`paper_content.txt` 第 6 页，对 auto/standby circuit 的描述，行 162-168。
- 证据 1：`The system can be in auto or standby`
- 证据 2：`This two state auto/standby FSM is shown in rung one of Figure 4`
