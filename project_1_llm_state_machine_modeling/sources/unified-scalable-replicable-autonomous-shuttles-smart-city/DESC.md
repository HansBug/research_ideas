# 统一架构下的自治 shuttle 规则式驾驶监督器 / A Unified, Scalable and Replicable Approach to Development, Implementation and HIL Evaluation of Autonomous Shuttles for Use in a Smart City

## 论文在讲什么

这篇 SAE 论文试图回答一个很工程化的问题：如果想让同一套 autonomous driving 架构既能迁移到乘用车，也能迁移到低速 shuttle，上层监督控制器该如何写得既统一又可复制。作者提出的是一个 unified architecture，不只是硬件传感器和执行器布局统一，还包括 Simulink 软件库和高层决策框架统一。论文特别强调，这样做的目标是让不同平台之间共享尽可能一致的自动驾驶能力，再通过少量参数调优完成迁移。

在这套统一架构中，我们最关心的部分是高层 decision-making framework。作者没有把它做成难以追踪的黑箱，而是明确采用一套 rule-based `FSM`/Stateflow 方案，用来在路径跟随、跟车、路口、交通灯、障碍物和紧急接管之间切换。相比很多只谈“自动驾驶系统架构”的文章，这篇稿子真正把监督器写成了一个可落地的状态机对象。

## 控制系统在文中的位置

控制系统描述在文中占据核心地位，因为整篇论文就是围绕“如何把统一自动驾驶架构部署到不同车辆平台”展开的。感知、定位、通信和底层控制当然都在讲，但它们最终都被组织到这套上层监督器之下。作者甚至直接说明：感知和定位块提供输入，高层决策块用有限状态机实现驾驶状态判断，底层控制块再据此计算油门、制动和转向命令。

这意味着文中的状态机不是一个边角概念，而是连接感知层和执行层的中心枢纽。对于 `sources/` 来说，这类样本非常有价值，因为它体现的是“系统监督器”而不是单一子模块。它既有明确的状态集合，又有层次化子状态和 `after(...)` 型局部定时，还把人工接管和急停放进了同一张状态图中。

## 对我们为什么有用

这篇论文之所以值得留在文库里，是因为它给出了一条比普通 `CC / ACC` 三态控制更完整的自治车监督链。`Self-localization` 负责进入可驾驶状态，`Path Following` 下还有 `CarFollow` 子状态，`Intersection` 与 `Traffic Light` 都带等待和再检查逻辑，`Obstacle` 用于单车道停车避障，而 `Emergency Stop` 可以从任意状态抢占。这种写法已经明显超出简单平面 FSM，更接近 `HSM + T1 + 协议交互` 的系统级样本。

它还有一个额外优势：作者把状态描述和 Stateflow 图放在了一起，并且给出了 `drive = 0 / 1 / 2`、`after(3,sec)`、`after(1,sec)`、`after(5,sec)` 这类很适合抽取的工程细节。对于后续 LLM 从自然语言重建层次化状态机来说，这种“正文规则解释 + 状态图条件 + 局部定时转移”三位一体的素材非常珍贵。

## 如果需要人工细读，建议怎么读

如果后续需要人工重读，建议先看第 3-5 页的 `Decision Making Framework` 与 Stateflow 图。第一轮阅读只要抓住三组东西就够了：状态集合、触发输入、定时/抢占条件。重点圈出 `Self-localization`、`Path Following / CarFollow`、`Intersection`、`Traffic Light`、`Obstacle`、`Emergency Stop`，再把 `left_turn`、`traffic_light_red`、`car_in_front`、`cross_traffic`、`obstacle`、`e_stop` 这些输入与 `after(...)` 定时条件对应起来。

至于前面更偏 unified hardware、Simulink library、鲁棒横向控制参数空间设计的内容，可以放到第二轮再看。它们对理解整篇论文的系统工程背景很重要，但如果目标是重做 `STM.md`，第一次人工复核最该确认的是这套高层监督器怎样基于感知输入切换状态，以及在异常和人工接管下如何安全退回手动控制。
