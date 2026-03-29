# Developing UPPAAL over 15 years

- 问题一句话：`UPPAAL` 从 1995 走到 2011 已经分化出多条工具支线，真正困难的不再只是“再发明一个算法”，而是如何让一个研究工具长期活下来、还能不断吸收新分支。
- 方法一句话：以 15 年维护经验为主线，复盘 `UPPAAL` 的核心架构、代码组织、分支共用机制和工具开发流程。
- 解决点一句话：给出 `UPPAAL` 为什么能从单一 model checker 长成一族工具的工程解释，并明确哪些架构决策支撑了这种生长。

## 论文定位

这篇论文是 `uppaal_tech/` 中文库里最重要的工程史条目之一。它的价值不在于提出某个新验证算法，而在于从维护者视角解释：

1. `UPPAAL` 的核心为什么能支撑 15 年持续演化。
2. 为什么 `Cora`、`Tron`、`CoVer`、`Tiga`、`Port`、`Times` 等分支不是各自重写，而是能共享一套代码底座。
3. 一个 formal methods 工具要想长期活着，需要什么样的架构、开发组织和社区条件。

因此，这篇论文最适合与技术性条目交叉阅读：

1. 与 [llpy97-compact-data-structure](../llpy97-compact-data-structure/) 和 [behrmann03-real-time-data-structures](../behrmann03-real-time-data-structures/) 联读，可以看到底层数据结构为什么重要。
2. 与 [behrmann07-uppaal-tiga](../behrmann07-uppaal-tiga/) 联读，可以看到新算法如何插进共享引擎。
3. 与 [mikucionis10-online-testing-real-time-systems](../mikucionis10-online-testing-real-time-systems/) 联读，可以看到 testing 分支如何重用主工具能力。

它更像是一篇“`UPPAAL` 内部操作系统说明”，把看似分散的论文线索压成了一个统一的工程谱系。

## 立足问题

这篇论文真正面对的问题，不是“`UPPAAL` 缺哪一个理论结果”，而是研究工具在真实世界里普遍会遇到的三类生存问题。

### 1. prototype 很容易写，长期维护的工具很难活

作者开篇就强调：在 formal methods 领域，写一个 proof-of-concept prototype 相对容易，但要把它做成能撑过十几年的工具极难。原因很现实：

1. academic credit 对理论新结果更友好，对持续维护不够友好；
2. 大量开发工作由短期学生承担，团队会不断更替；
3. 代码会老化，旧设计会阻碍新功能。

所以这篇文章从一开始就在回答一个硬问题：

$$
\text{一个学术验证工具怎样才能在功能持续扩张时不被自身复杂度拖垮。}
$$

### 2. `UPPAAL` 已经从单工具长成“工具家族”

到 2011 年时，`UPPAAL` 已经不只是一个 timed automata reachability checker，而是衍生出了多条支线：

1. `Cora`：cost-optimal reachability。
2. `Tron`：online testing。
3. `CoVer`：coverage-oriented test generation。
4. `Tiga`：timed games / controller synthesis。
5. `Port`：component-based modeling + partial order。
6. `Pro`：probabilities。
7. `Times`：scheduling and analysis。

如果这些分支各自单飞，维护成本会失控；如果全都硬塞在一个 monolith 里，代码又会僵死。论文要解决的正是这种“既要共享底座，又要允许分支长出不同能力”的张力。

### 3. formal methods 工具还面临独特的可信度问题

普通软件即便偶尔 bug，也只是功能问题；验证工具一旦 bug，输出的“正确性结论”本身就可能不可信。所以这篇论文还必须回答：

1. 如何组织数据结构和算法，让不同 checker 尽量复用同一底层逻辑。
2. 如何测试、管理和重构代码，使工具不会因为新增功能而悄悄破坏旧能力。
3. 如何在代码规模增长后，仍能让新人接手和外部合作成为可能。

因此，这篇文章立足的是“工具工程学”，而且是 formal verification 场景下最难的那种工具工程学。

## 核心方法

这篇论文的“方法”不是算法证明，而是一套已经被 15 年实践验证过的架构和开发组织原则。

### 1. 用 client-server 分离 GUI 和 model-checker engine

论文先给出 `UPPAAL` 最核心的总体结构：

1. 前端 GUI 用 Java 写。
2. 后端引擎用 C++ 写。
3. 两者通过本地 pipe 或网络通信。

这个决策听起来朴素，但后果非常深远。

**第一**，它把“用户交互/可视化”和“高性能符号计算”彻底解耦：

1. Java 更适合跨平台 GUI。
2. C++ 更适合底层数据结构和性能敏感算法。

**第二**，它让 remote verification、不同平台部署和不同分支前端定制变得容易。

**第三**，这层分离也让后来的 specialized variants 更容易重用已有组件，而不必每次重写 editor、simulator 和 verifier shell。

