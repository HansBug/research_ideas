# 架构图：面向架构风格规约的图形语言 / Architecture Diagrams: A Graphical Language for Architecture Style Specification

## 基本信息

- 标题：Architecture Diagrams: A Graphical Language for Architecture Style Specification
- 中文标题：架构图：面向架构风格规约的图形语言
- 作者：Anastasia Mavridou，Eduard Baranov，Simon Bliudze，Joseph Sifakis
- 发表：*Electronic Proceedings in Theoretical Computer Science*，223:83-97，2016
- DOI：`10.4204/EPTCS.223.6`
- 链接：https://doi.org/10.4204/EPTCS.223.6
- 形式主义：`architecture diagrams / interval architecture diagrams / connector motifs / BIP-rooted architecture style language`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🤝 接口 / 交互契约
- 所属领域：🌐 协议 / 分布式 / 交互系统
- 论文角色：组件交互结构图形语言与 conformance / synthesis 基础设施
- 工具/实现获取方式：原文说明作者已用 `JaCoP` 约束求解器实现 conformance checking 与合成原型；正文未给稳定公开仓库。
- 标准/格式获取方式：核心承载是 architecture diagram 本身的图形语法、component types、cardinality、connector motifs，以及 interval 扩展；不是工业中立交换标准。

## 简报

这篇论文补的不是某个组件运行时，而是“如何把架构风格本身画出来并检查它是否真的定义得通”的图形语义层。它把组件类型、端口、端口 multiplicity、degree 和 connector motifs 压成 architecture diagram，并给出何时存在 conforming architecture、如何检查具体架构是否符合图，以及如何从图合成满足约束的 connector 配置。

- 形式主义定位：面向交互结构与架构风格的图形语言 / 基础设施，不是新的行为语义引擎。
- 构造方式简述：先声明 component types 与 cardinality，再给每类 connector motif 标注端口 multiplicity / degree，必要时扩展成区间版本，随后做 consistency、conformance 与 configuration synthesis。
- 基础设施与场景简述：依托图形语法、matching factor、线性方程组和 conformance algorithm，服务组件化系统、架构风格说明与 `BIP` 系图形前端。

