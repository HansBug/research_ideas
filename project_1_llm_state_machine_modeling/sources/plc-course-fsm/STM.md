# Teaching Finite State Machines (FSMs) as Part of a PLC Course - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机） / FSM（普通离散状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：三步 box-fill 过程与外层 auto/standby 许可回路都足够清楚，且两层关系明确。

## 条目 1: Three-state box fill FSM
- 控制对象：PLC 控制的 box fill 子过程
- 状态机类型：FSM（普通离散状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是离散制造与 PLC 顺序控制领域的箱体灌装子过程，用于驱动输送机与填充装置完成找箱、灌装和移走满箱。
- 判断：算。虽然它是教学型小规模案例，但对象仍是实际设备子过程控制，顺序阶段、切换条件、状态线圈和输出映射都很清楚。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5-6 页，Figure 3 前后的 box fill 状态说明，行 151-177
> There are three states.
> In state 10 the conveyor is running and we are looking  for
> an empty box as indicated by the proximity switch.  In state 20 the box is filled until the level swit ch is
> made.  In state 30 the conveyor runs until the prox imity switch clears indicating the full box is gone .  The
> transition from standby is made to state 30 so that  if there is a box on the conveyor it is removed be fore
> the fill operation begins.
> ...
> Coil C101 is a state because it is dependent on the  previous value of C101, C102, and C103.  Coil C102  is
> a state because it depends on the previous scan val ue of C102, and C103.

#### 摘录 B
- 出处：第 8-9 页，对 states 10/20/30 与输出逻辑的说明，行 191-245
> Rung two is the load box state, state 10.
> ...
> State 20 is the box fill state.
> If the box is loading and the proximity switch is a ctivated the state 20 coil, C102 energizes.  This d rops
> out the C101 coil, and C102 seals in the fill state.
> ...
> In state 30 there are two entry conditions.
> ...
> Thus on
> the transition to auto the conveyor starts and runs  until the proximity clears.
> ...
> When in state 20 and the leve l switch activates the box is full and the FSM move s to
> state 30.
> ...
> Finally the outputs Y001 conveyor run in auto, and Y002 box fill are functions of the states.  The
> conveyor runs in state 10 load box, and state 30 re move box.  The box fill output Y002 is energized wh en
> in state 20.  The logic for the outputs is combinat ional.

### 2. 基于原文整理后的自然语言描述

In the three-state box-fill FSM, state `30` is entered when the system leaves standby so that any box already on the conveyor is removed before a new fill cycle begins. State `10` then runs the conveyor while looking for an empty box with the proximity switch, and state `20` seals in the fill phase while the box is being filled until the level switch is made. When the level switch indicates that the box is full, the FSM returns to state `30`, where the conveyor runs until the proximity switch clears and confirms that the full box has gone. The state coils are `C101`, `C102`, and `C103`, while the outputs are combinational: `Y001` runs the conveyor in states `10` and `30`, and `Y002` energizes the box-fill action in state `20`.

### 3. 逐句溯源

1. 句子 1：In the three-state box-fill FSM, state `30` is entered when the system leaves standby so that any box already on the conveyor is removed before a new fill cycle begins.
   对应摘录：A, B
2. 句子 2：State `10` then runs the conveyor while looking for an empty box with the proximity switch, and state `20` seals in the fill phase while the box is being filled until the level switch is made.
   对应摘录：A, B
3. 句子 3：When the level switch indicates that the box is full, the FSM returns to state `30`, where the conveyor runs until the proximity switch clears and confirms that the full box has gone.
   对应摘录：A, B
4. 句子 4：The state coils are `C101`, `C102`, and `C103`, while the outputs are combinational: `Y001` runs the conveyor in states `10` and `30`, and `Y002` energizes the box-fill action in state `20`.
   对应摘录：A, B

## 条目 2: Auto/standby permissive around the sequence
- 控制对象：PLC 子过程外层的 auto/standby 控制
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是离散制造与 PLC 顺序控制领域的上层运行许可回路，用于在 auto 和 standby 之间切换并决定箱体灌装子过程是否允许运行。
- 判断：算。它管理的是设备子过程的运行模式和安全许可，本质上就是上层模式控制逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，对 auto/standby circuit 的描述，行 164-168
> The system can be in auto or standby, and for safet y includes a Normally Open (NO) contact from an
> external estop relay.  The auto standby circuit is operated by an NO Pushbutton (PB) for auto start, a nd a
> Normally Closed (NC) PB for stop.  This two state a uto/standby FSM is shown in rung one of Figure 4.
> Note that rung one is a two state FSM and rungs two  through four are a separate three state FSM.

### 2. 基于原文整理后的自然语言描述

The outer permissive is a separate two-state FSM that places the sub-process either in `auto` or in `standby`, and it includes the normally open external estop contact as part of the safety permissive. This outer FSM is operated by a normally open auto-start pushbutton and a normally closed stop pushbutton. In the ladder structure, rung one implements this auto/standby FSM, while rungs two through four implement the inner three-state box-fill FSM whose execution is gated by the outer permissive.

### 3. 逐句溯源

1. 句子 1：The outer permissive is a separate two-state FSM that places the sub-process either in `auto` or in `standby`, and it includes the normally open external estop contact as part of the safety permissive.
   对应摘录：A
2. 句子 2：This outer FSM is operated by a normally open auto-start pushbutton and a normally closed stop pushbutton.
   对应摘录：A
3. 句子 3：In the ladder structure, rung one implements this auto/standby FSM, while rungs two through four implement the inner three-state box-fill FSM whose execution is gated by the outer permissive.
   对应摘录：A
