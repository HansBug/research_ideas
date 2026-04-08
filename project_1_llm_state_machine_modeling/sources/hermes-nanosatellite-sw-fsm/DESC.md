# HERMES 纳卫星三模软件监督器 / A finite state machine approach to nano-satellite SW design: the HERMES case study

## 论文在讲什么

这篇论文讨论的是纳卫星板载软件如何用有限状态机方法组织起来，并以 HERMES CubeSat 任务作为完整案例。作者并不是只做抽象“软件工程建议”，而是明确提出一个由 `LEOP`、`NOM`、`HSAFE` 组成的三模软件骨架，再把它应用到 HERMES 的双 OBC 架构中。对我们最重要的是，这套骨架不是停留在术语层，而是继续展开到启动顺序、时间槽、schedule upload、故障监测和 safe fallback。

从控制逻辑看，论文把小卫星软件中最常见的几类高层行为都压进了模式切换里：一次性的早期在轨启动、地面调度驱动的正常工作，以及非正常情形下的高生存性模式。与此同时，它还给出了 `SW-MAIN` 和 `SW-ADCS` 两个并行运行的软件 FSM 之间的主从关系，因此这个样本并不是一张简单的“mode diagram”，而是一个真正可追溯的软件监督控制器。

## 控制系统在文中的位置

这套控制系统是论文的主方法载体，也是 HERMES case study 的中心骨架。论文前半部分当然会讲 nano-satellite software design 的一般性方法，但一旦进入 HERMES case study，控制系统就不是陪衬，而是承接整篇设计与验证过程的核心对象。作者通过这套 FSM 来说明如何组织 LEOP、如何处理计划上传、如何并行放置监测器，以及如何在 failure 发生时退回 HSAFE。

它在文中的角色也很适合 `sources/`。很多航天论文虽然也谈 mode management，但常常只给 mission phases 的大致描述，缺少具体进入条件、退出条件和任务链。而这篇论文在 HERMES 部分把 `first schedule upload`、`time slot 1 / 2`、`detumbling`、`solar arrays deployment`、`SSAFE monitor` 这些关键控制节点写出来了，因此它更像一个真正的软件监督器实例，而不是松散的任务概览。

## 对我们为什么有用

这篇论文对 `sources/` 的价值，首先在于它补进了一类很有代表性的航天高层控制样本。文库里虽然已经有若干 UAV mission manager、landing gear 或 safe mode 相关案例，但 HERMES 这个样本提供的是 `CubeSat flight software + dual OBC + time-tagged LEOP + schedule-driven NOM + safe fallback` 的组合，这和传统飞行器或地面机器人监督器并不相同。

其次，它对后续“生成-验证-修复”链条也很有帮助。因为这篇论文本身就强调 formal verification，并且把软件骨架、模式切换条件和监测/恢复机制写得较明确，所以后续如果要从自然语言中抽模式管理状态机、再往验证性质或恢复策略上延伸，这篇样本是非常合适的中继材料。

## 如果需要人工细读，建议怎么读

如果后续需要人工重读，建议先看第 1-2 页摘要和引言，只确认论文不是泛泛 survey，而是明确提出 FSM-based software design 并把 HERMES 当成 case study。然后跳到第 4-6 页的通用方法部分，快速读一遍作者如何定义 `LEOP / NOM / HSAFE` 这三个高层模式。接着重点看第 7-10 页的 HERMES case study，尤其是 `4.2 HERMES software high-level design` 和 `4.3.1 HERMES SW-MAIN finite state machine`，把双 OBC 结构、mode transition、time slot 启动顺序和 `SSAFE` 连续监测逻辑逐条对齐。

至于更前面的文献综述和更后面的多学科分析、工具实现细节，可以放到第二轮再看。第一次人工复核时，真正值得优先抓住的是“模式是什么、谁触发进入/退出、哪些动作按时间槽执行、哪些监测器在并行运行、何时退回 HSAFE”；只要这条链读稳，这篇论文就已经足够支撑高质量 STM 抽取。
