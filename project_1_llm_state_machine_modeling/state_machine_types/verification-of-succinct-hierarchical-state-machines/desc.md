# 紧致层次状态机的验证 / Verification of Succinct Hierarchical State Machines

## 基本信息

- 标题：Verification of Succinct Hierarchical State Machines
- 中文标题：紧致层次状态机的验证
- 作者：Salvatore La Torre, Margherita Napoli, Mimmo Parente, Gennaro Parlato
- 发表：*Proceedings of the 1st International Conference on Language and Automata Theory and Applications*, pp. 485-496, 2007
- DOI：原文未给出
- 链接：https://eprints.soton.ac.uk/370685/1/lata07.pdf
- 形式主义：`Succinct Hierarchical State Machines (SHSM)`，并与 `HSM`、`CHSM` 对比
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `SHSM` 元组、well-formed sequence、flat Kripke structure `M^F`、context labels `true` 与 reachability / cycle / `LTL/CTL` model-checking 任务。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 machine tuple、box labeling、expansion mapping、context inheritance 语义与 automata-theoretic verification reduction。

## 简报

这篇论文做的增强很克制，但对层次状态机支线很关键：它允许 atomic propositions 不只贴在叶子节点上，也能贴在 box 上。这样一来，同一个被复用的子机在不同上下文中可以继承不同的命题标签，而不必复制出多个平行子机。作者把这种更紧凑的形式称为 `SHSM`。它严格强于普通 `HSM`，也严格强于早先的 `CHSM` 限制版 context-dependent hierarchy，因此非常适合在当前演化树里补出“上下文标注语义”这条更细的支线。

- 形式主义定位：`HSM` 的 context-labeling / succinctness 扩展，用更少结构表达原本需要显式复制的上下文差异。
- 构造方式简述：模型仍由多个 machine 组成；每个 machine 有 nodes、entry、exits、expansion mapping 与 edges；不同之处在于 box 也允许带命题标签，并把这些标签继承给其展开子机里的所有状态。
- 基础设施与场景简述：纯理论条目，但直接给出 `SHSM` 相对 `HSM/CHSM` 的 succinctness 关系，以及 reachability、cycle detection、`LTL/CTL` 复杂度。

```text
hierarchical machine reuse -> box-level atomic-proposition labels -> context inheritance -> 更紧凑的 flat Kripke semantics -> model checking
```

## 形式主义定义与核心对象

### 定义对象

原文把 `SHSM` 定义成一组 machine。其核心增强只有一个：box 也带有 `true` 标签，展开后这些标签会被继承到所有后代状态。这使得“同一子机在不同上下文里拥有不同命题环境”可以不靠复制结构来实现。

### 核心抽象

原文给出的 `SHSM` 写作：

$$
M = (M_1,\ldots,M_k)
$$

每个 machine

