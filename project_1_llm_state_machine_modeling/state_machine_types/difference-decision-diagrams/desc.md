# 差分决策图：面向时间系统的差分约束符号结构 / Difference Decision Diagrams

## 基本信息

- 标题：Difference Decision Diagrams
- 中文标题：差分决策图：面向时间系统的差分约束符号结构
- 作者：Jesper Møller，Jakob Lichtenberg，Henrik Reif Andersen，Henrik Hulgaard
- 发表：*Computer Science Logic*，pp. 111-125，1999
- DOI：`10.1007/3-540-48168-0_9`
- 链接：https://doi.org/10.1007/3-540-48168-0_9
- 形式主义：`Difference Decision Diagrams / DDD / ODDD / RPDDD`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：面向 `Timed Automata / Timed Petri Nets` 的差分约束符号表示底座
- 工具/实现获取方式：原文重点给出数据结构与操作算法，没有提供独立可下载工具或公开仓库。
- 标准/格式获取方式：它不是交换标准，核心承载是内存中的 decision-diagram 结构，节点测试条件为差分约束 `x-y<c` 或 `x-y\le c`。

## 简报

这篇论文补的不是一个新的状态机前端，而是实时状态机后端里非常关键的一层“差分约束表示结构”。`DDD` 把 `x-y<c`、`x-y\le c` 这类时间差分约束做成类似 `ROBDD` 的判定图，使带时钟的状态集合和时序关系可以共享子结构、表示非凸集合，并对 tautology、satisfiability、equivalence 这类问题做高效判断。

- 形式主义定位：实时系统 symbolic verification 的底层表示，不是新的建模语言。
- 构造方式简述：把差分约束表达式拆成 decision tree，每个非终端节点测试一个差分约束，high/low 分支分别表示约束为真或假。
- 基础设施与场景简述：服务 `Timed Automata`、`Timed Petri Nets` 等需要大量操作 difference constraints 的验证器，特别适合比较 `DBM` 难以自然共享的非凸状态集合。

