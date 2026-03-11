# Some Experiences on Formal Specification of Railway Interlocking Systems using Statecharts - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文把联锁系统的进路处理顺序写得很清楚，包括空闲检查、锁闭、道岔定位、信号开放和确认返回。

## 条目 1: Route Request Check-Lock-Green Sequence
- 控制对象：轨道交通领域的铁路联锁系统

### 0. 条目识别与判定
- 一句话说明：这是铁路联锁控制系统，用于处理进路请求、检查轨道区段状态、锁闭进路及相关道岔，并在安全条件满足后开放信号。
- 判断：算。对象是实际联锁系统，原文明确给出了进路请求后的检查与动作序列。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section 2, 行 94-106
> Typically, a RIS receives a route request; the answer to this request has to go through a series of checks and actions of the kind: a route can not be locked if a track section element is occupied; a route is available if no part of the route is already locked; if the route is available it will be locked; locking a route implies that all its track elements become locked; when a route is locked signals for the route can be switched to green, and then the original route request is positively acknowledged.

#### 摘录 B
- 出处：第 2-3 页，discussion of signalling rules, 行 145-153
> The rules usually enforce a predefined sequence of actions: issuing a route request command usually first triggers a check that all the track elements involved in the route are free; in the case, commands are issued for the positioning of switches for that route and for locking the track elements. This phase may be followed by a global centralized control over the correct state of the commanded elements, after which the route is locked and signal indications for the route are set.

### 2. 基于原文整理后的自然语言描述

When a route request is received, the interlocking first checks that no track section in the route is occupied and that no part of the route is already locked. If the route is available, the system commands the required switch positions, locks the route and its track elements, verifies the commanded state, and then sets the route signal to green while positively acknowledging the original request.

### 3. 逐句溯源

1. 句子 1：When a route request is received, the interlocking first checks that no track section in the route is occupied and that no part of the route is already locked.
   对应摘录：A, B
2. 句子 2：If the route is available, the system commands the required switch positions, locks the route and its track elements, verifies the commanded state, and then sets the route signal to green while positively acknowledging the original request.
   对应摘录：A, B
