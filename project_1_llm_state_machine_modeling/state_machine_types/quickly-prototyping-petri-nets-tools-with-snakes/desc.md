# SNAKES：快速原型化 Petri 网工具 / Quickly prototyping Petri nets tools with SNAKES

## 基本信息

- 标题：Quickly prototyping Petri nets tools with SNAKES
- 中文标题：SNAKES：快速原型化 Petri 网工具
- 作者：Franck Pommereau
- 发表：*Proceedings of the First International ICST Conference on Simulation Tools and Techniques for Communications, Networks and Systems*，2008
- DOI：`10.4108/ICST.SIMUTOOLS2008.3007`
- 链接：https://doi.org/10.4108/ICST.SIMUTOOLS2008.3007
- 形式主义：`General Petri Net core library / SNAKES`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 论文角色：general Petri-net prototyping library + plugin framework
- 工具/实现获取方式：原文明确给出 `SNAKES` 下载入口，并说明其以 `GNU LGPL` 发布；当前公开入口可由论文中的项目地址与 HAL 镜像追溯。
- 标准/格式获取方式：核心承载方式是 `Python` API、plugin modules 与 `PNML` import/export；除 `PNML` 外无额外中立交换标准。

## 简报

这篇论文的价值不在于提出一种新的 Petri 网，而在于把“快速试一种新的 Petri 网变体并立刻写工具”这件事做成了一套通用库。`SNAKES` 把 Petri 网压成一个尽量少内建限制的 core library，再通过 Python plugin 机制去长出 read arcs、PBC/M-nets 操作、Graphviz 可视化、data plugins 等扩展。

- 形式主义定位：广义 Petri 网原型化基础设施，而不是单一网类的专用工具。
- 构造方式简述：`Python` core library 表达 places/transitions/arcs/types/markings，再通过 plugin system 增量扩展模型与算法。
- 基础设施与场景简述：依托 general Petri-net skeleton、arbitrary Python inscriptions、plugin loading、`PNML` support 与 Graphviz/export，服务新网类试验、语义原型化和快速工具搭建。

