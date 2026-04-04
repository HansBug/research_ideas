# 一维可逆（单射）细胞自动机的计算通用性 / Computation Universality of One-Dimensional Reversible (Injective) Cellular Automata

## 基本信息

- 标题：Computation Universality of One-Dimensional Reversible (Injective) Cellular Automata
- 中文标题：一维可逆（单射）细胞自动机的计算通用性
- 作者：Kenichi Morita、Masateru Harao
- 发表：*The Transactions of the IEICE*, E72(6):758-762, 1989
- DOI：原文未提供
- 链接：https://hiroshima.repo.nii.ac.jp/record/2008959/files/TransIEICE_E72-6_758.pdf
- 形式主义：`Reversible / Injective Cellular Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🖼️ 网格 / 图案对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：理论分析
- 工具/实现获取方式：原文未提供软件实现；机器可处理入口是 `1-CA` 与 `1-PCA` 的局部函数、全局函数和 reversible `1-TM` 模拟构造。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 `1-CA` / `1-PCA` 元组、全局更新函数、局部可逆性判据和 `TM` embedding。

## 简报

这篇论文真正补出的，不只是“1D reversible CA 也能通用”这个结论，更重要的是把 `Reversible / Injective Cellular Automata` 这一支稳定命名下来，并通过 `1-PCA` 把“局部可逆”和“全局可逆”之间最关键的结构关系说清。对当前文库来说，它正好把 [cellular-automata/desc.md](../cellular-automata/desc.md) 主线往 `reversible / injective` 理论分支推进一步，也给后面的块划分可逆模型提供父节点。

- 形式主义定位：`Cellular Automata` 主干下的 reversible / injective 分支母节点。
- 构造方式简述：先定义 ordinary `1-CA`，再引入每个 cell 都拆成 `left / center / right` 三部分的 `1-PCA`，并在 `1-PCA` 上建立局部可逆性与全局可逆性的等价。
- 基础设施与场景简述：原文是纯理论工作，但 `1-CA` / `1-PCA` 元组、global function、local reversibility criterion 与 reversible `1-TM` embedding 非常清楚，足以直接挂树。

```text
局部状态邻域更新 -> reversible global map -> partitioned CA bridge -> reversible computation universality
```

## 形式主义定义与核心对象

### 定义对象

论文先给 ordinary one-dimensional cellular automaton 一个标准定义，再把“每个 cell 切成三部分”的 partitioned version 单独定义出来。核心目的不是引入另一门语言，而是让 reversible 设计变得局部可判。

### 核心抽象

原文把 one-dimensional cellular automaton 写成：

$$
A = (Z, Q, f_A)
$$

上式中的符号逐项解释如下：

1. `Z` 是所有整数位置组成的格点集合。
2. `Q` 是每个 cell 的有限内部状态集合。
3. `f_A : Q^3 \to Q` 是最近邻局部函数。

若 `c : Z \to Q` 是一个 configuration，则其全局函数满足：

$$
F_A(c)(i) = f_A(c(i-1), c(i), c(i+1))
$$

原文把 reversible 定义为：

$$
A \text{ is reversible } \iff F_A \text{ is one-to-one}
$$

随后，论文引入一维 partitioned cellular automaton：

$$
P = (Z, L, C, R, f_P)
$$

上式中的符号逐项解释如下：

1. `L`、`C`、`R` 分别是每个 cell 左、中、右三个分区上的状态集合。
2. `f_P : R \times C \times L \to L \times C \times R` 是局部函数。
3. 每个 cell 的下一状态不再读取完整三个相邻 cell，而是读取“左邻 cell 的右部、当前 cell 的中部、右邻 cell 的左部”。

对应的全局函数为：

$$
F_P(c)(i) = f_P(\mathrm{RIGHT}(c(i-1)), \mathrm{CENTER}(c(i)), \mathrm{LEFT}(c(i+1)))
$$

### 一个最小例子与通俗解释

一个最简单的可逆 `1-PCA` 例子，可以取局部函数：

$$
f_P(r,c,l) = (l,c,r)
$$

它的直觉含义是：

1. 把右邻居的左部拿来做当前 cell 的左部。
2. 保留当前 cell 的中心分量不变。
3. 把左邻居的右部拿来做当前 cell 的右部。

这本质上是一种局部信息重排，没有丢失任何信息，因此显然是可逆的。

通俗地说，`1-PCA` 像给普通 `CA` 每个格点都装了三个可单独接线的小接口。这样一来，设计 reversible rule 时就不再靠全局试错，而可以直接检查局部函数是否一一对应。

### 运行 / 接受 / 转移语义

这里的语义不是语言接受，而是 configuration 演化。一步运行语义就是：

$$
c \mapsto F_A(c)\quad \text{or}\quad c \mapsto F_P(c)
$$

在这个框架里，论文最关键的结构结论是：

$$
P \text{ is globally reversible } \iff P \text{ is locally reversible}
$$

其中 “locally reversible” 就是 `f_P` 本身是一一映射。也就是说，`1-PCA` 把“全局双射”这个难检性质，转成了“局部函数是否 injective”这个容易检查的性质。

### 语义边界

这条分支的边界很明确：

1. 对象是无限一维格点配置，不是词语言。
2. 关注点是信息不丢失的局部更新，而不是一般 `CA` 动力学分类。
3. `1-PCA` 是为 reversible construction 设计的桥接模型，不等于后来的 block / Margolus 型分块模型。

### 关键性质与判定边界

论文最值得保留的两条结论是：

$$
P \text{ globally reversible } \iff f_P \text{ injective}
$$

以及

$$
\forall \text{ reversible 1-TM } T,\ \exists \text{ reversible 1-PCA } P \text{ simulating } T
$$

结合文中的 `1-PCA -> 1-CA` 嵌入构造，可进一步得到：

$$
\forall \text{ 1-TM } T,\ \exists \text{ reversible 1-CA } A \text{ simulating } T
$$

这就是题目中的 computation universality 结论。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个格点取有限离散状态，`1-PCA` 还显式拆成三分区。 |
| 事件 / 触发 | 不适用 | 由同步离散步推进，而非事件触发。 |
| 守卫 / 数据 | 不支持 | 无一般变量守卫；增强点在局部结构与可逆性。 |
| 层次 | 不支持 | 不是层次状态图。 |
| 并发 / 同步 | 强支持 | 所有 cell 同步更新。 |
| 时间约束 | 部分支持 | 只有离散时步，无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散、确定性的格点演化模型。 |
| 可执行 / 可验证性 | 强理论支持 | local/global reversibility 判据和 `TM` embedding 都很明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| ordinary `1-CA` | `$A=(Z,Q,f_A)$` | reversible `CA` 分支的基础骨架。 |
| global map | `$F_A(c)(i)=f_A(c(i-1),c(i),c(i+1))$` | 说明一维最近邻 `CA` 的普通语义。 |
| partitioned `1-PCA` | `$P=(Z,L,C,R,f_P)$` | 论文为 reversible design 引入的关键中间模型。 |
| reversible criterion | `$P$ globally reversible $\iff f_P$ injective` | 使可逆性检查从全局落回局部。 |
| 通用性 | `reversible 1-TM -> reversible 1-PCA -> reversible 1-CA` | 把 reversible `CA` 从趣味对象推进到通用计算模型。 |

## 构造方式与承载格式

### 建模入口

建模时首先要决定：

1. 是直接使用 ordinary `1-CA`，还是先走 `1-PCA` 进行可逆构造。
2. 局部规则是否必须 information-preserving。
3. 关注点是 reversible computation，还是一般 `CA` 动力学。

### 机器可处理承载方式

原文的机器可处理承载方式是元组、configuration、global function 和 reversible embedding，不是某种文件格式。

### 交换与互操作

它与以下对象互操作最强：

1. reversible `1-TM`。
2. ordinary `1-CA`。
3. 后续的 reversible block / partitioning cellular automata。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 `1-CA` / `1-PCA` 元组和 global map 语义。
- 仿真/执行支持：可直接按局部函数同步迭代。
- 验证/分析支持：局部 / 全局可逆性等价是最关键的分析基础设施。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 reversible computation 与 classical `CA` 理论的交叉支线。

## 适用场景与需求前提

### 适用场景

适用于需要 information-preserving lattice dynamics、可回溯计算、reversible computation 理论或局部可逆规则设计的场景。

### 需求前提

1. 对象应是格点配置，而不是词语言或层次控制图。
2. 需求关心“每一步不能丢信息”，而不是只关心一般 reachability。
3. 若要直接利用论文中的易判性，最好先转成 `1-PCA` 视角。

### 不适用或高成本场景

如果需求核心是非均匀邻域、有限拓扑或 shift-dynamics 风格的全局结构，[local-and-global-reversibility-of-finite-inhomogeneous-cellular-automaton/desc.md](../local-and-global-reversibility-of-finite-inhomogeneous-cellular-automaton/desc.md) 更贴切；如果需求是块划分电路式结构分解，则后续 reversible block `CA` 更自然。

## 与相邻形式主义的关系

相对 [cellular-automata/desc.md](../cellular-automata/desc.md)，它把普通 `CA` 主线沿“information-preserving”方向单独收束成稳定分支；相对 [local-and-global-reversibility-of-finite-inhomogeneous-cellular-automaton/desc.md](../local-and-global-reversibility-of-finite-inhomogeneous-cellular-automaton/desc.md)，它不是讨论有限非均匀拓扑，而是一般一维 reversible / injective 结构；相对 [representing-reversible-cellular-automata-with-reversible-block-cellular-automata/desc.md](../representing-reversible-cellular-automata-with-reversible-block-cellular-automata/desc.md)，后者是把这条 reversible 主线进一步结构分解成 block permutation。

## 与本研究的关系

### 对 Project 1 的价值

它为演化树补出了 `Cellular Automata -> Reversible / Injective Cellular Automata` 这个关键母节点，也把 `reversible block CA` 这类后继模型挂到了更合理的位置。

### 作为目标形式主义还是中间表示

它主要是谱系节点和理论边界参照，不是控制系统需求建模的常规终点；但它很好地展示了“局部结构变化如何改变可验证性与表达边界”。

## 重要的相关工作

1. [cellular-automata/desc.md](../cellular-automata/desc.md)：更高一层的 `CA` 主节点。
2. [local-and-global-reversibility-of-finite-inhomogeneous-cellular-automaton/desc.md](../local-and-global-reversibility-of-finite-inhomogeneous-cellular-automaton/desc.md)：从有限非均匀角度研究 reversibility 的邻近条目。
3. [representing-reversible-cellular-automata-with-reversible-block-cellular-automata/desc.md](../representing-reversible-cellular-automata-with-reversible-block-cellular-automata/desc.md)：把 reversible `CA` 进一步表示成 block permutation 组合的后继分支。

## 文献分类总结

- 这是一篇 `🧱 模型本体` 条目，因为它给出了 reversible `1-CA` / `1-PCA` 的稳定定义和关键 structural theorem。
- 它应挂在 `Cellular Automata` 之下，并作为 `Reversible Block Cellular Automata` 的父节点。
- 它不是 DSL、工具或应用案例条目，也不是只证明某个具体 `CA` 例子可逆的局部论文。
