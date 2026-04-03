# Time-Complemented Event-Driven Architecture for Distributed Automation Systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🧰 需清洗样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签概况：显式时钟、并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：Sorter1 的 ETA 接收、action schedule、diverter/labeler 并行推进和同步时钟执行链都能从正文串起来。

## 条目 1: Sorter1 control flow in a TCED sorting machine
- 控制对象：分拣机系统中 Sorter1 的调度与执行逻辑
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：并行、显式时钟
- 原文细节充实度：🟠 C（只有主链）
- 描述细节充实度：🟠 C（只有主链）
- 数据集角色：🧰 清洗后保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是工业分拣自动化领域的 Sorter1 控制模块，用于依据主控下发的到达时间计划执行贴标和分流动作。
- 判断：算。它直接控制分拣设备执行机构的调度与动作时机，具有清晰的命令接收、计划更新和执行推进过程。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3-4 页，sorting machine 主控与 sorter side threads，行 214-225
> In the case of the sorting machine, the scanner and sorters
> operate asynchronously as conceptually depicted in Fig. 5.T h e
> main controller is responsible for analyzing scan results andmaking sorting decisions. Once a decision has been made, a
> time-stamped message will be dispatched to the corresponding
> sorter’s controller. This message will inform the sorter con-
> troller of the scanned item’s estimated time of arrival (ETA).
> There are two threads running on the sorter side and are asfollows.
> 1) Thread A, with unit execution time D1, receives mes-
> sages from the main controller and adds ETA to its localtimetable.
> 2) Thread B, with unit execution time D2, repeatedly com-
> pares the sorter’s current local time with the earliest timeentry in its timetable. Once the time is reached, the sorter
> controller will actuate its labeler and diverter.

#### 摘录 B
- 出处：第 5 页，Figure 6-7 / Sorter1 control flow，行 337-381
> Fig. 6presents the schematic composition of the TCED
> module for the sorting machine’s ﬁrst sorter, Sorter1. Theformal model of this Sorter1 module, m
> s1, can be speciﬁed as
> ms1=/angbracketleftBig
> ps1,/braceleftBig
> mdi,mla/bracerightBig
> ,ls1/angbracketrightBig
> where
> mdi=/angbracketleftbig
> pdi,cdi,/braceleftbig
> aextend,aretract/bracerightbig
> ,ldi,vdi/angbracketrightbig
> is the TCED
> module for the diverter;
> mla=/angbracketleftbig
> pla,cla,/braceleftbig
> aglue,acutter/bracerightbig
> ,{mpr},lla,vla/angbracketrightbig
> is the
> TCED module for the labeler.
> The TCED module for the printer, mpr, can be again
> speciﬁed as
> mpr=/angbracketleftBig
> ppr,cpr,/braceleftBig
> asm1,asm2/bracerightBig
> ,lpr,vpr/angbracketrightBig
> .
> The overall dynamic behavior of a sorter is further illus-
> trated using the place/transition Petri net model shown inFig. 7. In particular, this Petri net model demonstrates the
> control ﬂow of Sorter1. The meanings of places and transi-tions are listed in Table I. The control ﬂow is initiated after an
> item is scanned ( T1). Firstly, the EDPM of the main controller
> as a central scheduler analyzes the received scan result ( P2).
> Then, module commands are dispatched to the corresponding
> sorter modules to schedule their actuations. In this particular
> case, the item is assigned to Sorter1 ( T3), whose EDPM con-
> sequently analyzes the received module command ( P4) and
> dispatches actuation schedules to its diverter and labeler mod-
> ules ( P5). Once the diverter EDPM has analyzed the received
> command ( P6), it updates its action schedule ( P7). Depending
> on the commands stored in the action schedule ( P8), the
> diverter TDCM decides when to actuate the extend and retract
> agents ( P9). As actions are scheduled based on synchronous
> clocks, actuations of the extend ( P10) and retract ( P12) agents
> are synchronized to the item’s movement. P11 andP13 denote
> availability of the extend and retract agents, respectively.

