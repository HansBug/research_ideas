# 地铁 OCC 与供电协同控制 / Real Time Control System for Metro Railways Using PLC & SCADA

## 论文在讲什么

这篇论文讨论的是一个基于 `PLC + SCADA` 的地铁实时监控与列车控制系统原型。作者不是单点讲某个器件，而是把 `OCC`、站台运行、车站牵引、电力控制和 CCTV 一起组织成一个自动 metro operator，并强调通过 PLC ladder logic 和 SCADA 监控界面来减少故障、提高列车运行安全和供电可靠性。

文中最重要的不是“用了 SCADA”这件事，而是它把多个子控制链都写得比较具体。站台部分有红灯、开门、关门、受电、发车等带时间标签的阶段；牵引供电子系统有 `T1/T2/T3` 变压器及 `Aux-T1/Aux-T2/Aux-T3` 备援切换；故障状态还会触发 OCC 上的报警和应急灯。因此这篇论文本质上是在写一个带层次分工的地铁运行监督控制器。

## 控制系统在文中的位置

控制系统就是全文主角。第 `2` 节开始就在说明 PLC 如何接收传感器、站点和 emergency 输入，再输出 `signal/alarm`、`train running/halting`、`door open/close` 等控制信号；第 `3` 节和第 `4` 节则分别给出 metro platform、metro stations、electrical control 的 flowchart、时序描述和 SCADA 运行界面。也就是说，文中的控制逻辑不是背景案例，而是论文成果本身。

对我们关心的 `STM` 样本来说，这篇论文值得保留的地方是它同时覆盖了**站台时序控制**和**供电故障切换**两条链，并且通过 `OCC main application + sub-application` 的写法自然形成了分层监督结构。这使它比很多只写四相交通灯或单电梯门控的 PLC 论文更接近真实系统级 supervisor。

## 对我们为什么有用

这篇论文对 `🚆` 方向的价值主要有两点。第一，它把铁路/地铁控制从传统联锁或道口门控扩展到了 `OCC` 监督 + 站台发车 + 供电切换的综合系统，这能补足当前轨交领域里更少见的 `HSM + T1` 监督样本。第二，它保留了 `t = 0`、`20 > t >= 15`、`50 <= t1 < 100`、`50 <= t2 < 100` 这类工程级定时条件，后续做时间相关样本时比较好用。

此外，原文的提取质量也比较稳。关键状态信息没有只埋在图里，表格和正文就直接写出了主控层级、站台动作、故障站告警和辅助变压器接管逻辑，所以即便后面要人工重做 `STM.md`，也不需要从纯截图或极薄 caption 里重新猜状态链。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `4-7` 页。先抓 `OCC` 是 main application、其他是 sub-application 这一层次结构，再连续读 `Metro platform view description` 和 `Electrical control view description`，这样最容易把“站台发车”与“供电故障切换”两条核心控制链串起来。

第二轮再看 `Metro stations (traction SCADA)` 和结果展示页，补齐 train-location tracking、fault station alert、emergency light 等告警逻辑。至于前两页关于自动化背景、CBTC 缺陷或 SCADA 一般介绍的段落，可以后放，因为它们更像动机说明，不是直接决定状态机骨架的主证据。
