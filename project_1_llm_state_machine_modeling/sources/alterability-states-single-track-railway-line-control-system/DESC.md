# Identifying Alterability States of a Single Track Railway Line Control System

## 论文在讲什么

这篇论文研究低流量单线铁路控制系统在移除某个 station track 时如何安全更新控制逻辑。作者把单线铁路、车站、列车、track section 和 timetable 建成 FSP / labeled-transition graph，并用 dynamic software updating 的 alterability criteria 找到哪些状态可以安全切换到新控制系统。

## 控制系统在文中的位置

第 3-4 节是核心。论文先定义两站单线铁路：Station A 有 shunting track 和 deviation track，Station B 有 deviation track，两列车分别从 A 到 B 与从 B 到 A 循环通行。随后第 4 节给出 Station A graph、train graph、track graph 和 timetable graph 的 FSP 片段，并说明组合图有 100 个状态，更新后新图有 56 个状态。

## 对我们为什么有用

它补的是 `🚆` 方向里相对少见的“铁路控制系统动态更新”样本，而不是常规道口栏杆或联锁表条目。样本主体仍然是 FSM/T0：station、train 与 timetable 都由有限状态和带标签的离散迁移组成；同时 `deviation / shunt / leave / enter / switchtoA / switchtoB` 这组事件保留了清楚的铁路控制语义。

## 如果需要人工细读，建议怎么读

先读第 3 节，固定单线铁路基础设施和安全约束；再读第 4.1 节的 FSP 代码，把 station/train/track 三类状态机拆开；最后读第 4.2 节 updatable states，理解旧图与新图之间哪些状态能安全更新。
