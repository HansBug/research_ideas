# SharjahSat-1 八模 mission software / On-Board Software Development for a 3U CubeSat

## 论文在讲什么

这篇论文讲的是 SharjahSat-1 这颗 3U CubeSat 的机载软件开发，但它并不是那种只停留在软件架构层的报告。作者一方面介绍了 OBC、FreeRTOS、调试与可靠性设计，另一方面把卫星实际运行所依赖的 operation modes 和 task 结构讲得相当具体，尤其是 LEOP、Nominal、Safe、payload operation、Transmit 和 Autonomous 之间的衔接关系。

从 `sources/` 的角度看，最值得保留的是它明确把 SharjahSat-1 的 mission software 写成了一个顶层状态机。正文不是只说“有不同模式”，而是直接列出 `8` 个 fundamental operation modes，并为每个模式写出职责、触发条件、退出方式和与其他 task 的切换关系，还给出 `90 minutes`、`15 minutes`、`3 weeks` 这些非常典型的工程定时语义。

## 控制系统在文中的位置

这套控制系统描述在文中属于核心设计内容。虽然论文也谈到了 reusable software architecture、debugging、memory management 和任务划分，但这些内容最终都是围绕“这颗卫星在轨时到底怎么切模式、怎么进入 payload 任务、怎么在低电压和失联下退化运行”来组织的。换句话说，状态机不是附带例子，而是整套 mission software 的主骨架。

对于样本库来说，这一点非常关键。很多 CubeSat 软件论文会把重心放在软件分层、通信协议或硬件平台上，真正的 mode manager 只在图里一带而过；而这篇论文则把 operation modes 与 task-level implementation 都写进正文，使我们能够同时看到模式级控制语义和实现级 handoff 机制。这种“模式 + 任务 + 恢复”三层信息同时存在的文本，在航天方向并不常见。

## 对我们为什么有用

这篇论文补的是一个质量很高的 CubeSat 顶层运行管理样本。相比仓库里已有的一些 `LEOP / safe mode` 或单一 mission supervisor 条目，它更完整地覆盖了启动等待、姿态指向切换、payload 任务调度、低电压安全退化、通信丢失后的 autonomy fallback，以及接收到指令后的恢复路径。也就是说，它不是只给一条主模式链，而是给出了一套真实 flight software 的运行生态。

对 `project_1` 来说，这类样本尤其有价值，因为它把很多建模时需要显式保留的东西都写出来了：状态集合，内部检查项，定时阈值，任务通知与挂起关系，以及 mode restore/fallback 规则。后续如果要训练模型从论文文字恢复状态机，这篇文章能提供比“只有模式名列表”的样本更完整的监督信号。

## 如果需要人工细读，建议怎么读

如果后续要人工细读，建议先从第 3-5 页的 `3.1 Operation Modes` 和 `3.2 Tasks` 开始，而不是从软件需求或硬件背景顺读。第一轮先把 8 个 operation modes、`LEOP -> Nominal -> Payload/Transmit/Safe/Autonomous` 的主链，以及 `90 minutes / 15 minutes / 3 weeks` 三组时间阈值读稳；这一步已经足够支撑重写高质量 `STM.md`。

第二轮再回头看前两页的 requirements、OBC 选型和 debug/reliability 设计，用来理解为什么模式切换要依赖 registry、battery threshold 和 task notification。若只是为了状态机样本，最值得优先保住的仍然是模式职责、Nominal 的三类周期检查、Safe 的恢复条件、payload/transmit 的 handoff 方式，以及 Autonomous 在长时间失联下如何接管并在收到命令后立即退回 `Nominal`。
