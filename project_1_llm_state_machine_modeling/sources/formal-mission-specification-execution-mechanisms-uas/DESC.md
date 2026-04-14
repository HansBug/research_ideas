# 无人机系统的形式化任务规格与执行机制 / Formal Mission Specification and Execution Mechanisms for Unmanned Aircraft Systems

## 论文在讲什么

这是一篇偏完整体系的博士论文，讨论的是如何为无人机系统建立形式化的任务规格、飞行计划执行机制和任务管理机制。文章并不把重点放在底层姿态/轨迹连续控制，而是把 `flight plan manager`、`mission manager`、flight leg 选择条件、任务事件和执行接口组织成一个可运行的任务执行体系。

对 `sources/` 最有价值的部分，在于作者不仅说明“可以用状态图描述任务”，而且把热点侦察任务写成了可执行的 `statechart + SCXML` 控制逻辑。这里既有 `scanArea / scanPoint / hold` 这样的任务模式，也有 `hotspot` 触发后的更新 flight plan、跳过当前扫描、保存恢复位置等具体行为。

## 控制系统在文中的位置

我们关心的控制系统描述在文中属于核心方法载体。论文当然也讲了任务语言、飞行计划、执行引擎和软件集成，但真正把这些内容落到工程控制链上的，是 `Mission state` 的层次化细化以及 `Flight Plan Manager` 与 `Mission Manager` 的事件交互。

这意味着它不是“飞控背景论文里顺手给一张状态图”。相反，任务控制状态本身就是论文要解决的问题之一。对当前文库来说，它补的是航空航天方向里比较需要的高层任务监督样本，尤其适合补 `HSM + T0`、并且带扫描中断与恢复语义的 UAV 任务控制链。

## 对我们为什么有用

这篇论文的第一个价值，是它把无人机任务执行写到了比一般 conference short paper 更细的层级。很多 UAV 论文只给 mission manager 的 mode 名称或框架图，而本文明确写出了并行子状态、下一 leg 的默认选择、热点事件如何改写选择条件，以及扫描如何在中断后恢复。

第二个价值，是它能帮助平衡当前领域分布。文库里已经有若干 UAV/航天 mission supervisor 条目，但不少更偏模式总览或规划-执行分层。本文的 `scan-interrupt-resume` 任务链更接近“为了完成具体任务目标而动态改写 flight plan”的控制器，适合补更强的任务事件闭环样本。

## 如果需要人工细读，建议怎么读

如果后续需要人工重做 `STM.md`，建议先读第 8 章里第 94-100 页附近关于 `Mission` 状态细化的部分，先把 `scanArea / scanPoint / hold` 和 `HotSpotsCounter` 的结构画出来，再确认 `hotspot` 事件触发后到底改写了哪些条件和目标坐标。接着再回到第 74-80 页附近看 `FPM` 的接口与执行循环，用来补齐 `Mission Manager` 是如何通过 `update / skip / current leg` 这些事件驱动执行层的。

相对而言，前面的 UAS 背景、自治程度综述和很多任务语言细节可以放到第二轮再看。第一轮真正要抓住的，是 `Mission` 状态的层次/并行结构，以及 `scan` 被打断后如何跳到 `scanPoint` 再恢复 `scanArea` 这条主控制链；只要抓住这部分，人工复核时就不会被整篇 thesis 的体系性内容冲散。
