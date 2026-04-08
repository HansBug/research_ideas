# 无人水面艇自主靠泊状态机 / Model Reference Adaptive Control-Based Autonomous Berthing of an Unmanned Surface Vehicle under Environmental Disturbance

## 论文在讲什么

这篇论文讨论的是 small USV 在有风浪扰动条件下的自主靠泊问题。作者并没有把重点完全放在连续控制器性能上，而是先把 berthing scenario 形式化成 parallel type 和 finger type 两类靠泊流程，再在每个流程内部组织 approach、alignment 和 docking 阶段。

论文的结构也很适合样本库使用。前半段先讲 berth path planning，把状态机说清楚；后半段才接上 vector-field path following 和 MRAC/PID 控制。换句话说，离散阶段链和连续控制环是分层描述的，这让它很适合抽成 `STM.md`。

## 控制系统在文中的位置

这里的控制系统是论文主体，而且是一个典型的“高层 supervisor + 低层 controller”组合。高层 state machine 负责判断船现在属于哪一个靠泊阶段、何时转向、何时倒车、何时判定靠泊完成；低层控制器负责把这些阶段要求变成实际的航向和推进控制。

尤其有价值的是，作者没有只写“靠近目标然后停下”，而是把 parallel/finger 两条路径下的阶段分解和距离阈值说得很明确，还给了“误差连续保持 3 秒才算成功”的完成条件。这种写法对后续从自然语言恢复 EFSM 非常友好。

## 对我们为什么有用

对 `sources/` 来说，这篇论文补的是一个比较稀缺的海事/水面载具监督控制样本。虽然库里也有 ASV docking、mission management 一类条目，但这篇的重点是靠泊阶段机本身，而且把两种 docking pattern 放在同一框架里，结构差异很明显。

它对后续建模还有一个很直接的价值：离散阶段逻辑和连续控制器接口边界很清楚。做状态机恢复时，可以先只恢复 `approach / alignment / docking` 这些阶段和 guard，再把 path following 与 MRAC 看作 state-associated control law。这正是很多复杂控制系统里常见的建模方式。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `3-5` 页，把 Figure `2-3` 和 parallel/finger 两套状态机读透。先确认每个阶段叫什么、什么距离条件触发转移、何时进入最终 docking、成功条件为什么是 `10% length + 3 s`。只要这一层读明白，后面的控制器细节就好挂靠了。

然后再读第 `5-8` 页的控制系统部分，重点看 vector-field guidance 和 heading controller 怎样服务上层阶段。实验和 boxplot 结果可以放到第二轮再看；如果只是为了重做 `STM.md`，优先级最高的是两套状态机、距离 guard 和 final docking completion condition。