```text
timed-system states / clock relations -> difference constraints -> DDD / ODDD / RPDDD -> symbolic manipulation / satisfiability / equivalence checks
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. difference constraint expressions；
2. `DDD` 节点与 high/low 分支语义；
3. ordered DDD；
4. locally reduced DDD；
5. path-reduced DDD 与 semi-canonical 表示。

### 核心抽象

根据论文给出的 grammar，可把其差分约束逻辑保守整理为：

$$
\phi ::= x-y<c \mid x-y\le c \mid \neg \phi \mid \phi \land \phi \mid \phi \lor \phi \mid \exists x.\phi \mid \forall x.\phi
$$

上式中的符号逐项解释如下：

1. `$x,y$` 是整数或实数变量，典型地对应系统中的 clocks 或其他数值变量。
2. `$c$` 是常数。
3. `$x-y<c$` 与 `$x-y\le c$` 是最基本的 difference constraints。
4. `$\neg,\land,\lor$` 是布尔组合。
5. `$\exists x,\forall x$` 表示论文讨论的量化操作。

对一个非终端 `DDD` 节点 `$v$`，其测试条件记为 `$c_v$`，高分支记为 `$hi(v)$`，低分支记为 `$lo(v)$`。其布尔语义可整理为：

$$
\llbracket v \rrbracket = (c_v \land \llbracket hi(v) \rrbracket) \lor (\neg c_v \land \llbracket lo(v) \rrbracket)
$$

上式中的符号逐项解释如下：

1. `$\llbracket v \rrbracket$` 是节点 `$v$` 所表示的差分约束表达式。
2. `$c_v$` 是该节点当前要测试的 difference constraint。
3. `$hi(v)$` 是当 `$c_v$` 为真时继续访问的子图。
4. `$lo(v)$` 是当 `$c_v$` 为假时继续访问的子图。
5. 终端 `1` 与 `0` 分别表示 tautology 与 unsatisfiable expression。

论文进一步引入 ordered DDD。可保守写成：若 `$attr(v)$` 表示节点的测试属性，则 ordered DDD 要求沿任一路径满足全序约束

$$
attr(v_1) < attr(v_2) < \cdots < attr(v_k)
$$

上式中的符号逐项解释如下：

1. `$v_1,\ldots,v_k$` 是同一路径上的非终端节点。
2. `$attr(v_i)$` 是对应约束的变量对、比较符和边界三元属性。
3. 全序约束保证可以复用 `BDD` 风格的 `APPLY` 思路。

### 一个最小例子与通俗解释

可以把两个时钟 `$x,y$` 的关系写成：

$$
\phi = (x-y\le 3) \land (y-x<2)
$$

上式中的符号逐项解释如下：

1. `$x-y\le 3$` 表示时钟 `$x$` 最多比 `$y$` 大 `3`。
2. `$y-x<2$` 表示时钟 `$y$` 不能比 `$x$` 超前 `2` 或更多。
3. 合起来它描述的是两个时钟之间允许的相对偏差区间。

对应到 `DDD` 上，可以先测试 `$x-y\le 3$`，为真时继续测试 `$y-x<2$`，否则直接走向 `0`。通俗地说，`DDD` 像是把“时间差约束的判定过程”做成可共享子图的决策树。和把整个约束集硬塞进一张矩阵相比，它更适合表达“很多约束分支共享同一后缀条件”的情况。

### 运行 / 接受 / 转移语义

一条从根到终端 `1` 的路径对应一个差分约束系统。若路径 `$p$` 上诱导出的约束集记为 `$\Delta(p)$`，则该路径可行当且仅当：

$$
\exists \nu.\ \nu \models \bigwedge_{d \in \Delta(p)} d
$$

上式中的符号逐项解释如下：

1. `$\nu$` 是对全部变量的赋值。
2. `$\Delta(p)$` 是路径 `$p$` 上收集到的约束集合。
3. `$d$` 是其中一条 difference constraint。
4. 若存在赋值同时满足这些约束，则该路径是 feasible path。

论文定义 path-reduced DDD 的核心目标，就是删掉所有 infeasible paths。于是一个 path-reduced DDD 的终端语义可以概括为：

$$
\text{RPDDD}(\phi)=1 \iff \phi \text{ is a tautology}, \qquad
\text{RPDDD}(\phi)=0 \iff \phi \text{ is unsatisfiable}
$$

上式中的符号逐项解释如下：

1. `$\text{RPDDD}(\phi)$` 表示表达式 `$\phi$` 的 path-reduced 表示。
2. 终端 `1` 唯一对应 tautology。
3. 终端 `0` 唯一对应 unsatisfiable expression。
4. 这是论文给出的 semi-canonical 性质。

### 语义边界

1. `DDD` 主打的是 difference constraints，而不是任意线性或非线性约束。
2. 其 ordered 版本能借用 `BDD` 风格算法，但 existential quantification 为维持 orderedness 可能带来指数代价。
3. path-reduced 只做到 semi-canonical，不等于完全 canonical。
4. 它是表示层基础设施，不直接负责系统建模、仿真或代码生成。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 差分约束逻辑 | `$\phi ::= x-y<c \mid x-y\le c \mid \neg\phi \mid \phi\land\phi \mid \phi\lor\phi \mid \exists x.\phi \mid \forall x.\phi$` | `DDD` 所操作的基本对象。 |
| 节点语义 | `$\llbracket v \rrbracket = (c_v \land \llbracket hi(v) \rrbracket) \lor (\neg c_v \land \llbracket lo(v) \rrbracket)$` | `DDD` 的布尔决策图解释。 |
| 路径可行性 | `$\exists \nu.\ \nu \models \bigwedge_{d\in\Delta(p)} d$` | infeasible-path elimination 的依据。 |
| semi-canonical 性质 | `$\text{RPDDD}(\phi)=1 \iff \phi$ tautology` | path-reduced 后可常数时间判 tautology / unsat。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 间接支持 | 不定义状态机本体，但可表示带时钟状态集合。 |
| 事件 / 触发 | 不直接支持 | 事件语义来自上层 `Timed Automata / Petri Net`。 |
| 守卫 / 数据 | 很强 | 专门针对差分守卫 `x-y<c` / `x-y\le c`。 |
| 层次 | 不支持 | 不是层次状态机语言。 |
| 并发 / 同步 | 间接支持 | 可服务并发 timed models，但并发语义不在 `DDD` 本体里。 |
| 时间约束 | 很强 | 论文动机就是时间系统 symbolic verification。 |
| 连续动态 / 随机性 | 不支持 | 只处理差分约束逻辑。 |
| 可执行 / 可验证性 | 很强 | `APPLY`、reduction、satisfiability / equivalence 都可算法化。 |

### 形式化问题与性质

1. `DDD` 解决的是“怎样表示与操纵 difference constraints”，不是“怎样定义新的 timed automaton 家族”。
2. 相比 `DBM` 一类以凸区为中心的表示，`DDD` 强在共享子结构和表达非凸布尔组合。
3. 对 `Timed Automata / Timed Petri Nets` 来说，它更像 symbolic backend building block。

## 构造方式与承载格式

### 建模入口

典型入口不是图形建模器，而是：

1. 从 timed model 中收集差分守卫与不变式；
2. 把它们写成 difference constraint expressions；
3. 再构造为 `DDD` / `ODDD` / `RPDDD`。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 终端 `0/1`；
2. 非终端节点上的 difference constraint test；
3. high / low branches；
4. orderedness、local reduction、path reduction 等规范化条件。

### 交换与互操作

它没有独立交换标准，互操作主要体现在：

1. 上游 timed models 把 guard / invariant 下降为差分约束；
2. 下游 symbolic verification 算法在 `DDD` 上做布尔操作、量化和化简；
3. 可与 Boolean variables 混合表示，从而把布尔与时间条件放进同一结构。

## 配套基础设施

- 建模/编辑工具：原文未提供单独建模器，重点在符号数据结构。
- 解析/交换/元模型支持：无独立 schema；承载是内存中的 decision diagram。
- 仿真/执行支持：不提供运行时执行。
- 验证/分析支持：支持 `APPLY`、local reduction、path reduction、tautology / satisfiability / equivalence checking。
- 代码生成/转换支持：原文未涉及。
- 标准化或社区生态：不是行业标准；价值主要在 timed verification backends 的实现层。

## 适用场景与需求前提

### 适用场景

适合以下场景：

1. `Timed Automata`、`Timed Petri Nets` 的 symbolic state-space representation；
2. 需要频繁布尔组合差分约束、并保留共享子结构的验证器实现；
3. 需要表示非凸 clock constraints 的后端。

### 需求前提

1. 时序约束最好主要是 difference constraints，而不是一般非线性约束。
2. 验证器愿意用 decision-diagram 风格结构而不是纯矩阵表示。
3. 目标是符号分析，而不是前端建模体验。

### 不适用或高成本场景

若系统主要依赖一般线性规划、混成连续动力学或概率语义，`DDD` 只能覆盖其中的差分约束子问题，不能直接充当整体形式主义。

## 与相邻形式主义的关系

相对 [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)，`UPPAAL` 主打 `Timed Automata` 平台与 `DBM/zone` 路线，而 `DDD` 更像另一种差分约束符号底层；相对 [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)，`TINA` 面向 `TPN` 工具链，而 `DDD` 是可被此类工具借鉴的数据结构思路；相对 [fortuna-model-checking-priced-probabilistic-timed-automata/desc.md](../fortuna-model-checking-priced-probabilistic-timed-automata/desc.md)，`FORTUNA` 使用 multi-priced zones 做概率代价实时分析，而 `DDD` 提供的是更底层的差分约束判定图表示。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提醒我们“状态机类型谱系”不只看前端语言，还要看支撑这些语言可验证的约束表示层。
2. 若未来 `project_1` 需要把时间需求转成可验证模型，差分约束的数据结构选择会直接影响后端效率。
3. 对“生成-验证-修复”闭环来说，这类 backend representation 也是中间表示设计的重要参考。

### 作为目标形式主义还是中间表示

明显是验证后端的中间表示与实现基础设施，不是最终交付给控制工程师的目标形式主义。

### 对需求到模型生成的启发

1. 时间需求最后往往要落到 `x-y<c` 这类差分守卫。
2. 若 LLM 未来要输出 timed model，中间层最好能直接对接这类差分表示。
3. 对含大量共享子结构的时序约束，decision-diagram 风格比朴素枚举更适合闭环迭代。

### 现实限制

`DDD` 对差分约束很强，但它不是完整 timed-modeling ecosystem；如果没有上层 `Timed Automata / Timed Petri Nets / queries`，它本身并不能独立完成验证工作流。

## 重要的相关工作

1. [a-tutorial-on-uppaal/desc.md](../a-tutorial-on-uppaal/desc.md)：经典 `Timed Automata` 平台与 zone-based symbolic checking 主线。
2. [time-petri-nets-analysis-with-tina/desc.md](../time-petri-nets-analysis-with-tina/desc.md)：`TPN` 工具链视角下的时间网后端。
3. [fortuna-model-checking-priced-probabilistic-timed-automata/desc.md](../fortuna-model-checking-priced-probabilistic-timed-automata/desc.md)：更晚的 priced-probabilistic timed symbolic verification 工具线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Difference Decision Diagrams / DDD / ODDD / RPDDD`
- 归类理由：论文主贡献是 timed verification 的差分约束表示与算法基础设施，而不是新的状态机本体。
