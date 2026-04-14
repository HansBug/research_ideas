# 递归概率系统的模型检验 / Model Checking of Recursive Probabilistic Systems

## 基本信息

- 标题：Model Checking of Recursive Probabilistic Systems
- 中文标题：递归概率系统的模型检验
- 作者：Kousha Etessami、Mihalis Yannakakis
- 发表：*ACM Transactions on Computational Logic*, 13(2), pp. 1-40, 2012
- DOI：`10.1145/2159531.2159534`
- 链接：https://homepages.inf.ed.ac.uk/kousha/etessami_yannakakis_model_checking_rmcs_acm_tocl_2012.pdf
- 形式主义：`Recursive Probabilistic Systems / Recursive Markov Chains (RPS / RMC)`
- 主类：🌊 混成 / 随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / `RMC` model-checking family consolidation
- 工具/实现获取方式：原文未提供公开实现；机器可处理入口是 `RMC` tuple、`Buchi` / `LTL` satisfaction probability、`1-exit` 与 `linearly-recursive` 子类，以及 `pPDS` 等价翻译。
- 标准/格式获取方式：原文没有 DSL 或交换格式；核心承载方式是 `RMC` component tuple、`LFP` 语义、多项式系统与自动机 / 逻辑规格。

## 简报

这篇 `TOCL` 论文不是简单重印 `RMC`。它把 `RMC` 的 `Buchi` 与 `LTL` model checking 放到同一处系统整理，并把 `1-exit RMC`、`linearly-recursive RMC`、`pPDS` 等价、精确概率与复杂度边界一起补齐。对当前文库来说，它最适合作为 `RMC` 节点的 journal-level family consolidation 条目，同时也让 `1-exit` 与 `linearly-recursive` 这两个子类不再只靠 conference 版零散支撑。

- 形式主义定位：`RMC` family 的 journal full version，也是 `RMC -> 1-exit / linearly-recursive` 细分支的系统整理条目。
- 构造方式简述：仍以 components、boxes、entry/exit 和概率边建模，只是把 `omega`-regular automata 与 `LTL` 两条规格入口统一到同一篇里。
- 基础设施与场景简述：原文直接说明一般 `RMC` 与 probabilistic pushdown systems 等价，并把 `SCFG/MT-BP` 等 `1-exit` 对应再写了一遍，因此特别适合做 family-level 总结。

```text
RMC family -> omega-regular / LTL specifications -> qualitative / quantitative probabilities -> 1-exit / linearly-recursive subfamilies
```

## 形式主义定义与核心对象

### 定义对象

原文研究的“recursive probabilistic systems”在 formal core 上仍是 `RMC`。这里把 `RPS` 理解为 journal-level 的命名口径，而把 `RMC` 视为正文真正落到 tuple 和语义上的模型本体，这是基于原文定义部分的保守整理。

### 核心抽象

原文继续使用：

$$
A=(A_1,\ldots,A_k),\qquad A_i=(N_i,B_i,Y_i,En_i,Ex_i,\delta_i)
$$

上式中的符号逐项解释如下：

1. `A_i` 是第 `i` 个递归组件。
2. `N_i` 是 ordinary nodes。
3. `B_i` 是 boxes。
4. `Y_i` 把 box 映到被调用组件。
5. `En_i` 与 `Ex_i` 是接口。
6. `\delta_i` 是概率转移。

原文再次强调：

1. `RMCs are a probabilistic version of Recursive State Machines`。
2. `SCFGs` 对应 `1-exit RMCs`。
3. 一般 `RMCs` 与 `pPDSs` 可高效互译。

### 一个最小例子与通俗解释

最小直觉例子仍可理解成：

1. 一个顶层过程进入某个 box。
2. box 调用另一个概率组件。
3. 被调组件要么在某个 exit 返回，要么继续递归调用。
4. 最终整条运行是一个无限随机 execution，外部用 `Buchi` automaton 或 `LTL` 公式看它是否满足性质。

通俗地说，`RMC` 在这里就像“带无限调用栈的随机程序流程图”，而这篇文章的作用是把“它能验什么性质、哪些子类更规整”系统写全。

### 运行 / 接受 / 转移语义

原文把规格接受概率写成：

$$
P_A(L(B))
$$

上式中的符号逐项解释如下：

1. `A` 是给定 `RMC`。
2. `B` 是 `Buchi automaton`。
3. `L(B)` 是 `B` 的 `omega`-语言。
4. `P_A(L(B))` 是 `A` 的随机运行满足该语言的概率。

对 `LTL`，原文则直接讨论：

$$
P_A(\varphi)
$$

上式中的符号逐项解释如下：

1. `\varphi` 是 `LTL` 公式。
2. 其意义是同一随机执行满足该 `LTL` 性质的概率。

entry-exit probability 仍由多项式 fixed-point 给出：

$$
q^*=\mathrm{LFP}(P)
$$

这里 `q^*` 收集所有 entry-exit termination / reachability probabilities，`P` 是从组件结构诱导的单调多项式算子。

### 语义边界

原文把几个最值得保留的 family 边界并列出来：

1. `1-exit RMC`；
2. `linearly-recursive RMC`；
3. 一般 `RMC`；
4. 与 `pPDS` 的等价口径。

其中 `linearly-recursive RMC` 最适合挂树，因为它不是单纯“参数更小”，而是有清楚结构限制并带来 exact-probability 正结果。

### 关键性质与判定边界

对当前文库最关键的几点可压成：

$$
\text{qualitative model checking is polynomial-space in } |A|
$$

以及

$$
\text{for linearly-recursive RMCs, exact probabilities are computable in time polynomial in } |A|
$$

这两句真正重要的含义是：

