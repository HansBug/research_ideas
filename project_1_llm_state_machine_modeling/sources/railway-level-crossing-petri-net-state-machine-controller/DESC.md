# 四状态铁路道口定时控制 / Synthesis of Controller for Railway–Level Crossing Devices Using Petri Nets and State Machine

## 论文在讲什么

这篇论文讨论的是自动铁路平交道口控制器的综合过程。作者先从 warning / closing / opening 的实际作业规则出发，再把这些规则分别映射到 marked Petri net、simple time Petri net 和最后可执行的 state machine 上，因此它不是单纯讲 Petri net 方法，而是以真实道口控制对象为主线。

对 `sources/` 来说，它的价值在于把道口门控控制链写得很完整：列车进入 approach section 后何时亮红灯和鸣笛，多久后开始降栏，什么条件下算关闭完成，列车离开 danger zone 后多久开始抬栏，以及第二轨来车时为什么不能直接结束 warning。这样的正文非常适合抽成 timed FSM 样本。

## 控制系统在文中的位置

这里的控制系统描述是论文中心，而 Petri net 与 state machine 是作者用于落实现实控制逻辑的表示工具。也就是说，我们保留的重点不是“Petri net 可用于建模”这句方法论，而是那套具体的 crossing-device controller：消息 `close/open`、状态 `close/open`、预警时间 `t0`，以及 `waiting / closing / maintenance / opening` 四态流转。

它和一些只停留在传感器+电机框图的道口论文不同。本文把 warning 链、关闭链、打开链和继续关闭的异常条件都串了起来，因此不是很薄的“到车关门，走车开门”摘要，而是一条可以回溯到工程定时和状态图的完整控制链。

## 对我们为什么有用

这篇论文补的是 `🚆` 方向里比较典型的 `FSM + T1` 样本。铁路方向很多高质量论文会漂向 interlocking table、route locking 或资源互斥逻辑，而这篇保留下来的是更贴近路侧设备执行链的 crossing supervisor。它能让文库里“铁路联锁”之外再多一种道口门控画像。

它也给检索策略一个很好的提醒：如果题名同时出现 `railway level crossing`、`state machine`、`Petri net` 甚至 `simple time net`，而正文里又能看到 `8 s`、`6 s`、`30-90 s` 这类明确工程时序，那么这类论文往往不只是方法稿，而是真能落到状态机主链上的控制样本。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `6-7` 页 `3.1 Warning users of roads`，先把 warning、关闭、打开三段控制链和 `8 s / 6 s / 30-90 s` 的时序抓出来。随后看第 `8-10` 页，确认 simple time Petri net 里哪些 place / transition 对应 `message close/open` 和 `status close/open`，以及 state machine 最终压缩成哪四个状态。

如果只是为了重做 `STM.md`，前面大量关于 Petri net 基础定义的理论说明可以第二轮再看。第一轮真正关键的是作业规则、时间约束和最后四态控制图，这三部分已经足够把这篇论文恢复成一条高质量的铁路道口 timed controller 样本。
