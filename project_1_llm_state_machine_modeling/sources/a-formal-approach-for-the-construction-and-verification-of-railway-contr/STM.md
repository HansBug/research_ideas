# A formal approach for the construction and verification of railway control systems - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：Resource-flow（资源流/并发网模型）
- 代表时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签概况：显式时钟、资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：route reservation、point allocation、GO/STOP 信号切换和 route release 链路清楚，且保住了冲突互斥前提。

## 条目 1: Route reservation and release in a route-based tramway controller
- 控制对象：有轨电车/铁路 route-based 联锁控制器
- 状态机类型：Resource-flow（资源流/并发网模型）
- 时间级别：T2（强实时 / 显式时钟时间窗口）
- 结构标签：资源互斥、显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G1 铁路联锁进路生命周期）

### 0. 条目识别与判定

- 一句话说明：这是轨道交通联锁控制领域的 route-based tramway controller，用于在列车进入网络前保留进路、配置道岔、开放信号并在列车离开后释放进路。
- 判断：算。对象是实际铁路/有轨电车控制系统的联锁控制器，原文清楚给出了进路请求、冲突检查、道岔设置、信号开放和进路释放等离散控制步骤。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，Section 3.1，对 route-based control systems 的基本要求说明，行 226-230
> The basic requirements for avoiding tram collisions are that trams must onl y drive on predeﬁned routes
> previously reserved and that two conﬂicting (overlapping) routes must not be reserved a t the same time. As
> a consequence, controllers built to enforce these requirements depend on the railway networ k to be controlled
> and on a selection of predeﬁned routes through that network.

#### 摘录 B
- 出处：第 8 页，Section 3.2.2，SystemC Model for Controller，行 295-302
> The basic behavioural patterns of a control system generated for a network and col lection of routes are as
> follows. When a tram approaches the network, a route is requested to be reserved. T he control system makes
> a reservation for that route if no conﬂicting route has already been reserved. Then it a llocates the route by
> requesting points to be switched into positions that allow traversal o f the chosen route (as described by the
> point position table), and when the points have been switched it requests the en try signal to show a GO
> aspect ... As soon as the tram has passed the entry signal, the signal is requested to show STOP, and when t he
> tram has left the route, the route is deallocated by removing its reservation.

### 2. 基于原文整理后的自然语言描述

Before a tram is allowed to drive on a predefined route, that route must already have been reserved and no conflicting route may be reserved at the same time. When a route request arrives, the controller reserves the chosen route only if no overlapping route is already reserved. It then allocates the route by requesting all required points into the positions given by the point-position table, and once the points have switched it requests the entry signal to show a `GO` aspect so the tram may enter. As soon as the tram passes the entry signal, the signal is requested to show `STOP`, and when the tram has completely left the route the reservation is removed and the route is deallocated.

### 3. 逐句溯源

1. 句子 1：Before a tram is allowed to drive on a predefined route, that route must already have been reserved and no conflicting route may be reserved at the same time.
   对应摘录：A
2. 句子 2：When a route request arrives, the controller reserves the chosen route only if no overlapping route is already reserved.
   对应摘录：B, A
3. 句子 3：It then allocates the route by requesting all required points into the positions given by the point-position table, and once the points have switched it requests the entry signal to show a `GO` aspect so the tram may enter.
   对应摘录：B
4. 句子 4：As soon as the tram passes the entry signal, the signal is requested to show `STOP`, and when the tram has completely left the route the reservation is removed and the route is deallocated.
   对应摘录：B