$$
M_i = (N_i,in_i,out_i,true_i,expn_i,E_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是顶点集合。
2. `in_i \in N_i` 是初始顶点。
3. `out_i \subseteq N_i` 是输出顶点集合。
4. `true_i : N_i \to 2^{AP}` 为顶点分配原子命题集合。
5. `expn_i : N_i \to \{0,1,\ldots,k\}` 指出某个顶点是否展开成更低层 machine；`0` 表示普通节点。
6. `E_i` 是边集；边既可以从普通节点到普通节点，也可以从 box 的某个 output-port 返回。

原文进一步指出两个重要子类：

$$
\text{HSM} \subset \text{CHSM} \subset \text{SHSM}
$$

其中：

1. `HSM` 要求每个 box 的标签为空。
2. `CHSM` 要求祖先 box 与后代 machine 顶点的标签集合不相交。
3. `SHSM` 则不再保留这个限制。

### 一个最小例子与通俗解释

可以把它想成“复用同一计时子机，但在不同大模式下继承不同语义标签”的场景：

1. 顶层有两个 box，都展开到同一个子机 `M_j`。
2. 第一个 box 标注 `\{p_1\}`，第二个 box 标注 `\{p_2\}`。
3. 展开后，这两个上下文里的所有后代状态都会分别继承 `p_1` 或 `p_2`。

通俗地说，`SHSM` 像“允许大状态给整片子状态机统一贴一个上下文语义贴纸”的层次状态机。普通 `HSM` 只能在叶子节点上贴标签；`SHSM` 则允许在祖先 box 上贴，后代整体继承。

### 运行 / 接受 / 转移语义

原文使用 complete well-formed sequence 表示 flat state。可写成：

$$
X = \langle u_1u_2\cdots u_m \rangle
$$

上式中的符号逐项解释如下：

1. `u_1` 位于 top-level machine。
2. 若 `u_j` 是 box，则 `u_{j+1}` 位于它展开得到的下层 machine。
3. `u_m` 必须是普通 node。

`SHSM` 的 flat Kripke 结构记为：

$$
M^F
$$

其状态标签不再只看叶子节点，而是祖先链标签并集：

$$
true(X) = \bigcup_{j=1}^{m} true(u_j)
$$

这就是 `SHSM` 比 `HSM` 更紧凑的根源，因为上下文差异可以由祖先 box 直接携带，而无需复制整个子机。

### 语义边界

这篇论文清楚划出：

1. `SHSM` 没有增加并发、时间或变量。
2. 它只增强 labeling 语义，不改变 hierarchy 控制骨架。
3. `CHSM` 是它的受限子类，要求上下文标签和后代标签不冲突。
4. `HSM` 只是其最弱特例。

### 关键性质与判定边界

原文先给出 succinctness 结论：

$$
\text{SHSMs can be exponentially more succinct than CHSMs}
$$

同时，`CHSM` 又可以指数级强于 `HSM`。这说明 `SHSM` 不是表面上的小改动，而是真正改变了模型压缩能力。

在验证复杂度上，原文给出：

$$
\mathrm{Reachability}(\mathrm{SHSM}),\ \mathrm{CycleDetection}(\mathrm{SHSM}) \text{ are NP-complete}
$$

对 `LTL`：

$$
\mathrm{MC}_{LTL}(M,\varphi) = O(|M| \cdot 16^{|\varphi|})
$$

若 `M` 是 `CHSM`，则可改进为：

$$
\mathrm{MC}_{LTL}(M,\varphi) = O(|M| \cdot 8^{|\varphi|})
$$

对 `CTL`：

$$
\mathrm{MC}_{CTL}(M,\varphi) = O(|M| \cdot 4^{|\varphi| d})
$$

这里的 `d` 是 maximum number of exits。可见 `SHSM` 的更强 succinctness 直接换来了额外的验证代价。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | nodes + boxes 的层次骨架保持不变。 |
| 事件 / 触发 | 弱支持 | 主要是 graph-transition 语义。 |
| 守卫 / 数据 | 不支持 | 核心不在变量。 |
| 层次 | 强支持 | 仍是标准 hierarchy。 |
| 并发 / 同步 | 不支持 | sequential family。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | reachability、cycle、`LTL/CTL` 全覆盖。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `SHSM` 总体 | `$M=(M_1,\ldots,M_k)$` | 一组层次 machines。 |
| machine tuple | `$M_i=(N_i,in_i,out_i,true_i,expn_i,E_i)$` | 支持 box labeling 的 canonical 定义。 |
| flat state | `$X=\langle u_1\cdots u_m\rangle$` | 完整上下文链。 |
| context label | `$true(X)=\bigcup_{j=1}^{m} true(u_j)$` | box-level 标签继承的核心语义。 |
| 家族关系 | `$\text{HSM} \subset \text{CHSM} \subset \text{SHSM}$` | 说明 `SHSM` 是更强的一般化。 |

## 构造方式与承载格式

### 建模入口

1. 先按普通 `HSM` 一样定义 machines 与 expansion 关系。
2. 再决定哪些上下文性质更适合贴在 box 上，而不是复制出多个带不同叶子标签的子机。
3. 最后通过 `M^F` 的上下文标签并集语义得到整体 Kripke 结构。

### 机器可处理承载方式

主要包括：

1. machine tuple；
2. box labeling；
3. well-formed sequence；
4. flat Kripke structure `M^F`；
5. automata-theoretic model-checking reduction。

### 交换与互操作

它与现有谱系的关系非常直接：

1. 它一般化了 [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md) 的 plain `HSM`。
2. 它也一般化了 [hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md](../hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md) 里 non-recursive context-dependent line 的受限版本 `CHSM`。
3. 因而很适合作为“上下文标注 hierarchy”支线上的一个更强节点。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 box labeling 与 context inheritance。
- 仿真/执行支持：通过 `M^F` 可直接解释。
- 验证/分析支持：reachability、cycle detection、`LTL`、`CTL`。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要价值在语义压缩与复杂度边界。

## 适用场景与需求前提

### 适用场景

适合：

1. 同一子机需要在多个上下文中复用，但上下文命题标签不同。
2. 需要研究 hierarchy 上下文标注带来的 succinctness 增益。
3. 需要把 `HSM` 支线进一步细分到“context-labeling”方向。

### 需求前提

1. 系统仍是 sequential hierarchy。
2. 关注的上下文差异可以通过 atomic propositions 继承表达。
3. 接受更高的验证复杂度以换取更紧凑的模型。

### 不适用或高成本场景

如果根本不需要 box-level context labels，普通 `HSM` 就足够；如果还要递归调用，则应结合 `CDRSM` / `RSM` 视角继续扩展。

## 与相邻形式主义的关系

相对 `HSM`，`SHSM` 允许 box 带命题标签；相对 `CHSM`，`SHSM` 去掉了“祖先与后代标签不相交”的限制；相对 `CDHSM/CDRSM`，它更偏 non-recursive succinctness 一般化，而不是同时覆盖递归线。

## 与本研究的关系

### 对 Project 1 的价值

它让当前文库的层次状态机支线不只停留在“控制结构如何嵌套”，还能进一步表达“性质标签如何沿层次上下文传播”，这对后续把自然语言需求中的上下文语义压进模型非常有启发。

### 作为目标形式主义还是中间表示

更适合作为理论中间表示或谱系节点，而不是工业主语言。

### 对需求到模型生成的启发

如果需求中反复出现“只要处于某个大模式，其下所有细粒度状态都默认满足某类性质”这类上下文语义，LLM 应考虑 box-level labeling，而不是机械复制多个平行子机。

### 现实限制

它没有工程生态，而且 reachability / cycle complexity 已升到 `NP`-complete，更适合理论分析。

## 重要的相关工作

### 奠基或前身工作

- [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)
- [hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md](../hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md)

### 同类型或同家族工作

- `CHSM` 与 `CDHSM` 是它最直接的上下位关系条目。
- 若继续加入递归，则会与 `CDRSM / RSM` 支线相接。

## 文献分类总结

- 这篇论文严格属于 `HSM` 主枝上的语义扩展条目，而不是 DSL 或算法实现条目。
- 它对当前演化树的主要贡献，是把“context-dependent hierarchy”这条细分支线从 `CHSM` 推进到更一般的 `SHSM`。
- 因此它非常适合作为当前层次状态机理论支线下的新挂树节点。
