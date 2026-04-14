# 机器人足球分层状态机策略 / Robot Soccer Strategy Based on Hierarchical Finite State Machine to Centralized Architectures

## 论文在讲什么

这篇论文讨论的是一个 centralized robot soccer team 的团队策略系统。作者要解决的不是单个机器人怎么避障，而是整个球队如何根据球的位置和控球态势，在 defense、counterattack、pressure、attack 这些战术之间切换，并且在切换后重新分配 defender、midfielder、attacker 等角色。

论文的主线非常清楚：先给出分层状态机架构，再定义战术选择依据，然后给出角色分配算法，最后说明每个角色对应的行为。它不是泛泛讲“multi-agent coordination”，而是把具体条件、角色和行为都写到可执行的层次。

## 控制系统在文中的位置

这里的控制系统就是论文的核心对象。所谓 hierarchical finite state machine 不只是点到为止的建模术语，而是整个 team strategy 的组织方式：第一层选 tactic，第二层给角色分配行为，第三层才是机器人的低层控制执行。

尤其值得保留的是“virtual coach”这一层。它把球和球员的相对位置映射成角色分配规则，让这篇论文不只是一个静态行为库，而是一个会根据比赛局势重构团队分工的动态协调器。对样本库来说，这类“战术层 -> 角色层 -> 行为层”的层次非常有辨识度。

## 对我们为什么有用

对 `sources/` 来说，这篇论文补的是一个不依赖 PLC、但离散控制链很完整的 `HSM + T0` 协同机器人样本。它把 tactic、role、behavior 三层都写得比较清楚，可以帮助后续数据集摆脱“顺序控制设备”过多的单一画像。

另外，这篇论文在自然语言层面也很适合做状态机恢复。战术判定条件、角色集合、角色分配算法和行为名称都很明确，文本中有大量可直接抽取成状态、guard 和 action 的词汇。对于做层次状态机恢复、角色分配建模或多智能体离散协同的人来说，这篇文章的表达很有代表性。

## 如果需要人工细读，建议怎么读

人工重读时，建议先看第 `2-4` 页，把 `Figura 1-3` 附近的层次结构读清楚，先确认 top-level tactic selection、virtual coach role assignment 和 lower-level behavior selection 三层分别负责什么。只要这一层次关系读顺，后面的角色分配算法就不会看乱。

然后跳到第 `6-8` 页，重点看 `Asignación de roles` 和 `Selección de comportamientos`。先抓 `rd / rs / ra` 各自怎么由距离球、距离球门等几何条件决定，再看每种 tactic 下的主要行为。实验结果和 200 场仿真统计可以放到第二轮再看；如果是为了重做 `STM.md`，优先级最高的始终是层次结构、战术切换条件和角色行为映射。
