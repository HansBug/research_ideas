# A formal approach for the construction and verification of railway control systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：路由保留、道岔定位、进路开放与释放链路描述清楚，可直接整理为控制逻辑样本。

## 条目 1: Route reservation and release in a route-based tramway controller
- 控制对象：有轨电车/铁路 route-based 联锁控制器

### 0. 条目识别与判定

- 一句话说明：这是轨道交通联锁控制领域的 route-based tramway controller，用于在列车进入网络前保留进路、配置道岔、开放信号并在列车离开后释放进路。
- 判断：算。对象是实际铁路/有轨电车控制系统的联锁控制器，原文清楚给出了进路请求、冲突检查、道岔设置、信号开放和进路释放等离散控制步骤。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，Section 3.1，对 route-based control systems 的基本要求说明，行 226-230
> The basic requirements for avoiding tram collisions are that trams must onl y drive on predeﬁned routes
> previously reserved and that two conﬂicting (overlapping) routes must not be reserved a t the same time. As
> a consequence, controllers built to enforce these requirements depend on the railway networ k to be controlled
> and on a selection of predeﬁned routes through that network. This implies that the associ ated domain-speciﬁc
> description should include network speciﬁcations and interlocking tables describing the r outes.

#### 摘录 B
- 出处：第 8 页，Section 3.2.2，SystemC Model for Controller，行 295-302
> The basic behavioural patterns of a control system generated for a network and col lection of routes are as
> follows. When a tram approaches the network, a route is requested to be reserved. T he control system makes
> a reservation for that route if no conﬂicting route has already been reserved. Then it a llocates the route by
> requesting points to be switched into positions that allow traversal o f the chosen route (as described by the
> point position table), and when the points have been switched it requests the en try signal to show a GO
> aspect (as described by the signal setting table) indicating that the tram may enter the route. As soon as
> the tram has passed the entry signal, the signal is requested to show STOP, and when t he tram has left the
> route, the route is deallocated by removing its reservation.

### 2. 基于原文整理后的自然语言描述

Before a tram is allowed to drive on a predefined route, that route must already have been reserved and no conflicting route may be reserved at the same time. When a route is requested, the control system reserves it if no conflicting route has already been reserved, requests the points for that route to the required positions, and then requests the entry signal to show a GO aspect. After the tram has passed the entry signal, the signal is requested to show STOP, and the route is deallocated when the tram has left the route.

### 3. 逐句溯源

1. 句子 1：Before a tram is allowed to drive on a predefined route, that route must already have been reserved and no conflicting route may be reserved at the same time.
   对应摘录：A
2. 句子 2：When a route is requested, the control system reserves it if no conflicting route has already been reserved, requests the points for that route to the required positions, and then requests the entry signal to show a GO aspect.
   对应摘录：B
3. 句子 3：After the tram has passed the entry signal, the signal is requested to show STOP, and the route is deallocated when the tram has left the route.
   对应摘录：B
