# A real-time semantics for the IEC 61499 standard - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 文件级角色：🧰 需清洗样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：ECC 执行语义、事件时间窗口和任务链/资源关系都可追溯，但仍偏构件级控制语义样本。

## 条目 1: BFB execution control chart (ECC)
- 控制对象：IEC 61499 分布式控制系统中的 Basic Function Block 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：显式时钟
- 原文细节充实度：🟠 C（只有主链）
- 描述细节充实度：🟠 C（只有主链）
- 数据集角色：🧰 清洗后保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是工业自动化与分布式控制领域的 IEC 61499 Basic Function Block 控制器，用于在输入事件到达后按 ECC 检查 guard、执行算法并在给定时间窗口内触发后续任务链。
- 判断：算，但属于控制软件构件级样本。它描述的是控制系统内部一个明确具有状态机语义和实时语义的执行单元，而不是某个具体物理装置的整机需求。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Background / IEC 61499，行 122-141
> In common all FB types provide an interface deﬁning input
> events with associated input data variables, and output events
> with associated output variables.
> The operation of a BFB is deﬁned (in a ﬁnite state machine
> like manner) by its Execution Control Chart (ECC), input/out-
> put events, and input/output/local variables. A transition condi-
> tion (edge in the ECC) is either a single input event, a Boolean
> expression (guard) on input/output and local variables, or a
> combination thereof. Each state in the ECC, implies an ordered
> set of zero or more algorithms to execute and output events to
> emit. On the arrival of an input event (provided by the resource
> scheduler), the associated input data connections are ﬁrst
> sampled to the input variables, then transition conditions from
> the current state are checked (in order given by occurrence
> in the underlying XML). On a transition the algorithms of the
> target state are sequentially executed (implying potential output
> events and local and output variable updates), the input event
> is (conceptually) consumed, and further transition conditions
> (from the target state) inspected transitively until no more
> transitions are possible.

#### 摘录 B
- 出处：第 3-4 页，Real-Time For the Masses / RTFM-core，行 215-247, 372-417
> Each event (e) is associated with an baseline bl(e)(absolute
> point in time for the arrival of the event), a relative deadline
> dl(e)(indicating the timing requirement), and a minimum
> inter-arrival time ia(e). An event ei, is associated (triggers) a
> corresponding task (instance) ti(can be seen as a job request
> related to SRP).
> The Permissible Execution Window (PEW) for (an instance
> of)tiis the range in time from its baseline bl(ti) =bl(ei)to
> its absolute deadline dl(ti) =bl(ei) +dl(ei), Figure 2.
> A task ti, may emit further synchronous and asynchronous
> events ej, which by default inherits the sender’s timing prop-
> erties ( bl(ej) =bl(ei); dl(ej) =dl(ei)), and hence the corre-
> sponding task tjexecutes under the sender’s PEW. On emitting
> a synchronous event, the corresponding task is (directly) exe-
> cuted and the sender is suspended until tjcompletes), while on
> emitting an asynchronous event the sender continues execution.
> ...
> Event ::= async After? Before? Min?
> j pend Before? Min?
> j sync
> After ::= after Int
> Before ::= before Int
> Min ::= min Int
> Figure 4. RTFM event grammar for IEC 61499.
> ...
> Event chains: For (asynchronous) events we have the
> option inherit or explicitly state timing constraints, (Figure 4).
> Theafter option allows us to deﬁne complex timing patterns
> (for which delays and periodic behavior are trivial cases),
> without the need to infer special design elements.
> ...
> In order to satisfy both the component view and allow for
> maximum ﬂexibility we propose that default event properties
> should be stated as part of the FB event outputs, while allowing
> to be over-ridden by properties given for the connections at
> network level.

