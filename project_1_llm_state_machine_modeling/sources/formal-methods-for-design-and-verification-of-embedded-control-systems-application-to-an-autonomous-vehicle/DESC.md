# 自动驾驶车辆 Gcdrive 急停仲裁状态机 / Formal Methods for Design and Verification of Embedded Control Systems: Application to an Autonomous Vehicle

## 论文在讲什么

这是一篇 Caltech 的博士论文，主题是如何用 formal methods 支撑嵌入式控制系统的设计与验证。整篇论文范围很大，既讲混成系统验证，也讲控制软件综合，还用 DARPA Urban Challenge 的自动驾驶车辆 Alice 作为核心案例来说明这些方法怎样落到真实系统上。

对 `sources/` 来说，最有价值的不是整套形式化框架本身，而是作者没有停留在抽象建模层，而是把 Alice 中一些真实控制模块写到了可验证、可追溯的状态机粒度。这里选择的 `Gcdrive` 就是很典型的一条：它不是高层路线规划，而是车辆执行接口如何响应 `estop pause / run / disable` 等并发命令的安全仲裁逻辑。

## 控制系统在文中的位置

`Gcdrive` 状态机在文中属于低层执行控制模块，但它不是边角料。作者明确说明 `Gcdrive` 负责从 Path Follower 和 DARPA 接收独立命令，并把它们转换成油门、制动和变速执行命令，因此它直接处在“自动驾驶软件如何真正驱动车辆”的关键链路上。正因为这一层一旦写错会出现安全风险，论文才用 model checking 去验证它的实现是否满足急停和恢复性质。

这使得它非常适合作为 `sources/` 样本。很多自动驾驶论文即使有行为 planner，也未必把低层安全仲裁写成这么清楚的 FSM。这里不仅给出状态集合和转移，还把各状态下的执行器动作、`5 sec` 恢复定时，以及 `disable` 不可逆重启等规则都写清楚了。

## 对我们为什么有用

这篇论文补的是车辆方向里一类比较稀缺的 `FSM + T1` 样本：不是 lane change、intersection 或 overtaking 那类行为规划，而是急停仲裁与执行接口安全控制。对后续数据集而言，它能帮助拉开“高层行为决策”和“低层安全执行控制”之间的粒度差异，也能补上一个很典型的局部工程定时样本。

另外，它还展示了 formal methods 论文里什么样的案例值得真正收进 `sources/`。不是所有验证论文都该纳入，但像 `Gcdrive` 这样，论文虽然讲验证，却把实际控制状态机写得足够清楚，就很适合作为可追溯的控制系统样本保留下来。

## 如果需要人工细读，建议怎么读

人工重读时，建议直接跳到 `4.3 Verification of Gcdrive Finite State Machine` 这一节，从 Figure `4.3` 开始，把 `Disabled / Paused / Running / Resuming / Shifting` 五个主状态、`Unknown` 初始态、以及 `estop pause / run / disable` 三类触发先读清。然后继续往下看 global variables 和 desired properties，把 `timer ∈ {0..5}`、`Resuming` 的 `5 sec` timeout，以及哪些状态必须 `acc = -1` 这几条安全约束收齐。

Traffic Planner、PCHA、LTL synthesis 和后面的 autonomous driving case studies 可以第二轮再看。它们对整篇论文当然重要，但如果目的是稳定重建这条状态机样本，第一轮只需要把 `Gcdrive` 的状态图、输入命令集和安全性质读透即可。
