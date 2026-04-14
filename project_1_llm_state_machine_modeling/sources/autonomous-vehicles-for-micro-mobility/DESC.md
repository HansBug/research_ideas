# 面向微型移动出行的自动驾驶车辆 / Autonomous vehicles for micro-mobility

## 论文在讲什么

这篇论文介绍的是一套面向 campus / sidewalk 场景的微型自动驾驶车辆系统。文章覆盖地图、定位、感知、规划和控制多个部分，但对我们最有价值的是 motion planner 如何在道路规则、障碍物和 stop line 约束下组织离散行为。作者基于 `OpenPlanner` 修改了状态机逻辑，让车辆在 `Forward`、`Follow`、`StopSign` 与 `StopSignWait` 这些状态之间切换。

与很多只在附图里点到为止的自动驾驶论文不同，本文把状态内变量和转移条件也写出来了。尤其是目标速度生成、`DBW enable` 对 target speed 的影响、`dtarget / dtrigger` 的距离判定，以及 stop sign 停稳后 `three seconds` 的等待约束，都让这套 motion planner 更像一个可直接提炼的工程控制器。

## 控制系统在文中的位置

这套控制系统不是论文中的次要例子，而是 autonomous micro-mobility 方案能否落地的关键一环。全局规划负责提供 reference trajectory，但真正把交通规则、速度限制、车辆跟驰和 planned stop 执行出来的是 motion planner 的 `FSM`。因此这里的控制对象既真实，又直接处在系统主链上。

从样本库视角看，它属于比较好的道路车辆 `EFSM + T1` 案例。它不是单纯的行为树架构，也不是只给 high-level mode 名称；相反，作者把状态机的输入量、目标速度更新方式和状态转移 guard 讲得相当具体，因此能稳定支持高质量 `STM` 抽取。

## 对我们为什么有用

这篇论文最重要的价值，是为 `🚗` 方向补充了一类“道路行为监督 + 连续速度规划配合”的样本。文库里已有一些自动驾驶行为规划条目，但 stop-sign、vehicle-following 与 local speed target 的组合并不完全一样。这里既有状态切换，也有工程可执行的 guard，与后续做状态机建模和验证场景生成都贴得比较近。

此外，它对平衡领域分布也有帮助。相比大量 `PLC` 顺序控制样本，这类自动驾驶运动规划论文更能提供路况驱动的离散行为、交通规则约束和局部时间等待语义。只要后续保持这种“状态名 + trigger + output/intention”都明确的筛选标准，汽车方向的样本差异性会更好。

## 如果需要人工细读，建议怎么读

如果后续需要人工重做 `STM.md`，建议先从第 8 页 motion planner 对 `FSM` 的总述开始，确认 `Forward / Follow / StopSign` 是文中真正被实现和解释的状态。然后继续读第 8-9 页 `SpeedKeeping` 与 `Obstacles and Planned Stops`，这里最适合整理状态内变量、目标速度生成和 waypoint 距离定义。最后看第 9 页 state transition logic 部分，把 `dtrigger > dtarget` 和 `StopSignWait = 3 seconds` 这些关键 guard 补齐。

至于更下游的 trajectory tracking controller、pure pursuit 和连续控制设计，可以放到第二轮再看。那些内容对理解整套系统当然有用，但如果目标是抽离散状态机样本，第一轮最值得抓住的仍然是 motion planner 这一层的状态、触发和等待逻辑。
