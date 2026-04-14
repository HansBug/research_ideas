# 自动喷灌过程的状态机监督控制 / Modeling of Automatic Sprinkler Irrigation Process Using Finite State Machine (FSM) and Proportional Integral Derivative (PID) Controller

## 论文在讲什么

这篇论文表面上同时讲了 PID 和喷灌系统建模，但对 `sources/` 来说最重要的是其中的 FSM supervisory controller。作者没有只做“湿度低就浇水”的口头描述，而是明确用 Stateflow 组织土壤湿度、泵启动、喷头开闭、wilting、saturation、plant uptake 等状态，并给出 transition/action 表。

因此，这篇论文的价值不在连续控制参数本身，而在于它把灌溉系统的高层离散行为链讲清楚了：什么情况下开始浇水、为什么要先延时确认、达到高阈值后怎么停泵、以及作物水分状态如何跟执行器动作共同变化。

## 控制系统在文中的位置

FSM 在文中是明确的 supervisory layer。摘要就直接说明 automatic control logic 是用 FSM 设计的；第 2.2 节继续说明主输入是 soil moisture，主输出是 pump voltage，第 3-4 页则把 Stateflow chart 和 transition table 摆出来。也就是说，状态机不是辅助说明，而是作者表达灌溉控制逻辑的主入口。

这点使它和很多普通 irrigation 论文不同。很多文章只给阈值、框图或“若干传感器 + 阀门”的框架，而这篇把 state 名、guard 和 action 都落实到了表格。

## 对我们为什么有用

这篇论文对 `🌡️` 方向很有价值，因为它补了一条农业环境控制里的 `EFSM + T1` 样本。库里灌溉方向已有一些 PLC 条目，但像这样同时给出 `after(2,sec)`、`after(0.05,sec)` 这类显式时间 guard，又把 agronomic state 和 actuator state 连起来的条目并不多。

它也很适合后续做“从转移表恢复状态机”的任务。因为 Table 1 已经把 transition condition 和 transition action 明确列出来，后续无论是做自动抽取、结构化标注还是验证性质生成，都会比只靠摘要信息的样本更稳。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看摘要和第 2.2 节，确认这篇论文里 FSM 才是 supervisory controller。然后直接看 Figure 3 和 Table 1，把 `SoilMoisture -> PumpStart`、`SprinklerOff -> SprinklerOn`、`SprinklerOn -> SprinklerOff`、`Soil -> PumpStop`、`Wilting <-> Saturation` 这些主链串起来。最后再回到前面的 PID 部分补连续控制背景即可。
