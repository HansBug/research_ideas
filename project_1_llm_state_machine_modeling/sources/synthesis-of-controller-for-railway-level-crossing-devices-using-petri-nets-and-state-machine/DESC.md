# 铁路道口控制器的 Petri 网与状态机实现 / Synthesis of Controller for Railway-Level Crossing Devices Using Petri Nets and State Machine

## 论文在讲什么

这篇论文讨论的是铁路平交道口控制器怎样从行为规则出发，被综合成一个可实现的数字控制器。作者把自动道口设备视为典型的离散事件实时系统，先用 Petri net 建模其功能，再用 LabVIEW statechart 实现成程序。与很多只停留在“用 Petri 网做形式化分析”的文章不同，这篇论文并没有把道口设备当成抽象案例，而是直接给出了警示、栏杆关闭、栏杆开启以及预警时间这些工程上真正关心的动作链。

论文的关键价值在于它同时保住了两个层面。一方面，作者用 railway crossing 的 verbal description 展开 closing/opening 过程，包括红灯、警笛、栏杆驱动与验证信号。另一方面，他们又把这套行为进一步写成 marked Petri net、simple time Petri net 与四状态 statechart。也就是说，读者不仅能知道系统“做什么”，还能看到它如何被组织成带时间约束的状态机结构。

## 控制系统在文中的位置

这里的控制系统就是论文的中心对象。Petri net 和 statechart 确实是方法工具，但这些工具被引入的原因，是为了表达和实现铁路道口控制器本身。正文第 3 节先给出道路用户警示和栏杆动作规则，第 4-6 节再逐层把这套规则变成 marked net、simple time net 和实际状态机。这种写法说明控制器不是附属案例，而是整个方法链的起点和落点。

对于 `sources/` 而言，这类论文特别有价值，因为它既有工程控制规则，也有足够强的形式化表达。很多铁路方向的文章要么偏联锁表和方法讨论，要么只有设备概念；而这篇文章把 closing、opening、pre-warning、TM12/TM14 和 waiting/closing/maintenance/opening 都写在同一个语境里，因此非常适合做状态机自然语言与形式化结构之间的桥接样本。

## 对我们为什么有用

这篇论文最直接的样本价值，是为 `🚆` 方向补入一个明确的 `HSM + T1` 道口控制器。它不是只有一张状态图，也不是只有时序公式，而是把二者结合起来：8 秒延迟启动栏杆、列车离开危险区后 6 秒内开启栏杆、预警时间公式 `t0 = tn + tzp + t0p`、30-90 秒范围约束，以及四态控制图共同构成了完整的工程时序链。这对我们后续研究“带时间语义的自然语言状态机建模”非常有帮助。

另一个好处是，它天然带有层次和子过程观。closing/opening 本身就是子过程，TM11-TM14 是宏迁移，最终再落到 statechart 的 waiting、closing、maintenance、opening 四态。相比只有平面 FSM 的铁路短文，这类样本更容易支持后续的层次状态机建模、时间约束抽取和验证场景生成。

## 如果需要人工细读，建议怎么读

人工重读时，建议先从第 6-7 页 `Warning users of roads` 读起，把 closing 和 opening 的动作链单独摘出来，尤其要抓住红灯/警笛触发点、8 秒关栏杆、6 秒开栏杆以及预警时间范围。只要这部分读稳，控制器的主行为就已经足够清楚。接下来再读第 8-10 页，确认这些动作如何被放进 simple time Petri net 和四态 statechart 中。

如果后续要重写更细的 `STM.md`，第二轮再看 places、transitions、macrotransitions 和 hierarchy/substates 的描述，确认哪些内容该归为控制子过程，哪些属于实现平台细节。第一遍没有必要把所有 Petri 网理论都读完；对我们最重要的始终是道口控制器本身的警示、关栏、开栏与时间约束链。
