# 城市自动驾驶实时决策状态机 / Real-Time Decision Making for Autonomous City Vehicles

## 论文在讲什么

这篇论文关注的是城市自动驾驶里的高层实时决策问题。作者不是把重点放在底层转向或轨迹跟踪上，而是讨论车辆面对真实城市交通时，如何根据 World Model 选择合适的 driving maneuver，并把不同 maneuver 的执行逻辑统一成一个可切换、可中止、可恢复的离散控制框架。

论文最关键的技术点，是把每个 driving maneuver 都写成同一套确定有限自动机模板：有等待态 `q0`、若干 `Run` 相位、成功态 `qF` 和错误态 `qE`，并且统一使用 `Run / Stop / Restart / Error` 这组事件控制启停与异常中止。作者还给了 overtaking 的五阶段分解，说明这个模板不是空泛定义，而是真正用于组织具体 maneuver 的执行。

## 控制系统在文中的位置

这里的状态机不是附属图示，而是 decision making subsystem 的直接表达方式。论文第 4 节先解释 driving maneuver subsystem，再给出 automaton 的组成、输入事件和 Run-state 语义，随后在第 5 节说明 decision making 如何基于 World Model 选择可执行 maneuver。也就是说，这篇论文里“状态机”就是自动驾驶高层行为控制器本身的主表达载体。

对 `sources/` 来说，这类样本很有价值，因为它补的是“复杂自动驾驶任务如何被分解为阶段化离散 supervisor”的写法。它既不是纯粹的 architecture paper，也不是只剩一个抽象 behavior list 的概念稿，而是把 maneuver 的统一执行壳、错误出口和阶段分解都写得足够明确。

## 对我们为什么有用

这篇论文能补强 `🚗` 方向里比较难找的 `FSM + T0 + 双 A` 样本。它和库里那类“五种驾驶行为模式”条目不同，不是直接给平铺的行为集合，而是给出一个更通用的 multi-phase maneuver automaton，可以拿来支持后续“从自然语言中恢复统一状态机骨架”的实验。

它还有一个额外好处：原文明确把安全前置条件检查放在 Run states 内部，并规定未满足条件时进入 `qE`。这使得后续做自动化抽取时，不只是能抽出状态名，还能抽出“precondition failure -> abort”这种很重要的控制分支。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 2 节系统架构，再直接跳到第 4 节 `The Driving Maneuver Subsystem`。优先抓住三件事：第一，automaton 的统一组成；第二，`Run / Stop / Restart / Error` 这组事件各自代表什么；第三，overtaking 为什么会被拆成五个相位。读顺这三点后，再去第 5 节看 feasible maneuver 与 World Model events 的关系，就能把这篇文章的高层离散控制链完整接上。
