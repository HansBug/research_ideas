# Integrating Tools: Co-simulation in UPPAAL Using FMI-FMU

- 问题一句话：已有 `UPPAAL`-外部工具协同主要把 `UPPAAL` 当外部 `FMU` 用，仍缺一种能让 `UPPAAL SMC` 直接吃进 `FMU` 并对组合系统做统计时序分析的统一语义。
- 方法一句话：论文扩展 `UPPAAL` 以支持动态链接外部 `C` 库和 `FMI-FMU`，再把 master algorithm 编码成 timed automata，在 `UPPAAL SMC` 的随机语义里实现 interleaving-aware co-simulation。
- 解决点一句话：它把 `FMU` 真正内化为 `UPPAAL SMC` 可分析的组件，打开了 bounded `MITL` 统计验证、异构控制器分析以及后续 `Stratego/Tiga` 复用的入口。

## 论文定位

这篇论文属于 `🛠️ 工程/工具链`，但它在 `UPPAAL` 技术线里的地位比一般接口封装论文更重要。若说 [bogomolov15-cosimulation-hybrid-systems-spaceex-uppaal](./../bogomolov15-cosimulation-hybrid-systems-spaceex-uppaal/) 解决的是“如何让 `UPPAAL` 作为 `FMU` 接进外部协同环境”，那么本文解决的是反向问题：**如何让 `UPPAAL SMC` 自己成为 host/master，把外部 `FMU` 和任意 `C` 函数都拉进其统计语义框架。**

它所处的位置非常像一条工程演进主线上的第二步：

1. 先有 `FMI` 标准与跨工具 co-simulation；
2. 再有 `UPPAAL` 作为协同组件参与异构模型；
3. 然后本文把 `FMU` 直接嵌入 `UPPAAL SMC`，使外部工具模型变成 `UPPAAL` 查询语言、概率语义和时序逻辑能够直接分析的对象。

因此它并不只是“加个导入功能”，而是把 `UPPAAL SMC` 的语义边界从原生 automata 扩展到更广泛的异构组件系统。

## 立足问题

这篇论文面对的问题，与前一篇 `SpaceEx + UPPAAL` 协同工作相似，但更进一步。作者观察到：

1. 不同工程域已经各自有成熟建模工具，例如 `Modelica`、`Matlab`；
2. `FMI-FMU` 已经提供了共同接口，能让这些工具导出可组合组件；
3. 但现有 co-simulation 工具往往只负责“跑起来”，很少提供像 `UPPAAL SMC` 这样严肃的统计时序分析语义。

于是问题变成：**能否不重写外部模型，而是把它们直接带进 `UPPAAL SMC`，继续使用 `UPPAAL` 的概率模拟、bounded `MITL` 检查乃至后续控制器合成能力。**

这里有两个核心难点。

第一个难点是语义。单纯能“调用外部库”不代表分析结果有 formal meaning。作者要求：

1. 外部函数是 stateless 的；
2. 未解析的 nondeterminism 不能藏在 `FMU` 内部；
3. 所有 relevant state 都应通过 `FMU` 接口受 master algorithm 控制。

第二个难点是并发顺序。论文专门拿 `UPPAAL` 经典 interleaving semantics 和外部 `FMI` 协同语义对比，指出若 master algorithm 只选某一种固定顺序，就会 under-approximate 某些关键行为，尤其是在 0-delay / 同时可动作的场景下。

因此，本文真正立足的问题不是“让 `UPPAAL` 调用外部模型”，而是：

1. 如何把外部 `FMU` 包进 `UPPAAL` 的 STA/NTA 语义；
2. 如何在该语义里保留 interleaving 相关的统计意义；
3. 如何让 `MITL`、概率估计等分析仍然有可追溯解释。

## 核心方法

整篇论文的方法由三层组成：`UPPAAL` 运行时扩展、`FMU` 到 timed automata 的包装、以及 master algorithm 的显式 automata 化。

### 1. 先扩展 `UPPAAL`，允许动态调用外部 `C` 库

