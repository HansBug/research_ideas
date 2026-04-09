# 关于混成自动机，什么是可判定的？ / What's Decidable About Hybrid Automata?

## 基本信息

- 标题：What's Decidable About Hybrid Automata?
- 中文标题：关于混成自动机，什么是可判定的？
- 作者：Thomas A. Henzinger, Peter W. Kopke, Anuj Puri, Pravin Varaiya
- 发表：*Journal of Computer and System Sciences*, 57(1):94-124, 1998
- DOI：`10.1006/jcss.1998.1581`
- 链接：https://doi.org/10.1006/jcss.1998.1581
- 形式主义：`Initialized Rectangular Automata / Decidable Hybrid-Automata Boundary`
- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：分支整理
- 工具/实现获取方式：原文以 `HyTech` 可终止性和到 timed automata 的翻译为主要工程入口，但未提供仓库下载。
- 标准/格式获取方式：原文没有交换标准，核心承载方式是 rectangular automaton tuple、zone semantics、`Pre/Post/Reach` 算子和 initialized 条件。

## 简报

这篇论文不是泛泛讨论 hybrid verification，而是把 `Hybrid Automata` 主干附近“到底哪些子类可判定，哪些一放松就不可判定”这条边界系统化地画出来。它定义 rectangular automata、initialized rectangular automata、stopwatch automata、bounded nondeterminism 等子类，证明 initialized rectangular reachability 是 `PSPACE`-complete，同时指出只要破坏 rectangularity 或 initialization，甚至给 timed automata 加一个 uninitialized stopwatch，reachability 就会变成不可判定。对演化树来说，它最适合在 `Hybrid Automata` 下补出 `Initialized Rectangular Automata` 这一理论分支节点。

- 形式主义定位：`Hybrid Automata` 主干上的 decidable-subclass / boundary-classification 条目，核心节点是 initialized rectangular automata。
- 构造方式简述：用矩形 init/inv/flow/pre/post 区域和 jump 集合定义 hybrid state transitions，再用 initialization 约束把“流改变时是否重初始化”显式钉住。
- 基础设施与场景简述：理论上通过到 timed automata / singular automata 的翻译和 `Pre/Post/Reach` 分析给出 `PSPACE` 边界，工程上可解释 `HyTech` 为什么在 initialized rectangular 类上会终止。

```text
Hybrid Automata -> Rectangular Automata -> Initialized Rectangular Automata -> PSPACE reachability / undecidability boundary
```

## 形式主义定义与核心对象

### 定义对象

论文研究的是带实值变量的 rectangular automata 及其 initialized / bounded-nondeterministic / stopwatch 等子类。它们仍然是 hybrid automata，但所有连续约束都被限制成坐标轴对齐的矩形区间。

### 核心抽象

按原文 Section 2，可把一个 `n` 维 rectangular automaton 写成：

$$
A = (V,E,\Upsilon,\mathrm{init},\mathrm{inv},\mathrm{flow},\mathrm{pre},\mathrm{post},\mathrm{jump},\mathrm{obs})
$$

上式中的符号逐项解释如下：

1. `(V,E)` 是有限有向 multigraph。
2. `\Upsilon` 是 observation alphabet。
3. `\mathrm{init},\mathrm{inv},\mathrm{flow}:V\to \mathcal R^n` 给每个顶点标注初始区、状态不变区和导数区间。
4. `\mathrm{pre},\mathrm{post}:E\to \mathcal R^n` 给每条边标注 preguard 和 postguard 矩形区。
5. `\mathrm{jump}:E\to 2^{\{1,\ldots,n\}}` 指定哪些坐标在该边上可被重赋值。
6. `\mathrm{obs}:E\to\Upsilon` 或 `\Upsilon_=` 给边打观测标签。
7. `\mathcal R^n` 是 `\mathbb R^n` 上所有矩形区域的集合。

系统状态是：

$$
(v,x)\in V\times \mathbb R^n,\quad x\in \mathrm{inv}(v)
$$

### 一个最小例子与通俗解释

最小例子可以取一个 stopwatch 变量 `c`：在 `Run` 位置有 `\dot c=1`，在 `Pause` 位置有 `\dot c=0`。如果每次 `Run/Pause` 切换时，只要 `\dot c` 的速率变了就把 `c` 加入 `\mathrm{jump}(e)` 并按 `\mathrm{post}(e)` 重初始化，那么这是 initialized 风格；如果速率变了却保留旧值，则变成 uninitialized stopwatch，这正是论文指出会触发不可判定边界的危险点。

