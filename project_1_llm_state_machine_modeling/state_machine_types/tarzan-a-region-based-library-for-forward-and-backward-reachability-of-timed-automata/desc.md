# Tarzan：面向时间自动机前向与后向可达性的区域库 / Tarzan: A Region-Based Library for Forward and Backward Reachability of Timed Automata

## 基本信息

- 标题：Tarzan: A Region-Based Library for Forward and Backward Reachability of Timed Automata
- 中文标题：Tarzan：面向时间自动机前向与后向可达性的区域库
- 作者：Andrea Manini，Matteo Rossi，Pierluigi San Pietro
- 发表：arXiv 预印本 `arXiv:2602.15435`，2026（当前目录中的 `paper.pdf` 为扩展版）
- DOI：原文未提供
- 链接：https://arxiv.org/abs/2602.15435
- 形式主义：`timed automata / region abstraction / Tarzan`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：region-based timed-automata reachability library / forward-backward backend
- 工具/实现获取方式：原文明确给出库入口 `https://github.com/andreamanini98/TARZAN`，并给出 artifact DOI `10.5281/zenodo.18656202`；实现采用 `C++20`。
- 标准/格式获取方式：主承载是 `TA` 模型、region 数据结构和 reachability API；原文未给独立交换标准。

## 简报

`Tarzan` 补的是 timed-automata 验证生态里一个很新的空缺：大家都知道 zone / `DBM` 是事实标准，但 region-based 路线在某些 `TA` 子类上其实更强，尤其对 punctual guards、closed `TA` 和必须做 backward analysis 的场景。`Tarzan` 的做法不是复述经典 region，而是引入一种更细的 region 表示，额外记录“哪些时钟先变成 unbounded”，从而把 backward predecessor 的组合爆炸压住。

- 形式主义定位：`Timed Automata` 的 region-based reachability library / backend。
- 构造方式简述：`TA` 先压成带 ordered unbounded clocks 的 region，再计算 discrete successor / predecessor 与 immediate delay predecessor。
- 基础设施与场景简述：依托 `C++20`、GitHub、Zenodo artifact，并与 `Uppaal`、`TChecker` 做实验对比，服务 closed `TA`、punctual-guard `TA` 和 timed games 一类需要 backward exploration 的问题。

