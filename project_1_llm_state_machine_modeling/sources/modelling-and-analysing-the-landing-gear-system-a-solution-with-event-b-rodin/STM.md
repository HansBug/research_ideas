# Modelling and Analysing the Landing Gear System: a Solution with Event-B/Rodin - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对起落架系统的 handle、door automaton 以及 outgoing/retraction sequence 描述完整，证据清晰。

## 条目 1: Handle-driven outgoing sequence for landing gear actuation
- 控制对象：飞机起落架控制系统

### 0. 条目识别与判定

- 一句话说明：这是航空机电控制领域的 landing gear digital controller，用于接收飞行员 handle 命令并驱动门和起落架的伸放/回收序列。
- 判断：算。对象是实际起落架控制系统，原文明确给出了 handle 与 digital part 的关系、door state automaton，以及 outgoing sequence 的起止条件和步序控制变量。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，Analysing the landing system requirement，对 digital part 与 door automaton 的说明，行 69-105
> The landing system requirements have already been structured in a way that there is a clear separation between the digital part and the physical part. The physical part is mainly made of gears and doors; but there is also a cockpit viewed as a control and supervisory equipment; it is made of a handle driven by a human pilot.
>
> The digital part is located between the handle and the physical part: the orders from the digital part to the controlled (physical) part are originated from actioning the handle.
>
> we have drawn many state machines to capture the behaviour of doors, gears and the sequences of operations to extend or to retract the gears
>
> opening the doors ... unlock ... open position ... close ... EV open command ... EV close command ... door_closed

#### 摘录 B
- 出处：第 9-10 页，Modelling the outgoing sequence，对 outgoing sequence 的说明，行 290-315
> A thorough analysis of the two action sequences (outgoing sequence and retraction sequence) of the landing system helps us to capture the behaviour of the digital part. Even if they are nested each sequence is analysed precisely; it is made of a sequence of transition from state to state; each sequence is started as the effect of an action on the handle by the pilot.
>
> In order to control perfectly the evolution of the outgoing sequence we use a variable nextOGseq which indicates in the event guards the next step in the outgoing sequence. The variable is updated in the body of the events.
>
> The outgoing sequence is defined at the page 14 of the requirement document. It starts with the order DOWN and is finished when the gears are extended and door closed. Between these events we have an interaction involving the digital part which issues the orders, the physical part which executes the orders and the sensors which provide the various states of the gears and doors.

### 2. 基于原文整理后的自然语言描述

The landing gear system separates a physical part made of gears and doors from a digital part that sits between the pilot handle and the physical equipment, so actuation orders originate from handle actions. The door and gear behavior is organized with explicit state-machine style descriptions, including door opening, unlocking, open-position, and closing behavior. For gear extension, the outgoing sequence starts with the pilot order DOWN and ends when the gears are extended and the door is closed, and the digital controller uses the variable `nextOGseq` to track and guard the next step while coordinating commands with sensors and actuators.

### 3. 逐句溯源

1. 句子 1：The landing gear system separates a physical part made of gears and doors from a digital part that sits between the pilot handle and the physical equipment, so actuation orders originate from handle actions.
   对应摘录：A
2. 句子 2：The door and gear behavior is organized with explicit state-machine style descriptions, including door opening, unlocking, open-position, and closing behavior.
   对应摘录：A
3. 句子 3：For gear extension, the outgoing sequence starts with the pilot order DOWN and ends when the gears are extended and the door is closed, and the digital controller uses the variable `nextOGseq` to track and guard the next step while coordinating commands with sensors and actuators.
   对应摘录：B
