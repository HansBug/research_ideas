# 弱奇异混成自动机 / Weak Singular Hybrid Automata

## 基本信息

- 标题：Weak Singular Hybrid Automata
- 中文标题：弱奇异混成自动机
- 作者：Shankara Narayanan Krishna、Umang Mathur、Ashutosh Trivedi
- 发表：*Formal Modeling and Analysis of Timed Systems*, pp. 161-175, 2014
- DOI：`10.1007/978-3-319-10512-3_12`
- 链接：https://arxiv.org/pdf/1311.3826.pdf
- 形式主义：`Weak Singular Hybrid Automata (WSHA)`
- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型提出
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 `SHA` / `WSHA` tuple、rank function、run type 和 LP-style decidability proof skeleton。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 constant-rate modes、guard / reset、rank restriction 与 safety-set semantics。

## 简报

这篇论文在 `Hybrid Automata` 主干里补出了一条很重要但此前文库仍空着的线：**singular / constant-rate hybrid**。`WSHA` 的核心思想是把 `Singular Hybrid Automata` 限制成“rank 非递减的 mode 结构”，并要求同一 rank 内的 strongly connected part 本质上形成一个 `CMS` 风格的 constant-rate multi-mode system。这样既保留了比 `CMS` 更丰富的结构，又把若干关键问题从一般 `SHA` 的不可判边界拉回到了可判范围。

- 形式主义定位：`Hybrid Automata` 下 singular / constant-rate 支线上的可判定结构化子类。
- 构造方式简述：先从 `SHA` 出发，再附加 rank function、same-rank safety set 和 same-rank no-guard/no-reset 约束。
- 基础设施与场景简述：核心基础设施是 run type、线性规划式可达性检查、`NP` / `PSPACE` 复杂度边界，而不是工程执行框架。

```text
hybrid automaton -> singular hybrid automaton -> constant-rate multi-mode systems with structure -> WSHA -> decidable reachability / schedulability / LTL
```

## 形式主义定义与核心对象

### 定义对象

论文先回顾 `Singular Hybrid Automata (SHA)`，也就是每个 mode 的连续变量导数都是一个常向量的混成自动机。其基本 tuple 可写成：

$$
H = (M,M_0,\Sigma,X,\Delta,I,F)
$$

上式中的符号逐项解释如下：

1. `M` 是 modes 集合。
2. `M_0` 是初始 mode 集合。
3. `\Sigma` 是离散动作集。
4. `X` 是连续变量集。
5. `\Delta` 是离散转移关系。
6. `I` 是 mode invariants。
7. `F` 为每个 mode 指定常速率向量。

### 核心抽象

`WSHA` 在 `SHA` 的基础上增加一个 rank function：

$$
\varrho : M \to \mathbb N
$$

并要求：

$$
(m,G,a,R,m')\in\Delta \Rightarrow \varrho(m)\le \varrho(m')
$$

也就是说，离散迁移只能停在同 rank 或更高 rank 的 mode 上。对每个 rank `i`，论文还要求：

$$
M_i=\{m\mid \varrho(m)=i\}
$$

对应一个有界开多面体安全集 `S_i`，并满足：

$$
I(m)=S_i \quad \text{for all } m\in M_i
$$

同时，同一 rank 内部若有转移 `(m,G,a,R,m')`，则必须满足：

$$
G=\top,\qquad R=\varnothing
$$

这意味着 same-rank strongly connected component 内部像 `CMS` 一样可以自由切换，但不能再用 guard / reset 把结构搞回一般 `SHA` 的复杂度。

### 一个最小例子与通俗解释

一个直觉例子是把系统分成三个 rank：

1. `rank 0` 是“初始调整阶段”，几个模式之间可以自由切换，只要状态一直留在某个 bounded safety set 内。
2. 一旦满足某个外部 guard，系统沿离散边升到 `rank 1`，进入“主运行阶段”。
3. 再触发一次升级后进入 `rank 2` 的“收尾阶段”。

在每个 rank 内，系统像 constant-rate multi-mode system 那样自由切换；但一旦升 rank，就不能回到更低 rank。通俗地说，`WSHA` 像“被分层的 constant-rate hybrid system”，每一层内部很自由，层与层之间则单向推进。

### 运行 / 接受 / 转移语义

对 `SHA`，若当前配置是 `(m,\nu)`，在 mode `m` 中停留 `t` 时间并执行动作 `a` 后到达 `(m',\nu')`，则要求：

$$
(m,\nu)\xrightarrow{t,a}(m',\nu')
$$

满足：

$$
(\nu + F(m)\cdot \tau)\in [[I(m)]] \quad \text{for all } \tau\in[0,t]
$$

并且在离散跳转点：

$$
(\nu + F(m)\cdot t)\in [[G]],\qquad \nu' = (\nu + F(m)\cdot t)[R:=0]
$$

对 `WSHA` 而言，新增的是对 mode 结构的 rank 约束，而不是重新定义连续流本身。

### 语义边界

相对一般 `SHA`，`WSHA` 严格更弱，因为它限制了 rank 单调性和 same-rank 内部的 guard / reset；相对 `CMS`，它又更强，因为它允许多个 rank 之间存在结构化离散推进，而不只是一个平坦的自由切换集合。

### 关键性质与判定边界

论文最核心的结论是：

$$
\text{Reachability(WSHA)} \text{ and Schedulability(WSHA) are NP-complete}
$$

并且：

$$
\text{LTL model checking for WSHA is PSPACE-complete}
$$

与此同时，它也明确给出脆弱边界：

$$
\text{adding one unrestricted clock or unrestricted updates makes reachability undecidable}
$$

