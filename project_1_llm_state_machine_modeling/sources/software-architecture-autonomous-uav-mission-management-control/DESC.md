# 自主无人机任务管理与控制软件架构 / A Software Architecture for Autonomous UAV Mission Management and Control

## 论文在讲什么

这篇论文讨论的是一套自主无人机任务管理架构，重点不是底层连续飞控，而是如何把任务目标、飞行计划生成、重规划和动作执行组织成可运行的 agent-based control system。系统主要分成 `Planner agent` 和 `Execution agent` 两层：前者把高层 objective 转成 flight plan，后者把 plan 中的 action 逐个落成对 UAV 的直接命令或 autopilot 命令。

从文章结构看，作者先给出概念层的软件架构，再把重点收束到 `Planner` 与 `Exag` 的行为组织。尤其是 `Planner agent` 的状态和子状态、`Execution agent` 如何按 action number 顺序执行 `park/taxi/take-off/climb/travel/landing` 等动作，都不是一句抽象说明，而是具体到了可当状态机样本看的层级。

## 控制系统在文中的位置

我们关心的控制系统描述在这篇论文里属于核心内容。论文虽然以“software architecture”为题，但真正最有价值的部分不是泛泛分层，而是 `Planner agent` 的主状态与子状态如何展开、重规划何时发生、Flight Plan 何时交给执行层，以及执行层如何把 action 转成 UAV 控制命令。

这意味着它不是单纯“架构论文里顺手放一张状态图”。相反，状态组织本身就是 mission management 的工作核心。对 `sources/` 来说，它属于典型的航空航天 `HSM` 样本：高层任务模式、内层子流程和执行链条都比较清楚，而且与真实飞行任务直接相关。

## 对我们为什么有用

这篇论文对文库有两个直接价值。第一，它补的是当前比较重要的航空航天任务监督方向，而且控制对象明确是 `UAV mission management`，不是连续姿态控制、导航估计或路径优化本体。第二，它给出了比较像工程状态机的“计划生成 -> 计划修改 -> 动作执行”链条，能很好支持后续做高层状态机建模样本。

另一个价值是它能帮助平衡现有领域分布中的样本差异。文库里虽然已经有一些 `UAV` 与 mission supervisor 条目，但很多论文偏应急模式、safe mission manager 或 search-and-rescue。本文把 `Planner` 和 `Execution` 的角色拆得更细，适合补充“任务规划与执行解耦”的分层控制样本。

## 如果需要人工细读，建议怎么读

如果后续需要人工重做 `STM.md`，建议先看第 6-7 页关于 `Planner agent` 的部分，先把 `generate-plan / modify-plan` 及其子状态框架画出来，再确认 `plan-sequencing / actions-definition / plan-optimization` 这些内部阶段各自负责什么。随后再看第 9-10 页的 `Execution Agent Description and Testing`，把 action list 如何被顺序执行、每类 action 对应什么 UAV 命令补齐。

相对而言，仿真场景图和经纬度结果图可以放到第二轮再看。它们更适合用于确认这套监督器在复杂场景下如何触发 replanning，而不是第一轮抽取状态机样本时的主证据。只要先抓住 `Planner` 分层和 `Execution` 顺序执行链，人工复核时就能稳定回到最有用的原文位置。