通俗地说，initialized rectangular automaton 的关键纪律是：“只要某个连续变量换了一套流速规则，就先把它重置到 post 区间里，再继续跑”。这条纪律看起来很苛刻，但它正是保住可判定性的核心。

### 运行 / 接受 / 转移语义

边跳转语义可写成：

$$
(v,x)\xrightarrow{\sigma}(w,y) \iff \exists e=(v,w),\ \mathrm{obs}(e)=\sigma,\ x\in\mathrm{pre}(e),\ y\in\mathrm{post}(e),\ \forall i\notin\mathrm{jump}(e),\ y_i=x_i
$$

时间流逝语义可写成：

$$
(v,x)\xrightarrow{t}(v,y) \iff t\ge 0,\ (y-x)/t \in \mathrm{flow}(v),\ \text{and the trajectory stays in }\mathrm{inv}(v)
$$

initialized 条件是：

$$
\forall e=(v,w)\in E,\ \forall i,\ \mathrm{flow}(v)_i\neq \mathrm{flow}(w)_i \Rightarrow i\in\mathrm{jump}(e)
$$

这条式子中的含义是：只要某个坐标在边两端的流区间变了，该坐标就必须在这条边上被重初始化。

### 语义边界

如果把矩形区换成一般线性区，就回到 linear hybrid automata；如果所有变量都是 deterministic jumps 的 clocks，则得到 timed automata；如果变量只在 `1/0` 两种速率间切换，则得到 stopwatch automata。

### 关键性质与判定边界

论文最重要的正结论是：

$$
\text{Reachability for initialized rectangular automata is PSPACE-complete}
$$

并且对 bounded nondeterminism 下的 `\omega`-language emptiness 也能得到 `PSPACE` 结果。更强一点，initialized stopwatch automata 还能多项式编码到 timed automata：

$$
\mathrm{Reach}(C)=\mathrm{proj}(\mathrm{Reach}(D_C)),\quad \mathrm{Lang}(C)=\mathrm{Lang}(D_C)
$$

另一方面，负结论同样锋利：

$$
\text{Reachability is undecidable for simple rectangular automata with one two-slope variable}
$$

其中 stopwatch 就是 slopes `1` 和 `0` 的 two-slope variable。原文总结说，decidability 的两个关键因素正是 rectangularity 和 initialization。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 有限顶点 `V` 是离散控制骨架。 |
| 事件 / 触发 | 支持 | 边带 observation label，既可离散跳转也可 `=` 隐式步。 |
| 守卫 / 数据 | 强支持 | `init/inv/flow/pre/post/jump` 都直接约束连续状态与重置。 |
| 层次 | 不支持 | 原始模型不是层次混成自动机。 |
| 并发 / 同步 | 部分支持 | 论文重点是单体子类边界，不是组合语义。 |
| 时间约束 | 强支持 | 时间标签 `t\in\mathbb R_{\ge 0}` 与 flow/invariant 一起定义演化。 |
| 连续动态 / 随机性 | 强支持连续、无随机 | 连续变量按矩形导数区间非确定性演化。 |
| 可执行 / 可验证性 | 强理论支持 | initialized rectangular reachability 可判定且 `PSPACE`，但 uninitialized / nonrectangular 很快不可判定。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| rectangular automaton | `$A=(V,E,\Upsilon,\mathrm{init},\mathrm{inv},\mathrm{flow},\mathrm{pre},\mathrm{post},\mathrm{jump},\mathrm{obs})$` | 定义坐标解耦的混成子类。 |
| initialized 条件 | `$\mathrm{flow}(v)_i\neq\mathrm{flow}(w)_i \Rightarrow i\in\mathrm{jump}(e)$` | 流改变时必须重初始化该变量。 |
| stopwatch | `$k_1=1,\ k_2=0$` | two-slope 变量的暂停时钟特例。 |
| 正结论 | `$\text{Reachability} \in \text{PSPACE-complete}$ for initialized rectangular` | 保留可判定性且无复杂度惩罚。 |
| 负结论 | `$\text{Reachability}$ undecidable for one uninitialized two-slope variable` | 极小放松就越过可判定边界。 |

## 构造方式与承载格式

### 建模入口

1. 先确认连续约束能否写成每维独立区间，也就是 rectangular regions。
2. 为每个顶点定义 `init/inv/flow`，为每条边定义 `pre/post/jump/obs`。
3. 检查所有“流速变化边”是否满足 initialized 条件。
4. 若想落入可判定区，优先约束到 initialized rectangular / initialized stopwatch。

### 机器可处理承载方式

