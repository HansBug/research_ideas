# VTOL 无人机的机载任务与监督控制 / Onboard Mission Management for a VTOL UAV Using Sequence and Supervisory Control

## 论文在讲什么

这篇论文讨论的是一套装在 VTOL UAV 上的机载 mission management system。作者要解决的问题不是单一飞控回路，而是高层任务在链路丢失、人工切换、命令执行和 deliberate behavior 之间应该如何组织。为此，论文把 Sequence Control System 和 Supervisory Control System 分开建模，再用 UML state chart 把任务处理流程和高层目标管理表达出来。

它的核心价值在于没有把 mission management 只写成抽象框架。文中直接给出了 `Mission Mode`、`Command Mode`、`Mission Controller Off`、`Stand By`、`Slow Down`、`Parse Command` 等状态，还说明了 `Fly Home` 和 `Search and Track Object` 这类高层行为如何被监督层识别和下发，因此系统边界相当明确。

## 控制系统在文中的位置

我们关心的控制系统描述就是论文主体。第 4 章从 event-based system、UML state chart、层次状态、守卫条件和触发优先级一直讲到 supervisory layer 的 deliberate behaviors，整章都围绕无人机任务控制器本身展开，而不是把它当成附属实验对象。

这类论文对 `sources/` 很有价值，因为它保住的是航空航天方向里比较稀缺的“高层模式管理”样本。很多 UAV 论文会漂向连续飞控、轨迹优化或感知融合，而这篇稳定落在模式切换、命令解析和行为监督这条离散控制链上。

## 对我们为什么有用

这篇论文直接补强了 `✈️` 方向的 HSM 样本，而且不是重复已有的简单 `takeoff / mission / landing` 三段式写法。它同时保住了 top-level 模式切换、行为串行执行、command parser 回跳、人工接管和链路丢失下的监督层干预，因此对于任务级状态机建模很有代表性。

另一个价值是它把“sequence control”和“supervisory control”分成两层。后续做状态机数据集时，这类样本能帮助区分“直接命令执行状态链”和“高层目标选择状态链”两种语义层次，不至于把所有 UAV 样本都压成同一种平面流程图。

## 如果需要人工细读，建议怎么读

建议先读第 6-8 页，把 `Fig. 3` 和 `Fig. 4` 对应的正文段落一起看，先确认顶层状态、`Parse Command` 的作用、`Mission Mode` 与 `Command Mode` 的关系，以及 supervisory layer 如何识别 `Fly Home`。这一段已经足够支撑 `STM.md` 的主要状态链。

第二轮再去看 `Fly Home` 与 `Search and Track` 的行为说明、以及后面的 abstract testing 段落。前者能补强高层行为语义，后者则有助于确认状态、trigger 和 guard 在作者建模中的正式地位。相比之下，前面更泛的 autonomy background 和方法综述优先级可以低一些。