这说明 `WSHA` 的 decidability 不是偶然，而是精确依赖于这组结构约束。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | modes + rank structure 是模型核心。 |
| 事件 / 触发 | 支持 | 离散动作通过 `\Sigma` 与 `\Delta` 进入。 |
| 守卫 / 数据 | 部分支持 | 跨 rank 转移可有 guard / reset；same-rank 内部禁止 guard / reset。 |
| 层次 | 部分支持 | 不是 Harel 式层次，但 rank 提供了单调结构层次。 |
| 并发 / 同步 | 不支持 | 原始模型面向单体混成系统。 |
| 时间约束 | 强支持 | 连续时间与常速率流是模型基础。 |
| 连续动态 / 随机性 | 强支持连续、无随机 | 每个 mode 的流是 constant-rate vector。 |
| 可执行 / 可验证性 | 强理论支持 | reachability / schedulability / LTL 都有明确复杂度边界。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 母模型 | `$H=(M,M_0,\Sigma,X,\Delta,I,F)$` | `WSHA` 以 `SHA` 为母模型。 |
| rank 函数 | `$\varrho:M\to\mathbb N$` | 给 modes 增加单调层级结构。 |
| 单调性 | `$\varrho(m)\le \varrho(m')$` | 迁移不能回到更低 rank。 |
| same-rank 约束 | `$G=\top,\ R=\varnothing$` | 每个 rank 内部退化成 `CMS` 风格自由切换。 |
| 复杂度 | `Reach/Sched: NP-complete`, `LTL: PSPACE-complete` | 给 singular / constant-rate 支线一个稳定的 decidable frontier。 |

## 构造方式与承载格式

### 建模入口

建模时通常要先决定：

1. 哪些 modes 应属于同一个 constant-rate safety region。
2. 哪些切换必须视为“升 rank”的结构性阶段变化。
3. 哪些 guard / reset 是 truly necessary，哪些可以吸收到 same-rank `CMS` 语义里。

### 机器可处理承载方式

原文的机器可处理承载方式是：

1. `SHA` / `WSHA` 元组。
2. rank function 与 run type。
3. 基于多面体和 LP feasibility 的判定框架。

### 交换与互操作

它和 [the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md) 的 `Hybrid Automata` 母线、[the-algorithmic-analysis-of-hybrid-systems/desc.md](../the-algorithmic-analysis-of-hybrid-systems/desc.md) 的 linear hybrid branch，以及 [the-theory-of-rectangular-hybrid-automata/desc.md](../the-theory-of-rectangular-hybrid-automata/desc.md) 的可判定边界工作互补：后两者偏几何 / 线性约束可判定性，这篇则补出 constant-rate / singular 方向。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 run type、rank partition 和 LP-style feasibility reasoning。
- 仿真/执行支持：按 `SHA` 语义可直接执行。
- 验证/分析支持：reachability、schedulability、LTL / CTL complexity boundary、undecidable variants。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：属于 hybrid automata 理论中 singular / constant-rate 支线的经典 family 节点。

## 适用场景与需求前提

### 适用场景

适合那些连续流在每个 mode 内是常速率，且系统天然可以分成若干单调阶段的 hybrid system。

### 需求前提

1. 连续变量在每个 mode 内最好是 constant-rate。
2. 系统结构应能自然分成非递减 rank。
3. 同一阶段内部最好不依赖复杂 guard / reset，而更像自由 mode scheduling。

### 不适用或高成本场景

若系统需要同一层内频繁 guard / reset，或必须允许 rank 回退，这个 family 的 decidability 就很难保住。

## 与相邻形式主义的关系

相对一般 `Hybrid Automata`，`WSHA` 是更受限的可判定子类；相对 `CMS`，它通过 rank 把平坦 constant-rate system 结构化；相对 [the-theory-of-rectangular-hybrid-automata/desc.md](../the-theory-of-rectangular-hybrid-automata/desc.md)，这里的可判定性不依赖矩形导数区间，而依赖 rank + same-rank structural discipline。

## 与本研究的关系

### 对 Project 1 的价值

它把 `Hybrid Automata` 主干继续细化到 singular / constant-rate 方向，使混成分支不再只围绕 rectangular / o-minimal / PCD 一侧扩树。

### 作为目标形式主义还是中间表示

更适合作为理论选型节点或后续更工程化 constant-rate hybrid model 的中间抽象。

### 对需求到模型生成的启发

如果需求天然包含“系统分阶段推进、每阶段内部只有常速率连续演化、阶段之间单向切换”，那么 LLM 生成 `WSHA` 会比一般 `HA` 更容易保住可验证性。

### 现实限制

一旦放松 unrestricted clock 或 unrestricted update，reachability 立即回到不可判边界。

## 重要的相关工作

### 奠基或前身工作

- [the-theory-of-hybrid-automata/desc.md](../the-theory-of-hybrid-automata/desc.md)
- [the-algorithmic-analysis-of-hybrid-systems/desc.md](../the-algorithmic-analysis-of-hybrid-systems/desc.md)

### 同类型或同家族工作

- `Singular Hybrid Automata`
- `Constant-Rate Multi-Mode Systems`

### 标准 / 格式 / 工具链工作

- 原文没有工程标准或公开工具；最重要的基础设施是 rank discipline 与 run-type-based decision procedure。

### 与本研究关系最紧的工作

- 这篇条目最适合挂成 `Hybrid Automata -> Singular / Constant-Rate Hybrid 支线 -> Weak Singular Hybrid Automata`。

## 文献分类总结

- 主类：🌊 混成/随机扩展
- 对象类型：🧱 模型本体
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🧮 形式语言与自动机理论