#### 摘录 C
- 出处：第 5 页，事件源、任务链、资源与执行子任务说明，行 427-489
> IEC 61499 System model: Figure 5, depicts an IEC 61499
> model developed in the 4DIAC IDE [19]. The SIFB instances
> Ea1 andEc1 capture the external events from the underlying
> platform (or platforms if deployed onto different devices) and
> trigger the execution of actions associated to a1.i1 and
> c1.i1 respectively.
> ...
> Example: Event source: Assuming we deploy the system
> (application) onto a single device. The output events from
> SIFBs Ea1 andEc1 are obvious event sources (to the IEC
> 61499 network). In order to deﬁne the baseline, and should
> thus either be implemented natively in RTFM-core (and there
> originating from some ISR of the underlying hardware), or
> emitted with the pend option. In either case for the analysis
> the minimum inter-arrival should be stated using the min
> option.
> ...
> For the example, this
> gives us the (reduced) set of protected resources r(m)(for the
> ECC of m), its data output r(o)(for the connection m.OUT_1
> -> b1.di1 ) and the r(b)(for the ECC of b1).
> ...
> Each synchronous task
> chain, amounts to a RTFM task. For the example, the task chain
> triggered by ea1(with the sub-tasks a1:m1:b1) and task
> chain triggered by ec1(with the sub-tasks (c1) :a2:m2:b1,
> (c1) :b3:b2and (c1) :c2). Notice, this gives an upper bound
> to the set of sub-tasks executed on behalf of occurred source
> events ea1=ec1. For a given conﬁguration (ECC speciﬁcations
> of the FBs and FB states), actual execution involves a proper
> subset of the sub-tasks of the executing task.

### 2. 基于原文整理后的自然语言描述

A basic function block in IEC 61499 exposes input events with associated input data and output events with associated output data, and its ECC uses input events, Boolean guards, or combinations of both to trigger transitions. When an input event arrives, the block first samples the connected input data, checks the outgoing transition conditions of the current state in XML order, executes the algorithms of the target state sequentially, emits any output events, updates local and output variables, and then keeps firing further enabled transitions transitively until no transition remains possible. In the real-time semantics, every triggering event defines a task with a baseline, deadline, and minimum inter-arrival time, so execution is constrained by a permissible execution window; synchronous emissions inherit the sender timing and suspend the sender, whereas asynchronous emissions may use `after`, `before`, `min`, or `pend` to create explicit timing constraints. In the system example, Ea1 and Ec1 are event sources, `ea1` can trigger the synchronous task chain `a1:m1:b1`, and `ec1` can trigger `(c1):a2:m2:b1`, `(c1):b3:b2`, or `(c1):c2`, while the shared ECC/data resources `r(m)`, `r(o)`, and `r(b)` must be protected across chains. The concrete execution for an occurred source event is therefore only a proper subset of the upper-bound sub-task set, because it still depends on the current ECC specification and the current FB states.

### 3. 逐句溯源

1. 句子 1：A basic function block in IEC 61499 exposes input events with associated input data and output events with associated output data, and its ECC uses input events, Boolean guards, or combinations of both to trigger transitions.
   对应摘录：A
2. 句子 2：When an input event arrives, the block first samples the connected input data, checks the outgoing transition conditions of the current state in XML order, executes the algorithms of the target state sequentially, emits any output events, updates local and output variables, and then keeps firing further enabled transitions transitively until no transition remains possible.
   对应摘录：A
3. 句子 3：In the real-time semantics, every triggering event defines a task with a baseline, deadline, and minimum inter-arrival time, so execution is constrained by a permissible execution window; synchronous emissions inherit the sender timing and suspend the sender, whereas asynchronous emissions may use `after`, `before`, `min`, or `pend` to create explicit timing constraints.
   对应摘录：B
4. 句子 4：In the system example, Ea1 and Ec1 are event sources, `ea1` can trigger the synchronous task chain `a1:m1:b1`, and `ec1` can trigger `(c1):a2:m2:b1`, `(c1):b3:b2`, or `(c1):c2`, while the shared ECC/data resources `r(m)`, `r(o)`, and `r(b)` must be protected across chains.
   对应摘录：C
5. 句子 5：The concrete execution for an occurred source event is therefore only a proper subset of the upper-bound sub-task set, because it still depends on the current ECC specification and the current FB states.
   对应摘录：C