机器可处理承载方式是 rectangular zones、`Pre/Post/Reach` 运算、到 timed automata 或 singular automata 的翻译，以及 `HyTech` 风格符号可达性。

### 交换与互操作

它和 [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md) 的上位 hybrid 定义、[a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md) 的 timed 子类，以及现有 `Stopwatch Automata` / `Parametric Stopwatch Automata` 支线直接互操作。

## 配套基础设施

- 建模/编辑工具：论文多次以 `HyTech` 可终止性作为实践背景，但未提供独立下载入口。
- 解析/交换/元模型支持：核心是 rectangular automaton tuple 和 zone-based symbolic operators。
- 仿真/执行支持：可按边跳转和时间步构成无限状态 LTS。
- 验证/分析支持：initialized rectangular reachability、`\omega`-language emptiness、timed translation、simulation/bisimulation 和不可判定性构造。
- 代码生成/转换支持：可翻译到 timed automata / singular automata，但原文不是代码生成论文。
- 标准化或社区生态：是 hybrid automata decidability boundary 和 `HyTech` 终止性讨论的经典母文献之一。

## 适用场景与需求前提

### 适用场景

适合 bounded-drift clock protocols、rectangular differential inclusion、hybrid decidability classification，以及需要先判断“这个混成需求还能不能落入可判定子类”的建模预筛。

### 需求前提

1. 连续变量约束最好能按坐标解耦成矩形区间。
2. 如果希望保可判定，流变化边必须满足重初始化纪律。
3. 若模型含 uninitialized stopwatch 或跨维耦合线性区，就要接受不可判定风险。

### 不适用或高成本场景

对强耦合非矩形动力学、连续流不易分解的 CPS、或需要复杂层次组合语言的场景，rectangular/initialized 约束会过紧。

## 与相邻形式主义的关系

相对 [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md)，本文不是再定义一般 `HA`，而是系统划分其可判定子类边界；相对 [the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md)，本文更集中于 `initialized rectangular` 这一最大可判定带；相对 `Stopwatch Automata` 应用条目，本文给的是一根理论边界线，而不是某个工程案例。

## 与本研究的关系

### 对 Project 1 的价值

它为 `Hybrid Automata` 主干补出了一个极关键的“可判定边界子类节点”——`Initialized Rectangular Automata`，这比继续堆 hybrid 应用条目更能直接扩演化树。

### 作为目标形式主义还是中间表示

更适合作为“混成目标模型是否可继续验证/修复”的理论筛选层；若 LLM 生成了过强的 hybrid model，可用本文边界反向指导降阶到 initialized rectangular / timed 子类。

### 对需求到模型生成的启发

自然语言里如果出现“时钟漂移在区间内变化，但一旦模式切换就重新校准”这类句式，就非常适合直接抽成 initialized rectangular automata；如果出现“暂停后保留旧 stopwatch 值且流速改变”，则应立刻标记为可能越过可判定边界。

### 现实限制

原文没有工程文件格式；并且为了保可判定而要求 rectangularity + initialization，这对真实物理模型可能偏保守。

## 重要的相关工作

### 奠基或前身工作

- [hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md](../hybrid-automata-an-algorithmic-approach-to-the-specification-and-verification-of-hybrid-systems/desc.md)
- [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)

### 同类型或同家族工作

- [the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md)
- `Stopwatch Automata`
- `Integration Graphs`

### 标准 / 格式 / 工具链工作

- `HyTech`

### 与本研究关系最紧的工作

- 它最适合作为 `Hybrid Automata -> Initialized Rectangular Automata` 的文库代表条目，并直接服务“生成后判断是否还能验证”的模型选择逻辑。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 形式主义：`Initialized Rectangular Automata / Decidable Hybrid-Automata Boundary`
- 论文角色：分支整理
- 核心功能：系统划分 rectangular / initialized / stopwatch 等 hybrid 子类的可判定边界，并证明 initialized rectangular reachability 为 `PSPACE`-complete。
- 关键特性：rectangular zones、initialization discipline、timed translation、bounded nondeterminism、single-stopwatch undecidability。
- 构造方式：有限图 + `init/inv/flow/pre/post/jump/obs` 矩形标注 + zone/LTS 语义。
- 基础设施：`HyTech` 风格符号分析与到 timed automata 的翻译最关键，但无独立标准格式。
- 适用场景：bounded-drift 协议、rectangular hybrid modeling、混成模型可判定性预筛。
- 需求前提：连续变量需满足坐标解耦矩形约束，且希望保可判定时必须满足“流变则重初始化”。
- 状态：🟢
