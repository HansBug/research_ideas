# 容错列车车门控制 / Fault Tolerant Train Door Control

## 论文在讲什么

这篇论文是一篇围绕电动列车门控制器设计与实现展开的硕士论文。作者不是在写抽象的铁路安全框架，而是针对一个 London Underground train door rig，完整做了一套低成本嵌入式 fault-tolerant door controller：包括 H-Bridge、微控制器、编码器、红外到位传感器、电流/电压采样，以及配套的软件控制与故障检测算法。

从控制内容上看，论文最有价值的部分不是硬件搭建本身，而是它把“上电归零到 fully open、按钮触发开门/关门、PWM 曲线控制门速、到位/过流判定、障碍回退、重复关门、最终停用”这一条工程控制链写得很细。门的开门/关门时间目标、过流阈值、回退距离和 retry 次数都直接给出来了，因此它不是泛泛的设备介绍，而是能直接支撑状态机抽取的铁路门控控制样本。

## 控制系统在文中的位置

这里的控制系统描述是全文主角。第 3 章先把 controller requirements、硬件连接和 normal door-control algorithm 写清楚，第 4 章再专门进入 fault tolerance implementation，逐项解释哪些 fault 会被监测、哪些情况下只报警、哪些情况下要回退重试、哪些情况下要把门直接置为 out of service。

也就是说，我们关心的状态机语义不是藏在附录、验证案例或小实验里，而是直接承载了论文核心论点。作者关心的就是“这套门控制器如何正常工作、如何感知异常、如何在异常下继续安全运行或安全停用”，这正好对应 `sources/` 里最需要的系统级控制链。

## 对我们为什么有用

这篇论文对文库的价值很高，因为它把铁路方向里相对少见的“门控 + 故障退化 + 局部时间约束”三件事放在同一条控制链上。相比只写联锁表或道口栏杆开闭的样本，它更偏设备级控制器，但又比单纯诊断论文更完整，既保留了 nominal open/close cycle，也保留了 warning、obstruction reopen、three retries 和 out-of-service 这类异常恢复与降级分支。

从建模角度看，它也很适合做 `EFSM + T1` 样本。状态切换不只由按钮和到位传感器决定，还依赖电流阈值、编码器位置、时间目标和重试计数；同时，动作输出也不是一句“open/close door”，而是带 PWM duty、回退距离和停用处理的工程化执行链。这类样本对后续做“从自然语言生成带 guard 与异常链的状态机”很有帮助。

## 如果需要人工细读，建议怎么读

如果后续需要人工重读，建议先从 `paper_content.txt` 中对应第 40-54 页的内容开始。先看 requirements 与 `Controller functionality`，确认正常主链里有哪些输入、输出和时间指标，再继续看 `Development stages` 与 `Fault tolerance implementation`，把 `fully open` 初始条件、按钮触发、PWM 开关门、到位停止、两级过流阈值、回退 `100 mm`、`3` 次重试和 out-of-service 这几件核心事实圈出来。

第二轮再去看更后面的测试与分析章节，主要目的是核对这些 fault branches 在实验里如何被验证，以及是否还有对速度、摩擦、供电变化的补充说明。至于前面的 fault-tolerance 背景综述、通用 door-system 分类和更偏维护统计的内容，可以放到最后再看；它们有助于理解动机，但不是重建状态机主链的首要证据。
