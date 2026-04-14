# AnnieWAY 团队 2007 DARPA Urban Challenge 自主系统 / Team AnnieWAY's autonomous system for the 2007 DARPA Urban Challenge

## 论文在讲什么

这篇论文介绍的是 AnnieWAY 参加 `2007 DARPA Urban Challenge` 的整套自主驾驶系统。它覆盖车辆硬件、感知、地图、任务规划、轨迹生成和控制，但对我们最重要的是行为规划层，因为作者把城市道路中的正常行驶、路口通行、停车区导航、重规划和恢复策略统一组织成了一套并发层次状态机。

这不是一篇只讲局部算法的自动驾驶文章，而是一篇完整系统论文。它既要处理普通车道跟随，也要处理路口优先权、拥堵、死锁恢复和停车区机动，因此行为决策部分天然带有大量离散模式切换，非常适合作为 `HSM` 样本。

## 控制系统在文中的位置

我们关心的控制系统在文中属于核心架构层。第 8 节明确说 maneuver planner 是一个 `Concurrent Hierarchical State Machine`，图 10 把主状态和重要子状态直接列了出来；第 9 节再拿路口场景详细解释 `IntersectionApproach / Queue / Stop / Wait / DriveInside / PrioStop` 是如何切换的。

这意味着论文不是在泛泛介绍“自动驾驶一般需要状态机”，而是在直接描述参赛车辆的行为决策器。对于 `sources/` 来说，这类系统级论文最大的价值就是它能把高层 mission/behavior control 的状态骨架、守卫条件和恢复路径都固定下来。

## 对我们为什么有用

对 `🚗` 方向来说，这篇文章补的是一个非常强的城市道路行为决策样本。它与只讲单个场景的换道或超车控制不同，提供的是更完整的 urban driving HSM：既有 `Drive`、`Intersection`、`Zone` 这样的上层任务态，也有 `Queue / Wait / Recover / Replan` 这样的细粒度异常与恢复分支。

更重要的是，文中不是只列状态名，还把一个关键场景真正展开到了“何时排队、何时停车、何时等待、何时在 MTC 验证后进入路口”的粒度。这使它非常适合后续做高层驾驶行为状态机的自然语言样本，而不只是背景材料。

## 如果需要人工细读，建议怎么读

人工细读时，建议先看第 15-16 页的 Figure 10 和其说明，把主状态族 `Drive / Intersection / Zone / Replan / GlobalRecover / Pause` 以及各自子状态先框出来。随后直接跳到第 20-21 页看 Figure 14 对应的路口子状态机，这是全文最适合直接抽 `STM` 的部分。

如果第二轮还需要更细地理解 guard 的来源，再回到第 17-19 页阅读 `Moving Traffic Check` 和空间/时间验证部分。感知、建图、定位与低层轨迹控制章节可以放在后面，因为对首轮状态机抽取来说，优先级明显低于 CHSM 骨架、路口子状态和恢复/重规划逻辑。
