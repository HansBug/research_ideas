# 自动驾驶 safe-stop 高层监督器 / Design and Formal Verification of a Safe Stop Supervisor for an Automated Vehicle

## 论文在讲什么

这篇论文讨论的是自动驾驶车辆在 `parking lot A -> road network -> parking lot B` 任务中的高层监督控制器。作者关注的问题不是单个规划器如何算轨迹，而是如何在多个 nominal planner 之间切换，并在 GPS 或路径规划失败时可靠地触发 safe stop 或 AEB。

为了解决这个问题，论文把 Supervisor 设计成整个 ROS 架构中的顶层节点，再通过 model-based design、Stateflow 和 model checking 去验证这套切换逻辑是否满足形式化要求。它因此同时包含系统架构、状态机设计、形式化需求和实车/仿真验证四层内容。

## 控制系统在文中的位置

我们关心的控制系统描述是论文的主角，而不是为了说明验证工具才临时搭出来的示例。摘要就把 supervisor 的设计与 formal verification 并列为主要贡献，系统架构和实验部分也都围绕“谁在什么条件下切到哪条 planner / stop routine”展开。

更具体地说，这里的 supervisor 负责协调 `Localization / SPP / UPP / TP / SSTP / Controller`，它对系统的作用类似任务级 HSM：标称时串接 structured 与 unstructured path，失效时触发 `SSTP`，再失败时升级到 `AEB`。这正是 `sources/` 里非常需要的那类“系统级异常恢复链”样本。

## 对我们为什么有用

这篇论文对 `sources/` 的主要价值，是给 `🚗` 方向补入一条非常清晰的 mission supervisor 样本。与只写换道、跟驰或单个 maneuver 的车辆论文不同，它把整趟任务、路径拼接、故障触发和安全停车收拢到同一个高层状态机里。

其次，它不仅有自然语言需求，还有 `Stateflow FSM + LTL` 两层表达：前者帮助我们抽取状态链，后者帮助我们固定 safe stop / emergency stop 的 guard 语义。对后续状态机自动生成数据集来说，这种“自然语言任务链 + 形式化条件”并存的样本非常有代表性。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 2-4 页的摘要和 `System Architecture`，把 RCV 的任务边界、`SPP / UPP / TP / SSTP / AEB` 各自做什么先读清楚。随后立刻进入第 4-6 页 `Supervisor Design` 与 `Formal requirements / Modeling in Stateflow`，因为真正的控制链、故障回退和状态机实现都在这里。

如果需要进一步核对这些状态是否真的在系统中跑起来，再看第 7 页实验部分，特别是 GPS failure 之后的状态颜色与 `WaitingForGoal / CallForPlan / ParkingToRoad / SafeStop` 这些状态名。Promela/SPIN 的证明细节可以第二轮再看，第一轮重点还是把 supervisor 的主状态链和失败回退逻辑读稳。