#### 摘录 C
- 出处：第 4-5 页，TCED formal definitions，行 249-336
> B. Formal Model of TCED Control Architecture
> The formal model of the TCED control architecture is
> defined following a top-down approach. The basic construction
> unit in the TCED architecture is called a module.
> Definition 1 (TCED Module):
> m=<p,c,A,T,l,v>
> where p is an EDPM; c is an optional TDCM;
> A is a set of reactive agents; T is a set of constituent TCED modules;
> l is a synchronized local clock; v is an optional action schedule.
> Definition 2 (EDPM): p=<IMC,OMC,IAC,theta,tau>
> where theta updates the action schedule v based on received commands,
> and tau schedules the executions of constituent TCED modules
> based on received module commands and current local time.
> Definition 3 (Action Command): ac=<e,R>
> where e is the action to be executed and R is a set of action parameters or execution results.
> Definition 4 (Module Command): mc=<ac,ts>
> where ts is a timestamp indicating the action's scheduled execution time.
> Definition 5 (TDCM): c=<OAC,mu>
> where mu dispatches action commands scheduled in v based on local time l.
> Finally, an action schedule v is a set of chronologically ordered module commands.

### 2. 基于原文整理后的自然语言描述

In the TCED sorting machine, the main controller analyzes each scanned item, chooses a target sorter, and sends that sorter a time-stamped message carrying the estimated time of arrival. On the sorter side, Thread A, with unit execution time D1, inserts the received ETA into a local timetable, while Thread B, with unit execution time D2, repeatedly compares the synchronized local time with the earliest timetable entry and actuates the labeler and diverter as soon as the scheduled time is reached. Formally, Sorter1 is a TCED module ms1=<ps1,{mdi,mla},ls1>, where mdi is the diverter module, mla is the labeler module, and mla contains the printer submodule mpr; these modules share a synchronized local clock and an action schedule v that is a chronologically ordered set of timestamped module commands mc=<ac,ts>, updated by the EDPM and dispatched by the TDCM. In the Sorter1 control flow, once the item is assigned to Sorter1, its EDPM dispatches actuation schedules to the diverter and labeler branches, the diverter EDPM updates its schedule, and the diverter TDCM decides when to actuate the extend and retract agents, whose actual actuations are synchronized to the item’s movement while P11 and P13 represent extend/retract availability. While the diverter branch is processing its module command, the labeler branch concurrently analyzes its own command, updates its action schedule, dispatches the schedule to the printer module, and lets the labeler TDCM decide the cutter and glue-dispenser actions according to the stored schedule.

### 3. 逐句溯源

1. 句子 1：In the TCED sorting machine, the main controller analyzes each scanned item, chooses a target sorter, and sends that sorter a time-stamped message carrying the estimated time of arrival.
   对应摘录：A, B
2. 句子 2：On the sorter side, Thread A, with unit execution time D1, inserts the received ETA into a local timetable, while Thread B, with unit execution time D2, repeatedly compares the synchronized local time with the earliest timetable entry and actuates the labeler and diverter as soon as the scheduled time is reached.
   对应摘录：A
3. 句子 3：Formally, Sorter1 is a TCED module ms1=<ps1,{mdi,mla},ls1>, where mdi is the diverter module, mla is the labeler module, and mla contains the printer submodule mpr; these modules share a synchronized local clock and an action schedule v that is a chronologically ordered set of timestamped module commands mc=<ac,ts>, updated by the EDPM and dispatched by the TDCM.
   对应摘录：B, C
4. 句子 4：In the Sorter1 control flow, once the item is assigned to Sorter1, its EDPM dispatches actuation schedules to the diverter and labeler branches, the diverter EDPM updates its schedule, and the diverter TDCM decides when to actuate the extend and retract agents, whose actual actuations are synchronized to the item’s movement while P11 and P13 represent extend/retract availability.
   对应摘录：B
5. 句子 5：While the diverter branch is processing its module command, the labeler branch concurrently analyzes its own command, updates its action schedule, dispatches the schedule to the printer module, and lets the labeler TDCM decide the cutter and glue-dispenser actions according to the stored schedule.
   对应摘录：B
