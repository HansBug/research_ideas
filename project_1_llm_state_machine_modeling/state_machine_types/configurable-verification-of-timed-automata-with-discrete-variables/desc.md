# 带离散变量的时间自动机可配置验证 / Configurable verification of timed automata with discrete variables

## 基本信息

- 标题：Configurable verification of timed automata with discrete variables
- 中文标题：带离散变量的时间自动机可配置验证
- 作者：Tamás Tóth，István Majzik
- 发表：*Acta Informatica*，59:1-35，2022
- DOI：`10.1007/s00236-020-00393-4`
- 链接：https://doi.org/10.1007/s00236-020-00393-4
- 形式主义：`Timed Automata with discrete variables / configurable lazy abstraction / Theta`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：configurable lazy-abstraction framework for timed automata with clocks and discrete data, implemented in `Theta`
- 工具/实现获取方式：原文明确说明其算法框架已经在开源模型检查框架 `Theta` 中实现，并据此评测多种配置。
- 标准/格式获取方式：承载对象是带 discrete variables 的 timed automata、symbolic semantics、`ART`、abstract domains、`LU`/interpolation-based refiners 与 `Theta` 内部 workflow；不是独立交换标准。

## 简报

这篇论文补的是 timed verification 中一个很现实的裂口：很多工业实时模型并不只有 clocks，还带一批整数或枚举变量。只用 zone abstraction 只看 clocks 往往不够，而把所有离散变量都全量显式化又会迅速爆炸。本文的贡献，是把“时钟抽象”和“离散变量抽象”统一进一个可组合的 lazy-abstraction 框架里，让用户能自由组合 `LU`、zone interpolation、显式离散值跟踪、valuation interpolation 等策略。

- 形式主义定位：带离散变量的 `Timed Automata` 验证框架，不是新的 timed-language 母型。
- 构造方式简述：先把模型写成同时含 clocks 和 discrete variables 的 timed automaton，再用 `ART` 组织懒惰搜索，并用 direct-product abstract domains 分别处理 clocks 与 discrete part。
- 基础设施与场景简述：依托 symbolic semantics、`ART`、zone abstraction、interpolation、`LU` bounds、valuation visibility 与 `Theta` 实现，服务含时钟与整数控制变量的 reachability verification。

