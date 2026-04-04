# 土壤湿度监督喷灌控制 / Modeling of Automatic Sprinkler Irrigation Process Using Finite State Machine (FSM) and Proportional Integral Derivative (PID) Controller

## 论文在讲什么

这篇论文研究的是一个自动喷灌系统，整体上由土壤湿度反馈、离心泵、喷头和 `PID` 流量控制组成，但真正与我们最相关的是作者在其上层又搭了一层 `FSM` 监督控制逻辑。换句话说，它不是只做连续控制器调参，而是把“什么时候启动灌溉、什么时候停止、哪些土壤状态和阈值触发迁移”组织成离散状态机。

原文明确把控制器写成 `Stateflow` 风格的有限状态机，并列出 `soil moisture / saturation / wilting / plant uptake / pump / sprinkler` 等状态及其组合关系。对我们来说，最关键的是它把 `soilLL / soilHH` 阈值、`PumpStart` 与 `PumpStop` 的动作、以及 `after(2,sec)`、`after(0.05,sec)` 两个工程定时都落成了可直接复原的转移表。

## 控制系统在文中的位置

文中真正承载论文技术主线的是“喷灌系统总体模型”，其中 `PID` 负责连续流量调节，而 `FSM` 负责上层监督逻辑。也就是说，这个控制系统既不是背景例子，也不是附录性质的实验对象，而是作者拿来说明整个自动灌溉闭环如何工作的主体系统。

这对样本库维护很有价值，因为它提供了一个少见的“连续控制 + 离散监督”边界案例，但又没有滑到 `Hybrid/T3` 那种必须大量保留连续动力学细节的程度。当前最适合把它定位成“过程控制领域里、以 `EFSM + T1` 方式表达的监督层样本”。

## 对我们为什么有用

在当前 `sources/` 里，过程控制和真正带工程定时的农业/灌溉样本并不多，这篇论文正好补上了这块空白。相比一些只写水位高低启停的简单 PLC 样本，它多了 `Stateflow` 语义、阈值 guard、泵启停动作和两个明确的 `after(...)` 定时，因此更适合做双 A 样本。

后续若把它用于数据集，最该保住的是“土壤湿度输入如何驱动监督层切换”这条主线，而不是所有连续模型公式。第一层重点应是状态、guard、动作、延时确认和高阈值停泵；第二层才是 `PID` 连续调节、土壤物理参数和仿真曲线。

## 如果需要人工细读，建议怎么读

建议先看第 1-2 页摘要和 `2.1 Modeling of the Irrigation System Controller`，只建立系统边界；然后直接跳到第 2-4 页里 `State Machines (FSM)`、`Figure 2`、`Figure 3` 和 `Table 1`，优先读状态集合、输入输出、`soilLL / soilHH` 阈值、`PumpStart / PumpStop` 和两个 `after(...)` 定时迁移。

第 4-7 页里更多关于 `PID` 参数、土壤模型参数、响应曲线和仿真结果的内容可以放到第二轮。除非后续任务是复现整个灌溉闭环，否则第一次人工复核时不必先深挖连续控制细节，先把监督层状态机读稳更重要。
