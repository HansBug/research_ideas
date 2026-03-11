# A formal modeling methodology of the French railway interlocking system via HCPN - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：2
- 简要判断：论文直接给出了法国铁路联锁中的信号进路安全条件、进路建立检查链路以及 TP/DA/MO 等运行模式约束，适合整理为控制系统状态机描述。

## 条目 1: Route establishment in French railway interlocking
- 控制对象：法国铁路联锁系统中的进路建立控制逻辑

### 0. 条目识别与判定

- 一句话说明：这是轨道交通联锁领域的进路建立控制器，用于在列车请求通过某条 signal route 时检查安全条件、定位道岔并形成进路。
- 判断：算。对象是实际铁路联锁控制系统，原文明确给出了进路建立前置条件、检查顺序和形成流程。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，`2.1 Interlocking system`，行 92-100
> To fulﬁll the safety principles, the simplest but most important rule is that each
> train runs in own route. The route for a train to pass through is called “Signal
> Route”, usually guarded by mechanical, electrical and computer systems. There
> are interactions between paths, but no overlaps; the absolute separation of each
> route is a basic condition for the safety of railway trafﬁc. A signal route must meet
> the following conditions:
> all points must be set properly and locked;
> conﬂicting routes must be locked;
> the track must be clear.

#### 摘录 B
- 出处：第 6-7 页，`3.2.1 Mapping signaling control` 与 Figure 4 说明，行 239-299
> A signaling component is a sequence of commands and actions, similar to a
> working ﬂow chart with determining, selecting, loops and execution of speciﬁc
> instructions. Figure 4 illustrates a part of the RIS route establishment, including
> command and formation processes.
> Forbidden
> Route
> Incompatible
> RouteY
> N
> Y NRoute is forbidden ?
> Route is incompatible with
> existing routes
> Y N
> Turnouts
> switching
> YT
> urnout is in right position ?
> Turnout is free ?
> All turnouts of the route are
>  in right position ? Y N
> N
> …
> Command Formation!"##$%&'&
> (")*'
> (a)
> Route
> Request
> CmdRT
> IT
> Approuve
> CmdRTRoute
> Forbidden
> ERR
> Route
> Compatible
> CmdRT
> ALL Turnouts
> Positioned
> CmdRTRoute
> Incompatible
> ERRVerify Route Compatibility
> Verification CompatibleVerification Compatible
> Position Turnouts
> Aiguillage FormationAiguillage FormationVerify Route forbidden
> Verification InterditVerification Interdit
> cRT
> cRT
> cRT
> cRTerrcRT
> cRTerr (b)
> Figure 4: Example of mapping signaling control: (a) control ﬂow chart;
> (b) corresponding HCPN model.
> Figure 4(a) is the control ﬂow chart. It receives the route commands, and checks
> whether those commands are feasible and compatible with existing ones. Then it
> will format the route according to the formation information stored in the model,
> such as the positions of turnouts.

### 2. 基于原文整理后的自然语言描述

In the French railway interlocking system, each train is allowed to run only on its own signal route, and a route can be established only when all points are correctly set and locked, conflicting routes are locked, and the track is clear. When a route request is received, the controller first checks whether the route is forbidden and whether it is compatible with existing routes, then it switches and positions the required turnouts, and finally forms the command for the route.

### 3. 逐句溯源

1. 句子 1：In the French railway interlocking system, each train is allowed to run only on its own signal route, and a route can be established only when all points are correctly set and locked, conflicting routes are locked, and the track is clear.
   对应摘录：A
2. 句子 2：When a route request is received, the controller first checks whether the route is forbidden and whether it is compatible with existing routes, then it switches and positions the required turnouts, and finally forms the command for the route.
   对应摘录：B

## 条目 2: Movement mode gating in interlocking control
- 控制对象：法国铁路联锁系统中的运行模式选择与模式约束逻辑

### 0. 条目识别与判定

- 一句话说明：这是轨道交通联锁领域的上层模式控制逻辑，用于区分 TP、DA、MO 等列车运行/操作模式，并决定哪些进路命令可以进入形成过程。
- 判断：算。它管理的是联锁系统的实际运行模式与指令准入，不是工具流程或建模流程。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，`2.1 Interlocking system`，行 108-120
> Signaling control is a set of operating rules and control procedures of an
> interlocking system. It comprises computer automatic control and manual control.
> Normally, the computer processes are responsible for most of the device-oriented
> operations, such as route establishment, route auto-destruction, etc. while human
> despatchers deal with decision-making, such as route selection, mode selection,
> manual destruction, etc., and some non-regular operations, such as shunting
> operations.
> Thetrain runs on interlocking routes and are supervised by both route conditions
> and operating instructions.
> These three elements proposed will be the top level in the hierarchical model
> structure (ﬁg. 1). In the present architecture, trains communicate with signal
> control layers and interact with geographical route layers. The signal control layer
> directly controls the turnouts and signal lights according to its operating principles.

#### 摘录 B
- 出处：第 4 页，Figure 2 说明，行 157-163
> The CPN model shown in Figure 2 is an example of a HCPN model. The model
> on the left is one of the initial steps of the interlocking route establishment. The
> model in the right is a substituted transition of ‘mode TP’. In this paper, three types
> of train movements are considered: trance permanent (TP), destruction automatic
> (DA) and maintenance operation (MO). TP mode is only available in certain
> routes, so each route command based on TP mode should be checked before its
> formation process.

### 2. 基于原文整理后的自然语言描述

The signal-control part of the interlocking system combines automatic control with manual control. Computer procedures handle device-oriented operations such as route establishment and route auto-destruction, while dispatchers handle route selection, mode selection, manual destruction, and other non-regular operations. The modeled system distinguishes three movement modes, TP, DA, and MO, and any route command issued in TP mode must be checked before the route formation process starts because TP is allowed only on certain routes.

### 3. 逐句溯源

1. 句子 1：The signal-control part of the interlocking system combines automatic control with manual control.
   对应摘录：A
2. 句子 2：Computer procedures handle device-oriented operations such as route establishment and route auto-destruction, while dispatchers handle route selection, mode selection, manual destruction, and other non-regular operations.
   对应摘录：A
3. 句子 3：The modeled system distinguishes three movement modes, TP, DA, and MO, and any route command issued in TP mode must be checked before the route formation process starts because TP is allowed only on certain routes.
   对应摘录：B
