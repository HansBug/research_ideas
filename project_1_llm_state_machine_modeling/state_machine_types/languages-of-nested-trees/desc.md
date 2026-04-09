# 嵌套树的语言 / Languages of Nested Trees

## 基本信息

- 标题：Languages of Nested Trees
- 中文标题：嵌套树的语言
- 作者：Rajeev Alur、Swarat Chaudhuri、P. Madhusudan
- 发表：*Computer Aided Verification*, LNCS 4144, pp. 329-342, 2006
- DOI：`10.1007/11817963_31`
- 链接：https://www.cs.utexas.edu/~swarat/pubs/cav06.pdf
- 形式主义：`Nested Trees / Nested Tree Automata (NTA)`，并以 pushdown / `RSM` 程序展开为主要语义来源
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：conference origin / `NSM` branching semantics family
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 nested tree 结构、nested pushdown tree、`NP-NTA / AP-NTA` 与 `NT-μ`。
- 标准/格式获取方式：原文没有 DSL 或文件交换标准；核心承载方式是 graph/tree tuple、jump-edge relation 与 automata/game semantics。

## 简报

这篇论文把 `RSM` 之后的一类关键语义对象明确命名了出来：如果递归程序的 branching behavior 不再看成 plain tree，而是看成带匹配 jump-edge 的树形结构，那么我们得到的就是 `nested tree`。论文随后定义了 operating on such structures 的 `nested tree automata`，从而把 `NSM` / pushdown 程序的 branching-time semantics 稳定成一个可以单独挂树的 family。

- 形式主义定位：`RSM / NSM` 的 branching semantics family，用 `nested trees` 显式表达 call / return 的匹配结构。
- 构造方式简述：先从 pushdown system 或 recursive program 的配置树出发，再把 matching push / pop 关系补成 jump-edges，最后在该结构上定义 `NP-NTA / AP-NTA`。
- 基础设施与场景简述：纯理论论文，但它把 `nested trees`、`nested pushdown trees`、`AP-NTA` 与 `NT-μ` 一次性放进同一框架，很适合作为 `NSM` 分支的 conference origin。

```text
pushdown / recursive program -> nested pushdown tree -> nested tree language -> NP-NTA / AP-NTA -> branching-time specification
```

## 形式主义定义与核心对象

### 定义对象

原文研究的核心对象不是 ordinary tree，而是“在树上加一组 properly nested jump-edges”得到的 `nested tree`。这些 jump-edges 直接承担 call / return 的匹配语义。

### 核心抽象

文中把带标注的 nested tree 写成：

$$
T = (T,\rightsquigarrow,\lambda)
$$

上式中的符号逐项解释如下：

1. 左侧的 `T` 表示整棵 nested tree 结构。
2. 右侧第一个 `T` 是其底层 tree skeleton。
3. `\rightsquigarrow` 是 jump-edge relation，用来连接 matching call / return。
4. `\lambda` 是节点标注函数。

为了把 call / return / local 三类边显式化，原文还定义了 structured tree：

$$
\mathrm{Struct}(T) = (T,\lambda,\delta)
$$

这里：

1. `\delta : E \to \{call,ret,loc\}` 给每条 tree-edge 赋边类型；
2. 它保证 nested tree 的 jump-structure 可以由边标签恢复。

### 一个最小例子与通俗解释

论文图 1 的直觉非常清楚：

1. 普通程序展开先得到一棵 branching tree。
2. 某个 call node 沿不同路径可能对应多个 matching return。
3. 从该 call node 指向这些 return nodes 的虚线 jump-edges 就构成 nested structure。

通俗地说，`nested tree` 就像“把递归程序的树展开，再把所有匹配返回点用额外连线串起来”。这样它比 ordinary tree 多了“哪个返回是由哪个调用产生的”这层信息，因此能表达 plain tree logic 说不清的上下文相关性质。

### 运行 / 接受 / 转移语义

原文进一步把 pushdown system `P` 的 branching semantics 定义成 nested pushdown tree：

$$
CTree(P) = (T_P,\rightsquigarrow,\lambda)
$$

上式中的符号逐项解释如下：

1. `P` 是一个 pushdown system。
2. `T_P` 是其配置树。
3. `\rightsquigarrow` 把 stack 相同且“最近匹配”的 push / pop 对接起来。
4. `\lambda` 把配置映射到观测字母表。

在此基础上，nested tree automaton 的语言可写成：

$$
L(A)=\{\,T \mid A \text{ accepts } T\,\}
$$

这里：

1. `A` 可以是 nondeterministic parity nested tree automaton 或 alternating parity nested tree automaton。
2. `T` 是一个 nested tree。
3. `L(A)` 表示被该 automaton 接受的 nested-tree language。

### 语义边界

这篇论文明确了三条边界：

1. `nested trees` 比 ordinary trees 更强，因为它保留了 call / return 匹配关系。
2. `AP-NTA` 比 `NP-NTA` 更强，和普通 tree automata setting 不同，alternation 在这里会增加表达力。
3. `MSO` 直接加 matching predicate 会变得过强，以至于 model checking 不再可判定。

### 关键性质与判定边界

论文给出的核心复杂度结论可压成：

$$
\mathrm{MC}(\mathrm{AP\text{-}NTA},\mathrm{PDS}) \text{ is EXPTIME-complete}
$$

以及：

$$
\mathrm{AP\text{-}NTA} \equiv NT\text{-}\mu
$$

上式中的符号逐项解释如下：