也就是说，论文并不是事后回顾“我们用了两种语言”，而是在强调这是一种**分层分责**架构：界面问题和引擎问题必须拆开。

### 2. 用 pipeline architecture 组织引擎内部 checker

这是整篇论文里最关键的工程点。作者把 model-checker engine 设计成一条 filter pipeline，而不是一个巨大、难拆的控制流程序。

reachability 这一典型配置里，主要 filter 链条是：

1. `Transition`
2. `Successor`
3. `Delay`
4. `Extrapolation`
5. `PWList`
6. `Query`

这个设计的好处非常明显：

1. **每个 filter 只负责一个语义步骤**
   - 哪些离散迁移可走。
   - 迁移后怎么更新状态。
   - 时间如何流逝。
   - 何时做外推保证有限。
   - 如何做 waiting/passed 管理。
   - 何时检查查询。
2. **不同 checker 通过重组和替换 filter 获得**
   - 不是整套重写。
   - 而是在同一条管线结构上换掉若干环节。
3. **特性可以按需插拔**
   - 比如 `LazyCopy`、`Sorter`、`Trace`、`Symmetry` 都是可选 filter。

这使得引擎不再是“一坨写死逻辑”，而变成“稳定骨架 + 可替换器件”。

### 3. 用 `PWList` 统一 waiting/passed 状态管理

论文特别提到 `PWList`，这是个很值得注意的细节。传统 reachability 写法往往会维护两个独立结构：

1. waiting list
2. passed list

而 `UPPAAL` 把它们统一进一个结构里，对状态打颜色标记。这样做的好处包括：

1. inclusion check 不必在两个不同表里重复查找。
2. 主循环的状态管理更统一。
3. 对不同 checker 来说，这一层可以复用，而不必重复设计状态缓存机制。

这类设计在论文里只占少量篇幅，但它恰恰说明 `UPPAAL` 的可维护性来自大量类似的底层统一。

### 4. 用可替换 filter 支持不同语义与新算法插入

论文最能说明 pipeline 威力的地方，是它解释了新 checker 为什么能够“接在老引擎上”。

例如：

1. 做 timed games 时，需要 backward propagation、winning/losing 后处理、不同 graph representation。
2. 做 simulation checking 时，需要改写 `Transition` 和 `Delay` 的语义。

但这些变化并不需要重写整个 engine，而是：

1. 保留管线总形状。
2. 替换少数特定 filter。
3. 接上新的后处理组件。

这实际上就是 `UPPAAL` 能衍生出 `Tiga`、`Tron`、`CoVer` 等分支的工程基础。也就是说，许多后续论文能成立，不只是因为有理论结果，也因为核心引擎结构允许新结果插进去。

### 5. 复用 DBM、parser 和虚拟机等基础库

论文还强调了几个被多个分支共享的基础能力：

1. **DBM library**
   - 支持 DBM 与 federation。
   - 包括 subtraction、merging 等操作。
2. **parser**
   - 理解 `UPPAAL` XML 格式。
   - 让其他研究者和外部分支能对接相同模型格式。
3. **virtual machine**
   - 执行 `UPPAAL` 的 C-like 输入语言。
   - 支持用户自定义函数和复杂数据操作。

这里特别重要的是：`UPPAAL` 的可扩展性不只是“checker 能插 filter”，还包括“语言层和数据结构层本身就是共享资产”。所以后来像 [jensen23-dynamic-extrapolation-extended-timed-automata](../jensen23-dynamic-extrapolation-extended-timed-automata/) 这种更现代的 XTA 抽象工作，才有可能在已有语言底盘上继续推进。

### 6. 把“工具生存”视为架构与团队组织问题

从论文后半部分开始，作者转向真正少见但极有价值的话题：**工具为什么会死，怎样才能不死**。

作者给出的经验几乎每条都很硬：

1. 需要稳定的整体设计，哪怕后来的新人未必喜欢旧风格。
2. 需要有留得足够久的人来承担“大修”与重构。
3. 代码规模到一定程度后，必须重新抽象接口，否则新人无法进入。
4. 仅靠临时学生团队很难保证长期演进。

这些经验不是泛泛而谈，因为论文把它们和 `UPPAAL` 自己的 life cycle 连起来讲了。

### 7. 明确划分 `UPPAAL` 的多个 life cycles

论文把 `UPPAAL` 15 年的发展拆成多个生命周期：

1. 最早的 editor/simulator 原型阶段。
2. 引入 integrated graphical editor 与 client-server 结构的阶段。
3. 当前的 modular pipeline architecture 阶段。

这说明 `UPPAAL` 不是线性长大，而是经历过数次“旧设计不再够用，于是做一次大重构”的周期。对理解工具演进非常重要：

1. 早期重点是性能与基础功能。
2. 后期重点越来越多转向语言特性、界面和新分支算法。
3. 当前架构能活八年，说明它足够稳，但论文也明确说到了 2011 时已经再次接近需要大更新的边界。

