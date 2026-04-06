# 航空航天与飞行/空管控制 / Increasing the Autonomy of the Unmanned Aerial Platform

## 论文在讲什么

这篇论文讨论的是一套支持无人机在失联和危险场景下继续自主执行任务的控制架构。作者把平台分成 `FCC`（Flight Control Computer）和 `MC`（Mission Computer）两层，前者负责飞行与稳定控制，后者负责任务调度、传感器管理和更高层的危险情景处理，然后用 SysML 状态机把航路点飞行、识别任务、碰撞规避和失高救援串起来。

它最有价值的地方在于，论文没有只停留在“架构上分两个计算机”这一层，而是把一条完整的任务流和两条异常流都写成了状态机。`FWM1 / FWM2 / FWM3 / SUP / FWM4 / FWM5` 这些状态名，加上三正交状态、风况触发参数修正、碰撞处理和 parachute rescue，让这篇文章的离散控制链很容易被直接抽成状态机自然语言样本。

## 控制系统在文中的位置

这里的控制系统描述不是边缘案例，而是作者论证“平台 autonomy 如何落地”的中心对象。论文确实带有架构和建模方法色彩，但这些方法并不是脱离对象悬空存在的，最终都要落到一个可运行的 mission supervisor 上，因此状态机图本身就是文章最重要的成果之一。

对 `sources/` 而言，这类样本的特别之处在于它同时覆盖了 nominal mission chain 和 hazard hierarchy。很多 UAV 论文只把正常任务流程讲清楚，异常处理只点到为止；这篇论文则把 collision avoidance、terrain obstacle、loss of altitude 这些分支放进同一个 supervisor 里，并明确了优先级关系，这让它比单纯的 waypoint follower 更适合做状态机建模数据。

## 对我们为什么有用

这篇论文补的是一类比较理想的 `HSM + T0 + 层次/并行` 航空任务监督样本。它不像一些航空论文那样主轴是连续控制律，也不像纯 mission planner 论文那样只有高层任务列表，而是保住了 state name、parallel branch、entry/do/exit procedure 和异常优先级这些很适合转成自然语言控制描述的关键件。

另外，它还提供了一个很好的“架构到控制链”桥梁样本。后续如果要让模型从较长的工程叙述里恢复状态机，像 `FCC/MC` 这种职责分离、`WAYPOINT mode` 这种场景入口、以及 `SUP` 如何在多类危险之间做裁决，都很适合拿来训练模型学习如何把系统文字说明压缩成有边界的状态监督结构。

## 如果需要人工细读，建议怎么读

如果后续要人工细读，建议先看第 3-5 页：先用 `Use Case` 图确认 `WAYPOINT mode`、`SAR recognition`、`collision avoidance` 和 `loss of altitude` 这些场景在文中的边界，再直接看 Figure 3 附近的状态机说明，把三正交状态、`FWM1 -> FWM2 -> FWM3 -> ...` 主链，以及 `SUP -> FWM4 / FWM5` 两条异常链重新圈出来。

前面关于 PID、Dryden turbulence model 和更一般的无人机架构背景，可以放到第二轮再看。第一次人工复核时，真正重要的是抓住“基本任务链是什么、哪些 entry/do/exit 过程会改 FCC 参数、危险场景怎么被 `SUPERVISOR` 仲裁、失高失败后怎么终止任务”这四个问题；抓住这四点后，就足够支撑重新生成高质量 `STM.md`。