1. 一般 `RMC` 已经是成熟的 temporal-verification 对象。
2. `1-exit` 与 `linearly-recursive` 确实形成值得保留的 classic subfamilies。
3. 这篇 journal 版把它们写成了 family-level 口径，而不只是 conference paper 的局部现象。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | component、box、entry/exit 与 stack-based execution 都保留。 |
| 事件 / 触发 | 弱支持 | 核心仍是概率控制流，而不是显式事件代数。 |
| 守卫 / 数据 | 不支持 | 无显式程序变量。 |
| 层次 | 强支持 | 递归 component hierarchy 是模型本体。 |
| 并发 / 同步 | 不支持 | 仍是 sequential family。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 强支持 | 概率转移是母线扩展。 |
| 可执行 / 可验证性 | 强理论支持 | `Buchi` / `LTL`、qualitative / quantitative、`1-exit` / `lr-RMC` 全部系统化。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `RMC` tuple | `$A=(A_1,\ldots,A_k)$` | family 的核心骨架。 |
| component tuple | `$A_i=(N_i,B_i,Y_i,En_i,Ex_i,\delta_i)$` | 说明其仍是 `RSM` 式 component interface。 |
| `Buchi` satisfaction probability | `$P_A(L(B))$` | `omega`-regular 规格入口。 |
| `LTL` satisfaction probability | `$P_A(\varphi)$` | direct temporal-logic 入口。 |
| fixed-point semantics | `$q^*=\mathrm{LFP}(P)$` | 概率语义的正式落点。 |

## 构造方式与承载格式

### 建模入口

1. 先建立 `RMC` component graph。
2. 用 atomic propositions 标记顶点。
3. 根据需求选择 `Buchi` 或 `LTL` 规格入口。
4. 若系统结构更窄，再判断是否属于 `1-exit` 或 `lr-RMC`。

### 机器可处理承载方式

主要包括：

1. `RMC` tuple；
2. `LFP` 多项式系统；
3. `Buchi` automata；
4. `LTL` formulas；
5. `pPDS` translation。

### 交换与互操作

1. 向上承接 [algorithmic-verification-of-recursive-probabilistic-state-machines/desc.md](../algorithmic-verification-of-recursive-probabilistic-state-machines/desc.md)。
2. 向旁边与 [checking-ltl-properties-of-recursive-markov-chains/desc.md](../checking-ltl-properties-of-recursive-markov-chains/desc.md) 一起固定 `lr-RMC` 口径。
3. 向下再接 [recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md](../recursive-markov-decision-processes-and-recursive-stochastic-games-jacm/desc.md) 的 controlled/game recursive family。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：`RMC` 与 `pPDS` 的互译关系很关键。
- 仿真/执行支持：可按全局 Markov chain 运行。
- 验证/分析支持：`Buchi`、`LTL`、qualitative / quantitative analysis、exact probability for `lr-RMC`。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：是 probabilistic pushdown / recursive stochastic systems 社区的经典 journal consolidation 条目。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归概率控制流上的 `omega`-regular / `LTL` 性质分析。
2. 需要 journal-level family 边界而不只看 conference 原型条目的场景。
3. 需要把 `1-exit` 与 `lr-RMC` 当作独立 subtype 处理的扩树任务。

### 需求前提

1. 系统核心是 sequential recursive stochastic family。
2. 规格偏长期时序性质。
3. 过程接口宽度可有限化。

### 不适用或高成本场景

如果需求需要 control/game players，应转向 `RMDP/RSSG/RCSG`；如果系统是 open / partial-observation hierarchy，应转向 `OPD` family。

## 与相邻形式主义的关系

相对 conference 版 `RMC` 条目，这篇文章更像 family consolidation；相对 `RMDP/RSSG`，它仍保持无玩家分区的纯随机 family；相对 `pPDS`，它保留 component/box 的层次结构。

## 与本研究的关系

### 对 Project 1 的价值

它让 `RMC` 节点不只是一篇早期定义论文，而是一个已经补全 `Buchi/LTL/1-exit/lr-RMC/pPDS` 语义外延的稳定 family 节点。

### 作为目标形式主义还是中间表示

对递归概率过程，它可以直接作为目标形式主义；对一般需求到模型自动化，它更像高表达力理论落点与 family 参考。

### 对需求到模型生成的启发

若需求本身带有递归调用与满足概率叙述，LLM 不应急着把它平面化为普通 `Markov chain`，而应优先判断是否需要 `RMC`，以及是否进一步落在 `1-exit/lr-RMC` 子类。

## 重要的相关工作

1. [algorithmic-verification-of-recursive-probabilistic-state-machines/desc.md](../algorithmic-verification-of-recursive-probabilistic-state-machines/desc.md)：conference origin。
2. [checking-ltl-properties-of-recursive-markov-chains/desc.md](../checking-ltl-properties-of-recursive-markov-chains/desc.md)：`lr-RMC` 与 direct `LTL` 入口。
3. [recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md](../recursive-markov-chains-stochastic-grammars-and-monotone-systems-of-nonlinear-equations-jacm/desc.md)：`RMC/HMC` 的 reachability / family-boundary 主条目。

## 文献分类总结

- 这篇论文属于 `🌊 混成 / 随机扩展`。
- 这篇论文的对象类型是 `🧱 模型本体`。
- 这篇论文描述的客体是 `🎛️ 控制 / 反应式逻辑`。
- 这篇论文所属领域是 `🧮 形式语言与自动机理论`。

它最适合挂到当前演化树的 `RMC/HMC` 节点上，作为 `RMC -> 1-exit / linearly-recursive` 这两个子类被 journal-level 系统化整理后的代表条目。