作者首先改造 `UPPAAL`，加入动态链接外部 `C` library` 的能力。这个扩展表面上像一个编程接口，但实际上是后续所有 `FMU` 内化的基础，因为 `FMU` 本质上就是一组标准化的 `C` API。

论文补充了：

1. `string` 与 `ptrt` 等额外类型；
2. 每个 `import` 语句拥有独立作用域；
3. `ON_CONSTRUCT` / `ON_DESTRUCT` 生命周期钩子；
4. `UPPAAL` 类型与 `C` 类型的双向转换规则。

这一步的重要性在于：外部组件不再只是以 trace 文件或离线数据形式供 `UPPAAL` 使用，而是可以在 simulation loop 中被逐步调用。

### 2. 给 timed automata、NTA、STA 和 `FMU` 同时写清语义

论文没有直接跳进工具实现，而是先重述 timed automata / network of timed automata / stochastic timed automata 的语义，然后再定义 `FMU`：

$$ F = (S, init, V, set, get, doStep). $$

若是 stochastic `FMU`，则进一步扩展为：

$$ F_s = (S, V, set, get, doStep, P). $$

作者这里的关键判断是：`FMU` 可以被看作一个定时状态机，而 `UPPAAL SMC` 本来就在处理带概率的 timed automata。于是论文不是另起炉灶设计新分析器，而是试图把 `FMU` 包装进 `STA` 框架。

这种做法的难点，在于 `FMU` 没有原生的同步标签和 automaton-style discrete transitions，所以需要再包一层 TA 模板来承接 `initialize / get / set / doStep` 等标准接口。

### 3. 用 timed automata 明确编码 master algorithm

论文第四部分是方法核心。作者没有把 master algorithm 写成外部调度脚本，而是**直接把 MA 和每个 `FMU` 都建成 timed automata 模板**。

MA 的关键共享变量包括：

1. `comp`
   - 记录各 `FMU` 当前内部状态；
2. `time`
   - 记录全局仿真时间；
3. `x`
   - 记录自上一步以来流逝的时间；
4. `step[i]`
   - 每个 `FMU` 提议的步长；
5. `cnt`
   - 当前阶段已完成的 `FMU` 数量。

单轮 simulation step 大致分成：

1. `initialize`
   - 所有 `FMU` 完成初始化并向 MA 报到；
2. `FindMin`
   - 所有 `FMU` 提议自己的最大可接受步长；
3. `Waiting`
   - MA 取最小步长并推进时间；
4. `get`
   - 从发生变化的 `FMU` 拉取值；
5. `Transfer`
   - 把值分发给依赖该值的其他 `FMU`；
6. `Negotiate`
   - 回到下一轮步长协商。

这和单纯在外部运行一个 FMI host 最大的不同是：**整个 MA 本身也进入了 `UPPAAL` 的状态空间和概率语义**，因而后续 query 可以直接对这套协同过程发问。

### 4. 通过随机化 transfer 顺序显式恢复 interleaving 语义

本文一个非常关键的技术点，是作者并没有接受“一个确定的 FMI host 顺序就足够”这个前提。相反，他们把多个 `FMU` 的值传递顺序随机化，并明确说这是为了恢复 interleaving semantics 对结果概率的影响。

尤其在零延迟场景：

1. 若某个 `FMU` 以 0-delay 赢得 race，它先推进；
2. 其他 `FMU` 则等待后续同步；
3. 在 transfer 阶段，不同 `FMU` 的写入顺序按均匀分布随机选取；
4. 这样如果两个 `FMU` 都可能写同一变量，`UPPAAL SMC` 就会在多次仿真中逐渐探索到不同 interleaving。

换句话说，论文不是去消灭 interleaving，而是用 `SMC` 的随机仿真能力把它重新纳入可估计的语义对象。

### 5. 限制外部组件的行为边界，保证语义仍可解释

为了让上述方法不是“随便跑外部黑盒”，作者对外部函数和 `FMU` 提了非常明确的边界：

1. 外部函数必须 stateless；
2. `FMU` 内部可以有随机性，但不能保留未由 MA 控制的 nondeterminism；
3. 对 classical model checking 场景，还要进一步要求严格 determinism。

这些约束的本质是：外部组件状态必须被 `UPPAAL` 看得见、管得住，否则 query 的概率/时序解释就会漂掉。

### 6. 用三房间供热案例展示统计能力

论文案例不是为了展示一个特定控制算法，而是为了说明：

1. `OpenModelica` 导出的房屋热模型可以直接变成 `FMU`；
2. `UPPAAL` 写的 bang-bang controller 也可以导出或保留为原生 timed automata；
3. weather、controller、houses 组合后，可以直接在 `UPPAAL SMC` 里做：
   - simulation
   - estimation
   - statistical model checking

作者具体展示了：

1. 七天温度轨迹仿真；
2. 各房间最小/最大温度的期望估计；
3. `Pr[<=T](...)` 风格的统计性质；
4. bounded `MITL` 性质，例如“温度降到阈值以下后两小时内能否恢复”。

这表明方法已经不只是“支持导入”，而是能真正复用 `UPPAAL SMC` 的分析栈。

## 解决了什么问题

这篇论文解决的关键问题，是把 `FMU` 级异构组件真正纳入 `UPPAAL SMC` 的 formal analysis loop。

第一，它让 `UPPAAL` 不再局限于原生 automata 模型，而可以直接接 OpenModelica / Matlab 等外部工具导出的 `FMU`。

第二，它给出了一套 explicit master algorithm 语义，而不是把 host behavior 隐藏在工具外部。这样，组合系统的仿真与统计验证结果是可以追溯到 automata semantics 的。

第三，它通过随机化 transfer 和 0-delay 处理，把 interleaving 相关的行为差异重新纳入 `SMC` 可观察范围，而不是粗暴地被某个宿主固定顺序吞掉。

第四，它为后续 `UPPAAL Stratego`、`Uppaal Tiga` 对异构系统的合成/优化打开了接口，因为外部模型现在已经能在 `UPPAAL` 里被逐步驱动。

## 与 `UPPAAL` 技术线的关系

这篇论文与 `UPPAAL` 技术线的关系非常明确：

1. 它直接建立在 `UPPAAL SMC` 的概率/统计语义之上；
2. 它承接 [bogomolov15-cosimulation-hybrid-systems-spaceex-uppaal](./../bogomolov15-cosimulation-hybrid-systems-spaceex-uppaal/) 的 `FMI` 协同线，但把 `UPPAAL` 从从属组件提升为 host/master；
3. 它又显式把成果指向 `UPPAAL STRATEGO` 和 classical `UPPAAL`，说明这不是一次性的 `SMC` 特化 hack，而是更 general 的平台扩展。

在文库时间线中，它因此非常适合放在“`SMC/Stratego` 走向异构协同建模”的节点上看。

## 实现与材料

从内容详细程度看，这篇论文适合标 `🟩 较完整`。它把：

1. 外部库调用规则；
2. `FMU`/STA 语义桥接；
3. master algorithm 状态机；
4. 案例与 query 结果；

都写得比较充分。

从实现可获取程度看，更适合标 `🟧 仅可执行/可使用版本可得`：

1. 论文明确提供了扩展版 `UPPAAL SMC`、案例 `FMU` 和原型工具压缩包；
2. 这让能力可试用、可复现实验；
3. 但目前没有稳定可维护的公开源码仓库直接对应这篇论文整套实现。

因此按本库严格标准，它仍属于“可运行能力可得，但源码线不清晰”。

## 对本研究的启发

这篇论文对当前博士研究的启发非常直接。

第一，它说明 formal method 工具若要真正进入工程工作流，关键不是把所有外部模型重写，而是把接口层做成**语义上可控的内嵌对象**。这和你后续要把 LLM 生成、验证、修复串成闭环的方向非常一致。

第二，作者没有满足于“能连通就行”，而是专门讨论 interleaving、statelessness、determinism 这些语义条件。这提醒我们：异构模块接入 formal workflow 时，最容易被忽略的恰恰是语义边界。

第三，它还表明 `UPPAAL` 这条技术线在 `2010s` 后期并没有停在纯 timed automata 理论，而是在持续推进平台互操作与更大分析生态的整合。这对继续沿 `SMC / Stratego / FMI` 方向扩库非常重要。