```text
component types + cardinalities + connector motifs -> architecture diagram -> consistency / conformance / synthesis -> architecture-style specification
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. simple architecture diagrams；
2. interval architecture diagrams；
3. component types 与 generic ports；
4. connector motifs；
5. conformance、consistency 与 configuration synthesis。

### 核心抽象

论文对 simple architecture diagram 直接给出：

$$
D = \langle T,n,C \rangle
$$

上式中的符号逐项解释如下：

1. `$T=\{T_1,\ldots,T_k\}$` 是 component types 集合。
2. `$n:T\to\mathbb N$` 是 cardinality function，给出每种组件类型应有多少实例。
3. `$C=\{G_1,\ldots,G_l\}$` 是 connector motifs 集合。

单个 connector motif 写成：

$$
G = (a,\{m_p : d_p\}_{p\in a})
$$

上式中的符号逐项解释如下：

1. `$a$` 是参与该 connector 的 generic ports 集合。
2. `$m_p$` 是端口 `$p$` 的 multiplicity，即一个 connector 中必须出现多少个该类端口实例。
3. `$d_p$` 是端口 `$p$` 的 degree，即一个端口实例在整个配置中要参与多少个 connectors。

具体架构则被写成：

$$
\mathit{Arch} = \langle B,g \rangle
$$

上式中的符号逐项解释如下：

1. `$B$` 是具体组件实例集合。
2. `$g$` 是 configuration，即 connectors 的集合。
3. 每个组件实例要和其类型的 generic ports 一一对应。

论文对 conformance 的核心语义是：

$$
\langle B,g\rangle \models \langle T,n,C\rangle
$$

其含义是：

1. 每个组件类型的实例数必须等于其 cardinality。
2. `$g$` 必须能分区到各个 connector motifs 上。
3. 对每个 motif 中的每个 generic port，既要满足每个 connector 中的 multiplicity，也要满足每个实例总共参与的 degree。

为判断 diagram 是否一致，论文引入 matching factor：

$$
s_p = \frac{n_p \cdot d_p}{m_p}
$$

上式中的符号逐项解释如下：

1. `$n_p$` 是拥有 generic port `$p$` 的组件类型实例数。
2. `$d_p$` 是该端口的 degree。
3. `$m_p$` 是该端口的 multiplicity。
4. `$s_p$` 直观上表示：从端口 `$p$` 视角看，总共应出现多少个 connectors。

论文给出的 simple architecture diagram 一致性条件可压成：

$$
m_p \le n_p,\qquad \forall q\in a.\ s_p=s_q\in\mathbb N,\qquad s_p \le \prod_{q\in a}\binom{n_q}{m_q}
$$

上式中的符号逐项解释如下：

1. 第一项要求 multiplicity 不能超过该类端口实例数。
2. 第二项要求同一 motif 上所有端口的 matching factor 一致且为整数。
3. 第三项要求潜在可区分的 connector 数量足以满足所需的 degree / multiplicity 配置。

### 一个最小例子与通俗解释

论文给了一个很直观的对比：

1. 如果端口 `p` 的 multiplicity 为 `1`，端口 `q` 的 multiplicity 为 `3`，那就意味着每个 connector 都必须是“一个 `p` 连三个 `q`”的四元连接。
2. 如果 `p` 和 `q` 的 multiplicity 都是 `1`，但 `p` 的 degree 为 `3`，那就变成一个 `p` 要分别连到三个 `q`，形成三条二元连接。
3. 两张图用的是同一批组件类型和实例数，但架构语义完全不同。

通俗地说，architecture diagram 不是在画“组件之间有没有线”，而是在画“每种端口应该以什么组合规模、连接次数和重复模式参与同步”。这比普通组件连线图更像是“交互拓扑约束语言”。

### 运行 / 接受 / 转移语义

这篇论文没有提供行为迁移语义，而是提供配置生成语义。对某个 generic port `$p$`，论文把 regular configuration 写成线性方程：

$$
G X = D
$$

上式中的符号逐项解释如下：

1. `$G$` 是端口实例与候选 sub-connectors 的 incidence matrix。
2. `$X$` 是各候选 sub-connectors 取用次数向量。
3. `$D=[d_p,\ldots,d_p]$` 表示每个端口实例都必须出现 `$d_p$` 次。
4. 任一非负整数解都对应一个满足 degree 约束的 regular configuration。

而 conformance checking 则被落实为若干程序步骤：

1. `VerifyCardinality` 检查组件类型个数是否满足 diagram；
2. `VerifyMultiplicity` 检查每个 connector 是否满足 motif multiplicity；
3. `VerifyDegree` 检查每个端口实例是否满足 degree。

### 语义边界

1. 论文刻意忽略组件内部行为语义，只关心交互结构。
2. 数据流与端口值传递不在主体内，论文只在结尾把它列为未来工作。
3. architecture diagram 说明的是 architecture style，不是完整执行模型。
4. 若系统需要表达状态依赖或时序依赖，仍需接到 `BIP` 行为层或其他行为模型。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| diagram 骨架 | `$D=\langle T,n,C\rangle$` | 图形语言的最小定义单位。 |
| connector motif | `$G=(a,\{m_p:d_p\}_{p\in a})$` | 交互结构由 multiplicity 和 degree 精确定义。 |
| conformance | `$\langle B,g\rangle \models \langle T,n,C\rangle$` | 判断具体架构是否满足图。 |
| matching factor | `$s_p=\frac{n_p d_p}{m_p}$` | 一致性分析的核心数量关系。 |
| regular configuration | `$GX=D$` | 把 connector synthesis 约束化、方程化。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 不支持 | 不描述组件内部状态演化。 |
| 事件 / 触发 | 弱支持 | 通过 ports 抽象交互点，但不描述触发时机。 |
| 守卫 / 数据 | 不支持 | 主体是结构与连线约束，不处理 guards/data。 |
| 层次 | 弱支持 | 支持 component type 到 instance 的组织，但不是层次状态机。 |
| 并发 / 同步 | 很强 | connector motif 本质上就是同步/交互拓扑约束。 |
| 时间约束 | 不支持 | 不是 timed architecture language。 |
| 连续动态 / 随机性 | 不支持 | 不在范围内。 |
| 可执行 / 可验证性 | 中等支持 | 可做 consistency、conformance 和 configuration synthesis，但不直接执行行为。 |

### 形式化问题与性质

1. 这篇论文真正稳定下来的，是“connector motif 是否自洽、图是否能有实例、具体架构是否真的符合图”这三个基础问题。
2. 它提供的是架构风格的 machine-processable 表达，而不是又一个随手画画的组件图。
3. 对 `BIP/JavaBIP/DesignBIP` 这条线来说，它补的是图形语义与一致性地基。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 定义 component types 及其 generic ports；
2. 指定每种类型实例个数；
3. 为每类交互定义 connector motifs；
4. 必要时把单值 cardinality / multiplicity / degree 扩展成 interval。

### 机器可处理承载方式

机器可处理承载方式包括：

1. simple architecture diagrams；
2. interval architecture diagrams；
3. incidence matrix 与 regular-configuration vectors；
4. conformance-checking algorithm 的输入 configuration。

### 交换与互操作

1. 论文把图形约束直接连到线性方程和约束求解。
2. 这套语言和 `BIP` component / connector 思想高度同源。
3. 后续 `DesignBIP` 可以视作这类 diagram 的工程化、可视化和代码生成延伸。

## 配套基础设施

- 建模/编辑工具：原文主打图形 language，本身可作为编辑前端。
- 解析/交换/元模型支持：核心是 component types、ports、cardinality 和 connector motifs 的结构化表示。
- 仿真/执行支持：不主打执行。
- 验证/分析支持：diagram consistency、architecture conformance、configuration synthesis。
- 代码生成/转换支持：原文未直接给代码生成链，重点在 style specification 与 analysis。
- 标准化或社区生态：以 `BIP` 架构风格研究为背景，原型实现使用 `JaCoP` 约束求解器。

## 适用场景与需求前提

### 适用场景

适合那些已经清楚知道系统要由哪些组件类型、端口种类和交互模式组成，但希望先把“允许怎样连接”这件事固定下来，再去考虑行为语义的架构建模场景。

### 需求前提

1. 系统需能抽成有限个 component types 与端口种类。
2. 交互需求更像“某类端口需要几方同步、每个实例要参与几次连接”，而不是复杂局部算法。
3. 团队希望有可检验的架构风格，而不满足于 informal connector sketches。
4. 若要走 interval extension，需接受 cardinality / multiplicity / degree 的区间化表达。

### 不适用或高成本场景

若系统的关键差异来自局部状态、时序窗口或复杂数据依赖，仅靠 architecture diagram 不够；若交互结构本身高度动态、实例集合持续变化，也会超出本文固定-cardinality 主线。

## 与相邻形式主义的关系

相对 [modeling-heterogeneous-real-time-components-in-bip/desc.md](../modeling-heterogeneous-real-time-components-in-bip/desc.md)，那篇给出的是 `BIP` 行为/交互/优先级分层母线，而本文专注于 architecture-style 图形语义；相对 [designbip-a-design-studio-for-modeling-and-generating-systems-with-bip/desc.md](../designbip-a-design-studio-for-modeling-and-generating-systems-with-bip/desc.md)，`DesignBIP` 更偏工程工作台和代码生成，本文则是其前置图形语言与 conformance 理论地基；相对 [coordination-of-dynamic-software-components-with-javabip/desc.md](../coordination-of-dynamic-software-components-with-javabip/desc.md)，`JavaBIP` 面向运行时组件协调，而 architecture diagrams 还停留在架构风格规约层。

## 与本研究的关系

### 对 Project 1 的价值

1. 它说明“状态机建模”之外，还可以先把交互骨架和组合约束单独结构化出来。
2. 对 LLM 来说，这类 diagram 特别适合作为从文本需求中提取的中间层，因为它比完整行为模型更稳、更容易校验。
3. 如果后续要生成分组件状态机，architecture diagram 可以成为分解边界与交互接口的前置约束。

### 作为目标形式主义还是中间表示

更适合作为组合约束中间表示或架构风格规约，而不是单独承担全部行为语义的目标模型。

### 对需求到模型生成的启发

1. 先抽组件类型、端口和连接模式，再细化行为，往往比直接生成整套状态机更稳。
2. LLM 生成出来的架构图，可以先做 consistency / conformance 筛错，再进入更细粒度行为建模。
3. 多组件系统的“结构正确”与“行为正确”最好拆成两层分别验证。

## 重要的相关工作

1. [modeling-heterogeneous-real-time-components-in-bip/desc.md](../modeling-heterogeneous-real-time-components-in-bip/desc.md)：`BIP` 母线。
2. [designbip-a-design-studio-for-modeling-and-generating-systems-with-bip/desc.md](../designbip-a-design-studio-for-modeling-and-generating-systems-with-bip/desc.md)：基于 architecture diagrams 的工程化工作台。
3. [coordination-of-dynamic-software-components-with-javabip/desc.md](../coordination-of-dynamic-software-components-with-javabip/desc.md)：运行时 `JavaBIP` 协调基础设施。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
