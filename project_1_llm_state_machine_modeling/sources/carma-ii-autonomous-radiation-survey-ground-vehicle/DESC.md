# CARMA II 辐射巡检与污染规避监督控制 / CARMA II: A ground vehicle for autonomous surveying of alpha, beta and gamma radiation

## 论文在讲什么

这篇论文做的是一个面向核设施地面巡检的自主机器人系统。CARMA II 既要在核设施地面按 coverage path 做 alpha / beta / gamma 辐射测量，又要避免机器人自己把污染带着走，所以作者把探头前置、辐射 costmap、waypoint planner 和高层状态机绑成了一套完整 survey 平台。

从系统角度看，这不是普通“移动机器人导航加一个传感器”的文章。它把辐射感知如何影响路径、什么时候该倒车、什么时候该跳过 waypoint、什么时候该直接回 home 都写成了明确的监督逻辑，因此正文里我们关心的不是局部探测器，而是那个辐射感知驱动的高层 survey supervisor。

## 控制系统在文中的位置

状态机在文里是核心贡献之一。摘要就明确说引入了 “state-machine and radiation costmaps” 来防止污染扩散，而 Section `4.3.2` 则直接把 `waitingforcall / movingtocurrentwaypoint / reversing` 三态、服务调用、低电量回家、不可达 waypoint 以及辐射阈值触发倒车都写清楚了。

也就是说，这里的状态机不是附带的小实现细节，而是把 waypoint planner、导航栈、辐射探头和安全动作统一编排起来的上层 manager。对 `sources/` 来说，它比很多只写 costmap 或只写 survey path 的机器人论文更像标准的系统级离散控制链。

## 对我们为什么有用

这篇特别有价值的地方在于，它补的是“移动机器人任务 supervisor + 异常恢复链”样本。很多机器人论文只给 nominal path，而这篇把 `low battery`、`waypoint unreachable`、`alpha/beta above threshold` 这些真实工程事件都接进了状态机，而且恢复路径也不只是简单停机，而是会改写当前 waypoint、倒车、更新 costmap、重规划再继续。

另外，它还有很典型的工程时序语义。倒车距离不是随便写的，而是跟前向速度、探头刷新率和探头到车轮距离绑定，正文甚至给了 `1 Hz` 与 `1.0 m` 的工程化设置依据。这种“控制链 + 局部工程定时/采样约束”的写法，对后续 LLM 建模数据集很有参考价值。

## 如果需要人工细读，建议怎么读

如果后续要人工重做 `STM.md`，建议先看摘要，把 CARMA II 的总体任务和“污染规避是状态机负责”的定位抓住；然后直接跳到 Section `4.3.2 State machine` 和 Figure `6`，把状态名、事件名、home 逻辑、倒车逻辑和 waypoint 跳过逻辑逐条抄清；最后再看 Section `5` 里的实验和 Figure `7-9`，核对倒车、重规划和 gamma/alpha 混合场景下的行为。

像前面的硬件结构、costmap 包实现、SLAM 与 waypoint planner 数学细节，可以放到第二轮再看。第一次人工复核的重点应该始终是“survey 何时开始、何时回家、何时倒车、何时跳过、何时恢复”，因为这些才是这篇文献最核心的状态机样本价值。
