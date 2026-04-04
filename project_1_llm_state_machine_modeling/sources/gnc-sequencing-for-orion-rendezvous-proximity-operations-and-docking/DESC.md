# Orion 交会、近距离操作与对接的 GN&C 序列设计 / GN&C Sequencing for Orion Rendezvous, Proximity Operations, and Docking

## 论文在讲什么
这篇论文解决的是Orion 航天器在 Gateway / EUS 附近执行交会、近距离操作与对接时，高层 GN&C sequencing 如何设计与实现的问题。输入是 relative range、`NRI`/`RB3`/`RB5`/`RB6` 等关键任务事件、`ATP` 授权和 docking 状态，方法是以 `PSAM` 形式构建 `Phase -> Segment -> Activity -> Mode` 的层次序列控制，输出是可以嵌入 prototype flight software 的任务序列逻辑。
从论文的展开方式看，输入侧主要落在 range to Gateway、planned `TIG`、`ATP`、hard capture、undock 和 off-nominal 指令，核心做法是 层次 `PSAM` + nominal/off-nominal state machine design，最终形成的则是 Orion `RPODOperations` 阶段的 GN&C sequencing 定义与仿真实现。 因此它不是只在某个局部环节顺手提到状态机，而是在用一套较完整的系统叙事把任务目标、控制分层和运行结果串起来。 对后续维护样本库的人来说，这一节读完后就应该能先建立系统边界、主要参与量以及大致控制思路的整体印象。

## 控制系统在文中的位置
这里的控制系统就是正文反复展开的核心对象之一，论文的主要篇幅都在说明它如何分阶段运行、如何在条件满足时切换，以及如何产生可执行控制行为。 论文对象是 Artemis 任务中 Orion 航天器的 `RPOD` 高层序列控制，而不是轨道动力学求解器本身。它负责在不同接近距离和任务阶段下切换 GN&C software configuration，并决定何时进入 burn configuration、close range、docked、departure 等任务状态。
作者使用 `PSAM` 层次，例如 `Phase`、`Segment`、`Activity`。 论文最有价值的地方在于把关键任务时间点写得很具体，例如 `RangeToTarget < [TBD] km` 或 `NRI - 1 hr` 进入 `RPODOperations`、Far Range burn 前 `20 min` 切到 `RPOD_Burn_Config`、`5 min before TIG` 切到 `RPOD_Burn`。 也就是说，我们在这里看到的不是一句笼统的“有状态机控制”，而是一条能继续追溯到状态、触发条件、局部时间语义或阶段动作的控制链。

## 对我们为什么有用
对 `sources/` 来说，这篇论文补充了 `sources` 中高质量的航天任务序列控制样本。 它非常适合训练“长链任务阶段 + 层次状态 + 工程时序触发”的建模能力。 它不仅有 nominal path，还有明确的 contingency branches。
如果后续要把它继续清洗成数据集或训练样本，第一轮优先回看的通常是 `Phase / Segment / Activity / Mode` 的层次组织模式、把 `NRI-1h`、`20 min before TIG`、`5 min before TIG` 这类工程时间点写成状态转移条件、将 `Hold_Retreat` 与 `Abort` 作为独立 off-nominal segment 的设计方式 这些最容易直接转成状态机自然语言描述的部分。 论文重点是 sequencing 设计，不是完整 GN&C 低层算法细节。 `Activity` 级完整图太大，文中只给了局部示例，抽取时要以 phase/segment 主链为主。 这些内容更适合放到第二轮核对时再展开，而不是在第一次整理时全部摊开。
