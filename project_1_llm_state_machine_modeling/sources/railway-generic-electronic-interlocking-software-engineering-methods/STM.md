# Establish a generic railway electronic interlocking solution using software engineering methods - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：文献把 generic railway interlocking 的 route request、route call、train occupation、fault 与 safety-critical event 都落成 `UML statecharts` 和 Route 3 测试链，足以形成细节完整的铁路联锁样本。

## 条目 1: Route-3 request-call-occupation interlocking supervisor

- 控制对象：电子铁路联锁软件中 Route 3 的设路、呼叫、占用与故障安全控制链
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是轨道交通与铁路控制领域的电子联锁 route supervisor，用 `UML statecharts` 和布尔联锁函数协调 Route 3 所需的信号、轨道区段和 point machine 的申请、锁闭、呼叫、占用清除与 fail-safe 取消。
- 判断：算。对象是实际铁路联锁软件的运行控制链，原文不仅说明了 route request / call / occupation / safety-critical event 的流程，还用 Route 3 的具体元素 `s3/s5/Tb/Tc/Ty/w1` 给出了逐状态测试结果与故障回退行为。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 80-89 行
> The interlocking system is modelled using Boolean interlocking functions and UML (Unified Modelling Language) statecharts. Statecharts are used to graphically represent the procedures of interlocking operations. ... The behaviour of the interlocking during element faults and safety-critical events is validated through graphical software simulations.

#### 摘录 B

- 出处：第 67-70 页，`4.5.2 Primary Functions`，`paper_content.txt` 第 2184-2251、2260-2297 行
> A route request determines if a route can be set for a train to travel in a station. ... no conflicting routes ... current state and availability of the signals ... track sections ... points ...
>
> Set Route ... the track sections are checked again and then sequentially changed to a yellow indication from the destination signal backwards to the start signal. Next, the aspect of the start signal clears to yellow. Yellow indicates that the state of the elements have been set and reserved.
>
> Route Call ... the overlap turns yellow ... the start signal clears to green which indicates that the route is ready for occupation.
>
> Train Occupation ... As the train occupies this track section, it turns red ... The start signal then turns red ... Provided the train stops at this signal, the reserved overlap, the route and required elements are cleared and set to available.
>
> Safety-critical Events ... the state of the signaling elements is reset to a 0 value which indicates that they are occupied. This ensures the elements or route are not used for another route request. This procedure forces the signals to display a red aspect ...

#### 摘录 C

- 出处：第 128-131 页，`Appendix E / Route 3 test cases`，`paper_content.txt` 第 3798-3911 行
> Table E.17: Route 3 – Set route test case ... s3 = Yellow ... s5 = Yellow ... Tb = Yellow ... Tc = Yellow ... Ty = Yellow ... w1 = Yellow ... Route 3 is set.
>
> Table E.18: Route 3 – Call Route test case parameters ... s3 = Green ... s5 = Green ... Tb = Green ... Tc = Green ... Ty = Green ... w1 = Green ... Route 3 is called.
>
> Table E.19: Route 3 – Train Occupation test case parameters ... s3 = Grey ... s5 = Grey ... Tb = Grey ... Tc = Grey ... Ty = Grey ... w1 = Grey ... Route 3 is cleared.
>
> For Route 3, a fault has been initiated for element Tc ... Fault triggered for element Tc ... Route request is not issued. Route 3 cannot be set.
>
> ... “Unrequested switching of point’s machine” critical event ... All elements turn red. Route 3 is cancelled.
>
> ... “Faulty sensors” safety-critical event ... All elements in layout turn red. Route 3 is cancelled.

### 2. 基于原文整理后的自然语言描述

The generic electronic interlocking models route control with statecharts that first perform a route request, checking for conflicting routes and then verifying the availability of the required signals, track sections, and points before a path can be reserved. When Route 3 is set, the required elements `s3`, `s5`, `Tb`, `Tc`, `Ty`, and `w1` are driven into the reserved yellow state, after which the route call stage clears them to green so the route is ready for train occupation. During occupation, the train advances through the route while the used sections and signals are driven into the occupied state, and once the train reaches the destination side the overlap, route, and related elements are cleared again. The same controller also includes explicit fail-safe behavior: a fault on `Tc` prevents the route request from being issued at all, while safety-critical events such as unrequested point switching or faulty sensors force all Route 3 elements back to red and cancel the route.

### 3. 逐句溯源

1. 句子 1：The generic electronic interlocking models route control with statecharts that first perform a route request, checking for conflicting routes and then verifying the availability of the required signals, track sections, and points before a path can be reserved.
   对应摘录：A, B
2. 句子 2：When Route 3 is set, the required elements `s3`, `s5`, `Tb`, `Tc`, `Ty`, and `w1` are driven into the reserved yellow state, after which the route call stage clears them to green so the route is ready for train occupation.
   对应摘录：B, C
3. 句子 3：During occupation, the train advances through the route while the used sections and signals are driven into the occupied state, and once the train reaches the destination side the overlap, route, and related elements are cleared again.
   对应摘录：B, C
4. 句子 4：The same controller also includes explicit fail-safe behavior: a fault on `Tc` prevents the route request from being issued at all, while safety-critical events such as unrequested point switching or faulty sensors force all Route 3 elements back to red and cancel the route.
   对应摘录：A, C