这种“把架构重构作为工具生命周期的一部分”是整篇文章最成熟的判断之一。

### 8. 把 testing、bug management、community 视为核心基础设施

论文对 testing 和 community 的态度也非常务实。

1. formal tool 理应被严格测试，但现实中要完整验证工具本身极难。
2. 因此作者依赖 `gcov`、`purify`、bug management system` 等普通软件工程手段。
3. 同时依赖用户社区、邮件列表/论坛和外部用户互助来维持工具生命力。

这传达了一个很重要的信息：形式化工具并不会因为“自己做验证”就免于普通软件工程的纪律，相反，正因为它输出的结论太重要，测试、issue 管理和社区反馈更不可少。

## 解决了什么问题

这篇论文解决的主要不是“用户怎么按按钮”，而是“为什么 `UPPAAL` 没有像很多学术 prototype 那样在功能膨胀后崩掉”。

### 1. 它给出了 `UPPAAL` 多分支共存的工程解释

读完这篇论文后，就能比较系统地理解为什么 `UPPAAL` 能同时容纳：

1. reachability / liveness / leads-to 等传统 checker；
2. `Tiga` 这类新语义分支；
3. `Tron`、`CoVer` 这类 testing 分支；
4. `Cora`、`Times` 等 specialized branches。

答案不是“因为作者们努力”，而是因为有一套明确的共享底座与替换机制。

### 2. 它把“工具维护”本身提升成正式研究对象

很多论文默认工具只是承载理论的载体，这篇论文反过来说明：

1. 工具架构会反过来决定哪些理论结果更容易被落地。
2. 工具是否易扩展，会影响一个研究方向能否形成连续谱系。

所以这篇文章实际上解释了 `UPPAAL` 技术线为什么看起来比很多别的 formal tools 更连续。

### 3. 它明确指出了当时的技术债与未来方向

论文没有把 retrospective 写成庆功文，而是非常坦白地指出：

1. 缺乏 multi-core 支持。
2. 仍依赖 32-bit 假设与特定数据结构。
3. 架构已开始被新变体拉扯。
4. 需要新的大规模接口重构。

因此它不仅总结过去，也给出未来几年技术演进的压力点。

## 与 UPPAAL 技术线的关系

如果说很多论文解释的是 `UPPAAL` “会什么”，那这篇文章解释的是 `UPPAAL` “为什么能一直继续学会更多东西”。

它和技术线其他论文的关系可以概括成三层：

1. **向后看理论根基**
   - timed automata、zones、DBM 等早期理论工作是内核的语义与数据结构来源。
2. **横向看分支生态**
   - `Cora / Tiga / Tron / Times / Port / Pro` 都被放回同一工程框架来理解。
3. **向前看现代扩展**
   - 后续 randomized analysis、dynamic extrapolation、Stratego/Coshy 等新方向，都可以被视为在这个“共享底盘”上继续演化。

如果没有这篇工程 retrospective，单看论文时间线会觉得 `UPPAAL` 像是一串离散成果；看完这篇，再回头看那些论文，会更容易意识到它们其实是一个共同工程体的连续生长。

## 实现与材料

- 内容详细程度：`🟧 概览级`。它讲得很实，但毕竟是 retrospective，不会像算法论文那样把某个技术点推到复现级细节。
- 实现可获取程度：`🟨 部分实现源码可得`。从今天的视角看，可以直接拿到不少 `UPPAAL` 相关基础库源码，但不是整个历史版本工具树的完整公开快照。
- 可追线索：
  - `UDBM`
  - `utap`
  - `uppaal-libs`
  - 官方文档站与下载页
- 阅读策略：
  - 这篇最适合和具体技术论文对照着读。
  - 单独阅读可建立全局图景，但不够支持某个子分支的技术复现。

## 对本研究的启发

这篇论文对当前博士研究的启发，不在于 timed automata 理论，而在于**如何组织一条能活下去的研究工具链**。

1. **闭环系统必须从一开始就考虑模块化**
   - 你的研究目标覆盖“生成-验证-修复”三段，如果这三段没有共享中间表示和统一接口，后面一定会碎。
2. **算法与工具架构要双向适配**
   - 不是“先做完算法，再想怎么接工具”，而是要像 `UPPAAL` 一样让新算法能插进稳定骨架。
3. **需要明确生命周期和重构点**
   - 当状态机建模、性质生成、验证画像、修复策略不断叠加后，仓库也会出现“旧设计不再够用”的阶段。
   - 这篇论文提醒我们，要把大重构视为正常生命阶段，而不是事故。
4. **研究软件也要用普通软件工程纪律管起来**
   - bug 管理、接口抽象、文档、测试、社区入口，这些不会因为研究味更浓就自动消失。

简而言之，这篇文章解释了 `UPPAAL` 这条技术线为什么能持续二十多年。对你当前的研究仓库来说，这种“方法线 + 工具线共同演化”的组织方式本身，就是值得直接学习的东西。
