# 无人机自动应急管理安全监视器 / Automated Contingency Management in Unmanned Aircraft Systems

## 论文在讲什么

这是一篇关于无人机自动应急管理的博士论文，目标是让 `UAS` 在失链、导航退化、控制退化等异常情况下具备更高等级的机载自动化能力。整篇论文覆盖软件架构、任务计划表示、风险模型和仿真验证，篇幅很长，不是那种只给一张状态图的短文。

不过，对 `sources/` 最有价值的并不是整套规划框架，而是其中负责安全判别和应急升级的 `Safety Monitor`。论文在架构章节和附录里把这个监视器定义成一个明确的中央状态机，并进一步用 `C2 link loss` 仿真展示状态如何从 `Nominal operation` 切到 `Autonomous operation`，再在恢复信号后回到正常运行。

## 控制系统在文中的位置

我们关心的控制系统描述在文中属于“安全关键任务管理子系统”，不是外围示例。`Safety Monitor` 和 `Contingency Manager` 被明确区分：前者负责判断是否仍有安全余量去执行 contingency option，后者才负责在允许范围内挑选具体的应急策略。也就是说，`Safety Monitor` 不是普通状态标签器，而是机载应急管理架构里的核心判定器。

这使它非常适合作为 `project_1` 的一个航空任务管理样本。它既有清楚的状态集合和进入条件，又有“异常可恢复 / 紧急不可恢复”这种很典型的安全控制语义；同时还保留了“必须始终一跳可达 `Out of control`”这种工程约束，和普通 mission mode 说明相比，控制意图更集中。

## 对我们为什么有用

对 `sources/` 来说，这篇论文主要补的是 `✈️` 方向里较少见的“任务安全监视状态机”样本。航空航天方向很多论文会停留在连续飞控、轨迹规划或架构说明层，而这篇把安全监视器本身当作明确的状态机对象来定义，并且写出了状态语义、升级原则、不可恢复终态和验证场景，质量明显更高。

它对后续数据集构建也很有帮助，因为这里的控制对象不是普通的相位调度器，而是带安全阈值和异常升级逻辑的 mission safety supervisor。后续如果要让模型学习“单个异常进入可恢复态、嵌套异常升级到终止态、恢复后返回 nominal”这类安全模式，这篇提供了很好的英文原始语料。

## 如果需要人工细读，建议怎么读

人工细读时，建议先跳到第 `97-98` 页附近的 `Safe Mission Manager architecture design`，先把 `Safety Monitor` 与 `Contingency Manager` 的职责边界读清楚，尤其要抓住“谁决定是否直接终止飞行”“谁决定是否还可以尝试 contingency management option”这条分工线。然后直接看附录 A 的 `A.2 Specification of the Safety Monitor model`，这里有最完整的状态集、进入条件和模型约束。

读完状态机定义后，再去第 `222-224` 页的 `C2 link loss` 验证场景，看 `Safety Monitor` 如何实际进入 `Autonomous operation`、执行 regain-signal 策略并在恢复后返回 `Nominal operation`。其他关于 mission-plan 语法、风险模型和图搜索的章节可以第二轮再看；它们有助于理解整篇论文的系统设计，但对重做当前这条 `STM` 主链不是最优先的证据源。
