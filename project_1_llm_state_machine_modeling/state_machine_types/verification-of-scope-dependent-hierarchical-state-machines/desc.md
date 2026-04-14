# 作用域相关层次状态机的验证 / Verification of Scope-Dependent Hierarchical State Machines

## 基本信息

- 标题：Verification of Scope-Dependent Hierarchical State Machines
- 中文标题：作用域相关层次状态机的验证
- 作者：Salvatore La Torre, Margherita Napoli, Mimmo Parente, Gennaro Parlato
- 发表：*Information and Computation*, 206(9-10):1161-1177, 2008
- DOI：`10.1016/j.ic.2008.03.017`
- 链接：https://eprints.soton.ac.uk/272463/1/sdarticle.pdf
- 形式主义：`Scope-Dependent Hierarchical State Machines (Shsm / SHSM full version)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展 / journal full version
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `Shsm` 元组、flat Kripke structure `M^F`、partial evaluation、restricted `Shsm` 与 `LTL/CTL` verification reductions。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 box labeling、scope inheritance、restricted / unrestricted family distinction 与 automata-theoretic verification。

## 简报

这篇 journal 版把此前分散在 `CDHSM` 与 `SHSM` 两篇会议论文里的上下文标注语义收束成了一个统一名称：`scope-dependent hierarchical state machines`。它保留了 `HSM` 的 hierarchy 骨架，但允许 box 也带 atomic propositions，展开后这些命题会作为 scope 继承给后代状态。更关键的是，journal 版不只重复 2007 `SHSM` 会论文，而是显式加入 `restricted Shsm` 子类、succinctness 分层、`Reach/Cycle/LTL/CTL` 的完整复杂度表，因此它是当前树上 `CDHSM -> SHSM` 细枝最稳定的 full-version 依据。

- 形式主义定位：`HSM` 的 scope-labeling 扩展，也是 `CDHSM / SHSM` 支线的统一 journal 版定义。
- 构造方式简述：模型仍由多个 machines 组成；区别在于 box 允许携带命题标签，并把这些标签作为作用域继承给展开后的全部后代状态。
- 基础设施与场景简述：纯理论条目，但系统给出 unrestricted / restricted `Shsm`、succinctness 关系以及 reachability、cycle、`LTL/CTL` 复杂度。

```text
hierarchical machine reuse -> box-level scope labels -> inherited context propositions -> more succinct flat semantics -> reachability / LTL / CTL checking
```

## 形式主义定义与核心对象

### 定义对象

原文直接把 `HSM` 的增强点写成“scope-dependent properties”：不是增加新的控制结构，而是把原本只能贴在 node 上的 propositions 推到 box 上，并让它们在展开后沿祖先链继承。

### 核心抽象

原文把 `Shsm` 写成：

$$
M = (M_1,\ldots,M_k)
$$

其中每个 machine 为：

$$
M_i = (V_i,in_i,out_i,true_i,expn_i,E_i)
$$

上式中的符号逐项解释如下：

1. `V_i` 是顶点集合。
2. `in_i \in V_i` 是初始顶点。
3. `out_i \subseteq V_i` 是输出顶点。
4. `true_i : V_i \to 2^{AP}` 给 nodes 与 boxes 都分配命题标签。
5. `expn_i : V_i \to \{0,1,\ldots,k\}` 指定某个顶点是否展开为下层 machine。
6. `E_i` 是局部边集。

journal 版还额外定义了 restricted `Shsm`：若 `u` 是 `v` 的祖先，则祖先与后代标签不重叠，从而得到一个更容易验证但表达力稍弱的子类。

### 一个最小例子与通俗解释

论文里给出的经典直觉是 digital clock：

1. 顶层 box 标记当前小时。
2. 中层 box 标记当前分钟。
3. 最底层 node 标记当前秒。
4. 展开后的 flat state 同时继承小时、分钟、秒三个层次的命题。

通俗地说，`Shsm` 像“允许大状态给整片子状态机贴作用域标签”的层次状态机。这样同一个子机可以在不同上下文中复用，但仍然被区分为不同语义环境。

### 运行 / 接受 / 转移语义

原文把 flat Kripke structure 记作：

$$
M^F
$$

其中 flat state 写成：

$$
\langle u_1\cdots u_m \rangle
$$

上式中的符号逐项解释如下：

1. `u_1` 位于 top-level machine。
2. 若 `u_j` 是 box，则 `u_{j+1}` 位于其展开得到的下层 machine。
3. `u_m` 是最终的 basic node。

flat state 的标签不只看叶子，而是祖先链并集：

$$
true(\langle u_1\cdots u_m \rangle) = \bigcup_{j=1}^{m} true(u_j)
$$

这就是 scope inheritance 的核心，也是它比 plain `HSM` 更紧凑的根源。

### 语义边界

该 family 的边界如下：

1. 它没有增加并发、时间或变量。
2. 它的增强点只在 context / scope labeling。
3. unrestricted `Shsm` 最强，restricted `Shsm` 更易验证但表达力更弱。
4. 普通 `HSM` 是其特殊情形，即所有 boxes 的 `true` 标签为空。

### 关键性质与判定边界

journal 版的核心结论包括：

$$
\text{Shsms can be exponentially more succinct than Hsms}
$$

并且 unrestricted `Shsm` 还能指数级强于 restricted `Shsm`。

对验证复杂度，原文给出：

$$
\mathrm{Reachability}(\mathrm{Shsm}),\ \mathrm{CycleDetection}(\mathrm{Shsm}) \text{ are NP-complete}
$$

对 `LTL`：

$$
\mathrm{MC}_{LTL}(M,\varphi) = O(|M| \cdot 16^{|\varphi|})
$$

若 `M` 是 restricted `Shsm`，则可改进为：

$$
O(|M| \cdot 8^{|\varphi|})
$$

对 `CTL`：

$$
\mathrm{MC}_{CTL}(M,\varphi) = O(|M|2^{|\varphi|d+|AP_\varphi|})
$$

其中 `d` 是最大出口数。也就是说，journal 版不仅保留了 2007 `SHSM` 的核心结论，还把 restricted 子类与 `CTL` 复杂度口径补齐了。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | nodes + boxes + hierarchy。 |
| 事件 / 触发 | 弱支持 | 以 graph transitions 为主。 |
| 守卫 / 数据 | 不支持 | 核心不在变量。 |
| 层次 | 强支持 | 与 `HSM` 同骨架，但有 scope labels。 |
| 并发 / 同步 | 不支持 | sequential family。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | reachability、cycle、`LTL`、`CTL`。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 总元组 | `$M=(M_1,\ldots,M_k)$` | `Shsm` 总体定义。 |
| machine 元组 | `$M_i=(V_i,in_i,out_i,true_i,expn_i,E_i)$` | 单机结构骨架。 |
| flat state | `$\langle u_1\cdots u_m\rangle$` | 上下文链状态。 |
| scope label | `$true(\langle u_1\cdots u_m\rangle)=\bigcup_{j=1}^m true(u_j)$` | 作用域继承语义。 |
| 复杂度 | `Reach/Cycle: NP-complete` | unrestricted `Shsm` 的主边界。 |

## 构造方式与承载格式

### 建模入口

1. 先按 `HSM` 一样定义 hierarchy。
2. 再决定哪些命题应放在 boxes 上作为 scope。
3. 若想保持更强结构纪律，可再约束成 restricted `Shsm`。
4. 最后通过 `M^F` 解释 flat semantics。

### 机器可处理承载方式

机器可处理承载方式主要包括：

1. machine tuple；
2. box labeling；
3. flat Kripke structure `M^F`；
4. partial evaluation + automata-theoretic checking。

### 交换与互操作

它与当前文库中两个既有节点的关系最直接：

1. 向上承接 [hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md](../hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md) 的 `CDHSM` / `CDRSM` 预备工作。
2. 向旁承接 [verification-of-succinct-hierarchical-state-machines/desc.md](../verification-of-succinct-hierarchical-state-machines/desc.md) 的 2007 `SHSM` 会论文。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 box labeling 与 scope inheritance。
- 仿真/执行支持：通过 `M^F` 直接解释。
- 验证/分析支持：`Reach/Cycle/LTL/CTL` 全覆盖。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要价值是把 scope-labeling 语义稳定命名化。

## 适用场景与需求前提

### 适用场景

适合：

1. 同一子机需要在多个上下文中复用，但上下文命题不同。
2. 需要把“模式级性质”沿 hierarchy 传播，而不是复制结构。
3. 想补齐 `CDHSM -> SHSM` 这条 context-labeling 理论细枝。

### 需求前提

1. 系统仍是 sequential hierarchy。
2. 关心的上下文差异能用 atomic propositions 表达。
3. 愿意用更高验证成本换更高模型压缩率。

### 不适用或高成本场景

如果需求没有 scope-level propositions，普通 `HSM` 更简单；如果需要 recursion，则应继续转向 `CDRSM` / `RSM` 分支。

## 与相邻形式主义的关系

相对 `HSM`，它允许 scope labels；相对 `CDHSM`，它把 earlier context-dependent ideas 稳定整理成单一 `Shsm` family，并区分 restricted / unrestricted；相对 2007 `SHSM` 会论文，journal 版补全了 restricted 子类与完整复杂度边界。

## 与本研究的关系

### 对 Project 1 的价值

它把层次状态机树上“上下文命题如何沿 hierarchy 传播”这根细枝彻底稳定下来，对后续从需求抽取 mode-level assumptions / properties 很有启发。

### 作为目标形式主义还是中间表示

更适合作为理论中间表示和谱系节点，而不是工业建模前端。

### 对需求到模型生成的启发

如果需求反复出现“处于某大模式时，内部所有细状态默认带某些性质”这类描述，LLM 应优先考虑 scope-labeling，而不是复制多个平行子机。

### 现实限制

它没有工程生态，而且 unrestricted family 的验证复杂度已经明显上升，因此更适合理论选型与 family mapping。

## 重要的相关工作

### 奠基或前身工作

- [hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md](../hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md)
- [verification-of-succinct-hierarchical-state-machines/desc.md](../verification-of-succinct-hierarchical-state-machines/desc.md)

### 同类型或同家族工作

- [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)
- [hierarchical-state-machines/desc.md](../hierarchical-state-machines/desc.md)

## 文献分类总结

- 这篇论文是 `scope-dependent / SHSM` 支线的标准 journal full version。
- 它严格属于 `🧩 + 🧱 + 🧮` 的模型本体条目，不是 DSL 或应用案例。
- 在当前演化树里，它最适合作为 `CDHSM -> SHSM` 细枝的长期挂接依据，并把此前“scope-dependent gap”从待补条目变成正式节点。
