# 航天器子系统生命周期监督 / HIROSCO - A High-Level Robotic Spacecraft Controller

## 论文在讲什么

这篇论文介绍的是 `HIROSCO`，也就是一个面向在轨服务任务的高层航天器控制器。作者关心的核心问题不是某个单一执行器怎么调，而是当卫星进入 telepresence 或 autonomous 等不同工作模式时，哪些子系统需要上线、哪些实时链路需要建立、谁来做全局日志、资源管理和错误处理。换句话说，它是一篇把复杂 robotic spacecraft 运行组织起来的高层控制论文。

如果只看标题，很容易把它误当成纯框架或中间件论文；但正文并不止于组件化口号。论文明确要求每个子系统都必须实现统一的有限状态机模板，并把这套模板细化到 `Offline`、`Software-Init`、`Hardware-Init`、`Pre-Operational`、`Safe-Operational`、`Operational`、`Error-Operational` 以及若干 de-init/post 状态。它真正关心的是：一个子系统如何被投运、验证、全功能启用、再在错误时被有序降级。

## 控制系统在文中的位置

在这篇论文里，我们关心的控制系统描述处于主干位置，但它不是传统意义上的某个“被控对象局部回路”，而是高层 supervisory control。`HIROSCO` 的 supervisor 决定不同模式下哪些子系统要工作、哪些互联要建立，以及发生错误时应该日志记录、切回 safe-operational 还是直接关停网络。这套离散控制链实际上就是整篇论文最关键的执行骨架。

因此它虽然带有明显的架构论文气质，却没有脱离 `sources/` 的边界。这里的状态机不是开发流程，不是组件生命周期的抽象装饰，而是真正在约束 manipulator subsystem、joystick subsystem 和实时网络如何上线、验证、运行、退化和恢复。特别是 error severity 的处理规则，把 supervisor 从“结构说明”推进到了“可抽取的控制逻辑”层。

## 对我们为什么有用

这篇论文对文库的价值，在于它补到了一类在其他方向不太容易见到的样本：面向复杂系统集成的 lifecycle supervisor。很多控制论文都能提供 nominal 模式切换，但很少把 `commissioning -> verification -> full operation -> error degradation -> de-initialization` 这条链写得这么完整。它特别适合补强 `⚙️` 方向里“高层监督 + 生命周期管理 + severity-based recovery”这一类样本。

对后续自动建模任务来说，这类样本还有一个好处：状态名语义非常清晰，便于从自然语言稳定恢复成状态机骨架。`Safe-Operational` 和 `Operational` 的差异、`Error-Operational` 的触发条件、`medium/high severity` 分别导向什么恢复动作，都很适合做 prompt 里的显式结构约束，而不是只能做浅层摘要。

## 如果需要人工细读，建议怎么读

如果要人工细读，建议先看正文前半段里关于模式与 supervisor 职责的部分，确认 `telepresence / autonomous mode` 不是简单标签，而是决定子系统上线与实时互联的运行模式。接着直接跳到 `Figure 4` 和对应说明，把十个状态的职责、进入条件和 `Safe-Operational / Operational / Error-Operational` 三者关系先读稳。

再往后读 supervisor 的 event handling 和 practical tests，重点看 severity 分级和实际试验里的反应：高严重度立即关停网络，中严重度切回 `safe-operational`。像前面的 robot framework 综述、组件软件工程背景和一些平台说明，可以放到第二轮再看；如果你的目标是重构状态机样本，优先级远低于状态模板本身和错误处理规则。
