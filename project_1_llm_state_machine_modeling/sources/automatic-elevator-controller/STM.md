# Automatic Elevator Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自动电梯控制器直接建成由楼层态和运动态组成的 FSM，并给出从 `F1/F2/F3` 到 `MU2/MU3/MD1/MD2` 的具体跃迁示例，足够形成双 A 楼宇样本。

## 条目 1: Three-Floor Automatic Elevator Floor-Transition FSM

- 控制对象：三层自动电梯的楼层与升降方向控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个三层自动电梯控制器，用楼层状态、上/下行运动状态、楼层请求输入、到位传感输入和复位逻辑完成电梯的自动运行。
- 判断：算。对象是真实楼宇机电控制器，原文不只说“用了 FPGA”，而是明确写出理想初始态、上/下行两类运动态、状态名 `F1/F2/F3/MU2/MU3/MD1/MD2` 以及多组具体转移。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 23-26 行
> Automatic elevators runs without having floor buttons pressed. When passenger enters and/or leaves the elevator cab, door sensors detects passengers as they enters and /or leaves. After the doors closed, the elevator will starts to run by it's own. Three level efficient elevator control system is designed by simply changing the state diagram ...

#### 摘录 B

- 出处：第 4 页，`5 Algorithm`，`paper_content.txt` 第 122-134 行
> Initially the system is in the ideal state. the elevator will generally move in two state i.e up or down.
>
> If the elevator is moving in upward direction it will stop at desired floor and it will check for its next destination.
>
> And if the elevator is moving in downward direction it will stop at desired floor and it will check for its subsequent destination.
>
> According to the request from any floor the elevator will either move in downward direction or upward direction.
>
> If the system is reset, it will arrive to its ideal position regardless of any request.

#### 摘录 C

- 出处：第 5-7 页，`6 Result and Analysis`，`paper_content.txt` 第 155-208 行
> Here, floor1, floor2, floor3 are indicating the three floors of the elevators.
>
> The two states MU2 and MU3 indicates that the motor is moving in upwards direction ... Similarly, the other two states MD1 and MD2 indicates that the motor is moving downward direction ...
>
> PS1, PS2, PS3 are the inputs for floor1, floor2, floor3. S1, S2, S3 are the inputs for sensing MU2, MU3, MD1, MD2.
>
> Initially the elevator is on floor 1 when PS2 detects the person ... the state change from F1 to MU2 ... when S2 equal to "1" the next state changes from MU2 to F2 ...
>
> Initially the elevator is on floor 3 when PS1 detects the person ... the state change from F3 to MD1 ... when S1 equal to "1" the next state changes from MD1 to F1 ...
>
> Initially the elevator is on floor 2 as soon as rst =1 the elevator changes its state and come to its original position i.e floor 1.

### 2. 基于原文整理后的自然语言描述

The automatic elevator controller is built as a finite-state machine whose state space combines floor states `F1`, `F2`, and `F3` with motion states `MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel. In the normal workflow, the system starts from an ideal state, chooses either the up or down branch according to floor requests, stops at the requested floor, and then immediately checks the next destination before deciding whether to continue moving. The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as sensing inputs for arrival, so transitions such as `F1 -> MU2 -> F2`, `F2 -> MU3 -> F3`, `F3 -> MD1 -> F1`, and `F3 -> MD2 -> F2` are explicitly defined in the paper. The `hbrg` output distinguishes upward drive, downward drive, and stop conditions, while the reset signal forces the controller back to floor `1` regardless of the outstanding request context. Although the implementation is described in VHDL/FPGA terms, the underlying control object is still a concrete three-floor elevator supervisor rather than a generic hardware demo.

### 3. 逐句溯源

1. 句子 1：The automatic elevator controller is built as a finite-state machine whose state space combines floor states `F1`, `F2`, and `F3` with motion states `MU2`, `MU3`, `MD1`, and `MD2` for upward and downward travel.
   对应摘录：B, C
2. 句子 2：In the normal workflow, the system starts from an ideal state, chooses either the up or down branch according to floor requests, stops at the requested floor, and then immediately checks the next destination before deciding whether to continue moving.
   对应摘录：B
3. 句子 3：The controller uses `PS1/PS2/PS3` as floor-request inputs and `S1/S2/S3` as sensing inputs for arrival, so transitions such as `F1 -> MU2 -> F2`, `F2 -> MU3 -> F3`, `F3 -> MD1 -> F1`, and `F3 -> MD2 -> F2` are explicitly defined in the paper.
   对应摘录：C
4. 句子 4：The `hbrg` output distinguishes upward drive, downward drive, and stop conditions, while the reset signal forces the controller back to floor `1` regardless of the outstanding request context.
   对应摘录：C
5. 句子 5：Although the implementation is described in VHDL/FPGA terms, the underlying control object is still a concrete three-floor elevator supervisor rather than a generic hardware demo.
   对应摘录：A, C