```text
Petri-net idea -> SNAKES core library -> plugin extension -> prototype tool / semantics experiment / PNML exchange
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织 `SNAKES`：

1. places、transitions、arcs、nets、markings、reachability graphs 等 core classes。
2. place types、transition guards、arc annotations。
3. arbitrary Python objects 作为 tokens。
4. plugin-based extensions。
5. `PNML` import/export。

### 核心抽象

结合论文对 core library 的说明，可把 `SNAKES` 中一张网保守写成：

$$
N = (P, T, F, \Sigma, G, \Lambda)
$$

上式中的符号逐项解释如下：

1. `P` 是 places 集合。
2. `T` 是 transitions 集合。
3. `F` 是 arcs 及其方向关系。
4. `\Sigma` 是 places 的 type constraints。
5. `G` 是 transitions 的 guards。
6. `\Lambda` 是 arc annotations，包括 values、variables、expressions、multi-arcs、test arcs 等。

论文把 enabling binding 讲得很清楚，可保守整理为：

$$
\mathrm{Enabled}(t, M) = \{ \beta \mid pre_t[\beta] \subseteq M,\ G_t(\beta)=\mathrm{true},\ post_t[\beta]\ \text{is well-typed} \}
$$

上式中的符号逐项解释如下：

1. `t` 是某个 transition。
2. `M` 是当前 marking。
3. `\beta` 是变量绑定。
4. `pre_t[\beta]` 表示输入弧在绑定 `\beta` 下要求消费的 tokens。
5. `G_t(\beta)` 是 guard 在环境 `\beta` 下的求值结果。
6. `post_t[\beta]` 是输出弧在环境 `\beta` 下生成的 tokens。

### 一个最小例子与通俗解释

论文给出的 simplest running example 很直观：

1. `p1` 里有整数 token。
2. transition `t` 的 guard 是 `x > 0`。
3. 输入弧把 token 绑定到变量 `x`。
4. 输出弧写成表达式 `x + 1`，把结果放到 `p2`。

通俗地说，`SNAKES` 把 Petri 网做成了“带 Python 表达式的可编程网骨架”。你不必先等某种网类的官方工具出现，就能先把 token、guards 和算法原型写起来。

### 运行 / 接受 / 转移语义

论文明确说明 transition firing 按 coloured-net 风格执行：

$$
(N, M) \xrightarrow{t,\beta} (N, M')
$$

其中：

1. 先找到 enabling binding `\beta`。
2. 再消费 `pre_t[\beta]` 中要求的 tokens。
3. 最后把 `post_t[\beta]` 生成的 tokens 放到输出库所，并检查类型约束。

对 place typing，论文还强调 type 本身可以是任意 Python Boolean function，因此可写成：

$$
\forall p \in P,\ \forall m \in M(p),\ \Sigma_p(m) = \mathrm{true}
$$

上式中的符号逐项解释如下：

1. `\Sigma_p` 是 place `p` 的类型谓词。
2. `M(p)` 是 `p` 中当前 tokens。
3. 每个 token 都必须被对应 place type 接受。

### 语义边界

这篇论文也明确承认：

1. `SNAKES` 目标是快速原型，不是高性能执行引擎。
2. 它故意把性能让位给一般性和灵活性。
3. 很多 use cases 是先在 `SNAKES` 中构造网，再导向专用验证器。
4. 因为依赖 Python，工程部署和极致性能都不是它的主战场。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 网骨架 | `$N = (P, T, F, \Sigma, G, \Lambda)$` | `SNAKES` 把一般 Petri 网抽成 core library。 |
| enabling binding | `$\mathrm{Enabled}(t, M) = \{ \beta \mid pre_t[\beta] \subseteq M,\ G_t(\beta)=\mathrm{true},\ post_t[\beta]\ \text{well-typed} \}$` | 绑定、守卫与 place typing 一起决定 transition 是否可发射。 |
| firing 语义 | `$(N, M) \xrightarrow{t,\beta} (N, M')$` | 采用 coloured-net 风格执行。 |
| place typing | `$\forall p,\forall m\in M(p),\ \Sigma_p(m)=\mathrm{true}$` | place type 是运行时约束的一部分。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | Petri 网没有状态机式 mode，但 marking 与 transition skeleton 很明确。 |
| 事件 / 触发 | 中等支持 | 主要通过 transition enabling/firing 表达。 |
| 守卫 / 数据 | 很强 | Python guards、arbitrary tokens、typed places 都是一等能力。 |
| 层次 | 弱支持 | 主体不是 hierarchy，而是 general core + plugins。 |
| 并发 / 同步 | 很强 | Petri 网的 token-flow / concurrency 是主线。 |
| 时间约束 | 可扩展 | 核心库不固定某种 timed net，但 plugin 可加。 |
| 连续动态 / 随机性 | 核心不支持 | 需靠变体或插件扩展。 |
| 可执行 / 可验证性 | 很强 | 可执行、可导出、可做快速算法原型。 |

### 形式化问题与性质

1. `SNAKES` 的目标不是替代所有 Petri 网工具，而是降低“试新网类和新算法”的门槛。
2. plugin 机制让模型变体不必通过修改 core library 来实现。
3. `PNML` 支持意味着它不只是程序库，也能承担一定的交换与持久化角色。

## 构造方式与承载格式

### 建模入口

论文中的典型入口是：

1. 用 `snakes.nets` 定 place、transition、arcs、types。
2. 用 guards、variables、expressions 写 inscriptions。
3. 视需要加载 plugins。
4. 执行、导出或把结果交给专用工具继续分析。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `Python` API。
2. core modules：`snakes.data`、`snakes.typing`、`snakes.nets`、`snakes.plugins`。
3. plugin extensions。
4. `PNML` import/export。

### 交换与互操作

这篇论文的互操作重点在于：

1. `PNML` 导入导出。
2. plugin load chain 允许不同扩展叠加。
3. 许多原型流程是“在 `SNAKES` 构网，再导向别的专用验证器”。

## 配套基础设施

- 建模/编辑工具：以 `Python` 编程接口为主；无强图形前端。
- 解析/交换/元模型支持：`PNML` import/export。
- 仿真/执行支持：可执行一般 Petri 网与其变体，适合 simulation/prototyping。
- 验证/分析支持：可生成 reachability graph，也适合作为外部分析器前端。
- 代码生成/转换支持：不是代码生成框架，但便于写 translator/prototype plugins。
- 标准化或社区生态：`GNU LGPL`、`Python`、Graphviz plugin 与 `PNML` 共同构成主要生态。

## 适用场景与需求前提

### 适用场景

适合新 Petri 网变体、网语义实验、快速算法原型、教学和研究型工具开发。

### 需求前提

1. 团队能接受以 `Python` 编程方式操纵网模型。
2. 当前目标更偏原型验证和研究试错，而不是极限性能。
3. 需要的是 general Petri-net infrastructure，而不是固定单一网类工具。
4. 若后续要高性能验证，通常还需要接专用后端。

### 不适用或高成本场景

如果目标是工业级大规模 Petri 网高性能求解，`SNAKES` 本身会偏慢，往往更适合作为前端原型层。

## 与相邻形式主义的关系

相对 [renew-the-reference-net-workshop/desc.md](../renew-the-reference-net-workshop/desc.md)，`Renew` 面向 reference nets IDE 与执行环境，而 `SNAKES` 面向 general Petri-net prototyping library；相对 [pipe-plus-a-modeling-tool-for-high-level-petri-nets/desc.md](../pipe-plus-a-modeling-tool-for-high-level-petri-nets/desc.md)，`PIPE+` 是固定网类工具，而 `SNAKES` 主打低限制 core + plugin extensibility；相对 [the-greatspn-tool-recent-enhancements/desc.md](../the-greatspn-tool-recent-enhancements/desc.md)，`GreatSPN` 强在成熟分析，`SNAKES` 强在快速原型化。

## 与本研究的关系

### 对 Project 1 的价值

它说明如果 `project_1` 后续需要快速试验新的状态机/Petri 混合表示、翻译器或中间检查器，不一定要一开始就做重型工具，可以先用 general library 快速打样。

### 作为目标形式主义还是中间表示

它本身更像工具基础设施，而不是最终目标形式主义；更适合作为实验性中间表示与原型支撑层。

### 对需求到模型生成的启发

1. 若未来需要频繁试不同网类或状态机扩展，plugin-friendly infrastructure 很重要。
2. token、type、guard 和 arc annotation 最好在核心层就留有扩展口。
3. `PNML` 一类交换能力能显著降低后续工具桥接成本。

### 现实限制

`SNAKES` 强在灵活性，不强在工业级性能和大规模求解。

## 重要的相关工作

- [renew-the-reference-net-workshop/desc.md](../renew-the-reference-net-workshop/desc.md)：reference nets IDE 与 plugin environment。
- [pipe-plus-a-modeling-tool-for-high-level-petri-nets/desc.md](../pipe-plus-a-modeling-tool-for-high-level-petri-nets/desc.md)：高层 Petri 网工具。
- [the-greatspn-tool-recent-enhancements/desc.md](../the-greatspn-tool-recent-enhancements/desc.md)：成熟随机/高层 Petri 网分析环境。
- [pn-standardisation-survey/survey.md](../pn-standardisation-survey/survey.md)：Petri 网标准化与交换格式总览。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：💻 软件建模与程序行为
- 形式主义：`General Petri Net core library / SNAKES`
- 论文角色：general Petri-net prototyping library + plugin framework
