# A real-time semantics for the IEC 61499 standard - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：ECC 驱动逻辑和系统示例都可追溯，但示例状态名主要在图中。

## 条目 1: BFB execution control chart (ECC)
- 控制对象：IEC 61499 分布式控制系统中的 Basic Function Block 控制器

### 0. 条目识别与判定

- 一句话说明：这是工业自动化与分布式控制领域的 IEC 61499 Basic Function Block 控制器，用于在接收输入事件后依据 ECC 执行算法并发出输出事件。
- 判断：算，但属于控制软件构件级样本。它描述的是控制系统内部一个明确具有状态机语义的执行单元，而不是某个具体物理装置的整机需求。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Background / IEC 61499，行 122-140
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

#### 摘录 B
- 出处：第 5 页，System model example，行 427-449
> B. System model example
> IEC 61499 System model: Figure 5, depicts an IEC 61499
> model developed in the 4DIAC IDE [19]. The SIFB instances
> Ea1 andEc1 capture the external events from the underlying
> platform (or platforms if deployed onto different devices) and
> trigger the execution of actions associated to a1.i1 and
> c1.i1 respectively. Figure 6 depicts the ECC of b1, showing
> the associated actions (algorithms) taskb1 for input event
> i1andtaskb3 for input event i3respectively. The mis
> an FB (from the standard library) that merges (and serialize)
> incoming events (and associated data).
> Figure 5. Example IEC 61499 system model.
> Figure 6. ECC of FB b1.
> Example: Event source: Assuming we deploy the system
> (application) onto a single device. The output events from
> SIFBs Ea1 andEc1 are obvious event sources (to the IEC
> 61499 network). In order to deﬁne the baseline, and should
> thus either be implemented natively in RTFM-core (and there
> originating from some ISR of the underlying hardware), or
> emitted with the pend option. In either case for the analysis
> the minimum inter-arrival should be stated using the min
> option. Figure 7, depicts the timing property of the event
> Ea1.o1 -> a1.i1 at the network level.

#### 摘录 C
- 出处：第 5 页，事件链、资源与执行子任务说明，行 451-489
> Example: Event chains: If not explicitly stated, events are
> considered to be synchronous, i.e. the event chains originating
> from event sources will be treated as synchronous task chains
> in the model and for execution. For the example, this amounts
> to the set of tasks and resources depicted in Figure 8.Example: Resources: The assumption that dl(t)ia(t)
> (and that the system is schedulable), only the RTFM resources
> that are shared between tasks chains triggered by different
> event sources needs to be protected. For the example, this
> gives us the (reduced) set of protected resources r(m)(for the
> ECC of m), its data output r(o)(for the connection m.OUT_1
> -> b1.di1 ) and the r(b)(for the ECC of b1). Notice here,
> that the ECC of b1triggers an output event o1only on a
> incoming i3event, which in turn occurs on behalf of the
> single source event Ec1.o1 , thus neither the state of b2nor
> the data connection b1.d -> b2.d1 needs protection.
> a1 b1
> b2b3 a2
> c1c2ea1
> ec1m1
> m2r(b) r(m)r(o)c(a1)=50c(m1)=1c(b1)=1
> c(b2)=2 c(a2)=5
> c(m2)=1c(b3)=5
> c(c1)=5c(c2)=3
> Figure 8. Example RTFM system model. We have the (external) events
> ea1andec1, triggering the task chains headed by a1andc1respectively.
> Asynchronous events are marked as dashed, tasks are denoted by circles, boxes
> r(m),r(b)are resources for the corresponding FBs, while r(o)is a resource
> for a shared connection.
> Example: Scheduling: At device level, RTFM models
> can be scheduled efﬁciently by the RTFM-kernel, exploiting
> the underlying interrupt hardware[15]. Each synchronous task
> chain, amounts to a RTFM task. For the example, the task chain
> triggered by ea1(with the sub-tasks a1:m1:b1) and task
> chain triggered by ec1(with the sub-tasks (c1) :a2:m2:b1,
> (c1) :b3:b2and (c1) :c2). Notice, this gives an upper bound
> to the set of sub-tasks executed on behalf of occurred source
> events ea1=ec1. For a given conﬁguration (ECC speciﬁcations
> of the FBs and FB states), actual execution involves a proper
> subset of the sub-tasks of the executing task.

### 2. 基于原文整理后的自然语言描述

A basic function block in IEC 61499 is organized by an Execution Control Chart that reacts to input events, checks transition conditions, and then executes the algorithms and output events attached to the selected branch. In the example model, external events from Ea1 and Ec1 trigger the associated actions, and the ECC of b1 provides the behavior for its i1 and i3 inputs. At execution time, only the proper subset of sub-tasks corresponding to the current ECC specifications and FB states is carried out on behalf of the source events that have occurred.

### 3. 逐句溯源

1. 句子 1：A basic function block in IEC 61499 is organized by an Execution Control Chart that reacts to input events, checks transition conditions, and then executes the algorithms and output events attached to the selected branch.
   对应摘录：A
2. 句子 2：In the example model, external events from Ea1 and Ec1 trigger the associated actions, and the ECC of b1 provides the behavior for its i1 and i3 inputs.
   对应摘录：B
3. 句子 3：At execution time, only the proper subset of sub-tasks corresponding to the current ECC specifications and FB states is carried out on behalf of the source events that have occurred.
   对应摘录：C
