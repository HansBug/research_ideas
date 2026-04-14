# 三态启发式 SUAS 目标跟踪监督器 / Feasibility of Onboard Processing of Heuristic Path Planning and Navigation Algorithms within SUAS Autopilot Computational Constraints

## 论文在讲什么

这篇 AFIT 论文关注的是 SUAS 对移动地面目标执行 convoy overwatch / target tracking 时的飞行路径最优性问题。作者先用 HIL 和实验设计方法研究默认跟踪逻辑与若干导航参数，再尝试用一个可在机载 autopilot 上实时执行的启发式策略，去逼近更优的 stand-off range 维持效果。

论文的主线并不只是“算出一条最优路径”，而是问：在算力受限的 SUAS autopilot 上，能不能用足够轻量的状态机逻辑，在线近似这些更优策略。最后作者确实把这一思路落成了一套 revised FSM，并给出 `Jthreshold`、buffer 以及状态进入效果的飞行验证。

## 控制系统在文中的位置

这里的控制系统描述就是论文最核心的工程落地产物。前面的实验和 cost 分析都是为这个问题服务：哪些飞行情形真正需要切换行为、切换到什么程度才有意义、又怎样避免状态来回抖动。最终论文不是停留在“optimal path planning is desirable”的层面，而是明确构建了一张 revised FSM 图，把 nominal tracking 和两种增强 tracking 行为组织成一套可部署的监督器。

这一点对 `sources/` 很重要，因为它把“启发式 tracking policy”从连续优化背景中抽成了清楚的离散控制链。相比很多只给 cost function 或轨迹比较的论文，这篇更适合做状态机数据集样本，因为它真正给出了状态、切换逻辑和在线执行边界。

## 对我们为什么有用

它补的是航空航天方向里另一种和任务管理、flight mode 不同的 `FSM + T0` 样本：这里的状态并不是 mission phase，而是跟踪强度与控制 effort 的模式切换。与常见 `TakeOff / Cruise / Landing` 一类监督器相比，这种样本能让后续模型看到“状态机也可以用于在线启发式控制补偿”，而不只是顺序任务推进。

同时，这篇论文与另一篇 `36` 态 wind-maneuver 参数切换 FSM 形成了很好的互补。前者偏离散工况到参数表的映射，这篇则更像围绕 tracking error 与 `J_i` 设计少量高价值状态，因此非常适合作为同域但不同控制粒度的对照样本。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看摘要和 methodology 里关于 `finite state machine approach to path planning` 的几段，先确认作者是在把 tracking heuristic 写成在线状态机，而不是只做最优控制对比。随后直接跳到 Figure `29` 以及紧随其后的 second-iteration FSM 说明，把 `Initial State Check`、`Standard / Low Range / High Range Target Tracking` 三个主状态和 `Jthreshold = 0.003`、`35 m buffer` 这两个关键参数读清。

如果后续还想理解为什么会需要这三个状态，再回到前面的 `J_i` 曲线分析和 flight path 对比图。第一轮不必陷进大量代价函数和实验矩阵细节，因为对状态机抽取最关键的信息，已经集中在 revised FSM 图、阈值说明和 state profile 验证这几个位置了。