1. `\mathrm{MC}` 表示模型检验问题。
2. `\mathrm{PDS}` 是 pushdown system。
3. `\mathrm{AP\text{-}NTA}` 是 alternating parity nested tree automata。
4. `NT\text{-}\mu` 是论文采用的 nested-tree fixpoint calculus。

这说明 `nested tree` family 并非只是语义小修补，而是形成了一个稳固的新 regular-language theory。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 重点不是程序状态集合，而是 branching semantic object。 |
| 事件 / 触发 | 中等支持 | 通过 call / ret / loc 边类型体现。 |
| 守卫 / 数据 | 不支持 | 不讨论有限变量。 |
| 层次 | 强支持 | jump-edge 显式保留程序调用层次。 |
| 并发 / 同步 | 不支持 | 目标对象是 sequential pushdown programs。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散结构。 |
| 可执行 / 可验证性 | 强理论支持 | 有 `NTA`、`NT-μ` 与 `EXPTIME` model checking。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| nested tree | `$T=(T,\rightsquigarrow,\lambda)$` | 基本语义对象。 |
| structured tree | `$\mathrm{Struct}(T)=(T,\lambda,\delta)$` | 说明 jump-structure 可由边标签恢复。 |
| nested pushdown tree | `$CTree(P)=(T_P,\rightsquigarrow,\lambda)$` | 从 pushdown / `RSM` 语义生成 nested tree。 |
| automaton language | `$L(A)=\{T\mid A\text{ accepts }T\}$` | nested-tree language 的标准定义。 |
| 表达力与复杂度 | `$\mathrm{AP\text{-}NTA}\equiv NT\text{-}\mu$`, `$\mathrm{EXPTIME}$-complete` | 说明该 family 既稳固又可判定。 |

## 构造方式与承载格式

### 建模入口

1. 先把递归程序写成 pushdown system 或 `RSM` 风格程序抽象。
2. 展开出 branching configuration tree。
3. 再用 jump-edges 把 matching call / return 接起来，得到 nested tree。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. nested tree tuple；
2. nested pushdown tree；
3. `NP-NTA / AP-NTA`；
4. `NT-μ`。

### 交换与互操作

它与当前文库里的关系很清楚：

1. 向上衔接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 `RSM`。
2. 向旁边衔接 [logics-and-automata-for-software-model-checking/desc.md](../logics-and-automata-for-software-model-checking/desc.md) 的 `NSM` 讲义入口。
3. 向下被 [software-model-checking-using-languages-of-nested-trees/desc.md](../software-model-checking-using-languages-of-nested-trees/desc.md) 扩成 journal full version。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 nested-tree / structured-tree / automaton tuple。
- 仿真/执行支持：可由 pushdown / recursive program unfolding 获得。
- 验证/分析支持：`NP-NTA`、`AP-NTA`、`NT-μ`、MSO comparison。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 pushdown / recursive-program model checking 理论侧 family，不是工程标准。

## 适用场景与需求前提

### 适用场景

适合：

1. 需要在 branching-time 上显式跟踪 call / return 匹配的程序模型。
2. 想把 `RSM` 再投影成 regular languages of nested trees 的理论工作。
3. 需要比较 ordinary tree vs. nested tree 在表达力上的差异。

### 需求前提

1. 对象是顺序递归程序或等价 pushdown / `RSM` 抽象。
2. 需求关心 matching return、local context、summary edges 等结构性信息。
3. 可以接受模型最终落成 tree-like semantic object，而非平面状态图。

### 不适用或高成本场景

若只需 ordinary `RSM` 的 reachability / summary relation，不需要再投影成 nested trees；若主要关注工程可执行建模语言，则这条线过于理论化。

## 与相邻形式主义的关系

相对 `RSM`，`nested trees` 不是新的过程调用语法骨架，而是新的 branching semantic object；相对 plain tree automata，它把 call / return 匹配结构显式化；相对 `NSM`，它更像 `NSM` 的 branching-time 语义载体和其上的 automata family。

## 与本研究的关系

### 对 Project 1 的价值

它为当前 `RSM` 主枝补出一个此前缺失的“语义对象节点”：`NSM` 之下不仅有 call / return stack semantics，还可以长出 `nested tree` 这条 regular-language branch。

### 作为目标形式主义还是中间表示

更适合作为验证 / 规范分析的中间语义对象，而不是需求侧的直接输出模型。

### 对需求到模型生成的启发

如果后续要让 LLM 生成的递归状态机支持“当前过程块内部是否必然返回”“某个 call 的后置条件是否在 matching return 上成立”这类问题，那么把模型进一步翻译到 nested-tree family 会更自然。

## 重要的相关工作

1. [software-model-checking-using-languages-of-nested-trees/desc.md](../software-model-checking-using-languages-of-nested-trees/desc.md)：该线的 journal full version。
2. [logics-and-automata-for-software-model-checking/desc.md](../logics-and-automata-for-software-model-checking/desc.md)：把 `NSM` 与 nested structures 放进统一讲义框架。
3. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：作为该 semantic branch 的上游递归控制流模型。

## 文献分类总结

- 这篇论文最适合在当前文库里承担：`NSM` branching semantics 的 conference origin。
- 它的新增价值在于：把 `nested trees` 与 `nested tree automata` 稳定成单独 family，而不是只把它们当作 `RSM` 的证明辅助结构。
- 若后续演化树需要克制节点数量，可把它和 journal 版共同合并到 `Nested State Machines / Nested Trees` 一个节点下；但 conference / journal 双锚点仍值得保留。
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