```text
timed automaton with clocks + discrete vars -> abstract reachability tree -> clock abstraction × discrete abstraction -> local refinement -> Theta verification
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. 带离散变量的 timed automata；
2. symbolic semantics；
3. abstract reachability tree (`ART`)；
4. abstract domains；
5. direct-product abstraction 与可配置 refinement。

### 核心抽象

论文直接给出语法元组：

$$
A = (L, C, D, T, \ell_0)
$$

上式中的符号逐项解释如下：

1. `L` 是 location 集合。
2. `C` 是连续 clock 变量集合。
3. `D` 是离散 data 变量集合。
4. `T \subseteq L \times P(Constr) \times Update^\ast \times L` 是迁移集合。
5. `\ell_0` 是初始 location。

其符号语义把单个 valuation 扩成 valuation 集，写成：

$$
(\ell, \Sigma) \xrightarrow{t} (\ell', \Sigma') \quad \text{with} \quad \Sigma' = post_t(\Sigma)
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是 concrete states 的集合。
2. `t=(\ell,\cdot,\cdot,\ell')` 是一条迁移。
3. `post_t` 先执行 action，再考虑时间推进。
4. 这一步把普通 operational semantics 抬升到了 symbolic state level。

框架层的抽象域写成：

$$
\mathcal D = (S, \preceq, init, post, \llbracket \cdot \rrbracket)
$$

上式中的符号逐项解释如下：

1. `S` 是抽象状态集合。
2. `\preceq` 是覆盖或包含意义上的 preorder。
3. `init` 是抽象初始状态。
4. `post` 是抽象 post-image。
5. `\llbracket \cdot \rrbracket` 是 concretization。

本文最关键的组合手段是 direct product：

$$
\mathcal D_1 \times \mathcal D_2 = (S_1 \times S_2, \preceq, init, post, \llbracket \cdot \rrbracket)
$$

其中

$$
(s_1, s_2) \preceq (s'_1, s'_2) \iff s_1 \preceq_1 s'_1 \land s_2 \preceq_2 s'_2
$$

$$
\llbracket (s_1, s_2) \rrbracket = \llbracket s_1 \rrbracket_1 \cap \llbracket s_2 \rrbracket_2
$$

上式中的符号逐项解释如下：

1. 第一维通常处理 clocks。
2. 第二维通常处理 discrete variables。
3. 覆盖关系按分量同时成立。
4. concretization 则取两个抽象的交。
5. 这正是“时钟抽象 + 离散抽象可自由拼接”的数学基础。

### 一个最小例子与通俗解释

一个最小直觉例子是：

1. 系统有 clocks 控制 timeout，同时还有一个整数模式变量 `m`。
2. 仅用 zone abstraction 时，clock 关系能被压缩，但 `m` 的不同取值会把状态空间撕开。
3. 若某条伪反例其实只是因为 `m` 这个变量当前“看得太粗”，就只细化 discrete part。
4. 若问题来自 clocks，则只细化 zone / interpolation 部分。

通俗地说，这篇论文把 timed verification 里的“时钟太粗”与“离散变量太粗”拆开了，不再要求你每次都把整个状态空间一起加精。

### 运行 / 接受 / 转移语义

论文把 lazy search 组织成 `ART`。其 well-labeledness 的核心条件之一可写成：

$$
post_t(\llbracket s_m \rrbracket) \subseteq \llbracket s_n \rrbracket
$$

上式中的符号逐项解释如下：

1. `m` 是 `n` 的父节点。
2. `s_m`、`s_n` 分别是对应节点上的抽象状态。
3. `post_t` 是 concrete semantics 下的后继。
4. 若该包含成立，说明抽象节点 `n` soundly over-approximate 了真实后继。

节点覆盖则要求：

$$
\llbracket s_n \rrbracket \subseteq \llbracket s_{n'} \rrbracket
$$

这意味着当某个节点已被另一个同 location 节点覆盖时，可以在 `ART` 上剪枝。

### 语义边界

1. 论文主问题是 location reachability，不是更一般的时序逻辑模型检查。
2. 目标仍是 timed automata family，只是把离散变量纳入同一框架。
3. 强项在 configurability，而不是某一种单独抽象在所有 benchmark 上都最好。
4. 若只用 interpolation 且不配合合适 termination discipline，并不保证普遍终止。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 语法元组 | `$A = (L, C, D, T, \ell_0)$` | 把 clocks 与 discrete vars 同时纳入 timed automata。 |
| symbolic post | `$\Sigma' = post_t(\Sigma)$` | 从 concrete semantics 抬升到 symbolic semantics。 |
| 抽象域 | `$\mathcal D = (S, \preceq, init, post, \llbracket \cdot \rrbracket)$` | 统一表达多种 abstraction strategies。 |
| 直积抽象 | `$\mathcal D_1 \times \mathcal D_2$` | clocks 和 discrete part 可组合。 |
| 覆盖条件 | `$\llbracket s_n \rrbracket \subseteq \llbracket s_{n'} \rrbracket$` | `ART` 剪枝的核心逻辑。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | location + symbolic state 是主对象。 |
| 事件 / 触发 | 很强 | transitions、guards、updates 都是一等对象。 |
| 守卫 / 数据 | 很强 | 同时处理 clock constraints 与 discrete-variable visibility。 |
| 层次 | 不支持 | 不是层次状态机框架。 |
| 并发 / 同步 | 条件支持 | 可处理 networked models，但论文重点在 abstraction framework。 |
| 时间约束 | 很强 | zone、`LU`、interpolation 都围绕 clocks。 |
| 连续动态 / 随机性 | 不支持 | 不涉及 hybrid or probabilistic flow。 |
| 可执行 / 可验证性 | 很强 | 已在 `Theta` 中实现多种配置并系统评测。 |

## 构造方式与承载格式

### 建模入口

原文的主要入口包括：

1. 带 clocks 与 discrete vars 的 timed automata；
2. symbolic semantics；
3. `ART`；
4. configurable refiners over clock and discrete dimensions。

### 机器可处理承载方式

机器可处理承载方式包括：

1. zones / `DBM`；
2. explicit or partially hidden valuations；
3. interpolation results；
4. `ART` node labels and covering relation。

### 交换与互操作

互操作重点在框架层：

1. `LU`-style timed abstraction 可作为 clock-side component。
2. valuation interpolation / explicit tracking 可作为 discrete-side component。
3. 两边通过 direct-product domain 在 `Theta` 中无缝组合。

## 配套基础设施

- 建模/编辑工具：论文不主打建模器；默认模型由 `Theta` 或其前端工作流提供。
- 解析/交换/元模型支持：核心承载是 symbolic semantics、`ART` 和 abstract domains，不是中立交换格式。
- 仿真/执行支持：重点不在仿真，而在 lazy reachability checking。
- 验证/分析支持：`LU` abstraction、zone interpolation、valuation interpolation、explicit-value abstraction、local refinement。
- 代码生成/转换支持：不主打代码生成；重点是抽象与 refinement 配置组合。
- 标准化或社区生态：落地在开源 `Theta`，可与 state-of-the-art timed verification 方法比较。

## 适用场景与需求前提

### 适用场景

适合那些已经需要 `Timed Automata`，但又无法忽略整数模式、计数器、配置标志等离散变量的实时控制和协议模型。

### 需求前提

1. 系统需可写成 location + clocks + discrete updates 的 timed automaton。
2. 团队愿意接受 lazy abstraction / local refinement 工作流。
3. 目标主要是 reachability，而不是完整的 temporal-property suite。

### 不适用或高成本场景

如果模型的离散部分太接近通用程序语义，或者需要 richer arithmetic/heap reasoning，仅靠本文框架也会变重。

## 与相邻形式主义的关系

相对 [using-non-convex-approximations-for-efficient-analysis-of-timed-automata/desc.md](../using-non-convex-approximations-for-efficient-analysis-of-timed-automata/desc.md)，后者还只在纯时钟抽象上优化，这里把离散变量也纳入统一框架；相对 [reachability-for-updatable-timed-automata-made-faster-and-more-effective/desc.md](../reachability-for-updatable-timed-automata-made-faster-and-more-effective/desc.md)，那篇强调 richer clock updates 的 static analysis，这篇强调 clocks × discrete vars 的可配置抽象；相对 [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md)，本文把 `LU` 作为可插拔组件之一，而不是最终结论本身。

## 与本研究的关系

### 对 Project 1 的价值

它非常贴近 `project_1` 未来可能遇到的真实情况：生成出的 timed model 往往不会只有 clocks，还会混着离散模式和数据变量。

### 作为目标形式主义还是中间表示

对 `project_1` 而言，这更像验证后端或中间表示侧证，而不是最终面向用户的建模语言。

### 对需求到模型生成的启发

1. 需求建模时应尽量区分“真正需要时钟精化的部分”和“只需要离散变量可见性的部分”。
2. LLM 生成模型后，修模时不必总是整体重算，完全可以按 clocks / discrete 两侧局部加精。
3. 这类 configurable framework 适合做“生成-验证-修复”闭环里的 verification kernel。

### 现实限制

本文的结论主要落在 reachability，且具体哪种配置最优仍依赖 benchmark 类别。

## 重要的相关工作

### 奠基或前身工作

1. `LU` abstraction 与 zone interpolation 主线。
2. lazy abstraction / `ART` 主线。

### 同类型或同家族工作

1. [using-non-convex-approximations-for-efficient-analysis-of-timed-automata/desc.md](../using-non-convex-approximations-for-efficient-analysis-of-timed-automata/desc.md)：纯 clocks backend 侧。
2. [reachability-for-updatable-timed-automata-made-faster-and-more-effective/desc.md](../reachability-for-updatable-timed-automata-made-faster-and-more-effective/desc.md)：richer timed update 侧。

### 标准 / 格式 / 工具链工作

1. `Theta`：本文明确给出实现与实验平台。

### 与本研究关系最紧的工作

1. 含 discrete variables 的 timed automata verification。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🛠️ 方法路线
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Timed Automata with discrete variables / configurable lazy abstraction / Theta`
- 论文角色：configurable lazy-abstraction framework for timed automata with clocks and discrete data, implemented in `Theta`
- 核心功能：把 clocks 与 discrete variables 的多种 abstraction/refinement 统一成可组合的 lazy reachability framework
- 关键特性：`ART`、direct-product domains、`LU`、zone interpolation、valuation interpolation、`Theta`
- 构造方式：`TA + discrete vars -> ART -> clock abstraction × discrete abstraction -> local refinement`
- 基础设施：`Theta`、zones / `DBM`、interpolation、explicit-value and visibility-based discrete abstractions
- 适用场景：含 clocks 与整数模式变量的实时控制 / 协议 reachability verification
- 需求前提：系统需能写成 timed automaton，并接受 lazy abstraction / configurable refinement 工作流
- 状态：🟢 直接可用