```text
timed automaton -> ordered region abstraction -> forward/backward region operations -> reachability or safety result
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. timed automata (`TA`)；
2. clock-equivalence / region abstraction；
3. ordered unbounded clocks；
4. discrete successors 与 immediate delay predecessors；
5. `Tarzan` region-based library。

### 核心抽象

论文直接给出时间自动机定义：

$$
A = (Act, Q, Q_0, X_A, T, Inv)
$$

上式中的符号逐项解释如下：

1. `$Act$` 是有限动作集合。
2. `$Q$` 是 location 集合。
3. `$Q_0 \subseteq Q$` 是初始 location 集合。
4. `$X_A$` 是时钟集合。
5. `$T$` 是带 guard 与 reset 集合的迁移关系。
6. `$Inv : Q \to \Gamma(X_A)$` 为每个 location 指派 invariant。

论文还明确使用经典配置语义：

$$
TS(A) = (S, Act \cup \mathbb{R}_{\ge 0}, I, \to)
$$

上式中的符号逐项解释如下：

1. `$S = Q \times Eval_A$` 是由 location 与时钟赋值组成的状态空间。
2. `$I$` 是所有初始配置。
3. `$\to$` 同时包含 discrete transitions 与 delay transitions。

本文最关键的新贡献，是 region 的新表示：

$$
R = \{q, h, X_{-\ell}, X_{-(\ell-1)}, \ldots, X_{-1}, X_0, X_1, \ldots, X_r\}
$$

上式中的符号逐项解释如下：

1. `$q$` 是当前 location。
2. `$h : X_A \to \{0,\ldots,c_m\}$` 记录各时钟的整数部分。
3. `$X_{-\ell}, \ldots, X_{-1}$` 表示已经 unbounded 的时钟集合，并编码“谁先变成 unbounded”。
4. `$X_0$` 表示当前没有小数部分的 bounded clocks。
5. `$X_1, \ldots, X_r$` 按小数部分大小规律排列其余 bounded clocks。

### 一个最小例子与通俗解释

论文自己的例子很适合说明新表示：

1. 假设时钟集合为 `x, y, z, w`，最大常数 `c_m = 5`。
2. `x, y` 都落在 `(2,3)`，且两者小数部分相等。
3. `z, w` 都已经超过 `5`，但 `z` 比 `w` 更早成为 unbounded。
4. 这种 region 在 `Tarzan` 里不会只记“`z,w` 都大于 `c_m`”，还会额外保留两者进入 unbounded 的顺序。

通俗地说，经典 region 更像“只记住时钟现在在哪一格”，`Tarzan` 则多记了一层“它是按什么先后顺序冲出边界的”。这对 backward predecessor 计算特别关键。

### 运行 / 接受 / 转移语义

论文首先沿用经典时钟等价：

$$
v \cong v'
$$

其含义是：当两个时钟赋值在整数部分、零小数部分和 bounded clocks 的小数排序上都一致，且 unbounded clocks 的情形满足定义条件时，它们属于同一时钟 region。

区域上的后继 / 前驱语义则围绕以下对象展开：

$$
[s'] = (q', [v'])
$$

上式中的符号逐项解释如下：

1. `$[v']$` 是赋值 `$v'$` 所属的 clock region。
2. `$[s']$` 是 location 与该 clock region 组合成的 state region。
3. `Tarzan` 在这些离散 region 上计算 discrete successors 与 immediate delay predecessors。

论文特别强调新表示带来的关键边界：

$$
\text{any region has at most three immediate delay predecessors}
$$

这条性质是新 region 表示的核心收益之一，因为它显著抑制了 backward analysis 中对 unbounded clocks 全排序枚举的爆炸。

### 语义边界

1. `Tarzan` 当前只支持 `TA` reachability，不是完整 timed-logic platform。
2. 区域法在 closed `TA`、punctual guards 上更强，但常数很大且 strict guards 多时 zones 仍常常更优。
3. 工具的价值主要在 backend abstraction，而不是前端建模语言。
4. backward algorithms 是亮点，也意味着它非常适合作为 timed-game / safety reasoning 的后端基座。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TA` 元组 | `$A = (Act, Q, Q_0, X_A, T, Inv)$` | 论文直接采用的时间自动机对象。 |
| 经典配置语义 | `$TS(A) = (S, Act \cup \mathbb{R}_{\ge 0}, I, \to)$` | 前向 / 后向 reachability 的底层语义。 |
| 新 region 表示 | `$R = \{q, h, X_{-\ell}, \ldots, X_r\}$` | `Tarzan` 的核心数据结构。 |
| 时钟等价 | `$v \cong v'$` | region abstraction 的基本划分关系。 |
| backward 关键性质 | `$\text{at most three immediate delay predecessors}$` | 新表示相比传统 region 的主要优势。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 直接面向 `TA` location + clock valuations。 |
| 事件 / 触发 | 很强 | `Act` 与 discrete transitions 是基础对象。 |
| 守卫 / 数据 | 中等支持 | 强在 clock guards，不主打复杂数据变量。 |
| 层次 | 不支持 | 不是层次状态机。 |
| 并发 / 同步 | 中等支持 | 能处理网络化 `TA`，但重点仍是 region backend。 |
| 时间约束 | 很强 | 全文核心就是时钟约束与 region abstraction。 |
| 连续动态 / 随机性 | 不支持 | 不属于 hybrid / stochastic family。 |
| 可执行 / 可验证性 | 很强 | 前向与后向 reachability 都已实现并与 `Uppaal/TChecker` 对比。 |

### 形式化问题与性质

1. `Tarzan` 的真正贡献不在“又做一个 `TA` 工具”，而在把 region-based 路线重新工程化，并显式补上 backward analysis。
2. ordered unbounded clocks 是它区别于经典 region 表示的关键。
3. 它和 `TChecker/Uppaal` 不是替代关系，而是互补的 backend choice。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 标准 `Timed Automata`；
2. closed / punctual-guard `TA`；
3. 网络化 `TA` reachability 问题；
4. backward safety / timed-game style analysis。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `TA` tuple；
2. ordered-region data structure；
3. discrete successor / predecessor routines；
4. forward / backward reachability engine。

### 交换与互操作

1. 论文明确把 `Tarzan` 定位为可集成进现有 timed-verification 工具的库。
2. 它与 `Uppaal/TChecker` 的关系是对照与补充，而不是封闭孤岛。
3. 当前不主打独立 exchange standard，更像面向 backend integration 的 `C++` library。

## 配套基础设施

- 建模/编辑工具：不是图形建模器，核心是 `C++20` library。
- 解析/交换/元模型支持：region representation、class `Z/P/M/U`、successor / predecessor algorithms。
- 仿真/执行支持：重点是 reachability analysis，而不是运行时执行。
- 验证/分析支持：forward reachability、backward reachability、与 `Uppaal/TChecker` 的性能比较。
- 代码生成/转换支持：不主打部署代码生成，主要做 region-level backend operation。
- 标准化或社区生态：GitHub 仓库、Zenodo artifact、与成熟 zone-based 工具的接口兼容潜力。

## 适用场景与需求前提

### 适用场景

适合 closed `TA`、带 punctual guards 的 `TA`、需要 backward exploration 的安全验证，以及 timed games 这类更依赖前驱运算的后端分析场景。

### 需求前提

1. 系统需已落成 `TA` 或 network of `TA`。
2. 关心的问题最好能下沉成 reachability / safety。
3. 若使用 backward analysis，应接受 region-level backend 而不是只依赖 zones。
4. 如果模型常数很大且 strict guards 占主导，仍需谨慎评估 zone tool 是否更优。

### 不适用或高成本场景

如果需求主要是一般时序逻辑模型检验、统计验证或 hybrid dynamics，`Tarzan` 目前覆盖不够。

## 与相邻形式主义的关系

相对 [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md)，后者偏 `LU` abstraction / symbolic zone backend，`Tarzan` 明确走 region-based route；相对 [timing-analysis-of-asynchronous-circuits-using-timed-automata/desc.md](../timing-analysis-of-asynchronous-circuits-using-timed-automata/desc.md)，那篇是 `TA` 应用桥接，而 `Tarzan` 是后端库；相对 [verified-model-checking-of-timed-automata/desc.md](../verified-model-checking-of-timed-automata/desc.md) 与 [revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md](../revisiting-local-time-semantics-for-networks-of-timed-automata/desc.md)，`Munta` 和 local-zone 路线仍以 zone / verified checking 为主，而 `Tarzan` 把 region-based backward analysis 重新做成了工程基础设施。

## 与本研究的关系

### 对 Project 1 的价值

1. 它为 timed state machine 的后端验证提供了又一条明确可选路线，而不是默认只有 zones。
2. backward predecessor 能力对 `project_2/project_3` 的 property checking 与 profile-based verification 都有潜在价值。
3. ordered unbounded clocks 的结构化表示，也很适合作为 LLM 需要理解的“时间语义骨架”案例。

### 作为目标形式主义还是中间表示

明显更适合作为 timed verification backend，而不是前端目标建模语言。

### 对需求到模型生成的启发

1. 若未来需求生成目标是 `TA`，就要尽早考虑后端究竟更适合 zone 还是 region。
2. punctual guards 和 closed constraints 会显著影响后端选择，这些特征应尽量在需求结构化阶段就被保留下来。
3. 后向分析能力说明 timed 模型不仅要“能模拟”，还要“能从坏状态反推原因”。

## 重要的相关工作

1. `Uppaal`、`TChecker`：论文实验中的主要 zone-based 对照工具。
2. [better-abstractions-for-timed-automata/desc.md](../better-abstractions-for-timed-automata/desc.md)：`LU` abstraction backend 路线。
3. [verified-model-checking-of-timed-automata/desc.md](../verified-model-checking-of-timed-automata/desc.md)：可验证 `DBM` 检查器路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`timed automata / region abstraction / Tarzan`
- 论文角色：region-based timed-automata reachability library / forward-backward backend
- 归类理由：论文主体是 `TA` 的 region-based verification library 与其新 region 表示，核心贡献明显属于 timed backend 基础设施，而不是新的时间自动机本体。
