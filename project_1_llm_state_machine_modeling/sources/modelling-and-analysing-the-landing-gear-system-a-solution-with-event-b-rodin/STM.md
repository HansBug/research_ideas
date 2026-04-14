# Modelling and Analysing the Landing Gear System: a Solution with Event-B/Rodin - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对起落架系统的 handle、door automaton 以及 outgoing/retraction sequence 描述完整，证据清晰。

## 条目 1: Handle-driven outgoing sequence for landing gear actuation
- 控制对象：飞机起落架控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G6 起落架 handle-门-起落架序列）

### 0. 条目识别与判定

- 一句话说明：这是航空机电控制领域的 landing gear digital controller，用于接收飞行员 handle 命令并驱动门和起落架的伸放/回收序列。
- 判断：算。对象是实际起落架控制系统，原文明确给出了 handle 与 digital part 的关系、door state automaton，以及 outgoing sequence 的起止条件和步序控制变量。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，Analysing the landing system requirement，对 digital part、door automaton 与 state machines 的说明，行 69-105
> The landing system requirements have already been structured in a way that there is a clear separation between the digital part and the physical part. The physical part is mainly made of gears and doors; but there is also a cockpit viewed as a control and supervisory equipment; it is made of a handle driven by a human pilot.
>
> The digital part is located between the handle and the physical part: the orders from the digital part to the controlled (physical) part are originated from actioning the handle.
>
> we have drawn many state machines to capture the behaviour of doors, gears and the sequences of operations to extend or to retract the gears
>
> opening the doors ... unlock ... open position ... close ... EV open command ... EV close command ... door_closed

#### 摘录 B
- 出处：第 7-8 页，The interface of the digital part，对 triplicated inputs、order outputs 与 monitoring outputs 的说明，行 224-271
> we distinguish three categories of variables at the interface of the digital part.
>
> the input variables: handle, gear_extended, gear_retracted, analogical_switch, door_closed, door_open, etc.,
>
> the order output variables: general_EV, close_EV, open_EV, extend_EV and retract_EV
>
> the state output variables: gears_locked_down, gears_maneuvering and anomaly
>
> The input variables are triplicated ... handle ∈ TRIPLE → HSTATE ... gear_extended ∈ (TRIPLE × GEAR) → BOOL ... door_closed ∈ (TRIPLE × DOOR) → BOOL ... door_open ∈ (TRIPLE × DOOR) → BOOL

#### 摘录 C
- 出处：第 9-11 页，Deriving events from the action sequences / Modelling the outgoing sequence / Control events family，行 284-372
> A thorough analysis of the two action sequences (outgoing sequence and retraction sequence) of the landing system helps us to capture the behaviour of the digital part. Even if they are nested each sequence is analysed precisely; it is made of a sequence of transition from state to state; each sequence is started as the effect of an action on the handle by the pilot.
>
> In order to control perfectly the evolution of the outgoing sequence we use a variable nextOGseq which indicates in the event guards the next step in the outgoing sequence. The variable is updated in the body of the events.
>
> The outgoing sequence is defined at the page 14 of the requirement document. It starts with the order DOWN and is finished when the gears are extended and door closed.
>
> handleDown ... stmlt_generalEV ... stmlt_door_openEV ... stmlt_gear_outgoingEV ... stop_stmlt_gear_outgoingEV ... stop_stmlt_door_closeEV ... stmlt_door_closeEV ... stop_stmlt_door_closeEV ... stop_stmlt_generalEV
>
> event stmlt_gear_outgoing ... @g0 general_EV = TRUE ... @g1 order = hDown ... @g2 ran(handle) = {hDown} ... @g3 ran(door_closed) = {FALSE} ... @g4 ran(door_open) = {TRUE} ... @next nextOGseq = 3 ... @ga no anomaly = FALSE ... @notretract retract_EV = FALSE

#### 摘录 D
- 出处：第 14-15 页，Door behaviour / Gear behaviour，对门与起落架状态机的说明，行 444-521
> The door behaviour is described at page 11 of the requirement document. It is first captured with a state automata; the transitions of the automata are then described as events. For this purpose we use a transition function doorState ∈ DOOR → DSTATE where DSTATE = {ClosedLocked, ClosedUnlocked, OpenUnlocked}
>
> The starting transition of the door behaviour is enabled by the open_EV order ... there is a synchronisation between the digital part and the doors.
>
> The gear behaviour is specified in the same way as the doors ... gearState ∈ GEAR → GSTATE where GSTATE = {RetractedLocked, RetractedUnlocked, ExtendedUnlocked, ExtendedLocked}
>
> The labels of the transition correspond to the events that model the behaviour of the gears.

### 2. 基于原文整理后的自然语言描述

The landing gear controller separates a digital part from the physical doors and gears, and it receives triplicated pilot and sensor inputs such as `handle`, `door_open`, `door_closed`, `gear_extended`, and `gear_retracted` while issuing the order outputs `general_EV`, `open_EV`, `close_EV`, `extend_EV`, and `retract_EV` together with monitoring outputs such as `gears_locked_down`, `gears_maneuvering`, and `anomaly`. The physical side is modeled with explicit automata: each door moves through `ClosedLocked`, `ClosedUnlocked`, and `OpenUnlocked`, and each gear moves through `RetractedLocked`, `RetractedUnlocked`, `ExtendedUnlocked`, and `ExtendedLocked`, with door and gear transitions synchronized by the corresponding electro-valve orders. For the outgoing sequence, a pilot `DOWN` order starts a control cycle whose ordered steps are to stimulate `general_EV`, stimulate `open_EV`, stimulate `extend_EV` once all three doors are open, stop `extend_EV` once all three gears are locked down, stop door opening and stimulate door closure, stop `close_EV` once the three doors are closed, and finally stop `general_EV`. The digital part stores the pilot order in `order` and uses `nextOGseq` in event guards to force the next legal step, while the current sensor values and the `anomaly = FALSE` condition decide whether the sequence may continue.

### 3. 逐句溯源

1. 句子 1：The landing gear controller separates a digital part from the physical doors and gears, and it receives triplicated pilot and sensor inputs such as `handle`, `door_open`, `door_closed`, `gear_extended`, and `gear_retracted` while issuing the order outputs `general_EV`, `open_EV`, `close_EV`, `extend_EV`, and `retract_EV` together with monitoring outputs such as `gears_locked_down`, `gears_maneuvering`, and `anomaly`.
   对应摘录：A, B
2. 句子 2：The physical side is modeled with explicit automata: each door moves through `ClosedLocked`, `ClosedUnlocked`, and `OpenUnlocked`, and each gear moves through `RetractedLocked`, `RetractedUnlocked`, `ExtendedUnlocked`, and `ExtendedLocked`, with door and gear transitions synchronized by the corresponding electro-valve orders.
   对应摘录：A, D
3. 句子 3：For the outgoing sequence, a pilot `DOWN` order starts a control cycle whose ordered steps are to stimulate `general_EV`, stimulate `open_EV`, stimulate `extend_EV` once all three doors are open, stop `extend_EV` once all three gears are locked down, stop door opening and stimulate door closure, stop `close_EV` once the three doors are closed, and finally stop `general_EV`.
   对应摘录：C
4. 句子 4：The digital part stores the pilot order in `order` and uses `nextOGseq` in event guards to force the next legal step, while the current sensor values and the `anomaly = FALSE` condition decide whether the sequence may continue.
   对应摘录：C
